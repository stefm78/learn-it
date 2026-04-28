# Scope graph clustering progress tracker

Status: active tracker  
Related approach: `docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md`  
Related clarification: `docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md`  
Related maturity scoring spec: `docs/specs/constitution_scope_maturity_scoring.md`  
Pipeline: `constitution`  
Branch: `feat/core-modularization-bootstrap`

## Purpose

Synthetic progress tracker for the scope graph clustering approach.

The full method is described in `SCOPE_GRAPH_CLUSTERING_APPROACH.md`.

This tracker reflects the current Scope Lab execution state after:

- graph extraction;
- cluster detection;
- closure analysis;
- scope alignment review;
- redesign candidate generation;
- human arbitration;
- policy/decisions patching;
- deterministic scope catalog regeneration;
- ID-level bijection validation;
- successful patch_lifecycle bounded pilot run;
- canonical export of pilot governance backlog entries;
- post-scoping maturity scoring governance design.

## Current phase

```yaml
current_phase:
  phase_id: PHASE_16
  label: constitution_neighbor_ids_governance
  status: active
  summary: >-
    PHASE_16 governs explicit Constitution-to-Constitution neighbor IDs surfaced by
    maturity scoring V1.1. The generic mechanism is now wired into STAGE_00 through
    a non-mutating governance report, arbitration preparation, and arbitration validation.
    Human arbitration of the current candidates remains pending before any decisions.yaml
    patch. The decisions patcher is intentionally deferred until validation reaches
    PASS_READY_TO_PATCH.
```


## Phase tracker

