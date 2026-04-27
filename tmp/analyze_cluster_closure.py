#!/usr/bin/env python3
"""Analyze cluster closure for Scope Lab graph clusters.

PHASE_05 — cluster_closure_analysis

Reads:
  - tmp/scope_lab/constitution_graph_nodes.yaml
  - tmp/scope_lab/constitution_graph_edges.yaml
  - tmp/scope_lab/constitution_graph_clusters.yaml

Writes:
  - tmp/scope_lab/cluster_closure_report.yaml

Purpose:
  For each relevant cluster, classify:
    - internal edges
    - outgoing neighbor edges
    - incoming neighbor edges
    - bridge edges
    - missing target edges
    - candidate neighbor needs
    - ownership fragmentation
    - boundary pressure

This script does not modify canonical sources.
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
    edges_path: Path,
    clusters_path: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    nodes_doc = load_yaml(nodes_path)
    edges_doc = load_yaml(edges_path)
    clusters_doc = load_yaml(clusters_path)

    nodes = nodes_doc.get("constitution_graph_nodes", {}).get("nodes", []) or []
    edges = edges_doc.get("constitution_graph_edges", {}).get("edges", []) or []
    clusters = clusters_doc.get("constitution_graph_clusters", {}).get("clusters", []) or []

    node_by_id = {
        node["id"]: node
        for node in nodes
        if isinstance(node, dict) and node.get("id")
    }

    return node_by_id, edges, clusters


def edge_key(edge: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": edge.get("source"),
        "target": edge.get("target"),
        "edge_type": edge.get("edge_type"),
        "source_scope": edge.get("source_scope"),
        "target_scope": edge.get("target_scope"),
    }


def pressure_level(internal: int, external: int) -> str:
    if external == 0:
        return "low"
    if internal == 0:
        return "high"
    ratio = external / internal
    if ratio >= 1:
        return "high"
    if ratio >= 0.35:
        return "medium"
    return "low"


def ownership_assessment(owner_counts: Counter[str]) -> str:
    if not owner_counts:
        return "unknown"

    non_unowned = {
        owner: count
        for owner, count in owner_counts.items()
        if owner != "UNOWNED"
    }

    if not non_unowned:
        return "fully_unowned"

    if len(non_unowned) == 1 and "UNOWNED" not in owner_counts:
        return "single_owner"

    if len(non_unowned) == 1 and "UNOWNED" in owner_counts:
        return "single_owner_plus_unowned"

    return "multi_owner_fragmented"


def recommendation_for_cluster(
    cluster: dict[str, Any],
    owner_status: str,
    boundary_pressure: str,
    outgoing_count: int,
    incoming_count: int,
) -> str:
    method = cluster.get("method")
    node_count = cluster.get("node_count", 0)

    if method == "weak_component" and node_count > 50:
        return "too_coarse_for_scope_decision"

    if owner_status == "single_owner" and boundary_pressure == "low":
        return "stable_scope_candidate"

    if owner_status in {"single_owner", "single_owner_plus_unowned"} and boundary_pressure in {"medium", "high"}:
        return "declare_or_review_neighbors"

    if owner_status == "multi_owner_fragmented":
        return "review_split_merge_or_bridge"

    if owner_status == "fully_unowned":
        return "classify_unowned_core_area"

    if outgoing_count or incoming_count:
        return "review_boundary"

    return "review"


def analyze_cluster(
    cluster: dict[str, Any],
    node_by_id: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    cluster_id = cluster.get("cluster_id")
    method = cluster.get("method")
    node_ids = cluster.get("node_ids", []) or []
    node_set = set(node_ids)

    internal_edges = []
    outgoing_edges = []
    incoming_edges = []
    missing_target_edges = []

    external_neighbor_ids: set[str] = set()
    external_neighbor_scopes: set[str] = set()
    inbound_source_ids: set[str] = set()
    inbound_source_scopes: set[str] = set()

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        source_in = source in node_set
        target_in = target in node_set

        if source_in and target_in:
            internal_edges.append(edge_key(edge))

        elif source_in and not target_in:
            if edge.get("classification") == "missing_target_edge":
                missing_target_edges.append(edge_key(edge))
            else:
                outgoing_edges.append(edge_key(edge))
                if isinstance(target, str):
                    external_neighbor_ids.add(target)
                target_scope = edge.get("target_scope")
                if isinstance(target_scope, str):
                    external_neighbor_scopes.add(target_scope)

        elif target_in and not source_in:
            incoming_edges.append(edge_key(edge))
            if isinstance(source, str):
                inbound_source_ids.add(source)
            source_scope = edge.get("source_scope")
            if isinstance(source_scope, str):
                inbound_source_scopes.add(source_scope)

    owner_counts = Counter(
        node_by_id[node_id].get("current_owner_scope") or "UNOWNED"
        for node_id in node_ids
        if node_id in node_by_id
    )
    core_counts = Counter(
        node_by_id[node_id].get("source_core") or "UNKNOWN"
        for node_id in node_ids
        if node_id in node_by_id
    )
    section_counts = Counter(
        node_by_id[node_id].get("source_section") or "UNKNOWN"
        for node_id in node_ids
        if node_id in node_by_id
    )

    boundary = pressure_level(len(internal_edges), len(outgoing_edges) + len(incoming_edges))
    owner_status = ownership_assessment(owner_counts)

    candidate_neighbor_ids = sorted(external_neighbor_ids)
    candidate_neighbor_scopes = sorted(external_neighbor_scopes)

    return {
        "cluster_id": cluster_id,
        "method": method,
        "node_count": len(node_ids),
        "owner_status": owner_status,
        "boundary_pressure": boundary,
        "nodes_by_owner_scope": dict(sorted(owner_counts.items())),
        "nodes_by_core": dict(sorted(core_counts.items())),
        "nodes_by_section": dict(sorted(section_counts.items())),
        "internal_edge_count": len(internal_edges),
        "outgoing_edge_count": len(outgoing_edges),
        "incoming_edge_count": len(incoming_edges),
        "missing_target_edge_count": len(missing_target_edges),
        "candidate_neighbor_ids": candidate_neighbor_ids,
        "candidate_neighbor_scopes": candidate_neighbor_scopes,
        "inbound_source_ids": sorted(inbound_source_ids),
        "inbound_source_scopes": sorted(inbound_source_scopes),
        "recommendation": recommendation_for_cluster(
            cluster=cluster,
            owner_status=owner_status,
            boundary_pressure=boundary,
            outgoing_count=len(outgoing_edges),
            incoming_count=len(incoming_edges),
        ),
        "sample_internal_edges": internal_edges[:10],
        "sample_outgoing_edges": outgoing_edges[:10],
        "sample_incoming_edges": incoming_edges[:10],
        "sample_missing_target_edges": missing_target_edges[:10],
        "node_ids": node_ids,
    }


def should_keep_cluster(cluster: dict[str, Any], min_size: int, include_weak: bool) -> bool:
    method = cluster.get("method")
    node_count = int(cluster.get("node_count") or 0)

    if node_count < min_size:
        return False

    if method == "weak_component" and not include_weak:
        return False

    return True


def build_report(
    node_by_id: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    min_size: int,
    include_weak: bool,
) -> dict[str, Any]:
    selected = [
        cluster
        for cluster in clusters
        if should_keep_cluster(cluster, min_size=min_size, include_weak=include_weak)
    ]

    analyses = [
        analyze_cluster(cluster, node_by_id=node_by_id, edges=edges)
        for cluster in selected
    ]

    recommendation_counts = Counter(item["recommendation"] for item in analyses)
    owner_status_counts = Counter(item["owner_status"] for item in analyses)
    boundary_counts = Counter(item["boundary_pressure"] for item in analyses)

    high_priority = [
        {
            "cluster_id": item["cluster_id"],
            "method": item["method"],
            "node_count": item["node_count"],
            "owner_status": item["owner_status"],
            "boundary_pressure": item["boundary_pressure"],
            "recommendation": item["recommendation"],
            "candidate_neighbor_scopes": item["candidate_neighbor_scopes"],
        }
        for item in analyses
        if item["boundary_pressure"] == "high"
        or item["owner_status"] == "multi_owner_fragmented"
        or item["recommendation"] in {
            "review_split_merge_or_bridge",
            "declare_or_review_neighbors",
            "classify_unowned_core_area",
        }
    ]

    return {
        "cluster_closure_report": {
            "schema_version": 0.1,
            "status": "PASS",
            "input_cluster_count": len(clusters),
            "selected_cluster_count": len(analyses),
            "selection": {
                "min_size": min_size,
                "include_weak_components": include_weak,
            },
            "summary": {
                "recommendation_counts": dict(sorted(recommendation_counts.items())),
                "owner_status_counts": dict(sorted(owner_status_counts.items())),
                "boundary_pressure_counts": dict(sorted(boundary_counts.items())),
                "high_priority_cluster_count": len(high_priority),
            },
            "high_priority_clusters": high_priority,
            "clusters": analyses,
            "notes": [
                "This report is diagnostic only.",
                "Clusters do not become scopes automatically.",
                "Outgoing edges suggest neighbor needs or boundary pressure.",
                "Multi-owner clusters require split, merge, bridge, or ownership review.",
                "Fully unowned clusters likely correspond to referentiel/link areas not yet scoped.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze cluster closure.")
    parser.add_argument("--nodes", default="tmp/scope_lab/constitution_graph_nodes.yaml")
    parser.add_argument("--edges", default="tmp/scope_lab/constitution_graph_edges.yaml")
    parser.add_argument("--clusters", default="tmp/scope_lab/constitution_graph_clusters.yaml")
    parser.add_argument("--out", default="tmp/scope_lab/cluster_closure_report.yaml")
    parser.add_argument("--min-size", type=int, default=3)
    parser.add_argument("--include-weak", action="store_true")
    args = parser.parse_args()

    node_by_id, edges, clusters = load_inputs(
        nodes_path=Path(args.nodes),
        edges_path=Path(args.edges),
        clusters_path=Path(args.clusters),
    )

    report = build_report(
        node_by_id=node_by_id,
        edges=edges,
        clusters=clusters,
        min_size=args.min_size,
        include_weak=args.include_weak,
    )

    Path(args.out).write_text(dump_yaml(report), encoding="utf-8")

    summary = report["cluster_closure_report"]["summary"]
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
