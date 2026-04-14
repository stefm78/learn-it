#!/usr/bin/env python3
"""Registry-aware bootstrap launcher with runtime view + entry action contracts.

Compact prompt candidate:
- keeps --parallel-runs support
- consumes run_context.task_view when available
- avoids proposing continue on terminal closed runs
- loads canonical entry action contracts from docs/pipelines/<id>/entry_actions/
- renders compact entry prompts that reference the canonical contract + instance bindings

Scope of contract binding in this candidate:
- constitution entry actions only
- OPEN_NEW_RUN / CONTINUE_ACTIVE_RUN / DISAMBIGUATE / INSPECT / PARTITION_REFRESH

Still experimental: kept in tmp/ until hardened and promoted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

MATURITY_AXES_COUNT = 6
MATURITY_MAX_SCORE = 24
MATURITY_LEVELS: list[tuple[str, int, int]] = [
    ("L4_strong", 21, 24),
    ("L3_operational", 17, 20),
    ("L2_usable_with_care", 13, 16),
    ("L1_fragile", 9, 12),
    ("L0_experimental", 0, 8),
]
MATURITY_MINIMUM_LEVEL = "L2_usable_with_care"
MATURITY_GATED_LEVELS = {"L0_experimental", "L1_fragile"}
CONSOLIDATION_PENDING_STAGES = {
    "STAGE_06_CORE_VALIDATION",
    "STAGE_06B_CONSOLIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
}
_IN_PROGRESS_STALE_THRESHOLD_S = 6 * 3600


def maturity_pct(score: int) -> str:
    return f"{round(score * 100 / MATURITY_MAX_SCORE)}%"


def maturity_level_from_score(score: int) -> str:
    for level_key, lo, hi in MATURITY_LEVELS:
        if lo <= score <= hi:
            return level_key
    return "L0_experimental"


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def discover_pipelines_from_registry(registry_path: Path) -> list[dict[str, str]]:
    text = load_text(registry_path)
    lines = text.splitlines()
    pipelines: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if current:
                pipelines.append(current)
            current = {"pipeline_id": stripped[4:].strip()}
            continue
        if current and stripped.startswith("- Path:"):
            match = re.search(r"`([^`]+)`", stripped)
            if match:
                current["path"] = match.group(1)
        if current and stripped.startswith("- Canonical state:"):
            match = re.search(r"`([^`]+)`", stripped)
            if match:
                current["canonical_state"] = match.group(1)
        if current and stripped.startswith("- Goal:"):
            current["goal"] = stripped[len("- Goal:"):].strip()
    if current:
        pipelines.append(current)
    return pipelines


# ---------------------------------------------------------------------------
# Entry action contracts
# ---------------------------------------------------------------------------

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
    elif action_id == "CONTINUE_ACTIVE_RUN":
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


# ---------------------------------------------------------------------------
# run_context probe and active stage handling
# ---------------------------------------------------------------------------

def probe_run_context(pipeline_root: Path, run_id: str) -> dict[str, Any]:
    inputs_dir = pipeline_root / "runs" / run_id / "inputs"
    run_context_path = inputs_dir / "run_context.yaml"
    scope_extract_path = inputs_dir / "scope_extract.yaml"
    neighbor_extract_path = inputs_dir / "neighbor_extract.yaml"

    run_context_present = run_context_path.exists()
    scope_extract_present = scope_extract_path.exists()
    neighbor_extract_present = neighbor_extract_path.exists()

    scope_extract_complete = False
    if scope_extract_present:
        se = load_yaml(scope_extract_path)
        missing = se.get("scope_extract", {}).get("missing_ids", [])
        scope_extract_complete = len(missing) == 0

    probe: dict[str, Any] = {
        "run_context_present": run_context_present,
        "scope_extract_present": scope_extract_present,
        "scope_extract_complete": scope_extract_complete,
        "neighbor_extract_present": neighbor_extract_present,
        "ids_first_ready": run_context_present and scope_extract_present and scope_extract_complete,
    }

    if run_context_present:
        rc = load_yaml(run_context_path).get("run_context", {})
        task_view = rc.get("task_view", {}) or {}
        task_status = task_view.get("status", "")
        current_stage_rc = rc.get("current_stage", "")
        next_exec_canonical = rc.get("next_executable_stage_canonical", "")
        current_canonical = rc.get("current_stage_canonical", "")

        effective_current_stage = next_exec_canonical or current_canonical or current_stage_rc
        if task_status == "terminal_closed":
            effective_current_stage = next_exec_canonical or current_canonical or current_stage_rc

        probe.update(
            {
                "effective_current_stage": effective_current_stage,
                "run_context_last_stage_status": rc.get("last_stage_status", ""),
                "run_context_next_stage": rc.get("next_stage", ""),
                "task_view_present": bool(task_view),
                "task_view_status": task_status,
                "task_view": task_view,
                "terminal_closed": rc.get("terminal_closed", False),
                "next_executable_stage_canonical": next_exec_canonical,
                "current_stage_canonical": current_canonical,
                "compact_execution_prompt": task_view.get("compact_execution_prompt", ""),
            }
        )

    return probe


def build_stage_prompt(
    branch: str,
    pipeline_id: str,
    pipeline_path: str,
    run_id: str,
    scope_key: str,
    current_stage: str,
    ids_first: dict[str, Any],
) -> str:
    task_view_status = ids_first.get("task_view_status", "")
    compact_execution_prompt = ids_first.get("compact_execution_prompt", "")
    terminal_closed = ids_first.get("terminal_closed", False)
    ids_first_ready = ids_first.get("ids_first_ready", False)
    scope_extract_complete = ids_first.get("scope_extract_complete", False)

    if terminal_closed or task_view_status == "terminal_closed":
        return (
            f"Le run {run_id} du pipeline {pipeline_id} est fermé sur un stage terminal ({current_stage}). "
            f"Ne propose pas de continue. Inspecte uniquement run_context.yaml, run_manifest.yaml et les reports si besoin."
        )
    if compact_execution_prompt and task_view_status == "executable":
        return compact_execution_prompt
    if ids_first_ready:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline {pipeline_path} au {current_stage} en mode run-aware "
            f"pour run_id={run_id}. ORDRE DE LECTURE IDS-FIRST (obligatoire) : "
            f"1. runs/{run_id}/inputs/run_context.yaml ; 2. runs/{run_id}/inputs/scope_extract.yaml ; 3. runs/{run_id}/inputs/neighbor_extract.yaml. "
            f"Ne lis les Core complets QUE si missing_ids est non vide dans les extraits. Produis le livrable du stage uniquement sous runs/{run_id}/... "
            f"À la fin, donne la commande update_run_tracking.py de clôture du stage."
        )
    if scope_extract_complete:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, avant de démarrer {current_stage} pour run_id={run_id}, génère d'abord run_context.yaml manquant : "
            f"python docs/patcher/shared/build_run_context.py --run-id {run_id} Ensuite applique l'ordre de lecture ids-first : "
            f"run_context.yaml → scope_extract.yaml → neighbor_extract.yaml. Ne lis les Core complets que si missing_ids est non vide."
        )
    return (
        f"Dans le repo learn-it, sur la branche {branch}, les extraits ids-first sont absents ou incomplets pour run_id={run_id}. "
        f"Exécute d'abord la séquence de matérialisation complète : 1. python docs/patcher/shared/materialize_run_inputs.py --run-id {run_id} ; "
        f"2. python docs/patcher/shared/extract_scope_slice.py --run-id {run_id} ; 3. python docs/patcher/shared/build_run_context.py --run-id {run_id} ; "
        f"Puis démarre {current_stage} en mode ids-first."
    )


# ---------------------------------------------------------------------------
# Consolidation and anomaly helpers
# ---------------------------------------------------------------------------

def probe_integration_gate(pipeline_root: Path, run_id: str) -> str:
    gate_path = pipeline_root / "runs" / run_id / "inputs" / "integration_gate.yaml"
    if not gate_path.exists():
        return "missing"
    gate = load_yaml(gate_path)
    status = gate.get("integration_gate", {}).get("status") or gate.get("status", "missing")
    return status or "missing"


def detect_consolidation_ready(
    pipeline_root: Path,
    active_runs: list[dict[str, Any]],
    closed_runs: list[dict[str, Any]],
    branch: str,
    pipeline_id: str,
) -> dict[str, Any] | None:
    if active_runs:
        return None

    eligible_runs: list[dict[str, Any]] = []
    for run in closed_runs:
        closure_mode = run.get("closure_mode", "")
        if closure_mode == "abandoned":
            continue
        current_stage = run.get("current_stage", "")
        if current_stage not in CONSOLIDATION_PENDING_STAGES:
            continue
        run_id = run.get("run_id", "")
        gate_status = probe_integration_gate(pipeline_root, run_id)
        eligible_runs.append(
            {
                "run_id": run_id,
                "scope_key": run.get("scope_key", ""),
                "current_stage": current_stage,
                "integration_gate_status": gate_status,
            }
        )

    if not eligible_runs:
        return None

    pending_gates = [r for r in eligible_runs if r["integration_gate_status"] not in ("cleared", "not_applicable")]
    all_gates_cleared = len(pending_gates) == 0
    run_ids = [r["run_id"] for r in eligible_runs]
    is_solo_promote = len(eligible_runs) == 1

    if is_solo_promote:
        consolidation_cmd = ""
        consolidation_dry_run_cmd = ""
    else:
        runs_arg = " ".join(run_ids)
        consolidation_cmd = (
            f"python docs/patcher/shared/consolidate_parallel_runs.py "
            f"--runs {runs_arg} --base docs/cores/current "
            f"--output docs/pipelines/{pipeline_id}/work/consolidation --pipeline {pipeline_id}"
        )
        consolidation_dry_run_cmd = consolidation_cmd + " --dry-run"

    stage_prompt = _build_consolidation_stage_prompt(
        branch=branch,
        pipeline_id=pipeline_id,
        run_ids=run_ids,
        eligible_runs=eligible_runs,
        all_gates_cleared=all_gates_cleared,
        pending_gates=pending_gates,
        consolidation_dry_run_cmd=consolidation_dry_run_cmd,
        consolidation_cmd=consolidation_cmd,
        is_solo_promote=is_solo_promote,
    )

    return {
        "consolidation_ready": True,
        "eligible_runs_count": len(eligible_runs),
        "eligible_runs": eligible_runs,
        "all_integration_gates_cleared": all_gates_cleared,
        "pending_gates": pending_gates,
        "is_solo_promote": is_solo_promote,
        "consolidation_dry_run_cmd": consolidation_dry_run_cmd,
        "consolidation_cmd": consolidation_cmd,
        "stage_prompt": stage_prompt,
    }


def _build_consolidation_stage_prompt(
    branch: str,
    pipeline_id: str,
    run_ids: list[str],
    eligible_runs: list[dict[str, Any]],
    all_gates_cleared: bool,
    pending_gates: list[dict[str, Any]],
    consolidation_dry_run_cmd: str,
    consolidation_cmd: str,
    is_solo_promote: bool = False,
) -> str:
    runs_list = ", ".join(run_ids)
    if not all_gates_cleared:
        pending_list = ", ".join(
            f"{r['run_id']} (gate={r['integration_gate_status']})" for r in pending_gates
        )
        gate_block = (
            f"ATTENTION : {len(pending_gates)} integration_gate(s) non cleared : {pending_list}. "
            f"Pour chaque run concerné, effectue la review des gate_checks dans runs/<run_id>/inputs/integration_gate.yaml, "
            f"marque chaque check cleared: true et passe status: cleared. Ensuite seulement, exécute la promotion. "
        )
    else:
        gate_block = "Toutes les integration_gates sont cleared. "

    if is_solo_promote:
        run_id = run_ids[0]
        run_current_stage = eligible_runs[0]["current_stage"] if eligible_runs else ""
        if run_current_stage == "STAGE_07_RELEASE_MATERIALIZATION":
            next_step = (
                f"Étape unique — Exécuter STAGE_08_PROMOTE_CURRENT directement sur ce run : "
                f"lire runs/{run_id}/outputs/ et promouvoir les artefacts vers docs/cores/current/. "
                f"Mettre à jour runs/{run_id}/run_manifest.yaml (current_stage: STAGE_08_PROMOTE_CURRENT, done). "
                f"Produis uniquement les fichiers sous docs/cores/ et runs/{run_id}/."
            )
        else:
            next_step = (
                f"Étape 1 — Exécuter STAGE_07_RELEASE_MATERIALIZATION sur ce run : lire runs/{run_id}/outputs/ et matérialiser les release notes. "
                f"Étape 2 — Enchaîner STAGE_08_PROMOTE_CURRENT : promouvoir les artefacts vers docs/cores/current/. "
                f"Mettre à jour runs/{run_id}/run_manifest.yaml à chaque étape. Produis uniquement les fichiers sous docs/cores/ et runs/{run_id}/."
            )
        return (
            f"Dans le repo learn-it, sur la branche {branch}, le run {run_id} du pipeline {pipeline_id} est clos à {run_current_stage} "
            f"(run solo — pas de consolidation parallèle nécessaire). {gate_block}"
            f"Ne lance pas consolidate_parallel_runs.py (script multi-runs uniquement). {next_step}"
        )

    return (
        f"Dans le repo learn-it, sur la branche {branch}, tous les runs du pipeline {pipeline_id} sont clos. "
        f"Runs éligibles à la consolidation : {runs_list}. {gate_block}"
        f"Étape 1 — Dry-run obligatoire : {consolidation_dry_run_cmd} "
        f"Étape 2 — Si dry-run PASS, consolidation réelle : {consolidation_cmd} "
        f"Étape 3 — Enchaîner STAGE_07_RELEASE_MATERIALIZATION sur work/consolidation/. "
        f"Étape 4 — Enchaîner STAGE_08_PROMOTE_CURRENT. Ne saute aucune étape. Ne simule pas la consolidation. "
        f"Produis uniquement les fichiers sous docs/pipelines/{pipeline_id}/work/consolidation/ et docs/cores/."
    )


def detect_abnormal_state(
    run: dict[str, Any], probe: dict[str, Any], run_manifest_path: Path
) -> dict[str, Any] | None:
    run_status = run.get("run_status", "")
    if run_status in ("blocked", "failed"):
        return {"reason": f"run_status={run_status}", "code": "run_status_abnormal"}

    if run_manifest_path.exists():
        manifest = load_yaml(run_manifest_path)
        exec_state = manifest.get("run_manifest", {}).get("execution_state", {})
        last_stage_status = exec_state.get("last_stage_status", "")
        last_updated_str = exec_state.get("last_updated", "")
        if last_stage_status == "in_progress" and last_updated_str:
            try:
                import datetime as dt2
                last_updated = dt2.datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
                age_s = (dt2.datetime.now(dt2.timezone.utc) - last_updated).total_seconds()
                if age_s > _IN_PROGRESS_STALE_THRESHOLD_S:
                    return {
                        "reason": f"stage in_progress depuis {int(age_s / 3600)}h sans update",
                        "code": "in_progress_stale",
                    }
            except ValueError:
                pass

    index_stage = run.get("current_stage", "")
    rc_stage = probe.get("effective_current_stage", "")
    rc_last_status = probe.get("run_context_last_stage_status", "")
    if rc_stage and index_stage and rc_stage != index_stage and rc_last_status != "done":
        return {
            "reason": f"désynchronisation index ({index_stage}) vs run_context ({rc_stage})",
            "code": "stage_desync",
        }
    return None


def build_bootstrap_command(
    pipeline_id: str, run_id: str, stage_id: str, run_status: str, anomaly: dict[str, Any]
) -> str:
    if anomaly["code"] == "run_status_abnormal":
        return (
            f"python docs/patcher/shared/update_run_tracking.py --pipeline {pipeline_id} --run-id {run_id} "
            f"--stage-id {stage_id} --stage-status in_progress --run-status active "
            f"--summary \"manual recovery from {anomaly['reason']}\""
        )
    if anomaly["code"] == "in_progress_stale":
        return (
            f"python docs/patcher/shared/update_run_tracking.py --pipeline {pipeline_id} --run-id {run_id} "
            f"--stage-id {stage_id} --stage-status in_progress --run-status active "
            f"--summary \"reset stale in_progress — {anomaly['reason']}\""
        )
    if anomaly["code"] == "stage_desync":
        return f"python docs/patcher/shared/build_run_context.py --pipeline {pipeline_id} --run-id {run_id}"
    return ""


# ---------------------------------------------------------------------------
# Pipeline state discovery
# ---------------------------------------------------------------------------

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

    enriched_scopes = sort_scopes_by_maturity([enrich_scope_maturity(s) for s in published_scopes_raw])
    maturity_summary = build_maturity_summary(enriched_scopes)

    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if probe.get("effective_current_stage"):
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        merged_run["task_view_status"] = probe.get("task_view_status", "")
        merged_run["terminal_closed"] = probe.get("terminal_closed", False)
        merged_run["compact_execution_prompt"] = probe.get("compact_execution_prompt", "")
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
            merged_run["current_stage"] = probe["effective_current_STAGE"]
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


def _scope_choice_entry(s: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "scope_key": s["scope_key"],
        "maturity_pct": maturity_pct(s["maturity_score"]),
        "maturity_level": s["maturity_level"],
        "available": s["maturity_available_for_run"],
    }
    if not s["maturity_available_for_run"]:
        entry["gate_reason"] = s["maturity_gate_reason"]
    return entry


def build_continue_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    ids_first = state.get("recommended_ids_first", {})
    other_scopes = state.get("other_available_scopes", [])
    other_scope_choices = [_scope_choice_entry(s) for s in other_scopes]
    pipeline_id = state.get("pipeline_id", "constitution")
    continue_available = ids_first.get("task_view_status") != "terminal_closed"

    entry_prompt = render_entry_action_prompt(
        repo_root,
        branch=branch,
        pipeline_id=pipeline_id,
        pipeline_path=pipeline_path,
        action_id="CONTINUE_ACTIVE_RUN",
        bindings={
            "run_id": run_id,
            "scope_key": scope_key,
            "current_stage": current_stage,
        },
    )
    stage_prompt = build_stage_prompt(
        branch, pipeline_id, pipeline_path, run_id, scope_key, current_stage, ids_first
    )

    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "continue" if continue_available else "inspect",
            "active_run": run_id,
            "active_scope": scope_key,
            "active_stage": current_stage,
            "ids_first_ready": ids_first.get("ids_first_ready", False),
            "task_view_status": ids_first.get("task_view_status", ""),
        },
        "action_menu": [
            {
                "key": "continue",
                "label": "Continue active run",
                "available": continue_available,
                "recommended": continue_available,
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
            },
            {
                "key": "new_run",
                "label": "Open new run on another published scope",
                "available": bool(other_scope_choices),
                "recommended": False,
                "scope_choices": other_scope_choices,
            },
            {
                "key": "inspect",
                "label": "Inspect current run state only",
                "available": True,
                "recommended": not continue_available,
                "run_id": run_id,
            },
        ],
        "next_best_actions": {
            "continue": {
                "entry_prompt": entry_prompt,
                "stage_prompt": stage_prompt,
                "status": "available" if continue_available else "unavailable_terminal_closed",
            },
            "new_run": {
                "status": "available" if other_scope_choices else "unavailable_now",
                "scope_choices": other_scope_choices,
            },
            "inspect": {
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pipeline_id,
                    pipeline_path=pipeline_path,
                    action_id="INSPECT",
                    bindings={"run_id": run_id},
                )
            },
        },
    }


def build_open_new_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    all_scopes = state.get("published_scopes", [])
    scope_choices = [_scope_choice_entry(s) for s in all_scopes]
    available_choices = [c for c in scope_choices if c["available"]]
    gated_choices = [c for c in scope_choices if not c["available"]]
    top_choice = available_choices[0] if available_choices else {}
    entry_prompt = (
        render_entry_action_prompt(
            repo_root,
            branch=branch,
            pipeline_id=pipeline_id,
            pipeline_path=pipeline_path,
            action_id="OPEN_NEW_RUN",
            bindings={
                "scope_key": top_choice.get("scope_key", ""),
                "maturity_pct": top_choice.get("maturity_pct", ""),
                "maturity_level": top_choice.get("maturity_level", ""),
            },
        )
        if available_choices
        else "Aucun scope disponible — publie des scopes d'abord."
    )
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "new_run",
            "active_run": "",
            "active_scope": "",
            "active_stage": "",
        },
        "action_menu": [
            {
                "key": "new_run",
                "label": "Open new run on a published scope",
                "available": bool(available_choices),
                "recommended": True,
                "scope_choices": scope_choices,
                "recommended_scope": top_choice.get("scope_key", ""),
            }
        ],
        "next_best_actions": {
            "new_run": {
                "status": "available" if available_choices else "unavailable_now",
                "scope_choices_available": available_choices,
                "scope_choices_gated": gated_choices,
                "entry_prompt": entry_prompt,
            }
        },
    }


def build_disambiguation_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    shortlist = [f"{r.get('run_id','')}:{r.get('scope_key','')}:{r.get('current_stage','')}" for r in state.get("active_runs", [])]
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "disambiguate",
            "active_run": "multiple",
            "active_scope": "multiple",
            "active_stage": "multiple",
        },
        "action_menu": [
            {
                "key": "disambiguate",
                "label": "Choose one active run before any deep read",
                "available": True,
                "recommended": True,
            }
        ],
        "next_best_actions": {
            "disambiguate": {
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pipeline_id,
                    pipeline_path=pipeline_path,
                    action_id="DISAMBIGUATE",
                    bindings={"active_runs_shortlist": shortlist},
                )
            }
        },
    }


def build_consolidate_actions(state: dict[str, Any]) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    probe = state.get("consolidation_probe", {})
    is_solo_promote = probe.get("is_solo_promote", False)
    active_stage = "STAGE_08_PROMOTE_CURRENT" if is_solo_promote else "STAGE_06B_CONSOLIDATION"
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "consolidate",
            "active_run": "",
            "active_scope": "pipeline-level",
            "active_stage": active_stage,
            "is_solo_promote": is_solo_promote,
            "all_integration_gates_cleared": probe.get("all_integration_gates_cleared", False),
            "eligible_runs_count": probe.get("eligible_runs_count", 0),
        },
        "action_menu": [
            {
                "key": "consolidate",
                "label": "Run STAGE_08_PROMOTE_CURRENT (solo run)" if is_solo_promote else "Run STAGE_06B consolidation then STAGE_07 and STAGE_08",
                "available": True,
                "recommended": True,
                "is_solo_promote": is_solo_promote,
                "eligible_runs": probe.get("eligible_runs", []),
                "all_gates_cleared": probe.get("all_integration_gates_cleared", False),
                "pending_gates": probe.get("pending_gates", []),
            }
        ],
        "next_best_actions": {
            "consolidate": {
                "consolidation_dry_run_cmd": probe.get("consolidation_dry_run_cmd", ""),
                "consolidation_cmd": probe.get("consolidation_cmd", ""),
                "stage_prompt": probe.get("stage_prompt", ""),
                "guidance": "clear_pending_integration_gates_first" if probe.get("pending_gates") else ("run_stage_08_promote_current_directly" if is_solo_promote else "run_dry_run_then_real_consolidation_then_07_then_08"),
            }
        },
    }


def build_menu(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    action = state.get("recommended_action")
    if action == "consolidate":
        return build_consolidate_actions(state)
    if action == "CONTINUE_ACTIVE_RUN":
        return build_continue_actions(repo_root, branch, state, pipeline_path)
    if action == "OPEN_NEW_RUN":
        return build_open_new_actions(repo_root, branch, state, pipeline_path)
    return build_disambiguation_actions(repo_root, branch, state, pipeline_path)


def build_parallel_slots(
    repo_root: Path,
    branch: str,
    pipelines: list[dict[str, str]],
    pipeline_states: dict[str, dict[str, Any]],
    n: int,
) -> dict[str, Any]:
    slots: list[dict[str, Any]] = []
    slot_index = 0
    pipelines_with_consolidation_slot: set[str] = set()

    for pipeline_info in pipelines:
        if slot_index >= n:
            break
        pid = pipeline_info.get("pipeline_id", "")
        state = pipeline_states.get(pid, {})
        consolidation_probe = state.get("consolidation_probe")
        if not consolidation_probe:
            continue
        if state.get("active_runs_count", 0) > 0:
            continue
        slots.append(
            {
                "slot": slot_index + 1,
                "pipeline_id": pid,
                "action": "consolidate",
                "is_solo_promote": consolidation_probe.get("is_solo_promote", False),
                "eligible_runs": consolidation_probe.get("eligible_runs", []),
                "all_integration_gates_cleared": consolidation_probe.get("all_integration_gates_cleared", False),
                "pending_gates": consolidation_probe.get("pending_gates", []),
                "consolidation_dry_run_cmd": consolidation_probe.get("consolidation_dry_run_cmd", ""),
                "consolidation_cmd": consolidation_probe.get("consolidation_cmd", ""),
                "stage_prompt": consolidation_probe.get("stage_prompt", ""),
            }
        )
        pipelines_with_consolidation_slot.add(pid)
        slot_index += 1

    for pipeline_info in pipelines:
        pid = pipeline_info.get("pipeline_id", "")
        ppath = pipeline_info.get("path", f"docs/pipelines/{pid}/pipeline.md")
        state = pipeline_states.get(pid, {})
        active_runs = state.get("active_runs", [])
        pipeline_root = repo_root / "docs" / "pipelines" / pid

        for run in active_runs:
            if slot_index >= n:
                break
            run_id = run.get("run_id", "")
            scope_key = run.get("scope_key", "")
            current_stage = run.get("current_stage", "")
            ids_first = run.get("ids_first", {})
            run_status = run.get("run_status", "active")

            if ids_first.get("task_view_status") == "terminal_closed":
                continue

            run_manifest_path = pipeline_root / "runs" / run_id / "run_manifest.yaml"
            anomaly = detect_abnormal_state(run, ids_first, run_manifest_path)
            slot: dict[str, Any] = {
                "slot": slot_index + 1,
                "pipeline_id": pid,
                "action": "continue",
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
                "current_stage_source": run.get("current_stage_source", "index.yaml"),
                "ids_first_ready": ids_first.get("ids_first_ready", False),
                "task_view_status": ids_first.get("task_view_status", ""),
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pid,
                    pipeline_path=ppath,
                    action_id="CONTINUE_ACTIVE_RUN",
                    bindings={
                        "run_id": run_id,
                        "scope_key": scope_key,
                        "current_stage": current_stage,
                    },
                ) if pid == "constitution" else "",
                "stage_prompt": build_stage_prompt(branch, pid, ppath, run_id, scope_key, current_stage, ids_first),
            }
            if anomaly:
                slot["anomaly_detected"] = anomaly["reason"]
                slot["bootstrap_command"] = build_bootstrap_command(pid, run_id, current_stage, run_status, anomaly)
            slots.append(slot)
            slot_index += 1

    if slot_index < n:
        active_run_scope_keys: set[str] = set()
        for pid, state in pipeline_states.items():
            for run in state.get("active_runs", []):
                sk = run.get("scope_key", "")
                if sk:
                    active_run_scope_keys.add(f"{pid}:{sk}")

        open_candidates: list[dict[str, Any]] = []
        for pipeline_info in pipelines:
            pid = pipeline_info.get("pipeline_id", "")
            ppath = pipeline_info.get("path", f"docs/pipelines/{pid}/pipeline.md")
            state = pipeline_states.get(pid, {})
            has_consolidation_slot = pid in pipelines_with_consolidation_slot
            if state.get("consolidation_probe") and not has_consolidation_slot:
                continue
            for scope in state.get("published_scopes", []):
                sk = scope.get("scope_key", "")
                if not scope.get("maturity_available_for_run", False):
                    continue
                if f"{pid}:{sk}" in active_run_scope_keys:
                    continue
                candidate: dict[str, Any] = {
                    "pipeline_id": pid,
                    "pipeline_path": ppath,
                    "scope_key": sk,
                    "maturity_score": scope.get("maturity_score", 0),
                    "maturity_level": scope.get("maturity_level", ""),
                    "maturity_pct": maturity_pct(scope.get("maturity_score", 0)),
                }
                if has_consolidation_slot:
                    candidate["parallel_with_consolidation"] = True
                open_candidates.append(candidate)
        open_candidates.sort(key=lambda x: -x["maturity_score"])

        for candidate in open_candidates:
            if slot_index >= n:
                break
            slot_entry: dict[str, Any] = {
                "slot": slot_index + 1,
                "pipeline_id": candidate["pipeline_id"],
                "action": "open_new_run",
                "scope_key": candidate["scope_key"],
                "maturity_level": candidate["maturity_level"],
                "maturity_pct": candidate["maturity_pct"],
                "open_run_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=candidate["pipeline_id"],
                    pipeline_path=candidate["pipeline_path"],
                    action_id="OPEN_NEW_RUN",
                    bindings={
                        "scope_key": candidate["scope_key"],
                        "maturity_pct": candidate["maturity_pct"],
                        "maturity_level": candidate["maturity_level"],
                    },
                ) if candidate["pipeline_id"] == "constitution" else (
                    f"Dans le repo learn-it, sur la branche {branch}, ouvre un nouveau run sur le pipeline {candidate['pipeline_path']} pour le scope {candidate['scope_key']} ({candidate['maturity_pct']} — {candidate['maturity_level']})."
                ),
            }
            if candidate.get("parallel_with_consolidation"):
                slot_entry["parallel_with_consolidation"] = True
                slot_entry["isolation_note"] = (
                    "Ce run s'exécute en parallèle d'une consolidation en cours sur ce pipeline. "
                    "Il doit produire ses livrables uniquement sous runs/<new_run_id>/. "
                    "Ne pas toucher docs/cores/current avant que la consolidation soit terminée."
                )
            slots.append(slot_entry)
            slot_index += 1

    return {
        "parallel_slots_requested": n,
        "parallel_slots_available": len(slots),
        "parallelism_safe": True,
        "slots": slots,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--branch", default="feat/core-modularization-bootstrap")
    parser.add_argument("--parallel-runs", type=int, default=None, metavar="N")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines_from_registry(registry_path)

    print("PIPELINE_REGISTRY_STATE:")
    print(yaml.safe_dump({"pipelines": pipelines}, sort_keys=False, allow_unicode=True).rstrip())
    print()

    if args.parallel_runs is not None:
        pipeline_states: dict[str, dict[str, Any]] = {}
        for pipeline_info in pipelines:
            pid = pipeline_info.get("pipeline_id", "")
            if pid == "constitution":
                pipeline_states[pid] = discover_constitution(repo_root)
            else:
                pipeline_states[pid] = discover_generic_pipeline(repo_root, pid)
        parallel = build_parallel_slots(repo_root=repo_root, branch=args.branch, pipelines=pipelines, pipeline_states=pipeline_states, n=args.parallel_runs)
        print("PIPELINE_PARALLEL_SLOTS:")
        print(yaml.safe_dump(parallel, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    pipeline_path = next((p.get("path", "") for p in pipelines if p.get("pipeline_id") == args.pipeline), f"docs/pipelines/{args.pipeline}/pipeline.md")
    if args.pipeline != "constitution":
        print("PIPELINE_LAUNCH_MENU:")
        print(yaml.safe_dump({
            "decision_summary": {"pipeline_id": args.pipeline, "recommended_default": "unsupported"},
            "action_menu": [],
            "next_best_actions": {"unsupported": {"guidance": "use constitution entry action contracts pattern as template"}},
        }, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    state = discover_constitution(repo_root)
    menu = build_menu(repo_root, args.branch, state, pipeline_path)
    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_MENU:")
    print(yaml.safe_dump(menu, sort_keys=False, allow_unicode=True).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
