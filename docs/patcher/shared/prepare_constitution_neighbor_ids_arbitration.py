#!/usr/bin/env python3
"""Prepare PHASE_16B human arbitration draft for Constitution neighbor IDs.

Generic non-mutating helper for STAGE_00 neighbor IDs governance.

Default input:
  docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml

Default outputs:
  docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml
  docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.md
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml

DEFAULT_SOURCE_REPORT = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml")
DEFAULT_ARBITRATION_YAML = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml")
DEFAULT_ARBITRATION_MD = Path("docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.md")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    if not isinstance(doc, dict):
        raise SystemExit(f"Invalid YAML root: {path}")
    return doc


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def priority_from_severity(severity: str) -> str:
    return {
        "fail": "P1_blocking_scoring_delta",
        "warn": "P2_non_blocking_scoring_delta",
        "none": "P3_dependency_explicitness_hygiene",
    }.get(severity, "P3_dependency_explicitness_hygiene")


def build_arbitration(source: Dict[str, Any], source_report_path: Path) -> Dict[str, Any]:
    root = source.get("constitution_neighbor_ids_governance_report")
    if not isinstance(root, dict):
        raise SystemExit(f"Missing constitution_neighbor_ids_governance_report root in {source_report_path}")

    if root.get("status") != "READY_FOR_HUMAN_ARBITRATION":
        raise SystemExit(f"Source report is not ready for arbitration: {root.get('status')}")

    consistency = root.get("policy_scoring_scope_consistency", {})
    if consistency.get("status") != "PASS":
        raise SystemExit("Policy/scoring scope consistency is not PASS. Resolve source alignment before human arbitration.")

    items: List[Dict[str, Any]] = []
    by_priority: Counter[str] = Counter()
    by_scope: Counter[str] = Counter()

    for candidate in root.get("decision_candidates", []) or []:
        if not isinstance(candidate, dict):
            continue

        severity = candidate.get("source_signal", {}).get("scope_delta_severity", "none")
        priority = priority_from_severity(str(severity))
        by_priority[priority] += 1
        by_scope[str(candidate.get("scope_key"))] += 1

        items.append({
            "candidate_id": candidate.get("candidate_id"),
            "scope_key": candidate.get("scope_key"),
            "uncovered_id": candidate.get("uncovered_id"),
            "owner_scope_key": candidate.get("owner_scope_key"),
            "owner_decision_id": candidate.get("owner_decision_id"),
            "priority": priority,
            "source_signal": candidate.get("source_signal", {}),
            "recommended_decision": candidate.get("recommended_decision"),
            "human_decision": "pending",
            "allowed_human_decisions": [
                "add_as_default_neighbor",
                "defer_to_governance_backlog",
                "wont_fix_with_rationale",
            ],
            "human_rationale": "TODO",
            "patch_policy_decisions_after_approval": False,
            "rationale_from_report": candidate.get("rationale"),
        })

    items.sort(key=lambda x: (x["priority"], str(x["scope_key"]), str(x["uncovered_id"])))

    return {
        "constitution_neighbor_ids_arbitration": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "phase": "PHASE_16B",
            "status": "PENDING_HUMAN_ARBITRATION",
            "source_report": str(source_report_path).replace("\\", "/"),
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "governance_backlog_yaml": "not_modified",
                "scope_catalog": "not_modified",
                "maturity_scores": "not_modified",
                "scorer_v1_1_rules": "not_modified",
            },
            "arbitration_policy": {
                "allowed_human_decisions": [
                    "add_as_default_neighbor",
                    "defer_to_governance_backlog",
                    "wont_fix_with_rationale",
                ],
                "completion_rule": "Every item must have human_decision != pending and human_rationale != TODO.",
                "post_arbitration_rule": (
                    "Only candidates with human_decision=add_as_default_neighbor and "
                    "patch_policy_decisions_after_approval=true may be patched into decisions.yaml."
                ),
            },
            "summary": {
                "candidate_count": len(items),
                "candidate_counts_by_priority": dict(sorted(by_priority.items())),
                "candidate_counts_by_scope": dict(sorted(by_scope.items())),
            },
            "items": items,
        }
    }


def render_md(arbitration: Dict[str, Any]) -> str:
    root = arbitration["constitution_neighbor_ids_arbitration"]
    items = root["items"]

    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item["priority"]].append(item)

    lines: List[str] = [
        "# PHASE_16B — Constitution neighbor IDs human arbitration",
        "",
        "Status: `PENDING_HUMAN_ARBITRATION`",
        "",
        "This document is a human arbitration surface. It does not modify `policy.yaml`, `decisions.yaml`, the scope catalog, governance backlog, maturity scores, or scorer rules.",
        "",
        "## Decision values",
        "",
        "- `add_as_default_neighbor`: accept adding the ID as an explicit Constitution read neighbor for the scope.",
        "- `defer_to_governance_backlog`: do not patch now; route the candidate to backlog or a later STAGE_00/content review.",
        "- `wont_fix_with_rationale`: explicitly reject the neighbor declaration with a rationale.",
        "",
        "## Summary",
        "",
        "```yaml",
        yaml.safe_dump(root["summary"], allow_unicode=True, sort_keys=False).rstrip(),
        "```",
        "",
    ]

    priority_titles = {
        "P1_blocking_scoring_delta": "P1 — blocking scoring delta",
        "P2_non_blocking_scoring_delta": "P2 — non-blocking scoring delta",
        "P3_dependency_explicitness_hygiene": "P3 — dependency explicitness hygiene",
    }

    for priority in ["P1_blocking_scoring_delta", "P2_non_blocking_scoring_delta", "P3_dependency_explicitness_hygiene"]:
        group = grouped.get(priority, [])
        if not group:
            continue
        lines.append(f"## {priority_titles.get(priority, priority)}")
        lines.append("")
        for item in group:
            lines.extend([
                f"### {item['candidate_id']}",
                "",
                f"- Scope: `{item['scope_key']}`",
                f"- Uncovered ID: `{item['uncovered_id']}`",
                f"- Owner scope: `{item['owner_scope_key']}` via `{item['owner_decision_id']}`",
                f"- Recommended decision: `{item['recommended_decision']}`",
                f"- Human decision: `{item['human_decision']}`",
                f"- Human rationale: {item['human_rationale']}",
                "",
                "Source signal:",
                "",
                "```yaml",
                yaml.safe_dump(item["source_signal"], allow_unicode=True, sort_keys=False).rstrip(),
                "```",
                "",
                f"Report rationale: {item['rationale_from_report']}",
                "",
            ])

    lines.extend([
        "## How to complete",
        "",
        "Edit the arbitration YAML file.",
        "",
        "For every item:",
        "",
        "```yaml",
        "human_decision: add_as_default_neighbor | defer_to_governance_backlog | wont_fix_with_rationale",
        "human_rationale: <non-empty rationale>",
        "patch_policy_decisions_after_approval: true | false",
        "```",
        "",
        "Do not patch `policy.yaml` or `decisions.yaml` until the arbitration file is complete and validated.",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare Constitution neighbor IDs arbitration artifacts.")
    parser.add_argument("--source-report", default=str(DEFAULT_SOURCE_REPORT))
    parser.add_argument("--arbitration-yaml", default=str(DEFAULT_ARBITRATION_YAML))
    parser.add_argument("--arbitration-md", default=str(DEFAULT_ARBITRATION_MD))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_report = Path(args.source_report)
    arbitration_yaml = Path(args.arbitration_yaml)
    arbitration_md = Path(args.arbitration_md)

    if not source_report.exists():
        raise SystemExit(f"Missing source report: {source_report}")

    source = load_yaml(source_report)
    arbitration = build_arbitration(source, source_report)

    write_yaml(arbitration_yaml, arbitration)
    arbitration_md.parent.mkdir(parents=True, exist_ok=True)
    arbitration_md.write_text(render_md(arbitration), encoding="utf-8")

    root = arbitration["constitution_neighbor_ids_arbitration"]
    print(f"Wrote {arbitration_yaml}")
    print(f"Wrote {arbitration_md}")
    print(f"Status: {root['status']}")
    print(f"Candidate count: {root['summary']['candidate_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
