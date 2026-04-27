# STAGE_01_CHALLENGE — patch_lifecycle bounded local run

Run ID: `CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01`  
Pipeline: `constitution`  
Mode: `bounded_local_run`  
Scope: `patch_lifecycle`  
Stage: `STAGE_01_CHALLENGE`

## 1. Executive summary

The `patch_lifecycle` scope is executable and internally coherent enough to continue to `STAGE_02_ARBITRAGE`, but it carries several high-value arbitration points before any patch synthesis.

The strongest part of the current scope is the separation between:

- patch artifact structure;
- deterministic local validation;
- off-session preparation;
- local rollback/rejection;
- governed patch triggers.

The main challenge is boundary safety. Several entries in `patch_lifecycle` depend on learner-state signals such as VC and AR, but the run currently has only one explicit neighbor ID: `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`. The scope can still be challenged without full-core fallback because all extracted IDs are present, but the arbitration stage should decide whether learner-state trigger dependencies must be converted into explicit read neighbors, backlog items, or cross-scope review items.

No YAML patch is proposed in this stage.

## 2. Challenge scope

### 2.1 Read surface declared

Primary bounded-local inputs read:

- `run_context.yaml`
- `scope_extract.yaml`
- `neighbor_extract.yaml`
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`
- `STAGE_01_CHALLENGE.skill.yaml`

### 2.2 Fallback status

No full-core fallback was used.

Reason: `scope_extract.yaml` reports 22 target IDs found and 0 missing IDs; `neighbor_extract.yaml` reports 1 target ID found and 0 missing IDs. Therefore the stage contract does not justify reading full `constitution.yaml`, `referentiel.yaml`, or `link.yaml`.

### 2.3 Writable perimeter

Writable scope IDs are limited to the 22 IDs declared in the `patch_lifecycle` scope manifest:

- patch artifact structure: `TYPE_PATCH_ARTIFACT`, `TYPE_PATCH_IMPACT_SCOPE`, `TYPE_PATCH_QUALITY_GATE`;
- patch validation invariants: `INV_NO_PARTIAL_PATCH_STATE`, `INV_INVALID_PATCH_REJECTED`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`;
- off-session patch architecture: `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`;
- patch escalation: `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`, `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION`, `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`;
- governed patch triggers: `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`, `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`;
- rollback/invalid patch handling: `EVENT_PATCH_INVALID`, `ACTION_ROLLBACK_PATCH`;
- patch serialization: `RULE_PATCH_SERIALIZATION`;
- protected constraints: `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE`, `CONSTRAINT_NO_ADAPTIVE_PHILOSOPHY_CHANGE`;
- runtime governance trace: `ACTION_LOG_UNCOVERED_CONFLICT`.

Mandatory read neighbor currently extracted:

- `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`.

## 3. Detailed analysis by axis

### 3.1 Internal coherence

The core patch flow is mostly coherent:

1. `TYPE_PATCH_ARTIFACT` depends on `TYPE_PATCH_IMPACT_SCOPE`, `TYPE_PATCH_QUALITY_GATE`, and the explicit referential inter-core reference.
2. Patch validation invariants require atomicity, deterministic validation, impact-scope calculability, and full rejection of invalid patches.
3. `EVENT_PATCH_INVALID` triggers `ACTION_ROLLBACK_PATCH`.
4. `ACTION_ROLLBACK_PATCH` specifies snapshot restoration and traceability.
5. `RULE_PATCH_SERIALIZATION` prevents concurrent patch mutation for the same learner.

This forms a credible local safety model: no partial patch, no non-deterministic local decision, rollback on invalidity, serialized patch execution.

Residual challenge: `TYPE_PATCH_QUALITY_GATE` validates `TYPE_PATCH_ARTIFACT`, while `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` says semantic or pedagogical criteria must not be decided locally. The model is coherent only if the quality gate is explicitly split into:

- deterministic local checks;
- precomputed off-session pedagogical QA evidence.

Without this operational split, the quality gate could reintroduce semantic judgment into local validation.

Scope status: `in_scope`.

### 3.2 Theoretical soundness

