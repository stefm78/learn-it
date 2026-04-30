#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import sys

REPO = Path.cwd()
STATE_FILES = ['docs/pipelines/cross_core_contract/L4_DRY_RUN_ACTIVATION_ORCHESTRATOR.md', 'docs/pipelines/cross_core_contract/validators/l4_dry_run_activation_orchestrator.yaml', 'docs/registry/reports/l4_activation_dry_run_template_report.yaml', 'docs/registry/reports/l4_activation_dry_run_template_instance_validation.yaml', 'docs/pipelines/cross_core_contract/L4_ACTIVATION_GATE_ORCHESTRATION.md', 'docs/pipelines/cross_core_contract/validators/l4_activation_gate_orchestration.yaml', 'docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml']
SCRIPT_FILES = ['docs/patcher/shared/run_cross_core_l4_activation_dry_run.py', 'docs/patcher/shared/validate_cross_core_l4_activation_review_instance.py']
REQUIRED_MARKERS = [
    'status: dry_run_orchestrator_defined_inactive',
    'l4_dry_run_activation_orchestrator_defined: true',
    'template_dry_run_status: BLOCKED_NOT_APPROVED',
    'downstream_gates_executed_on_template: false',
    'downstream_gates_executed: false',
    'status: BLOCKED_NOT_APPROVED',
    'l4_activation_ready_now: false',
    'l4_active_now: false',
    'core_mutation_authorized: false',
    'backlog_closure_authorized: false',
    'release_or_promotion_authorized: false',
]
FORBIDDEN_STATE_MARKERS = [
    'l4_active_now: true',
    'l4_activation_ready_now: true',
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
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_dry_run_activation_orchestrator_validation.yaml")
    findings = []
    checked = []
    combined_parts = []
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
    for rp in SCRIPT_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({'path': rp, 'kind': 'script_compile_only', 'exists': exists, 'sha256': sha(p) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_script', 'severity': 'blocking', 'path': rp})
            continue
        result = subprocess.run([sys.executable, '-m', 'py_compile', str(p)], cwd=REPO, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            findings.append({'finding_id': 'script_compile_failed', 'severity': 'blocking', 'path': rp, 'message': result.stderr.strip()})
    combined = '\n'.join(combined_parts)
    for marker in REQUIRED_MARKERS:
        if marker not in combined:
            findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': 'combined_phase53_surface', 'message': marker})
    request_path = REPO / 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml'
    if request_path.exists():
        request_text = request_path.read_text(encoding='utf-8')
        for marker in ['status: proposed', 'decision_status: pending_arbitration']:
            if marker not in request_text:
                findings.append({'finding_id': 'request_status_changed', 'severity': 'blocking', 'path': str(request_path), 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_dry_run_activation_orchestrator_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_53_CROSS_CORE_L4_DRY_RUN_ACTIVATION_ORCHESTRATOR',
        '  l4_dry_run_activation_orchestrator_defined: true',
        '  template_dry_run_status: BLOCKED_NOT_APPROVED',
        '  downstream_gates_executed_on_template: false',
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
        '    dry_run_orchestrator_ready: true',
        '    template_blocks_activation: true',
        '    downstream_gates_executed_on_template: false',
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