```yaml
phases:
  - phase_id: PHASE_00
    label: approach_definition
    status: done
    outputs:
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md

  - phase_id: PHASE_01
    label: disposable_run_cleanup
    status: deferred_not_blocking
    objective: Stop, abandon, or purge disposable test runs so they do not constrain scoping redesign.
    note: >-
      Current active/test runs are considered disposable for the purpose of this
      scoping redesign. Cleanup remains useful but did not block Scope Lab progress.

  - phase_id: PHASE_02
    label: scope_lab_workspace
    status: done
    objective: Create tmp/scope_lab/ for experimental graph outputs.
    outputs:
      - tmp/scope_lab/

  - phase_id: PHASE_03
    label: full_graph_extraction
    status: done
    objective: Extract graph nodes and edges from constitution, referentiel, and link.
    outputs:
      - tmp/analyze_constitution_dependency_graph.py
      - tmp/scope_lab/constitution_graph_nodes.yaml
      - tmp/scope_lab/constitution_graph_edges.yaml
      - tmp/scope_lab/constitution_graph_report.yaml
    result:
      status: PASS
      node_count: 246
      edge_count: 402
      missing_target_edge_count: 0
      duplicate_node_id_count: 0

  - phase_id: PHASE_04
    label: natural_cluster_detection
    status: done
    objective: Detect deterministic, explainable graph clusters.
    outputs:
      - tmp/detect_constitution_graph_clusters.py
      - tmp/scope_lab/constitution_graph_clusters.yaml
      - tmp/scope_lab/constitution_graph_clusters_report.yaml
    result:
      status: PASS
      weak_component_count: 34
      label_cluster_count: 56
      largest_weak_component_size: 195
      largest_label_cluster_size: 26

  - phase_id: PHASE_05
    label: cluster_closure_analysis
    status: done
    objective: Classify internal edges, external neighbor edges, bridge edges, missing targets, candidate nodes, and candidate edges.
    outputs:
      - tmp/analyze_cluster_closure.py
      - tmp/scope_lab/cluster_closure_report.yaml
    result:
      status: PASS
      selected_cluster_count: 28
      high_priority_cluster_count: 27

  - phase_id: PHASE_06
    label: scope_alignment_review
    status: done
    objective: Compare graph clusters with current canonical scopes.
    outputs:
      - tmp/analyze_scope_alignment.py
      - tmp/scope_lab/scope_alignment_report.yaml
    result:
      status: PASS
      scope_count: 5
      selected_cluster_count: 28
      alignment_status_counts:
        split_merge_or_bridge_review: 5

  - phase_id: PHASE_07
    label: redesign_candidates
    status: done
    objective: Produce explicit scoping redesign candidates for human arbitration.
    outputs:
      - tmp/generate_scope_redesign_candidates.py
      - tmp/scope_lab/scope_redesign_candidates.yaml
    result:
      status: PASS
      candidate_count: 34
      priority_counts:
        high: 27
        medium: 7

  - phase_id: PHASE_08
    label: human_arbitration
    status: partially_done
    objective: Resolve each candidate as accepted, rejected, deferred, or backlog.
    outputs:
      - tmp/generate_scope_redesign_arbitration.py
      - tmp/scope_lab/scope_redesign_arbitration.yaml
      - tmp/apply_scope_arbitration_decisions.py
      - tmp/scope_lab/scope_redesign_arbitration_summary.md
    accepted_macro_decisions:
      - MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION
      - MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE
      - MACRO_003_PATCH_TRIGGER_BOUNDARY
      - MACRO_006_SCOPE_BOUNDARY_REVIEW
    pending_macro_decisions:
      - MACRO_004_MULTI_OWNER_CLUSTER_REVIEW
      - MACRO_005_NEIGHBOR_DECLARATION_REVIEW

  - phase_id: PHASE_09
    label: canonical_patch
    status: done
    objective: Apply accepted changes to canonical scope generation inputs.
    outputs:
      - tmp/scope_lab/phase_09_canonicalization_plan.yaml
      - tmp/apply_phase_09_policy_decisions_patch.py
      - docs/pipelines/constitution/policies/scope_generation/policy.yaml
      - docs/pipelines/constitution/policies/scope_generation/decisions.yaml
      - docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md
    result:
      policy_updated: true
      decisions_updated: true
      canonical_cores_modified: false
      generated_catalog_modified_directly: false

  - phase_id: PHASE_10
    label: scope_catalog_regeneration
    status: done
    objective: Regenerate the scope catalog deterministically.
    outputs:
      - docs/patcher/shared/generate_constitution_scopes.py
      - tmp/constitution_scope_generation_report.yaml
      - docs/pipelines/constitution/scope_catalog/manifest.yaml
      - docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml
    result:
      status: PASS
      apply_mode: true
      generated_scope_count: 5

  - phase_id: PHASE_11
    label: bijection_and_reconstruction_validation
    status: done
    objective: Validate ownership bijection and full structural reconstruction of constitution, referentiel, and link.
    outputs:
      - tmp/validate_scope_partition_bijection.py
      - tmp/fix_phase11_bijection_inputs.py
      - tmp/scope_partition_bijection_validation.yaml
    result:
      id_level_bijection_status: PASS
      ownership_bijection_status: PASS
      external_read_only_classification_status: PASS
      neighbor_validation_status: PASS
      reconstruction_readiness_status: PASS
      full_structural_reconstruction_status: PASS
    note: >-
      The ID-level validator proves partition readiness. Full normalized
      structural reconstruction is validated separately in PHASE_11B.

  - phase_id: PHASE_11B
    label: full_structural_reconstruction_validation
    status: done
    objective: Validate normalized structural reconstruction of constitution, referentiel, and link from a content-carrying partition or scope extracts.
    outputs:
      - tmp/validate_scope_partition_reconstruction.py
      - tmp/scope_partition_reconstruction_validation.yaml
    result:
      status: PASS
      validation_mode: normalized_structural_reconstruction
      blocking_findings: []
      constitution_reconstruction_mode: owned_scope_partition_plus_constitution_intercore_references
      referentiel_reconstruction_mode: external_read_only_passthrough
      link_reconstruction_mode: external_read_only_passthrough

  - phase_id: PHASE_12
    label: extract_validation
    status: done
    objective: Validate scope_extract.yaml and neighbor_extract.yaml on a synthetic or pilot patch_lifecycle run.
    outputs:
      - tmp/run_phase12_extract_validation.py
      - tmp/scope_extract_validation_report.yaml
      - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01/inputs/scope_manifest.yaml
      - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01/inputs/impact_bundle.yaml
      - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01/inputs/integration_gate.yaml
      - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01/inputs/scope_extract.yaml
      - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_EXTRACT_VALIDATION_R01/inputs/neighbor_extract.yaml
    result:
      status: PASS
      validation_target: synthetic_patch_lifecycle_run
      scope_extract:
        target_count: 22
        found_count: 22
        missing_count: 0
      neighbor_extract:
        target_count: 1
        found_count: 1
        missing_count: 0
      integration_gate:
        status: open
        gate_check_count: 6
      blocking_findings: []

  - phase_id: PHASE_13
    label: pilot_bounded_local_run
    status: done
    objective: Open, execute, promote, close, and archive one serious pilot bounded_local_run after all scoping gates pass.
    recommended_scope: patch_lifecycle
    run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    result:
      status: PASS
      run_status: closed
      final_stage: STAGE_09_CLOSEOUT_AND_ARCHIVE
      release_id: CORE_RELEASE_2026_04_28_R01
      promoted_to_current: true
      active_constitution_core_id: CORE_LEARNIT_CONSTITUTION_V5_0
      active_constitution_version: V5_0_FINAL
      promotion_report: docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01/reports/promotion_report.yaml
      current_manifest: docs/cores/current/manifest.yaml
      governance_backlog_exported: true
      governance_backlog_path: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
      exported_governance_backlog_count: 6
      blocking_findings: []
    preconditions:
      - PHASE_09 policy/decisions patch passed
      - PHASE_10 scope catalog regeneration passed
      - PHASE_11 ID-level bijection passed
      - PHASE_11B normalized structural reconstruction passed
      - PHASE_12 synthetic extract validation passed

  - phase_id: PHASE_14
    label: governance_backlog_pipeline_integration
    status: done
    objective: >-
      Complete the generic Constitution pipeline integration of governance backlog entries
      generated during runs, by ensuring that they are produced in STAGE_02, exported in
      STAGE_09, stored in governance_backlog.yaml, consumed in STAGE_00, and surfaced by
      launcher / entry resolution before new runs are opened.
    scope: pipeline_generic
    canonical_backlog:
      path: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
      role: inter_run_source_of_truth
    completed_subtasks:
      - subtask_id: PHASE_14A_STAGE02_CANDIDATE_GENERATION
        status: done
        evidence:
          - docs/pipelines/constitution/stages/STAGE_02_ARBITRAGE.skill.yaml
        summary: >-
          STAGE_02 serializes governance_backlog_candidates locally in arbitrage*.md
          and never writes governance_backlog.yaml directly.
      - subtask_id: PHASE_14B_STAGE09_CANONICAL_EXPORT
        status: done
        evidence:
          - docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml
          - docs/patcher/shared/closeout_pipeline_run.py
        summary: >-
          STAGE_09 exports candidates canonically, supports multiple arbitrage*.md files,
          and preserves source_arbitrage_path.
      - subtask_id: PHASE_14C_STAGE00_BACKLOG_CONSUMPTION
        status: done
        evidence:
          - docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
          - docs/pipelines/constitution/reports/governance_backlog_stage00_consumption_audit.yaml
        summary: >-
          STAGE_00 already declares governance_backlog.yaml as a required input,
          requires reading and filtering open entries before semantic partition analysis,
          blocks completion while open entries are unresolved or unjustified, and requires
          resolution metadata. The audit is scoped to backlog consumption only and explicitly
          excludes maturity scoring.
      - subtask_id: PHASE_14D_DETERMINISTIC_BACKLOG_REPORT
        status: done
        evidence:
          - docs/patcher/shared/report_governance_backlog.py
          - docs/pipelines/constitution/reports/governance_backlog_report.yaml
        summary: >-
          A deterministic read-only report now summarizes governance backlog entries by
          status, type, scope, related scope, source run, candidate status, Stage 00
          relevance, and launcher-facing impacted scopes.
      - subtask_id: PHASE_14E_LAUNCHER_BACKLOG_WARNING
        status: done
        evidence:
          - tmp/pipeline_launcher.py
          - docs/pipelines/constitution/reports/governance_backlog_report.yaml
        summary: >-
          The experimental launcher now reads the canonical governance backlog,
          computes open backlog warnings by impacted scope, annotates published scopes
          and active runs with governance_backlog_signal, and propagates the signal into
          OPEN_NEW_RUN entry action prompt bindings.
      - subtask_id: PHASE_14F_BACKLOG_STATUS_LIFECYCLE
        status: done
        evidence:
          - docs/specs/constitution_governance_backlog_lifecycle.md
          - docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
          - docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
          - docs/patcher/shared/validate_governance_backlog_lifecycle.py
          - docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml
        summary: >-
          The backlog lifecycle is now explicit: canonical statuses are open,
          addressed and wont_fix. Deferred/reporté is not a status; deferred entries
          remain open with atomic review metadata. A deterministic validator verifies
          status values, resolution metadata, unique entry IDs, known entry types and
          open review metadata consistency.
    pending_subtasks: []
    related_reference_artifacts:
      - docs/transformations/core_modularization/POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md
    note: >-
      The post-pilot patch_lifecycle triage report remains a non-canonical example /
      analysis artifact. PHASE_14 itself is now generic pipeline integration work,
      not a pilot-specific triage phase.

  - phase_id: PHASE_15
    label: scope_maturity_post_scoping_governance
    status: active
    objective: >-
      Implement the deterministic post-scoping maturity scoring report introduced
      by docs/specs/constitution_scope_maturity_scoring.md and integrated into
      STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md.
    governance_position:
      published_authority: docs/pipelines/constitution/policies/scope_generation/policy.yaml
      computed_report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      mutation_policy: diagnostic_report_only_no_policy_rewrite
    completed_design_outputs:
      - docs/specs/constitution_scope_maturity_scoring.md
      - docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
    completed_implementation_outputs:
      - docs/patcher/shared/score_constitution_scope_maturity.py
      - docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      - docs/pipelines/constitution/reports/scope_maturity_scoring_calibration_report.md
    result:
      first_report_status: FAIL
      first_report_computed_lower_than_published_count: 4
      first_report_computed_delta_non_blocking_count: 1
      calibration_report_created: true
      calibration_report_status: calibration_required
      v1_1_candidate_applied: true
      v1_1_report_status: FAIL
      v1_1_scope_count: 5
      v1_1_computed_lower_than_published_count: 2
      v1_1_computed_delta_non_blocking_count: 1
      v1_1_remaining_blocking_scopes:
        - deployment_governance
        - learner_state
      v1_1_non_blocking_delta_scopes:
        - patch_lifecycle
      v1_1_aligned_scopes:
        - knowledge_and_design
        - mastery_evaluation
      v1_1_accepted_as_current_diagnostic_baseline: true
      neighbor_ids_governance_required: true
      publication_authority_unchanged: true
      calibration_decisions:
        keep_policy_authority: accepted
        keep_dependency_explicitness_strict: accepted
        adjust_internal_coherence: accepted_in_v1_1
        split_stability_score_and_confidence: accepted_in_v1_1
        stop_scorer_calibration_loop: accepted
        open_neighbor_ids_governance_follow_up: accepted
    pending_outputs:
      - neighbor_ids governance decision report for Constitution-to-Constitution dependencies
      - optional scope_generation policy/decisions updates after human arbitration
      - rerun scope maturity scoring report after explicit neighbor declarations are governed
    note: >-
      PHASE_15 V1.1 is accepted as the current diagnostic baseline. The remaining
      FAIL status is no longer treated as scorer over-severity by default. It is a
      governance signal that explicit Constitution neighbor IDs are under-declared
      for some scopes. policy.yaml remains authoritative until a future governed
      authority migration.

  - phase_id: PHASE_16
    label: constitution_neighbor_ids_governance
    status: active
    objective: >-
      Govern explicit Constitution-to-Constitution neighbor IDs surfaced by the
      maturity scoring V1.1 diagnostic baseline, without merging this content-specific
      arbitration into PHASE_14 governance_backlog_pipeline_integration.
    source_signal:
      phase: PHASE_15
      report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      signal: constitution_neighbor_ids_under_declared
    governance_position:
      phase14_relationship: >-
        Related through STAGE_00, but distinct from the generic governance backlog
        mechanism. PHASE_14 governs backlog plumbing; PHASE_16 governs the specific
        neighbor_ids content revealed by scoring.
      policy_authority: docs/pipelines/constitution/policies/scope_generation/policy.yaml
      mutation_policy: >-
        Do not change published maturity scores. Update policy.yaml / decisions.yaml
        only after human arbitration of explicit neighbor IDs.
    planned_inputs:
      - docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      - docs/pipelines/constitution/policies/scope_generation/policy.yaml
      - docs/pipelines/constitution/policies/scope_generation/decisions.yaml
      - docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
    planned_outputs:
      - neighbor_ids governance decision report
      - optional governance_backlog entries for deferred neighbor IDs
      - optional scope_generation policy/decisions updates after human arbitration
      - regenerated scope catalog only if policy/decisions change
      - rerun scope maturity scoring report after explicit neighbor declarations are governed
    decision_values:
      - add_as_default_neighbor
      - defer_to_governance_backlog
      - wont_fix_with_rationale
    constraints:
      - do_not_absorb_into_phase14
      - do_not_change_published_maturity_scores_in_this_phase
      - do_not_change_scorer_v1_1_rules
      - update_scope_generation_policy_only_after_human_arbitration
      - regenerate_scope_catalog_only_if_policy_decisions_change
    policy_domain_review:
      status: done
      reviewed_domains:
        - docs/pipelines/constitution/policies/scope_generation/
        - docs/pipelines/constitution/policies/integration/
        - docs/pipelines/constitution/policies/canonical_rebuild/
      conclusion: >-
        scope_generation is the correct policy domain for published scope maturity
        and explicit Constitution neighbor IDs. integration governs local-run results
        into integrated changesets. canonical_rebuild governs deterministic rebuild
        from integrated structured inputs. No migration of neighbor ID governance to
        integration or canonical_rebuild is required at this point.
      scope_generation_role:
        published_maturity_authority: docs/pipelines/constitution/policies/scope_generation/policy.yaml
        neighbor_ids_authority: docs/pipelines/constitution/policies/scope_generation/decisions.yaml
        neighbor_decision_type: force_logical_neighbors
      integration_role:
        status: not_primary_for_neighbor_ids
        rationale: >-
          The integration policy handles run admission, collision resolution,
          integration gates and integrated changeset publication. It does not currently
          own published maturity or explicit neighbor IDs.
      canonical_rebuild_role:
        status: not_primary_for_neighbor_ids
        rationale: >-
          The canonical rebuild policy handles deterministic rebuild rules and
          serialization decisions. It does not currently own published maturity or
          explicit neighbor IDs.
    completed_subtasks:
      - subtask_id: PHASE_16A_NEIGHBOR_IDS_GOVERNANCE_REPORT
        status: done
        evidence:
          - docs/patcher/shared/report_constitution_neighbor_ids_governance.py
          - docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
        summary: >-
          A deterministic non-mutating report extracts uncovered Constitution neighbor IDs
          from scope_maturity_scoring_report.yaml, maps each ID to its current owner scope
          using approved assign_ids_to_scope decisions, and proposes a human-arbitrable
          decision value per candidate.
      - subtask_id: PHASE_16B_GENERIC_PIPELINE_MECHANISM
        status: done
        evidence:
          - docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
          - docs/patcher/shared/prepare_constitution_neighbor_ids_arbitration.py
          - docs/patcher/shared/validate_constitution_neighbor_ids_arbitration.py
          - docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml
        summary: >-
          STAGE_00 now documents the generic post-scoring neighbor IDs governance
          sequence: governance report, arbitration preparation, arbitration validation,
          and only after PASS_READY_TO_PATCH an optional decisions.yaml patch followed
          by scope catalog regeneration and scoring rerun. The current validation state
          is PENDING_HUMAN_ARBITRATION, which is valid but not patch-ready.
    pending_subtasks:
      - subtask_id: PHASE_16C_HUMAN_ARBITRATION
        status: pending
        objective: >-
          Decide each candidate as add_as_default_neighbor, defer_to_governance_backlog,
          or wont_fix_with_rationale before any policy/decisions update.
      - subtask_id: PHASE_16D_DECISIONS_PATCHER
        status: deferred
        objective: >-
          Install and use a gated deterministic patcher for decisions.yaml only after
          constitution_neighbor_ids_arbitration_validation.yaml reaches PASS_READY_TO_PATCH.
        expected_script: docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py
        target_policy_domain: docs/pipelines/constitution/policies/scope_generation/
        target_file: docs/pipelines/constitution/policies/scope_generation/decisions.yaml

```

