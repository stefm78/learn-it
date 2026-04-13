#!/usr/bin/env python3
"""Update run tracking for pipeline runs.

This script updates:
- the run_manifest.yaml of a run instance
- the lightweight runs/index.yaml summary
- a stage completion record under the run reports directory
- run_context.yaml (auto-rebuilt via build_run_context.py if present)

Bootstrap scope:
- pipeline `constitution`

The script is intentionally conservative and deterministic.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def ensure_mapping(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        value = {}
        parent[key] = value
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update run tracking after a stage finishes.")
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--stage-id", required=True)
    parser.add_argument("--stage-status", required=True, choices=["done", "in_progress", "blocked", "failed", "skipped"])
    parser.add_argument("--run-status", required=True, choices=["bootstrap_open", "active", "blocked", "failed", "closed"])
    parser.add_argument("--next-stage", default="")
    parser.add_argument("--scope-status", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--close-run", action="store_true")
    parser.add_argument(
        "--skip-rebuild-context",
        action="store_true",
        help="Ne pas rebuilder run_context.yaml apres la mise a jour (deconseille).",
    )
    return parser.parse_args()


def repo_root_from_script(script_path: Path) -> Path:
    # docs/patcher/shared/update_run_tracking.py -> repo root = parents[3]
    return script_path.resolve().parents[3]


def resolve_pipeline_paths(repo_root: Path, pipeline_id: str, run_id: str) -> tuple[Path, Path, Path, Path]:
    if pipeline_id != "constitution":
        raise ValueError(f"Unsupported pipeline for now: {pipeline_id}")

    pipeline_root = repo_root / "docs" / "pipelines" / pipeline_id
    run_root = pipeline_root / "runs" / run_id
    run_manifest = run_root / "run_manifest.yaml"
    runs_index = pipeline_root / "runs" / "index.yaml"
    reports_root = run_root / "reports"
    return run_root, run_manifest, runs_index, reports_root


def update_run_manifest(
    manifest_data: dict[str, Any],
    *,
    stage_id: str,
    stage_status: str,
    run_status: str,
    next_stage: str,
    scope_status: str,
    summary: str,
    close_run: bool,
) -> dict[str, Any]:
    run_manifest = ensure_mapping(manifest_data, "run_manifest")
    run_manifest["status"] = run_status

    execution_state = ensure_mapping(run_manifest, "execution_state")
    execution_state["current_stage"] = stage_id
    execution_state["last_stage_status"] = stage_status
    execution_state["last_updated"] = utc_now_iso()
    if next_stage:
        execution_state["next_stage"] = next_stage
    elif close_run:
        execution_state["next_stage"] = ""

    completed_stages = execution_state.get("completed_stages")
    if not isinstance(completed_stages, list):
        completed_stages = []
        execution_state["completed_stages"] = completed_stages
    if stage_status == "done" and stage_id not in completed_stages:
        completed_stages.append(stage_id)

    stage_history = execution_state.get("stage_history")
    if not isinstance(stage_history, list):
        stage_history = []
        execution_state["stage_history"] = stage_history
    stage_history.append(
        {
            "stage_id": stage_id,
            "stage_status": stage_status,
            "recorded_at": utc_now_iso(),
            "summary": summary,
        }
    )

    if scope_status:
        scope_tracking = ensure_mapping(run_manifest, "scope_tracking")
        scope_tracking["scope_status"] = scope_status
        scope_tracking["last_updated"] = utc_now_iso()
        if summary:
            scope_tracking["last_note"] = summary

    return manifest_data


def update_runs_index(
    index_data: dict[str, Any],
    *,
    run_manifest_data: dict[str, Any],
    run_id: str,
    stage_id: str,
    stage_status: str,
    run_status: str,
    next_stage: str,
    scope_status: str,
    close_run: bool,
) -> dict[str, Any]:
    root = ensure_mapping(index_data, "runs_index")
    active_runs = root.get("active_runs")
    if not isinstance(active_runs, list):
        active_runs = []
        root["active_runs"] = active_runs
    closed_runs = root.get("closed_runs")
    if not isinstance(closed_runs, list):
        closed_runs = []
        root["closed_runs"] = closed_runs

    run_manifest = ensure_mapping(run_manifest_data, "run_manifest")
    scope_binding = ensure_mapping(run_manifest, "scope_binding")
    scope_id = scope_binding.get("scope_id", "")
    scope_key = ""
    if scope_id.startswith("CONSTITUTION_SCOPE_"):
        scope_key = scope_id.replace("CONSTITUTION_SCOPE_", "").lower()

    # current_stage dans index.yaml = next_stage si done, sinon stage_id courant
    # Cela garantit que le launcher affiche le prochain stage actionnable.
    displayed_stage = next_stage if (stage_status == "done" and next_stage) else stage_id

    updated_entry: dict[str, Any] = {
        "run_id": run_id,
        "scope_id": scope_id,
        "scope_key": scope_key,
        "run_status": run_status,
        "current_stage": displayed_stage,
        "mode": run_manifest.get("mode", "bounded_local_run"),
        "run_manifest_ref": f"docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml",
    }
    if scope_status:
        updated_entry["scope_status"] = scope_status

    # Remove existing entry from both lists
    active_runs[:] = [entry for entry in active_runs if entry.get("run_id") != run_id]
    closed_runs[:] = [entry for entry in closed_runs if entry.get("run_id") != run_id]

    if close_run or run_status == "closed":
        closed_runs.append(updated_entry)
    else:
        active_runs.append(updated_entry)

    root["last_updated"] = utc_now_iso().split("T", 1)[0]
    return index_data


def write_stage_record(
    reports_root: Path,
    *,
    pipeline_id: str,
    run_id: str,
    stage_id: str,
    stage_status: str,
    run_status: str,
    next_stage: str,
    scope_status: str,
    summary: str,
) -> Path:
    filename = f"stage_completion_{stage_id}.yaml"
    record_path = reports_root / filename
    record = {
        "stage_completion_record": {
            "schema_version": 0.1,
            "pipeline_id": pipeline_id,
            "run_id": run_id,
            "stage_id": stage_id,
            "stage_status": stage_status,
            "run_status": run_status,
            "next_stage": next_stage,
            "scope_status": scope_status,
            "summary": summary,
            "recorded_at": utc_now_iso(),
        }
    }
    dump_yaml(record_path, record)
    return record_path


def rebuild_run_context(repo_root: Path, pipeline_id: str, run_id: str) -> bool:
    """Rebuild run_context.yaml via build_run_context.py.

    Appelé automatiquement après chaque mise à jour de tracking pour garantir
    la synchronisation entre run_manifest.yaml / index.yaml et run_context.yaml.

    Retourne True si le rebuild a réussi, False sinon (non bloquant).
    """
    build_script = repo_root / "docs" / "patcher" / "shared" / "build_run_context.py"
    if not build_script.exists():
        print(
            f"[update_run_tracking] WARN: build_run_context.py absent à {build_script} — "
            "run_context.yaml non reconstruit.",
            file=sys.stderr,
        )
        return False

    cmd = [
        sys.executable,
        str(build_script),
        "--pipeline", pipeline_id,
        "--run-id", run_id,
        "--repo-root", str(repo_root),
    ]
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode != 0:
        print(
            f"[update_run_tracking] WARN: build_run_context.py a échoué (code {result.returncode}) — "
            "run_context.yaml potentiellement désynchronisé.",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    args = parse_args()
    repo_root = repo_root_from_script(Path(__file__))
    run_root, run_manifest_path, runs_index_path, reports_root = resolve_pipeline_paths(
        repo_root, args.pipeline, args.run_id
    )

    if not run_root.exists():
        raise FileNotFoundError(f"Run root does not exist: {run_root}")

    manifest_data = load_yaml(run_manifest_path)
    index_data = load_yaml(runs_index_path)

    manifest_data = update_run_manifest(
        manifest_data,
        stage_id=args.stage_id,
        stage_status=args.stage_status,
        run_status=args.run_status,
        next_stage=args.next_stage,
        scope_status=args.scope_status,
        summary=args.summary,
        close_run=args.close_run,
    )
    dump_yaml(run_manifest_path, manifest_data)

    index_data = update_runs_index(
        index_data,
        run_manifest_data=manifest_data,
        run_id=args.run_id,
        stage_id=args.stage_id,
        stage_status=args.stage_status,
        run_status=args.run_status,
        next_stage=args.next_stage,
        scope_status=args.scope_status,
        close_run=args.close_run,
    )
    dump_yaml(runs_index_path, index_data)

    record_path = write_stage_record(
        reports_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        stage_id=args.stage_id,
        stage_status=args.stage_status,
        run_status=args.run_status,
        next_stage=args.next_stage,
        scope_status=args.scope_status,
        summary=args.summary,
    )

    print("RUN_TRACKING_UPDATED:")
    print(f"  pipeline: {args.pipeline}")
    print(f"  run_id: {args.run_id}")
    print(f"  stage_id: {args.stage_id}")
    print(f"  stage_status: {args.stage_status}")
    print(f"  run_status: {args.run_status}")
    print(f"  run_manifest: {run_manifest_path.relative_to(repo_root)}")
    print(f"  runs_index: {runs_index_path.relative_to(repo_root)}")
    print(f"  stage_record: {record_path.relative_to(repo_root)}")

    # Auto-rebuild run_context.yaml sauf si explicitement désactivé
    if not args.skip_rebuild_context:
        print()
        print("[update_run_tracking] Reconstruction de run_context.yaml...")
        ok = rebuild_run_context(repo_root, args.pipeline, args.run_id)
        if ok:
            print("[update_run_tracking] run_context.yaml synchronisé.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
