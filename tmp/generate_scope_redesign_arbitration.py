#!/usr/bin/env python3
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


MACROS = {
    "MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION": {
        "types": ["classify_unowned_core_area"],
        "title": "Classify currently UNOWNED referentiel/link areas",
        "priority": "high",
        "problem_statement": "Referentiel/link areas are currently UNOWNED by the constitution scope catalog.",
        "default_recommendation": "Do not force all referentiel/link IDs into existing constitution scopes. Classify them explicitly.",
        "options": [
            "declare_referentiel_and_link_as_read_only_external_cores",
            "create_separate_referentiel_link_scope_family",
            "assign_selected_referentiel_link_clusters_to_existing_scopes",
            "declare_shared_or_global_ids",
            "defer_to_backlog",
        ],
    },
    "MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE": {
        "types": ["keep_patch_core_with_subcluster"],
        "title": "Decide whether patch lifecycle structural core remains a canonical scope/subcluster",
        "priority": "medium",
        "problem_statement": "The graph identifies a strong patch_lifecycle structural core.",
        "default_recommendation": "Keep the structural patch core in patch_lifecycle for now and name it as a diagnostic subcluster.",
        "options": [
            "keep_in_patch_lifecycle",
            "name_as_patch_structure_subcluster",
            "split_as_patch_core_scope",
            "defer_to_backlog",
        ],
    },
    "MACRO_003_PATCH_TRIGGER_BOUNDARY": {
        "types": ["review_patch_trigger_boundary"],
        "title": "Decide boundary for patch triggers and learner/runtime signals",
        "priority": "high",
        "problem_statement": "Patch trigger nodes are graph-close to learner_state and runtime signals.",
        "default_recommendation": "Keep governed patch decisions in patch_lifecycle, but declare learner/runtime inputs as explicit neighbors.",
        "options": [
            "keep_triggers_in_patch_lifecycle_with_neighbors",
            "move_triggers_to_learner_state",
            "create_patch_trigger_bridge",
            "split_patch_lifecycle",
            "defer_to_backlog",
        ],
    },
    "MACRO_004_MULTI_OWNER_CLUSTER_REVIEW": {
        "types": ["review_multi_owner_cluster"],
        "title": "Review multi-owner graph clusters",
        "priority": "high",
        "problem_statement": "Some graph clusters contain nodes owned by several current scopes.",
        "default_recommendation": "Prefer explicit neighbors or bridge classification before moving ownership.",
        "options": [
            "split_clusters_by_existing_owners",
            "declare_bridge_areas",
            "move_selected_node_ownership",
            "declare_neighbors_only",
            "defer_to_backlog",
        ],
    },
    "MACRO_005_NEIGHBOR_DECLARATION_REVIEW": {
        "types": ["declare_or_review_neighbors"],
        "title": "Review explicit neighbor declarations",
        "priority": "medium",
        "problem_statement": "Several clusters show external dependency pressure.",
        "default_recommendation": "Convert stable external dependencies into explicit neighbor decisions where appropriate.",
        "options": [
            "declare_neighbor_ids",
            "declare_neighbor_scope",
            "move_ownership_if_boundary_is_wrong",
            "create_bridge_if_dependency_is_structural",
            "defer_to_backlog",
        ],
    },
    "MACRO_006_SCOPE_BOUNDARY_REVIEW": {
        "types": ["review_scope_boundary"],
        "title": "Review all existing scope boundaries",
        "priority": "high",
        "problem_statement": "All five current scopes are marked as split_merge_or_bridge_review.",
        "default_recommendation": "Do not redesign all scopes at once. Use patch_lifecycle as first stress-test.",
        "options": [
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
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def load_candidates(path: Path) -> list[dict[str, Any]]:
    doc = load_yaml(path)
    return doc.get("scope_redesign_candidates", {}).get("candidates", []) or []


def macro_for_type(candidate_type: str | None) -> str:
    for macro_id, spec in MACROS.items():
        if candidate_type in spec["types"]:
            return macro_id
    return "MACRO_999_OTHER"


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


def pending_decision() -> dict[str, Any]:
    return {
        "arbitration_status": "pending",
        "selected_option": None,
        "rationale": None,
        "canonicalization_action": None,
    }


def build_macro_decisions(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for candidate in candidates:
        grouped[macro_for_type(candidate.get("candidate_type"))].append(candidate)

    result = []
    for macro_id, spec in MACROS.items():
        items = grouped.get(macro_id, [])
        result.append(
            {
                "macro_decision_id": macro_id,
                "title": spec["title"],
                "status": "pending_human_arbitration",
                "priority": spec["priority"],
                "candidate_count": len(items),
                "candidate_ids": [c.get("candidate_id") for c in items if c.get("candidate_id")],
                "problem_statement": spec["problem_statement"],
                "default_recommendation": spec["default_recommendation"],
                "human_arbitration_options": spec["options"],
                "human_decision": pending_decision(),
            }
        )
    return result


def build_items(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = []
    for candidate in candidates:
        item = short_candidate(candidate)
        item["macro_decision_id"] = macro_for_type(candidate.get("candidate_type"))
        item["human_decision"] = pending_decision()
        items.append(item)
    return items


def summarize(candidates: list[dict[str, Any]], macros: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(candidates),
        "macro_decision_count": len(macros),
        "candidate_type_counts": dict(sorted(Counter(c.get("candidate_type") for c in candidates).items())),
        "priority_counts": dict(sorted(Counter(c.get("priority") for c in candidates).items())),
        "macro_candidate_counts": dict(sorted(Counter(macro_for_type(c.get("candidate_type")) for c in candidates).items())),
    }


def build_artifact(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    macros = build_macro_decisions(candidates)
    return {
        "scope_redesign_arbitration": {
            "schema_version": 0.1,
            "status": "PENDING_HUMAN_ARBITRATION",
            "source": "tmp/scope_lab/scope_redesign_candidates.yaml",
            "summary": summarize(candidates, macros),
            "macro_decisions": macros,
            "candidate_arbitration_items": build_items(candidates),
            "completion_criteria": [
                "Each macro_decision has a non-pending human_decision.",
                "Each accepted macro_decision identifies a canonicalization_action.",
                "Accepted changes are converted into core patches and/or scope_generation decisions.",
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
