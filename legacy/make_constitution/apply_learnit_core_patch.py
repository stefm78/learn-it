#!/usr/bin/env python3
import copy
import os
import sys
import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            width=1000
        )


def ensure_list_section(doc, section_name):
    if section_name not in doc or doc[section_name] is None:
        doc[section_name] = []
    if not isinstance(doc[section_name], list):
        raise ValueError(f"Section '{section_name}' n'est pas une liste.")
    return doc[section_name]


def find_item_by_id(items, item_id):
    for idx, item in enumerate(items):
        if isinstance(item, dict) and item.get("id") == item_id:
            return idx, item
    return None, None


def get_core_id(doc):
    if isinstance(doc, dict):
        if "id" in doc and isinstance(doc["id"], str):
            return doc["id"]
        if "CORE" in doc and isinstance(doc["CORE"], dict):
            return doc["CORE"].get("id")
    return None


def detect_root(doc):
    if isinstance(doc, dict) and "CORE" in doc and isinstance(doc["CORE"], dict):
        return doc["CORE"]
    return doc


def apply_replace(root, op):
    section = op["target"]["section"]
    item_id = op["target"]["id"]
    value = op["value"]

    items = ensure_list_section(root, section)
    idx, _ = find_item_by_id(items, item_id)
    if idx is None:
        raise ValueError(
            f"replace impossible: id '{item_id}' introuvable dans section '{section}'"
        )
    items[idx] = value
    return f"replace {section}/{item_id}"


def append_if_missing(items, new_item):
    new_id = new_item.get("id")
    if not new_id:
        items.append(new_item)
        return "append <no-id>"
    idx, _ = find_item_by_id(items, new_id)
    if idx is not None:
        return f"skip-existing {new_id}"
    items.append(new_item)
    return f"append {new_id}"


def apply_append(root, op):
    section = op["target"]["section"]
    items = ensure_list_section(root, section)

    results = []
    if "value" in op:
        results.append(append_if_missing(items, op["value"]))
    elif "values" in op:
        for v in op["values"]:
            results.append(append_if_missing(items, v))
    else:
        raise ValueError("append sans 'value' ou 'values'")
    return results


def apply_no_change(op):
    return f"no_change ({op.get('reason', 'no reason')})"


def apply_note(op):
    return f"note ({op['value'].get('id', 'no-id')})"


def main():
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: apply_learnit_core_patch.py <patchfile> <rootpath> <whatif:true|false>"
        )

    patch_file = sys.argv[1]
    root_path = sys.argv[2]
    whatif = sys.argv[3].lower() == "true"

    patch_doc = load_yaml(patch_file)
    patch_set = patch_doc["PATCH_SET"]

    print(f"[INFO] PatchSet: {patch_set.get('id')}")

    for file_entry in patch_set["files"]:
        rel_path = file_entry["file"]
        expected_core_id = file_entry.get("expected_core_id")
        full_path = os.path.join(root_path, rel_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Fichier introuvable: {full_path}")

        original = load_yaml(full_path)
        doc = copy.deepcopy(original)
        root = detect_root(doc)
        actual_core_id = get_core_id(doc) or get_core_id(root)

        print(f"[INFO] Traitement: {rel_path}")

        if expected_core_id and actual_core_id and expected_core_id != actual_core_id:
            raise ValueError(
                f"Core ID inattendu pour {rel_path}: attendu={expected_core_id} trouvé={actual_core_id}"
            )

        op_logs = []
        changed = False

        for op in file_entry["operations"]:
            op_type = op["op"]

            if op_type == "replace":
                log = apply_replace(root, op)
                op_logs.append(log)
                changed = True

            elif op_type == "append":
                logs = apply_append(root, op)
                op_logs.extend(logs)
                if any(not x.startswith("skip-existing") for x in logs):
                    changed = True

            elif op_type == "no_change":
                op_logs.append(apply_no_change(op))

            elif op_type == "note":
                op_logs.append(apply_note(op))

            else:
                raise ValueError(f"Type d'opération non supporté: {op_type}")

        for line in op_logs:
            print(f"  - {line}")

        if changed:
            if whatif:
                print(f"[WHATIF] Modifications détectées pour {rel_path}, aucune écriture.")
            else:
                bak_path = full_path + ".bak"
                if not os.path.exists(bak_path):
                    dump_yaml(bak_path, original)
                    print(f"[INFO] Backup créé: {bak_path}")
                dump_yaml(full_path, doc)
                print(f"[OK] Fichier mis à jour: {full_path}")
        else:
            print(f"[INFO] Aucun changement écrit pour {rel_path}")


if __name__ == "__main__":
    main()