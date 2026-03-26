#!/usr/bin/env python3
import copy
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import yaml

ALLOWED_SECTIONS = {
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "DEPENDENCIES",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
}

CORE_TYPE_BY_FILENAME = {
    "constitution": "CONSTITUTION",
    "referentiel": "REFERENTIEL",
    "link": "LINK",
}

REQUIRED_CORE_FIELDS = {
    "id",
    "authority",
    "core_type",
    "source_anchor",
    "depends_on",
    "relations",
    "patchable",
    "parameterizable",
    "human_readable",
    "logic",
}

EXTERNAL_REF_PREFIXES = (
    "REF_",
    "LINK_REF_",
    "CORE_",
)

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


class PatchError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)


def detect_root(doc: Any) -> Any:
    if isinstance(doc, dict) and "CORE" in doc and isinstance(doc["CORE"], dict):
        return doc["CORE"]
    return doc


def get_core_id(doc: Any) -> Optional[str]:
    root = detect_root(doc)
    if isinstance(root, dict) and isinstance(root.get("id"), str):
        return root["id"]
    return None


def infer_file_core_type(file_path: str) -> Optional[str]:
    lower = file_path.lower()
    for key, core_type in CORE_TYPE_BY_FILENAME.items():
        if key in lower:
            return core_type
    return None


def ensure_list_section(root: Dict[str, Any], section_name: str) -> List[Dict[str, Any]]:
    if section_name not in ALLOWED_SECTIONS:
        raise PatchError(f"Section non supportée: {section_name}")
    if section_name not in root or root[section_name] is None:
        root[section_name] = []
    if not isinstance(root[section_name], list):
        raise PatchError(f"Section '{section_name}' n'est pas une liste")
    return root[section_name]


def find_item_by_id(items: List[Dict[str, Any]], item_id: str) -> Tuple[Optional[int], Optional[Dict[str, Any]]]:
    for idx, item in enumerate(items):
        if isinstance(item, dict) and item.get("id") == item_id:
            return idx, item
    return None, None


def split_field_path(path: str) -> List[str]:
    return [p for p in path.split(".") if p]


def get_nested_value(obj: Dict[str, Any], field_path: str) -> Any:
    cur: Any = obj
    for part in split_field_path(field_path):
        if not isinstance(cur, dict) or part not in cur:
            raise PatchError(f"Champ introuvable: {field_path}")
        cur = cur[part]
    return cur


def set_nested_value(obj: Dict[str, Any], field_path: str, value: Any, create_missing: bool = False) -> None:
    parts = split_field_path(field_path)
    if not parts:
        raise PatchError("field vide")
    cur: Any = obj
    for part in parts[:-1]:
        if not isinstance(cur, dict):
            raise PatchError(f"Chemin invalide pour champ '{field_path}'")
        if part not in cur:
            if create_missing:
                cur[part] = {}
            else:
                raise PatchError(f"Champ intermédiaire introuvable: {field_path}")
        if not isinstance(cur[part], dict):
            raise PatchError(f"Champ intermédiaire non-dict: {field_path}")
        cur = cur[part]
    if not isinstance(cur, dict):
        raise PatchError(f"Chemin invalide pour champ '{field_path}'")
    cur[parts[-1]] = value


def collect_ids(root: Dict[str, Any]) -> Dict[str, Tuple[str, Dict[str, Any]]]:
    index: Dict[str, Tuple[str, Dict[str, Any]]] = {}
    for section in ALLOWED_SECTIONS:
        items = root.get(section) or []
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not item_id:
                continue
            if item_id in index:
                raise PatchError(f"ID dupliqué détecté: {item_id}")
            index[item_id] = (section, item)
    return index


