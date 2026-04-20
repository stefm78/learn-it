#!/usr/bin/env python3
"""
Reconcile a constitution run from its run_id.

Scope of this initial version:
- pipeline: constitution
- mode: bounded_local_run only
- purpose: restore a run to an executable state without replaying business stages

Principles:
- compute the longest trusted prefix of stages that is still materially justified
- repair only derivable artifacts via their owner scripts
- truncate downstream state that is no longer justifiable
- rebuild run_context.yaml after applied reconciliation
- do not create an audit layer or a persistent drift report
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


STAGE_ORDER: List[str] = [
    "STAGE_01_CHALLENGE",
    "STAGE_02_ARBITRAGE",
    "STAGE_03_PATCH_SYNTHESIS",
    "STAGE_04_PATCH_VALIDATION",
    "STAGE_05_APPLY",
    "STAGE_06_CORE_VALIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
    "STAGE_08_PROMOTE_CURRENT",
    "STAGE_09_CLOSEOUT_AND_ARCHIVE",
]

STAGE_ALIASES: Dict[str, str] = {
    "STAGE_05_PATCH_APPLICATION": "STAGE_05_APPLY",
    "STAGE_09_CLOSEOUT": "STAGE_09_CLOSEOUT_AND_ARCHIVE",
}

STAGE_EVIDENCE: Dict[str, List[str]] = {
    "STAGE_01_CHALLENGE": [
        "work/01_challenge/challenge_report_*.md",
    ],
    "STAGE_02_ARBITRAGE": [
        "work/02_arbitrage/arbitrage.md",
    ],
    "STAGE_03_PATCH_SYNTHESIS": [
        "work/03_patch/patchset.yaml",
    ],
    "STAGE_04_PATCH_VALIDATION": [
        "work/04_patch_validation/patch_validation.yaml",
    ],
    "STAGE_05_APPLY": [
        "reports/patch_execution_report.yaml",
    ],
    "STAGE_06_CORE_VALIDATION": [
        "work/06_core_validation/core_validation.yaml",
    ],
    "STAGE_07_RELEASE_MATERIALIZATION": [
        "work/07_release/release_plan.yaml",
        "reports/release_materialization_report.yaml",
    ],
    "STAGE_08_PROMOTE_CURRENT": [
        "reports/promotion_report.yaml",
        "reports/current_manifest_validation.yaml",
        "reports/promotion_report_validation.yaml",
    ],
    "STAGE_09_CLOSEOUT_AND_ARCHIVE": [
        "reports/closeout_report.yaml",
        "outputs/final_run_summary.md",
    ],
}

DERIVABLE_INPUTS = [
    "inputs/scope_manifest.yaml",
    "inputs/impact_bundle.yaml",
    "inputs/integration_gate.yaml",
]

DERIVABLE_EXTRACTS = [
    "inputs/scope_extract.yaml",
    "inputs/neighbor_extract.yaml",
]

DERIVABLE_CONTEXT = [
    "inputs/run_context.yaml",
]


class ReconciliationError(Exception):
    pass


def canonical_stage_id(stage_id: str) -> str:
    return STAGE_ALIASES.get(stage_id, stage_id)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_yaml_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def repo_root_from_script(script_path: Path) -> Path:
    return script_path.resolve().parents[3]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile a constitution run.")
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the reconciliation plan materially.",
    )
    return parser.parse_args()


def run_script(cmd: List[str], *, apply: bool, cwd: Path) -> Dict[str, Any]:
    if not apply:
        return {"planned": True, "applied": False, "command": " ".join(cmd), "returncode": None}

    result = subprocess.run(cmd, cwd=str(cwd), capture_output=False, text=True)
    if result.returncode != 0:
        raise ReconciliationError(f"Command failed ({result.returncode}): {' '.join(cmd)}")
    return {"planned": True, "applied": True, "command": " ".join(cmd), "returncode": result.returncode}


def stage_index(stage_id: str) -> int:
    return STAGE_ORDER.index(stage_id)


def next_stage_after(stage_id: str) -> Optional[str]:
    idx = stage_index(stage_id)
    if idx + 1 >= len(STAGE_ORDER):
        return None
    return STAGE_ORDER[idx + 1]


def matches_any_glob(base: Path, pattern: str) -> bool:
    return any(base.glob(pattern))


def stage_evidence_status(run_root: Path, stage_id: str) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for pattern in STAGE_EVIDENCE.get(stage_id, []):
        if "*" in pattern or "?" in pattern or "[" in pattern:
            if not matches_any_glob(run_root, pattern):
                missing.append(pattern)
        else:
            if not (run_root / pattern).exists():
                missing.append(pattern)
    return len(missing) == 0, missing


def derive_claimed_done_stages(run_manifest_root: Dict[str, Any]) -> List[str]:
    exec_state = run_manifest_root.get("execution_state", {})
    completed = exec_state.get("completed_stages", [])
    if not isinstance(completed, list):
        completed = []

    normalized = []
    seen = set()
    for stage in completed:
        if not isinstance(stage, str):
            continue
        c = canonical_stage_id(stage)
        if c in STAGE_ORDER and c not in seen:
            normalized.append(c)
            seen.add(c)

    current_stage = canonical_stage_id(str(exec_state.get("current_stage", "")))
    last_stage_status = str(exec_state.get("last_stage_status", ""))

    if current_stage in STAGE_ORDER and last_stage_status == "done" and current_stage not in seen:
        normalized.append(current_stage)

    normalized.sort(key=stage_index)
    return normalized


def contiguous_claimed_prefix(claimed_done: List[str]) -> List[str]:
    prefix: List[str] = []
    claimed_set = set(claimed_done)
    for stage in STAGE_ORDER:
        if stage in claimed_set:
            prefix.append(stage)
        else:
            break
    return prefix


def repair_derivable_inputs(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    run_root: Path,
    apply: bool,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    repaired: List[str] = []
    commands: List[Dict[str, Any]] = []

    missing_inputs = [p for p in DERIVABLE_INPUTS if not (run_root / p).exists()]
    if missing_inputs:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "materialize_run_inputs.py"),
            "--pipeline", pipeline_id,
            "--run-id", run_id,
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_inputs)

    missing_extracts = [p for p in DERIVABLE_EXTRACTS if not (run_root / p).exists()]
    if missing_extracts:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "extract_scope_slice.py"),
            "--pipeline", pipeline_id,
            "--run-id", run_id,
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_extracts)

    missing_context = [p for p in DERIVABLE_CONTEXT if not (run_root / p).exists()]
    if missing_context:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "build_run_context.py"),
            "--pipeline", pipeline_id,
            "--run-id", run_id,
            "--repo-root", str(repo_root),
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_context)

    return repaired, commands


def delete_path(path: Path, *, apply: bool) -> bool:
    if not path.exists():
        return False
    if not apply:
        return True
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def invalidate_downstream_artifacts(
    *,
    run_root: Path,
    invalidated_stages: List[str],
    apply: bool,
) -> List[str]:
    removed: List[str] = []

    for stage in invalidated_stages:
        for pattern in STAGE_EVIDENCE.get(stage, []):
            if "*" in pattern or "?" in pattern or "[" in pattern:
                for match in run_root.glob(pattern):
                    if delete_path(match, apply=apply):
                        removed.append(str(match.relative_to(run_root)).replace("\\", "/"))
            else:
                path = run_root / pattern
                if delete_path(path, apply=apply):
                    removed.append(str(path.relative_to(run_root)).replace("\\", "/"))

        stage_record = run_root / "reports" / f"stage_completion_{stage}.yaml"
        if delete_path(stage_record, apply=apply):
            removed.append(str(stage_record.relative_to(run_root)).replace("\\", "/"))

    return sorted(set(removed))


def rewrite_manifest_for_reconciliation(
    manifest_data: Dict[str, Any],
    *,
    trusted_prefix: List[str],
    restart_stage: Optional[str],
) -> Dict[str, Any]:
    root = manifest_data.setdefault("run_manifest", {})
    exec_state = root.setdefault("execution_state", {})

    if trusted_prefix:
        current_stage = trusted_prefix[-1]
        last_stage_status = "done"
    else:
        current_stage = "RUN_BOOTSTRAP"
        last_stage_status = "done"

    if restart_stage is None and trusted_prefix and trusted_prefix[-1] == "STAGE_09_CLOSEOUT_AND_ARCHIVE":
        run_status = "closed"
        next_stage = ""
    else:
        run_status = "active"
        next_stage = restart_stage or ""

    root["status"] = run_status
    exec_state["current_stage"] = current_stage
    exec_state["last_stage_status"] = last_stage_status
    exec_state["next_stage"] = next_stage
    exec_state["completed_stages"] = trusted_prefix

    stage_history = exec_state.get("stage_history", [])
    if isinstance(stage_history, list):
        exec_state["stage_history"] = [
            item for item in stage_history
            if isinstance(item, dict)
            and canonical_stage_id(str(item.get("stage_id", ""))) in trusted_prefix
        ]

    return manifest_data


def rewrite_runs_index_for_reconciliation(
    index_data: Dict[str, Any],
    *,
    manifest_data: Dict[str, Any],
    run_id: str,
) -> Dict[str, Any]:
    root = index_data.setdefault("runs_index", {})
    active_runs = root.setdefault("active_runs", [])
    closed_runs = root.setdefault("closed_runs", [])

    if not isinstance(active_runs, list):
        active_runs = []
        root["active_runs"] = active_runs
    if not isinstance(closed_runs, list):
        closed_runs = []
        root["closed_runs"] = closed_runs

    run_manifest = manifest_data.get("run_manifest", {})
    exec_state = run_manifest.get("execution_state", {})

    scope_binding = run_manifest.get("scope_binding", {})
    scope_id = scope_binding.get("scope_id", "")
    scope_key = run_manifest.get("scope_key", "")
    run_status = run_manifest.get("status", "active")
    current_stage = exec_state.get("current_stage", "")
    next_stage = exec_state.get("next_stage", "")

    displayed_stage = next_stage if next_stage else current_stage

    updated_entry = {
        "run_id": run_id,
        "scope_id": scope_id,
        "scope_key": scope_key,
        "run_status": run_status,
        "current_stage": displayed_stage,
        "mode": run_manifest.get("mode", "bounded_local_run"),
        "run_manifest_ref": f"docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml",
    }

    active_runs[:] = [entry for entry in active_runs if entry.get("run_id") != run_id]
    closed_runs[:] = [entry for entry in closed_runs if entry.get("run_id") != run_id]

    if run_status == "closed":
        closed_runs.append(updated_entry)
    else:
        active_runs.append(updated_entry)

    return index_data


def rebuild_run_context(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    apply: bool,
) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        str(repo_root / "docs" / "patcher" / "shared" / "build_run_context.py"),
        "--pipeline", pipeline_id,
        "--run-id", run_id,
        "--repo-root", str(repo_root),
    ]
    return run_script(cmd, apply=apply, cwd=repo_root)


def main() -> int:
    args = parse_args()
    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline for now: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    run_manifest_path = run_root / "run_manifest.yaml"
    runs_index_path = pipeline_root / "runs" / "index.yaml"

    if not run_root.exists():
        raise SystemExit(f"Run root does not exist: {run_root}")
    if not run_manifest_path.exists():
        raise SystemExit(f"run_manifest.yaml missing: {run_manifest_path}")

    manifest_data = load_yaml(run_manifest_path)
    index_data = load_yaml(runs_index_path)
    run_manifest_root = manifest_data.get("run_manifest", {})
    mode = run_manifest_root.get("mode", "")

    if mode != "bounded_local_run":
        raise SystemExit(
            f"Unsupported mode for this initial version: {mode!r}. "
            "This first implementation supports bounded_local_run only."
        )

    repaired_artifacts, repair_commands = repair_derivable_inputs(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        run_root=run_root,
        apply=args.apply,
    )

    # Reload after potential repairs
    manifest_data = load_yaml(run_manifest_path)
    run_manifest_root = manifest_data.get("run_manifest", {})

    claimed_done = derive_claimed_done_stages(run_manifest_root)
    claimed_prefix = contiguous_claimed_prefix(claimed_done)

    trusted_prefix: List[str] = []
    stage_missing_map: Dict[str, List[str]] = {}
    first_non_trusted_stage: Optional[str] = None

    for stage in claimed_prefix:
        ok, missing = stage_evidence_status(run_root, stage)
        if ok:
            trusted_prefix.append(stage)
        else:
            first_non_trusted_stage = stage
            stage_missing_map[stage] = missing
            break

    exec_state = run_manifest_root.get("execution_state", {})
    current_stage = canonical_stage_id(str(exec_state.get("current_stage", "")))
    last_stage_status = str(exec_state.get("last_stage_status", ""))
    next_stage = canonical_stage_id(str(exec_state.get("next_stage", ""))) if exec_state.get("next_stage") else ""

    if first_non_trusted_stage:
        restart_stage = first_non_trusted_stage
    elif current_stage in STAGE_ORDER and last_stage_status in {"in_progress", "blocked", "failed"}:
        restart_stage = current_stage
    elif next_stage in STAGE_ORDER:
        restart_stage = next_stage
    elif trusted_prefix:
        restart_stage = next_stage_after(trusted_prefix[-1])
    else:
        restart_stage = "STAGE_01_CHALLENGE"

    if trusted_prefix and trusted_prefix[-1] == "STAGE_09_CLOSEOUT_AND_ARCHIVE" and restart_stage is None:
        reconciliation_status = "run_reconciled_without_truncation"
        invalidated_stages: List[str] = []
    else:
        invalidated_stages = []
        if restart_stage in STAGE_ORDER:
            restart_idx = stage_index(restart_stage)
            for stage in claimed_done:
                if stage_index(stage) >= restart_idx:
                    invalidated_stages.append(stage)
            if current_stage in STAGE_ORDER and stage_index(current_stage) >= restart_idx:
                invalidated_stages.append(current_stage)
        invalidated_stages = sorted(set(invalidated_stages), key=stage_index)
        reconciliation_status = (
            "run_truncated_to_restart_stage" if invalidated_stages else "run_reconciled_without_truncation"
        )

    removed_artifacts = invalidate_downstream_artifacts(
        run_root=run_root,
        invalidated_stages=invalidated_stages,
        apply=args.apply,
    )

    manifest_data = rewrite_manifest_for_reconciliation(
        manifest_data,
        trusted_prefix=trusted_prefix,
        restart_stage=restart_stage,
    )
    index_data = rewrite_runs_index_for_reconciliation(
        index_data,
        manifest_data=manifest_data,
        run_id=args.run_id,
    )

    if args.apply:
        dump_yaml(run_manifest_path, manifest_data)
        dump_yaml(runs_index_path, index_data)

    run_context_command = rebuild_run_context(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        apply=args.apply,
    )

    final_manifest = manifest_data.get("run_manifest", {})
    final_exec_state = final_manifest.get("execution_state", {})

    result = {
        "reconcile_run": {
            "status": "DONE",
            "apply": args.apply,
            "pipeline_id": args.pipeline,
            "run_id": args.run_id,
            "mode": mode,
            "reconciliation_status": reconciliation_status,
            "trusted_prefix_end_stage": trusted_prefix[-1] if trusted_prefix else "",
            "restart_stage": restart_stage or "",
            "claimed_done_stages": claimed_done,
            "trusted_prefix": trusted_prefix,
            "missing_evidence_by_stage": stage_missing_map,
            "repaired_artifacts": repaired_artifacts,
            "repair_commands": repair_commands,
            "invalidated_downstream_stage_set": invalidated_stages,
            "removed_artifacts": removed_artifacts,
            "run_status_after_reconciliation": final_manifest.get("status", ""),
            "current_stage_after_reconciliation": final_exec_state.get("current_stage", ""),
            "next_stage_after_reconciliation": final_exec_state.get("next_stage", ""),
            "run_context_rebuild": run_context_command,
            "next_best_action": "CONTINUE_ACTIVE_RUN" if restart_stage else "INSPECT",
            "next_best_action_reason": (
                f"Run repositioned on {restart_stage}." if restart_stage
                else "Run is fully reconciled and does not require stage restart."
            ),
        }
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
