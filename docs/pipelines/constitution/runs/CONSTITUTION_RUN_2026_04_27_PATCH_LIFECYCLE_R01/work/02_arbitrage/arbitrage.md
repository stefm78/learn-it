# STAGE_02_ARBITRAGE — patch_lifecycle pilot

Run ID: `CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01`  
Pipeline: `constitution`  
Mode: `bounded_local_run`  
Scope: `patch_lifecycle`  
Stage: `STAGE_02_ARBITRAGE`

## 1. Executive summary

Two STAGE_01 challenge reports were considered:

- `work/01_challenge/challenge_report_patch_lifecycle_r01.md`
- `work/01_challenge/challenge_report_patch_lifecycle_r02.md`

R02 is treated as the stricter consolidation of R01, while R01 remains useful because it expresses the same findings with less severe framing. No significant finding from either report is omitted.

Arbitrage outcome:

- The run may proceed to STAGE_03 only after human validation of this arbitration.
- STAGE_03 must synthesize a narrow local patch only for in-scope Constitution IDs owned by `patch_lifecycle`.
- Scope-generation changes, learner-state neighbor changes, referentiel/link changes, and governance backlog exports are not to be patched directly in STAGE_03.
- The strongest local patch target is the quality-gate / off-session-QA / deterministic-local-validation boundary.
- Several important findings are deliberately converted into governance backlog candidates instead of being silently fixed in this bounded run.

No YAML patch is produced by this stage.

## 2. Scope analysed

### 2.1 Bounded local run surface

The run is scoped to `patch_lifecycle` and may write only the IDs in `scope_manifest.yaml` for this run.

The extracted writable perimeter contains 22 IDs, including patch artifact structure, local validation invariants, rollback, patch serialization, relevance/AR triggers, escalation, and protected constraints.

The mandatory read surface includes `referentiel.yaml` and `link.yaml` as external read-only files, but the only extracted neighbor ID is:

- `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`

### 2.2 Stage input status

- `run_context.yaml`: present.
- `scope_manifest.yaml`: present.
- `impact_bundle.yaml`: present.
- `integration_gate.yaml`: present.
- `challenge_report_patch_lifecycle_r01.md`: present and considered.
- `challenge_report_patch_lifecycle_r02.md`: present and considered.
- `scope_extract.yaml` and `neighbor_extract.yaml`: used as supporting reads because both challenge reports rely on ids-first extract completeness.

No full-core fallback is triggered because both challenge reports declare no missing IDs.

## 3. Detailed arbitrage by finding

### ARB-F01 — Quality gate can leak semantic judgment into local validation

- Challenge source: R01 `PR-01`, R02 `BLOCKER-01`, `IC-02`, `AI-01`.
- Challenge scope status: `in_scope`.
- Related IDs:
  - `TYPE_PATCH_QUALITY_GATE`
  - `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
  - `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
  - `TYPE_PATCH_ARTIFACT`
- Related gate checks:
  - `WP_01`: local validation remains deterministic.
  - `WP_02`: patch artifacts remain precomputed off-session.
- Gate effect: `helps_clear` if patched narrowly; otherwise `keeps_open`.
- Arbitrage decision: `corriger_maintenant`.
- Patch readiness: `ready_for_local_patch`.

Justification:

This is the highest-value in-scope correction. The current model is directionally right, but it can still be misread as allowing the local runtime to perform pedagogical quality judgment. The safe interpretation must be made explicit: the local runtime verifies deterministic evidence, not semantic quality.

Patch instruction for STAGE_03:

Clarify the relevant in-scope entries so that `TYPE_PATCH_QUALITY_GATE` becomes a deterministic local verifier of precomputed off-session QA evidence. The patch should state that local checks may verify presence, integrity, source fingerprint alignment, scope coverage, declared pass/fail status, and version/freshness metadata, but must not perform semantic or pedagogical evaluation locally.

### ARB-F02 — Patch lifecycle consumes learner-state signals but does not own their production

