#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()
FILES = ['docs/pipelines/cross_core_contract/validators/validate_multi_core_promotion_manifest.contract.yaml', 'docs/pipelines/cross_core_contract/validators/validate_multi_core_promotion_manifest.contract.md', 'docs/pipelines/cross_core_contract/validators/validate_cross_core_backlog_resolution.contract.yaml', 'docs/pipelines/cross_core_contract/validators/validate_cross_core_backlog_resolution.contract.md', 'docs/pipelines/cross_core_contract/validators/validate_cross_core_rollback_or_reconciliation_path.contract.yaml', 'docs/pipelines/cross_core_contract/validators/validate_cross_core_rollback_or_reconciliation_path.contract.md', 'docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md', 'docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml', 'docs/pipelines/cross_core_contract/l4_transition_checklist.yaml', 'docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml', 'docs/pipelines/cross_core_contract/pipeline.md', 'docs/pipelines/cross_core_contract/state.yaml', 'docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml']
VALIDATOR_IDS = ['validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution', 'validate_cross_core_rollback_or_reconciliation_path']
FORBIDDEN = [
    "core_mutation_authorized: true",
    "backlog_closure_authorized: true",
    "release_or_promotion_authorized: true",
    "l4_active_now: true",
    "executable_as_l4_gate_now: true",
    "decision_status: approved",
    "promotion_materialized_now: true",
    "backlog_closure_now: true",
    "rollback_execution_now: true",
]

def iso_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_remaining_l4_validator_contracts_validation.yaml")
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
        for marker in FORBIDDEN:
            if marker in text:
                findings.append({"finding_id": "forbidden_marker", "severity": "blocking", "path": rp, "message": marker})
        if rp.endswith(".contract.yaml"):
            for marker in [
                "status: contract_defined_inactive",
                "l4_active_now: false",
                "executable_as_l4_gate_now: false",
                "core_mutation_authorized: false",
                "backlog_closure_authorized: false",
                "release_or_promotion_authorized: false",
            ]:
                if marker not in text:
                    findings.append({"finding_id": "missing_contract_marker", "severity": "blocking", "path": rp, "message": marker})
        if rp.endswith(".contract.md"):
            for marker in ["contract_defined: true", "l4_active_now: false", "executable_as_l4_gate_now: false"]:
                if marker not in text:
                    findings.append({"finding_id": "missing_contract_md_marker", "severity": "blocking", "path": rp, "message": marker})

    aggregate_files = [
        "docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md",
        "docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml",
        "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml",
        "docs/pipelines/cross_core_contract/pipeline.md",
        "docs/pipelines/cross_core_contract/state.yaml",
        "docs/pipelines/cross_core_contract/l4_transition_checklist.yaml",
    ]
    for rp in aggregate_files:
        text = (REPO / rp).read_text(encoding="utf-8") if (REPO / rp).exists() else ""
        for validator_id in VALIDATOR_IDS:
            if validator_id not in text:
                findings.append({"finding_id": "aggregate_missing_validator_id", "severity": "blocking", "path": rp, "message": validator_id})

    request_path = REPO / "docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml"
    request_text = request_path.read_text(encoding="utf-8")
    for marker in ["status: proposed", "decision_status: pending_arbitration"]:
        if marker not in request_text:
            findings.append({"finding_id": "request_status_changed", "severity": "blocking", "path": str(request_path), "message": marker})

    status = "PASS" if not findings else "FAIL"
    lines = [
        "cross_core_remaining_l4_validator_contracts_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        "  phase: PHASE_45_CROSS_CORE_REMAINING_L4_VALIDATOR_CONTRACTS",
        "  l4_active_now: false",
        "  executable_as_l4_gate_now: false",
        "  checked_files:",
    ]
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
            if "message" in item:
                lines.append(f"      message: {item['message']}")
    else:
        lines.append("    []")
    lines.extend([
        "  result_summary:",
        f"    blocking_finding_count: {len(findings)}",
        "    remaining_l4_validator_contracts_defined: true",
        "    l4_active_now: false",
        "    executable_as_l4_gate_now: false",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
        "    request_remains_proposed_pending_arbitration: true",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Status: {status}")
    print(f"Wrote {report_path}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
