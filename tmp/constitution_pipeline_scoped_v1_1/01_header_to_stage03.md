# PIPELINE — constitution

id: constitution
version: 1.1
scope: core-governance

## Goal

Challenger les Core actifs, arbitrer les corrections, produire un patch, le valider, l'appliquer dans une zone de travail et préparer la promotion.

## Operating modes

Le pipeline `constitution` supporte désormais deux modes opératoires :

### Mode nominal global
- aucun `scope_manifest` fourni ;
- le pipeline s'exécute sur le périmètre canonique complet ;
- le comportement reste celui du pipeline historique.

### Mode borné (`bounded_local_run`)
- un `scope_manifest` est fourni dans `inputs/` ;
- le pipeline travaille sur un sous-ensemble borné ;
- le droit de modifier est gouverné par le `scope_manifest` ;
- le devoir de lecture du voisinage logique est gouverné par le `impact_bundle` ;
- tout passage vers release/promotion reste soumis à un `integration_gate` explicite.

Règle structurante :
- un succès local en mode borné n'est jamais équivalent à une cohérence canonique globale acquise ;
- la promotion de `current/` reste un acte centralisé et explicite.

## Canonical resources

### Prompts

- Challenge: `docs/prompts/shared/Challenge_constitution.md`
- Arbitrage: `docs/prompts/shared/Make04ConstitutionArbitrage.md`
- Patch synthesis: `docs/prompts/shared/Make05CorePatch.md`
- Patch validation: `docs/prompts/shared/Make06PatchValidation.md`
- Core validation: `docs/prompts/shared/Make02CoreValidation.md`
- Execution review: `docs/prompts/shared/Make08PatchExecutionReview.md`
- Release: `docs/prompts/shared/Make07CoreRelease.md`

### Spec and tools

- Patch DSL: `docs/specs/patch-dsl/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`
- `Build release plan: docs/patcher/shared/build_release_plan.py`
- `Materialize release: docs/patcher/shared/materialize_release.py`
- `Validate release plan: docs/patcher/shared/validate_release_plan.py`
- `Closeout pipeline run: docs/patcher/shared/closeout_pipeline_run.py`

### Core inputs

Canonical inputs:
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Optional bounded-run control inputs:
- `docs/pipelines/constitution/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/inputs/integration_gate.yaml`

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
- archive: `docs/pipelines/constitution/archive/`

## Scope control artifacts

### `scope_manifest`
Déclare le périmètre modifiable autorisé du run.
En mode borné, ce qui n'est pas dans le scope ne peut pas être modifié implicitement.

### `impact_bundle`
Déclare le voisinage logique à relire pour travailler sûrement.
Il étend le devoir de lecture, pas le droit de modifier.

### `integration_gate`
Déclare les contrôles globaux à rejouer avant release/promotion.
En mode borné, il bloque toute promotion implicite d'un succès local.

## Stages

### STAGE_01_CHALLENGE

- Inputs:
  - current cores
  - optional focus note in `inputs/`
  - optional `inputs/scope_manifest.yaml`
  - optional `inputs/impact_bundle.yaml`
- Prompt:
  - `docs/prompts/shared/Challenge_constitution.md`
- Rules:
  - if `scope_manifest.yaml` is absent, the stage runs in nominal global mode
  - if `scope_manifest.yaml` is present, the stage runs in bounded mode and must challenge only the declared scope
  - any impact, weakness, contradiction or required change detected outside the declared scope must be explicitly flagged as `out_of_scope`
  - no hidden recommendation of out-of-scope modification is allowed
- Output:
  - `work/01_challenge/challenge_report_##.md`

### STAGE_02_ARBITRAGE

- Inputs:
  - challenge reports from `docs/pipelines/constitution/work/01_challenge/`
  - optional human arbitrage notes
  - optional `inputs/scope_manifest.yaml`
  - optional `inputs/impact_bundle.yaml`
- Prompt:
  - `docs/prompts/shared/Make04ConstitutionArbitrage.md`
- Rule:
  - every `challenge_report*.md` file present in `docs/pipelines/constitution/work/01_challenge/` must be considered during arbitrage
  - the arbitrage must consolidate all retained, rejected, deferred, or out-of-scope findings into a single decision record
  - in bounded mode, the arbitrage must distinguish retained in-scope findings, retained out-of-scope findings, and deferred findings caused by scope limits
  - any required scope extension must be made explicit
- Output:
  - `work/02_arbitrage/arbitrage.md`

### STAGE_03_PATCH_SYNTHESIS

- Inputs:
  - current cores
  - challenge report
  - arbitrage
  - optional `inputs/scope_manifest.yaml`
- Prompt:
  - `docs/prompts/shared/Make05CorePatch.md`
- Rules:
  - in nominal mode, patch synthesis remains global
  - in bounded mode, the patch must remain inside the declared writable scope
  - any dependency outside the scope that cannot be ignored must be flagged explicitly
  - no silent out-of-scope modification is allowed
- Output:
  - `work/03_patch/patchset.yaml`