- Challenge source: R01 `PR-02`, R02 `BLOCKER-02`, `TS-01`, `AI-02`.
- Challenge scope status: mixed: `in_scope` for trigger wording, `out_of_scope_but_relevant` for signal production, `needs_scope_extension` for explicit neighbor declaration.
- Related IDs:
  - `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
  - `EVENT_PERSISTENT_LOW_VC`
  - `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`
  - `EVENT_AR_REFRACTORY_PROFILE_DETECTED`
  - `TYPE_STATE_AXIS_VALUE_COST`
  - `TYPE_SELF_REPORT_AR_N1`
- Related gate checks:
  - `WP_03`: patch triggers must not become runtime direct adaptation.
  - `WP_04`: boundary between patch triggers and learner_state.
- Gate effect: `keeps_open` for neighbor declaration; `helps_clear` only for local wording clarifications.
- Arbitrage decision: split decision.
  - Local trigger wording: `corriger_maintenant`.
  - Neighbor declaration / learner-state ownership: `necessite_extension_scope`.
- Patch readiness:
  - Local trigger wording: `ready_for_local_patch`.
  - Neighbor declaration: `blocked_by_scope_extension`.

Justification:

The bounded run may clarify that patch_lifecycle consumes governed upstream signals and never computes learner-state semantics. It must not add learner_state-owned IDs to the patch_lifecycle ownership perimeter and must not patch learner_state. Explicit read-neighbor selection belongs to scope-generation policy/decisions, not this local patch.

Patch instruction for STAGE_03:

For the in-scope trigger rules/events, clarify that VC and AR patch triggers consume explicit, already-governed learner-state signals. Replace any wording that could imply psychological inference or direct runtime adaptation. Do not modify learner_state IDs. Do not modify scope catalog files.

Backlog instruction:

Create a governance backlog candidate for explicit learner-state read-neighbor review for `TYPE_STATE_AXIS_VALUE_COST` and `TYPE_SELF_REPORT_AR_N1`.

### ARB-F03 — Patch lifecycle state machine is implicit

- Challenge source: R01 `PR-03`, `UE-01`; R02 `BLOCKER-03`, `IC-01`.
- Challenge scope status: `in_scope` for minimal semantics; broader state-model formalization may require future expansion.
- Related IDs:
  - `RULE_PATCH_SERIALIZATION`
  - `ACTION_ROLLBACK_PATCH`
  - `INV_NO_PARTIAL_PATCH_STATE`
  - `EVENT_PATCH_INVALID`
- Related gate checks:
  - `WP_01`: deterministic local validation.
  - `FORBIDDEN_OPS_ENFORCEMENT`: no silent out-of-scope modification.
- Gate effect: `helps_clear` if limited to minimal terminal-state wording; `keeps_open` for full state-machine design.
- Arbitrage decision: split decision.
  - Minimal terminal-state clarification: `corriger_maintenant`.
  - Full canonical state machine: `reporter`.
- Patch readiness:
  - Minimal clarification: `ready_for_local_patch`.
  - Full state machine: `decision_only_no_patch_yet`.

Justification:

The pilot should not invent a broad new state-machine type unless necessary. However, STAGE_03 can safely clarify that serialization uses deterministic terminal conditions: applied, rejected, or rollback completed/failed-and-blocked. A future full state model can be tracked separately.

Patch instruction for STAGE_03:

Clarify `RULE_PATCH_SERIALIZATION` and/or rollback-related logic so that a patch is considered non-active only after a deterministic terminal condition is reached. Do not introduce a new top-level state-machine type unless STAGE_03 can do so without scope expansion; default is no new ID.

### ARB-F04 — Rollback failure is undefined

- Challenge source: R01 `UE-02`; R02 `UE-01`, `ARB-R02-04`.
- Challenge scope status: `in_scope`.
- Related IDs:
  - `ACTION_ROLLBACK_PATCH`
  - `INV_NO_PARTIAL_PATCH_STATE`
  - `EVENT_PATCH_INVALID`
- Related gate checks:
  - `WP_01`: deterministic local validation.
  - `FORBIDDEN_OPS_ENFORCEMENT`: no forbidden operation after failure.
- Gate effect: `helps_clear` if patched.
- Arbitrage decision: `corriger_maintenant`.
- Patch readiness: `ready_for_local_patch`.

Justification:

A model that forbids partial patch states must define the safe response when rollback cannot be completed or verified. This is in-scope and directly supports deterministic local safety.

Patch instruction for STAGE_03:

Clarify `ACTION_ROLLBACK_PATCH` so that rollback verification failure leads to a safe blocked state / off-session repair requirement, with no further patch application until integrity is restored. The patch must remain deterministic and must not introduce runtime semantic interpretation.

### ARB-F05 — FIFO serialization may be deterministic but unsafe

- Challenge source: R01 `UE-04`; R02 `UE-02`, `ARB-R02-05`.
- Challenge scope status: `in_scope`.
- Related IDs:
  - `RULE_PATCH_SERIALIZATION`
  - `ACTION_ROLLBACK_PATCH`
  - `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
  - `ACTION_TRIGGER_RELEVANCE_PATCH`
  - `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`
