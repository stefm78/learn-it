#!/usr/bin/env python3
"""Fix PHASE_11 bijection inputs and validator classification.

This script:
  1. Replaces REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION with
     REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION in SGEN_DECISION_006.
  2. Adds RULE_PATCH_SERIALIZATION to patch_lifecycle ownership decision.
  3. Updates tmp/validate_scope_partition_bijection.py so
     REF_CORE_*_IN_CONSTITUTION entries are classified as inter-core references,
     not as missing Constitution business owners.

It does not modify docs/cores/current/*.yaml.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


DECISIONS_PATH = Path("docs/pipelines/constitution/policies/scope_generation/decisions.yaml")
VALIDATOR_PATH = Path("tmp/validate_scope_partition_bijection.py")

OLD_REF = "REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION"
NEW_REF = "REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION"
PATCH_RULE = "RULE_PATCH_SERIALIZATION"


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.write_text(
        yaml.dump(
            data,
            Dumper=NoAliasDumper,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=120,
        ),
        encoding="utf-8",
    )


def replace_string_deep(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_string_deep(item, old, new) for item in value]
    if isinstance(value, dict):
        return {
            key: replace_string_deep(item, old, new)
            for key, item in value.items()
        }
    return value


def find_decision(decisions: list[dict[str, Any]], decision_id: str) -> dict[str, Any]:
    for decision in decisions:
        if decision.get("decision_id") == decision_id:
            return decision
    raise ValueError(f"Decision not found: {decision_id}")


def patch_decisions() -> list[str]:
    doc = load_yaml(DECISIONS_PATH)
    root = doc.get("scope_generation_decisions", {})
    decisions = root.get("decisions", [])
    if not isinstance(decisions, list):
        raise ValueError("Expected decisions list in decisions.yaml")

    changed: list[str] = []

    # Patch SGEN_DECISION_005: add RULE_PATCH_SERIALIZATION to patch_lifecycle.
    d005 = find_decision(decisions, "SGEN_DECISION_005")
    target_ids = d005.setdefault("target_ids", [])
    if PATCH_RULE not in target_ids:
        target_ids.append(PATCH_RULE)
        d005["justification"] = (
            str(d005.get("justification", "")).rstrip()
            + " RULE_PATCH_SERIALIZATION est ajouté au périmètre patch_lifecycle car la sérialisation "
              "des patches relève du cycle de vie patch et de ses garanties de validation/rejouabilité."
        )
        changed.append("decisions.SGEN_DECISION_005.add_RULE_PATCH_SERIALIZATION")

    # Patch SGEN_DECISION_006: replace old referentiel V2 neighbor by current V4 reference.
    index_006 = None
    for index, decision in enumerate(decisions):
        if decision.get("decision_id") == "SGEN_DECISION_006":
            index_006 = index
            break
    if index_006 is None:
        raise ValueError("Decision not found: SGEN_DECISION_006")

    before = repr(decisions[index_006])
    decisions[index_006] = replace_string_deep(decisions[index_006], OLD_REF, NEW_REF)
    after = repr(decisions[index_006])
    if before != after:
        changed.append("decisions.SGEN_DECISION_006.replace_referentiel_V2_with_V4")

    write_yaml(DECISIONS_PATH, doc)
    return changed


def patch_validator() -> list[str]:
    if not VALIDATOR_PATH.exists():
        raise FileNotFoundError(f"Missing validator: {VALIDATOR_PATH}")

    text = VALIDATOR_PATH.read_text(encoding="utf-8")
    changed: list[str] = []

    if "def is_constitution_intercore_reference_id" not in text:
        marker = "\ndef classify_id(entry: dict[str, Any], owners: list[str], external_files: set[str]) -> str:\n"
        helper = (
            "\n"
            "def is_constitution_intercore_reference_id(entry_id: str | None) -> bool:\n"
            "    return (\n"
            "        isinstance(entry_id, str)\n"
            "        and entry_id.startswith(\"REF_CORE_\")\n"
            "        and entry_id.endswith(\"_IN_CONSTITUTION\")\n"
            "    )\n"
            "\n"
        )
        if marker not in text:
            raise RuntimeError("Could not locate classify_id marker in validator.")
        text = text.replace(marker, helper + marker, 1)
        changed.append("validator.add_intercore_reference_helper")

    old = (
        "def classify_id(entry: dict[str, Any], owners: list[str], external_files: set[str]) -> str:\n"
        "    source_core = entry.get(\"source_core\")\n"
        "    source_section = entry.get(\"source_section\")\n"
        "    source_path = entry.get(\"source_path\")\n"
        "\n"
        "    if source_section == \"CORE\":\n"
        "        return \"canonical_core_header\"\n"
        "\n"
        "    if source_core == \"constitution\":\n"
        "        if len(owners) == 1:\n"
        "            return \"constitution_owned\"\n"
        "        if len(owners) == 0:\n"
        "            return \"missing_constitution_owner\"\n"
        "        return \"duplicate_constitution_owner\"\n"
    )

    new = (
        "def classify_id(entry: dict[str, Any], owners: list[str], external_files: set[str]) -> str:\n"
        "    entry_id = entry.get(\"id\")\n"
        "    source_core = entry.get(\"source_core\")\n"
        "    source_section = entry.get(\"source_section\")\n"
        "    source_path = entry.get(\"source_path\")\n"
        "\n"
        "    if source_section == \"CORE\":\n"
        "        return \"canonical_core_header\"\n"
        "\n"
        "    if source_core == \"constitution\" and is_constitution_intercore_reference_id(entry_id):\n"
        "        return \"constitution_intercore_reference\"\n"
        "\n"
        "    if source_core == \"constitution\":\n"
        "        if len(owners) == 1:\n"
        "            return \"constitution_owned\"\n"
        "        if len(owners) == 0:\n"
        "            return \"missing_constitution_owner\"\n"
        "        return \"duplicate_constitution_owner\"\n"
    )

    if old in text:
        text = text.replace(old, new, 1)
        changed.append("validator.classify_intercore_references")
    elif "constitution_intercore_reference" not in text:
        raise RuntimeError("Could not patch classify_id in validator.")

    VALIDATOR_PATH.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    changed = []
    changed.extend(patch_decisions())
    changed.extend(patch_validator())

    if changed:
        print("updated:")
        for item in changed:
            print(f" - {item}")
    else:
        print("No changes needed.")

    print("")
    print("Next commands:")
    print("python docs/patcher/shared/generate_constitution_scopes.py --report tmp/constitution_scope_generation_report.yaml --apply")
    print("python tmp/validate_scope_partition_bijection.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
