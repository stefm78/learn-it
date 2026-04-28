#!/usr/bin/env python3
"""Prepare PHASE_19B multi-owner cluster human arbitration surface.

Non-mutating deterministic preparation:
- reads PHASE_19A inventory report;
- creates a human-editable arbitration YAML;
- creates a readable Markdown summary;
- does not modify policy.yaml, decisions.yaml, scope catalog, cores, or reports other than
  the arbitration surface.
"""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEFAULT_INVENTORY = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_inventory_report.yaml")
DEFAULT_ARBITRATION = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_arbitration.yaml")
DEFAULT_MARKDOWN = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_arbitration.md")

ALLOWED_HUMAN_DECISIONS = [
    "keep_current_ownership_with_existing_governance",
    "keep_current_ownership_with_explicit_neighbors",
    "record_diagnostic_subcluster",
    "move_node_ownership",
    "split_scope",
    "merge_scope_fragments",
    "open_or_update_governance_backlog",
    "defer_to_governance_backlog",
    "wont_fix_with_rationale",
]


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}")
    return value


def recommended_decision_for(candidate: Dict[str, Any]) -> Dict[str, Any]:
    cid = candidate.get("candidate_id")
    cluster_id = candidate.get("cluster_id")

    if cid == "CAND_MULTI_OWNER_CLUSTER_006":
        return {
            "recommended_human_decision": "keep_current_ownership_with_existing_governance",
            "recommended_requires_policy_decisions_patch": False,
            "recommended_requires_catalog_regeneration": False,
            "recommended_rationale": (
                "Cluster LABEL_CLUSTER_001 is broad and mixed, but the strongest signals are already filtered by "
                "PHASE_18 doctrine: explicit read-neighbors exist, patch_trigger_governance is already a diagnostic "
                "subcluster with ownership_effect none, and UNOWNED/external material is a bridge/read signal rather "
                "than ownership transfer. Keep current ownership and use existing backlog items for residual design questions."
            ),
            "recommended_follow_up": [
                "keep_current_ownership",
                "preserve_existing_read_neighbors",
                "preserve_existing_diagnostic_subcluster",
                "review_existing_governance_backlog_refs_before opening any new backlog item",
            ],
        }

    if cid == "CAND_MULTI_OWNER_CLUSTER_008":
        return {
            "recommended_human_decision": "keep_current_ownership_with_explicit_neighbors",
            "recommended_requires_policy_decisions_patch": False,
            "recommended_requires_catalog_regeneration": False,
            "recommended_rationale": (
                "Cluster LABEL_CLUSTER_008 spans deployment_governance, knowledge_and_design and mastery_evaluation, "
                "but the concrete cross-scope links are already represented as explicit read-neighbors around graph propagation, "
                "explicit dependencies and knowledge graph usage. This looks like a semantic dependency bridge, not an ownership move."
            ),
            "recommended_follow_up": [
                "keep_current_ownership",
                "preserve_existing_read_neighbors",
                "optionally revisit as diagnostic_subcluster only if future runs show repeated ambiguity",
            ],
        }

    if cid == "CAND_MULTI_OWNER_CLUSTER_010":
        return {
            "recommended_human_decision": "keep_current_ownership_with_existing_governance",
            "recommended_requires_policy_decisions_patch": False,
            "recommended_requires_catalog_regeneration": False,
            "recommended_rationale": (
                "Cluster LABEL_CLUSTER_013 has high boundary pressure, but PHASE_16 and PHASE_18 already separate the concerns: "
                "runtime/no-generation invariants are governed read-neighbors, patch trigger governance is already a diagnostic "
                "subcluster, and read-neighbor edges must not be interpreted as ownership transfer. Keep current ownership unless "
                "a future run identifies a concrete node-level ownership defect."
            ),
            "recommended_follow_up": [
                "keep_current_ownership",
                "preserve_existing_read_neighbors",
                "preserve_patch_trigger_governance_diagnostic_subcluster",
                "do_not_move runtime/no-generation invariants solely because of graph proximity",
            ],
        }

    return {
        "recommended_human_decision": "defer_to_governance_backlog",
        "recommended_requires_policy_decisions_patch": False,
        "recommended_requires_catalog_regeneration": False,
        "recommended_rationale": f"No specific recommendation rule defined for {cid} / {cluster_id}.",
        "recommended_follow_up": ["manual_review_required"],
    }


