#!/usr/bin/env python3
"""Close out a completed Platform Factory pipeline run.

This script archives the transient run state, writes a closeout report and a final
summary, and recreates an empty work/ directory for the next execution.

Unlike the constitution closeout, this V0 variant does not rely on
`docs/cores/current/manifest.yaml` because Platform Factory promotion currently
tracks provenance through the materialized release and promotion report.

Usage:
    python docs/patcher/shared/closeout_platform_factory_run.py \
      ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml \
      ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml \
      ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md \
      ./docs/pipelines/platform_factory/archive
"""

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

PROMOTION_REPORT_ROOT = "PROMOTION_REPORT"
RELEASE_PLAN_ROOT = "RELEASE_PLAN"
MATERIALIZATION_ROOT = "PLATFORM_FACTORY_RELEASE_MATERIALIZATION"
DEFAULT_CLOSEOUT_REPORT_PATH = "docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml"
DEFAULT_FINAL_SUMMARY_PATH = "docs/pipelines/platform_factory/outputs/platform_factory_summary.md"
DEFAULT_ARCHIVE_ROOT = "docs/pipelines/platform_factory/archive"
DEFAULT_WORK_ROOT = "docs/pipelines/platform_factory/work"
DEFAULT_REPORTS_ROOT = "docs/pipelines/platform_factory/reports"
DEFAULT_OUTPUTS_ROOT = "docs/pipelines/platform_factory/outputs"


class CloseoutError(Exception):
    pass



def repo_path(value: Any) -> str:
    return str(value).replace("\\", "/")



def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)



def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)



def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")



def read_rooted_yaml(path: Path, root_key: str) -> dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or root_key not in doc:
        raise CloseoutError(f"{root_key} absent dans {path}")
    root = doc[root_key]
    if not isinstance(root, dict):
        raise CloseoutError(f"{root_key} invalide dans {path}")
    return root



def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def validate_inputs(
    promotion_report: dict[str, Any],
    release_plan: dict[str, Any],
    materialization_report: dict[str, Any],
) -> dict[str, Any]:
    promotion_status = promotion_report.get("status")
    promotion_mode = promotion_report.get("promotion_mode")
    release_id = promotion_report.get("release_id")
    source_release_path = repo_path(promotion_report.get("source_release_path"))

    if promotion_status != "PASS":
        raise CloseoutError("platform_factory_promotion_report doit être en status PASS")
    if promotion_mode not in {"applied", "already_current"}:
        raise CloseoutError("platform_factory_promotion_report doit être en mode applied ou already_current")
    if not isinstance(release_id, str) or not release_id:
        raise CloseoutError("release_id absent ou invalide dans platform_factory_promotion_report")
    if not isinstance(source_release_path, str) or not source_release_path:
        raise CloseoutError("source_release_path absent ou invalide dans platform_factory_promotion_report")

    plan_status = release_plan.get("status")
    plan_bundle = release_plan.get("release_bundle")
    if plan_status != "PASS":
        raise CloseoutError("platform_factory_release_plan doit être en status PASS")
    if not isinstance(plan_bundle, dict):
        raise CloseoutError("release_bundle absent ou invalide dans platform_factory_release_plan")
    if release_plan.get("release_required") is not True:
        raise CloseoutError("platform_factory_release_plan doit indiquer release_required: true pour un closeout post-promotion")
    if plan_bundle.get("release_id") != release_id:
        raise CloseoutError("release_id incohérent entre promotion_report et release_plan")
    if repo_path(plan_bundle.get("release_path")) != source_release_path:
        raise CloseoutError("release_path incohérent entre promotion_report et release_plan")

    materialization_status = materialization_report.get("status")
    if materialization_status != "PASS":
        raise CloseoutError("platform_factory_release_materialization_report doit être en status PASS")
    if materialization_report.get("release_id") != release_id:
        raise CloseoutError("release_id incohérent entre promotion_report et release_materialization_report")
    if repo_path(materialization_report.get("release_path")) != source_release_path:
        raise CloseoutError("release_path incohérent entre promotion_report et release_materialization_report")

    release_dir = Path(source_release_path.rstrip("/"))
    manifest_path = release_dir / "manifest.yaml"
    if not release_dir.exists():
        raise CloseoutError(f"Répertoire de release introuvable: {repo_path(release_dir)}")
    if not manifest_path.exists():
        raise CloseoutError(f"Manifest de release introuvable: {repo_path(manifest_path)}")

    for filename in ["platform_factory_architecture.yaml", "platform_factory_state.yaml"]:
        if not (release_dir / filename).exists():
            raise CloseoutError(f"Artefact de release introuvable: {repo_path(release_dir / filename)}")

    return {
        "release_id": release_id,
        "source_release_path": source_release_path,
        "promotion_mode": promotion_mode,
        "manifest_path": repo_path(manifest_path),
    }



