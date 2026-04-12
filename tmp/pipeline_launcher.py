#!/usr/bin/env python3
"""Registry-aware bootstrap launcher for pipeline prompt prebuilding.

Current candidate launcher.
Goals:
- low-context discovery
- synthetic entry menu
- next best actions
- actionable continue-run path

Still experimental: kept in tmp/ until hardened and promoted.
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


def build_continue_actions(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    other_scopes = [s.get("scope_key") or "?" for s in state.get("other_available_scopes", [])[:5]]

    bootstrap_command = (
        f"python docs/patcher/shared/update_run_tracking.py --pipeline constitution --run-id {run_id} "
        f"--stage-id {current_stage} --stage-status in_progress --run-status active --next-stage {current_stage} "
        f"--scope-status confirmed_for_bounded_run --summary \"Entry decision resolved; resuming existing {scope_key} run at {current_stage}\""
    )

    stage_prompt = (
        f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md "
        f"au {current_stage} en mode run-aware pour run_id={run_id}. "
        f"Lis d'abord docs/pipelines/constitution/AI_PROTOCOL.yaml, puis le run_manifest.yaml et les inputs du run, "
        f"et produis le livrable du stage uniquement sous docs/pipelines/constitution/runs/{run_id}/... "
        f"À la fin, donne-moi la commande update_run_tracking.py de clôture du stage à exécuter."
    )

    return {
        "decision_summary": {
            "pipeline_id": "constitution",
            "recommended_default": "continue",
            "active_run": run_id,
            "active_scope": scope_key,
            "active_stage": current_stage,
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
            },
            {
                "key": "new_run",
                "label": "Open new run on another published scope",
                "available": bool(other_scopes),
                "recommended": False,
                "scope_choices": other_scopes,
                "reason_if_unavailable": "no_other_published_scope_available" if not other_scopes else "",
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
                "status": "available" if other_scopes else "unavailable_now",
                "scope_choices": other_scopes,
                "guidance": "publish_additional_scopes_first" if not other_scopes else "choose_a_scope_key_then_open_new_run",
            },
            "inspect": {
                "guidance": f"Read docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml and recent stage_completion records only.",
            },
        },
    }


def build_open_new_actions(branch: str, state: dict[str, Any]) -> dict[str, Any]:
    scopes = [s.get("scope_key") or "?" for s in state.get("published_scopes", [])[:5]]
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
                "available": bool(scopes),
                "recommended": True,
                "scope_choices": scopes,
            }
        ],
        "next_best_actions": {
            "new_run": {
                "status": "available" if scopes else "unavailable_now",
                "scope_choices": scopes,
                "guidance": "choose_a_scope_key_then_open_new_run" if scopes else "publish_scopes_first",
                "entry_prompt": (
                    f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
                    f"Pour l'instant, ne résous que l'ouverture d'un nouveau run selon docs/pipelines/constitution/AI_PROTOCOL.yaml. "
                    f"Scopes publiés disponibles: {', '.join(scopes)}."
                ),
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