def build_arbitration(inventory_root: Dict[str, Any], inventory_path: Path) -> Dict[str, Any]:
    candidates = [
        candidate for candidate in inventory_root.get("candidates", [])
        if candidate.get("primary_classification") == "true_ownership_ambiguity"
        and candidate.get("recommended_next_action") == "human_arbitration_required"
    ]

    items = []
    for candidate in candidates:
        rec = recommended_decision_for(candidate)
        items.append({
            "candidate_id": candidate.get("candidate_id"),
            "cluster_id": candidate.get("cluster_id"),
            "title": candidate.get("title"),
            "affected_scope_keys": candidate.get("affected_scope_keys", []),
            "boundary_pressure": candidate.get("boundary_pressure"),
            "nodes_by_owner_scope": candidate.get("nodes_by_owner_scope", {}),
            "dominant_scope": candidate.get("dominant_scope"),
            "dominance_ratio": candidate.get("dominance_ratio"),
            "classification_tags": candidate.get("classification_tags", []),
            "approved_read_neighbor_hit_count": candidate.get("approved_read_neighbor_hit_count", 0),
            "diagnostic_subcluster_hit_count": candidate.get("diagnostic_subcluster_hit_count", 0),
            "open_governance_backlog_refs_for_affected_scopes": candidate.get(
                "open_governance_backlog_refs_for_affected_scopes", []
            ),
            "recommendation": rec,
            "human_arbitration": {
                "decision": "pending",
                "accepted": False,
                "requires_policy_decisions_patch": None,
                "requires_catalog_regeneration": None,
                "rationale": "TO_BE_COMPLETED_BY_HUMAN_ARBITRATION",
                "follow_up_actions": [],
            },
            "allowed_human_decisions": ALLOWED_HUMAN_DECISIONS,
        })

    return {
        "constitution_multi_owner_cluster_arbitration": {
            "schema_version": "0.1",
            "phase_id": "PHASE_19B",
            "generated_at": iso_now(),
            "status": "PENDING_HUMAN_ARBITRATION",
            "source_inventory_report": normalize_path(inventory_path),
            "source_inventory_sha256": sha256_file(inventory_path),
            "scope": "true_ownership_ambiguity_candidates_only",
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "cores": "not_modified",
            },
            "allowed_human_decisions": ALLOWED_HUMAN_DECISIONS,
            "summary": {
                "candidate_count": len(items),
                "pending_count": len(items),
                "accepted_count": 0,
                "requires_policy_decisions_patch_count": 0,
                "requires_catalog_regeneration_count": 0,
            },
            "items": items,
            "human_instructions": [
                "For each item, replace human_arbitration.decision with one allowed value.",
                "Set human_arbitration.accepted to true when the decision is final.",
                "Set requires_policy_decisions_patch and requires_catalog_regeneration explicitly.",
                "Do not infer ownership changes from read-neighbor or diagnostic-subcluster evidence.",
                "If any item requires ownership changes, PHASE_19C must apply through policy/decisions patching and regenerate the catalog.",
            ],
        }
    }


def build_markdown(arbitration_root: Dict[str, Any]) -> str:
    items = arbitration_root["items"]
    lines = [
        "# PHASE_19B — Multi-owner cluster human arbitration",
        "",
        "Status: `PENDING_HUMAN_ARBITRATION`",
        "",
        "Doctrine reminder: read-neighbor declarations, diagnostic subclusters and generated views do **not** transfer ownership.",
        "",
        "## Candidates requiring arbitration",
        "",
        "| Candidate | Cluster | Scopes | Pressure | Recommended decision | Patch? |",
        "|---|---|---|---|---|---|",
    ]

    for item in items:
        rec = item["recommendation"]
        lines.append(
            "| {candidate} | {cluster} | {scopes} | {pressure} | {decision} | {patch} |".format(
                candidate=item["candidate_id"],
                cluster=item["cluster_id"],
                scopes=", ".join(item.get("affected_scope_keys", [])),
                pressure=item.get("boundary_pressure"),
                decision=rec["recommended_human_decision"],
                patch=str(rec["recommended_requires_policy_decisions_patch"]).lower(),
            )
        )

    lines.extend(["", "## Recommended arbitration", ""])
    for item in items:
        rec = item["recommendation"]
        lines.extend([
            f"### {item['candidate_id']} / {item['cluster_id']}",
            "",
            f"- Recommendation: `{rec['recommended_human_decision']}`",
            f"- Requires policy/decisions patch: `{str(rec['recommended_requires_policy_decisions_patch']).lower()}`",
            f"- Requires catalog regeneration: `{str(rec['recommended_requires_catalog_regeneration']).lower()}`",
            f"- Affected scopes: `{', '.join(item.get('affected_scope_keys', []))}`",
            f"- Classification tags: `{', '.join(item.get('classification_tags', []))}`",
            "",
            rec["recommended_rationale"],
            "",
            "Human arbitration fields to complete in YAML:",
            "",
            "```yaml",
            "human_arbitration:",
            "  decision: pending",
            "  accepted: false",
            "  requires_policy_decisions_patch: null",
            "  requires_catalog_regeneration: null",
            "  rationale: TO_BE_COMPLETED_BY_HUMAN_ARBITRATION",
            "```",
            "",
        ])

    lines.extend([
        "## Allowed decisions",
        "",
    ])
    for decision in ALLOWED_HUMAN_DECISIONS:
        lines.append(f"- `{decision}`")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare PHASE_19B multi-owner cluster arbitration surface.")
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY))
    parser.add_argument("--arbitration", default=str(DEFAULT_ARBITRATION))
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inventory_path = Path(args.inventory)
    arbitration_path = Path(args.arbitration)
    markdown_path = Path(args.markdown)

    inventory_doc = load_yaml(inventory_path)
    inventory_root = get_root(inventory_doc, "constitution_multi_owner_cluster_inventory_report")
    if inventory_root.get("status") != "PASS":
        raise SystemExit(f"Inventory report must be PASS, got {inventory_root.get('status')!r}")

    arbitration_doc = build_arbitration(inventory_root, inventory_path)
    arbitration_root = arbitration_doc["constitution_multi_owner_cluster_arbitration"]

    write_yaml(arbitration_path, arbitration_doc)
    write_text(markdown_path, build_markdown(arbitration_root))

    print(f"Wrote {arbitration_path}")
    print(f"Wrote {markdown_path}")
    print(f"Status: {arbitration_root['status']}")
    print(f"Pending: {arbitration_root['summary']['pending_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
