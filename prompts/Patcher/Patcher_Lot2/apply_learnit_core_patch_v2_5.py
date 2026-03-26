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
    if isinstance(doc, dict):
        if isinstance(doc.get("id"), str):
            return doc["id"]
        if isinstance(doc.get("CORE"), dict) and isinstance(doc["CORE"].get("id"), str):
            return doc["CORE"]["id"]
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
        if not create_missing:
            raise
        set_nested_value(item, field, [], create_missing=True)
        value = get_nested_value(item, field)
    if not isinstance(value, list):
        raise PatchError(f"Le champ cible n'est pas une liste: {field}")
    return value


def apply_assert(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    _, _, item = get_object(root, section, item_id)
    field = target.get("field")
    if field:
        _ = get_nested_value(item, field)
        return f"assert {section}/{item_id} field={field}"
    return f"assert {section}/{item_id}"


def append_if_missing(items: List[Dict[str, Any]], new_item: Dict[str, Any], section: str) -> str:
    validate_new_object_shape(new_item, section)
    new_id = new_item.get("id")
    idx, _ = find_item_by_id(items, new_id)
    if idx is not None:
        return f"skip-existing {new_id}"
    items.append(new_item)
    return f"append {new_id}"


def apply_append(root: Dict[str, Any], op: Dict[str, Any]) -> List[str]:
    section = op["target"]["section"]
    items = ensure_list_section(root, section)
    results: List[str] = []
    if "value" in op:
        results.append(append_if_missing(items, op["value"], section))
    elif "values" in op:
        for value in op["values"]:
            results.append(append_if_missing(items, value, section))
    else:
        raise PatchError("append sans 'value' ou 'values'")
    return results


def apply_replace(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    value = op["value"]
    validate_new_object_shape(value, section)
    items, idx, _ = get_object(root, section, item_id)
    items[idx] = value
    return f"replace {section}/{item_id}"


def apply_replace_field(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    field = target["field"]
    create_missing = bool(op.get("create_missing", False))
    _, _, item = get_object(root, section, item_id)
    set_nested_value(item, field, op["value"], create_missing=create_missing)
    return f"replace_field {section}/{item_id} field={field}"


def apply_remove(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    refs = extract_references(root)
    inbound = [source for source, targets in refs.items() if item_id in targets]
    if inbound and not bool(op.get("force", False)):
        raise PatchError(f"remove interdit: {item_id} encore référencé par {inbound}")
    items, idx, _ = get_object(root, section, item_id)
    del items[idx]
    return f"remove {section}/{item_id}"


def apply_rename(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    new_id = op["new_id"]
    items = ensure_list_section(root, section)
    existing_idx, _ = find_item_by_id(items, new_id)
    if existing_idx is not None:
        raise PatchError(f"rename interdit: nouvel id déjà présent dans {section}: {new_id}")
    _, _, item = get_object(root, section, item_id)
    item["id"] = new_id
    return f"rename {section}/{item_id} -> {new_id}"


def apply_append_field_list(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    field = target["field"]
    create_missing = bool(op.get("create_missing", False))
    unique = bool(op.get("unique", True))
    _, _, item = get_object(root, section, item_id)
    lst = get_list_field(item, field, create_missing=create_missing)
    value = op["value"]
    if unique and value in lst:
        return f"skip-existing-field-list {section}/{item_id} field={field}"
    lst.append(value)
    return f"append_field_list {section}/{item_id} field={field}"


def apply_remove_field_list_item(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    section = target["section"]
    item_id = target["id"]
    field = target["field"]
    all_matches = bool(op.get("all_matches", False))
    _, _, item = get_object(root, section, item_id)
    lst = get_list_field(item, field, create_missing=False)
    value = op["value"]
    removed = 0
    i = 0
    while i < len(lst):
        if lst[i] == value:
            del lst[i]
            removed += 1
            if not all_matches:
                break
            continue
        i += 1
    if removed == 0:
        raise PatchError(f"Élément de liste introuvable dans {section}/{item_id} field={field}")
    return f"remove_field_list_item {section}/{item_id} field={field} removed={removed}"


def apply_move(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    target = op["target"]
    src_section = target["section"]
    item_id = target["id"]
    dst_section = op["destination"]["section"]
    src_items, idx, item = get_object(root, src_section, item_id)
    dst_items = ensure_list_section(root, dst_section)
    existing_idx, _ = find_item_by_id(dst_items, item_id)
    if existing_idx is not None:
        raise PatchError(f"move interdit: {item_id} déjà présent dans {dst_section}")
    validate_new_object_shape(item, dst_section)
    moved = copy.deepcopy(item)
    del src_items[idx]
    dst_items.append(moved)
    return f"move {src_section}/{item_id} -> {dst_section}/{item_id}"


def apply_ensure_exists(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is not None:
        return f"ensure_exists skip {section}/{item_id}"
    value = op["value"]
    if value.get("id") != item_id:
        raise PatchError(f"ensure_exists incohérent: target.id={item_id} value.id={value.get('id')}")
    validate_new_object_shape(value, section)
    items.append(value)
    return f"ensure_exists append {section}/{item_id}"


def apply_ensure_absent(root: Dict[str, Any], op: Dict[str, Any]) -> str:
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is None:
        return f"ensure_absent ok {section}/{item_id}"
    if bool(op.get("remove_if_present", False)):
        return apply_remove(root, {"target": {"section": section, "id": item_id}, "force": op.get("force", False)})
    raise PatchError(f"ensure_absent échoué: {section}/{item_id} est présent")


def apply_no_change(op: Dict[str, Any]) -> str:
    return f"no_change ({op.get('reason', 'no reason')})"


def apply_note(op: Dict[str, Any]) -> str:
    value = op.get("value", {})
    note_id = value.get("id", "no-id") if isinstance(value, dict) else "no-id"
    return f"note ({note_id})"


def validate_root(root: Dict[str, Any], file_path: str) -> None:
    _ = collect_ids(root)
    validate_local_references(root)
    validate_core_type_consistency(root, file_path)


def dispatch_operation(root: Dict[str, Any], op: Dict[str, Any]) -> Tuple[List[str], bool]:
    op_type = op["op"]
    if op_type not in SUPPORTED_OPS:
        raise PatchError(f"Type d'opération non supporté: {op_type}")
    if op_type == "assert":
        return [apply_assert(root, op)], False
    if op_type == "append":
        logs = apply_append(root, op)
        changed = any(not x.startswith(("skip-existing",)) for x in logs)
        return logs, changed
    if op_type == "replace":
        return [apply_replace(root, op)], True
    if op_type == "replace_field":
        return [apply_replace_field(root, op)], True
    if op_type == "remove":
        return [apply_remove(root, op)], True
    if op_type == "rename":
        return [apply_rename(root, op)], True
    if op_type == "append_field_list":
        logs = [apply_append_field_list(root, op)]
        changed = not logs[0].startswith("skip-existing-field-list")
        return logs, changed
    if op_type == "remove_field_list_item":
        return [apply_remove_field_list_item(root, op)], True
    if op_type == "move":
        return [apply_move(root, op)], True
    if op_type == "ensure_exists":
        logs = [apply_ensure_exists(root, op)]
        changed = logs[0].startswith("ensure_exists append")
        return logs, changed
    if op_type == "ensure_absent":
        logs = [apply_ensure_absent(root, op)]
        changed = logs[0].startswith("remove ")
        return logs, changed
    if op_type == "no_change":
        return [apply_no_change(op)], False
    if op_type == "note":
        return [apply_note(op)], False
    raise PatchError(f"Type d'opération non supporté: {op_type}")


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: apply_learnit_core_patch_v2_5.py <patchfile> <rootpath> <whatif:true|false>"
        )
    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"
    patch_doc = load_yaml(patch_file)
    if not isinstance(patch_doc, dict) or "PATCH_SET" not in patch_doc:
        raise PatchError("PATCH_SET absent")
    patch_set = patch_doc["PATCH_SET"]
    if not isinstance(patch_set, dict):
        raise PatchError("PATCH_SET invalide")

    patch_id = patch_set.get("id")
    patch_dsl_version = patch_set.get("patch_dsl_version")
    atomic = bool(patch_set.get("atomic", True))

    print(f"[INFO] PatchSet: {patch_id}")
    if patch_dsl_version is None:
        print("[WARN] patch_dsl_version absent ; compatibilité legacy activée")
    else:
        print(f"[INFO] Patch DSL version: {patch_dsl_version}")
    print(f"[INFO] Atomic mode: {atomic}")

    files = patch_set.get("files")
    if not isinstance(files, list) or not files:
        raise PatchError("PATCH_SET.files absent ou invalide")

    staged_docs: List[Dict[str, Any]] = []

    for file_entry in files:
        rel_path = file_entry["file"]
        expected_core_id = file_entry.get("expected_core_id")
        full_path = os.path.join(root_path, rel_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Fichier introuvable: {full_path}")
        original = load_yaml(full_path)
        doc = copy.deepcopy(original)
        root = detect_root(doc)
        if not isinstance(root, dict):
            raise PatchError(f"Racine invalide dans {rel_path}")
        actual_core_id = get_core_id(doc) or get_core_id(root)
        print(f"[INFO] Traitement: {rel_path}")
        if expected_core_id and actual_core_id and expected_core_id != actual_core_id:
            raise PatchError(
                f"Core ID inattendu pour {rel_path}: attendu={expected_core_id} trouvé={actual_core_id}"
            )
        operations = file_entry.get("operations", [])
        if not isinstance(operations, list):
            raise PatchError(f"operations invalide pour {rel_path}")

        op_logs: List[str] = []
        changed = False
        for op in operations:
            logs, op_changed = dispatch_operation(root, op)
            op_logs.extend(logs)
            changed = changed or op_changed
        validate_root(root, rel_path)
        staged_docs.append(
            {
                "rel_path": rel_path,
                "full_path": full_path,
                "original": original,
                "doc": doc,
                "changed": changed,
                "op_logs": op_logs,
            }
        )

    if atomic:
        # Future cross-file validations can be added here.
        pass

    for staged in staged_docs:
        rel_path = staged["rel_path"]
        for line in staged["op_logs"]:
            print(f"  - {line}")
        if staged["changed"]:
            if whatif:
                print(f"[WHATIF] Modifications détectées pour {rel_path}, aucune écriture.")
            else:
                bak_path = staged["full_path"] + ".bak"
                if not os.path.exists(bak_path):
                    dump_yaml(bak_path, staged["original"])
                    print(f"[INFO] Backup créé: {bak_path}")
                dump_yaml(staged["full_path"], staged["doc"])
                print(f"[OK] Fichier mis à jour: {staged['full_path']}")
        else:
            print(f"[INFO] Aucun changement écrit pour {rel_path}")


if __name__ == "__main__":
    try:
        main()
    except PatchError as e:
        print(f"[ERR]  {e}", file=sys.stderr)
        sys.exit(1)