The patch lifecycle theory is sound if the system preserves a strict distinction between:

- local application safety;
- off-session pedagogical validation;
- runtime signal detection;
- cross-session correction governance.

The model correctly rejects adaptive philosophy changes and autonomous psychological inference. This prevents patching from becoming an uncontrolled adaptation layer.

Residual challenge: `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION` has a broad trigger: persistent drift, systemic investigation not closed, persistent distress, or conservatism without exit. Some of those causes sound broader than patch lifecycle. The action may be valid in `patch_lifecycle`, but arbitration should verify whether all trigger causes are patch-governance triggers or whether some belong primarily to `learner_state` or another governance scope.

Scope status: `needs_scope_extension` or `out_of_scope_but_relevant` depending on arbitration.

### 3.3 Undefined engine states

The following engine states are underdefined or require arbitration before patch synthesis:

#### UE-01 — Patch active state lifecycle

`RULE_PATCH_SERIALIZATION` says a patch is active until it is applied, rejected, or rollbacked. The extracted scope does not define a first-class lifecycle state such as `pending`, `active`, `applied`, `rejected`, `rollbacked`, `escalated`, or `expired`.

Risk: serialization is conceptually defined, but implementation may later invent implicit states.

Scope status: `in_scope`.

#### UE-02 — Failed rollback state

`ACTION_ROLLBACK_PATCH` requires full snapshot restoration. The extracted scope does not state what happens if rollback itself fails or if restoration cannot be verified deterministically.

Risk: the system forbids partial patch state but does not define the terminal safe state for rollback failure.

Scope status: `in_scope`.

#### UE-03 — Repeated valid-but-ineffective patches

`INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` covers the case where N successive patches of the same type are applied without eliminating the drift signal. The parameter N is delegated to the Referentiel. The extracted neighbor is only the inter-core reference, not the specific parameter ID.

Risk: the rule is operationally dependent on a referential parameter, but the bounded read perimeter does not expose the specific parameter entry.

Scope status: `out_of_scope_but_relevant` with possible `cross_core_change_request` or neighbor selection review.

#### UE-04 — Queue overflow or starvation

`RULE_PATCH_SERIALIZATION` queues concurrent patch triggers FIFO. The extracted scope does not define queue limits, prioritization when safety/escalation competes with relevance patches, or starvation handling.

Risk: FIFO is deterministic but may be pedagogically unsafe if urgent escalation waits behind low-priority relevance patches.

Scope status: `in_scope`.

### 3.4 Implicit AI dependencies

The local patch validation model explicitly forbids semantic or pedagogical interpretation during local validation. This is strong.

However, implicit AI dependency can re-enter through three paths:

1. `TYPE_PATCH_QUALITY_GATE`: if the gate is not materialized as precomputed evidence, local validation may require interpretation.
2. `TYPE_PATCH_IMPACT_SCOPE`: the definition insists that impact_scope is calculated structurally by deterministic diff. This is good, but future patch synthesis must not add semantic impact inference under this label.
3. Patch triggers based on VC and AR: runtime detection may depend on learner-state interpretation. The patch scope should only consume governed signals, not infer psychological states.

Scope status: mixed:

- `TYPE_PATCH_QUALITY_GATE`: `in_scope`;
- learner-state signal production: `out_of_scope_but_relevant`;
- signal consumption by patch triggers: `in_scope`.

### 3.5 Governance

The scope has strong governance guardrails:

- no direct current promotion;
- no silent out-of-scope modification;
- no implicit cross-core reallocation;
- referentiel/link are mandatory reads, not writable surfaces;
- promotion is blocked by the integration gate until checks are cleared.

Residual challenge: `ACTION_LOG_UNCOVERED_CONFLICT` has `scope: runtime_governance`, but is included in the `patch_lifecycle` writable perimeter. This may be valid as a trace action used by patch governance, but it creates a boundary ambiguity with deployment/runtime governance.

Arbitration should decide whether:

- it stays in `patch_lifecycle` as a patch-related logging action;
- it becomes a read neighbor from a governance scope;
- it is split into a generic runtime-governance log action and a patch-specific log action.

