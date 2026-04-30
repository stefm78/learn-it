# Generic mutating execution framework

Status: framework defined, non-mutating
Phase: `PHASE_56_CROSS_CORE_GENERIC_MUTATING_EXECUTION_FRAMEWORK`
Generated at: `2026-04-30T14:53:39Z`

## Purpose

This document adds the generic execution layer for `cross_core_contract`.

It is request-independent: it applies to any future `cross_core_change_request`, not to a specific candidate request.

## Current posture

```yaml
generic_mutating_execution_framework_defined: true
cross_core_execution_contract_schema_defined: true
cross_core_execution_contract_validator_defined: true
template_validation_status: BLOCKED_TEMPLATE_ONLY
l4_control_plane_active_now: true
l4_mutating_execution_framework_ready: true
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

## Generic flow

```text
cross_core_change_request
  -> source evidence review
  -> arbitration
  -> cross_core_execution_contract
  -> generic contract validation
  -> L4 gate execution
  -> apply only if every gate passes
  -> release / promotion planning
  -> backlog resolution policy
```

## Generic artifacts

```yaml
schema: docs/pipelines/cross_core_contract/schemas/cross_core_execution_contract.schema.yaml
template: docs/pipelines/cross_core_contract/templates/cross_core_execution_contract.template.yaml
validator: docs/patcher/shared/validate_cross_core_execution_contract.py
template_validation_report: docs/registry/reports/cross_core_execution_contract_template_validation.yaml
framework_validation_report: docs/registry/reports/cross_core_generic_mutating_execution_framework_validation.yaml
```

## Required validators

- `validate_cross_core_execution_contract`
- `validate_cross_core_l4_transition_review`
- `validate_cross_core_write_surface`
- `validate_cross_core_rollback_or_reconciliation_path`
- `validate_link_binding_consistency`
- `validate_constitution_referentiel_link_reconstruction`
- `validate_multi_core_release_plan`
- `validate_multi_core_promotion_manifest`
- `validate_cross_core_backlog_resolution`

## Boundary

```yaml
allowed_now:
  - define generic execution contracts
  - validate template contracts as blocked
  - validate future concrete execution contracts
forbidden_now:
  - apply Core writes from the template
  - close backlog entries from the template
  - materialize releases from the template
  - promote current Core from the template
```
