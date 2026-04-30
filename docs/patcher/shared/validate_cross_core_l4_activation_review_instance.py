#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import sys

REPO = Path.cwd()
REQUIRED_TOP_LEVEL_FIELDS = ['review_id', 'request_id', 'explicit_human_decision', 'decision_timestamp', 'requested_l4_scope', 'declared_read_surface', 'declared_write_surface', 'impacted_cores', 'required_validators', 'validator_execution_plan', 'release_and_promotion_plan', 'backlog_resolution_plan', 'rollback_or_reconciliation_path', 'non_goals_and_forbidden_mutations', 'activation_guardrails']
REQUIRED_VALIDATORS = ['validate_cross_core_l4_transition_review', 'validate_cross_core_write_surface', 'validate_constitution_referentiel_link_reconstruction', 'validate_link_binding_consistency', 'validate_multi_core_release_plan', 'validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution', 'validate_cross_core_rollback_or_reconciliation_path']
REQUEST_ID = 'CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01'

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def has_token(text: str, token: str) -> bool:
    return token in text

def validate_text(text: str, input_path: str) -> tuple[str, list[dict]]:
    findings = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if not has_token(text, field + ':'):
            findings.append({'finding_id': 'missing_required_field', 'severity': 'blocking', 'path': input_path, 'message': field})
    for validator_id in REQUIRED_VALIDATORS:
        if validator_id not in text:
            findings.append({'finding_id': 'missing_required_validator', 'severity': 'blocking', 'path': input_path, 'message': validator_id})
    if REQUEST_ID not in text:
        findings.append({'finding_id': 'missing_request_id', 'severity': 'blocking', 'path': input_path, 'message': REQUEST_ID})

    approval_present = 'decision: approve_l4_activation_review' in text
    rejection_present = 'decision: reject_l4_activation_review' in text
    maker_tbd = 'decision_maker: TBD' in text
    timestamp_tbd = 'decision_timestamp: TBD' in text
    materialized_false = 'l4_activation_review_materialized_now: false' in text
    activation_ready_false = 'l4_activation_ready_now: false' in text
    l4_active_false = 'l4_active_now: false' in text

    if approval_present:
        # This validator exists before activation. Approval instances must still be checked by future L4 gates.
        for marker in [
            'confirms_no_implicit_core_mutation: true',
            'confirms_no_implicit_backlog_closure: true',
            'confirms_no_implicit_release_or_promotion: true',
            'all_l4_gate_validations_required: true',
        ]:
            if marker not in text:
                findings.append({'finding_id': 'approval_missing_guardrail', 'severity': 'blocking', 'path': input_path, 'message': marker})
        status = 'PASS_SHAPE_ONLY' if not findings else 'FAIL'
    elif rejection_present or maker_tbd or timestamp_tbd or materialized_false or activation_ready_false or l4_active_false:
        findings.append({'finding_id': 'activation_review_not_approved', 'severity': 'blocking', 'path': input_path, 'message': 'template_or_rejected_review_cannot_activate_l4'})
        status = 'BLOCKED_NOT_APPROVED'
    else:
        findings.append({'finding_id': 'decision_missing_or_unknown', 'severity': 'blocking', 'path': input_path})
        status = 'FAIL'
    return status, findings

def write_report(report_path: Path, input_path: Path, status: str, findings: list[dict]) -> None:
    lines = [
        'cross_core_l4_activation_review_instance_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        f'  input: {str(input_path).replace(chr(92), chr(47))}',
        '  l4_activation_review_instance_validated: true',
        '  l4_activation_ready_now: false',
        '  l4_active_now: false',
        '  input_file:',
        f'    exists: {str(input_path.exists()).lower()}',
        f'    sha256: {sha(input_path) if input_path.exists() else None}',
        '  blocking_findings:',
    ]
    if findings:
        for item in findings:
            lines.append(f"    - finding_id: {item['finding_id']}")
            lines.append(f"      severity: {item['severity']}")
            lines.append(f"      path: {item['path']}")
            if 'message' in item:
                lines.append(f"      message: {item['message']}")
    else:
        lines.append('    []')
    lines.extend([
        '  result_summary:',
        f'    blocking_finding_count: {len(findings)}',
        '    l4_activation_ready_now: false',
        '    l4_active_now: false',
        '    core_mutation_authorized: false',
        '    backlog_closure_authorized: false',
        '    release_or_promotion_authorized: false',
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    input_path = Path(args.input)
    report_path = Path(args.report)
    if not input_path.exists():
        findings = [{'finding_id': 'missing_input_file', 'severity': 'blocking', 'path': str(input_path)}]
        write_report(report_path, input_path, 'FAIL', findings)
        print('FAIL')
        return 1
    text = input_path.read_text(encoding='utf-8')
    status, findings = validate_text(text, str(input_path))
    write_report(report_path, input_path, status, findings)
    print(status)
    if status == 'PASS_SHAPE_ONLY':
        return 0
    if status == 'BLOCKED_NOT_APPROVED':
        return 2
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
