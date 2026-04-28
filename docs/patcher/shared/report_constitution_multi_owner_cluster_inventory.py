#!/usr/bin/env python3
"""Inventory MACRO_004 / PHASE_19 multi-owner cluster candidates.

PHASE_19A deterministic, non-mutating report.

Purpose:
- extract historical review_multi_owner_cluster candidates from Scope Lab;
- reclassify each signal after PHASE_18 clarified that read-neighbor declarations
  are read authority, not ownership authority;
- separate true ownership ambiguity from bridge/read-neighbor/diagnostic/generated-view signals.

Always writes:
  docs/pipelines/constitution/reports/constitution_multi_owner_cluster_inventory_report.yaml
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import yaml


DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_inventory_report.yaml")

CANDIDATES = Path("tmp/scope_lab/scope_redesign_candidates.yaml")
DECISIONS = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
NEIGHBOR_MODEL = Path("docs/specs/constitution_neighbor_declaration_model.md")
NEIGHBOR_INVENTORY = Path("docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml")
GOVERNANCE_BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def stable_list(values: Iterable[Any]) -> List[str]:
    return sorted(set(str(v) for v in values if str(v).strip()))


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}")
    return value


def collect_decision_context(decisions_doc: Dict[str, Any]) -> Dict[str, Any]:
    root = get_root(decisions_doc, "scope_generation_decisions")
    decisions = root.get("decisions") or []

    approved_read_neighbors_by_scope: Dict[str, Set[str]] = defaultdict(set)
    approved_read_neighbor_decisions = []
    diagnostic_subclusters_by_cluster: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        decision_id = str(decision.get("decision_id"))
        status = str(decision.get("status"))
        decision_type = str(decision.get("decision_type"))
        scopes = stable_list(decision.get("scope_keys_affected") or [])
        target_ids = stable_list(decision.get("target_ids") or [])
        payload = decision.get("decision_payload") or {}

        if decision_type == "force_logical_neighbors" and status == "approved":
            entry = {
                "decision_id": decision_id,
                "scope_keys_affected": scopes,
                "target_ids": target_ids,
                "neighbor_class": payload.get("neighbor_class") if isinstance(payload, dict) else None,
                "source_phase": payload.get("source_phase") if isinstance(payload, dict) else None,
            }
            approved_read_neighbor_decisions.append(entry)
            for scope in scopes:
                approved_read_neighbors_by_scope[scope].update(target_ids)

        if decision_type == "record_diagnostic_subcluster" and status == "approved":
            cluster_ids = stable_list(payload.get("source_cluster_ids") or []) if isinstance(payload, dict) else []
            for cluster_id in cluster_ids:
                diagnostic_subclusters_by_cluster[cluster_id].append({
                    "decision_id": decision_id,
                    "scope_keys_affected": scopes,
                    "target_ids": target_ids,
                    "subcluster_key": payload.get("subcluster_key") if isinstance(payload, dict) else None,
                    "ownership_effect": payload.get("ownership_effect") if isinstance(payload, dict) else None,
                })

    return {
        "approved_read_neighbors_by_scope": {scope: sorted(ids) for scope, ids in approved_read_neighbors_by_scope.items()},
        "approved_read_neighbor_decisions": sorted(approved_read_neighbor_decisions, key=lambda x: x["decision_id"]),
        "diagnostic_subclusters_by_cluster": {
            cluster_id: sorted(entries, key=lambda x: x["decision_id"])
            for cluster_id, entries in diagnostic_subclusters_by_cluster.items()
        },
    }


def collect_open_governance_backlog_ids(backlog_doc: Dict[str, Any]) -> Dict[str, Any]:
    if not backlog_doc:
        return {"open_entry_count": 0, "entries_by_scope": {}}

    # The backlog schema evolved. Keep this tolerant and non-blocking.
    entries = []
    for key in ["governance_backlog", "backlog", "entries"]:
        value = backlog_doc.get(key) if isinstance(backlog_doc, dict) else None
        if isinstance(value, dict) and isinstance(value.get("entries"), list):
            entries = value.get("entries")
            break
        if isinstance(value, list):
            entries = value
            break

    by_scope: Dict[str, List[str]] = defaultdict(list)
    open_count = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        status = str(entry.get("status", "open"))
        if status != "open":
            continue
        open_count += 1
        entry_id = str(entry.get("entry_id") or entry.get("id") or "unknown")
        scopes = entry.get("scope_keys") or entry.get("affected_scope_keys") or entry.get("related_scope_keys") or []
        for scope in stable_list(scopes):
            by_scope[scope].append(entry_id)

    return {
        "open_entry_count": open_count,
        "entries_by_scope": {scope: sorted(ids) for scope, ids in by_scope.items()},
    }


def candidate_cluster_id(candidate: Dict[str, Any]) -> str:
    clusters = candidate.get("affected_cluster_ids") or []
    return str(clusters[0]) if clusters else "UNKNOWN_CLUSTER"


def classify_candidate(
    candidate: Dict[str, Any],
    decision_context: Dict[str, Any],
    backlog_context: Dict[str, Any],
) -> Dict[str, Any]:
    cluster_id = candidate_cluster_id(candidate)
    source = candidate.get("source_signals") or {}
    affected_node_ids = stable_list(candidate.get("affected_node_ids") or [])
    affected_scopes = stable_list(candidate.get("affected_scope_keys") or [])
    nodes_by_owner = source.get("nodes_by_owner_scope") or {}
    boundary_pressure = str(source.get("boundary_pressure") or "unknown")

    owner_counts = {
        str(scope): int(count)
        for scope, count in nodes_by_owner.items()
        if isinstance(count, int)
    }
    total_nodes = sum(owner_counts.values())
    unowned_count = owner_counts.get("UNOWNED", 0)
    owned_counts = {scope: count for scope, count in owner_counts.items() if scope != "UNOWNED"}
    owner_scope_count = len(owned_counts)
    dominant_scope = None
    dominant_count = 0
    if owned_counts:
        dominant_scope, dominant_count = max(owned_counts.items(), key=lambda item: item[1])
    dominance_ratio = round(dominant_count / total_nodes, 4) if total_nodes else 0

    approved_neighbors_by_scope = decision_context["approved_read_neighbors_by_scope"]
    diagnostic_subclusters = decision_context["diagnostic_subclusters_by_cluster"].get(cluster_id, [])

    approved_read_neighbor_hits_by_scope = {}
    all_read_neighbor_hits: Set[str] = set()
    for scope in affected_scopes:
        hits = sorted(set(affected_node_ids) & set(approved_neighbors_by_scope.get(scope, [])))
        if hits:
            approved_read_neighbor_hits_by_scope[scope] = hits
            all_read_neighbor_hits.update(hits)

    diagnostic_covered_ids: Set[str] = set()
    for entry in diagnostic_subclusters:
        diagnostic_covered_ids.update(entry.get("target_ids") or [])
    diagnostic_hits = sorted(set(affected_node_ids) & diagnostic_covered_ids)

    classification_tags = []
    evidence = []

    if diagnostic_subclusters:
        classification_tags.append("diagnostic_subcluster")
        evidence.append(f"{cluster_id} is referenced by approved record_diagnostic_subcluster decision(s).")

    if approved_read_neighbor_hits_by_scope:
        classification_tags.append("read_neighbor_relation")
        evidence.append("Some affected IDs are already governed as explicit read-neighbors; this is not ownership transfer.")

    if unowned_count > 0:
        classification_tags.append("bridge_edge")
        evidence.append("Cluster includes UNOWNED/external material; this should be treated as bridge or external-read signal before ownership changes.")

    if boundary_pressure == "high":
        classification_tags.append("true_ownership_ambiguity")
        evidence.append("Boundary pressure is high and requires human ownership arbitration.")
    elif owner_scope_count >= 3 and dominance_ratio < 0.65:
        classification_tags.append("true_ownership_ambiguity")
        evidence.append("Cluster spans at least three owned scopes with no dominant owner above 65%.")
    elif owner_scope_count >= 2 and not approved_read_neighbor_hits_by_scope and not diagnostic_subclusters:
        classification_tags.append("true_ownership_ambiguity")
        evidence.append("Cluster spans multiple owned scopes and is not already covered by read-neighbor or diagnostic-subcluster governance.")

    # Generated-view artifact is not expected here, but keep the explicit category from PHASE_19 plan.
    if not classification_tags:
        classification_tags.append("generated_view_artifact")
        evidence.append("No direct ownership action signal remains after PHASE_18 filters; retain for traceability only.")

    # Recommended routing after filtering.
    if "true_ownership_ambiguity" in classification_tags:
        recommended_next_action = "human_arbitration_required"
    elif "diagnostic_subcluster" in classification_tags and "read_neighbor_relation" in classification_tags:
        recommended_next_action = "likely_keep_current_ownership_with_existing_governance"
    elif "read_neighbor_relation" in classification_tags:
        recommended_next_action = "likely_keep_current_ownership_with_explicit_neighbors"
    elif "diagnostic_subcluster" in classification_tags:
        recommended_next_action = "likely_keep_current_ownership_as_diagnostic_subcluster"
    else:
        recommended_next_action = "defer_or_keep_for_traceability"

    open_backlog_refs = []
    entries_by_scope = backlog_context.get("entries_by_scope", {})
    for scope in affected_scopes:
        open_backlog_refs.extend(entries_by_scope.get(scope, []))

    return {
        "candidate_id": candidate.get("candidate_id"),
        "cluster_id": cluster_id,
        "title": candidate.get("title"),
        "priority": candidate.get("priority"),
        "affected_scope_keys": affected_scopes,
        "affected_node_count": len(affected_node_ids),
        "boundary_pressure": boundary_pressure,
        "owner_scope_count": owner_scope_count,
        "nodes_by_owner_scope": owner_counts,
        "dominant_scope": dominant_scope,
        "dominance_ratio": dominance_ratio,
        "unowned_count": unowned_count,
        "classification_tags": sorted(set(classification_tags)),
        "primary_classification": (
            "true_ownership_ambiguity"
            if "true_ownership_ambiguity" in classification_tags
            else "diagnostic_subcluster"
            if "diagnostic_subcluster" in classification_tags
            else "read_neighbor_relation"
            if "read_neighbor_relation" in classification_tags
            else classification_tags[0]
        ),
        "approved_read_neighbor_hits_by_scope": approved_read_neighbor_hits_by_scope,
        "approved_read_neighbor_hit_count": len(all_read_neighbor_hits),
        "diagnostic_subcluster_decisions": diagnostic_subclusters,
        "diagnostic_subcluster_hit_count": len(diagnostic_hits),
        "open_governance_backlog_refs_for_affected_scopes": sorted(set(open_backlog_refs)),
        "evidence": evidence,
        "recommended_next_action": recommended_next_action,
        "arbitration_options": [
            "keep_current_ownership",
            "record_or_keep_diagnostic_subcluster",
            "declare_or_keep_read_neighbors",
            "move_node_ownership",
            "split_scope",
            "merge_scope_fragments",
            "open_or_update_governance_backlog",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory MACRO_004 multi-owner cluster candidates.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    required = [CANDIDATES, DECISIONS, NEIGHBOR_MODEL, NEIGHBOR_INVENTORY]
    for path in required:
        sha256_file(path)

    candidate_doc = load_yaml(CANDIDATES)
    decisions_doc = load_yaml(DECISIONS)
    neighbor_inventory_doc = load_yaml(NEIGHBOR_INVENTORY)
    backlog_doc = load_yaml(GOVERNANCE_BACKLOG) if GOVERNANCE_BACKLOG.exists() else {}

    candidate_root = get_root(candidate_doc, "scope_redesign_candidates")
    candidates = [
        item for item in candidate_root.get("candidates", [])
        if isinstance(item, dict) and item.get("candidate_type") == "review_multi_owner_cluster"
    ]

    decision_context = collect_decision_context(decisions_doc)
    backlog_context = collect_open_governance_backlog_ids(backlog_doc)

    inventory = [
        classify_candidate(candidate, decision_context, backlog_context)
        for candidate in candidates
    ]

    primary_counts = Counter(item["primary_classification"] for item in inventory)
    tag_counts = Counter(tag for item in inventory for tag in item["classification_tags"])
    next_action_counts = Counter(item["recommended_next_action"] for item in inventory)
    pressure_counts = Counter(item["boundary_pressure"] for item in inventory)

    # This is an inventory, not a blocking validator. PASS means the report was produced
    # and PHASE_18 prerequisites are clean.
    neighbor_inventory_root = get_root(neighbor_inventory_doc, "constitution_neighbor_declaration_inventory_report")
    findings = []
    if neighbor_inventory_root.get("status") != "PASS":
        findings.append({
            "finding_id": "NEIGHBOR_DECLARATION_INVENTORY_NOT_PASS",
            "severity": "error",
            "message": "PHASE_19A requires PHASE_18 inventory to be PASS before multi-owner review.",
        })
    if not candidates:
        findings.append({
            "finding_id": "NO_MULTI_OWNER_CANDIDATES",
            "severity": "warning",
            "message": "No review_multi_owner_cluster candidates found in scope_redesign_candidates.yaml.",
        })

    severity_counts = Counter(finding["severity"] for finding in findings)
    status = "FAIL" if severity_counts.get("error", 0) else "WARN" if severity_counts.get("warning", 0) else "PASS"

    report = {
        "constitution_multi_owner_cluster_inventory_report": {
            "schema_version": "0.1",
            "phase_id": "PHASE_19A",
            "generated_at": iso_now(),
            "status": status,
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "scope_lab_reports": "not_modified",
                "cores": "not_modified",
            },
            "doctrine_refs": [
                "docs/specs/constitution_neighbor_declaration_model.md",
                "docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml",
            ],
            "inputs": [
                {"ref": normalize_path(path), "sha256": sha256_file(path)}
                for path in required
            ],
            "summary": {
                "candidate_count": len(inventory),
                "primary_classification_counts": dict(sorted(primary_counts.items())),
                "classification_tag_counts": dict(sorted(tag_counts.items())),
                "recommended_next_action_counts": dict(sorted(next_action_counts.items())),
                "boundary_pressure_counts": dict(sorted(pressure_counts.items())),
                "human_arbitration_required_count": next_action_counts.get("human_arbitration_required", 0),
                "finding_count": len(findings),
                "warning_count": severity_counts.get("warning", 0),
                "error_count": severity_counts.get("error", 0),
            },
            "classification_rules": {
                "true_ownership_ambiguity": [
                    "boundary_pressure is high",
                    "or cluster spans at least three owned scopes without a dominant owner above 65%",
                    "or cluster spans multiple owned scopes and is not already covered by read-neighbor or diagnostic-subcluster governance",
                ],
                "read_neighbor_relation": [
                    "one or more affected IDs are already governed by approved force_logical_neighbors decisions",
                    "read-neighbor declarations do not transfer ownership",
                ],
                "diagnostic_subcluster": [
                    "cluster is referenced by approved record_diagnostic_subcluster decisions",
                    "diagnostic subclusters do not transfer ownership",
                ],
                "bridge_edge": [
                    "cluster includes UNOWNED/external material",
                    "external or bridge material must be classified before ownership changes",
                ],
                "generated_view_artifact": [
                    "fallback category for traceability when no ownership action signal remains",
                ],
            },
            "decision_context": {
                "approved_read_neighbor_decision_count": len(decision_context["approved_read_neighbor_decisions"]),
                "diagnostic_subcluster_cluster_count": len(decision_context["diagnostic_subclusters_by_cluster"]),
                "open_governance_backlog_count": backlog_context.get("open_entry_count", 0),
            },
            "candidates": inventory,
            "findings": findings,
            "recommended_next_steps": [
                "Use this report as PHASE_19B human arbitration input.",
                "Start arbitration with candidates whose primary_classification is true_ownership_ambiguity.",
                "Do not move ownership for candidates classified only as read_neighbor_relation or diagnostic_subcluster without a separate explicit human decision.",
                "If an ownership change is accepted, apply it later through policy/decisions patching, then regenerate the scope catalog and rerun validators.",
            ],
        }
    }

    write_yaml(Path(args.report), report)
    print(f"Wrote {args.report}")
    print(f"Status: {status}")
    print(f"Multi-owner candidates: {len(inventory)}")
    print(f"Human arbitration required: {next_action_counts.get('human_arbitration_required', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