- Related gate checks:
  - `WP_03`: governed patch triggers must not become direct runtime adaptation.
  - `WP_05`: escalation off-session must not be confused with learner-state escalation.
- Gate effect: `requires_human_clearance` if changing FIFO priority semantics; `keeps_open` if deferred.
- Arbitrage decision: `reporter` for priority-lane redesign; `corriger_maintenant` only for a minimal exception that rollback of the active patch is not a queued new patch.
- Patch readiness:
  - Priority redesign: `decision_only_no_patch_yet`.
  - Minimal rollback exception: `ready_for_local_patch` if STAGE_03 can keep it narrow.

Justification:

Changing FIFO to a priority queue may be behaviorally significant and should not be silently introduced. A minimal clarification is acceptable: rollback required by the currently active patch is part of terminal handling, not a new patch that waits behind FIFO queue entries.

Patch instruction for STAGE_03:

Do not redesign FIFO globally. Only clarify, if needed, that rollback/invalidation of the active patch is immediate terminal handling. Defer general patch priority lanes to backlog.

### ARB-F06 — Patch expiration / freshness is undefined

- Challenge source: R02 `UE-03`.
- Challenge scope status: `in_scope`, with possible referential parameter dependency.
- Related IDs:
  - `TYPE_PATCH_ARTIFACT`
  - `TYPE_PATCH_IMPACT_SCOPE`
  - `TYPE_PATCH_QUALITY_GATE`
  - `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
- Related gate checks:
  - `WP_02`: patch artifacts must be precomputed off-session.
  - `WP_01`: deterministic validation.
- Gate effect: `helps_clear` if reduced to fingerprint/freshness metadata; broader policy remains `keeps_open`.
- Arbitrage decision: `corriger_maintenant` for minimal artifact freshness/fingerprint requirement; `reporter` for full expiry policy.
- Patch readiness: `ready_for_local_patch` for minimal metadata; `decision_only_no_patch_yet` for full expiry policy.

Justification:

Precomputed artifacts can become stale. A minimal requirement that patch artifacts carry source fingerprints / validity metadata is consistent with deterministic local validation and does not require broad scope expansion.

Patch instruction for STAGE_03:

Clarify that a patch artifact must carry enough deterministic metadata for the local runtime to verify that the artifact still matches its declared source state and impact scope. Do not define a complete referential expiry policy in this run.

### ARB-F07 — Referential parameter dependency is under-extracted

- Challenge source: R1 `PR-05`, `UE-03`; R2 `GOV-01`, `ARB-R02-06`.
- Challenge scope status: `out_of_scope_but_relevant` and `needs_scope_extension`.
- Related IDs:
  - `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
  - `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`
  - `PARAM_REFERENTIEL_MAX_PATCH_ITERATIONS_BEFORE_ESCALATION`
- Related gate checks:
  - `WP_05`: patch escalation vs learner-state escalation.
  - `FORBIDDEN_OPS_ENFORCEMENT`: no implicit cross-core reallocation.
- Gate effect: `keeps_open` until governance follow-up.
- Arbitrage decision: `necessite_extension_scope`.
- Patch readiness: `blocked_by_scope_extension`.

Justification:

The challenge reports correctly identify that a concrete referential parameter is named but not extracted as a concrete neighbor. Because referentiel/link are external read-only for Constitution runs, STAGE_03 must not patch `referentiel.yaml`. This is a scope-generation / cross-core follow-up matter.

Patch instruction for STAGE_03:

Do not patch referentiel. Do not invent or add referential parameter IDs. At most, keep the Constitution wording compatible with an external parameter and emit backlog/cross-core follow-up.

### ARB-F08 — Escalation action may be too broad for patch_lifecycle

