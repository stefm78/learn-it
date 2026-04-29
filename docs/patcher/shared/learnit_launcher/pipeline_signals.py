from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml


SIGNALS_FILENAME = "signals.yaml"


def load_pipeline_signals(repo_root: Path, pipeline_id: str) -> dict[str, Any]:
    signals_path = repo_root / "docs" / "pipelines" / pipeline_id / SIGNALS_FILENAME
    root = load_yaml(signals_path).get("pipeline_signals", {})

    if not isinstance(root, dict):
        return _empty_slot(pipeline_id, signals_path, provider="missing_or_invalid")

    signals = root.get("signals", []) or []
    if not isinstance(signals, list):
        signals = []

    compact_signals: list[dict[str, Any]] = []
    for signal in signals:
        if not isinstance(signal, dict):
            continue
        compact_signals.append(
            {
                "id": signal.get("id", ""),
                "status": signal.get("status", ""),
                "summary": signal.get("summary", ""),
                "scope_key": signal.get("scope_key", ""),
                "recommended_action": signal.get("recommended_action", ""),
                "recommended_mode": signal.get("recommended_mode", ""),
                "run_opening_authorized_by_signal": signal.get("run_opening_authorized_by_signal") is True,
            }
        )

    attention_count = sum(1 for signal in compact_signals if signal.get("status") == "attention")
    return {
        "pipeline_id": str(root.get("pipeline_id") or pipeline_id),
        "signals_path": str(signals_path).replace("\\", "/"),
        "provider": str(root.get("signals_provider") or "missing"),
        "status": "attention" if attention_count else "clear",
        "has_attention_signals": attention_count > 0,
        "attention_count": attention_count,
        "run_opening_authorized_by_signals": False,
        "signals": compact_signals,
    }


def build_pipeline_signal_slots(repo_root: Path, pipeline_ids: list[str]) -> list[dict[str, Any]]:
    return [load_pipeline_signals(repo_root, pipeline_id) for pipeline_id in pipeline_ids]


def build_launcher_signal_summary(signal_slots: list[dict[str, Any]]) -> dict[str, Any]:
    attention_slots = [slot for slot in signal_slots if slot.get("has_attention_signals") is True]
    return {
        "has_attention_signals": bool(attention_slots),
        "attention_pipeline_count": len(attention_slots),
        "recommended_default_hint": "review_pipeline_signals" if attention_slots else "new_run",
        "run_opening_authorized_by_signals": False,
        "attention_slots": attention_slots,
    }


def build_review_action_slot(signal_summary: dict[str, Any]) -> dict[str, Any]:
    has_attention = signal_summary.get("has_attention_signals") is True
    return {
        "key": "review_pipeline_signals",
        "label": "Review pipeline attention signals before opening a new run",
        "available": has_attention,
        "recommended": has_attention,
        "pipeline_signals": signal_summary,
    }


def build_next_best_action_slot(signal_summary: dict[str, Any]) -> dict[str, Any]:
    if signal_summary.get("has_attention_signals") is not True:
        return {
            "status": "unavailable_now",
            "reason": "no pipeline attention signal is currently declared",
            "pipeline_signals": signal_summary,
        }

    return {
        "status": "attention_review_available",
        "meaning": "A pipeline attention signal exists; review it before deciding whether to open a new run.",
        "pipeline_signals": signal_summary,
        "run_opening_authorized_by_signals": False,
        "run_materialization_authorized_by_signals": False,
    }


def compact_prompt_binding(signal_summary: dict[str, Any]) -> dict[str, str]:
    attention_slots = signal_summary.get("attention_slots", []) or []
    if not attention_slots:
        return {
            "pipeline_signals": "provider=none status=clear signals=[]",
            "pipeline_signals_handling": "",
        }

    parts: list[str] = []
    for slot in attention_slots:
        provider = slot.get("provider", "missing")
        for signal in slot.get("signals", []) or []:
            parts.append(
                "pipeline={pipeline} provider={provider} id={id} status={status} scope={scope} action={action} mode={mode} summary={summary} run_opening_authorized_by_signal={auth}".format(
                    pipeline=slot.get("pipeline_id", ""),
                    provider=provider,
                    id=signal.get("id", ""),
                    status=signal.get("status", ""),
                    scope=signal.get("scope_key", ""),
                    action=signal.get("recommended_action", ""),
                    mode=signal.get("recommended_mode", ""),
                    summary=str(signal.get("summary", "")).replace(";", ","),
                    auth=str(signal.get("run_opening_authorized_by_signal") is True).lower(),
                )
            )

    return {
        "pipeline_signals": "status=attention signals=[" + " | ".join(parts) + "]",
        "pipeline_signals_handling": (
            "attention_signal_must_be_acknowledged; "
            "if signal scope matches target_scope_key, preflight_or_explicit_human_override_required; "
            "if signal scope differs from target_scope_key, warn_human_and_state_intentional_non_treatment"
        ),
    }


def _empty_slot(pipeline_id: str, path: Path, *, provider: str) -> dict[str, Any]:
    return {
        "pipeline_id": pipeline_id,
        "signals_path": str(path).replace("\\", "/"),
        "provider": provider,
        "status": "clear",
        "has_attention_signals": False,
        "attention_count": 0,
        "run_opening_authorized_by_signals": False,
        "signals": [],
    }