Scope status: `needs_scope_extension` or `out_of_scope_but_relevant`.

### 3.6 Adversarial scenarios

#### ADV-01 — Malicious patch claims deterministic validation but hides semantic impact

A patch could pass structural diff while changing behavior in a semantically broad way. `TYPE_PATCH_IMPACT_SCOPE` only captures affected IDs structurally.

Mitigation already present: semantic/pedagogical validation must be off-session.  
Challenge: the off-session QA artifact is not explicitly modeled in the extracted scope.

Scope status: `in_scope`.

#### ADV-02 — Patch trigger loop

Low VC triggers a relevance patch; the patch does not improve VC; another low VC signal triggers another patch. The invariant mentions N ineffective patches before escalation, but the queue and escalation interaction is not fully modeled.

Scope status: `in_scope` plus referentiel neighbor dependency.

#### ADV-03 — AR refractory profile over-adaptation

An AR-refractory profile triggers solicitation patching. Without strict boundaries, this could become autonomous psychological inference or pressure on learner behavior.

Mitigation already present: `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE` and no penalization.  
Challenge: ensure the trigger consumes only explicit AR non-response windows, not inferred psychology.

Scope status: `in_scope` for patch action, `out_of_scope_but_relevant` for signal production.

#### ADV-04 — Rollback trace tampering

Rollback requires traceability, but the extracted scope does not define immutable logging or audit format.

Scope status: `in_scope` or backlog.

### 3.7 Risk prioritization

High-priority risks for arbitration:

1. `RISK_PATCH_QA_SEMANTIC_LEAKAGE`: quality gate may reintroduce local semantic/pedagogical judgment unless represented as precomputed evidence.
2. `RISK_LEARNER_STATE_BOUNDARY_BLUR`: VC/AR patch triggers depend on learner-state IDs not declared as explicit extracted neighbors in this run.
3. `RISK_PATCH_LIFECYCLE_STATES_UNDEFINED`: active/terminal/failed rollback states are not first-class enough for robust serialization and rollback.
4. `RISK_ESCALATION_SCOPE_BLUR`: escalation action contains triggers that may belong partly to learner_state or governance rather than patch_lifecycle.
5. `RISK_REFERENTIEL_PARAMETER_OPACITY`: N-patch escalation parameter is delegated to Referentiel but not explicitly extracted as a concrete neighbor ID.

## 4. Priority risks

### PR-01 — Quality gate must not become local semantic judgment

Severity: high  
Scope status: `in_scope`  
Affected IDs:

- `TYPE_PATCH_QUALITY_GATE`
- `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
- `TYPE_PATCH_ARTIFACT`

Challenge:

The current text is directionally correct but needs arbitration on whether the patch quality gate is represented as:

- a purely local deterministic checklist; or
- a precomputed off-session QA attestation consumed locally; or
- both, with strict separation.

### PR-02 — Learner-state trigger dependencies are not explicit enough

Severity: high  
Scope status: `out_of_scope_but_relevant` / `needs_scope_extension`  
Affected IDs:

- `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
- `EVENT_PERSISTENT_LOW_VC`
- `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`
- `EVENT_AR_REFRACTORY_PROFILE_DETECTED`
- `TYPE_STATE_AXIS_VALUE_COST`
- `TYPE_SELF_REPORT_AR_N1`

Challenge:

The scope entries depend on learner-state IDs, but the current neighbor extract exposes only the inter-core referential reference. Arbitration should determine whether `TYPE_STATE_AXIS_VALUE_COST` and `TYPE_SELF_REPORT_AR_N1` must be declared as explicit read neighbors for this pilot or recorded as follow-up backlog.

### PR-03 — Patch lifecycle state machine is implicit

Severity: medium-high  
Scope status: `in_scope`  
Affected IDs:

- `RULE_PATCH_SERIALIZATION`
- `ACTION_ROLLBACK_PATCH`
- `INV_NO_PARTIAL_PATCH_STATE`
- `EVENT_PATCH_INVALID`

Challenge:

The model states important constraints but does not define a canonical patch state machine. This may be acceptable for the current constitution level, but patch synthesis should not invent state names silently.

