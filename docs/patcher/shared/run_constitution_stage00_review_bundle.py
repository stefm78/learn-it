#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

RUNS_INDEX = Path("docs/pipelines/constitution/runs/index.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/stage00_review_bundle_report.yaml")

COMMANDS = [
    ("validate_governance_backlog_lifecycle", ["docs/patcher/shared/validate_governance_backlog_lifecycle.py", "--report", "docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml"], ["docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml"]),
    ("report_governance_backlog", ["docs/patcher/shared/report_governance_backlog.py", "--report", "docs/pipelines/constitution/reports/governance_backlog_report.yaml"], ["docs/pipelines/constitution/reports/governance_backlog_report.yaml"]),
    ("analyze_constitution_scope_partition", ["docs/patcher/shared/analyze_constitution_scope_partition.py", "--report", "docs/pipelines/constitution/reports/scope_partition_review_report.yaml"], ["docs/pipelines/constitution/reports/scope_partition_review_report.yaml"]),
    ("score_constitution_scope_maturity", ["docs/patcher/shared/score_constitution_scope_maturity.py", "--report", "docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml"], ["docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml"]),
    ("report_constitution_neighbor_ids_governance", ["docs/patcher/shared/report_constitution_neighbor_ids_governance.py", "--report", "docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml"], ["docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml"]),
    ("report_constitution_neighbor_declaration_inventory", ["docs/patcher/shared/report_constitution_neighbor_declaration_inventory.py", "--report", "docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml"], ["docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml"]),
    ("refresh_constitution_pipeline_signals", ["docs/patcher/shared/refresh_constitution_pipeline_signals.py", "--apply"], ["docs/pipelines/constitution/signals.yaml", "docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml", "docs/pipelines/constitution/reports/pipeline_signals_refresh_report.yaml"]),
]

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid YAML root: {path}")
    return data

def get_active_runs() -> list[Any]:
    root = load_yaml(RUNS_INDEX).get("runs_index", {})
    active = root.get("active_runs", []) if isinstance(root, dict) else []
    return active if isinstance(active, list) else []

def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic Constitution STAGE_00 review diagnostics bundle.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-failure", action="store_true")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    report_path = Path(args.report)
    active_runs = get_active_runs()
    command_results: list[dict[str, Any]] = []
    report = {
        "stage00_review_bundle_report": {
            "schema_version": "0.1",
            "pipeline_id": "constitution",
            "stage_id": "STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN",
            "mode": "partition_refresh_diagnostic_bundle",
            "started_at": utc_now(),
            "finished_at": None,
            "status": "RUNNING",
            "dry_run": bool(args.dry_run),
            "active_run_check": {
                "active_run_count": len(active_runs),
                "active_runs": active_runs,
                "no_active_run_confirmed": len(active_runs) == 0,
            },
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "governance_backlog_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "cores": "not_modified",
                "reports": "written",
                "signals_yaml": "derived_refresh_only",
                "bounded_run_preflight_report": "derived_refresh_only",
            },
            "commands": command_results,
            "outputs": sorted({out for _, _, outs in COMMANDS for out in outs} | {str(report_path)}),
            "notes": [],
        }
    }
    root = report["stage00_review_bundle_report"]
    if active_runs:
        root["status"] = "BLOCKED_ACTIVE_RUNS_PRESENT"
        root["finished_at"] = utc_now()
        root["notes"].append("STAGE_00 review bundle requires no active constitution run.")
        write_report(report_path, report)
        print(f"Status: {root['status']}")
        print(f"Wrote {report_path}")
        return 2

    overall = "PASS_DRY_RUN" if args.dry_run else "PASS"
    for command_id, argv, outputs in COMMANDS:
        full = [sys.executable] + argv
        result = {"id": command_id, "command": " ".join(full), "outputs": outputs, "executed": not args.dry_run}
        print(f"[{command_id}]")
        if args.dry_run:
            result.update({"status": "DRY_RUN", "returncode": None, "stdout_tail": "", "stderr_tail": ""})
            print("  DRY_RUN")
        else:
            proc = subprocess.run(full, text=True, capture_output=True, check=False)
            result.update({"status": "PASS" if proc.returncode == 0 else "FAIL", "returncode": proc.returncode, "stdout_tail": proc.stdout[-4000:], "stderr_tail": proc.stderr[-4000:]})
            print(f"  {result['status']}")
            if proc.returncode != 0:
                overall = "FAIL"
                if proc.stderr:
                    print(proc.stderr[-2000:])
                command_results.append(result)
                if not args.continue_on_failure:
                    break
        command_results.append(result)

    root["status"] = overall
    root["finished_at"] = utc_now()
    if overall == "PASS":
        root["notes"].append("All deterministic STAGE_00 diagnostic commands passed.")
    elif overall == "PASS_DRY_RUN":
        root["notes"].append("Dry-run only; commands were not executed.")
    else:
        root["notes"].append("At least one deterministic STAGE_00 diagnostic command failed.")
    write_report(report_path, report)
    print(f"Status: {overall}")
    print(f"Wrote {report_path}")
    return 0 if overall in {"PASS", "PASS_DRY_RUN"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
