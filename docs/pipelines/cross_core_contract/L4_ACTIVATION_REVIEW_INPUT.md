# Cross-core L4 activation review input contract

Status: contract defined, inactive
Phase: `PHASE_50_CROSS_CORE_L4_ACTIVATION_REVIEW_INPUT_CONTRACT`
Generated at: `2026-04-30T12:47:07Z`

## Purpose

This document defines the mandatory input shape for a future L4 activation review.

It does not activate L4. It only defines what a future human-authorized activation review must contain before any L4 gate may become executable.

## Required posture

```yaml
l4_activation_input_contract_defined: true
l4_activation_review_materialized_now: false
l4_activation_ready_now: false
l4_active_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

## Mandatory activation review fields

```yaml
required_fields:
  - review_id
  - request_id
  - explicit_human_decision
  - decision_timestamp
  - requested_l4_scope
  - declared_read_surface
  - declared_write_surface
  - impacted_cores
  - required_validators
  - validator_execution_plan
  - release_and_promotion_plan
  - backlog_resolution_plan
  - rollback_or_reconciliation_path
  - non_goals_and_forbidden_mutations
  - activation_guardrails
```

## Required validators

- `validate_cross_core_l4_transition_review`
- `validate_cross_core_write_surface`
- `validate_constitution_referentiel_link_reconstruction`
- `validate_link_binding_consistency`
- `validate_multi_core_release_plan`
- `validate_multi_core_promotion_manifest`
- `validate_cross_core_backlog_resolution`
- `validate_cross_core_rollback_or_reconciliation_path`

## Required human decision shape

```yaml
explicit_human_decision:
  decision: approve_l4_activation_review | reject_l4_activation_review
  decision_maker: <human>
  rationale: <required>
  confirms_no_implicit_core_mutation: true
  confirms_no_implicit_backlog_closure: true
  confirms_no_implicit_release_or_promotion: true
```

## Blocking rule

Any future review missing this shape must block L4 activation.
