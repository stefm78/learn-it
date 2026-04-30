# Generic execution contract instantiator

Status: instantiator defined, non-mutating  
Phase: `PHASE_57_CROSS_CORE_GENERIC_EXECUTION_CONTRACT_INSTANTIATOR`  
Generated at: `2026-04-30T15:18:25Z`

## Purpose

This phase adds the generic materializer that turns any `cross_core_change_request`
into a concrete `cross_core_execution_contract`.

It does not encode request-specific business logic. It does not authorize writes.

## Current posture

```yaml
generic_execution_contract_instantiator_defined: true
instantiation_smoke_status: BLOCKED_NOT_AUTHORIZED
instantiated_contract_created: true
concrete_request_bound: true
request_specific_logic_encoded: false
l4_control_plane_active_now: true
l4_mutating_execution_framework_ready: true
l4_mutating_gate_active_now: false
l4_core_mutation_authorized_now: false
core_mutation_authorized: false
backlog_closure_authorized: false
release_or_promotion_authorized: false
```

## Generic command

```bash
python docs/patcher/shared/materialize_cross_core_execution_contract.py \
  --request docs/pipelines/cross_core_contract/requests/<REQUEST_ID>.yaml \
  --output docs/pipelines/cross_core_contract/work/03_contract_synthesis/<CONTRACT_ID>.yaml
```

## Boundary

The instantiator creates a request-bound contract, but the first output remains
non-authorized until arbitration, write surface declaration, rollback declaration,
and all required L4 gates pass.
