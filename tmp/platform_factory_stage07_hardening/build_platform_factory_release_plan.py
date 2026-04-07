#!/usr/bin/env python3
"""Build a deterministic release plan for Platform Factory Stage 07A.

Usage:
    python docs/patcher/shared/build_platform_factory_release_plan.py \
      ./docs/pipelines/platform_factory/work/05_apply/patched \
      ./docs/cores/current \
      ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
      ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
"""

from __future__ import annotations

import copy
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

CORE_VALIDATION_ROOT = "PLATFORM_FACTORY_CORE_VALIDATION"
EXECUTION_ROOT = "PLATFORM_FACTORY_PATCH_EXECUTION"
RELEASE_ID_PATTERN = re.compile(r"^PLATFORM_FACTORY_RELEASE_(\d{4})_(\d{2})_(\d{2})_R(\d{2})$")
EDITORIAL_METADATA_KEYS = {"artifact_id", "version", "status"}

ARTIFACTS = [
    {
        "role": "platform_factory_architecture",
        "filename": "platform_factory_architecture.yaml",
        "root_key": "PLATFORM_FACTORY_ARCHITECTURE",
        "metadata_type": "platform_factory_architecture",
    },
    {
        "role": "platform_factory_state",
        "filename": "platform_factory_state.yaml",
        "root_key": "PLATFORM_FACTORY_STATE",
        "metadata_type": "platform_factory_state",
    },
]


def _repo_path(value: Any) -> str:
    return str(value).replace("\\", "/")


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def _sha256_of_yaml(data: Any) -> str:
    dumped = yaml.safe_dump(data, sort_keys=True, allow_unicode=True)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()


def _semantic_sanitize(data: Any) -> Any:
    sanitized = copy.deepcopy(data)
    if not isinstance(sanitized, dict):
        return sanitized
    root_key = next(iter(sanitized.keys()), None)
    if root_key and isinstance(sanitized.get(root_key), dict):
        metadata = sanitized[root_key].get("metadata")
        if isinstance(metadata, dict):
            for key in EDITORIAL_METADATA_KEYS:
                metadata.pop(key, None)
    return sanitized


def _compare_change_depth(current_doc: Any, patched_doc: Any) -> str:
    if current_doc == patched_doc:
        return "none"
    if _semantic_sanitize(current_doc) == _semantic_sanitize(patched_doc):
        return "editorial"

    current_invariants = []
    patched_invariants = []
    try:
        current_root = next(iter(current_doc.values()))
        patched_root = next(iter(patched_doc.values()))
        if isinstance(current_root, dict):
            current_invariants = current_root.get("invariants", []) or []
        if isinstance(patched_root, dict):
            patched_invariants = patched_root.get("invariants", []) or []
    except Exception:
        pass

    if current_invariants != patched_invariants:
        return "major"
    return "minor"


def _parse_version(raw: str) -> tuple[int, int, int]:
    parts = raw.split(".")
    if len(parts) != 3:
        raise ValueError(f"Version invalide: {raw}")
    return tuple(int(part) for part in parts)


def _format_version(parts: tuple[int, int, int]) -> str:
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


def _bump_version(raw: str, depth: str) -> str:
    major, minor, patch = _parse_version(raw)
    if depth == "none":
        return raw
    if depth == "editorial":
        return _format_version((major, minor, patch + 1))
    if depth == "minor":
        return _format_version((major, minor + 1, 0))
    return _format_version((major + 1, 0, 0))


def _artifact_major_minor_token(version: str) -> str:
    major, minor, _patch = _parse_version(version)
    return f"V{major}_{minor}"


def _target_artifact_id(current_artifact_id: str, patched_artifact_id: str, current_version: str, target_version: str) -> str:
    if patched_artifact_id and patched_artifact_id != current_artifact_id:
        return patched_artifact_id
    if not current_artifact_id:
        return patched_artifact_id or current_artifact_id

    current_token = _artifact_major_minor_token(current_version)
    target_token = _artifact_major_minor_token(target_version)
    if current_token == target_token:
        return current_artifact_id

    needle = f"_{current_token}"
    replacement = f"_{target_token}"
    if needle in current_artifact_id:
        return current_artifact_id.replace(needle, replacement, 1)
    return current_artifact_id


