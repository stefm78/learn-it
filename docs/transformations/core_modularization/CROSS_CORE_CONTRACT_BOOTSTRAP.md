# Cross-core contract bootstrap

Status: bootstrap materialized  
Transformation phase: `PHASE_32_CROSS_CORE_CONTRACT_BOOTSTRAP`  
Created by: `phase32_cross_core_contract_bootstrap_v2.py`  
Generated at: `2026-04-30T10:15:12Z`  
Branch: `feat/core-modularization-bootstrap`

Related files:

```text
docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md
docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml
docs/pipelines/constitution/signals.yaml
```

## 1. Purpose

This document bootstraps the governed flow for change requests crossing the Core
boundary:

```text
Constitution <-> Referentiel <-> Link
```

It exists because Constitution bounded runs may discover requirements that depend
on Referentiel parameters or Link bindings, while remaining forbidden from directly
patching `referentiel.yaml` or `link.yaml`.

Immediate trigger: reviewed `patch_lifecycle` backlog items, especially the external
threshold `N` controlling ineffective patch iterations before escalation.

## 2. Bootstrap decision

```yaml
cross_core_contract_bootstrap:
  phase: PHASE_32_CROSS_CORE_CONTRACT_BOOTSTRAP
  default_model: dedicated_cross_core_contract_pipeline
  proposed_pipeline_path: docs/pipelines/cross_core_contract/
  constitution_mode_extension: cross_core_governed_run
  constitution_mode_status: exceptional_not_default
  constitution_only_runs_may_emit_requests: true
  constitution_only_runs_may_apply_referentiel_or_link_changes: false
  open_constitution_run_now: false
```

Interpretation:

- A Constitution run remains the wrong place to silently modify Referentiel or Link.
- A dedicated `cross_core_contract` pipeline is the preferred long-term control plane.
- `cross_core_governed_run` may exist later as an explicit exceptional execution mode.
- This bootstrap does not open a Constitution run.

## 3. Draft contract object: `cross_core_change_request`

A Constitution run or Stage 00 review may emit a request, but this request is not
a patch authorization.

```yaml
cross_core_change_request:
  schema_version: '0.1'
  request_id: CCR_<DOMAIN>_<TOPIC>_RNN
  status: proposed

  source:
    source_pipeline: constitution
    source_scope_key: patch_lifecycle
    source_run_id: null
    source_stage: STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN
    source_backlog_entries:
      - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
      - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R02

  summary:
    title: Short human-readable title
    problem_statement: Why a Constitution-only run cannot safely resolve this
    desired_outcome: What the cross-core contract must decide or materialize
    non_goals:
      - Do not mutate referentiel/link from a Constitution-only run
      - Do not silently move ownership between cores

  affected_cores:
    - core: constitution
      role: source_consumer_or_rule_owner
      read_surface:
        - docs/cores/current/constitution.yaml
      proposed_write_surface: []
    - core: referentiel
      role: parameter_or_reference_owner
      read_surface:
        - docs/cores/current/referentiel.yaml
      proposed_write_surface: pending_arbitration
    - core: link
      role: inter_core_binding_owner
      read_surface:
        - docs/cores/current/link.yaml
      proposed_write_surface: pending_arbitration

  target_ids:
    constitution_ids: []
    referentiel_ids: []
    link_ids: []
    external_read_only_ids: []
    proposed_new_ids: []

  mutation_policy:
    request_creation: allowed
    core_write_authorization: forbidden_until_arbitrated
    generated_scope_catalog_update: forbidden_until_contract_decision
    backlog_closure: forbidden_until_validated_resolution

  validation_gates:
    required_before_apply:
      - validate_cross_core_change_request
      - validate_cross_core_write_surface
      - validate_constitution_referentiel_link_reconstruction
      - validate_link_binding_consistency
      - validate_multi_core_release_plan
      - validate_multi_core_promotion_manifest

  release_policy:
    release_scope: multi_core_or_explicitly_single_core_with_link_compatibility
    promotion_mode: atomic_preferred
    constitution_only_release_may_close_request: false

  decision:
    decision_status: pending_arbitration
    selected_execution_model: null
    notes: []
```

## 4. Lifecycle

```yaml
cross_core_change_request_lifecycle:
  allowed_status_values:
    - proposed
    - accepted_for_arbitration
    - rejected
    - deferred
    - materialized
    - closed

  transition_rules:
    - from: proposed
      to: accepted_for_arbitration
      requires:
        - source evidence
        - affected core list
        - initial mutation policy
    - from: accepted_for_arbitration
      to: materialized
      requires:
        - explicit write surface
        - validated patchset or release plan
        - multi-core validation report
    - from: materialized
      to: closed
      requires:
        - release evidence
        - promotion evidence
        - backlog resolution mapping
```

Backlog entries remain open until a validated resolution exists. A request can
reference backlog items, but creating the request does not close them.

## 5. Write surface rules

### Request phase

Allowed writes:

```text
docs/transformations/core_modularization/*
docs/pipelines/cross_core_contract/ only after explicit human decision
docs/pipelines/*/reports/ when generated by validators
```

Forbidden writes by this bootstrap:

