from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

# -------------------------------------------------------------------
# 1) STAGE_07_RELEASE_MATERIALIZATION.skill.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/stages/STAGE_07_RELEASE_MATERIALIZATION.skill.yaml")
text = p.read_text(encoding="utf-8")

old = """  on_pass:
    step: 1
    label: Mettre à jour le tracking et poursuivre vers STAGE_08_PROMOTE_CURRENT
    mandatory: true
    command: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_07_RELEASE_MATERIALIZATION
      --stage-status done
      --run-status active
      --next-stage STAGE_08_PROMOTE_CURRENT
      --summary "Release materialization completed with validated artifacts; ready for promote current."
"""

new = """  on_pass:
    step: 1
    label: Poursuivre vers STAGE_08_PROMOTE_CURRENT avec action humaine adaptée au mode
    mandatory: true
    command_bounded_local_run: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_07_RELEASE_MATERIALIZATION
      --stage-status done
      --run-status active
      --next-stage STAGE_08_PROMOTE_CURRENT
      --summary "Release materialization completed with validated artifacts; ready for promote current."
    note_pipeline_level_modes: >-
      En modes parallel_consolidation, nominal_global et bounded_transition,
      aucun update_run_tracking.py run-level ne doit être émis ici.
      La suite consiste à démarrer explicitement STAGE_08_PROMOTE_CURRENT
      sur les artefacts pipeline-level matérialisés.
"""

text = replace_once(text, old, new, "STAGE_07 on_pass")

old = """  on_pass:
    next_stage: STAGE_08_PROMOTE_CURRENT
    precondition: human must confirm update_run_tracking.py execution
"""

new = """  on_pass:
    next_stage: STAGE_08_PROMOTE_CURRENT
    precondition: >-
      En bounded_local_run, human must confirm update_run_tracking.py execution.
      En parallel_consolidation, nominal_global et bounded_transition,
      la transition est pipeline-level et ne dépend pas d'un run_id unique.
"""

text = replace_once(text, old, new, "STAGE_07 allowed_transitions on_pass")

p.write_text(text, encoding="utf-8")
print("OK: STAGE_07_RELEASE_MATERIALIZATION.skill.yaml corrigé")

# -------------------------------------------------------------------
# 2) STAGE_08_PROMOTE_CURRENT.skill.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/stages/STAGE_08_PROMOTE_CURRENT.skill.yaml")
text = p.read_text(encoding="utf-8")

old = """  on_pass:
    step: 1
    label: Mettre à jour le tracking et poursuivre vers STAGE_09_CLOSEOUT_AND_ARCHIVE
    mandatory: true
    command: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_08_PROMOTE_CURRENT
      --stage-status done
      --run-status active
      --next-stage STAGE_09_CLOSEOUT_AND_ARCHIVE
      --summary "Promotion to current completed with validated manifests; ready for closeout."
"""

new = """  on_pass:
    step: 1
    label: Poursuivre vers STAGE_09_CLOSEOUT_AND_ARCHIVE avec action humaine adaptée au mode
    mandatory: true
    command_bounded_local_run: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_08_PROMOTE_CURRENT
      --stage-status done
      --run-status active
      --next-stage STAGE_09_CLOSEOUT_AND_ARCHIVE
      --summary "Promotion to current completed with validated manifests; ready for closeout."
    note_pipeline_level_modes: >-
      En modes parallel_consolidation, nominal_global et bounded_transition,
      aucun update_run_tracking.py run-level ne doit être émis ici.
      La suite consiste à démarrer explicitement STAGE_09_CLOSEOUT_AND_ARCHIVE
      sur les artefacts pipeline-level de promotion validés.
"""

text = replace_once(text, old, new, "STAGE_08 on_pass")

old = """  on_pass:
    next_stage: STAGE_09_CLOSEOUT_AND_ARCHIVE
    precondition: human must confirm update_run_tracking.py execution
"""

