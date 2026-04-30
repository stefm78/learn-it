#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()

REQUIRED_FILES = [
    'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml',
    'docs/pipelines/cross_core_contract/entry_actions/OPEN_REQUEST.action.yaml',
    'docs/pipelines/cross_core_contract/entry_actions/MATERIALIZE_REQUEST.action.yaml',
    'docs/pipelines/cross_core_contract/entry_actions/CONTINUE_REQUEST.action.yaml',
    'docs/pipelines/cross_core_contract/entry_actions/RECONCILE_REQUEST.action.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_00_INTAKE_AND_SHAPE_VALIDATION.skill.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_01_SOURCE_EVIDENCE_REVIEW.skill.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_02_CROSS_CORE_ARBITRAGE.skill.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_03_CONTRACT_SYNTHESIS.skill.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_04_VALIDATION.skill.yaml',
    'docs/pipelines/cross_core_contract/stages/STAGE_05_RELEASE_AND_PROMOTION_PLANNING.skill.yaml',
    'docs/pipelines/cross_core_contract/pipeline.md',
    'docs/pipelines/cross_core_contract/state.yaml',
]

REQUIRED_MARKERS = {
    'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml': [
        'hardening_level: L3_managed_execution_pipeline',
        'l4_status: future_explicit_phase_required_before_any_core_write',
        'core_mutation_authorized: false',
        'backlog_closure_authorized: false',
    ],
    'docs/pipelines/cross_core_contract/pipeline.md': [
        'hardening_level: L3_managed_execution_pipeline',
        'L4 before any Core write',
        'AI_PROTOCOL.yaml',
    ],
    'docs/pipelines/cross_core_contract/state.yaml': [
        'hardening_level: L3_managed_execution_pipeline',
        'status: idle',
        'current_run_id: null',
    ],
}

FORBIDDEN_MARKERS = [
    'core_mutation_authorized: true',
    'backlog_closure_authorized: true',
    'release_or_promotion_authorized: true',
    'l4_status: active',
    'status: approved',
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace('\\\\', '/')

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('docs/registry/reports/cross_core_contract_hardening_validation.yaml')
    findings = []
    checked = []
    for rel_path in REQUIRED_FILES:
        path = REPO / rel_path
        exists = path.exists()
        checked.append({'path': rel_path, 'exists': exists, 'sha256': sha256_file(path) if exists else None})
        if not exists:
            findings.append({'finding_id': 'missing_required_file', 'severity': 'blocking', 'path': rel_path})
            continue
        text = path.read_text(encoding='utf-8')
        for marker in REQUIRED_MARKERS.get(rel_path, []):
            if marker not in text:
                findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': rel_path, 'message': marker})
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                findings.append({'finding_id': 'forbidden_marker', 'severity': 'blocking', 'path': rel_path, 'message': marker})
    for rel_path in REQUIRED_FILES:
        if '/stages/' in rel_path:
            text = (REPO / rel_path).read_text(encoding='utf-8') if (REPO / rel_path).exists() else ''
            for marker in ['no_core_write', 'no_backlog_closure', 'future_l4_phase_required_before_core_write: true']:
                if marker not in text:
                    findings.append({'finding_id': 'stage_missing_guardrail', 'severity': 'blocking', 'path': rel_path, 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_contract_hardening_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  hardening_level: L3_managed_execution_pipeline',
        '  l4_status: future_explicit_phase_required_before_any_core_write',
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
        '    l3_managed_pipeline: true',
        '    l4_core_write_enabled: false',
        '    core_mutation_authorized: false',
        '    backlog_closure_authorized: false',
        '    release_or_promotion_authorized: false',
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(f'Status: {status}')
    print(f'Wrote {report_path}')
    return 0 if status == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
