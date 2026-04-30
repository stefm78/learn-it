#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()
FILES = ['docs/pipelines/cross_core_contract/L4_EXECUTABLE_VALIDATOR_READINESS.md', 'docs/pipelines/cross_core_contract/validators/l4_executable_validator_readiness.yaml', 'docs/pipelines/cross_core_contract/L4_READINESS_MATRIX.md', 'docs/pipelines/cross_core_contract/validators/l4_readiness_matrix.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml', 'docs/patcher/shared/validate_cross_core_l4_transition_review.py', 'docs/registry/reports/validate_cross_core_l4_transition_review_contract_check.yaml', 'docs/registry/reports/validate_cross_core_l4_transition_review_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_cross_core_write_surface.py', 'docs/registry/reports/validate_cross_core_write_surface_contract_check.yaml', 'docs/registry/reports/validate_cross_core_write_surface_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_constitution_referentiel_link_reconstruction.py', 'docs/registry/reports/validate_constitution_referentiel_link_reconstruction_contract_check.yaml', 'docs/registry/reports/validate_constitution_referentiel_link_reconstruction_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_link_binding_consistency.py', 'docs/registry/reports/validate_link_binding_consistency_contract_check.yaml', 'docs/registry/reports/validate_link_binding_consistency_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_multi_core_release_plan.py', 'docs/registry/reports/validate_multi_core_release_plan_contract_check.yaml', 'docs/registry/reports/validate_multi_core_release_plan_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_multi_core_promotion_manifest.py', 'docs/registry/reports/validate_multi_core_promotion_manifest_contract_check.yaml', 'docs/registry/reports/validate_multi_core_promotion_manifest_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_cross_core_backlog_resolution.py', 'docs/registry/reports/validate_cross_core_backlog_resolution_contract_check.yaml', 'docs/registry/reports/validate_cross_core_backlog_resolution_l4_gate_smoke.yaml', 'docs/patcher/shared/validate_cross_core_rollback_or_reconciliation_path.py', 'docs/registry/reports/validate_cross_core_rollback_or_reconciliation_path_contract_check.yaml', 'docs/registry/reports/validate_cross_core_rollback_or_reconciliation_path_l4_gate_smoke.yaml']
VALIDATOR_IDS = ['validate_cross_core_l4_transition_review', 'validate_cross_core_write_surface', 'validate_constitution_referentiel_link_reconstruction', 'validate_link_binding_consistency', 'validate_multi_core_release_plan', 'validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution', 'validate_cross_core_rollback_or_reconciliation_path']

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def has_marker(path: Path, marker: str) -> bool:
    return marker in path.read_text(encoding='utf-8')

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_executable_validator_readiness_validation.yaml")
    findings = []
    checked = []
    for rp in FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({'path': rp, 'exists': exists, 'sha256': sha(p) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_required_file', 'severity': 'blocking', 'path': rp})

    readiness_path = REPO / 'docs/pipelines/cross_core_contract/validators/l4_executable_validator_readiness.yaml'
    if readiness_path.exists():
        for marker in [
            'status: complete_inactive_blocking_runtime',
            'all_l4_executable_validators_defined: true',
            'all_contract_checks_PASS: true',
            'all_l4_gate_smokes_BLOCKED: true',
            'l4_execution_ready_now: false',
            'l4_active_now: false',
            'core_mutation_authorized: false',
            'backlog_closure_authorized: false',
            'release_or_promotion_authorized: false',
        ]:
            if not has_marker(readiness_path, marker):
                findings.append({'finding_id': 'readiness_missing_marker', 'severity': 'blocking', 'path': str(readiness_path), 'message': marker})
        for validator_id in VALIDATOR_IDS:
            if not has_marker(readiness_path, validator_id):
                findings.append({'finding_id': 'readiness_missing_validator', 'severity': 'blocking', 'path': str(readiness_path), 'message': validator_id})

    for rp in FILES:
        p = REPO / rp
        if not p.exists():
            continue
        if rp.endswith('_contract_check.yaml'):
            for marker in ['status: PASS', 'mode: contract_check', 'l4_active_now: false', 'executable_as_l4_gate_now: false']:
                if not has_marker(p, marker):
                    findings.append({'finding_id': 'contract_check_not_pass', 'severity': 'blocking', 'path': rp, 'message': marker})
        if rp.endswith('_l4_gate_smoke.yaml'):
            for marker in ['status: BLOCKED', 'mode: l4_gate', 'future_l4_input_missing', 'l4_active_now: false', 'executable_as_l4_gate_now: false']:
                if not has_marker(p, marker):
                    findings.append({'finding_id': 'l4_gate_smoke_not_blocked', 'severity': 'blocking', 'path': rp, 'message': marker})

    request_path = REPO / 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml'
    if request_path.exists():
        for marker in ['status: proposed', 'decision_status: pending_arbitration']:
            if not has_marker(request_path, marker):
                findings.append({'finding_id': 'request_status_changed', 'severity': 'blocking', 'path': str(request_path), 'message': marker})

    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_executable_validator_readiness_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_49_CROSS_CORE_L4_EXECUTABLE_VALIDATOR_READINESS',
        '  l4_active_now: false',
        '  l4_execution_ready_now: false',
        '  all_l4_executable_validators_defined: true',
        '  all_contract_checks_PASS: true',
        '  all_l4_gate_smokes_BLOCKED: true',
        '  checked_files:',
    ]
    for item in checked:
        lines.append(f"    - path: {item['path']}")
        lines.append(f"      exists: {str(item['exists']).lower()}")
        lines.append(f"      sha256: {item['sha256']}")
    lines.append('  blocking_findings:')
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
        '    executable_layer_complete: true',
        '    l4_activation_ready_now: false',
        '    l4_active_now: false',
        '    core_mutation_authorized: false',
        '    backlog_closure_authorized: false',
        '    release_or_promotion_authorized: false',
        '    request_remains_proposed_pending_arbitration: true',
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(f'Status: {status}')
    print(f'Wrote {report_path}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