## Implementation checklist

```yaml
implementation_tracking:
  approach_document_created: true
  progress_tracker_created: true
  referentiel_link_treatment_documented: true
  disposable_runs_cleaned_or_abandoned: false
  disposable_runs_marked_non_blocking_for_scope_lab: true
  scope_lab_workspace_created: true
  full_graph_script_created: true
  graph_nodes_edges_generated: true
  cluster_detection_generated: true
  cluster_closure_report_generated: true
  scope_alignment_report_generated: true
  redesign_candidates_generated: true
  human_arbitration_recorded: true
  canonical_core_patches_applied_if_needed: false
  scope_generation_policy_updated: true
  scope_generation_decisions_updated: true
  scope_catalog_regenerated: true
  bijection_validator_created: true
  ownership_bijection_passed: true
  external_read_only_classification_passed: true
  neighbor_validation_passed: true
  id_level_reconstruction_readiness_passed: true
  full_reconstruction_passed: true
  extract_tests_passed: true
  pilot_bounded_local_run_opened: true
  pilot_bounded_local_run_closed: true
  pilot_bounded_local_run_promoted_to_current: true
  pilot_governance_backlog_exported: true
  pilot_governance_backlog_count: 6
  governance_backlog_pipeline_integration_opened: true
  stage00_backlog_consumption_integrated: true
  stage00_backlog_consumption_audit_report_created: true
  governance_backlog_report_script_created: true
  governance_backlog_report_generated: true
  launcher_backlog_warning_integrated: true
  backlog_status_lifecycle_defined: true
  governance_backlog_lifecycle_validator_created: true
  governance_backlog_lifecycle_validation_passed: true
  scope_maturity_scoring_spec_created: true
  stage00_maturity_scoring_integrated: true
  score_constitution_scope_maturity_script_created: true
  scope_maturity_scoring_report_generated: true
  scope_maturity_scoring_report_status: FAIL
  scope_maturity_scoring_calibration_required: true
  scope_maturity_scoring_calibration_report_created: true
  scope_maturity_scoring_v1_1_candidate_required: false
  scorer_v1_1_candidate_applied: true
  scope_maturity_scoring_report_v1_1_status: FAIL
  scope_maturity_scoring_report_v1_1_lower_than_published_count: 2
  scorer_v1_1_accepted_as_current_diagnostic_baseline: true
  neighbor_ids_governance_follow_up_required: true
  phase16_constitution_neighbor_ids_governance_planned: true
  phase16_constitution_neighbor_ids_governance_active: true
  constitution_neighbor_ids_governance_report_created: true
  constitution_neighbor_ids_arbitration_prepared: true
  constitution_neighbor_ids_arbitration_validator_created: true
  constitution_neighbor_ids_arbitration_status: PENDING_HUMAN_ARBITRATION
  constitution_neighbor_ids_decisions_patcher_deferred_until_pass_ready: true
  policy_domain_review_for_scores_and_neighbor_ids_done: true
  published_maturity_authority_unchanged: true
```

