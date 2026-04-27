#!/usr/bin/env python3
"""Apply PHASE_09B policy/decisions patch for Scope Graph Clustering.

This script updates only:
  - docs/pipelines/constitution/policies/scope_generation/policy.yaml
  - docs/pipelines/constitution/policies/scope_generation/decisions.yaml

It does not modify:
  - docs/cores/current/*.yaml
  - docs/pipelines/constitution/scope_catalog/*

The patch is intentionally idempotent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


POLICY_PATH = Path("docs/pipelines/constitution/policies/scope_generation/policy.yaml")
DECISIONS_PATH = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
CANDIDATES_PATH = Path("tmp/scope_lab/scope_redesign_candidates.yaml")
PLAN_PATH = Path("tmp/scope_lab/phase_09_canonicalization_plan.yaml")


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.write_text(
        yaml.safe_dump(
            data,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        ),
        encoding="utf-8",
    )


def get_root(doc: dict[str, Any], key: str) -> dict[str, Any]:
    root = doc.get(key)
    if not isinstance(root, dict):
        raise ValueError(f"Expected top-level key {key!r} in document.")
    return root


def find_candidate(candidates_doc: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    candidates = candidates_doc.get("scope_redesign_candidates", {}).get("candidates", []) or []
    for candidate in candidates:
        if candidate.get("candidate_id") == candidate_id:
            return candidate
    raise ValueError(f"Candidate not found: {candidate_id}")


def decision_exists(decisions: list[dict[str, Any]], decision_id: str) -> bool:
    return any(item.get("decision_id") == decision_id for item in decisions)


def upsert_policy_block(root: dict[str, Any]) -> list[str]:
    changed: list[str] = []

    core_role_classification = {
        "owned_core_family": "constitution",
        "owned_core_files": [
            "docs/cores/current/constitution.yaml",
        ],
        "external_read_only_core_files": [
            "docs/cores/current/referentiel.yaml",
            "docs/cores/current/link.yaml",
        ],
        "default_cross_core_write_policy": "forbidden_without_explicit_cross_core_run_contract",
        "rationale": (
            "Constitution scope generation owns Constitution IDs. Referentiel and Link are readable external cores "
            "for Constitution bounded runs and must not be patched without an explicit cross-core governed run contract."
        ),
    }

    if root.get("core_role_classification") != core_role_classification:
        root["core_role_classification"] = core_role_classification
        changed.append("policy.core_role_classification")

    id_classification_contract = {
        "constitution_owned": {
            "description": "ID owned by exactly one published Constitution scope.",
            "requires_unique_owner": True,
            "blocking_if_missing_owner": True,
        },
        "external_read_only_referentiel": {
            "description": "Referentiel ID readable by Constitution runs but not owned by them.",
            "requires_unique_constitution_owner": False,
            "allowed_source_files": [
                "docs/cores/current/referentiel.yaml",
            ],
        },
        "external_read_only_link": {
            "description": "Link ID readable by Constitution runs but not owned by them.",
            "requires_unique_constitution_owner": False,
            "allowed_source_files": [
                "docs/cores/current/link.yaml",
            ],
        },
        "shared_or_global": {
            "description": "Explicitly governed shared/global ID classification.",
            "requires_explicit_decision": True,
        },
        "missing_or_invalid": {
            "description": "Referenced ID absent from canonical sources or not classified.",
            "blocking": True,
        },
    }

    if root.get("id_classification_contract") != id_classification_contract:
        root["id_classification_contract"] = id_classification_contract
        changed.append("policy.id_classification_contract")

    diagnostic_subclusters = {
        "status": "scope_lab_only_until_promoted",
        "allowed_use": [
            "explain cluster structure",
            "guide neighbor review",
            "guide future scope redesign",
        ],
        "forbidden_use": [
            "direct ownership reassignment",
            "generated catalog mutation without explicit decisions",
        ],
        "promotion_rule": (
            "A diagnostic subcluster may influence scope_generation decisions only after human arbitration. "
            "It is not itself an ownership boundary."
        ),
    }

    if root.get("diagnostic_subclusters") != diagnostic_subclusters:
        root["diagnostic_subclusters"] = diagnostic_subclusters
        changed.append("policy.diagnostic_subclusters")

    return changed


def build_external_read_only_decision() -> dict[str, Any]:
    return {
        "decision_id": "SGEN_DECISION_008",
        "status": "approved",
        "decision_type": "classify_external_read_only_cores",
        "scope_keys_affected": [
            "deployment_governance",
            "knowledge_and_design",
            "learner_state",
            "mastery_evaluation",
            "patch_lifecycle",
        ],
        "target_core_files": [
            "docs/cores/current/referentiel.yaml",
            "docs/cores/current/link.yaml",
        ],
        "target_ids": [],
        "target_patterns": [],
        "decision_payload": {
            "classification_mode": "external_read_only_core",
            "external_id_classes": [
                "external_read_only_referentiel",
                "external_read_only_link",
            ],
            "write_policy": "forbidden_without_explicit_cross_core_run_contract",
            "read_mode": "neighbor_or_fallback",
            "source_decision": "MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION",
        },
        "applies_from": "2026-04-27",
        "decided_by": "human",
        "challenged_with_ai": True,
        "justification": (
            "Referentiel and Link IDs are readable by Constitution bounded runs but are not owned by Constitution "
            "scopes. They must be classified explicitly so the bijection validator can distinguish Constitution "
            "ownership from external read-only core references."
        ),
    }


def build_subcluster_decision(
    decision_id: str,
    subcluster_key: str,
    candidate: dict[str, Any],
    justification: str,
) -> dict[str, Any]:
    target_ids = candidate.get("affected_node_ids", []) or []
    cluster_ids = candidate.get("affected_cluster_ids", []) or []

    return {
        "decision_id": decision_id,
        "status": "approved",
        "decision_type": "record_diagnostic_subcluster",
        "scope_keys_affected": [
            "patch_lifecycle",
        ],
        "target_ids": target_ids,
        "target_patterns": [],
        "decision_payload": {
            "subcluster_key": subcluster_key,
            "classification": "diagnostic_subcluster",
            "ownership_effect": "none",
            "owner_scope_remains": "patch_lifecycle",
            "source_candidate_id": candidate.get("candidate_id"),
            "source_cluster_ids": cluster_ids,
            "scope_lab_only_until_promoted": True,
        },
        "applies_from": "2026-04-27",
        "decided_by": "human",
        "challenged_with_ai": True,
        "justification": justification,
    }


def build_neighbor_review_placeholder(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_id": "SGEN_DECISION_011",
        "status": "proposed",
        "decision_type": "force_logical_neighbors",
        "scope_keys_affected": [
            "patch_lifecycle",
        ],
        "target_ids": [],
        "target_patterns": [],
        "decision_payload": {
            "neighbor_class": "patch_trigger_governance_required_read_neighbor",
            "read_mode": "primary",
            "source_candidate_id": candidate.get("candidate_id"),
            "source_cluster_ids": candidate.get("affected_cluster_ids", []) or [],
            "requires_exact_id_selection_before_approval": True,
            "note": (
                "Patch trigger governance remains owned by patch_lifecycle, but required learner_state/runtime signal IDs "
                "must be selected explicitly before this decision can become approved."
            ),
        },
        "applies_from": "2026-04-27",
        "decided_by": "human",
        "challenged_with_ai": True,
        "justification": (
            "This placeholder records the accepted arbitration direction without silently selecting neighbor IDs. "
            "Exact learner_state/runtime neighbors must be reviewed before approval."
        ),
    }


def append_decisions(root: dict[str, Any], candidates_doc: dict[str, Any]) -> list[str]:
    decisions = root.get("decisions")
    if not isinstance(decisions, list):
        raise ValueError("Expected scope_generation_decisions.decisions to be a list.")

    changed: list[str] = []

    patch_core = find_candidate(candidates_doc, "CAND_PATCH_LIFECYCLE_033")
    patch_triggers = find_candidate(candidates_doc, "CAND_PATCH_LIFECYCLE_034")

    new_decisions = [
        build_external_read_only_decision(),
        build_subcluster_decision(
            decision_id="SGEN_DECISION_009",
            subcluster_key="patch_structure_and_quality",
            candidate=patch_core,
            justification=(
                "The Scope Lab graph identified a coherent patch_lifecycle structural core around patch artifacts, "
                "impact scope, quality gate, rollback, deterministic validation, and invalid patch rejection. "
                "This is recorded as a diagnostic subcluster while ownership remains unchanged."
            ),
        ),
        build_subcluster_decision(
            decision_id="SGEN_DECISION_010",
            subcluster_key="patch_trigger_governance",
            candidate=patch_triggers,
            justification=(
                "Patch trigger nodes are close to learner_state/runtime signals, but they represent governed patch "
                "lifecycle decisions. They remain in patch_lifecycle and are recorded as a diagnostic subcluster."
            ),
        ),
        build_neighbor_review_placeholder(patch_triggers),
    ]

    for decision in new_decisions:
        decision_id = decision["decision_id"]
        if decision_exists(decisions, decision_id):
            continue
        decisions.append(decision)
        changed.append(f"decisions.{decision_id}")

    return changed


def main() -> int:
    if not PLAN_PATH.exists():
        raise FileNotFoundError(f"Missing phase 09 plan: {PLAN_PATH}")
    if not CANDIDATES_PATH.exists():
        raise FileNotFoundError(f"Missing candidates: {CANDIDATES_PATH}")

    policy_doc = load_yaml(POLICY_PATH)
    decisions_doc = load_yaml(DECISIONS_PATH)
    candidates_doc = load_yaml(CANDIDATES_PATH)

    policy_root = get_root(policy_doc, "scope_generation_policy")
    decisions_root = get_root(decisions_doc, "scope_generation_decisions")

    changed = []
    changed.extend(upsert_policy_block(policy_root))
    changed.extend(append_decisions(decisions_root, candidates_doc))

    write_yaml(POLICY_PATH, policy_doc)
    write_yaml(DECISIONS_PATH, decisions_doc)

    if changed:
        print("PHASE_09B patch applied:")
        for item in changed:
            print(f" - {item}")
    else:
        print("PHASE_09B patch already applied; no changes.")

    print(f"updated: {POLICY_PATH}")
    print(f"updated: {DECISIONS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
