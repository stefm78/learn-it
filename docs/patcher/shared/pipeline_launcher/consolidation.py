from __future__ import annotations

from pathlib import Path
from typing import Any

CONSOLIDATION_PENDING_STAGES = {
    "STAGE_06_CORE_VALIDATION",
    "STAGE_06B_CONSOLIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
}
_IN_PROGRESS_STALE_THRESHOLD_S = 6 * 3600

from .yaml_io import load_yaml

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
            f"Pour chaque run concerné, effectue la review des gate_checks dans docs/pipelines/{pipeline_id}/runs/<run_id>/inputs/integration_gate.yaml, "
            f"marque chaque check cleared: true et passe status: cleared. Ensuite seulement, exécute la promotion. "
        )
    else:
        gate_block = "Toutes les integration_gates sont cleared. "

    if is_solo_promote:
        run_id = run_ids[0]
        run_root = f"docs/pipelines/{pipeline_id}/runs/{run_id}"
        run_current_stage = eligible_runs[0]["current_stage"] if eligible_runs else ""
        if run_current_stage == "STAGE_07_RELEASE_MATERIALIZATION":
            next_step = (
                f"Étape unique — Exécuter STAGE_08_PROMOTE_CURRENT directement sur ce run : "
                f"lire {run_root}/outputs/ et promouvoir les artefacts vers docs/cores/current/. "
                f"Mettre à jour {run_root}/run_manifest.yaml (current_stage: STAGE_08_PROMOTE_CURRENT, done). "
                f"Produis uniquement les fichiers sous docs/cores/ et {run_root}/."
            )
        else:
            next_step = (
                f"Étape 1 — Exécuter STAGE_07_RELEASE_MATERIALIZATION sur ce run : lire {run_root}/outputs/ et matérialiser les release notes. "
                f"Étape 2 — Enchaîner STAGE_08_PROMOTE_CURRENT : promouvoir les artefacts vers docs/cores/current/. "
                f"Mettre à jour {run_root}/run_manifest.yaml à chaque étape. Produis uniquement les fichiers sous docs/cores/ et {run_root}/."
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
        f"Étape 3 — Enchaîner STAGE_07_RELEASE_MATERIALIZATION sur docs/pipelines/{pipeline_id}/work/consolidation/. "
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


