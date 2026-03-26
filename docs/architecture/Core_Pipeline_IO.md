# Core Pipeline IO

## Global flow

1. Challenge
2. Arbitrage
3. Patch synthesis
4. Patch validation
5. Dry-run / apply
6. Core validation
7. Release plan
8. Promotion

## Constitution pipeline

### Inputs
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- optional note in `docs/pipelines/constitution/inputs/`

### Outputs
- `docs/pipelines/constitution/work/01_challenge/challenge_report.md`
- `docs/pipelines/constitution/work/02_arbitrage/arbitrage.md`
- `docs/pipelines/constitution/work/03_patch/patchset.yaml`
- `docs/pipelines/constitution/work/04_patch_validation/patch_validation.yaml`
- `docs/pipelines/constitution/work/06_core_validation/core_validation.yaml`
- `docs/pipelines/constitution/work/07_release/release_plan.yaml`
- reports in `docs/pipelines/constitution/reports/`

## Release pipeline

### Inputs
- release candidate from constitution pipeline
- execution and validation reports

### Outputs
- release patchset
- promotion report
- release notes

## Rule

Aucun pipeline ne doit écrire directement dans `docs/cores/current/` sans passer par validation et plan de release.
