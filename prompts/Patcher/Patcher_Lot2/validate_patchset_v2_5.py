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
    "note",
    "no_change",
}

class ValidationError(Exception):
    pass


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValidationError(msg)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_patchset_v2_5.py <patchfile>")
    path = sys.argv[1]
    doc = load_yaml(path)
    require(isinstance(doc, dict) and "PATCH_SET" in doc, "PATCH_SET absent")
    ps = doc["PATCH_SET"]
    require(isinstance(ps, dict), "PATCH_SET invalide")
    require(isinstance(ps.get("id"), str) and ps.get("id"), "PATCH_SET.id absent")
    require(ps.get("patch_dsl_version") in {"2.0", "2.5"} or ps.get("patch_dsl_version") is None, "patch_dsl_version invalide")
    require("atomic" in ps, "PATCH_SET.atomic absent")
    files = ps.get("files")
    require(isinstance(files, list) and len(files) > 0, "PATCH_SET.files absent ou invalide")

    seen_ops: List[str] = []
    for file_idx, file_entry in enumerate(files):
        require(isinstance(file_entry, dict), f"file entry invalide index={file_idx}")
        require(isinstance(file_entry.get("file"), str) and file_entry.get("file"), f"file absent index={file_idx}")
        require(isinstance(file_entry.get("expected_core_id"), str) and file_entry.get("expected_core_id"), f"expected_core_id absent index={file_idx}")
        ops = file_entry.get("operations")
        require(isinstance(ops, list), f"operations invalide index={file_idx}")
        for op_idx, op in enumerate(ops):
            require(isinstance(op, dict), f"op invalide file={file_idx} op={op_idx}")
            op_type = op.get("op")
            require(op_type in SUPPORTED_OPS, f"op non supportée file={file_idx} op={op_idx}: {op_type}")
            seen_ops.append(op_type)
            if op_type not in {"note", "no_change"}:
                target = op.get("target")
                require(isinstance(target, dict), f"target absent file={file_idx} op={op_idx}")
                require(isinstance(target.get("section"), str) and target.get("section"), f"target.section absent file={file_idx} op={op_idx}")
                require(isinstance(target.get("id"), str) and target.get("id"), f"target.id absent file={file_idx} op={op_idx}")
            if op_type == "replace_field":
                require(isinstance(op.get("target", {}).get("field"), str), f"target.field absent file={file_idx} op={op_idx}")
            if op_type in {"append", "replace", "ensure_exists"}:
                require("value" in op or "values" in op, f"value(s) absent file={file_idx} op={op_idx}")
            if op_type == "rename":
                require(isinstance(op.get("new_id"), str) and op.get("new_id"), f"new_id absent file={file_idx} op={op_idx}")
            if op_type in {"append_field_list", "remove_field_list_item"}:
                require(isinstance(op.get("target", {}).get("field"), str), f"target.field absent file={file_idx} op={op_idx}")
                require("value" in op, f"value absent file={file_idx} op={op_idx}")
            if op_type == "move":
                dest = op.get("destination")
                require(isinstance(dest, dict), f"destination absente file={file_idx} op={op_idx}")
                require(isinstance(dest.get("section"), str) and dest.get("section"), f"destination.section absente file={file_idx} op={op_idx}")

    print("PATCH_VALIDATION:")
    print("  status: PASS")
    print("  scope: patch")
    print(f"  patch_id: {ps.get('id')}")
    print(f"  supported_ops_checked: {sorted(set(seen_ops))}")
    print("  anomalies: []")
    print("  warnings: []")
    print("  corrections: []")


if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        print("PATCH_VALIDATION:")
        print("  status: FAIL")
        print("  scope: patch")
        print("  patch_id: unknown")
        print("  supported_ops_checked: []")
        print("  anomalies:")
        print(f"    - severity: critique")
        print(f"      type: patch_schema")
        print(f"      op_index: null")
        print(f"      file: null")
        print(f"      description: \"{str(e).replace(chr(34), chr(39))}\"")
        print("  warnings: []")
        print("  corrections: []")
        sys.exit(1)
