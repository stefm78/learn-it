#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


DEFAULT_SCHEMA_PATH = "docs/specs/core-release/promotion_report.schema.yaml"
ROOT_KEY = "PROMOTION_REPORT"
CURRENT_ROOT_KEY = "CURRENT_CORESET"
RELEASE_ROOT_KEY = "RELEASE_MANIFEST"
ALLOWED_STATUS = {"PASS", "FAIL"}
ALLOWED_PROMOTION_MODES = {"applied", "already_current", "failed"}


class PromotionReportValidationError(Exception):
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


def validate_against_schema(report: Dict[str, Any], schema: Dict[str, Any], errors: List[str]) -> None:
    required_fields = schema.get("required", [])
    fields = schema.get("fields", {})

    if not isinstance(required_fields, list):
        errors.append("schema.required doit être une liste")
        required_fields = []
    if not isinstance(fields, dict):
        errors.append("schema.fields doit être un objet")
        fields = {}

    for field_name in required_fields:
        if field_name not in report:
            errors.append(f"champ requis manquant: {field_name}")

    for field_name, rules in fields.items():
        if not isinstance(rules, dict):
            errors.append(f"schema.fields[{field_name}] invalide")
            continue

        required = bool(rules.get("required", False))
        if field_name not in report:
            if required:
                errors.append(f"champ requis manquant: {field_name}")
            continue

        value = report[field_name]
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


def read_rooted_yaml(path: Path, root_key: str) -> Dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or root_key not in doc:
        raise PromotionReportValidationError(f"{root_key} absent dans {path}")
    root = doc[root_key]
    if not isinstance(root, dict):
        raise PromotionReportValidationError(f"{root_key} invalide dans {path}")
    return root


def validate_report_semantics(report: Dict[str, Any], errors: List[str], warnings: List[str]) -> None:
    status = report.get("status")
    release_id = report.get("release_id")
    source_release_path = report.get("source_release_path")
    promotion_mode = report.get("promotion_mode")
    files_promoted = report.get("files_promoted")
    current_manifest_updated = report.get("current_manifest_updated")

    if status not in ALLOWED_STATUS:
        errors.append(f"status doit être dans {sorted(ALLOWED_STATUS)}")
    if not isinstance(release_id, str) or not release_id:
        errors.append("release_id absent ou invalide")
    elif not release_id.startswith("CORE_RELEASE_"):
        warnings.append("release_id ne suit pas le préfixe recommandé CORE_RELEASE_")

    if not isinstance(source_release_path, str) or not source_release_path:
        errors.append("source_release_path absent ou invalide")
    elif not source_release_path.startswith("docs/cores/releases/"):
        warnings.append("source_release_path devrait pointer sous docs/cores/releases/")

    if promotion_mode not in ALLOWED_PROMOTION_MODES:
        errors.append(f"promotion_mode doit être dans {sorted(ALLOWED_PROMOTION_MODES)}")

    if not isinstance(files_promoted, list):
        errors.append("files_promoted doit être une liste")
    else:
        for idx, path in enumerate(files_promoted):
            if not isinstance(path, str) or not path:
                errors.append(f"files_promoted[{idx}] invalide")
                continue
            if not path.startswith("docs/cores/current/"):
                errors.append(f"files_promoted[{idx}] doit pointer sous docs/cores/current/")

    if current_manifest_updated is not None and not isinstance(current_manifest_updated, bool):
        errors.append("current_manifest_updated doit être booléen si présent")

    if status == "PASS" and promotion_mode == "failed":
        errors.append("status=PASS est incohérent avec promotion_mode=failed")
    if status == "FAIL" and promotion_mode != "failed":
        warnings.append("status=FAIL avec promotion_mode différent de failed ; vérifier l'intention")

    if promotion_mode == "already_current" and files_promoted:
        warnings.append("already_current avec files_promoted non vide ; vérifier l'idempotence")
    if promotion_mode == "applied" and isinstance(current_manifest_updated, bool) and not current_manifest_updated:
        warnings.append("applied avec current_manifest_updated=false ; vérifier le flux")


def validate_against_release_and_current(report: Dict[str, Any], errors: List[str], warnings: List[str]) -> None:
    release_id = report.get("release_id")
    source_release_path = report.get("source_release_path")
    promotion_mode = report.get("promotion_mode")

    if not isinstance(source_release_path, str) or not source_release_path:
        return

    release_path = Path(source_release_path)
    release_manifest_path = release_path / "manifest.yaml"
    if not release_manifest_path.exists():
        errors.append(f"manifest de release source absent: {release_manifest_path}")
        return

    try:
        release_manifest = read_rooted_yaml(release_manifest_path, RELEASE_ROOT_KEY)
    except Exception as exc:
        errors.append(str(exc))
        return

    release_manifest_id = release_manifest.get("release_id")
    if release_manifest_id != release_id:
        errors.append(
            f"release_id incohérent entre promotion report et manifest de release: report={release_id} release={release_manifest_id}"
        )

    current_manifest_path = Path("docs/cores/current/manifest.yaml")
    if promotion_mode in {"applied", "already_current"}:
        if not current_manifest_path.exists():
            errors.append("current manifest absent alors que la promotion est censée être active")
            return
        try:
            current_manifest = read_rooted_yaml(current_manifest_path, CURRENT_ROOT_KEY)
        except Exception as exc:
            errors.append(str(exc))
            return

        current_release_id = current_manifest.get("release_id")
        current_source_release_path = current_manifest.get("source_release_path")
        if current_release_id != release_id:
            errors.append(
                f"release_id incohérent entre promotion report et current manifest: report={release_id} current={current_release_id}"
            )
        if current_source_release_path != source_release_path:
            errors.append(
                "source_release_path incohérent entre promotion report et current manifest"
            )

        current_cores = current_manifest.get("cores")
        release_cores = release_manifest.get("cores")
        if isinstance(current_cores, list) and isinstance(release_cores, list):
            release_by_role = {
                entry.get("role"): entry for entry in release_cores if isinstance(entry, dict) and isinstance(entry.get("role"), str)
            }
            for entry in current_cores:
                if not isinstance(entry, dict):
                    continue
                role = entry.get("role")
                if not isinstance(role, str):
                    continue
                release_entry = release_by_role.get(role)
                if release_entry is None:
                    errors.append(f"rôle {role} absent du manifest de release source")
                    continue
                for field_name in ("file", "core_id", "version"):
                    if entry.get(field_name) != release_entry.get(field_name):
                        errors.append(
                            f"current manifest non aligné avec la release pour rôle {role} champ {field_name}"
                        )
        else:
            warnings.append("impossible de comparer finement current manifest et release manifest")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_promotion_report.py <promotion_report.yaml> [schema.yaml]")

    report_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(DEFAULT_SCHEMA_PATH)

    report_doc = load_yaml(report_path)
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

    if not isinstance(report_doc, dict) or ROOT_KEY not in report_doc:
        raise SystemExit(f"{ROOT_KEY} absent")
    report = report_doc[ROOT_KEY]
    if not isinstance(report, dict):
        raise SystemExit(f"{ROOT_KEY} invalide")

    validate_against_schema(report, schema, errors)
    validate_report_semantics(report, errors, warnings)
    validate_against_release_and_current(report, errors, warnings)

    print("PROMOTION_REPORT_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: promotion_report")
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
