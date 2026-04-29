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
    """Machine-readable overlay kept for validation and future integrations."""
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines(registry_path)
    pipeline_ids = [str(pipeline.get("pipeline_id", "")) for pipeline in pipelines if pipeline.get("pipeline_id")]

    signal_slots = build_pipeline_signal_slots(repo_root, pipeline_ids)
    signal_summary = build_launcher_signal_summary(signal_slots)

    return {
        "pipeline_signals_overlay": {
            "schema_version": "0.2",
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


def build_pipeline_signals_review(repo_root: Path) -> dict[str, Any]:
    """Human-oriented review block shown by the wrapper."""
    overlay = build_pipeline_signals_overlay(repo_root)["pipeline_signals_overlay"]
    summary = overlay.get("signal_summary", {})
    attention_slots = summary.get("attention_slots", []) or []

    signal_lines: list[str] = []
    affected_scopes: list[str] = []
    recommended_actions: list[str] = []

    for slot in attention_slots:
        pipeline_id = slot.get("pipeline_id", "")
        for signal in slot.get("signals", []) or []:
            scope_key = signal.get("scope_key", "")
            recommended_action = signal.get("recommended_action", "")
            if scope_key:
                affected_scopes.append(scope_key)
            if recommended_action:
                recommended_actions.append(recommended_action)

            signal_lines.append(
                "{pipeline}/{signal_id}: {summary} | scope={scope} | recommended_action={action}".format(
                    pipeline=pipeline_id,
                    signal_id=signal.get("id", ""),
                    summary=signal.get("summary", ""),
                    scope=scope_key or "n/a",
                    action=recommended_action or "review_required",
                )
            )

    affected_scopes = sorted(set(affected_scopes))
    recommended_actions = sorted(set(recommended_actions))

    status = overlay.get("status", "clear")
    recommended_default = overlay.get("recommended_default_hint", "new_run")

    prompt = build_pipeline_signals_review_prompt(
        status=status,
        signal_lines=signal_lines,
        affected_scopes=affected_scopes,
        recommended_actions=recommended_actions,
    )

    return {
        "pipeline_signals_review": {
            "schema_version": "0.1",
            "status": status,
            "recommended_default": recommended_default,
            "human_summary": (
                "Pipeline attention signal detected; review signals before opening a new run."
                if status == "attention"
                else "No pipeline attention signal is currently declared."
            ),
            "attention_signal_count": len(signal_lines),
            "attention_signals": signal_lines,
            "affected_scope_keys": affected_scopes,
            "recommended_actions": recommended_actions,
            "run_opening_authorized_by_signals": False,
            "run_materialization_authorized_by_signals": False,
            "recommended_prompt": prompt,
        }
    }


def build_pipeline_signals_review_prompt(
    *,
    status: str,
    signal_lines: list[str],
    affected_scopes: list[str],
    recommended_actions: list[str],
) -> str:
    if status != "attention":
        return (
            "Dans le repo learn-it, vérifie les signaux pipeline. "
            "Aucun signal d'attention n'est actuellement déclaré. "
            "Ne lance aucun run automatiquement."
        )

    signal_summary = "\n".join(f"- {line}" for line in signal_lines) or "- signal attention déclaré"
    scopes = ", ".join(affected_scopes) if affected_scopes else "non précisé"
    actions = ", ".join(recommended_actions) if recommended_actions else "revue humaine requise"

    return f"""Dans le repo learn-it, sur la branche feat/core-modularization-bootstrap,
analyse les signaux pipeline avant toute ouverture de run.

Lis en priorité :
- docs/pipelines/constitution/signals.yaml
- docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml
- docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
- docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml

Signal(s) à traiter :
{signal_summary}

Interprétation :
- scope(s) concerné(s) : {scopes}
- action recommandée par le signal : {actions}
- ce signal n'autorise pas l'ouverture d'un run
- ce signal n'autorise pas la matérialisation d'un run

Objectif :
proposer la prochaine décision humaine entre :
1. garder NO_ACTIVE_PHASE,
2. lancer une revue STAGE_00 / backlog review,
3. préparer un OPEN_NEW_RUN uniquement avec confirmation ou override humain explicite.

Contraintes :
- n'ouvre pas de run ;
- ne matérialise rien ;
- ne modifie pas policy.yaml, decisions.yaml, scope_catalog ou governance_backlog.yaml ;
- si un OPEN_NEW_RUN est envisagé, le preflight doit être explicitement pris en compte."""
