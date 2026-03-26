# PIPELINE — release

id: release
version: 1
scope: promotion-and-version-sync

## Goal

Synchroniser les versions internes, les références inter-Core, les alias `current/`, les `releases/` et produire une note de release.

## Canonical resources

### Prompts
- Release prompt: `docs/prompts/shared/Make07CoreRelease.md`
- Execution review: `docs/prompts/shared/Make08PatchExecutionReview.md`

### Spec and tools
- Patch DSL: `docs/specs/patch-dsl/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`

## Inputs

- release candidate from `docs/pipelines/constitution/outputs/`
- release plan in `docs/pipelines/constitution/work/07_release/release_plan.yaml`

## Staging

- inputs: `docs/pipelines/release/inputs/`
- work/01_review: `docs/pipelines/release/work/01_review/`
- work/02_patch: `docs/pipelines/release/work/02_patch/`
- work/03_validation: `docs/pipelines/release/work/03_validation/`
- work/04_promotion: `docs/pipelines/release/work/04_promotion/`
- outputs: `docs/pipelines/release/outputs/`
- reports: `docs/pipelines/release/reports/`

## Stages

### STAGE_01_REVIEW
- Review release candidate and execution report
- Output: `work/01_review/release_review.md`

### STAGE_02_RELEASE_PATCH
- Produce release patchset for version bump and alias sync
- Output: `work/02_patch/release_patchset.yaml`

### STAGE_03_VALIDATION
- Validate release patchset and candidate
- Output: `work/03_validation/release_patch_validation.yaml`

### STAGE_04_PROMOTION
- Promote validated candidate to `docs/cores/current/` and `docs/cores/releases/`
- Outputs:
  - `outputs/release_notes.md`
  - `reports/promotion_report.yaml`

## Success criteria

- Internal core metadata and filenames must be synchronized
- No promotion without validated release plan