- Challenge source: R01 `PR-04`, theoretical soundness section; R02 `WATCH-01`.
- Challenge scope status: `needs_scope_extension` for broad distress/conservatism/systemic-investigation triggers; `in_scope` for patch-blocked / ineffective-patch escalation.
- Related IDs:
  - `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`
  - `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
  - `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION`
- Related gate checks:
  - `WP_05`: escalation off-session vs learner_state escalation.
- Gate effect: `helps_clear` if patch-owned escalation semantics are narrowed; `keeps_open` for broader trigger ownership.
- Arbitrage decision: split decision.
  - Narrow patch-blocked escalation semantics: `corriger_maintenant`.
  - Broader escalation ownership review: `necessite_extension_scope`.
- Patch readiness:
  - Narrowing: `ready_for_local_patch`.
  - Ownership review: `blocked_by_scope_extension`.

Justification:

Patch lifecycle should own escalation caused by blocked, invalid, impossible, or repeatedly ineffective patches. It should not silently own every distress/conservatism/systemic-investigation trigger if those originate in learner_state or runtime governance.

Patch instruction for STAGE_03:

Clarify in-scope escalation wording so that patch_lifecycle escalation is tied to patch-blocked or patch-ineffective drift. Preserve broader triggers as follow-up/backlog, not local correction.

### ARB-F09 — `ACTION_LOG_UNCOVERED_CONFLICT` has boundary smell

- Challenge source: R01 governance section; R02 `WATCH-02`, `GOV-02`.
- Challenge scope status: `needs_scope_extension` or `out_of_scope_but_relevant`.
- Related ID:
  - `ACTION_LOG_UNCOVERED_CONFLICT`
- Related gate checks:
  - `FORBIDDEN_OPS_ENFORCEMENT`.
- Gate effect: `keeps_open`.
- Arbitrage decision: `reporter` for this pilot, plus backlog candidate.
- Patch readiness: `decision_only_no_patch_yet`.

Justification:

This ID is in the writable perimeter, but its own logic scope says `runtime_governance`. It is not the strongest or safest target for this pilot. Moving it or splitting it would involve broader scope-boundary work. The safe local decision is to avoid patching it now and record boundary debt.

Patch instruction for STAGE_03:

Do not patch `ACTION_LOG_UNCOVERED_CONFLICT` in this pilot unless a later human note explicitly instructs otherwise.

### ARB-F10 — Relevance patch must not become difficulty adaptation

- Challenge source: R02 `TS-02` and adversarial scenarios.
- Challenge scope status: `in_scope`.
- Related IDs:
  - `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
  - `ACTION_TRIGGER_RELEVANCE_PATCH`
  - `CONSTRAINT_NO_ADAPTIVE_PHILOSOPHY_CHANGE`
- Related gate checks:
  - `WP_03`: governed patch triggers must not become direct runtime adaptation.
  - `WP_04`: boundary with learner_state.
- Gate effect: `helps_clear` if patched.
- Arbitrage decision: `corriger_maintenant`.
- Patch readiness: `ready_for_local_patch`.

Justification:

This is a narrow in-scope safety clarification. A relevance patch may alter context, stakes, or authentic-context connection, but must not lower difficulty, mastery thresholds, graph propagation, or evaluation philosophy.

Patch instruction for STAGE_03:

Clarify the relevance patch action/rule to preserve difficulty and mastery semantics.

### ARB-F11 — AR solicitation patch must remain non-punitive and observable

- Challenge source: R02 `ADV-04`, `AI-02`, `TS-01`.
- Challenge scope status: `in_scope` for patch trigger wording; `out_of_scope_but_relevant` for signal production.
- Related IDs:
  - `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH`
  - `EVENT_AR_REFRACTORY_PROFILE_DETECTED`
  - `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`
  - `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE`
- Related gate checks:
  - `WP_03`: no direct runtime adaptation drift.
  - `WP_04`: boundary with learner_state.
- Gate effect: `helps_clear` if patched narrowly.
- Arbitrage decision: `corriger_maintenant`.
- Patch readiness: `ready_for_local_patch`.

Justification:

The wording should avoid any implication that the system diagnoses psychology. The trigger must be framed as an observable non-response window and the solicitation patch must remain non-punitive.

Patch instruction for STAGE_03:

Clarify AR trigger/action wording accordingly without patching learner_state signal definitions.

## 4. Consolidated points

### 4.1 Accepted for local patch synthesis

The following decisions are accepted as STAGE_03 patch inputs:

1. Clarify the patch quality gate as deterministic local verification of precomputed off-session QA evidence.
2. Clarify that patch_lifecycle consumes upstream learner-state signals but does not compute or infer learner-state semantics.
3. Add minimal terminal-state semantics around active patch lifecycle / serialization without introducing a broad new state machine.
4. Define safe deterministic handling for rollback verification failure.
5. Clarify rollback of the active patch as terminal handling, not a queued FIFO patch.
6. Add minimal freshness/fingerprint metadata expectation for precomputed patch artifacts.
7. Narrow patch-owned escalation semantics to patch-blocked / patch-ineffective cases.
8. Clarify that relevance patching must not lower difficulty or modify mastery/evaluation philosophy.
9. Clarify that AR solicitation patching must remain observable, non-punitive, and non-psychological.

### 4.2 Not accepted for local patch synthesis

The following are not accepted as local patch targets in this bounded run:

1. Adding learner_state IDs to `patch_lifecycle` ownership.
2. Modifying `referentiel.yaml` or `link.yaml`.
3. Directly editing generated scope catalog files.
4. Adding concrete referential parameter definitions.
5. Moving or splitting `ACTION_LOG_UNCOVERED_CONFLICT` now.
6. Replacing FIFO with a full priority queue.
7. Introducing a full patch state-machine type unless a later human decision explicitly authorizes it.

### 4.3 Integration gate implications

The local patch can help clear:

- `WP_01` via deterministic validation clarification.
- `WP_02` via off-session QA/fingerprint clarification.
- `WP_03` via trigger wording constraints.
- `WP_04` via explicit boundary between signal consumption and signal production.
- `WP_05` via narrowed patch escalation semantics.

The gate must remain open for:

- explicit learner-state neighbor review;
- referentiel parameter extraction / external-read-only follow-up;
- broader scope-boundary review for `ACTION_LOG_UNCOVERED_CONFLICT`;
- broader escalation ownership review.

## 5. Decisions for patch

```yaml
decisions_for_patch:
  - decision_id: PATCH_DECISION_001
    title: Clarify quality gate as deterministic verifier of off-session QA evidence
    target_ids:
      - TYPE_PATCH_QUALITY_GATE
      - INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC
      - INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION
      - TYPE_PATCH_ARTIFACT
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - no local semantic or pedagogical judgment
      - local runtime may verify deterministic evidence only
      - preserve off-session QA boundary

  - decision_id: PATCH_DECISION_002
    title: Clarify patch triggers as consumption of governed upstream learner-state signals
    target_ids:
      - RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH
      - EVENT_PERSISTENT_LOW_VC
      - RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH
      - EVENT_AR_REFRACTORY_PROFILE_DETECTED
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - do not patch learner_state IDs
      - do not infer psychology
      - do not declare new owners

  - decision_id: PATCH_DECISION_003
    title: Add minimal deterministic terminal handling for active patch lifecycle
    target_ids:
      - RULE_PATCH_SERIALIZATION
      - ACTION_ROLLBACK_PATCH
      - INV_NO_PARTIAL_PATCH_STATE
      - EVENT_PATCH_INVALID
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - do not introduce broad new state machine unless strictly necessary
      - no new scope ownership change

  - decision_id: PATCH_DECISION_004
    title: Define rollback verification failure as safe blocked/off-session repair state
    target_ids:
      - ACTION_ROLLBACK_PATCH
      - INV_NO_PARTIAL_PATCH_STATE
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - deterministic handling only
      - no further patch application until integrity is restored

  - decision_id: PATCH_DECISION_005
    title: Clarify relevance patch boundaries
    target_ids:
      - RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH
      - ACTION_TRIGGER_RELEVANCE_PATCH
      - CONSTRAINT_NO_ADAPTIVE_PHILOSOPHY_CHANGE
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - relevance patch changes context/stakes/authenticity only
      - no difficulty reduction
      - no mastery or evaluation philosophy change

  - decision_id: PATCH_DECISION_006
    title: Clarify AR solicitation patch boundaries
    target_ids:
      - RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH
      - EVENT_AR_REFRACTORY_PROFILE_DETECTED
      - ACTION_TRIGGER_AR_SOLLICITATION_PATCH
      - CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - observable non-response window only
      - non-punitive solicitation changes only
      - no psychological profiling

  - decision_id: PATCH_DECISION_007
    title: Narrow patch-owned escalation semantics
    target_ids:
      - INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED
      - RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION
      - ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION
    decision: corriger_maintenant
    patch_readiness: ready_for_local_patch
    constraints:
      - patch_lifecycle owns patch-blocked and patch-ineffective escalation
      - broader learner-state distress/conservatism escalation remains backlog/scope review
```

