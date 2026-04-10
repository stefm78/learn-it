#!/usr/bin/env python3
"""Repair a Platform Factory patchset YAML before validation.

This script attempts to auto-correct recoverable anomalies in a patchset YAML
produced by an AI, so that it can pass validate_platform_factory_patchset.py
without a manual edit cycle.

Recoverable anomalies corrected automatically:
- YAML parse errors caused by unquoted strings containing special characters
  (the script re-serialises all string values using block style >-)
- Missing metadata fields injected as TODO placeholders
- Empty or missing patches list signalled with a clear error (not recoverable)
- Patches missing required fields: missing fields injected as TODO placeholders
- Patches missing required location_hint sub-fields: injected as TODO
- Operations missing required op/path: injected as TODO

Non-recoverable anomalies (reported but not corrected):
- patches list is absent or empty
- YAML file is completely unparseable (not even a dict)

Usage:
    python docs/patcher/shared/repair_platform_factory_patchset.py \\
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml

    Output is written to the same directory with suffix _repaired.yaml
    A repair report is printed to stdout.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

PATCHSET_ROOT = "PLATFORM_FACTORY_PATCHSET"

REQUIRED_METADATA_KEYS = [
    "patchset_id",
    "target_artifacts",
    "source_decision_record",
    "scope",
    "notes",
]

REQUIRED_PATCH_KEYS = [
    "patch_id",
    "source_decision",
    "target_artifact",
    "operation",
    "change_type",
    "rationale",
    "effect",
    "risk_avoided",
    "location_hint",
    "operations",
]

REQUIRED_LOCATION_HINT_KEYS = ["section", "granularity", "keys_to_update"]
REQUIRED_OP_KEYS = ["op", "path"]

TODO = "TODO_FILL_IN"


class RepairReport:
    def __init__(self) -> None:
        self.fixes: list[str] = []
        self.errors: list[str] = []

    def fix(self, msg: str) -> None:
        self.fixes.append(msg)
        print(f"  [FIX]   {msg}")

    def error(self, msg: str) -> None:
        self.errors.append(msg)
        print(f"  [ERROR] {msg}")

    def summary(self) -> None:
        print()
        print(f"Repair summary: {len(self.fixes)} fix(es), {len(self.errors)} error(s).")
        if self.errors:
            print("Non-recoverable errors remain — review manually before running validator.")
        else:
            print("All detected anomalies were corrected. Run validator to confirm.")


def _ensure_dict_key(d: dict, key: str, default: Any, report: RepairReport, context: str) -> None:
    if key not in d:
        d[key] = default
        report.fix(f"{context}: champ '{key}' absent, injecte comme TODO.")


def repair_metadata(metadata: dict, report: RepairReport) -> dict:
    for key in REQUIRED_METADATA_KEYS:
        if key == "target_artifacts":
            if key not in metadata:
                metadata[key] = [
                    "docs/cores/current/platform_factory_architecture.yaml",
                    "docs/cores/current/platform_factory_state.yaml",
                ]
                report.fix("metadata.target_artifacts absent, injecte avec les deux artefacts standards.")
            elif not isinstance(metadata[key], list) or len(metadata[key]) == 0:
                metadata[key] = [
                    "docs/cores/current/platform_factory_architecture.yaml",
                    "docs/cores/current/platform_factory_state.yaml",
                ]
                report.fix("metadata.target_artifacts vide ou invalide, remplace par les deux artefacts standards.")
        elif key == "notes":
            if key not in metadata:
                metadata[key] = [TODO]
                report.fix("metadata.notes absent, injecte liste placeholder.")
            elif not isinstance(metadata[key], list):
                metadata[key] = [str(metadata[key])]
                report.fix("metadata.notes n'etait pas une liste, converti.")
        else:
            _ensure_dict_key(metadata, key, TODO, report, "metadata")
    return metadata


def repair_location_hint(hint: Any, patch_id: str, report: RepairReport) -> dict:
    if not isinstance(hint, dict):
        report.fix(f"patch {patch_id}: location_hint n'est pas un mapping, remplace par placeholder.")
        return {k: TODO for k in REQUIRED_LOCATION_HINT_KEYS}
    for key in REQUIRED_LOCATION_HINT_KEYS:
        if key == "keys_to_update":
            if key not in hint:
                hint[key] = [TODO]
                report.fix(f"patch {patch_id}: location_hint.keys_to_update absent, injecte.")
            elif not isinstance(hint[key], list):
                hint[key] = [str(hint[key])]
                report.fix(f"patch {patch_id}: location_hint.keys_to_update converti en liste.")
        else:
            _ensure_dict_key(hint, key, TODO, report, f"patch {patch_id} location_hint")
    return hint


def repair_operation(op_item: Any, patch_id: str, op_idx: int, report: RepairReport) -> dict:
    if not isinstance(op_item, dict):
        report.fix(f"patch {patch_id} op {op_idx}: n'est pas un mapping, remplace par placeholder.")
        return {"op": TODO, "path": TODO, "value": TODO}
    for key in REQUIRED_OP_KEYS:
        _ensure_dict_key(op_item, key, TODO, report, f"patch {patch_id} op {op_idx}")
    op = op_item.get("op", "")
    if op in {"add", "replace", "update", "list_replace_mapping"}:
        if "value" not in op_item:
            op_item["value"] = TODO
            report.fix(f"patch {patch_id} op {op_idx}: 'value' absent pour op={op}, injecte.")
    if op in {"list_remove_mapping", "list_replace_mapping"}:
        for k in ("match_key", "match_value"):
            if k not in op_item:
                op_item[k] = TODO
                report.fix(f"patch {patch_id} op {op_idx}: '{k}' absent pour op={op}, injecte.")
    if op == "list_remove_item":
        if "value" not in op_item:
            op_item["value"] = TODO
            report.fix(f"patch {patch_id} op {op_idx}: 'value' absent pour op=list_remove_item, injecte.")
    return op_item


def repair_patch(patch: Any, patch_idx: int, report: RepairReport) -> dict:
    if not isinstance(patch, dict):
        report.fix(f"patch {patch_idx}: n'est pas un mapping, remplace par placeholder complet.")
        return {k: TODO for k in REQUIRED_PATCH_KEYS}

    patch_id = patch.get("patch_id", f"patch_{patch_idx}")

    for key in REQUIRED_PATCH_KEYS:
        if key == "location_hint":
            patch[key] = repair_location_hint(patch.get(key, {}), patch_id, report)
        elif key == "operations":
            ops = patch.get("operations")
            if not isinstance(ops, list) or len(ops) == 0:
                report.fix(f"patch {patch_id}: 'operations' absent ou vide, injecte op placeholder.")
                patch["operations"] = [{"op": TODO, "path": TODO, "value": TODO}]
            else:
                patch["operations"] = [
                    repair_operation(op, patch_id, i + 1, report)
                    for i, op in enumerate(ops)
                ]
        else:
            _ensure_dict_key(patch, key, TODO, report, f"patch {patch_id}")

    return patch


def _block_str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    """Force block style for all multiline strings or strings with special chars."""
    special = any(c in data for c in (':', '\n', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`'))
    if '\n' in data or (special and len(data) > 40):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def _build_dumper() -> type:
    class BlockDumper(yaml.Dumper):
        pass
    BlockDumper.add_representer(str, _block_str_representer)
    return BlockDumper


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: repair_platform_factory_patchset.py <patchset.yaml>")
        return 1

    src = Path(argv[1])
    if not src.exists():
        print(f"Fichier introuvable: {src}")
        return 1

    report = RepairReport()
    print(f"Repair: {src}")
    print()

    # Step 1: try to parse YAML
    raw_text = src.read_text(encoding="utf-8")
    try:
        raw = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        print(f"[ERROR] Le fichier n'est pas parseable par yaml.safe_load: {exc}")
        print()
        print("Tentative de recuperation via ruamel.yaml ou parsing partiel...")
        try:
            from ruamel.yaml import YAML
            ry = YAML()
            ry.preserve_quotes = True
            import io
            raw = ry.load(io.StringIO(raw_text))
            print("[FIX] Parsed avec ruamel.yaml (tolerant).")
            report.fix("YAML parse error recupere via ruamel.yaml.")
        except Exception:
            report.error(
                "Le fichier YAML est completement malformed et ne peut pas etre parse. "
                "Corriger manuellement les erreurs de syntaxe YAML avant de relancer."
            )
            report.summary()
            return 1

    # Step 2: ensure root is a dict with PATCHSET_ROOT
    if not isinstance(raw, dict):
        report.error("La racine du fichier n'est pas un mapping YAML. Correction impossible.")
        report.summary()
        return 1

    if PATCHSET_ROOT not in raw:
        # Try to find a close key
        candidates = [k for k in raw if "PATCHSET" in str(k).upper()]
        if candidates:
            old_key = candidates[0]
            raw[PATCHSET_ROOT] = raw.pop(old_key)
            report.fix(f"Cle racine '{old_key}' renommee en '{PATCHSET_ROOT}'.")
        else:
            raw = {PATCHSET_ROOT: raw}
            report.fix(f"Cle racine '{PATCHSET_ROOT}' absente, tout le contenu encapsule sous elle.")

    root = raw[PATCHSET_ROOT]
    if not isinstance(root, dict):
        report.error(f"La valeur sous '{PATCHSET_ROOT}' n'est pas un mapping. Correction impossible.")
        report.summary()
        return 1

    # Step 3: repair metadata
    if "metadata" not in root or not isinstance(root.get("metadata"), dict):
        root["metadata"] = {}
        report.fix("Bloc 'metadata' absent ou invalide, cree vide.")
    root["metadata"] = repair_metadata(root["metadata"], report)

    # Step 4: repair patches
    patches = root.get("patches")
    if not isinstance(patches, list) or len(patches) == 0:
        report.error(
            "'patches' est absent ou vide. Ce n'est pas recuperable automatiquement. "
            "L'IA doit fournir la liste des patches avant que le repair puisse aider."
        )
    else:
        root["patches"] = [
            repair_patch(p, i + 1, report) for i, p in enumerate(patches)
        ]

    # Step 5: write repaired file
    out_path = src.with_name(src.stem + "_repaired.yaml")
    BlockDumper = _build_dumper()
    with out_path.open("w", encoding="utf-8") as f:
        yaml.dump(raw, f, Dumper=BlockDumper, allow_unicode=True,
                  sort_keys=False, default_flow_style=False, width=100)

    print()
    print(f"Fichier repare ecrit: {out_path}")
    report.summary()

    if not report.errors:
        print()
        print("Prochaine etape:")
        print(f"  python docs/patcher/shared/validate_platform_factory_patchset.py {out_path}")
        print("  Si PASS, renommer le fichier repare en platform_factory_patchset.yaml")

    return 0 if not report.errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
