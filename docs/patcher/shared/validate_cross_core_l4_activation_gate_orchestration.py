#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import sys

REPO = Path.cwd()
STATE_FILES = ['docs/pipelines/cross_core_contract/L4_ACTIVATION_GATE_ORCHESTRATION.md', 'docs/pipelines/cross_core_contract/validators/l4_activation_gate_orchestration.yaml', 'docs/pipelines/cross_core_contract/L4_ACTIVATION_REVIEW_INSTANCE_VALIDATION.md', 'docs/pipelines/cross_core_contract/validators/l4_activation_review_instance_validation.yaml', 'docs/registry/reports/cross_core_l4_activation_review_instance_validator_validation.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml']
SCRIPT_FILES = ['docs/patcher/shared/validate_cross_core_l4_activation_review_instance.py', 'docs/patcher/shared/validate_cross_core_l4_transition_review.py', 'docs/patcher/shared/validate_cross_core_write_surface.py', 'docs/patcher/shared/validate_cross_core_rollback_or_reconciliation_path.py', 'docs/patcher/shared/validate_link_binding_consistency.py', 'docs/patcher/shared/validate_constitution_referentiel_link_reconstruction.py', 'docs/patcher/shared/validate_multi_core_release_plan.py', 'docs/patcher/shared/validate_multi_core_promotion_manifest.py', 'docs/patcher/shared/validate_cross_core_backlog_resolution.py']
GATE_IDS = ['activation_review_instance_validation', 'transition_review', 'write_surface', 'rollback_or_reconciliation_path', 'link_binding_consistency', 'constitution_referentiel_link_reconstruction', 'multi_core_release_plan', 'multi_core_promotion_manifest', 'cross_core_backlog_resolution']
VALIDATOR_IDS = ['validate_cross_core_l4_activation_review_instance', 'validate_cross_core_l4_transition_review', 'validate_cross_core_write_surface', 'validate_cross_core_rollback_or_reconciliation_path', 'validate_link_binding_consistency', 'validate_constitution_referentiel_link_reconstruction', 'validate_multi_core_release_plan', 'validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution']
REQUIRED_MARKERS = [
    'status: orchestration_defined_inactive',
    'l4_activation_gate_orchestration_defined: true',
    'l4_gate_orchestration_executable_now: false',
    'l4_activation_ready_now: false',
    'l4_active_now: false',
    'core_mutation_authorized: false',
    'backlog_closure_authorized: false',
    'release_or_promotion_authorized: false',
    'orchestration_model_complete: true',
]
FORBIDDEN_STATE_MARKERS = [
    'l4_active_now: true',
    'l4_activation_ready_now: true',
    'l4_gate_orchestration_executable_now: true',
    'core_mutation_authorized: true',
    'backlog_closure_authorized: true',
    'release_or_promotion_authorized: true',
    'decision_status: approved',
]

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml")
    findings = []
    checked = []
    combined_parts = []

    # State-like files: scan content for required and forbidden runtime-state markers.
    for rp in STATE_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({'path': rp, 'kind': 'state', 'exists': exists, 'sha256': sha(p) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_required_file', 'severity': 'blocking', 'path': rp})
            continue
        text = p.read_text(encoding='utf-8')
        combined_parts.append(text)
        for marker in FORBIDDEN_STATE_MARKERS:
            if marker in text:
                findings.append({'finding_id': 'forbidden_state_marker', 'severity': 'blocking', 'path': rp, 'message': marker})

    # Script files: compile only. Do NOT scan text markers because validators intentionally contain forbidden-marker strings.
    for rp in SCRIPT_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({'path': rp, 'kind': 'script_compile_only', 'exists': exists, 'sha256': sha(p) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_validator_script', 'severity': 'blocking', 'path': rp})
            continue
        result = subprocess.run([sys.executable, '-m', 'py_compile', str(p)], cwd=REPO, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            findings.append({'finding_id': 'validator_script_compile_failed', 'severity': 'blocking', 'path': rp, 'message': result.stderr.strip()})

    combined = '\n'.join(combined_parts)
    for marker in REQUIRED_MARKERS:
        if marker not in combined:
            findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': 'combined_phase52_state_surface', 'message': marker})
    for gate_id in GATE_IDS:
        if gate_id not in combined:
            findings.append({'finding_id': 'missing_gate_id', 'severity': 'blocking', 'path': 'combined_phase52_state_surface', 'message': gate_id})
    for validator_id in VALIDATOR_IDS:
        if validator_id not in combined:
            findings.append({'finding_id': 'missing_validator_id', 'severity': 'blocking', 'path': 'combined_phase52_state_surface', 'message': validator_id})
    request_path = REPO / 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml'
    if request_path.exists():
        request_text = request_path.read_text(encoding='utf-8')
        for marker in ['status: proposed', 'decision_status: pending_arbitration']:
            if marker not in request_text:
                findings.append({'finding_id': 'request_status_changed', 'severity': 'blocking', 'path': str(request_path), 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_activation_gate_orchestration_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_52_CROSS_CORE_L4_ACTIVATION_GATE_ORCHESTRATION',
        '  l4_activation_gate_orchestration_defined: true',
        '  l4_gate_orchestration_executable_now: false',
        '  l4_activation_ready_now: false',
        '  l4_active_now: false',
        '  checked_files:',
    ]
    for item in checked:
        lines.append(f"    - path: {item['path']}")
        lines.append(f"      kind: {item['kind']}")
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
        '    orchestration_model_complete: true',
        '    l4_gate_orchestration_executable_now: false',
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
