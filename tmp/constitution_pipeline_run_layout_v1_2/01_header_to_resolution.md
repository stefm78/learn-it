# PIPELINE — constitution

id: constitution
version: 1.2
scope: core-governance

## Goal

Challenger les Core actifs, arbitrer les corrections, produire un patch, le valider, l'appliquer dans une zone de travail et préparer la promotion.

## Operating modes

Le pipeline `constitution` supporte désormais trois régimes opératoires :

### Mode nominal global
- aucun `scope_manifest` fourni ;
- aucun `run_id` fourni ;
- le pipeline s'exécute sur le périmètre canonique complet ;
- le comportement reste celui du pipeline historique.

### Mode borné historique de transition
- un `scope_manifest` est fourni dans `inputs/` ;
- le pipeline travaille sur un sous-ensemble borné ;
- le layout plat historique reste utilisé ;
- ce mode est transitoire.

### Mode borné par run (`bounded_local_run`)
- un `run_id` est fourni ;
- le pipeline travaille à partir d'un scope catalogué matérialisé dans `runs/<run_id>/...` ;
- le droit de modifier est gouverné par le `scope_manifest` du run ;
- le devoir de lecture du voisinage logique est gouverné par le `impact_bundle` du run ;
- tout passage vers release/promotion reste soumis au `integration_gate` du run.

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

Historical flat bounded-run control inputs:
- `docs/pipelines/constitution/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/inputs/integration_gate.yaml`

Run-based bounded-run control inputs:
- `docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/integration_gate.yaml`

## Layout resolution

Reference companion:
- `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`

Resolution rules:
- if `run_id` is provided and the run exists, the pipeline must resolve paths from `docs/pipelines/constitution/runs/<run_id>/...`
- else if `inputs/scope_manifest.yaml` exists, the pipeline may run in bounded transition mode using the historical flat layout
- else the pipeline runs in nominal global mode
- bounded runs should no longer open new artifacts in the flat historical layout except during explicit transition handling

## Staging

Historical flat layout:
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

Run-based layout:
- `docs/pipelines/constitution/runs/<run_id>/inputs/`
- `docs/pipelines/constitution/runs/<run_id>/work/01_challenge/`
- `docs/pipelines/constitution/runs/<run_id>/work/02_arbitrage/`
- `docs/pipelines/constitution/runs/<run_id>/work/03_patch/`
- `docs/pipelines/constitution/runs/<run_id>/work/04_patch_validation/`
- `docs/pipelines/constitution/runs/<run_id>/work/05_apply/`
- `docs/pipelines/constitution/runs/<run_id>/work/06_core_validation/`
- `docs/pipelines/constitution/runs/<run_id>/work/07_release/`
- `docs/pipelines/constitution/runs/<run_id>/reports/`
- `docs/pipelines/constitution/runs/<run_id>/outputs/`
- `docs/pipelines/constitution/runs/<run_id>/archive/`

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

### `run_manifest`
Déclare l'identité du run, son `scope_id`, ses chemins d'exécution et la référence vers la scope definition source.

## Stages

### STAGE_01_CHALLENGE

- Inputs:
  - current cores
  - optional focus note
  - optional `run_id`
  - optional run-scoped inputs under `runs/<run_id>/inputs/`
  - optional flat `inputs/scope_manifest.yaml`
  - optional flat `inputs/impact_bundle.yaml`
- Prompt:
  - `docs/prompts/shared/Challenge_constitution.md`
- Rules:
  - if `run_id` is present, the stage runs in bounded run mode and writes in `runs/<run_id>/work/01_challenge/`
  - else if `scope_manifest.yaml` is present, the stage runs in bounded transition mode in the flat layout
  - else the stage runs in nominal global mode
  - any impact, weakness, contradiction or required change detected outside the declared scope must be explicitly flagged as `out_of_scope`
  - no hidden recommendation of out-of-scope modification is allowed
- Output:
  - flat mode: `work/01_challenge/challenge_report_##.md`
  - run mode: `runs/<run_id>/work/01_challenge/challenge_report_##.md`

### STAGE_02_ARBITRAGE

- Inputs:
  - challenge reports from the resolved challenge directory
  - optional human arbitrage notes
  - optional `run_id`
  - optional resolved `scope_manifest`
  - optional resolved `impact_bundle`
- Prompt:
  - `docs/prompts/shared/Make04ConstitutionArbitrage.md`
- Rule:
  - every `challenge_report*.md` file present in the resolved challenge directory must be considered during arbitrage
  - the arbitrage must consolidate all retained, rejected, deferred, or out-of-scope findings into a single decision record
  - in bounded mode, the arbitrage must distinguish retained in-scope findings, retained out-of-scope findings, and deferred findings caused by scope limits
  - any required scope extension must be made explicit
- Output:
  - flat mode: `work/02_arbitrage/arbitrage.md`
  - run mode: `runs/<run_id>/work/02_arbitrage/arbitrage.md`
