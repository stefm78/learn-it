# STAGE_01_CHALLENGE — second challenge report for patch_lifecycle pilot

Run ID: `CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01`
Pipeline: `constitution`
Mode: `bounded_local_run`
Scope: `patch_lifecycle`
Stage: `STAGE_01_CHALLENGE`
Report version: `R02`
Intent: stricter adversarial challenge before STAGE_02 arbitration

## 1. Executive summary

This second challenge report deliberately takes a stricter position than the first report.

The `patch_lifecycle` scope is structurally executable, but it should not go directly to patch synthesis without strong arbitration. The pilot is valuable because it exposes the exact boundary pressure we wanted to test: patch triggers, local deterministic validation, off-session QA, learner-state dependencies, rollback, and escalation.

The central challenge is this:

```text
patch_lifecycle owns trigger decisions that depend on learner-state signals,
but the current bounded extract exposes only the inter-core referential reference
as an explicit neighbor.
```

This does not block STAGE_01 because no extracted ID is missing. However, it should strongly constrain STAGE_02. Arbitration must decide whether the current scope partition is sufficient for patch synthesis, or whether the pilot should emit backlog, neighbor review, or cross-core change requests before any YAML patch is synthesized.

This report does not modify any YAML file, does not update tracking, and does not start STAGE_02.

## 2. Challenge scope

### 2.1 Read surface declared

This challenge uses only the bounded-local ids-first inputs:

* `run_context.yaml`
* `scope_extract.yaml`
* `neighbor_extract.yaml`
* `scope_manifest.yaml`
* `impact_bundle.yaml`
* `integration_gate.yaml`
* `STAGE_01_CHALLENGE.skill.yaml`

### 2.2 Fallback status

No full-core fallback was used.

Reason:

* `scope_extract.yaml` contains all 22 target IDs.
* `neighbor_extract.yaml` contains the one declared neighbor ID.
* `missing_ids` is empty in both extracts.

Therefore, reading full `constitution.yaml`, `referentiel.yaml`, or `link.yaml` is not justified by the bounded-local fallback rule.

### 2.3 Writable perimeter reminder

The writable perimeter is limited to the 22 `patch_lifecycle` IDs declared in `scope_manifest.yaml`.

Mandatory reads in `impact_bundle.yaml` extend the reading duty only. They do not grant write permission on `referentiel.yaml` or `link.yaml`.

## 3. Core thesis of the challenge

The current `patch_lifecycle` model is not mainly weak because of missing patch rules. It is weak because it sits at the boundary between four responsibilities that must remain separated:

1. detecting learner-state signals;
2. deciding that a signal should trigger a patch;
3. validating and applying a patch locally;
4. escalating unresolved drift off-session.

The extracted scope owns items from responsibilities 2, 3 and 4. It references responsibility 1 through IDs such as `TYPE_STATE_AXIS_VALUE_COST` and `TYPE_SELF_REPORT_AR_N1`, but these learner-state IDs are not present in the current neighbor extract.

This creates a hidden-coupling risk: the patch scope may appear local and well bounded, while actually relying on semantics produced by another scope.

## 4. Detailed analysis by axis

## 4.1 Internal coherence

### Finding IC-01 — The patch artifact model is coherent but underspecified as a runtime object

The following IDs form a coherent artifact-validation nucleus:

* `TYPE_PATCH_ARTIFACT`
* `TYPE_PATCH_IMPACT_SCOPE`
* `TYPE_PATCH_QUALITY_GATE`
* `INV_NO_PARTIAL_PATCH_STATE`
* `INV_INVALID_PATCH_REJECTED`
* `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
* `EVENT_PATCH_INVALID`
* `ACTION_ROLLBACK_PATCH`

The model is directionally strong: every patch must have a calculable impact scope, invalid patches are rejected, local validation must remain deterministic, partial states are forbidden, and rollback is required when application fails.

Challenge:

The model does not define a first-class patch lifecycle state. It speaks about active patches, applied patches, rejected patches, rollbacked patches and queued patches, but those states are not represented as explicit canonical IDs in the extracted scope.

Why this matters:

`RULE_PATCH_SERIALIZATION` depends on knowing when a patch is active and when it reaches a terminal state. Without explicit state semantics, downstream stages may invent state names or termination rules during patch synthesis.

Scope status: `in_scope`.

Recommended arbitration:

Do not necessarily add a full state machine in this pilot, but require STAGE_02 to decide whether this becomes:

* an in-scope minimal clarification;
* a backlog item;
* or a deferred future scope expansion.

### Finding IC-02 — `TYPE_PATCH_QUALITY_GATE` is the most dangerous ambiguity

`TYPE_PATCH_QUALITY_GATE` validates `TYPE_PATCH_ARTIFACT`.

At the same time, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` forbids local semantic, pedagogical or interpretive criteria.

