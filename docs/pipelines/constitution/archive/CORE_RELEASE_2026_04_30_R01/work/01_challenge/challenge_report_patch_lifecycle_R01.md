# STAGE_01_CHALLENGE — patch_lifecycle

run_id: `CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01`  
pipeline: `constitution`  
mode: `bounded_local_run`  
stage: `STAGE_01_CHALLENGE`  
status: `challenge_report_written`

## 1. Executive summary

Le périmètre `patch_lifecycle` est suffisamment matérialisé pour être challengé en mode borné : les entrées `scope_extract.yaml` et `neighbor_extract.yaml` sont présentes, aucun ID explicitement demandé n'est manquant, et la surface de lecture est compatible avec une exécution ids-first.

Le système est globalement cohérent sur trois piliers :

1. la validation locale des patches doit rester déterministe ;
2. les artefacts de patch et la QA pédagogique doivent être précomputés hors session ;
3. les signaux learner_state consommés par le patch_lifecycle ne doivent pas être recalculés ou interprétés par le patch_lifecycle.

Les risques principaux ne portent donc pas sur une incohérence immédiate de surface, mais sur des zones de conception encore sous-spécifiées : état terminal des patches, priorité ou non-priorité de la file FIFO, paramètre externe `N` côté Référentiel, frontière entre escalation patch_lifecycle et escalation learner_state/governance, et dépendance indirecte non exposée `TYPE_SELF_REPORT_AR_N2` derrière le signal voisin `TYPE_STATE_AXIS_VALUE_COST`.

Conclusion de challenge : **le scope peut avancer vers arbitrage**, mais STAGE_02 doit décider explicitement quelles corrections sont intégrables dans le périmètre `patch_lifecycle` et lesquelles doivent rester en backlog/cross-core follow-up.

## 2. Challenge scope

### 2.1 Read surface declared

Primary reads used:

- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/run_context.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/scope_extract.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/neighbor_extract.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/integration_gate.yaml`

Fallback reads used: **none**.

Fallback IDs declared: **none from extract missing_ids**.

Additional dependency surfaced without fallback read: `TYPE_SELF_REPORT_AR_N2`, referenced as a dependency of neighbor ID `TYPE_STATE_AXIS_VALUE_COST`, but not itself included in `mandatory_reads.ids`. This is not treated as a silent fallback. It is reported as a boundary/scope signal for arbitration.

### 2.2 Writable perimeter

Writable perimeter is limited to `docs/cores/current/constitution.yaml`, modules `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`, and the 22 IDs listed in the run's `scope_manifest.yaml`.

Forbidden operations explicitly in force:

- `direct_current_promotion`
- `silent_out_of_scope_modification`
- `implicit_cross_core_reallocation`

### 2.3 Integration gate reminders

Promotion is blocked until integration checks are cleared. The gate specifically requires attention to deterministic validation, precomputed artifacts, no runtime adaptation drift, learner_state boundary, escalation boundary, and forbidden operations enforcement.

## 3. Detailed analysis by axis

### 3.1 Internal coherence

The core patch lifecycle chain is internally coherent at a high level:

- `TYPE_PATCH_ARTIFACT` requires `TYPE_PATCH_IMPACT_SCOPE`, `TYPE_PATCH_QUALITY_GATE`, and deterministic invariants.
- `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` forbids semantic or pedagogical interpretation during local validation.
- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` aligns with the runtime-local and no-runtime-generation neighbors.
- `INV_NO_PARTIAL_PATCH_STATE`, `EVENT_PATCH_INVALID`, and `ACTION_ROLLBACK_PATCH` form a coherent rejection/rollback safety path.

Main coherence gap: the lifecycle uses several terminal notions (`appliqué`, `rejeté`, `rollbacké`, `bloqué`, rollback non vérifiable, escalation hors session), but there is no single canonical state model describing allowed transitions. The text is coherent enough for a rule-level patch, but fragile for deterministic implementation.

### 3.2 Theoretical soundness

The architecture correctly separates:

- production of learning/state signals outside the patch lifecycle;
- consumption of already-governed signals inside patch governance;
- deterministic runtime verification from off-session semantic/QA assessment.

This is theoretically sound because it prevents local runtime inference from becoming an implicit adaptive pedagogy engine.

Main theoretical weakness: escalation is both a patch lifecycle outcome and a broader governance/learner-state concern. `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION` mentions distress, conservatism without exit and systemic investigation signals, while also stating that these remain external when not directly caused by the patch cycle. This is probably intentional, but it needs a crisp ownership boundary.

### 3.3 Undefined engine states