## Key decisions recorded

```yaml
decision_log:
  - decision_id: DECISION_001
    date: 2026-04-27
    status: accepted
    decision: Use graph clustering as a diagnostic and validation layer, not as an automatic replacement for human-governed scope partitioning.

  - decision_id: DECISION_002
    date: 2026-04-27
    status: accepted
    decision: Require ownership bijection and full structural reconstruction of constitution, referentiel, and link before opening serious bounded local runs.

  - decision_id: DECISION_003
    date: 2026-04-27
    status: accepted
    decision: Allow candidate nodes and candidate edges in the Scope Lab, but prohibit canonical use until explicitly accepted and patched into canonical cores.

  - decision_id: DECISION_004
    date: 2026-04-27
    status: accepted
    decision: Treat referentiel and link as external_read_only cores for Constitution bounded runs.

  - decision_id: DECISION_005
    date: 2026-04-27
    status: accepted
    decision: Do not redesign all scopes at once; use patch_lifecycle as the first graph-based scoping pilot.

  - decision_id: DECISION_006
    date: 2026-04-27
    status: accepted
    decision: Keep patch_lifecycle structural IDs in patch_lifecycle and record patch_structure_and_quality as a diagnostic subcluster.

  - decision_id: DECISION_007
    date: 2026-04-27
    status: accepted
    decision: Keep governed patch trigger IDs in patch_lifecycle and represent learner_state/runtime signals as explicit read neighbors where needed.

  - decision_id: DECISION_008
    date: 2026-04-28
    status: accepted
    decision: Export STAGE_02 governance backlog candidates canonically to docs/pipelines/constitution/scope_catalog/governance_backlog.yaml during STAGE_09 closeout.

  - decision_id: DECISION_009
    date: 2026-04-28
    status: accepted
    decision: >-
      Treat exported governance backlog entries as inter-run inputs to the generic
      PHASE_14 governance_backlog_pipeline_integration phase, before STAGE_00
      scope partition review, launcher surfacing, or future bounded design runs.
  - decision_id: DECISION_010
    date: 2026-04-28
    status: accepted
    decision: >-
      Introduce deterministic post-scoping maturity scoring as a diagnostic report
      after scope catalog generation, while keeping policy.yaml authoritative for
      published maturity until an explicit future authority migration is governed.

  - decision_id: DECISION_011
    date: 2026-04-28
    status: accepted
    decision: >-
      Treat the first scope_maturity_scoring_report.yaml status FAIL as a
      diagnostic calibration signal, not as an automatic reason to rewrite
      policy.yaml maturity values. The next step is scorer calibration and
      human arbitration of deltas.
  - decision_id: DECISION_012
    date: 2026-04-28
    status: accepted
    decision: >-
      Record the first maturity scoring calibration pass as a documentary
      arbitration input. Dependency explicitness remains a real governance
      signal; internal coherence and inter-release stability require V1.1
      calibration before any maturity authority migration.
  - decision_id: DECISION_013
    date: 2026-04-28
    status: accepted
    decision: >-
      Accept score_constitution_scope_maturity.py V1.1 as the current diagnostic
      baseline. Stop further scorer calibration for now: the remaining FAIL is
      treated as a governance signal about under-declared Constitution neighbor
      IDs, not as an automatic reason to rewrite policy.yaml maturity values.
  - decision_id: DECISION_014
    date: 2026-04-28
    status: accepted
    decision: >-
      Separate the content-specific constitution_neighbor_ids_under_declared signal
      surfaced by maturity scoring V1.1 from PHASE_14 governance backlog pipeline
      integration. PHASE_16 is planned to govern explicit Constitution neighbor IDs,
      while PHASE_14 remains limited to the generic backlog mechanism.

```

