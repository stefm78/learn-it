from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml

BOUNDED_RUN_PREFLIGHT_REPORT_PATH = Path("docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml")


def empty_bounded_run_preflight_signal() -> dict[str, Any]:
    return {
        "warning": "none",
        "requested_scope_key": "",
        "status": "",
        "recommendation": "",
        "new_bounded_run_recommended_now": False,
        "matching_open_entry_count": 0,
        "open_new_run_authorized_by_default": False,
        "recommended_entry_decision": "",
    }


def build_bounded_run_preflight_summary(repo_root: Path) -> dict[str, dict[str, Any]]:
    report_path = repo_root / BOUNDED_RUN_PREFLIGHT_REPORT_PATH
    if not report_path.exists():
        return {}

    root = load_yaml(report_path).get("bounded_run_preflight_report", {})
    if not isinstance(root, dict):
        return {}

    scope_key = str(root.get("requested_scope_key") or "")
    if not scope_key:
        return {}

    decision = root.get("decision") or {}
    backlog_signal = root.get("backlog_signal") or {}
    status = str(root.get("status") or decision.get("status") or "")
    recommendation = str(decision.get("recommendation") or "")
    new_run = bool(decision.get("new_bounded_run_recommended_now") is True)
    matching_count = int(backlog_signal.get("matching_open_entry_count") or 0)

    if status == "PREFLIGHT_READY_TO_OPEN_RUN":
        warning = "bounded_run_preflight_ready_requires_confirmation"
        default_authorized = False
        recommended_entry_decision = "open_new_run_authorized_after_human_confirmation"
    elif status == "PREFLIGHT_DEFER_TO_STAGE00_REVIEW":
        warning = "bounded_run_preflight_defer_to_stage00_review"
        default_authorized = False
        recommended_entry_decision = "partition_refresh_preferred_or_open_new_run_blocked"
    elif status == "BLOCKED":
        warning = "bounded_run_preflight_blocked"
        default_authorized = False
        recommended_entry_decision = "open_new_run_blocked"
    elif status:
        warning = "bounded_run_preflight_non_authorizing"
        default_authorized = False
        recommended_entry_decision = "open_new_run_blocked_or_requires_preflight"
    else:
        warning = "none"
        default_authorized = False
        recommended_entry_decision = ""

    return {
        scope_key: {
            "warning": warning,
            "requested_scope_key": scope_key,
            "status": status,
            "recommendation": recommendation,
            "new_bounded_run_recommended_now": new_run,
            "matching_open_entry_count": matching_count,
            "open_new_run_authorized_by_default": default_authorized,
            "recommended_entry_decision": recommended_entry_decision,
        }
    }


def attach_bounded_run_preflight_signal(
    scope_record: dict[str, Any],
    preflight_summary: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    scope_key = str(scope_record.get("scope_key") or "")
    signal = preflight_summary.get(scope_key, empty_bounded_run_preflight_signal())
    return {**scope_record, "bounded_run_preflight_signal": signal}


def compact_bounded_run_preflight_signal(signal: dict[str, Any]) -> str:
    if not signal or signal.get("warning") == "none":
        return "none"

    return (
        f"status={signal.get('status', '')} "
        f"recommendation={signal.get('recommendation', '')} "
        f"new_run={str(signal.get('new_bounded_run_recommended_now') is True).lower()} "
        f"default_authorized={str(signal.get('open_new_run_authorized_by_default') is True).lower()} "
        f"matching_open={signal.get('matching_open_entry_count', 0)} "
        f"entry_decision={signal.get('recommended_entry_decision', '')}"
    )
