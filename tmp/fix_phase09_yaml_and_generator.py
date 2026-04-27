#!/usr/bin/env python3
"""Fix PHASE_09 YAML anchors and make scope generation tolerate metadata decisions.

This script performs two safe local changes:

1. Rewrites decisions.yaml without YAML aliases/anchors.
2. Updates generate_constitution_scopes.py so metadata-only decision types do not
   break deterministic catalog generation.

It does not modify:
  - docs/cores/current/*.yaml
  - docs/pipelines/constitution/scope_catalog/*
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


DECISIONS_PATH = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
GENERATOR_PATH = Path("docs/patcher/shared/generate_constitution_scopes.py")


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml_no_aliases(data: Any) -> str:
    return yaml.dump(
        data,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )


def rewrite_decisions_without_aliases() -> bool:
    before = DECISIONS_PATH.read_text(encoding="utf-8")
    data = load_yaml(DECISIONS_PATH)
    after = dump_yaml_no_aliases(data)

    if before == after:
        return False

    DECISIONS_PATH.write_text(after, encoding="utf-8")
    return True


def patch_generator() -> bool:
    text = GENERATOR_PATH.read_text(encoding="utf-8")

    if "METADATA_ONLY_DECISION_TYPES" in text:
        return False

    old = """def collect_decisions(decisions: Dict[str, Any]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    decisions_root = decisions["scope_generation_decisions"]
    target_ids: Dict[str, List[str]] = {}
    neighbor_ids: Dict[str, List[str]] = {}

    for decision in decisions_root.get("decisions", []):
        if decision.get("status") != "approved":
            continue
        decision_type = decision["decision_type"]
        affected = decision.get("scope_keys_affected", [])
        ids = decision.get("target_ids", []) or []

        if decision_type == "assign_ids_to_scope":
            for scope_key in affected:
                target_ids.setdefault(scope_key, []).extend(ids)
        elif decision_type == "force_logical_neighbors":
            for scope_key in affected:
                neighbor_ids.setdefault(scope_key, []).extend(ids)
        else:
            raise ValueError(f"Unsupported scope generation decision_type: {decision_type}")

    return (
        {k: sorted_unique(v) for k, v in target_ids.items()},
        {k: sorted_unique(v) for k, v in neighbor_ids.items()},
    )
"""

    new = """METADATA_ONLY_DECISION_TYPES = {
    "classify_external_read_only_cores",
    "record_diagnostic_subcluster",
}


def collect_decisions(decisions: Dict[str, Any]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    decisions_root = decisions["scope_generation_decisions"]
    target_ids: Dict[str, List[str]] = {}
    neighbor_ids: Dict[str, List[str]] = {}

    for decision in decisions_root.get("decisions", []):
        if decision.get("status") != "approved":
            continue
        decision_type = decision["decision_type"]
        affected = decision.get("scope_keys_affected", [])
        ids = decision.get("target_ids", []) or []

        if decision_type == "assign_ids_to_scope":
            for scope_key in affected:
                target_ids.setdefault(scope_key, []).extend(ids)
        elif decision_type == "force_logical_neighbors":
            for scope_key in affected:
                neighbor_ids.setdefault(scope_key, []).extend(ids)
        elif decision_type in METADATA_ONLY_DECISION_TYPES:
            # These decisions enrich scoping governance and validation semantics,
            # but they do not directly add target IDs or neighbor IDs to generated
            # scope definitions.
            continue
        else:
            raise ValueError(f"Unsupported scope generation decision_type: {decision_type}")

    return (
        {k: sorted_unique(v) for k, v in target_ids.items()},
        {k: sorted_unique(v) for k, v in neighbor_ids.items()},
    )
"""

    if old not in text:
        raise RuntimeError(
            "Could not locate collect_decisions block in generator. "
            "Patch manually or inspect generator drift."
        )

    text = text.replace(old, new)
    GENERATOR_PATH.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = []

    if rewrite_decisions_without_aliases():
        changed.append(str(DECISIONS_PATH))

    if patch_generator():
        changed.append(str(GENERATOR_PATH))

    if changed:
        print("updated:")
        for item in changed:
            print(f" - {item}")
    else:
        print("No changes needed.")

    print("Next command:")
    print("python docs/patcher/shared/generate_constitution_scopes.py --report tmp/constitution_scope_generation_report.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
