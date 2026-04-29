from __future__ import annotations

from pathlib import Path
from typing import Any

from .pipeline_signals import (
    build_launcher_signal_summary,
    build_next_best_action_slot,
    build_pipeline_signal_slots,
    build_review_action_slot,
    compact_prompt_binding,
)
from .registry import discover_pipelines


def build_pipeline_signals_overlay(repo_root: Path) -> dict[str, Any]:
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines(registry_path)
    pipeline_ids = [str(pipeline.get("pipeline_id", "")) for pipeline in pipelines if pipeline.get("pipeline_id")]

    signal_slots = build_pipeline_signal_slots(repo_root, pipeline_ids)
    signal_summary = build_launcher_signal_summary(signal_slots)

    return {
        "pipeline_signals_overlay": {
            "schema_version": "0.1",
            "source": "docs/pipelines/<pipeline_id>/signals.yaml",
            "status": "attention" if signal_summary.get("has_attention_signals") else "clear",
            "recommended_default_hint": signal_summary.get("recommended_default_hint", "new_run"),
            "signal_summary": signal_summary,
            "action_menu_addition": build_review_action_slot(signal_summary),
            "next_best_actions_addition": {
                "review_pipeline_signals": build_next_best_action_slot(signal_summary)
            },
            "open_new_run_prompt_binding_addition": compact_prompt_binding(signal_summary),
            "launcher_authorizes_run_from_signals": False,
        }
    }
