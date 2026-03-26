#!/usr/bin/env python3
import sys
from typing import Any, Dict, List

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
    "note",
    "no_change",
}


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_patchset_v3.py <patchset.yaml>")

    path = sys.argv[1]
    doc = load_yaml(path)
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(doc, dict) or "PATCH_SET" not in doc:
        raise SystemExit("PATCH_SET absent")

    patch = doc["PATCH_SET"]
    if patch.get("patch_dsl_version") != "3.0":
        errors.append("patch_dsl_version doit être '3.0'")
    if "atomic" not in patch:
        errors.append("atomic manquant")
    files = patch.get("files")
    if not isinstance(files, list) or not files:
        errors.append("files manquant ou vide")
        files = []

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
        saw_meta_change = False
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
                saw_meta_change = True
                tgt = op.get("target", {})
                if "field" not in tgt:
                    errors.append(f"{op_type} sans target.field (file {file_idx}, op {op_idx})")
            if op_type == "replace_field":
                tgt = op.get("target", {})
                if "field" not in tgt:
                    errors.append(f"replace_field sans target.field (file {file_idx}, op {op_idx})")
        if saw_rename and not saw_rewrite:
            warnings.append(
                f"file[{file_idx}] contient un rename sans rewrite_references explicite ; vérifier la propagation"
            )
        if saw_meta_change and not any(op.get("op") == "assert_meta" for op in ops if isinstance(op, dict)):
            warnings.append(
                f"file[{file_idx}] modifie des meta fields sans assert_meta préalable"
            )

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
