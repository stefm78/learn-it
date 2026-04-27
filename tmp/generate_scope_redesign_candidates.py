#!/usr/bin/env python3
"""Generate scope redesign candidates from Scope Lab reports.

PHASE_07 — redesign_candidates

Reads:
  - tmp/scope_lab/scope_alignment_report.yaml
  - tmp/scope_lab/cluster_closure_report.yaml

Writes:
  - tmp/scope_lab/scope_redesign_candidates.yaml

Purpose:
  Convert graph/cluster/scope alignment findings into explicit candidates
  for human arbitration.

This script is diagnostic only.
It does not modify canonical cores, policies, decisions, or scope catalog.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )


def stable_candidate_id(prefix: str, index: int) -> str:
    return f"{prefix}_{index:03d}"


def priority_from_signals(
    owner_status: str | None = None,
    boundary_pressure: str | None = None,
    recommendation: str | None = None,
) -> str:
    if owner_status == "multi_owner_fragmented":
        return "high"
    if boundary_pressure == "high":
        return "high"
    if recommendation in {
        "review_split_merge_or_bridge",
        "classify_unowned_core_area",
    }:
        return "high"
    if boundary_pressure == "medium":
        return "medium"
    if recommendation == "declare_or_review_neighbors":
        return "medium"
    return "low"


def unique_sorted(values: list[Any]) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def candidate_scope_boundary_review(index: int, scope_report: dict[str, Any]) -> dict[str, Any]:
    scope_key = scope_report.get("scope_key")
    findings = scope_report.get("findings", []) or []

    return {
        "candidate_id": stable_candidate_id("CAND_SCOPE_BOUNDARY", index),
        "candidate_type": "review_scope_boundary",
        "priority": "high",
        "status": "proposed",
        "title": f"Review graph boundary alignment for scope {scope_key}",
        "affected_scope_keys": [scope_key],
        "affected_cluster_ids": [
            view.get("cluster_id")
            for view in scope_report.get("cluster_views", []) or []
            if view.get("cluster_id")
        ],
        "affected_node_ids": [],
        "source_signals": {
            "alignment_status": scope_report.get("alignment_status"),
            "owned_node_count": scope_report.get("owned_node_count"),
            "selected_cluster_touch_count": scope_report.get("selected_cluster_touch_count"),
            "findings": findings,
        },
        "rationale": (
            "The current scope ownership is distributed across graph clusters "
            "that show split, merge, bridge, neighbor, or unowned-area signals."
        ),
        "recommended_arbitration_options": [
            "keep_scope_with_explicit_neighbors",
            "split_scope",
            "merge_with_related_scope",
            "move_selected_nodes",
            "create_bridge_or_shared_classification",
            "defer_to_backlog",
        ],
    }


def candidate_multi_owner_cluster(index: int, cluster: dict[str, Any]) -> dict[str, Any]:
    cluster_id = cluster.get("cluster_id")
    nodes_by_owner = cluster.get("nodes_by_owner_scope", {}) or {}

    return {
        "candidate_id": stable_candidate_id("CAND_MULTI_OWNER_CLUSTER", index),
        "candidate_type": "review_multi_owner_cluster",
        "priority": priority_from_signals(
            owner_status=cluster.get("owner_status"),
            boundary_pressure=cluster.get("boundary_pressure"),
            recommendation=cluster.get("recommendation"),
        ),
        "status": "proposed",
        "title": f"Review multi-owner cluster {cluster_id}",
        "affected_scope_keys": sorted(
            scope for scope in nodes_by_owner
            if scope != "UNOWNED"
        ),
        "affected_cluster_ids": [cluster_id],
        "affected_node_ids": cluster.get("node_ids", []) or [],
        "source_signals": {
            "owner_status": cluster.get("owner_status"),
            "boundary_pressure": cluster.get("boundary_pressure"),
            "recommendation": cluster.get("recommendation"),
            "nodes_by_owner_scope": nodes_by_owner,
            "candidate_neighbor_scopes": cluster.get("candidate_neighbor_scopes", []) or [],
        },
        "rationale": (
            "This cluster contains nodes owned by multiple current scopes. "
            "It may indicate an artificial boundary, a bridge area, or a need "
            "for explicit neighbor declarations."
        ),
        "recommended_arbitration_options": [
            "split_cluster_by_existing_owners",
            "merge_scope_fragments",
            "declare_bridge_area",
            "move_node_ownership",
            "declare_neighbors",
            "defer_to_backlog",
        ],
    }


def candidate_unowned_cluster(index: int, cluster: dict[str, Any]) -> dict[str, Any]:
    cluster_id = cluster.get("cluster_id")

    return {
        "candidate_id": stable_candidate_id("CAND_UNOWNED_AREA", index),
        "candidate_type": "classify_unowned_core_area",
        "priority": priority_from_signals(
            owner_status=cluster.get("owner_status"),
            boundary_pressure=cluster.get("boundary_pressure"),
            recommendation=cluster.get("recommendation"),
        ),
        "status": "proposed",
        "title": f"Classify unowned core area {cluster_id}",
        "affected_scope_keys": [],
        "affected_cluster_ids": [cluster_id],
        "affected_node_ids": cluster.get("node_ids", []) or [],
        "source_signals": {
            "owner_status": cluster.get("owner_status"),
            "boundary_pressure": cluster.get("boundary_pressure"),
            "recommendation": cluster.get("recommendation"),
            "nodes_by_core": cluster.get("nodes_by_core", {}) or {},
            "nodes_by_section": cluster.get("nodes_by_section", {}) or {},
            "candidate_neighbor_scopes": cluster.get("candidate_neighbor_scopes", []) or [],
        },
        "rationale": (
            "This cluster is fully UNOWNED in the current scope model. "
            "It likely corresponds to referentiel/link or shared cross-core material "
            "that must be classified before ownership bijection can pass."
        ),
        "recommended_arbitration_options": [
            "assign_to_existing_scope",
            "create_new_scope",
            "declare_shared_or_global",
            "declare_read_only_referentiel_area",
            "exclude_from_constitution_scope_bijection_with_policy",
            "defer_to_backlog",
        ],
    }


def candidate_neighbor_review(index: int, cluster: dict[str, Any]) -> dict[str, Any]:
    cluster_id = cluster.get("cluster_id")
    neighbor_scopes = cluster.get("candidate_neighbor_scopes", []) or []

    return {
        "candidate_id": stable_candidate_id("CAND_NEIGHBOR_REVIEW", index),
        "candidate_type": "declare_or_review_neighbors",
        "priority": priority_from_signals(
            owner_status=cluster.get("owner_status"),
            boundary_pressure=cluster.get("boundary_pressure"),
            recommendation=cluster.get("recommendation"),
        ),
        "status": "proposed",
        "title": f"Review neighbor declarations for cluster {cluster_id}",
        "affected_scope_keys": unique_sorted(neighbor_scopes),
        "affected_cluster_ids": [cluster_id],
        "affected_node_ids": cluster.get("candidate_neighbor_ids", []) or [],
        "source_signals": {
            "owner_status": cluster.get("owner_status"),
            "boundary_pressure": cluster.get("boundary_pressure"),
            "recommendation": cluster.get("recommendation"),
            "candidate_neighbor_ids": cluster.get("candidate_neighbor_ids", []) or [],
            "candidate_neighbor_scopes": neighbor_scopes,
            "incoming_edge_count": cluster.get("incoming_edge_count"),
            "outgoing_edge_count": cluster.get("outgoing_edge_count"),
        },
        "rationale": (
            "The cluster has external dependency pressure. "
            "The likely safe action is not necessarily to move ownership, "
            "but to declare explicit read neighbors where appropriate."
        ),
        "recommended_arbitration_options": [
            "declare_neighbor_ids",
            "declare_neighbor_scope",
            "move_ownership_if_boundary_is_wrong",
            "create_bridge_if_dependency_is_structural",
            "defer_to_backlog",
        ],
    }


def candidate_patch_lifecycle_focus(index: int, scope_report: dict[str, Any]) -> list[dict[str, Any]]:
    """Create explicit candidates for the known patch_lifecycle stress-test."""
    if scope_report.get("scope_key") != "patch_lifecycle":
        return []

    candidates: list[dict[str, Any]] = []
    views = scope_report.get("cluster_views", []) or []

    strong_core = [
        view for view in views
        if view.get("scope_owned_ratio_in_cluster", 0) >= 0.8
    ]

    fragmented = [
        view for view in views
        if view.get("owner_status") == "multi_owner_fragmented"
    ]

    if strong_core:
        candidates.append(
            {
                "candidate_id": stable_candidate_id("CAND_PATCH_LIFECYCLE", index),
                "candidate_type": "keep_patch_core_with_subcluster",
                "priority": "medium",
                "status": "proposed",
                "title": "Keep patch lifecycle structural core as a coherent subcluster",
                "affected_scope_keys": ["patch_lifecycle"],
                "affected_cluster_ids": [view.get("cluster_id") for view in strong_core],
                "affected_node_ids": sorted(
                    node_id
                    for view in strong_core
                    for node_id in (view.get("owned_node_ids", []) or [])
                ),
                "source_signals": {
                    "strong_core_clusters": [
                        {
                            "cluster_id": view.get("cluster_id"),
                            "scope_owned_ratio_in_cluster": view.get("scope_owned_ratio_in_cluster"),
                            "owner_status": view.get("owner_status"),
                            "boundary_pressure": view.get("boundary_pressure"),
                        }
                        for view in strong_core
                    ]
                },
                "rationale": (
                    "Patch lifecycle contains a strong structural core around patch artifact, "
                    "impact scope, quality gate, rollback, and validation. This may remain "
                    "a canonical scope or become a named subcluster."
                ),
                "recommended_arbitration_options": [
                    "keep_in_patch_lifecycle",
                    "name_as_patch_structure_subcluster",
                    "split_as_patch_core_scope",
                    "declare_neighbors_for_unowned_reference",
                ],
            }
        )

    if fragmented:
        candidates.append(
            {
                "candidate_id": stable_candidate_id("CAND_PATCH_LIFECYCLE", index + 1),
                "candidate_type": "review_patch_trigger_boundary",
                "priority": "high",
                "status": "proposed",
                "title": "Review patch trigger boundary with learner_state and runtime signals",
                "affected_scope_keys": ["patch_lifecycle"],
                "affected_cluster_ids": [view.get("cluster_id") for view in fragmented],
                "affected_node_ids": sorted(
                    node_id
                    for view in fragmented
                    for node_id in (view.get("owned_node_ids", []) or [])
                ),
                "source_signals": {
                    "fragmented_clusters": [
                        {
                            "cluster_id": view.get("cluster_id"),
                            "scope_owned_ratio_in_cluster": view.get("scope_owned_ratio_in_cluster"),
                            "nodes_by_owner_scope": view.get("nodes_by_owner_scope", {}),
                            "candidate_neighbor_scopes": view.get("candidate_neighbor_scopes", []),
                        }
                        for view in fragmented
                    ]
                },
                "rationale": (
                    "Patch trigger nodes are graph-close to learner_state and other runtime signals. "
                    "This suggests either stronger neighbor declarations, a bridge treatment, "
                    "or a split between patch structure and patch triggers."
                ),
                "recommended_arbitration_options": [
                    "keep_triggers_in_patch_lifecycle_with_neighbors",
                    "move_triggers_to_learner_state",
                    "create_patch_trigger_bridge",
                    "split_patch_lifecycle",
                    "defer_to_backlog",
                ],
            }
        )

    return candidates


def load_reports(
    alignment_path: Path,
    closure_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    alignment_doc = load_yaml(alignment_path)
    closure_doc = load_yaml(closure_path)

    alignment = alignment_doc.get("scope_alignment_report", {})
    closure = closure_doc.get("cluster_closure_report", {})

    return alignment, closure


def generate_candidates(alignment: dict[str, Any], closure: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []

    scope_reports = alignment.get("scope_reports", []) or []
    closure_clusters = closure.get("clusters", []) or []

    index = 1
    for scope_report in scope_reports:
        if scope_report.get("alignment_status") != "stable_or_minor_review":
            candidates.append(candidate_scope_boundary_review(index, scope_report))
            index += 1

    for cluster in closure_clusters:
        if cluster.get("owner_status") == "multi_owner_fragmented":
            candidates.append(candidate_multi_owner_cluster(index, cluster))
            index += 1

    for cluster in closure_clusters:
        if cluster.get("owner_status") == "fully_unowned":
            candidates.append(candidate_unowned_cluster(index, cluster))
            index += 1

    for cluster in closure_clusters:
        if cluster.get("recommendation") == "declare_or_review_neighbors":
            candidates.append(candidate_neighbor_review(index, cluster))
            index += 1

    for scope_report in scope_reports:
        patch_candidates = candidate_patch_lifecycle_focus(index, scope_report)
        candidates.extend(patch_candidates)
        index += len(patch_candidates)

    return candidates


def summarize(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    type_counts = Counter(candidate["candidate_type"] for candidate in candidates)
    priority_counts = Counter(candidate["priority"] for candidate in candidates)
    scope_counts: Counter[str] = Counter()

    for candidate in candidates:
        for scope in candidate.get("affected_scope_keys", []) or []:
            scope_counts[scope] += 1

    return {
        "candidate_count": len(candidates),
        "candidate_type_counts": dict(sorted(type_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "affected_scope_counts": dict(sorted(scope_counts.items())),
    }


def build_artifact(alignment: dict[str, Any], closure: dict[str, Any]) -> dict[str, Any]:
    candidates = generate_candidates(alignment, closure)
    summary = summarize(candidates)

    return {
        "scope_redesign_candidates": {
            "schema_version": 0.1,
            "status": "PASS",
            "source_reports": [
                "tmp/scope_lab/scope_alignment_report.yaml",
                "tmp/scope_lab/cluster_closure_report.yaml",
            ],
            "summary": summary,
            "candidates": candidates,
            "arbitration_contract": {
                "allowed_status_values": [
                    "proposed",
                    "accepted",
                    "rejected",
                    "deferred",
                    "backlog",
                ],
                "required_human_decision_fields": [
                    "arbitration_status",
                    "arbitration_rationale",
                    "canonicalization_action",
                ],
                "notes": [
                    "Candidates are not canonical decisions.",
                    "Accepted candidates must be converted into core patches and/or scope_generation decisions.",
                    "The scope catalog must only be updated by deterministic regeneration.",
                ],
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate scope redesign candidates.")
    parser.add_argument("--alignment", default="tmp/scope_lab/scope_alignment_report.yaml")
    parser.add_argument("--closure", default="tmp/scope_lab/cluster_closure_report.yaml")
    parser.add_argument("--out", default="tmp/scope_lab/scope_redesign_candidates.yaml")
    args = parser.parse_args()

    alignment, closure = load_reports(
        alignment_path=Path(args.alignment),
        closure_path=Path(args.closure),
    )

    artifact = build_artifact(alignment, closure)
    Path(args.out).write_text(dump_yaml(artifact), encoding="utf-8")

    print(json.dumps(artifact["scope_redesign_candidates"]["summary"], indent=2, ensure_ascii=False))
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
