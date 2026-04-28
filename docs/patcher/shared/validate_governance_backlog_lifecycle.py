#!/usr/bin/env python3
# Validate Constitution governance backlog lifecycle constraints.
#
# Read-only validator.
#
# Default input:
#   docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
#
# Default output:
#   docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEFAULT_BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml")

ALLOWED_STATUSES = {"open", "addressed", "wont_fix"}
FORBIDDEN_PSEUDO_STATUSES = {"deferred", "reported", "report_decided", "reporté", "postponed"}
REQUIRED_RESOLUTION_FIELDS = ["resolved_at", "resolved_by", "resolution_note"]
OPEN_REVIEW_FIELDS = ["last_reviewed_at", "last_reviewed_by", "review_note", "next_review_trigger"]


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


def has_non_empty(entry: Dict[str, Any], field: str) -> bool:
    return field in entry and entry[field] not in (None, "")


def validate(backlog_path: Path) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    doc = load_yaml(backlog_path)
    root = doc.get("governance_backlog")
    if not isinstance(root, dict):
        findings.append({
            "finding_id": "GBLIFE_ROOT_MISSING",
            "severity": "blocking",
            "message": "Missing governance_backlog mapping root.",
        })
        entries: List[Dict[str, Any]] = []
        declared_statuses = {}
        declared_types = {}
    else:
        entries_raw = root.get("entries", [])
        entries = entries_raw if isinstance(entries_raw, list) else []
        if not isinstance(entries_raw, list):
            findings.append({
                "finding_id": "GBLIFE_ENTRIES_NOT_LIST",
                "severity": "blocking",
                "message": "governance_backlog.entries must be a list.",
            })
        declared_statuses = root.get("statuses", {}) if isinstance(root.get("statuses", {}), dict) else {}
        declared_types = root.get("entry_types", {}) if isinstance(root.get("entry_types", {}), dict) else {}

    declared_status_keys = set(str(k) for k in declared_statuses.keys())
    if declared_status_keys and declared_status_keys != ALLOWED_STATUSES:
        findings.append({
            "finding_id": "GBLIFE_STATUS_DECLARATION_MISMATCH",
            "severity": "blocking",
            "message": "governance_backlog.statuses must declare exactly open/addressed/wont_fix.",
            "declared": sorted(declared_status_keys),
            "expected": sorted(ALLOWED_STATUSES),
        })

    entry_ids = [str(e.get("entry_id", "")) for e in entries if isinstance(e, dict)]
    duplicates = sorted([entry_id for entry_id, count in Counter(entry_ids).items() if entry_id and count > 1])
    if duplicates:
        findings.append({
            "finding_id": "GBLIFE_DUPLICATE_ENTRY_ID",
            "severity": "blocking",
            "duplicates": duplicates,
        })

    status_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()

    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append({
                "finding_id": "GBLIFE_ENTRY_NOT_MAPPING",
                "severity": "blocking",
                "entry_index": idx,
            })
            continue

        entry_id = str(entry.get("entry_id") or f"<missing:{idx}>")
        status = str(entry.get("status") or "")
        entry_type = str(entry.get("type") or "")
        status_counts[status or "missing"] += 1
        type_counts[entry_type or "missing"] += 1

        if not entry.get("entry_id"):
            findings.append({
                "finding_id": "GBLIFE_ENTRY_ID_MISSING",
                "severity": "blocking",
                "entry_index": idx,
            })

        if status in FORBIDDEN_PSEUDO_STATUSES:
            findings.append({
                "finding_id": "GBLIFE_FORBIDDEN_PSEUDO_STATUS",
                "severity": "blocking",
                "entry_id": entry_id,
                "status": status,
                "message": "Deferred/reported is not a status; keep status=open with review metadata.",
            })
        elif status not in ALLOWED_STATUSES:
            findings.append({
                "finding_id": "GBLIFE_UNKNOWN_STATUS",
                "severity": "blocking",
                "entry_id": entry_id,
                "status": status,
                "allowed": sorted(ALLOWED_STATUSES),
            })

        if declared_types and entry_type not in declared_types:
            findings.append({
                "finding_id": "GBLIFE_UNKNOWN_ENTRY_TYPE",
                "severity": "blocking",
                "entry_id": entry_id,
                "type": entry_type,
                "allowed": sorted(str(k) for k in declared_types.keys()),
            })

        if status in {"addressed", "wont_fix"}:
            missing = [field for field in REQUIRED_RESOLUTION_FIELDS if not has_non_empty(entry, field)]
            if missing:
                findings.append({
                    "finding_id": "GBLIFE_RESOLUTION_METADATA_MISSING",
                    "severity": "blocking",
                    "entry_id": entry_id,
                    "status": status,
                    "missing_fields": missing,
                })

        if status == "open":
            present_review_fields = [field for field in OPEN_REVIEW_FIELDS if has_non_empty(entry, field)]
            if present_review_fields and len(present_review_fields) != len(OPEN_REVIEW_FIELDS):
                findings.append({
                    "finding_id": "GBLIFE_OPEN_REVIEW_METADATA_PARTIAL",
                    "severity": "blocking",
                    "entry_id": entry_id,
                    "present_fields": present_review_fields,
                    "required_group": OPEN_REVIEW_FIELDS,
                    "message": "Open deferral review metadata must be atomic if present.",
                })

    if status_counts.get("open", 0) > 0:
        warnings.append({
            "warning_id": "GBLIFE_OPEN_ENTRIES_PRESENT",
            "severity": "informational",
            "message": "Open entries remain active and must continue to surface in STAGE_00 and launcher warnings.",
            "open_count": status_counts.get("open", 0),
        })

    status = "PASS" if not findings else "FAIL"
    return {
        "governance_backlog_lifecycle_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": status,
            "source": str(backlog_path).replace("\\", "/"),
            "allowed_statuses": sorted(ALLOWED_STATUSES),
            "forbidden_pseudo_statuses": sorted(FORBIDDEN_PSEUDO_STATUSES),
            "entry_count": len(entries),
            "status_counts": dict(sorted(status_counts.items())),
            "type_counts": dict(sorted(type_counts.items())),
            "blocking_findings": findings,
            "warnings": warnings,
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate governance backlog lifecycle constraints.")
    parser.add_argument("--backlog", default=str(DEFAULT_BACKLOG))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate(Path(args.backlog))
    write_yaml(Path(args.report), report)
    status = report["governance_backlog_lifecycle_validation"]["status"]
    print(f"Wrote {args.report}")
    print(f"Status: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
