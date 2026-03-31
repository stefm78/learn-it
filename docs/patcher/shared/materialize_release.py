#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT_KEY = "RELEASE_PLAN"
ROLE_FILES = {
    "constitution": "constitution.yaml",
    "referentiel": "referentiel.yaml",
    "link": "link.yaml",
}
DEFAULT_REPORT_PATH = "docs/pipelines/constitution/reports/release_materialization_report.yaml"
DEFAULT_NOTES_PATH = "docs/pipelines/constitution/outputs/release_candidate_notes.md"


class MaterializationError(Exception):
    pass


def repo_path(value: Any) -> str:
    return str(value).replace("\\", "/")


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_release_plan(path: Path) -> Dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or ROOT_KEY not in doc:
        raise MaterializationError(f"{ROOT_KEY} absent")
    plan = doc[ROOT_KEY]
    if not isinstance(plan, dict):
        raise MaterializationError(f"{ROOT_KEY} invalide")
    return plan


def normalize_replacement(entry: Dict[str, Any]) -> Tuple[str, str, str | None]:
    old_value = entry.get("from") or entry.get("old_id") or entry.get("replace")
    new_value = entry.get("to") or entry.get("new_id") or entry.get("with")
    role = entry.get("file_role") or entry.get("role")
    if not isinstance(old_value, str) or not old_value:
        raise MaterializationError(f"replacement invalide sans ancienne valeur: {entry}")
    if not isinstance(new_value, str) or not new_value:
        raise MaterializationError(f"replacement invalide sans nouvelle valeur: {entry}")
    if role is not None and role not in ROLE_FILES:
        raise MaterializationError(f"replacement avec rôle inconnu: {role}")
    return old_value, new_value, role


def collect_replacements(plan: Dict[str, Any]) -> List[Tuple[str, str, str | None]]:
    replacements: List[Tuple[str, str, str | None]] = []
    for field_name in ("required_renames", "required_reference_updates"):
        value = plan.get(field_name, [])
        if value is None:
            continue
        if not isinstance(value, list):
            raise MaterializationError(f"{field_name} doit être une liste")
        for entry in value:
            if not isinstance(entry, dict):
                raise MaterializationError(f"{field_name} contient une entrée invalide")
            replacements.append(normalize_replacement(entry))
    return replacements


def deep_replace_strings(obj: Any, replacements: List[Tuple[str, str]]) -> Any:
    if isinstance(obj, dict):
        return {k: deep_replace_strings(v, replacements) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_replace_strings(item, replacements) for item in obj]
    if isinstance(obj, str):
        updated = obj
        for old_value, new_value in replacements:
            updated = updated.replace(old_value, new_value)
        return updated
    return obj


def semantic_version_aliases(version: str) -> List[str]:
    aliases = {version}
    if version.endswith("_FINAL"):
        aliases.add(version.replace("_FINAL", ""))
    raw = version.replace("_FINAL", "")
    if raw.startswith("V") and "_" in raw:
        major_minor = raw[1:]
        aliases.add(f"v{major_minor.replace('_', '.')}")
        aliases.add(f"V{major_minor.replace('_', '.')}")
    return sorted(aliases, key=len, reverse=True)


def build_editorial_replacements(target_versions: Dict[str, Any]) -> List[Tuple[str, str, None]]:
    replacements: List[Tuple[str, str, None]] = []
    seen = set()
    for role, entry in target_versions.items():
        if not isinstance(entry, dict):
            continue
        current_version = entry.get("current_version")
        target_version = entry.get("target_version")
        current_core_id = entry.get("current_core_id")
        target_core_id = entry.get("target_core_id")
        if isinstance(current_core_id, str) and isinstance(target_core_id, str) and current_core_id != target_core_id:
            key = (current_core_id, target_core_id)
            if key not in seen:
                seen.add(key)
                replacements.append((current_core_id, target_core_id, None))
        if isinstance(current_version, str) and isinstance(target_version, str) and current_version != target_version:
            current_aliases = semantic_version_aliases(current_version)
            target_aliases = semantic_version_aliases(target_version)
            for old_alias, new_alias in zip(current_aliases, target_aliases):
                key = (old_alias, new_alias)
                if old_alias != new_alias and key not in seen:
                    seen.add(key)
                    replacements.append((old_alias, new_alias, None))
    return replacements


