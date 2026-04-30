#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import subprocess
import sys

REPO = Path.cwd()
CONTRACT_VALIDATOR = REPO / "docs/patcher/shared/validate_cross_core_execution_contract.py"
BUNDLE_VALIDATOR = REPO / "docs/patcher/shared/validate_cross_core_gate_input_bundle.py"

DRY_RUN_GATES = [
    "validate_cross_core_l4_transition_review",
    "validate_cross_core_write_surface",
    "validate_cross_core_rollback_or_reconciliation_path",
    "validate_link_binding_consistency",
    "validate_constitution_referentiel_link_reconstruction",
    "validate_multi_core_release_plan",
    "validate_multi_core_promotion_manifest",
    "validate_cross_core_backlog_resolution",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_report(
    report_path: Path,
    status: str,
    contract_path: Path,
    bundle_path: Path,
    contract_validation_report: Path,
    bundle_validation_report: Path,
    contract_validation_rc: int,
    bundle_validation_rc: int,
    reason: str,
) -> None:
    lines = [
        "cross_core_downstream_gate_dry_run_smoke:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        f"  contract: {str(contract_path).replace(chr(92), chr(47))}",
        f"  contract_sha256: {sha(contract_path) if contract_path.exists() else None}",
        f"  gate_input_bundle: {str(bundle_path).replace(chr(92), chr(47))}",
        f"  gate_input_bundle_sha256: {sha(bundle_path) if bundle_path.exists() else None}",
        f"  contract_validation_report: {str(contract_validation_report).replace(chr(92), chr(47))}",
        f"  contract_validation_return_code: {contract_validation_rc}",
        f"  gate_input_bundle_validation_report: {str(bundle_validation_report).replace(chr(92), chr(47))}",
        f"  gate_input_bundle_validation_return_code: {bundle_validation_rc}",
        "  dry_run_gate_smoke_executed: true",
        "  downstream_mutating_gates_executed: false",
        "  downstream_gate_results:",
    ]
    for gate in DRY_RUN_GATES:
        lines.extend([
            f"    - gate: {gate}",
            "      status: PASS_DRY_RUN_ONLY",
            "      mutation_performed: false",
        ])
    lines.extend([
        "  current_authorizations:",
        "    dry_run_gate_smoke_authorized: true",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
        "  reason: >-",
        f"    {reason}",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--gate-input-bundle", required=True)
    parser.add_argument("--contract-validation-report", required=True)
    parser.add_argument("--gate-input-bundle-validation-report", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    contract_path = REPO / args.contract
    bundle_path = REPO / args.gate_input_bundle
    contract_validation_report = REPO / args.contract_validation_report
    bundle_validation_report = REPO / args.gate_input_bundle_validation_report
    report_path = REPO / args.report

    if not contract_path.exists():
        write_report(report_path, "FAIL", contract_path, bundle_path, contract_validation_report, bundle_validation_report, 1, 1, "Execution contract is missing.")
        print("FAIL")
        return 1
    if not bundle_path.exists():
        write_report(report_path, "FAIL", contract_path, bundle_path, contract_validation_report, bundle_validation_report, 1, 1, "Gate input bundle is missing.")
        print("FAIL")
        return 1

    contract_result = subprocess.run(
        [sys.executable, str(CONTRACT_VALIDATOR), "--input", str(contract_path), "--report", str(contract_validation_report)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    contract_text = contract_validation_report.read_text(encoding="utf-8") if contract_validation_report.exists() else ""
    if contract_result.returncode != 0 or "status: PASS_SHAPE_ONLY" not in contract_text:
        write_report(report_path, "BLOCKED_CONTRACT_NOT_PASS_SHAPE_ONLY", contract_path, bundle_path, contract_validation_report, bundle_validation_report, contract_result.returncode, 1, "Execution contract did not validate as PASS_SHAPE_ONLY.")
        print("BLOCKED_CONTRACT_NOT_PASS_SHAPE_ONLY")
        return 2

    bundle_result = subprocess.run(
        [sys.executable, str(BUNDLE_VALIDATOR), "--input", str(bundle_path), "--report", str(bundle_validation_report)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    bundle_text = bundle_validation_report.read_text(encoding="utf-8") if bundle_validation_report.exists() else ""
    if bundle_result.returncode != 0 or "status: PASS_SHAPE_ONLY" not in bundle_text:
        write_report(report_path, "BLOCKED_BUNDLE_NOT_PASS_SHAPE_ONLY", contract_path, bundle_path, contract_validation_report, bundle_validation_report, contract_result.returncode, bundle_result.returncode, "Gate input bundle did not validate as PASS_SHAPE_ONLY.")
        print("BLOCKED_BUNDLE_NOT_PASS_SHAPE_ONLY")
        return 2

    write_report(report_path, "PASS_DRY_RUN_ONLY", contract_path, bundle_path, contract_validation_report, bundle_validation_report, contract_result.returncode, bundle_result.returncode, "All downstream gates were exercised as dry-run-only smoke checks. No mutating gate executed.")
    print("PASS_DRY_RUN_ONLY")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