### PR-04 — Escalation action may be too broad for patch_lifecycle

Severity: medium  
Scope status: `needs_scope_extension`  
Affected IDs:

- `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
- `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
- `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION`

Challenge:

The action’s trigger includes conditions that may originate outside patch lifecycle. Arbitration should keep the patch-blocked and ineffective-patch cases in scope, but review whether distress/conservatism/systemic investigation clauses are neighbors or cross-scope concerns.

### PR-05 — Referential parameter dependency is under-extracted

Severity: medium  
Scope status: `out_of_scope_but_relevant`  
Affected IDs:

- `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
- `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`
- `PARAM_REFERENTIEL_MAX_PATCH_ITERATIONS_BEFORE_ESCALATION`

Challenge:

The invariant explicitly names a referential parameter, but the bounded read surface only includes the generic inter-core reference. Because referentiel is external_read_only, this should not become a direct Constitution patch, but it may require a neighbor extraction improvement or cross-core follow-up.

## 5. Corrections to arbitrate before patch

No correction is applied in STAGE_01. The following items should be arbitrated in STAGE_02 before any patch synthesis.

### ARB-01 — Define quality gate operational boundary

Decision needed:

Should `TYPE_PATCH_QUALITY_GATE` be clarified as:

1. deterministic local validation only;
2. off-session QA attestation only;
3. a two-layer construct: local deterministic checks plus precomputed off-session QA evidence?

Recommended arbitration direction:

Option 3. It preserves local determinism while keeping pedagogical QA meaningful.

### ARB-02 — Decide explicit learner-state read neighbors for patch triggers

Decision needed:

Should `TYPE_STATE_AXIS_VALUE_COST` and `TYPE_SELF_REPORT_AR_N1` be added as explicit read neighbors for `patch_lifecycle`, or should their absence be tracked as backlog until global neighbor review?

Recommended arbitration direction:

Declare them as explicit read-neighbor candidates, not owned IDs. Do not patch learner_state from this run.

### ARB-03 — Decide whether to model patch lifecycle states

Decision needed:

Should this run introduce or request a canonical type/parameter for patch state lifecycle, or should it only create backlog?

Recommended arbitration direction:

Backlog or minimal in-scope clarification only. Avoid expanding the pilot too much.

### ARB-04 — Narrow escalation trigger semantics

Decision needed:

Should `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION` be narrowed to patch-blocked / ineffective-patch escalation for this scope, while broader distress/conservatism triggers are treated as neighbors or backlog?

Recommended arbitration direction:

Narrow patch lifecycle ownership. Emit backlog/cross-scope review for broader triggers.

### ARB-05 — Handle referentiel parameter dependency without cross-core write

Decision needed:

Should `PARAM_REFERENTIEL_MAX_PATCH_ITERATIONS_BEFORE_ESCALATION` become an explicit external read neighbor or be emitted as a cross-core change request?

Recommended arbitration direction:

Do not patch `referentiel.yaml`. Record explicit neighbor/backlog requirement and keep issue #4 as durable follow-up.

## 6. Human actions to execute

1. Review this challenge report and decide whether it is acceptable as STAGE_01 evidence.
2. If accepted, run the canonical tracking update command:

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_02_ARBITRAGE \
  --summary "Challenge report produced; ready for arbitrage."
```

3. Commit and push the report plus tracking updates.
4. Relaunch the pipeline with:

```text
Continue le run CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 — STAGE_01 est done, démarre STAGE_02_ARBITRAGE.
```

## 7. Completion evidence

- `challenge_report_written`: yes.
- `read_surface_declared`: yes.
- `fallback_ids_declared_if_any`: no fallback; no missing IDs.
- `scope_status_declared_for_major_findings`: yes.
- `human_actions_explicitly_stated_in_output`: yes.

## 8. Stage boundary statement

This report completes the cognitive output expected from `STAGE_01_CHALLENGE` only.

No YAML patch was generated.  
No canonical core was modified.  
No full-core fallback was used.  
No transition to `STAGE_02_ARBITRAGE` was performed by this report.
