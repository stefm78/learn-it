#!/usr/bin/env python3
"""Refresh Constitution pipeline signals from reviewed governance backlog state.

This script is deterministic and scoped to derived signal/preflight artifacts.

Default dry-run:
  python docs/patcher/shared/refresh_constitution_pipeline_signals.py

Apply:
  python docs/patcher/shared/refresh_constitution_pipeline_signals.py --apply
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

DEFAULT_RUNS_INDEX = Path("docs/pipelines/constitution/runs/index.yaml")
DEFAULT_BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
DEFAULT_BACKLOG_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_report.yaml")
DEFAULT_LIFECYCLE_VALIDATION = Path("docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml")
DEFAULT_SIGNALS = Path("docs/pipelines/constitution/signals.yaml")
DEFAULT_PREFLIGHT = Path("docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/pipeline_signals_refresh_report.yaml")

OPEN_REVIEW_FIELDS = ["last_reviewed_at", "last_reviewed_by", "review_note", "next_review_trigger"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing required YAML file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid YAML mapping root: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_non_empty(entry: dict[str, Any], field: str) -> bool:
    return entry.get(field) not in (None, "")


def review_metadata_complete(entry: dict[str, Any]) -> bool:
    return all(has_non_empty(entry, field) for field in OPEN_REVIEW_FIELDS)


def active_runs(runs_index: dict[str, Any]) -> list[dict[str, Any]]:
    root = runs_index.get("runs_index", {})
    active = root.get("active_runs", []) if isinstance(root, dict) else []
    if not isinstance(active, list):
        return []
    return [r for r in active if isinstance(r, dict)]


def direct_scope_key(entry: dict[str, Any]) -> str:
    value = entry.get("scope_key")
    return value if isinstance(value, str) and value else "unknown"


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if str(v)]
    if isinstance(value, str) and value:
        return [value]
    return []


def primary_scope_key(open_entries: list[dict[str, Any]]) -> str | None:
    scopes = sorted({direct_scope_key(entry) for entry in open_entries if direct_scope_key(entry) != "unknown"})
    return scopes[0] if len(scopes) == 1 else None


def classify_state(open_entries: list[dict[str, Any]], lifecycle_status: str, active_run_count: int) -> dict[str, Any]:
    missing_review = [entry for entry in open_entries if not review_metadata_complete(entry)]
    reviewed = [entry for entry in open_entries if review_metadata_complete(entry)]

    if lifecycle_status != "PASS":
        return {
            "state": "blocked_lifecycle_validation",
            "signal_status": "attention",
            "summary": "governance backlog lifecycle validation is not PASS",
            "recommended_action": "FIX_GOVERNANCE_BACKLOG_LIFECYCLE",
            "recommended_mode": "no_run_id_mode",
            "preflight_status": "BLOCKED",
            "preflight_recommendation": "fix_governance_backlog_lifecycle",
            "new_bounded_run_recommended_now": False,
            "reason": "Governance backlog lifecycle validation must be PASS before signals can authorize any next step.",
            "next_action": "fix_governance_backlog_lifecycle",
        }

    if active_run_count > 0:
        return {
            "state": "blocked_active_runs_present",
            "signal_status": "attention",
            "summary": "active constitution run exists; Stage 00 signal refresh is blocked for partition changes",
            "recommended_action": "CONTINUE_ACTIVE_RUN",
            "recommended_mode": "run_id_mode",
            "preflight_status": "BLOCKED_ACTIVE_RUNS_PRESENT",
            "preflight_recommendation": "continue_or_reconcile_active_run",
            "new_bounded_run_recommended_now": False,
            "reason": "Active constitution runs exist. Do not open a new run or refresh partition decisions around an active run.",
            "next_action": "continue_or_reconcile_active_run",
        }

    if not open_entries:
        return {
            "state": "clear_no_open_backlog",
            "signal_status": "clear",
            "summary": "no open governance backlog entries",
            "recommended_action": "NO_ACTION",
            "recommended_mode": "no_run_id_mode",
            "preflight_status": "PREFLIGHT_CLEAR",
            "preflight_recommendation": "no_backlog_driven_run_needed",
            "new_bounded_run_recommended_now": False,
            "reason": "No open governance backlog entries are present.",
            "next_action": "keep_no_active_phase",
        }

    if missing_review:
        return {
            "state": "open_entries_require_stage00_review",
            "signal_status": "attention",
            "summary": f"{len(open_entries)} open entries requiring STAGE_00 review",
            "recommended_action": "STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN",
            "recommended_mode": "partition_refresh",
            "preflight_status": "PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
            "preflight_recommendation": "defer_to_stage00_backlog_review",
            "new_bounded_run_recommended_now": False,
            "reason": "Open governance backlog entries exist and at least one lacks complete STAGE_00 review metadata.",
            "next_action": "run_stage00_backlog_review",
        }

    scope_key = primary_scope_key(open_entries)
    scope_text = f" {scope_key}" if scope_key else ""
    return {
        "state": "reviewed_open_backlog_keep_open",
        "signal_status": "attention",
        "summary": f"{len(open_entries)} reviewed open{scope_text} design follow-ups; keep backlog open until explicit design trigger",
        "recommended_action": "KEEP_BACKLOG_OPEN_WITH_REVIEW_METADATA",
        "recommended_mode": "no_run_id_mode",
        "preflight_status": "PREFLIGHT_KEEP_BACKLOG_OPEN",
        "preflight_recommendation": "keep_backlog_open",
        "new_bounded_run_recommended_now": False,
        "reason": (
            "STAGE_00 semantic backlog review has been completed. Open backlog entries remain active with "
            "review metadata, but they are design follow-ups rather than immediate pipeline blockers. "
            "Do not open a new bounded run from this signal without explicit human override."
        ),
        "next_action": "keep_backlog_open_with_review_metadata",
    }


def build_signal(root: dict[str, Any], derived: dict[str, Any], scope_key: str | None, source: Path) -> None:
    signals = root.setdefault("signals", [])
    if not isinstance(signals, list):
        signals = []
        root["signals"] = signals

    signal = None
    for item in signals:
        if isinstance(item, dict) and item.get("id") == "backlog":
            signal = item
            break

    if signal is None:
        signal = {"id": "backlog"}
        signals.append(signal)

    signal["status"] = derived["signal_status"]
    signal["source"] = str(source).replace("\\", "/")
    signal["summary"] = derived["summary"]
    signal["scope_key"] = scope_key or ""
    signal["recommended_action"] = derived["recommended_action"]
    signal["recommended_mode"] = derived["recommended_mode"]
    signal["run_opening_authorized_by_signal"] = False


def build_preflight(
    preflight: dict[str, Any],
    *,
    derived: dict[str, Any],
    now: str,
    open_entries: list[dict[str, Any]],
    reviewed_count: int,
    missing_review_count: int,
    active: list[dict[str, Any]],
    lifecycle_status: str,
    paths: dict[str, Path],
) -> None:
    scope_key = primary_scope_key(open_entries)

    preflight["generated_at"] = now
    preflight["status"] = derived["preflight_status"]
    preflight["requested_scope_key"] = scope_key or ""

    preflight["inputs"] = [
        {"ref": str(paths["runs_index"]).replace("\\", "/"), "sha256": sha256_file(paths["runs_index"])},
        {"ref": str(paths["backlog"]).replace("\\", "/"), "sha256": sha256_file(paths["backlog"])},
        {"ref": str(paths["backlog_report"]).replace("\\", "/"), "sha256": sha256_file(paths["backlog_report"])},
        {"ref": str(paths["lifecycle_validation"]).replace("\\", "/"), "sha256": sha256_file(paths["lifecycle_validation"])},
    ]

    preflight["active_run_check"] = {
        "active_run_count": len(active),
        "active_runs": active,
        "no_active_run_confirmed": len(active) == 0,
    }

    preflight["backlog_signal"] = {
        "matching_open_entry_count": len(open_entries),
        "reviewed_open_entry_count": reviewed_count,
        "missing_review_metadata_count": missing_review_count,
        "matching_counts_by_type": dict(sorted(Counter(str(e.get("type") or "unknown") for e in open_entries).items())),
        "matching_counts_by_scope_key": dict(sorted(Counter(direct_scope_key(e) for e in open_entries).items())),
        "lifecycle_validation_status": lifecycle_status,
        "open_entries_all_scopes": len(open_entries),
    }

    decision = preflight.get("decision")
    if not isinstance(decision, dict):
        decision = {}
    decision["status"] = derived["preflight_status"]
    decision["recommendation"] = derived["preflight_recommendation"]
    decision["new_bounded_run_recommended_now"] = derived["new_bounded_run_recommended_now"]
    decision["reason"] = derived["reason"]
    decision["next_action"] = derived["next_action"]
    if scope_key:
        decision["proposed_scope_key_if_later_opened"] = scope_key
    decision.setdefault("proposed_run_theme_if_later_opened", "patch_lifecycle_state_machine_and_priority_lanes")
    preflight["decision"] = decision

    preflight["entries"] = []
    for rank, entry in enumerate(open_entries, start=1):
        preflight["entries"].append({
            "entry_id": entry.get("entry_id"),
            "candidate_id": entry.get("candidate_id"),
            "title": entry.get("title"),
            "type": entry.get("type"),
            "scope_key": entry.get("scope_key"),
            "related_scope_keys": as_list(entry.get("related_scope_keys")),
            "stage00_relevant": True,
            "review_metadata_complete": review_metadata_complete(entry),
            "last_reviewed_at": entry.get("last_reviewed_at"),
            "last_reviewed_by": entry.get("last_reviewed_by"),
            "next_review_trigger": entry.get("next_review_trigger"),
            "recommended_action_from_backlog": entry.get("recommended_action"),
            "rank": rank,
        })

    preflight["guardrails"] = [
        "This report does not open a run.",
        "Do not mutate policy.yaml or decisions.yaml from preflight.",
        "Do not regenerate the scope catalog from preflight.",
        "Do not close backlog entries from preflight; use the lifecycle validator and an explicit lifecycle patch.",
        "Do not include cross-core referentiel dependencies in a Constitution-only run without a cross-core contract.",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh Constitution pipeline signals from backlog review state.")
    parser.add_argument("--apply", action="store_true", help="write signals.yaml and bounded_run_preflight_report.yaml")
    parser.add_argument("--runs-index", default=str(DEFAULT_RUNS_INDEX))
    parser.add_argument("--backlog", default=str(DEFAULT_BACKLOG))
    parser.add_argument("--backlog-report", default=str(DEFAULT_BACKLOG_REPORT))
    parser.add_argument("--lifecycle-validation", default=str(DEFAULT_LIFECYCLE_VALIDATION))
    parser.add_argument("--signals", default=str(DEFAULT_SIGNALS))
    parser.add_argument("--preflight", default=str(DEFAULT_PREFLIGHT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = {
        "runs_index": Path(args.runs_index),
        "backlog": Path(args.backlog),
        "backlog_report": Path(args.backlog_report),
        "lifecycle_validation": Path(args.lifecycle_validation),
        "signals": Path(args.signals),
        "preflight": Path(args.preflight),
        "report": Path(args.report),
    }

    runs_index = load_yaml(paths["runs_index"])
    backlog_doc = load_yaml(paths["backlog"])
    backlog_report = load_yaml(paths["backlog_report"])
    lifecycle_doc = load_yaml(paths["lifecycle_validation"])
    signals_doc = load_yaml(paths["signals"])
    preflight_doc = load_yaml(paths["preflight"])

    backlog_root = backlog_doc.get("governance_backlog")
    if not isinstance(backlog_root, dict):
        raise SystemExit("Missing governance_backlog root")
    entries = backlog_root.get("entries", [])
    if not isinstance(entries, list):
        raise SystemExit("governance_backlog.entries must be a list")

    lifecycle_root = lifecycle_doc.get("governance_backlog_lifecycle_validation", {})
    lifecycle_status = str(lifecycle_root.get("status") or "UNKNOWN")

    report_root = backlog_report.get("governance_backlog_report", {})
    report_status = str(report_root.get("status") or "UNKNOWN")
    if report_status != "PASS":
        raise SystemExit(f"governance_backlog_report status must be PASS, got {report_status}")

    open_entries = [e for e in entries if isinstance(e, dict) and e.get("status") == "open"]
    reviewed_count = sum(1 for entry in open_entries if review_metadata_complete(entry))
    missing_review_count = len(open_entries) - reviewed_count
    active = active_runs(runs_index)

    derived = classify_state(open_entries, lifecycle_status, len(active))
    now = utc_now()
    scope_key = primary_scope_key(open_entries)

    signals_root = signals_doc.get("pipeline_signals")
    if not isinstance(signals_root, dict):
        raise SystemExit("Missing pipeline_signals root")

    preflight_root = preflight_doc.get("bounded_run_preflight_report")
    if not isinstance(preflight_root, dict):
        raise SystemExit("Missing bounded_run_preflight_report root")

    build_signal(signals_root, derived, scope_key, paths["backlog_report"])
    build_preflight(
        preflight_root,
        derived=derived,
        now=now,
        open_entries=open_entries,
        reviewed_count=reviewed_count,
        missing_review_count=missing_review_count,
        active=active,
        lifecycle_status=lifecycle_status,
        paths=paths,
    )

    refresh_report = {
        "pipeline_signals_refresh_report": {
            "schema_version": "0.1",
            "generated_at": now,
            "status": "PASS_APPLIED" if args.apply else "PASS_DRY_RUN",
            "pipeline_id": "constitution",
            "derived_state": derived["state"],
            "open_entry_count": len(open_entries),
            "reviewed_open_entry_count": reviewed_count,
            "missing_review_metadata_count": missing_review_count,
            "active_run_count": len(active),
            "lifecycle_validation_status": lifecycle_status,
            "signals_status": derived["signal_status"],
            "signals_recommended_action": derived["recommended_action"],
            "preflight_status": derived["preflight_status"],
            "run_opening_authorized_by_signal": False,
            "new_bounded_run_recommended_now": derived["new_bounded_run_recommended_now"],
            "applied": bool(args.apply),
            "would_write": [
                str(paths["signals"]).replace("\\", "/"),
                str(paths["preflight"]).replace("\\", "/"),
            ],
            "report_path": str(paths["report"]).replace("\\", "/"),
        }
    }

    if args.apply:
        write_yaml(paths["signals"], signals_doc)
        write_yaml(paths["preflight"], preflight_doc)

    write_yaml(paths["report"], refresh_report)

    print(f"Status: {refresh_report['pipeline_signals_refresh_report']['status']}")
    print(f"Derived state: {derived['state']}")
    print(f"Open entries: {len(open_entries)}")
    print(f"Reviewed open entries: {reviewed_count}")
    print(f"Missing review metadata: {missing_review_count}")
    print(f"Signals action: {derived['recommended_action']}")
    print(f"Preflight status: {derived['preflight_status']}")
    print(f"Wrote report: {paths['report']}")
    if args.apply:
        print(f"Updated: {paths['signals']}")
        print(f"Updated: {paths['preflight']}")
    else:
        print("Dry-run only. Re-run with --apply to update derived artifacts.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
