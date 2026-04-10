#!/usr/bin/env python3
"""Build a Platform Factory patchset YAML from an AI-friendly intent file.

This script transforms a free-form intent file (patchset_intent.yaml) produced
by an AI into a fully conformant patchset YAML that passes
validate_platform_factory_patchset.py without any manual editing.

The intent file has a relaxed schema that is easy for an AI to produce:
- No strict quoting rules (the script handles serialisation)
- Fields can be in any order
- Optional fields can be omitted
- The script injects required fields as TODO placeholders if missing

Intent file format (patchset_intent.yaml):

  intent_metadata:
    patchset_id: PFPATCH_20260410_PPLX_FINAL
    date: '2026-04-10'
    source_decision_record: docs/pipelines/.../platform_factory_arbitrage.md
    scope: Description libre du perimetre.
    notes:
    - Note 1.

  patch_intents:
  - id: PFPATCH_A1
    decision: CONS-04
    target: arch          # 'arch' = architecture.yaml, 'state' = state.yaml
    op_type: add          # add | replace | update | list_replace_mapping | list_remove_mapping | list_remove_item | remove
    change_type: metadata_enrichment
    sequence: 1
    priority: eleve
    rationale: Justification libre.
    effect: Effet libre.
    risk_avoided: Risque evite.
    section: PLATFORM_FACTORY_ARCHITECTURE.metadata
    granularity: field
    keys_to_update:
    - authority_rank
    operations:
    - op: add
      path: PLATFORM_FACTORY_ARCHITECTURE.metadata.authority_rank
      value: factory_layer

Usage:
    python docs/patcher/shared/build_platform_factory_patchset.py \\
        ./docs/pipelines/platform_factory/work/03_patch/patchset_intent.yaml \\
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

PATCHSET_ROOT = "PLATFORM_FACTORY_PATCHSET"

TARGET_MAP = {
    "arch": "docs/cores/current/platform_factory_architecture.yaml",
    "architecture": "docs/cores/current/platform_factory_architecture.yaml",
    "state": "docs/cores/current/platform_factory_state.yaml",
    "docs/cores/current/platform_factory_architecture.yaml": "docs/cores/current/platform_factory_architecture.yaml",
    "docs/cores/current/platform_factory_state.yaml": "docs/cores/current/platform_factory_state.yaml",
}

TODO = "TODO_FILL_IN"


def _block_str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    special = any(c in data for c in (':', '\n', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`'))
    if '\n' in data or (special and len(data) > 40):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def _build_dumper() -> type:
    class BlockDumper(yaml.Dumper):
        pass
    BlockDumper.add_representer(str, _block_str_representer)
    return BlockDumper


def _resolve_target(raw_target: str) -> str:
    key = str(raw_target).strip().lower()
    return TARGET_MAP.get(key, TARGET_MAP.get(raw_target, raw_target))


def _build_metadata(intent_meta: dict) -> dict:
    targets_declared = [
        "docs/cores/current/platform_factory_architecture.yaml",
        "docs/cores/current/platform_factory_state.yaml",
    ]
    notes = intent_meta.get("notes", [TODO])
    if not isinstance(notes, list):
        notes = [str(notes)]
    return {
        "patchset_id": intent_meta.get("patchset_id", TODO),
        "date": intent_meta.get("date", TODO),
        "target_artifacts": targets_declared,
        "source_decision_record": intent_meta.get("source_decision_record", TODO),
        "scope": intent_meta.get("scope", TODO),
        "notes": notes,
    }


def _build_operations(raw_ops: Any, patch_id: str) -> list[dict]:
    if not isinstance(raw_ops, list) or len(raw_ops) == 0:
        print(f"  [WARN] patch {patch_id}: 'operations' absent ou vide, placeholder injecte.")
        return [{"op": TODO, "path": TODO, "value": TODO}]
    result = []
    for i, op in enumerate(raw_ops):
        if not isinstance(op, dict):
            print(f"  [WARN] patch {patch_id} op {i+1}: n'est pas un mapping, placeholder injecte.")
            result.append({"op": TODO, "path": TODO, "value": TODO})
            continue
        item: dict[str, Any] = {
            "op": op.get("op", TODO),
            "path": op.get("path", TODO),
        }
        op_name = str(item["op"])
        if op_name in {"add", "replace", "update", "list_replace_mapping"}:
            item["value"] = op.get("value", TODO)
        if op_name in {"list_remove_mapping", "list_replace_mapping"}:
            item["match_key"] = op.get("match_key", TODO)
            item["match_value"] = op.get("match_value", TODO)
        if op_name == "list_remove_item":
            item["value"] = op.get("value", TODO)
        # pass through any extra keys (e.g. match_key already set)
        for k, v in op.items():
            if k not in item:
                item[k] = v
        result.append(item)
    return result


def _build_patch(intent: dict, idx: int) -> dict:
    patch_id = intent.get("id", intent.get("patch_id", f"PFPATCH_UNNAMED_{idx}"))
    raw_target = intent.get("target", intent.get("target_artifact", TODO))
    target = _resolve_target(str(raw_target)) if raw_target != TODO else TODO

    keys_to_update = intent.get("keys_to_update", [TODO])
    if not isinstance(keys_to_update, list):
        keys_to_update = [str(keys_to_update)]

    return {
        "patch_id": patch_id,
        "source_decision": intent.get("decision", intent.get("source_decision", TODO)),
        "target_artifact": target,
        "operation": intent.get("op_type", intent.get("operation", TODO)),
        "change_type": intent.get("change_type", TODO),
        "sequence": intent.get("sequence", idx),
        "priority": intent.get("priority", TODO),
        "rationale": intent.get("rationale", TODO),
        "effect": intent.get("effect", TODO),
        "risk_avoided": intent.get("risk_avoided", TODO),
        "location_hint": {
            "section": intent.get("section", TODO),
            "granularity": intent.get("granularity", TODO),
            "keys_to_update": keys_to_update,
        },
        "operations": _build_operations(
            intent.get("operations", intent.get("ops")), patch_id
        ),
    }


def _build_exclusions(raw_exclusions: Any) -> dict | None:
    if not raw_exclusions:
        return None
    items_raw = raw_exclusions if isinstance(raw_exclusions, list) else raw_exclusions.get("items", [])
    items = []
    for excl in items_raw:
        if not isinstance(excl, dict):
            continue
        items.append({
            "id": excl.get("id", TODO),
            "reason": excl.get("reason", TODO),
            "note": excl.get("note", TODO),
        })
    return {"items": items} if items else None


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: build_platform_factory_patchset.py <intent.yaml> <output_patchset.yaml>")
        return 1

    intent_path = Path(argv[1])
    out_path = Path(argv[2])

    if not intent_path.exists():
        print(f"Intent file introuvable: {intent_path}")
        return 1

    raw = yaml.safe_load(intent_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print("Le fichier intent n'est pas un mapping YAML valide.")
        return 1

    print(f"Build patchset from intent: {intent_path}")
    print()

    intent_meta = raw.get("intent_metadata", raw.get("metadata", {}))
    patch_intents = raw.get("patch_intents", raw.get("patches", []))
    raw_exclusions = raw.get("exclusions")

    metadata = _build_metadata(intent_meta)
    patches = [_build_patch(pi, i + 1) for i, pi in enumerate(patch_intents)]

    patchset: dict[str, Any] = {
        PATCHSET_ROOT: {
            "metadata": metadata,
            "patches": patches,
        }
    }

    excl = _build_exclusions(raw_exclusions)
    if excl:
        patchset[PATCHSET_ROOT]["exclusions"] = excl

    BlockDumper = _build_dumper()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        yaml.dump(patchset, f, Dumper=BlockDumper, allow_unicode=True,
                  sort_keys=False, default_flow_style=False, width=100)

    print(f"Patchset ecrit: {out_path}")
    print(f"{len(patches)} patch(es) genere(s).")
    print()
    print("Prochaine etape:")
    print(f"  python docs/patcher/shared/validate_platform_factory_patchset.py {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
