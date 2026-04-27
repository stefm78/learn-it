#!/usr/bin/env python3
"""Detect deterministic graph clusters from Scope Lab nodes/edges.

Experimental PHASE_04 script.

Reads:
  - tmp/scope_lab/constitution_graph_nodes.yaml
  - tmp/scope_lab/constitution_graph_edges.yaml

Writes:
  - tmp/scope_lab/constitution_graph_clusters.yaml
  - tmp/scope_lab/constitution_graph_clusters_report.yaml
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
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


def load_graph(nodes_path: Path, edges_path: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    nodes_doc = load_yaml(nodes_path)
    edges_doc = load_yaml(edges_path)

    nodes = nodes_doc.get("constitution_graph_nodes", {}).get("nodes", []) or []
    edges = edges_doc.get("constitution_graph_edges", {}).get("edges", []) or []

    node_by_id = {
        node["id"]: node
        for node in nodes
        if isinstance(node, dict) and node.get("id")
    }
    return node_by_id, edges


def build_adjacency(node_by_id: dict[str, dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in node_by_id}

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        if source in node_by_id and target in node_by_id:
            adjacency[source].add(target)
            adjacency[target].add(source)

    return adjacency


def weak_components(adjacency: dict[str, set[str]]) -> list[list[str]]:
    seen: set[str] = set()
    components: list[list[str]] = []

    for start in sorted(adjacency):
        if start in seen:
            continue

        queue = deque([start])
        seen.add(start)
        component: list[str] = []

        while queue:
            node = queue.popleft()
            component.append(node)

            for neighbor in sorted(adjacency[node]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        components.append(sorted(component))

    return sorted(components, key=lambda c: (-len(c), c[0] if c else ""))


def label_propagation(adjacency: dict[str, set[str]], max_rounds: int = 20) -> list[list[str]]:
    """Deterministic label propagation used as a lightweight community heuristic."""
    labels = {node_id: node_id for node_id in adjacency}

    for _ in range(max_rounds):
        changed = False

        for node_id in sorted(adjacency):
            neighbor_labels = Counter(labels[neighbor] for neighbor in adjacency[node_id])
            if not neighbor_labels:
                continue

            best_count = max(neighbor_labels.values())
            best_labels = sorted(
                label
                for label, count in neighbor_labels.items()
                if count == best_count
            )
            new_label = best_labels[0]

            if new_label != labels[node_id]:
                labels[node_id] = new_label
                changed = True

        if not changed:
            break

    clusters_by_label: dict[str, list[str]] = defaultdict(list)
    for node_id, label in labels.items():
        clusters_by_label[label].append(node_id)

    clusters = [sorted(ids) for ids in clusters_by_label.values()]
    return sorted(clusters, key=lambda c: (-len(c), c[0] if c else ""))


def edge_counts(node_ids: set[str], edges: list[dict[str, Any]]) -> tuple[int, int]:
    internal = 0
    external = 0

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        if source in node_ids and target in node_ids:
            internal += 1
        elif source in node_ids or target in node_ids:
            external += 1

    return internal, external


def summarize_cluster(
    cluster_id: str,
    node_ids: list[str],
    node_by_id: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    method: str,
) -> dict[str, Any]:
    node_set = set(node_ids)
    internal, external = edge_counts(node_set, edges)

    owner_counts = Counter(
        node_by_id[node_id].get("current_owner_scope") or "UNOWNED"
        for node_id in node_ids
    )
    core_counts = Counter(
        node_by_id[node_id].get("source_core") or "UNKNOWN"
        for node_id in node_ids
    )
    section_counts = Counter(
        node_by_id[node_id].get("source_section") or "UNKNOWN"
        for node_id in node_ids
    )

    dominant_owner, dominant_count = owner_counts.most_common(1)[0]

    if external >= internal and external > 0:
        boundary_pressure = "high"
    elif external > 0:
        boundary_pressure = "medium"
    else:
        boundary_pressure = "low"

    return {
        "cluster_id": cluster_id,
        "method": method,
        "node_count": len(node_ids),
        "internal_edge_count": internal,
        "external_edge_count": external,
        "boundary_pressure": boundary_pressure,
        "dominant_owner_scope": dominant_owner,
        "dominant_owner_ratio": round(dominant_count / len(node_ids), 4) if node_ids else 0,
        "nodes_by_owner_scope": dict(sorted(owner_counts.items())),
        "nodes_by_core": dict(sorted(core_counts.items())),
        "nodes_by_section": dict(sorted(section_counts.items())),
        "node_ids": node_ids,
    }


def build_artifacts(
    node_by_id: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    max_rounds: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    adjacency = build_adjacency(node_by_id, edges)

    weak = weak_components(adjacency)
    label_clusters = label_propagation(adjacency, max_rounds=max_rounds)

    clusters: list[dict[str, Any]] = []

    for index, ids in enumerate(weak, start=1):
        clusters.append(
            summarize_cluster(
                f"WEAK_COMPONENT_{index:03d}",
                ids,
                node_by_id,
                edges,
                "weak_component",
            )
        )

    for index, ids in enumerate(label_clusters, start=1):
        clusters.append(
            summarize_cluster(
                f"LABEL_CLUSTER_{index:03d}",
                ids,
                node_by_id,
                edges,
                "label_propagation",
            )
        )

    artifact = {
        "constitution_graph_clusters": {
            "schema_version": 0.1,
            "status": "PASS",
            "cluster_count": len(clusters),
            "methods": [
                "weak_component",
                "label_propagation",
            ],
            "clusters": clusters,
        }
    }

    report = {
        "constitution_graph_clusters_report": {
            "schema_version": 0.1,
            "status": "PASS",
            "node_count": len(node_by_id),
            "edge_count": len(edges),
            "weak_component_count": len(weak),
            "label_cluster_count": len(label_clusters),
            "largest_weak_component_size": len(weak[0]) if weak else 0,
            "largest_label_cluster_size": len(label_clusters[0]) if label_clusters else 0,
            "notes": [
                "Weak components show pure graph connectivity.",
                "Label propagation is a deterministic lightweight community heuristic.",
                "PHASE_05 must perform closure analysis before any scoping decision.",
            ],
        }
    }

    return artifact, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect Scope Lab graph clusters.")
    parser.add_argument("--nodes", default="tmp/scope_lab/constitution_graph_nodes.yaml")
    parser.add_argument("--edges", default="tmp/scope_lab/constitution_graph_edges.yaml")
    parser.add_argument("--out", default="tmp/scope_lab/constitution_graph_clusters.yaml")
    parser.add_argument("--report", default="tmp/scope_lab/constitution_graph_clusters_report.yaml")
    parser.add_argument("--max-rounds", type=int, default=20)
    args = parser.parse_args()

    node_by_id, edges = load_graph(Path(args.nodes), Path(args.edges))
    artifact, report = build_artifacts(node_by_id, edges, args.max_rounds)

    Path(args.out).write_text(dump_yaml(artifact), encoding="utf-8")
    Path(args.report).write_text(dump_yaml(report), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"written: {args.out}")
    print(f"written: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
