# Scope graph clustering progress tracker

Status: draft tracker  
Related approach: `docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md`  
Pipeline: `constitution`  
Branch: `feat/core-modularization-bootstrap`

## Purpose

Synthetic progress tracker for the scope graph clustering approach. The full method is described in `SCOPE_GRAPH_CLUSTERING_APPROACH.md`.

## Current phase

```yaml
current_phase:
  phase_id: PHASE_00
  label: approach_definition
  status: in_progress
  summary: >-
    The graph-based scoping approach has been formulated. The next step is to
    materialize the approach document, confirm this tracker, then start the
    Scope Lab implementation.
```

## Phase tracker

```yaml
phases:
  - phase_id: PHASE_00
    label: approach_definition
    status: in_progress
    outputs:
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
      - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md

  - phase_id: PHASE_01
    label: disposable_run_cleanup
    status: not_started
    objective: Stop, abandon, or purge disposable test runs so they do not constrain scoping redesign.

  - phase_id: PHASE_02
    label: scope_lab_workspace
    status: not_started
    objective: Create tmp/scope_lab/ for experimental graph outputs.

  - phase_id: PHASE_03
    label: full_graph_extraction
    status: not_started
    objective: Extract graph nodes and edges from constitution, referentiel, and link.
    expected_outputs:
      - tmp/analyze_constitution_dependency_graph.py
      - tmp/scope_lab/constitution_graph_nodes.yaml
      - tmp/scope_lab/constitution_graph_edges.yaml

  - phase_id: PHASE_04
    label: natural_cluster_detection
    status: not_started
    objective: Detect deterministic, explainable graph clusters.
    expected_outputs:
      - tmp/scope_lab/constitution_graph_clusters.yaml

  - phase_id: PHASE_05
    label: cluster_closure_analysis
    status: not_started
    objective: Classify internal edges, external neighbor edges, bridge edges, missing targets, candidate nodes, and candidate edges.
    expected_outputs:
      - tmp/scope_lab/cluster_closure_report.yaml

  - phase_id: PHASE_06
    label: scope_alignment_review
    status: not_started
    objective: Compare graph clusters with current canonical scopes.
    expected_outputs:
      - tmp/scope_lab/scope_alignment_report.yaml

  - phase_id: PHASE_07
    label: redesign_candidates
    status: not_started
    objective: Produce explicit scoping redesign candidates for human arbitration.
    expected_outputs:
      - tmp/scope_lab/scope_redesign_candidates.yaml

  - phase_id: PHASE_08
    label: human_arbitration
    status: not_started
    objective: Resolve each candidate as accepted, rejected, deferred, or backlog.
    expected_outputs:
      - tmp/scope_lab/scope_redesign_arbitration.yaml

  - phase_id: PHASE_09
    label: canonical_patch
    status: not_started
    objective: Apply accepted changes to canonical cores and scope generation inputs.

  - phase_id: PHASE_10
    label: scope_catalog_regeneration
    status: not_started
    objective: Regenerate the scope catalog deterministically.
    expected_outputs:
      - tmp/constitution_scope_generation_report.yaml

  - phase_id: PHASE_11
    label: bijection_and_reconstruction_validation
    status: not_started
    objective: Validate ownership bijection and full structural reconstruction of constitution, referentiel, and link.
    expected_outputs:
      - tmp/validate_scope_partition_bijection.py
      - tmp/scope_partition_bijection_validation.yaml

  - phase_id: PHASE_12
    label: extract_validation
    status: not_started
    objective: Validate scope_extract.yaml and neighbor_extract.yaml on a synthetic or pilot run.

  - phase_id: PHASE_13
    label: pilot_bounded_local_run
    status: not_started
    objective: Open one serious pilot bounded_local_run after all scoping gates pass.
    recommended_scope: patch_lifecycle
```

## Implementation checklist

```yaml
implementation_tracking:
  approach_document_created: false
  progress_tracker_created: true
  disposable_runs_cleaned_or_abandoned: false
  scope_lab_workspace_created: false
  full_graph_script_created: false
  graph_nodes_edges_generated: false
  cluster_detection_generated: false
  cluster_closure_report_generated: false
  scope_alignment_report_generated: false
  redesign_candidates_generated: false
  human_arbitration_recorded: false
  canonical_core_patches_applied_if_needed: false
  scope_generation_decisions_updated: false
  scope_catalog_regenerated: false
  bijection_validator_created: false
  ownership_bijection_passed: false
  full_reconstruction_passed: false
  extract_tests_passed: false
  pilot_bounded_local_run_opened: false
```

## Open risks

```yaml
risks:
  - risk_id: RISK_001
    label: graph_analysis_becomes_source_of_truth
    severity: high
    mitigation: Keep graph outputs experimental until canonicalized through core patches, decisions, regeneration, and validation.

  - risk_id: RISK_002
    label: neighbor_confused_with_owner
    severity: high
    mitigation: Keep target.ids and default_neighbors_to_read.ids strictly separated.

  - risk_id: RISK_003
    label: candidate_nodes_or_edges_bypass_canon
    severity: high
    mitigation: Candidate nodes and edges remain proposed until accepted and patched into canonical cores.

  - risk_id: RISK_004
    label: reconstruction_validation_too_weak
    severity: high
    mitigation: Require normalized structural reconstruction of constitution, referentiel, and link.
```

## Next actions

```yaml
next_actions:
  - action_id: NEXT_001
    status: pending
    label: Create or confirm approach document
    target: docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md

  - action_id: NEXT_002
    status: pending
    label: Decide how to handle disposable active runs
    target: docs/pipelines/constitution/runs/index.yaml

  - action_id: NEXT_003
    status: pending
    label: Create Scope Lab workspace
    target: tmp/scope_lab/

  - action_id: NEXT_004
    status: pending
    label: Draft experimental graph extraction script
    target: tmp/analyze_constitution_dependency_graph.py

  - action_id: NEXT_005
    status: pending
    label: Draft bijection and reconstruction validator contract
    target: tmp/validate_scope_partition_bijection.py
```

## Decision log

```yaml
decision_log:
  - decision_id: DECISION_001
    date: 2026-04-27
    status: proposed
    decision: Use graph clustering as a diagnostic and validation layer, not as an automatic replacement for human-governed scope partitioning.

  - decision_id: DECISION_002
    date: 2026-04-27
    status: proposed
    decision: Require ownership bijection and full structural reconstruction of constitution, referentiel, and link before opening serious bounded local runs.

  - decision_id: DECISION_003
    date: 2026-04-27
    status: proposed
    decision: Allow candidate nodes and candidate edges in the Scope Lab, but prohibit canonical use until explicitly accepted and patched into canonical cores.
```
