#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Purge an index-only stale constitution run reference."
    )
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the purge. Without this flag, run in dry-run mode.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    runs_root = pipeline_root / "runs"
    run_root = runs_root / args.run_id
    archive_run_root = pipeline_root / "archive" / "runs" / args.run_id
    runs_index_path = runs_root / "index.yaml"

    if not runs_index_path.exists():
        raise FileNotFoundError(f"runs/index.yaml missing: {runs_index_path}")

    index_data = load_yaml(runs_index_path)
    runs_index = index_data.setdefault("runs_index", {})
    active_runs = runs_index.setdefault("active_runs", [])
    closed_runs = runs_index.setdefault("closed_runs", [])

    if not isinstance(active_runs, list) or not isinstance(closed_runs, list):
        raise ValueError("runs_index.active_runs and closed_runs must be lists")

    active_matches = [entry for entry in active_runs if entry.get("run_id") == args.run_id]
    closed_matches = [entry for entry in closed_runs if entry.get("run_id") == args.run_id]

    if not active_matches and not closed_matches:
        raise SystemExit(f"Run id not found in index: {args.run_id}")

    if run_root.exists():
        raise SystemExit(
            f"Run root exists; not an index-only stale reference: {run_root}"
        )

    if archive_run_root.exists():
        raise SystemExit(
            f"Archived run root exists; refusing purge because this is not a pure ghost reference: {archive_run_root}"
        )

    new_active_runs = [entry for entry in active_runs if entry.get("run_id") != args.run_id]
    new_closed_runs = [entry for entry in closed_runs if entry.get("run_id") != args.run_id]

    removed_bucket = "active" if active_matches else "closed"
    removed_count = len(active_matches) + len(closed_matches)

    if args.apply:
        runs_index["active_runs"] = new_active_runs
        runs_index["closed_runs"] = new_closed_runs
        runs_index["last_updated"] = datetime.now(UTC).strftime("%Y-%m-%d")
        notes = runs_index.setdefault("notes", [])
        if isinstance(notes, list):
            notes.append(
                f"Purged stale index-only run reference {args.run_id} on {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}."
            )
        dump_yaml(runs_index_path, index_data)

    result = {
        "purge_run_reference": {
            "status": "DONE",
            "apply": args.apply,
            "pipeline_id": args.pipeline,
            "run_id": args.run_id,
            "removed_from_bucket": removed_bucket,
            "removed_entry_count": removed_count,
            "run_root_exists": run_root.exists(),
            "archive_run_root_exists": archive_run_root.exists(),
            "index_path": str(runs_index_path),
            "next_best_action": "INSPECT_INDEX",
            "next_best_action_reason": (
                "Ghost run reference purged from runs/index.yaml."
                if args.apply
                else "Dry-run only; no change written."
            ),
        }
    }

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())