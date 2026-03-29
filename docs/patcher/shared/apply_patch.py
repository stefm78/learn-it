#!/usr/bin/env python3
from __future__ import annotations

import copy
import os
import re
import sys
from typing import Any, Dict, List, Tuple

import yaml

SECTIONS = [
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "DEPENDENCIES",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
]

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

ALLOWED_CORE_REF_PREFIXES = ("REF_CORE_", "LINK_REF_CORE_")
EXTERNAL_REF_SEPARATOR = "::"


class PatchError(Exception):
    pass


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)


def detect_root(doc: Any) -> Dict[str, Any]:
    if isinstance(doc, dict) and "CORE" in doc and isinstance(doc["CORE"], dict):
        return doc["CORE"]
    if isinstance(doc, dict):
        return doc
    raise PatchError("Document YAML invalide")


def get_core_id(doc: Any) -> str | None:
    if isinstance(doc, dict):
        if isinstance(doc.get("id"), str):
            return doc["id"]
        if isinstance(doc.get("CORE"), dict):
            core = doc["CORE"]
            if isinstance(core.get("id"), str):
                return core["id"]
    return None


def ensure_list_section(root: Dict[str, Any], section: str) -> List[Dict[str, Any]]:
    if section not in SECTIONS:
        raise PatchError(f"Section inconnue: {section}")
    if section not in root or root[section] is None:
        root[section] = []
    if not isinstance(root[section], list):
        raise PatchError(f"Section '{section}' n'est pas une liste")
    return root[section]


def find_item_by_id(items: List[Dict[str, Any]], item_id: str) -> Tuple[int | None, Dict[str, Any] | None]:
    for idx, item in enumerate(items):
        if isinstance(item, dict) and item.get("id") == item_id:
            return idx, item
    return None, None


def get_field(obj: Dict[str, Any], field_path: str) -> Any:
    cur: Any = obj
    for part in field_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise PatchError(f"Champ introuvable: {field_path}")
        cur = cur[part]
    return cur


def set_field(obj: Dict[str, Any], field_path: str, value: Any) -> None:
    parts = field_path.split(".")
    cur: Any = obj
    for part in parts[:-1]:
        if part not in cur or not isinstance(cur[part], dict):
            raise PatchError(f"Champ intermédiaire introuvable: {field_path}")
        cur = cur[part]
    cur[parts[-1]] = value


