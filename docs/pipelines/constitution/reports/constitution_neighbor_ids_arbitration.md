# PHASE_16B — Constitution neighbor IDs human arbitration

Status: `PENDING_HUMAN_ARBITRATION`

This document is a human arbitration surface. It does not modify `policy.yaml`, `decisions.yaml`, the scope catalog, governance backlog, maturity scores, or scorer rules.

## Decision values

- `add_as_default_neighbor`: accept adding the ID as an explicit Constitution read neighbor for the scope.
- `defer_to_governance_backlog`: do not patch now; route the candidate to backlog or a later STAGE_00/content review.
- `wont_fix_with_rationale`: explicitly reject the neighbor declaration with a rationale.

## Summary

```yaml
candidate_count: 18
candidate_counts_by_priority:
  P1_blocking_scoring_delta: 9
  P2_non_blocking_scoring_delta: 4
  P3_dependency_explicitness_hygiene: 5
candidate_counts_by_scope:
  deployment_governance: 7
  knowledge_and_design: 2
  learner_state: 2
  mastery_evaluation: 3
  patch_lifecycle: 4
```

## P1 — blocking scoring delta

### NIDG_DEPLOYMENT_GOVERNANCE__ACTION_LOG_UNCOVERED_CONFLICT

- Scope: `deployment_governance`
- Uncovered ID: `ACTION_LOG_UNCOVERED_CONFLICT`
- Owner scope: `patch_lifecycle` via `SGEN_DECISION_005`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by patch_lifecycle and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__INV_GRAPH_PROPAGATION_ONE_HOP

- Scope: `deployment_governance`
- Uncovered ID: `INV_GRAPH_PROPAGATION_ONE_HOP`
- Owner scope: `mastery_evaluation` via `SGEN_DECISION_004`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by mastery_evaluation and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__INV_MSC_AND_STRICT

- Scope: `deployment_governance`
- Uncovered ID: `INV_MSC_AND_STRICT`
- Owner scope: `mastery_evaluation` via `SGEN_DECISION_004`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by mastery_evaluation and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__TYPE_AUTHENTIC_CONTEXT

- Scope: `deployment_governance`
- Uncovered ID: `TYPE_AUTHENTIC_CONTEXT`
- Owner scope: `knowledge_and_design` via `SGEN_DECISION_002`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by knowledge_and_design and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__TYPE_CORPUS_CONFIDENCE_ICC

- Scope: `deployment_governance`
- Uncovered ID: `TYPE_CORPUS_CONFIDENCE_ICC`
- Owner scope: `knowledge_and_design` via `SGEN_DECISION_002`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by knowledge_and_design and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__TYPE_FEEDBACK_COVERAGE_MATRIX

- Scope: `deployment_governance`
- Uncovered ID: `TYPE_FEEDBACK_COVERAGE_MATRIX`
- Owner scope: `knowledge_and_design` via `SGEN_DECISION_002`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by knowledge_and_design and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_DEPLOYMENT_GOVERNANCE__TYPE_SESSION_INTEGRITY_SCORE

- Scope: `deployment_governance`
- Uncovered ID: `TYPE_SESSION_INTEGRITY_SCORE`
- Owner scope: `mastery_evaluation` via `SGEN_DECISION_004`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 19
published_level: L3_operational
```

Report rationale: ID is owned by mastery_evaluation and used by deployment_governance; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_LEARNER_STATE__ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION

- Scope: `learner_state`
- Uncovered ID: `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
- Owner scope: `patch_lifecycle` via `SGEN_DECISION_005`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 15
computed_level: L2_usable_with_care
published_score_total: 17
published_level: L3_operational
```

Report rationale: ID is owned by patch_lifecycle and used by learner_state; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_LEARNER_STATE__ACTION_PLAN_SHORT_DIAGNOSTIC_TASK

- Scope: `learner_state`
- Uncovered ID: `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`
- Owner scope: `mastery_evaluation` via `SGEN_DECISION_004`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: fail
computed_score_total: 15
computed_level: L2_usable_with_care
published_score_total: 17
published_level: L3_operational
```

Report rationale: ID is owned by mastery_evaluation and used by learner_state; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

## P2 — non-blocking scoring delta

### NIDG_PATCH_LIFECYCLE__INV_NO_RUNTIME_CONTENT_GENERATION

