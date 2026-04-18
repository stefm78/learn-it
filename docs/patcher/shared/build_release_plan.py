#!/usr/bin/env python3
import copy
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


ROLE_FILES = {
    "constitution": "constitution.yaml",
    "referentiel": "referentiel.yaml",
    "link": "link.yaml",
}
ROLE_ORDER = ["constitution", "referentiel", "link"]
ROOT_KEY = "RELEASE_PLAN"
EDITORIAL_FIELDS = {"description", "human_readable", "source_anchor"}
SECTION_NAMES = [
    "TYPES",
    "INVARIANTS",
    "RULES",
    "PARAMETERS",
    "CONSTRAINTS",
    "EVENTS",
    "ACTIONS",
    "DEPENDENCIES",
]
CHANGE_RANK = {"none": 0, "editorial": 1, "minor": 2, "major": 3}
NESTED_CORE_SUBPATH = Path("docs/cores/current")


class ReleasePlanError(Exception):
    pass


@dataclass
class RoleAssessment:
    role: str
    current_core_id: str
    current_version: str
    target_core_id: str
    target_version: str
    change_depth: str
    identical_content: bool
    additions: List[str]
    removals: List[str]
    modifications: List[str]
    editorial_only: bool



def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)



def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)



def ensure_file(path: Path) -> None:
    if not path.exists():
        raise ReleasePlanError(f"fichier introuvable: {path}")



def resolve_core_file(base_dir: Path, file_name: str) -> Path:
    candidates = [
        base_dir / file_name,
        base_dir / NESTED_CORE_SUBPATH / file_name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    tried = " | ".join(str(candidate) for candidate in candidates)
    raise ReleasePlanError(
        f"fichier introuvable pour {file_name} sous {base_dir}. chemins essayés: {tried}"
    )



def read_core(path: Path) -> Dict[str, Any]:
    ensure_file(path)
    doc = load_yaml(path)
    if not isinstance(doc, dict) or "CORE" not in doc or not isinstance(doc["CORE"], dict):
        raise ReleasePlanError(f"CORE absent ou invalide: {path}")
    return doc



def clone_without_editorial_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            k: clone_without_editorial_fields(v)
            for k, v in value.items()
            if k not in EDITORIAL_FIELDS
        }
    if isinstance(value, list):
        return [clone_without_editorial_fields(item) for item in value]
    return copy.deepcopy(value)



def list_to_id_map(value: Any) -> Optional[Dict[str, Dict[str, Any]]]:
    if not isinstance(value, list):
        return None
    mapped: Dict[str, Dict[str, Any]] = {}
    for item in value:
        if not isinstance(item, dict):
            return None
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            return None
        if item_id in mapped:
            return None
        mapped[item_id] = item
    return mapped



def compare_section(section_name: str, patched: Any, current: Any) -> Tuple[List[str], List[str], List[str], bool]:
    additions: List[str] = []
    removals: List[str] = []
    modifications: List[str] = []
    editorial_only = True

    patched_map = list_to_id_map(patched)
    current_map = list_to_id_map(current)

    if patched_map is None or current_map is None:
        if patched != current:
            modifications.append(section_name)
            editorial_only = clone_without_editorial_fields(patched) == clone_without_editorial_fields(current)
        return additions, removals, modifications, editorial_only

    patched_ids = set(patched_map.keys())
    current_ids = set(current_map.keys())

    for added_id in sorted(patched_ids - current_ids):
        additions.append(f"{section_name}/{added_id}")

    for removed_id in sorted(current_ids - patched_ids):
        removals.append(f"{section_name}/{removed_id}")
        editorial_only = False

    for shared_id in sorted(patched_ids & current_ids):
        patched_entry = patched_map[shared_id]
        current_entry = current_map[shared_id]
        if patched_entry == current_entry:
            continue
        modifications.append(f"{section_name}/{shared_id}")
        if clone_without_editorial_fields(patched_entry) != clone_without_editorial_fields(current_entry):
            editorial_only = False

    return additions, removals, modifications, editorial_only



