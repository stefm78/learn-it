#!/usr/bin/env python3
"""Analyze constitution scope partition readiness deterministically.

This script is the mandatory deterministic base for Stage 00
(SCOPE_PARTITION_REVIEW_AND_REGEN).

It does not publish a new partition. It only:
- blocks if any constitution run is active
- analyzes the current constitution core
- reports current generated scopes
- reports logic.scope distribution and cross-group couplings
- provides stable candidate partition signals for human + AI review
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run this script.") from exc


ENTRY_SECTIONS = ["TYPES", "INVARIANTS", "RULES", "PARAMETERS", "CONSTRAINTS", "EVENTS", "ACTIONS"]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML object must be a mapping: {path}")
    return data


ndef dump_yaml(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_target_id(raw: Any) -> str | None:
    if isinstance(raw, str):
        return raw.split("::", 1)[0]
    if isinstance(raw, dict):
        value = raw.get("id")
        if isinstance(value, str):
            return value.split("::", 1)[0]
    return None


def iter_refs(entry: Dict[str, Any]) -> Iterable[str]:
    for dep in entry.get("depends_on", []) or []:
        if isinstance(dep, str):
            yield dep.split("::", 1)[0]
    for rel in entry.get("relations", []) or []:
        target_id = normalize_target_id(rel.get("target"))
        if target_id:
            yield target_id


def collect_entries(core: Dict[str, Any]) -> List[Dict[str, Any]]:
    core_root = core.get("CORE", {})
    entries: List[Dict[str, Any]] = []
    for section in ENTRY_SECTIONS:
        for raw in core_root.get(section, []) or []:
            if not isinstance(raw, dict) or "id" not in raw:
                continue
            logic = raw.get("logic") or {}
            entries.append(
                {
                    "id": raw["id"],
                    "section": section,
                    "logic_scope": logic.get("scope", "unknown"),
                    "refs": list(iter_refs(raw)),
                }
            )
    return entries


def active_runs(runs_index: Dict[str, Any]) -> List[Dict[str, Any]]:
    root = runs_index.get("runs_index", {})
    active = root.get("active_runs", []) or []
    return [r for r in active if r.get("run_status") == "active"]


def current_scope_catalog(catalog: Dict[str, Any]) -> List[Dict[str, Any]]:
    return catalog.get("scope_catalog", {}).get("published_scopes", []) or []


def build_partition_metrics(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_logic_scope: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_id: Dict[str, Dict[str, Any]] = {}
    for entry in entries:
        by_logic_scope[entry["logic_scope"]].append(entry)
        by_id[entry["id"]] = entry

    logic_scope_counts = []
    for scope_name in sorted(by_logic_scope):
        scope_entries = by_logic_scope[scope_name]
        section_counts = Counter(e["section"] for e in scope_entries)
        logic_scope_counts.append(
            {
                "logic_scope": scope_name,
                "entry_count": len(scope_entries),
                "section_distribution": dict(sorted(section_counts.items())),
            }
        )

    cross_scope_edges: Dict[Tuple[str, str], int] = defaultdict(int)
    internal_scope_edges: Dict[str, int] = defaultdict(int)
    for entry in entries:
        src_scope = entry["logic_scope"]
        for ref in entry["refs"]:
            target = by_id.get(ref)
            if not target:
                continue
            dst_scope = target["logic_scope"]
            if src_scope == dst_scope:
                internal_scope_edges[src_scope] += 1
            else:
                cross_scope_edges[(src_scope, dst_scope)] += 1

    cross_scope_list = [
        {"from": src, "to": dst, "edge_count": count}
        for (src, dst), count in sorted(cross_scope_edges.items(), key=lambda x: (-x[1], x[0][0], x[0][1]))
    ]

    candidate_partition_units = []
    for scope_name in sorted(by_logic_scope):
        total = len(by_logic_scope[scope_name])
        internal = internal_scope_edges.get(scope_name, 0)
        outgoing = sum(v for (src, _), v in cross_scope_edges.items() if src == scope_name)
        incoming = sum(v for (_, dst), v in cross_scope_edges.items() if dst == scope_name)
        candidate_partition_units.append(
            {
                "logic_scope": scope_name,
                "entry_count": total,
                "internal_edge_count": internal,
                "cross_scope_outgoing_edge_count": outgoing,
                "cross_scope_incoming_edge_count": incoming,
            }
        )

    return {
        "total_entry_count": len(entries),
        "logic_scope_count": len(by_logic_scope),
        "logic_scope_distribution": logic_scope_counts,
        "cross_scope_edges": cross_scope_list,
        "candidate_partition_units": candidate_partition_units,
    }


def recommend_direction(metrics: Dict[str, Any], current_scope_count: int) -> str:
    logic_scope_count = metrics["logic_scope_count"]
    total_entry_count = metrics["total_entry_count"]
    if total_entry_count <= 40:
        return "keep_or_reduce"
    if logic_scope_count > current_scope_count:
        return "increase"
    if logic_scope_count < max(1, current_scope_count - 1):
        return "decrease_or_merge"
    return "keep_or_review_semantics"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze constitution scope partition deterministically.")
    parser.add_argument("--runs-index", default="docs/pipelines/constitution/runs/index.yaml")
    parser.add_argument("--constitution", default="docs/cores/current/constitution.yaml")
    parser.add_argument("--scope-catalog", default="docs/pipelines/constitution/scope_catalog/manifest.yaml")
    parser.add_argument("--scope-policy", default="docs/pipelines/constitution/policies/scope_generation/policy.yaml")
    parser.add_argument("--scope-decisions", default="docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
    parser.add_argument("--report", default="tmp/constitution_scope_partition_review_report.yaml")
    args = parser.parse_args()

    repo_root = Path.cwd()
    runs_index = load_yaml(repo_root / args.runs_index)
    active = active_runs(runs_index)
    core = load_yaml(repo_root / args.constitution)
    catalog = load_yaml(repo_root / args.scope_catalog)
    policy = load_yaml(repo_root / args.scope_policy)
    decisions = load_yaml(repo_root / args.scope_decisions)

    constitution_text = (repo_root / args.constitution).read_text(encoding="utf-8")
    source_fingerprint = sha256_text(constitution_text)

    published_scopes = current_scope_catalog(catalog)
    current_scope_count = len(published_scopes)

    if active:
        report = {
            "scope_partition_review_report": {
                "schema_version": 0.1,
                "pipeline_id": "constitution",
                "status": "BLOCKED_ACTIVE_RUNS_PRESENT",
                "source_fingerprint": source_fingerprint,
                "active_run_count": len(active),
                "active_runs": active,
                "current_published_scope_count": current_scope_count,
                "current_published_scope_keys": [s.get("scope_key") for s in published_scopes],
                "notes": [
                    "Stage 00 est interdit tant qu'un run actif existe.",
                    "La partition doit rester figée pendant la vie d'un run.",
                ],
            }
        }
    else:
        entries = collect_entries(core)
        metrics = build_partition_metrics(entries)
        policy_root = policy.get("scope_generation_policy", {})
        decisions_root = decisions.get("scope_generation_decisions", {})
        report = {
            "scope_partition_review_report": {
                "schema_version": 0.1,
                "pipeline_id": "constitution",
                "status": "READY_FOR_SEMANTIC_REVIEW",
                "source_fingerprint": source_fingerprint,
                "current_published_scope_count": current_scope_count,
                "current_published_scope_keys": [s.get("scope_key") for s in published_scopes],
                "current_policy_id": policy_root.get("policy_id"),
                "current_decisionset_id": decisions_root.get("decisionset_id"),
                "partition_signals": metrics,
                "recommended_scope_count_direction": recommend_direction(metrics, current_scope_count),
                "notes": [
                    "Le rapport déterministe n'édite pas la partition publiée.",
                    "Il sert de base à l'analyse sémantique assistée par IA et à l'arbitrage humain.",
                ],
            }
        }

    report_path = repo_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(dump_yaml(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
