#!/usr/bin/env python3
"""Report explicit Constitution neighbor IDs surfaced by maturity scoring V1.1.

This is a deterministic, non-mutating governance report.

It reads:
- docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
- docs/pipelines/constitution/policies/scope_generation/policy.yaml
- docs/pipelines/constitution/policies/scope_generation/decisions.yaml
- docs/pipelines/constitution/scope_catalog/governance_backlog.yaml

It writes only the requested report path.

Default output:
- docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

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


def build_owner_map(decisions_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    owner_map: Dict[str, Dict[str, Any]] = {}
    decisions = decisions_doc.get("scope_generation_decisions", {}).get("decisions", []) or []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        if decision.get("decision_type") != "assign_ids_to_scope":
            continue
        status = decision.get("status")
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
            "rationale": "No Constitution owner scope was found for this uncovered ID in approved assign_ids_to_scope decisions.",
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


def build_report(
    scoring_path: Path,
    policy_path: Path,
    decisions_path: Path,
    backlog_path: Path,
) -> Dict[str, Any]:
    scoring_doc = load_yaml(scoring_path)
    # Policy is loaded to bind the report to the published authority even though this
    # V1 report does not need fields beyond its presence and fingerprint in git.
    _policy_doc = load_yaml(policy_path)
    decisions_doc = load_yaml(decisions_path)
    backlog_doc = load_yaml(backlog_path)

    scoring_root = scoring_doc.get("scope_maturity_scoring_report", {})
    if not isinstance(scoring_root, dict):
        raise SystemExit(f"Missing scope_maturity_scoring_report root in {scoring_path}")

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

    blocking_scopes = []
    for finding in scoring_root.get("blocking_findings", []) or []:
        if not isinstance(finding, dict):
            continue
        for item in finding.get("items", []) or []:
            if isinstance(item, dict) and item.get("scope_key"):
                blocking_scopes.append(item.get("scope_key"))

    warning_scopes = []
    for warning in scoring_root.get("warnings", []) or []:
        if not isinstance(warning, dict):
            continue
        for item in warning.get("items", []) or []:
            if isinstance(item, dict) and item.get("scope_key"):
                warning_scopes.append(item.get("scope_key"))

    return {
        "constitution_neighbor_ids_governance_report": {
            "schema_version": "0.1",
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
            "summary": {
                "scope_count": len(scope_summaries),
                "candidate_count": len(candidates),
                "candidate_counts_by_recommended_decision": dict(sorted(decision_counts.items())),
                "scope_counts_by_delta_severity": dict(sorted(severity_counts.items())),
                "blocking_scopes_from_scoring": sorted(set(blocking_scopes)),
                "warning_scopes_from_scoring": sorted(set(warning_scopes)),
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
