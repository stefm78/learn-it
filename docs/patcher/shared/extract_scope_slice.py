#!/usr/bin/env python3
"""Extract scope-specific slices from canonical Core files for a bounded run.

For a given run_id, reads:
  - runs/<run_id>/inputs/scope_manifest.yaml   -> writable_perimeter.ids (scope IDs)
  - runs/<run_id>/inputs/impact_bundle.yaml    -> mandatory_reads.ids (neighbor IDs)
  - docs/cores/current/constitution.yaml       -> canonical Core (source of truth)
  - docs/cores/current/referentiel.yaml        -> canonical Core (source of truth)
  - docs/cores/current/link.yaml               -> canonical Core (source of truth)

Produces (deterministically, no AI required):
  - runs/<run_id>/inputs/scope_extract.yaml    -> entries matching scope IDs only
  - runs/<run_id>/inputs/neighbor_extract.yaml -> entries matching neighbor IDs only

Goal (J2 — effective read surface reduction):
  The AI working on STAGE_01_CHALLENGE reads scope_extract.yaml + neighbor_extract.yaml
  instead of the full Core files. This reduces context payload from ~160 KB to the
  strict minimum required for the declared scope.

  The canonical Core files remain the authoritative source of truth.
  scope_extract.yaml and neighbor_extract.yaml are derived views, NOT a second source.

Fallback rule:
  If a critical ID is missing from the extract (e.g. not yet indexed), the AI must
  explicitly signal it and fall back to the full canonical Core file for that ID only.

IDENTIFICATION STRATEGY:
  Entries are matched by id fields at any nesting level within each Core file's
  top-level collection keys. The script walks all top-level list/dict structures
  and collects any entry whose recognized id field matches the target set.

Integration in pipeline.md:
  Spec and tools section — called after materialize_run_inputs.py, before STAGE_01_CHALLENGE.
  Command:
    python docs/patcher/shared/extract_scope_slice.py --run-id <RUN_ID>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required.") from exc


# ---------------------------------------------------------------------------
# ID field candidates (in priority order)
# ---------------------------------------------------------------------------

ID_FIELD_CANDIDATES = [
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


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True,
                          default_flow_style=False, width=100)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Entry extraction
# ---------------------------------------------------------------------------

def _get_entry_id(entry: Any) -> str | None:
    """Return the canonical ID of a dict entry, trying all known id fields."""
    if not isinstance(entry, dict):
        return None
    for field in ID_FIELD_CANDIDATES:
        val = entry.get(field)
        if val and isinstance(val, str):
            return val
    return None


def extract_entries_by_ids(
    core_data: Any,
    target_ids: Set[str],
    core_name: str,
) -> tuple[List[Dict[str, Any]], Set[str]]:
    """Walk a Core YAML structure and collect all entries whose ID is in target_ids.

    Returns:
        matched   : list of (section_key, entry) dicts with provenance metadata
        found_ids : set of IDs actually found
    """
    matched: List[Dict[str, Any]] = []
    found_ids: Set[str] = set()

    if not isinstance(core_data, dict):
        return matched, found_ids

    for section_key, section_value in core_data.items():
        # Top-level section is a list of entries
        if isinstance(section_value, list):
            for entry in section_value:
                entry_id = _get_entry_id(entry)
                if entry_id and entry_id in target_ids:
                    matched.append({
                        "_source_core": core_name,
                        "_source_section": section_key,
                        "_matched_id": entry_id,
                        "entry": entry,
                    })
                    found_ids.add(entry_id)
        # Top-level section is a dict of entries keyed by id
        elif isinstance(section_value, dict):
            for key, entry in section_value.items():
                entry_id = _get_entry_id(entry) or (key if key in target_ids else None)
                if entry_id and entry_id in target_ids:
                    matched.append({
                        "_source_core": core_name,
                        "_source_section": section_key,
                        "_matched_id": entry_id,
                        "entry": entry,
                    })
                    found_ids.add(entry_id)

    return matched, found_ids


# ---------------------------------------------------------------------------
# Build extract artifact
# ---------------------------------------------------------------------------

def build_extract(
    run_id: str,
    extract_type: str,   # 'scope' or 'neighbor'
    target_ids: List[str],
    core_files: Dict[str, Path],
    scope_manifest_fingerprint: str,
    impact_bundle_fingerprint: str,
) -> tuple[Dict[str, Any], Set[str], Set[str]]:
    """Extract all entries matching target_ids from all provided Core files.

    Returns:
        artifact        : the YAML artifact dict
        found_ids       : IDs that were matched in at least one Core
        missing_ids     : IDs declared but not found in any Core
    """
    target_set = set(target_ids)
    all_matched: List[Dict[str, Any]] = []
    all_found: Set[str] = set()
    core_fingerprints: Dict[str, str] = {}

    for core_name, core_path in core_files.items():
        core_data = load_yaml(core_path)
        core_fingerprints[core_name] = sha256_file(core_path)
        matched, found = extract_entries_by_ids(core_data, target_set, core_name)
        all_matched.extend(matched)
        all_found.update(found)

    missing_ids = sorted(target_set - all_found)

    artifact = {
        f"{extract_type}_extract": {
            "schema_version": 0.1,
            "extract_type": extract_type,
            "run_id": run_id,
            "source": {
                "scope_manifest_fingerprint": scope_manifest_fingerprint,
                "impact_bundle_fingerprint": impact_bundle_fingerprint,
                "core_fingerprints": core_fingerprints,
            },
            "target_ids": sorted(target_ids),
            "found_ids": sorted(all_found),
            "missing_ids": missing_ids,
            "entries": all_matched,
            "fallback_rule": (
                "If missing_ids is non-empty, the AI must explicitly signal each missing ID "
                "and fall back to reading the full canonical Core file for that ID only. "
                "It must NOT silently ignore missing IDs."
            ),
            "notes": [
                "Généré déterministiquement par extract_scope_slice.py depuis les Core canoniques.",
                "Ce fichier est une vue dérivée. Les Core canoniques restent la source de vérité.",
                "En mode bounded_local_run, l'IA doit lire ce fichier en priorité sur les Core complets.",
                "Le champ _source_core indique l'origine canonique de chaque entrée.",
            ],
        }
    }
    return artifact, all_found, set(missing_ids)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract scope-specific slices from canonical Core files (J2 — ids-first)."
    )
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    inputs_dir = run_root / "inputs"

    # Load inputs
    scope_manifest_path = inputs_dir / "scope_manifest.yaml"
    impact_bundle_path = inputs_dir / "impact_bundle.yaml"
    scope_manifest = load_yaml(scope_manifest_path)
    impact_bundle = load_yaml(impact_bundle_path)

    scope_manifest_fingerprint = sha256_file(scope_manifest_path)
    impact_bundle_fingerprint = sha256_file(impact_bundle_path)

    # Resolve target ID sets
    sm = scope_manifest.get("scope_manifest", {})
    ib = impact_bundle.get("impact_bundle", {})

    scope_ids: List[str] = sm.get("writable_perimeter", {}).get("ids", [])
    neighbor_ids: List[str] = ib.get("mandatory_reads", {}).get("ids", [])

    if not scope_ids:
        print("WARNING: scope_manifest.writable_perimeter.ids is empty — scope_extract will be empty",
              file=sys.stderr)

    # Canonical Core files
    cores_root = repo_root / "docs" / "cores" / "current"
    core_files: Dict[str, Path] = {
        "constitution": cores_root / "constitution.yaml",
        "referentiel": cores_root / "referentiel.yaml",
        "link": cores_root / "link.yaml",
    }
    for name, path in core_files.items():
        if not path.exists():
            print(f"ERROR: canonical Core file not found: {path}", file=sys.stderr)
            return 1

    # Extract scope slice
    print(f"[extract_scope_slice] Extracting scope slice — {len(scope_ids)} target IDs")
    scope_artifact, scope_found, scope_missing = build_extract(
        run_id=args.run_id,
        extract_type="scope",
        target_ids=scope_ids,
        core_files=core_files,
        scope_manifest_fingerprint=scope_manifest_fingerprint,
        impact_bundle_fingerprint=impact_bundle_fingerprint,
    )

    # Extract neighbor slice
    print(f"[extract_scope_slice] Extracting neighbor slice — {len(neighbor_ids)} target IDs")
    neighbor_artifact, neighbor_found, neighbor_missing = build_extract(
        run_id=args.run_id,
        extract_type="neighbor",
        target_ids=neighbor_ids,
        core_files=core_files,
        scope_manifest_fingerprint=scope_manifest_fingerprint,
        impact_bundle_fingerprint=impact_bundle_fingerprint,
    )

    # Write outputs
    inputs_dir.mkdir(parents=True, exist_ok=True)
    scope_extract_path = inputs_dir / "scope_extract.yaml"
    neighbor_extract_path = inputs_dir / "neighbor_extract.yaml"

    scope_extract_path.write_text(dump_yaml(scope_artifact), encoding="utf-8")
    neighbor_extract_path.write_text(dump_yaml(neighbor_artifact), encoding="utf-8")

    print(f"[extract_scope_slice] written: {scope_extract_path.relative_to(repo_root)}")
    print(f"[extract_scope_slice] written: {neighbor_extract_path.relative_to(repo_root)}")

    # Warnings for missing IDs
    if scope_missing:
        print(f"WARNING: {len(scope_missing)} scope IDs not found in any Core: {sorted(scope_missing)}",
              file=sys.stderr)
    if neighbor_missing:
        print(f"WARNING: {len(neighbor_missing)} neighbor IDs not found in any Core: {sorted(neighbor_missing)}",
              file=sys.stderr)

    result = {
        "extract_scope_slice": {
            "status": "DONE",
            "run_id": args.run_id,
            "scope_extract": {
                "target_count": len(scope_ids),
                "found_count": len(scope_found),
                "missing_count": len(scope_missing),
                "missing_ids": sorted(scope_missing),
                "path": str(scope_extract_path.relative_to(repo_root)),
            },
            "neighbor_extract": {
                "target_count": len(neighbor_ids),
                "found_count": len(neighbor_found),
                "missing_count": len(neighbor_missing),
                "missing_ids": sorted(neighbor_missing),
                "path": str(neighbor_extract_path.relative_to(repo_root)),
            },
        }
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
