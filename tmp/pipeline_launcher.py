#!/usr/bin/env python3
"""Registry-aware bootstrap launcher for pipeline prompt prebuilding.

Current candidate launcher.
Goals:
- low-context discovery
- synthetic entry menu
- next best actions
- actionable continue-run path
- scope maturity-aware action ranking and gating

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
    """Check whether run_context.yaml and extracts are present for a run."""
    inputs_dir = pipeline_root / "runs" / run_id / "inputs"
    run_context_path = inputs_dir / "run_context.yaml"
    scope_extract_path = inputs_dir / "scope_extract.yaml"
    neighbor_extract_path = inputs_dir / "neighbor_extract.yaml"

    run_context_present = run_context_path.exists()
    scope_extract_present = scope_extract_path.exists()
    neighbor_extract_present = neighbor_extract_path.exists()

    # Check missing_ids in scope_extract
    scope_extract_complete = False
    if scope_extract_present:
        se = load_yaml(scope_extract_path)
        missing = se.get("scope_extract", {}).get("missing_ids", [])
        scope_extract_complete = len(missing) == 0

    return {
        "run_context_present": run_context_present,
        "scope_extract_present": scope_extract_present,
        "scope_extract_complete": scope_extract_complete,
        "neighbor_extract_present": neighbor_extract_present,
        "ids_first_ready": run_context_present and scope_extract_present and scope_extract_complete,
    }


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

    if current:
        pipelines.append(current)
    return pipelines


# ---------------------------------------------------------------------------
# Maturity enrichment
# ---------------------------------------------------------------------------

def enrich_scope_maturity(scope_record: dict[str, Any]) -> dict[str, Any]:
    """Return an enriched copy of a scope record with full maturity annotation."""
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
    """Sort scope records by maturity score descending, then alphabetically."""
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
        "minimum_recommended_pct": maturity_pct(13),  # L2 lower bound
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

    active_runs = runs_index.get("runs_index", {}).get("active_runs", [])
    published_scopes_raw = scope_catalog.get("scope_catalog", {}).get("published_scopes", [])

    enriched_scopes = [enrich_scope_maturity(s) for s in published_scopes_raw]
    enriched_scopes = sort_scopes_by_maturity(enriched_scopes)
    maturity_summary = build_maturity_summary(enriched_scopes)

    # Probe run_context availability for each active run
    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        enriched_runs.append({**run, "ids_first": probe})

    result: dict[str, Any] = {
        "pipeline_id": "constitution",
        "ai_protocol_present": bool(ai_protocol),
        "active_runs_count": len(active_runs),
        "active_runs": enriched_runs,
        "published_scopes": enriched_scopes,
        "maturity_summary": maturity_summary,
    }

    if len(active_runs) == 1:
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


# ---------------------------------------------------------------------------
# Menu builders
# ---------------------------------------------------------------------------

def _scope_choice_entry(s: dict[str, Any]) -> dict[str, Any]:
    """Build a scope entry for the action menu scope_choices list."""
    entry: dict[str, Any] = {
        "scope_key": s["scope_key"],
        "maturity_pct": maturity_pct(s["maturity_score"]),
        "maturity_level": s["maturity_level"],
        "available": s["maturity_available_for_run"],
    }
    if not s["maturity_available_for_run"]:
        entry["gate_reason"] = s["maturity_gate_reason"]
    return entry


def build_stage_prompt(branch: str, run_id: str, scope_key: str,
                        current_stage: str, ids_first: dict[str, Any]) -> str:
    """Build the stage_prompt for the AI, ids-first if run_context is ready."""
    ids_first_ready = ids_first.get("ids_first_ready", False)
    scope_extract_complete = ids_first.get("scope_extract_complete", False)

    if ids_first_ready:
        # Optimal path: run_context + extracts available, no full Core read needed
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline "
            f"docs/pipelines/constitution/pipeline.md au {current_stage} en mode run-aware "
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
        # Extracts present but run_context missing — regenerate it first
        return (
            f"Dans le repo learn-it, sur la branche {branch}, avant de démarrer {current_stage} "
            f"pour run_id={run_id}, génère d'abord run_context.yaml manquant : "
            f"python docs/patcher/shared/build_run_context.py --run-id {run_id} "
            f"Ensuite applique l'ordre de lecture ids-first : "
            f"run_context.yaml → scope_extract.yaml → neighbor_extract.yaml. "
            f"Ne lis les Core complets que si missing_ids est non vide."
        )
    else:
        # Extracts absent or incomplete — full materialization needed first
        return (
            f"Dans le repo learn-it, sur la branche {branch}, les extraits ids-first sont absents "
            f"ou incomplets pour run_id={run_id}. "
            f"Exécute d'abord la séquence de matérialisation complète : "
            f"1. python docs/patcher/shared/materialize_run_inputs.py --run-id {run_id} ; "
            f"2. python docs/patcher/shared/extract_scope_slice.py --run-id {run_id} ; "
            f"3. python docs/patcher/shared/build_run_context.py --run-id {run_id} ; "
            f"Puis démarre {current_stage} en mode ids-first."
        )


def build_continue_actions(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    ids_first = state.get("recommended_ids_first", {})
    other_scopes = state.get("other_available_scopes", [])
    other_scope_choices = [_scope_choice_entry(s) for s in other_scopes]

    bootstrap_command = (
        f"python docs/patcher/shared/update_run_tracking.py --pipeline constitution --run-id {run_id} "
        f"--stage-id {current_stage} --stage-status in_progress --run-status active --next-stage {current_stage} "
        f"--scope-status confirmed_for_bounded_run --summary \""
        f"Entry decision resolved; resuming existing {scope_key} run at {current_stage}\""
    )

    stage_prompt = build_stage_prompt(branch, run_id, scope_key, current_stage, ids_first)

    return {
        "decision_summary": {
            "pipeline_id": "constitution",
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
            "continue": {
                "bootstrap_command": bootstrap_command,
                "stage_prompt": stage_prompt,
            },
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


def build_open_new_actions(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    all_scopes = state.get("published_scopes", [])
    scope_choices = [_scope_choice_entry(s) for s in all_scopes]
    available_choices = [c for c in scope_choices if c["available"]]
    gated_choices = [c for c in scope_choices if not c["available"]]

    entry_prompt = (
        f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
        f"Pour l'instant, ne résous que l'ouverture d'un nouveau run selon docs/pipelines/constitution/AI_PROTOCOL.yaml. "
        f"Scopes disponibles (triés par maturité décroissante): "
        + ", ".join(
            f"{c['scope_key']} ({c['maturity_pct']} — {c['maturity_level']})"
            for c in available_choices
        )
        + "."
    ) if available_choices else "Aucun scope disponible — publie des scopes d'abord."

    return {
        "decision_summary": {
            "pipeline_id": "constitution",
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


def build_disambiguation_actions(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_summary": {
            "pipeline_id": "constitution",
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
                    f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
                    f"Pour l'instant, ne résous que la désambiguïsation des runs actifs selon docs/pipelines/constitution/AI_PROTOCOL.yaml."
                ),
            }
        },
    }


def build_menu(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    action = state.get("recommended_action")
    if action == "continue_active_run":
        return build_continue_actions(branch, state)
    if action == "open_new_run":
        return build_open_new_actions(branch, state)
    return build_disambiguation_actions(branch, state)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--branch", default="feat/core-modularization-bootstrap")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines_from_registry(registry_path)

    print("PIPELINE_REGISTRY_STATE:")
    print(yaml.safe_dump({"pipelines": pipelines}, sort_keys=False, allow_unicode=True).rstrip())
    print()

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
                    "guidance": "extend launcher support for this pipeline",
                }
            }
        }, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    state = discover_constitution(repo_root)
    menu = build_menu(args.branch, state)

    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_MENU:")
    print(yaml.safe_dump(menu, sort_keys=False, allow_unicode=True).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
