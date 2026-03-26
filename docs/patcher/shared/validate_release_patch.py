#!/usr/bin/env python3
import sys
from typing import Any, Dict, List

import yaml

SUPPORTED_OPS = {
    "assert_file_exists",
    "assert_file_contains",
    "promote_file",
    "sync_copy",
    "replace_text",
    "note",
    "no_change",
}


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: validate_release_patch.py <release_patch.yaml>")

    doc = load_yaml(sys.argv[1])
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(doc, dict) or "RELEASE_PATCH_SET" not in doc:
        raise SystemExit("RELEASE_PATCH_SET absent")

    patch = doc["RELEASE_PATCH_SET"]
    if patch.get("version") != "1.0":
        errors.append("version doit être '1.0'")
    if "atomic" not in patch:
        errors.append("atomic manquant")

    ops = patch.get("operations")
    if not isinstance(ops, list) or not ops:
        errors.append("operations manquant ou vide")
        ops = []

    saw_promote = False
    for idx, op in enumerate(ops):
        if not isinstance(op, dict) or "op" not in op:
            errors.append(f"operation[{idx}] invalide")
            continue
        op_type = op["op"]
        if op_type not in SUPPORTED_OPS:
            errors.append(f"operation non supportee: {op_type}")
            continue
        if op_type in {"promote_file", "sync_copy"}:
            saw_promote = True
            if "from" not in op or "to" not in op:
                errors.append(f"{op_type} incomplet en operation[{idx}]")
        elif op_type == "assert_file_exists":
            if "path" not in op:
                errors.append(f"assert_file_exists sans path en operation[{idx}]")
        elif op_type == "assert_file_contains":
            if "path" not in op or "text" not in op:
                errors.append(f"assert_file_contains incomplet en operation[{idx}]")
        elif op_type == "replace_text":
            if "file" not in op or "old" not in op or "new" not in op:
                errors.append(f"replace_text incomplet en operation[{idx}]")

    if not saw_promote:
        warnings.append("aucune operation de promotion ou synchronisation detectee")

    print("RELEASE_PATCH_VALIDATION:")
    print(f"  status: {'FAIL' if errors else 'PASS'}")
    print("  scope: release_patch")
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
