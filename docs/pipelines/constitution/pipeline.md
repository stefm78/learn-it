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
### STAGE_04_PATCH_VALIDATION
Objectif :
- vérifier que le patch synthétisé au Stage 03 est structurellement valide
- vérifier qu’il reste minimal, cohérent et compatible avec la séparation Constitution / Référentiel / LINK
- en mode borné, vérifier qu’il n’écrit pas hors du scope déclaré
- décider s’il est autorisé ou non à passer au Stage 05_APPLY

Inputs :
- `work/03_patch/patchset.yaml`
- contexte d’arbitrage si nécessaire :
  - `work/02_arbitrage/arbitrage.md`
- optional `inputs/scope_manifest.yaml`
- éventuellement le prompt de revue :
  - `docs/prompts/shared/Make06PatchValidation.md`

Commandes de référence :
- validation structurelle automatique du patchset :
  - `python docs/patcher/shared/validate_patchset.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml > ./docs/pipelines/constitution/work/04_patch_validation/patch_validation.yaml`

Vérifications attendues :
- présence de `PATCH_SET`
- `patch_dsl_version` déclaré et compatible
- `atomic` déclaré
- présence de `files`
- opérations supportées uniquement
- cohérence minimale des opérations `rename`, `rewrite_references`, `replace_field`, `replace_text`
- cohérence du bloc `federation` si des références inter-Core fines sont utilisées
- absence d’anomalie bloquante dans la structure du patchset
- en mode borné, absence d’écriture hors du périmètre autorisé ou signalement explicite du dépassement

Revue logique attendue en complément :
- patch sûr
- patch minimal
- patch cohérent avec la répartition Constitution / Référentiel / LINK
- absence de logique métier autonome introduite dans le LINK
- absence de régression évidente de gouvernance
- absence de déplacement injustifié de logique entre couches
- réécriture des références prévue si nécessaire
- en mode borné, cohérence du patch avec le `scope_manifest`

Interprétation du résultat :
- si `patch_validation.yaml` retourne `status: PASS`, le patch peut être considéré comme structurellement recevable pour le Stage 05
- si `patch_validation.yaml` retourne `status: FAIL`, le pipeline s’arrête ici et le patch doit être corrigé en `work/03_patch/patchset.yaml` avant nouvelle validation
- un `PASS` structurel n’exonère pas d’une revue logique ciblée si le patch modifie des bindings inter-Core sensibles
- le dry-run du Stage 05 constitue la validation exécutable finale avant apply réel
- en mode borné, un PASS local ne vaut pas clearance globale d’intégration

Tools :
- `docs/patcher/shared/validate_patchset.py`
- `docs/prompts/shared/Make06PatchValidation.md`

Outputs :
- `work/04_patch_validation/patch_validation.yaml`
- `reports/patch_validation_report.md`

Règle opératoire :
- `patch_validation.yaml` est la trace canonique de validation automatique du Stage 04
- `patch_validation_report.md` est une trace de lecture humaine complémentaire, utile si une revue logique explicite est produite
- aucun passage à l’apply réel du Stage 05 ne doit avoir lieu sans validation `PASS`

### STAGE_05_APPLY
Objectif :
- appliquer le patch validé dans une zone de travail isolée
- produire une trace d’exécution exploitable
- matérialiser les Core patchés sans modifier directement `docs/cores/current/`

Inputs :
- `work/03_patch/patchset.yaml`
- `work/04_patch_validation/patch_validation.yaml`
- copies de référence issues de :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

Précondition :
- `work/04_patch_validation/patch_validation.yaml` doit être en `status: PASS`

Principe opératoire :
- le patchset peut continuer à référencer les chemins canoniques `docs/cores/current/*.yaml`
- l’application réelle du patch se fait sur une racine sandbox située sous `work/05_apply/`
- la sandbox reproduit la structure canonique du repo pour éviter toute réécriture du patchset d’exécution
- `docs/cores/current/` ne doit jamais être modifié directement par ce stage
- en mode borné, le succès d’apply reste un succès local tant que le `integration_gate` n’est pas clarifié

Commandes de référence :
- préparer la racine sandbox :
  - `mkdir -p ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current`
  - `cp ./docs/cores/current/constitution.yaml ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/constitution.yaml`
  - `cp ./docs/cores/current/referentiel.yaml ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/referentiel.yaml`
  - `cp ./docs/cores/current/link.yaml ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/link.yaml`

- dry-run sur sandbox :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml ./docs/pipelines/constitution/work/05_apply/sandbox true ./docs/pipelines/constitution/reports/patch_execution_report.yaml`

- apply sur sandbox :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml ./docs/pipelines/constitution/work/05_apply/sandbox false ./docs/pipelines/constitution/reports/patch_execution_report.yaml`

- matérialiser la sortie patchée :
  - `mkdir -p ./docs/pipelines/constitution/work/05_apply/patched`
  - `cp ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/constitution.yaml ./docs/pipelines/constitution/work/05_apply/patched/constitution.yaml`
  - `cp ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/referentiel.yaml ./docs/pipelines/constitution/work/05_apply/patched/referentiel.yaml`
  - `cp ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current/link.yaml ./docs/pipelines/constitution/work/05_apply/patched/link.yaml`

Effets attendus :
- en dry-run :
  - aucune modification effective des fichiers sandbox
  - vérification finale de l’applicabilité du patch
  - génération du report d’exécution si un chemin est fourni

- en apply :
  - application effective du patch dans la racine sandbox uniquement
  - génération ou mise à jour de `reports/patch_execution_report.yaml`
  - matérialisation des Core patchés dans `work/05_apply/patched/`

