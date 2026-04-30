#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()
FILES = [
    "docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.yaml",
    "docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.md",
    "docs/pipelines/cross_core_contract/validators/validate_cross_core_l4_transition_review.contract.yaml",
    "docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md",
    "docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml",
    "docs/pipelines/cross_core_contract/l4_transition_checklist.yaml",
    "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml",
    "docs/pipelines/cross_core_contract/pipeline.md",
    "docs/pipelines/cross_core_contract/state.yaml",
    "docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml",
]
REQUIRED = {
    "docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.yaml": [
        "validator_id: validate_cross_core_write_surface", "status: contract_defined_inactive",
        "l4_active_now: false", "executable_as_l4_gate_now: false",
        "declared_write_surface", "every_write_target_has_owner",
        "every_write_target_has_validation_gate", "rollback_or_reconciliation_path_missing",
        "core_mutation_authorized: false", "backlog_closure_authorized: false", "release_or_promotion_authorized: false",
    ],
    "docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.md": [
        "validate_cross_core_write_surface", "contract_defined: true", "l4_active_now: false", "executable_as_l4_gate_now: false",
    ],
    "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml": ["validate_cross_core_write_surface_contract:", "contract_defined: true", "executable_as_l4_gate_now: false"],
    "docs/pipelines/cross_core_contract/pipeline.md": ["validate_cross_core_write_surface contract", "executable_as_l4_gate_now: false"],
    "docs/pipelines/cross_core_contract/state.yaml": ["validate_cross_core_write_surface_contract_defined: true", "executable_as_l4_gate_now: false"],
    "docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml": ["status: proposed", "decision_status: pending_arbitration"],
}
FORBIDDEN = ["core_mutation_authorized: true", "backlog_closure_authorized: true", "release_or_promotion_authorized: true", "l4_active_now: true", "executable_as_l4_gate_now: true", "decision_status: approved"]
def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_write_surface_validator_contract_validation.yaml")
    findings = []
    checked = []
    for rp in FILES:
        p = REPO / rp
        exists = p.exists()
        checked.append({"path": rp, "exists": exists, "sha256": sha(p) if exists else None})
        if not exists:
            findings.append({"finding_id": "missing_required_file", "severity": "blocking", "path": rp})
            continue
        text = p.read_text(encoding="utf-8")
        for marker in REQUIRED.get(rp, []):
            if marker not in text:
                findings.append({"finding_id": "missing_required_marker", "severity": "blocking", "path": rp, "message": marker})
        for marker in FORBIDDEN:
            if marker in text:
                findings.append({"finding_id": "forbidden_marker", "severity": "blocking", "path": rp, "message": marker})
    status = "PASS" if not findings else "FAIL"
    lines = ["cross_core_write_surface_validator_contract_validation:", "  schema_version: '0.1'", f"  generated_at: '{iso_now()}'", f"  status: {status}", "  validator_id: validate_cross_core_write_surface", "  contract_defined: true", "  l4_active_now: false", "  executable_as_l4_gate_now: false", "  checked_files:"]
    for item in checked:
        lines.append(f"    - path: {item['path']}")
        lines.append(f"      exists: {str(item['exists']).lower()}")
        lines.append(f"      sha256: {item['sha256']}")
    lines.append("  blocking_findings:")
    if findings:
        for item in findings:
            lines.append(f"    - finding_id: {item['finding_id']}")
            lines.append(f"      severity: {item['severity']}")
            lines.append(f"      path: {item['path']}")
            if "message" in item: lines.append(f"      message: {item['message']}")
    else:
        lines.append("    []")
    lines += ["  result_summary:", f"    blocking_finding_count: {len(findings)}", "    write_surface_validator_contract_defined: true", "    l4_active_now: false", "    executable_as_l4_gate_now: false", "    core_mutation_authorized: false", "    backlog_closure_authorized: false", "    release_or_promotion_authorized: false", "    request_remains_proposed_pending_arbitration: true"]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Status: {status}")
    print(f"Wrote {report_path}")
    return 0 if status == "PASS" else 1
if __name__ == "__main__":
    raise SystemExit(main())
