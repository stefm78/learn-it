#!/usr/bin/env python3
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


PROMOTION_REPORT_ROOT = "PROMOTION_REPORT"
CURRENT_MANIFEST_ROOT = "CURRENT_CORESET"
DEFAULT_CLOSEOUT_REPORT_PATH = "docs/pipelines/constitution/reports/closeout_report.yaml"
DEFAULT_FINAL_SUMMARY_PATH = "docs/pipelines/constitution/outputs/final_run_summary.md"
DEFAULT_ARCHIVE_ROOT = "docs/pipelines/constitution/archive"
DEFAULT_WORK_ROOT = "docs/pipelines/constitution/work"
DEFAULT_REPORTS_ROOT = "docs/pipelines/constitution/reports"
DEFAULT_OUTPUTS_ROOT = "docs/pipelines/constitution/outputs"


class CloseoutError(Exception):
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
    path.write_text(content, encoding="utf-8")


def read_rooted_yaml(path: Path, root_key: str) -> Dict[str, Any]:
    doc = load_yaml(path)
    if not isinstance(doc, dict) or root_key not in doc:
        raise CloseoutError(f"{root_key} absent dans {path}")
    root = doc[root_key]
    if not isinstance(root, dict):
        raise CloseoutError(f"{root_key} invalide dans {path}")
    return root


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_promotion_and_current(
    promotion_report: Dict[str, Any], current_manifest: Dict[str, Any]
) -> Dict[str, Any]:
    promotion_status = promotion_report.get("status")
    promotion_mode = promotion_report.get("promotion_mode")
    promotion_release_id = promotion_report.get("release_id")
    promotion_source_release_path = repo_path(promotion_report.get("source_release_path"))

    if promotion_status != "PASS":
        raise CloseoutError("promotion_report doit être en status PASS")
    if promotion_mode not in {"applied", "already_current"}:
        raise CloseoutError("promotion_report doit être en mode applied ou already_current")
    if not isinstance(promotion_release_id, str) or not promotion_release_id:
        raise CloseoutError("release_id absent ou invalide dans promotion_report")
    if not isinstance(promotion_source_release_path, str) or not promotion_source_release_path:
        raise CloseoutError("source_release_path absent ou invalide dans promotion_report")

    current_release_id = current_manifest.get("release_id")
    current_source_release_path = repo_path(current_manifest.get("source_release_path"))
    current_status = current_manifest.get("status")
    current_promotion_mode = current_manifest.get("promotion_mode")
    current_cores = current_manifest.get("cores")

    if current_status != "active":
        raise CloseoutError("current manifest doit être en status active")
    if current_promotion_mode not in {"applied", "already_current"}:
        raise CloseoutError("current manifest promotion_mode invalide")
    if current_release_id != promotion_release_id:
        raise CloseoutError("release_id incohérent entre promotion_report et current manifest")
    if current_source_release_path != promotion_source_release_path:
        raise CloseoutError("source_release_path incohérent entre promotion_report et current manifest")
    if not isinstance(current_cores, list) or not current_cores:
        raise CloseoutError("cores absent ou invalide dans current manifest")

    return {
        "release_id": promotion_release_id,
        "source_release_path": promotion_source_release_path,
        "promotion_mode": promotion_mode,
        "current_cores": current_cores,
    }


def copy_tree_if_exists(source: Path, destination: Path) -> List[str]:
    if not source.exists():
        return []

    if source.is_dir():
        shutil.copytree(source, destination)
        archived_paths: List[str] = []
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
) -> Tuple[str, List[str]]:
    archive_path = archive_root / release_id
    if archive_path.exists():
        raise CloseoutError(f"archive déjà existante pour ce release_id: {repo_path(archive_path)}")

    archive_path.mkdir(parents=True, exist_ok=False)

    archived_paths: List[str] = []
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
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    archived_paths: List[str],
    work_reset: bool,
    closeout_status: str,
    notes: List[str],
) -> Dict[str, Any]:
    return {
        "CLOSEOUT_REPORT": {
            "status": closeout_status,
            "pipeline_id": "constitution",
            "closed_at": utc_now_iso(),
            "run_closed": closeout_status == "PASS",
            "release_id": release_id,
            "source_release_path": source_release_path,
            "promotion_mode": promotion_mode,
            "archive_path": archive_path,
            "archived_paths": archived_paths,
            "work_reset": work_reset,
            "active_cores": current_cores,
            "notes": notes,
        }
    }


