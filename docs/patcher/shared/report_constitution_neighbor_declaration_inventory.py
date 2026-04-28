#!/usr/bin/env python3
"""Inventory Constitution neighbor declaration surfaces.

PHASE_18A deterministic, non-mutating report.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml


DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/constitution_neighbor_declaration_inventory_report.yaml")

POLICY = Path("docs/pipelines/constitution/policies/scope_generation/policy.yaml")
DECISIONS = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
MANIFEST = Path("docs/pipelines/constitution/scope_catalog/manifest.yaml")
SCOPE_DEFS_DIR = Path("docs/pipelines/constitution/scope_catalog/scope_definitions")
PIPELINE = Path("docs/pipelines/constitution/pipeline.md")
STAGE00 = Path("docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md")
RUNS_DIR = Path("docs/pipelines/constitution/runs")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def get_mapping(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}.")
    return value


def stable_list(values: Iterable[Any]) -> List[str]:
    return sorted(set(str(v) for v in values if str(v).strip()))


def nested_get(obj: Any, path: List[str]) -> Any:
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def collect_policy_surfaces(policy_doc: Dict[str, Any]) -> Dict[str, Any]:
    root = get_mapping(policy_doc, "scope_generation_policy")
    shared_read_surface = nested_get(root, ["shared_defaults", "read_surface"]) or {}
    core_role = root.get("core_role_classification") or {}
    id_contract = root.get("id_classification_contract") or {}
    declared_scopes = root.get("declared_scopes") or []

    policy_scope_neighbor_files = []
    for scope in declared_scopes:
        if not isinstance(scope, dict):
            continue
        policy_scope_neighbor_files.append({
            "scope_key": scope.get("scope_key"),
            "neighbor_files": stable_list(scope.get("neighbor_files") or []),
            "target_files": stable_list(scope.get("target_files") or []),
        })

    return {
        "shared_read_surface": {
            "mode": shared_read_surface.get("mode"),
            "fallback_files": stable_list(shared_read_surface.get("fallback_files") or []),
            "fallback_trigger_conditions": stable_list(shared_read_surface.get("fallback_trigger_conditions") or []),
        },
        "declared_scope_neighbor_files": policy_scope_neighbor_files,
        "core_role_classification": {
            "owned_core_family": core_role.get("owned_core_family"),
            "owned_core_files": stable_list(core_role.get("owned_core_files") or []),
            "external_read_only_core_files": stable_list(core_role.get("external_read_only_core_files") or []),
            "default_cross_core_write_policy": core_role.get("default_cross_core_write_policy"),
        },
        "id_classification_contract_keys": stable_list(id_contract.keys() if isinstance(id_contract, dict) else []),
    }


def collect_decision_surfaces(decisions_doc: Dict[str, Any]) -> Dict[str, Any]:
    root = get_mapping(decisions_doc, "scope_generation_decisions")
    decisions = root.get("decisions") or []
    by_type = Counter()
    by_status = Counter()
    force_neighbor_decisions = []
    external_core_decisions = []
    proposed_neighbor_placeholders = []

    for decision in decisions:
        if not isinstance(decision, dict):
            continue

        decision_type = str(decision.get("decision_type"))
        status = str(decision.get("status"))
        by_type[decision_type] += 1
        by_status[status] += 1

        if decision_type == "force_logical_neighbors":
            payload = decision.get("decision_payload") or {}
            entry = {
                "decision_id": decision.get("decision_id"),
                "status": status,
                "scope_keys_affected": stable_list(decision.get("scope_keys_affected") or []),
                "target_id_count": len(decision.get("target_ids") or []),
                "target_ids": stable_list(decision.get("target_ids") or []),
                "neighbor_class": payload.get("neighbor_class") if isinstance(payload, dict) else None,
                "read_mode": payload.get("read_mode") if isinstance(payload, dict) else None,
                "source_phase": payload.get("source_phase") if isinstance(payload, dict) else None,
                "superseded_by_decision_id": payload.get("superseded_by_decision_id") if isinstance(payload, dict) else None,
                "superseded_by_phase": payload.get("superseded_by_phase") if isinstance(payload, dict) else None,
                "requires_exact_id_selection_before_approval": bool(
                    isinstance(payload, dict) and payload.get("requires_exact_id_selection_before_approval") is True
                ),
            }
            force_neighbor_decisions.append(entry)
            is_superseded = status.startswith("superseded")
            if (status != "approved" and not is_superseded) or (
                entry["requires_exact_id_selection_before_approval"] and not is_superseded
            ):
                proposed_neighbor_placeholders.append(entry)

        if decision_type == "classify_external_read_only_cores":
            payload = decision.get("decision_payload") or {}
            external_core_decisions.append({
                "decision_id": decision.get("decision_id"),
                "status": status,
                "scope_keys_affected": stable_list(decision.get("scope_keys_affected") or []),
                "target_core_files": stable_list(decision.get("target_core_files") or []),
                "external_id_classes": stable_list(payload.get("external_id_classes") or []) if isinstance(payload, dict) else [],
                "read_mode": payload.get("read_mode") if isinstance(payload, dict) else None,
                "write_policy": payload.get("write_policy") if isinstance(payload, dict) else None,
            })

    return {
        "decision_count": len([d for d in decisions if isinstance(d, dict)]),
        "decision_count_by_type": dict(sorted(by_type.items())),
        "decision_count_by_status": dict(sorted(by_status.items())),
        "force_logical_neighbors": sorted(force_neighbor_decisions, key=lambda x: str(x.get("decision_id"))),
        "external_read_only_core_decisions": sorted(external_core_decisions, key=lambda x: str(x.get("decision_id"))),
        "non_approved_or_placeholder_neighbor_decisions": sorted(
            proposed_neighbor_placeholders, key=lambda x: str(x.get("decision_id"))
        ),
    }


def read_scope_def(path: Path) -> Dict[str, Any]:
    doc = load_yaml(path)
    if isinstance(doc, dict) and len(doc) == 1 and isinstance(next(iter(doc.values())), dict):
        return next(iter(doc.values()))
    return doc if isinstance(doc, dict) else {}


def collect_scope_definition_surfaces() -> Dict[str, Any]:
    scope_files = sorted(SCOPE_DEFS_DIR.glob("*.yaml"))
    scope_entries = []
    key_counter = Counter()
    neighbor_id_total = 0
    neighbor_file_total = 0

    interesting_keys = [
        "default_neighbors_to_read",
        "neighbor_files",
        "neighbor_ids",
        "target_ids",
        "target_files",
        "external_read_only_core_files",
        "read_surface",
        "scope_extract",
        "neighbor_extract",
    ]

    for path in scope_files:
        scope = read_scope_def(path)
        scope_key = scope.get("scope_key") or scope.get("key") or path.stem
        found = {}
        for key in interesting_keys:
            value = scope.get(key)
            if value is not None:
                key_counter[key] += 1
                found[key] = value

        default_neighbors = scope.get("default_neighbors_to_read") or {}
        default_neighbor_ids = []
        default_neighbor_files = []
        if isinstance(default_neighbors, dict):
            default_neighbor_ids = stable_list(default_neighbors.get("ids") or [])
            default_neighbor_files = stable_list(default_neighbors.get("files") or [])
        elif isinstance(default_neighbors, list):
            default_neighbor_ids = stable_list(default_neighbors)

        neighbor_files = stable_list(scope.get("neighbor_files") or [])
        neighbor_ids = stable_list(scope.get("neighbor_ids") or [])
        neighbor_id_total += len(default_neighbor_ids) + len(neighbor_ids)
        neighbor_file_total += len(default_neighbor_files) + len(neighbor_files)

        scope_entries.append({
            "scope_key": scope_key,
            "path": normalize_path(path),
            "declared_surface_keys": sorted(found.keys()),
            "default_neighbor_id_count": len(default_neighbor_ids),
            "default_neighbor_ids": default_neighbor_ids,
            "neighbor_id_count": len(neighbor_ids),
            "neighbor_ids": neighbor_ids,
            "default_neighbor_file_count": len(default_neighbor_files),
            "default_neighbor_files": default_neighbor_files,
            "neighbor_file_count": len(neighbor_files),
            "neighbor_files": neighbor_files,
        })

    return {
        "scope_definition_count": len(scope_files),
        "surface_key_presence_count": dict(sorted(key_counter.items())),
        "total_generated_neighbor_id_references": neighbor_id_total,
        "total_generated_neighbor_file_references": neighbor_file_total,
        "scopes": scope_entries,
    }


def collect_run_extract_surfaces() -> Dict[str, Any]:
    if not RUNS_DIR.exists():
        return {"run_extract_file_count": 0, "scope_extract_count": 0, "neighbor_extract_count": 0, "files": []}

    files = []
    for path in sorted(RUNS_DIR.glob("*/inputs/*extract*.yaml")):
        kind = "neighbor_extract" if "neighbor_extract" in path.name else "scope_extract" if "scope_extract" in path.name else "other_extract"
        try:
            doc = load_yaml(path)
        except SystemExit:
            doc = {}
        counts = {}
        if isinstance(doc, dict):
            for key in ["ids", "target_ids", "neighbor_ids", "items", "entries", "nodes"]:
                value = doc.get(key)
                if isinstance(value, list):
                    counts[key] = len(value)
                elif isinstance(value, dict):
                    counts[key] = len(value)

        files.append({
            "path": normalize_path(path),
            "kind": kind,
            "top_level_keys": sorted(doc.keys()) if isinstance(doc, dict) else [],
            "counts": counts,
        })

    return {
        "run_extract_file_count": len(files),
        "scope_extract_count": sum(1 for f in files if f["kind"] == "scope_extract"),
        "neighbor_extract_count": sum(1 for f in files if f["kind"] == "neighbor_extract"),
        "files": files,
    }


def collect_pipeline_doc_surfaces() -> Dict[str, Any]:
    pipeline_text = PIPELINE.read_text(encoding="utf-8") if PIPELINE.exists() else ""
    stage00_text = STAGE00.read_text(encoding="utf-8") if STAGE00.exists() else ""
    expected_script_refs = [
        "score_constitution_scope_maturity.py",
        "apply_constitution_scope_maturity_scores.py",
        "report_constitution_neighbor_ids_governance.py",
        "prepare_constitution_neighbor_ids_arbitration.py",
        "validate_constitution_neighbor_ids_arbitration.py",
        "apply_constitution_neighbor_ids_arbitration.py",
        "extract_scope_slice.py",
        "materialize_run_inputs.py",
    ]

    return {
        "pipeline_md_script_refs": {ref: (ref in pipeline_text) for ref in expected_script_refs},
        "stage00_script_refs": {ref: (ref in stage00_text) for ref in expected_script_refs},
        "pipeline_md_needs_resource_index_update": any(
            ref not in pipeline_text
            for ref in [
                "score_constitution_scope_maturity.py",
                "apply_constitution_scope_maturity_scores.py",
                "report_constitution_neighbor_ids_governance.py",
                "apply_constitution_neighbor_ids_arbitration.py",
            ]
        ),
        "stage00_contains_score_publication_chain": "apply_constitution_scope_maturity_scores.py" in stage00_text,
        "stage00_contains_neighbor_ids_governance_chain": "report_constitution_neighbor_ids_governance.py" in stage00_text,
    }


def derive_findings(decision_surfaces: Dict[str, Any], pipeline_surfaces: Dict[str, Any], scope_surfaces: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    placeholders = decision_surfaces.get("non_approved_or_placeholder_neighbor_decisions") or []

    if placeholders:
        findings.append({
            "finding_id": "NEIGHBOR_DECISION_PLACEHOLDER_PRESENT",
            "severity": "info",
            "message": "At least one force_logical_neighbors decision is not approved or still requires exact ID selection.",
            "items": [
                {
                    "decision_id": item.get("decision_id"),
                    "status": item.get("status"),
                    "requires_exact_id_selection_before_approval": item.get("requires_exact_id_selection_before_approval"),
                }
                for item in placeholders
            ],
        })

    if pipeline_surfaces.get("pipeline_md_needs_resource_index_update"):
        findings.append({
            "finding_id": "PIPELINE_RESOURCE_INDEX_MISSING_RECENT_STAGE00_SCRIPTS",
            "severity": "warning",
            "message": "pipeline.md does not list all recent STAGE_00 scoring and neighbor-governance scripts, although STAGE_00 itself is updated.",
            "items": [
                ref for ref, present in pipeline_surfaces.get("pipeline_md_script_refs", {}).items()
                if not present
            ],
        })

    if not pipeline_surfaces.get("stage00_contains_score_publication_chain"):
        findings.append({
            "finding_id": "STAGE00_MISSING_SCORE_PUBLICATION_CHAIN",
            "severity": "error",
            "message": "STAGE_00 does not reference the maturity score publication patcher.",
            "items": [],
        })

    if not pipeline_surfaces.get("stage00_contains_neighbor_ids_governance_chain"):
        findings.append({
            "finding_id": "STAGE00_MISSING_NEIGHBOR_IDS_GOVERNANCE_CHAIN",
            "severity": "error",
            "message": "STAGE_00 does not reference the neighbor IDs governance chain.",
            "items": [],
        })

    if scope_surfaces.get("scope_definition_count", 0) == 0:
        findings.append({
            "finding_id": "NO_SCOPE_DEFINITIONS_FOUND",
            "severity": "error",
            "message": "No generated scope definitions found.",
            "items": [],
        })

    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory Constitution neighbor declaration surfaces.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required = [POLICY, DECISIONS, MANIFEST, PIPELINE, STAGE00]
    for path in required:
        sha256_file(path)

    policy_doc = load_yaml(POLICY)
    decisions_doc = load_yaml(DECISIONS)
    policy_surfaces = collect_policy_surfaces(policy_doc)
    decision_surfaces = collect_decision_surfaces(decisions_doc)
    scope_surfaces = collect_scope_definition_surfaces()
    run_extract_surfaces = collect_run_extract_surfaces()
    pipeline_surfaces = collect_pipeline_doc_surfaces()

    findings = derive_findings(decision_surfaces, pipeline_surfaces, scope_surfaces)
    severity_counts = Counter(finding["severity"] for finding in findings)
    status = "FAIL" if severity_counts.get("error", 0) else "WARN" if severity_counts.get("warning", 0) else "PASS"

    report = {
        "constitution_neighbor_declaration_inventory_report": {
            "schema_version": "0.1",
            "phase_id": "PHASE_18A",
            "generated_at": iso_now(),
            "status": status,
            "mutation_policy": {
                "policy_yaml": "not_modified",
                "decisions_yaml": "not_modified",
                "catalog_manifest": "not_modified",
                "scope_definitions": "not_modified",
                "pipeline_docs": "not_modified",
                "cores": "not_modified",
            },
            "inputs": [{"ref": normalize_path(path), "sha256": sha256_file(path)} for path in required],
            "summary": {
                "policy_declared_scope_count": len(policy_surfaces.get("declared_scope_neighbor_files", [])),
                "force_logical_neighbor_decision_count": len(decision_surfaces.get("force_logical_neighbors", [])),
                "external_read_only_core_decision_count": len(decision_surfaces.get("external_read_only_core_decisions", [])),
                "scope_definition_count": scope_surfaces.get("scope_definition_count", 0),
                "run_extract_file_count": run_extract_surfaces.get("run_extract_file_count", 0),
                "finding_count": len(findings),
                "warning_count": severity_counts.get("warning", 0),
                "error_count": severity_counts.get("error", 0),
            },
            "surfaces": {
                "policy": policy_surfaces,
                "decisions": decision_surfaces,
                "generated_scope_definitions": scope_surfaces,
                "run_extracts": run_extract_surfaces,
                "pipeline_docs": pipeline_surfaces,
            },
            "findings": findings,
            "recommended_next_steps": [
                "Patch pipeline.md canonical resources to list recent STAGE_00 scoring and neighbor-governance scripts.",
                "Arbitrate whether proposed SGEN_DECISION_011 remains a placeholder, is superseded by PHASE_16, or should be closed.",
                "Define which neighbor declaration surfaces are canonical inputs versus generated outputs.",
                "Align validators and materialization scripts with the accepted declaration model after arbitration.",
            ],
        }
    }

    write_yaml(Path(args.report), report)
    print(f"Wrote {args.report}")
    print(f"Status: {status}")
    print(f"Findings: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
