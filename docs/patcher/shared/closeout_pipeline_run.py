#!/usr/bin/env python3
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


PROMOTION_REPORT_ROOT = "PROMOTION_REPORT"
CURRENT_MANIFEST_ROOT = "CURRENT_CORESET"
DEFAULT_CLOSEOUT_REPORT_PATH = "docs/pipelines/constitution/reports/closeout_report.yaml"
DEFAULT_FINAL_SUMMARY_PATH = "docs/pipelines/constitution/outputs/final_run_summary.md"
DEFAULT_ARCHIVE_ROOT = "docs/pipelines/constitution/archive"
DEFAULT_WORK_ROOT = "docs/pipelines/constitution/work"
DEFAULT_REPORTS_ROOT = "docs/pipelines/constitution/reports"
DEFAULT_OUTPUTS_ROOT = "docs/pipelines/constitution/outputs"
DEFAULT_GOVERNANCE_BACKLOG_PATH = "docs/pipelines/constitution/scope_catalog/governance_backlog.yaml"
_GOVERNANCE_BACKLOG_CANDIDATES_ROOT = "governance_backlog_candidates"

# ---------------------------------------------------------------------------
# Backlog entry type inference from note content (legacy fallback)
# ---------------------------------------------------------------------------
# Pattern: C\d+ — <description>
# Heuristics to classify the entry type from note text.
_TYPE_KEYWORDS: List[Tuple[str, str]] = [
    ("hors scope", "scope_gap"),
    ("hors p\u00e9rim\u00e8tre", "scope_gap"),
    ("d\u00e9pendance non couverte", "scope_gap"),
    ("missing_ids", "scope_gap"),
    ("\u00e9tendre", "scope_extension_needed"),
    ("extension", "scope_extension_needed"),
    ("\u00e9largir", "scope_extension_needed"),
    ("orphelin", "orphan_id"),
    ("orphan", "orphan_id"),
    ("non rattach\u00e9", "orphan_id"),
    ("conflit", "policy_conflict"),
    ("contradiction", "policy_conflict"),
    ("angle mort", "partition_angle_mort"),
    ("zone non couverte", "partition_angle_mort"),
]


def infer_entry_type(description: str) -> str:
    low = description.lower()
    for keyword, entry_type in _TYPE_KEYWORDS:
        if keyword in low:
            return entry_type
    return "scope_gap"  # default fallback


# ---------------------------------------------------------------------------
# Backlog note extraction from arbitrage report
# ---------------------------------------------------------------------------

# Legacy fallback matches lines like: **C05** — description
# or: - C05 — description
# or: C05 : description
_NOTE_RE = re.compile(
    r"(?:\*{1,2})?C(\d{2,3})(?:\*{1,2})?\s*[\u2014\-:]+\s*(.+)",
    re.IGNORECASE,
)

# Preferred structured block:
# ```yaml
# governance_backlog_candidates:
#   - candidate_id: ...
#     backlog_entry_type: ...
#     ...
# ```
_YAML_FENCE_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL)


def extract_structured_backlog_candidates(arbitrage_path: Path) -> List[Dict[str, Any]]:
    if not arbitrage_path.exists():
        return []

    text = arbitrage_path.read_text(encoding="utf-8")
    candidates: List[Dict[str, Any]] = []
    for match in _YAML_FENCE_RE.finditer(text):
        block = match.group(1)
        try:
            parsed = yaml.safe_load(block) or {}
        except Exception:
            continue
        if not isinstance(parsed, dict):
            continue
        raw_candidates = parsed.get(_GOVERNANCE_BACKLOG_CANDIDATES_ROOT)
        if not isinstance(raw_candidates, list):
            continue
        for candidate in raw_candidates:
            if isinstance(candidate, dict):
                candidates.append(candidate)
    return candidates


def extract_backlog_notes_from_arbitrage(
    arbitrage_path: Path,
) -> List[Dict[str, str]]:
    """Extract governance notes (Cxx pattern) from arbitrage report.

    Legacy fallback kept for backward compatibility.
    Returns list of dicts with keys: note_id, description.
    """
    if not arbitrage_path.exists():
        return []

    notes: List[Dict[str, str]] = []
    seen: set = set()
    text = arbitrage_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = _NOTE_RE.search(line)
        if m:
            note_id = f"C{m.group(1).zfill(2)}"
            description = m.group(2).strip().rstrip(".")
            if note_id not in seen:
                notes.append({"note_id": note_id, "description": description})
                seen.add(note_id)
    return notes


# ---------------------------------------------------------------------------
# Backlog YAML read/write
# ---------------------------------------------------------------------------

