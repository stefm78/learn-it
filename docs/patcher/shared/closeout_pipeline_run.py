#!/usr/bin/env python3
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


PROMOTION_REPORT_ROOT = "PROMOTION_REPORT"
CURRENT_MANIFEST_ROOT = "CURRENT_CORESET"
DEFAULT_CLOSEOUT_REPORT_PATH = "docs/pipelines/constitution/reports/closeout_report.yaml"
DEFAULT_FINAL_SUMMARY_PATH = "docs/pipelines/constitution/outputs/final_run_summary.md"
DEFAULT_SANDBOX_PATH = "docs/pipelines/constitution/work/05_apply/sandbox"
CANONICAL_ARTIFACTS = [
    "docs/pipelines/constitution/work/01_challenge/",
    "docs/pipelines/constitution/work/02_arbitrage/arbitrage.md",
    "docs/pipelines/constitution/work/03_patch/patchset.yaml",
    "docs/pipelines/constitution/work/04_patch_validation/patch_validation.yaml",
    "docs/pipelines/constitution/reports/patch_execution_report.yaml",
    "docs/pipelines/constitution/work/06_core_validation/core_validation.yaml",
    "docs/pipelines/constitution/work/07_release/release_plan.yaml",
    "docs/pipelines/constitution/reports/release_materialization_report.yaml",
    "docs/pipelines/constitution/reports/promotion_report.yaml",
]
EPHEMERAL_ARTIFACTS = [
    DEFAULT_SANDBOX_PATH,
]


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


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise CloseoutError(f"booléen invalide: {value}")


def ensure_safe_cleanup_path(path: Path) -> Path:
    normalized = Path(repo_path(path))
    expected = Path(DEFAULT_SANDBOX_PATH)
    if normalized != expected:
        raise CloseoutError(
            f"sandbox_path non autorisé pour cleanup: {repo_path(path)} ; attendu: {repo_path(expected)}"
        )
    return normalized


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
        raise CloseoutError(
            "release_id incohérent entre promotion_report et current manifest"
        )
    if current_source_release_path != promotion_source_release_path:
        raise CloseoutError(
            "source_release_path incohérent entre promotion_report et current manifest"
        )
    if not isinstance(current_cores, list) or not current_cores:
        raise CloseoutError("cores absent ou invalide dans current manifest")

    return {
        "release_id": promotion_release_id,
        "source_release_path": promotion_source_release_path,
        "promotion_mode": promotion_mode,
        "current_cores": current_cores,
    }


def cleanup_sandbox(cleanup_enabled: bool, sandbox_path: Path) -> Dict[str, Any]:
    sandbox_path = ensure_safe_cleanup_path(sandbox_path)
    sandbox_repo_path = repo_path(sandbox_path)

    if not cleanup_enabled:
        return {
            "cleanup_enabled": False,
            "cleanup_performed": False,
            "cleaned_paths": [],
            "notes": ["aucun nettoyage technique demandé"],
        }

    if sandbox_path.exists():
        shutil.rmtree(sandbox_path)
        return {
            "cleanup_enabled": True,
            "cleanup_performed": True,
            "cleaned_paths": [sandbox_repo_path],
            "notes": ["sandbox technique supprimée"],
        }

    return {
        "cleanup_enabled": True,
        "cleanup_performed": False,
        "cleaned_paths": [],
        "notes": ["sandbox technique absente ; rien à supprimer"],
    }


def build_closeout_report(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    cleanup_result: Dict[str, Any],
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
            "active_cores": current_cores,
            "canonical_artifacts_retained": CANONICAL_ARTIFACTS,
            "ephemeral_artifacts": EPHEMERAL_ARTIFACTS,
            "cleanup_enabled": cleanup_result["cleanup_enabled"],
            "cleanup_performed": cleanup_result["cleanup_performed"],
            "cleaned_paths": cleanup_result["cleaned_paths"],
            "notes": notes + cleanup_result["notes"],
        }
    }


def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    cleanup_result: Dict[str, Any],
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
            "## Canonical retained artifacts",
            "",
        ]
    )
    for artifact in CANONICAL_ARTIFACTS:
        lines.append(f"- `{artifact}`")

    lines.extend(
        [
            "",
            "## Ephemeral technical artifacts",
            "",
        ]
    )
    for artifact in EPHEMERAL_ARTIFACTS:
        lines.append(f"- `{artifact}`")

    lines.extend(
        [
            "",
            "## Technical cleanup",
            "",
            f"- Cleanup requested: `{cleanup_result['cleanup_enabled']}`",
            f"- Cleanup performed: `{cleanup_result['cleanup_performed']}`",
        ]
    )

    if cleanup_result["cleaned_paths"]:
        lines.append("- Cleaned paths:")
        for path in cleanup_result["cleaned_paths"]:
            lines.append(f"  - `{path}`")
    else:
        lines.append("- Cleaned paths: none")

    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: closeout_pipeline_run.py <promotion_report.yaml> <current_manifest.yaml> [closeout_report.yaml] [final_run_summary.md] [cleanup_sandbox=false] [sandbox_path]"
        )

    promotion_report_path = Path(sys.argv[1])
    current_manifest_path = Path(sys.argv[2])
    closeout_report_path = (
        Path(sys.argv[3]) if len(sys.argv) >= 4 else Path(DEFAULT_CLOSEOUT_REPORT_PATH)
    )
    final_summary_path = (
        Path(sys.argv[4]) if len(sys.argv) >= 5 else Path(DEFAULT_FINAL_SUMMARY_PATH)
    )
    cleanup_enabled = parse_bool(sys.argv[5]) if len(sys.argv) >= 6 else False
    sandbox_path = Path(sys.argv[6]) if len(sys.argv) >= 7 else Path(DEFAULT_SANDBOX_PATH)

    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"

    try:
        promotion_report = read_rooted_yaml(promotion_report_path, PROMOTION_REPORT_ROOT)
        current_manifest = read_rooted_yaml(current_manifest_path, CURRENT_MANIFEST_ROOT)

        checked = validate_promotion_and_current(promotion_report, current_manifest)
        release_id = checked["release_id"]
        source_release_path = checked["source_release_path"]
        promotion_mode = checked["promotion_mode"]
        current_cores = checked["current_cores"]

        cleanup_result = cleanup_sandbox(cleanup_enabled, sandbox_path)
        notes = [
            "run clôturé après promotion active vérifiée",
            "aucune modification des artefacts métiers de release ou de current pendant le closeout",
        ]

        closeout_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            cleanup_result=cleanup_result,
            closeout_status="PASS",
            notes=notes,
        )
        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            cleanup_result=cleanup_result,
        )

        dump_yaml(closeout_report_path, closeout_report)
        write_text(final_summary_path, final_summary)

    except Exception as exc:
        fail_cleanup = {
            "cleanup_enabled": cleanup_enabled,
            "cleanup_performed": False,
            "cleaned_paths": [],
            "notes": [],
        }
        dump_yaml(
            closeout_report_path,
            build_closeout_report(
                release_id=release_id,
                source_release_path=source_release_path,
                promotion_mode=promotion_mode,
                current_cores=[],
                cleanup_result=fail_cleanup,
                closeout_status="FAIL",
                notes=[str(exc)],
            ),
        )
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
