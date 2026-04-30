#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import re

GATES = [
    "validate_cross_core_l4_transition_review",
    "validate_cross_core_write_surface",
    "validate_cross_core_rollback_or_reconciliation_path",
    "validate_link_binding_consistency",
    "validate_constitution_referentiel_link_reconstruction",
    "validate_multi_core_release_plan",
    "validate_multi_core_promotion_manifest",
    "validate_cross_core_backlog_resolution",
]

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def extract_contract_id(text: str, fallback: str) -> str:
    match = re.search(r"^\s*contract_id:\s*([A-Za-z0-9_\-]+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else fallback

def materialize(contract_path: Path, output_path: Path, bundle_id: str | None) -> None:
    contract_text = contract_path.read_text(encoding="utf-8")
    contract_id = extract_contract_id(contract_text, contract_path.stem.upper().replace(".", "_"))
    bid = bundle_id or f"CROSS_CORE_GATE_INPUT_BUNDLE__{contract_id}__R00"
    generated_at = iso_now()

    lines = [
        "cross_core_gate_input_bundle:",
        "  schema_version: '0.1'",
        "  template_status: materialized_dry_run_fixture",
        f"  generated_at: '{generated_at}'",
        f"  bundle_id: {bid}",
        "  source_execution_contract:",
        f"    contract_id: {contract_id}",
        f"    contract_file: {str(contract_path).replace(chr(92), chr(47))}",
        "    concrete_contract_bound: true",
        f"    contract_sha256: {sha(contract_path)}",
        "  gate_input_model:",
        "    template_only: false",
        "    gate_input_bundle_ready: true",
        "    request_specific_logic_encoded: false",
        "    dry_run_only: true",
        "  gate_inputs:",
    ]
    for gate in GATES:
        lines.extend([
            f"    {gate}:",
            "      status: materialized_dry_run_input",
            "      input_files:",
            f"        - {str(contract_path).replace(chr(92), chr(47))}",
            f"        - {str(output_path).replace(chr(92), chr(47))}",
            "      expected_execution_mode: dry_run_or_shape_only",
        ])
    lines.extend([
        "  write_surface:",
        "    declared: true",
        "    dry_run_sandbox_only: true",
        "    paths:",
        "      - docs/pipelines/cross_core_contract/work/dry_run_sandbox/**",
        "  rollback_or_reconciliation_inputs:",
        "    declared: true",
        "    files:",
        "      - docs/pipelines/cross_core_contract/work/dry_run_sandbox/rollback_plan.yaml",
        "    rollback_action: discard dry_run_sandbox outputs",
        "  release_and_promotion_inputs:",
        "    release_plan_declared: true",
        "    promotion_manifest_declared: true",
        "    release_materialization_requested: false",
        "    promotion_requested: false",
        "    files:",
        "      - docs/pipelines/cross_core_contract/work/dry_run_sandbox/release_plan.preview.yaml",
        "      - docs/pipelines/cross_core_contract/work/dry_run_sandbox/promotion_manifest.preview.yaml",
        "  backlog_inputs:",
        "    backlog_resolution_requested: false",
        "    backlog_closure_requested: false",
        "    backlog_entries: []",
        "  execution_guardrails:",
        "    downstream_gates_executed: false",
        "    apply_authorized: false",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
        "",
    ])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--bundle-id")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    output_path = Path(args.output)
    if not contract_path.exists():
        print(f"Missing contract: {contract_path}")
        return 1
    materialize(contract_path, output_path, args.bundle_id)
    print(f"Wrote {output_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