## 6. Decisions not retained

```yaml
decisions_not_retained:
  - rejected_decision_id: NOT_RETAINED_001
    title: Patch referentiel parameter definitions directly
    decision: rejeté
    reason: Referentiel is external_read_only for Constitution bounded runs.

  - rejected_decision_id: NOT_RETAINED_002
    title: Add learner_state IDs to patch_lifecycle ownership
    decision: rejeté
    reason: Would violate scope ownership boundaries and create implicit cross-scope reallocation.

  - rejected_decision_id: NOT_RETAINED_003
    title: Directly edit generated scope catalog to add neighbors
    decision: rejeté
    reason: Scope catalog is generated; changes must go through policy/decisions and deterministic regeneration.

  - rejected_decision_id: NOT_RETAINED_004
    title: Move ACTION_LOG_UNCOVERED_CONFLICT during this local patch
    decision: reporter
    reason: Boundary smell is real but moving/splitting ownership is scope-design work, not a narrow patch_lifecycle local patch.

  - rejected_decision_id: NOT_RETAINED_005
    title: Replace FIFO with a complete priority queue
    decision: reporter
    reason: Priority queue semantics may be correct but require human/governance review beyond this pilot patch.
```

## 7. Governance backlog candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_PATCH_LIFECYCLE_LEARNER_STATE_NEIGHBORS_R01
    backlog_entry_type: scope_extension_needed
    title: Review explicit learner_state read neighbors for patch_lifecycle triggers
    related_scope_keys:
      - patch_lifecycle
      - learner_state
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F02
    rationale: >-
      Patch lifecycle trigger rules consume learner-state signals such as value-cost
      and AR non-response, but the current bounded extract exposes only the generic
      referential inter-core reference as neighbor. The ownership must remain in learner_state,
      but explicit read-neighbor selection should be reviewed through scope generation.
    recommended_stage00_action: >-
      Review scope_generation policy/decisions to decide whether TYPE_STATE_AXIS_VALUE_COST
      and TYPE_SELF_REPORT_AR_N1, or equivalent signal IDs, should be declared as explicit
      read neighbors for patch_lifecycle. Regenerate the scope catalog deterministically if approved.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
    backlog_entry_type: scope_gap
    title: Track external_read_only referentiel parameter dependency for patch escalation threshold
    related_scope_keys:
      - patch_lifecycle
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F07
    rationale: >-
      INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED mentions a referential
      parameter controlling the maximum number of ineffective patch iterations before escalation,
      but the bounded neighbor extract only includes the generic Constitution inter-core reference.
      This must not be solved by patching referentiel from this Constitution run.
    recommended_stage00_action: >-
      Coordinate with the external-read-only referentiel/link follow-up and decide whether the
      specific parameter should become a concrete external read neighbor or a cross_core_change_request.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01
    backlog_entry_type: scope_extension_needed
    title: Review broad escalation triggers crossing patch_lifecycle and learner_state/governance
    related_scope_keys:
      - patch_lifecycle
      - learner_state
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F08
    rationale: >-
      Patch-blocked and ineffective-patch escalation belong in patch_lifecycle, but broader
      distress, conservatism-without-exit, and systemic-investigation triggers may belong to
      learner_state or governance boundaries. The pilot should not silently own all such cases.
    recommended_stage00_action: >-
      Revisit escalation ownership during scope partition review, decide explicit owners and neighbors,
      and regenerate scope catalog if boundaries change.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_UNCOVERED_CONFLICT_LOGGING_R01
    backlog_entry_type: partition_angle_mort
    title: Review ACTION_LOG_UNCOVERED_CONFLICT ownership boundary
    related_scope_keys:
      - patch_lifecycle
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F09
    rationale: >-
      ACTION_LOG_UNCOVERED_CONFLICT is owned by the patch_lifecycle writable perimeter,
      but its internal logic scope is runtime_governance. This may be historical or valid,
      but should not be silently reinforced by the pilot patch.
    recommended_stage00_action: >-
      Review whether ACTION_LOG_UNCOVERED_CONFLICT should remain patch_lifecycle-owned,
      become a governance neighbor, or be split into generic and patch-specific logging actions.
    candidate_status: candidate_needs_human_review

  - candidate_id: GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01
    backlog_entry_type: scope_gap
    title: Decide whether patch serialization requires deterministic priority lanes
    related_scope_keys:
      - patch_lifecycle
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F05
    rationale: >-
      FIFO serialization is deterministic but may be unsafe if escalation or rollback-related work
      can starve behind low-priority relevance or solicitation patches. A full priority model should
      not be introduced silently in the pilot.
    recommended_stage00_action: >-
      Evaluate whether patch queue semantics require deterministic priority lanes, and if so define
      them through a governed scope update rather than ad hoc patch synthesis.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01
    backlog_entry_type: scope_gap
    title: Decide whether patch_lifecycle needs a canonical patch state machine
    related_scope_keys:
      - patch_lifecycle
    originating_run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
    source_finding_id: ARB-F03
    rationale: >-
      Minimal terminal semantics can be patched locally, but a full patch state machine with states
      such as pending, active, applied, rejected, rollbacked, failed, expired, or escalated may require
      dedicated canonical design.
    recommended_stage00_action: >-
      Review whether a future patch_lifecycle scope iteration should introduce an explicit patch state model.
    candidate_status: candidate_open
