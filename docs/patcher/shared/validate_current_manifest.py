#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml


DEFAULT_SCHEMA_PATH = "docs/specs/core-release/current_manifest.schema.yaml"
CURRENT_ROOT_KEY = "CURRENT_CORESET"
RELEASE_ROOT_KEY = "RELEASE_MANIFEST"
EXPECTED_ROLES = {"constitution", "referentiel", "link"}
EXPECTED_PROMOTION_MODES = {"applied", "already_current"}


class CurrentManifestValidationError(Exception):
    pass


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_type(value: Any, expected_type: str) -> bool:
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "map":
        return isinstance(value, dict)
    if expected_type == "list":
        return isinstance(value, list)
    if expected_type == "enum":
        return isinstance(value, str)
    return True


def validate_against_schema(current: Dict[str, Any], schema: Dict[str, Any], errors: List[str]) -> None:
    required_fields = schema.get("required", [])
    fields = schema.get("fields", {})

    if not isinstance(required_fields, list):
        errors.append("schema.required doit être une liste")
        required_fields = []
    if not isinstance(fields, dict):
        errors.append("schema.fields doit être un objet")
        fields = {}

    for field_name in required_fields:
        if field_name not in current:
            errors.append(f"champ requis manquant: {field_name}")

    for field_name, rules in fields.items():
        if not isinstance(rules, dict):
            errors.append(f"schema.fields[{field_name}] invalide")
            continue

        required = bool(rules.get("required", False))
        if field_name not in current:
            if required:
                errors.append(f"champ requis manquant: {field_name}")
            continue

        value = current[field_name]
        expected_type = rules.get("type")
        if isinstance(expected_type, str) and not ensure_type(value, expected_type):
            errors.append(f"{field_name} doit être de type {expected_type}")
            continue

        if expected_type == "list":
            item_type = rules.get("item_type")
            if isinstance(item_type, str):
                for idx, item in enumerate(value):
                    if not ensure_type(item, item_type):
                        errors.append(f"{field_name}[{idx}] doit être de type {item_type}")

            min_items = rules.get("min_items")
            if isinstance(min_items, int) and len(value) < min_items:
                errors.append(f"{field_name} doit contenir au moins {min_items} éléments")

            required_item_keys = rules.get("required_item_keys", [])
            if isinstance(required_item_keys, list):
                for idx, item in enumerate(value):
                    if not isinstance(item, dict):
                        continue
                    for key in required_item_keys:
                        if key not in item:
                            errors.append(f"{field_name}[{idx}] doit contenir la clé {key}")


def read_rooted_yaml(path: Path, root_key: str) -> Dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or root_key not in doc:
        raise CurrentManifestValidationError(f"{root_key} absent dans {path}")
    root = doc[root_key]
    if not isinstance(root, dict):
        raise CurrentManifestValidationError(f"{root_key} invalide dans {path}")
    return root


def validate_cores_section(current: Dict[str, Any], current_manifest_path: Path, errors: List[str], warnings: List[str]) -> None:
    cores = current.get("cores")
    if not isinstance(cores, list):
        errors.append("cores doit être une liste")
        return

    roles_seen: Set[str] = set()
    files_seen: Set[str] = set()
    current_dir = current_manifest_path.parent

    for idx, entry in enumerate(cores):
        if not isinstance(entry, dict):
            errors.append(f"cores[{idx}] doit être un objet")
            continue

        role = entry.get("role")
        file_name = entry.get("file")
        core_id = entry.get("core_id")
        version = entry.get("version")

        if not isinstance(role, str) or not role:
            errors.append(f"cores[{idx}].role absent ou invalide")
            continue
        if role not in EXPECTED_ROLES:
            errors.append(f"cores[{idx}].role invalide: {role}")
            continue
        if role in roles_seen:
            errors.append(f"rôle dupliqué dans cores: {role}")
        roles_seen.add(role)

        if not isinstance(file_name, str) or not file_name:
            errors.append(f"cores[{idx}].file absent ou invalide")
            continue
        if file_name in files_seen:
            errors.append(f"fichier dupliqué dans cores: {file_name}")
        files_seen.add(file_name)
        if not file_name.endswith(".yaml"):
            warnings.append(f"cores[{idx}].file ne se termine pas par .yaml: {file_name}")

        if not isinstance(core_id, str) or not core_id:
            errors.append(f"cores[{idx}].core_id absent ou invalide")
        if not isinstance(version, str) or not version:
            errors.append(f"cores[{idx}].version absente ou invalide")

        file_path = current_dir / file_name
        if not file_path.exists():
            errors.append(f"fichier déclaré absent du répertoire current: {file_path}")
            continue

        doc = load_yaml(file_path)
        if not isinstance(doc, dict) or "CORE" not in doc or not isinstance(doc["CORE"], dict):
            errors.append(f"fichier Core invalide ou sans racine CORE: {file_path}")
            continue

        core = doc["CORE"]
        actual_core_id = core.get("id")
        actual_version = core.get("version")
        if actual_core_id != core_id:
            errors.append(
                f"mismatch core_id pour {file_name}: manifest={core_id} fichier={actual_core_id}"
            )
        if actual_version != version:
            errors.append(
                f"mismatch version pour {file_name}: manifest={version} fichier={actual_version}"
            )

    missing_roles = sorted(EXPECTED_ROLES - roles_seen)
    extra_roles = sorted(roles_seen - EXPECTED_ROLES)
    for role in missing_roles:
        errors.append(f"rôle manquant dans cores: {role}")
    for role in extra_roles:
        errors.append(f"rôle inattendu dans cores: {role}")