def _build_release_id(releases_root: Path) -> str:
    today = datetime.now(timezone.utc)
    prefix = f"PLATFORM_FACTORY_RELEASE_{today.year:04d}_{today.month:02d}_{today.day:02d}_R"
    max_n = 0
    if releases_root.exists():
        for child in releases_root.iterdir():
            if not child.is_dir():
                continue
            match = RELEASE_ID_PATTERN.match(child.name)
            if match and child.name.startswith(prefix):
                max_n = max(max_n, int(match.group(4)))
    return f"{prefix}{max_n + 1:02d}"


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "Usage: python build_platform_factory_release_plan.py <patched_dir> <current_dir> <core_validation.yaml> <execution_report.yaml> <release_plan.yaml>",
            file=sys.stderr,
        )
        return 2

    patched_dir = Path(argv[1])
    current_dir = Path(argv[2])
    core_validation_path = Path(argv[3])
    execution_report_path = Path(argv[4])
    output_path = Path(argv[5])

    anomalies: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    for required in [patched_dir, current_dir, core_validation_path, execution_report_path]:
        if not required.exists():
            anomalies.append(f"Entrée requise introuvable: {_repo_path(required)}")

    current_docs: dict[str, Any] = {}
    patched_docs: dict[str, Any] = {}
    compared_against_current: list[dict[str, Any]] = []
    target_versions: list[dict[str, Any]] = []
    required_renames: list[dict[str, Any]] = []
    required_reference_updates: list[dict[str, Any]] = []
    release_bundle_files: list[str] = []
    validated_inputs: list[str] = []
    change_depths: list[str] = []

    if not anomalies:
        try:
            core_validation_doc = _load_yaml(core_validation_path)
            execution_doc = _load_yaml(execution_report_path)
        except Exception as exc:
            anomalies.append(f"Impossible de charger les reports Stage 06/05: {exc}")
        else:
            core_validation = core_validation_doc.get(CORE_VALIDATION_ROOT, {})
            execution = execution_doc.get(EXECUTION_ROOT, {})
            if not isinstance(core_validation, dict):
                anomalies.append(f"Racine `{CORE_VALIDATION_ROOT}` absente ou invalide dans {_repo_path(core_validation_path)}.")
            elif core_validation.get("status") != "PASS":
                anomalies.append(
                    f"Le Stage 07 exige `status: PASS` dans {_repo_path(core_validation_path)}; reçu `{core_validation.get('status')}`."
                )
            else:
                validated_inputs.append(_repo_path(core_validation_path))

            if not isinstance(execution, dict):
                anomalies.append(f"Racine `{EXECUTION_ROOT}` absente ou invalide dans {_repo_path(execution_report_path)}.")
            elif execution.get("status") != "PASS":
                anomalies.append(
                    f"Le Stage 07 exige `status: PASS` dans {_repo_path(execution_report_path)}; reçu `{execution.get('status')}`."
                )
            else:
                validated_inputs.append(_repo_path(execution_report_path))

    if not anomalies:
        for artifact in ARTIFACTS:
            patched_path = patched_dir / artifact["filename"]
            current_path = current_dir / artifact["filename"]

            if not patched_path.exists():
                anomalies.append(f"Artefact patché introuvable: {_repo_path(patched_path)}")
                continue
            if not current_path.exists():
                anomalies.append(f"Artefact current introuvable: {_repo_path(current_path)}")
                continue

            try:
                patched_doc = _load_yaml(patched_path)
                current_doc = _load_yaml(current_path)
            except Exception as exc:
                anomalies.append(f"Impossible de charger {artifact['filename']}: {exc}")
                continue

            patched_root = patched_doc.get(artifact["root_key"]) if isinstance(patched_doc, dict) else None
            current_root = current_doc.get(artifact["root_key"]) if isinstance(current_doc, dict) else None
            if not isinstance(patched_root, dict):
                anomalies.append(
                    f"Racine `{artifact['root_key']}` absente ou invalide dans {_repo_path(patched_path)}."
                )
                continue
            if not isinstance(current_root, dict):
                anomalies.append(
                    f"Racine `{artifact['root_key']}` absente ou invalide dans {_repo_path(current_path)}."
                )
                continue

            patched_meta = patched_root.get("metadata")
            current_meta = current_root.get("metadata")
            if not isinstance(patched_meta, dict):
                anomalies.append(f"Bloc metadata absent ou invalide dans {_repo_path(patched_path)}.")
                continue
            if not isinstance(current_meta, dict):
                anomalies.append(f"Bloc metadata absent ou invalide dans {_repo_path(current_path)}.")
                continue

            if patched_meta.get("artifact_type") != artifact["metadata_type"]:
                anomalies.append(
                    f"`{artifact['filename']}` patché doit déclarer metadata.artifact_type=`{artifact['metadata_type']}`."
                )
                continue
            if current_meta.get("artifact_type") != artifact["metadata_type"]:
                anomalies.append(
                    f"`{artifact['filename']}` current doit déclarer metadata.artifact_type=`{artifact['metadata_type']}`."
                )
                continue

            current_docs[artifact["role"]] = current_doc
            patched_docs[artifact["role"]] = patched_doc
            validated_inputs.extend([_repo_path(patched_path), _repo_path(current_path)])

            content_hash_current = _sha256_of_yaml(current_doc)
            content_hash_patched = _sha256_of_yaml(patched_doc)
            identical = current_doc == patched_doc
            depth = _compare_change_depth(current_doc, patched_doc)
            change_depths.append(depth)

            artifact_id_current = str(current_meta.get("artifact_id", "") or "")
            artifact_id_patched = str(patched_meta.get("artifact_id", artifact_id_current) or artifact_id_current)
            version_current = str(current_meta.get("version", "0.0.0") or "0.0.0")
            version_target = _bump_version(version_current, depth)
            artifact_id_target = _target_artifact_id(
                artifact_id_current,
                artifact_id_patched,
                version_current,
                version_target,
            )

            if depth in {"minor", "major"} and artifact_id_target == artifact_id_current:
                warnings.append(
                    f"{artifact['role']}: version cible `{version_target}` calculée sans renommage déterministe de `artifact_id`."
                )

            compared_against_current.append(
                {
                    "role": artifact["role"],
                    "current_path": _repo_path(current_path),
                    "patched_path": _repo_path(patched_path),
                    "content_identical": identical,
                    "change_depth": depth,
                    "current_sha256": content_hash_current,
                    "patched_sha256": content_hash_patched,
                    "current_artifact_id": artifact_id_current,
                    "patched_artifact_id": artifact_id_patched,
                    "target_artifact_id": artifact_id_target,
                    "current_version": version_current,
                    "target_version": version_target,
                }
            )
            target_versions.append(
                {
                    "role": artifact["role"],
                    "from_artifact_id": artifact_id_current,
                    "to_artifact_id": artifact_id_target,
                    "from_version": version_current,
                    "to_version": version_target,
                }
            )

            if artifact_id_current != artifact_id_target:
                required_renames.append(
                    {
                        "role": artifact["role"],
                        "field": "metadata.artifact_id",
                        "from": artifact_id_current,
                        "to": artifact_id_target,
                    }
                )
            if version_target != version_current:
                required_reference_updates.append(
                    {
                        "role": artifact["role"],
                        "field": "metadata.version",
                        "from": version_current,
                        "to": version_target,
                    }
                )

            notes.append(
                f"{artifact['role']}: identical={str(identical).lower()}, change_depth={depth}, "
                f"artifact_id={artifact_id_current or 'none'}->{artifact_id_target or 'none'}, "
                f"version={version_current}->{version_target}"
            )

    global_depth = "none"
    if "major" in change_depths:
        global_depth = "major"
    elif "minor" in change_depths:
        global_depth = "minor"
    elif "editorial" in change_depths:
        global_depth = "editorial"

    release_required = global_depth != "none" and not anomalies
    promotion_candidate = release_required and not anomalies

    releases_root = Path("docs/cores/releases")
    release_id = _build_release_id(releases_root) if release_required else "none"
    release_path = f"docs/cores/releases/{release_id}/" if release_required else "none"

    if release_required:
        release_bundle_files = [
            f"docs/cores/releases/{release_id}/platform_factory_architecture.yaml",
            f"docs/cores/releases/{release_id}/platform_factory_state.yaml",
            f"docs/cores/releases/{release_id}/manifest.yaml",
        ]
    elif not anomalies:
        notes.append("Aucun changement détecté nécessitant une nouvelle release Platform Factory.")

    output = {
        "RELEASE_PLAN": {
            "status": "FAIL" if anomalies else "PASS",
            "release_required": release_required,
            "change_depth": global_depth,
            "validated_inputs": _unique_preserve_order(validated_inputs),
            "compared_against_current": compared_against_current,
            "target_versions": target_versions,
            "required_renames": required_renames or ["none"],
            "required_reference_updates": required_reference_updates or ["none"],
            "release_bundle": {
                "release_id": release_id,
                "release_path": release_path,
                "promotion_candidate": promotion_candidate,
                "files": release_bundle_files or ["none"],
            },
            "warnings_count": len(warnings),
            "warnings": warnings or ["none"],
            "notes": notes or ["none"],
            "anomalies": anomalies or ["none"],
        }
    }

    _save_yaml(output_path, output)
    return 0 if not anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
