from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

# -------------------------------------------------------------------
# 1) closeout_pipeline_run.py
# -------------------------------------------------------------------
p = Path("docs/patcher/shared/closeout_pipeline_run.py")
text = p.read_text(encoding="utf-8")

text = replace_once(
    text,
    """    parser.add_argument("--archive-root", default=DEFAULT_ARCHIVE_ROOT)
""",
    """    parser.add_argument("--archive-root", default=DEFAULT_ARCHIVE_ROOT)
    parser.add_argument("--work-root", default=DEFAULT_WORK_ROOT)
    parser.add_argument("--reports-root", default=DEFAULT_REPORTS_ROOT)
    parser.add_argument("--outputs-root", default=DEFAULT_OUTPUTS_ROOT)
""",
    "closeout_pipeline_run argparse roots",
)

text = replace_once(
    text,
    """    archive_root = Path(args.archive_root)
    work_root = Path(DEFAULT_WORK_ROOT)
    reports_root = Path(DEFAULT_REPORTS_ROOT)
    outputs_root = Path(DEFAULT_OUTPUTS_ROOT)
""",
    """    archive_root = Path(args.archive_root)
    work_root = Path(args.work_root)
    reports_root = Path(args.reports_root)
    outputs_root = Path(args.outputs_root)
""",
    "closeout_pipeline_run effective roots",
)

p.write_text(text, encoding="utf-8")
print("OK: closeout_pipeline_run.py corrigé")

# -------------------------------------------------------------------
# 2) STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")
text = p.read_text(encoding="utf-8")

old = """  bounded_local_run:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
    close_tracking: >-
"""

new = """  bounded_local_run:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
      --work-root docs/pipelines/constitution/runs/<run_id>/work
      --reports-root docs/pipelines/constitution/runs/<run_id>/reports
      --outputs-root docs/pipelines/constitution/runs/<run_id>/outputs
    close_tracking: >-
"""

text = replace_once(text, old, new, "STAGE_09 bounded_local_run closeout command")

p.write_text(text, encoding="utf-8")
print("OK: STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml corrigé")

print("\\nTerminé.")
print("Fichiers modifiés :")
print("- docs/patcher/shared/closeout_pipeline_run.py")
print("- docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")