def validate_derivation_from_release(current: Dict[str, Any], errors: List[str], warnings: List[str]) -> None:
    release_id = current.get("release_id")
    source_release_path = current.get("source_release_path")
    current_cores = current.get("cores")

    if not isinstance(release_id, str) or not release_id:
        errors.append("release_id absent ou invalide")
        return
    if not release_id.startswith("CORE_RELEASE_"):
        warnings.append("release_id ne suit pas le préfixe recommandé CORE_RELEASE_")

    if not isinstance(source_release_path, str) or not source_release_path:
        errors.append("source_release_path absent ou invalide")
        return

    release_path = Path(source_release_path)
    manifest_path = release_path / "manifest.yaml"
    if not manifest_path.exists():
        errors.append(f"manifest de release source absent: {manifest_path}")
        return

    try:
        release_manifest = read_rooted_yaml(manifest_path, RELEASE_ROOT_KEY)
    except Exception as exc:
        errors.append(str(exc))
        return

    release_manifest_id = release_manifest.get("release_id")
    if release_manifest_id != release_id:
        errors.append(
            f"release_id incohérent entre current manifest et release source: current={release_id} release={release_manifest_id}"
        )

    release_cores = release_manifest.get("cores")
    if not isinstance(release_cores, list):
        errors.append("cores absent ou invalide dans le release manifest source")
        return
    if not isinstance(current_cores, list):
        errors.append("cores absent ou invalide dans le current manifest")
        return

    release_by_role: Dict[str, Dict[str, Any]] = {}
    for entry in release_cores:
        if isinstance(entry, dict) and isinstance(entry.get("role"), str):
            release_by_role[entry["role"]] = entry

    for entry in current_cores:
        if not isinstance(entry, dict):
            continue
        role = entry.get("role")
        if not isinstance(role, str):
            continue
        release_entry = release_by_role.get(role)
        if release_entry is None:
            errors.append(f"rôle {role} absent du release manifest source")
            continue
        for field_name in ("file", "core_id", "version"):
            if entry.get(field_name) != release_entry.get(field_name):
                errors.append(
                    f"current manifest non dérivé fidèlement de la release pour rôle {role} champ {field_name}: current={entry.get(field_name)} release={release_entry.get(field_name)}"
                )


def validate_current_manifest_semantics(current: Dict[str, Any], current_manifest_path: Path, errors: List[str], warnings: List[str]) -> None:
    promoted_at = current.get("promoted_at")
    status = current.get("status")
    promotion_mode = current.get("promotion_mode")

    if not isinstance(promoted_at, str) or not promoted_at:
        errors.append("promoted_at absent ou invalide")

    if status is not None and not isinstance(status, str):
        errors.append("status doit être une chaîne si présent")
    elif status == "":
        errors.append("status ne doit pas être vide")

    if promotion_mode is not None and not isinstance(promotion_mode, str):
        errors.append("promotion_mode doit être une chaîne si présent")
    elif isinstance(promotion_mode, str) and promotion_mode not in EXPECTED_PROMOTION_MODES:
        warnings.append(
            f"promotion_mode non standard: {promotion_mode} ; valeurs attendues {sorted(EXPECTED_PROMOTION_MODES)}"
        )

    current_dir = current_manifest_path.parent.as_posix()
    if not current_dir.endswith("docs/cores/current") and current_dir != "docs/cores/current":
        warnings.append("le current manifest n'est pas situé sous docs/cores/current")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_current_manifest.py <current_manifest.yaml> [schema.yaml]")

    current_manifest_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(DEFAULT_SCHEMA_PATH)

    current_doc = load_yaml(current_manifest_path)
    schema_doc = load_yaml(schema_path)

    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(schema_doc, dict) or "SCHEMA" not in schema_doc:
        raise SystemExit("SCHEMA absent du fichier de schéma")
    schema = schema_doc["SCHEMA"]
    if not isinstance(schema, dict):
        raise SystemExit("SCHEMA invalide")

    root_key = schema.get("root_key")
    if root_key != CURRENT_ROOT_KEY:
        raise SystemExit(f"root_key inattendu dans le schéma: {root_key}")

    if not isinstance(current_doc, dict) or CURRENT_ROOT_KEY not in current_doc:
        raise SystemExit(f"{CURRENT_ROOT_KEY} absent")
    current = current_doc[CURRENT_ROOT_KEY]
    if not isinstance(current, dict):
        raise SystemExit(f"{CURRENT_ROOT_KEY} invalide")

    validate_against_schema(current, schema, errors)
    validate_current_manifest_semantics(current, current_manifest_path, errors, warnings)
    validate_cores_section(current, current_manifest_path, errors, warnings)
    validate_derivation_from_release(current, errors, warnings)

    print("CURRENT_MANIFEST_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: current_manifest")
    print(f"  schema_id: {schema.get('id', 'unknown')}")
    print(f"  anomalies_count: {len(errors)}")
    print(f"  warnings_count: {len(warnings)}")
    print("  anomalies:")
    if errors:
        for err in errors:
            print(f"    - {err}")
    else:
        print("    - none")
    print("  warnings:")
    if warnings:
        for warn in warnings:
            print(f"    - {warn}")
    else:
        print("    - none")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
