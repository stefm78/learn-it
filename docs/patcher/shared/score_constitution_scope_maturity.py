#!/usr/bin/env python3
"""Compute a deterministic post-scoping maturity report for Constitution scopes.

This script is intentionally non-publishing:
- it writes only the report path passed with --report;
- it never rewrites policy.yaml, decisions.yaml, the scope catalog, or scope definitions;
- in V1.1, policy.yaml remains authoritative for published maturity.

The report compares published governed maturity with a deterministic diagnostic score
computed from generated scope definitions, canon IDs, ownership coverage, explicit
neighbors, partition signals, and governance backlog signals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run this script.") from exc


ENTRY_SECTIONS = [
    "SYSTEM",
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
]

AXES = [
    "clarity_of_scope",
    "internal_coherence",
    "inter_scope_boundaries",
    "dependency_explicitness",
    "bounded_run_executability",
    "inter_release_stability",
]

MATURITY_MAX_SCORE = 24
MATURITY_LEVELS: list[tuple[str, int, int]] = [
    ("L4_strong", 21, 24),
    ("L3_operational", 17, 20),
    ("L2_usable_with_care", 13, 16),
    ("L1_fragile", 9, 12),
    ("L0_experimental", 0, 8),
]

SEVERE_BACKLOG_TYPES = {
    "scope_gap",
    "scope_extension_needed",
    "orphan_id",
    "partition_angle_mort",
}


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML object must be a mapping: {path}")
    return data


def load_yaml_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def dump_yaml(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def read_required_yaml(
    repo_root: Path,
    ref: str,
    blocking_findings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    path = repo_root / ref
    if not path.exists():
        blocking_findings.append(
            {
                "finding_id": f"MISSING_REQUIRED_INPUT::{ref}",
                "severity": "blocking",
                "message": f"Required input is missing: {ref}",
            }
        )
        return {}
    try:
        return load_yaml(path)
    except Exception as exc:  # deterministic failure captured in report
        blocking_findings.append(
            {
                "finding_id": f"INVALID_REQUIRED_INPUT::{ref}",
                "severity": "blocking",
                "message": f"Required input could not be parsed: {ref}",
                "error": str(exc),
            }
        )
        return {}


def input_record(repo_root: Path, ref: str, required: bool = True) -> Dict[str, Any]:
    path = repo_root / ref
    record = {"ref": ref, "required": required, "present": path.exists()}
    if path.exists() and path.is_file():
        record["sha256"] = sha256_file(path)
    return record


# ---------------------------------------------------------------------------
# Canon extraction
# ---------------------------------------------------------------------------

def normalize_target_id(raw: Any) -> Optional[str]:
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
        if not isinstance(rel, dict):
            continue
        target_id = normalize_target_id(rel.get("target"))
        if target_id:
            yield target_id
        source_id = normalize_target_id(rel.get("source"))
        if source_id:
            yield source_id


def collect_entries(core_doc: Dict[str, Any], *, core_name: str, source_ref: str) -> Dict[str, Dict[str, Any]]:
    core_root = core_doc.get("CORE", {})
    entries: Dict[str, Dict[str, Any]] = {}
    if not isinstance(core_root, dict):
        return entries

    for section in ENTRY_SECTIONS:
        raw_items = core_root.get(section, []) or []
        if not isinstance(raw_items, list):
            continue
        for raw in raw_items:
            if not isinstance(raw, dict) or not isinstance(raw.get("id"), str):
                continue
            entry_id = raw["id"]
            logic = raw.get("logic") or {}
            entries[entry_id] = {
                "id": entry_id,
                "core": core_name,
                "source_ref": source_ref,
                "section": section,
                "logic_scope": logic.get("scope", "unknown") if isinstance(logic, dict) else "unknown",
                "refs": sorted(set(iter_refs(raw))),
            }
    return entries


def collect_all_entries(
    constitution: Dict[str, Any],
    referentiel: Dict[str, Any],
    link: Dict[str, Any],
    refs: Dict[str, str],
) -> Dict[str, Dict[str, Any]]:
    entries: Dict[str, Dict[str, Any]] = {}
    for core_name, doc in [
        ("constitution", constitution),
        ("referentiel", referentiel),
        ("link", link),
    ]:
        entries.update(
            collect_entries(doc, core_name=core_name, source_ref=refs[core_name])
        )
    return entries


# ---------------------------------------------------------------------------
# Catalog / policy extraction
# ---------------------------------------------------------------------------

def maturity_level_from_score(score: int) -> str:
    for level, lo, hi in MATURITY_LEVELS:
        if lo <= score <= hi:
            return level
    return "L0_experimental"


def level_rank(level: str) -> int:
    # Higher means stronger maturity.
    ordered = ["L0_experimental", "L1_fragile", "L2_usable_with_care", "L3_operational", "L4_strong"]
    return ordered.index(level) if level in ordered else 0


def collect_policy_scopes(policy: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    root = policy.get("scope_generation_policy", {})
    scopes: Dict[str, Dict[str, Any]] = {}
    for entry in root.get("declared_scopes", []) or []:
        if isinstance(entry, dict) and entry.get("scope_key"):
            scopes[entry["scope_key"]] = entry
    return scopes


def collect_catalog_scopes(catalog: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    root = catalog.get("scope_catalog", {})
    scopes: Dict[str, Dict[str, Any]] = {}
    for entry in root.get("published_scopes", []) or []:
        if isinstance(entry, dict) and entry.get("scope_key"):
            scopes[entry["scope_key"]] = entry
    return scopes


def collect_scope_definitions(scope_dir: Path) -> Dict[str, Dict[str, Any]]:
    definitions: Dict[str, Dict[str, Any]] = {}
    if not scope_dir.exists():
        return definitions
    for path in sorted(scope_dir.glob("*.yaml")):
        data = load_yaml_optional(path)
        root = data.get("scope_definition", {})
        scope_key = root.get("scope_key")
        if isinstance(scope_key, str):
            definitions[scope_key] = data
    return definitions


def build_owner_maps(scope_defs: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    owners_by_id: Dict[str, List[str]] = defaultdict(list)
    for scope_key, scope_def in scope_defs.items():
        root = scope_def.get("scope_definition", {})
        target_ids = root.get("target", {}).get("ids", []) or []
        for target_id in target_ids:
            if isinstance(target_id, str):
                owners_by_id[target_id].append(scope_key)

    single_owner: Dict[str, str] = {}
    duplicate_owners: Dict[str, List[str]] = {}
    for id_, owners in owners_by_id.items():
        unique = sorted(set(owners))
        if len(unique) == 1:
            single_owner[id_] = unique[0]
        elif len(unique) > 1:
            duplicate_owners[id_] = unique
    return single_owner, duplicate_owners


def collect_open_backlog_by_scope(backlog_doc: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    result: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    root = backlog_doc.get("governance_backlog", {})
    entries = root.get("entries", []) or []
    if not isinstance(entries, list):
        return result

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("status") != "open":
            continue
        related: Set[str] = set()
        if isinstance(entry.get("scope_key"), str):
            related.add(entry["scope_key"])
        for scope_key in entry.get("related_scope_keys", []) or []:
            if isinstance(scope_key, str):
                related.add(scope_key)
        for scope_key in related:
            result[scope_key].append(entry)
    return {k: sorted(v, key=lambda item: item.get("entry_id", "")) for k, v in result.items()}


def active_constitution_runs(runs_index: Dict[str, Any]) -> List[Dict[str, Any]]:
    root = runs_index.get("runs_index", {})
    active = root.get("active_runs", []) or []
    return [
        run for run in active
        if isinstance(run, dict) and run.get("run_status", "active") == "active"
    ]


# ---------------------------------------------------------------------------
# Diagnostic scoring
# ---------------------------------------------------------------------------

def clamp_score(score: int) -> int:
    return max(0, min(4, int(score)))


def score_clarity(scope_root: Dict[str, Any], published_axes: Dict[str, Any]) -> Dict[str, Any]:
    target = scope_root.get("target", {})
    maturity = scope_root.get("maturity", {})
    evidence = []
    score = 0

    if target.get("files"):
        score += 1
        evidence.append("target.files present")
    else:
        evidence.append("target.files missing")

    if target.get("modules"):
        score += 1
        evidence.append("target.modules present")
    else:
        evidence.append("target.modules missing")

    if target.get("ids"):
        score += 1
        evidence.append("target.ids present")
    else:
        evidence.append("target.ids missing")

    if scope_root.get("watchpoints") or maturity.get("rationale") or scope_root.get("notes"):
        score += 1
        evidence.append("watchpoints, rationale, or notes present")
    else:
        evidence.append("watchpoints/rationale/notes missing")

    return {
        "score": clamp_score(score),
        "evidence": evidence,
        "published_axis_score": published_axes.get("clarity_of_scope"),
    }


def score_internal_coherence(
    target_ids: List[str],
    all_entries: Dict[str, Dict[str, Any]],
    owners_by_id: Dict[str, str],
    scope_key: str,
) -> Dict[str, Any]:
    # V1.1: score internal coherence using both label concentration and edge cohesion.
    # Composite scopes may cover several logic.scope values and still be coherent
    # when their owned IDs are strongly linked internally.
    logic_scopes = [
        all_entries[id_]["logic_scope"]
        for id_ in target_ids
        if id_ in all_entries
    ]
    distribution = dict(sorted(Counter(logic_scopes).items()))
    evidence: List[Any] = [{"logic_scope_distribution": distribution}]

    if not target_ids:
        return {
            "score": 0,
            "evidence": evidence + ["no target ids"],
            "calibration": "v1_1_no_target_ids",
        }

    dominant_ratio = 0.0
    if logic_scopes:
        dominant_ratio = max(Counter(logic_scopes).values()) / len(logic_scopes)

    internal_edges = 0
    external_edges = 0
    for id_ in target_ids:
        entry = all_entries.get(id_)
        if not entry:
            continue
        for ref in entry.get("refs", []):
            owner = owners_by_id.get(ref)
            if owner == scope_key:
                internal_edges += 1
            elif owner:
                external_edges += 1

    total_owned_edges = internal_edges + external_edges
    internal_ratio = 1.0 if total_owned_edges == 0 else internal_edges / total_owned_edges

    if dominant_ratio >= 0.75 and internal_ratio >= 0.70:
        score = 4
        reason = "dominant_logic_scope_and_internal_edges_strong"
    elif dominant_ratio >= 0.55 and internal_ratio >= 0.50:
        score = 3
        reason = "dominant_logic_scope_good"
    elif internal_ratio >= 0.80 and internal_edges >= 10:
        score = 3
        reason = "composite_scope_with_high_internal_edge_cohesion"
    elif dominant_ratio >= 0.35:
        score = 2
        reason = "moderate_dominant_logic_scope"
    elif logic_scopes:
        score = 1
        reason = "weak_logic_scope_concentration"
    else:
        score = 0
        reason = "no_logic_scope_evidence"

    evidence.append(
        {
            "dominant_logic_scope_ratio": round(dominant_ratio, 3),
            "internal_owned_edge_count": internal_edges,
            "external_owned_edge_count": external_edges,
            "internal_owned_edge_ratio": round(internal_ratio, 3),
            "v1_1_reason": reason,
        }
    )

    return {"score": clamp_score(score), "evidence": evidence, "calibration": "v1_1"}


def compute_scope_edges(
    target_ids: List[str],
    neighbor_ids: Set[str],
    neighbor_files: Set[str],
    all_entries: Dict[str, Dict[str, Any]],
    owners_by_id: Dict[str, str],
    scope_key: str,
) -> Dict[str, Any]:
    internal_edges: List[Dict[str, Any]] = []
    outgoing_edges: List[Dict[str, Any]] = []
    covered_outgoing_edges: List[Dict[str, Any]] = []
    uncovered_outgoing_edges: List[Dict[str, Any]] = []
    missing_target_edges: List[Dict[str, Any]] = []

    for id_ in target_ids:
        entry = all_entries.get(id_)
        if not entry:
            continue
        for ref in entry.get("refs", []):
            target = all_entries.get(ref)
            if not target:
                missing_target_edges.append({"source": id_, "target": ref})
                continue

            owner = owners_by_id.get(ref)
            edge = {
                "source": id_,
                "target": ref,
                "target_owner_scope": owner or "unowned_or_external",
                "target_core": target.get("core", ""),
                "target_source_ref": target.get("source_ref", ""),
            }

            if owner == scope_key:
                internal_edges.append(edge)
                continue

            if owner or target.get("core") != "constitution":
                outgoing_edges.append(edge)

                covered_by_neighbor_id = ref in neighbor_ids
                covered_by_neighbor_file = target.get("source_ref") in neighbor_files
                if covered_by_neighbor_id or covered_by_neighbor_file:
                    covered_outgoing_edges.append(
                        {
                            **edge,
                            "coverage": "neighbor_id" if covered_by_neighbor_id else "neighbor_file",
                        }
                    )
                else:
                    uncovered_outgoing_edges.append(edge)

    return {
        "internal_edges": sorted(internal_edges, key=lambda e: (e["source"], e["target"])),
        "outgoing_edges": sorted(outgoing_edges, key=lambda e: (e["source"], e["target"])),
        "covered_outgoing_edges": sorted(covered_outgoing_edges, key=lambda e: (e["source"], e["target"])),
        "uncovered_outgoing_edges": sorted(uncovered_outgoing_edges, key=lambda e: (e["source"], e["target"])),
        "missing_target_edges": sorted(missing_target_edges, key=lambda e: (e["source"], e["target"])),
    }


def score_boundaries(
    *,
    missing_target_ids: List[str],
    duplicate_owned_ids: Dict[str, List[str]],
    edges: Dict[str, Any],
    backlog_entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    severe_backlog_count = sum(
        1 for entry in backlog_entries
        if entry.get("type") in SEVERE_BACKLOG_TYPES
    )
    uncovered_count = len(edges["uncovered_outgoing_edges"])
    missing_edge_count = len(edges["missing_target_edges"])

    evidence = [
        {"missing_target_ids": missing_target_ids},
        {"duplicate_owned_ids": duplicate_owned_ids},
        {"uncovered_outgoing_edge_count": uncovered_count},
        {"missing_target_edge_count": missing_edge_count},
        {"related_open_backlog_count": len(backlog_entries)},
        {"related_severe_open_backlog_count": severe_backlog_count},
    ]

    if missing_target_ids or duplicate_owned_ids or missing_edge_count:
        score = 0
    elif uncovered_count == 0 and severe_backlog_count == 0:
        score = 4
    elif uncovered_count <= 2 and severe_backlog_count <= 1:
        score = 3
    elif uncovered_count <= 6 and severe_backlog_count <= 3:
        score = 2
    elif uncovered_count <= 12:
        score = 1
    else:
        score = 0

    return {"score": clamp_score(score), "evidence": evidence}


def score_dependency_explicitness(edges: Dict[str, Any]) -> Dict[str, Any]:
    # V1.1 keeps strict scoring but improves diagnostic granularity.
    outgoing_edges = edges["outgoing_edges"]
    covered_edges = edges["covered_outgoing_edges"]
    uncovered_edges = edges["uncovered_outgoing_edges"]

    outgoing_count = len(outgoing_edges)
    covered_count = len(covered_edges)
    uncovered_count = len(uncovered_edges)

    constitution_edges = [edge for edge in outgoing_edges if edge.get("target_core") == "constitution"]
    external_edges = [edge for edge in outgoing_edges if edge.get("target_core") != "constitution"]

    constitution_covered = [
        edge for edge in covered_edges
        if edge.get("target_core") == "constitution" and edge.get("coverage") == "neighbor_id"
    ]
    external_file_covered = [
        edge for edge in covered_edges
        if edge.get("target_core") != "constitution" and edge.get("coverage") == "neighbor_file"
    ]
    external_id_covered = [
        edge for edge in covered_edges
        if edge.get("target_core") != "constitution" and edge.get("coverage") == "neighbor_id"
    ]

    uncovered_constitution = [
        edge for edge in uncovered_edges if edge.get("target_core") == "constitution"
    ]
    uncovered_external = [
        edge for edge in uncovered_edges if edge.get("target_core") != "constitution"
    ]

    if outgoing_count == 0:
        coverage_ratio = 1.0
        score = 4
    else:
        coverage_ratio = covered_count / outgoing_count
        if coverage_ratio >= 0.90 and uncovered_count == 0:
            score = 4
        elif coverage_ratio >= 0.70:
            score = 3
        elif coverage_ratio >= 0.40:
            score = 2
        elif coverage_ratio > 0:
            score = 1
        else:
            score = 0

    return {
        "score": clamp_score(score),
        "evidence": [
            {
                "outgoing_dependency_count": outgoing_count,
                "covered_outgoing_dependency_count": covered_count,
                "uncovered_outgoing_dependency_count": uncovered_count,
                "coverage_ratio": round(coverage_ratio, 3),
                "constitution_neighbor_id_coverage": {
                    "outgoing_count": len(constitution_edges),
                    "covered_by_neighbor_id_count": len(constitution_covered),
                    "uncovered_count": len(uncovered_constitution),
                    "uncovered_ids": sorted({edge["target"] for edge in uncovered_constitution}),
                },
                "external_core_coverage": {
                    "outgoing_count": len(external_edges),
                    "covered_by_neighbor_file_count": len(external_file_covered),
                    "covered_by_neighbor_id_count": len(external_id_covered),
                    "uncovered_count": len(uncovered_external),
                    "uncovered_ids": sorted({edge["target"] for edge in uncovered_external}),
                },
                "v1_1_position": "strict_score_preserved_evidence_granularity_improved",
            }
        ],
        "calibration": "v1_1",
    }


def score_bounded_run_executability(
    target_ids: List[str],
    neighbor_ids: Set[str],
    neighbor_files: Set[str],
    watchpoints: List[Any],
    backlog_entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    target_count = len(target_ids)
    neighbor_id_count = len(neighbor_ids)
    watchpoint_count = len(watchpoints)
    severe_backlog_count = sum(
        1 for entry in backlog_entries
        if entry.get("type") in SEVERE_BACKLOG_TYPES
    )

    if target_count == 0:
        score = 0
    elif target_count <= 30 and neighbor_id_count <= 20 and watchpoint_count <= 8:
        score = 4
    elif target_count <= 60 and neighbor_id_count <= 40 and watchpoint_count <= 12:
        score = 3
    elif target_count <= 100 and neighbor_id_count <= 80:
        score = 2
    else:
        score = 1

    if severe_backlog_count >= 3:
        score -= 1

    return {
        "score": clamp_score(score),
        "evidence": [
            {
                "target_id_count": target_count,
                "neighbor_id_count": neighbor_id_count,
                "neighbor_file_count": len(neighbor_files),
                "watchpoint_count": watchpoint_count,
                "related_severe_open_backlog_count": severe_backlog_count,
            }
        ],
    }


def score_inter_release_stability(
    published_axes: Dict[str, Any],
    backlog_entries: List[Dict[str, Any]],
    generation_report: Dict[str, Any],
) -> Dict[str, Any]:
    # V1.1 separates stability score from evidence confidence.
    # Missing release-to-release scope history limits confidence; it is not by
    # itself an automatic maturity penalty. Severe backlog remains a real penalty.
    published_axis = published_axes.get("inter_release_stability")
    if isinstance(published_axis, int):
        base = min(published_axis, 3)
    else:
        base = 3

    severe_backlog_count = sum(
        1 for entry in backlog_entries
        if entry.get("type") in SEVERE_BACKLOG_TYPES
    )

    changed_files = (
        generation_report
        .get("scope_generation_report", {})
        .get("changed_files", [])
    )
    changed_files_count = 0 if changed_files == ["none"] else len(changed_files or [])

    score = base
    if severe_backlog_count > 0:
        score = min(score, 2)

    confidence = "limited"
    confidence_reason = "no dedicated release-to-release scope maturity history is consumed in V1.1"
    if severe_backlog_count > 0:
        confidence = "limited_with_backlog_pressure"
    elif changed_files_count == 0:
        confidence = "moderate"

    return {
        "score": clamp_score(score),
        "confidence": confidence,
        "evidence": [
            f"evidence_confidence: {confidence_reason}",
            {
                "published_axis_used_as_bounded_prior": published_axis,
                "score_cap_without_history": 3,
                "related_severe_open_backlog_count": severe_backlog_count,
                "generation_changed_files_count": changed_files_count,
                "confidence": confidence,
                "v1_1_position": "missing_history_limits_confidence_not_score_by_itself",
            },
        ],
        "calibration": "v1_1",
    }


def compare_maturity(published: Dict[str, Any], computed_score: int) -> Dict[str, Any]:
    published_score = published.get("score_total")
    published_level = published.get("level")
    computed_level = maturity_level_from_score(computed_score)

    score_delta = None
    if isinstance(published_score, int):
        score_delta = computed_score - published_score

    level_delta = "unknown"
    action_required = False
    severity = "none"

    if isinstance(published_level, str):
        published_rank = level_rank(published_level)
        computed_rank = level_rank(computed_level)
        if computed_rank < published_rank:
            level_delta = "computed_lower_than_published"
            action_required = True
            severity = "fail"
        elif computed_rank > published_rank:
            level_delta = "computed_higher_than_published"
            severity = "warn"
        else:
            level_delta = "none"
            if score_delta not in (None, 0):
                severity = "warn"

    if score_delta is not None and abs(score_delta) >= 2:
        action_required = True
        if severity == "none":
            severity = "warn"

    return {
        "score_delta": score_delta,
        "level_delta": level_delta,
        "action_required": action_required,
        "severity": severity,
    }


def build_scope_result(
    *,
    scope_key: str,
    scope_def_doc: Dict[str, Any],
    policy_scope: Dict[str, Any],
    catalog_scope: Dict[str, Any],
    all_entries: Dict[str, Dict[str, Any]],
    owners_by_id: Dict[str, str],
    duplicate_owners_by_id: Dict[str, List[str]],
    backlog_entries: List[Dict[str, Any]],
    generation_report: Dict[str, Any],
) -> Dict[str, Any]:
    scope_root = scope_def_doc.get("scope_definition", {})
    target = scope_root.get("target", {})
    neighbors = scope_root.get("default_neighbors_to_read", {})
    maturity = scope_root.get("maturity", {})

    target_ids = sorted([id_ for id_ in target.get("ids", []) or [] if isinstance(id_, str)])
    neighbor_ids = set(id_ for id_ in neighbors.get("ids", []) or [] if isinstance(id_, str))
    neighbor_files = set(path for path in neighbors.get("files", []) or [] if isinstance(path, str))
    watchpoints = scope_root.get("watchpoints", []) or []

    published_axes = {}
    policy_maturity = policy_scope.get("maturity", {}) if isinstance(policy_scope, dict) else {}
    if isinstance(policy_maturity.get("axes"), dict):
        published_axes = policy_maturity["axes"]

    published_maturity = {
        "source": "policy.yaml",
        "axes": policy_maturity.get("axes", maturity.get("axes", {})),
        "score_total": policy_maturity.get("score_total", maturity.get("score_total")),
        "level": policy_maturity.get("level", maturity.get("level")),
        "rationale": policy_maturity.get("rationale", maturity.get("rationale", [])),
    }

    catalog_maturity = catalog_scope.get("maturity", {}) if isinstance(catalog_scope, dict) else {}

    missing_target_ids = sorted(id_ for id_ in target_ids if id_ not in all_entries)
    duplicate_ids_for_scope = {
        id_: owners
        for id_, owners in duplicate_owners_by_id.items()
        if id_ in target_ids
    }

    edges = compute_scope_edges(
        target_ids=target_ids,
        neighbor_ids=neighbor_ids,
        neighbor_files=neighbor_files,
        all_entries=all_entries,
        owners_by_id=owners_by_id,
        scope_key=scope_key,
    )

    axis_scores = {
        "clarity_of_scope": score_clarity(scope_root, published_axes),
        "internal_coherence": score_internal_coherence(target_ids, all_entries, owners_by_id, scope_key),
        "inter_scope_boundaries": score_boundaries(
            missing_target_ids=missing_target_ids,
            duplicate_owned_ids=duplicate_ids_for_scope,
            edges=edges,
            backlog_entries=backlog_entries,
        ),
        "dependency_explicitness": score_dependency_explicitness(edges),
        "bounded_run_executability": score_bounded_run_executability(
            target_ids,
            neighbor_ids,
            neighbor_files,
            watchpoints,
            backlog_entries,
        ),
        "inter_release_stability": score_inter_release_stability(
            published_axes,
            backlog_entries,
            generation_report,
        ),
    }

    computed_score = sum(axis_scores[axis]["score"] for axis in AXES)
    computed_maturity = {
        "score_total": computed_score,
        "level": maturity_level_from_score(computed_score),
        "max_score": MATURITY_MAX_SCORE,
    }

    delta = compare_maturity(published_maturity, computed_score)

    recommendations = []
    if delta["action_required"]:
        recommendations.append("review_published_maturity_before_authority_change")
    elif delta["severity"] == "warn":
        recommendations.append("record_delta_as_non_blocking_or_arbitrate")
    else:
        recommendations.append("keep_published_score")

    related_backlog_summary = [
        {
            "entry_id": entry.get("entry_id"),
            "type": entry.get("type"),
            "status": entry.get("status"),
            "title": entry.get("title"),
        }
        for entry in backlog_entries
    ]

    return {
        "scope_key": scope_key,
        "scope_id": scope_root.get("scope_id") or policy_scope.get("scope_id") or catalog_scope.get("scope_id"),
        "published_maturity": published_maturity,
        "catalog_maturity": catalog_maturity,
        "computed_maturity": computed_maturity,
        "axis_scores": axis_scores,
        "diagnostic_metrics": {
            "target_id_count": len(target_ids),
            "neighbor_id_count": len(neighbor_ids),
            "neighbor_file_count": len(neighbor_files),
            "watchpoint_count": len(watchpoints),
            "internal_edge_count": len(edges["internal_edges"]),
            "outgoing_edge_count": len(edges["outgoing_edges"]),
            "covered_outgoing_edge_count": len(edges["covered_outgoing_edges"]),
            "uncovered_outgoing_edge_count": len(edges["uncovered_outgoing_edges"]),
            "missing_target_edge_count": len(edges["missing_target_edges"]),
            "missing_target_ids": missing_target_ids,
            "duplicate_owned_ids": duplicate_ids_for_scope,
        },
        "related_open_backlog_entries": related_backlog_summary,
        "delta": delta,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute deterministic post-scoping maturity report for Constitution scopes."
    )
    parser.add_argument("--runs-index", default="docs/pipelines/constitution/runs/index.yaml")
    parser.add_argument("--constitution", default="docs/cores/current/constitution.yaml")
    parser.add_argument("--referentiel", default="docs/cores/current/referentiel.yaml")
    parser.add_argument("--link", default="docs/cores/current/link.yaml")
    parser.add_argument("--policy", default="docs/pipelines/constitution/policies/scope_generation/policy.yaml")
    parser.add_argument("--decisions", default="docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
    parser.add_argument("--catalog", default="docs/pipelines/constitution/scope_catalog/manifest.yaml")
    parser.add_argument("--scope-definitions-dir", default="docs/pipelines/constitution/scope_catalog/scope_definitions")
    parser.add_argument("--partition-report", default="docs/pipelines/constitution/reports/scope_partition_review_report.yaml")
    parser.add_argument("--generation-report", default="tmp/constitution_scope_generation_report.yaml")
    parser.add_argument("--governance-backlog", default="docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
    parser.add_argument("--report", default="docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()

    blocking_findings: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    required_refs = {
        "runs_index": args.runs_index,
        "constitution": args.constitution,
        "referentiel": args.referentiel,
        "link": args.link,
        "policy": args.policy,
        "decisions": args.decisions,
        "catalog": args.catalog,
        "partition_report": args.partition_report,
        "generation_report": args.generation_report,
    }

    runs_index = read_required_yaml(repo_root, args.runs_index, blocking_findings)
    constitution = read_required_yaml(repo_root, args.constitution, blocking_findings)
    referentiel = read_required_yaml(repo_root, args.referentiel, blocking_findings)
    link = read_required_yaml(repo_root, args.link, blocking_findings)
    policy = read_required_yaml(repo_root, args.policy, blocking_findings)
    decisions = read_required_yaml(repo_root, args.decisions, blocking_findings)
    catalog = read_required_yaml(repo_root, args.catalog, blocking_findings)
    partition_report = read_required_yaml(repo_root, args.partition_report, blocking_findings)
    generation_report = read_required_yaml(repo_root, args.generation_report, blocking_findings)

    # decisions are currently loaded to make the dependency explicit and to keep
    # the CLI/input contract stable for future scoring refinements.
    _ = decisions

    governance_backlog = load_yaml_optional(repo_root / args.governance_backlog)
    if not governance_backlog:
        warnings.append(
            {
                "finding_id": "OPTIONAL_GOVERNANCE_BACKLOG_MISSING_OR_EMPTY",
                "severity": "warning",
                "message": f"Optional governance backlog not loaded: {args.governance_backlog}",
            }
        )

    active_runs = active_constitution_runs(runs_index)
    if active_runs:
        blocking_findings.append(
            {
                "finding_id": "ACTIVE_CONSTITUTION_RUNS_PRESENT",
                "severity": "blocking",
                "message": "Stage 00 scoring must not run while constitution runs are active.",
                "active_run_count": len(active_runs),
                "active_runs": active_runs,
            }
        )

    scope_dir = repo_root / args.scope_definitions_dir
    scope_defs = collect_scope_definitions(scope_dir)
    if not scope_dir.exists():
        blocking_findings.append(
            {
                "finding_id": "MISSING_SCOPE_DEFINITIONS_DIR",
                "severity": "blocking",
                "message": f"Scope definitions directory is missing: {args.scope_definitions_dir}",
            }
        )

    policy_scopes = collect_policy_scopes(policy)
    catalog_scopes = collect_catalog_scopes(catalog)

    all_scope_keys = sorted(set(policy_scopes) | set(catalog_scopes) | set(scope_defs))
    for scope_key in sorted(set(catalog_scopes) - set(scope_defs)):
        blocking_findings.append(
            {
                "finding_id": f"MISSING_SCOPE_DEFINITION::{scope_key}",
                "severity": "blocking",
                "message": f"Catalog publishes scope but generated scope definition is missing: {scope_key}",
            }
        )
    for scope_key in sorted(set(scope_defs) - set(catalog_scopes)):
        warnings.append(
            {
                "finding_id": f"SCOPE_DEFINITION_NOT_IN_CATALOG::{scope_key}",
                "severity": "warning",
                "message": f"Scope definition exists but manifest does not publish it: {scope_key}",
            }
        )

    all_entries = collect_all_entries(
        constitution,
        referentiel,
        link,
        refs={
            "constitution": args.constitution,
            "referentiel": args.referentiel,
            "link": args.link,
        },
    )
    owners_by_id, duplicate_owners_by_id = build_owner_maps(scope_defs)
    backlog_by_scope = collect_open_backlog_by_scope(governance_backlog)

    partition_status = partition_report.get("scope_partition_review_report", {}).get("status")
    if partition_status and partition_status not in ("READY_FOR_SEMANTIC_REVIEW", "PASS"):
        warnings.append(
            {
                "finding_id": "PARTITION_REPORT_STATUS_NOT_PASS_LIKE",
                "severity": "warning",
                "message": "Partition report status is not PASS-like.",
                "partition_report_status": partition_status,
            }
        )

    scope_results: List[Dict[str, Any]] = []
    for scope_key in all_scope_keys:
        if scope_key not in scope_defs:
            continue
        scope_results.append(
            build_scope_result(
                scope_key=scope_key,
                scope_def_doc=scope_defs.get(scope_key, {}),
                policy_scope=policy_scopes.get(scope_key, {}),
                catalog_scope=catalog_scopes.get(scope_key, {}),
                all_entries=all_entries,
                owners_by_id=owners_by_id,
                duplicate_owners_by_id=duplicate_owners_by_id,
                backlog_entries=backlog_by_scope.get(scope_key, []),
                generation_report=generation_report,
            )
        )

    fail_deltas = [
        {
            "scope_key": result["scope_key"],
            "published_level": result["published_maturity"].get("level"),
            "computed_level": result["computed_maturity"].get("level"),
            "score_delta": result["delta"].get("score_delta"),
        }
        for result in scope_results
        if result.get("delta", {}).get("severity") == "fail"
    ]

    warn_deltas = [
        {
            "scope_key": result["scope_key"],
            "published_level": result["published_maturity"].get("level"),
            "computed_level": result["computed_maturity"].get("level"),
            "score_delta": result["delta"].get("score_delta"),
        }
        for result in scope_results
        if result.get("delta", {}).get("severity") == "warn"
    ]

    if fail_deltas:
        blocking_findings.append(
            {
                "finding_id": "COMPUTED_MATURITY_LOWER_THAN_PUBLISHED",
                "severity": "blocking",
                "message": "At least one computed maturity level is lower than the published governed level.",
                "items": fail_deltas,
            }
        )

    if warn_deltas:
        warnings.append(
            {
                "finding_id": "COMPUTED_MATURITY_DELTA_NON_BLOCKING",
                "severity": "warning",
                "message": "At least one computed score differs from the published score without lowering the level.",
                "items": warn_deltas,
            }
        )

    if blocking_findings:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    input_refs = [
        input_record(repo_root, ref, required=True)
        for ref in required_refs.values()
    ] + [
        input_record(repo_root, args.governance_backlog, required=False),
    ]

    report = {
        "scope_maturity_scoring_report": {
            "schema_version": 0.1,
            "pipeline_id": "constitution",
            "status": status,
            "authority": "diagnostic_report_only",
            "does_not_update_policy": True,
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "catalog_manifest": "not_modified",
                "scope_definitions": "not_modified",
            },
            "inputs": input_refs,
            "scoring_model": {
                "ref": "docs/transformations/core_modularization/CONSTITUTION_SCOPE_MATURITY_MODEL.md",
                "max_score": MATURITY_MAX_SCORE,
                "axes": AXES,
                "levels": [
                    {"level": level, "min": lo, "max": hi}
                    for level, lo, hi in MATURITY_LEVELS
                ],
            },
            "summary": {
                "scope_count": len(scope_results),
                "blocking_finding_count": len(blocking_findings),
                "warning_count": len(warnings),
                "computed_lower_than_published_count": len(fail_deltas),
                "computed_delta_non_blocking_count": len(warn_deltas),
            },
            "scope_results": scope_results,
            "blocking_findings": blocking_findings,
            "warnings": warnings,
            "notes": [
                "This report is deterministic and non-publishing.",
                "policy.yaml remains authoritative for published maturity in V1.",
                "Computed maturity is a post-scoping diagnostic signal and must be arbitrated before any authority migration.",
                "The script writes only the report path passed with --report.",
            ],
        }
    }

    report_path = repo_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(dump_yaml(report), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