def extract_references(root: Dict[str, Any]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    id_index = collect_ids(root)
    for source_id, (_, item) in id_index.items():
        local_refs: List[str] = []
        depends_on = item.get("depends_on", [])
        if isinstance(depends_on, list):
            for dep in depends_on:
                if isinstance(dep, str):
                    local_refs.append(dep)
        relations = item.get("relations", [])
        if isinstance(relations, list):
            for rel in relations:
                if isinstance(rel, dict):
                    target = rel.get("target")
                    if isinstance(target, dict):
                        target_id = target.get("id")
                        if isinstance(target_id, str):
                            local_refs.append(target_id)
        refs[source_id] = local_refs
    return refs


def is_external_reference(ref_id: str) -> bool:
    return ref_id.startswith(EXTERNAL_REF_PREFIXES)


def validate_local_references(root: Dict[str, Any]) -> None:
    id_index = collect_ids(root)
    refs = extract_references(root)
    for source_id, targets in refs.items():
        for target_id in targets:
            if target_id in id_index:
                continue
            if is_external_reference(target_id):
                continue
            raise PatchError(f"Référence non résolue: {source_id} -> {target_id}")


def validate_core_type_consistency(root: Dict[str, Any], file_path: str) -> None:
    expected = infer_file_core_type(file_path)
    if not expected:
        return
    for section in ALLOWED_SECTIONS:
        for item in root.get(section, []) or []:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            core_type = item.get("core_type")
            if item_id and core_type and core_type != expected:
                raise PatchError(
                    f"core_type incohérent dans {file_path}: {item_id} a {core_type}, attendu {expected}"
                )


def validate_new_object_shape(item: Dict[str, Any], section: str) -> None:
    if section not in ALLOWED_SECTIONS:
        raise PatchError(f"Section non supportée: {section}")
    missing = sorted(REQUIRED_CORE_FIELDS - set(item.keys()))
    if missing:
        raise PatchError(f"Objet incomplet pour {item.get('id', '<sans id>')}: champs manquants {missing}")


def get_object(root: Dict[str, Any], section: str, item_id: str) -> Tuple[List[Dict[str, Any]], int, Dict[str, Any]]:
    items = ensure_list_section(root, section)
    idx, item = find_item_by_id(items, item_id)
    if idx is None or item is None:
        raise PatchError(f"ID introuvable dans {section}: {item_id}")
    return items, idx, item


def get_list_field(item: Dict[str, Any], field: str, create_missing: bool = False) -> List[Any]:
    try:
        value = get_nested_value(item, field)
    except PatchError:
        if create_missing:
            set_nested_value(item, field, [], create_missing=True)
            value = get_nested_value(item, field)
        else:
            raise
    if not isinstance(value, list):
        raise PatchError(f"Le champ '{field}' n'est pas une liste")
    return value


def validate_root_metadata(root: Dict[str, Any]) -> None:
    if not isinstance(root.get("id"), str) or not root.get("id"):
        raise PatchError("Métadonnée racine invalide: id manquant")
    if not isinstance(root.get("core_type"), str) or not root.get("core_type"):
        raise PatchError("Métadonnée racine invalide: core_type manquant")


def apply_text_replace(text: str, op: Dict[str, Any], remaining: Optional[int]) -> Tuple[str, int]:
    regex_mode = bool(op.get("regex", False))
    if regex_mode:
        pattern = op.get("pattern")
        replacement = op.get("replacement")
        if pattern is None or replacement is None:
            raise PatchError("replace_text regex exige pattern et replacement")
        count = 0 if remaining is None else remaining
        new_text, replaced = re.subn(pattern, replacement, text, count=count)
        return new_text, replaced
    old = op.get("old")
    new = op.get("new")
    if old is None or new is None:
        raise PatchError("replace_text littéral exige old et new")
    if remaining is None:
        replaced = text.count(old)
        return text.replace(old, new), replaced
    replaced = min(text.count(old), remaining)
    return text.replace(old, new, remaining), replaced


def iter_string_leaves(obj: Any, prefix: str = ""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            yield from iter_string_leaves(value, new_prefix)
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            new_prefix = f"{prefix}[{idx}]"
            yield from iter_string_leaves(value, new_prefix)
    elif isinstance(obj, str):
        yield prefix, obj


def replace_string_at_path(root: Dict[str, Any], path: str, op: Dict[str, Any], remaining: Optional[int]) -> int:
    value = get_nested_value(root, path)
    if not isinstance(value, str):
        raise PatchError(f"Le champ texte '{path}' n'est pas une chaîne")
    new_value, replaced = apply_text_replace(value, op, remaining)
    if replaced:
        set_nested_value(root, path, new_value)
    return replaced


def apply_assert(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    _, _, item = get_object(root, section, item_id)
    field = op["target"].get("field")
    if field:
        _ = get_nested_value(item, field)
    return f"assert {section}/{item_id}"


def apply_append(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    value = op["value"]
    validate_new_object_shape(value, section)
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, value.get("id"))
    if idx is not None:
        raise PatchError(f"append impossible: id déjà existant dans {section}: {value['id']}")
    items.append(value)
    return f"append {section}/{value['id']}"


def apply_replace(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    value = op["value"]
    validate_new_object_shape(value, section)
    items, idx, _ = get_object(root, section, item_id)
    items[idx] = value
    return f"replace {section}/{item_id}"


def apply_replace_field(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    field = op["target"]["field"]
    create_missing = bool(op.get("create_missing", False))
    _, _, item = get_object(root, section, item_id)
    set_nested_value(item, field, op["value"], create_missing=create_missing)
    return f"replace_field {section}/{item_id}.{field}"


def apply_remove(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    refs = extract_references(root)
    inbound = [src for src, targets in refs.items() if item_id in targets]
    if inbound:
        raise PatchError(f"remove impossible: {item_id} encore référencé par {inbound}")
    items, idx, _ = get_object(root, section, item_id)
    del items[idx]
    return f"remove {section}/{item_id}"


def apply_rename(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    new_id = op["new_id"]
    items = ensure_list_section(root, section)
    existing_idx, _ = find_item_by_id(items, new_id)
    if existing_idx is not None:
        raise PatchError(f"rename impossible: nouvel id déjà existant dans {section}: {new_id}")
    _, _, item = get_object(root, section, item_id)
    item["id"] = new_id
    return f"rename {section}/{item_id} -> {new_id}"


def apply_append_field_list(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    field = op["target"]["field"]
    create_missing = bool(op.get("create_missing", False))
    unique = bool(op.get("unique", True))
    _, _, item = get_object(root, section, item_id)
    values = get_list_field(item, field, create_missing=create_missing)
    if unique and op["value"] in values:
        return f"append_field_list skipped-existing {section}/{item_id}.{field}"
    values.append(op["value"])
    return f"append_field_list {section}/{item_id}.{field}"


def apply_remove_field_list_item(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    field = op["target"]["field"]
    all_matches = bool(op.get("all_matches", False))
    _, _, item = get_object(root, section, item_id)
    values = get_list_field(item, field, create_missing=False)
    removed = 0
    while op["value"] in values:
        values.remove(op["value"])
        removed += 1
        if not all_matches:
            break
    if removed == 0:
        raise PatchError(f"Valeur non trouvée dans {section}/{item_id}.{field}: {op['value']}")
    return f"remove_field_list_item {section}/{item_id}.{field} ({removed})"


def apply_move(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    src_section = op["target"]["section"]
    item_id = op["target"]["id"]
    dst_section = op["destination"]["section"]
    src_items, idx, item = get_object(root, src_section, item_id)
    dst_items = ensure_list_section(root, dst_section)
    existing_idx, _ = find_item_by_id(dst_items, item_id)
    if existing_idx is not None:
        raise PatchError(f"move impossible: id déjà existant dans {dst_section}: {item_id}")
    src_items.pop(idx)
    dst_items.append(item)
    return f"move {src_section}/{item_id} -> {dst_section}"


def apply_ensure_exists(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is not None:
        return f"ensure_exists already-present {section}/{item_id}"
    value = op["value"]
    validate_new_object_shape(value, section)
    items.append(value)
    return f"ensure_exists created {section}/{item_id}"


def apply_ensure_absent(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is None:
        return f"ensure_absent already-absent {section}/{item_id}"
    if not bool(op.get("remove_if_present", False)):
        raise PatchError(f"ensure_absent échoué: {section}/{item_id} encore présent")
    return apply_remove(root, {"target": {"section": section, "id": item_id}})


def apply_assert_meta(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    field = op["target"]["field"]
    value = get_nested_value(root, field)
    if "equals" in op and value != op["equals"]:
        raise PatchError(f"assert_meta échoué pour {field}: attendu {op['equals']}, trouvé {value}")
    return f"assert_meta {field}"


def apply_replace_meta_field(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    field = op["target"]["field"]
    create_missing = bool(op.get("create_missing", False))
    set_nested_value(root, field, op["value"], create_missing=create_missing)
    return f"replace_meta_field {field}"


def apply_rewrite_references(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    old_id = op["target"]["old_id"]
    new_id = op["target"]["new_id"]
    rewrite_depends_on = bool(op.get("rewrite_depends_on", True))
    rewrite_relations = bool(op.get("rewrite_relations", True))
    rewrite_text_fields = op.get("rewrite_text_fields", []) or []
    rewritten = 0

    for section in ALLOWED_SECTIONS:
        items = root.get(section, []) or []
        for item in items:
            if not isinstance(item, dict):
                continue
            if rewrite_depends_on:
                deps = item.get("depends_on", [])
                if isinstance(deps, list):
                    for i, dep in enumerate(list(deps)):
                        if dep == old_id:
                            deps[i] = new_id
                            rewritten += 1
            if rewrite_relations:
                rels = item.get("relations", [])
                if isinstance(rels, list):
                    for rel in rels:
                        if not isinstance(rel, dict):
                            continue
                        target = rel.get("target")
                        if isinstance(target, dict) and target.get("id") == old_id:
                            target["id"] = new_id
                            rewritten += 1

    for field_path in rewrite_text_fields:
        rewritten += replace_string_at_path(root, field_path, {"old": old_id, "new": new_id}, None)

    return f"rewrite_references {old_id} -> {new_id} ({rewritten})"


def apply_replace_text(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op.get("target", {})
    scope = target.get("scope")
    require_match = bool(op.get("require_match", False))
    max_replacements = op.get("max_replacements")
    if max_replacements is not None:
        try:
            remaining: Optional[int] = int(max_replacements)
        except Exception as exc:
            raise PatchError(f"max_replacements invalide: {max_replacements}") from exc
        if remaining < 0:
            raise PatchError("max_replacements doit être >= 0")
    else:
        remaining = None
    total = 0

    def consume(path: str, current_remaining: Optional[int]) -> Optional[int]:
        nonlocal total
        replaced = replace_string_at_path(root, path, op, current_remaining)
        total += replaced
        if current_remaining is None:
            return None
        return max(current_remaining - replaced, 0)

    if scope == "meta_field":
        field = target.get("field")
        if not field:
            raise PatchError("replace_text meta_field exige target.field")
        remaining = consume(field, remaining)
    elif scope == "object_field":
        section = target.get("section")
        item_id = target.get("id")
        field = target.get("field")
        if not section or not item_id or not field:
            raise PatchError("replace_text object_field exige section, id et field")
        _, _, item = get_object(root, section, item_id)
        value = get_nested_value(item, field)
        if not isinstance(value, str):
            raise PatchError(f"Le champ texte '{field}' n'est pas une chaîne")
        new_value, replaced = apply_text_replace(value, op, remaining)
        if replaced:
            set_nested_value(item, field, new_value)
            total += replaced
            if remaining is not None:
                remaining = max(remaining - replaced, 0)
    elif scope == "section_fields":
        section = target.get("section")
        fields = target.get("fields") or []
        if not section or not isinstance(fields, list) or not fields:
            raise PatchError("replace_text section_fields exige section et fields non vide")
        items = ensure_list_section(root, section)
        for item in items:
            if remaining == 0:
                break
            if not isinstance(item, dict):
                continue
            for field in fields:
                if remaining == 0:
                    break
                try:
                    value = get_nested_value(item, field)
                except PatchError:
                    continue
                if not isinstance(value, str):
                    continue
                new_value, replaced = apply_text_replace(value, op, remaining)
                if replaced:
                    set_nested_value(item, field, new_value)
                    total += replaced
                    if remaining is not None:
                        remaining = max(remaining - replaced, 0)
    elif scope == "all_strings":
        include_meta = bool(target.get("include_meta", True))
        paths: List[str] = []
        if include_meta:
            for path, value in iter_string_leaves(root):
                if path and isinstance(value, str):
                    paths.append(path)
        else:
            for section in ALLOWED_SECTIONS:
                section_value = root.get(section)
                if section_value is None:
                    continue
                for path, value in iter_string_leaves(section_value, section):
                    if path and isinstance(value, str):
                        paths.append(path)
        for path in paths:
            if remaining == 0:
                break
            try:
                remaining = consume(path, remaining)
            except PatchError:
                continue
    else:
        raise PatchError(f"replace_text scope non supporté: {scope}")

    if require_match and total == 0:
        raise PatchError("replace_text n'a trouvé aucune occurrence")
    return f"replace_text {scope} ({total})"


def apply_operation(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    op_type = op["op"]
    if op_type not in SUPPORTED_OPS:
        raise PatchError(f"Opération non supportée: {op_type}")
    if op_type == "assert":
        return apply_assert(root, op)
    if op_type == "append":
        return apply_append(root, op)
    if op_type == "replace":
        return apply_replace(root, op)
    if op_type == "replace_field":
        return apply_replace_field(root, op)
    if op_type == "remove":
        return apply_remove(root, op)
    if op_type == "rename":
        return apply_rename(root, op)
    if op_type == "append_field_list":
        return apply_append_field_list(root, op)
    if op_type == "remove_field_list_item":
        return apply_remove_field_list_item(root, op)
    if op_type == "move":
        return apply_move(root, op)
    if op_type == "ensure_exists":
        return apply_ensure_exists(root, op)
    if op_type == "ensure_absent":
        return apply_ensure_absent(root, op)
    if op_type == "assert_meta":
        return apply_assert_meta(root, op)
    if op_type == "replace_meta_field":
        return apply_replace_meta_field(root, op)
    if op_type == "rewrite_references":
        return apply_rewrite_references(root, op)
    if op_type == "replace_text":
        return apply_replace_text(root, op)
    if op_type == "note":
        return f"note ({op.get('value', {}).get('reason', 'no reason')})"
    if op_type == "no_change":
        return f"no_change ({op.get('reason', 'no reason')})"
    raise PatchError(f"Opération non gérée: {op_type}")


def compute_report_path(patch_set: Dict[str, Any], cli_report_path: Optional[str], root_path: str) -> Optional[str]:
    if cli_report_path:
        return cli_report_path
    report_cfg = patch_set.get("report")
    if not isinstance(report_cfg, dict):
        return None
    if not report_cfg.get("enabled", False):
        return None
    path = report_cfg.get("path")
    if not path:
        return None
    if os.path.isabs(path):
        return path
    return os.path.join(root_path, path)


def write_report(path: str, report: Dict[str, Any]) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    dump_yaml(path, {"PATCH_EXECUTION_REPORT": report})


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: apply_learnit_core_patch_v4.py <patchfile> <rootpath> <whatif:true|false> [report_path]"
        )

    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"
    cli_report_path = sys.argv[4] if len(sys.argv) >= 5 else None

    patch_doc = load_yaml(patch_file)
    patch_set = patch_doc["PATCH_SET"]
    dsl_version = str(patch_set.get("patch_dsl_version", ""))
    if dsl_version not in {"2.0", "2.5", "3.0", "4.0"}:
        raise PatchError(f"Version de DSL non supportée: {dsl_version}")
    atomic = bool(patch_set.get("atomic", True))
    report_path = compute_report_path(patch_set, cli_report_path, root_path)

    report: Dict[str, Any] = {
        "patch_id": patch_set.get("id"),
        "patch_dsl_version": dsl_version,
        "atomic": atomic,
        "whatif": whatif,
        "started_at": utc_now(),
        "status": "PASS",
        "files": [],
        "summary": {
            "files_total": 0,
            "files_changed": 0,
            "operations_total": 0,
            "operations_applied": 0,
            "operations_skipped": 0,
            "backups_created": 0,
        },
    }

    staged_docs: Dict[str, Tuple[Any, Any, Any]] = {}
    file_entries = patch_set.get("files", []) or []
    report["summary"]["files_total"] = len(file_entries)

    try:
        for file_entry in file_entries:
            rel_path = file_entry["file"]
            expected_core_id = file_entry.get("expected_core_id")
            full_path = os.path.join(root_path, rel_path)
            if not os.path.exists(full_path):
                raise PatchError(f"Fichier introuvable: {full_path}")

            original = load_yaml(full_path)
            doc = copy.deepcopy(original)
            root = detect_root(doc)
            actual_core_id = get_core_id(doc)
            if expected_core_id and actual_core_id and expected_core_id != actual_core_id:
                raise PatchError(
                    f"Core ID inattendu pour {rel_path}: attendu={expected_core_id} trouvé={actual_core_id}"
                )

            file_report = {
                "file": rel_path,
                "expected_core_id": expected_core_id,
                "actual_core_id": actual_core_id,
                "changed": False,
                "backups_created": [],
                "operations": [],
            }

            changed = False
            for op in file_entry.get("operations", []):
                report["summary"]["operations_total"] += 1
                op_type = op.get("op")
                try:
                    message = apply_operation(root, op)
                    file_report["operations"].append({
                        "op": op_type,
                        "status": "applied",
                        "message": message,
                    })
                    if op_type not in {"assert", "assert_meta", "note", "no_change"}:
                        changed = True
                        report["summary"]["operations_applied"] += 1
                    else:
                        report["summary"]["operations_skipped"] += 1
                except Exception as exc:
                    file_report["operations"].append({
                        "op": op_type,
                        "status": "failed",
                        "message": str(exc),
                    })
                    raise

            validate_root_metadata(root)
            validate_core_type_consistency(root, rel_path)
            validate_local_references(root)
            collect_ids(root)

            file_report["changed"] = changed
            if changed:
                report["summary"]["files_changed"] += 1
            report["files"].append(file_report)
            staged_docs[full_path] = (original, doc, root)

        if not whatif:
            for file_report in report["files"]:
                rel_path = file_report["file"]
                full_path = os.path.join(root_path, rel_path)
                original, doc, _ = staged_docs[full_path]
                if not file_report["changed"]:
                    continue
                bak_path = full_path + ".bak"
                if not os.path.exists(bak_path):
                    dump_yaml(bak_path, original)
                    file_report["backups_created"].append(bak_path)
                    report["summary"]["backups_created"] += 1
                dump_yaml(full_path, doc)

    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = str(exc)
        report["finished_at"] = utc_now()
        if report_path:
            write_report(report_path, report)
        if atomic:
            raise
        else:
            print(f"[WARN] Erreur non atomique: {exc}", file=sys.stderr)
            sys.exit(1)

    report["finished_at"] = utc_now()
    if report_path:
        write_report(report_path, report)

    print("PATCH_EXECUTION:")
    print(f"  status: {report['status']}")
    print(f"  patch_id: {report['patch_id']}")
    print(f"  patch_dsl_version: {report['patch_dsl_version']}")
    print(f"  whatif: {str(whatif).lower()}")
    print(f"  files_total: {report['summary']['files_total']}")
    print(f"  files_changed: {report['summary']['files_changed']}")
    print(f"  operations_total: {report['summary']['operations_total']}")
    print(f"  operations_applied: {report['summary']['operations_applied']}")
    print(f"  operations_skipped: {report['summary']['operations_skipped']}")
    if report_path:
        print(f"  report_path: {report_path}")


if __name__ == "__main__":
    main()