## Open risks

```yaml
risks:
  - risk_id: RISK_001
    label: graph_analysis_becomes_source_of_truth
    severity: high
    status: mitigated
    mitigation: Graph outputs remain experimental until canonicalized through policy/decisions, deterministic regeneration, and validation.

  - risk_id: RISK_002
    label: neighbor_confused_with_owner
    severity: high
    status: mitigated_for_current_partition
    mitigation: target.ids and default_neighbors_to_read.ids are separated; referentiel/link are classified external_read_only.

  - risk_id: RISK_003
    label: candidate_nodes_or_edges_bypass_canon
    severity: high
    status: open
    mitigation: Candidate nodes and edges remain proposed until accepted and patched into canonical cores.

  - risk_id: RISK_004
    label: reconstruction_validation_too_weak
    severity: high
    status: mitigated_for_current_partition
    mitigation: ID-level readiness and normalized structural reconstruction both pass for the current partition.

  - risk_id: RISK_005
    label: global_multi_owner_clusters_unresolved
    severity: medium
    status: open
    mitigation: MACRO_004 remains pending; resolve through PHASE_14 / STAGE_00 follow-up.

  - risk_id: RISK_006
    label: global_neighbor_review_unresolved
    severity: medium
    status: open
    mitigation: MACRO_005 remains pending; resolve through PHASE_14 / STAGE_00 follow-up.

  - risk_id: RISK_007
    label: governance_backlog_not_consumed_by_stage00_or_launcher
    severity: medium
    status: open
    mitigation: >-
      PHASE_14 is now active and must integrate governance_backlog.yaml into
      STAGE_00 consumption, deterministic reporting, launcher surfacing, and
      explicit open/addressed/wont_fix lifecycle rules.
  - risk_id: RISK_008
    label: maturity_scoring_creates_two_truths
    severity: high
    status: mitigated_by_design
    mitigation: >-
      The scoring script is specified as diagnostic_report_only. It must compare
      computed maturity with published maturity but must not rewrite policy.yaml
      or override launcher gating until a future authority migration is explicitly governed.

  - risk_id: RISK_009
    label: maturity_scoring_v1_over_penalizes_dependency_explicitness
    severity: medium
    status: mitigated_by_v1_1_calibration
    mitigation: >-
      V1.1 keeps dependency explicitness strict but improves evidence granularity.
      Remaining low dependency_explicitness scores are treated as governance signals,
      not as scorer over-penalization by default.
  - risk_id: RISK_010
    label: constitution_neighbor_ids_under_declared
    severity: medium
    status: open
    mitigation: >-
      Open a governed follow-up to decide which Constitution-to-Constitution
      dependencies must be declared as explicit neighbor IDs in scope_generation
      policy/decisions. Do not rewrite maturity scores until this arbitration is done.
  - risk_id: RISK_011
    label: phase14_absorbs_scoring_neighbor_ids_content
    severity: medium
    status: mitigated_by_phase16_planning
    mitigation: >-
      PHASE_16 is planned as a separate content-governance phase. PHASE_14 remains
      focused on generic backlog production, export, reporting, launcher surfacing,
      and lifecycle rules.

```

