#!/usr/bin/env python3
"""Prepare a non-mutating bounded run preflight report for STAGE_00.

Implements STAGE_00 mode `run_candidate_preflight`.
It never opens a run and never mutates canonical files.
"""
from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

DEFAULT_RUNS_INDEX = Path("docs/pipelines/constitution/runs/index.yaml")
DEFAULT_BACKLOG_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_report.yaml")
DEFAULT_LIFECYCLE_VALIDATION = Path("docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml")
DEFAULT_MARKDOWN = Path("docs/pipelines/constitution/reports/bounded_run_preflight.md")


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


def candidate_matches_scope(entry: Dict[str, Any], scope_key: str) -> bool:
    related = entry.get("related_scope_keys") or []
    return entry.get("scope_key") == scope_key or scope_key in related


def classify_entry_for_preflight(entry: Dict[str, Any]) -> Dict[str, Any]:
    candidate_id = str(entry.get("candidate_id", ""))
    if candidate_id.endswith("FULL_STATE_MACHINE_R01"):
        return {
            "preflight_class": "primary_run_seed",
            "recommended_inclusion": "include_first_if_run_opened",
            "rank": 1,
            "rationale": "Canonical patch lifecycle state machine is the coherent seed for a future patch_lifecycle design run.",
        }
    if candidate_id.endswith("PRIORITY_QUEUE_R01"):
        return {
            "preflight_class": "dependent_design_extension",
            "recommended_inclusion": "include_first_if_run_opened",
            "rank": 2,
            "rationale": "Priority lanes depend naturally on the patch lifecycle state model and fit the same targeted design run.",
        }
    if candidate_id.endswith("ESCALATION_BOUNDARY_R01"):
        return {
            "preflight_class": "conditional_cross_scope_boundary",
            "recommended_inclusion": "include_conditionally_after_state_machine_design",
            "rank": 3,
            "rationale": "Escalation semantics cross patch_lifecycle, learner_state and deployment_governance; include only if escalation triggers are explicitly in scope.",
        }
    if candidate_id.endswith("REFERENTIEL_PARAMETER_R01"):
        return {
            "preflight_class": "cross_core_follow_up",
            "recommended_inclusion": "exclude_from_constitution_only_run",
            "rank": 4,
            "rationale": "Referentiel parameter dependency is cross-core/external-read-only and needs a separate referentiel/link or cross-core contract.",
        }
    return {
        "preflight_class": "generic_scope_backlog_signal",
        "recommended_inclusion": "manual_review_required",
        "rank": 99,
        "rationale": "No specific classifier matched this backlog entry.",
    }


