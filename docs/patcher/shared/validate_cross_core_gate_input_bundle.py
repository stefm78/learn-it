#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib

REQUIRED_FIELDS = [
    "bundle_id:",
    "source_execution_contract:",
    "gate_input_model:",
    "gate_inputs:",
    "write_surface:",
    "rollback_or_reconciliation_inputs:",
    "release_and_promotion_inputs:",
    "backlog_inputs:",
    "execution_guardrails:",
]

REQUIRED_GATES = [
    "validate_cross_core_l4_transition_review",
    "validate_cross_core_write_surface",
    "validate_cross_core_rollback_or_reconciliation_path",
    "validate_link_binding_consistency",
    "validate_constitution_referentiel_link_reconstruction",
    "validate_multi_core_release_plan",
    "validate_multi_core_promotion_manifest",
    "validate_cross_core_backlog_resolution",
]

FORBIDDEN_MARKERS = [
    "core_mutation_authorized: true",
    "backlog_closure_authorized: true",
    "release_or_promotion_authorized: true",
    "downstream_gates_executed: true",
    "apply_authorized: true",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_text(text: str, input_label: str) -> tuple[str, list[dict]]:
    findings = []
    for field in REQUIRED_FIELDS:
        if field not in text:
            findings.append({"finding_id": "missing_required_field", "severity": "blocking", "path": input_label, "message": field})
    for gate in REQUIRED_GATES:
        if gate not in text:
            findings.append({"finding_id": "missing_required_gate_input", "severity": "blocking", "path": input_label, "message": gate})
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            findings.append({"finding_id": "forbidden_marker", "severity": "blocking", "path": input_label, "message": marker})

    is_template = "template_status: inactive_template" in text or "template_only: true" in text
    concrete_bound = "concrete_contract_bound: true" in text
    if is_template:
        findings.append({"finding_id": "template_bundle_cannot_execute_gates", "severity": "blocking", "path": input_label})
        return "BLOCKED_TEMPLATE_ONLY", findings
    if not concrete_bound:
        findings.append({"finding_id": "bundle_not_bound_to_concrete_contract", "severity": "blocking", "path": input_label})
        return "BLOCKED_NOT_BOUND", findings
    if "gate_input_bundle_ready: true" in text and not findings:
        return "PASS_SHAPE_ONLY", findings
    findings.append({"finding_id": "gate_input_bundle_not_ready", "severity": "blocking", "path": input_label})
    return "BLOCKED_NOT_READY", findings

def write_report(report_path: Path, input_path: Path, status: str, findings: list[dict]) -> None:
    lines = [
        "cross_core_gate_input_bundle_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        f"  input: {str(input_path).replace(chr(92), chr(47))}",
        "  validator: validate_cross_core_gate_input_bundle",
        "  core_mutation_authorized: false",
        "  backlog_closure_authorized: false",
        "  release_or_promotion_authorized: false",
        "  input_file:",
        f"    exists: {str(input_path.exists()).lower()}",
        f"    sha256: {sha(input_path) if input_path.exists() else None}",
        "  blocking_findings:",
    ]
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
        "    gate_input_bundle_shape_checked: true",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    report_path = Path(args.report)

    if not input_path.exists():
        findings = [{"finding_id": "missing_input_file", "severity": "blocking", "path": str(input_path)}]
        write_report(report_path, input_path, "FAIL", findings)
        print("FAIL")
        return 1

    status, findings = validate_text(input_path.read_text(encoding="utf-8"), str(input_path))
    write_report(report_path, input_path, status, findings)
    print(status)
    if status == "PASS_SHAPE_ONLY":
        return 0
    if status in {"BLOCKED_TEMPLATE_ONLY", "BLOCKED_NOT_BOUND", "BLOCKED_NOT_READY"}:
        return 2
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