def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    work_reset: bool,
) -> str:
    lines = [
        "# Final run summary — constitution",
        "",
        "## Final status",
        "",
        "- Pipeline: `constitution`",
        "- Status: `closed`",
        f"- Release active: `{release_id}`",
        f"- Source release path: `{source_release_path}`",
        f"- Promotion mode: `{promotion_mode}`",
        f"- Archive path: `{archive_path}`",
        f"- Work reset: `{work_reset}`",
        f"- Closed at: `{utc_now_iso()}`",
        "",
        "## Active cores",
        "",
    ]

    for entry in current_cores:
        role = entry.get("role", "unknown")
        core_id = entry.get("core_id", "unknown")
        version = entry.get("version", "unknown")
        lines.append(f"- `{role}`: `{core_id}` — `{version}`")

    lines.extend(
        [
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
            "- `docs/pipelines/constitution/work/` has been recreated empty and is ready for a new run.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: closeout_pipeline_run.py <promotion_report.yaml> <current_manifest.yaml> [closeout_report.yaml] [final_run_summary.md] [archive_root]"
        )

    promotion_report_path = Path(sys.argv[1])
    current_manifest_path = Path(sys.argv[2])
    closeout_report_path = (
        Path(sys.argv[3]) if len(sys.argv) >= 4 else Path(DEFAULT_CLOSEOUT_REPORT_PATH)
    )
    final_summary_path = (
        Path(sys.argv[4]) if len(sys.argv) >= 5 else Path(DEFAULT_FINAL_SUMMARY_PATH)
    )
    archive_root = Path(sys.argv[5]) if len(sys.argv) >= 6 else Path(DEFAULT_ARCHIVE_ROOT)

    work_root = Path(DEFAULT_WORK_ROOT)
    reports_root = Path(DEFAULT_REPORTS_ROOT)
    outputs_root = Path(DEFAULT_OUTPUTS_ROOT)

    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"
    archive_path = "unknown"

    try:
        promotion_report = read_rooted_yaml(promotion_report_path, PROMOTION_REPORT_ROOT)
        current_manifest = read_rooted_yaml(current_manifest_path, CURRENT_MANIFEST_ROOT)

        checked = validate_promotion_and_current(promotion_report, current_manifest)
        release_id = checked["release_id"]
        source_release_path = checked["source_release_path"]
        promotion_mode = checked["promotion_mode"]
        current_cores = checked["current_cores"]

        archive_root.mkdir(parents=True, exist_ok=True)

        preliminary_notes = [
            "run clôturé après promotion active vérifiée",
            "archive complète du run effectuée sous docs/pipelines/constitution/archive/<release_id>/",
            "workspace docs/pipelines/constitution/work/ réinitialisé pour une nouvelle exécution",
        ]

        preliminary_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            archived_paths=[],
            work_reset=False,
            closeout_status="PASS",
            notes=preliminary_notes,
        )
        preliminary_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            work_reset=False,
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
            "workspace docs/pipelines/constitution/work/ réinitialisé pour une nouvelle exécution",
        ]
        closeout_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            archived_paths=archived_paths,
            work_reset=work_reset,
            closeout_status="PASS",
            notes=final_notes,
        )
        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            work_reset=work_reset,
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
                current_cores=[],
                archive_path=archive_path,
                archived_paths=[],
                work_reset=False,
                closeout_status="FAIL",
                notes=[str(exc)],
            ),
        )
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
