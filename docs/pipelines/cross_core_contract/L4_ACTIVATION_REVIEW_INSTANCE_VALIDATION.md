# L4 activation review instance validation

Status: validator defined, inactive
Phase: `PHASE_51_CROSS_CORE_L4_ACTIVATION_REVIEW_INSTANCE_VALIDATOR`
Generated at: `2026-04-30T12:49:33Z`

## Purpose

This document records the validator for future real `l4_activation_review` instances.

The validator is tested against the inactive template and must return `BLOCKED_NOT_APPROVED`, proving that the template cannot activate L4.

## Current posture

```yaml
activation_review_instance_validator_defined: true
template_instance_validation_status: BLOCKED_NOT_APPROVED
l4_activation_review_instance_validation_ready: true
l4_activation_ready_now: false
l4_active_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

## Validator

```yaml
validator: docs/patcher/shared/validate_cross_core_l4_activation_review_instance.py
template_smoke_report: docs/registry/reports/l4_activation_review_template_instance_validation.yaml
expected_template_status: BLOCKED_NOT_APPROVED
```
