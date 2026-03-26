# PIPELINE — constitution

id: constitution
version: 1
scope: core-governance

## Goal

Challenger les Core actifs, arbitrer les corrections, produire un patch, le valider, l'appliquer dans une zone de travail et préparer la promotion.

## Canonical resources

### Prompts
- Challenge: `docs/prompts/shared/Challenge_constitution.md`
- Patch synthesis: `docs/prompts/shared/Make05CorePatch.md`
- Patch validation: `docs/prompts/shared/Make06PatchValidation.md`
- Core validation: `docs/prompts/shared/Make02CoreValidation.md`
- Execution review: `docs/prompts/shared/Make08PatchExecutionReview.md`
- Release: `docs/prompts/shared/Make07CoreRelease.md`

### Spec and tools
- Patch DSL: `docs/specs/patch-dsl/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`

### Core inputs
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

## Staging

- inputs: `docs/pipelines/constitution/inputs/`
- work/01_challenge: `docs/pipelines/constitution/work/01_challenge/`
- work/02_arbitrage: `docs/pipelines/constitution/work/02_arbitrage/`
- work/03_patch: `docs/pipelines/constitution/work/03_patch/`
- work/04_patch_validation: `docs/pipelines/constitution/work/04_patch_validation/`
- work/05_apply: `docs/pipelines/constitution/work/05_apply/`
- work/06_core_validation: `docs/pipelines/constitution/work/06_core_validation/`
- work/07_release: `docs/pipelines/constitution/work/07_release/`
- outputs: `docs/pipelines/constitution/outputs/`
- reports: `docs/pipelines/constitution/reports/`

## Stages

### STAGE_01_CHALLENGE
- Inputs:
  - current cores
  - optional focus note in `inputs/`
- Prompt:
  - `docs/prompts/shared/Challenge_constitution.md`
- Output:
  - `work/01_challenge/challenge_report.md`

### STAGE_02_ARBITRAGE
- Inputs:
  - `work/01_challenge/challenge_report.md`
  - optional human arbitrage notes
- Output:
  - `work/02_arbitrage/arbitrage.md`

### STAGE_03_PATCH_SYNTHESIS
- Inputs:
  - current cores
  - challenge report
  - arbitrage
- Prompt:
  - `docs/prompts/shared/Make05CorePatch.md`
- Output:
  - `work/03_patch/patchset.yaml`

### STAGE_04_PATCH_VALIDATION
- Inputs:
  - `work/03_patch/patchset.yaml`
- Tools:
  - `docs/patcher/shared/validate_patchset.py`
  - `docs/prompts/shared/Make06PatchValidation.md`
- Outputs:
  - `work/04_patch_validation/patch_validation.yaml`
  - `reports/patch_validation_report.md`

### STAGE_05_APPLY
- Inputs:
  - validated patchset
- Tool:
  - `docs/patcher/shared/apply_patch.py`
- Outputs:
  - `work/05_apply/patched/`
  - `reports/patch_execution_report.yaml`

### STAGE_06_CORE_VALIDATION
- Inputs:
  - patched cores from Stage 05
- Prompt:
  - `docs/prompts/shared/Make02CoreValidation.md`
- Outputs:
  - `work/06_core_validation/core_validation.yaml`
  - `reports/core_validation_report.md`

### STAGE_07_RELEASE_PLAN
- Inputs:
  - patched validated cores
  - execution report
- Prompt:
  - `docs/prompts/shared/Make07CoreRelease.md`
- Outputs:
  - `work/07_release/release_plan.yaml`
  - `outputs/release_candidate_notes.md`

## Success criteria

- No stage may be skipped
- No file in `current/` may be modified directly by this pipeline
- Promotion is out of scope of this pipeline and must be explicit
