# Platform Factory Pipeline

## Purpose

This pipeline governs the `platform_factory` layer.
It does not instantiate a domain application.
It governs:
- the prescriptive architecture of the Platform Factory,
- the recognized current state of the Platform Factory,
- the rules for validated derived execution projections,
- the generic minimum contract of a produced application.

It keeps the same overall spirit as the `constitution` pipeline:
- explicit stages,
- challenge and arbitrage,
- patching,
- validation,
- release materialization,
- optional promotion,
- cleanup and archive.

---

## Governed artifacts

Primary governed artifacts:
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Related reference inputs:
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/architecture/Platform_Factory_Plan.md`

Non-governed by this pipeline:
- one specific instantiated application,
- domain-specific learning content,
- learner runtime state,
- the future application instantiation pipeline itself.

---

## Operating doctrine

### Rule 1 — No duplication of normative authority
The pipeline must not rewrite the Constitution, the Référentiel or the LINK indirectly.
It may only:
- reference them,
- bind to them,
- derive validated execution projections from them,
- operationalize them for factory-level concerns.

### Rule 2 — Separation of prescriptive and constatative artifacts
- `platform_factory_architecture.yaml` is prescriptive.
- `platform_factory_state.yaml` is constatative.

These two roles must remain separate throughout the pipeline.

### Rule 3 — Released baseline posture
The current `platform_factory` artifacts are considered a released baseline.
A new pipeline run does not start with a discovery audit of an unknown object.
It starts by challenging the released baseline and deciding whether corrections are required.

### Rule 4 — Derived execution projections must remain strictly conformant
A `validated_derived_execution_projection` may be the only artifact given to an IA for a bounded task, but only if it is validated as strictly conformant to the applicable canon.

### Rule 5 — Multi-IA readiness is a first-rank design constraint
The pipeline must preserve or improve the ability of the Platform Factory to support bounded, parallel work by multiple IAs.

### Rule 6 — Release and promotion are distinct acts
Release materialization and promotion to `docs/cores/current/` must remain explicitly separated.
A validated patched state is not yet the promoted current state until a dedicated promotion stage completes.

---

## Stage map

### STAGE_01_CHALLENGE
**Goal**
- challenge the released `platform_factory` baseline,
- identify weaknesses, ambiguities, contradictions, incompletenesses or drifts,
- prepare explicit findings for arbitrage.

**Inputs**
- current `platform_factory` artifacts,
- canonical foundation,
- optional human focus note in `inputs/`.

**Prompt**
- `docs/prompts/shared/Challenge_platform_factory.md`

**Outputs**
- `work/01_challenge/challenge_report_##.md`

---

### STAGE_02_FACTORY_ARBITRAGE
**Goal**
- decide what to correct now,
- decide what to defer,
- decide what belongs to the architecture,
- decide what belongs to the state,
- decide what requires later pipeline/tooling work.

**Inputs**
- challenge reports from `work/01_challenge/`,
- optional human arbitrage notes.

**Prompt**
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

**Rule**
- every `challenge_report*.md` present in `work/01_challenge/` must be considered during arbitrage,
- the arbitrage must consolidate retained, rejected, deferred and out-of-scope findings into a single decision record.

**Outputs**
- `work/02_arbitrage/platform_factory_arbitrage.md`

---

### STAGE_03_FACTORY_PATCH_SYNTHESIS
**Goal**
- synthesize selected changes,
- produce a patchset for `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, or both.

**Inputs**
- current governed artifacts,
- challenge reports,
- arbitrage record.

**Prompt**
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`

**Outputs**
- `work/03_patch/platform_factory_patchset.yaml`

---

### STAGE_04_FACTORY_PATCH_VALIDATION
**Goal**
- validate patch structure,
- validate architecture/state separation,
- validate consistency of the minimum application contract,
- validate consistency of derived projection rules.

**Inputs**
- `work/03_patch/platform_factory_patchset.yaml`,
- `work/02_arbitrage/platform_factory_arbitrage.md` if needed.

**Prompt**
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

**Outputs**
- `work/04_patch_validation/platform_factory_patch_validation.yaml`
- `reports/platform_factory_patch_validation_report.md`

---

### STAGE_05_FACTORY_APPLY
**Goal**
- apply the patch in a sandbox,
- materialize patched factory artifacts,
- preserve a technical execution trace.

**Prompt**
- no specialized prompt required

**Outputs**
- `work/05_apply/patched/platform_factory_architecture.yaml`
- `work/05_apply/patched/platform_factory_state.yaml`
- `reports/platform_factory_execution_report.yaml`

---

### STAGE_06_FACTORY_CORE_VALIDATION
**Goal**
- validate the patched `platform_factory` artifacts as a coherent pair,
- validate coherence with canonical foundation,
- validate support for strictly conformant derived projections.

**Prompt**
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

**Outputs**
- `work/06_core_validation/platform_factory_core_validation.yaml`
- `reports/platform_factory_core_validation_report.md`

---

### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
**Goal**
- materialize a releasable immutable factory artifact set,
- prepare explicit release outputs before any promotion to current,
- preserve traceability between validated patched artifacts and releasable artifacts.

**Prompt**
- no specialized prompt required

**Outputs**
- `work/07_release/platform_factory_release_plan.yaml`
- `reports/platform_factory_release_materialization_report.yaml`
- `outputs/platform_factory_release_candidate_notes.md`

---

### STAGE_08_FACTORY_PROMOTION
**Goal**
- promote the validated released factory artifacts into `docs/cores/current/` if required,
- preserve explicit traceability of the promotion event.

**Prompt**
- no specialized prompt required

**Outputs**
- `reports/platform_factory_promotion_report.yaml`

---

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
**Goal**
- archive the run,
- generate a final summary,
- reset working state for the next execution.

**Prompt**
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

**Outputs**
- `reports/platform_factory_closeout_report.yaml`
- `outputs/platform_factory_summary.md`

---

## Minimal write zones

Expected write zones for this pipeline:
- `docs/pipelines/platform_factory/work/`
- `docs/pipelines/platform_factory/reports/`
- `docs/pipelines/platform_factory/outputs/`
- `docs/pipelines/platform_factory/archive/`

Primary target artifacts:
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

---

## Required shared prompts

Expected shared prompt family:
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

Prompt usage companion:
- `docs/pipelines/platform_factory/PROMPT_USAGE.md`

---

## Validation expectations

At minimum, the pipeline must preserve:
- separation between architecture and state,
- strict fidelity requirements for validated derived execution projections,
- explicit dependence on Constitution/Référentiel/LINK,
- minimum produced-application contract integrity,
- multi-IA parallel readiness constraints.

---

## Success criteria

- No stage may be skipped
- A new run starts from challenge of the released baseline, not from a discovery audit
- No file in `docs/cores/current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under `work/05_apply/`
- Any release materialization should happen before promotion
- Promotion to `current/` must remain explicit and occur in a dedicated stage
- Any successful promotion should be followed by an explicit archive-and-reset closeout stage

---

## Current V0 posture

This pipeline skeleton is intentionally V0.
It is sufficient to begin challenge and iterative hardening.
It is not yet a fully tooled execution framework.