- Scope: `patch_lifecycle`
- Uncovered ID: `INV_NO_RUNTIME_CONTENT_GENERATION`
- Owner scope: `deployment_governance` via `SGEN_DECISION_001`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: warn
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 16
published_level: L2_usable_with_care
```

Report rationale: ID is owned by deployment_governance and used by patch_lifecycle; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_PATCH_LIFECYCLE__INV_RUNTIME_FULLY_LOCAL

- Scope: `patch_lifecycle`
- Uncovered ID: `INV_RUNTIME_FULLY_LOCAL`
- Owner scope: `deployment_governance` via `SGEN_DECISION_001`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: warn
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 16
published_level: L2_usable_with_care
```

Report rationale: ID is owned by deployment_governance and used by patch_lifecycle; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_PATCH_LIFECYCLE__TYPE_SELF_REPORT_AR_N1

- Scope: `patch_lifecycle`
- Uncovered ID: `TYPE_SELF_REPORT_AR_N1`
- Owner scope: `learner_state` via `SGEN_DECISION_003`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: warn
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 16
published_level: L2_usable_with_care
```

Report rationale: ID is owned by learner_state and used by patch_lifecycle; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_PATCH_LIFECYCLE__TYPE_STATE_AXIS_VALUE_COST

- Scope: `patch_lifecycle`
- Uncovered ID: `TYPE_STATE_AXIS_VALUE_COST`
- Owner scope: `learner_state` via `SGEN_DECISION_003`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: warn
computed_score_total: 13
computed_level: L2_usable_with_care
published_score_total: 16
published_level: L2_usable_with_care
```

Report rationale: ID is owned by learner_state and used by patch_lifecycle; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

## P3 — dependency explicitness hygiene

### NIDG_KNOWLEDGE_AND_DESIGN__INV_NO_RUNTIME_CONTENT_GENERATION

- Scope: `knowledge_and_design`
- Uncovered ID: `INV_NO_RUNTIME_CONTENT_GENERATION`
- Owner scope: `deployment_governance` via `SGEN_DECISION_001`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: none
computed_score_total: 17
computed_level: L3_operational
published_score_total: 17
published_level: L3_operational
```

Report rationale: ID is owned by deployment_governance and used by knowledge_and_design; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_KNOWLEDGE_AND_DESIGN__TYPE_HUMAN_CHECKPOINT

- Scope: `knowledge_and_design`
- Uncovered ID: `TYPE_HUMAN_CHECKPOINT`
- Owner scope: `deployment_governance` via `SGEN_DECISION_001`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: none
computed_score_total: 17
computed_level: L3_operational
published_score_total: 17
published_level: L3_operational
```

Report rationale: ID is owned by deployment_governance and used by knowledge_and_design; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_MASTERY_EVALUATION__ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION

- Scope: `mastery_evaluation`
- Uncovered ID: `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
- Owner scope: `patch_lifecycle` via `SGEN_DECISION_005`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: none
computed_score_total: 18
computed_level: L3_operational
published_score_total: 18
published_level: L3_operational
```

Report rationale: ID is owned by patch_lifecycle and used by mastery_evaluation; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_MASTERY_EVALUATION__TYPE_INTEGRITY_MODES

- Scope: `mastery_evaluation`
- Uncovered ID: `TYPE_INTEGRITY_MODES`
- Owner scope: `deployment_governance` via `SGEN_DECISION_001`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: none
computed_score_total: 18
computed_level: L3_operational
published_score_total: 18
published_level: L3_operational
```

Report rationale: ID is owned by deployment_governance and used by mastery_evaluation; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

### NIDG_MASTERY_EVALUATION__TYPE_SELF_REPORT_AR_N1

- Scope: `mastery_evaluation`
- Uncovered ID: `TYPE_SELF_REPORT_AR_N1`
- Owner scope: `learner_state` via `SGEN_DECISION_003`
- Recommended decision: `add_as_default_neighbor`
- Human decision: `pending`
- Human rationale: TODO

Source signal:

```yaml
report: docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
axis: dependency_explicitness
scope_delta_severity: none
computed_score_total: 18
computed_level: L3_operational
published_score_total: 18
published_level: L3_operational
```

Report rationale: ID is owned by learner_state and used by mastery_evaluation; declare it as an explicit Constitution read neighbor if the dependency is legitimate.

## How to complete

Edit `docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml`.

For every item:

```yaml
human_decision: add_as_default_neighbor | defer_to_governance_backlog | wont_fix_with_rationale
human_rationale: <non-empty rationale>
patch_policy_decisions_after_approval: true | false
```

Do not patch `policy.yaml` or `decisions.yaml` until the arbitration file is complete and validated.
