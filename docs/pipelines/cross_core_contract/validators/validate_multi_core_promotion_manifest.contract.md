# L4 validator contract — validate_multi_core_promotion_manifest

Status: contract defined, inactive
Phase: `PHASE_45_CROSS_CORE_REMAINING_L4_VALIDATOR_CONTRACTS`
Generated at: `2026-04-30T12:26:02Z`

## Purpose

This file defines the contract for the future validator:

```text
validate_multi_core_promotion_manifest
```

Validate the future multi-Core promotion manifest before any current Core promotion.

## What the future validator must prove

```yaml
future_validator_must_prove:
  promotion_manifest_declares_all_impacted_cores: true
  promotion_manifest_references_validated_multi_core_release: true
  promotion_manifest_declares_current_versions: true
  promotion_manifest_declares_target_versions: true
  promotion_manifest_declares_compatibility_matrix: true
  promotion_manifest_declares_validation_reports: true
  promotion_manifest_declares_rollback_or_reconciliation_path: true
  no_promotion_without_release_plan_PASS: true
  no_partial_promotion_for_cross_core_change: true
```

## Current phase posture

```yaml
contract_defined: true
l4_active_now: false
executable_as_l4_gate_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
constitution_run_authorized: false
```
