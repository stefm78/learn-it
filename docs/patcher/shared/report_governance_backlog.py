#!/usr/bin/env python3
"""Generate a deterministic report for Constitution governance backlog entries.

Read-only with regard to the backlog itself. This script does not modify:
- governance_backlog.yaml
- policy.yaml
- decisions.yaml
- generated scope catalog
- maturity scoring artifacts

Default output:
  docs/pipelines/constitution/reports/governance_backlog_report.yaml
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml

DEFAULT_BACKLOG = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/governance_backlog_report.yaml")

STAGE00_REVIEW_TYPES = {
    "scope_gap",
    "scope_extension_needed",
    "orphan_id",
    "policy_conflict",
    "partition_angle_mort",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    if not isinstance(doc, dict):
        raise SystemExit(f"Invalid YAML document at {path}: root must be a mapping")
    return doc


def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def parse_recorded_at(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    try:
        if raw.endswith("Z"):
            return datetime.fromisoformat(raw[:-1] + "+00:00")
        parsed = datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None


def age_days(recorded_at: Any, now: datetime) -> Optional[int]:
    parsed = parse_recorded_at(recorded_at)
    if parsed is None:
        return None
    return max(0, (now - parsed).days)


def as_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def selected_entries(entries: Iterable[Dict[str, Any]], status_filter: str, scope_key: Optional[str]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for entry in entries:
        if status_filter != "all" and entry.get("status") != status_filter:
            continue
        if scope_key:
            related = set(as_list(entry.get("related_scope_keys")))
            direct = entry.get("scope_key")
            if direct != scope_key and scope_key not in related:
                continue
        result.append(entry)
    return result


def sorted_counter(counter: Counter) -> Dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def classify_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    entry_type = str(entry.get("type") or "unknown")
    related = as_list(entry.get("related_scope_keys"))
    scope_key = str(entry.get("scope_key") or "unknown")
    return {
        "entry_id": entry.get("entry_id"),
        "candidate_id": entry.get("candidate_id"),
        "status": entry.get("status"),
        "type": entry_type,
        "scope_key": scope_key,
        "related_scope_keys": related,
        "source_run_id": entry.get("source_run_id"),
        "source_stage": entry.get("source_stage"),
        "source_finding_id": entry.get("source_finding_id"),
        "candidate_status": entry.get("candidate_status"),
        "title": entry.get("title"),
        "recommended_action": entry.get("recommended_action"),
        "stage00_relevant": entry_type in STAGE00_REVIEW_TYPES,
        "source_arbitrage_path": entry.get("source_arbitrage_path"),
        "recorded_at": entry.get("recorded_at"),
    }


def build_launcher_scope_summary(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_scope: Dict[str, Dict[str, Any]] = {}

    def ensure(scope: str) -> Dict[str, Any]:
        if scope not in by_scope:
            by_scope[scope] = {
                "direct_open_count": 0,
                "related_open_count": 0,
                "open_entry_ids": [],
                "open_types": {},
                "warning": "none",
            }
        return by_scope[scope]

    for entry in entries:
        if entry.get("status") != "open":
            continue
        entry_id = str(entry.get("entry_id"))
        entry_type = str(entry.get("type") or "unknown")
        direct_scope = str(entry.get("scope_key") or "unknown")
        direct_bucket = ensure(direct_scope)
        direct_bucket["direct_open_count"] += 1
        direct_bucket["open_entry_ids"].append(entry_id)
        direct_bucket["open_types"][entry_type] = direct_bucket["open_types"].get(entry_type, 0) + 1

        for related_scope in as_list(entry.get("related_scope_keys")):
            related_bucket = ensure(related_scope)
            related_bucket["related_open_count"] += 1
            if entry_id not in related_bucket["open_entry_ids"]:
                related_bucket["open_entry_ids"].append(entry_id)
            related_bucket["open_types"][entry_type] = related_bucket["open_types"].get(entry_type, 0) + 1

    for _, bucket in by_scope.items():
        total = bucket["direct_open_count"] + bucket["related_open_count"]
        bucket["open_entry_ids"] = sorted(bucket["open_entry_ids"])
        bucket["open_types"] = dict(sorted(bucket["open_types"].items()))
        bucket["warning"] = "open_governance_backlog_entries" if total > 0 else "none"

    return dict(sorted(by_scope.items()))


def build_report(backlog_path: Path, status_filter: str, scope_key: Optional[str]) -> Dict[str, Any]:
    now = utc_now()
    doc = load_yaml(backlog_path)
    root = doc.get("governance_backlog")
    if not isinstance(root, dict):
        raise SystemExit(f"Missing governance_backlog root in {backlog_path}")

    entries = root.get("entries", [])
    if not isinstance(entries, list):
        raise SystemExit(f"governance_backlog.entries must be a list in {backlog_path}")

    selected = selected_entries(entries, status_filter=status_filter, scope_key=scope_key)

    counts_status = Counter(str(e.get("status") or "unknown") for e in entries)
    counts_type = Counter(str(e.get("type") or "unknown") for e in selected)
    counts_scope = Counter(str(e.get("scope_key") or "unknown") for e in selected)
    counts_source_run = Counter(str(e.get("source_run_id") or "unknown") for e in selected)
    counts_candidate_status = Counter(str(e.get("candidate_status") or "unknown") for e in selected)

    counts_related_scope = Counter()
    for entry in selected:
        for related_scope in as_list(entry.get("related_scope_keys")):
            counts_related_scope[related_scope] += 1

    classified_entries = []
    for entry in selected:
        classified = classify_entry(entry)
        classified["age_days"] = age_days(entry.get("recorded_at"), now)
        classified_entries.append(classified)

    classified_entries.sort(
        key=lambda e: (
            str(e.get("scope_key") or ""),
            str(e.get("type") or ""),
            str(e.get("entry_id") or ""),
        )
    )

    open_entries = [e for e in entries if e.get("status") == "open"]
    launcher_summary = build_launcher_scope_summary(open_entries)

    return {
        "governance_backlog_report": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS",
            "source": {
                "backlog_path": str(backlog_path).replace("\\", "/"),
                "backlog_schema_version": root.get("schema_version"),
            },
            "filters": {
                "status": status_filter,
                "scope_key": scope_key,
            },
            "summary": {
                "total_entries": len(entries),
                "selected_entries": len(selected),
                "open_entries": len(open_entries),
                "counts_by_status_all_entries": sorted_counter(counts_status),
                "selected_counts_by_type": sorted_counter(counts_type),
                "selected_counts_by_scope_key": sorted_counter(counts_scope),
                "selected_counts_by_related_scope_key": sorted_counter(counts_related_scope),
                "selected_counts_by_source_run_id": sorted_counter(counts_source_run),
                "selected_counts_by_candidate_status": sorted_counter(counts_candidate_status),
            },
            "stage00_review": {
                "open_entries_requiring_review_count": sum(
                    1 for e in open_entries if str(e.get("type") or "") in STAGE00_REVIEW_TYPES
                ),
                "review_relevant_types": sorted(STAGE00_REVIEW_TYPES),
                "note": (
                    "This report classifies and summarizes backlog entries only. "
                    "It does not mark entries addressed/wont_fix and does not arbitrate scope changes."
                ),
            },
            "launcher_scope_summary": launcher_summary,
            "selected_entries_detail": classified_entries,
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report Constitution governance backlog entries.")
    parser.add_argument("--backlog", default=str(DEFAULT_BACKLOG), help=f"Default: {DEFAULT_BACKLOG}")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help=f"Default: {DEFAULT_REPORT}")
    parser.add_argument(
        "--status",
        default="open",
        choices=["open", "addressed", "wont_fix", "all"],
        help="Entry status filter. Default: open.",
    )
    parser.add_argument(
        "--scope-key",
        default=None,
        help="Optional scope filter. Matches direct scope_key or related_scope_keys.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(Path(args.backlog), status_filter=args.status, scope_key=args.scope_key)
    dump_yaml(Path(args.report), report)
    summary = report["governance_backlog_report"]["summary"]
    print(f"Wrote {args.report}")
    print(f"Status: {report['governance_backlog_report']['status']}")
    print(f"Selected entries: {summary['selected_entries']}")
    print(f"Open entries: {summary['open_entries']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
