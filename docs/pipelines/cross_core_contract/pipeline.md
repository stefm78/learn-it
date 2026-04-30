# PIPELINE — cross_core_contract

id: cross_core_contract
version: 0.1
scope: cross-core-change-control
status: governed_l3

## Goal

Gouverner les demandes de changement qui traversent les frontières entre les Core :

```text
Constitution <-> Referentiel <-> Link
```

Ce pipeline existe pour éviter qu'un run Constitution ne modifie implicitement
`referentiel.yaml` ou `link.yaml`.

## Non-goals

```yaml
non_goals:
  - open_constitution_run
  - patch_core_files_without_explicit_cross_core_authorization
  - close_constitution_backlog_entries_without_validated_resolution
  - resolve_patch_lifecycle_threshold_N_inside_constitution_only_scope
  - modify_TYPE_SELF_REPORT_AR_N2_neighbor_declaration_without_dedicated_arbitration
```

## Canonical resources

```text
docs/transformations/core_modularization/CROSS_CORE_CONTRACT_BOOTSTRAP.md
docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md
docs/pipelines/cross_core_contract/schemas/cross_core_change_request.schema.yaml
docs/pipelines/cross_core_contract/requests/
docs/pipelines/cross_core_contract/reports/
```

## Controlled write surface

### Request/bootstrap mode

Allowed:

```text
docs/pipelines/cross_core_contract/**
docs/registry/pipelines.md
docs/registry/reports/**
docs/patcher/shared/validate_cross_core_contract_pipeline.py
docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
```

Forbidden:

```text
docs/cores/current/constitution.yaml
docs/cores/current/referentiel.yaml
docs/cores/current/link.yaml
docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml by hand
```

### Execution mode

Core writes require an explicit future execution contract:

```yaml
cross_core_execution_authorization:
  explicit_execution_model_selected: true
  write_surface_declared: true
  affected_cores_declared: true
  validators_passed_before_apply: true
  release_and_promotion_policy_declared: true
  human_decision_recorded: true
```

## Staging

```text
inputs: docs/pipelines/cross_core_contract/inputs/
requests: docs/pipelines/cross_core_contract/requests/
work/01_intake: docs/pipelines/cross_core_contract/work/01_intake/
work/02_arbitrage: docs/pipelines/cross_core_contract/work/02_arbitrage/
work/03_contract_synthesis: docs/pipelines/cross_core_contract/work/03_contract_synthesis/
work/04_validation: docs/pipelines/cross_core_contract/work/04_validation/
work/05_release_planning: docs/pipelines/cross_core_contract/work/05_release_planning/
reports: docs/pipelines/cross_core_contract/reports/
outputs: docs/pipelines/cross_core_contract/outputs/
```

## Hardening level

