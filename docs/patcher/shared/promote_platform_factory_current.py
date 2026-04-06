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


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)



def _save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)



def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()



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
    warnings: list[str] = []
    files_promoted: list[str] = []
    promotion_mode = "not_started"
    release_id = "none"
    source_release_path = "none"

    for required in [release_plan_path, materialization_report_path]:
        if not required.exists():
            anomalies.append(f"Entrée requise introuvable: {required}")

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

            if plan.get("status") != "PASS":
                anomalies.append(
                    f"Le Stage 08 exige `status: PASS` dans {release_plan_path}; reçu `{plan.get('status')}`."
                )
            if materialization.get("status") != "PASS":
                anomalies.append(
                    f"Le Stage 08 exige `status: PASS` dans {materialization_report_path}; reçu `{materialization.get('status')}`."
                )

            release_required = bool(plan.get("release_required"))
            if not release_required:
                anomalies.append("Le release plan indique `release_required: false`; aucune promotion vers current ne doit être effectuée.")

            bundle = plan.get("release_bundle", {}) if isinstance(plan.get("release_bundle"), dict) else {}
            release_id = str(bundle.get("release_id", "none"))
            source_release_path = str(bundle.get("release_path", "none"))
            if release_id == "none" or source_release_path == "none":
                anomalies.append("Le release plan ne déclare pas correctement `release_id`/`release_path`.")
            else:
                release_dir = Path(source_release_path.rstrip("/"))
                manifest_path = release_dir / "manifest.yaml"

            if materialization.get("release_id") != release_id:
                warnings.append(
                    "Le release_id du report de matérialisation diffère de celui du release plan."
                )
            if str(materialization.get("release_path", "none")) != source_release_path:
                warnings.append(
                    "Le release_path du report de matérialisation diffère de celui du release plan."
                )

    if not anomalies:
        if not release_dir.exists():
            anomalies.append(f"Répertoire de release introuvable: {release_dir}")
        if not manifest_path.exists():
            anomalies.append(f"Manifest de release introuvable: {manifest_path}")
        for filename in ARTIFACTS:
            path = release_dir / filename
            if not path.exists():
                anomalies.append(f"Artefact de release introuvable: {path}")

    release_manifest: dict[str, Any] = {}
    if not anomalies:
        try:
            release_manifest_doc = _load_yaml(manifest_path)
        except Exception as exc:
            anomalies.append(f"Impossible de charger le manifest de release: {exc}")
        else:
            release_manifest = release_manifest_doc.get(RELEASE_MANIFEST_ROOT, {})
            if str(release_manifest.get("release_id", "none")) != release_id:
                anomalies.append("Le manifest de release ne porte pas le bon `release_id`.")
            if not bool(release_manifest.get("promotion_candidate")):
                warnings.append("Le manifest de release n’indique pas explicitement `promotion_candidate: true`.")

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
        else:
            for filename in ARTIFACTS:
                release_file = release_dir / filename
                current_file = current_dir / filename
                shutil.copy2(release_file, current_file)
                files_promoted.append(str(current_file))
            promotion_mode = "applied"

    report = {
        "PROMOTION_REPORT": {
            "status": "FAIL" if anomalies else ("WARN" if warnings else "PASS"),
            "release_id": release_id,
            "source_release_path": source_release_path,
            "promotion_mode": promotion_mode,
            "files_promoted": files_promoted or ["none"],
            "notes": warnings or ["none"],
            "anomalies": anomalies or ["none"],
        }
    }

    _save_yaml(promotion_report_path, report)
    return 0 if not anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
