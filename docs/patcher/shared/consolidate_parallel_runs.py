#!/usr/bin/env python3
"""Consolidate N parallel scoped run sandboxes into a single work/consolidation/ Core set.

Preconditions (all checked before any write):
  - All provided run_ids must have a sandbox under
    docs/pipelines/constitution/runs/<run_id>/work/05_apply/sandbox/
  - All provided run_ids must have integration_gate.yaml with status: cleared or not_applicable
    (warning only in --dry-run mode; blocking in real run)
  - Scope IDs across all runs must be disjoint (no overlapping writable IDs)

Output:
  - docs/pipelines/constitution/work/consolidation/constitution.yaml
  - docs/pipelines/constitution/work/consolidation/referentiel.yaml
  - docs/pipelines/constitution/work/consolidation/link.yaml
  - docs/pipelines/constitution/work/consolidation/consolidation_report.yaml

Usage:
  python docs/patcher/shared/consolidate_parallel_runs.py \\
    --runs RUN_A RUN_B RUN_C \\
    --base docs/cores/current \\
    --output docs/pipelines/constitution/work/consolidation \\
    --pipeline constitution \\
    [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def dump_yaml(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Precondition checks
# ---------------------------------------------------------------------------

def check_sandbox_exists(pipeline_runs_root: Path, run_id: str) -> Path:
    sandbox = pipeline_runs_root / run_id / "work" / "05_apply" / "sandbox"
    if not sandbox.exists():
        raise FileNotFoundError(
            f"Sandbox not found for run {run_id}: {sandbox}\n"
            f"STAGE_05_APPLY must be completed before consolidation."
        )
    return sandbox


def check_integration_gate_cleared(
    pipeline_runs_root: Path, run_id: str, dry_run: bool = False
) -> str:
    """Check integration_gate status.

    Returns the status string.
    In dry-run mode: non-cleared status emits a WARNING but does not abort.
    In real mode: non-cleared status raises ValueError (blocking).
    """
    gate_path = pipeline_runs_root / run_id / "inputs" / "integration_gate.yaml"
    if not gate_path.exists():
        raise FileNotFoundError(
            f"integration_gate.yaml not found for run {run_id}: {gate_path}"
        )
    gate = load_yaml(gate_path)
    status = (
        gate.get("integration_gate", {}).get("status")
        or gate.get("status", "")
    )
    if status not in ("cleared", "not_applicable"):
        msg = (
            f"integration_gate not cleared for run {run_id}: status='{status}'.\n"
            f"All integration gates must be explicitly cleared before real consolidation."
        )
        if dry_run:
            print(f"  WARNING (dry-run): {msg}")
        else:
            raise ValueError(msg)
    return status


def collect_scope_writable_ids(pipeline_runs_root: Path, run_id: str) -> set[str]:
    """Extract the set of writable IDs declared in the run's scope_manifest."""
    scope_manifest_path = pipeline_runs_root / run_id / "inputs" / "scope_manifest.yaml"
    if not scope_manifest_path.exists():
        return set()
    sm = load_yaml(scope_manifest_path)
    sm_root = sm.get("scope_manifest", sm)
    writable: list[str] = (
        sm_root.get("writable_ids")
        or sm_root.get("scope", {}).get("writable_ids")
        or []
    )
    return set(writable)