def load_governance_backlog(backlog_path: Path) -> Dict[str, Any]:
    if not backlog_path.exists():
        return {
            "governance_backlog": {
                "schema_version": "0.1",
                "entries": [],
            }
        }
    with open(backlog_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    if "governance_backlog" not in doc:
        doc["governance_backlog"] = {"schema_version": "0.1", "entries": []}
    if "entries" not in doc["governance_backlog"]:
        doc["governance_backlog"]["entries"] = []
    return doc


def save_governance_backlog(backlog_path: Path, doc: Dict[str, Any]) -> None:
    backlog_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backlog_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False)


def build_entry_id(run_id: str, suffix: str) -> str:
    normalized_run_id = run_id.replace("CONSTITUTION_RUN_", "").replace("-", "_")
    normalized_suffix = re.sub(r"[^A-Za-z0-9_]+", "_", suffix).strip("_")
    return f"GB_{normalized_run_id}_{normalized_suffix}"


def normalize_scope_keys(value: Any, fallback_scope_key: str) -> List[str]:
    if isinstance(value, list):
        keys = [str(v).strip() for v in value if str(v).strip()]
        return keys or [fallback_scope_key]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return [fallback_scope_key]


def normalize_candidate_entry(
    candidate: Dict[str, Any],
    run_id: str,
    fallback_scope_key: str,
    current_stage: str,
) -> Dict[str, Any]:
    candidate_id = str(candidate.get("candidate_id") or "CANDIDATE").strip()
    entry_id = build_entry_id(run_id, candidate_id)
    return {
        "entry_id": entry_id,
        "type": str(candidate.get("backlog_entry_type") or "scope_gap"),
        "status": "open",
        "source_run_id": run_id,
        "source_stage": current_stage,
        "scope_key": fallback_scope_key,
        "related_scope_keys": normalize_scope_keys(candidate.get("related_scope_keys"), fallback_scope_key),
        "candidate_id": candidate_id,
        "source_finding_id": str(candidate.get("source_finding_id") or "unknown"),
        "title": str(candidate.get("title") or candidate_id),
        "description": str(candidate.get("rationale") or candidate.get("title") or candidate_id),
        "recommended_action": str(candidate.get("recommended_stage00_action") or "review_at_stage_00"),
        "candidate_status": str(candidate.get("candidate_status") or "candidate_open"),
        "recorded_at": utc_now_iso(),
    }


