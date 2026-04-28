#!/usr/bin/env python3
"""PHASE_21A remaining patch_lifecycle backlog decision report.

Non-mutating decision report:
- reads the current open governance backlog report;
- classifies the four remaining patch_lifecycle backlog entries;
- recommends whether to open a new bounded run now or keep entries in normal STAGE_00 review;
- does not modify governance_backlog.yaml, policy.yaml, decisions.yaml, tracker, or cores.

Outputs:
  docs/pipelines/constitution/reports/remaining_patch_lifecycle_backlog_decision_report.yaml
  docs/pipelines/constitution/reports/remaining_patch_lifecycle_backlog_decision_report.md
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/remaining_patch_lifecycle_backlog_decision_report.yaml")
DEFAULT_MARKDOWN = Path("docs/pipelines/constitution/reports/remaining_patch_lifecycle_backlog_decision_report.md")

BACKLOG_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_report.yaml")
LIFECYCLE_VALIDATION = Path("docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml")
TRACKER = Path("docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md")


EXPECTED_OPEN_CANDIDATES = {
    "GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01",
    "GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01",
    "GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01",
    "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01",
}


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


def classify_candidate(candidate_id: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    if candidate_id == "GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01":
        return {
            "topic_class": "core_patch_lifecycle_design_extension",
            "run_fit": "good_if_design_run_is_opened",
            "recommended_treatment": "keep_open_until_explicit_design_run",
            "priority_rank_if_run_opened": 1,
            "rationale": (
                "This is the most coherent seed for a future patch_lifecycle design run: a canonical patch state machine "
                "would provide the backbone for priority lanes and escalation semantics. It is not urgent enough by itself "
                "to force a new run immediately after macro closeout."
            ),
        }

    if candidate_id == "GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01":
        return {
            "topic_class": "dependent_patch_lifecycle_design_extension",
            "run_fit": "good_as_part_of_state_machine_run",
            "recommended_treatment": "keep_open_until_explicit_design_run",
            "priority_rank_if_run_opened": 2,
            "rationale": (
                "Priority queue semantics should not be added in isolation. They fit naturally after, or inside, a patch "
                "state machine design run."
            ),
        }

    if candidate_id == "GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01":
        return {
            "topic_class": "cross_scope_escalation_boundary",
            "run_fit": "conditional_after_state_machine_design",
            "recommended_treatment": "keep_open_for_stage00_backlog_review",
            "priority_rank_if_run_opened": 3,
            "rationale": (
                "The escalation boundary spans patch_lifecycle, learner_state and deployment_governance. PHASE_19 removed "
                "ownership-transfer pressure. It should be revisited only after patch lifecycle semantics are clearer or "
                "when a future run touches escalation triggers."
            ),
        }

    if candidate_id == "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01":
        return {
            "topic_class": "cross_core_external_read_only_follow_up",
            "run_fit": "poor_for_constitution_only_run",
            "recommended_treatment": "keep_open_for_referentiel_link_follow_up",
            "priority_rank_if_run_opened": 4,
            "rationale": (
                "The referentiel parameter dependency is a cross-core/external-read-only topic. It should not be silently "
                "folded into a Constitution-only patch_lifecycle run unless a cross-core change request or explicit "
                "external neighbor decision is prepared."
            ),
        }

    return {
        "topic_class": "unknown",
        "run_fit": "manual_review_required",
        "recommended_treatment": "keep_open_for_stage00_backlog_review",
        "priority_rank_if_run_opened": 99,
        "rationale": "No PHASE_21A classifier matched this candidate.",
    }


def build_report() -> Dict[str, Any]:
    backlog_report_doc = load_yaml(BACKLOG_REPORT)
    backlog_root = get_root(backlog_report_doc, "governance_backlog_report")
    lifecycle_doc = load_yaml(LIFECYCLE_VALIDATION)
    lifecycle_root = get_root(lifecycle_doc, "governance_backlog_lifecycle_validation")

    if backlog_root.get("status") != "PASS":
        raise SystemExit(f"Backlog report must be PASS, got {backlog_root.get('status')!r}")
    if lifecycle_root.get("status") != "PASS":
        raise SystemExit(f"Lifecycle validation must be PASS, got {lifecycle_root.get('status')!r}")

    summary = backlog_root.get("summary") or {}
    open_count = summary.get("open_entries")
    if open_count != 4:
        raise SystemExit(f"Expected 4 open entries after PHASE_20B, got {open_count!r}")

    entries = backlog_root.get("selected_entries_detail") or []
    if not isinstance(entries, list):
        raise SystemExit("governance_backlog_report.selected_entries_detail must be a list")

    candidates = []
    found_ids = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        candidate_id = str(entry.get("candidate_id"))
        found_ids.add(candidate_id)
        classification = classify_candidate(candidate_id, entry)
        candidates.append({
            "entry_id": entry.get("entry_id"),
            "candidate_id": candidate_id,
            "title": entry.get("title"),
            "type": entry.get("type"),
            "scope_key": entry.get("scope_key"),
            "related_scope_keys": entry.get("related_scope_keys") or [],
            "stage00_relevant": entry.get("stage00_relevant"),
            "recommended_action_from_backlog": entry.get("recommended_action"),
            "classification": classification,
        })

    missing = sorted(EXPECTED_OPEN_CANDIDATES - found_ids)
    unexpected = sorted(found_ids - EXPECTED_OPEN_CANDIDATES)
    findings = []
    if missing:
        findings.append({
            "finding_id": "PHASE21A_EXPECTED_OPEN_CANDIDATES_MISSING",
            "severity": "blocking",
            "missing_candidate_ids": missing,
        })
    if unexpected:
        findings.append({
            "finding_id": "PHASE21A_UNEXPECTED_OPEN_CANDIDATES",
            "severity": "blocking",
            "unexpected_candidate_ids": unexpected,
        })

    topic_counts = Counter(item["classification"]["topic_class"] for item in candidates)
    run_fit_counts = Counter(item["classification"]["run_fit"] for item in candidates)

    # Explicit decision recommendation.
    decision = {
        "recommended_decision": "do_not_open_new_bounded_run_now",
        "recommended_status_for_phase21a": "PASS_RECOMMEND_DEFER_TO_NORMAL_STAGE00_REVIEW",
        "new_pipeline_run_recommended_now": False,
        "reason": (
            "The four remaining entries are reviewed design follow-ups, not unresolved macro blockers. "
            "Opening a new run immediately would mix three different concerns: state-machine design, escalation boundary, "
            "and cross-core referentiel parameter governance. Keep the entries open and let STAGE_00/launcher warnings "
            "surface them for the next relevant scope decision."
        ),
        "if_human_overrides_and_opens_run": {
            "recommended_scope_key": "patch_lifecycle",
            "recommended_run_theme": "patch_lifecycle_state_machine_and_priority_lanes",
            "recommended_first_entries": [
                "GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01",
                "GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01",
            ],
            "conditional_entries": [
                "GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01",
            ],
            "excluded_or_separate_follow_up": [
                "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01",
            ],
            "guardrail": (
                "Do not include the referentiel parameter dependency in a Constitution-only run unless a cross-core "
                "read-neighbor/change-request contract is explicitly prepared."
            ),
        },
    }

    status = "FAIL" if any(f["severity"] == "blocking" for f in findings) else "PASS"

    return {
        "remaining_patch_lifecycle_backlog_decision_report": {
            "schema_version": "0.1",
            "phase_id": "PHASE_21A",
            "generated_at": iso_now(),
            "status": status,
            "mutation_policy": {
                "governance_backlog_yaml": "not_modified",
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "tracker": "not_modified",
                "cores": "not_modified",
            },
            "inputs": [
                {"ref": normalize_path(path), "sha256": sha256_file(path)}
                for path in [BACKLOG_REPORT, LIFECYCLE_VALIDATION, TRACKER]
            ],
            "summary": {
                "open_backlog_entry_count": len(candidates),
                "topic_class_counts": dict(sorted(topic_counts.items())),
                "run_fit_counts": dict(sorted(run_fit_counts.items())),
                "new_pipeline_run_recommended_now": decision["new_pipeline_run_recommended_now"],
                "recommended_decision": decision["recommended_decision"],
                "finding_count": len(findings),
            },
            "decision": decision,
            "candidates": sorted(candidates, key=lambda item: item["classification"]["priority_rank_if_run_opened"]),
            "findings": findings,
            "recommended_next_steps": [
                "Use this report as PHASE_21A decision evidence.",
                "If accepted, update the tracker only: PHASE_21A done, no new run opened, PHASE_21B done_not_required or handoff-only.",
                "Keep the four backlog entries open with their PHASE_20B review metadata.",
                "Do not mutate policy.yaml, decisions.yaml, or the scope catalog for PHASE_21A.",
            ],
        }
    }


def build_markdown(root: Dict[str, Any]) -> str:
    decision = root["decision"]
    lines = [
        "# PHASE_21A — Remaining patch_lifecycle backlog decision",
        "",
        f"Status: `{root['status']}`",
        "",
        "## Decision recommendation",
        "",
        f"- Recommended decision: `{decision['recommended_decision']}`",
        f"- New bounded pipeline run recommended now: `{str(decision['new_pipeline_run_recommended_now']).lower()}`",
        "",
        decision["reason"],
        "",
        "## Remaining open entries",
        "",
        "| Rank if run opened | Candidate | Topic class | Run fit | Recommended treatment |",
        "|---:|---|---|---|---|",
    ]

    for item in root["candidates"]:
        classification = item["classification"]
        lines.append(
            f"| {classification['priority_rank_if_run_opened']} | `{item['candidate_id']}` | "
            f"`{classification['topic_class']}` | `{classification['run_fit']}` | "
            f"`{classification['recommended_treatment']}` |"
        )

    lines.extend([
        "",
        "## If a human overrides and opens a run",
        "",
        f"- Scope: `{decision['if_human_overrides_and_opens_run']['recommended_scope_key']}`",
        f"- Theme: `{decision['if_human_overrides_and_opens_run']['recommended_run_theme']}`",
        "- First entries:",
    ])
    for cid in decision["if_human_overrides_and_opens_run"]["recommended_first_entries"]:
        lines.append(f"  - `{cid}`")
    lines.append("- Conditional entries:")
    for cid in decision["if_human_overrides_and_opens_run"]["conditional_entries"]:
        lines.append(f"  - `{cid}`")
    lines.append("- Separate follow-up:")
    for cid in decision["if_human_overrides_and_opens_run"]["excluded_or_separate_follow_up"]:
        lines.append(f"  - `{cid}`")
    lines.extend([
        "",
        f"Guardrail: {decision['if_human_overrides_and_opens_run']['guardrail']}",
        "",
    ])

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PHASE_21A remaining patch_lifecycle backlog decision report.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    root = report["remaining_patch_lifecycle_backlog_decision_report"]

    write_yaml(Path(args.report), report)
    write_text(Path(args.markdown), build_markdown(root))

    print(f"Wrote {args.report}")
    print(f"Wrote {args.markdown}")
    print(f"Status: {root['status']}")
    print(f"Recommended decision: {root['summary']['recommended_decision']}")
    print(f"New run recommended now: {root['summary']['new_pipeline_run_recommended_now']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