new = """  on_pass:
    next_stage: STAGE_09_CLOSEOUT_AND_ARCHIVE
    precondition: >-
      En bounded_local_run, human must confirm update_run_tracking.py execution.
      En parallel_consolidation, nominal_global et bounded_transition,
      la transition est pipeline-level et ne dépend pas d'un run_id unique.
"""

text = replace_once(text, old, new, "STAGE_08 allowed_transitions on_pass")

p.write_text(text, encoding="utf-8")
print("OK: STAGE_08_PROMOTE_CURRENT.skill.yaml corrigé")

# -------------------------------------------------------------------
# 3) STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")
text = p.read_text(encoding="utf-8")

text = replace_once(
    text,
    """mission: >-
  Superviser la clôture finale du run après promotion validée, avec
  exécution réelle du script de closeout et vérification de la cohérence
  des artefacts finaux. Ce stage termine le run et archive son état
  opératoire sans réécrire les Core métier eux-mêmes.
""",
    """mission: >-
  Superviser la clôture finale après promotion validée, soit au niveau d'un
  run unique, soit au niveau pipeline-level après consolidation, avec
  exécution réelle du script de closeout et vérification de la cohérence
  des artefacts finaux. Ce stage termine proprement le cycle opératoire
  sans réécrire les Core métier eux-mêmes.
""",
    "STAGE_09 mission",
)

text = replace_once(
    text,
    """  expected_mode_values:
    - bounded_local_run
    - nominal_global
    - bounded_transition
""",
    """  expected_mode_values:
    - bounded_local_run
    - parallel_consolidation
    - nominal_global
    - bounded_transition
""",
    "STAGE_09 expected_mode_values",
)

text = replace_once(
    text,
    """  run_context_role: >-
    En mode bounded_local_run, run_context.yaml doit être lu en premier.
    Il ne remplace pas la preuve d'exécution réelle du closeout.
""",
    """  run_context_role: >-
    En mode bounded_local_run, run_context.yaml doit être lu en premier.
    En mode parallel_consolidation, nominal_global ou bounded_transition,
    les artefacts pipeline-level font autorité.
    Il ne remplace pas la preuve d'exécution réelle du closeout.
""",
    "STAGE_09 run_context_role",
)

text = replace_once(
    text,
    """primary_reads:
  bounded_local_run:
    - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
    - docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
  nominal_global:
    - docs/pipelines/constitution/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
  bounded_transition:
    - docs/pipelines/constitution/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
""",
    """primary_reads:
  bounded_local_run:
    - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
    - docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
  parallel_consolidation:
    - docs/pipelines/constitution/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
  nominal_global:
    - docs/pipelines/constitution/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
  bounded_transition:
    - docs/pipelines/constitution/reports/promotion_report.yaml
    - docs/cores/current/manifest.yaml
""",
    "STAGE_09 primary_reads",
)

text = replace_once(
    text,
    """deterministic_command_templates:
  bounded_local_run:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
    close_tracking: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_09_CLOSEOUT_AND_ARCHIVE
      --stage-status done
      --run-status closed
      --summary "Run closeout completed with archive and final summary; pipeline run is closed."
      --close-run
  nominal_global:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/outputs/final_run_summary.md
  bounded_transition:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/outputs/final_run_summary.md
""",
    """deterministic_command_templates:
  bounded_local_run:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/runs/<run_id>/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
    close_tracking: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_09_CLOSEOUT_AND_ARCHIVE
      --stage-status done
      --run-status closed
      --summary "Run closeout completed with archive and final summary; pipeline run is closed."
      --close-run
  parallel_consolidation:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/outputs/final_run_summary.md
  nominal_global:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/outputs/final_run_summary.md
  bounded_transition:
    closeout: >-
      python docs/patcher/shared/closeout_pipeline_run.py
      docs/pipelines/constitution/reports/promotion_report.yaml
      docs/cores/current/manifest.yaml
      --closeout-report docs/pipelines/constitution/reports/closeout_report.yaml
      --final-summary docs/pipelines/constitution/outputs/final_run_summary.md
""",
    "STAGE_09 deterministic_command_templates",
)