def export_backlog_entries(
    run_id: str,
    scope_key: str,
    arbitrage_path: Path,
    backlog_path: Path,
    current_stage: str,
) -> List[Dict[str, Any]]:
    """Export governance backlog entries from arbitrage report.

    Preferred mode: extract a structured YAML fenced block rooted at
    governance_backlog_candidates.
    Legacy fallback: extract Cxx notes and infer entry types heuristically.

    Skips entries whose entry_id already exists (idempotent).
    Returns the list of newly added entries.
    """
    structured_candidates = extract_structured_backlog_candidates(arbitrage_path)
    legacy_notes = extract_backlog_notes_from_arbitrage(arbitrage_path) if not structured_candidates else []
    if not structured_candidates and not legacy_notes:
        return []

    doc = load_governance_backlog(backlog_path)
    entries: List[Dict[str, Any]] = doc["governance_backlog"]["entries"]
    existing_ids = {e.get("entry_id") for e in entries}

    added: List[Dict[str, Any]] = []

    if structured_candidates:
        for candidate in structured_candidates:
            entry = normalize_candidate_entry(
                candidate=candidate,
                run_id=run_id,
                fallback_scope_key=scope_key,
                current_stage=current_stage,
            )
            if entry["entry_id"] in existing_ids:
                continue
            entries.append(entry)
            added.append(entry)
    else:
        for note in legacy_notes:
            entry_id = build_entry_id(run_id, note["note_id"])
            if entry_id in existing_ids:
                continue
            entry: Dict[str, Any] = {
                "entry_id": entry_id,
                "type": infer_entry_type(note["description"]),
                "status": "open",
                "source_run_id": run_id,
                "source_stage": current_stage,
                "scope_key": scope_key,
                "note_ref": note["note_id"],
                "description": note["description"],
                "recommended_action": "review_at_stage_00",
                "recorded_at": utc_now_iso(),
            }
            entries.append(entry)
            added.append(entry)

    if added:
        save_governance_backlog(backlog_path, doc)

    return added


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Archive helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Report / summary builders
# ---------------------------------------------------------------------------

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
    backlog_entries_exported: Optional[int] = None,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {
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
    if backlog_entries_exported is not None:
        report["CLOSEOUT_REPORT"]["governance_backlog_entries_exported"] = backlog_entries_exported
    return report


def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    work_reset: bool,
    backlog_entries_exported: Optional[int] = None,
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
    ]
    if backlog_entries_exported is not None:
        lines.append(f"- Governance backlog entries exported: `{backlog_entries_exported}`")
    lines.extend([
        "",
        "## Active cores",
        "",
    ])

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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Close out a constitution pipeline run."
    )
    parser.add_argument("promotion_report", help="Path to promotion_report.yaml")
    parser.add_argument("current_manifest", help="Path to current_manifest.yaml (CURRENT_CORESET)")
    parser.add_argument("--closeout-report", default=DEFAULT_CLOSEOUT_REPORT_PATH)
    parser.add_argument("--final-summary", default=DEFAULT_FINAL_SUMMARY_PATH)
    parser.add_argument("--archive-root", default=DEFAULT_ARCHIVE_ROOT)
    parser.add_argument(
        "--export-backlog-entries",
        action="store_true",
        help=(
            "Export governance backlog entries from the run's arbitrage report. "
            "Preferred input: a structured YAML fenced block rooted at governance_backlog_candidates. "
            "Legacy fallback: Cxx notes."
        ),
    )
    parser.add_argument(
        "--arbitrage-path",
        default=None,
        help="Path to arbitrage report (default: docs/pipelines/constitution/work/arbitrage.md)",
    )
    parser.add_argument(
        "--backlog-path",
        default=DEFAULT_GOVERNANCE_BACKLOG_PATH,
        help=f"Path to governance_backlog.yaml (default: {DEFAULT_GOVERNANCE_BACKLOG_PATH})",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Run ID for backlog entry source annotation (read from promotion_report if absent)",
    )
    parser.add_argument(
        "--scope-key",
        default=None,
        help="Scope key for backlog entry annotation (read from promotion_report if absent)",
    )
    parser.add_argument(
        "--current-stage",
        default="STAGE_09",
        help="Current stage label for backlog entry source annotation (default: STAGE_09)",
    )
    args = parser.parse_args()

    closeout_report_path = Path(args.closeout_report)
    final_summary_path = Path(args.final_summary)
    archive_root = Path(args.archive_root)
    work_root = Path(DEFAULT_WORK_ROOT)
    reports_root = Path(DEFAULT_REPORTS_ROOT)
    outputs_root = Path(DEFAULT_OUTPUTS_ROOT)

    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"
    archive_path = "unknown"
    backlog_entries_exported: Optional[int] = None

    try:
        promotion_report = read_rooted_yaml(Path(args.promotion_report), PROMOTION_REPORT_ROOT)
        current_manifest = read_rooted_yaml(Path(args.current_manifest), CURRENT_MANIFEST_ROOT)

        checked = validate_promotion_and_current(promotion_report, current_manifest)
        release_id = checked["release_id"]
        source_release_path = checked["source_release_path"]
        promotion_mode = checked["promotion_mode"]
        current_cores = checked["current_cores"]

        # Resolve run_id / scope_key for backlog annotation
        run_id_for_backlog = args.run_id or promotion_report.get("run_id") or release_id
        scope_key_for_backlog = args.scope_key or promotion_report.get("scope_key") or "unknown"

        # --export-backlog-entries : extract entries from arbitrage report
        if args.export_backlog_entries:
            arbitrage_path = Path(
                args.arbitrage_path
                if args.arbitrage_path
                else f"{DEFAULT_WORK_ROOT}/arbitrage.md"
            )
            backlog_path = Path(args.backlog_path)
            added = export_backlog_entries(
                run_id=run_id_for_backlog,
                scope_key=scope_key_for_backlog,
                arbitrage_path=arbitrage_path,
                backlog_path=backlog_path,
                current_stage=args.current_stage,
            )
            backlog_entries_exported = len(added)
            if added:
                print(f"[backlog] {backlog_entries_exported} entrée(s) exportée(s) vers {args.backlog_path}:")
                for e in added:
                    title = e.get("title") or e.get("description") or e.get("entry_id")
                    print(f"  + {e['entry_id']} [{e['type']}] — {str(title)[:80]}")
            else:
                print("[backlog] Aucune nouvelle entrée à exporter (aucun candidat structuré, aucune note legacy, ou déjà présentes).")

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
            backlog_entries_exported=backlog_entries_exported,
        )
        preliminary_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            work_reset=False,
            backlog_entries_exported=backlog_entries_exported,
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
        if backlog_entries_exported is not None:
            final_notes.append(
                f"{backlog_entries_exported} entrée(s) de gouvernance exportée(s) vers governance_backlog.yaml"
            )

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
            backlog_entries_exported=backlog_entries_exported,
        )
        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            work_reset=work_reset,
            backlog_entries_exported=backlog_entries_exported,
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
