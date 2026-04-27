#!/usr/bin/env python3
"""Run PHASE_12 extract validation on a synthetic patch_lifecycle run.

This script creates a minimal synthetic run manifest, then executes the canonical
deterministic scripts:

  1. docs/patcher/shared/materialize_run_inputs.py
  2. docs/patcher/shared/extract_scope_slice.py

It validates that:
  - scope_manifest.writable_perimeter.ids matches patch_lifecycle scope target.ids
  - scope_extract target/found/missing counts are coherent
  - neighbor_extract target/found/missing counts are coherent
  - every scope_extract entry belongs to a writable target id
  - every neighbor_extract entry belongs to a mandatory read id
  - no missing ids remain

It writes:
  - tmp/scope_extract_validation_report.yaml

It also materializes a synthetic run under:
  docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01

This is a diagnostic validation run, not a real bounded_local_run.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


RUN_ID = "CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01"
PIPELINE = "constitution"
SCOPE_KEY = "patch_lifecycle"

RUN_ROOT = Path("docs/pipelines/constitution/runs") / RUN_ID
INPUTS_DIR = RUN_ROOT / "inputs"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.yaml"
SCOPE_DEF_PATH = Path("docs/pipelines/constitution/scope_catalog/scope_definitions/patch_lifecycle.yaml")
REPORT_PATH = Path("tmp/scope_extract_validation_report.yaml")

MATERIALIZE_SCRIPT = Path("docs/patcher/shared/materialize_run_inputs.py")
EXTRACT_SCRIPT = Path("docs/patcher/shared/extract_scope_slice.py")


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def write_synthetic_run_manifest() -> None:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_manifest": {
            "schema_version": 0.1,
            "run_id": RUN_ID,
            "pipeline_id": PIPELINE,
            "scope_key": SCOPE_KEY,
            "run_mode": "synthetic_extract_validation",
            "status": "synthetic_validation_only",
            "purpose": (
                "PHASE_12 validation of deterministic scope_extract.yaml and neighbor_extract.yaml generation "
                "for patch_lifecycle."
            ),
            "scope_definition_ref": SCOPE_DEF_PATH.as_posix(),
            "notes": [
                "This is not a real bounded_local_run.",
                "This run exists only to validate materialize_run_inputs.py and extract_scope_slice.py.",
                "No canonical core files are modified by this validation.",
            ],
        }
    }

    RUN_MANIFEST_PATH.write_text(dump_yaml(manifest), encoding="utf-8")


def run_command(command: list[str]) -> dict[str, Any]:
    proc = subprocess.run(command, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def get_scope_def_ids() -> list[str]:
    doc = load_yaml(SCOPE_DEF_PATH)
    return sorted(doc["scope_definition"]["target"]["ids"] or [])


def get_scope_def_neighbor_ids() -> list[str]:
    doc = load_yaml(SCOPE_DEF_PATH)
    return sorted(doc["scope_definition"]["default_neighbors_to_read"]["ids"] or [])


def extract_root(doc: dict[str, Any], key: str) -> dict[str, Any]:
    root = doc.get(key)
    if not isinstance(root, dict):
        raise ValueError(f"Missing root key: {key}")
    return root


def matched_ids_from_entries(entries: list[dict[str, Any]]) -> list[str]:
    return sorted(
        entry.get("_matched_id")
        for entry in entries
        if isinstance(entry, dict) and entry.get("_matched_id")
    )


def source_cores_from_entries(entries: list[dict[str, Any]]) -> list[str]:
    return sorted({
        entry.get("_source_core")
        for entry in entries
        if isinstance(entry, dict) and entry.get("_source_core")
    })


def validate_outputs() -> tuple[str, list[str], dict[str, Any]]:
    findings: list[str] = []

    scope_def_ids = get_scope_def_ids()
    scope_def_neighbor_ids = get_scope_def_neighbor_ids()

    scope_manifest = extract_root(load_yaml(INPUTS_DIR / "scope_manifest.yaml"), "scope_manifest")
    impact_bundle = extract_root(load_yaml(INPUTS_DIR / "impact_bundle.yaml"), "impact_bundle")
    integration_gate = extract_root(load_yaml(INPUTS_DIR / "integration_gate.yaml"), "integration_gate")
    scope_extract = extract_root(load_yaml(INPUTS_DIR / "scope_extract.yaml"), "scope_extract")
    neighbor_extract = extract_root(load_yaml(INPUTS_DIR / "neighbor_extract.yaml"), "neighbor_extract")

    manifest_ids = sorted(scope_manifest.get("writable_perimeter", {}).get("ids", []) or [])
    mandatory_read_ids = sorted(impact_bundle.get("mandatory_reads", {}).get("ids", []) or [])

    scope_target_ids = sorted(scope_extract.get("target_ids", []) or [])
    scope_found_ids = sorted(scope_extract.get("found_ids", []) or [])
    scope_missing_ids = sorted(scope_extract.get("missing_ids", []) or [])
    scope_matched_ids = matched_ids_from_entries(scope_extract.get("entries", []) or [])

    neighbor_target_ids = sorted(neighbor_extract.get("target_ids", []) or [])
    neighbor_found_ids = sorted(neighbor_extract.get("found_ids", []) or [])
    neighbor_missing_ids = sorted(neighbor_extract.get("missing_ids", []) or [])
    neighbor_matched_ids = matched_ids_from_entries(neighbor_extract.get("entries", []) or [])

    if manifest_ids != scope_def_ids:
        findings.append("scope_manifest_ids_do_not_match_scope_definition_ids")

    if mandatory_read_ids != scope_def_neighbor_ids:
        findings.append("impact_bundle_mandatory_reads_do_not_match_scope_definition_neighbors")

    if scope_target_ids != manifest_ids:
        findings.append("scope_extract_target_ids_do_not_match_scope_manifest_ids")

    if scope_found_ids != scope_target_ids:
        findings.append("scope_extract_found_ids_do_not_match_target_ids")

    if scope_missing_ids:
        findings.append("scope_extract_has_missing_ids")

    if sorted(set(scope_matched_ids)) != scope_target_ids:
        findings.append("scope_extract_entries_do_not_cover_target_ids")

    if len(scope_matched_ids) != len(scope_target_ids):
        findings.append("scope_extract_entry_count_does_not_match_target_count")

    if neighbor_target_ids != mandatory_read_ids:
        findings.append("neighbor_extract_target_ids_do_not_match_impact_bundle_mandatory_reads")

    if neighbor_found_ids != neighbor_target_ids:
        findings.append("neighbor_extract_found_ids_do_not_match_target_ids")

    if neighbor_missing_ids:
        findings.append("neighbor_extract_has_missing_ids")

    if sorted(set(neighbor_matched_ids)) != neighbor_target_ids:
        findings.append("neighbor_extract_entries_do_not_cover_target_ids")

    if len(neighbor_matched_ids) != len(neighbor_target_ids):
        findings.append("neighbor_extract_entry_count_does_not_match_target_count")

    if integration_gate.get("status") != "open":
        findings.append("integration_gate_status_is_not_open")

    scope_source_cores = source_cores_from_entries(scope_extract.get("entries", []) or [])
    neighbor_source_cores = source_cores_from_entries(neighbor_extract.get("entries", []) or [])

    details = {
        "run_id": RUN_ID,
        "scope_key": SCOPE_KEY,
        "synthetic_run_root": RUN_ROOT.as_posix(),
        "scope_definition_ref": SCOPE_DEF_PATH.as_posix(),
        "scope_manifest": {
            "id_count": len(manifest_ids),
            "ids": manifest_ids,
        },
        "impact_bundle": {
            "mandatory_read_count": len(mandatory_read_ids),
            "mandatory_read_ids": mandatory_read_ids,
        },
        "scope_extract": {
            "target_count": len(scope_target_ids),
            "found_count": len(scope_found_ids),
            "missing_count": len(scope_missing_ids),
            "entry_count": len(scope_extract.get("entries", []) or []),
            "source_cores": scope_source_cores,
            "missing_ids": scope_missing_ids,
            "path": (INPUTS_DIR / "scope_extract.yaml").as_posix(),
        },
        "neighbor_extract": {
            "target_count": len(neighbor_target_ids),
            "found_count": len(neighbor_found_ids),
            "missing_count": len(neighbor_missing_ids),
            "entry_count": len(neighbor_extract.get("entries", []) or []),
            "source_cores": neighbor_source_cores,
            "missing_ids": neighbor_missing_ids,
            "path": (INPUTS_DIR / "neighbor_extract.yaml").as_posix(),
        },
        "integration_gate": {
            "status": integration_gate.get("status"),
            "gate_check_count": len(integration_gate.get("gate_checks", []) or []),
            "path": (INPUTS_DIR / "integration_gate.yaml").as_posix(),
        },
    }

    status = "PASS" if not findings else "FAIL"
    return status, findings, details


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PHASE_12 extract validation.")
    parser.add_argument("--skip-execution", action="store_true", help="Validate existing outputs without rerunning scripts.")
    args = parser.parse_args()

    if not SCOPE_DEF_PATH.exists():
        raise FileNotFoundError(f"Missing scope definition: {SCOPE_DEF_PATH}")

    write_synthetic_run_manifest()

    commands = []

    if not args.skip_execution:
        commands.append(
            run_command([
                sys.executable,
                MATERIALIZE_SCRIPT.as_posix(),
                "--pipeline",
                PIPELINE,
                "--run-id",
                RUN_ID,
            ])
        )
        commands.append(
            run_command([
                sys.executable,
                EXTRACT_SCRIPT.as_posix(),
                "--pipeline",
                PIPELINE,
                "--run-id",
                RUN_ID,
            ])
        )

    command_failures = [
        command for command in commands
        if command["returncode"] != 0
    ]

    if command_failures:
        report = {
            "scope_extract_validation_report": {
                "schema_version": 0.1,
                "status": "FAIL",
                "phase": "PHASE_12_EXTRACT_VALIDATION",
                "run_id": RUN_ID,
                "blocking_findings": ["command_execution_failed"],
                "commands": commands,
            }
        }
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(dump_yaml(report), encoding="utf-8")
        print(f"status: FAIL")
        print(f"blocking_findings: ['command_execution_failed']")
        print(f"written: {REPORT_PATH}")
        return 2

    status, findings, details = validate_outputs()

    report = {
        "scope_extract_validation_report": {
            "schema_version": 0.1,
            "status": status,
            "phase": "PHASE_12_EXTRACT_VALIDATION",
            "validation_target": "synthetic_patch_lifecycle_run",
            "run_id": RUN_ID,
            "scope_key": SCOPE_KEY,
            "commands": commands,
            "details": details,
            "blocking_findings": findings,
            "notes": [
                "This validates deterministic extract generation for a synthetic patch_lifecycle run.",
                "The synthetic run is not a real bounded_local_run and should not be promoted.",
                "scope_extract.yaml is expected to contain only writable target IDs.",
                "neighbor_extract.yaml is expected to contain mandatory read IDs only.",
            ],
        }
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(dump_yaml(report), encoding="utf-8")

    print(f"status: {status}")
    print(f"blocking_findings: {findings}")
    print(f"written: {REPORT_PATH}")

    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
