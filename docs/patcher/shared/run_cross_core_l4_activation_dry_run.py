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
INSTANCE_VALIDATOR = REPO / 'docs/patcher/shared/validate_cross_core_l4_activation_review_instance.py'

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_report(report_path: Path, status: str, activation_review: Path, instance_report: Path, instance_rc: int, downstream_gates_executed: bool, reason: str) -> None:
    lines = [
        'cross_core_l4_activation_dry_run:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        f'  activation_review: {str(activation_review).replace(chr(92), chr(47))}',
        f'  activation_review_exists: {str(activation_review.exists()).lower()}',
        f'  activation_review_sha256: {sha(activation_review) if activation_review.exists() else None}',
        f'  instance_validation_report: {str(instance_report).replace(chr(92), chr(47))}',
        f'  instance_validator_return_code: {instance_rc}',
        f'  downstream_gates_executed: {str(downstream_gates_executed).lower()}',
        '  l4_activation_ready_now: false',
        '  l4_active_now: false',
        '  current_authorizations:',
        '    core_mutation_authorized: false',
        '    backlog_closure_authorized: false',
        '    release_or_promotion_authorized: false',
        '  reason: >-',
        f'    {reason}',
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--activation-review', default='docs/pipelines/cross_core_contract/templates/l4_activation_review.template.yaml')
    parser.add_argument('--instance-report', default='docs/registry/reports/l4_activation_dry_run_template_instance_validation.yaml')
    parser.add_argument('--report', default='docs/registry/reports/l4_activation_dry_run_template_report.yaml')
    parser.add_argument('--allow-downstream-gate-smoke', action='store_true')
    args = parser.parse_args()

    activation_review = REPO / args.activation_review
    instance_report = REPO / args.instance_report
    report_path = REPO / args.report

    if not INSTANCE_VALIDATOR.exists():
        write_report(report_path, 'FAIL', activation_review, instance_report, 1, False, 'Instance validator is missing.')
        print('FAIL')
        return 1
    if not activation_review.exists():
        write_report(report_path, 'FAIL', activation_review, instance_report, 1, False, 'Activation review input file is missing.')
        print('FAIL')
        return 1

    result = subprocess.run([sys.executable, str(INSTANCE_VALIDATOR), '--input', str(activation_review), '--report', str(instance_report)], cwd=REPO, text=True, capture_output=True, check=False)
    instance_text = instance_report.read_text(encoding='utf-8') if instance_report.exists() else ''

    if result.returncode == 2 and 'status: BLOCKED_NOT_APPROVED' in instance_text:
        write_report(report_path, 'BLOCKED_NOT_APPROVED', activation_review, instance_report, result.returncode, False, 'Activation review is not approved; downstream L4 gates were not executed.')
        print('BLOCKED_NOT_APPROVED')
        return 2

    if result.returncode == 0 and 'status: PASS_SHAPE_ONLY' in instance_text:
        if not args.allow_downstream_gate_smoke:
            write_report(report_path, 'BLOCKED_GATE_SMOKE_NOT_REQUESTED', activation_review, instance_report, result.returncode, False, 'Activation review shape passed, but downstream gate smoke was not explicitly requested.')
            print('BLOCKED_GATE_SMOKE_NOT_REQUESTED')
            return 2
        write_report(report_path, 'BLOCKED_DOWNSTREAM_GATE_SMOKE_NOT_IMPLEMENTED_IN_PHASE_53', activation_review, instance_report, result.returncode, False, 'Phase 53 dry-run does not execute downstream gates; it only proves non-approved template blocking.')
        print('BLOCKED_DOWNSTREAM_GATE_SMOKE_NOT_IMPLEMENTED_IN_PHASE_53')
        return 2

    write_report(report_path, 'FAIL', activation_review, instance_report, result.returncode, False, 'Activation review instance validation failed unexpectedly.')
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    print('FAIL')
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
