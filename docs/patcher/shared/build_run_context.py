#!/usr/bin/env python3
"""Build a lightweight run_context.yaml for a bounded pipeline run.

For a given run_id, reads:
  - runs/<run_id>/run_manifest.yaml
  - runs/<run_id>/inputs/scope_manifest.yaml
  - runs/<run_id>/inputs/impact_bundle.yaml
  - runs/<run_id>/inputs/integration_gate.yaml
  - runs/<run_id>/inputs/scope_extract.yaml    (optional — enriches context if present)
  - runs/<run_id>/inputs/neighbor_extract.yaml (optional — enriches context if present)

Produces (deterministically, no AI required):
  - runs/<run_id>/inputs/run_context.yaml

Goal (J3 — minimal AI read surface):
  The AI working on any stage reads run_context.yaml as its FIRST and often ONLY
  file before loading scope_extract.yaml + neighbor_extract.yaml.
  This replaces 5–7 sequential reads (run_manifest, scope_manifest, impact_bundle,
  integration_gate, AI_PROTOCOL, pipeline.md, index.yaml) with a single synthesized file.

  run_context.yaml is a derived view. run_manifest + inputs remain authoritative.

Idempotent: re-running overwrites with the same content as long as source files are unchanged.

Integration in pipeline.md / materialize_run_inputs.py:
  Called after materialize_run_inputs.py + extract_scope_slice.py.
  Command:
    python docs/patcher/shared/build_run_context.py --run-id <RUN_ID>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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
        return yaml.safe_load(fh) or {}


def load_yaml_optional(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True,
                          default_flow_style=False, width=100)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Build run_context
# ---------------------------------------------------------------------------

def build_run_context(
    run_id: str,
    run_manifest: Dict[str, Any],
    scope_manifest: Dict[str, Any],
    impact_bundle: Dict[str, Any],
    integration_gate: Dict[str, Any],
    scope_extract: Optional[Dict[str, Any]],
    neighbor_extract: Optional[Dict[str, Any]],
    inputs_dir: Path,
) -> Dict[str, Any]:
    rm = run_manifest.get("run_manifest", {})
    sm = scope_manifest.get("scope_manifest", {})
    ib = impact_bundle.get("impact_bundle", {})
    ig = integration_gate.get("integration_gate", {})

    # Execution state
    exec_state = rm.get("execution_state", {})
    current_stage = exec_state.get("current_stage") or rm.get("current_stage")
    last_stage_status = exec_state.get("last_stage_status", "unknown")
    next_stage = exec_state.get("next_stage", current_stage)
    completed_stages: List[str] = exec_state.get("completed_stages", []) or []

    # Scope IDs
    scope_ids: List[str] = sm.get("writable_perimeter", {}).get("ids", [])
    neighbor_ids: List[str] = ib.get("mandatory_reads", {}).get("ids", [])

    # Integration gate summary
    gate_checks = ig.get("gate_checks", []) or []
    gate_cleared = [c for c in gate_checks if c.get("cleared")]
    gate_summary = {
        "status": ig.get("status", "unknown"),
        "total_checks": len(gate_checks),
        "cleared_checks": len(gate_cleared),
        "promotion_blocked": ig.get("promotion_blocked_until_cleared", True),
    }

    # Extract status
    scope_extract_status: Dict[str, Any] = {"present": False}
    neighbor_extract_status: Dict[str, Any] = {"present": False}

    if scope_extract is not None:
        se = scope_extract.get("scope_extract", {})
        scope_extract_status = {
            "present": True,
            "found_ids_count": len(se.get("found_ids", [])),
            "missing_ids_count": len(se.get("missing_ids", [])),
            "missing_ids": se.get("missing_ids", []),
            "ref": f"runs/{run_id}/inputs/scope_extract.yaml",
        }

    if neighbor_extract is not None:
        ne = neighbor_extract.get("neighbor_extract", {})
        neighbor_extract_status = {
            "present": True,
            "found_ids_count": len(ne.get("found_ids", [])),
            "missing_ids_count": len(ne.get("missing_ids", [])),
            "missing_ids": ne.get("missing_ids", []),
            "ref": f"runs/{run_id}/inputs/neighbor_extract.yaml",
        }

    # Source fingerprints
    fingerprints: Dict[str, str] = {}
    for fname in ["run_manifest.yaml", "scope_manifest.yaml",
                  "impact_bundle.yaml", "integration_gate.yaml",
                  "scope_extract.yaml", "neighbor_extract.yaml"]:
        fpath = inputs_dir.parent / fname if fname == "run_manifest.yaml" else inputs_dir / fname
        if fpath.exists():
            fingerprints[fname] = sha256_file(fpath)

    return {
        "run_context": {
            "schema_version": 0.1,
            "generated_by": "build_run_context.py",
            "note": (
                "Fichier synthétique — lire EN PREMIER. Remplace la lecture séquentielle de "
                "run_manifest + scope_manifest + impact_bundle + integration_gate. "
                "Sources canoniques inchangées."
            ),
            # --- Identity ---
            "run_id": run_id,
            "pipeline_id": rm.get("pipeline_id", "constitution"),
            "mode": rm.get("mode", "bounded_local_run"),
            "status": rm.get("status", "active"),
            "scope_key": rm.get("scope_key"),
            # --- Stage courant ---
            "current_stage": current_stage,
            "last_stage_status": last_stage_status,
            "next_stage": next_stage,
            "completed_stages": completed_stages,
            # --- IDs du scope ---
            "scope_ids": sorted(scope_ids),
            "scope_ids_count": len(scope_ids),
            # --- IDs voisinage ---
            "neighbor_ids": sorted(neighbor_ids),
            "neighbor_ids_count": len(neighbor_ids),
            # --- Statut des extraits (ids-first) ---
            "scope_extract": scope_extract_status,
            "neighbor_extract": neighbor_extract_status,
            # --- Gate summary ---
            "integration_gate": gate_summary,
            # --- Refs canoniques ---
            "canonical_refs": {
                "run_manifest": f"docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml",
                "scope_manifest": f"docs/pipelines/constitution/runs/{run_id}/inputs/scope_manifest.yaml",
                "impact_bundle": f"docs/pipelines/constitution/runs/{run_id}/inputs/impact_bundle.yaml",
                "integration_gate": f"docs/pipelines/constitution/runs/{run_id}/inputs/integration_gate.yaml",
            },
            # --- Fingerprints ---
            "source_fingerprints": fingerprints,
        }
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build run_context.yaml — lightweight AI entry point (J3 — minimal read surface)."
    )
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    inputs_dir = run_root / "inputs"

    # Required files
    run_manifest = load_yaml(run_root / "run_manifest.yaml")
    scope_manifest = load_yaml(inputs_dir / "scope_manifest.yaml")
    impact_bundle = load_yaml(inputs_dir / "impact_bundle.yaml")
    integration_gate = load_yaml(inputs_dir / "integration_gate.yaml")

    # Optional extracts (present after extract_scope_slice.py)
    scope_extract = load_yaml_optional(inputs_dir / "scope_extract.yaml")
    neighbor_extract = load_yaml_optional(inputs_dir / "neighbor_extract.yaml")

    if scope_extract is None:
        print("[build_run_context] scope_extract.yaml absent — run extract_scope_slice.py first for full context",
              file=sys.stderr)
    if neighbor_extract is None:
        print("[build_run_context] neighbor_extract.yaml absent — run extract_scope_slice.py first for full context",
              file=sys.stderr)

    print(f"[build_run_context] Building run_context for run: {args.run_id}")

    context = build_run_context(
        run_id=args.run_id,
        run_manifest=run_manifest,
        scope_manifest=scope_manifest,
        impact_bundle=impact_bundle,
        integration_gate=integration_gate,
        scope_extract=scope_extract,
        neighbor_extract=neighbor_extract,
        inputs_dir=inputs_dir,
    )

    inputs_dir.mkdir(parents=True, exist_ok=True)
    out_path = inputs_dir / "run_context.yaml"
    out_path.write_text(dump_yaml(context), encoding="utf-8")
    print(f"[build_run_context] written: {out_path.relative_to(repo_root)}")

    rc = context["run_context"]
    result = {
        "build_run_context": {
            "status": "DONE",
            "run_id": args.run_id,
            "current_stage": rc["current_stage"],
            "scope_ids_count": rc["scope_ids_count"],
            "neighbor_ids_count": rc["neighbor_ids_count"],
            "scope_extract_present": rc["scope_extract"]["present"],
            "neighbor_extract_present": rc["neighbor_extract"]["present"],
            "path": str(out_path.relative_to(repo_root)),
        }
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