def collect_all_ids(root: Dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for section in SECTIONS:
        for item in ensure_list_section(root, section):
            item_id = item.get("id")
            if isinstance(item_id, str):
                ids.add(item_id)
    return ids


def iter_all_objects(root: Dict[str, Any]):
    for section in SECTIONS:
        for item in ensure_list_section(root, section):
            yield section, item


def assert_unique_ids(root: Dict[str, Any]) -> None:
    seen: set[str] = set()
    for _, item in iter_all_objects(root):
        item_id = item.get("id")
        if not isinstance(item_id, str):
            raise PatchError("Objet sans id détecté")
        if item_id in seen:
            raise PatchError(f"Collision d'id: {item_id}")
        seen.add(item_id)


def validate_core_type_consistency(root: Dict[str, Any], expected: str | None) -> None:
    if expected is None:
        return
    for _, item in iter_all_objects(root):
        core_type = item.get("core_type")
        if core_type != expected:
            raise PatchError(f"core_type incohérent: attendu={expected} trouvé={core_type} pour id={item.get('id')}")


def parse_external_ref(value: str) -> Tuple[str, str] | None:
    if EXTERNAL_REF_SEPARATOR not in value:
        return None
    core_ref, item_id = value.split(EXTERNAL_REF_SEPARATOR, 1)
    if not core_ref or not item_id:
        raise PatchError(f"Référence inter-Core invalide: {value}")
    if not core_ref.startswith(ALLOWED_CORE_REF_PREFIXES):
        raise PatchError(f"Alias de Core invalide dans la référence inter-Core: {value}")
    return core_ref, item_id


def validate_reference_string(
    ref_value: str,
    local_ids: set[str],
    source_id: str,
    external_ids_by_core_ref: Dict[str, set[str]],
    *,
    context: str,
) -> None:
    if ref_value in local_ids or ref_value.startswith(ALLOWED_CORE_REF_PREFIXES):
        return

    parsed = parse_external_ref(ref_value)
    if parsed is None:
        raise PatchError(f"{context} orpheline: {source_id} -> {ref_value}")

    core_ref, item_id = parsed
    if core_ref not in external_ids_by_core_ref:
        raise PatchError(f"Alias de Core non résolu: {source_id} -> {core_ref}")
    if item_id not in external_ids_by_core_ref[core_ref]:
        raise PatchError(f"{context} inter-Core orpheline: {source_id} -> {ref_value}")


def validate_rel_target(
    source_id: str,
    target: Dict[str, Any],
    local_ids: set[str],
    external_ids_by_core_ref: Dict[str, set[str]],
) -> None:
    target_id = target.get("id")
    if not isinstance(target_id, str):
        return

    core_ref = target.get("core_ref")
    if core_ref is not None:
        if not isinstance(core_ref, str):
            raise PatchError(f"Relation inter-Core invalide: {source_id} -> core_ref non chaîne")
        if not core_ref.startswith(ALLOWED_CORE_REF_PREFIXES):
            raise PatchError(f"Relation inter-Core invalide: alias non autorisé pour {source_id} -> {core_ref}")
        if core_ref not in external_ids_by_core_ref:
            raise PatchError(f"Alias de Core non résolu: {source_id} -> {core_ref}")
        if target_id not in external_ids_by_core_ref[core_ref]:
            raise PatchError(f"Relation inter-Core orpheline: {source_id} -> {core_ref}{EXTERNAL_REF_SEPARATOR}{target_id}")
        return

    validate_reference_string(
        target_id,
        local_ids,
        source_id,
        external_ids_by_core_ref,
        context="Relation",
    )


def validate_references(root: Dict[str, Any], external_ids_by_core_ref: Dict[str, set[str]] | None = None) -> None:
    local_ids = collect_all_ids(root)
    external_ids_by_core_ref = external_ids_by_core_ref or {}

    for _, item in iter_all_objects(root):
        source_id = item.get("id", "<unknown>")

        deps = item.get("depends_on", [])
        if isinstance(deps, list):
            for dep in deps:
                if isinstance(dep, str):
                    validate_reference_string(
                        dep,
                        local_ids,
                        source_id,
                        external_ids_by_core_ref,
                        context="Dépendance",
                    )

        rels = item.get("relations", [])
        if isinstance(rels, list):
            for rel in rels:
                if not isinstance(rel, dict):
                    continue
                tgt = rel.get("target", {})
                if isinstance(tgt, dict):
                    validate_rel_target(source_id, tgt, local_ids, external_ids_by_core_ref)


def append_if_missing(items: List[Dict[str, Any]], new_item: Dict[str, Any]) -> str:
    item_id = new_item.get("id")
    if not isinstance(item_id, str):
        raise PatchError("append exige un objet avec id")
    idx, _ = find_item_by_id(items, item_id)
    if idx is not None:
        return f"skip-existing {item_id}"
    items.append(new_item)
    return f"append {item_id}"


def remove_item(root: Dict[str, Any], section: str, item_id: str) -> str:
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is None:
        raise PatchError(f"remove impossible: {section}/{item_id} introuvable")
    candidate_root = copy.deepcopy(root)
    candidate_items = ensure_list_section(candidate_root, section)
    del candidate_items[idx]
    validate_references(candidate_root)
    del items[idx]
    return f"remove {section}/{item_id}"


def rewrite_id_references(root: Dict[str, Any], old_id: str, new_id: str) -> int:
    rewritten = 0
    for _, item in iter_all_objects(root):
        deps = item.get("depends_on")
        if isinstance(deps, list):
            for i, dep in enumerate(deps):
                if dep == old_id:
                    deps[i] = new_id
                    rewritten += 1
        rels = item.get("relations")
        if isinstance(rels, list):
            for rel in rels:
                if isinstance(rel, dict):
                    tgt = rel.get("target")
                    if isinstance(tgt, dict) and tgt.get("id") == old_id and tgt.get("core_ref") is None:
                        tgt["id"] = new_id
                        rewritten += 1
    return rewritten


def replace_text_literal(value: str, old: str, new: str) -> Tuple[str, int]:
    count = value.count(old)
    return value.replace(old, new), count


def replace_text_regex(value: str, pattern: str, replacement: str) -> Tuple[str, int]:
    compiled = re.compile(pattern)
    new_value, count = compiled.subn(replacement, value)
    return new_value, count


def walk_strings(obj: Any):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                yield obj, k, v
            else:
                yield from walk_strings(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                yield obj, i, v
            else:
                yield from walk_strings(v)


def normalize_federation(patch_set: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    federation = patch_set.get("federation", {})
    if federation is None:
        return {}
    if not isinstance(federation, dict):
        raise PatchError("federation doit être un objet")
    normalized: Dict[str, Dict[str, str]] = {}
    for core_ref, entry in federation.items():
        if not isinstance(core_ref, str) or not core_ref.startswith(ALLOWED_CORE_REF_PREFIXES):
            raise PatchError(f"Alias de federation invalide: {core_ref}")
        if not isinstance(entry, dict):
            raise PatchError(f"Entrée federation invalide pour {core_ref}")
        file_path = entry.get("file")
        expected_core_id = entry.get("expected_core_id")
        if not isinstance(file_path, str) or not file_path:
            raise PatchError(f"federation[{core_ref}].file manquant ou invalide")
        if not isinstance(expected_core_id, str) or not expected_core_id:
            raise PatchError(f"federation[{core_ref}].expected_core_id manquant ou invalide")
        normalized[core_ref] = {
            "file": file_path,
            "expected_core_id": expected_core_id,
        }
    return normalized


def build_external_ids_by_core_ref(
    federation: Dict[str, Dict[str, str]],
    root_path: str,
    prepared_docs_by_relpath: Dict[str, Any],
) -> Dict[str, set[str]]:
    external_ids: Dict[str, set[str]] = {}

    for core_ref, entry in federation.items():
        rel_path = entry["file"]
        expected_core_id = entry["expected_core_id"]

        if rel_path in prepared_docs_by_relpath:
            doc = prepared_docs_by_relpath[rel_path]
        else:
            full_path = os.path.join(root_path, rel_path)
            if not os.path.exists(full_path):
                raise PatchError(f"Fichier federation introuvable: {full_path}")
            doc = load_yaml(full_path)

        root = detect_root(doc)
        actual_core_id = get_core_id(doc) or get_core_id(root)
        if actual_core_id != expected_core_id:
            raise PatchError(
                f"Core ID inattendu dans federation pour {core_ref}: attendu={expected_core_id} trouvé={actual_core_id}"
            )

        external_ids[core_ref] = collect_all_ids(root)

    return external_ids


def apply_operation(root: Dict[str, Any], op: Dict[str, Any], file_report: Dict[str, Any]) -> None:
    op_type = op["op"]
    if op_type not in SUPPORTED_OPS:
        raise PatchError(f"Opération non supportée: {op_type}")

    if op_type == "assert":
        tgt = op["target"]
        section = tgt["section"]
        item_id = tgt["id"]
        items = ensure_list_section(root, section)
        idx, _ = find_item_by_id(items, item_id)
        if idx is None:
            raise PatchError(f"assert échoué: {section}/{item_id} introuvable")
        file_report["operations"].append(f"assert {section}/{item_id}")

    elif op_type == "append":
        section = op["target"]["section"]
        items = ensure_list_section(root, section)
        values = op.get("values") if "values" in op else [op.get("value")]
        for value in values:
            file_report["operations"].append(append_if_missing(items, value))

    elif op_type == "replace":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        items = ensure_list_section(root, section)
        idx, _ = find_item_by_id(items, item_id)
        if idx is None:
            raise PatchError(f"replace impossible: {section}/{item_id} introuvable")
        items[idx] = op["value"]
        file_report["operations"].append(f"replace {section}/{item_id}")

    elif op_type == "replace_field":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        field = op["target"]["field"]
        items = ensure_list_section(root, section)
        _, item = find_item_by_id(items, item_id)
        if item is None:
            raise PatchError(f"replace_field impossible: {section}/{item_id} introuvable")
        set_field(item, field, op["value"])
        file_report["operations"].append(f"replace_field {section}/{item_id}.{field}")

    elif op_type == "remove":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        file_report["operations"].append(remove_item(root, section, item_id))

    elif op_type == "rename":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        new_id = op["new_id"]
        items = ensure_list_section(root, section)
        _, item = find_item_by_id(items, item_id)
        if item is None:
            raise PatchError(f"rename impossible: {section}/{item_id} introuvable")
        _, other = find_item_by_id(items, new_id)
        if other is not None:
            raise PatchError(f"rename impossible: nouvel id déjà présent: {new_id}")
        item["id"] = new_id
        file_report["operations"].append(f"rename {section}/{item_id}->{new_id}")

    elif op_type == "append_field_list":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        field = op["target"]["field"]
        items = ensure_list_section(root, section)
        _, item = find_item_by_id(items, item_id)
        if item is None:
            raise PatchError(f"append_field_list impossible: {section}/{item_id} introuvable")
        current = get_field(item, field)
        if not isinstance(current, list):
            raise PatchError(f"Champ non liste: {field}")
        current.append(op["value"])
        file_report["operations"].append(f"append_field_list {section}/{item_id}.{field}")

    elif op_type == "remove_field_list_item":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        field = op["target"]["field"]
        items = ensure_list_section(root, section)
        _, item = find_item_by_id(items, item_id)
        if item is None:
            raise PatchError(f"remove_field_list_item impossible: {section}/{item_id} introuvable")
        current = get_field(item, field)
        if not isinstance(current, list):
            raise PatchError(f"Champ non liste: {field}")
        try:
            current.remove(op["value"])
        except ValueError as e:
            raise PatchError(f"Valeur absente dans liste: {op['value']}") from e
        file_report["operations"].append(f"remove_field_list_item {section}/{item_id}.{field}")

    elif op_type == "move":
        src_section = op["target"]["section"]
        item_id = op["target"]["id"]
        dst_section = op["destination"]["section"]
        src = ensure_list_section(root, src_section)
        dst = ensure_list_section(root, dst_section)
        idx, item = find_item_by_id(src, item_id)
        if item is None:
            raise PatchError(f"move impossible: {src_section}/{item_id} introuvable")
        _, existing = find_item_by_id(dst, item_id)
        if existing is not None:
            raise PatchError(f"move impossible: id déjà présent en destination: {item_id}")
        dst.append(item)
        del src[idx]
        file_report["operations"].append(f"move {src_section}/{item_id}->{dst_section}")

    elif op_type == "ensure_exists":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        items = ensure_list_section(root, section)
        idx, _ = find_item_by_id(items, item_id)
        if idx is None:
            items.append(op["value"])
            file_report["operations"].append(f"ensure_exists created {section}/{item_id}")
        else:
            file_report["operations"].append(f"ensure_exists already-present {section}/{item_id}")

    elif op_type == "ensure_absent":
        section = op["target"]["section"]
        item_id = op["target"]["id"]
        items = ensure_list_section(root, section)
        idx, _ = find_item_by_id(items, item_id)
        if idx is None:
            file_report["operations"].append(f"ensure_absent already-absent {section}/{item_id}")
        else:
            remove_item(root, section, item_id)
            file_report["operations"].append(f"ensure_absent removed {section}/{item_id}")

    elif op_type == "assert_meta":
        field = op["target"]["field"]
        expected = op.get("value")
        actual = get_field(root, field)
        if expected is not None and actual != expected:
            raise PatchError(f"assert_meta échoué: {field} attendu={expected} trouvé={actual}")
        file_report["operations"].append(f"assert_meta {field}")

    elif op_type == "replace_meta_field":
        field = op["target"]["field"]
        set_field(root, field, op["value"])
        file_report["operations"].append(f"replace_meta_field {field}")

    elif op_type == "rewrite_references":
        old_id = op["target"]["old_id"]
        new_id = op["target"]["new_id"]
        rewritten = rewrite_id_references(root, old_id, new_id)
        file_report["operations"].append(f"rewrite_references {old_id}->{new_id} ({rewritten})")

    elif op_type == "replace_text":
        tgt = op["target"]
        scope = tgt["scope"]
        regex_mode = bool(op.get("regex", False))
        replacements = 0

        def apply_text(value: str) -> Tuple[str, int]:
            if regex_mode:
                return replace_text_regex(value, op["pattern"], op["replacement"])
            return replace_text_literal(value, op["old"], op["new"])

        if scope == "meta_field":
            field = tgt["field"]
            current = get_field(root, field)
            if not isinstance(current, str):
                raise PatchError(f"replace_text meta_field exige une chaîne: {field}")
            new_value, count = apply_text(current)
            set_field(root, field, new_value)
            replacements += count
        elif scope == "object_field":
            section = tgt["section"]
            item_id = tgt["id"]
            field = tgt["field"]
            items = ensure_list_section(root, section)
            _, item = find_item_by_id(items, item_id)
            if item is None:
                raise PatchError(f"replace_text object_field: {section}/{item_id} introuvable")
            current = get_field(item, field)
            if not isinstance(current, str):
                raise PatchError(f"replace_text object_field exige une chaîne: {field}")
            new_value, count = apply_text(current)
            set_field(item, field, new_value)
            replacements += count
        elif scope == "section_fields":
            section = tgt["section"]
            fields = tgt["fields"]
            items = ensure_list_section(root, section)
            for item in items:
                for field in fields:
                    try:
                        current = get_field(item, field)
                    except PatchError:
                        continue
                    if isinstance(current, str):
                        new_value, count = apply_text(current)
                        if count:
                            set_field(item, field, new_value)
                            replacements += count
        elif scope == "all_strings":
            for parent, key, value in walk_strings(root):
                new_value, count = apply_text(value)
                if count:
                    parent[key] = new_value
                    replacements += count
        else:
            raise PatchError(f"replace_text scope inconnu: {scope}")

        file_report["operations"].append(f"replace_text {scope} ({replacements})")
        file_report["text_replacements"] += replacements

    elif op_type == "note":
        value = op.get("value", {})
        note_id = value.get("id") if isinstance(value, dict) else "no-id"
        file_report["operations"].append(f"note {note_id}")

    elif op_type == "no_change":
        file_report["operations"].append(f"no_change {op.get('reason', '')}")


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: apply_patch.py <patchfile> <rootpath> <whatif:true|false> [report_path]")

    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"
    cli_report_path = sys.argv[4] if len(sys.argv) >= 5 else None

    patch_doc = load_yaml(patch_file)
    if not isinstance(patch_doc, dict) or "PATCH_SET" not in patch_doc:
        raise PatchError("PATCH_SET absent")

    patch_set = patch_doc["PATCH_SET"]
    if patch_set.get("patch_dsl_version") != "4.0":
        raise PatchError("Ce moteur exige patch_dsl_version=4.0")

    federation = normalize_federation(patch_set)

    report_cfg = patch_set.get("report", {}) if isinstance(patch_set.get("report"), dict) else {}
    report_enabled = bool(report_cfg.get("enabled") or cli_report_path)
    report_path = cli_report_path or report_cfg.get("path")

    report: Dict[str, Any] = {
        "PATCH_EXECUTION_REPORT": {
            "patch_id": patch_set.get("id"),
            "patch_dsl_version": patch_set.get("patch_dsl_version"),
            "atomic": patch_set.get("atomic", True),
            "whatif": whatif,
            "status": "IN_PROGRESS",
            "files": [],
            "errors": [],
            "federation": federation,
        }
    }

    prepared: List[Tuple[str, str, Any, Any, Dict[str, Any], str | None]] = []
    prepared_docs_by_relpath: Dict[str, Any] = {}
    files = patch_set.get("files", [])

    try:
        for file_entry in files:
            rel_path = file_entry["file"]
            full_path = os.path.join(root_path, rel_path)
            if not os.path.exists(full_path):
                raise PatchError(f"Fichier introuvable: {full_path}")

            original = load_yaml(full_path)
            doc = copy.deepcopy(original)
            root = detect_root(doc)
            actual_core_id = get_core_id(doc) or get_core_id(root)
            expected_core_id = file_entry.get("expected_core_id")
            if expected_core_id and actual_core_id != expected_core_id:
                raise PatchError(f"Core ID inattendu pour {rel_path}: attendu={expected_core_id} trouvé={actual_core_id}")

            file_report = {
                "file": rel_path,
                "expected_core_id": expected_core_id,
                "actual_core_id": actual_core_id,
                "operations": [],
                "text_replacements": 0,
            }

            for op in file_entry.get("operations", []):
                apply_operation(root, op, file_report)

            expected_core_type = root.get("core_type") if isinstance(root.get("core_type"), str) else None
            assert_unique_ids(root)
            validate_core_type_consistency(root, expected_core_type)

            prepared.append((rel_path, full_path, original, doc, file_report, expected_core_type))
            prepared_docs_by_relpath[rel_path] = doc
            report["PATCH_EXECUTION_REPORT"]["files"].append(file_report)

        external_ids_by_core_ref = build_external_ids_by_core_ref(federation, root_path, prepared_docs_by_relpath)

        for rel_path, _, _, doc, _, _ in prepared:
            root = detect_root(doc)
            validate_references(root, external_ids_by_core_ref)

        report["PATCH_EXECUTION_REPORT"]["status"] = "PASS"

        if whatif:
            print(f"[WHATIF] PatchSet {patch_set.get('id')} prêt à être appliqué.")
        else:
            for _, full_path, original, doc, _, _ in prepared:
                bak_path = full_path + ".bak"
                if not os.path.exists(bak_path):
                    dump_yaml(bak_path, original)
                dump_yaml(full_path, doc)
            print(f"[OK] PatchSet {patch_set.get('id')} appliqué.")

    except Exception as exc:
        report["PATCH_EXECUTION_REPORT"]["status"] = "FAIL"
        report["PATCH_EXECUTION_REPORT"]["errors"].append(str(exc))
        if report_enabled and report_path:
            dump_yaml(report_path, report)
        raise

    if report_enabled and report_path:
        dump_yaml(report_path, report)


if __name__ == "__main__":
    main()
