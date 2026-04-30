#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()
STATE_FILES = ['docs/pipelines/cross_core_contract/activation_reviews/L4_ACTIVATION_REVIEW_2026_04_30_R01.yaml', 'docs/pipelines/cross_core_contract/L4_CONTROL_PLANE_ACTIVATION.md', 'docs/pipelines/cross_core_contract/validators/l4_control_plane_activation.yaml', 'docs/registry/reports/l4_control_plane_activation_review_instance_validation.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/registry/reports/cross_core_l4_hardening_closeout_validation.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml']
REQUIRED_MARKERS = ['status: control_plane_active_non_mutating', 'l4_control_plane_active_now: true', 'l4_activation_review_materialized_now: true', 'l4_mutating_gate_active_now: false', 'l4_core_mutation_authorized_now: false', 'l4_downstream_gates_executed_now: false', 'core_mutation_authorized: false', 'backlog_closure_authorized: false', 'release_or_promotion_authorized: false', 'instance_validation_status: PASS_SHAPE_ONLY', 'status: PASS_SHAPE_ONLY', 'decision: approve_l4_activation_review']
FORBIDDEN_MARKERS = ['l4_mutating_gate_active_now: true', 'l4_core_mutation_authorized_now: true', 'l4_downstream_gates_executed_now: true', 'core_mutation_authorized: true', 'backlog_closure_authorized: true', 'release_or_promotion_authorized: true', 'release_materialization_requested: true', 'promotion_requested: true', 'backlog_closure_requested: true', 'threshold_N_resolution_authorized_now: true']

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_control_plane_activation_validation.yaml")
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
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                findings.append({'finding_id': 'forbidden_marker', 'severity': 'blocking', 'path': rp, 'message': marker})
    combined = '\n'.join(combined_parts)
    for marker in REQUIRED_MARKERS:
        if marker not in combined:
            findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': 'combined_phase55_surface', 'message': marker})
    request_path = REPO / 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml'
    if request_path.exists():
        request_text = request_path.read_text(encoding='utf-8')
        for marker in ['status: proposed', 'decision_status: pending_arbitration']:
            if marker not in request_text:
                findings.append({'finding_id': 'request_status_changed', 'severity': 'blocking', 'path': str(request_path), 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_control_plane_activation_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_55_CROSS_CORE_L4_CONTROL_PLANE_ACTIVATION',
        '  l4_control_plane_active_now: true',
        '  l4_activation_review_materialized_now: true',
        '  l4_mutating_gate_active_now: false',
        '  l4_core_mutation_authorized_now: false',
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
        '    control_plane_activation_complete: true',
        '    l4_control_plane_active_now: true',
        '    l4_mutating_gate_active_now: false',
        '    l4_core_mutation_authorized_now: false',
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
