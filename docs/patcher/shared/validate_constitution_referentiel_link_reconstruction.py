#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import sys

REPO = Path.cwd()
VALIDATOR_ID = 'validate_constitution_referentiel_link_reconstruction'
CONTRACT = 'docs/pipelines/cross_core_contract/validators/validate_constitution_referentiel_link_reconstruction.contract.yaml'
FUTURE_INPUTS = ['docs/pipelines/cross_core_contract/work/03_contract_synthesis/cross_core_execution_contract.yaml', 'docs/pipelines/cross_core_contract/work/07_multi_core_release_planning/multi_core_release_plan.yaml']
REQUIRED_MARKERS = ['constitution_reconstruction_PASS', 'referentiel_reconstruction_PASS', 'link_reconstruction_PASS', 'cross_core_reference_ids_resolvable']

FORBIDDEN_MARKERS = [
    "core_mutation_authorized: true",
    "backlog_closure_authorized: true",
    "release_or_promotion_authorized: true",
    "l4_active_now: true",
    "executable_as_l4_gate_now: true",
    "decision_status: approved",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_contract() -> list[dict]:
    findings = []
    path = REPO / CONTRACT
    if not path.exists():
        return [{"finding_id": "missing_contract", "severity": "blocking", "path": CONTRACT}]
    text = path.read_text(encoding="utf-8")
    required = [
        f"validator_id: {VALIDATOR_ID}",
        "status: contract_defined_inactive",
        "l4_active_now: false",
        "executable_as_l4_gate_now: false",
        "core_mutation_authorized: false",
        "backlog_closure_authorized: false",
        "release_or_promotion_authorized: false",
    ] + REQUIRED_MARKERS
    for marker in required:
        if marker not in text:
            findings.append({"finding_id": "missing_contract_marker", "severity": "blocking", "path": CONTRACT, "message": marker})
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            findings.append({"finding_id": "forbidden_contract_marker", "severity": "blocking", "path": CONTRACT, "message": marker})
    return findings

def check_l4_gate_inputs() -> list[dict]:
    findings = check_contract()
    for rel_path in FUTURE_INPUTS:
        path = REPO / rel_path
        if not path.exists():
            findings.append({"finding_id": "future_l4_input_missing", "severity": "blocking", "path": rel_path})
    return findings

def write_report(report_path: Path, mode: str, status: str, findings: list[dict]) -> None:
    lines = [
        f"{VALIDATOR_ID}_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  validator_id: {VALIDATOR_ID}",
        f"  mode: {mode}",
        f"  status: {status}",
        "  l4_active_now: false",
        "  executable_as_l4_gate_now: false",
        f"  contract: {CONTRACT}",
        "  future_inputs:",
    ]
    for rel_path in FUTURE_INPUTS:
        path = REPO / rel_path
        lines.append(f"    - path: {rel_path}")
        lines.append(f"      exists: {str(path.exists()).lower()}")
        lines.append(f"      sha256: {sha(path) if path.exists() else None}")
    lines.append("  blocking_findings:")
    if findings:
        for item in findings:
            lines.append(f"    - finding_id: {item['finding_id']}")
            lines.append(f"      severity: {item['severity']}")
            lines.append(f"      path: {item['path']}")
            if 'message' in item:
                lines.append(f"      message: {item['message']}")
    else:
        lines.append("    []")
    lines.extend([
        "  result_summary:",
        f"    blocking_finding_count: {len(findings)}",
        "    contract_defined: true",
        "    l4_active_now: false",
        "    executable_as_l4_gate_now: false",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['contract_check', 'l4_gate'], default='contract_check')
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    if args.mode == 'contract_check':
        findings = check_contract()
        status = 'PASS' if not findings else 'FAIL'
        rc = 0 if status == 'PASS' else 1
    else:
        findings = check_l4_gate_inputs()
        status = 'BLOCKED' if findings else 'PASS'
        rc = 2 if findings else 0
    write_report(Path(args.report), args.mode, status, findings)
    print(f'{VALIDATOR_ID}: {status}')
    return rc

if __name__ == '__main__':
    raise SystemExit(main())