def check_scope_disjointness(
    run_ids: list[str],
    scope_ids_by_run: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """Return list of conflicts. Empty list = disjoint = safe to merge."""
    conflicts: list[dict[str, Any]] = []
    runs = list(run_ids)
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            a, b = runs[i], runs[j]
            overlap = scope_ids_by_run[a] & scope_ids_by_run[b]
            if overlap:
                conflicts.append({
                    "run_a": a,
                    "run_b": b,
                    "overlapping_ids": sorted(overlap),
                })
    return conflicts


# ---------------------------------------------------------------------------
# Core file discovery
# ---------------------------------------------------------------------------

CORE_FILES = ["constitution.yaml", "referentiel.yaml", "link.yaml"]


def find_core_files_in_sandbox(sandbox_root: Path) -> dict[str, Path]:
    """Locate Core files inside a sandbox. Supports both flat and canonical layouts.

    Canonical layout: sandbox/docs/cores/current/<file>
    Flat layout:      sandbox/<file>
    """
    canonical_dir = sandbox_root / "docs" / "cores" / "current"
    result: dict[str, Path] = {}
    for fname in CORE_FILES:
        canonical_path = canonical_dir / fname
        flat_path = sandbox_root / fname
        if canonical_path.exists():
            result[fname] = canonical_path
        elif flat_path.exists():
            result[fname] = flat_path
    return result


# ---------------------------------------------------------------------------
# Merge logic
# ---------------------------------------------------------------------------

def _get_top_level_key(data: dict[str, Any], filename: str) -> str:
    """Infer the top-level YAML key from the filename (e.g. 'constitution')."""
    stem = Path(filename).stem
    if stem in data:
        return stem
    keys = list(data.keys())
    return keys[0] if keys else stem


def merge_core_files(
    base_path: Path,
    filename: str,
    sandbox_files: list[tuple[str, Path]],
    scope_ids_by_run: dict[str, set[str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Merge N patched Core files into one.

    Strategy:
    - Start from base (current/) as the reference
    - For each run, overwrite only the IDs that belong to that run's scope
    - IDs not in any scope come from base unchanged

    Returns (merged_data, merge_log).
    """
    base_data = load_yaml(base_path / filename)
    top_key = _get_top_level_key(base_data, filename)
    base_entries: list[dict[str, Any]] = base_data.get(top_key, [])

    base_index: dict[str, dict[str, Any]] = {}
    base_order: list[str] = []
    for entry in base_entries:
        eid = entry.get("id", "")
        base_index[eid] = entry
        base_order.append(eid)

    patched_index = dict(base_index)
    new_ids: list[str] = []
    merge_log: list[dict[str, Any]] = []

    for run_id, patched_path in sandbox_files:
        if not patched_path.exists():
            merge_log.append({
                "run_id": run_id,
                "file": filename,
                "status": "skipped",
                "reason": "file not found in sandbox",
            })
            continue

        patched_data = load_yaml(patched_path)
        patched_entries: list[dict[str, Any]] = patched_data.get(top_key, [])
        run_scope_ids = scope_ids_by_run.get(run_id, set())
        applied_ids: list[str] = []

        for entry in patched_entries:
            eid = entry.get("id", "")
            if not run_scope_ids or eid in run_scope_ids:
                if eid not in patched_index:
                    new_ids.append(eid)
                patched_index[eid] = entry
                applied_ids.append(eid)

        merge_log.append({
            "run_id": run_id,
            "file": filename,
            "status": "applied",
            "applied_ids_count": len(applied_ids),
            "applied_ids": applied_ids,
        })

    merged_entries: list[dict[str, Any]] = []
    for eid in base_order:
        merged_entries.append(patched_index[eid])
    for eid in new_ids:
        merged_entries.append(patched_index[eid])

    merged_data = {top_key: merged_entries}
    return merged_data, merge_log


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_consolidation_report(
    run_ids: list[str],
    merge_logs: dict[str, list[dict[str, Any]]],
    scope_ids_by_run: dict[str, set[str]],
    conflicts: list[dict[str, Any]],
    output_path: Path,
    dry_run: bool,
    gate_warnings: list[str],
) -> dict[str, Any]:
    report = {
        "consolidation_report": {
            "schema_version": "0.1",
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "dry_run": dry_run,
            "status": "PASS" if not conflicts else "FAIL",
            "participating_runs": run_ids,
            "scope_disjointness": {
                "status": "PASS" if not conflicts else "FAIL",
                "conflicts": conflicts,
            },
            "merge_log": [
                {"file": fname, "entries": logs}
                for fname, logs in merge_logs.items()
            ],
            "output_path": str(output_path),
            "warnings": gate_warnings,
            "note": (
                "Dry run — no files written."
                if dry_run
                else "Consolidation applied to work/consolidation/."
            ),
        }
    }
    return report


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consolidate N parallel scoped run sandboxes into a single work/consolidation/ Core set."
    )
    parser.add_argument(
        "--runs",
        nargs="+",
        required=True,
        metavar="RUN_ID",
        help="One or more run IDs to consolidate.",
    )
    parser.add_argument(
        "--base",
        default="docs/cores/current",
        help="Base Core directory (current/). Default: docs/cores/current",
    )
    parser.add_argument(
        "--output",
        default="docs/pipelines/constitution/work/consolidation",
        help="Output directory. Default: docs/pipelines/constitution/work/consolidation",
    )
    parser.add_argument(
        "--pipeline",
        default="constitution",
        help="Pipeline ID. Default: constitution",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check preconditions and produce report without writing output files.",
    )
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    pipeline_runs_root = repo_root / "docs" / "pipelines" / args.pipeline / "runs"
    base_path = repo_root / Path(args.base)
    output_path = repo_root / Path(args.output)
    run_ids: list[str] = args.runs

    print(f"Consolidating {len(run_ids)} run(s): {', '.join(run_ids)}")
    print(f"Base: {base_path}")
    print(f"Output: {output_path}")
    if args.dry_run:
        print("DRY RUN — no files will be written.")

    # --- Precondition checks ---
    sandboxes: dict[str, Path] = {}
    scope_ids_by_run: dict[str, set[str]] = {}
    gate_warnings: list[str] = []

    for run_id in run_ids:
        print(f"  Checking run: {run_id}")
        try:
            sandbox = check_sandbox_exists(pipeline_runs_root, run_id)
            sandboxes[run_id] = sandbox
        except FileNotFoundError as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            return 1

        try:
            gate_status = check_integration_gate_cleared(
                pipeline_runs_root, run_id, dry_run=args.dry_run
            )
            if gate_status not in ("cleared", "not_applicable"):
                gate_warnings.append(
                    f"{run_id}: integration_gate status='{gate_status}' (not cleared)"
                )
        except (FileNotFoundError, ValueError) as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            return 1

        scope_ids_by_run[run_id] = collect_scope_writable_ids(pipeline_runs_root, run_id)
        print(f"    scope writable IDs: {len(scope_ids_by_run[run_id])}")

    # --- Disjointness check ---
    conflicts = check_scope_disjointness(run_ids, scope_ids_by_run)
    if conflicts:
        print("\nERROR: Scope overlap detected — consolidation aborted.", file=sys.stderr)
        for c in conflicts:
            print(
                f"  {c['run_a']} x {c['run_b']}: overlapping IDs: {c['overlapping_ids']}",
                file=sys.stderr,
            )
        report = build_consolidation_report(
            run_ids, {}, scope_ids_by_run, conflicts, output_path, args.dry_run, gate_warnings
        )
        report_path = output_path / "consolidation_report.yaml"
        if not args.dry_run:
            dump_yaml(report, report_path)
            print(f"\nConsolidation report (FAIL) written to {report_path}")
        return 1

    print("  Scope disjointness: PASS")

    # --- Merge ---
    merge_logs: dict[str, list[dict[str, Any]]] = {}

    for filename in CORE_FILES:
        base_file = base_path / filename
        if not base_file.exists():
            print(f"  WARNING: base file not found, skipping: {base_file}")
            continue

        sandbox_files: list[tuple[str, Path]] = []
        for run_id in run_ids:
            core_files = find_core_files_in_sandbox(sandboxes[run_id])
            patched_path = core_files.get(filename, sandboxes[run_id] / filename)
            sandbox_files.append((run_id, patched_path))

        print(f"  Merging {filename}...")
        merged_data, log = merge_core_files(
            base_path, filename, sandbox_files, scope_ids_by_run
        )
        merge_logs[filename] = log

        if not args.dry_run:
            out_file = output_path / filename
            dump_yaml(merged_data, out_file)
            print(f"    Written: {out_file}")
        else:
            for entry in log:
                print(f"    [{entry['run_id']}] {entry['status']}: {entry.get('applied_ids_count', 0)} IDs")

    # --- Report ---
    report = build_consolidation_report(
        run_ids, merge_logs, scope_ids_by_run, conflicts, output_path, args.dry_run, gate_warnings
    )
    report_path = output_path / "consolidation_report.yaml"
    if not args.dry_run:
        dump_yaml(report, report_path)
        print(f"\nConsolidation report written to {report_path}")
    else:
        print("\nDry run complete — report:")
        print(yaml.safe_dump(report, sort_keys=False, allow_unicode=True))

    print("\nStatus: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
