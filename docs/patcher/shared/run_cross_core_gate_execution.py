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

GATE_ORDER = [
    "validate_cross_core_execution_contract",
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

def write_report(report_path: Path, status: str, contract_path: Path, contract_validation_report: Path, rc: int, downstream_executed: bool, reason: str) -> None:
    lines = [
        "cross_core_gate_execution:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        f"  contract: {str(contract_path).replace(chr(92), chr(47))}",
        f"  contract_exists: {str(contract_path.exists()).lower()}",
        f"  contract_sha256: {sha(contract_path) if contract_path.exists() else None}",
        f"  contract_validation_report: {str(contract_validation_report).replace(chr(92), chr(47))}",
        f"  contract_validation_return_code: {rc}",
        f"  downstream_gates_executed: {str(downstream_executed).lower()}",
        "  gate_order:",
    ]
    lines.extend([f"    - {gate}" for gate in GATE_ORDER])
    lines.extend([
        "  current_authorizations:",
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
    parser.add_argument("--contract-validation-report", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    contract_path = REPO / args.contract
    contract_validation_report = REPO / args.contract_validation_report
    report_path = REPO / args.report

    if not contract_path.exists():
        write_report(report_path, "FAIL", contract_path, contract_validation_report, 1, False, "Contract file is missing.")
        print("FAIL")
        return 1

    if not CONTRACT_VALIDATOR.exists():
        write_report(report_path, "FAIL", contract_path, contract_validation_report, 1, False, "Contract validator is missing.")
        print("FAIL")
        return 1

    result = subprocess.run(
        [sys.executable, str(CONTRACT_VALIDATOR), "--input", str(contract_path), "--report", str(contract_validation_report)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    validation_text = contract_validation_report.read_text(encoding="utf-8") if contract_validation_report.exists() else ""

    if result.returncode == 2 and "status: BLOCKED_NOT_AUTHORIZED" in validation_text:
        write_report(report_path, "BLOCKED_NOT_AUTHORIZED", contract_path, contract_validation_report, result.returncode, False, "Execution contract is request-bound but not write-authorized; downstream gates were not executed.")
        print("BLOCKED_NOT_AUTHORIZED")
        return 2

    if result.returncode == 2 and "status: BLOCKED_TEMPLATE_ONLY" in validation_text:
        write_report(report_path, "BLOCKED_TEMPLATE_ONLY", contract_path, contract_validation_report, result.returncode, False, "Template execution contract cannot execute downstream gates.")
        print("BLOCKED_TEMPLATE_ONLY")
        return 2

    if result.returncode == 0 and "status: PASS_SHAPE_ONLY" in validation_text:
        write_report(report_path, "BLOCKED_DOWNSTREAM_GATE_INPUTS_NOT_IMPLEMENTED_IN_PHASE_58", contract_path, contract_validation_report, result.returncode, False, "Contract shape passed, but Phase 58 only defines the generic runner and does not execute downstream mutating gates.")
        print("BLOCKED_DOWNSTREAM_GATE_INPUTS_NOT_IMPLEMENTED_IN_PHASE_58")
        return 2

    write_report(report_path, "FAIL", contract_path, contract_validation_report, result.returncode, False, "Execution contract validation failed unexpectedly.")
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    print("FAIL")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
