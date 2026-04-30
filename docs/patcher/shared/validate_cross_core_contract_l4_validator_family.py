#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

REPO = Path.cwd()

REQUIRED_FILES = [
    "docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md",
    "docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml",
    "docs/pipelines/cross_core_contract/L4_TARGET_CONTRACT.md",
    "docs/pipelines/cross_core_contract/l4_transition_checklist.yaml",
    "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml",
    "docs/pipelines/cross_core_contract/pipeline.md",
    "docs/pipelines/cross_core_contract/state.yaml",
    "docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml",
]

VALIDATOR_NAMES = [
    "validate_cross_core_l4_transition_review",
    "validate_cross_core_write_surface",
    "validate_constitution_referentiel_link_reconstruction",
    "validate_link_binding_consistency",
    "validate_multi_core_release_plan",
    "validate_multi_core_promotion_manifest",
    "validate_cross_core_backlog_resolution",
    "validate_cross_core_rollback_or_reconciliation_path",
]

REQUIRED_MARKERS = {
    "docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md": [
        "validator_family_defined: true",
        "validators_executable_as_l4_gate_now: false",
        "core_mutation_authorized: false",
        "backlog_closure_authorized: false",
        "release_or_promotion_authorized: false",
    ],
    "docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml": [
        "status: target_defined_inactive",
        "l4_active_now: false",
        "validator_family_defined: true",
        "validators_executable_as_l4_gate_now: false",
    ],
    "docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml": [
        "l4_validator_family:",
        "validators_executable_as_l4_gate_now: false",
        "individual_validator_scripts_required_before_L4_execution: true",
    ],
    "docs/pipelines/cross_core_contract/pipeline.md": [
        "L4 validator family",
        "validators_executable_as_l4_gate_now: false",
    ],
    "docs/pipelines/cross_core_contract/state.yaml": [
        "l4_validator_family_defined: true",
        "validators_executable_as_l4_gate_now: false",
    ],
    "docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml": [
        "status: proposed",
        "decision_status: pending_arbitration",
    ],
}

FORBIDDEN_MARKERS = [
    "core_mutation_authorized: true",
    "backlog_closure_authorized: true",
    "release_or_promotion_authorized: true",
    "l4_active_now: true",
    "validators_executable_as_l4_gate_now: true",
    "decision_status: approved",
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml")
    findings = []
    checked = []

    for rel_path in REQUIRED_FILES:
        path = REPO / rel_path
        exists = path.exists()
        checked.append({"path": rel_path, "exists": exists, "sha256": sha256_file(path) if exists else None})
        if not exists:
            findings.append({"finding_id": "missing_required_file", "severity": "blocking", "path": rel_path})
            continue
        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS.get(rel_path, []):
            if marker not in text:
                findings.append({"finding_id": "missing_required_marker", "severity": "blocking", "path": rel_path, "message": marker})
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                findings.append({"finding_id": "forbidden_marker", "severity": "blocking", "path": rel_path, "message": marker})
        if rel_path.endswith("L4_VALIDATOR_FAMILY.md") or rel_path.endswith("l4_validator_family.yaml"):
            for name in VALIDATOR_NAMES:
                if name not in text:
                    findings.append({"finding_id": "missing_validator_name", "severity": "blocking", "path": rel_path, "message": name})

    status = "PASS" if not findings else "FAIL"
    lines = [
        "cross_core_contract_l4_validator_family_validation:",
        "  schema_version: '0.1'",
        f"  generated_at: '{iso_now()}'",
        f"  status: {status}",
        "  target_level: L4_critical_canonical_pipeline",
        "  l4_active_now: false",
        "  validator_family_defined: true",
        "  validators_executable_as_l4_gate_now: false",
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
        "    l4_validator_family_defined: true",
        "    l4_active_now: false",
        "    validators_executable_as_l4_gate_now: false",
        "    individual_validator_scripts_required_before_L4_execution: true",
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