```yaml
hardening_level: L3_managed_execution_pipeline
hardening_reference: docs/specs/pipeline_hardening_model.md
ai_protocol: docs/pipelines/cross_core_contract/AI_PROTOCOL.yaml
entry_actions: docs/pipelines/cross_core_contract/entry_actions/
stage_skills: docs/pipelines/cross_core_contract/stages/
validation_report: docs/registry/reports/cross_core_contract_hardening_validation.yaml
l4_boundary: L4 before any Core write
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

This pipeline is hardened to L3 for intake, evidence review, arbitration and contract synthesis.
It remains below L4: no Core write, backlog closure, release or promotion is authorized.
## Generic gate execution runner

```yaml
phase: PHASE_58_CROSS_CORE_GENERIC_GATE_EXECUTION_RUNNER
runner_ref: docs/pipelines/cross_core_contract/GENERIC_GATE_EXECUTION_RUNNER.md
runner_yaml: docs/pipelines/cross_core_contract/validators/generic_gate_execution_runner.yaml
runner_script: docs/patcher/shared/run_cross_core_gate_execution.py
validation_report: docs/registry/reports/cross_core_generic_gate_execution_runner_validation.yaml
generic_gate_execution_runner_defined: true
gate_execution_smoke_status: BLOCKED_NOT_AUTHORIZED
downstream_gates_executed_on_smoke: false
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
```

The generic runner starts from any instantiated execution contract and blocks before downstream gates unless the contract is authorized.

## Generic execution contract instantiator

```yaml
phase: PHASE_57_CROSS_CORE_GENERIC_EXECUTION_CONTRACT_INSTANTIATOR
instantiator_ref: docs/pipelines/cross_core_contract/GENERIC_EXECUTION_CONTRACT_INSTANTIATOR.md
instantiator_yaml: docs/pipelines/cross_core_contract/validators/generic_execution_contract_instantiator.yaml
instantiator_script: docs/patcher/shared/materialize_cross_core_execution_contract.py
validation_report: docs/registry/reports/cross_core_execution_contract_instantiator_validation.yaml
generic_execution_contract_instantiator_defined: true
instantiation_smoke_status: BLOCKED_NOT_AUTHORIZED
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
```

The instantiator is request-independent. It can materialize a non-authorized execution contract from any `cross_core_change_request`.

## Generic mutating execution framework

```yaml
phase: PHASE_56_CROSS_CORE_GENERIC_MUTATING_EXECUTION_FRAMEWORK
framework_ref: docs/pipelines/cross_core_contract/GENERIC_MUTATING_EXECUTION_FRAMEWORK.md
framework_yaml: docs/pipelines/cross_core_contract/validators/generic_mutating_execution_framework.yaml
execution_contract_schema: docs/pipelines/cross_core_contract/schemas/cross_core_execution_contract.schema.yaml
execution_contract_template: docs/pipelines/cross_core_contract/templates/cross_core_execution_contract.template.yaml
execution_contract_validator: docs/patcher/shared/validate_cross_core_execution_contract.py
validation_report: docs/registry/reports/cross_core_generic_mutating_execution_framework_validation.yaml
generic_mutating_execution_framework_defined: true
l4_mutating_execution_framework_ready: true
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
```

This framework is generic. It applies to any future `cross_core_change_request`, not to a specific candidate request.

## L4 control-plane activation

```yaml
phase: PHASE_55_CROSS_CORE_L4_CONTROL_PLANE_ACTIVATION
activation_ref: docs/pipelines/cross_core_contract/L4_CONTROL_PLANE_ACTIVATION.md
activation_yaml: docs/pipelines/cross_core_contract/validators/l4_control_plane_activation.yaml
activation_review: docs/pipelines/cross_core_contract/activation_reviews/L4_ACTIVATION_REVIEW_2026_04_30_R01.yaml
validation_report: docs/registry/reports/cross_core_l4_control_plane_activation_validation.yaml
l4_control_plane_active_now: true
l4_activation_review_materialized_now: true
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
```

The L4 control plane is active. This does not authorize Core mutation, backlog closure, release, promotion, or threshold N resolution.

## L4 hardening closeout

```yaml
phase: PHASE_54_CROSS_CORE_L4_HARDENING_CLOSEOUT
closeout_ref: docs/pipelines/cross_core_contract/L4_HARDENING_CLOSEOUT.md
closeout_yaml: docs/pipelines/cross_core_contract/validators/l4_hardening_closeout.yaml
validation_report: docs/registry/reports/cross_core_l4_hardening_closeout_validation.yaml
l4_hardening_closeout_complete: true
recommended_next_action: stop_at_NO_ACTIVE_PHASE
l4_activation_ready_now: false
l4_active_now: false
```

The L4 hardening sequence is structurally complete and validated, but inactive. Future activation requires a real approved L4 activation review instance and passing gates.

## L4 dry-run activation orchestrator

```yaml
phase: PHASE_53_CROSS_CORE_L4_DRY_RUN_ACTIVATION_ORCHESTRATOR
orchestrator_ref: docs/pipelines/cross_core_contract/L4_DRY_RUN_ACTIVATION_ORCHESTRATOR.md
orchestrator_yaml: docs/pipelines/cross_core_contract/validators/l4_dry_run_activation_orchestrator.yaml
script: docs/patcher/shared/run_cross_core_l4_activation_dry_run.py
validation_report: docs/registry/reports/cross_core_l4_dry_run_activation_orchestrator_validation.yaml
template_dry_run_report: docs/registry/reports/l4_activation_dry_run_template_report.yaml
template_dry_run_status: BLOCKED_NOT_APPROVED
downstream_gates_executed_on_template: false
l4_activation_ready_now: false
l4_active_now: false
```

The dry-run orchestrator blocks before downstream gates when the activation review is not approved. It never authorizes mutation.

## L4 activation gate orchestration

```yaml
phase: PHASE_52_CROSS_CORE_L4_ACTIVATION_GATE_ORCHESTRATION
orchestration_ref: docs/pipelines/cross_core_contract/L4_ACTIVATION_GATE_ORCHESTRATION.md
orchestration_yaml: docs/pipelines/cross_core_contract/validators/l4_activation_gate_orchestration.yaml
validation_report: docs/registry/reports/cross_core_l4_activation_gate_orchestration_validation.yaml
l4_activation_gate_orchestration_defined: true
l4_gate_orchestration_executable_now: false
l4_activation_ready_now: false
l4_active_now: false
```

This defines the mandatory future order of L4 activation gates. It does not activate L4.

## L4 activation review instance validator

```yaml
phase: PHASE_51_CROSS_CORE_L4_ACTIVATION_REVIEW_INSTANCE_VALIDATOR
validator: docs/patcher/shared/validate_cross_core_l4_activation_review_instance.py
validation_surface: docs/pipelines/cross_core_contract/L4_ACTIVATION_REVIEW_INSTANCE_VALIDATION.md
validation_yaml: docs/pipelines/cross_core_contract/validators/l4_activation_review_instance_validation.yaml
validation_report: docs/registry/reports/cross_core_l4_activation_review_instance_validator_validation.yaml
template_smoke_report: docs/registry/reports/l4_activation_review_template_instance_validation.yaml
activation_review_instance_validator_defined: true
template_instance_validation_status: BLOCKED_NOT_APPROVED
l4_activation_ready_now: false
l4_active_now: false
```

The inactive template must be rejected as `BLOCKED_NOT_APPROVED`; real L4 activation remains unavailable without a future approved review and passing L4 gates.

## L4 activation review input contract

```yaml
phase: PHASE_50_CROSS_CORE_L4_ACTIVATION_REVIEW_INPUT_CONTRACT
contract_ref: docs/pipelines/cross_core_contract/L4_ACTIVATION_REVIEW_INPUT.md
schema_ref: docs/pipelines/cross_core_contract/schemas/l4_activation_review.schema.yaml
template_ref: docs/pipelines/cross_core_contract/templates/l4_activation_review.template.yaml
validation_report: docs/registry/reports/cross_core_l4_activation_review_input_contract_validation.yaml
l4_activation_input_contract_defined: true
l4_activation_review_materialized_now: false
l4_activation_ready_now: false
l4_active_now: false
```

This contract defines the required shape of a future human-authorized L4 activation review. It does not activate L4.

## L4 executable validator readiness

```yaml
phase: PHASE_49_CROSS_CORE_L4_EXECUTABLE_VALIDATOR_READINESS
readiness_ref: docs/pipelines/cross_core_contract/L4_EXECUTABLE_VALIDATOR_READINESS.md
readiness_yaml_ref: docs/pipelines/cross_core_contract/validators/l4_executable_validator_readiness.yaml
validation_report: docs/registry/reports/cross_core_l4_executable_validator_readiness_validation.yaml
executable_layer_complete: true
all_contract_checks_PASS: true
all_l4_gate_smokes_BLOCKED: true
l4_activation_ready_now: false
l4_active_now: false
```

All eight L4 validators are executable, but L4 gate mode remains intentionally blocking without future L4 execution inputs.

## L4 executable validators batch 2

```yaml
phase: PHASE_48_CROSS_CORE_L4_EXECUTABLE_VALIDATORS_BATCH2
executable_validators_batch2_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
l4_execution_ready_now: false
validate_multi_core_release_plan:
  script: docs/patcher/shared/validate_multi_core_release_plan.py
  contract_check_report: docs/registry/reports/validate_multi_core_release_plan_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_multi_core_promotion_manifest:
  script: docs/patcher/shared/validate_multi_core_promotion_manifest.py
  contract_check_report: docs/registry/reports/validate_multi_core_promotion_manifest_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_cross_core_backlog_resolution:
  script: docs/patcher/shared/validate_cross_core_backlog_resolution.py
  contract_check_report: docs/registry/reports/validate_cross_core_backlog_resolution_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_cross_core_rollback_or_reconciliation_path:
  script: docs/patcher/shared/validate_cross_core_rollback_or_reconciliation_path.py
  contract_check_report: docs/registry/reports/validate_cross_core_rollback_or_reconciliation_path_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
