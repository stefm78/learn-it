#!/usr/bin/env python3
"""Report explicit Constitution neighbor IDs surfaced by maturity scoring V1.1.

Deterministic, non-mutating governance report.

V1.1 hardening:
- no hard-coded scope list;
- compares policy.yaml declared scopes with scoring_report scope_results;
- reports policy/scoring drift without changing policy, decisions, catalog, backlog, scores,
  or scorer rules;
- builds owner and existing-neighbor maps from decisions.yaml dynamically.

Default output:
- docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEFAULT_SCORING_REPORT = Path("docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml")
DEFAULT_POLICY = Path("docs/pipelines/constitution/policies/scope_generation/policy.yaml")
DEFAULT_DECISIONS = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
DEFAULT_BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    if not isinstance(doc, dict):
        raise SystemExit(f"Invalid YAML root in {path}: expected mapping")
    return doc


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().upper())
    return re.sub(r"_+", "_", value).strip("_")


def as_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def policy_scope_keys(policy_doc: Dict[str, Any]) -> List[str]:
    scopes = policy_doc.get("scope_generation_policy", {}).get("declared_scopes", []) or []
    result = []
    for scope in scopes:
        if isinstance(scope, dict) and scope.get("scope_key"):
            result.append(str(scope["scope_key"]))
    return sorted(set(result))


def scoring_scope_keys(scoring_root: Dict[str, Any]) -> List[str]:
    results = scoring_root.get("scope_results", []) or []
    result = []
    for scope_result in results:
        if isinstance(scope_result, dict) and scope_result.get("scope_key"):
            result.append(str(scope_result["scope_key"]))
    return sorted(set(result))


def build_scope_consistency(policy_doc: Dict[str, Any], scoring_root: Dict[str, Any]) -> Dict[str, Any]:
    p_scopes = set(policy_scope_keys(policy_doc))
    s_scopes = set(scoring_scope_keys(scoring_root))
    in_scoring_not_policy = sorted(s_scopes - p_scopes)
    in_policy_not_scoring = sorted(p_scopes - s_scopes)
    status = "PASS" if not in_scoring_not_policy and not in_policy_not_scoring else "REVIEW"
    return {
        "status": status,
        "policy_scope_count": len(p_scopes),
        "scoring_scope_count": len(s_scopes),
        "declared_scope_keys_from_policy": sorted(p_scopes),
        "scope_keys_from_scoring_report": sorted(s_scopes),
        "scopes_in_scoring_not_in_policy": in_scoring_not_policy,
        "scopes_in_policy_not_in_scoring": in_policy_not_scoring,
        "note": (
            "Scope sets match. Candidate extraction can be interpreted against current policy."
            if status == "PASS"
            else "Scope sets differ. Treat candidate extraction as provisional until policy/scoring alignment is reviewed."
        ),
    }


def build_owner_map(decisions_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    owner_map: Dict[str, Dict[str, Any]] = {}
    decisions = decisions_doc.get("scope_generation_decisions", {}).get("decisions", []) or []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        if decision.get("decision_type") != "assign_ids_to_scope":
            continue
        status = str(decision.get("status") or "unknown")
        if status != "approved":
            continue
        scopes = as_list(decision.get("scope_keys_affected"))
        if len(scopes) != 1:
            continue
        scope_key = scopes[0]
        for target_id in as_list(decision.get("target_ids")):
            record = {
                "owner_scope_key": scope_key,
                "decision_id": decision.get("decision_id"),
                "decision_status": status,
            }
            existing = owner_map.get(target_id)
            if existing and existing.get("owner_scope_key") != scope_key:
                record["owner_conflict"] = True
                record["conflicting_owner_scope_key"] = existing.get("owner_scope_key")
                record["conflicting_decision_id"] = existing.get("decision_id")
            owner_map[target_id] = record
    return owner_map


def build_existing_neighbor_map(decisions_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    existing: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"approved": set(), "proposed": set(), "decisions": []})
    decisions = decisions_doc.get("scope_generation_decisions", {}).get("decisions", []) or []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        if decision.get("decision_type") != "force_logical_neighbors":
            continue
        status = str(decision.get("status") or "unknown")
        decision_id = decision.get("decision_id")
        for scope_key in as_list(decision.get("scope_keys_affected")):
            for target_id in as_list(decision.get("target_ids")):
                bucket = "approved" if status == "approved" else "proposed"
                existing[scope_key][bucket].add(target_id)
                existing[scope_key]["decisions"].append({
                    "decision_id": decision_id,
                    "status": status,
                    "target_id": target_id,
                })
    return existing


def open_backlog_by_scope(backlog_doc: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    root = backlog_doc.get("governance_backlog", {})
    entries = root.get("entries", []) if isinstance(root, dict) else []
    result: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    if not isinstance(entries, list):
        return result

    for entry in entries:
        if not isinstance(entry, dict) or entry.get("status") != "open":
            continue
        impacted = set(as_list(entry.get("related_scope_keys")))
        if entry.get("scope_key"):
            impacted.add(str(entry.get("scope_key")))
        for scope in impacted:
            result[scope].append({
                "entry_id": entry.get("entry_id"),
                "type": entry.get("type"),
                "title": entry.get("title"),
                "candidate_id": entry.get("candidate_id"),
            })
    return result


def extract_uncovered_ids(scope_result: Dict[str, Any]) -> List[str]:
    dep_axis = scope_result.get("axis_scores", {}).get("dependency_explicitness", {})
    evidence = dep_axis.get("evidence", [])
    if not isinstance(evidence, list):
        return []

    uncovered: List[str] = []
    for evidence_item in evidence:
        if not isinstance(evidence_item, dict):
            continue
        coverage = evidence_item.get("constitution_neighbor_id_coverage")
        if not isinstance(coverage, dict):
            continue
        uncovered.extend(as_list(coverage.get("uncovered_ids")))
    return sorted(set(uncovered))


def extract_dependency_metrics(scope_result: Dict[str, Any]) -> Dict[str, Any]:
    dep_axis = scope_result.get("axis_scores", {}).get("dependency_explicitness", {})
    evidence = dep_axis.get("evidence", [])
    if not isinstance(evidence, list):
        return {"dependency_axis_score": dep_axis.get("score")}
    for evidence_item in evidence:
        if isinstance(evidence_item, dict) and "outgoing_dependency_count" in evidence_item:
            return {
                "dependency_axis_score": dep_axis.get("score"),
                "outgoing_dependency_count": evidence_item.get("outgoing_dependency_count"),
                "covered_outgoing_dependency_count": evidence_item.get("covered_outgoing_dependency_count"),
                "uncovered_outgoing_dependency_count": evidence_item.get("uncovered_outgoing_dependency_count"),
                "coverage_ratio": evidence_item.get("coverage_ratio"),
            }
    return {"dependency_axis_score": dep_axis.get("score")}


def severity_for_scope(scope_result: Dict[str, Any]) -> str:
    delta = scope_result.get("delta", {}) or {}
    severity = delta.get("severity")
    if severity in {"fail", "warn", "none"}:
        return severity
    if delta.get("action_required"):
        return "warn"
    return "none"


def recommend_decision(
    *,
    scope_key: str,
    target_id: str,
    owner_info: Dict[str, Any] | None,
    existing_neighbors: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    if not owner_info:
        return {
            "recommended_decision": "defer_to_governance_backlog",
            "rationale": "No approved Constitution owner scope was found for this uncovered ID in assign_ids_to_scope decisions.",
            "requires_human_arbitration": True,
        }

    if owner_info.get("owner_conflict"):
        return {
            "recommended_decision": "defer_to_governance_backlog",
            "rationale": "Multiple owner scopes appear to be associated with this ID; resolve ownership before declaring a neighbor.",
            "requires_human_arbitration": True,
        }

    owner_scope = owner_info.get("owner_scope_key")
    if owner_scope == scope_key:
        return {
            "recommended_decision": "wont_fix_with_rationale",
            "rationale": "The uncovered ID appears to be owned by the same scope; this may be an internal edge or scorer evidence issue, not a neighbor declaration.",
            "requires_human_arbitration": True,
        }

    scope_neighbors = existing_neighbors.get(scope_key, {"approved": set(), "proposed": set()})
    if target_id in scope_neighbors.get("approved", set()):
        return {
            "recommended_decision": "wont_fix_with_rationale",
            "rationale": "The ID is already present in an approved force_logical_neighbors decision; investigate scorer or catalog regeneration instead of adding a duplicate.",
            "requires_human_arbitration": True,
        }

    if target_id in scope_neighbors.get("proposed", set()):
        return {
            "recommended_decision": "add_as_default_neighbor",
            "rationale": "The ID is already present in a proposed force_logical_neighbors decision; human arbitration can promote the proposal to approved.",
            "requires_human_arbitration": True,
        }

    return {
        "recommended_decision": "add_as_default_neighbor",
        "rationale": f"ID is owned by {owner_scope} and used by {scope_key}; declare it as an explicit Constitution read neighbor if the dependency is legitimate.",
        "requires_human_arbitration": True,
    }


def collect_scoring_items(scoring_root: Dict[str, Any], field: str) -> List[str]:
    values = []
    for item_group in scoring_root.get(field, []) or []:
        if not isinstance(item_group, dict):
            continue
        for item in item_group.get("items", []) or []:
            if isinstance(item, dict) and item.get("scope_key"):
                values.append(str(item["scope_key"]))
    return sorted(set(values))


def build_report(
    scoring_path: Path,
    policy_path: Path,
    decisions_path: Path,
    backlog_path: Path,
) -> Dict[str, Any]:
    scoring_doc = load_yaml(scoring_path)
    policy_doc = load_yaml(policy_path)
    decisions_doc = load_yaml(decisions_path)
    backlog_doc = load_yaml(backlog_path)

    scoring_root = scoring_doc.get("scope_maturity_scoring_report", {})
    if not isinstance(scoring_root, dict):
        raise SystemExit(f"Missing scope_maturity_scoring_report root in {scoring_path}")

    scope_consistency = build_scope_consistency(policy_doc, scoring_root)
    owner_map = build_owner_map(decisions_doc)
    existing_neighbor_map = build_existing_neighbor_map(decisions_doc)
    backlog_by_scope = open_backlog_by_scope(backlog_doc)

    scope_results = scoring_root.get("scope_results", [])
    if not isinstance(scope_results, list):
        raise SystemExit("scope_maturity_scoring_report.scope_results must be a list")

    candidates: List[Dict[str, Any]] = []
    scope_summaries: List[Dict[str, Any]] = []
    decision_counts: Counter[str] = Counter()
    severity_counts: Counter[str] = Counter()

    for scope_result in scope_results:
        if not isinstance(scope_result, dict):
            continue
        scope_key = str(scope_result.get("scope_key") or "")
        uncovered_ids = extract_uncovered_ids(scope_result)
        severity = severity_for_scope(scope_result)
        severity_counts[severity] += 1

        scope_decision_counts: Counter[str] = Counter()
        for target_id in uncovered_ids:
            owner_info = owner_map.get(target_id)
            recommendation = recommend_decision(
                scope_key=scope_key,
                target_id=target_id,
                owner_info=owner_info,
                existing_neighbors=existing_neighbor_map,
            )
            decision_counts[recommendation["recommended_decision"]] += 1
            scope_decision_counts[recommendation["recommended_decision"]] += 1

            candidates.append({
                "candidate_id": f"NIDG_{slug(scope_key)}__{slug(target_id)}",
                "scope_key": scope_key,
                "uncovered_id": target_id,
                "owner_scope_key": owner_info.get("owner_scope_key") if owner_info else None,
                "owner_decision_id": owner_info.get("decision_id") if owner_info else None,
                "source_signal": {
                    "report": str(scoring_path).replace("\\", "/"),
                    "axis": "dependency_explicitness",
                    "scope_delta_severity": severity,
                    "computed_score_total": scope_result.get("computed_maturity", {}).get("score_total"),
                    "computed_level": scope_result.get("computed_maturity", {}).get("level"),
                    "published_score_total": scope_result.get("published_maturity", {}).get("score_total"),
                    "published_level": scope_result.get("published_maturity", {}).get("level"),
                },
                "recommended_decision": recommendation["recommended_decision"],
                "requires_human_arbitration": recommendation["requires_human_arbitration"],
                "rationale": recommendation["rationale"],
            })

        scope_summaries.append({
            "scope_key": scope_key,
            "scope_delta_severity": severity,
            "published_level": scope_result.get("published_maturity", {}).get("level"),
            "computed_level": scope_result.get("computed_maturity", {}).get("level"),
            "score_delta": scope_result.get("delta", {}).get("score_delta"),
            "dependency_metrics": extract_dependency_metrics(scope_result),
            "uncovered_id_count": len(uncovered_ids),
            "recommended_decision_counts": dict(sorted(scope_decision_counts.items())),
            "related_open_backlog_count": len(backlog_by_scope.get(scope_key, [])),
            "related_open_backlog_entries": backlog_by_scope.get(scope_key, []),
        })

    candidates.sort(key=lambda x: (x["scope_key"], x["uncovered_id"]))

    return {
        "constitution_neighbor_ids_governance_report": {
            "schema_version": "0.2",
            "generated_at": iso_now(),
            "phase": "PHASE_16",
            "status": "READY_FOR_HUMAN_ARBITRATION",
            "authority": "diagnostic_governance_report_only",
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "governance_backlog_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "maturity_scores": "not_modified",
                "scorer_v1_1_rules": "not_modified",
            },
            "inputs": {
                "scoring_report": str(scoring_path).replace("\\", "/"),
                "policy": str(policy_path).replace("\\", "/"),
                "decisions": str(decisions_path).replace("\\", "/"),
                "governance_backlog": str(backlog_path).replace("\\", "/"),
            },
            "policy_scoring_scope_consistency": scope_consistency,
            "summary": {
                "scope_count": len(scope_summaries),
                "candidate_count": len(candidates),
                "candidate_counts_by_recommended_decision": dict(sorted(decision_counts.items())),
                "scope_counts_by_delta_severity": dict(sorted(severity_counts.items())),
                "blocking_scopes_from_scoring": collect_scoring_items(scoring_root, "blocking_findings"),
                "warning_scopes_from_scoring": collect_scoring_items(scoring_root, "warnings"),
            },
            "scope_summaries": scope_summaries,
            "decision_candidates": candidates,
            "next_step": {
                "recommended_action": "human_arbitration",
                "allowed_decisions": [
                    "add_as_default_neighbor",
                    "defer_to_governance_backlog",
                    "wont_fix_with_rationale",
                ],
                "after_arbitration": [
                    "patch policy.yaml / decisions.yaml only for accepted explicit neighbor IDs",
                    "regenerate scope catalog only if policy/decisions change",
                    "rerun scope maturity scoring after regeneration",
                ],
            },
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report Constitution neighbor IDs governance candidates.")
    parser.add_argument("--scoring-report", default=str(DEFAULT_SCORING_REPORT))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--decisions", default=str(DEFAULT_DECISIONS))
    parser.add_argument("--backlog", default=str(DEFAULT_BACKLOG))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(
        scoring_path=Path(args.scoring_report),
        policy_path=Path(args.policy),
        decisions_path=Path(args.decisions),
        backlog_path=Path(args.backlog),
    )
    write_yaml(Path(args.report), report)
    root = report["constitution_neighbor_ids_governance_report"]
    print(f"Wrote {args.report}")
    print(f"Status: {root['status']}")
    print(f"Candidate count: {root['summary']['candidate_count']}")
    print(f"Policy/scoring scope consistency: {root['policy_scoring_scope_consistency']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