def copy_tree_if_exists(source: Path, destination: Path) -> list[str]:
    if not source.exists():
        return []
    if source.is_dir():
        shutil.copytree(source, destination)
        archived_paths: list[str] = []
        for path in sorted(destination.rglob("*")):
            archived_paths.append(repo_path(path))
        if not archived_paths:
            archived_paths.append(repo_path(destination))
        return archived_paths
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return [repo_path(destination)]



def archive_run_state(
    release_id: str,
    archive_root: Path,
    work_root: Path,
    reports_root: Path,
    outputs_root: Path,
) -> tuple[str, list[str]]:
    archive_path = archive_root / release_id
    if archive_path.exists():
        raise CloseoutError(f"archive déjà existante pour ce release_id: {repo_path(archive_path)}")
    archive_path.mkdir(parents=True, exist_ok=False)

    archived_paths: list[str] = []
    archived_paths.extend(copy_tree_if_exists(work_root, archive_path / "work"))
    archived_paths.extend(copy_tree_if_exists(reports_root, archive_path / "reports"))
    archived_paths.extend(copy_tree_if_exists(outputs_root, archive_path / "outputs"))
    if not archived_paths:
        archived_paths.append(repo_path(archive_path))
    return repo_path(archive_path), archived_paths



def reset_work_root(work_root: Path) -> bool:
    if work_root.exists():
        shutil.rmtree(work_root)
    work_root.mkdir(parents=True, exist_ok=True)
    return True



def build_closeout_report(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    archive_path: str,
    archived_paths: list[str],
    work_reset: bool,
    closeout_status: str,
    manifest_path: str,
    notes: list[str],
) -> dict[str, Any]:
    return {
        "PLATFORM_FACTORY_CLOSEOUT_REPORT": {
            "status": closeout_status,
            "pipeline_id": "platform_factory",
            "closed_at": utc_now_iso(),
            "run_closed": closeout_status == "PASS",
            "release_id": release_id,
            "source_release_path": source_release_path,
            "promotion_mode": promotion_mode,
            "manifest_path": manifest_path,
            "archive_path": archive_path,
            "archived_paths": archived_paths,
            "work_reset": work_reset,
            "notes": notes,
        }
    }



def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    archive_path: str,
    work_reset: bool,
    manifest_path: str,
) -> str:
    lines = [
        "# Final run summary — platform_factory",
        "",
        "## Final status",
        "",
        "- Pipeline: `platform_factory`",
        "- Status: `closed`",
        f"- Release active: `{release_id}`",
        f"- Source release path: `{source_release_path}`",
        f"- Promotion mode: `{promotion_mode}`",
        f"- Release manifest: `{manifest_path}`",
        f"- Archive path: `{archive_path}`",
        f"- Work reset: `{work_reset}`",
        f"- Closed at: `{utc_now_iso()}`",
        "",
        "## Archived run snapshot",
        "",
        "- Archived directories copied under the release archive:",
        "  - `work/`",
        "  - `reports/`",
        "  - `outputs/`",
        "",
        "## Workspace reset",
        "",
        "- `docs/pipelines/platform_factory/work/` has been recreated empty and is ready for a new run.",
    ]
    return "\n".join(lines) + "\n"