```

These validators are executable in contract-check mode only. L4 gate mode is intentionally blocking until future L4 inputs exist.
## L4 executable validators batch 1

```yaml
phase: PHASE_47_CROSS_CORE_L4_EXECUTABLE_VALIDATORS_BATCH1
executable_validators_batch1_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
l4_execution_ready_now: false
validate_cross_core_l4_transition_review:
  script: docs/patcher/shared/validate_cross_core_l4_transition_review.py
  contract_check_report: docs/registry/reports/validate_cross_core_l4_transition_review_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_cross_core_write_surface:
  script: docs/patcher/shared/validate_cross_core_write_surface.py
  contract_check_report: docs/registry/reports/validate_cross_core_write_surface_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_constitution_referentiel_link_reconstruction:
  script: docs/patcher/shared/validate_constitution_referentiel_link_reconstruction.py
  contract_check_report: docs/registry/reports/validate_constitution_referentiel_link_reconstruction_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
validate_link_binding_consistency:
  script: docs/patcher/shared/validate_link_binding_consistency.py
  contract_check_report: docs/registry/reports/validate_link_binding_consistency_contract_check.yaml
  default_mode: contract_check
  l4_gate_mode_blocks_without_future_inputs: true
```

These validators are executable in contract-check mode only. L4 gate mode is intentionally blocking until future L4 inputs exist.
## L4 readiness matrix

```yaml
matrix_ref: docs/pipelines/cross_core_contract/L4_READINESS_MATRIX.md
yaml_ref: docs/pipelines/cross_core_contract/validators/l4_readiness_matrix.yaml
validation_report: docs/registry/reports/cross_core_l4_readiness_matrix_validation.yaml
target_model_complete: true
implementation_ready_to_start_l4_validator_scripts: true
l4_execution_ready_now: false
l4_active_now: false
```

The matrix consolidates all inactive L4 validator contracts. It does not activate L4.

## Remaining L4 validator contracts

```yaml
batch_phase: PHASE_45_CROSS_CORE_REMAINING_L4_VALIDATOR_CONTRACTS
l4_active_now: false
executable_as_l4_gate_now: false
validate_multi_core_promotion_manifest:
  contract_yaml: docs/pipelines/cross_core_contract/validators/validate_multi_core_promotion_manifest.contract.yaml
  contract_markdown: docs/pipelines/cross_core_contract/validators/validate_multi_core_promotion_manifest.contract.md
  contract_defined: true
