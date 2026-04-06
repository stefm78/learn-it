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

import copy
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

RELEASE_PLAN_ROOT = "RELEASE_PLAN"
ARTIFACT_FILENAMES = ["platform_factory_architecture.yaml", "platform_factory_state.yaml"]



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
    current[keys[-1]] = copy.deepcopy(value)
    return True



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

    if not release_plan_path.exists():
        anomalies.append(f"Release plan introuvable: {release_plan_path}")
    if not patched_dir.exists():
        anomalies.append(f"Répertoire patched introuvable: {patched_dir}")

    release_required = False
    release_id = "none"
    release_path = "none"
    release_dir = Path("docs/cores/releases/none")
    promotion_candidate = False

    if not anomalies:
        try:
            plan_doc = _load_yaml(release_plan_path)
        except Exception as exc:
            anomalies.append(f"Impossible de charger le release plan: {exc}")
        else:
            plan = plan_doc.get(RELEASE_PLAN_ROOT, {})
            status = plan.get("status")
            if status == "FAIL":
                anomalies.append(f"Le release plan est en FAIL dans {release_plan_path}.")
            release_required = bool(plan.get("release_required"))
            bundle = plan.get("release_bundle", {}) if isinstance(plan.get("release_bundle"), dict) else {}
            release_id = str(bundle.get("release_id", "none"))
            release_path = str(bundle.get("release_path", "none"))
            promotion_candidate = bool(bundle.get("promotion_candidate"))
            release_dir = Path(release_path.rstrip("/")) if release_required and release_path != "none" else Path("docs/cores/releases")

            if release_required:
                if release_id == "none" or release_path == "none":
                    anomalies.append("Le release plan exige une release mais ne déclare pas correctement `release_id`/`release_path`.")
                if release_dir.exists():
                    anomalies.append(f"Le répertoire de release existe déjà: {release_dir}")
            else:
                warnings.append("Le release plan indique `release_required: false`; aucune nouvelle release ne sera matérialisée.")

            target_versions = plan.get("target_versions", [])
            if target_versions == ["none"]:
                target_versions = []
            reference_updates = plan.get("required_reference_updates", [])
            if reference_updates == ["none"]:
                reference_updates = []

    if not anomalies and release_required:
        release_dir.mkdir(parents=True, exist_ok=False)

        role_to_version = {
            item.get("role"): item.get("to_version")
            for item in target_versions
            if isinstance(item, dict)
        }

        role_by_filename = {
            "platform_factory_architecture.yaml": "platform_factory_architecture",
            "platform_factory_state.yaml": "platform_factory_state",
        }

        for filename in ARTIFACT_FILENAMES:
            source_path = patched_dir / filename
            if not source_path.exists():
                anomalies.append(f"Artefact patché introuvable pour matérialisation: {source_path}")
                continue
            try:
                document = _load_yaml(source_path)
            except Exception as exc:
                anomalies.append(f"Impossible de charger l'artefact patché {source_path}: {exc}")
                continue

            root_key = next(iter(document.keys()), None)
            if root_key is None or not isinstance(document.get(root_key), dict):
                anomalies.append(f"Document YAML invalide pour la release: {source_path}")
                continue

            metadata = document[root_key].get("metadata")
            if not isinstance(metadata, dict):
                anomalies.append(f"Bloc metadata introuvable dans {source_path}")
                continue

            role = role_by_filename[filename]
            to_version = role_to_version.get(role)
            if to_version:
                metadata["version"] = to_version
            metadata["status"] = "RELEASE_CANDIDATE"

            for update in reference_updates:
                if not isinstance(update, dict):
                    continue
                if update.get("role") == role:
                    field = update.get("field")
                    value = update.get("to")
                    if isinstance(field, str):
                        _set_nested_value(document[root_key], field.replace("metadata.", "metadata."), value)

            destination = release_dir / filename
            _save_yaml(destination, document)
            files_written.append(str(destination))

        manifest = {
            "PLATFORM_FACTORY_RELEASE_MANIFEST": {
                "release_id": release_id,
                "release_path": f"{release_dir.as_posix()}/",
                "status": "RELEASE_CANDIDATE",
                "promotion_candidate": promotion_candidate,
                "materialized_at": datetime.now(timezone.utc).isoformat(),
                "files": [
                    f"{release_dir.as_posix()}/platform_factory_architecture.yaml",
                    f"{release_dir.as_posix()}/platform_factory_state.yaml",
                ],
            }
        }
        manifest_path = release_dir / "manifest.yaml"
        _save_yaml(manifest_path, manifest)
        files_written.append(str(manifest_path))

        notes = f"# Platform Factory Release Candidate\n\n- release_id: `{release_id}`\n- release_path: `{release_dir.as_posix()}/`\n- promotion_candidate: `{promotion_candidate}`\n- files:\n  - `{release_dir.as_posix()}/platform_factory_architecture.yaml`\n  - `{release_dir.as_posix()}/platform_factory_state.yaml`\n  - `{release_dir.as_posix()}/manifest.yaml`\n"
        _save_text(release_notes_path, notes)
        files_written.append(str(release_notes_path))

    report = {
        "PLATFORM_FACTORY_RELEASE_MATERIALIZATION": {
            "status": "FAIL" if anomalies else ("WARN" if warnings else "PASS"),
            "release_required": release_required,
            "release_id": release_id,
            "release_path": release_path,
            "promotion_candidate": promotion_candidate,
            "release_plan_path": str(release_plan_path),
            "patched_dir": str(patched_dir),
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
