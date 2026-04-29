#!/usr/bin/env python3
"""Registry-aware promoted pipeline launcher runtime.

Responsibilities kept in this engine:
- parse CLI arguments;
- print registry state;
- route to parallel slot rendering or the selected pipeline launch menu;
- delegate domain logic to docs.patcher.shared.pipeline_launcher modules.

The human-facing command is:
    python docs/patcher/shared/pipeline_launcher/cli.py

The legacy tmp/pipeline_launcher.py is only a compatibility wrapper.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

# Support direct execution as `python docs/patcher/shared/pipeline_launcher/engine.py`
# while importing modules from the repository root.
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.registry import discover_pipelines_from_registry
from docs.patcher.shared.pipeline_launcher.pipeline_state import (
    discover_constitution,
    discover_generic_pipeline,
)

from docs.patcher.shared.pipeline_launcher.launch_menu import (
    build_menu,
    build_parallel_slots,
)

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
