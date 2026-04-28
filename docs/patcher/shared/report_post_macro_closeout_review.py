#!/usr/bin/env python3
"""PHASE_20A post-macro closeout review report.

Non-mutating reconciliation report:
- reads canonical governance_backlog.yaml;
- reads post-pilot macro evidence from PHASE_16/18/19;
- classifies backlog entries as already addressed, still open, or needing lifecycle decision;
- does not modify governance_backlog.yaml.

Always writes:
  docs/pipelines/constitution/reports/post_macro_closeout_review_report.yaml
  docs/pipelines/constitution/reports/post_macro_closeout_review_report.md
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/post_macro_closeout_review_report.yaml")
DEFAULT_MARKDOWN = Path("docs/pipelines/constitution/reports/post_macro_closeout_review_report.md")

BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
BACKLOG_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_report.yaml")
TRACKER = Path("docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md")
SCOPE_MATURITY = Path("docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml")
NEIGHBOR_IDS_VALIDATION = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml")
NEIGHBOR_DECL_INVENTORY = Path("docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml")
MULTI_OWNER_INVENTORY = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_inventory_report.yaml")
MULTI_OWNER_ARBITRATION_VALIDATION = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_arbitration_validation.yaml")


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
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False, width=120)


def write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8", newline="\n")


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}")
    return value


def read_statuses() -> Dict[str, Any]:
    maturity_root = get_root(load_yaml(SCOPE_MATURITY), "scope_maturity_scoring_report")
    neighbor_validation_root = get_root(load_yaml(NEIGHBOR_IDS_VALIDATION), "constitution_neighbor_ids_arbitration_validation")
    neighbor_inventory_root = get_root(load_yaml(NEIGHBOR_DECL_INVENTORY), "constitution_neighbor_declaration_inventory_report")
    multi_owner_inventory_root = get_root(load_yaml(MULTI_OWNER_INVENTORY), "constitution_multi_owner_cluster_inventory_report")
    multi_owner_validation_root = get_root(
        load_yaml(MULTI_OWNER_ARBITRATION_VALIDATION),
        "constitution_multi_owner_cluster_arbitration_validation",
    )

    return {
        "scope_maturity_scoring_status": maturity_root.get("status"),
        "scope_maturity_blocking_finding_count": (maturity_root.get("summary") or {}).get("blocking_finding_count"),
        "scope_maturity_warning_count": (maturity_root.get("summary") or {}).get("warning_count"),
        "neighbor_ids_arbitration_validation_status": neighbor_validation_root.get("status"),
        "neighbor_ids_arbitration_pending_count": (neighbor_validation_root.get("summary") or {}).get("pending_count"),
        "neighbor_declaration_inventory_status": neighbor_inventory_root.get("status"),
        "neighbor_declaration_inventory_finding_count": (neighbor_inventory_root.get("summary") or {}).get("finding_count"),
        "multi_owner_inventory_status": multi_owner_inventory_root.get("status"),
        "multi_owner_human_arbitration_required_count": (multi_owner_inventory_root.get("summary") or {}).get(
            "human_arbitration_required_count"
        ),
        "multi_owner_arbitration_validation_status": multi_owner_validation_root.get("status"),
        "multi_owner_patch_ready_count": (multi_owner_validation_root.get("summary") or {}).get("patch_ready_count"),
    }


def classify_entry(entry: Dict[str, Any], statuses: Dict[str, Any]) -> Dict[str, Any]:
    entry_id = str(entry.get("entry_id"))
    candidate_id = str(entry.get("candidate_id"))
    title = str(entry.get("title"))
    entry_type = str(entry.get("type"))
    related_scopes = entry.get("related_scope_keys") or []

    # Default: still open.
    classification = {
        "entry_id": entry_id,
        "candidate_id": candidate_id,
        "title": title,
        "type": entry_type,
        "status": entry.get("status"),
        "scope_key": entry.get("scope_key"),
        "related_scope_keys": related_scopes,
        "post_macro_classification": "still_open",
        "recommended_lifecycle_action": "keep_open_with_review_metadata",
        "recommended_resolution_status": "open",
        "requires_backlog_patch": True,
        "requires_policy_decisions_patch": False,
        "requires_catalog_regeneration": False,
        "evidence": [],
        "recommended_resolution_note": "",
        "next_review_trigger": "next STAGE_00 scope partition review or next patch_lifecycle bounded run",
    }

    if candidate_id == "GBC_PATCH_LIFECYCLE_LEARNER_STATE_NEIGHBORS_R01":
        classification.update({
            "post_macro_classification": "addressed_by_phase16_and_phase17",
            "recommended_lifecycle_action": "mark_addressed",
            "recommended_resolution_status": "addressed",
            "requires_backlog_patch": True,
            "evidence": [
                "PHASE_16 approved exact patch_lifecycle read-neighbor IDs TYPE_STATE_AXIS_VALUE_COST and TYPE_SELF_REPORT_AR_N1.",
                "PHASE_17 scoring publication converged to PASS with dependency coverage 1.0 and no maturity delta.",
            ],
            "recommended_resolution_note": (
                "Addressed by PHASE_16/17. Explicit learner_state read-neighbor IDs for patch_lifecycle triggers were governed, "
                "applied through decisions.yaml, regenerated into the scope catalog, and scoring now converges to PASS."
            ),
            "next_review_trigger": "none; reopen only if future scoring/reporting identifies missing learner_state read-neighbors",
        })
        return classification

    if candidate_id == "GBC_PATCH_LIFECYCLE_UNCOVERED_CONFLICT_LOGGING_R01":
        classification.update({
            "post_macro_classification": "reviewed_no_ownership_change",
            "recommended_lifecycle_action": "mark_addressed",
            "recommended_resolution_status": "addressed",
            "requires_backlog_patch": True,
            "evidence": [
                "PHASE_19A classified the related multi-owner signal as diagnostic_subcluster/read_neighbor_relation rather than ownership transfer.",
                "PHASE_19B closed MACRO_004 with PASS_NO_PATCH_REQUIRED and no ownership changes.",
            ],
            "recommended_resolution_note": (
                "Addressed by PHASE_19. Multi-owner review concluded no ownership transfer is required; ACTION_LOG_UNCOVERED_CONFLICT "
                "can remain governed by existing patch_lifecycle/diagnostic governance unless a future concrete node-level defect appears."
            ),
            "next_review_trigger": "future concrete ownership defect or repeated patch_lifecycle run issue",
        })
        return classification

    if candidate_id == "GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01":
        classification.update({
            "post_macro_classification": "partially_reviewed_still_open",
            "recommended_lifecycle_action": "keep_open_with_review_metadata",
            "recommended_resolution_status": "open",
            "requires_backlog_patch": True,
            "evidence": [
                "PHASE_19B rejected ownership moves from current multi-owner signals.",
                "The broader escalation boundary still spans patch_lifecycle, learner_state and deployment_governance and was not fully designed.",
            ],
            "recommended_resolution_note": (
                "Keep open. PHASE_19 removed the immediate ownership-transfer pressure, but the broader escalation-trigger boundary "
                "still requires design when escalation semantics are revisited."
            ),
            "next_review_trigger": "next patch_lifecycle run touching escalation triggers or dedicated escalation-boundary design run",
        })
        return classification

    if candidate_id == "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01":
        classification.update({
            "post_macro_classification": "still_open_cross_core_follow_up",
            "recommended_lifecycle_action": "keep_open_with_review_metadata",
            "recommended_resolution_status": "open",
            "requires_backlog_patch": True,
            "evidence": [
                "PHASE_18 clarified external read-only core semantics.",
                "The specific referentiel parameter dependency still requires referentiel/link coordination or a cross-core change request.",
            ],
            "recommended_resolution_note": (
                "Keep open. PHASE_18 clarified the model, but did not select or govern the specific referentiel parameter as a concrete "
                "external read neighbor."
            ),
            "next_review_trigger": "referentiel/link external-read-only follow-up or patch escalation threshold design",
        })
        return classification

    if candidate_id == "GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01":
        classification.update({
            "post_macro_classification": "still_open_design_extension",
            "recommended_lifecycle_action": "keep_open_with_review_metadata",
            "recommended_resolution_status": "open",
            "requires_backlog_patch": True,
            "evidence": [
                "No later phase introduced a canonical deterministic priority lane model.",
                "PHASE_19 concerned ownership ambiguity, not patch queue semantics.",
            ],
            "recommended_resolution_note": (
                "Keep open. Priority queue semantics remain a future patch_lifecycle design extension and should not be silently added."
            ),
            "next_review_trigger": "future run requiring escalation/rollback priority semantics or dedicated patch queue design",
        })
        return classification

    if candidate_id == "GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01":
        classification.update({
            "post_macro_classification": "still_open_design_extension",
            "recommended_lifecycle_action": "keep_open_with_review_metadata",
            "recommended_resolution_status": "open",
            "requires_backlog_patch": True,
            "evidence": [
                "No later phase introduced a full canonical patch state machine.",
                "Pilot and macro follow-ups stabilized scoping/governance, not a complete patch lifecycle state model.",
            ],
            "recommended_resolution_note": (
                "Keep open. A full patch state machine remains a future patch_lifecycle design extension."
            ),
            "next_review_trigger": "future patch_lifecycle run requiring explicit state transitions beyond current terminal semantics",
        })
        return classification

    classification["evidence"].append("No PHASE_20A rule matched this backlog candidate.")
    classification["recommended_resolution_note"] = "Keep open until manually reviewed."
    return classification


def build_report() -> Dict[str, Any]:
    backlog_root = get_root(load_yaml(BACKLOG), "governance_backlog")
    entries = backlog_root.get("entries") or []
    open_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("status") == "open"]
    statuses = read_statuses()

    reconciled = [classify_entry(entry, statuses) for entry in open_entries]
    class_counts = Counter(item["post_macro_classification"] for item in reconciled)
    action_counts = Counter(item["recommended_lifecycle_action"] for item in reconciled)
    resolution_counts = Counter(item["recommended_resolution_status"] for item in reconciled)

    status = "PASS"

    return {
        "post_macro_closeout_review_report": {
            "schema_version": "0.1",
            "phase_id": "PHASE_20A",
            "generated_at": iso_now(),
            "status": status,
            "mutation_policy": {
                "governance_backlog_yaml": "not_modified",
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "cores": "not_modified",
            },
            "inputs": [
                {"ref": normalize_path(path), "sha256": sha256_file(path)}
                for path in [
                    BACKLOG,
                    BACKLOG_REPORT,
                    TRACKER,
                    SCOPE_MATURITY,
                    NEIGHBOR_IDS_VALIDATION,
                    NEIGHBOR_DECL_INVENTORY,
                    MULTI_OWNER_INVENTORY,
                    MULTI_OWNER_ARBITRATION_VALIDATION,
                ]
            ],
            "macro_status_snapshot": statuses,
            "summary": {
                "open_backlog_entry_count_before_review": len(open_entries),
                "recommended_mark_addressed_count": action_counts.get("mark_addressed", 0),
                "recommended_keep_open_count": action_counts.get("keep_open_with_review_metadata", 0),
                "recommended_wont_fix_count": action_counts.get("mark_wont_fix", 0),
                "requires_backlog_patch_count": sum(1 for item in reconciled if item["requires_backlog_patch"]),
                "requires_policy_decisions_patch_count": sum(
                    1 for item in reconciled if item["requires_policy_decisions_patch"]
                ),
                "requires_catalog_regeneration_count": sum(
                    1 for item in reconciled if item["requires_catalog_regeneration"]
                ),
                "post_macro_classification_counts": dict(sorted(class_counts.items())),
                "recommended_resolution_status_counts": dict(sorted(resolution_counts.items())),
            },
            "entries": reconciled,
            "recommended_next_steps": [
                "Use this report as PHASE_20B input.",
                "If accepted, apply a governance_backlog.yaml lifecycle patch only; do not change policy.yaml or decisions.yaml.",
                "Expected PHASE_20B outcome: mark two entries addressed and keep four entries open with review metadata.",
                "After backlog patch, rerun validate_governance_backlog_lifecycle.py and report_governance_backlog.py.",
            ],
        }
    }


def build_markdown(report_root: Dict[str, Any]) -> str:
    summary = report_root["summary"]
    lines = [
        "# PHASE_20A — Post-macro closeout review",
        "",
        f"Status: `{report_root['status']}`",
        "",
        "## Summary",
        "",
        f"- Open backlog entries before review: `{summary['open_backlog_entry_count_before_review']}`",
        f"- Recommended mark addressed: `{summary['recommended_mark_addressed_count']}`",
        f"- Recommended keep open with review metadata: `{summary['recommended_keep_open_count']}`",
        f"- Requires policy/decisions patch: `{summary['requires_policy_decisions_patch_count']}`",
        f"- Requires catalog regeneration: `{summary['requires_catalog_regeneration_count']}`",
        "",
        "## Recommended backlog lifecycle actions",
        "",
        "| Entry | Recommended status | Classification | Patch? |",
        "|---|---:|---|---|",
    ]

    for entry in report_root["entries"]:
        lines.append(
            f"| `{entry['candidate_id']}` | `{entry['recommended_resolution_status']}` | "
            f"`{entry['post_macro_classification']}` | `{str(entry['requires_backlog_patch']).lower()}` |"
        )

    lines.extend([
        "",
        "## Detail",
        "",
    ])

    for entry in report_root["entries"]:
        lines.extend([
            f"### {entry['candidate_id']}",
            "",
            f"- Title: {entry['title']}",
            f"- Recommended lifecycle action: `{entry['recommended_lifecycle_action']}`",
            f"- Recommended resolution status: `{entry['recommended_resolution_status']}`",
            f"- Next review trigger: {entry['next_review_trigger']}",
            "",
            entry["recommended_resolution_note"],
            "",
        ])

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PHASE_20A post-macro closeout review report.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    root = report["post_macro_closeout_review_report"]

    write_yaml(Path(args.report), report)
    write_text(Path(args.markdown), build_markdown(root))

    print(f"Wrote {args.report}")
    print(f"Wrote {args.markdown}")
    print(f"Status: {root['status']}")
    print(f"Recommended mark addressed: {root['summary']['recommended_mark_addressed_count']}")
    print(f"Recommended keep open: {root['summary']['recommended_keep_open_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