def assess_role(role: str, patched_doc: Dict[str, Any], current_doc: Dict[str, Any]) -> RoleAssessment:
    patched_core = patched_doc["CORE"]
    current_core = current_doc["CORE"]

    current_core_id = str(current_core.get("id", ""))
    current_version = str(current_core.get("version", ""))
    patched_core_id = str(patched_core.get("id", current_core_id))
    patched_version = str(patched_core.get("version", current_version))

    additions: List[str] = []
    removals: List[str] = []
    modifications: List[str] = []
    editorial_only = True

    for section_name in SECTION_NAMES:
        section_additions, section_removals, section_modifications, section_editorial_only = compare_section(
            section_name,
            patched_core.get(section_name, []),
            current_core.get(section_name, []),
        )
        additions.extend(section_additions)
        removals.extend(section_removals)
        modifications.extend(section_modifications)
        editorial_only = editorial_only and section_editorial_only

    meta_paths = [
        ("CORE/description", patched_core.get("description"), current_core.get("description")),
    ]
    for path, patched_value, current_value in meta_paths:
        if patched_value != current_value:
            modifications.append(path)

    identical_content = patched_core == current_core

    if identical_content:
        change_depth = "none"
    elif removals:
        change_depth = "major"
    elif modifications and not editorial_only:
        change_depth = "major"
    elif additions:
        change_depth = "minor"
    elif modifications:
        change_depth = "editorial"
    else:
        change_depth = "none"

    return RoleAssessment(
        role=role,
        current_core_id=current_core_id,
        current_version=current_version,
        target_core_id=patched_core_id,
        target_version=patched_version,
        change_depth=change_depth,
        identical_content=identical_content,
        additions=additions,
        removals=removals,
        modifications=modifications,
        editorial_only=editorial_only,
    )



def parse_version(version: str) -> Tuple[int, int, str]:
    match = re.fullmatch(r"V(\d+)_(\d+)(.*)", version)
    if not match:
        raise ReleasePlanError(f"version non supportée pour incrémentation: {version}")
    major = int(match.group(1))
    minor = int(match.group(2))
    suffix = match.group(3)
    return major, minor, suffix



def format_version(major: int, minor: int, suffix: str) -> str:
    return f"V{major}_{minor}{suffix}"



def bump_version(version: str, depth: str) -> str:
    major, minor, suffix = parse_version(version)
    if depth == "minor":
        return format_version(major, minor + 1, suffix)
    if depth == "major":
        return format_version(major + 1, 0, suffix)
    return version



def replace_version_token(text: str, old_version: str, new_version: str) -> str:
    token_old = old_version.replace("_FINAL", "")
    token_new = new_version.replace("_FINAL", "")
    return text.replace(token_old, token_new)



def build_target_core_id(current_core_id: str, current_version: str, target_version: str) -> str:
    return replace_version_token(current_core_id, current_version, target_version)



def normalize_link_id_token(version: str, current_token: str) -> str:
    raw = version.replace("_FINAL", "")
    match = re.fullmatch(r"V(\d+)_(\d+)", raw)
    if not match:
        raise ReleasePlanError(f"version LINK non supportée: {version}")
    major = match.group(1)
    minor = match.group(2)

    if current_token.startswith("v") and "." in current_token:
        return f"v{major}.{minor}"
    if current_token.startswith("V") and "." in current_token:
        return f"V{major}.{minor}"
    if current_token.startswith("v"):
        return f"v{major}_{minor}"
    return f"V{major}_{minor}"



def compute_link_targets(
    current_doc: Dict[str, Any],
    constitution_target_version: str,
    referentiel_target_version: str,
) -> Tuple[str, str]:
    core = current_doc["CORE"]
    current_core_id = str(core.get("id", ""))
    current_version = str(core.get("version", ""))

    current_constitution_token = re.search(r"CONSTITUTION_([Vv]\d+(?:_\d+|\.\d+))", current_core_id)
    current_referentiel_token = re.search(r"REFERENTIEL_([Vv]\d+(?:_\d+|\.\d+))", current_core_id)
    if not current_constitution_token or not current_referentiel_token:
        raise ReleasePlanError(f"core_id LINK non supporté: {current_core_id}")

    constitution_token = normalize_link_id_token(
        constitution_target_version,
        current_constitution_token.group(1),
    )
    referentiel_token = normalize_link_id_token(
        referentiel_target_version,
        current_referentiel_token.group(1),
    )

    target_core_id = current_core_id
    target_core_id = re.sub(
        r"CONSTITUTION_[Vv]\d+(?:_\d+|\.\d+)",
        f"CONSTITUTION_{constitution_token}",
        target_core_id,
    )
    target_core_id = re.sub(
        r"REFERENTIEL_[Vv]\d+(?:_\d+|\.\d+)",
        f"REFERENTIEL_{referentiel_token}",
        target_core_id,
    )

    target_version = f"{constitution_target_version.replace('_FINAL', '')}__{referentiel_target_version.replace('_FINAL', '')}_FINAL"
    if current_version == target_version and current_core_id == target_core_id:
        return current_core_id, current_version
    return target_core_id, target_version



