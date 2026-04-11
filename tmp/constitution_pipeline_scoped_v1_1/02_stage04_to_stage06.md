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
