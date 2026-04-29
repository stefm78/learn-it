from __future__ import annotations

from pathlib import Path
from typing import Any

from .maturity import (
    MATURITY_AXES_COUNT,
    MATURITY_GATED_LEVELS,
    MATURITY_LEVELS,
    MATURITY_MAX_SCORE,
    MATURITY_MINIMUM_LEVEL,
    maturity_level_from_score,
    maturity_pct,
)
from .governance_backlog import (
    attach_governance_backlog_signal,
    build_governance_backlog_scope_summary,
    empty_governance_backlog_signal,
)
from .bounded_preflight import (
    attach_bounded_run_preflight_signal,
    build_bounded_run_preflight_summary,
    empty_bounded_run_preflight_signal,
)
from .run_context import probe_run_context
from .consolidation import detect_abnormal_state, detect_consolidation_ready
from .yaml_io import load_yaml

def enrich_scope_maturity(scope_record: dict[str, Any]) -> dict[str, Any]:
    raw_maturity = scope_record.get("maturity") or {}
    score = raw_maturity.get("score_total", 0)
    level = raw_maturity.get("level") or maturity_level_from_score(score)
    gated = level in MATURITY_GATED_LEVELS
    return {
        "scope_key": scope_record.get("scope_key"),
        "scope_id": scope_record.get("scope_id"),
        "maturity_score": score,
        "maturity_score_max": MATURITY_MAX_SCORE,
        "maturity_axes_count": MATURITY_AXES_COUNT,
        "maturity_level": level,
        "maturity_available_for_run": not gated,
        "maturity_gate_reason": f"scope level {level} is below minimum {MATURITY_MINIMUM_LEVEL}" if gated else "",
    }