Challenge:

A quality gate can be deterministic only if the local runtime checks a precomputed attestation or fixed checklist. If the local runtime evaluates pedagogical quality itself, the model violates its own deterministic validation invariant.

Scope status: `in_scope`.

Recommended arbitration:

STAGE_02 should treat this as a blocking arbitration item.

Safest direction:

```text
TYPE_PATCH_QUALITY_GATE =
deterministic local verifier of precomputed off-session QA evidence
```

The local runtime may verify presence, integrity, version, scope, signature/fingerprint, and declared pass/fail status. It must not decide pedagogical quality semantically.

## 4.2 Theoretical soundness

### Finding TS-01 — The patch layer risks becoming a hidden adaptation layer

The scope includes explicit constraints:

* `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE`
* `CONSTRAINT_NO_ADAPTIVE_PHILOSOPHY_CHANGE`

These are strong guardrails. However, the same scope includes trigger rules based on persistent low VC and AR-refractory profile:

* `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
* `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`

Challenge:

If those triggers consume only explicit upstream signals, they are acceptable. If they infer motivation, psychology or learner intent directly, they undermine the constraints.

Scope status: mixed.

* trigger decision: `in_scope`;
* signal production and interpretation: `out_of_scope_but_relevant`.

Recommended arbitration:

STAGE_02 should require a strict wording distinction:

```text
patch_lifecycle consumes governed learner-state signals;
patch_lifecycle does not compute or infer learner-state semantics.
```

### Finding TS-02 — Relevance patching must not become difficulty adaptation

The low-VC rule states that persistent low VC triggers relevance/context patching, not difficulty reduction.

This is theoretically sound.

Challenge:

The patch output path must preserve this prohibition. `ACTION_TRIGGER_RELEVANCE_PATCH` should never authorize simplification, lowering mastery requirements, or changing evaluation philosophy.

Scope status: `in_scope`.

Recommended arbitration:

Make this a later validation gate: every relevance patch should prove that it modifies contextualization, enjeux or authentic context, but not difficulty, mastery thresholds, graph propagation, or evaluation logic.

## 4.3 Undefined engine states

### Finding UE-01 — Rollback failure is not defined

`ACTION_ROLLBACK_PATCH` says the snapshot must be restored and no partial write may remain.

This is good, but it does not define the engine behavior if rollback cannot be completed or verified.

Challenge:

A constitution that forbids partial state must also define the safe terminal behavior when rollback verification fails.

Possible safe outcomes:

* enter a blocked local state;
* mark the patch as failed and require off-session repair;
* emit a minimal emergency diagnostic payload;
* disable further patch application until state integrity is restored.

Scope status: `in_scope`.

Recommended arbitration:

Add a backlog or in-scope clarification for rollback failure. Do not leave it implicit.

### Finding UE-02 — FIFO serialization may be deterministic but unsafe

`RULE_PATCH_SERIALIZATION` chooses FIFO for concurrent patch triggers.

Challenge:

FIFO is deterministic, but not necessarily safe. A low-priority relevance patch could block an urgent rollback or escalation if all triggers share one queue.

Scope status: `in_scope`.

Recommended arbitration:

Decide whether FIFO is absolute, or whether there are deterministic priority lanes for:

* rollback;
* invalid patch handling;
* escalation;
* relevance/solicitation patching.

If priority is introduced, it must remain rule-based and deterministic. It must not rely on semantic judgment at runtime.

### Finding UE-03 — Patch expiration is undefined

The scope defines active and queued patches but not patch expiry.

Challenge:

A patch generated off-session may become stale if the underlying learner state, referential parameters, source fingerprints, or target IDs change before application.

Scope status: `in_scope` or `out_of_scope_but_relevant`, depending on whether expiry policy is local or referential.

Recommended arbitration:

Decide whether patch artifacts require freshness metadata, source fingerprints, or validity windows before application.

## 4.4 Implicit AI dependencies

### Finding AI-01 — Off-session QA is not the same as local AI-free execution

The constitution can allow off-session QA, but the local runtime must remain deterministic.

The extracted scope says patch artifacts must be precomputed off-session, but it does not fully define the artifact evidence consumed locally.

Challenge:

Without a concrete attestation model, downstream implementation may blur the boundary between precomputed QA and local evaluation.

Scope status: `in_scope`.

Recommended arbitration:

Define or backlog a minimal `patch_qa_evidence` concept.

For this pilot, it may be safer to emit backlog rather than add a new canonical type immediately.

### Finding AI-02 — AR-refractory detection risks becoming psychological inference

The rule says AR-refractory profile triggers solicitation patching. That is acceptable only if `AR-refractory` means a purely observable non-response pattern over an explicit window.

Challenge:

The term `profile` can invite interpretation. It should not imply a psychological diagnosis, intent, resistance, motivation, or character trait.

Scope status:

* patch trigger wording: `in_scope`;
* signal generation: `out_of_scope_but_relevant`.

Recommended arbitration:

Clarify that the trigger consumes an explicit non-response window signal, not a psychological profile.

## 4.5 Governance

### Finding GOV-01 — External read-only rules are respected, but operational dependency is still under-modeled

The run correctly treats `referentiel.yaml` and `link.yaml` as read-only external cores.

The neighbor extract includes only:

* `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`

Challenge:

Some extracted entries refer to concrete referential concepts, especially the maximum number of ineffective patches before escalation. The current extract does not expose the concrete parameter entry.

Scope status: `out_of_scope_but_relevant`.

Recommended arbitration:

Do not patch `referentiel.yaml`.

Instead, STAGE_02 should decide whether to:

* emit a `cross_core_change_request`;
* record backlog against issue #4;
* add explicit read neighbor selection in future scope generation;
* or accept the generic inter-core reference as sufficient for this pilot.

### Finding GOV-02 — `ACTION_LOG_UNCOVERED_CONFLICT` is suspicious in this scope

`ACTION_LOG_UNCOVERED_CONFLICT` has `scope: runtime_governance`, but is owned by the `patch_lifecycle` run.

Challenge:

This may be historically justified, but it is a boundary smell. Logging uncovered conflicts sounds closer to runtime/deployment governance than patch lifecycle.

Scope status: `needs_scope_extension` or `out_of_scope_but_relevant`.

Recommended arbitration:

STAGE_02 should not silently keep or patch this item without deciding one of:

1. it is genuinely a patch-lifecycle log action;
2. it is a shared runtime-governance neighbor;
3. it needs a future scope split;
4. it stays for now but is marked as boundary debt.

## 4.6 Adversarial scenarios

### Scenario ADV-01 — Semantic payload hidden in structural impact scope

A patch declares a deterministic structural impact scope, but the actual behavioral impact is broader than the affected IDs suggest.

Risk:

The runtime accepts a patch because its structural diff is valid, while the pedagogical consequence is unsafe.

Required mitigation:

Local validation must only accept patches with precomputed off-session QA evidence tied to the exact structural diff and source fingerprints.

### Scenario ADV-02 — Patch loop masks persistent design failure

Low VC triggers a relevance patch. The relevance patch is valid but ineffective. The system repeats this several times, then finally escalates.

Risk:

The learner experiences repeated ineffective changes before escalation, while the system remains technically compliant.

Required mitigation:

The escalation threshold must be explicit, bounded, and auditable. If the threshold is referential, the referential parameter must be traceable from the patch lifecycle rule.

### Scenario ADV-03 — Queue determinism causes safety starvation

FIFO serialization makes execution deterministic, but a less urgent patch blocks a more important rollback or escalation.

Risk:

The constitution preserves determinism while violating operational safety priorities.

Required mitigation:

Arbitrate whether rollback and escalation bypass ordinary FIFO patch queues.

### Scenario ADV-04 — AR solicitation patch becomes pressure mechanism

A learner does not answer AR prompts. The system repeatedly modifies solicitation strategy. Without constraints, this can become pressure rather than support.

Risk:

The model violates non-penalization and no psychological inference constraints.

Required mitigation:

AR solicitation patches must be bounded, non-punitive, and based only on explicit observable non-response windows.

### Scenario ADV-05 — Rollback succeeds technically but audit trace is absent

A patch is rolled back, but the rollback report is incomplete or not linked to the patch artifact.

Risk:

The runtime state is safe, but governance cannot prove what happened.

Required mitigation:

Rollback trace requirements should be explicit enough for later deterministic validation.

## 5. Priority risks

### BLOCKER-01 — Quality gate boundary not explicit enough

Severity: high
Scope status: `in_scope`
Primary IDs:

* `TYPE_PATCH_QUALITY_GATE`
* `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
* `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`

