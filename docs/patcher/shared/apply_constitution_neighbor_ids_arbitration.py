#!/usr/bin/env python3
"""Apply PHASE_16 Constitution neighbor IDs arbitration to decisions.yaml.

Generic deterministic patcher for STAGE_00 neighbor IDs governance.

Safety gates:
- refuses to patch unless the arbitration validation report is PASS_READY_TO_PATCH;
- only applies items where:
    human_decision: add_as_default_neighbor
    patch_policy_decisions_after_approval: true
- default mode is dry-run; use --apply to write decisions.yaml;
- never modifies policy.yaml, generated scope catalog files, maturity scores, or scorer rules.

Reads:
  docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml
  docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml
  docs/pipelines/constitution/policies/scope_generation/decisions.yaml

Writes with --apply:
  docs/pipelines/constitution/policies/scope_generation/decisions.yaml

Always writes:
  docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml
"""

from __future__ import annotations

import argparse
import copy
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEFAULT_ARBITRATION = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml")
DEFAULT_VALIDATION = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml")
DEFAULT_DECISIONS = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().upper())
    return re.sub(r"_+", "_", value).strip("_")


def unique_sorted(values: List[str]) -> List[str]:
    return sorted(set(str(v) for v in values if str(v).strip()))


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    root = doc.get(key)
    if not isinstance(root, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}.")
    return root


def validation_status(validation_doc: Dict[str, Any]) -> str:
    return str(
        validation_doc.get("constitution_neighbor_ids_arbitration_validation", {})
        .get("status", "")
    )


