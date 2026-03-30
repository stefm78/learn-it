#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml


DEFAULT_SCHEMA_PATH = "docs/specs/core-release/release_manifest.schema.yaml"
ROOT_KEY = "RELEASE_MANIFEST"
EXPECTED_ROLES = {"constitution", "referentiel", "link"}
EXPECTED_STATUS_VALUES = {"READY", "FAILED"}


class ReleaseManifestValidationError(Exception):
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


def validate_against_schema(manifest: Dict[str, Any], schema: Dict[str, Any], errors: List[str]) -> None:
    required_fields = schema.get("required", [])
    fields = schema.get("fields", {})

    if not isinstance(required_fields, list):
        errors.append("schema.required doit être une liste")
        required_fields = []
    if not isinstance(fields, dict):
        errors.append("schema.fields doit être un objet")
        fields = {}

    for field_name in required_fields:
        if field_name not in manifest:
            errors.append(f"champ requis manquant: {field_name}")

    for field_name, rules in fields.items():
        if not isinstance(rules, dict):
            errors.append(f"schema.fields[{field_name}] invalide")
            continue

        required = bool(rules.get("required", False))
        if field_name not in manifest:
            if required:
                errors.append(f"champ requis manquant: {field_name}")
            continue

        value = manifest[field_name]
        expected_type = rules.get("type")
        if isinstance(expected_type, str) and not ensure_type(value, expected_type):
            errors.append(f"{field_name} doit être de type {expected_type}")
            continue

        if expected_type == "enum":
            allowed = rules.get("values", [])
            if value not in allowed:
                errors.append(f"{field_name} doit être dans {allowed}")

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

        if expected_type == "map":
            nested_fields = rules.get("fields", {})
            if isinstance(nested_fields, dict) and isinstance(value, dict):
                for nested_name, nested_rules in nested_fields.items():
                    if not isinstance(nested_rules, dict):
                        errors.append(f"{field_name}.{nested_name} a des règles invalides")
                        continue
                    nested_required = bool(nested_rules.get("required", False))
                    if nested_name not in value:
                        if nested_required:
                            errors.append(f"{field_name}.{nested_name} manquant")
                        continue
                    nested_type = nested_rules.get("type")
                    if isinstance(nested_type, str) and not ensure_type(value[nested_name], nested_type):
                        errors.append(f"{field_name}.{nested_name} doit être de type {nested_type}")


def validate_cores_section(manifest: Dict[str, Any], manifest_path: Path, errors: List[str], warnings: List[str]) -> None:
    cores = manifest.get("cores")
    if not isinstance(cores, list):
        errors.append("cores doit être une liste")
        return

    roles_seen: Set[str] = set()
    files_seen: Set[str] = set()
    release_dir = manifest_path.parent

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

        file_path = release_dir / file_name
        if not file_path.exists():
            errors.append(f"fichier déclaré absent du répertoire release: {file_path}")
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


def validate_release_manifest_semantics(manifest: Dict[str, Any], manifest_path: Path, errors: List[str], warnings: List[str]) -> None:
    release_id = manifest.get("release_id")
    status = manifest.get("status")
    immutable = manifest.get("immutable")
    provenance = manifest.get("provenance")
    promotion = manifest.get("promotion")

    if not isinstance(release_id, str) or not release_id:
        errors.append("release_id absent ou invalide")
    elif not release_id.startswith("CORE_RELEASE_"):
        warnings.append("release_id ne suit pas le préfixe recommandé CORE_RELEASE_")

    if status not in EXPECTED_STATUS_VALUES:
        errors.append(f"status doit être dans {sorted(EXPECTED_STATUS_VALUES)}")

    if status == "READY" and immutable is not True:
        errors.append("immutable doit être true pour une release READY")

    if not isinstance(provenance, dict) or not provenance:
        errors.append("provenance absent ou invalide")
    elif "release_plan" not in provenance:
        warnings.append("provenance.release_plan absent ; traçabilité amont incomplète")

    if isinstance(promotion, dict):
        promotion_candidate = promotion.get("promotion_candidate")
        promoted_to_current = promotion.get("promoted_to_current")
        if promotion_candidate is not None and not isinstance(promotion_candidate, bool):
            errors.append("promotion.promotion_candidate doit être booléen")
        if promoted_to_current is not None and not isinstance(promoted_to_current, bool):
            errors.append("promotion.promoted_to_current doit être booléen")

    manifest_parent = manifest_path.parent.as_posix()
    if "/docs/cores/releases/" not in f"/{manifest_parent}" and not manifest_parent.startswith("docs/cores/releases/"):
        warnings.append("le manifest n'est pas situé sous docs/cores/releases/")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_release_manifest.py <manifest.yaml> [schema.yaml]")

    manifest_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(DEFAULT_SCHEMA_PATH)

    manifest_doc = load_yaml(manifest_path)
    schema_doc = load_yaml(schema_path)

    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(schema_doc, dict) or "SCHEMA" not in schema_doc:
        raise SystemExit("SCHEMA absent du fichier de schéma")
    schema = schema_doc["SCHEMA"]
    if not isinstance(schema, dict):
        raise SystemExit("SCHEMA invalide")

    root_key = schema.get("root_key")
    if root_key != ROOT_KEY:
        raise SystemExit(f"root_key inattendu dans le schéma: {root_key}")

    if not isinstance(manifest_doc, dict) or ROOT_KEY not in manifest_doc:
        raise SystemExit(f"{ROOT_KEY} absent")
    manifest = manifest_doc[ROOT_KEY]
    if not isinstance(manifest, dict):
        raise SystemExit(f"{ROOT_KEY} invalide")

    validate_against_schema(manifest, schema, errors)
    validate_release_manifest_semantics(manifest, manifest_path, errors, warnings)
    validate_cores_section(manifest, manifest_path, errors, warnings)

    print("RELEASE_MANIFEST_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: release_manifest")
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
