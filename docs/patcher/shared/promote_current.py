#!/usr/bin/env python3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


RELEASE_PLAN_ROOT = "RELEASE_PLAN"
MATERIALIZATION_REPORT_ROOT = "RELEASE_MATERIALIZATION_REPORT"
RELEASE_MANIFEST_ROOT = "RELEASE_MANIFEST"
CURRENT_MANIFEST_ROOT = "CURRENT_CORESET"
DEFAULT_REPORT_PATH = "docs/pipelines/constitution/reports/promotion_report.yaml"
ROLE_FILES = {
    "constitution": "constitution.yaml",
    "referentiel": "referentiel.yaml",
    "link": "link.yaml",
}


class PromotionError(Exception):
    pass


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def read_rooted_yaml(path: Path, root_key: str) -> Dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or root_key not in doc:
        raise PromotionError(f"{root_key} absent dans {path}")
    root = doc[root_key]
    if not isinstance(root, dict):
        raise PromotionError(f"{root_key} invalide dans {path}")
    return root


def build_report(
    status: str,
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    files_promoted: List[str],
    current_manifest_updated: bool,
    notes: List[str],
) -> Dict[str, Any]:
    return {
        "PROMOTION_REPORT": {
            "status": status,
            "release_id": release_id,
            "source_release_path": source_release_path,
            "promotion_mode": promotion_mode,
            "files_promoted": files_promoted,
            "current_manifest_updated": current_manifest_updated,
            "notes": notes,
        }
    }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_current_manifest(release_manifest: Dict[str, Any], promotion_mode: str) -> Dict[str, Any]:
    release_id = release_manifest.get("release_id")
    source_release_path = release_manifest.get("source", {}).get("release_path")
    if not isinstance(source_release_path, str) or not source_release_path:
        raise PromotionError("source.release_path absent du release manifest")

    cores = release_manifest.get("cores")
    if not isinstance(cores, list) or not cores:
        raise PromotionError("cores absent ou invalide dans le release manifest")

    return {
        CURRENT_MANIFEST_ROOT: {
            "release_id": release_id,
            "promoted_at": utc_now_iso(),
            "source_release_path": source_release_path,
            "status": "active",
            "promotion_mode": promotion_mode,
            "cores": cores,
        }
    }


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: promote_current.py <release_plan.yaml> <release_materialization_report.yaml> [promotion_report.yaml]"
        )

    plan_path = Path(sys.argv[1])
    materialization_report_path = Path(sys.argv[2])
    promotion_report_path = Path(sys.argv[3]) if len(sys.argv) >= 4 else Path(DEFAULT_REPORT_PATH)

    release_id = "unknown"
    source_release_path = "unknown"

    try:
        release_plan = read_rooted_yaml(plan_path, RELEASE_PLAN_ROOT)
        if release_plan.get("status") != "PASS":
            raise PromotionError("release_plan doit être en status PASS")

        materialization_report = read_rooted_yaml(materialization_report_path, MATERIALIZATION_REPORT_ROOT)
        if materialization_report.get("status") != "PASS":
            raise PromotionError("release_materialization_report doit être en status PASS")

        release_bundle = release_plan.get("release_bundle")
        if not isinstance(release_bundle, dict):
            raise PromotionError("release_bundle absent ou invalide")

        release_id = release_bundle.get("release_id")
        source_release_path = release_bundle.get("release_path")
        if not isinstance(release_id, str) or not release_id:
            raise PromotionError("release_bundle.release_id absent ou invalide")
        if not isinstance(source_release_path, str) or not source_release_path:
            raise PromotionError("release_bundle.release_path absent ou invalide")

        report_release_id = materialization_report.get("release_id")
        report_release_path = materialization_report.get("release_path")
        if report_release_id != release_id:
            raise PromotionError("release_id incohérent entre release_plan et release_materialization_report")
        if report_release_path != source_release_path:
            raise PromotionError("release_path incohérent entre release_plan et release_materialization_report")

        release_path = Path(source_release_path)
        manifest_path = release_path / "manifest.yaml"
        if not manifest_path.exists():
            raise PromotionError(f"manifest de release absent: {manifest_path}")

        for file_name in list(ROLE_FILES.values()):
            role_path = release_path / file_name
            if not role_path.exists():
                raise PromotionError(f"fichier de release absent: {role_path}")

        release_manifest = read_rooted_yaml(manifest_path, RELEASE_MANIFEST_ROOT)
        if release_manifest.get("status") != "READY":
            raise PromotionError("release manifest doit être en status READY")
        if release_manifest.get("release_id") != release_id:
            raise PromotionError("release_id incohérent entre manifest de release et release_plan")

        promotion = release_manifest.get("promotion", {})
        if isinstance(promotion, dict) and "promotion_candidate" in promotion:
            if promotion.get("promotion_candidate") is False:
                raise PromotionError("release non promotable: promotion_candidate=false")

        release_manifest.setdefault("source", {})
        if not isinstance(release_manifest["source"], dict):
            raise PromotionError("release manifest source invalide")
        release_manifest["source"]["release_path"] = source_release_path

        current_dir = Path("docs/cores/current")
        current_manifest_path = current_dir / "manifest.yaml"

        if current_manifest_path.exists():
            current_manifest = read_rooted_yaml(current_manifest_path, CURRENT_MANIFEST_ROOT)
            current_release_id = current_manifest.get("release_id")
            current_source_release_path = current_manifest.get("source_release_path")
            if current_release_id == release_id and current_source_release_path == source_release_path:
                notes = ["release déjà active dans docs/cores/current/", "aucune réécriture effectuée"]
                dump_yaml(
                    promotion_report_path,
                    build_report(
                        status="PASS",
                        release_id=release_id,
                        source_release_path=source_release_path,
                        promotion_mode="already_current",
                        files_promoted=[],
                        current_manifest_updated=False,
                        notes=notes,
                    ),
                )
                return

        current_dir.mkdir(parents=True, exist_ok=True)
        files_promoted: List[str] = []

        for file_name in ROLE_FILES.values():
            source_file = release_path / file_name
            destination_file = current_dir / file_name
            destination_file.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8")
            files_promoted.append(str(destination_file))

        current_manifest_doc = build_current_manifest(release_manifest, promotion_mode="applied")
        dump_yaml(current_manifest_path, current_manifest_doc)
        files_promoted.append(str(current_manifest_path))

        notes = [
            f"release {release_id} promue vers docs/cores/current/",
            "manifest courant dérivé du manifest de la release promue",
        ]
        dump_yaml(
            promotion_report_path,
            build_report(
                status="PASS",
                release_id=release_id,
                source_release_path=source_release_path,
                promotion_mode="applied",
                files_promoted=files_promoted,
                current_manifest_updated=True,
                notes=notes,
            ),
        )

    except Exception as exc:
        dump_yaml(
            promotion_report_path,
            build_report(
                status="FAIL",
                release_id=release_id,
                source_release_path=source_release_path,
                promotion_mode="failed",
                files_promoted=[],
                current_manifest_updated=False,
                notes=[str(exc)],
            ),
        )
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