def collect_reference_updates(
    assessments: Dict[str, RoleAssessment],
    current_docs: Dict[str, Dict[str, Any]],
) -> Tuple[List[Dict[str, str]], List[str]]:
    updates: List[Dict[str, str]] = []
    link_updates: List[str] = []

    for role in ["constitution", "referentiel", "link"]:
        assessment = assessments[role]
        if assessment.current_core_id != assessment.target_core_id:
            updates.append(
                {
                    "file_role": role,
                    "from": assessment.current_core_id,
                    "to": assessment.target_core_id,
                }
            )
        if assessment.current_version != assessment.target_version:
            old_token = assessment.current_version.replace("_FINAL", "")
            new_token = assessment.target_version.replace("_FINAL", "")
            updates.append(
                {
                    "file_role": role,
                    "from": old_token,
                    "to": new_token,
                }
            )

    constitution_changed = assessments["constitution"].current_version != assessments["constitution"].target_version
    referentiel_changed = assessments["referentiel"].current_version != assessments["referentiel"].target_version
    if constitution_changed or referentiel_changed:
        link_updates.append("link_target_versions_realigned_with_constitution_and_referentiel")

        for role in ["constitution", "referentiel", "link"]:
            if constitution_changed:
                current_constitution_id = assessments["constitution"].current_core_id
                target_constitution_id = assessments["constitution"].target_core_id
                if current_constitution_id != target_constitution_id:
                    updates.append({"file_role": role, "from": current_constitution_id, "to": target_constitution_id})
                    updates.append({"file_role": role, "from": current_constitution_id.replace("CORE_", "REF_CORE_") + "_IN_REFERENTIEL", "to": current_constitution_id.replace("CORE_", "REF_CORE_") + "_IN_REFERENTIEL"})
            if referentiel_changed:
                current_referentiel_id = assessments["referentiel"].current_core_id
                target_referentiel_id = assessments["referentiel"].target_core_id
                if current_referentiel_id != target_referentiel_id:
                    updates.append({"file_role": role, "from": current_referentiel_id, "to": target_referentiel_id})

    deduped: List[Dict[str, str]] = []
    seen = set()
    for item in updates:
        key = (item.get("file_role"), item.get("from"), item.get("to"))
        if item.get("from") == item.get("to"):
            continue
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped, link_updates



def build_required_renames(assessments: Dict[str, RoleAssessment]) -> List[Dict[str, str]]:
    renames: List[Dict[str, str]] = []
    for role in ROLE_ORDER:
        assessment = assessments[role]
        if assessment.current_core_id != assessment.target_core_id:
            renames.append(
                {
                    "file_role": role,
                    "from": assessment.current_core_id,
                    "to": assessment.target_core_id,
                }
            )
    return renames



def max_change_depth(depths: List[str]) -> str:
    return max(depths, key=lambda item: CHANGE_RANK[item])



def next_release_id(repo_root: Path) -> Tuple[str, str]:
    release_root = repo_root / "docs" / "cores" / "releases"
    release_root.mkdir(parents=True, exist_ok=True)

    stamp = datetime.utcnow().strftime("%Y_%m_%d")
    pattern = re.compile(rf"CORE_RELEASE_{stamp}_R(\d{{2}})")
    existing_numbers: List[int] = []
    if release_root.exists():
        for child in release_root.iterdir():
            if not child.is_dir():
                continue
            match = pattern.fullmatch(child.name)
            if match:
                existing_numbers.append(int(match.group(1)))

    next_number = max(existing_numbers, default=0) + 1
    release_id = f"CORE_RELEASE_{stamp}_R{next_number:02d}"
    release_path = f"docs/cores/releases/{release_id}/"
    return release_id, release_path



def build_notes(assessments: Dict[str, RoleAssessment], aggregate_depth: str, release_required: bool) -> List[str]:
    notes: List[str] = []
    for role in ROLE_ORDER:
        assessment = assessments[role]
        counter = Counter()
        counter["added"] = len(assessment.additions)
        counter["removed"] = len(assessment.removals)
        counter["modified"] = len(assessment.modifications)
        notes.append(
            f"{role}: change_depth={assessment.change_depth}, identical_content={str(assessment.identical_content).lower()}, added={counter['added']}, removed={counter['removed']}, modified={counter['modified']}"
        )
    notes.append(f"aggregate_change_depth={aggregate_depth}")
    notes.append(f"release_required={str(release_required).lower()}")
    return notes



