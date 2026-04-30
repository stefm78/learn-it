# L4 validator contract — validate_link_binding_consistency

Status: contract defined, inactive
Phase: `PHASE_43_CROSS_CORE_LINK_BINDING_VALIDATOR_CONTRACT`
Generated at: `2026-04-30T11:47:59Z`

## Purpose

This file defines the contract for the future validator:

```text
validate_link_binding_consistency
```

It guarantees that future cross-core changes have explicit, coherent Link bindings between Constitution and Referentiel before release or promotion.

## What the future validator must prove

```yaml
future_validator_must_prove:
  every_cross_core_reference_has_link_binding: true
  every_link_binding_has_source_core: true
  every_link_binding_has_target_core: true
  every_link_binding_has_source_id: true
  every_link_binding_has_target_id: true
  referentiel_parameter_ids_resolvable: true
  constitution_external_reference_ids_resolvable: true
  no_orphan_link_binding: true
  no_duplicate_link_binding: true
  link_binding_version_compatibility_declared: true
  link_binding_release_impact_declared: true
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