```

## 8. Deferred or blocked decisions

```yaml
deferred_or_blocked_decisions:
  - decision_id: DEFERRED_001
    title: Explicit learner_state neighbor selection
    status: blocked_by_scope_extension
    reason: Requires scope_generation policy/decisions update and deterministic scope catalog regeneration.

  - decision_id: DEFERRED_002
    title: Concrete referentiel parameter extraction
    status: blocked_by_scope_extension
    reason: Referentiel is external_read_only; concrete parameter handling belongs to cross-core follow-up.

  - decision_id: DEFERRED_003
    title: ACTION_LOG_UNCOVERED_CONFLICT ownership change
    status: decision_only_no_patch_yet
    reason: Boundary issue is real but not safe as a local patch target in this pilot.

  - decision_id: DEFERRED_004
    title: Full patch priority queue semantics
    status: decision_only_no_patch_yet
    reason: Could alter runtime behavior too broadly; needs governed review.

  - decision_id: DEFERRED_005
    title: Full patch state machine
    status: decision_only_no_patch_yet
    reason: Minimal terminal semantics may be patched; full state model is deferred.
```

## 9. Ambiguities requiring human decision

No ambiguity blocks producing a local STAGE_03 patch if the human accepts the conservative defaults in this report.

Human validation is still mandatory before transition to STAGE_03 because STAGE_02 is an arbitration stage.

Material defaults selected by this report:

1. Patch quality-gate clarification now.
2. Patch trigger wording now, but do not change learner_state ownership or generated scope catalog.
3. Patch minimal terminal/rollback semantics now, but defer full state machine.
4. Patch narrow patch-blocked escalation wording now, but defer broad escalation ownership review.
5. Do not patch referentiel/link.
6. Do not move `ACTION_LOG_UNCOVERED_CONFLICT` in this run.

If the human disagrees with any of these defaults, STAGE_02 must be revised before STAGE_03.

## 10. Human actions to execute

1. Review this arbitration report.
2. If decisions are accepted, run:

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 \
  --stage-id STAGE_02_ARBITRAGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_03_PATCH_SYNTHESIS \
  --summary "Arbitrage report validated; decisions ready for patch synthesis."
```

3. Commit and push the arbitration report and tracking updates.
4. Continue with:

```text
Continue le run CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01 — STAGE_02 est done, démarre STAGE_03_PATCH_SYNTHESIS.
```

## 11. Completion evidence

- `arbitrage_report_written`: yes.
- `all_challenge_reports_considered`: yes, R01 and R02.
- `every_significant_finding_has_explicit_decision`: yes.
- `every_priority_risk_from_challenge_has_explicit_decision`: yes.
- `every_arbitrage_request_from_challenge_is_resolved`: yes.
- `decisions_for_patch_section_present`: yes.
- `scope_status_declared_per_finding`: yes.
- `human_notes_integrated_if_provided`: no human notes were provided beyond the instruction to continue.
- `ambiguities_explicitly_flagged_if_any`: yes.
- `governance_backlog_candidates_declared_if_needed`: yes.
- `governance_backlog_candidates_serialized_in_yaml_block_if_present`: yes.

## 12. Stage boundary statement

This file is the STAGE_02 arbitration output only.

No patch YAML was generated.  
No Core document was rewritten.  
No generated scope catalog file was modified.  
No governance backlog file was directly updated.  
No deterministic script execution was simulated.  
No transition to STAGE_03 was performed by this report.
