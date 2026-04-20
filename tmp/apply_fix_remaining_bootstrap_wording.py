from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

p = Path("docs/patcher/shared/closeout_pipeline_run.py")
text = p.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1) helper to derive closeout scope from work_root
# -------------------------------------------------------------------
anchor = """def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
"""

replacement = """def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def infer_closeout_scope(work_root: Path) -> str:
    normalized = repo_path(work_root)
    return "run" if "/runs/" in normalized else "pipeline"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
"""

text = replace_once(text, anchor, replacement, "infer_closeout_scope insertion")

# -------------------------------------------------------------------
# 2) build_closeout_report signature + payload
# -------------------------------------------------------------------
text = replace_once(
    text,
    """def build_closeout_report(
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
""",
    """def build_closeout_report(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    archived_paths: List[str],
    work_reset: bool,
    closeout_status: str,
    notes: List[str],
    closeout_scope: str,
    backlog_entries_exported: Optional[int] = None,
) -> Dict[str, Any]:
""",
    "build_closeout_report signature",
)

text = replace_once(
    text,
    """            "status": closeout_status,
            "pipeline_id": "constitution",
            "closed_at": utc_now_iso(),
            "run_closed": closeout_status == "PASS",
""",
    """            "status": closeout_status,
            "pipeline_id": "constitution",
            "closeout_scope": closeout_scope,
            "closed_at": utc_now_iso(),
            "run_closed": closeout_status == "PASS" and closeout_scope == "run",
""",
    "build_closeout_report payload",
)

# -------------------------------------------------------------------
# 3) build_final_summary signature + wording
# -------------------------------------------------------------------
text = replace_once(
    text,
    """def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    work_reset: bool,
    backlog_entries_exported: Optional[int] = None,
) -> str:
""",
    """def build_final_summary(
    release_id: str,
    source_release_path: str,
    promotion_mode: str,
    current_cores: List[Dict[str, Any]],
    archive_path: str,
    work_reset: bool,
    work_root_path: str,
    closeout_scope: str,
    backlog_entries_exported: Optional[int] = None,
) -> str:
""",
    "build_final_summary signature",
)

text = replace_once(
    text,
    """    lines = [
        "# Final run summary — constitution",
""",
    """    lines = [
        "# Final closeout summary — constitution",
""",
    "build_final_summary title",
)

text = replace_once(
    text,
    """        "- Pipeline: `constitution`",
        "- Status: `closed`",
""",
    """        "- Pipeline: `constitution`",
        f"- Closeout scope: `{closeout_scope}`",
        "- Status: `closed`",
""",
    "build_final_summary scope line",
)

text = replace_once(
    text,
    """            "## Archived run snapshot",
""",
    """            "## Archived operational snapshot",
""",
    "build_final_summary archived section title",
)

text = replace_once(
    text,
    """            "- `docs/pipelines/constitution/work/` has been recreated empty and is ready for a new run.",
""",
    """            f"- `{work_root_path}` has been recreated empty and is ready for a new execution cycle.",
""",
    "build_final_summary workspace line",
)

# -------------------------------------------------------------------
# 4) use args.work_root for default arbitrage path
# -------------------------------------------------------------------
text = replace_once(
    text,
    """    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"
    archive_path = "unknown"
    backlog_entries_exported: Optional[int] = None
""",
    """    release_id = "unknown"
    source_release_path = "unknown"
    promotion_mode = "unknown"
    archive_path = "unknown"
    closeout_scope = infer_closeout_scope(work_root)
    backlog_entries_exported: Optional[int] = None
""",
    "main closeout_scope init",
)

text = replace_once(
    text,
    """                if args.arbitrage_path
                else f"{DEFAULT_WORK_ROOT}/arbitrage.md"
""",
    """                if args.arbitrage_path
                else str(work_root / "arbitrage.md")
""",
    "main arbitrage fallback path",
)

# -------------------------------------------------------------------
# 5) neutralize notes + pass closeout_scope/work_root_path
# -------------------------------------------------------------------
text = replace_once(
    text,
    """        preliminary_notes = [
            "run clôturé après promotion active vérifiée",
            "archive complète du run effectuée sous docs/pipelines/constitution/archive/<release_id>/",
            "workspace docs/pipelines/constitution/work/ réinitialisé pour une nouvelle exécution",
        ]
""",
    """        preliminary_notes = [
            "closeout validé après promotion active vérifiée",
            "archive complète de l'état opératoire effectuée sous docs/pipelines/constitution/archive/<release_id>/",
            f"workspace {repo_path(work_root)} réinitialisé pour une nouvelle exécution",
        ]
""",
    "preliminary_notes",
)

text = replace_once(
    text,
    """        preliminary_report = build_closeout_report(
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
""",
    """        preliminary_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            archived_paths=[],
            work_reset=False,
            closeout_status="PASS",
            notes=preliminary_notes,
            closeout_scope=closeout_scope,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    "preliminary_report call",
)

text = replace_once(
    text,
    """        preliminary_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            work_reset=False,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    """        preliminary_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path="pending",
            work_reset=False,
            work_root_path=repo_path(work_root),
            closeout_scope=closeout_scope,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    "preliminary_summary call",
)

text = replace_once(
    text,
    """        final_notes = [
            "run clôturé après promotion active vérifiée",
            f"run archivé sous {archive_path}",
            "workspace docs/pipelines/constitution/work/ réinitialisé pour une nouvelle exécution",
        ]
""",
    """        final_notes = [
            "closeout validé après promotion active vérifiée",
            f"état opératoire archivé sous {archive_path}",
            f"workspace {repo_path(work_root)} réinitialisé pour une nouvelle exécution",
        ]
""",
    "final_notes",
)

text = replace_once(
    text,
    """        closeout_report = build_closeout_report(
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
""",
    """        closeout_report = build_closeout_report(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            archived_paths=archived_paths,
            work_reset=work_reset,
            closeout_status="PASS",
            notes=final_notes,
            closeout_scope=closeout_scope,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    "final_report call",
)

text = replace_once(
    text,
    """        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            work_reset=work_reset,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    """        final_summary = build_final_summary(
            release_id=release_id,
            source_release_path=source_release_path,
            promotion_mode=promotion_mode,
            current_cores=current_cores,
            archive_path=archive_path,
            work_reset=work_reset,
            work_root_path=repo_path(work_root),
            closeout_scope=closeout_scope,
            backlog_entries_exported=backlog_entries_exported,
        )
""",
    "final_summary call",
)

text = replace_once(
    text,
    """        dump_yaml(
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
""",
    """        dump_yaml(
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
                closeout_scope=closeout_scope,
            ),
        )
""",
    "failure closeout_report call",
)

p.write_text(text, encoding="utf-8")
print("OK: closeout_pipeline_run.py corrigé")

print("\\nTerminé.")
print("Fichier modifié :")
print("- docs/patcher/shared/closeout_pipeline_run.py")