def load_and_validate_inputs(runs_index_path: Path, backlog_report_path: Path, lifecycle_validation_path: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    runs_root = get_root(load_yaml(runs_index_path), "runs_index")
    backlog_root = get_root(load_yaml(backlog_report_path), "governance_backlog_report")
    lifecycle_root = get_root(load_yaml(lifecycle_validation_path), "governance_backlog_lifecycle_validation")
    if backlog_root.get("status") != "PASS":
        raise SystemExit(f"governance_backlog_report must be PASS, got {backlog_root.get('status')!r}")
    if lifecycle_root.get("status") != "PASS":
        raise SystemExit(f"governance_backlog_lifecycle_validation must be PASS, got {lifecycle_root.get('status')!r}")
    return runs_root, backlog_root, lifecycle_root


def build_decision(scope_key: str, matching_entries: List[Dict[str, Any]], active_runs: List[Any], force_open: bool) -> Dict[str, Any]:
    if active_runs:
        return {
            "status": "BLOCKED",
            "recommendation": "cannot_open_run_active_runs_present",
            "new_bounded_run_recommended_now": False,
            "reason": "A constitution run is already active; STAGE_00 preflight cannot authorize another run.",
            "next_action": "resolve_or_close_active_runs_first",
        }
    if not matching_entries:
        return {
            "status": "PREFLIGHT_KEEP_BACKLOG_OPEN",
            "recommendation": "no_open_backlog_signal_for_scope",
            "new_bounded_run_recommended_now": False,
            "reason": f"No open governance backlog entry currently impacts scope {scope_key!r}.",
            "next_action": "OPEN_NEW_RUN may proceed only if justified by another explicit signal",
        }

    included_first = [e for e in matching_entries if e["classification"]["recommended_inclusion"] == "include_first_if_run_opened"]
    conditional = [e for e in matching_entries if e["classification"]["recommended_inclusion"] == "include_conditionally_after_state_machine_design"]
    excluded = [e for e in matching_entries if e["classification"]["recommended_inclusion"] == "exclude_from_constitution_only_run"]

    if force_open:
        return {
            "status": "PREFLIGHT_READY_TO_OPEN_RUN",
            "recommendation": "open_new_bounded_run",
            "new_bounded_run_recommended_now": True,
            "reason": "Human override requested force-open. A targeted run can be opened if entry action records included, conditional and excluded backlog entries.",
            "next_action": "OPEN_NEW_RUN_ENTRY_ACTION",
            "proposed_scope_key": scope_key,
            "proposed_run_theme": "patch_lifecycle_state_machine_and_priority_lanes",
            "included_candidate_ids": [e["candidate_id"] for e in included_first],
            "conditional_candidate_ids": [e["candidate_id"] for e in conditional],
            "excluded_candidate_ids": [e["candidate_id"] for e in excluded],
        }

    return {
        "status": "PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
        "recommendation": "defer_to_stage00_backlog_review",
        "new_bounded_run_recommended_now": False,
        "reason": "Open backlog entries exist for the requested scope, but they are reviewed design follow-ups rather than urgent pipeline blockers. Do not open a new bounded run now unless a human explicitly overrides the preflight.",
        "next_action": "keep_backlog_open_with_review_metadata",
        "proposed_scope_key_if_later_opened": scope_key,
        "proposed_run_theme_if_later_opened": "patch_lifecycle_state_machine_and_priority_lanes",
        "included_first_if_later_opened": [e["candidate_id"] for e in included_first],
        "conditional_if_later_opened": [e["candidate_id"] for e in conditional],
        "excluded_or_separate_follow_up": [e["candidate_id"] for e in excluded],
    }


def build_report(scope_key: str, runs_index_path: Path, backlog_report_path: Path, lifecycle_validation_path: Path, force_open: bool) -> Dict[str, Any]:
    runs_root, backlog_root, lifecycle_root = load_and_validate_inputs(runs_index_path, backlog_report_path, lifecycle_validation_path)
    active_runs = runs_root.get("active_runs") or []
    all_entries = backlog_root.get("selected_entries_detail") or []
    if not isinstance(all_entries, list):
        raise SystemExit("governance_backlog_report.selected_entries_detail must be a list")

    matching_entries = []
    for entry in all_entries:
        if isinstance(entry, dict) and candidate_matches_scope(entry, scope_key):
            item = {
                "entry_id": entry.get("entry_id"),
                "candidate_id": entry.get("candidate_id"),
                "title": entry.get("title"),
                "type": entry.get("type"),
                "scope_key": entry.get("scope_key"),
                "related_scope_keys": entry.get("related_scope_keys") or [],
                "stage00_relevant": entry.get("stage00_relevant"),
                "recommended_action_from_backlog": entry.get("recommended_action"),
                "classification": classify_entry_for_preflight(entry),
            }
            matching_entries.append(item)
    matching_entries.sort(key=lambda item: item["classification"]["rank"])

    type_counts = Counter(str(e.get("type")) for e in matching_entries)
    inclusion_counts = Counter(e["classification"]["recommended_inclusion"] for e in matching_entries)
    decision = build_decision(scope_key, matching_entries, active_runs, force_open)

    return {
        "bounded_run_preflight_report": {
            "schema_version": "0.1",
            "stage_id": "STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN",
            "mode": "run_candidate_preflight",
            "generated_at": iso_now(),
            "status": decision["status"],
            "mutation_policy": {
                "runs_index": "not_modified",
                "governance_backlog_yaml": "not_modified",
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "cores": "not_modified",
            },
            "inputs": [
                {"ref": normalize_path(path), "sha256": sha256_file(path)}
                for path in [runs_index_path, backlog_report_path, lifecycle_validation_path]
            ],
            "requested_scope_key": scope_key,
            "active_run_check": {
                "active_run_count": len(active_runs),
                "active_runs": active_runs,
                "no_active_run_confirmed": len(active_runs) == 0,
            },
            "backlog_signal": {
                "matching_open_entry_count": len(matching_entries),
                "matching_counts_by_type": dict(sorted(type_counts.items())),
                "matching_counts_by_recommended_inclusion": dict(sorted(inclusion_counts.items())),
                "lifecycle_validation_status": lifecycle_root.get("status"),
                "open_entries_all_scopes": (backlog_root.get("summary") or {}).get("open_entries"),
            },
            "decision": decision,
            "entries": matching_entries,
            "guardrails": [
                "This report does not open a run.",
                "Do not mutate policy.yaml or decisions.yaml from preflight.",
                "Do not regenerate the scope catalog from preflight.",
                "Do not close backlog entries from preflight; use the lifecycle validator and an explicit lifecycle patch.",
                "Do not include cross-core referentiel dependencies in a Constitution-only run without a cross-core contract.",
            ],
        }
    }


def build_markdown(root: Dict[str, Any]) -> str:
    decision = root["decision"]
    lines = [
        "# Bounded run preflight",
        "",
        f"Stage: `{root['stage_id']}`",
        f"Mode: `{root['mode']}`",
        f"Status: `{root['status']}`",
        f"Requested scope: `{root['requested_scope_key']}`",
        "",
        "## Decision",
        "",
        f"- Recommendation: `{decision['recommendation']}`",
        f"- New bounded run recommended now: `{str(decision['new_bounded_run_recommended_now']).lower()}`",
        f"- Next action: `{decision['next_action']}`",
        "",
        decision["reason"],
        "",
        "## Backlog signal",
        "",
        f"- Matching open backlog entries: `{root['backlog_signal']['matching_open_entry_count']}`",
        f"- Active constitution runs: `{root['active_run_check']['active_run_count']}`",
        "",
        "## Entries",
        "",
        "| Rank | Candidate | Type | Inclusion |",
        "|---:|---|---|---|",
    ]
    for entry in root["entries"]:
        c = entry["classification"]
        lines.append(f"| {c['rank']} | `{entry['candidate_id']}` | `{entry['type']}` | `{c['recommended_inclusion']}` |")
    lines.extend(["", "## Guardrails", ""])
    for guardrail in root["guardrails"]:
        lines.append(f"- {guardrail}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a bounded run preflight report.")
    parser.add_argument("--scope-key", required=True, help="Target scope key to evaluate, e.g. patch_lifecycle")
    parser.add_argument("--runs-index", default=str(DEFAULT_RUNS_INDEX))
    parser.add_argument("--backlog-report", default=str(DEFAULT_BACKLOG_REPORT))
    parser.add_argument("--lifecycle-validation", default=str(DEFAULT_LIFECYCLE_VALIDATION))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN))
    parser.add_argument("--force-open", action="store_true", help="Human override: emit PREFLIGHT_READY_TO_OPEN_RUN")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(
        scope_key=args.scope_key,
        runs_index_path=Path(args.runs_index),
        backlog_report_path=Path(args.backlog_report),
        lifecycle_validation_path=Path(args.lifecycle_validation),
        force_open=args.force_open,
    )
    root = report["bounded_run_preflight_report"]
    write_yaml(Path(args.report), report)
    write_text(Path(args.markdown), build_markdown(root))
    print(f"Wrote {args.report}")
    print(f"Wrote {args.markdown}")
    print(f"Status: {root['status']}")
    print(f"Recommendation: {root['decision']['recommendation']}")
    print(f"New bounded run recommended now: {root['decision']['new_bounded_run_recommended_now']}")
    return 0 if root["status"] != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
