#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib

REQUIRED_VALIDATORS = ['validate_cross_core_execution_contract', 'validate_cross_core_l4_transition_review', 'validate_cross_core_write_surface', 'validate_cross_core_rollback_or_reconciliation_path', 'validate_link_binding_consistency', 'validate_constitution_referentiel_link_reconstruction', 'validate_multi_core_release_plan', 'validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution']
REQUIRED_TOP_LEVEL_FIELDS = [
    "contract_id",
    "source_request",
    "execution_model",
    "affected_cores",
    "declared_read_surface",
    "declared_write_surface",
    "write_authorization",
    "validation_plan",
    "rollback_or_reconciliation_path",
    "release_and_promotion_policy",
    "backlog_policy",
    "execution_guardrails",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_text(text: str, input_label: str) -> tuple[str, list[dict]]:
    findings = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field + ":" not in text:
            findings.append({"finding_id": "missing_required_field", "severity": "blocking", "path": input_label, "message": field})
    for validator in REQUIRED_VALIDATORS:
        if validator not in text:
            findings.append({"finding_id": "missing_required_validator", "severity": "blocking", "path": input_label, "message": validator})

    is_template = "template_status: inactive_template" in text or "template_only: true" in text
    if is_template:
        if "core_mutation_authorized: false" not in text:
            findings.append({"finding_id": "template_missing_core_mutation_false", "severity": "blocking", "path": input_label})
        findings.append({"finding_id": "template_contract_cannot_authorize_mutation", "severity": "blocking", "path": input_label})
        hard_missing = [f for f in findings if f["finding_id"].startswith("missing")]
        return ("FAIL" if hard_missing else "BLOCKED_TEMPLATE_ONLY"), findings

    if "concrete_request_bound: true" not in text:
        findings.append({"finding_id": "concrete_request_not_bound", "severity": "blocking", "path": input_label})
    if "granted_now: true" not in text:
        findings.append({"finding_id": "write_not_granted", "severity": "blocking", "path": input_label})
    return ("PASS_SHAPE_ONLY" if not findings else "BLOCKED_NOT_AUTHORIZED"), findings

def write_report(report_path: Path, input_path: Path, status: str, findings: list[dict]) -> None:
    lines = [
        "cross_core_execution_contract_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        f"  input: {str(input_path).replace(chr(92), chr(47))}",
        "  generic_contract_validator: validate_cross_core_execution_contract",
        "  template_validation_expected_to_block: true",
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
        "    generic_contract_shape_checked: true",
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
    if status in {"BLOCKED_TEMPLATE_ONLY", "BLOCKED_NOT_AUTHORIZED"}:
        return 2
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