def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: closeout_platform_factory_run.py <promotion_report.yaml> <release_plan.yaml> <release_materialization_report.yaml> [closeout_report.yaml] [final_summary.md] [archive_root]"
        )

    promotion_report_path = Path(sys.argv[1])
    release_plan_path = Path(sys.argv[2])
    materialization_report_path = Path(sys.argv[3])
    closeout_report_path = Path(sys.argv[4]) if len(sys.argv) >= 5 else Path(DEFAULT_CLOSEOUT_REPORT_PATH)
    final_summary_path = Path(sys.argv[5]) if len(sys.argv) >= 6 else Path(DEFAULT_FINAL_SUMMARY_PATH)
    archive_root = Path(sys.argv[6]) if len(sys.argv) >= 7 else Path(DEFAULT_ARCHIVE_ROOT)

    work_root = Path(DEFAULT_WORK_ROOT)
    reports_root = Path(DEFAULT_REPORTS_ROOT)
    outputs_root = Path(DEFAULT_OUTPUTS_ROOT)

    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"
    archive_path = "unknown"
    manifest_path = "unknown"

    try:
        promotion_report = read_rooted_yaml(promotion_report_path, PROMOTION_REPORT_ROOT)
        release_plan = read_rooted_yaml(release_plan_path, RELEASE_PLAN_ROOT)
        materialization_report = read_rooted_yaml(materialization_report_path, MATERIALIZATION_ROOT)

        checked = validate_inputs(promotion_report, release_plan, materialization_report)
        release_id = checked["release_id"]
        source_release_path = checked["source_release_path"]
        promotion_mode = checked["promotion_mode"]
        manifest_path = checked["manifest_path"]

        archive_root.mkdir(parents=True, exist_ok=True)

        preliminary_notes = [
            "run clôturé après promotion active vérifiée",
            "archive complète du run effectuée sous docs/pipelines/platform_factory/archive/<release_id>/",
            "workspace docs/pipelines/platform_factory/work/ réinitialisé pour une nouvelle exécution",
        ]
        preliminary_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            archive_path="pending",
            archived_paths=[],
            work_reset=False,
            closeout_status="PASS",
            manifest_path=manifest_path,
            notes=preliminary_notes,
        )
        preliminary_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            archive_path="pending",
            work_reset=False,
            manifest_path=manifest_path,
        )
        dump_yaml(closeout_report_path, preliminary_report)
        write_text(final_summary_path, preliminary_summary)

        archive_path, archived_paths = archive_run_state(
            release_id=release_id,
            archive_root=archive_root,
            work_root=work_root,
            reports_root=reports_root,
            outputs_root=outputs_root,
        )

        work_reset = reset_work_root(work_root)

        final_notes = [
            "run clôturé après promotion active vérifiée",
            f"run archivé sous {archive_path}",
            "workspace docs/pipelines/platform_factory/work/ réinitialisé pour une nouvelle exécution",
        ]
        closeout_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            archive_path=archive_path,
            archived_paths=archived_paths,
            work_reset=work_reset,
            closeout_status="PASS",
            manifest_path=manifest_path,
            notes=final_notes,
        )
        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            archive_path=archive_path,
            work_reset=work_reset,
            manifest_path=manifest_path,
        )
        dump_yaml(closeout_report_path, closeout_report)
        write_text(final_summary_path, final_summary)

    except Exception as exc:
        dump_yaml(
            closeout_report_path,
            build_closeout_report(
                release_id=release_id,
                source_release_path=source_release_path,
                promotion_mode=promotion_mode,
                archive_path=archive_path,
                archived_paths=[],
                work_reset=False,
                closeout_status="FAIL",
                manifest_path=manifest_path,
                notes=[str(exc)],
            ),
        )
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
