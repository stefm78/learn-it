#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import sys

REPO = Path.cwd()
STATE_FILES = ['docs/pipelines/cross_core_contract/GENERIC_EXECUTION_CONTRACT_INSTANTIATOR.md', 'docs/pipelines/cross_core_contract/validators/generic_execution_contract_instantiator.yaml', 'docs/pipelines/cross_core_contract/templates/cross_core_change_request.fixture.yaml', 'docs/pipelines/cross_core_contract/work/03_contract_synthesis/GENERIC_FIXTURE_EXECUTION_CONTRACT_R00.yaml', 'docs/registry/reports/generic_execution_contract_instantiation_smoke.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/registry/reports/cross_core_generic_mutating_execution_framework_validation.yaml']
SCRIPT_FILES = ['docs/patcher/shared/materialize_cross_core_execution_contract.py', 'docs/patcher/shared/validate_cross_core_execution_contract.py']
REQUIRED_MARKERS = ['generic_execution_contract_instantiator_defined: true', 'instantiation_smoke_status: BLOCKED_NOT_AUTHORIZED', 'instantiated_contract_created: true', 'concrete_request_bound: true', 'request_specific_logic_encoded: false', 'status: BLOCKED_NOT_AUTHORIZED', 'core_mutation_authorized: false', 'backlog_closure_authorized: false', 'release_or_promotion_authorized: false', 'l4_mutating_gate_active_now: false', 'l4_core_mutation_authorized_now: false']
FORBIDDEN_MARKERS = ['core_mutation_authorized: true', 'backlog_closure_authorized: true', 'release_or_promotion_authorized: true', 'l4_mutating_gate_active_now: true', 'l4_core_mutation_authorized_now: true', 'release_materialization_requested: true', 'promotion_requested: true', 'backlog_closure_requested: true']

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_execution_contract_instantiator_validation.yaml")
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
        for marker in FORBIDDEN_MARKERS:
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
            findings.append({'finding_id': 'missing_required_marker', 'severity': 'blocking', 'path': 'combined_phase57_surface', 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_execution_contract_instantiator_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_57_CROSS_CORE_GENERIC_EXECUTION_CONTRACT_INSTANTIATOR',
        '  generic_execution_contract_instantiator_defined: true',
        '  instantiation_smoke_status: BLOCKED_NOT_AUTHORIZED',
        '  instantiated_contract_created: true',
        '  concrete_request_bound: true',
        '  request_specific_logic_encoded: false',
        '  l4_mutating_gate_active_now: false',
        '  l4_core_mutation_authorized_now: false',
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
        '    generic_execution_contract_instantiator_defined: true',
        '    instantiated_contract_created: true',
        '    template_or_fixture_blocks_mutation: true',
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
