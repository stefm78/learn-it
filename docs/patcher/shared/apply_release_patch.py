#!/usr/bin/env python3
from __future__ import annotations

import copy
import os
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


class ReleasePatchError(Exception):
    pass


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: apply_release_patch.py <patchfile> <rootpath> <whatif:true|false> [report_path]")

    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"
    report_path = sys.argv[4] if len(sys.argv) >= 5 else None

    patch_doc = load_yaml(patch_file)
    if not isinstance(patch_doc, dict) or "RELEASE_PATCH_SET" not in patch_doc:
        raise ReleasePatchError("RELEASE_PATCH_SET absent")

    patch = patch_doc["RELEASE_PATCH_SET"]
    if patch.get("version") != "1.0":
        raise ReleasePatchError("Ce moteur exige version=1.0")

    operations = patch.get("operations", [])
    report: Dict[str, Any] = {
        "RELEASE_PATCH_EXECUTION_REPORT": {
            "patch_id": patch.get("id"),
            "version": patch.get("version"),
            "atomic": patch.get("atomic", True),
            "whatif": whatif,
            "status": "IN_PROGRESS",
            "operations": [],
            "errors": [],
        }
    }

    text_writes: Dict[str, str] = {}

    try:
        for op in operations:
            op_type = op["op"]
            if op_type not in SUPPORTED_OPS:
                raise ReleasePatchError(f"Operation non supportee: {op_type}")

            if op_type == "assert_file_exists":
                path = os.path.join(root_path, op["path"])
                if not os.path.exists(path):
                    raise ReleasePatchError(f"Fichier absent: {path}")
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"assert_file_exists {op['path']}")

            elif op_type == "assert_file_contains":
                path = os.path.join(root_path, op["path"])
                if not os.path.exists(path):
                    raise ReleasePatchError(f"Fichier absent: {path}")
                content = read_text(path)
                if op["text"] not in content:
                    raise ReleasePatchError(f"Texte attendu absent dans {op['path']}")
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"assert_file_contains {op['path']}")

            elif op_type in {"promote_file", "sync_copy"}:
                src = os.path.join(root_path, op["from"])
                dst = os.path.join(root_path, op["to"])
                if not os.path.exists(src):
                    raise ReleasePatchError(f"Source absente: {src}")
                content = read_text(src)
                if not content.strip():
                    raise ReleasePatchError(f"Source vide: {src}")
                text_writes[dst] = content
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"{op_type} {op['from']} -> {op['to']}")

            elif op_type == "replace_text":
                rel = op["file"]
                path = os.path.join(root_path, rel)
                base_content = text_writes[path] if path in text_writes else read_text(path)
                if op["old"] not in base_content:
                    if op.get("strict", True):
                        raise ReleasePatchError(f"replace_text: fragment absent dans {rel}")
                    report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"replace_text no-op {rel}")
                    continue
                new_content = base_content.replace(op["old"], op["new"])
                text_writes[path] = new_content
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"replace_text {rel}")

            elif op_type == "note":
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"note {op.get('id', 'no-id')}")

            elif op_type == "no_change":
                report["RELEASE_PATCH_EXECUTION_REPORT"]["operations"].append(f"no_change {op.get('reason', '')}")

        report["RELEASE_PATCH_EXECUTION_REPORT"]["status"] = "PASS"

        if not whatif:
            for path, content in text_writes.items():
                ensure_parent(path)
                if os.path.exists(path):
                    bak = path + ".bak"
                    if not os.path.exists(bak):
                        write_text(bak, read_text(path))
                write_text(path, content)
            print(f"[OK] RELEASE_PATCH_SET {patch.get('id')} applique.")
        else:
            print(f"[WHATIF] RELEASE_PATCH_SET {patch.get('id')} pret a etre applique.")

    except Exception as exc:
        report["RELEASE_PATCH_EXECUTION_REPORT"]["status"] = "FAIL"
        report["RELEASE_PATCH_EXECUTION_REPORT"]["errors"].append(str(exc))
        if report_path:
            dump_yaml(report_path, report)
        raise

    if report_path:
        dump_yaml(report_path, report)


if __name__ == "__main__":
    main()