```text
docs/cores/current/constitution.yaml
docs/cores/current/referentiel.yaml
docs/cores/current/link.yaml
docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml by hand
```

### Execution phase

Execution may write Core files only if all of the following are true:

```yaml
cross_core_execution_authorization:
  explicit_execution_model_selected: true
  write_surface_declared: true
  affected_cores_declared: true
  validators_passed_before_apply: true
  release_and_promotion_policy_declared: true
  human_decision_recorded: true
```

## 6. Validation gates to introduce later

```yaml
validators:
  request_shape:
    script: docs/patcher/shared/validate_cross_core_change_request.py
    purpose: validate request schema, source evidence, lifecycle status, and mutation policy

  write_surface:
    script: docs/patcher/shared/validate_cross_core_write_surface.py
    purpose: ensure proposed writes match selected execution model and affected cores

  reconstruction:
    script: docs/patcher/shared/validate_cross_core_reconstruction.py
    purpose: check Constitution, Referentiel, and Link consistency after proposed changes

  release_plan:
    script: docs/patcher/shared/validate_cross_core_release_plan.py
    purpose: prevent single-core release from silently closing cross-core obligations

  promotion_manifest:
    script: docs/patcher/shared/validate_cross_core_promotion_manifest.py
    purpose: verify promoted current Core set and compatibility references
```

These scripts are not created by this bootstrap.

## 7. Release and promotion rule

A cross-core request can be closed only when release evidence maps the request to
one of these outcomes:

```yaml
closure_outcomes:
  - multi_core_release_promoted
  - single_core_release_promoted_with_validated_link_compatibility
  - rejected_with_reason
  - wont_fix_with_reason
```

A Constitution-only release may reference an open request, but it must not claim
that the Referentiel/Link part has been resolved.

## 8. Treatment of patch_lifecycle threshold `N`

```yaml
patch_lifecycle_threshold_N:
  status: cross_core_follow_up
  constitution_resolution_now: forbidden
  referentiel_link_mutation_now: forbidden
  backlog_entries_remain_open:
    - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
    - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R02
  proposed_request_id: CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01
  next_contract_question: >-
    Should the ineffective patch iteration threshold N become a Referentiel parameter,
    a Link-bound external read-only reference, or a different cross-core construct?
```

The parameter `N` must not be added to Constitution as a local parameter merely to
complete a bounded patch_lifecycle run.

## 9. Treatment of `TYPE_SELF_REPORT_AR_N2`

```yaml
type_self_report_ar_n2_neighbor:
  status: pending_neighbor_closure_arbitration
  update_scope_generation_decisions_now: forbidden
  backlog_entry_remains_open: GBC_PATCH_LIFECYCLE_VALUE_COST_AR_N2_NEIGHBOR_R01
  next_contract_question: >-
    Is TYPE_SELF_REPORT_AR_N2 a transitive learner_state dependency only, or should it
    become an explicit patch_lifecycle read neighbor through scope_generation policy?
```

This bootstrap does not modify neighbor declarations.

## 10. Open implementation questions

```yaml
open_questions:
  - id: CC_001
    question: Should docs/pipelines/cross_core_contract/ be created now as a first-class pipeline skeleton?
    recommended_answer: yes_after_human_decision

  - id: CC_002
    question: Should cross_core_change_request files live under the new pipeline or under the emitting pipeline?
    recommended_answer: canonical_under_cross_core_contract_with_source_references_from_emitting_pipelines

  - id: CC_003
    question: Should cross_core_governed_run be implemented as a Constitution mode before the dedicated pipeline exists?
    recommended_answer: no

  - id: CC_004
    question: What is the first real request to materialize?
    recommended_answer: CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01
```

## 11. Guardrails

```yaml
guardrails:
  - do_not_open_constitution_run_from_this_bootstrap
  - do_not_modify_constitution_yaml
  - do_not_modify_referentiel_yaml
  - do_not_modify_link_yaml
  - do_not_resolve_patch_lifecycle_threshold_N_in_constitution
  - do_not_modify_TYPE_SELF_REPORT_AR_N2_neighbor_declaration_without_dedicated_arbitration
  - keep_patch_lifecycle_backlog_entries_open_with_review_metadata
  - treat_cross_core_change_request_as_request_not_patch_authorization
```

## 12. Recommended next step

```yaml
recommended_next_step:
  phase: PHASE_32_CROSS_CORE_CONTRACT_BOOTSTRAP
  action: decide whether to instantiate docs/pipelines/cross_core_contract/ skeleton
  default: prepare skeleton only, no core mutation, no run opening
```


## 13. Materialization evidence

```yaml
materialized_by_phase:
  phase: PHASE_32_CROSS_CORE_CONTRACT_BOOTSTRAP
  pipeline_skeleton: docs/pipelines/cross_core_contract/
  registry_updated: docs/registry/pipelines.md
  validator: docs/patcher/shared/validate_cross_core_contract_pipeline.py
  validation_report: docs/registry/reports/cross_core_contract_pipeline_validation.yaml
  pipeline_signals_validation: docs/registry/reports/pipeline_signals_validation.yaml
  recovery_script: phase32_recover_cross_core_contract_validator.py
  no_core_mutation: true
  no_constitution_run_opened: true
```
