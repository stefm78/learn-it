#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import re

REQUIRED_VALIDATORS = ['validate_cross_core_execution_contract', 'validate_cross_core_l4_transition_review', 'validate_cross_core_write_surface', 'validate_cross_core_rollback_or_reconciliation_path', 'validate_link_binding_consistency', 'validate_constitution_referentiel_link_reconstruction', 'validate_multi_core_release_plan', 'validate_multi_core_promotion_manifest', 'validate_cross_core_backlog_resolution']

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def extract_request_id(text: str, fallback: str) -> str:
    match = re.search(r"^\s*request_id:\s*([A-Za-z0-9_\-]+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else fallback

def materialize_contract(request_path: Path, output_path: Path, contract_id: str | None) -> None:
    request_text = request_path.read_text(encoding="utf-8")
    request_id = extract_request_id(request_text, request_path.stem.upper().replace(".", "_"))
    cid = contract_id or f"CROSS_CORE_EXECUTION_CONTRACT__{{request_id}}__R00"
    generated_at = iso_now()
    request_ref = str(request_path).replace(chr(92), chr(47))

    lines = [
        "cross_core_execution_contract:",
        "  schema_version: '0.1'",
        "  template_status: materialized_from_request_non_authorized",
        f"  generated_at: '{{generated_at}}'",
        f"  contract_id: {{cid}}",
        "  source_request:",
        f"    request_id: {{request_id}}",
        f"    request_file: {{request_ref}}",
        "    request_status_required: accepted_for_arbitrage",
        "  execution_model:",
        "    selected_model: pending_arbitration",
        "    model_selection_status: not_selected",
        "    generic_pipeline_instance: true",
        "  affected_cores:",
        "    constitution:",
        "      affected: maybe",
        "      read_surface: []",
        "      write_surface: []",
        "    referentiel:",
        "      affected: maybe",
        "      read_surface: []",
        "      write_surface: []",
        "    link:",
        "      affected: maybe",
        "      read_surface: []",
        "      write_surface: []",
        "  declared_read_surface:",
        f"    - {{request_ref}}",
        "  declared_write_surface: []",
        "  write_authorization:",
        "    requested_now: false",
        "    granted_now: false",
        "    core_mutation_authorized: false",
        "    backlog_closure_authorized: false",
        "    release_or_promotion_authorized: false",
        "  validation_plan:",
        "    required_validators:",
    ]
    lines.extend([f"      - {{v}}" for v in REQUIRED_VALIDATORS])
    lines.extend([
        "    all_required_validators_must_pass_before_apply: true",
        "    current_validation_status: not_executed_instantiated_contract",
        "  rollback_or_reconciliation_path:",
        "    status: not_declared_yet",
        "    required_before_apply: true",
        "  release_and_promotion_policy:",
        "    release_policy_declared: false",
        "    promotion_policy_declared: false",
        "    release_materialization_requested: false",
        "    promotion_requested: false",
        "  backlog_policy:",
        "    backlog_resolution_requested: false",
        "    backlog_closure_requested: false",
        "    backlog_entries_to_resolve: []",
        "  execution_guardrails:",
        "    template_only: false",
        "    concrete_request_bound: true",
        "    mutating_execution_ready_now: false",
        "    mutating_apply_ready_now: false",
        "    downstream_mutating_gates_executed_now: false",
        "    no_core_write_from_instantiation: true",
        f"    source_request_sha256: {{sha(request_path)}}",
        "",
    ])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--contract-id")
    args = parser.parse_args()

    request_path = Path(args.request)
    output_path = Path(args.output)
    if not request_path.exists():
        print(f"Missing request: {{request_path}}")
        return 1
    materialize_contract(request_path, output_path, args.contract_id)
    print(f"Wrote {{output_path}}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
