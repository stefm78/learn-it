#!/usr/bin/env python3
"""Minimal canonical patchset validator for Learn-it.

This validator is intentionally lightweight. It checks the outer shape of a patchset
before a richer validator is promoted to the canonical shared location.
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

REQUIRED_TOP = {"id", "patch_dsl_version", "atomic", "description", "files"}
ALLOWED_OPS = {
    "assert", "append", "replace", "replace_field", "remove", "rename",
    "append_field_list", "remove_field_list_item", "move", "ensure_exists",
    "ensure_absent", "assert_meta", "replace_meta_field", "rewrite_references",
    "replace_text", "note", "no_change"
}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_patchset.py <patchset.yaml>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL: file not found: {path}")
        return 1

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "PATCH_SET" not in data:
        print("FAIL: PATCH_SET missing")
        return 1

    patch = data["PATCH_SET"]
    missing = [k for k in REQUIRED_TOP if k not in patch]
    if missing:
        print(f"FAIL: missing top-level keys: {missing}")
        return 1

    if not isinstance(patch["files"], list):
        print("FAIL: PATCH_SET.files must be a list")
        return 1

    for idx, file_entry in enumerate(patch["files"]):
        if not isinstance(file_entry, dict):
            print(f"FAIL: file entry #{idx} is not a mapping")
            return 1
        for k in ("file", "expected_core_id", "operations"):
            if k not in file_entry:
                print(f"FAIL: file entry #{idx} missing key: {k}")
                return 1
        if not isinstance(file_entry["operations"], list):
            print(f"FAIL: operations in file entry #{idx} must be a list")
            return 1
        for jdx, op in enumerate(file_entry["operations"]):
            if not isinstance(op, dict) or "op" not in op:
                print(f"FAIL: operation #{jdx} in file entry #{idx} is invalid")
                return 1
            if op["op"] not in ALLOWED_OPS:
                print(f"FAIL: unsupported operation '{op['op']}' in file entry #{idx}")
                return 1

    print("PASS: patchset outer structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