Potentially undefined or underdefined states:

1. patch queued but underlying learner/state signal disappears before processing;
2. patch active while a higher-severity rollback/escalation condition appears;
3. patch blocked after rollback failure and another trigger arrives;
4. patch applied successfully but the signal persists until the external `N` threshold;
5. off-session escalation opened, but local runtime receives further patch triggers for the same learner.

These states do not necessarily require new runtime behavior in STAGE_01, but they should be arbitrated before patch synthesis if the run intends to touch serialization, rollback, or escalation semantics.

### 3.4 Implicit AI dependencies

The current scope explicitly prevents local AI dependence by requiring deterministic validation and off-session precomputation. However, two implicit-decision risks remain:

- `TYPE_PATCH_QUALITY_GATE` refers to a proof of QA pédagogique but does not name a concrete proof schema in this bounded surface.
- `TYPE_PATCH_IMPACT_SCOPE` is structurally deterministic by diff, but the boundary between structural diff and semantic impact can become ambiguous if future patches affect IDs with cross-core effects.

These are manageable if arbitration limits the patch to deterministic metadata/schema reinforcement, not semantic QA evaluation.

### 3.5 Governance

Governance is strong on forbidden operations and local/global separation. The scope correctly says the impact bundle extends reading, not writing.

Governance risk: the backlog and preflight already indicate that some open items are design follow-ups, not immediate blockers. STAGE_02 must avoid silently transforming backlog signals into local Constitution-only fixes when they are actually referentiel/link or cross-scope design issues.

### 3.6 Adversarial scenarios

Relevant adversarial scenarios:

- A low-severity relevance patch is queued before a critical escalation condition and FIFO delays the critical case.
- A patch artifact claims a valid QA status but its proof is stale, mismatched to source fingerprints, or only semantically asserted.
- A rollback is partial but reports success because verification criteria are underspecified.
- A VC or AR signal is treated as psychological diagnosis despite constraints forbidding autonomous psychological inference.
- A repeated ineffective patch loops locally without reaching off-session escalation because the external `N` threshold is unavailable or ambiguous.

### 3.7 Risk prioritization

| id | priority | finding | scope status | recommended arbitration |
|---|---:|---|---|---|
| CH-PL-01 | P1 | Patch lifecycle has terminal-state vocabulary but no explicit state machine. | in_scope | Decide whether to introduce a minimal canonical patch state model or only harden terminal-state wording. |
| CH-PL-02 | P1 | FIFO serialization may be insufficient for rollback/escalation priority semantics. | in_scope | Decide whether escalation/rollback remains out-of-band, FIFO, or priority-laned. |
| CH-PL-03 | P1 | External parameter `N` for ineffective patch iterations is referenced but not concretely available in the bounded surface. | out_of_scope_but_relevant | Keep as referentiel/link follow-up unless a cross-core read contract is explicitly added. |
| CH-PL-04 | P1 | Escalation boundary crosses patch_lifecycle, learner_state and governance. | needs_scope_extension | Define ownership boundary; do not silently transfer learner_state/governance ownership into patch_lifecycle. |
| CH-PL-05 | P2 | `EVENT_AR_REFRACTORY_PROFILE_DETECTED` and related wording risk psychologizing despite logic forbidding inference. | in_scope | Consider renaming/rewording to observable non-response terminology. |
| CH-PL-06 | P2 | `TYPE_PATCH_QUALITY_GATE` depends on precomputed QA proof, but no proof schema is visible in this bounded surface. | in_scope | Decide whether to add deterministic proof metadata requirements or defer schema definition. |
| CH-PL-07 | P2 | `TYPE_STATE_AXIS_VALUE_COST` depends on `TYPE_SELF_REPORT_AR_N2`, not included in mandatory neighbor reads. | needs_scope_extension | Add/read the dependency in a future scope generation update, or explicitly document why not needed. |
| CH-PL-08 | P3 | `ACTION_LOG_UNCOVERED_CONFLICT` is writable in patch_lifecycle but semantically scoped to runtime_governance. | out_of_scope_but_relevant | Keep if intentional; otherwise split or reassign in a future governance run. |

## 4. Priority risks

### CH-PL-01 — Missing explicit patch state model

Severity: P1  
Scope status: `in_scope`

The scope repeatedly relies on terminal states but does not define a canonical state machine. This is risky because deterministic enforcement needs a closed set of states and transitions. A patch may be applied, rejected, rollbacked, blocked, escalated, ineffective, or partially restored, but the allowed transition graph is implicit.

Arbitrage question: should this run introduce a minimal state model, or only harden the wording around terminal states while leaving full state-machine design for a dedicated run?

