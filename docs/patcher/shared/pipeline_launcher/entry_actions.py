from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml
from .governance_backlog import compact_governance_backlog_signal
from .bounded_preflight import compact_bounded_run_preflight_signal

def load_entry_actions_index(repo_root: Path, pipeline_id: str) -> dict[str, Any]:
    path = repo_root / "docs" / "pipelines" / pipeline_id / "entry_actions" / "ENTRY_ACTIONS_INDEX.yaml"
    return load_yaml(path).get("entry_actions_index", {})


def load_entry_action_contract(repo_root: Path, pipeline_id: str, action_id: str) -> dict[str, Any]:
    index = load_entry_actions_index(repo_root, pipeline_id)
    for action in index.get("entry_actions", []) or []:
        if action.get("action_id") == action_id:
            ref = action.get("ref", "")
            if ref:
                return load_yaml(repo_root / ref).get("entry_action", {})
    return {}


def resolve_entry_action_ref(repo_root: Path, pipeline_id: str, action_id: str) -> str:
    index = load_entry_actions_index(repo_root, pipeline_id)
    for action in index.get("entry_actions", []) or []:
        if action.get("action_id") == action_id:
            return action.get("ref", "")
    return ""


def render_entry_action_prompt(
    repo_root: Path,
    *,
    branch: str,
    pipeline_id: str,
    pipeline_path: str,
    action_id: str,
    bindings: dict[str, Any],
) -> str:
    action_ref = resolve_entry_action_ref(repo_root, pipeline_id, action_id)
    contract = load_entry_action_contract(repo_root, pipeline_id, action_id)
    if not action_ref or not contract:
        return f"No entry action contract found for {pipeline_id}:{action_id}."

    protocol_anchor = contract.get(
        "entry_binding", {}
    ).get("protocol_anchor", f"docs/pipelines/{pipeline_id}/AI_PROTOCOL.yaml")
    stop_after_decision = contract.get("entry_binding", {}).get("stop_after_decision", True)

    instance_parts: list[str] = [f"pipeline={pipeline_path}"]
    if action_id == "OPEN_NEW_RUN":
        instance_parts.append(f"target_scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"target_scope_maturity_pct={bindings.get('maturity_pct', '')}")
        instance_parts.append(f"target_scope_maturity_level={bindings.get('maturity_level', '')}")
        instance_parts.append(
            "governance_backlog_signal="
            + compact_governance_backlog_signal(bindings.get("governance_backlog_signal", {}))
        )
        instance_parts.append(
            "bounded_run_preflight_signal="
            + compact_bounded_run_preflight_signal(bindings.get("bounded_run_preflight_signal", {}))
        )
    elif action_id == "CONTINUE_ACTIVE_RUN":
        instance_parts.append(f"run_id={bindings.get('run_id', '')}")
        instance_parts.append(f"scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"current_stage={bindings.get('current_stage', '')}")
    elif action_id == "RECONCILE_RUN":
        instance_parts.append(f"run_id={bindings.get('run_id', '')}")
        instance_parts.append(f"scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"current_stage={bindings.get('current_stage', '')}")
    elif action_id == "DISAMBIGUATE":
        shortlist = bindings.get("active_runs_shortlist", []) or []
        if shortlist:
            instance_parts.append("active_runs_shortlist=" + ", ".join(shortlist))
    elif action_id == "INSPECT":
        if bindings.get("run_id"):
            instance_parts.append(f"run_id={bindings.get('run_id', '')}")
    elif action_id == "PARTITION_REFRESH":
        instance_parts.append("mode=partition_refresh")

    stop_clause = "Arrête-toi après la décision d'entrée." if stop_after_decision else "Respecte la condition d'arrêt du contrat."

    return (
        f"Dans le repo learn-it, sur la branche {branch}, résous l'action d'entrée {action_id} du pipeline {pipeline_id} "
        f"en appliquant strictement le contrat canonique {action_ref}. "
        f"Ancre de protocole: {protocol_anchor}. "
        f"Bindings d'instance: {' ; '.join(instance_parts)}. "
        f"Ne déplie pas le contrat, ne l'étends pas, ne lis rien hors de sa surface autorisée. "
        f"{stop_clause}"
    )


