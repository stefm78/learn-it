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
- auditable transformations,
- challenge and arbitrage,
- patching,
- validation,
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

### Rule 3 — Derived execution projections must remain strictly conformant
A `validated_derived_execution_projection` may be the only artifact given to an IA for a bounded task, but only if it is validated as strictly conformant to the applicable canon.

### Rule 4 — Multi-IA readiness is a first-rank design constraint
The pipeline must preserve or improve the ability of the Platform Factory to support bounded, parallel work by multiple IAs.

---

## Stage map

### STAGE_00_SCOPE_AND_INPUT_CHECK
**Goal**
- confirm the pipeline intent,
- confirm the governed artifacts,
- confirm the current source inputs.

**Inputs**
- current `platform_factory` artifacts if present,
- canonical foundation,
- architecture planning materials.

**Outputs**
- `work/00_scope/platform_factory_scope_check.md`

---

### STAGE_01_FACTORY_SCAN
**Goal**
- inventory factory-relevant artifacts,
- identify existing architecture/state material,
- map missing pieces before audit.

**Outputs**
- `work/01_scan/platform_factory_inventory.md`

---

### STAGE_02_FACTORY_AUDIT
**Goal**
- audit the Platform Factory as a governed capability,
- assess readiness of the architecture,
- assess minimum produced-application contract,
- assess derived projection fidelity model,
- assess multi-IA parallel readiness.

**Outputs**
- `work/02_audit/platform_factory_audit.md`
- `reports/platform_factory_scorecard.yaml`

---

### STAGE_03_FACTORY_ARBITRAGE
**Goal**
- decide what to correct now,
- decide what to defer,
- decide what belongs to the architecture,
- decide what belongs to the state,
- decide what requires later pipeline/tooling work.

**Outputs**
- `work/03_arbitrage/platform_factory_arbitrage.md`

---

### STAGE_04_FACTORY_PATCH_SYNTHESIS
**Goal**
- synthesize selected changes,
- produce a patchset for `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, or both.

**Outputs**
- `work/04_patch/platform_factory_patchset.yaml`

---

### STAGE_05_FACTORY_PATCH_VALIDATION
**Goal**
- validate patch structure,
- validate architecture/state separation,
- validate consistency of the minimum application contract,
- validate consistency of derived projection rules.

**Outputs**
- `work/05_validation/platform_factory_patch_validation.yaml`
- `reports/platform_factory_patch_validation_report.md`

---

### STAGE_06_FACTORY_APPLY
**Goal**
- apply the patch in a sandbox,
- materialize patched factory artifacts,
- preserve a technical execution trace.

**Outputs**
- `work/06_apply/patched/platform_factory_architecture.yaml`
- `work/06_apply/patched/platform_factory_state.yaml`
- `reports/platform_factory_execution_report.yaml`

---

### STAGE_07_FACTORY_CORE_VALIDATION
**Goal**
- validate the patched `platform_factory` artifacts as a coherent pair,
- validate coherence with canonical foundation,
- validate support for strictly conformant derived projections.

**Outputs**
- `work/07_validation/platform_factory_core_validation.yaml`
- `reports/platform_factory_core_validation_report.md`

---

### STAGE_08_FACTORY_PROMOTION
**Goal**
- promote the validated factory artifacts into `docs/cores/current/` if required,
- preserve explicit traceability of the promotion event.

**Outputs**
- `reports/platform_factory_promotion_report.yaml`

---

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
**Goal**
- archive the run,
- generate a final summary,
- reset working state for the next execution.

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
- `docs/prompts/shared/Make20PlatformFactoryAudit.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

---

## Validation expectations

At minimum, the pipeline must preserve:
- separation between architecture and state,
- strict fidelity requirements for validated derived execution projections,
- explicit dependence on Constitution/Référentiel/LINK,
- minimum produced-application contract integrity,
- multi-IA parallel readiness constraints.

---

## Current V0 posture

This pipeline skeleton is intentionally V0.
It is sufficient to begin challenge and iterative hardening.
It is not yet a fully tooled execution framework.