### CH-PL-02 — FIFO serialization vs severity/priority semantics

Severity: P1  
Scope status: `in_scope`

`RULE_PATCH_SERIALIZATION` uses FIFO for concurrent patch triggers. FIFO is deterministic, but not necessarily safe if a critical escalation or rollback-related condition must bypass low-priority relevance/AR patches. The current rule partially avoids this by treating rollback as immediate terminal processing, not as a new queued patch. Escalation semantics remain less clear.

Arbitrage question: should escalation be outside the FIFO patch queue, inside FIFO, or governed by deterministic priority lanes?

### CH-PL-03 — External parameter `N`

Severity: P1  
Scope status: `out_of_scope_but_relevant`

`INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` refers to `N` successive patches, where `N` is an external Référentiel parameter. This scope can consume the concept, but cannot safely patch Référentiel/link or invent the parameter locally.

Arbitrage question: should the Constitution entry merely declare an external-read-only dependency, or should this remain a cross-core change request?

### CH-PL-04 — Escalation ownership boundary

Severity: P1  
Scope status: `needs_scope_extension`

The action `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION` includes triggers such as distress, conservatism without exit, systemic investigation, and patch failures. The text correctly says non-patch causes remain external, but this boundary is delicate.

Arbitrage question: should the patch_lifecycle only own escalation caused by patch failure/ineffectiveness, while learner_state/governance own broader escalation sources?

### CH-PL-05 — AR refractory wording

Severity: P2  
Scope status: `in_scope`

The logic forbids psychological inference, but labels such as `AR_REFRACTORY_PROFILE_DETECTED` and human text such as “profil AR-réfractaire” may encourage interpretation. This is a naming/wording risk, not necessarily a logic defect.

Arbitrage question: should these be renamed to observable non-response terminology?

## 5. Scope maturity signals

No maturity score is recalculated or published in this stage.

Positive signals:

- ids-first extraction is ready;
- no requested scope or neighbor ID is missing;
- patch validation determinism is explicit;
- no runtime content generation and local runtime constraints are visible as neighbors;
- integration gate watchpoints are aligned with the actual risks.

Negative or caution signals:

- state-machine semantics are still implicit;
- FIFO queue semantics are deterministic but may be operationally too simple;
- cross-core parameter `N` is not locally resolvable;
- escalation boundary remains cross-scope;
- dependency closure of neighbor IDs is incomplete for `TYPE_STATE_AXIS_VALUE_COST` because `TYPE_SELF_REPORT_AR_N2` is referenced but not read.

Operational maturity signal: `patch_lifecycle` is runnable for bounded challenge and arbitrage, but the next patch should be narrow. A broad patch that tries to solve state machine, priority lanes, escalation boundary and referentiel parameterization at once would likely exceed the safe local scope.

## 6. Corrections to arbitrate before patch

Recommended arbitration candidates:

1. Minimal patch state model: introduce or defer.
2. FIFO/priority policy: keep FIFO, add priority lanes, or mark escalation out-of-band.
3. External parameter `N`: cross-core request vs local external-read-only declaration.
4. Escalation ownership: restrict patch_lifecycle wording to patch-caused failures/ineffectiveness.
5. AR non-response wording: replace psychologizing labels with observable event terminology.
6. QA proof schema: strengthen deterministic required metadata, or defer schema definition.
7. Neighbor dependency closure: decide whether `TYPE_SELF_REPORT_AR_N2` should be part of the mandatory read surface.
8. `ACTION_LOG_UNCOVERED_CONFLICT`: confirm intentional ownership or leave as future governance cleanup.

## 7. Human actions to execute

1. Review this challenge report and decide which findings enter STAGE_02_ARBITRAGE.
2. Do not start patch synthesis from this report directly.
3. If the report is accepted, update run tracking with the canonical command from the stage contract:

```bash
RUN_ID="CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01"

python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id "$RUN_ID" \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_02_ARBITRAGE \
  --summary "Challenge report produced; ready for arbitrage."
```

4. Then sync and continue with STAGE_02_ARBITRAGE only after the tracking command has completed successfully.

## 8. Completion evidence

- `challenge_report_written`: yes
- `read_surface_declared`: yes
- `fallback_ids_declared_if_any`: yes, none used
- `scope_status_declared_for_major_findings`: yes
- `human_actions_explicitly_stated_in_output`: yes
- `scope_maturity_signals_declared_in_bounded_mode`: yes
- `patch_yaml_generation_in_stage_01`: no
- `full_core_read_in_bounded_local_run`: no
