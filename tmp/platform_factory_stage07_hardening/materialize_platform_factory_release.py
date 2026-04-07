#!/usr/bin/env python3
"""Materialize a Platform Factory release from a Stage 07 release plan.

Usage:
    python docs/patcher/shared/materialize_platform_factory_release.py \
      ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
      ./docs/pipelines/platform_factory/work/05_apply/patched \
      ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
      ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

RELEASE_PLAN_ROOT = "RELEASE_PLAN"
ARTIFACT_FILENAMES = ["platform_factory_architecture.yaml", "platform_factory_state.yaml"]


def _repo_path(value: Any) -> str:
    return str(value).replace("\\", "/")


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def _save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _set_nested_value(document: Any, dotted_path: str, value: Any) -> bool:
    keys = dotted_path.split(".")
    current = document
    for key in keys[:-1]:
        if not isinstance(current, dict):
            return False
        if key not in current or current[key] is None:
            current[key] = {}
        if not isinstance(current[key], dict):
            return False
        current = current[key]
    if not isinstance(current, dict):
        return False
    current[keys[-1]] = value
    return True


def _artifact_lines(artifacts: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for artifact in artifacts:
        lines.append(
            f"- `{artifact.get('role')}` → `{artifact.get('artifact_id')}` / `{artifact.get('version')}` "
            f"(sha256 `{artifact.get('sha256')}`)"
        )
    return lines


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "Usage: python materialize_platform_factory_release.py <release_plan.yaml> <patched_dir> <report.yaml> <release_candidate_notes.md>",
            file=sys.stderr,
        )
        return 2

    release_plan_path = Path(argv[1])
    patched_dir = Path(argv[2])
    report_path = Path(argv[3])
    release_notes_path = Path(argv[4])

    anomalies: list[str] = []
    warnings: list[str] = []
    files_written: list[str] = []
    release_dir_created = False

    if not release_plan_path.exists():
        anomalies.append(f"Release plan introuvable: {_repo_path(release_plan_path)}")
    if not patched_dir.exists():
        anomalies.append(f"Répertoire patched introuvable: {_repo_path(patched_dir)}")

    release_required = False
    release_id = "none"
    release_path = "none"
    release_dir = Path("docs/cores/releases")
    promotion_candidate = False
    target_versions: list[Any] = []
    reference_updates: list[Any] = []
    change_depth = "none"
    notes_from_plan: list[str] = []

    try:
        if not anomalies:
            plan_doc = _load_yaml(release_plan_path)
            plan = plan_doc.get(RELEASE_PLAN_ROOT, {})
            if not isinstance(plan, dict):
                anomalies.append(f"Racine `{RELEASE_PLAN_ROOT}` absente ou invalide dans {_repo_path(release_plan_path)}.")
            else:
                status = plan.get("status")
                if status != "PASS":
                    anomalies.append(f"Le release plan doit être en `PASS` dans {_repo_path(release_plan_path)}; reçu `{status}`.")

                release_required = bool(plan.get("release_required"))
                change_depth = str(plan.get("change_depth", "none"))
                bundle = plan.get("release_bundle", {}) if isinstance(plan.get("release_bundle"), dict) else {}
                release_id = str(bundle.get("release_id", "none"))
                release_path = str(bundle.get("release_path", "none"))
                promotion_candidate = bool(bundle.get("promotion_candidate"))
                notes_from_plan = plan.get("notes", []) if isinstance(plan.get("notes"), list) else []
                target_versions = plan.get("target_versions", []) if isinstance(plan.get("target_versions"), list) else []
                reference_updates = plan.get("required_reference_updates", []) if isinstance(plan.get("required_reference_updates"), list) else []

                if reference_updates == ["none"]:
                    reference_updates = []
                if target_versions == ["none"]:
                    target_versions = []

                if release_required:
                    if release_id == "none" or release_path == "none":
                        anomalies.append("Le release plan exige une release mais ne déclare pas correctement `release_id`/`release_path`.")
                    else:
                        release_dir = Path(release_path.rstrip("/"))
                        if release_dir.exists():
                            anomalies.append(f"Le répertoire de release existe déjà: {_repo_path(release_dir)}")
                else:
                    release_dir = Path("docs/cores/releases")

        if not anomalies and not release_required:
            notes_text = "\n".join(
                [
                    "# Platform Factory Release Candidate",
                    "",
                    "- release_required: `false`",
                    f"- release_plan: `{_repo_path(release_plan_path)}`",
                    f"- change_depth: `{change_depth}`",
                    "",
                    "## Statut",
                    "",
                    "Aucune nouvelle release matérialisée : le calcul déterministe de Stage 07A n'a détecté aucun changement nécessitant une release.",
                    "",
                ]
            )
            _save_text(release_notes_path, notes_text)
            files_written.append(_repo_path(release_notes_path))

        if not anomalies and release_required:
            release_dir.mkdir(parents=True, exist_ok=False)
            release_dir_created = True

            role_to_target = {
                item.get("role"): item
                for item in target_versions
                if isinstance(item, dict) and isinstance(item.get("role"), str)
            }
            role_by_filename = {
                "platform_factory_architecture.yaml": "platform_factory_architecture",
                "platform_factory_state.yaml": "platform_factory_state",
            }

            artifact_records: list[dict[str, Any]] = []

            for filename in ARTIFACT_FILENAMES:
                source_path = patched_dir / filename
                if not source_path.exists():
                    anomalies.append(f"Artefact patché introuvable pour matérialisation: {_repo_path(source_path)}")
                    continue

                document = _load_yaml(source_path)
                if not isinstance(document, dict):
                    anomalies.append(f"Document YAML invalide pour la release: {_repo_path(source_path)}")
                    continue

                root_key = next(iter(document.keys()), None)
                if root_key is None or not isinstance(document.get(root_key), dict):
                    anomalies.append(f"Document YAML invalide pour la release: {_repo_path(source_path)}")
                    continue

                metadata = document[root_key].get("metadata")
                if not isinstance(metadata, dict):
                    anomalies.append(f"Bloc metadata introuvable dans {_repo_path(source_path)}")
                    continue

                role = role_by_filename[filename]
                target = role_to_target.get(role, {})
                to_artifact_id = target.get("to_artifact_id")
                to_version = target.get("to_version")

                if isinstance(to_artifact_id, str) and to_artifact_id:
                    metadata["artifact_id"] = to_artifact_id
                if isinstance(to_version, str) and to_version:
                    metadata["version"] = to_version
                metadata["status"] = "RELEASE_CANDIDATE"

                for update in reference_updates:
                    if not isinstance(update, dict):
                        continue
                    if update.get("role") != role:
                        continue
                    field = update.get("field")
                    value = update.get("to")
                    if isinstance(field, str) and field:
                        _set_nested_value(document[root_key], field, value)

                destination = release_dir / filename
                _save_yaml(destination, document)
                files_written.append(_repo_path(destination))

                artifact_records.append(
                    {
                        "role": role,
                        "file": filename,
                        "root_key": root_key,
                        "artifact_id": metadata.get("artifact_id"),
                        "version": metadata.get("version"),
                        "status": metadata.get("status"),
                        "sha256": _sha256_of_file(destination),
                    }
                )

            if anomalies:
                raise RuntimeError("Échec de matérialisation Platform Factory.")

            manifest = {
                "PLATFORM_FACTORY_RELEASE_MANIFEST": {
                    "release_id": release_id,
                    "release_path": f"{_repo_path(release_dir)}/",
                    "status": "RELEASE_CANDIDATE",
                    "promotion_candidate": promotion_candidate,
                    "change_depth": change_depth,
                    "materialized_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                    "source_release_plan": _repo_path(release_plan_path),
                    "artifacts": artifact_records,
                    "files": [
                        f"{_repo_path(release_dir)}/platform_factory_architecture.yaml",
                        f"{_repo_path(release_dir)}/platform_factory_state.yaml",
                        f"{_repo_path(release_dir)}/manifest.yaml",
                    ],
                }
            }
            manifest_path = release_dir / "manifest.yaml"
            _save_yaml(manifest_path, manifest)
            files_written.append(_repo_path(manifest_path))

            notes_lines = [
                "# Platform Factory Release Candidate",
                "",
                f"- release_id: `{release_id}`",
                f"- release_path: `{_repo_path(release_dir)}/`",
                f"- promotion_candidate: `{promotion_candidate}`",
                f"- change_depth: `{change_depth}`",
                "",
                "## Artifacts",
                "",
                *_artifact_lines(artifact_records),
            ]
            if notes_from_plan:
                notes_lines.extend(["", "## Notes", ""])
                notes_lines.extend(f"- {note}" for note in notes_from_plan)
            notes_lines.extend(["", "## Statut", "", "Release matérialisée sans modification de `docs/cores/current/`.", ""])
            _save_text(release_notes_path, "\n".join(notes_lines))
            files_written.append(_repo_path(release_notes_path))

    except Exception as exc:
        anomalies.append(str(exc))
        if release_dir_created and release_required and release_dir.exists():
            shutil.rmtree(release_dir, ignore_errors=True)

    report = {
        "PLATFORM_FACTORY_RELEASE_MATERIALIZATION": {
            "status": "FAIL" if anomalies else "PASS",
            "release_required": release_required,
            "release_id": release_id,
            "release_path": release_path,
            "promotion_candidate": promotion_candidate,
            "release_plan_path": _repo_path(release_plan_path),
            "patched_dir": _repo_path(patched_dir),
            "files_written": files_written or ["none"],
            "anomalies_count": len(anomalies),
            "warnings_count": len(warnings),
            "anomalies": anomalies or ["none"],
            "warnings": warnings or ["none"],
        }
    }
    _save_yaml(report_path, report)
    return 0 if not anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
