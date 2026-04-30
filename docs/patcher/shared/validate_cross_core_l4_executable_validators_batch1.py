#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import sys

REPO = Path.cwd()
VALIDATOR_SPECS = {'validate_cross_core_l4_transition_review': {'script': 'docs/patcher/shared/validate_cross_core_l4_transition_review.py', 'contract_check_report': 'docs/registry/reports/validate_cross_core_l4_transition_review_contract_check.yaml'}, 'validate_cross_core_write_surface': {'script': 'docs/patcher/shared/validate_cross_core_write_surface.py', 'contract_check_report': 'docs/registry/reports/validate_cross_core_write_surface_contract_check.yaml'}, 'validate_constitution_referentiel_link_reconstruction': {'script': 'docs/patcher/shared/validate_constitution_referentiel_link_reconstruction.py', 'contract_check_report': 'docs/registry/reports/validate_constitution_referentiel_link_reconstruction_contract_check.yaml'}, 'validate_link_binding_consistency': {'script': 'docs/patcher/shared/validate_link_binding_consistency.py', 'contract_check_report': 'docs/registry/reports/validate_link_binding_consistency_contract_check.yaml'}}

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_l4_executable_validators_batch1_validation.yaml")
    findings = []
    checked = []
    for validator_id, spec in VALIDATOR_SPECS.items():
        script = REPO / spec['script']
        checked.append({'path': spec['script'], 'exists': script.exists(), 'sha256': sha(script) if script.exists() else None})
        if not script.exists():
            findings.append({'finding_id': 'missing_validator_script', 'severity': 'blocking', 'path': spec['script']})
            continue
        compile_result = subprocess.run([sys.executable, '-m', 'py_compile', str(script)], cwd=REPO, text=True, capture_output=True, check=False)
        if compile_result.returncode != 0:
            findings.append({'finding_id': 'validator_py_compile_failed', 'severity': 'blocking', 'path': spec['script'], 'message': compile_result.stderr.strip()})
            continue
        run_result = subprocess.run([sys.executable, str(script), '--mode', 'contract_check', '--report', spec['contract_check_report']], cwd=REPO, text=True, capture_output=True, check=False)
        if run_result.returncode != 0:
            findings.append({'finding_id': 'validator_contract_check_failed', 'severity': 'blocking', 'path': spec['script'], 'message': run_result.stdout.strip() + run_result.stderr.strip()})
        report = REPO / spec['contract_check_report']
        checked.append({'path': spec['contract_check_report'], 'exists': report.exists(), 'sha256': sha(report) if report.exists() else None})
        if not report.exists():
            findings.append({'finding_id': 'missing_contract_check_report', 'severity': 'blocking', 'path': spec['contract_check_report']})
        else:
            text = report.read_text(encoding='utf-8')
            for marker in ['status: PASS', 'mode: contract_check', 'l4_active_now: false', 'executable_as_l4_gate_now: false']:
                if marker not in text:
                    findings.append({'finding_id': 'contract_check_report_missing_marker', 'severity': 'blocking', 'path': spec['contract_check_report'], 'message': marker})
    status = 'PASS' if not findings else 'FAIL'
    lines = [
        'cross_core_l4_executable_validators_batch1_validation:',
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f'  status: {status}',
        '  phase: PHASE_47_CROSS_CORE_L4_EXECUTABLE_VALIDATORS_BATCH1',
        '  l4_active_now: false',
        '  executable_as_l4_gate_now: false',
        '  batch1_executable_validator_count: 4',
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
        '    executable_validators_batch1_defined: true',
        '    l4_active_now: false',
        '    executable_as_l4_gate_now: false',
        '    l4_execution_ready_now: false',
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
