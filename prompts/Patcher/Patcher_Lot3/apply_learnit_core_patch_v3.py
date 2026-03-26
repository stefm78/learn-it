#!/usr/bin/env python3
import copy
import os
import sys
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
    "note",
    "no_change",
}


class PatchError(Exception):
    pass


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


def rewrite_text_path(root: Dict[str, Any], field_path: str, old_id: str, new_id: str) -> int:
    value = get_nested_value(root, field_path)
    if not isinstance(value, str):
        raise PatchError(f"Le champ texte '{field_path}' n'est pas une chaîne")
    new_value = value.replace(old_id, new_id)
    count = 1 if new_value != value else 0
    set_nested_value(root, field_path, new_value)
    return count


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
        rewritten += rewrite_text_path(root, field_path, old_id, new_id)

    return f"rewrite_references {old_id} -> {new_id} ({rewritten})"


def validate_root_metadata(root: Dict[str, Any]) -> None:
    if not isinstance(root.get("id"), str) or not root.get("id"):
        raise PatchError("Métadonnée racine invalide: id manquant")
    if not isinstance(root.get("core_type"), str) or not root.get("core_type"):
        raise PatchError("Métadonnée racine invalide: core_type manquant")


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
    if op_type == "note":
        return f"note ({op.get('value', {}).get('reason', 'no reason')})"
    if op_type == "no_change":
        return f"no_change ({op.get('reason', 'no reason')})"
    raise PatchError(f"Opération non gérée: {op_type}")


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: apply_learnit_core_patch_v3.py <patchfile> <rootpath> <whatif:true|false>")

    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"

    patch_doc = load_yaml(patch_file)
    patch_set = patch_doc["PATCH_SET"]
    dsl_version = str(patch_set.get("patch_dsl_version", ""))
    if dsl_version not in {"2.0", "2.5", "3.0"}:
        raise PatchError(f"Version de DSL non supportée: {dsl_version}")
    atomic = bool(patch_set.get("atomic", True))

    staged_docs: Dict[str, Tuple[Any, Any, Any]] = {}
    logs: List[Tuple[str, List[str], bool]] = []

    for file_entry in patch_set["files"]:
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
        staged_docs[rel_path] = (original, doc, root)

    for file_entry in patch_set["files"]:
        rel_path = file_entry["file"]
        _, doc, root = staged_docs[rel_path]
        op_logs: List[str] = []
        changed = False
        for op in file_entry["operations"]:
            log = apply_operation(root, op)
            op_logs.append(log)
            if op["op"] not in {"assert", "assert_meta", "note", "no_change"}:
                changed = True
        validate_root_metadata(root)
        validate_local_references(root)
        validate_core_type_consistency(root, rel_path)
        _ = collect_ids(root)
        logs.append((rel_path, op_logs, changed))

    for rel_path, op_logs, changed in logs:
        print(f"[INFO] Traitement: {rel_path}")
        for line in op_logs:
            print(f"  - {line}")
        if changed:
            if whatif:
                print(f"[WHATIF] Modifications détectées pour {rel_path}, aucune écriture.")
            else:
                original, doc, _ = staged_docs[rel_path]
                full_path = os.path.join(root_path, rel_path)
                bak_path = full_path + ".bak"
                if not os.path.exists(bak_path):
                    dump_yaml(bak_path, original)
                    print(f"[INFO] Backup créé: {bak_path}")
                dump_yaml(full_path, doc)
                print(f"[OK] Fichier mis à jour: {full_path}")
        else:
            print(f"[INFO] Aucun changement écrit pour {rel_path}")

    if atomic:
        print("[OK] Patch appliqué en mode atomique.")


if __name__ == "__main__":
    try:
        main()
    except PatchError as e:
        print(f"[ERR] {e}", file=sys.stderr)
        sys.exit(1)
