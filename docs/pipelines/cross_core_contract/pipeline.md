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
