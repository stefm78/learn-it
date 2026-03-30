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
- `Build release plan: docs/patcher/shared/build_release_plan.py`
- `Materialize release: docs/patcher/shared/materialize_release.py`
- `Validate release plan: docs/patcher/shared/validate_release_plan.py`

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
Objectif :
- vérifier que le patch synthétisé au Stage 03 est structurellement valide
- vérifier qu’il reste minimal, cohérent et compatible avec la séparation Constitution / Référentiel / LINK
- décider s’il est autorisé ou non à passer au Stage 05_APPLY

Inputs :
- `work/03_patch/patchset.yaml`
- contexte d’arbitrage si nécessaire :
  - `work/02_arbitrage/arbitrage.md`
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

Revue logique attendue en complément :
- patch sûr
- patch minimal
- patch cohérent avec la répartition Constitution / Référentiel / LINK
- absence de logique métier autonome introduite dans le LINK
- absence de régression évidente de gouvernance
- absence de déplacement injustifié de logique entre couches
- réécriture des références prévue si nécessaire

Interprétation du résultat :
- si `patch_validation.yaml` retourne `status: PASS`, le patch peut être considéré comme structurellement recevable pour le Stage 05
- si `patch_validation.yaml` retourne `status: FAIL`, le pipeline s’arrête ici et le patch doit être corrigé en `work/03_patch/patchset.yaml` avant nouvelle validation
- un `PASS` structurel n’exonère pas d’une revue logique ciblée si le patch modifie des bindings inter-Core sensibles
- le dry-run du Stage 05 constitue la validation exécutable finale avant apply réel

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
- Prompt:
  - `docs/prompts/shared/Make02CoreValidation.md`
- Outputs:
  - `work/06_core_validation/core_validation.yaml`
  - `reports/core_validation_report.md`

### STAGE_07_RELEASE_MATERIALIZATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

- Rule:
  - `STAGE_07_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07

### STAGE_08_PROMOTE_CURRENT
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_08_PROMOTE_CURRENT.md`

- Rule:
  - `STAGE_08_PROMOTE_CURRENT.md` is the canonical specification for Stage 08

## Success criteria

- No stage may be skipped
- No file in `current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under `work/05_apply/`
- Any release materialization must write immutable artifacts under `docs/cores/releases/`
- Promotion to `current/` must remain explicit and occur in a dedicated stage