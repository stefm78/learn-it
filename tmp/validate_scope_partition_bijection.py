#!/usr/bin/env python3
"""Validate Constitution scope partition bijection and external core classification.

PHASE_11 — bijection_and_reconstruction_validation

Reads:
  - docs/cores/current/constitution.yaml
  - docs/cores/current/referentiel.yaml
  - docs/cores/current/link.yaml
  - docs/pipelines/constitution/policies/scope_generation/policy.yaml
  - docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml

Writes:
  - tmp/scope_partition_bijection_validation.yaml

Validation intent:
  - Constitution business IDs must be owned by exactly one Constitution scope.
  - Referentiel/Link IDs must be explicitly classified as external_read_only.
  - Neighbor IDs must resolve to a canonical ID.
  - Generated scope definitions remain an ownership/index catalog; they do not
    carry full entry bodies, so this script performs a reconstruction readiness
    check rather than a byte-for-byte core reconstruction.

This script is read-only with regard to canonical inputs.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


CORE_FILES = {
    "constitution": Path("docs/cores/current/constitution.yaml"),
    "referentiel": Path("docs/cores/current/referentiel.yaml"),
    "link": Path("docs/cores/current/link.yaml"),
}

ENTRY_SECTIONS = [
    "SYSTEM",
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
    "REFERENCES",
    "BINDINGS",
]

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


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def normalized_fingerprint(value: Any) -> str:
    text = yaml.safe_dump(value, sort_keys=True, allow_unicode=True, default_flow_style=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def unwrap_core(data: Any) -> dict[str, Any]:
    if isinstance(data, dict) and isinstance(data.get("CORE"), dict):
        return data["CORE"]
    if isinstance(data, dict):
        return data
    return {}


def get_entry_id(entry: Any, fallback_key: str | None = None) -> str | None:
    if isinstance(entry, dict):
        for field in ID_FIELDS:
            value = entry.get(field)
            if isinstance(value, str) and value:
                return value.split("::", 1)[0]
    if fallback_key:
        return fallback_key.split("::", 1)[0]
    return None


def iter_core_entries(core_root: dict[str, Any]):
    core_id = core_root.get("id")
    if isinstance(core_id, str):
        yield "CORE", None, {
            "id": core_id,
            "version": core_root.get("version"),
            "description": core_root.get("description"),
        }

    for section in ENTRY_SECTIONS:
        value = core_root.get(section)
        if value is None:
            continue

        if isinstance(value, list):
            for entry in value:
                yield section, None, entry

        elif isinstance(value, dict):
            if get_entry_id(value):
                yield section, None, value
            else:
                for key, entry in value.items():
                    yield section, str(key), entry


def collect_canonical_ids(repo_root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    id_index: dict[str, dict[str, Any]] = {}
    ids_by_core: dict[str, list[str]] = defaultdict(list)
    duplicate_ids: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for core_name, rel_path in CORE_FILES.items():
        data = load_yaml(repo_root / rel_path)
        core_root = unwrap_core(data)
        core_id = core_root.get("id") if isinstance(core_root.get("id"), str) else None
        core_version = core_root.get("version") if isinstance(core_root.get("version"), str) else None

        for section, fallback_key, entry in iter_core_entries(core_root):
            entry_id = get_entry_id(entry, fallback_key)
            if not entry_id:
                continue

            record = {
                "id": entry_id,
                "source_core": core_name,
                "source_path": rel_path.as_posix(),
                "source_section": section,
                "source_core_id": core_id,
                "source_core_version": core_version,
                "entry_fingerprint": normalized_fingerprint(entry),
            }

            if entry_id in id_index:
                duplicate_ids[entry_id].append(record)
            else:
                id_index[entry_id] = record
                ids_by_core[core_name].append(entry_id)

    if duplicate_ids:
        # Preserve duplicate information without destroying the primary index.
        for entry_id, dupes in duplicate_ids.items():
            id_index[entry_id].setdefault("duplicates", []).extend(dupes)

    return id_index, {core: sorted(ids) for core, ids in ids_by_core.items()}


def collect_scope_catalog(scope_dir: Path) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    owners_by_id: dict[str, list[str]] = defaultdict(list)
    neighbors_by_scope: dict[str, list[str]] = {}
    targets_by_scope: dict[str, list[str]] = {}

    if not scope_dir.exists():
        raise FileNotFoundError(f"Missing scope definitions dir: {scope_dir}")

    for path in sorted(scope_dir.glob("*.yaml")):
        doc = load_yaml(path)
        root = doc.get("scope_definition", {})
        scope_key = root.get("scope_key")
        if not isinstance(scope_key, str):
            continue

        target_ids = root.get("target", {}).get("ids", []) or []
        neighbor_ids = root.get("default_neighbors_to_read", {}).get("ids", []) or []

        targets_by_scope[scope_key] = sorted(target_ids)
        neighbors_by_scope[scope_key] = sorted(neighbor_ids)

        for target_id in target_ids:
            owners_by_id[target_id].append(scope_key)

    return dict(owners_by_id), targets_by_scope, neighbors_by_scope


def policy_external_files(policy_doc: dict[str, Any]) -> set[str]:
    root = policy_doc.get("scope_generation_policy", {})
    classification = root.get("core_role_classification", {})
    files = classification.get("external_read_only_core_files", []) or []
    return set(files)


def classify_id(entry: dict[str, Any], owners: list[str], external_files: set[str]) -> str:
    source_core = entry.get("source_core")
    source_section = entry.get("source_section")
    source_path = entry.get("source_path")

    if source_section == "CORE":
        return "canonical_core_header"

    if source_core == "constitution":
        if len(owners) == 1:
            return "constitution_owned"
        if len(owners) == 0:
            return "missing_constitution_owner"
        return "duplicate_constitution_owner"

    if source_core == "referentiel" and source_path in external_files:
        return "external_read_only_referentiel"

    if source_core == "link" and source_path in external_files:
        return "external_read_only_link"

    if len(owners) == 1:
        return "owned_non_constitution_id"

    if len(owners) > 1:
        return "duplicate_non_constitution_owner"

    return "unclassified_external_or_unknown"


def build_validation(repo_root: Path, scope_dir: Path, policy_path: Path) -> dict[str, Any]:
    policy_doc = load_yaml(policy_path)
    external_files = policy_external_files(policy_doc)

    id_index, ids_by_core = collect_canonical_ids(repo_root)
    owners_by_id, targets_by_scope, neighbors_by_scope = collect_scope_catalog(scope_dir)

    all_canonical_ids = set(id_index)
    all_owned_ids = set(owners_by_id)
    all_neighbor_ids = {item for values in neighbors_by_scope.values() for item in values}

    duplicate_canonical_ids = sorted(
        entry_id for entry_id, entry in id_index.items()
        if entry.get("duplicates")
    )

    duplicate_owned_ids = sorted(
        entry_id for entry_id, owners in owners_by_id.items()
        if len(owners) > 1
    )

    extra_owned_ids_not_in_canon = sorted(all_owned_ids - all_canonical_ids)
    neighbor_ids_not_in_canon = sorted(all_neighbor_ids - all_canonical_ids)

    classifications: dict[str, list[str]] = defaultdict(list)
    classified_ids: dict[str, dict[str, Any]] = {}

    for entry_id, entry in sorted(id_index.items()):
        owners = owners_by_id.get(entry_id, [])
        classification = classify_id(entry, owners, external_files)
        classifications[classification].append(entry_id)
        classified_ids[entry_id] = {
            "source_core": entry.get("source_core"),
            "source_section": entry.get("source_section"),
            "owners": owners,
            "classification": classification,
        }

    missing_constitution_owner = sorted(classifications.get("missing_constitution_owner", []))
    duplicate_constitution_owner = sorted(classifications.get("duplicate_constitution_owner", []))
    unclassified_external_or_unknown = sorted(classifications.get("unclassified_external_or_unknown", []))

    blocking_findings = []

    if duplicate_canonical_ids:
        blocking_findings.append("duplicate_canonical_ids_detected")

    if extra_owned_ids_not_in_canon:
        blocking_findings.append("scope_owns_ids_absent_from_canon")

    if duplicate_owned_ids:
        blocking_findings.append("duplicate_scope_ownership_detected")

    if neighbor_ids_not_in_canon:
        blocking_findings.append("neighbor_ids_absent_from_canon")

    if missing_constitution_owner:
        blocking_findings.append("constitution_business_ids_without_owner")

    if duplicate_constitution_owner:
        blocking_findings.append("constitution_business_ids_with_multiple_owners")

    if unclassified_external_or_unknown:
        blocking_findings.append("external_ids_without_classification")

    status = "PASS" if not blocking_findings else "FAIL"

    source_fingerprints = {
        core_name: normalized_fingerprint(load_yaml(repo_root / rel_path))
        for core_name, rel_path in CORE_FILES.items()
    }

    return {
        "scope_partition_bijection_validation": {
            "schema_version": 0.1,
            "status": status,
            "policy_ref": policy_path.as_posix(),
            "scope_definitions_dir": scope_dir.as_posix(),
            "source_fingerprints": source_fingerprints,
            "canonical_id_summary": {
                "total_canonical_id_count": len(all_canonical_ids),
                "ids_by_core": {
                    core: len(ids)
                    for core, ids in sorted(ids_by_core.items())
                },
                "classification_counts": {
                    key: len(value)
                    for key, value in sorted(classifications.items())
                },
            },
            "ownership_bijection": {
                "status": "PASS" if not (
                    missing_constitution_owner
                    or duplicate_constitution_owner
                    or duplicate_owned_ids
                    or extra_owned_ids_not_in_canon
                ) else "FAIL",
                "missing_constitution_owner_ids": missing_constitution_owner,
                "duplicate_constitution_owner_ids": duplicate_constitution_owner,
                "duplicate_owned_ids": duplicate_owned_ids,
                "extra_owned_ids_not_in_canon": extra_owned_ids_not_in_canon,
                "targets_by_scope": targets_by_scope,
            },
            "external_read_only_classification": {
                "status": "PASS" if not unclassified_external_or_unknown else "FAIL",
                "external_read_only_core_files": sorted(external_files),
                "external_read_only_referentiel_count": len(classifications.get("external_read_only_referentiel", [])),
                "external_read_only_link_count": len(classifications.get("external_read_only_link", [])),
                "unclassified_external_or_unknown_ids": unclassified_external_or_unknown,
            },
            "neighbor_validation": {
                "status": "PASS" if not neighbor_ids_not_in_canon else "FAIL",
                "neighbor_ids_not_in_canon": neighbor_ids_not_in_canon,
                "neighbors_by_scope": neighbors_by_scope,
            },
            "reconstruction_readiness": {
                "status": "PASS" if status == "PASS" else "BLOCKED",
                "mode": "id_partition_readiness",
                "note": (
                    "Generated scope definitions are an ownership/index catalog and do not carry full entry bodies. "
                    "Full structural reconstruction must be validated later from source cores plus scope extracts or a "
                    "content-carrying partition artifact."
                ),
                "constitution_business_ids_are_partitioned": not missing_constitution_owner and not duplicate_constitution_owner,
                "referentiel_link_are_explicitly_classified": not unclassified_external_or_unknown,
            },
            "blocking_findings": blocking_findings,
            "warnings": [
                "CORE header IDs are classified as canonical_core_header and are not required to be owned by a scope.",
                "This validator checks ID-level bijection. It does not prove byte-for-byte YAML reconstruction.",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Constitution scope partition bijection.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--scope-dir",
        default="docs/pipelines/constitution/scope_catalog/scope_definitions",
    )
    parser.add_argument(
        "--policy",
        default="docs/pipelines/constitution/policies/scope_generation/policy.yaml",
    )
    parser.add_argument(
        "--out",
        default="tmp/scope_partition_bijection_validation.yaml",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    scope_dir = repo_root / args.scope_dir
    policy_path = repo_root / args.policy
    out_path = repo_root / args.out

    report = build_validation(repo_root, scope_dir, policy_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(dump_yaml(report), encoding="utf-8")

    root = report["scope_partition_bijection_validation"]
    print(f"status: {root['status']}")
    print(f"blocking_findings: {root['blocking_findings']}")
    print(f"written: {out_path.relative_to(repo_root).as_posix()}")

    return 0 if root["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