def apply_target_version(doc: Dict[str, Any], role: str, target_versions: Dict[str, Any]) -> None:
    entry = target_versions.get(role)
    if not isinstance(entry, dict):
        return
    core = doc.get("CORE")
    if not isinstance(core, dict):
        raise MaterializationError(f"CORE absent dans le fichier {role}")
    target_core_id = entry.get("target_core_id")
    target_version = entry.get("target_version")
    if isinstance(target_core_id, str) and target_core_id:
        core["id"] = target_core_id
    if isinstance(target_version, str) and target_version:
        core["version"] = target_version


def apply_role_replacements(doc: Dict[str, Any], role: str, replacements: List[Tuple[str, str, str | None]]) -> Dict[str, Any]:
    scoped_replacements: List[Tuple[str, str]] = []
    for old_value, new_value, target_role in replacements:
        if target_role is None or target_role == role:
            scoped_replacements.append((old_value, new_value))
    scoped_replacements.sort(key=lambda item: len(item[0]), reverse=True)
    return deep_replace_strings(doc, scoped_replacements)


def build_release_manifest(
    release_id: str,
    plan_path: Path,
    plan: Dict[str, Any],
    role_docs: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    validated_inputs = plan.get("validated_inputs")
    release_bundle = plan.get("release_bundle", {})
    promotion_candidate = False
    if isinstance(release_bundle, dict):
        promotion_candidate = bool(release_bundle.get("promotion_candidate", False))

    cores: List[Dict[str, Any]] = []
    for role, file_name in ROLE_FILES.items():
        core = role_docs[role].get("CORE", {})
        cores.append(
            {
                "role": role,
                "file": file_name,
                "core_id": core.get("id"),
                "version": core.get("version"),
            }
        )

    provenance: Dict[str, Any] = {"release_plan": repo_path(plan_path)}
    if isinstance(validated_inputs, dict):
        for key, value in validated_inputs.items():
            provenance[key] = repo_path(value) if isinstance(value, str) else value

    return {
        "RELEASE_MANIFEST": {
            "release_id": release_id,
            "status": "READY",
            "immutable": True,
            "source": {
                "pipeline": "constitution",
                "stage": "07B_RELEASE_MATERIALIZATION",
                "release_plan": repo_path(plan_path),
            },
            "cores": cores,
            "provenance": provenance,
            "promotion": {
                "promotion_candidate": promotion_candidate,
                "promoted_to_current": False,
            },
            "notes": plan.get("notes", []),
        }
    }


def build_release_notes(release_id: str, release_path: str, plan: Dict[str, Any], manifest: Dict[str, Any]) -> str:
    change_depth = plan.get("change_depth", "unknown")
    release_required = plan.get("release_required")
    lines = [
        f"# Release candidate — {release_id}",
        "",
        f"- release_required: `{release_required}`",
        f"- change_depth: `{change_depth}`",
        f"- release_path: `{release_path}`",
        "",
        "## Cores matérialisés",
        "",
    ]
    cores = manifest.get("RELEASE_MANIFEST", {}).get("cores", [])
    for entry in cores:
        if isinstance(entry, dict):
            lines.append(f"- `{entry.get('role')}` → `{entry.get('core_id')}` / `{entry.get('version')}`")
    notes = plan.get("notes", [])
    if isinstance(notes, list) and notes:
        lines.extend(["", "## Notes", ""])
        for note in notes:
            lines.append(f"- {note}")
    lines.extend(["", "## Statut", "", "Release matérialisée sans modification de `docs/cores/current/`.", ""])
    return "\n".join(lines)


def build_report(status: str, release_id: str, release_path: str, files_written: List[str], notes: List[str]) -> Dict[str, Any]:
    normalized_release_path = repo_path(release_path)
    normalized_files_written = [repo_path(path) for path in files_written]
    return {
        "RELEASE_MATERIALIZATION_REPORT": {
            "status": status,
            "release_id": release_id,
            "release_path": normalized_release_path,
            "files_written": normalized_files_written,
            "manifest_written": any(path.endswith("manifest.yaml") for path in normalized_files_written),
            "notes": notes,
        }
    }


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: materialize_release_v2.py <release_plan.yaml> <patched_dir> [report.yaml] [release_candidate_notes.md]"
        )
    plan_path = Path(sys.argv[1])
    patched_dir = Path(sys.argv[2])
    report_path = Path(sys.argv[3]) if len(sys.argv) >= 4 else Path(DEFAULT_REPORT_PATH)
    notes_path = Path(sys.argv[4]) if len(sys.argv) >= 5 else Path(DEFAULT_NOTES_PATH)

    try:
        plan = read_release_plan(plan_path)
        if plan.get("status") != "PASS":
            raise MaterializationError("release_plan doit être en status PASS")

        release_required = plan.get("release_required")
        if not isinstance(release_required, bool):
            raise MaterializationError("release_required doit être explicitement booléen")

        release_bundle = plan.get("release_bundle")
        if not isinstance(release_bundle, dict):
            raise MaterializationError("release_bundle absent ou invalide")

        release_id = release_bundle.get("release_id")
        release_path_value = release_bundle.get("release_path")
        if not isinstance(release_id, str) or not release_id:
            raise MaterializationError("release_bundle.release_id absent ou invalide")
        if not isinstance(release_path_value, str) or not release_path_value:
            raise MaterializationError("release_bundle.release_path absent ou invalide")

        normalized_release_path_value = repo_path(release_path_value)
        release_path = Path(normalized_release_path_value)

        if not release_required:
            notes = ["release_required=false : aucune matérialisation effectuée"]
            write_text(notes_path, "# Release candidate\n\nAucune release matérialisée : `release_required=false`.\n")
            dump_yaml(report_path, build_report("PASS", release_id, normalized_release_path_value, [], notes))
            return

        target_versions = plan.get("target_versions")
        if not isinstance(target_versions, dict):
            raise MaterializationError("target_versions absent ou invalide")

        replacements = collect_replacements(plan) + build_editorial_replacements(target_versions)
        role_docs: Dict[str, Dict[str, Any]] = {}
        files_written: List[str] = []

        release_path.mkdir(parents=True, exist_ok=True)

        for role, file_name in ROLE_FILES.items():
            source_path = patched_dir / file_name
            if not source_path.exists():
                raise MaterializationError(f"fichier patché manquant: {source_path}")

            doc = load_yaml(source_path)
            if not isinstance(doc, dict):
                raise MaterializationError(f"document YAML invalide: {source_path}")

            apply_target_version(doc, role, target_versions)
            doc = apply_role_replacements(doc, role, replacements)
            role_docs[role] = doc

            destination_path = release_path / file_name
            dump_yaml(destination_path, doc)
            files_written.append(repo_path(destination_path))

        manifest = build_release_manifest(release_id, plan_path, plan, role_docs)
        manifest_path = release_path / "manifest.yaml"
        dump_yaml(manifest_path, manifest)
        files_written.append(repo_path(manifest_path))

        write_text(notes_path, build_release_notes(release_id, normalized_release_path_value, plan, manifest))
        dump_yaml(
            report_path,
            build_report(
                "PASS",
                release_id,
                normalized_release_path_value,
                files_written,
                [f"release matérialisée sous {normalized_release_path_value}", "aucune modification de docs/cores/current/"],
            ),
        )

    except Exception as exc:
        release_id = "unknown"
        release_path = "unknown"
        try:
            if plan_path.exists():
                plan = read_release_plan(plan_path)
                release_bundle = plan.get("release_bundle", {})
                if isinstance(release_bundle, dict):
                    release_id = str(release_bundle.get("release_id", release_id))
                    release_path = repo_path(release_bundle.get("release_path", release_path))
        except Exception:
            pass

        dump_yaml(report_path, build_report("FAIL", release_id, release_path, [], [str(exc)]))
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