## Next actions

```yaml
next_actions:
  - action_id: NEXT_001
    status: done
    label: Implement structural reconstruction validator
    target: tmp/validate_scope_partition_reconstruction.py
    phase: PHASE_11B

  - action_id: NEXT_002
    status: done
    label: Validate scope_extract.yaml and neighbor_extract.yaml on a synthetic or pilot patch_lifecycle run
    phase: PHASE_12

  - action_id: NEXT_003
    status: done
    label: Decide whether extract validation is sufficient for opening a serious patch_lifecycle pilot run
    target: docs/patcher/shared/extract_scope_slice.py

  - action_id: NEXT_004
    status: done
    label: Open, execute, promote, close, and archive one serious pilot bounded_local_run after reconstruction and extract gates pass
    recommended_scope: patch_lifecycle
    phase: PHASE_13
    run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01

  - action_id: NEXT_005
    status: done
    label: Export governance backlog candidates from the patch_lifecycle pilot into the canonical inter-run governance backlog
    phase: PHASE_13
    target: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml

  - action_id: NEXT_006
    status: done
    label: Integrate governance backlog consumption into the Constitution pipeline
    phase: PHASE_14
    input: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
    completed_decisions:
      - stage00_consumption_contract
      - deterministic_backlog_report_script
      - launcher_backlog_warning_behavior
    completed_outputs:
      - docs/pipelines/constitution/reports/governance_backlog_stage00_consumption_audit.yaml
      - docs/patcher/shared/report_governance_backlog.py
      - docs/pipelines/constitution/reports/governance_backlog_report.yaml
      - tmp/pipeline_launcher.py
      - docs/specs/constitution_governance_backlog_lifecycle.md
      - docs/patcher/shared/validate_governance_backlog_lifecycle.py
      - docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml
    remaining_decisions: []
  - action_id: NEXT_007
    status: done
    label: Implement deterministic post-scoping scope maturity scoring report
    phase: PHASE_15
    target: docs/patcher/shared/score_constitution_scope_maturity.py
    expected_output: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
    constraints:
      - do_not_modify_policy_yaml
      - do_not_modify_decisions_yaml
      - do_not_modify_generated_scope_catalog
      - keep_policy_yaml_authoritative_for_published_maturity

  - action_id: NEXT_008
    status: done
    label: Calibrate first deterministic scope maturity scoring report
    phase: PHASE_15
    input: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
    output: docs/pipelines/constitution/reports/scope_maturity_scoring_calibration_report.md
    decisions:
      - keep_policy_yaml_authoritative_until_arbitrated
      - keep_dependency_explicitness_strict
      - adjust_internal_coherence_in_v1_1_candidate
      - split_or_qualify_inter_release_stability_confidence_in_v1_1_candidate
  - action_id: NEXT_009
    status: done
    label: Implement scorer V1.1 candidate and rerun maturity report
    phase: PHASE_15
    target: docs/patcher/shared/score_constitution_scope_maturity.py
    expected_outputs:
      - docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      - comparison against docs/pipelines/constitution/reports/scope_maturity_scoring_calibration_report.md
    result:
      v1_1_report_status: FAIL
      computed_lower_than_published_count: 2
      non_blocking_delta_count: 1
      accepted_as_current_diagnostic_baseline: true
    constraints:
      - keep_dependency_explicitness_as_governance_signal
      - do_not_modify_policy_yaml
      - do_not_modify_generated_scope_catalog
      - keep_policy_yaml_authoritative_until_arbitrated

  - action_id: NEXT_010
    status: in_progress
    label: Govern explicit Constitution neighbor IDs surfaced by maturity scoring V1.1
    phase: PHASE_16
    inputs:
      - docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
      - docs/pipelines/constitution/policies/scope_generation/policy.yaml
      - docs/pipelines/constitution/policies/scope_generation/decisions.yaml
    completed_outputs:
      - docs/patcher/shared/report_constitution_neighbor_ids_governance.py
      - docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
    completed_outputs:
      - docs/patcher/shared/report_constitution_neighbor_ids_governance.py
      - docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
      - docs/patcher/shared/prepare_constitution_neighbor_ids_arbitration.py
      - docs/patcher/shared/validate_constitution_neighbor_ids_arbitration.py
      - docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml
    expected_decisions:
      - decide_neighbor_ids_to_add_per_scope
      - decide_entries_to_defer_to_governance_backlog
      - keep_policy_yaml_authoritative_until_arbitrated
    deferred_outputs:
      - docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py
    constraints:
      - do_not_change_published_maturity_scores_in_this_step
      - update_scope_generation_policy_only_after_human_arbitration
      - regenerate_scope_catalog_only_if_policy_decisions_change

```
