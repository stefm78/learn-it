#!/usr/bin/env python3
"""Validate the OPEN_NEW_RUN bounded-run preflight gate.

Read-only validator, except for its own report output.

Purpose:
- prove that OPEN_NEW_RUN reads and preserves bounded-run preflight status;
- prove that a current PREFLIGHT_DEFER_TO_STAGE00_REVIEW report does not authorize
  opening a backlog-driven run by default;
- prove that ignoring PREFLIGHT_DEFER_TO_STAGE00_REVIEW requires explicit human override.

Default output:
  docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml
"""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

DEFAULT_ENTRY_ACTION = Path("docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml")
DEFAULT_PREFLIGHT_REPORT = Path("docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml")
DEFAULT_RUNS_INDEX = Path("docs/pipelines/constitution/runs/index.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml")

DEFER_STATUS = "PREFLIGHT_DEFER_TO_STAGE00_REVIEW"
READY_STATUS = "PREFLIGHT_READY_TO_OPEN_RUN"
BLOCKED_STATUS = "BLOCKED"

REQUIRED_PRECONDITIONS = [
    "no_active_run_required_for_recommended_default",
    "scope_key_must_be_published",
    "scope_maturity_must_be_available_for_run",
    "bounded_run_preflight_required_when_backlog_signal_impacts_target_scope",
    "bounded_run_preflight_must_be_non_mutating",
]

REQUIRED_DECISION_PAYLOAD_FIELDS = [
    "entry_decision",
    "target_scope_key",
    "scope_publication_status",
    "active_runs_count",
    "governance_backlog_signal",
    "bounded_run_preflight_required",
    "bounded_run_preflight_status",
    "bounded_run_preflight_recommendation",
    "bounded_run_preflight_report_ref",
    "open_materialization_status",
    "next_best_action",
    "next_action_contract_ref",
    "run_id_pattern",
    "canonical_scripts",
    "stop_after_decision",
    "next_best_action_reason",
]

REQUIRED_ALLOWED_DECISIONS = [
    "open_new_run_authorized",
    "open_new_run_blocked",
    "open_new_run_requires_preflight",
    "partition_refresh_preferred",
]

REQUIRED_FORBIDDEN_ACTIONS = [
    "direct_write_of_runs_index",
    "implicit_stage_start",
    "ignore_required_bounded_run_preflight",
    "mutate_bounded_run_preflight_report_from_open_new_run",
    "authorize_backlog_driven_run_when_preflight_is_missing_or_blocked",
    "auto_chain_to_next_action_without_confirmation",
]

REQUIRED_RULE_FRAGMENTS = [
    "read bounded_run_preflight_report.yaml before authorizing open_new_run",
    "PREFLIGHT_READY_TO_OPEN_RUN",
    "open_new_run_authorized may be emitted after human confirmation",
    "PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
    "prefer partition_refresh_preferred or open_new_run_blocked unless human explicitly overrides",
    "PREFLIGHT_DESIGN_NOTE_ONLY or PREFLIGHT_KEEP_BACKLOG_OPEN",
    "do not authorize run opening from backlog signal alone",
    "BLOCKED or is missing while required",
    "emit open_new_run_blocked",
    "do not start STAGE_01_CHALLENGE",
    "do not emit or apply stage transition commands",
]

REQUIRED_PREFLIGHT_BEHAVIOR_MUST_DO_FRAGMENTS = [
    "read bounded_run_preflight_report.yaml if present in allowed_reads",
    "preserve the preflight status and recommendation in decision_payload",
    "block or require preflight if report is missing or BLOCKED",
    "require explicit human override before ignoring PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
]

REQUIRED_PREFLIGHT_BEHAVIOR_MUST_NOT_DO_FRAGMENTS = [
    "treat open backlog entries as sufficient authorization by themselves",
    "open a run when preflight recommends design_note_only or keep_backlog_open",
    "mutate bounded_run_preflight_report.yaml from OPEN_NEW_RUN",
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid YAML root in {path}: expected mapping")
    return data


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False, width=120)


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}")
    return value


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def text_blob(values: Iterable[Any]) -> str:
    parts: List[str] = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            parts.extend(text_blob(value.values()).split("\n"))
        elif isinstance(value, list):
            parts.extend(text_blob(value).split("\n"))
        elif value is not None:
            parts.append(str(value))
    return "\n".join(parts)


def has_exact(items: List[Any], expected: str) -> bool:
    return expected in [str(item) for item in items]