def patch_ready_items(arbitration_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    root = get_root(arbitration_doc, "constitution_neighbor_ids_arbitration")
    items = root.get("items", [])
    if not isinstance(items, list):
        raise SystemExit("constitution_neighbor_ids_arbitration.items must be a list.")

    selected = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if (
            item.get("human_decision") == "add_as_default_neighbor"
            and item.get("patch_policy_decisions_after_approval") is True
        ):
            selected.append(item)
    return selected


def existing_decision_by_id(decisions: List[Dict[str, Any]], decision_id: str) -> Dict[str, Any] | None:
    for decision in decisions:
        if decision.get("decision_id") == decision_id:
            return decision
    return None


def build_decision(scope_key: str, items: List[Dict[str, Any]], applies_from: str) -> Dict[str, Any]:
    target_ids = unique_sorted([str(item.get("uncovered_id")) for item in items])
    candidate_ids = unique_sorted([str(item.get("candidate_id")) for item in items])
    owner_scopes = unique_sorted([str(item.get("owner_scope_key")) for item in items if item.get("owner_scope_key")])

    return {
        "decision_id": f"SGEN_DECISION_PHASE16_NEIGHBOR_IDS__{slug(scope_key)}",
        "status": "approved",
        "decision_type": "force_logical_neighbors",
        "scope_keys_affected": [scope_key],
        "target_ids": target_ids,
        "target_patterns": [],
        "decision_payload": {
            "neighbor_class": "explicit_constitution_dependency_from_scoring_v1_1",
            "read_mode": "primary",
            "source_phase": "PHASE_16",
            "source_report": "docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml",
            "source_arbitration": "docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml",
            "source_validation": "docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml",
            "source_candidate_ids": candidate_ids,
            "owner_scope_keys": owner_scopes,
            "note": (
                "Approved by human arbitration after scope maturity scoring V1.1 surfaced "
                "under-declared Constitution neighbor IDs."
            ),
        },
        "applies_from": applies_from,
        "decided_by": "human",
        "challenged_with_ai": True,
        "justification": (
            "Human arbitration accepted these uncovered Constitution IDs as explicit read neighbors "
            f"for scope {scope_key}. The change declares read dependencies only; ownership remains unchanged."
        ),
    }


def merge_existing_decision(existing: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    if existing.get("decision_type") != "force_logical_neighbors":
        raise SystemExit(f"Existing decision {existing.get('decision_id')} is not force_logical_neighbors.")
    if existing.get("status") != "approved":
        raise SystemExit(f"Existing decision {existing.get('decision_id')} is not approved.")

    merged = copy.deepcopy(existing)
    merged["target_ids"] = unique_sorted((merged.get("target_ids") or []) + (patch.get("target_ids") or []))

    payload = merged.setdefault("decision_payload", {})
    if not isinstance(payload, dict):
        raise SystemExit(f"Existing decision {existing.get('decision_id')} has non-mapping decision_payload.")

    patch_payload = patch.get("decision_payload", {})
    payload["source_phase"] = "PHASE_16"
    payload["neighbor_class"] = payload.get("neighbor_class") or patch_payload.get("neighbor_class")
    payload["read_mode"] = payload.get("read_mode") or patch_payload.get("read_mode")
    payload["source_report"] = patch_payload.get("source_report")
    payload["source_arbitration"] = patch_payload.get("source_arbitration")
    payload["source_validation"] = patch_payload.get("source_validation")
    payload["source_candidate_ids"] = unique_sorted(
        (payload.get("source_candidate_ids") or []) + (patch_payload.get("source_candidate_ids") or [])
    )
    payload["owner_scope_keys"] = unique_sorted(
        (payload.get("owner_scope_keys") or []) + (patch_payload.get("owner_scope_keys") or [])
    )

    merged["justification"] = patch["justification"]
    return merged


def synthesize_patch(decisions_doc: Dict[str, Any], items: List[Dict[str, Any]], applies_from: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
    decisions_root = get_root(decisions_doc, "scope_generation_decisions")
    decisions = decisions_root.get("decisions")
    if not isinstance(decisions, list):
        raise SystemExit("scope_generation_decisions.decisions must be a list.")

    patched_doc = copy.deepcopy(decisions_doc)
    patched_decisions = get_root(patched_doc, "scope_generation_decisions")["decisions"]

    by_scope: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        scope_key = str(item.get("scope_key") or "")
        if not scope_key:
            raise SystemExit(f"Patch-ready item missing scope_key: {item.get('candidate_id')}")
        by_scope[scope_key].append(item)

    actions = []
    for scope_key in sorted(by_scope):
        proposed = build_decision(scope_key, by_scope[scope_key], applies_from)
        decision_id = proposed["decision_id"]
        existing = existing_decision_by_id(patched_decisions, decision_id)
        if existing is None:
            patched_decisions.append(proposed)
            actions.append({
                "action": "append_decision",
                "decision_id": decision_id,
                "scope_key": scope_key,
                "target_ids": proposed["target_ids"],
                "candidate_ids": proposed["decision_payload"]["source_candidate_ids"],
            })
        else:
            merged = merge_existing_decision(existing, proposed)
            patched_decisions[patched_decisions.index(existing)] = merged
            actions.append({
                "action": "merge_existing_decision",
                "decision_id": decision_id,
                "scope_key": scope_key,
                "target_ids": merged["target_ids"],
                "candidate_ids": merged["decision_payload"].get("source_candidate_ids", []),
            })

    return patched_doc, {
        "scope_count": len(by_scope),
        "patch_ready_item_count": len(items),
        "decision_count_to_append_or_merge": len(actions),
        "actions": actions,
    }


def blocked_report(report_path: Path, args: argparse.Namespace, status: str) -> None:
    report = {
        "constitution_neighbor_ids_decisions_patch_report": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "BLOCKED",
            "apply_mode": bool(args.apply),
            "blocking_reason": "arbitration_validation_not_pass_ready_to_patch",
            "validation_status": status,
            "inputs": {
                "arbitration": str(Path(args.arbitration)).replace("\\", "/"),
                "validation": str(Path(args.validation)).replace("\\", "/"),
                "decisions": str(Path(args.decisions)).replace("\\", "/"),
            },
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "maturity_scores": "not_modified",
                "scorer_rules": "not_modified",
            },
        }
    }
    write_yaml(report_path, report)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply PHASE_16 neighbor IDs arbitration to decisions.yaml.")
    parser.add_argument("--arbitration", default=str(DEFAULT_ARBITRATION))
    parser.add_argument("--validation", default=str(DEFAULT_VALIDATION))
    parser.add_argument("--decisions", default=str(DEFAULT_DECISIONS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--applies-from", default=today())
    parser.add_argument("--apply", action="store_true", help="Write decisions.yaml. Default is dry-run only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    arbitration_doc = load_yaml(Path(args.arbitration))
    validation_doc = load_yaml(Path(args.validation))
    decisions_doc = load_yaml(Path(args.decisions))
    report_path = Path(args.report)

    status = validation_status(validation_doc)
    if status != "PASS_READY_TO_PATCH":
        blocked_report(report_path, args, status)
        print(f"Wrote {report_path}")
        print(f"Status: BLOCKED ({status})")
        return 0

    selected = patch_ready_items(arbitration_doc)
    patched_doc, patch_summary = synthesize_patch(decisions_doc, selected, str(args.applies_from))
    changed = patched_doc != decisions_doc

    if args.apply and changed:
        write_yaml(Path(args.decisions), patched_doc)

    report = {
        "constitution_neighbor_ids_decisions_patch_report": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS",
            "apply_mode": bool(args.apply),
            "changed": changed,
            "inputs": {
                "arbitration": str(Path(args.arbitration)).replace("\\", "/"),
                "validation": str(Path(args.validation)).replace("\\", "/"),
                "decisions": str(Path(args.decisions)).replace("\\", "/"),
            },
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "modified_if_apply_true_and_changed",
                "scope_catalog": "not_modified",
                "maturity_scores": "not_modified",
                "scorer_rules": "not_modified",
            },
            "patch_summary": patch_summary,
            "next_steps_after_apply": [
                "run generate_constitution_scopes.py --apply",
                "rerun scope maturity scoring",
                "validate that dependency_explicitness deltas are reduced or explicitly accepted",
            ] if args.apply and changed else [],
        }
    }
    write_yaml(report_path, report)

    print(f"Wrote {report_path}")
    print(f"Status: PASS apply_mode={args.apply} changed={changed}")
    print(f"Patch-ready items: {patch_summary['patch_ready_item_count']}")
    print(f"Decisions append/merge: {patch_summary['decision_count_to_append_or_merge']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
