#!/usr/bin/env python3
"""Materialize the three deterministic input files for a bounded pipeline run.

For a given run_id, reads:
  - runs/<run_id>/run_manifest.yaml          -> resolves scope_key + scope_definition_ref
  - scope_catalog/scope_definitions/<scope_key>.yaml -> authoritative source of truth
  - reports/scope_partition_review_report.yaml (optional) -> cross-scope edges for impact_bundle

Produces (deterministically, no AI required):
  - runs/<run_id>/inputs/scope_manifest.yaml
  - runs/<run_id>/inputs/impact_bundle.yaml
  - runs/<run_id>/inputs/integration_gate.yaml

All three files are idempotent: re-running overwrites with the same content
as long as the scope_definition has not changed.

scope_key resolution order (robustness):
  1. run_manifest.scope_key          (canonical, top-level field)
  2. run_manifest.scope_binding.scope_key  (fallback for older manifests)

Integration in pipeline.md:
  Spec and tools section — called before STAGE_01_CHALLENGE.
  Command:
    python docs/patcher/shared/materialize_run_inputs.py --run-id <RUN_ID>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required.") from exc


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data or {}


def load_yaml_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data or {}


def dump_yaml(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# scope_key resolution (robust)
# ---------------------------------------------------------------------------

def resolve_scope_key(run_meta: Dict[str, Any]) -> str | None:
    """Resolve scope_key with fallback to scope_binding.scope_key.

    Resolution order:
      1. run_manifest.scope_key          (canonical top-level field)
      2. run_manifest.scope_binding.scope_key  (fallback for older manifests)
    """
    # 1. canonical top-level
    scope_key = run_meta.get("scope_key")
    if scope_key:
        return scope_key
    # 2. fallback via scope_binding
    scope_binding = run_meta.get("scope_binding") or {}
    return scope_binding.get("scope_key")


# ---------------------------------------------------------------------------
# Scope manifest
# ---------------------------------------------------------------------------

def build_scope_manifest(
    run_id: str,
    scope_def: Dict[str, Any],
    scope_def_fingerprint: str,
) -> Dict[str, Any]:
    """Derive scope_manifest from scope_definition.target + governance."""
    sd = scope_def.get("scope_definition", {})
    target = sd.get("target", {})
    governance = sd.get("governance", {})

    return {
        "scope_manifest": {
            "schema_version": 0.1,
            "run_id": run_id,
            "scope_id": sd.get("scope_id"),
            "scope_key": sd.get("scope_key"),
            "source": {
                "scope_definition_ref": f"docs/pipelines/constitution/scope_catalog/scope_definitions/{sd.get('scope_key')}.yaml",
                "scope_definition_fingerprint": scope_def_fingerprint,
            },
            "writable_perimeter": {
                "files": target.get("files", []),
                "modules": target.get("modules", []),
                "ids": sorted(target.get("ids", [])),
            },
            "governance": {
                "allowed_operations": governance.get("default_allowed_operations", []),
                "forbidden_operations": governance.get("default_forbidden_operations", []),
                "scope_extension_policy": governance.get("scope_extension_policy", {}),
            },
            "notes": [
                "Généré déterministiquement par materialize_run_inputs.py depuis la scope_definition.",
                "Ce fichier déclare le périmètre modifiable autorisé du run.",
                "Tout ce qui n'est pas dans writable_perimeter.ids ne peut pas être modifié implicitement.",
            ],
        }
    }


# ---------------------------------------------------------------------------
# Impact bundle
# ---------------------------------------------------------------------------

def extract_cross_scope_edges(
    partition_report: Dict[str, Any],
    scope_key: str,
) -> List[Dict[str, Any]]:
    """Extract cross-scope edges involving this scope from the partition report."""
    signals = (
        partition_report
        .get("scope_partition_review_report", {})
        .get("partition_signals", {})
    )
    edges = signals.get("cross_scope_edges", []) or []
    relevant: List[Dict[str, Any]] = []
    for edge in edges:
        if edge.get("from") == scope_key or edge.get("to") == scope_key:
            relevant.append(edge)
    return sorted(relevant, key=lambda e: -e.get("edge_count", 0))


def build_impact_bundle(
    run_id: str,
    scope_def: Dict[str, Any],
    partition_report: Dict[str, Any],
    scope_def_fingerprint: str,
) -> Dict[str, Any]:
    """Derive impact_bundle from default_neighbors_to_read + cross-scope edges."""
    sd = scope_def.get("scope_definition", {})
    scope_key = sd.get("scope_key")
    neighbors = sd.get("default_neighbors_to_read", {})
    cross_edges = extract_cross_scope_edges(partition_report, scope_key)

    neighbor_scopes: List[Dict[str, Any]] = []
    seen: set = set()
    for edge in cross_edges:
        direction = "outgoing" if edge.get("from") == scope_key else "incoming"
        other = edge.get("to") if direction == "outgoing" else edge.get("from")
        if other and other not in seen:
            seen.add(other)
            neighbor_scopes.append({
                "scope_key": other,
                "direction": direction,
                "edge_count": edge.get("edge_count", 0),
                "read_required": True,
                "modify_allowed": False,
            })

    return {
        "impact_bundle": {
            "schema_version": 0.1,
            "run_id": run_id,
            "scope_id": sd.get("scope_id"),
            "scope_key": scope_key,
            "source": {
                "scope_definition_ref": f"docs/pipelines/constitution/scope_catalog/scope_definitions/{scope_key}.yaml",
                "scope_definition_fingerprint": scope_def_fingerprint,
                "partition_report_used": bool(partition_report),
            },
            "mandatory_reads": {
                "files": neighbors.get("files", []),
                "ids": sorted(neighbors.get("ids", [])),
            },
            "neighbor_scopes": neighbor_scopes,
            "notes": [
                "Généré déterministiquement par materialize_run_inputs.py.",
                "Ce fichier étend le devoir de lecture, pas le droit de modifier.",
                "neighbor_scopes dérivés des cross_scope_edges du rapport de partition.",
                "Un voisin absent de ce fichier mais découvert pendant le run doit être signalé explicitement.",
            ],
        }
    }


# ---------------------------------------------------------------------------
# Integration gate
# ---------------------------------------------------------------------------

def build_integration_gate(
    run_id: str,
    scope_def: Dict[str, Any],
    scope_def_fingerprint: str,
) -> Dict[str, Any]:
    """Derive integration_gate from watchpoints + governance.forbidden_operations."""
    sd = scope_def.get("scope_definition", {})
    scope_key = sd.get("scope_key")
    governance = sd.get("governance", {})
    watchpoints = sd.get("watchpoints", []) or []
    forbidden_ops = governance.get("default_forbidden_operations", [])

    gate_checks = [
        {
            "check_id": f"WP_{i + 1:02d}",
            "description": wp,
            "source": "watchpoint",
            "clearance_required": True,
            "cleared": False,
        }
        for i, wp in enumerate(watchpoints)
    ]

    if forbidden_ops:
        gate_checks.append({
            "check_id": "FORBIDDEN_OPS_ENFORCEMENT",
            "description": "Vérifier qu'aucune opération interdite n'a été effectuée pendant le run.",
            "forbidden_operations": forbidden_ops,
            "source": "governance.default_forbidden_operations",
            "clearance_required": True,
            "cleared": False,
        })

    return {
        "integration_gate": {
            "schema_version": 0.1,
            "run_id": run_id,
            "scope_id": sd.get("scope_id"),
            "scope_key": scope_key,
            "status": "open",
            "source": {
                "scope_definition_ref": f"docs/pipelines/constitution/scope_catalog/scope_definitions/{scope_key}.yaml",
                "scope_definition_fingerprint": scope_def_fingerprint,
            },
            "promotion_blocked_until_cleared": True,
            "gate_checks": gate_checks,
            "clearance_record": [],
            "notes": [
                "Généré déterministiquement par materialize_run_inputs.py.",
                "Ce fichier déclare les contrôles globaux à rejouer avant release/promotion.",
                "En mode borné, il bloque toute promotion implicite d'un succès local.",
                "Chaque check doit être explicitement cleared avant que status puisse passer à 'cleared'.",
                "La clearance finale est un acte humain ou IA gouverné — pas automatique.",
            ],
        }
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize deterministic run input files from scope_definition."
    )
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--partition-report",
        default="docs/pipelines/constitution/reports/scope_partition_review_report.yaml",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    inputs_dir = run_root / "inputs"

    # Load run manifest
    run_manifest_path = run_root / "run_manifest.yaml"
    run_manifest = load_yaml(run_manifest_path)
    run_meta = run_manifest.get("run_manifest", {})

    # Resolve scope_key with fallback
    scope_key = resolve_scope_key(run_meta)
    if not scope_key:
        print(
            "ERROR: scope_key not found in run_manifest.yaml.\n"
            "  Expected: run_manifest.scope_key (canonical)\n"
            "  Fallback:  run_manifest.scope_binding.scope_key\n"
            "  Neither field is present or non-empty.",
            file=sys.stderr,
        )
        return 1

    scope_key_source = "scope_key" if run_meta.get("scope_key") else "scope_binding.scope_key (fallback)"
    print(f"[materialize_run_inputs] scope_key resolved from: {scope_key_source} -> {scope_key}")

    # Load scope definition
    scope_def_path = pipeline_root / "scope_catalog" / "scope_definitions" / f"{scope_key}.yaml"
    scope_def = load_yaml(scope_def_path)
    scope_def_fingerprint = sha256_file(scope_def_path)

    # Load partition report (optional)
    partition_report_path = repo_root / args.partition_report
    partition_report = load_yaml_optional(partition_report_path)
    if not partition_report:
        print("[materialize_run_inputs] partition report not found — impact_bundle.neighbor_scopes will be empty")

    # Generate the three files
    scope_manifest_data = build_scope_manifest(args.run_id, scope_def, scope_def_fingerprint)
    impact_bundle = build_impact_bundle(args.run_id, scope_def, partition_report, scope_def_fingerprint)
    integration_gate = build_integration_gate(args.run_id, scope_def, scope_def_fingerprint)

    # Write outputs
    inputs_dir.mkdir(parents=True, exist_ok=True)

    files_written = []
    for filename, content in [
        ("scope_manifest.yaml", scope_manifest_data),
        ("impact_bundle.yaml", impact_bundle),
        ("integration_gate.yaml", integration_gate),
    ]:
        out_path = inputs_dir / filename
        out_path.write_text(dump_yaml(content), encoding="utf-8")
        files_written.append(str(out_path.relative_to(repo_root)))
        print(f"[materialize_run_inputs] written: {out_path.relative_to(repo_root)}")

    result = {
        "materialize_run_inputs": {
            "status": "DONE",
            "run_id": args.run_id,
            "scope_key": scope_key,
            "scope_key_source": scope_key_source,
            "scope_definition_fingerprint": scope_def_fingerprint,
            "partition_report_used": bool(partition_report),
            "files_written": files_written,
        }
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