text = replace_once(
    text,
    """expected_outputs:
  bounded_local_run:
    primary_output_path_pattern: docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
  nominal_global:
    primary_output_path_pattern: docs/pipelines/constitution/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/outputs/final_run_summary.md
  bounded_transition:
    primary_output_path_pattern: docs/pipelines/constitution/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/outputs/final_run_summary.md
""",
    """expected_outputs:
  bounded_local_run:
    primary_output_path_pattern: docs/pipelines/constitution/runs/<run_id>/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/runs/<run_id>/outputs/final_run_summary.md
  parallel_consolidation:
    primary_output_path_pattern: docs/pipelines/constitution/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/outputs/final_run_summary.md
  nominal_global:
    primary_output_path_pattern: docs/pipelines/constitution/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/outputs/final_run_summary.md
  bounded_transition:
    primary_output_path_pattern: docs/pipelines/constitution/reports/closeout_report.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/outputs/final_run_summary.md
""",
    "STAGE_09 expected_outputs",
)

old = """  on_pass:
    step: 1
    label: Fermer explicitement le tracking du run
    mandatory: true
    command: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_09_CLOSEOUT_AND_ARCHIVE
      --stage-status done
      --run-status closed
      --summary "Run closeout completed with archive and final summary; pipeline run is closed."
      --close-run
    note: >-
      Aucun stage supplémentaire n'est requis après cette fermeture de tracking.
      Le prochain point d'entrée redevient la résolution d'entrée du pipeline.
"""

new = """  on_pass:
    step: 1
    label: Finaliser la clôture avec action humaine adaptée au mode
    mandatory: true
    command_bounded_local_run: >-
      python docs/patcher/shared/update_run_tracking.py
      --pipeline constitution
      --run-id <RUN_ID>
      --stage-id STAGE_09_CLOSEOUT_AND_ARCHIVE
      --stage-status done
      --run-status closed
      --summary "Run closeout completed with archive and final summary; pipeline run is closed."
      --close-run
    note_pipeline_level_modes: >-
      En modes parallel_consolidation, nominal_global et bounded_transition,
      aucun close tracking run-level n'est requis ici.
      Le closeout pipeline-level est convergent dès que les artefacts de closeout
      sont validés. Le prochain point d'entrée redevient la résolution d'entrée du pipeline.
    note: >-
      Aucun stage supplémentaire n'est requis après cette clôture.
"""

text = replace_once(text, old, new, "STAGE_09 on_pass")

p.write_text(text, encoding="utf-8")
print("OK: STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml corrigé")

# -------------------------------------------------------------------
# 4) PIPELINE_MODEL.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/PIPELINE_MODEL.yaml")
text = p.read_text(encoding="utf-8")

text = replace_once(
    text,
    """  - stage_id: STAGE_09_CLOSEOUT_AND_ARCHIVE
    optional: false
    orchestration_scope: run
""",
    """  - stage_id: STAGE_09_CLOSEOUT_AND_ARCHIVE
    optional: false
    orchestration_scope: run_or_pipeline
""",
    "PIPELINE_MODEL STAGE_09 orchestration_scope",
)

p.write_text(text, encoding="utf-8")
print("OK: PIPELINE_MODEL.yaml corrigé")

print("\\nTerminé.")
print("Fichiers modifiés :")
print("- docs/pipelines/constitution/stages/STAGE_07_RELEASE_MATERIALIZATION.skill.yaml")
print("- docs/pipelines/constitution/stages/STAGE_08_PROMOTE_CURRENT.skill.yaml")
print("- docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")
print("- docs/pipelines/constitution/PIPELINE_MODEL.yaml")