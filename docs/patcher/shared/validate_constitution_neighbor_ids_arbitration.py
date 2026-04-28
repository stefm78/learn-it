#!/usr/bin/env python3
# Validate PHASE_16B Constitution neighbor IDs arbitration.
#
# Deterministic and non-mutating.
#
# Status semantics:
# - FAIL: structural or rule violation.
# - PENDING_HUMAN_ARBITRATION: structurally valid, but some items still have pending decisions.
# - PASS_READY_TO_PATCH: all items arbitrated and patch flags are coherent.
#
# Default input:
#   docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml
#
# Default output:
#   docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEFAULT_ARBITRATION = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml")

ALLOWED_DECISIONS = {
    "add_as_default_neighbor",
    "defer_to_governance_backlog",
    "wont_fix_with_rationale",
}
PENDING_VALUE = "pending"


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    if not isinstance(doc, dict):
        raise SystemExit(f"Invalid YAML root in {path}: expected mapping")
    return doc


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def is_non_empty_rationale(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return bool(stripped) and stripped.upper() != "TODO"


def validate(arbitration_path: Path) -> Dict[str, Any]:
    doc = load_yaml(arbitration_path)
    root = doc.get("constitution_neighbor_ids_arbitration")

    findings: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    if not isinstance(root, dict):
        findings.append({
            "finding_id": "NID_ARB_ROOT_MISSING",
            "severity": "blocking",
            "message": "Missing constitution_neighbor_ids_arbitration mapping root.",
        })
        root = {}

    items = root.get("items", [])
    if not isinstance(items, list):
        findings.append({
            "finding_id": "NID_ARB_ITEMS_NOT_LIST",
            "severity": "blocking",
            "message": "items must be a list.",
        })
        items = []

    candidate_ids: List[str] = []
    by_decision: Counter[str] = Counter()
    by_priority: Counter[str] = Counter()
    by_scope: Counter[str] = Counter()
    patch_ready_count = 0
    pending_count = 0
    completed_count = 0

    expected_count = root.get("summary", {}).get("candidate_count") if isinstance(root.get("summary"), dict) else None
    if isinstance(expected_count, int) and expected_count != len(items):
        findings.append({
            "finding_id": "NID_ARB_CANDIDATE_COUNT_MISMATCH",
            "severity": "blocking",
            "summary_candidate_count": expected_count,
            "actual_item_count": len(items),
        })

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            findings.append({
                "finding_id": "NID_ARB_ITEM_NOT_MAPPING",
                "severity": "blocking",
                "item_index": index,
            })
            continue

        candidate_id = str(item.get("candidate_id") or "")
        if not candidate_id:
            findings.append({
                "finding_id": "NID_ARB_CANDIDATE_ID_MISSING",
                "severity": "blocking",
                "item_index": index,
            })
            candidate_id = f"<missing:{index}>"
        candidate_ids.append(candidate_id)

        scope_key = str(item.get("scope_key") or "unknown")
        priority = str(item.get("priority") or "unknown")
        decision = str(item.get("human_decision") or "")
        rationale = item.get("human_rationale")
        patch_flag = item.get("patch_policy_decisions_after_approval")

        by_decision[decision or "missing"] += 1
        by_priority[priority] += 1
        by_scope[scope_key] += 1

        if decision == PENDING_VALUE:
            pending_count += 1
            if patch_flag is True:
                findings.append({
                    "finding_id": "NID_ARB_PENDING_ITEM_CANNOT_PATCH",
                    "severity": "blocking",
                    "candidate_id": candidate_id,
                    "message": "pending items must not set patch_policy_decisions_after_approval=true.",
                })
            continue

        if decision not in ALLOWED_DECISIONS:
            findings.append({
                "finding_id": "NID_ARB_UNKNOWN_HUMAN_DECISION",
                "severity": "blocking",
                "candidate_id": candidate_id,
                "human_decision": decision,
                "allowed": sorted(ALLOWED_DECISIONS | {PENDING_VALUE}),
            })
            continue

        completed_count += 1

        if not is_non_empty_rationale(rationale):
            findings.append({
                "finding_id": "NID_ARB_RATIONALE_MISSING",
                "severity": "blocking",
                "candidate_id": candidate_id,
                "human_decision": decision,
                "message": "Completed decisions require human_rationale that is not TODO.",
            })

        if not isinstance(patch_flag, bool):
            findings.append({
                "finding_id": "NID_ARB_PATCH_FLAG_NOT_BOOLEAN",
                "severity": "blocking",
                "candidate_id": candidate_id,
                "patch_policy_decisions_after_approval": patch_flag,
            })

        if decision != "add_as_default_neighbor" and patch_flag is True:
            findings.append({
                "finding_id": "NID_ARB_PATCH_FLAG_INVALID_FOR_DECISION",
                "severity": "blocking",
                "candidate_id": candidate_id,
                "human_decision": decision,
                "message": "Only add_as_default_neighbor may set patch_policy_decisions_after_approval=true.",
            })

        if decision == "add_as_default_neighbor" and patch_flag is True:
            patch_ready_count += 1

    duplicate_ids = sorted([candidate_id for candidate_id, count in Counter(candidate_ids).items() if count > 1])
    if duplicate_ids:
        findings.append({
            "finding_id": "NID_ARB_DUPLICATE_CANDIDATE_ID",
            "severity": "blocking",
            "duplicates": duplicate_ids,
        })

    if pending_count:
        warnings.append({
            "warning_id": "NID_ARB_PENDING_ITEMS_REMAIN",
            "severity": "informational",
            "pending_count": pending_count,
            "message": "Arbitration is structurally valid but not complete.",
        })

    if findings:
        status = "FAIL"
    elif pending_count:
        status = "PENDING_HUMAN_ARBITRATION"
    else:
        status = "PASS_READY_TO_PATCH"

    return {
        "constitution_neighbor_ids_arbitration_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": status,
            "source": str(arbitration_path).replace("\\", "/"),
            "allowed_decisions": sorted(ALLOWED_DECISIONS),
            "summary": {
                "item_count": len(items),
                "pending_count": pending_count,
                "completed_count": completed_count,
                "patch_ready_count": patch_ready_count,
                "counts_by_human_decision": dict(sorted(by_decision.items())),
                "counts_by_priority": dict(sorted(by_priority.items())),
                "counts_by_scope": dict(sorted(by_scope.items())),
            },
            "blocking_findings": findings,
            "warnings": warnings,
            "next_step": (
                "Complete human_decision, human_rationale and patch_policy_decisions_after_approval for every item."
                if status == "PENDING_HUMAN_ARBITRATION"
                else "Ready for deterministic decisions.yaml patch synthesis for patch-ready items."
                if status == "PASS_READY_TO_PATCH"
                else "Fix blocking findings before continuing."
            ),
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate PHASE_16B neighbor IDs arbitration.")
    parser.add_argument("--arbitration", default=str(DEFAULT_ARBITRATION))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate(Path(args.arbitration))
    write_yaml(Path(args.report), report)
    root = report["constitution_neighbor_ids_arbitration_validation"]
    print(f"Wrote {args.report}")
    print(f"Status: {root['status']}")
    print(f"Pending count: {root['summary']['pending_count']}")
    print(f"Patch-ready count: {root['summary']['patch_ready_count']}")

    # Structural FAIL is non-zero. Pending is a valid intermediate state.
    return 1 if root["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
