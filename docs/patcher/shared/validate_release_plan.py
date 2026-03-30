#!/usr/bin/env python3
import sys
from typing import Any, Dict, List

import yaml


DEFAULT_SCHEMA_PATH = "docs/specs/core-release/release_plan.schema.yaml"
EXPECTED_TARGET_VERSION_KEYS = ["constitution", "referentiel", "link"]
COMMON_TARGET_VERSION_FIELDS = [
    "current_core_id",
    "current_version",
    "target_core_id",
    "target_version",
]


def load_yaml(path: str) -> Any:
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


def validate_against_schema(plan: Dict[str, Any], schema: Dict[str, Any], errors: List[str], warnings: List[str]) -> None:
    required_fields = schema.get("required", [])
    fields = schema.get("fields", {})

    if not isinstance(required_fields, list):
        errors.append("schema.required doit être une liste")
        required_fields = []
    if not isinstance(fields, dict):
        errors.append("schema.fields doit être un objet")
        fields = {}

    for field_name in required_fields:
        if field_name not in plan:
            errors.append(f"champ requis manquant: {field_name}")

    for field_name, rules in fields.items():
        if not isinstance(rules, dict):
            errors.append(f"schema.fields[{field_name}] invalide")
            continue

        required = bool(rules.get("required", False))
        if field_name not in plan:
            if required:
                errors.append(f"champ requis manquant: {field_name}")
            continue

        value = plan[field_name]
        expected_type = rules.get("type")
        if isinstance(expected_type, str) and not ensure_type(value, expected_type):
            errors.append(f"{field_name} doit être de type {expected_type}")
            continue

        if expected_type == "enum":
            allowed = rules.get("values", [])
            if value not in allowed:
                errors.append(f"{field_name} doit être dans {allowed}")

        if expected_type == "map":
            expected_keys = rules.get("expected_keys", [])
            if isinstance(expected_keys, list):
                for key in expected_keys:
                    if key not in value:
                        errors.append(f"{field_name} doit contenir la clé {key}")

            required_keys = rules.get("required_keys", [])
            if isinstance(required_keys, list):
                for key in required_keys:
                    if key not in value:
                        errors.append(f"{field_name} doit contenir la clé requise {key}")

            nested_fields = rules.get("fields", {})
            if isinstance(nested_fields, dict):
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
                        continue
                    if nested_type == "enum":
                        allowed_nested = nested_rules.get("values", [])
                        if value[nested_name] not in allowed_nested:
                            errors.append(f"{field_name}.{nested_name} doit être dans {allowed_nested}")

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
            if required_item_keys and isinstance(required_item_keys, list):
                for idx, item in enumerate(value):
                    if not isinstance(item, dict):
                        errors.append(f"{field_name}[{idx}] doit être un objet")
                        continue
                    for key in required_item_keys:
                        if key not in item:
                            errors.append(f"{field_name}[{idx}] doit contenir la clé {key}")

    status = plan.get("status")
    release_required = plan.get("release_required")
    change_depth = plan.get("change_depth")

    if status == "FAIL" and not isinstance(release_required, bool):
        errors.append("status=FAIL exige release_required explicitement renseigné")

    if isinstance(release_required, bool) and isinstance(change_depth, str):
        if release_required and change_depth == "none":
            warnings.append("release_required=true avec change_depth=none ; vérifier la nécessité réelle de la release")
        if not release_required and change_depth in {"minor", "major"}:
            warnings.append("release_required=false avec change_depth significatif ; vérifier l'intention")


def validate_target_versions(target_versions: Any, errors: List[str], warnings: List[str]) -> None:
    if not isinstance(target_versions, dict):
        errors.append("target_versions doit être un objet")
        return

    for role in EXPECTED_TARGET_VERSION_KEYS:
        if role not in target_versions:
            errors.append(f"target_versions doit contenir le rôle {role}")
            continue
        entry = target_versions[role]
        if not isinstance(entry, dict):
            errors.append(f"target_versions.{role} doit être un objet")
            continue
        for key in COMMON_TARGET_VERSION_FIELDS:
            if key not in entry:
                warnings.append(f"target_versions.{role}.{key} absent ; structure minimale tolérée mais incomplète pour certains usages")
            elif not isinstance(entry[key], str) or not entry[key]:
                errors.append(f"target_versions.{role}.{key} doit être une chaîne non vide")

    extra_roles = sorted(set(target_versions.keys()) - set(EXPECTED_TARGET_VERSION_KEYS))
    for role in extra_roles:
        warnings.append(f"target_versions contient un rôle supplémentaire non standard: {role}")


def validate_release_bundle(release_bundle: Any, errors: List[str], warnings: List[str]) -> None:
    if not isinstance(release_bundle, dict):
        errors.append("release_bundle doit être un objet")
        return

    release_id = release_bundle.get("release_id")
    release_path = release_bundle.get("release_path")
    promotion_candidate = release_bundle.get("promotion_candidate")

    if not isinstance(release_id, str) or not release_id:
        errors.append("release_bundle.release_id manquant ou invalide")
    elif not release_id.startswith("CORE_RELEASE_"):
        warnings.append("release_bundle.release_id ne suit pas le préfixe recommandé CORE_RELEASE_")

    if not isinstance(release_path, str) or not release_path:
        errors.append("release_bundle.release_path manquant ou invalide")
    elif not release_path.startswith("docs/cores/releases/"):
        warnings.append("release_bundle.release_path devrait pointer sous docs/cores/releases/")

    if promotion_candidate is not None and not isinstance(promotion_candidate, bool):
        errors.append("release_bundle.promotion_candidate doit être booléen si présent")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_release_plan.py <release_plan.yaml> [schema.yaml]")

    plan_path = sys.argv[1]
    schema_path = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_SCHEMA_PATH

    doc = load_yaml(plan_path)
    schema_doc = load_yaml(schema_path)

    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(schema_doc, dict) or "SCHEMA" not in schema_doc:
        raise SystemExit("SCHEMA absent du fichier de schéma")
    schema = schema_doc["SCHEMA"]
    if not isinstance(schema, dict):
        raise SystemExit("SCHEMA invalide")

    root_key = schema.get("root_key")
    if not isinstance(root_key, str) or not root_key:
        raise SystemExit("root_key manquant dans le schéma")

    if not isinstance(doc, dict) or root_key not in doc:
        raise SystemExit(f"{root_key} absent")

    plan = doc[root_key]
    if not isinstance(plan, dict):
        raise SystemExit(f"{root_key} invalide")

    validate_against_schema(plan, schema, errors, warnings)
    validate_target_versions(plan.get("target_versions"), errors, warnings)
    validate_release_bundle(plan.get("release_bundle"), errors, warnings)

    print("RELEASE_PLAN_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: release_plan")
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
