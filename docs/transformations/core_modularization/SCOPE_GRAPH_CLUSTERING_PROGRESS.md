# Scope graph clustering progress tracker

Status: active tracker  
Related approach: `docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md`  
Related clarification: `docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md`  
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
- canonical export of pilot governance backlog entries.

## Current phase

```yaml
current_phase:
  phase_id: PHASE_14
  label: pilot_backlog_triage
  status: active
  summary: >-
    The serious patch_lifecycle pilot bounded_local_run is complete. Run
    CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 reached STAGE_09_CLOSEOUT_AND_ARCHIVE,
    is closed, promoted CORE_RELEASE_2026_04_28_R01 to docs/cores/current, and exported
    six governance backlog entries to docs/pipelines/constitution/scope_catalog/governance_backlog.yaml.
    Current work is to triage those entries and decide which items feed STAGE_00 scope
    partition review, cross-core follow-up, or future bounded patch_lifecycle design runs.
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
    label: pilot_backlog_triage
    status: active
    objective: >-
      Ingest governance backlog entries exported by the patch_lifecycle pilot,
      classify them into scope-neighbor review, scope-boundary review, external_read_only
      follow-up, or future bounded patch_lifecycle design work, and decide which entries
      should feed STAGE_00 scope partition review.
    primary_inputs:
      - docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
      - docs/pipelines/constitution/policies/scope_generation/policy.yaml
      - docs/pipelines/constitution/policies/scope_generation/decisions.yaml
    backlog_entries_in_scope:
      - GBC_PATCH_LIFECYCLE_LEARNER_STATE_NEIGHBORS_R01
      - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
      - GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01
      - GBC_PATCH_LIFECYCLE_UNCOVERED_CONFLICT_LOGGING_R01
      - GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01
      - GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01
    expected_triage_buckets:
      stage00_scope_partition_review:
        - learner_state_neighbor_review
        - escalation_boundary_review
        - uncovered_conflict_logging_ownership_review
      external_read_only_follow_up:
        - referentiel_parameter_dependency
      future_bounded_run_or_design_backlog:
        - patch_priority_queue_semantics
        - patch_lifecycle_full_state_machine
    related_open_macro_decisions:
      - MACRO_004_MULTI_OWNER_CLUSTER_REVIEW
      - MACRO_005_NEIGHBOR_DECLARATION_REVIEW
      - external_read_only_referentiel_link_follow_up
    expected_outputs:
      - backlog triage decision report
      - explicit mapping from each open backlog entry to next treatment path
      - optional accepted updates to scope_generation policy/decisions
      - regenerated scope catalog only if policy/decisions are changed
    note: >-
      PHASE_14 does not reopen CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01.
      It uses the exported inter-run governance backlog as an input to decide the
      next re-scoping or follow-up work.
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
  phase_14_backlog_triage_opened: true
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
    decision: Treat exported pilot backlog entries as inputs to PHASE_14 pilot_backlog_triage before any further re-scoping or future bounded design run.
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
    label: exported_backlog_entries_not_triaged
    severity: medium
    status: open
    mitigation: PHASE_14 is now active and must map each open backlog entry to a next treatment path.
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
    status: next
    label: Triage exported patch_lifecycle pilot governance backlog entries
    phase: PHASE_14
    input: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
    expected_decisions:
      - feed_stage00_scope_partition_review
      - feed_external_read_only_follow_up
      - defer_to_future_bounded_run_or_design_backlog
```
