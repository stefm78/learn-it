#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import sys

REPO = Path.cwd()

EVIDENCE_FILES = [
    "docs/registry/reports/cross_core_l4_control_plane_activation_validation.yaml",
    "docs/registry/reports/cross_core_generic_mutating_execution_framework_validation.yaml",
    "docs/registry/reports/cross_core_execution_contract_instantiator_validation.yaml",
    "docs/registry/reports/cross_core_generic_gate_execution_runner_validation.yaml",
    "docs/registry/reports/cross_core_generic_authorized_dry_run_gate_smoke_validation.yaml",
    "docs/registry/reports/cross_core_generic_downstream_gate_input_bundle_contract_validation.yaml",
    "docs/registry/reports/cross_core_generic_dry_run_gate_input_bundle_fixture_validation.yaml",
    "docs/registry/reports/cross_core_generic_downstream_gate_dry_run_smoke_validation.yaml",
    "docs/pipelines/cross_core_contract/GENERIC_MUTATING_READINESS_LOCK.md",
    "docs/pipelines/cross_core_contract/validators/generic_mutating_readiness_lock.yaml",
    "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml",
    "docs/pipelines/cross_core_contract/pipeline.md",
    "docs/pipelines/cross_core_contract/state.yaml",
    "docs/pipelines/cross_core_contract/l4_transition_checklist.yaml",
]

SCRIPT_FILES = [
    "docs/patcher/shared/validate_cross_core_generic_mutating_readiness_lock.py",
]

REQUIRED_MARKERS = [
    "generic_mutating_readiness_lock_defined: true",
    "generic_pipeline_ready_for_future_concrete_request: true",
    "real_mutation_authorized_now: false",
    "requires_future_explicit_human_decision: true",
    "requires_concrete_cross_core_change_request: true",
    "requires_all_downstream_gates_PASS_for_real_request: true",
    "l4_control_plane_active_now: true",
    "l4_mutating_execution_framework_ready: true",
    "dry_run_gate_smoke_executed: true",
    "downstream_mutating_gates_executed: false",
    "core_mutation_authorized: false",
    "backlog_closure_authorized: false",
    "release_or_promotion_authorized: false",
    "status: PASS",
    "status: PASS_DRY_RUN_ONLY",
]

FORBIDDEN_MARKERS = [
    "real_mutation_authorized_now: true",
    "core_mutation_authorized: true",
    "backlog_closure_authorized: true",
    "release_or_promotion_authorized: true",
    "l4_core_mutation_authorized_now: true",
    "downstream_mutating_gates_executed: true",
    "apply_authorized: true",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_generic_mutating_readiness_lock_validation.yaml")
    findings = []
    checked = []
    combined_parts = []

    for rp in EVIDENCE_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({"path": rp, "kind": "evidence", "exists": exists, "sha256": sha(p) if exists else None})
        if not exists:
            findings.append({"finding_id": "missing_evidence_file", "severity": "blocking", "path": rp})
            continue
        text = p.read_text(encoding="utf-8")
        combined_parts.append(text)
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                findings.append({"finding_id": "forbidden_marker", "severity": "blocking", "path": rp, "message": marker})

    for rp in SCRIPT_FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({"path": rp, "kind": "script_compile_only", "exists": exists, "sha256": sha(p) if exists else None})
        if not exists:
            findings.append({"finding_id": "missing_script", "severity": "blocking", "path": rp})
            continue
        result = subprocess.run([sys.executable, "-m", "py_compile", str(p)], cwd=REPO, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            findings.append({"finding_id": "script_compile_failed", "severity": "blocking", "path": rp, "message": result.stderr.strip()})

    combined = "\n".join(combined_parts)
    for marker in REQUIRED_MARKERS:
        if marker not in combined:
            findings.append({"finding_id": "missing_required_marker", "severity": "blocking", "path": "combined_phase63_surface", "message": marker})

    status = "PASS" if not findings else "FAIL"
    lines = [
        "cross_core_generic_mutating_readiness_lock_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        "  phase: PHASE_63_CROSS_CORE_GENERIC_MUTATING_READINESS_LOCK",
        "  generic_mutating_readiness_lock_defined: true",
        "  generic_pipeline_ready_for_future_concrete_request: true",
        "  real_mutation_authorized_now: false",
        "  requires_future_explicit_human_decision: true",
        "  requires_concrete_cross_core_change_request: true",
        "  requires_all_downstream_gates_PASS_for_real_request: true",
        "  checked_files:",
    ]
    for item in checked:
        lines.append(f"    - path: {item['path']}")
        lines.append(f"      kind: {item['kind']}")
        lines.append(f"      exists: {str(item['exists']).lower()}")
        lines.append(f"      sha256: {item['sha256']}")
    lines.append("  blocking_findings:")
    if findings:
        for item in findings:
            lines.append(f"    - finding_id: {item['finding_id']}")
            lines.append(f"      severity: {item['severity']}")
            lines.append(f"      path: {item['path']}")
            if "message" in item:
                lines.append(f"      message: {item['message']}")
    else:
        lines.append("    []")
    lines.extend([
        "  result_summary:",
        f"    blocking_finding_count: {len(findings)}",
        "    generic_cross_core_execution_pipeline_complete: true",
        "    generic_pipeline_ready_for_future_concrete_request: true",
        "    real_mutation_authorized_now: false",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
        "    recommended_next_action: stop_at_NO_ACTIVE_PHASE_until_specific_request_is_selected",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Status: {status}")
    print(f"Wrote {report_path}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
