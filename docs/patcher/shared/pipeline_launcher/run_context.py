from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml

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

    neighbor_extract_complete = False
    if neighbor_extract_present:
        ne = load_yaml(neighbor_extract_path)
        missing = ne.get("neighbor_extract", {}).get("missing_ids", [])
        neighbor_extract_complete = len(missing) == 0

    probe: dict[str, Any] = {
        "run_context_present": run_context_present,
        "scope_extract_present": scope_extract_present,
        "scope_extract_complete": scope_extract_complete,
        "neighbor_extract_present": neighbor_extract_present,
        "neighbor_extract_complete": neighbor_extract_complete,
        "ids_first_ready": (
            run_context_present
            and scope_extract_present
            and neighbor_extract_present
            and scope_extract_complete
            and neighbor_extract_complete
        ),
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


def ensure_prompt_mentions_branch(prompt: str, branch: str) -> str:
    branch_marker = f"sur la branche {branch}"
    if branch_marker in prompt:
        return prompt
    repo_prefix = "Dans le repo learn-it,"
    if prompt.startswith(repo_prefix):
        return prompt.replace(repo_prefix, f"{repo_prefix} sur la branche {branch},", 1)
    return f"Dans le repo learn-it, sur la branche {branch}, {prompt}"


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
    neighbor_extract_complete = ids_first.get("neighbor_extract_complete", False)
    run_root = f"docs/pipelines/{pipeline_id}/runs/{run_id}"

    if terminal_closed or task_view_status == "terminal_closed":
        return (
            f"Le run {run_id} du pipeline {pipeline_id} est fermé sur un stage terminal ({current_stage}). "
            f"Ne propose pas de continue. Inspecte uniquement {run_root}/inputs/run_context.yaml, {run_root}/run_manifest.yaml et les reports si besoin."
        )
    if compact_execution_prompt and task_view_status == "executable":
        compact_execution_prompt = compact_execution_prompt.replace(
            "runs/<run_id>/", f"{run_root}/"
        )
        return ensure_prompt_mentions_branch(compact_execution_prompt, branch)

    if ids_first_ready:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline {pipeline_path} au {current_stage} en mode run-aware "
            f"pour run_id={run_id}. ORDRE DE LECTURE IDS-FIRST (obligatoire) : "
            f"1. {run_root}/inputs/run_context.yaml ; 2. {run_root}/inputs/scope_extract.yaml ; 3. {run_root}/inputs/neighbor_extract.yaml. "
            f"Ne lis les Core complets QUE si missing_ids est non vide dans les extraits. Produis le livrable du stage uniquement sous {run_root}/... "
            f"À la fin, donne la commande update_run_tracking.py de clôture du stage."
        )
    if scope_extract_complete and neighbor_extract_complete:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, avant de démarrer {current_stage} pour run_id={run_id}, génère d'abord run_context.yaml manquant : "
            f"python docs/patcher/shared/build_run_context.py --pipeline {pipeline_id} --run-id {run_id} Ensuite applique l'ordre de lecture ids-first : "
            f"{run_root}/inputs/run_context.yaml → {run_root}/inputs/scope_extract.yaml → {run_root}/inputs/neighbor_extract.yaml. Ne lis les Core complets que si missing_ids est non vide."
        )
    return (
        f"Dans le repo learn-it, sur la branche {branch}, les extraits ids-first sont absents ou incomplets pour run_id={run_id}. "
        f"Exécute d'abord la séquence de matérialisation complète : 1. python docs/patcher/shared/materialize_run_inputs.py --pipeline {pipeline_id} --run-id {run_id} ; "
        f"2. python docs/patcher/shared/extract_scope_slice.py --pipeline {pipeline_id} --run-id {run_id} ; 3. python docs/patcher/shared/build_run_context.py --pipeline {pipeline_id} --run-id {run_id} ; "
        f"Puis démarre {current_stage} en mode ids-first avec lecture sous {run_root}/inputs/."
    )


