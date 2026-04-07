#!/usr/bin/env python3
"""Promote a materialized Platform Factory release into docs/cores/current.

Usage:
    python docs/patcher/shared/promote_platform_factory_current.py \
      ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

RELEASE_PLAN_ROOT = "RELEASE_PLAN"
MATERIALIZATION_ROOT = "PLATFORM_FACTORY_RELEASE_MATERIALIZATION"
RELEASE_MANIFEST_ROOT = "PLATFORM_FACTORY_RELEASE_MANIFEST"
ARTIFACTS = [
    "platform_factory_architecture.yaml",
    "platform_factory_state.yaml",
]


def _repo_path(value: Any) -> str:
    return str(value).replace("\\", "/")


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_metadata(path: Path) -> tuple[str, dict[str, Any]]:
    document = _load_yaml(path)
    if not isinstance(document, dict):
        raise ValueError(f"Document YAML invalide: {_repo_path(path)}")
    root_key = next(iter(document.keys()), None)
    if root_key is None or not isinstance(document.get(root_key), dict):
        raise ValueError(f"Racine YAML invalide: {_repo_path(path)}")
    metadata = document[root_key].get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"Bloc metadata introuvable: {_repo_path(path)}")
    return root_key, metadata


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "Usage: python promote_platform_factory_current.py <release_plan.yaml> <release_materialization_report.yaml> <promotion_report.yaml>",
            file=sys.stderr,
        )
        return 2

    release_plan_path = Path(argv[1])
    materialization_report_path = Path(argv[2])
    promotion_report_path = Path(argv[3])

    anomalies: list[str] = []
    notes: list[str] = []
    files_promoted: list[str] = []
    promotion_mode = "not_started"
    release_id = "none"
    source_release_path = "none"

    for required in [release_plan_path, materialization_report_path]:
        if not required.exists():
            anomalies.append(f"Entrée requise introuvable: {_repo_path(required)}")

    release_dir = Path("docs/cores/releases")
    current_dir = Path("docs/cores/current")
    manifest_path = Path("docs/cores/releases/none/manifest.yaml")

    if not anomalies:
        try:
            release_plan_doc = _load_yaml(release_plan_path)
            materialization_doc = _load_yaml(materialization_report_path)
        except Exception as exc:
            anomalies.append(f"Impossible de charger les reports Stage 07: {exc}")
        else:
            plan = release_plan_doc.get(RELEASE_PLAN_ROOT, {})
            materialization = materialization_doc.get(MATERIALIZATION_ROOT, {})

            if not isinstance(plan, dict):
                anomalies.append(f"Racine `{RELEASE_PLAN_ROOT}` absente ou invalide dans {_repo_path(release_plan_path)}.")
            if not isinstance(materialization, dict):
                anomalies.append(f"Racine `{MATERIALIZATION_ROOT}` absente ou invalide dans {_repo_path(materialization_report_path)}.")

            if not anomalies:
                if plan.get("status") != "PASS":
                    anomalies.append(
                        f"Le Stage 08 exige `status: PASS` dans {_repo_path(release_plan_path)}; reçu `{plan.get('status')}`."
                    )
                if materialization.get("status") != "PASS":
                    anomalies.append(
                        f"Le Stage 08 exige `status: PASS` dans {_repo_path(materialization_report_path)}; reçu `{materialization.get('status')}`."
                    )

                release_required = bool(plan.get("release_required"))
                if not release_required:
                    anomalies.append("Le release plan indique `release_required: false`; aucune promotion vers current ne doit être effectuée.")

                bundle = plan.get("release_bundle", {}) if isinstance(plan.get("release_bundle"), dict) else {}
                release_id = str(bundle.get("release_id", "none"))
                source_release_path = _repo_path(bundle.get("release_path", "none"))
                if release_id == "none" or source_release_path == "none":
                    anomalies.append("Le release plan ne déclare pas correctement `release_id`/`release_path`.")
                else:
                    release_dir = Path(source_release_path.rstrip("/"))
                    manifest_path = release_dir / "manifest.yaml"

                materialization_release_id = str(materialization.get("release_id", "none"))
                materialization_release_path = _repo_path(materialization.get("release_path", "none"))
                if materialization_release_id != release_id:
                    anomalies.append("Le release_id du report de matérialisation diffère de celui du release plan.")
                if materialization_release_path != source_release_path:
                    anomalies.append("Le release_path du report de matérialisation diffère de celui du release plan.")

    if not anomalies:
        if not release_dir.exists():
            anomalies.append(f"Répertoire de release introuvable: {_repo_path(release_dir)}")
        if not manifest_path.exists():
            anomalies.append(f"Manifest de release introuvable: {_repo_path(manifest_path)}")
        for filename in ARTIFACTS:
            path = release_dir / filename
            if not path.exists():
                anomalies.append(f"Artefact de release introuvable: {_repo_path(path)}")

    release_manifest: dict[str, Any] = {}
    manifest_artifacts: dict[str, dict[str, Any]] = {}
    if not anomalies:
        try:
            release_manifest_doc = _load_yaml(manifest_path)
        except Exception as exc:
            anomalies.append(f"Impossible de charger le manifest de release: {exc}")
        else:
            release_manifest = release_manifest_doc.get(RELEASE_MANIFEST_ROOT, {})
            if not isinstance(release_manifest, dict):
                anomalies.append(f"Racine `{RELEASE_MANIFEST_ROOT}` absente ou invalide dans {_repo_path(manifest_path)}.")
            else:
                if str(release_manifest.get("release_id", "none")) != release_id:
                    anomalies.append("Le manifest de release ne porte pas le bon `release_id`.")
                if not bool(release_manifest.get("promotion_candidate")):
                    anomalies.append("Le manifest de release doit indiquer explicitement `promotion_candidate: true`.")

                raw_artifacts = release_manifest.get("artifacts", [])
                if not isinstance(raw_artifacts, list) or len(raw_artifacts) != len(ARTIFACTS):
                    anomalies.append("Le manifest de release doit contenir une entrée `artifacts` complète pour chaque artefact Platform Factory.")
                else:
                    for item in raw_artifacts:
                        if not isinstance(item, dict):
                            anomalies.append("Le manifest de release contient une entrée `artifacts` invalide.")
                            continue
                        file_name = item.get("file")
                        if not isinstance(file_name, str) or not file_name:
                            anomalies.append("Chaque entrée `artifacts` du manifest doit déclarer `file`.")
                            continue
                        manifest_artifacts[file_name] = item

    if not anomalies:
        for filename in ARTIFACTS:
            release_file = release_dir / filename
            manifest_entry = manifest_artifacts.get(filename)
            if manifest_entry is None:
                anomalies.append(f"Entrée manifest absente pour `{filename}`.")
                continue

            try:
                _root_key, metadata = _artifact_metadata(release_file)
            except Exception as exc:
                anomalies.append(str(exc))
                continue

            manifest_artifact_id = manifest_entry.get("artifact_id")
            manifest_version = manifest_entry.get("version")
            manifest_sha256 = manifest_entry.get("sha256")

            if metadata.get("artifact_id") != manifest_artifact_id:
                anomalies.append(f"`artifact_id` incohérent entre release et manifest pour `{filename}`.")
            if metadata.get("version") != manifest_version:
                anomalies.append(f"`version` incohérente entre release et manifest pour `{filename}`.")
            if _sha256(release_file) != manifest_sha256:
                anomalies.append(f"`sha256` incohérent entre release et manifest pour `{filename}`.")

    if not anomalies:
        current_dir.mkdir(parents=True, exist_ok=True)
        current_matches_release = True
        for filename in ARTIFACTS:
            release_file = release_dir / filename
            current_file = current_dir / filename
            if not current_file.exists():
                current_matches_release = False
                break
            if _sha256(release_file) != _sha256(current_file):
                current_matches_release = False
                break

        if current_matches_release:
            promotion_mode = "already_current"
            notes.append("already_current")
        else:
            for filename in ARTIFACTS:
                release_file = release_dir / filename
                current_file = current_dir / filename
                shutil.copy2(release_file, current_file)
                files_promoted.append(_repo_path(current_file))
            promotion_mode = "applied"
            notes.append("promotion appliquée depuis la release matérialisée")

    report = {
        "PROMOTION_REPORT": {
            "status": "FAIL" if anomalies else "PASS",
            "release_id": release_id,
            "source_release_path": source_release_path,
            "promotion_mode": promotion_mode,
            "files_promoted": files_promoted or ["none"],
            "notes": notes or ["none"],
            "anomalies": anomalies or ["none"],
        }
    }

    _save_yaml(promotion_report_path, report)
    return 0 if not anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
