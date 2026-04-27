#!/usr/bin/env python3
"""Generate a human arbitration scaffold from scope redesign candidates.

PHASE_08 — human_arbitration

Reads:
  - tmp/scope_lab/scope_redesign_candidates.yaml

Writes:
  - tmp/scope_lab/scope_redesign_arbitration.yaml
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


MACRO_DEFINITIONS = {
    "MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION": {
        "title": "Classify currently UNOWNED referentiel/link areas",
        "priority": "high",
        "problem_statement": (
            "A large part of the graph belongs to referentiel/link and is currently UNOWNED by the "
            "constitution scope catalog. Ownership bijection cannot pass until these areas are explicitly classified."
        ),
        "default_recommendation": (
            "Do not force all referentiel/link IDs into the existing constitution scopes. Introduce an explicit "
            "classification policy: referentiel-owned/read-only, link-owned/read-only, shared/global, or assigned "
            "to an existing scope only when there is true governance ownership."
        ),
        "human_arbitration_options": [
            "declare_referentiel_and_link_as_read_only_external_cores",
            "create_separate_referentiel_link_scope_family",
            "assign_selected_referentiel_link_clusters_to_existing_scopes",
            "declare_shared_or_global_ids",
            "defer_to_backlog",
        ],
    },
    "MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE": {
        "title": "Decide whether patch lifecycle structural core remains a canonical scope/subcluster",
        "priority": "medium",
        "problem_statement": (
            "The graph identifies a strong patch_lifecycle structural core around patch artifact, impact scope, "
            "quality gate, rollback, and validation."
        ),
        "default_recommendation": (
            "Keep the structural patch core in patch_lifecycle for now, and name it explicitly as a diagnostic "
            "subcluster. Do not split it before deciding the trigger boundary."
        ),
        "human_arbitration_options": [
            "keep_in_patch_lifecycle",
            "name_as_patch_structure_subcluster",
            "split_as_patch_core_scope",
            "defer_to_backlog",
        ],
    },
    "MACRO_003_PATCH_TRIGGER_BOUNDARY": {
        "title": "Decide boundary for patch triggers and learner/runtime signals",
        "priority": "high",
        "problem_statement": (
            "Patch trigger nodes are graph-close to learner_state and runtime signals. This is the main stress-test "
            "for the current patch_lifecycle scope."
        ),
        "default_recommendation": (
            "Do not move trigger nodes immediately. Keep them in patch_lifecycle if they represent governed patch "
            "decisions, but declare learner_state/runtime inputs as explicit neighbors. If the boundary remains "
            "ambiguous, create a bridge treatment for patch_trigger_governance."
        ),
        "human_arbitration_options": [
            "keep_triggers_in_patch_lifecycle_with_neighbors",
            "move_triggers_to_learner_state",
            "create_patch_trigger_bridge",
            "split_patch_lifecycle",
            "defer_to_backlog",
        ],
    },
    "MACRO_004_MULTI_OWNER_CLUSTER_REVIEW": {
        "title": "Review multi-owner graph clusters",
        "priority": "high",
        "problem_statement": (
            "Some graph clusters contain nodes owned by several current scopes. These clusters may indicate bridge "
            "areas, bad boundaries, or missing neighbor declarations."
        ),
        "default_recommendation": (
            "Do not merge scopes globally. Review each multi-owner cluster and prefer explicit neighbors or bridge "
            "classification before moving ownership."
        ),
        "human_arbitration_options": [
            "split_clusters_by_existing_owners",
            "declare_bridge_areas",
            "move_selected_node_ownership",
            "declare_neighbors_only",
            "defer_to_backlog",
        ],
    },
    "MACRO_005_NEIGHBOR_DECLARATION_REVIEW": {
        "title": "Review explicit neighbor declarations",
        "priority": "medium",
        "problem_statement": (
            "Several clusters show external dependency pressure. Most of these dependencies should probably become "
            "explicit read neighbors rather than ownership moves."
        ),
        "default_recommendation": (
            "Convert stable external dependencies into force_logical_neighbors decisions where appropriate."
        ),
        "human_arbitration_options": [
            "declare_neighbor_ids",
            "declare_neighbor_scope",
            "move_ownership_if_boundary_is_wrong",
            "create_bridge_if_dependency_is_structural",
            "defer_to_backlog",
        ],
    },
    "MACRO_006_SCOPE_BOUNDARY_REVIEW": {
        "title": "Review all existing scope boundaries",
        "priority": "high",
        "problem_statement": (
            "All five current scopes are marked as split_merge_or_bridge_review by graph alignment."
        ),
        "default_recommendation": (
            "Do not redesign all scopes at once. Use patch_lifecycle as the first stress-test, then update the "
            "general scoping policy based on what is learned."
        ),
        "human_arbitration_options": [
            "keep_all_current_scopes_for_now",
            "redesign_patch_lifecycle_first",
            "redesign_all_scopes",
            "create_scope_generation_policy_v2",
            "defer_to_backlog",
        ],
    },
}


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


def load_candidates(path: Path) -> list[dict[str, Any]]:
    doc = load_yaml(path)
    root = doc.get("scope_redesign_candidates", {})
    return root.get("candidates", []) or []


def group_for_candidate(candidate: dict[str, Any]) -> str:
    candidate_type = candidate.get("candidate_type")

    mapping = {
        "classify_unowned_core_area": "MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION",
        "keep_patch_core_with_subcluster": "MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE",
        "review_patch_trigger_boundary": "MACRO_003_PATCH_TRIGGER_BOUNDARY",
        "review_multi_owner_cluster": "MACRO_004_MULTI_OWNER_CLUSTER_REVIEW",
        "declare_or_review_neighbors": "MACRO_005_NEIGHBOR_DECLARATION_REVIEW",
        "review_scope_boundary": "MACRO_006_SCOPE_BOUNDARY_REVIEW",
    }

    return mapping.get(candidate_type, "MACRO_999_OTHER")


def short_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate.get("candidate_type"),
        "priority": candidate.get("priority"),
        "title": candidate.get("title"),
        "affected_scope_keys": candidate.get("affected_scope_keys", []) or [],
        "affected_cluster_ids": candidate.get("affected_cluster_ids", []) or [],
        "affected_node_count": len(candidate.get("affected_node_ids", []) or []),
        "recommended_arbitration_options": candidate.get("recommended_arbitration_options", []) or [],
    }


def build_macro_decisions(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for candidate in candidates:
        grouped[group_for_candidate(candidate)].append(candidate)

    macros: list[dict[str, Any]] = []

    for macro_id, definition in MACRO_DEFINITIONS.items():
        macro_candidates = grouped.get(macro_id, [])
        macros.append(
            {
                "macro_decision_id": macro_id,
                "title": definition["title"],
                "status": "pending_human_arbitration",
                "priority": definition["priority"],
                "candidate_ids": [
                    candidate.get("candidate_id")
                    for candidate in macro_candidates
                    if candidate.get("candidate_id")
                ],
                "candidate_count": len(macro_candidates),
                "problem_statement": definition["problem_statement"],
                "default_recommendation": definition["default_recommendation"],
                "human_arbitration_options": definition["human_arbitration_options"],
                "human_decision": {
                    "arbitration_status": "pending",
                    "selected_option": None,
                    "rationale": None,
                    "canonicalization_action": None,
                },
            }
        )

    return macros


def build_arbitration_items(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for candidate in candidates:
        item = short_candidate(candidate)
        item["macro_decision_id"] = group_for_candidate(candidate)
        item["human_decision"] = {
            "arbitration_status": "pending",
            "selected_option": None,
            "rationale": None,
            "canonicalization_action": None,
        }
        items.append(item)

    return items


def summarize(candidates: list[dict[str, Any]], macros: list[dict[str, Any]]) -> dict[str, Any]:
    type_counts = Counter(candidate.get("candidate_type") for candidate in candidates)
    priority_counts = Counter(candidate.get("priority") for candidate in candidates)
    macro_counts = Counter(group_for_candidate(candidate) for candidate in candidates)

    return {
        "candidate_count": len(candidates),
        "macro_decision_count": len(macros),
        "candidate_type_counts": dict(sorted(type_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "macro_candidate_counts": dict(sorted(macro_counts.items())),
    }


def build_artifact(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    macros = build_macro_decisions(candidates)
    items = build_arbitration_items(candidates)

    return {
        "scope_redesign_arbitration": {
            "schema_version": 0.1,
            "status": "PENDING_HUMAN_ARBITRATION",
            "source": "tmp/scope_lab/scope_redesign_candidates.yaml",
            "summary": summarize(candidates, macros),
            "macro_decisions": macros,
            "candidate_arbitration_items": items,
            "completion_criteria": [
                "Each macro_decision has a non-pending human_decision.",
                "Each accepted macro_decision identifies a canonicalization_action.",
                "Accepted changes are later converted into core patches and/or scope_generation decisions.",
                "The scope catalog is regenerated deterministically after canonical changes.",
                "Ownership bijection and full reconstruction are validated before serious bounded runs.",
            ],
            "notes": [
                "This file is editable by humans.",
                "It is not a canonical policy file yet.",
                "It is an arbitration scaffold for the Scope Lab.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate human arbitration scaffold.")
    parser.add_argument("--candidates", default="tmp/scope_lab/scope_redesign_candidates.yaml")
    parser.add_argument("--out", default="tmp/scope_lab/scope_redesign_arbitration.yaml")
    args = parser.parse_args()

    candidates = load_candidates(Path(args.candidates))
    artifact = build_artifact(candidates)

    Path(args.out).write_text(dump_yaml(artifact), encoding="utf-8")

    print(json.dumps(artifact["scope_redesign_arbitration"]["summary"], indent=2, ensure_ascii=False))
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
