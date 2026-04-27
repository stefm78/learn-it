#!/usr/bin/env python3
"""Validate normalized structural reconstruction of current cores from the scope partition.

PHASE_11B — full_structural_reconstruction_validation

Validation model:
  - constitution.yaml is reconstructed from the generated scope catalog target.ids
    plus explicitly pass-through Constitution metadata/reference entries.
  - referentiel.yaml and link.yaml are reconstructed in external_read_only passthrough
    mode, according to policy.core_role_classification.external_read_only_core_files.
  - Comparison is structural and normalized via YAML dump with sorted keys.
  - This validator does not mutate canonical files or generated scope catalog files.

Writes:
  - tmp/scope_partition_reconstruction_validation.yaml

Why passthrough for referentiel/link?
  In the accepted arbitration, referentiel and link are external_read_only for
  Constitution bounded runs. Therefore the Constitution scope catalog is not
  expected to own or partition their entries. The valid reconstruction mode for
  these cores in this catalog is controlled passthrough, not ownership partition.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


POLICY_PATH = Path("docs/pipelines/constitution/policies/scope_generation/policy.yaml")
SCOPE_DIR = Path("docs/pipelines/constitution/scope_catalog/scope_definitions")
CORE_FILES = {
    "constitution": Path("docs/cores/current/constitution.yaml"),
    "referentiel": Path("docs/cores/current/referentiel.yaml"),
    "link": Path("docs/cores/current/link.yaml"),
}

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


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(data: Any) -> str:
    return yaml.dump(
        data,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )


def normalized_text(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=True,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )


def normalized_fingerprint(data: Any) -> str:
    return hashlib.sha256(normalized_text(data).encode("utf-8")).hexdigest()


def get_entry_id(entry: Any, fallback_key: str | None = None) -> str | None:
    if isinstance(entry, dict):
        for field in ID_FIELDS:
            value = entry.get(field)
            if isinstance(value, str) and value:
                return value.split("::", 1)[0]
    if fallback_key:
        return fallback_key.split("::", 1)[0]
    return None


def is_intercore_ref_id(entry_id: str | None) -> bool:
    return (
        isinstance(entry_id, str)
        and entry_id.startswith("REF_CORE_")
        and entry_id.endswith("_IN_CONSTITUTION")
    )


def is_core_envelope(doc: Any) -> bool:
    return isinstance(doc, dict) and isinstance(doc.get("CORE"), dict)


def core_root(doc: Any) -> dict[str, Any]:
    if is_core_envelope(doc):
        return doc["CORE"]
    if isinstance(doc, dict):
        return doc
    return {}


def wrap_like_original(original: Any, root: dict[str, Any]) -> Any:
    if is_core_envelope(original):
        return {"CORE": root}
    return root


def collect_scope_targets(repo_root: Path, scope_dir: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    targets_by_scope: dict[str, list[str]] = {}
    owners_by_id: dict[str, list[str]] = defaultdict(list)

    if not scope_dir.exists():
        raise FileNotFoundError(f"Missing scope definitions dir: {scope_dir}")

    for path in sorted(scope_dir.glob("*.yaml")):
        doc = load_yaml(path)
        root = doc.get("scope_definition", {})
        scope_key = root.get("scope_key")
        if not isinstance(scope_key, str):
            continue

        target_ids = root.get("target", {}).get("ids", []) or []
        targets_by_scope[scope_key] = sorted(target_ids)

        for target_id in target_ids:
            owners_by_id[target_id].append(scope_key)

    return targets_by_scope, {entry_id: sorted(scopes) for entry_id, scopes in owners_by_id.items()}


def policy_external_read_only_files(policy_doc: dict[str, Any]) -> set[str]:
    root = policy_doc.get("scope_generation_policy", {})
    classification = root.get("core_role_classification", {})
    return set(classification.get("external_read_only_core_files", []) or [])


def iter_core_entries(root: dict[str, Any]):
    for section_key, section_value in root.items():
        if isinstance(section_value, list):
            for index, entry in enumerate(section_value):
                yield section_key, index, None, entry
        elif isinstance(section_value, dict):
            # Dict sections can be maps of entries or plain scalar metadata maps.
            for key, entry in section_value.items():
                yield section_key, None, str(key), entry


def reconstruct_constitution(
    original_doc: Any,
    owned_ids: set[str],
) -> tuple[Any, dict[str, Any]]:
    root = core_root(original_doc)
    reconstructed_root: dict[str, Any] = {}

    included_ids: list[str] = []
    pass_through_ids: list[str] = []
    missing_owner_ids: list[str] = []
    duplicate_or_unidentified_entries: list[dict[str, Any]] = []

    for section_key, section_value in root.items():
        # Scalar metadata fields are copied as pass-through because they are part
        # of the core envelope, not owned business entries.
        if not isinstance(section_value, (list, dict)):
            reconstructed_root[section_key] = deepcopy(section_value)
            continue

        if isinstance(section_value, list):
            new_list = []
            for entry in section_value:
                entry_id = get_entry_id(entry)

                if entry_id in owned_ids:
                    new_list.append(deepcopy(entry))
                    included_ids.append(entry_id)
                elif is_intercore_ref_id(entry_id):
                    new_list.append(deepcopy(entry))
                    pass_through_ids.append(entry_id)
                elif entry_id is None:
                    new_list.append(deepcopy(entry))
                    duplicate_or_unidentified_entries.append(
                        {
                            "section": section_key,
                            "reason": "entry_without_id_in_list_copied_as_passthrough",
                        }
                    )
                else:
                    missing_owner_ids.append(entry_id)

            reconstructed_root[section_key] = new_list

        elif isinstance(section_value, dict):
            # If the dict itself looks like one ID-bearing entry, treat it as a
            # single entry. Otherwise treat it as a map.
            dict_entry_id = get_entry_id(section_value)
            if dict_entry_id:
                if dict_entry_id in owned_ids or is_intercore_ref_id(dict_entry_id):
                    reconstructed_root[section_key] = deepcopy(section_value)
                    if dict_entry_id in owned_ids:
                        included_ids.append(dict_entry_id)
                    else:
                        pass_through_ids.append(dict_entry_id)
                else:
                    missing_owner_ids.append(dict_entry_id)
                    reconstructed_root[section_key] = {}
            else:
                new_dict = {}
                for key, entry in section_value.items():
                    entry_id = get_entry_id(entry, fallback_key=str(key))
                    if entry_id in owned_ids:
                        new_dict[key] = deepcopy(entry)
                        included_ids.append(entry_id)
                    elif is_intercore_ref_id(entry_id):
                        new_dict[key] = deepcopy(entry)
                        pass_through_ids.append(entry_id)
                    elif entry_id is None:
                        new_dict[key] = deepcopy(entry)
                        duplicate_or_unidentified_entries.append(
                            {
                                "section": section_key,
                                "key": str(key),
                                "reason": "entry_without_id_in_dict_copied_as_passthrough",
                            }
                        )
                    else:
                        missing_owner_ids.append(entry_id)
                reconstructed_root[section_key] = new_dict

    reconstructed_doc = wrap_like_original(original_doc, reconstructed_root)

    details = {
        "included_owned_id_count": len(sorted(set(included_ids))),
        "included_owned_ids": sorted(set(included_ids)),
        "pass_through_intercore_reference_ids": sorted(set(pass_through_ids)),
        "missing_owner_ids_during_reconstruction": sorted(set(missing_owner_ids)),
        "unidentified_entries_copied_as_passthrough": duplicate_or_unidentified_entries,
    }

    return reconstructed_doc, details


def validate(repo_root: Path) -> dict[str, Any]:
    policy_doc = load_yaml(repo_root / POLICY_PATH)
    external_files = policy_external_read_only_files(policy_doc)

    targets_by_scope, owners_by_id = collect_scope_targets(repo_root, repo_root / SCOPE_DIR)
    owned_ids = set(owners_by_id)

    core_results: dict[str, Any] = {}
    blocking_findings: list[str] = []

    for core_name, rel_path in CORE_FILES.items():
        original_path = repo_root / rel_path
        original_doc = load_yaml(original_path)
        source_fp = normalized_fingerprint(original_doc)

        if core_name == "constitution":
            reconstructed_doc, details = reconstruct_constitution(original_doc, owned_ids)
            reconstruction_mode = "owned_scope_partition_plus_constitution_intercore_references"
        else:
            if rel_path.as_posix() in external_files:
                reconstructed_doc = deepcopy(original_doc)
                details = {
                    "mode": "external_read_only_passthrough",
                    "reason": "Core is classified as external_read_only for Constitution scoping.",
                }
                reconstruction_mode = "external_read_only_passthrough"
            else:
                reconstructed_doc = None
                details = {
                    "mode": "unsupported",
                    "reason": "Core is neither Constitution-owned nor external_read_only.",
                }
                reconstruction_mode = "unsupported"
                blocking_findings.append(f"{core_name}_not_reconstructable_by_policy")

        reconstructed_fp = normalized_fingerprint(reconstructed_doc)
        match = source_fp == reconstructed_fp

        if not match:
            blocking_findings.append(f"{core_name}_structural_fingerprint_mismatch")

        if core_name == "constitution":
            missing = details.get("missing_owner_ids_during_reconstruction", [])
            if missing:
                blocking_findings.append("constitution_entries_missing_from_partition")

        core_results[core_name] = {
            "status": "PASS" if match else "FAIL",
            "source_ref": rel_path.as_posix(),
            "reconstruction_mode": reconstruction_mode,
            "source_normalized_fingerprint": source_fp,
            "reconstructed_normalized_fingerprint": reconstructed_fp,
            "details": details,
        }

    status = "PASS" if not blocking_findings else "FAIL"

    return {
        "scope_partition_reconstruction_validation": {
            "schema_version": 0.1,
            "status": status,
            "validation_mode": "normalized_structural_reconstruction",
            "policy_ref": POLICY_PATH.as_posix(),
            "scope_definitions_dir": SCOPE_DIR.as_posix(),
            "scope_count": len(targets_by_scope),
            "scope_keys": sorted(targets_by_scope),
            "core_results": core_results,
            "blocking_findings": sorted(set(blocking_findings)),
            "notes": [
                "Constitution is reconstructed from generated scope target.ids plus pass-through Constitution inter-core references.",
                "Referentiel and Link are reconstructed as external_read_only passthrough cores according to policy.",
                "Comparison uses normalized YAML structural fingerprints, not byte-for-byte file comparison.",
                "This validator does not mutate canonical cores or generated catalog files.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate full structural reconstruction of scope partition.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="tmp/scope_partition_reconstruction_validation.yaml")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    out_path = repo_root / args.out

    report = validate(repo_root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(dump_yaml(report), encoding="utf-8")

    root = report["scope_partition_reconstruction_validation"]
    print(f"status: {root['status']}")
    print(f"blocking_findings: {root['blocking_findings']}")
    print(f"written: {out_path.relative_to(repo_root).as_posix()}")

    return 0 if root["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