def sort_scopes_by_maturity(scopes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(scopes, key=lambda s: (-s.get("maturity_score", 0), s.get("scope_key", "")))


def build_maturity_summary(enriched_scopes: list[dict[str, Any]]) -> dict[str, Any]:
    available = [s for s in enriched_scopes if s["maturity_available_for_run"]]
    gated = [s for s in enriched_scopes if not s["maturity_available_for_run"]]
    return {
        "score_model": f"6 axes x 4 pts = {MATURITY_MAX_SCORE} pts max (displayed as %)",
        "levels_scale": [
            {"level": lvl, "range_pct": f"{round(lo * 100 / MATURITY_MAX_SCORE)}% - {round(hi * 100 / MATURITY_MAX_SCORE)}%"}
            for lvl, lo, hi in MATURITY_LEVELS
        ],
        "minimum_recommended_level": MATURITY_MINIMUM_LEVEL,
        "minimum_recommended_pct": maturity_pct(13),
        "scopes_available_count": len(available),
        "scopes_gated_count": len(gated),
        "scopes_ranked": [
            {
                "scope_key": s["scope_key"],
                "maturity_pct": maturity_pct(s["maturity_score"]),
                "maturity_level": s["maturity_level"],
                "available_for_run": s["maturity_available_for_run"],
            }
            for s in enriched_scopes
        ],
    }


def discover_constitution(repo_root: Path) -> dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / "constitution"
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    scope_catalog = load_yaml(pipeline_root / "scope_catalog" / "manifest.yaml")
    ai_protocol = load_yaml(pipeline_root / "AI_PROTOCOL.yaml")

    index_data = runs_index.get("runs_index", {})
    active_runs = index_data.get("active_runs", [])
    closed_runs = index_data.get("closed_runs", [])
    published_scopes_raw = scope_catalog.get("scope_catalog", {}).get("published_scopes", [])

    governance_backlog_scope_summary = build_governance_backlog_scope_summary(repo_root)
    bounded_run_preflight_summary = build_bounded_run_preflight_summary(repo_root)
    enriched_scopes = sort_scopes_by_maturity([enrich_scope_maturity(s) for s in published_scopes_raw])
    enriched_scopes = [
        attach_bounded_run_preflight_signal(
            attach_governance_backlog_signal(s, governance_backlog_scope_summary),
            bounded_run_preflight_summary,
        )
        for s in enriched_scopes
    ]
    maturity_summary = build_maturity_summary(enriched_scopes)

    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        run_scope_key = str(run.get("scope_key") or "")
        merged_run["governance_backlog_signal"] = governance_backlog_scope_summary.get(
            run_scope_key,
            empty_governance_backlog_signal(),
        )
        merged_run["bounded_run_preflight_signal"] = bounded_run_preflight_summary.get(
            run_scope_key,
            empty_bounded_run_preflight_signal(),
        )
        if probe.get("effective_current_stage"):
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        merged_run["task_view_status"] = probe.get("task_view_status", "")
        merged_run["terminal_closed"] = probe.get("terminal_closed", False)
        merged_run["compact_execution_prompt"] = probe.get("compact_execution_prompt", "")
        run_manifest_path = pipeline_root / "runs" / run_id / "run_manifest.yaml"
        anomaly = detect_abnormal_state(run, probe, run_manifest_path)
        if anomaly:
            merged_run["anomaly_detected"] = anomaly["reason"]
            merged_run["anomaly_code"] = anomaly["code"]
            merged_run["recommended_entry_action"] = "RECONCILE_RUN"
        else:
            merged_run["recommended_entry_action"] = "CONTINUE_ACTIVE_RUN"
        enriched_runs.append({**merged_run, "ids_first": probe})

    consolidation_probe = detect_consolidation_ready(
        pipeline_root=pipeline_root,
        active_runs=active_runs,
        closed_runs=closed_runs,
        branch="feat/core-modularization-bootstrap",
        pipeline_id="constitution",
    )

    result: dict[str, Any] = {
        "pipeline_id": "constitution",
        "ai_protocol_present": bool(ai_protocol),
        "active_runs_count": len(active_runs),
        "active_runs": enriched_runs,
        "closed_runs_count": len(closed_runs),
        "published_scopes": enriched_scopes,
        "maturity_summary": maturity_summary,
        "governance_backlog_scope_summary": governance_backlog_scope_summary,
    }
    if consolidation_probe:
        result["consolidation_probe"] = consolidation_probe

    executable_active_runs = [r for r in enriched_runs if r.get("task_view_status") != "terminal_closed"]

    if consolidation_probe and len(active_runs) == 0:
        result.update(
            {
                "recommended_action": "consolidate",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": False,
            }
        )
    elif len(executable_active_runs) == 1:
        run = executable_active_runs[0]
        other_scopes = [s for s in enriched_scopes if s.get("scope_key") != run.get("scope_key")]
        result.update(
            {
                "recommended_action": "CONTINUE_ACTIVE_RUN",
                "recommended_run_id": run.get("run_id"),
                "recommended_scope_key": run.get("scope_key"),
                "recommended_current_stage": run.get("current_stage"),
                "recommended_ids_first": run.get("ids_first", {}),
                "recommended_entry_action": run.get("recommended_entry_action", "CONTINUE_ACTIVE_RUN"),
                "recommended_anomaly_detected": run.get("anomaly_detected", ""),
                "recommended_anomaly_code": run.get("anomaly_code", ""),
                "other_available_scopes": other_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in other_scopes),
            }
        )
    elif len(active_runs) == 0:
        result.update(
            {
                "recommended_action": "OPEN_NEW_RUN",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in enriched_scopes),
            }
        )
    elif len(executable_active_runs) == 0:
        result.update(
            {
                "recommended_action": "DISAMBIGUATE",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in enriched_scopes),
                "note": "active runs exist but none is executable according to run_context.task_view",
            }
        )
    else:
        result.update(
            {
                "recommended_action": "DISAMBIGUATE",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in enriched_scopes),
            }
        )
    return result


def discover_generic_pipeline(repo_root: Path, pipeline_id: str) -> dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / pipeline_id
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    active_runs = runs_index.get("runs_index", {}).get("active_runs", [])

    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if probe.get("effective_current_stage"):
            merged_run["current_stage"] = probe.get("effective_current_stage", "")
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        merged_run["task_view_status"] = probe.get("task_view_status", "")
        merged_run["terminal_closed"] = probe.get("terminal_closed", False)
        merged_run["compact_execution_prompt"] = probe.get("compact_execution_prompt", "")
        enriched_runs.append({**merged_run, "ids_first": probe})

    executable_active_runs = [r for r in enriched_runs if r.get("task_view_status") != "terminal_closed"]
    recommended_action = "CONTINUE_ACTIVE_RUN" if executable_active_runs else "OPEN_NEW_RUN"
    result: dict[str, Any] = {
        "pipeline_id": pipeline_id,
        "active_runs_count": len(active_runs),
        "active_runs": enriched_runs,
        "recommended_action": recommended_action,
        "published_scopes": [],
    }
    if executable_active_runs:
        run = executable_active_runs[0]
        result["recommended_run_id"] = run.get("run_id", "")
        result["recommended_scope_key"] = run.get("scope_key", "")
        result["recommended_current_stage"] = run.get("current_stage", "")
        result["recommended_ids_first"] = run.get("ids_first", {})
    return result

