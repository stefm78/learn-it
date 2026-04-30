# Generic gate execution runner

Status: runner defined, non-mutating
Phase: `PHASE_58_CROSS_CORE_GENERIC_GATE_EXECUTION_RUNNER`
Generated at: `2026-04-30T15:28:01Z`

## Purpose

This phase adds the generic runner that receives a `cross_core_execution_contract` and decides whether downstream gates may run.

It is request-independent and contains no logic specific to any business request.

## Current posture

```yaml
generic_gate_execution_runner_defined: true
gate_execution_smoke_status: BLOCKED_NOT_AUTHORIZED
downstream_gates_executed_on_smoke: false
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
python docs/patcher/shared/run_cross_core_gate_execution.py \
  --contract docs/pipelines/cross_core_contract/work/03_contract_synthesis/<CONTRACT_ID>.yaml \
  --contract-validation-report docs/pipelines/cross_core_contract/reports/<CONTRACT_ID>_contract_validation.yaml \
  --report docs/pipelines/cross_core_contract/reports/<CONTRACT_ID>_gate_execution.yaml
```

## Gate order

1. `validate_cross_core_execution_contract`
2. `validate_cross_core_l4_transition_review`
3. `validate_cross_core_write_surface`
4. `validate_cross_core_rollback_or_reconciliation_path`
5. `validate_link_binding_consistency`
6. `validate_constitution_referentiel_link_reconstruction`
7. `validate_multi_core_release_plan`
8. `validate_multi_core_promotion_manifest`
9. `validate_cross_core_backlog_resolution`

The runner blocks before downstream gates when the contract is not authorized.
