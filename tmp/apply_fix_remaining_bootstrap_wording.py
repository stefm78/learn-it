from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

path = Path("docs/pipelines/constitution/AI_PROTOCOL.yaml")
text = path.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1) entry_actions
# -------------------------------------------------------------------
old_entry_actions = """  entry_actions:
    decision_action_ref: docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml
    materialization_action_ref: docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml
    sequencing_rule: >-
      En no_run_id_mode, l'ouverture d'un nouveau run suit deux actes canoniques distincts :
      d'abord OPEN_NEW_RUN pour résoudre la décision d'entrée sans écriture de tracking,
      puis MATERIALIZE_NEW_RUN pour matérialiser le run via update_run_tracking.py,
      materialize_run_inputs.py, extract_scope_slice.py et build_run_context.py,
      sans démarrer STAGE_01_CHALLENGE.
"""

new_entry_actions = """  entry_actions:
    decision_action_ref: docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml
    materialization_action_ref: docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml
    reconciliation_action_ref: docs/pipelines/constitution/entry_actions/RECONCILE_RUN.action.yaml
    sequencing_rule: >-
      En no_run_id_mode, l'ouverture d'un nouveau run suit deux actes canoniques distincts :
      d'abord OPEN_NEW_RUN pour résoudre la décision d'entrée sans écriture de tracking,
      puis MATERIALIZE_NEW_RUN pour matérialiser le run via update_run_tracking.py,
      materialize_run_inputs.py, extract_scope_slice.py et build_run_context.py,
      sans démarrer STAGE_01_CHALLENGE.
      En run_id_mode, la remise en ligne d'un run existant peut passer par
      RECONCILE_RUN avant toute reprise métier, lorsqu'une réconciliation explicite
      est demandée ou lorsqu'un run doit être revalidé face aux contrats stables actuels.
"""

text = replace_once(text, old_entry_actions, new_entry_actions, "entry_actions")

# -------------------------------------------------------------------
# 2) run_id_mode
# -------------------------------------------------------------------
old_run_id_mode = """  run_id_mode:
    optimal_read_sequence:
      - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_extract.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/neighbor_extract.yaml
    allowed_reads:
      - docs/pipelines/constitution/AI_PROTOCOL.yaml
      - docs/pipelines/constitution/pipeline.md
      - docs/pipelines/constitution/runs/index.yaml
      - docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/impact_bundle.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/integration_gate.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_extract.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/neighbor_extract.yaml
    forbidden_before_run_resolution:
      - any_search
      - compare_commits
      - docs/cores/current/constitution.yaml
      - docs/cores/current/referentiel.yaml
      - docs/cores/current/link.yaml
      - docs/pipelines/constitution/inputs/*
    if_run_exists: resume_existing_run
    if_run_missing: emit_next_best_action_only
    ids_first_rule: >-
      Si run_context.yaml est présent, l'IA DOIT le lire en premier et utiliser
      scope_extract.yaml + neighbor_extract.yaml comme source principale des entrées Core.
      En bootstrap canonique, ces extraits doivent avoir été matériellement produits
      par MATERIALIZE_NEW_RUN avant tout démarrage de STAGE_01_CHALLENGE.
"""

new_run_id_mode = """  run_id_mode:
    optimal_read_sequence:
      - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_extract.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/neighbor_extract.yaml
    allowed_reads:
      - docs/pipelines/constitution/AI_PROTOCOL.yaml
      - docs/pipelines/constitution/pipeline.md
      - docs/pipelines/constitution/runs/index.yaml
      - docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/impact_bundle.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/integration_gate.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/scope_extract.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/neighbor_extract.yaml
    forbidden_before_run_resolution:
      - any_search
      - compare_commits
      - docs/cores/current/constitution.yaml
      - docs/cores/current/referentiel.yaml
      - docs/cores/current/link.yaml
      - docs/pipelines/constitution/inputs/*
    if_run_exists: resume_existing_run
    if_run_exists_and_reconciliation_requested: reconcile_existing_run
    if_run_missing: emit_next_best_action_only
    ids_first_rule: >-
      Si run_context.yaml est présent, l'IA DOIT le lire en premier et utiliser
      scope_extract.yaml + neighbor_extract.yaml comme source principale des entrées Core.
      En bootstrap canonique, ces extraits doivent avoir été matériellement produits
      par MATERIALIZE_NEW_RUN avant tout démarrage de STAGE_01_CHALLENGE.
    reconciliation_rule: >-
      RECONCILE_RUN est une action canonique de remise en ligne par run_id.
      Elle ne rejoue aucun stage métier. Elle répare uniquement les artefacts
      dérivables via leurs scripts propriétaires, calcule le plus long préfixe
      encore justifiable selon les contrats stables actuels, puis tronque le
      run au bon stage de reprise si nécessaire.
"""

text = replace_once(text, old_run_id_mode, new_run_id_mode, "run_id_mode")

# -------------------------------------------------------------------
# 3) reconciliation_mode
# -------------------------------------------------------------------
old_reconciliation_mode = """  reconciliation_mode:
    allowed_reads:
      - docs/pipelines/constitution/AI_PROTOCOL.yaml
      - docs/pipelines/constitution/pipeline.md
      - docs/pipelines/constitution/PIPELINE_MODEL.yaml
      - docs/pipelines/constitution/runs/index.yaml
      - docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/*
      - docs/pipelines/constitution/runs/<run_id>/work/*
      - docs/pipelines/constitution/runs/<run_id>/reports/*
      - docs/pipelines/constitution/runs/<run_id>/outputs/*
    next_step_policy:
      after_reconciliation_success: CONTINUE_ACTIVE_RUN
"""

new_reconciliation_mode = """  reconciliation_mode:
    expected_mode: run_id_mode
    allowed_reads:
      - docs/pipelines/constitution/AI_PROTOCOL.yaml
      - docs/pipelines/constitution/pipeline.md
      - docs/pipelines/constitution/PIPELINE_MODEL.yaml
      - docs/pipelines/constitution/runs/index.yaml
      - docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml
      - docs/pipelines/constitution/runs/<run_id>/run_tracking.yaml
      - docs/pipelines/constitution/runs/<run_id>/inputs/*
      - docs/pipelines/constitution/runs/<run_id>/work/*
      - docs/pipelines/constitution/runs/<run_id>/reports/*
      - docs/pipelines/constitution/runs/<run_id>/outputs/*
      - docs/pipelines/constitution/stages/*
      - docs/patcher/shared/reconcile_run.py
      - docs/patcher/shared/materialize_run_inputs.py
      - docs/patcher/shared/extract_scope_slice.py
      - docs/patcher/shared/build_run_context.py
    next_step_policy:
      after_reconciliation_success: CONTINUE_ACTIVE_RUN
    reconciliation_constraints:
      - bounded_local_run_only_for_initial_version
      - no_business_stage_replay_inside_reconciliation
      - derivable_artifacts_only_may_be_rebuilt_implicitly
      - non_justifiable_downstream_state_must_be_truncated
"""

text = replace_once(text, old_reconciliation_mode, new_reconciliation_mode, "reconciliation_mode")

path.write_text(text, encoding="utf-8")
print("OK: AI_PROTOCOL.yaml mis à jour pour RECONCILE_RUN")