from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_io import load_yaml

GOVERNANCE_BACKLOG_PATH = Path("docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")


def empty_governance_backlog_signal() -> dict[str, Any]:
    return {
        "warning": "none",
        "direct_open_count": 0,
        "related_open_count": 0,
        "open_entry_ids": [],
        "open_types": {},
    }


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def build_governance_backlog_scope_summary(repo_root: Path) -> dict[str, dict[str, Any]]:
    backlog_path = repo_root / GOVERNANCE_BACKLOG_PATH
    if not backlog_path.exists():
        return {}

    root = load_yaml(backlog_path).get("governance_backlog", {})
    entries = root.get("entries", []) or []
    if not isinstance(entries, list):
        return {}

    summary: dict[str, dict[str, Any]] = {}

    def ensure(scope_key: str) -> dict[str, Any]:
        if scope_key not in summary:
            summary[scope_key] = empty_governance_backlog_signal()
        return summary[scope_key]

    for entry in entries:
        if entry.get("status") != "open":
            continue

        entry_id = str(entry.get("entry_id") or "")
        entry_type = str(entry.get("type") or "unknown")
        direct_scope = str(entry.get("scope_key") or "unknown")

        direct_bucket = ensure(direct_scope)
        direct_bucket["direct_open_count"] += 1
        if entry_id and entry_id not in direct_bucket["open_entry_ids"]:
            direct_bucket["open_entry_ids"].append(entry_id)
        direct_bucket["open_types"][entry_type] = direct_bucket["open_types"].get(entry_type, 0) + 1

        for related_scope in _as_string_list(entry.get("related_scope_keys")):
            if related_scope == direct_scope:
                continue
            related_bucket = ensure(related_scope)
            related_bucket["related_open_count"] += 1
            if entry_id and entry_id not in related_bucket["open_entry_ids"]:
                related_bucket["open_entry_ids"].append(entry_id)
            related_bucket["open_types"][entry_type] = related_bucket["open_types"].get(entry_type, 0) + 1

    for bucket in summary.values():
        bucket["open_entry_ids"] = sorted(bucket["open_entry_ids"])
        bucket["open_types"] = dict(sorted(bucket["open_types"].items()))
        total = bucket["direct_open_count"] + bucket["related_open_count"]
        bucket["warning"] = "open_governance_backlog_entries" if total else "none"

    return dict(sorted(summary.items()))


def attach_governance_backlog_signal(
    scope_record: dict[str, Any],
    backlog_summary: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    scope_key = str(scope_record.get("scope_key") or "")
    signal = backlog_summary.get(scope_key, empty_governance_backlog_signal())
    return {**scope_record, "governance_backlog_signal": signal}


def compact_governance_backlog_signal(signal: dict[str, Any]) -> str:
    if not signal or signal.get("warning") == "none":
        return "none"

    direct = int(signal.get("direct_open_count") or 0)
    related = int(signal.get("related_open_count") or 0)
    types = signal.get("open_types") or {}
    type_summary = ",".join(f"{k}:{v}" for k, v in sorted(types.items())) if isinstance(types, dict) else "unknown"
    return f"open_entries direct={direct} related={related} types={type_summary}"

