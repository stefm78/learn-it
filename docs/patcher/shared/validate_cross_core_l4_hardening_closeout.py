#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()
STATE_FILES = ['docs/pipelines/cross_core_contract/L4_HARDENING_CLOSEOUT.md', 'docs/pipelines/cross_core_contract/validators/l4_hardening_closeout.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml', 'docs/pipelines/cross_core_contract/L4_TARGET_CONTRACT.md', 'docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml', 'docs/registry/reports/cross_core_l4_transition_review_validator_contract_validation.yaml', 'docs/registry/reports/cross_core_write_surface_validator_contract_validation.yaml', 'docs/registry/reports/constitution_referentiel_link_reconstruction_validator_contract_validation.yaml', 'docs/registry/reports/link_binding_consistency_validator_contract_validation.yaml', 'docs/registry/reports/multi_core_release_plan_validator_contract_validation.yaml', 'docs/registry/reports/cross_core_remaining_l4_validator_contracts_validation.yaml', 'docs/registry/reports/cross_core_l4_readiness_matrix_validation.yaml', 'docs/registry/reports/cross_core_l4_executable_validators_batch1_validation.yaml', 'docs/registry/reports/cross_core_l4_executable_validators_batch2_validation.yaml', 'docs/registry/reports/cross_core_l4_executable_validator_readiness_validation.yaml', 'docs/registry/reports/cross_core_l4_activation_review_input_contract_validation.yaml', 'docs/registry/reports/cross_core_l4_activation_review_instance_validator_validation.yaml', 'docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml', 'docs/registry/reports/cross_core_l4_dry_run_activation_orchestrator_validation.yaml']
EVIDENCE_ITEMS = [{'phase': 'PHASE_38', 'label': 'cross_core_l4_target_contract', 'candidates': ['docs/pipelines/cross_core_contract/L4_TARGET_CONTRACT.md', 'docs/registry/reports/cross_core_l4_target_contract_validation.yaml'], 'required_markers': ['Phase: `PHASE_38_CROSS_CORE_L4_TARGET_CONTRACT`', 'l4_target_defined: true', 'l4_active_now: false', 'core_mutation_authorized: false', 'backlog_closure_authorized: false', 'release_or_promotion_authorized: false'], 'path': 'docs/pipelines/cross_core_contract/L4_TARGET_CONTRACT.md'}, {'phase': 'PHASE_39', 'label': 'cross_core_l4_validator_family_contract', 'candidates': ['docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml', 'docs/registry/reports/cross_core_l4_validator_family_contract_validation.yaml'], 'required_markers': ['status: PASS', 'validator_family_defined: true', 'l4_active_now: false', 'validators_executable_as_l4_gate_now: false'], 'path': 'docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml'}, {'phase': 'PHASE_40', 'label': 'cross_core_l4_transition_review_validator_contract', 'candidates': ['docs/registry/reports/cross_core_l4_transition_review_validator_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_transition_review_validator_contract_validation.yaml'}, {'phase': 'PHASE_41', 'label': 'cross_core_write_surface_validator_contract', 'candidates': ['docs/registry/reports/cross_core_write_surface_validator_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_write_surface_validator_contract_validation.yaml'}, {'phase': 'PHASE_42', 'label': 'cross_core_reconstruction_validator_contract', 'candidates': ['docs/registry/reports/constitution_referentiel_link_reconstruction_validator_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_active_now: false'], 'path': 'docs/registry/reports/constitution_referentiel_link_reconstruction_validator_contract_validation.yaml'}, {'phase': 'PHASE_43', 'label': 'cross_core_link_binding_validator_contract', 'candidates': ['docs/registry/reports/link_binding_consistency_validator_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_active_now: false'], 'path': 'docs/registry/reports/link_binding_consistency_validator_contract_validation.yaml'}, {'phase': 'PHASE_44', 'label': 'cross_core_multi_core_release_plan_validator_contract', 'candidates': ['docs/registry/reports/multi_core_release_plan_validator_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_active_now: false'], 'path': 'docs/registry/reports/multi_core_release_plan_validator_contract_validation.yaml'}, {'phase': 'PHASE_45', 'label': 'cross_core_remaining_l4_validator_contracts', 'candidates': ['docs/registry/reports/cross_core_remaining_l4_validator_contracts_validation.yaml'], 'required_markers': ['status: PASS', 'remaining_l4_validator_contracts_defined: true', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_remaining_l4_validator_contracts_validation.yaml'}, {'phase': 'PHASE_46', 'label': 'cross_core_l4_readiness_matrix', 'candidates': ['docs/registry/reports/cross_core_l4_readiness_matrix_validation.yaml'], 'required_markers': ['status: PASS', 'target_model_complete: true', 'l4_execution_ready_now: false'], 'path': 'docs/registry/reports/cross_core_l4_readiness_matrix_validation.yaml'}, {'phase': 'PHASE_47', 'label': 'cross_core_l4_executable_validators_batch1', 'candidates': ['docs/registry/reports/cross_core_l4_executable_validators_batch1_validation.yaml'], 'required_markers': ['status: PASS', 'executable_validators_batch1_defined: true', 'l4_execution_ready_now: false'], 'path': 'docs/registry/reports/cross_core_l4_executable_validators_batch1_validation.yaml'}, {'phase': 'PHASE_48', 'label': 'cross_core_l4_executable_validators_batch2', 'candidates': ['docs/registry/reports/cross_core_l4_executable_validators_batch2_validation.yaml'], 'required_markers': ['status: PASS', 'executable_validators_batch2_defined: true', 'l4_execution_ready_now: false'], 'path': 'docs/registry/reports/cross_core_l4_executable_validators_batch2_validation.yaml'}, {'phase': 'PHASE_49', 'label': 'cross_core_l4_executable_validator_readiness', 'candidates': ['docs/registry/reports/cross_core_l4_executable_validator_readiness_validation.yaml'], 'required_markers': ['status: PASS', 'all_l4_executable_validators_defined: true', 'all_l4_gate_smokes_BLOCKED: true', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_executable_validator_readiness_validation.yaml'}, {'phase': 'PHASE_50', 'label': 'cross_core_l4_activation_review_input_contract', 'candidates': ['docs/registry/reports/cross_core_l4_activation_review_input_contract_validation.yaml'], 'required_markers': ['status: PASS', 'l4_activation_input_contract_defined: true', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_activation_review_input_contract_validation.yaml'}, {'phase': 'PHASE_51', 'label': 'cross_core_l4_activation_review_instance_validator', 'candidates': ['docs/registry/reports/cross_core_l4_activation_review_instance_validator_validation.yaml'], 'required_markers': ['status: PASS', 'activation_review_instance_validator_defined: true', 'template_instance_validation_status: BLOCKED_NOT_APPROVED', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_activation_review_instance_validator_validation.yaml'}, {'phase': 'PHASE_52', 'label': 'cross_core_l4_activation_gate_orchestration', 'candidates': ['docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml'], 'required_markers': ['status: PASS', 'orchestration_model_complete: true', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml'}, {'phase': 'PHASE_53', 'label': 'cross_core_l4_dry_run_activation_orchestrator', 'candidates': ['docs/registry/reports/cross_core_l4_dry_run_activation_orchestrator_validation.yaml'], 'required_markers': ['status: PASS', 'dry_run_orchestrator_ready: true', 'template_blocks_activation: true', 'downstream_gates_executed_on_template: false', 'l4_active_now: false'], 'path': 'docs/registry/reports/cross_core_l4_dry_run_activation_orchestrator_validation.yaml'}]
REQUIRED_MARKERS = ['status: closed_out_inactive', 'l4_hardening_closeout_complete: true', 'l4_activation_ready_now: false', 'l4_active_now: false', 'core_mutation_authorized: false', 'backlog_closure_authorized: false', 'release_or_promotion_authorized: false', 'default: stop_at_NO_ACTIVE_PHASE', 'request_status_required_now: proposed', 'decision_status_required_now: pending_arbitration']
FORBIDDEN_STATE_MARKERS = ['l4_active_now: true', 'l4_activation_ready_now: true', 'l4_execution_ready_now: true', 'core_mutation_authorized: true', 'backlog_closure_authorized: true', 'release_or_promotion_authorized: true', 'decision_status: approved']

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_hardening_closeout_validation.yaml")
    findings = []
    checked = []
    combined_parts = []
    for rp in STATE_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({'path': rp, 'exists': exists, 'sha256': sha(p) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_required_file', 'severity': 'blocking', 'path': rp})
            continue
        text = p.read_text(encoding='utf-8')
        combined_parts.append(text)
        for marker in FORBIDDEN_STATE_MARKERS:
            if marker in text:
                findings.append({'finding_id': 'forbidden_state_marker', 'severity': 'blocking', 'path': rp, 'message': marker})
    combined = '\n'.join(combined_parts)
    for marker in REQUIRED_MARKERS:
        if marker not in combined:
            findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': 'combined_phase54_surface', 'message': marker})
    for item in EVIDENCE_ITEMS:
        p = REPO / item['path']
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        for marker in item['required_markers']:
            if marker not in text:
                findings.append({'finding_id': 'evidence_missing_marker', 'severity': 'blocking', 'path': item['path'], 'message': marker})
    request_path = REPO / 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml'
    if request_path.exists():
        request_text = request_path.read_text(encoding='utf-8')
        for marker in ['status: proposed', 'decision_status: pending_arbitration']:
            if marker not in request_text:
                findings.append({'finding_id': 'request_status_changed', 'severity': 'blocking', 'path': str(request_path), 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_hardening_closeout_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_54_CROSS_CORE_L4_HARDENING_CLOSEOUT',
        '  l4_hardening_closeout_complete: true',
        '  l4_activation_ready_now: false',
        '  l4_active_now: false',
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
        '    closeout_evidence_item_count: ' + str(len(EVIDENCE_ITEMS)),
        '    l4_hardening_closeout_complete: true',
        '    recommended_next_action: stop_at_NO_ACTIVE_PHASE',
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
