# Pipeline hardening checklist

Use this checklist before declaring a pipeline hardened.

## Identification

```yaml
pipeline_id:
risk_level: L1 | L2 | L3 | L4
canonical_write_surface: none | reports | state | generated_catalog | core | release | promotion
```

## Minimum checklist

### L1 — Exploratory

- [ ] `pipeline.md` exists.
- [ ] Goal is explicit.
- [ ] Non-goals are explicit.
- [ ] Outputs are declared.
- [ ] Canonical writes are forbidden or absent.

### L2 — Governed diagnostic

- [ ] `state.yaml` or equivalent status surface exists.
- [ ] Reports have status values.
- [ ] A validation script exists.
- [ ] Validation report path is declared.
- [ ] Mutation policy is explicit.
- [ ] Forbidden write surface is explicit.

### L3 — Managed execution

- [ ] Entry actions exist.
- [ ] Run/request id semantics are explicit.
- [ ] Materialization step exists.
- [ ] Generated state files have owner scripts.
- [ ] AI direct writes to owned state are forbidden.
- [ ] Stage contracts exist.
- [ ] Stage completion evidence is machine-checkable or explicitly inspectable.
- [ ] Recovery/reconciliation behavior is defined.

### L4 — Critical canonical

- [ ] AI protocol exists and is authoritative.
- [ ] Required scripts cannot be simulated.
- [ ] Baseline capture exists when before/after matters.
- [ ] Pre-release or pre-apply preview exists when release/write decision matters.
- [ ] Final closeout/evolution report exists.
- [ ] Release/promotion authority is explicit.
- [ ] Backlog closure rules are explicit.
- [ ] Core writes require explicit execution authorization.
- [ ] Human decision points are explicit.
- [ ] Local success is not treated as global consistency.

## Decision gates

```yaml
can_open:
  requires:
    - entry_decision
    - no_conflicting_active_run_or_request
    - required_preflight_if_applicable

can_materialize:
  requires:
    - entry_authorized
    - deterministic_materialization_script

can_execute_stage:
  requires:
    - declared_primary_reads_available
    - previous_stage_evidence_available

can_release:
  requires:
    - release_plan
    - release_plan_validation
    - pre_release_preview_if_applicable

can_promote:
  requires:
    - release_materialized
    - manifest_validated
    - promotion_script
    - promotion_report_validation

can_close:
  requires:
    - final_summary
    - closeout_report
    - backlog_export_or_absence_declared
    - final_score_or_evidence_report_if_applicable
```

## Reviewer summary

```yaml
review_result:
  status: PASS | WARN | FAIL
  recommended_level:
  current_level:
  missing_controls:
  blocking_findings:
  non_blocking_findings:
```
