#!/usr/bin/env python3
"""Abandon and archive a constitution run instance.

This script is intentionally conservative:
- it only supports pipeline `constitution`
- it closes the run with an explicit abandonment trace
- it writes a dedicated abandonment record inside the run reports
- it moves the run out of the active `runs/` layout into `archive/runs/`
- it updates `runs/index.yaml` so the launcher no longer sees the run as active

It does *not* silently delete run content.
It archives it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path
from typing import Any

import yaml


ABANDON_STAGE_ID = "RUN_ABANDONED"


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


def ensure_list(parent: dict[str, Any], key: str) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        value = []
        parent[key] = value
    return value


def repo_root_from_script(script_path: Path) -> Path:
    return script_path.resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Abandon and archive a constitution run.")
    parser.add_argument("--pipeline", required=True, choices=["constitution"])
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--summary",
        default="Run abandoned by operator decision before completion.",
        help="Explicit abandonment reason recorded in tracking.",
    )
    parser.add_argument(
        "--archive-root",
        default="",
        help="Optional archive root relative to repo. Defaults to docs/pipelines/constitution/archive/runs",
    )
    return parser.parse_args()


def resolve_paths(repo_root: Path, pipeline_id: str, run_id: str, archive_root_override: str) -> tuple[Path, Path, Path, Path, Path]:
    if pipeline_id != "constitution":
        raise ValueError(f"Unsupported pipeline: {pipeline_id}")

    pipeline_root = repo_root / "docs" / "pipelines" / pipeline_id
    runs_root = pipeline_root / "runs"
    run_root = runs_root / run_id
    run_manifest_path = run_root / "run_manifest.yaml"
    runs_index_path = runs_root / "index.yaml"
    reports_root = run_root / "reports"

    if archive_root_override:
        archive_runs_root = repo_root / archive_root_override
    else:
        archive_runs_root = pipeline_root / "archive" / "runs"

    archive_run_root = archive_runs_root / run_id
    return run_root, run_manifest_path, runs_index_path, reports_root, archive_run_root


def derive_scope_key(scope_id: str) -> str:
    prefix = "CONSTITUTION_SCOPE_"
    if scope_id.startswith(prefix):
        return scope_id.replace(prefix, "").lower()
    return ""


def update_run_manifest_for_abandon(manifest_data: dict[str, Any], summary: str) -> tuple[dict[str, Any], str, str, str]:
    root = ensure_mapping(manifest_data, "run_manifest")
    root["status"] = "closed"

    execution_state = ensure_mapping(root, "execution_state")
    previous_stage = str(execution_state.get("current_stage", ""))
    scope_tracking = ensure_mapping(root, "scope_tracking")
    scope_status = str(scope_tracking.get("scope_status", ""))

    execution_state["current_stage"] = ABANDON_STAGE_ID
    execution_state["last_stage_status"] = "blocked"
    execution_state["last_updated"] = utc_now_iso()
    execution_state["next_stage"] = ""

    stage_history = ensure_list(execution_state, "stage_history")
    stage_history.append(
        {
            "stage_id": ABANDON_STAGE_ID,
            "stage_status": "blocked",
            "recorded_at": utc_now_iso(),
            "summary": summary,
        }
    )

    scope_tracking["last_updated"] = utc_now_iso()
    scope_tracking["last_note"] = summary

    scope_binding = ensure_mapping(root, "scope_binding")
    scope_id = str(scope_binding.get("scope_id", ""))
    return manifest_data, previous_stage, scope_status, scope_id


def write_abandonment_record(reports_root: Path, run_id: str, summary: str, previous_stage: str, scope_status: str) -> Path:
    record_path = reports_root / f"stage_completion_{ABANDON_STAGE_ID}.yaml"
    record = {
        "stage_completion_record": {
            "schema_version": 0.1,
            "pipeline_id": "constitution",
            "run_id": run_id,
            "stage_id": ABANDON_STAGE_ID,
            "stage_status": "blocked",
            "run_status": "closed",
            "next_stage": "",
            "scope_status": scope_status,
            "summary": summary,
            "previous_stage": previous_stage,
            "recorded_at": utc_now_iso(),
        }
    }
    dump_yaml(record_path, record)
    return record_path


def update_runs_index_for_abandon(index_data: dict[str, Any], run_id: str, scope_id: str, scope_status: str, archive_run_root_relative: str) -> dict[str, Any]:
    root = ensure_mapping(index_data, "runs_index")
    active_runs = ensure_list(root, "active_runs")
    closed_runs = ensure_list(root, "closed_runs")

    active_runs[:] = [entry for entry in active_runs if entry.get("run_id") != run_id]
    closed_runs[:] = [entry for entry in closed_runs if entry.get("run_id") != run_id]

    closed_runs.append(
        {
            "run_id": run_id,
            "scope_id": scope_id,
            "scope_key": derive_scope_key(scope_id),
            "run_status": "closed",
            "current_stage": ABANDON_STAGE_ID,
            "archived_run_manifest_ref": archive_run_root_relative.replace("\\", "/") + "/run_manifest.yaml",
            "scope_status": scope_status,
            "closure_mode": "abandoned",
            "archived_at": utc_now_iso(),
        }
    )

    root["last_updated"] = utc_now_iso().split("T", 1)[0]
    return index_data


def main() -> int:
    args = parse_args()
    repo_root = repo_root_from_script(Path(__file__))

    run_root, run_manifest_path, runs_index_path, reports_root, archive_run_root = resolve_paths(
        repo_root,
        args.pipeline,
        args.run_id,
        args.archive_root,
    )

    if not run_root.exists():
        raise FileNotFoundError(f"Run root does not exist: {run_root}")
    if archive_run_root.exists():
        raise FileExistsError(f"Archive destination already exists: {archive_run_root}")

    manifest_data = load_yaml(run_manifest_path)
    index_data = load_yaml(runs_index_path)

    manifest_data, previous_stage, scope_status, scope_id = update_run_manifest_for_abandon(manifest_data, args.summary)
    dump_yaml(run_manifest_path, manifest_data)
    record_path = write_abandonment_record(reports_root, args.run_id, args.summary, previous_stage, scope_status)

    archive_run_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(run_root), str(archive_run_root))

    archive_run_root_relative = str(archive_run_root.relative_to(repo_root))
    index_data = update_runs_index_for_abandon(index_data, args.run_id, scope_id, scope_status, archive_run_root_relative)
    dump_yaml(runs_index_path, index_data)

    print("RUN_ABANDONED:")
    print(f"  pipeline: {args.pipeline}")
    print(f"  run_id: {args.run_id}")
    print(f"  previous_stage: {previous_stage}")
    print(f"  archive_run_root: {archive_run_root_relative}")
    print(f"  abandonment_record: {record_path.relative_to(repo_root)}")
    print(f"  runs_index: {runs_index_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