validate_cross_core_backlog_resolution:
  contract_yaml: docs/pipelines/cross_core_contract/validators/validate_cross_core_backlog_resolution.contract.yaml
  contract_markdown: docs/pipelines/cross_core_contract/validators/validate_cross_core_backlog_resolution.contract.md
  contract_defined: true
validate_cross_core_rollback_or_reconciliation_path:
  contract_yaml: docs/pipelines/cross_core_contract/validators/validate_cross_core_rollback_or_reconciliation_path.contract.yaml
  contract_markdown: docs/pipelines/cross_core_contract/validators/validate_cross_core_rollback_or_reconciliation_path.contract.md
  contract_defined: true
```

These contracts complete the inactive L4 validator family. They do not activate L4 or authorize canonical writes.
## validate_multi_core_release_plan contract

```yaml
contract_yaml: docs/pipelines/cross_core_contract/validators/validate_multi_core_release_plan.contract.yaml
contract_markdown: docs/pipelines/cross_core_contract/validators/validate_multi_core_release_plan.contract.md
contract_validation_report: docs/registry/reports/multi_core_release_plan_validator_contract_validation.yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
release_materialized_now: false
```

This is a future L4 validator contract. It does not activate L4 or create a release.

## validate_link_binding_consistency contract

```yaml
contract_yaml: docs/pipelines/cross_core_contract/validators/validate_link_binding_consistency.contract.yaml
contract_markdown: docs/pipelines/cross_core_contract/validators/validate_link_binding_consistency.contract.md
contract_validation_report: docs/registry/reports/link_binding_consistency_validator_contract_validation.yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
```

This is a future L4 validator contract. It does not activate L4 or authorize canonical writes.

## validate_constitution_referentiel_link_reconstruction contract

```yaml
contract_yaml: docs/pipelines/cross_core_contract/validators/validate_constitution_referentiel_link_reconstruction.contract.yaml
contract_markdown: docs/pipelines/cross_core_contract/validators/validate_constitution_referentiel_link_reconstruction.contract.md
contract_validation_report: docs/registry/reports/constitution_referentiel_link_reconstruction_validator_contract_validation.yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
```

This is a future L4 validator contract. It does not activate L4 or authorize canonical writes.

## validate_cross_core_write_surface contract

```yaml
contract_yaml: docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.yaml
contract_markdown: docs/pipelines/cross_core_contract/validators/validate_cross_core_write_surface.contract.md
contract_validation_report: docs/registry/reports/cross_core_write_surface_validator_contract_validation.yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
```

This is a future L4 validator contract. It does not activate L4 or authorize canonical writes.

## validate_cross_core_l4_transition_review contract

```yaml
contract_yaml: docs/pipelines/cross_core_contract/validators/validate_cross_core_l4_transition_review.contract.yaml
contract_markdown: docs/pipelines/cross_core_contract/validators/validate_cross_core_l4_transition_review.contract.md
contract_validation_report: docs/registry/reports/cross_core_l4_transition_review_validator_contract_validation.yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
```

This is a future L4 validator contract. It does not activate L4 or authorize canonical writes.

## L4 validator family

```yaml
l4_validator_family: docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md
l4_validator_family_yaml: docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml
l4_validator_family_validation: docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml
validator_family_defined: true
validators_executable_as_l4_gate_now: false
individual_validator_scripts_required_before_L4_execution: true
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

