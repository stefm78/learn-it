#!/usr/bin/env python3
"""Registry-aware bootstrap launcher for pipeline prompt prebuilding.

Current candidate launcher.
Goals:
- low-context discovery
- synthetic entry menu
- next best actions
- actionable continue-run path
- scope maturity-aware action ranking and gating
- parallel-runs: N independent slots across all registered pipelines
- consolidation-ready detection: when all runs are closed and eligible,
  automatically propose STAGE_06B → STAGE_07 → STAGE_08 slot.

Maturity model reference:
  docs/transformations/core_modularization/CONSTITUTION_SCOPE_MATURITY_MODEL.md

  Score = sum of 6 axes (A1 to A6), each 0-4, total on 24.
  Displayed as percentage (0-100%) for human readability.
  Levels:
    L0_experimental   :  0-8   (  0% -  33%)
    L1_fragile        :  9-12  ( 37% -  50%)
    L2_usable_with_care: 13-16 ( 54% -  67%)
    L3_operational    : 17-20  ( 71% -  83%)
    L4_strong         : 21-24  ( 87% - 100%)
  Minimum for recommended parallel runs: L2_usable_with_care (>= 54%)
  Scores L0/L1 are gated: available=false in action menu.

Still experimental: kept in tmp/ until hardened and promoted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Maturity model constants (mirror of CONSTITUTION_SCOPE_MATURITY_MODEL.md)
# ---------------------------------------------------------------------------
MATURITY_AXES_COUNT = 6
MATURITY_MAX_SCORE = 24  # 6 axes x 4 points each
MATURITY_LEVELS: list[tuple[str, int, int]] = [
    # (level_key, min_score_inclusive, max_score_inclusive)
    ("L4_strong",              21, 24),
    ("L3_operational",         17, 20),
    ("L2_usable_with_care",    13, 16),
    ("L1_fragile",              9, 12),
    ("L0_experimental",         0,  8),
]
MATURITY_MINIMUM_LEVEL = "L2_usable_with_care"  # minimum for recommended runs
MATURITY_GATED_LEVELS = {"L0_experimental", "L1_fragile"}  # blocked in menu

# Stage order used to determine whether a run reached STAGE_06_CORE_VALIDATION.
# A run is consolidation-eligible if its current_stage is at or beyond this.
CONSOLIDATION_ELIGIBLE_STAGES = {
    "STAGE_06_CORE_VALIDATION",
    "STAGE_06B_CONSOLIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
    "STAGE_08_PROMOTE_CURRENT",
    "STAGE_09_CLOSEOUT_AND_ARCHIVE",
    "DONE",
}

# Seuil en secondes au-delà duquel un stage in_progress sans update est considéré
# comme potentiellement bloqué (6 heures).
_IN_PROGRESS_STALE_THRESHOLD_S = 6 * 3600


def maturity_pct(score: int) -> str:
    """Convert raw score to human-readable percentage string, e.g. '79%'."""
    return f"{round(score * 100 / MATURITY_MAX_SCORE)}%"


def maturity_level_from_score(score: int) -> str:
    for level_key, lo, hi in MATURITY_LEVELS:
        if lo <= score <= hi:
            return level_key
    return "L0_experimental"


def maturity_rank(level: str) -> int:
    """Higher = better. Used for sorting scopes by maturity descending."""
    for rank, (level_key, _, _) in enumerate(reversed(MATURITY_LEVELS)):
        if level_key == level:
            return rank
    return 0


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


# ---------------------------------------------------------------------------
# run_context availability probe
# ---------------------------------------------------------------------------

def probe_run_context(pipeline_root: Path, run_id: str) -> dict[str, Any]:
    """Check whether run_context.yaml and extracts are present for a run.

    Returns probe metadata AND — si run_context.yaml est present —
    l'etat de stage courant lu directement depuis run_context.yaml.
    run_context.yaml est toujours plus a jour que index.yaml car il est
    reconstruit automatiquement par update_run_tracking.py apres chaque update.
    """
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
        last_stage_status = rc.get("last_stage_status", "")
        current_stage_rc = rc.get("current_stage", "")
        next_stage_rc = rc.get("next_stage", "")

        if last_stage_status == "done" and next_stage_rc and next_stage_rc != current_stage_rc:
            probe["effective_current_stage"] = next_stage_rc
        else:
            probe["effective_current_stage"] = current_stage_rc

        probe["run_context_last_stage_status"] = last_stage_status
        probe["run_context_next_stage"] = next_stage_rc

    return probe


# ---------------------------------------------------------------------------
# Consolidation-ready detection
# ---------------------------------------------------------------------------

def probe_integration_gate(pipeline_root: Path, run_id: str) -> str:
    """Read integration_gate status for a run. Returns status string or 'missing'."""
    gate_path = pipeline_root / "runs" / run_id / "inputs" / "integration_gate.yaml"
    if not gate_path.exists():
        return "missing"
    gate = load_yaml(gate_path)
    status = (
        gate.get("integration_gate", {}).get("status")
        or gate.get("status", "missing")
    )
    return status or "missing"


def detect_consolidation_ready(
    pipeline_root: Path,
    active_runs: list[dict[str, Any]],
    closed_runs: list[dict[str, Any]],
    branch: str,
    pipeline_id: str,
) -> dict[str, Any] | None:
    """Detect whether the pipeline is in consolidation-ready state.

    Conditions:
    - active_runs is empty
    - At least one closed run is eligible (reached STAGE_06_CORE_VALIDATION+)
      and not abandoned
    - All eligible closed runs have integration_gate status cleared/not_applicable
      OR at least one has it open (still report, but flag pending_gates)

    Returns a consolidation_probe dict, or None if conditions not met.
    """
    if active_runs:
        return None

    eligible_runs: list[dict[str, Any]] = []
    for run in closed_runs:
        closure_mode = run.get("closure_mode", "")
        if closure_mode == "abandoned":
            continue
        current_stage = run.get("current_stage", "")
        if current_stage not in CONSOLIDATION_ELIGIBLE_STAGES:
            continue
        run_id = run.get("run_id", "")
        gate_status = probe_integration_gate(pipeline_root, run_id)
        eligible_runs.append({
            "run_id": run_id,
            "scope_key": run.get("scope_key", ""),
            "current_stage": current_stage,
            "integration_gate_status": gate_status,
        })

    if not eligible_runs:
        return None

    pending_gates = [
        r for r in eligible_runs
        if r["integration_gate_status"] not in ("cleared", "not_applicable")
    ]
    all_gates_cleared = len(pending_gates) == 0
    run_ids = [r["run_id"] for r in eligible_runs]

    # Build consolidation command
    runs_arg = " ".join(run_ids)
    consolidation_cmd = (
        f"python docs/patcher/shared/consolidate_parallel_runs.py "
        f"--runs {runs_arg} "
        f"--base docs/cores/current "
        f"--output docs/pipelines/{pipeline_id}/work/consolidation "
        f"--pipeline {pipeline_id}"
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
    )

    return {
        "consolidation_ready": True,
        "eligible_runs_count": len(eligible_runs),
        "eligible_runs": eligible_runs,
        "all_integration_gates_cleared": all_gates_cleared,
        "pending_gates": pending_gates,
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
) -> str:
    runs_list = ", ".join(run_ids)

    if not all_gates_cleared:
        pending_list = ", ".join(
            f"{r['run_id']} (gate={r['integration_gate_status']})"
            for r in pending_gates
        )
        gate_block = (
            f"ATTENTION : {len(pending_gates)} integration_gate(s) non cleared : {pending_list}. "
            f"Pour chaque run concerné, effectue la review des gate_checks dans "
            f"runs/<run_id>/inputs/integration_gate.yaml, marque chaque check "
            f"cleared: true et passe status: cleared. "
            f"Ensuite seulement, exécute la consolidation réelle. "
        )
    else:
        gate_block = "Toutes les integration_gates sont cleared. "

    return (
        f"Dans le repo learn-it, sur la branche {branch}, "
        f"tous les runs du pipeline {pipeline_id} sont clos. "
        f"Runs éligibles à la consolidation : {runs_list}. "
        f"{gate_block}"
        f"Étape 1 — Dry-run obligatoire : {consolidation_dry_run_cmd} "
        f"Étape 2 — Si dry-run PASS, consolidation réelle : {consolidation_cmd} "
        f"Étape 3 — Enchaîner STAGE_07_RELEASE_MATERIALIZATION sur work/consolidation/. "
        f"Étape 4 — Enchaîner STAGE_08_PROMOTE_CURRENT. "
        f"Ne saute aucune étape. Ne simule pas la consolidation. "
        f"Produis uniquement les fichiers sous docs/pipelines/{pipeline_id}/work/consolidation/ "
        f"et docs/cores/."
    )


# ---------------------------------------------------------------------------
# Abnormal state detection — bootstrap_command guard
# ---------------------------------------------------------------------------

def detect_abnormal_state(
    run: dict[str, Any],
    probe: dict[str, Any],
    run_manifest_path: Path,
) -> dict[str, Any] | None:
    """Retourne un dict décrivant l'anomalie détectée, ou None si l'état est sain.

    Anomalies détectées :
    1. run_status bloqué (blocked / failed)
    2. last_stage_status == in_progress et last_updated trop ancien
    3. Désynchronisation index.yaml vs run_context.yaml sur current_stage
    """
    import datetime as dt

    run_status = run.get("run_status", "")
    if run_status in ("blocked", "failed"):
        return {
            "reason": f"run_status={run_status}",
            "code": "run_status_abnormal",
        }

    # Lire execution_state depuis run_manifest si accessible
    if run_manifest_path.exists():
        manifest = load_yaml(run_manifest_path)
        exec_state = manifest.get("run_manifest", {}).get("execution_state", {})
        last_stage_status = exec_state.get("last_stage_status", "")
        last_updated_str = exec_state.get("last_updated", "")

        if last_stage_status == "in_progress" and last_updated_str:
            try:
                import datetime as dt2
                last_updated = dt2.datetime.fromisoformat(
                    last_updated_str.replace("Z", "+00:00")
                )
                age_s = (
                    dt2.datetime.now(dt2.timezone.utc) - last_updated
                ).total_seconds()
                if age_s > _IN_PROGRESS_STALE_THRESHOLD_S:
                    return {
                        "reason": f"stage in_progress depuis {int(age_s / 3600)}h sans update",
                        "code": "in_progress_stale",
                    }
            except ValueError:
                pass

    # Désynchronisation index.yaml vs run_context.yaml
    index_stage = run.get("current_stage", "")
    rc_stage = probe.get("effective_current_stage", "")
    rc_last_status = probe.get("run_context_last_stage_status", "")
    if (
        rc_stage
        and index_stage
        and rc_stage != index_stage
        and rc_last_status != "done"  # si done c'est normal, le fix corrige l'index
    ):
        return {
            "reason": f"désynchronisation index ({index_stage}) vs run_context ({rc_stage})",
            "code": "stage_desync",
        }

    return None


def build_bootstrap_command(
    pipeline_id: str,
    run_id: str,
    stage_id: str,
    run_status: str,
    anomaly: dict[str, Any],
) -> str:
    """Génère la bootstrap_command uniquement pour corriger un état anormal."""
    # Pour un run bloqué : reset vers active
    if anomaly["code"] == "run_status_abnormal":
        return (
            f"python docs/patcher/shared/update_run_tracking.py "
            f"--pipeline {pipeline_id} --run-id {run_id} "
            f"--stage-id {stage_id} --stage-status in_progress "
            f"--run-status active "
            f"--summary \"manual recovery from {anomaly['reason']}\""
        )
    # Pour un stage bloqué en vol : reset vers in_progress (idempotent)
    if anomaly["code"] == "in_progress_stale":
        return (
            f"python docs/patcher/shared/update_run_tracking.py "
            f"--pipeline {pipeline_id} --run-id {run_id} "
            f"--stage-id {stage_id} --stage-status in_progress "
            f"--run-status active "
            f"--summary \"reset stale in_progress — {anomaly['reason']}\""
        )
    # Pour une désynchronisation : rebuild run_context
    if anomaly["code"] == "stage_desync":
        return (
            f"python docs/patcher/shared/build_run_context.py "
            f"--pipeline {pipeline_id} --run-id {run_id}"
        )
    return ""


# ---------------------------------------------------------------------------
# Registry discovery
# ---------------------------------------------------------------------------

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
# Maturity enrichment
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
    return sorted(
        scopes,
        key=lambda s: (-s.get("maturity_score", 0), s.get("scope_key", "")),
    )


def build_maturity_summary(enriched_scopes: list[dict[str, Any]]) -> dict[str, Any]:
    available = [s for s in enriched_scopes if s["maturity_available_for_run"]]
    gated = [s for s in enriched_scopes if not s["maturity_available_for_run"]]
    return {
        "score_model": f"6 axes x 4 pts = {MATURITY_MAX_SCORE} pts max (displayed as %)",
        "levels_scale": [
            {
                "level": lvl,
                "range_pct": f"{round(lo * 100 / MATURITY_MAX_SCORE)}% - {round(hi * 100 / MATURITY_MAX_SCORE)}%",
            }
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


# ---------------------------------------------------------------------------
# Constitution pipeline discovery
# ---------------------------------------------------------------------------

def discover_constitution(repo_root: Path) -> dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / "constitution"
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    scope_catalog = load_yaml(pipeline_root / "scope_catalog" / "manifest.yaml")
    ai_protocol = load_yaml(pipeline_root / "AI_PROTOCOL.yaml")

    index_data = runs_index.get("runs_index", {})
    active_runs = index_data.get("active_runs", [])
    closed_runs = index_data.get("closed_runs", [])
    published_scopes_raw = scope_catalog.get("scope_catalog", {}).get("published_scopes", [])

    enriched_scopes = [enrich_scope_maturity(s) for s in published_scopes_raw]
    enriched_scopes = sort_scopes_by_maturity(enriched_scopes)
    maturity_summary = build_maturity_summary(enriched_scopes)

    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if "effective_current_stage" in probe and probe["effective_current_stage"]:
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        enriched_runs.append({**merged_run, "ids_first": probe})

    # --- Consolidation-ready detection ---
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

    if consolidation_probe and len(active_runs) == 0:
        # Consolidation takes priority over open_new_run when all runs are closed
        result.update(
            {
                "recommended_action": "consolidate",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": False,  # consolidate first
            }
        )
    elif len(active_runs) == 1:
        run = enriched_runs[0]
        other_scopes = [s for s in enriched_scopes if s.get("scope_key") != run.get("scope_key")]
        result.update(
            {
                "recommended_action": "continue_active_run",
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
                "recommended_action": "open_new_run",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in enriched_scopes),
            }
        )
    else:
        result.update(
            {
                "recommended_action": "disambiguate",
                "other_available_scopes": enriched_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in enriched_scopes),
            }
        )

    return result


def discover_generic_pipeline(repo_root: Path, pipeline_id: str) -> dict[str, Any]:
    """Discovery minimale pour les pipelines sans support étendu (release, migration, governance).

    Lit uniquement runs/index.yaml si présent, pas de scope catalog.
    """
    pipeline_root = repo_root / "docs" / "pipelines" / pipeline_id
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    active_runs = runs_index.get("runs_index", {}).get("active_runs", [])

    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if "effective_current_stage" in probe and probe["effective_current_stage"]:
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        enriched_runs.append({**merged_run, "ids_first": probe})

    recommended_action = "continue_active_run" if active_runs else "open_new_run"
    result: dict[str, Any] = {
        "pipeline_id": pipeline_id,
        "active_runs_count": len(active_runs),
        "active_runs": enriched_runs,
        "recommended_action": recommended_action,
        "published_scopes": [],  # non applicable hors constitution
    }
    if active_runs:
        run = enriched_runs[0]
        result["recommended_run_id"] = run.get("run_id", "")
        result["recommended_scope_key"] = run.get("scope_key", "")
        result["recommended_current_stage"] = run.get("current_stage", "")
        result["recommended_ids_first"] = run.get("ids_first", {})
    return result


# ---------------------------------------------------------------------------
# Stage prompt builders
# ---------------------------------------------------------------------------

def build_stage_prompt(
    branch: str,
    pipeline_id: str,
    pipeline_path: str,
    run_id: str,
    scope_key: str,
    current_stage: str,
    ids_first: dict[str, Any],
) -> str:
    """Build the stage_prompt for the AI, ids-first if run_context is ready."""
    ids_first_ready = ids_first.get("ids_first_ready", False)
    scope_extract_complete = ids_first.get("scope_extract_complete", False)

    if ids_first_ready:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline "
            f"{pipeline_path} au {current_stage} en mode run-aware "
            f"pour run_id={run_id}. "
            f"ORDRE DE LECTURE IDS-FIRST (obligatoire) : "
            f"1. runs/{run_id}/inputs/run_context.yaml (fichier synthétique — identité run, stage, IDs) ; "
            f"2. runs/{run_id}/inputs/scope_extract.yaml (entrées Core du scope uniquement) ; "
            f"3. runs/{run_id}/inputs/neighbor_extract.yaml (entrées Core voisinage). "
            f"Ne lis les Core complets (constitution.yaml, referentiel.yaml, link.yaml) "
            f"QUE si missing_ids est non vide dans les extraits. "
            f"Produis le livrable du stage uniquement sous runs/{run_id}/... "
            f"À la fin, donne la commande update_run_tracking.py de clôture du stage."
        )
    elif scope_extract_complete:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, avant de démarrer {current_stage} "
            f"pour run_id={run_id}, génère d'abord run_context.yaml manquant : "
            f"python docs/patcher/shared/build_run_context.py --run-id {run_id} "
            f"Ensuite applique l'ordre de lecture ids-first : "
            f"run_context.yaml → scope_extract.yaml → neighbor_extract.yaml. "
            f"Ne lis les Core complets que si missing_ids est non vide."
        )
    else:
        return (
            f"Dans le repo learn-it, sur la branche {branch}, les extraits ids-first sont absents "
            f"ou incomplets pour run_id={run_id}. "
            f"Exécute d'abord la séquence de matérialisation complète : "
            f"1. python docs/patcher/shared/materialize_run_inputs.py --run-id {run_id} ; "
            f"2. python docs/patcher/shared/extract_scope_slice.py --run-id {run_id} ; "
            f"3. python docs/patcher/shared/build_run_context.py --run-id {run_id} ; "
            f"Puis démarre {current_stage} en mode ids-first."
        )


def build_open_run_prompt(
    branch: str,
    pipeline_id: str,
    pipeline_path: str,
    scope_key: str,
    maturity_pct_str: str,
    maturity_level: str,
) -> str:
    return (
        f"Dans le repo learn-it, sur la branche {branch}, ouvre un nouveau run "
        f"sur le pipeline {pipeline_path} pour le scope {scope_key} "
        f"({maturity_pct_str} — {maturity_level}). "
        f"Résous uniquement l'ouverture du run selon docs/pipelines/{pipeline_id}/AI_PROTOCOL.yaml. "
        f"Ne démarre aucun stage avant confirmation."
    )


# ---------------------------------------------------------------------------
# Parallel slots builder
# ---------------------------------------------------------------------------

def build_parallel_slots(
    repo_root: Path,
    branch: str,
    pipelines: list[dict[str, str]],
    pipeline_states: dict[str, dict[str, Any]],
    n: int,
) -> dict[str, Any]:
    """Construit N slots parallèles indépendants, tous pipelines confondus.

    Priorité:
    1. Consolidation-ready (pipeline-level) — passe avant tout
    2. Runs actifs (continue) — triés par pipeline, puis par maturité scope décroissante
    3. Scopes sans run actif disponibles (open_new_run) — triés par maturité décroissante

    Chaque slot écrit/lit des fichiers strictement isolés (run_id distinct).
    bootstrap_command inclus uniquement si anomalie détectée.
    """
    slots: list[dict[str, Any]] = []
    slot_index = 0

    # --- Slot consolidation-ready (prioritaire, pipeline-level) ---
    for pipeline_info in pipelines:
        if slot_index >= n:
            break
        pid = pipeline_info.get("pipeline_id", "")
        state = pipeline_states.get(pid, {})
        consolidation_probe = state.get("consolidation_probe")
        if not consolidation_probe:
            continue
        if state.get("active_runs_count", 0) > 0:
            continue  # runs still active — don't propose consolidation yet

        slots.append({
            "slot": slot_index + 1,
            "pipeline_id": pid,
            "action": "consolidate",
            "eligible_runs": consolidation_probe.get("eligible_runs", []),
            "all_integration_gates_cleared": consolidation_probe.get("all_integration_gates_cleared", False),
            "pending_gates": consolidation_probe.get("pending_gates", []),
            "consolidation_dry_run_cmd": consolidation_probe.get("consolidation_dry_run_cmd", ""),
            "consolidation_cmd": consolidation_probe.get("consolidation_cmd", ""),
            "stage_prompt": consolidation_probe.get("stage_prompt", ""),
        })
        slot_index += 1

    # --- Slots continue (runs actifs) ---
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

            # Détection anomalie
            run_manifest_path = pipeline_root / "runs" / run_id / "run_manifest.yaml"
            probe = ids_first  # déjà calculé dans discover_*
            anomaly = detect_abnormal_state(run, probe, run_manifest_path)

            slot: dict[str, Any] = {
                "slot": slot_index + 1,
                "pipeline_id": pid,
                "action": "continue",
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
                "current_stage_source": run.get("current_stage_source", "index.yaml"),
                "ids_first_ready": ids_first.get("ids_first_ready", False),
                "stage_prompt": build_stage_prompt(
                    branch, pid, ppath, run_id, scope_key, current_stage, ids_first
                ),
            }

            if anomaly:
                slot["anomaly_detected"] = anomaly["reason"]
                slot["bootstrap_command"] = build_bootstrap_command(
                    pid, run_id, current_stage, run_status, anomaly
                )

            slots.append(slot)
            slot_index += 1

    # --- Slots open_new_run (scopes disponibles sans run actif) ---
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
            # Ne pas proposer open_new_run si consolidation en attente
            if state.get("consolidation_probe") and state.get("active_runs_count", 0) == 0:
                continue
            for scope in state.get("published_scopes", []):
                sk = scope.get("scope_key", "")
                if not scope.get("maturity_available_for_run", False):
                    continue
                if f"{pid}:{sk}" in active_run_scope_keys:
                    continue
                open_candidates.append({
                    "pipeline_id": pid,
                    "pipeline_path": ppath,
                    "scope_key": sk,
                    "maturity_score": scope.get("maturity_score", 0),
                    "maturity_level": scope.get("maturity_level", ""),
                    "maturity_pct": maturity_pct(scope.get("maturity_score", 0)),
                })

        open_candidates.sort(key=lambda x: -x["maturity_score"])

        for candidate in open_candidates:
            if slot_index >= n:
                break
            slots.append({
                "slot": slot_index + 1,
                "pipeline_id": candidate["pipeline_id"],
                "action": "open_new_run",
                "scope_key": candidate["scope_key"],
                "maturity_level": candidate["maturity_level"],
                "maturity_pct": candidate["maturity_pct"],
                "open_run_prompt": build_open_run_prompt(
                    branch,
                    candidate["pipeline_id"],
                    candidate["pipeline_path"],
                    candidate["scope_key"],
                    candidate["maturity_pct"],
                    candidate["maturity_level"],
                ),
            })
            slot_index += 1

    return {
        "parallel_slots_requested": n,
        "parallel_slots_available": len(slots),
        "parallelism_safe": True,
        "slots": slots,
    }


# ---------------------------------------------------------------------------
# Legacy single-pipeline menu builders (utilisés si --parallel-runs absent)
# ---------------------------------------------------------------------------

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


def build_continue_actions(branch: str, state: dict[str, Any], pipeline_path: str) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    ids_first = state.get("recommended_ids_first", {})
    other_scopes = state.get("other_available_scopes", [])
    other_scope_choices = [_scope_choice_entry(s) for s in other_scopes]
    pipeline_id = state.get("pipeline_id", "constitution")

    stage_prompt = build_stage_prompt(
        branch, pipeline_id, pipeline_path, run_id, scope_key, current_stage, ids_first
    )

    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "continue",
            "active_run": run_id,
            "active_scope": scope_key,
            "active_stage": current_stage,
            "ids_first_ready": ids_first.get("ids_first_ready", False),
        },
        "action_menu": [
            {
                "key": "continue",
                "label": "Continue active run",
                "available": True,
                "recommended": True,
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
                "ids_first_ready": ids_first.get("ids_first_ready", False),
            },
            {
                "key": "new_run",
                "label": "Open new run on another published scope",
                "available": bool(other_scope_choices),
                "recommended": False,
                "scope_choices": other_scope_choices,
                "reason_if_unavailable": "no_other_published_scope_available" if not other_scope_choices else "",
            },
            {
                "key": "inspect",
                "label": "Inspect current run state only",
                "available": True,
                "recommended": False,
                "run_id": run_id,
            },
        ],
        "next_best_actions": {
            "continue": {"stage_prompt": stage_prompt},
            "new_run": {
                "status": "available" if other_scope_choices else "unavailable_now",
                "scope_choices": other_scope_choices,
                "guidance": "publish_additional_scopes_first" if not other_scope_choices else "choose_a_scope_key_then_open_new_run",
            },
            "inspect": {
                "guidance": f"Read docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml and recent stage_completion records only.",
            },
        },
    }


def build_consolidate_actions(state: dict[str, Any]) -> dict[str, Any]:
    """Menu legacy pour le cas consolidate (active_runs == 0, consolidation_probe présent)."""
    pipeline_id = state.get("pipeline_id", "constitution")
    probe = state.get("consolidation_probe", {})
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "consolidate",
            "active_run": "",
            "active_scope": "pipeline-level",
            "active_stage": "STAGE_06B_CONSOLIDATION",
            "all_integration_gates_cleared": probe.get("all_integration_gates_cleared", False),
            "eligible_runs_count": probe.get("eligible_runs_count", 0),
        },
        "action_menu": [
            {
                "key": "consolidate",
                "label": "Run STAGE_06B consolidation then STAGE_07 and STAGE_08",
                "available": True,
                "recommended": True,
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
                "guidance": (
                    "clear_pending_integration_gates_first"
                    if probe.get("pending_gates")
                    else "run_dry_run_then_real_consolidation_then_07_then_08"
                ),
            }
        },
    }


def build_open_new_actions(branch: str, state: dict[str, Any], pipeline_path: str) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    all_scopes = state.get("published_scopes", [])
    scope_choices = [_scope_choice_entry(s) for s in all_scopes]
    available_choices = [c for c in scope_choices if c["available"]]
    gated_choices = [c for c in scope_choices if not c["available"]]

    entry_prompt = (
        f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline {pipeline_path}. "
        f"Pour l'instant, ne résous que l'ouverture d'un nouveau run selon docs/pipelines/{pipeline_id}/AI_PROTOCOL.yaml. "
        f"Scopes disponibles (triés par maturité décroissante): "
        + ", ".join(
            f"{c['scope_key']} ({c['maturity_pct']} — {c['maturity_level']})"
            for c in available_choices
        )
        + "."
    ) if available_choices else "Aucun scope disponible — publie des scopes d'abord."

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
                "recommended_scope": available_choices[0]["scope_key"] if available_choices else "",
            }
        ],
        "next_best_actions": {
            "new_run": {
                "status": "available" if available_choices else "unavailable_now",
                "scope_choices_available": available_choices,
                "scope_choices_gated": gated_choices,
                "guidance": "choose_a_scope_key_then_open_new_run" if available_choices else "publish_scopes_first",
                "entry_prompt": entry_prompt,
            }
        },
    }


def build_disambiguation_actions(branch: str, state: dict[str, Any], pipeline_path: str) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
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
                "guidance": "inspect runs/index.yaml only and ask for a short choice among active runs",
                "entry_prompt": (
                    f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline. "
                    f"Pour l'instant, ne résous que la désambiguïsation des runs actifs selon docs/pipelines/{pipeline_id}/AI_PROTOCOL.yaml."
                ),
            }
        },
    }


def build_menu(branch: str, state: dict[str, Any], pipeline_path: str) -> dict[str, Any]:
    action = state.get("recommended_action")
    if action == "consolidate":
        return build_consolidate_actions(state)
    if action == "continue_active_run":
        return build_continue_actions(branch, state, pipeline_path)
    if action == "open_new_run":
        return build_open_new_actions(branch, state, pipeline_path)
    return build_disambiguation_actions(branch, state, pipeline_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--branch", default="feat/core-modularization-bootstrap")
    parser.add_argument(
        "--parallel-runs",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Génère N slots de prompts parallèles indépendants, tous pipelines confondus. "
            "Chaque slot opère sur un run_id distinct — pas d'interférence possible. "
            "Les runs actifs sont proposés en premier (continue), "
            "puis les meilleurs scopes disponibles (open_new_run)."
        ),
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines_from_registry(registry_path)

    print("PIPELINE_REGISTRY_STATE:")
    print(yaml.safe_dump({"pipelines": pipelines}, sort_keys=False, allow_unicode=True).rstrip())
    print()

    # --- Mode parallel-runs : tous pipelines, N slots ---
    if args.parallel_runs is not None:
        pipeline_states: dict[str, dict[str, Any]] = {}
        for pipeline_info in pipelines:
            pid = pipeline_info.get("pipeline_id", "")
            if pid == "constitution":
                pipeline_states[pid] = discover_constitution(repo_root)
            else:
                pipeline_states[pid] = discover_generic_pipeline(repo_root, pid)

        parallel = build_parallel_slots(
            repo_root=repo_root,
            branch=args.branch,
            pipelines=pipelines,
            pipeline_states=pipeline_states,
            n=args.parallel_runs,
        )

        print("PIPELINE_PARALLEL_SLOTS:")
        print(yaml.safe_dump(parallel, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    # --- Mode legacy : pipeline unique ---
    pipeline_path = next(
        (p.get("path", "") for p in pipelines if p.get("pipeline_id") == args.pipeline),
        f"docs/pipelines/{args.pipeline}/pipeline.md",
    )

    if args.pipeline != "constitution":
        print("PIPELINE_LAUNCH_MENU:")
        print(yaml.safe_dump({
            "decision_summary": {
                "pipeline_id": args.pipeline,
                "recommended_default": "unsupported",
            },
            "action_menu": [],
            "next_best_actions": {
                "unsupported": {
                    "guidance": "use --parallel-runs to include all pipelines",
                }
            }
        }, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    state = discover_constitution(repo_root)
    menu = build_menu(args.branch, state, pipeline_path)

    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_MENU:")
    print(yaml.safe_dump(menu, sort_keys=False, allow_unicode=True).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
