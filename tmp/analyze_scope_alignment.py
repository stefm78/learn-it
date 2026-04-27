#!/usr/bin/env python3
"""Analyze alignment between current scopes and graph clusters.

PHASE_06 — scope_alignment_review

Reads:
  - tmp/scope_lab/constitution_graph_nodes.yaml
  - tmp/scope_lab/cluster_closure_report.yaml

Writes:
  - tmp/scope_lab/scope_alignment_report.yaml

Purpose:
  Compare current canonical scope ownership with discovered graph clusters.

This script is diagnostic only.
It does not modify canonical cores, policies, decisions, or scope catalog.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )


def load_inputs(
    nodes_path: Path,
    closure_path: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    nodes_doc = load_yaml(nodes_path)
    closure_doc = load_yaml(closure_path)

    nodes = nodes_doc.get("constitution_graph_nodes", {}).get("nodes", []) or []
    clusters = closure_doc.get("cluster_closure_report", {}).get("clusters", []) or []

    node_by_id = {
        node["id"]: node
        for node in nodes
        if isinstance(node, dict) and node.get("id")
    }

    return node_by_id, clusters


def collect_scope_nodes(node_by_id: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    by_scope: dict[str, list[str]] = defaultdict(list)

    for node_id, node in node_by_id.items():
        scope = node.get("current_owner_scope")
        if isinstance(scope, str) and scope:
            by_scope[scope].append(node_id)

    return {
        scope: sorted(ids)
        for scope, ids in sorted(by_scope.items())
    }


def build_cluster_index(clusters: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for cluster in clusters:
        for node_id in cluster.get("node_ids", []) or []:
            index[node_id].append(cluster)

    return index


def cluster_scope_view(
    scope: str,
    owned_node_ids: list[str],
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    owned_set = set(owned_node_ids)
    views: list[dict[str, Any]] = []

    for cluster in clusters:
        node_ids = cluster.get("node_ids", []) or []
        owned_in_cluster = sorted(node_id for node_id in node_ids if node_id in owned_set)

        if not owned_in_cluster:
            continue

        cluster_node_count = int(cluster.get("node_count") or len(node_ids) or 0)
        owned_count = len(owned_in_cluster)

        views.append(
            {
                "cluster_id": cluster.get("cluster_id"),
                "method": cluster.get("method"),
                "cluster_node_count": cluster_node_count,
                "scope_owned_node_count_in_cluster": owned_count,
                "scope_owned_ratio_in_cluster": round(owned_count / cluster_node_count, 4)
                if cluster_node_count
                else 0,
                "owner_status": cluster.get("owner_status"),
                "boundary_pressure": cluster.get("boundary_pressure"),
                "recommendation": cluster.get("recommendation"),
                "candidate_neighbor_scopes": cluster.get("candidate_neighbor_scopes", []) or [],
                "nodes_by_owner_scope": cluster.get("nodes_by_owner_scope", {}) or {},
                "owned_node_ids": owned_in_cluster,
            }
        )

    return sorted(
        views,
        key=lambda item: (
            -item["scope_owned_node_count_in_cluster"],
            item["cluster_id"] or "",
        ),
    )


def assess_scope_alignment(
    scope: str,
    owned_node_ids: list[str],
    cluster_views: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    findings: list[str] = []

    if not owned_node_ids:
        return "empty_scope", ["No owned node found for this scope."]

    if not cluster_views:
        return "not_covered_by_selected_clusters", [
            "Owned nodes exist but are not covered by selected closure clusters."
        ]

    multi_owner = [
        item for item in cluster_views
        if item.get("owner_status") == "multi_owner_fragmented"
    ]
    high_boundary = [
        item for item in cluster_views
        if item.get("boundary_pressure") == "high"
    ]
    neighbor_review = [
        item for item in cluster_views
        if item.get("recommendation") == "declare_or_review_neighbors"
    ]
    unowned_mix = [
        item for item in cluster_views
        if item.get("owner_status") == "single_owner_plus_unowned"
    ]

    if multi_owner:
        findings.append(
            f"{len(multi_owner)} cluster(s) mix this scope with other owned scopes."
        )

    if high_boundary:
        findings.append(
            f"{len(high_boundary)} cluster(s) have high boundary pressure."
        )

    if neighbor_review:
        findings.append(
            f"{len(neighbor_review)} cluster(s) suggest neighbor review."
        )

    if unowned_mix:
        findings.append(
            f"{len(unowned_mix)} cluster(s) mix owned nodes with currently UNOWNED nodes."
        )

    if len(cluster_views) >= 5:
        findings.append(
            f"Owned nodes are spread across {len(cluster_views)} selected clusters."
        )

    if multi_owner:
        return "split_merge_or_bridge_review", findings

    if high_boundary or neighbor_review:
        return "requires_neighbor_review", findings

    if unowned_mix:
        return "requires_unowned_classification", findings

    if len(cluster_views) >= 5:
        return "possibly_fragmented", findings

    return "stable_or_minor_review", findings or ["No major alignment issue detected."]


def build_scope_reports(
    scope_nodes: dict[str, list[str]],
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []

    for scope, owned_ids in scope_nodes.items():
        views = cluster_scope_view(scope, owned_ids, clusters)
        alignment_status, findings = assess_scope_alignment(scope, owned_ids, views)

        reports.append(
            {
                "scope_key": scope,
                "alignment_status": alignment_status,
                "owned_node_count": len(owned_ids),
                "selected_cluster_touch_count": len(views),
                "findings": findings,
                "cluster_views": views,
            }
        )

    return sorted(reports, key=lambda item: item["scope_key"])


def summarize(scope_reports: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> dict[str, Any]:
    alignment_counts = Counter(item["alignment_status"] for item in scope_reports)
    recommendation_counts = Counter(cluster.get("recommendation") for cluster in clusters)
    owner_status_counts = Counter(cluster.get("owner_status") for cluster in clusters)
    boundary_counts = Counter(cluster.get("boundary_pressure") for cluster in clusters)

    return {
        "scope_count": len(scope_reports),
        "selected_cluster_count": len(clusters),
        "alignment_status_counts": dict(sorted(alignment_counts.items())),
        "cluster_recommendation_counts": dict(sorted(recommendation_counts.items())),
        "cluster_owner_status_counts": dict(sorted(owner_status_counts.items())),
        "cluster_boundary_pressure_counts": dict(sorted(boundary_counts.items())),
    }


def build_report(
    node_by_id: dict[str, dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> dict[str, Any]:
    scope_nodes = collect_scope_nodes(node_by_id)
    scope_reports = build_scope_reports(scope_nodes, clusters)
    summary = summarize(scope_reports, clusters)

    global_findings: list[str] = []

    if summary["alignment_status_counts"].get("split_merge_or_bridge_review", 0):
        global_findings.append(
            "At least one scope has multi-owner graph clusters and requires split/merge/bridge review."
        )

    if summary["cluster_owner_status_counts"].get("fully_unowned", 0):
        global_findings.append(
            "Some clusters are fully UNOWNED; referentiel/link ownership or classification must be addressed."
        )

    if summary["cluster_recommendation_counts"].get("classify_unowned_core_area", 0):
        global_findings.append(
            "Unowned core areas must be classified before a full bijection gate can pass."
        )

    if not global_findings:
        global_findings.append("No global blocking alignment signal detected.")

    return {
        "scope_alignment_report": {
            "schema_version": 0.1,
            "status": "PASS",
            "summary": summary,
            "global_findings": global_findings,
            "scope_reports": scope_reports,
            "notes": [
                "This report compares current ownership with graph clusters.",
                "It does not decide new scopes.",
                "PHASE_07 should convert these findings into explicit redesign candidates.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze scope alignment against graph clusters.")
    parser.add_argument("--nodes", default="tmp/scope_lab/constitution_graph_nodes.yaml")
    parser.add_argument("--closure", default="tmp/scope_lab/cluster_closure_report.yaml")
    parser.add_argument("--out", default="tmp/scope_lab/scope_alignment_report.yaml")
    args = parser.parse_args()

    node_by_id, clusters = load_inputs(
        nodes_path=Path(args.nodes),
        closure_path=Path(args.closure),
    )

    report = build_report(node_by_id=node_by_id, clusters=clusters)

    Path(args.out).write_text(dump_yaml(report), encoding="utf-8")

    print(json.dumps(report["scope_alignment_report"]["summary"], indent=2, ensure_ascii=False))
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
