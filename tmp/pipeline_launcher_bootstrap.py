#!/usr/bin/env python3
"""Bootstrap launcher for pipeline prompt prebuilding.

Intent:
- discover known pipelines
- inspect lightweight run/scope state
- recommend continue vs new run
- build a short deterministic AI launch prompt

Bootstrap scope:
- constitution first

This file is intentionally placed in tmp/ for iterative hardening before moving
into docs/patcher/shared/.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def discover_constitution(repo_root: Path) -> dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / "constitution"
    runs_index = load_yaml(pipeline_root / "runs" / "index.yaml")
    scope_catalog = load_yaml(pipeline_root / "scope_catalog" / "manifest.yaml")

    active_runs = runs_index.get("runs_index", {}).get("active_runs", [])
    published_scopes = scope_catalog.get("scope_catalog", {}).get("published_scopes", [])

    result: dict[str, Any] = {
        "pipeline_id": "constitution",
        "active_runs_count": len(active_runs),
        "active_runs": active_runs,
        "published_scopes": [
            {
                "scope_id": s.get("scope_id"),
                "scope_key": s.get("scope_key"),
                "maturity": s.get("maturity", {}),
            }
            for s in published_scopes
        ],
    }

    if len(active_runs) == 1:
        run = active_runs[0]
        result["recommended_action"] = "continue_active_run"
        result["recommended_run_id"] = run.get("run_id")
        result["recommended_scope_key"] = run.get("scope_key")
        other_scopes = [s for s in result["published_scopes"] if s.get("scope_key") != run.get("scope_key")]
        result["other_available_scopes"] = other_scopes
    elif len(active_runs) == 0:
        result["recommended_action"] = "open_new_run"
        result["other_available_scopes"] = result["published_scopes"]
    else:
        result["recommended_action"] = "disambiguate"
        result["other_available_scopes"] = result["published_scopes"]

    return result


def build_prompt(branch: str, state: dict[str, Any]) -> str:
    pipeline_id = state["pipeline_id"]
    if pipeline_id != "constitution":
        raise ValueError("Only constitution is supported in bootstrap version")

    if state.get("recommended_action") == "continue_active_run":
        run_id = state.get("recommended_run_id")
        scope_key = state.get("recommended_scope_key")
        others = ", ".join(s.get("scope_key") or "?" for s in state.get("other_available_scopes", [])[:5])
        suffix = f" Autres scopes publiés disponibles pour un nouveau run: {others}." if others else ""
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
            f"Ne commence pas de stage tout de suite: commence seulement par une décision d'entrée selon docs/pipelines/constitution/AI_PROTOCOL.yaml. "
            f"Il existe déjà un run actif {run_id} sur {scope_key}; propose explicitement soit de continuer ce run, soit d'ouvrir un nouveau run sur un autre scope publié.{suffix}"
        )

    if state.get("recommended_action") == "open_new_run":
        scopes = ", ".join(s.get("scope_key") or "?" for s in state.get("published_scopes", [])[:5])
        return (
            f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
            f"Commence par proposer l'ouverture d'un nouveau run à partir d'un scope publié selon docs/pipelines/constitution/AI_PROTOCOL.yaml. "
            f"Scopes disponibles: {scopes}."
        )

    return (
        f"Dans le repo learn-it, sur la branche {branch}, exécute le pipeline docs/pipelines/constitution/pipeline.md. "
        f"Commence par désambiguïser les runs actifs selon docs/pipelines/constitution/AI_PROTOCOL.yaml avant toute lecture profonde."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--branch", default="feat/core-modularization-bootstrap")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if args.pipeline != "constitution":
        raise ValueError("Bootstrap version supports constitution only")

    state = discover_constitution(repo_root)
    prompt = build_prompt(args.branch, state)

    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_PROMPT:")
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