Interprétation du résultat :
- si `patch_execution_report.yaml` est en `PASS`, le pipeline peut passer au `STAGE_06_CORE_VALIDATION`
- si le report est en `FAIL`, le pipeline s’arrête ici
- aucun succès du Stage 05 n’autorise à modifier `current/` sans étape explicite de promotion

Tools :
- `docs/patcher/shared/apply_patch.py`

Outputs :
- `work/05_apply/sandbox/`
- `work/05_apply/patched/`
- `reports/patch_execution_report.yaml`

### STAGE_06_CORE_VALIDATION

- Inputs:
  - `work/05_apply/patched/constitution.yaml`
  - `work/05_apply/patched/referentiel.yaml`
  - `work/05_apply/patched/link.yaml`
  - optional `inputs/scope_manifest.yaml`
  - optional `inputs/integration_gate.yaml`
- Prompt:
  - `docs/prompts/shared/Make02CoreValidation.md`
- Rules:
  - in nominal mode, this stage remains the standard post-apply core validation
  - in bounded mode, this stage must distinguish local scope validation from full global validation
  - any unmet global recheck requirement must be propagated to the `integration_gate`
- Outputs:
  - `work/06_core_validation/core_validation.yaml`
  - `reports/core_validation_report.md`
### STAGE_07_RELEASE_MATERIALIZATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

- Rule:
  - `STAGE_07_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07
  - in bounded mode, no release materialization may be treated as promotable if the `integration_gate` is not explicitly cleared

### STAGE_08_PROMOTE_CURRENT
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_08_PROMOTE_CURRENT.md`

- Rule:
  - `STAGE_08_PROMOTE_CURRENT.md` is the canonical specification for Stage 08
  - in bounded mode, promotion remains blocked until global checks required by the `integration_gate` are explicitly satisfied


### STAGE_09_CLOSEOUT_AND_ARCHIVE
Objectif :
- clôturer explicitement le run du pipeline après promotion réussie
- archiver le run terminé sous `docs/pipelines/constitution/archive/<release_id>/`
- réinitialiser `docs/pipelines/constitution/work/` pour rendre le pipeline immédiatement prêt à une nouvelle exécution
- conserver une trace finale de clôture exploitable humainement et techniquement

Inputs :
- `docs/pipelines/constitution/reports/promotion_report.yaml`
- `docs/cores/current/manifest.yaml`
- `docs/pipelines/constitution/work/07_release/release_plan.yaml`
- `docs/pipelines/constitution/reports/release_materialization_report.yaml`
- `docs/pipelines/constitution/reports/patch_execution_report.yaml`
- `docs/pipelines/constitution/work/06_core_validation/core_validation.yaml`

Préconditions :
- `reports/promotion_report.yaml` doit être en `status: PASS`
- `docs/cores/current/manifest.yaml` doit être valide
- `docs/cores/current/manifest.yaml` doit pointer vers la release promue par le Stage 08

Principe opératoire :
- vérifier que la promotion Stage 08 constitue bien l’état actif final du run
- produire `reports/closeout_report.yaml` et `outputs/final_run_summary.md`
- archiver une copie complète du run terminé sous `docs/pipelines/constitution/archive/<release_id>/` avec :
  - `work/`
  - `reports/`
  - `outputs/`
- considérer `work/` comme un workspace transitoire et non comme une archive canonique
- supprimer puis recréer `docs/pipelines/constitution/work/` vide
- ne modifier ni `docs/cores/releases/` ni `docs/cores/current/`

Archive attendue :
- `archive/<release_id>/work/`
- `archive/<release_id>/reports/`
- `archive/<release_id>/outputs/`

Commandes de référence :
- vérifier l’état courant final :
  - `python docs/patcher/shared/validate_current_manifest.py ./docs/cores/current/manifest.yaml ./docs/specs/core-release/current_manifest.schema.yaml`
- vérifier la traçabilité de promotion :
  - `python docs/patcher/shared/validate_promotion_report.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/specs/core-release/promotion_report.schema.yaml`
- clôturer, archiver et réinitialiser le workspace :
  - `python docs/patcher/shared/closeout_pipeline_run.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/cores/current/manifest.yaml ./docs/pipelines/constitution/reports/closeout_report.yaml ./docs/pipelines/constitution/outputs/final_run_summary.md ./docs/pipelines/constitution/archive`

Outputs :
- `reports/closeout_report.yaml`
- `outputs/final_run_summary.md`
- `archive/<release_id>/`
- `work/` recréé vide

Règle opératoire :
- `docs/cores/releases/` reste l’archive métier immuable
- `docs/cores/current/` reste uniquement la vue active promue
- `docs/pipelines/constitution/work/` est un workspace transitoire du run courant
- l’archive des runs terminés se trouve sous `docs/pipelines/constitution/archive/`
- le Stage 09 ne laisse pas l’historique d’un run uniquement dans `work/`
- le Stage 09 clôture, archive et réinitialise ; il ne recalcule aucun contenu métier

## Success criteria

- No stage may be skipped
- No file in `current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under `work/05_apply/`
- Any release materialization must write immutable artifacts under `docs/cores/releases/`
- Promotion to `current/` must remain explicit and occur in a dedicated stage
- Any successful promotion should be followed by an explicit archive-and-reset closeout stage
- Any completed run should be archived under `docs/pipelines/constitution/archive/<release_id>/`
- `docs/pipelines/constitution/work/` should be reset after closeout to prepare the next execution
- In bounded mode, no silent out-of-scope modification is allowed
- In bounded mode, no promotion may occur until the `integration_gate` is explicitly cleared
