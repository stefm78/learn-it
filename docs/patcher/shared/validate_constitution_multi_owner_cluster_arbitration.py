#!/usr/bin/env python3
"""Validate PHASE_19B multi-owner cluster arbitration surface."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEFAULT_ARBITRATION = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_arbitration.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_multi_owner_cluster_arbitration_validation.yaml")

ALLOWED_HUMAN_DECISIONS = {
    "keep_current_ownership_with_existing_governance",
    "keep_current_ownership_with_explicit_neighbors",
    "record_diagnostic_subcluster",
    "move_node_ownership",
    "split_scope",
    "merge_scope_fragments",
    "open_or_update_governance_backlog",
    "defer_to_governance_backlog",
    "wont_fix_with_rationale",
}


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def get_root(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}")
    return value


def validate(root: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    pending = []
    accepted = []
    patch_ready = []

    items = root.get("items")
    if not isinstance(items, list) or not items:
        findings.append({
            "finding_id": "NO_ARBITRATION_ITEMS",
            "severity": "error",
            "message": "Arbitration file contains no items.",
        })
        items = []

    seen = set()
    for item in items:
        cid = item.get("candidate_id")
        if not cid:
            findings.append({"finding_id": "MISSING_CANDIDATE_ID", "severity": "error", "message": "Item without candidate_id."})
            continue
        if cid in seen:
            findings.append({"finding_id": "DUPLICATE_CANDIDATE_ID", "severity": "error", "candidate_id": cid})
        seen.add(cid)

        human = item.get("human_arbitration")
        if not isinstance(human, dict):
            findings.append({"finding_id": "MISSING_HUMAN_ARBITRATION", "severity": "error", "candidate_id": cid})
            continue

        decision = human.get("decision")
        accepted_flag = human.get("accepted") is True
        requires_patch = human.get("requires_policy_decisions_patch")
        requires_catalog = human.get("requires_catalog_regeneration")
        rationale = str(human.get("rationale") or "")

        if decision == "pending" or not accepted_flag:
            pending.append(cid)
            continue

        if decision not in ALLOWED_HUMAN_DECISIONS:
            findings.append({
                "finding_id": "INVALID_HUMAN_DECISION",
                "severity": "error",
                "candidate_id": cid,
                "decision": decision,
            })

        if not isinstance(requires_patch, bool):
            findings.append({
                "finding_id": "PATCH_REQUIREMENT_NOT_BOOLEAN",
                "severity": "error",
                "candidate_id": cid,
            })

        if not isinstance(requires_catalog, bool):
            findings.append({
                "finding_id": "CATALOG_REQUIREMENT_NOT_BOOLEAN",
                "severity": "error",
                "candidate_id": cid,
            })

        if not rationale or rationale == "TO_BE_COMPLETED_BY_HUMAN_ARBITRATION":
            findings.append({
                "finding_id": "MISSING_HUMAN_RATIONALE",
                "severity": "error",
                "candidate_id": cid,
            })

        accepted.append(cid)
        if requires_patch is True:
            patch_ready.append(cid)

    severity_counts = Counter(f["severity"] for f in findings)
    if severity_counts.get("error", 0):
        status = "FAIL"
    elif pending:
        status = "PENDING_HUMAN_ARBITRATION"
    elif patch_ready:
        status = "PASS_READY_FOR_POLICY_DECISIONS_PATCH"
    else:
        status = "PASS_NO_PATCH_REQUIRED"

    return {
        "status": status,
        "pending_count": len(pending),
        "accepted_count": len(accepted),
        "patch_ready_count": len(patch_ready),
        "pending_candidate_ids": pending,
        "accepted_candidate_ids": accepted,
        "patch_ready_candidate_ids": patch_ready,
        "findings": findings,
        "error_count": severity_counts.get("error", 0),
        "warning_count": severity_counts.get("warning", 0),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate PHASE_19B multi-owner cluster arbitration.")
    parser.add_argument("--arbitration", default=str(DEFAULT_ARBITRATION))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    arbitration_path = Path(args.arbitration)
    report_path = Path(args.report)

    arbitration_doc = load_yaml(arbitration_path)
    root = get_root(arbitration_doc, "constitution_multi_owner_cluster_arbitration")
    result = validate(root)

    report = {
        "constitution_multi_owner_cluster_arbitration_validation": {
            "schema_version": "0.1",
            "phase_id": "PHASE_19B",
            "generated_at": iso_now(),
            "status": result["status"],
            "inputs": {
                "arbitration": normalize_path(arbitration_path),
                "arbitration_sha256": sha256_file(arbitration_path),
            },
            "summary": {
                "pending_count": result["pending_count"],
                "accepted_count": result["accepted_count"],
                "patch_ready_count": result["patch_ready_count"],
                "error_count": result["error_count"],
                "warning_count": result["warning_count"],
            },
            "pending_candidate_ids": result["pending_candidate_ids"],
            "accepted_candidate_ids": result["accepted_candidate_ids"],
            "patch_ready_candidate_ids": result["patch_ready_candidate_ids"],
            "findings": result["findings"],
            "next_step": (
                "complete_human_arbitration"
                if result["status"] == "PENDING_HUMAN_ARBITRATION"
                else "prepare_policy_decisions_patch"
                if result["status"] == "PASS_READY_FOR_POLICY_DECISIONS_PATCH"
                else "close_phase19b_no_patch_required"
                if result["status"] == "PASS_NO_PATCH_REQUIRED"
                else "fix_arbitration_file"
            ),
        }
    }

    write_yaml(report_path, report)
    print(f"Wrote {report_path}")
    print(f"Status: {result['status']}")
    print(f"Pending: {result['pending_count']}")
    print(f"Patch ready: {result['patch_ready_count']}")
    return 0 if result["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
