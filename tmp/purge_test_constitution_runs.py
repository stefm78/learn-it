from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from datetime import datetime, timezone

import yaml

TARGET_RUN_IDS = [
    "CONSTITUTION_RUN_2026_04_20_DEPLOYMENT_GOVERNANCE_R01",
    "CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02",
    "CONSTITUTION_RUN_2026_04_20_PATCH_LIFECYCLE_R01",
    "CONSTITUTION_RUN_2026_04_20_LEARNER_STATE_R01",
    "CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01",
]

PROTECTED_RUN_IDS = {
    "CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01",
}

def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}

def dump_yaml(path: Path, data: dict) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    runs_root = repo / "docs/pipelines/constitution/runs"
    index_path = runs_root / "index.yaml"

    index = load_yaml(index_path)
    root = index.get("runs_index", {})
    active_runs = root.get("active_runs", []) or []
    closed_runs = root.get("closed_runs", []) or []

    target_set = set(TARGET_RUN_IDS)

    forbidden = target_set & PROTECTED_RUN_IDS
    if forbidden:
        raise SystemExit(f"Refusing to purge protected runs: {sorted(forbidden)}")

    found_active = [r for r in active_runs if r.get("run_id") in target_set]
    found_closed = [r for r in closed_runs if r.get("run_id") in target_set]
    missing_from_index = sorted(
        target_set
        - {r.get("run_id") for r in found_active}
        - {r.get("run_id") for r in found_closed}
    )

    run_dirs = []
    missing_dirs = []

    for run_id in TARGET_RUN_IDS:
        p = runs_root / run_id
        if p.exists():
            run_dirs.append(p)
        else:
            missing_dirs.append(run_id)

    report = {
        "purge_test_constitution_runs": {
            "mode": "apply" if args.apply else "dry_run",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "target_run_ids": TARGET_RUN_IDS,
            "protected_run_ids": sorted(PROTECTED_RUN_IDS),
            "found_in_active_index": [r.get("run_id") for r in found_active],
            "found_in_closed_index": [r.get("run_id") for r in found_closed],
            "missing_from_index": missing_from_index,
            "run_dirs_to_delete": [p.relative_to(repo).as_posix() for p in run_dirs],
            "missing_run_dirs": missing_dirs,
            "files_to_update": [
                "docs/pipelines/constitution/runs/index.yaml",
            ],
            "apply_done": False,
        }
    }

    report_path = repo / "tmp/purge_test_constitution_runs_report.yaml"

    if not args.apply:
        report_path.write_text(
            yaml.safe_dump(report, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"DRY_RUN written: {report_path.relative_to(repo).as_posix()}")
        return 0

    # Backup index before mutation
    backup_path = repo / "tmp/runs_index_before_test_purge.yaml"
    backup_path.write_text(index_path.read_text(encoding="utf-8"), encoding="utf-8")

    # Remove entries from index
    root["active_runs"] = [r for r in active_runs if r.get("run_id") not in target_set]
    root["closed_runs"] = [r for r in closed_runs if r.get("run_id") not in target_set]
    root["last_updated"] = datetime.now(timezone.utc).date().isoformat()

    notes = root.get("notes")
    if not isinstance(notes, list):
        notes = []
        root["notes"] = notes

    notes.append(
        "Purged disposable 2026-04-20 test runs before PHASE_13 patch_lifecycle pilot."
    )

    dump_yaml(index_path, index)

    # Delete run directories
    for p in run_dirs:
        shutil.rmtree(p)

    report["purge_test_constitution_runs"]["apply_done"] = True
    report["purge_test_constitution_runs"]["backup_index"] = backup_path.relative_to(repo).as_posix()

    report_path.write_text(
        yaml.safe_dump(report, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    print(f"APPLY written: {report_path.relative_to(repo).as_posix()}")
    print(f"Backup written: {backup_path.relative_to(repo).as_posix()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
