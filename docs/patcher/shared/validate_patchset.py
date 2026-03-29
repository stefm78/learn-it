#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Set

import yaml

SUPPORTED_OPS = {
    "assert",
    "append",
    "replace",
    "replace_field",
    "remove",
    "rename",
    "append_field_list",
    "remove_field_list_item",
    "move",
    "ensure_exists",
    "ensure_absent",
    "assert_meta",
    "replace_meta_field",
    "rewrite_references",
    "replace_text",
    "note",
    "no_change",
}

VALID_REPLACE_TEXT_SCOPES = {"meta_field", "object_field", "section_fields", "all_strings"}
ALLOWED_CORE_REF_PREFIXES = ("REF_CORE_", "LINK_REF_CORE_")
EXTERNAL_REF_SEPARATOR = "::"


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_external_core_refs(obj: Any) -> Set[str]:
    refs: Set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if "core_ref" in value and "id" in value and isinstance(value["core_ref"], str) and isinstance(value["id"], str):
                refs.add(value["core_ref"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str) and EXTERNAL_REF_SEPARATOR in value:
            core_ref, item_id = value.split(EXTERNAL_REF_SEPARATOR, 1)
            if core_ref and item_id and core_ref.startswith(ALLOWED_CORE_REF_PREFIXES):
                refs.add(core_ref)

    walk(obj)
    return refs


def validate_federation(federation: Any, errors: List[str]) -> Dict[str, Dict[str, str]]:
    normalized: Dict[str, Dict[str, str]] = {}

    if federation is None:
        return normalized

    if not isinstance(federation, dict):
        errors.append("federation doit être un objet")
        return normalized

    for core_ref, entry in federation.items():
        if not isinstance(core_ref, str) or not core_ref.startswith(ALLOWED_CORE_REF_PREFIXES):
            errors.append(f"alias federation invalide: {core_ref}")
            continue
        if not isinstance(entry, dict):
            errors.append(f"federation[{core_ref}] doit être un objet")
            continue

        file_path = entry.get("file")
        expected_core_id = entry.get("expected_core_id")
        if not isinstance(file_path, str) or not file_path:
            errors.append(f"federation[{core_ref}].file manquant ou invalide")
        if not isinstance(expected_core_id, str) or not expected_core_id:
            errors.append(f"federation[{core_ref}].expected_core_id manquant ou invalide")

        if isinstance(file_path, str) and file_path and isinstance(expected_core_id, str) and expected_core_id:
            normalized[core_ref] = {
                "file": file_path,
                "expected_core_id": expected_core_id,
            }

    return normalized


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_patchset.py <patchset.yaml>")

    path = sys.argv[1]
    doc = load_yaml(path)
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(doc, dict) or "PATCH_SET" not in doc:
        raise SystemExit("PATCH_SET absent")

    patch = doc["PATCH_SET"]
    if patch.get("patch_dsl_version") != "4.0":
        errors.append("patch_dsl_version doit être '4.0'")
    if "atomic" not in patch:
        errors.append("atomic manquant")

    report_cfg = patch.get("report")
    if report_cfg is not None:
        if not isinstance(report_cfg, dict):
            errors.append("report doit être un objet")
        else:
            if report_cfg.get("enabled") and not report_cfg.get("path"):
                errors.append("report.enabled=true exige report.path")

    federation = validate_federation(patch.get("federation"), errors)

    files = patch.get("files")
    if not isinstance(files, list) or not files:
        errors.append("files manquant ou vide")
        files = []

    used_external_core_refs: Set[str] = set()

    for file_idx, file_entry in enumerate(files):
        if not isinstance(file_entry, dict):
            errors.append(f"file[{file_idx}] invalide")
            continue

        for req in ("file", "expected_core_id", "operations"):
            if req not in file_entry:
                errors.append(f"file[{file_idx}] champ manquant: {req}")

        ops = file_entry.get("operations", [])
        if not isinstance(ops, list):
            errors.append(f"file[{file_idx}] operations n'est pas une liste")
            continue

        saw_rename = False
        saw_rewrite = False
        saw_all_strings = False

        used_external_core_refs.update(collect_external_core_refs(file_entry))

        for op_idx, op in enumerate(ops):
            if not isinstance(op, dict) or "op" not in op:
                errors.append(f"file[{file_idx}].operations[{op_idx}] opération invalide")
                continue

            op_type = op["op"]
            if op_type not in SUPPORTED_OPS:
                errors.append(f"opération non supportée: {op_type} (file {file_idx}, op {op_idx})")
                continue

            if op_type == "rename":
                saw_rename = True
                if "new_id" not in op:
                    errors.append(f"rename sans new_id (file {file_idx}, op {op_idx})")

            if op_type == "rewrite_references":
                saw_rewrite = True
                tgt = op.get("target", {})
                if "old_id" not in tgt or "new_id" not in tgt:
                    errors.append(f"rewrite_references incomplet (file {file_idx}, op {op_idx})")

            if op_type in {"assert_meta", "replace_meta_field"}:
                tgt = op.get("target", {})
                if "field" not in tgt:
                    errors.append(f"{op_type} sans target.field (file {file_idx}, op {op_idx})")

            if op_type == "replace_field":
                tgt = op.get("target", {})
                if "field" not in tgt:
                    errors.append(f"replace_field sans target.field (file {file_idx}, op {op_idx})")

            if op_type == "replace_text":
                tgt = op.get("target", {})
                scope = tgt.get("scope")
                if scope not in VALID_REPLACE_TEXT_SCOPES:
                    errors.append(f"replace_text scope invalide (file {file_idx}, op {op_idx})")
                else:
                    if scope == "meta_field" and "field" not in tgt:
                        errors.append(f"replace_text meta_field sans target.field (file {file_idx}, op {op_idx})")
                    if scope == "object_field" and not all(k in tgt for k in ("section", "id", "field")):
                        errors.append(f"replace_text object_field incomplet (file {file_idx}, op {op_idx})")
                    if scope == "section_fields":
                        if "section" not in tgt or not isinstance(tgt.get("fields"), list) or not tgt.get("fields"):
                            errors.append(f"replace_text section_fields incomplet (file {file_idx}, op {op_idx})")
                    if scope == "all_strings":
                        saw_all_strings = True

                regex_mode = bool(op.get("regex", False))
                if regex_mode:
                    if "pattern" not in op or "replacement" not in op:
                        errors.append(f"replace_text regex incomplet (file {file_idx}, op {op_idx})")
                else:
                    if "old" not in op or "new" not in op:
                        errors.append(f"replace_text littéral incomplet (file {file_idx}, op {op_idx})")

        if saw_rename and not saw_rewrite:
            warnings.append(
                f"file[{file_idx}] contient un rename sans rewrite_references explicite ; vérifier la propagation"
            )

        if saw_all_strings:
            warnings.append(
                f"file[{file_idx}] utilise replace_text scope=all_strings ; vérifier que le périmètre est bien borné"
            )

    missing_federation_refs = sorted(core_ref for core_ref in used_external_core_refs if core_ref not in federation)
    for core_ref in missing_federation_refs:
        errors.append(f"référence inter-Core utilisée sans déclaration federation: {core_ref}")

    if federation and not used_external_core_refs:
        warnings.append("federation déclarée mais aucune référence inter-Core qualifiée détectée")

    print("PATCHSET_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: patchset")
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
