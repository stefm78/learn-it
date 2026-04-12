#!/usr/bin/env python3
"""Registry-aware bootstrap launcher for pipeline prompt prebuilding.

v4 changes:
- keep registry-aware discovery
- emit a structured action menu
- emit next-step prompt and command suggestions
- remain honest when no alternative scope is currently published

Still experimental: kept in tmp/ until hardened.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


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

    if current:
        pipelines.append(current)
    return pipelines


def discover_constitution(repo_root: Path) -> dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / "constitution"
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    scope_catalog = load_yaml(pipeline_root / "scope_catalog" / "manifest.yaml")
    ai_protocol = load_yaml(pipeline_root / "AI_PROTOCOL.yaml")

    active_runs = runs_index.get("runs_index", {}).get("active_runs", [])
    published_scopes = scope_catalog.get("scope_catalog", {}).get("published_scopes", [])

    published_scope_records = [
        {
            "scope_id": s.get("scope_id"),
            "scope_key": s.get("scope_key"),
            "maturity": s.get("maturity", {}),
        }
        for s in published_scopes
    ]

    result: dict[str, Any] = {
        "pipeline_id": "constitution",
        "ai_protocol_present": bool(ai_protocol),
        "active_runs_count": len(active_runs),
        "active_runs": active_runs,
        "published_scopes": published_scope_records,
    }

    if len(active_runs) == 1:
        run = active_runs[0]
        other_scopes = [s for s in published_scope_records if s.get("scope_key") != run.get("scope_key")]
        result.update(
            {
                "recommended_action": "continue_active_run",
                "recommended_run_id": run.get("run_id"),
                "recommended_scope_key": run.get("scope_key"),
                "recommended_current_stage": run.get("current_stage"),
                "other_available_scopes": other_scopes,
                "can_open_new_run_on_other_scope_now": len(other_scopes) > 0,
            }
        )
    elif len(active_runs) == 0:
        result.update(
            {
                "recommended_action": "open_new_run",
                "other_available_scopes": published_scope_records,
                "can_open_new_run_on_other_scope_now": len(published_scope_records) > 0,
            }
        )
    else:
        result.update(
            {
                "recommended_action": "disambiguate",
                "other_available_scopes": published_scope_records,
                "can_open_new_run_on_other_scope_now": len(published_scope_records) > 0,
            }
        )

    return result


def build_constitution_outputs(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    action = state.get("recommended_action")

    if action == "continue_active_run":
        run_id = state.get("recommended_run_id")
        scope_key = state.get("recommended_scope_key")
        current_stage = state.get("recommended_current_stage")
        others = [s.get("scope_key") or "?" for s in state.get("other_available_scopes", [])[:5]]

        entry_prompt = (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
            f"Pour l'instant, ne résous que le point d'entrée selon docs/pipelines/constitution/AI_PROTOCOL.yaml: "
            f"il existe déjà un run actif {run_id} sur {scope_key}, actuellement sur {current_stage}."
        )
        if others:
            entry_prompt += f" Propose explicitement soit de continuer ce run, soit d'ouvrir un nouveau run sur un autre scope publié ({', '.join(others)}), puis arrête-toi."
        else:
            entry_prompt += " Aucun autre scope publié n'est encore disponible pour ouvrir immédiatement un nouveau run; recommande de continuer ce run, puis arrête-toi."

        bootstrap_command = (
            f"python docs/patcher/shared/update_run_tracking.py --pipeline constitution --run-id {run_id} "
            f"--stage-id {current_stage} --stage-status in_progress --run-status active --next-stage {current_stage} "
            f"--scope-status confirmed_for_bounded_run --summary \"Entry decision resolved; resuming existing {scope_key} run at {current_stage}\""
        )

        return {
            "action_menu": [
                {"action": "continue_active_run", "run_id": run_id, "scope_key": scope_key, "current_stage": current_stage, "recommended": True},
                {"action": "open_new_run", "available_now": bool(others), "other_scope_keys": others, "recommended": False},
            ],
            "entry_prompt": entry_prompt,
            "bootstrap_command_if_continue": bootstrap_command,
        }

    if action == "open_new_run":
        scopes = [s.get("scope_key") or "?" for s in state.get("published_scopes", [])[:5]]
        entry_prompt = (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
            f"Pour l'instant, ne résous que le point d'entrée selon docs/pipelines/constitution/AI_PROTOCOL.yaml: "
            f"aucun run actif n'est ouvert. Propose l'ouverture d'un nouveau run à partir d'un scope publié, puis arrête-toi. "
            f"Scopes disponibles: {', '.join(scopes)}."
        )
        return {
            "action_menu": [
                {"action": "open_new_run", "available_now": bool(scopes), "other_scope_keys": scopes, "recommended": True}
            ],
            "entry_prompt": entry_prompt,
        }

    return {
        "action_menu": [{"action": "disambiguate", "recommended": True}],
        "entry_prompt": (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
            f"Pour l'instant, ne résous que le point d'entrée selon docs/pipelines/constitution/AI_PROTOCOL.yaml et propose une courte désambiguïsation des runs actifs avant toute lecture profonde."
        ),
    }


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
        print("PIPELINE_LAUNCHER_STATE:")
        print(yaml.safe_dump({
            "pipeline_id": args.pipeline,
            "status": "unsupported_in_bootstrap_v4",
            "next_best_action": "extend launcher support for this pipeline",
        }, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    state = discover_constitution(repo_root)
    outputs = build_constitution_outputs(args.branch, state)

    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_ACTIONS:")
    print(yaml.safe_dump(outputs, sort_keys=False, allow_unicode=True).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