Arbitration requirement:

Before patch synthesis, decide how local deterministic validation consumes off-session QA evidence.

### BLOCKER-02 — Learner-state dependencies are not extracted as concrete neighbors

Severity: high
Scope status: `out_of_scope_but_relevant`
Primary IDs:

* `TYPE_STATE_AXIS_VALUE_COST`
* `TYPE_SELF_REPORT_AR_N1`
* `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
* `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`

Arbitration requirement:

Decide whether this pilot may proceed with generic inter-core/referential neighbor only, or whether explicit learner-state neighbors must be introduced as backlog or scope-generation change.

### BLOCKER-03 — Patch lifecycle state semantics are implicit

Severity: medium-high
Scope status: `in_scope`
Primary IDs:

* `RULE_PATCH_SERIALIZATION`
* `ACTION_ROLLBACK_PATCH`
* `INV_NO_PARTIAL_PATCH_STATE`

Arbitration requirement:

Decide whether the pilot will patch state semantics, emit backlog, or keep this as known debt.

### WATCH-01 — Escalation may cross scope boundaries

Severity: medium
Scope status: `needs_scope_extension`
Primary IDs:

* `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
* `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
* `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION`

Arbitration requirement:

Keep patch-blocked escalation in scope, but review distress/conservatism/systemic investigation clauses as possible cross-scope dependencies.

### WATCH-02 — Governance logging boundary unclear

Severity: medium
Scope status: `needs_scope_extension`
Primary ID:

* `ACTION_LOG_UNCOVERED_CONFLICT`

Arbitration requirement:

Decide whether it remains owned by `patch_lifecycle` or becomes a boundary/backlog issue.

## 6. Corrections to arbitrate before patch

### ARB-R02-01 — Quality gate model

Question:

Should the constitution clarify the quality gate as a local deterministic verifier of precomputed off-session QA evidence?

Recommended answer:

Yes. This is the most important in-scope clarification.

### ARB-R02-02 — Learner-state neighbor declaration

Question:

Should learner-state trigger dependencies become explicit read neighbors for `patch_lifecycle`?

Recommended answer:

Yes, but not by directly patching `learner_state` in this run. Either emit a scope-generation follow-up or formal backlog item.

### ARB-R02-03 — Patch state lifecycle

Question:

Should this pilot define minimal patch states?

Recommended answer:

Probably backlog first, unless STAGE_02 decides that serialization cannot be made safe without minimal state semantics.

### ARB-R02-04 — Rollback failure

Question:

Should rollback failure be explicitly handled?

Recommended answer:

Yes. A forbidden partial state needs a safe behavior when rollback cannot be verified.

### ARB-R02-05 — FIFO versus priority

Question:

Should all patches share FIFO, or should rollback/escalation have deterministic priority?

Recommended answer:

Arbitrate carefully. If priority is introduced, it must be deterministic and rule-based.

### ARB-R02-06 — External referential parameter dependency

Question:

Should referential parameters mentioned by patch rules be concrete read neighbors?

Recommended answer:

Record as external-read-only follow-up. Do not patch `referentiel.yaml` in this Constitution run.

## 7. Human actions to execute

1. Review this second challenge report alongside the first one.
2. Decide whether R02 supersedes R01 for STAGE_02 input, or whether both reports are accepted as STAGE_01 evidence.
3. Save this file as:

```text
docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01/work/01_challenge/challenge_report_patch_lifecycle_r02.md
```

4. Commit and push the report.
5. Then run the canonical tracking update command once only:

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

6. Commit and push the tracking updates.
7. Relaunch with:

```text
Continue le run CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 — STAGE_01 est done, démarre STAGE_02_ARBITRAGE.
```

## 8. Completion evidence

* `challenge_report_written`: yes, once saved in the path above.
* `read_surface_declared`: yes.
* `fallback_ids_declared_if_any`: no fallback; no missing IDs.
* `scope_status_declared_for_major_findings`: yes.
* `human_actions_explicitly_stated_in_output`: yes.

## 9. Stage boundary statement

This report is a second STAGE_01 challenge output only.

No YAML patch was generated.
No canonical core was modified.
No full-core fallback was used.
No tracking update was performed by this report.
No transition to `STAGE_02_ARBITRAGE` was performed.
