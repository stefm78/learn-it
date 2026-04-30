# Cross-core contract — L4 target contract

Status: target defined, inactive
Phase: `PHASE_38_CROSS_CORE_L4_TARGET_CONTRACT`
Generated at: `2026-04-30T11:19:15Z`

## Purpose

This document defines the future L4 target for `cross_core_contract`.

It takes the real target now, because this pipeline will eventually govern changes that may touch:

```text
Constitution
Referentiel
Link
governance backlog
release / promotion
```

This phase does not activate L4 and does not authorize any Core, backlog, release or promotion write.

## Current posture

```yaml
current_hardening_level: L3_managed_execution_pipeline
target_hardening_level: L4_critical_canonical_pipeline
l4_target_defined: true
l4_active_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
constitution_run_authorized: false
```

## L4 activation principle

```yaml
activation_rule:
  requires_explicit_human_decision: true
  requires_l4_transition_review: true
  requires_declared_read_surface: true
  requires_declared_write_surface: true
  requires_validated_contract_synthesis: true
  requires_multi_core_release_plan: true
  requires_promotion_manifest_policy: true
  requires_rollback_or_reconciliation_path: true
  request_creation_is_not_authorization: true
```

## Future L4 write surfaces

These are target surfaces only. They are not active in the current phase.

```yaml
future_l4_write_surfaces:
  constitution:
    path: docs/cores/current/constitution.yaml
    status: future_explicit_authorization_required
  referentiel:
    path: docs/cores/current/referentiel.yaml
    status: future_explicit_authorization_required
  link:
    path: docs/cores/current/link.yaml
    status: future_explicit_authorization_required
  governance_backlog:
    path: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
    status: future_validated_resolution_required
  releases:
    path: docs/cores/releases/**
    status: future_multi_core_release_plan_required
  current_manifest:
    path: docs/cores/current/manifest.yaml
    status: future_promotion_manifest_validation_required
```

## Future L4 stages

```yaml
l4_target_stages:
  - STAGE_06_L4_TRANSITION_REVIEW
  - STAGE_07_MULTI_CORE_RELEASE_PLANNING
  - STAGE_08_MULTI_CORE_PROMOTION_CONTROL
  - STAGE_09_CLOSEOUT_AND_BACKLOG_RESOLUTION
```

## Required validator family

```yaml
future_validators:
  - validate_cross_core_contract_l4_target
  - validate_cross_core_l4_transition_review
  - validate_cross_core_write_surface
  - validate_constitution_referentiel_link_reconstruction
  - validate_link_binding_consistency
  - validate_multi_core_release_plan
  - validate_multi_core_promotion_manifest
  - validate_cross_core_backlog_resolution
```

## Specific treatment of threshold N

The request `CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01` remains proposed / pending arbitration.

```yaml
request_status_preserved:
  request_id: CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01
  status: proposed
  decision_status: pending_arbitration
  threshold_N_materialized_now: false
```

## Non-goals

```yaml
non_goals:
  - activate_L4_now
  - modify_Core_files
  - close_governance_backlog_entries
  - create_release
  - promote_current
  - open_Constitution_run
```


## L4 validator family contract

```yaml
l4_validator_family: docs/pipelines/cross_core_contract/L4_VALIDATOR_FAMILY.md
l4_validator_family_yaml: docs/pipelines/cross_core_contract/validators/l4_validator_family.yaml
l4_validator_family_validation: docs/registry/reports/cross_core_contract_l4_validator_family_validation.yaml
validators_executable_as_l4_gate_now: false
individual_validator_scripts_required_before_L4_execution: true
```

The family contract is part of the L4 target. It defines the validators that must exist and pass before any future L4 execution.

