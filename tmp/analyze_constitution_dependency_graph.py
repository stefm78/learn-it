#!/usr/bin/env python3
"""Extract a first dependency graph from Learn-It current cores.

Experimental Scope Lab script.

Reads:
  - docs/cores/current/constitution.yaml
  - docs/cores/current/referentiel.yaml
  - docs/cores/current/link.yaml
  - docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml

Writes:
  - tmp/scope_lab/constitution_graph_nodes.yaml
  - tmp/scope_lab/constitution_graph_edges.yaml
  - tmp/scope_lab/constitution_graph_report.yaml

This script is read-only with regard to canonical sources.
It does not modify the scope catalog or the current cores.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


CORE_FILES = {
    "constitution": Path("docs/cores/current/constitution.yaml"),
    "referentiel": Path("docs/cores/current/referentiel.yaml"),
    "link": Path("docs/cores/current/link.yaml"),
}

ENTRY_SECTIONS = [
    "SYSTEM",
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
    "REFERENCES",
    "BINDINGS",
]

ID_FIELDS = [
    "id",
    "rule_id",
    "event_id",
    "constraint_id",
    "invariant_id",
    "action_id",
    "type_id",
    "system_id",
    "ref_id",
    "binding_id",
]

REFERENCE_KEYS = {
    "depends_on",
    "relations",
    "target",
    "targets",
    "source",
    "sources",
    "ref",
    "refs",
    "reference",
    "references",
    "core_ref",
    "core_refs",
    "binding_ref",
    "binding_refs",
    "related_id",
    "related_ids",
}

ID_LIKE_RE = re.compile(r"^[A-Z][A-Z0-9_]*(?:\.[A-Z0-9_]+)?$")


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fingerprint(value: Any) -> str:
    normalized = yaml.safe_dump(
        value,
        sort_keys=True,
        allow_unicode=True,
        default_flow_style=False,
    )
    return sha256_text(normalized)


def unwrap_core(data: Any) -> dict[str, Any]:
    if isinstance(data, dict) and isinstance(data.get("CORE"), dict):
        return data["CORE"]
    if isinstance(data, dict):
        return data
    return {}


def is_id_like(value: str) -> bool:
    return bool(ID_LIKE_RE.match(value))


def get_entry_id(entry: Any, fallback_key: str | None = None) -> str | None:
    if isinstance(entry, dict):
        for field in ID_FIELDS:
            value = entry.get(field)
            if isinstance(value, str) and value:
                return value.split("::", 1)[0]
    if fallback_key and is_id_like(fallback_key):
        return fallback_key.split("::", 1)[0]
    return None


def normalize_ref(raw: Any) -> str | None:
    if isinstance(raw, str):
        value = raw.split("::", 1)[0]
        return value if is_id_like(value) else None

    if isinstance(raw, dict):
        for field in ID_FIELDS:
            value = raw.get(field)
            if isinstance(value, str):
                value = value.split("::", 1)[0]
                return value if is_id_like(value) else None

        for field in ("target", "source", "ref", "reference"):
            value = raw.get(field)
            if isinstance(value, str):
                value = value.split("::", 1)[0]
                return value if is_id_like(value) else None

    return None


def iter_core_entries(core_root: dict[str, Any]):
    """Yield (section, fallback_key, entry)."""
    root_id = core_root.get("id")
    if isinstance(root_id, str):
        yield "CORE", None, {
            "id": root_id,
            "version": core_root.get("version"),
            "description": core_root.get("description"),
        }

    for section in ENTRY_SECTIONS:
        value = core_root.get(section)
        if value is None:
            continue

        if isinstance(value, list):
            for entry in value:
                yield section, None, entry

        elif isinstance(value, dict):
            # Section may itself be one ID-bearing entry.
            if get_entry_id(value):
                yield section, None, value
            else:
                for key, entry in value.items():
                    yield section, str(key), entry


def load_scope_indexes(scope_dir: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    """Return owner_by_id and neighbor_scopes_by_id."""
    owner_by_id: dict[str, str] = {}
    neighbor_scopes_by_id: dict[str, set[str]] = defaultdict(set)

    if not scope_dir.exists():
        return owner_by_id, neighbor_scopes_by_id

    for path in sorted(scope_dir.glob("*.yaml")):
        data = load_yaml(path)
        root = data.get("scope_definition", {}) if isinstance(data, dict) else {}
        scope_key = root.get("scope_key")
        if not isinstance(scope_key, str):
            continue

        target_ids = root.get("target", {}).get("ids", []) or []
        for item in target_ids:
            if isinstance(item, str):
                owner_by_id[item] = scope_key

        neighbor_ids = root.get("default_neighbors_to_read", {}).get("ids", []) or []
        for item in neighbor_ids:
            if isinstance(item, str):
                neighbor_scopes_by_id[item].add(scope_key)

    return owner_by_id, neighbor_scopes_by_id


def collect_nodes(
    repo_root: Path,
    owner_by_id: dict[str, str],
    neighbor_scopes_by_id: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    node_by_id: dict[str, dict[str, Any]] = {}

    for core_name, rel_path in CORE_FILES.items():
        data = load_yaml(repo_root / rel_path)
        core_root = unwrap_core(data)
        core_id = core_root.get("id")
        core_version = core_root.get("version")

        for section, fallback_key, entry in iter_core_entries(core_root):
            entry_id = get_entry_id(entry, fallback_key)
            if not entry_id:
                continue

            logic = entry.get("logic", {}) if isinstance(entry, dict) else {}

            node = {
                "id": entry_id,
                "source_core": core_name,
                "source_path": rel_path.as_posix(),
                "source_core_id": core_id if isinstance(core_id, str) else None,
                "source_core_version": core_version if isinstance(core_version, str) else None,
                "source_section": section,
                "logic_scope": logic.get("scope") if isinstance(logic, dict) else None,
                "current_owner_scope": owner_by_id.get(entry_id),
                "neighbor_of_scopes": sorted(neighbor_scopes_by_id.get(entry_id, set())),
                "entry_fingerprint": fingerprint(entry),
            }

            nodes.append(node)

            if entry_id in node_by_id:
                node["duplicate_node_id_detected"] = True
            node_by_id[entry_id] = node

    nodes.sort(key=lambda n: (n["source_core"], n["source_section"], n["id"]))
    return nodes, node_by_id


def iter_explicit_refs(value: Any, key_path: tuple[str, ...] = ()):
    """Yield (target_id, edge_type) from explicit reference-shaped fields."""
    if isinstance(value, dict):
        for key, child in value.items():
            key_str = str(key)
            child_path = key_path + (key_str,)

            if key_str in REFERENCE_KEYS:
                if isinstance(child, list):
                    for item in child:
                        ref = normalize_ref(item)
                        if ref:
                            yield ref, ".".join(child_path)
                else:
                    ref = normalize_ref(child)
                    if ref:
                        yield ref, ".".join(child_path)

            yield from iter_explicit_refs(child, child_path)

    elif isinstance(value, list):
        for item in value:
            yield from iter_explicit_refs(item, key_path)


def classify_edge(source_scope: str | None, target_scope: str | None, target_exists: bool) -> str:
    if not target_exists:
        return "missing_target_edge"
    if source_scope and target_scope and source_scope == target_scope:
        return "internal_scope_edge"
    if source_scope and target_scope and source_scope != target_scope:
        return "cross_scope_edge"
    return "unowned_or_unscoped_edge"


def collect_edges(
    repo_root: Path,
    node_by_id: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edges: list[dict[str, Any]] = []
    missing_targets: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for core_name, rel_path in CORE_FILES.items():
        data = load_yaml(repo_root / rel_path)
        core_root = unwrap_core(data)

        for section, fallback_key, entry in iter_core_entries(core_root):
            source_id = get_entry_id(entry, fallback_key)
            if not source_id or not isinstance(entry, dict):
                continue

            source_node = node_by_id.get(source_id, {})
            source_scope = source_node.get("current_owner_scope")

            for target_id, edge_type in iter_explicit_refs(entry):
                if target_id == source_id:
                    continue

                key = (source_id, target_id, edge_type)
                if key in seen:
                    continue
                seen.add(key)

                target_node = node_by_id.get(target_id)
                target_scope = target_node.get("current_owner_scope") if target_node else None

                edge = {
                    "source": source_id,
                    "target": target_id,
                    "edge_type": edge_type,
                    "status": "canonical_explicit",
                    "source_core": core_name,
                    "source_section": section,
                    "source_scope": source_scope,
                    "target_core": target_node.get("source_core") if target_node else None,
                    "target_section": target_node.get("source_section") if target_node else None,
                    "target_scope": target_scope,
                    "classification": classify_edge(source_scope, target_scope, target_node is not None),
                }

                edges.append(edge)
                if target_node is None:
                    missing_targets.append(edge)

    edges.sort(key=lambda e: (e["source"], e["target"], e["edge_type"]))
    return edges, missing_targets


def build_report(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    missing_targets: list[dict[str, Any]],
) -> dict[str, Any]:
    nodes_by_core = Counter(node["source_core"] for node in nodes)
    nodes_by_section = Counter(node["source_section"] for node in nodes)
    nodes_by_owner = Counter(node.get("current_owner_scope") or "UNOWNED" for node in nodes)
    edges_by_classification = Counter(edge["classification"] for edge in edges)

    cross_scope_pairs = Counter(
        (
            edge.get("source_scope") or "UNOWNED",
            edge.get("target_scope") or "UNOWNED",
        )
        for edge in edges
        if edge["classification"] == "cross_scope_edge"
    )

    duplicate_node_ids = sorted(
        node["id"] for node in nodes if node.get("duplicate_node_id_detected")
    )

    return {
        "constitution_dependency_graph_report": {
            "schema_version": 0.1,
            "status": "PASS" if not missing_targets else "PASS_WITH_MISSING_TARGETS",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "missing_target_edge_count": len(missing_targets),
            "duplicate_node_id_count": len(duplicate_node_ids),
            "duplicate_node_ids": duplicate_node_ids,
            "nodes_by_core": dict(sorted(nodes_by_core.items())),
            "nodes_by_section": dict(sorted(nodes_by_section.items())),
            "nodes_by_owner_scope": dict(sorted(nodes_by_owner.items())),
            "edges_by_classification": dict(sorted(edges_by_classification.items())),
            "cross_scope_pairs": [
                {
                    "source_scope": source,
                    "target_scope": target,
                    "edge_count": count,
                }
                for (source, target), count in sorted(
                    cross_scope_pairs.items(),
                    key=lambda item: (-item[1], item[0][0], item[0][1]),
                )
            ],
            "missing_targets": [
                {
                    "source": edge["source"],
                    "target": edge["target"],
                    "edge_type": edge["edge_type"],
                }
                for edge in missing_targets
            ],
            "notes": [
                "Experimental Scope Lab graph extraction. Does not modify canonical sources.",
                "Only explicit reference-shaped fields are treated as edges in this first version.",
                "Graph clustering and closure analysis are intentionally left to later phases.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract Learn-It dependency graph.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--scope-dir",
        default="docs/pipelines/constitution/scope_catalog/scope_definitions",
    )
    parser.add_argument("--out-dir", default="tmp/scope_lab")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    owner_by_id, neighbor_scopes_by_id = load_scope_indexes(repo_root / args.scope_dir)
    nodes, node_by_id = collect_nodes(repo_root, owner_by_id, neighbor_scopes_by_id)
    edges, missing_targets = collect_edges(repo_root, node_by_id)
    report = build_report(nodes, edges, missing_targets)

    nodes_artifact = {
        "constitution_graph_nodes": {
            "schema_version": 0.1,
            "source_cores": {
                core_name: rel_path.as_posix()
                for core_name, rel_path in CORE_FILES.items()
            },
            "node_count": len(nodes),
            "nodes": nodes,
        }
    }

    edges_artifact = {
        "constitution_graph_edges": {
            "schema_version": 0.1,
            "edge_count": len(edges),
            "edges": edges,
        }
    }

    nodes_path = out_dir / "constitution_graph_nodes.yaml"
    edges_path = out_dir / "constitution_graph_edges.yaml"
    report_path = out_dir / "constitution_graph_report.yaml"

    nodes_path.write_text(dump_yaml(nodes_artifact), encoding="utf-8")
    edges_path.write_text(dump_yaml(edges_artifact), encoding="utf-8")
    report_path.write_text(dump_yaml(report), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"written: {nodes_path.relative_to(repo_root).as_posix()}")
    print(f"written: {edges_path.relative_to(repo_root).as_posix()}")
    print(f"written: {report_path.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