def main() -> None:
    if len(sys.argv) < 6:
        raise SystemExit(
            "Usage: build_release_plan.py <patched_dir> <current_dir> <core_validation.yaml> <patch_execution_report.yaml> <output_release_plan.yaml>"
        )

    patched_dir = Path(sys.argv[1])
    current_dir = Path(sys.argv[2])
    core_validation_path = Path(sys.argv[3])
    patch_execution_report_path = Path(sys.argv[4])
    output_path = Path(sys.argv[5])

    ensure_file(core_validation_path)
    ensure_file(patch_execution_report_path)

    repo_root = Path.cwd()

    patched_paths = {
        role: resolve_core_file(patched_dir, file_name)
        for role, file_name in ROLE_FILES.items()
    }
    current_paths = {
        role: resolve_core_file(current_dir, file_name)
        for role, file_name in ROLE_FILES.items()
    }

    patched_docs = {role: read_core(path) for role, path in patched_paths.items()}
    current_docs = {role: read_core(path) for role, path in current_paths.items()}

    assessments = {
        role: assess_role(role, patched_docs[role], current_docs[role])
        for role in ROLE_ORDER
    }

    constitution_depth = assessments["constitution"].change_depth
    referentiel_depth = assessments["referentiel"].change_depth

    if constitution_depth in {"minor", "major"}:
        assessments["constitution"].target_version = bump_version(
            assessments["constitution"].current_version,
            constitution_depth,
        )
        assessments["constitution"].target_core_id = build_target_core_id(
            assessments["constitution"].current_core_id,
            assessments["constitution"].current_version,
            assessments["constitution"].target_version,
        )

    if referentiel_depth in {"minor", "major"}:
        assessments["referentiel"].target_version = bump_version(
            assessments["referentiel"].current_version,
            referentiel_depth,
        )
        assessments["referentiel"].target_core_id = build_target_core_id(
            assessments["referentiel"].current_core_id,
            assessments["referentiel"].current_version,
            assessments["referentiel"].target_version,
        )

    link_target_core_id, link_target_version = compute_link_targets(
        current_docs["link"],
        assessments["constitution"].target_version,
        assessments["referentiel"].target_version,
    )
    assessments["link"].target_core_id = link_target_core_id
    assessments["link"].target_version = link_target_version
    if link_target_core_id != assessments["link"].current_core_id or link_target_version != assessments["link"].current_version:
        if assessments["link"].change_depth == "none":
            assessments["link"].change_depth = "minor"
            assessments["link"].modifications.append("CORE/link_version_alignment")

    aggregate_depth = max_change_depth([assessments[role].change_depth for role in ROLE_ORDER])
    release_required = aggregate_depth in {"minor", "major"}

    release_id, release_path = next_release_id(repo_root)
    if not release_required:
        release_id = f"{release_id}_NOOP"

    required_renames = build_required_renames(assessments)
    required_reference_updates, link_updates = collect_reference_updates(assessments, current_docs)

    release_plan = {
        ROOT_KEY: {
            "status": "PASS",
            "release_required": release_required,
            "change_depth": aggregate_depth,
            "validated_inputs": {
                "core_validation": str(core_validation_path),
                "patch_execution_report": str(patch_execution_report_path),
                "patched_cores": {
                    role: str(path)
                    for role, path in patched_paths.items()
                },
            },
            "compared_against_current": {
                role: str(path)
                for role, path in current_paths.items()
            },
            "target_versions": {
                role: {
                    "current_core_id": assessments[role].current_core_id,
                    "current_version": assessments[role].current_version,
                    "target_core_id": assessments[role].target_core_id,
                    "target_version": assessments[role].target_version,
                }
                for role in ROLE_ORDER
            },
            "required_renames": required_renames,
            "required_reference_updates": required_reference_updates,
            "link_updates": link_updates,
            "release_bundle": {
                "release_id": release_id,
                "release_path": release_path,
                "promotion_candidate": release_required,
            },
            "notes": build_notes(assessments, aggregate_depth, release_required),
        }
    }

    dump_yaml(output_path, release_plan)


if __name__ == "__main__":
    main()