def contains_fragment(text: str, fragment: str) -> bool:
    return fragment in text


def add_blocking(findings: List[Dict[str, Any]], finding_id: str, message: str, **extra: Any) -> None:
    item: Dict[str, Any] = {
        "finding_id": finding_id,
        "severity": "blocking",
        "message": message,
    }
    item.update(extra)
    findings.append(item)


def add_warning(warnings: List[Dict[str, Any]], warning_id: str, message: str, **extra: Any) -> None:
    item: Dict[str, Any] = {
        "warning_id": warning_id,
        "severity": "warning",
        "message": message,
    }
    item.update(extra)
    warnings.append(item)


def evaluate_contract(entry_action: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    findings: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    if entry_action.get("action_id") != "OPEN_NEW_RUN":
        add_blocking(
            findings,
            "OPEN_GATE_ACTION_ID_MISMATCH",
            "entry_action.action_id must be OPEN_NEW_RUN.",
            actual=entry_action.get("action_id"),
        )

    if entry_action.get("action_kind") != "entry_resolution":
        add_blocking(
            findings,
            "OPEN_GATE_ACTION_KIND_MISMATCH",
            "entry_action.action_kind must be entry_resolution.",
            actual=entry_action.get("action_kind"),
        )

    allowed_reads = as_list(entry_action.get("allowed_reads"))
    preconditions = as_list(entry_action.get("preconditions"))
    resolution_rules = as_list(entry_action.get("resolution_rules"))
    forbidden_actions = as_list(entry_action.get("forbidden_actions"))
    required_outputs = as_dict(entry_action.get("required_outputs"))
    decision_payload = as_list(required_outputs.get("decision_payload"))
    allowed_decisions = as_list(required_outputs.get("allowed_entry_decision_values"))
    response_contract = as_dict(entry_action.get("response_contract"))
    preflight_behavior = as_dict(response_contract.get("preflight_behavior"))
    preflight_must_do = as_list(preflight_behavior.get("must_do"))
    preflight_must_not_do = as_list(preflight_behavior.get("must_not_do"))

    allowed_reads_ok = "docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml" in allowed_reads
    if not allowed_reads_ok:
        add_blocking(
            findings,
            "OPEN_GATE_PREFLIGHT_REPORT_NOT_ALLOWED_READ",
            "OPEN_NEW_RUN must allow reading bounded_run_preflight_report.yaml.",
        )

    for precondition in REQUIRED_PRECONDITIONS:
        if not has_exact(preconditions, precondition):
            add_blocking(
                findings,
                "OPEN_GATE_REQUIRED_PRECONDITION_MISSING",
                "OPEN_NEW_RUN is missing a required precondition.",
                missing_precondition=precondition,
            )

    rules_blob = text_blob(resolution_rules)
    for fragment in REQUIRED_RULE_FRAGMENTS:
        if not contains_fragment(rules_blob, fragment):
            add_blocking(
                findings,
                "OPEN_GATE_REQUIRED_RESOLUTION_RULE_FRAGMENT_MISSING",
                "OPEN_NEW_RUN is missing an expected resolution rule fragment.",
                missing_fragment=fragment,
            )

    for forbidden in REQUIRED_FORBIDDEN_ACTIONS:
        if not has_exact(forbidden_actions, forbidden):
            add_blocking(
                findings,
                "OPEN_GATE_REQUIRED_FORBIDDEN_ACTION_MISSING",
                "OPEN_NEW_RUN is missing a required forbidden action.",
                missing_forbidden_action=forbidden,
            )

    for field in REQUIRED_DECISION_PAYLOAD_FIELDS:
        if not has_exact(decision_payload, field):
            add_blocking(
                findings,
                "OPEN_GATE_DECISION_PAYLOAD_FIELD_MISSING",
                "OPEN_NEW_RUN decision payload must expose preflight and decision metadata.",
                missing_field=field,
            )

    for decision in REQUIRED_ALLOWED_DECISIONS:
        if not has_exact(allowed_decisions, decision):
            add_blocking(
                findings,
                "OPEN_GATE_ALLOWED_DECISION_MISSING",
                "OPEN_NEW_RUN allowed_entry_decision_values is missing an expected value.",
                missing_decision=decision,
            )

    must_do_blob = text_blob(preflight_must_do)
    for fragment in REQUIRED_PREFLIGHT_BEHAVIOR_MUST_DO_FRAGMENTS:
        if not contains_fragment(must_do_blob, fragment):
            add_blocking(
                findings,
                "OPEN_GATE_PREFLIGHT_MUST_DO_FRAGMENT_MISSING",
                "OPEN_NEW_RUN preflight_behavior.must_do is missing an expected fragment.",
                missing_fragment=fragment,
            )

    must_not_blob = text_blob(preflight_must_not_do)
    for fragment in REQUIRED_PREFLIGHT_BEHAVIOR_MUST_NOT_DO_FRAGMENTS:
        if not contains_fragment(must_not_blob, fragment):
            add_blocking(
                findings,
                "OPEN_GATE_PREFLIGHT_MUST_NOT_DO_FRAGMENT_MISSING",
                "OPEN_NEW_RUN preflight_behavior.must_not_do is missing an expected fragment.",
                missing_fragment=fragment,
            )

    stop_after_decision = as_dict(entry_action.get("entry_binding")).get("stop_after_decision")
    if stop_after_decision is not True:
        add_blocking(
            findings,
            "OPEN_GATE_STOP_AFTER_DECISION_NOT_TRUE",
            "OPEN_NEW_RUN must stop after decision resolution.",
            actual=stop_after_decision,
        )

    contract_eval = {
        "action_id": entry_action.get("action_id"),
        "action_kind": entry_action.get("action_kind"),
        "allowed_reads_contains_preflight_report": allowed_reads_ok,
        "required_preconditions_present": sorted(set(REQUIRED_PRECONDITIONS) - {f.get("missing_precondition") for f in findings if f.get("finding_id") == "OPEN_GATE_REQUIRED_PRECONDITION_MISSING"}),
        "allowed_entry_decision_values": [str(item) for item in allowed_decisions],
        "stop_after_decision": stop_after_decision,
        "defer_rule_present": contains_fragment(rules_blob, "PREFLIGHT_DEFER_TO_STAGE00_REVIEW")
        and contains_fragment(rules_blob, "prefer partition_refresh_preferred or open_new_run_blocked unless human explicitly overrides"),
        "ready_rule_requires_human_confirmation": contains_fragment(rules_blob, "PREFLIGHT_READY_TO_OPEN_RUN")
        and contains_fragment(rules_blob, "open_new_run_authorized may be emitted after human confirmation"),
        "missing_or_blocked_rule_present": contains_fragment(rules_blob, "BLOCKED or is missing while required")
        and contains_fragment(rules_blob, "emit open_new_run_blocked"),
        "preflight_behavior_requires_human_override_on_defer": contains_fragment(
            must_do_blob,
            "require explicit human override before ignoring PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
        ),
        "preflight_behavior_preserves_status_and_recommendation": contains_fragment(
            must_do_blob,
            "preserve the preflight status and recommendation in decision_payload",
        ),
    }

    if findings:
        add_warning(
            warnings,
            "OPEN_GATE_CONTRACT_HAS_BLOCKING_FINDINGS",
            "Contract evaluation has blocking findings; derived default decision may be unsafe.",
            blocking_finding_count=len(findings),
        )

    return contract_eval, findings, warnings


def evaluate_preflight(preflight_root: Dict[str, Any], runs_root: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    findings: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    decision = as_dict(preflight_root.get("decision"))
    active_run_check = as_dict(preflight_root.get("active_run_check"))
    backlog_signal = as_dict(preflight_root.get("backlog_signal"))
    mutation_policy = as_dict(preflight_root.get("mutation_policy"))

    status = preflight_root.get("status")
    decision_status = decision.get("status")
    recommendation = decision.get("recommendation")
    new_run_recommended = decision.get("new_bounded_run_recommended_now")
    active_runs = as_list(runs_root.get("active_runs"))

    if status != decision_status:
        add_blocking(
            findings,
            "OPEN_GATE_PREFLIGHT_STATUS_MISMATCH",
            "Preflight top-level status must match decision.status.",
            top_level_status=status,
            decision_status=decision_status,
        )

    if status != DEFER_STATUS:
        add_blocking(
            findings,
            "OPEN_GATE_CURRENT_PREFLIGHT_NOT_DEFER",
            "Current PHASE_23B validation expects PREFLIGHT_DEFER_TO_STAGE00_REVIEW.",
            actual_status=status,
        )

    if recommendation != "defer_to_stage00_backlog_review":
        add_blocking(
            findings,
            "OPEN_GATE_PREFLIGHT_RECOMMENDATION_MISMATCH",
            "PREFLIGHT_DEFER_TO_STAGE00_REVIEW must recommend defer_to_stage00_backlog_review.",
            actual_recommendation=recommendation,
        )

    if new_run_recommended is not False:
        add_blocking(
            findings,
            "OPEN_GATE_PREFLIGHT_RECOMMENDS_RUN_UNEXPECTEDLY",
            "Current preflight must not recommend a new bounded run now.",
            actual=new_run_recommended,
        )

    if active_run_check.get("active_run_count") != 0:
        add_blocking(
            findings,
            "OPEN_GATE_PREFLIGHT_ACTIVE_RUN_COUNT_NOT_ZERO",
            "Current preflight should confirm no active run.",
            actual=active_run_check.get("active_run_count"),
        )

    if active_runs:
        add_blocking(
            findings,
            "OPEN_GATE_RUNS_INDEX_HAS_ACTIVE_RUNS",
            "runs/index.yaml currently has active runs; default run opening cannot be validated as clean.",
            active_runs=active_runs,
        )

    if backlog_signal.get("matching_open_entry_count", 0) <= 0:
        add_blocking(
            findings,
            "OPEN_GATE_NO_BACKLOG_SIGNAL_TO_GATE",
            "Current validation expects open backlog entries impacting the target scope.",
            actual=backlog_signal.get("matching_open_entry_count"),
        )

    for key in ["runs_index", "governance_backlog_yaml", "policy_yaml", "decisions_yaml", "scope_catalog", "cores"]:
        if mutation_policy.get(key) != "not_modified":
            add_blocking(
                findings,
                "OPEN_GATE_PREFLIGHT_MUTATION_POLICY_NOT_READ_ONLY",
                "Preflight mutation policy must remain non-mutating.",
                mutation_key=key,
                actual=mutation_policy.get(key),
            )

    current_preflight = {
        "requested_scope_key": preflight_root.get("requested_scope_key"),
        "status": status,
        "decision_status": decision_status,
        "recommendation": recommendation,
        "new_bounded_run_recommended_now": new_run_recommended,
        "matching_open_entry_count": backlog_signal.get("matching_open_entry_count"),
        "open_entries_all_scopes": backlog_signal.get("open_entries_all_scopes"),
        "active_run_count_from_preflight": active_run_check.get("active_run_count"),
        "active_run_count_from_runs_index": len(active_runs),
        "non_mutating_preflight_confirmed": all(
            mutation_policy.get(key) == "not_modified"
            for key in ["runs_index", "governance_backlog_yaml", "policy_yaml", "decisions_yaml", "scope_catalog", "cores"]
        ),
    }

    return current_preflight, findings, warnings


def derive_default_gate_decision(preflight_status: str) -> Dict[str, Any]:
    if preflight_status == READY_STATUS:
        return {
            "preflight_status": preflight_status,
            "open_new_run_authorized_by_default": False,
            "open_new_run_authorizable_after_human_confirmation": True,
            "recommended_entry_decision": "open_new_run_authorized_after_human_confirmation",
            "next_best_action": "MATERIALIZE_NEW_RUN",
            "human_override_required_to_ignore_preflight": False,
            "reason": "READY status can authorize opening only after explicit human confirmation.",
        }
    if preflight_status == DEFER_STATUS:
        return {
            "preflight_status": preflight_status,
            "open_new_run_authorized_by_default": False,
            "open_new_run_authorizable_after_human_confirmation": False,
            "recommended_entry_decision": "partition_refresh_preferred_or_open_new_run_blocked",
            "next_best_action": "PARTITION_REFRESH_OR_STOP",
            "human_override_required_to_authorize": True,
            "reason": "DEFER status is not a run-opening authorization. It requires STAGE_00 review or explicit human override.",
        }
    if preflight_status == BLOCKED_STATUS:
        return {
            "preflight_status": preflight_status,
            "open_new_run_authorized_by_default": False,
            "open_new_run_authorizable_after_human_confirmation": False,
            "recommended_entry_decision": "open_new_run_blocked",
            "next_best_action": "RESOLVE_BLOCKER",
            "human_override_required_to_authorize": True,
            "reason": "BLOCKED status must block default run opening.",
        }
    return {
        "preflight_status": preflight_status,
        "open_new_run_authorized_by_default": False,
        "open_new_run_authorizable_after_human_confirmation": False,
        "recommended_entry_decision": "open_new_run_blocked_or_requires_preflight",
        "next_best_action": "INSPECT_PREFLIGHT",
        "human_override_required_to_authorize": True,
        "reason": "Unknown or non-authorizing preflight status cannot authorize default run opening.",
    }


def build_report(entry_action_path: Path, preflight_report_path: Path, runs_index_path: Path) -> Dict[str, Any]:
    entry_root = get_root(load_yaml(entry_action_path), "entry_action")
    preflight_root = get_root(load_yaml(preflight_report_path), "bounded_run_preflight_report")
    runs_root = get_root(load_yaml(runs_index_path), "runs_index")

    contract_eval, contract_findings, contract_warnings = evaluate_contract(entry_root)
    preflight_eval, preflight_findings, preflight_warnings = evaluate_preflight(preflight_root, runs_root)
    derived_decision = derive_default_gate_decision(str(preflight_root.get("status")))

    findings = contract_findings + preflight_findings
    warnings = contract_warnings + preflight_warnings

    if derived_decision.get("open_new_run_authorized_by_default") is not False:
        add_blocking(
            findings,
            "OPEN_GATE_DEFAULT_AUTHORIZATION_NOT_FALSE",
            "Derived default gate decision must not authorize opening a run by default.",
            derived_decision=derived_decision,
        )

    expected_recommended = "partition_refresh_preferred_or_open_new_run_blocked"
    if preflight_root.get("status") == DEFER_STATUS and derived_decision.get("recommended_entry_decision") != expected_recommended:
        add_blocking(
            findings,
            "OPEN_GATE_DEFER_RECOMMENDED_DECISION_MISMATCH",
            "DEFER status must map to partition_refresh_preferred_or_open_new_run_blocked.",
            actual=derived_decision.get("recommended_entry_decision"),
        )

    status = "PASS" if not findings else "FAIL"

    return {
        "open_new_run_preflight_gate_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": status,
            "purpose": (
                "Validate that OPEN_NEW_RUN respects bounded-run preflight and does not authorize "
                "a backlog-driven run by default when preflight is PREFLIGHT_DEFER_TO_STAGE00_REVIEW."
            ),
            "mutation_policy": {
                "entry_action": "read_only",
                "bounded_run_preflight_report": "read_only",
                "runs_index": "read_only",
                "policy_yaml": "not_read",
                "decisions_yaml": "not_read",
                "scope_catalog": "not_read",
                "governance_backlog_yaml": "not_read",
                "cores": "not_read",
                "report": "write_only_output",
            },
            "inputs": [
                {"ref": normalize_path(entry_action_path), "sha256": sha256_file(entry_action_path)},
                {"ref": normalize_path(preflight_report_path), "sha256": sha256_file(preflight_report_path)},
                {"ref": normalize_path(runs_index_path), "sha256": sha256_file(runs_index_path)},
            ],
            "evaluated_contract": contract_eval,
            "current_preflight": preflight_eval,
            "evaluated_default_entry_decision": derived_decision,
            "blocking_findings": findings,
            "warnings": warnings,
            "result_summary": {
                "open_new_run_authorized_by_default": derived_decision.get("open_new_run_authorized_by_default"),
                "preflight_status": preflight_eval.get("status"),
                "recommended_entry_decision": derived_decision.get("recommended_entry_decision"),
                "human_override_required_to_authorize": derived_decision.get("human_override_required_to_authorize"),
                "no_active_run_confirmed": preflight_eval.get("active_run_count_from_runs_index") == 0,
                "blocking_finding_count": len(findings),
                "warning_count": len(warnings),
            },
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate OPEN_NEW_RUN bounded-run preflight gate.")
    parser.add_argument("--entry-action", default=str(DEFAULT_ENTRY_ACTION))
    parser.add_argument("--preflight-report", default=str(DEFAULT_PREFLIGHT_REPORT))
    parser.add_argument("--runs-index", default=str(DEFAULT_RUNS_INDEX))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(
        entry_action_path=Path(args.entry_action),
        preflight_report_path=Path(args.preflight_report),
        runs_index_path=Path(args.runs_index),
    )
    write_yaml(Path(args.report), report)

    root = report["open_new_run_preflight_gate_validation"]
    summary = root["result_summary"]
    print(f"Wrote {args.report}")
    print(f"Status: {root['status']}")
    print(f"Preflight status: {summary['preflight_status']}")
    print(f"Open new run authorized by default: {summary['open_new_run_authorized_by_default']}")
    print(f"Recommended entry decision: {summary['recommended_entry_decision']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    print(f"Warnings: {summary['warning_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