This family defines the validators required before future L4 activation. It does not
activate L4 or authorize any canonical write.

## L4 target contract

```yaml
l4_target_contract: docs/pipelines/cross_core_contract/L4_TARGET_CONTRACT.md
l4_transition_checklist: docs/pipelines/cross_core_contract/l4_transition_checklist.yaml
l4_target_defined: true
l4_active_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

The pipeline is intentionally L3 active / L4 targeted. Future L4 activation requires
explicit human decision and validation of the transition checklist.

## Stages

### STAGE_00_INTAKE_AND_SHAPE_VALIDATION

Objectif :

```text
Valider qu'une cross_core_change_request est bien une demande gouvernée,
pas une autorisation de patch.
```

Entrées :

```text
docs/pipelines/cross_core_contract/requests/*.yaml
docs/pipelines/cross_core_contract/schemas/cross_core_change_request.schema.yaml
```

Sorties :

```text
docs/pipelines/cross_core_contract/reports/cross_core_change_request_validation.yaml
```

### STAGE_01_SOURCE_EVIDENCE_REVIEW

Objectif : vérifier les preuves source : backlog, run, STAGE_00, arbitrage ou release.

Sorties :

```text
docs/pipelines/cross_core_contract/work/01_intake/source_evidence_review.md
docs/pipelines/cross_core_contract/reports/source_evidence_review.yaml
```

### STAGE_02_CROSS_CORE_ARBITRAGE

Objectif : décider si la demande relève de Constitution, Referentiel, Link, ou d'une coordination multi-Core.

Sorties :

```text
docs/pipelines/cross_core_contract/work/02_arbitrage/cross_core_arbitrage.md
```

### STAGE_03_CONTRACT_SYNTHESIS

Objectif : produire un contrat d'exécution : surface de lecture, surface d'écriture, validations, release et promotion.

Sorties :

```text
docs/pipelines/cross_core_contract/work/03_contract_synthesis/cross_core_execution_contract.yaml
```

### STAGE_04_VALIDATION

Objectif : valider la cohérence du contrat avant toute écriture Core.

Validations cibles :

```text
validate_cross_core_change_request
validate_cross_core_write_surface
validate_constitution_referentiel_link_reconstruction
validate_link_binding_consistency
validate_multi_core_release_plan
validate_multi_core_promotion_manifest
```

### STAGE_05_RELEASE_AND_PROMOTION_PLANNING

Objectif : décider si la résolution exige une release multi-Core ou une release single-Core avec compatibilité Link validée.

Sorties :

```text
docs/pipelines/cross_core_contract/work/05_release_planning/cross_core_release_plan.yaml
```

## Initial candidate request

```yaml
candidate:
  request_id: CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01
  status: materialized_as_proposed_request
  source_scope_key: patch_lifecycle
  request_file: docs/pipelines/cross_core_contract/requests/CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01.yaml
  linked_backlog_candidates:
    - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
    - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R02
  question: >-
    Should ineffective patch iteration threshold N become a Referentiel parameter,
    a Link-bound external read-only reference, or another cross-core construct?
```

## Success criteria

```yaml
success_criteria:
  - cross_core_change_request shape exists and is validated
  - no Constitution-only run can silently write Referentiel or Link
  - backlog references remain open until validated resolution
  - release/promotion impact is explicit before Core mutation
  - launcher and registry can discover this pipeline without authorizing runs
```
