### STAGE_07_RELEASE_MATERIALIZATION

Objectif :
- classifier la profondeur d’évolution des Core patchés validés ;
- calculer les versions cibles et les éventuels renommages ;
- synchroniser les références inter-Core nécessaires à la release ;
- matérialiser une release immuable dans `docs/cores/releases/` ;
- produire une note de release candidate exploitable ;
- préparer une promotion explicite ultérieure sans modifier `docs/cores/current/`.

Sous-étapes :
- `07A_RELEASE_CLASSIFICATION`
- `07B_RELEASE_MATERIALIZATION`

Inputs :
- `work/05_apply/patched/constitution.yaml`
- `work/05_apply/patched/referentiel.yaml`
- `work/05_apply/patched/link.yaml`
- `work/06_core_validation/core_validation.yaml`
- `reports/patch_execution_report.yaml`
- état actif courant :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

Précondition :
- `work/06_core_validation/core_validation.yaml` doit être en `status: PASS`

#### 07A_RELEASE_CLASSIFICATION

Objectif :
- comparer les Core patchés validés avec l’état actif de `current/` ;
- déterminer s’il existe une évolution réelle ;
- qualifier la profondeur du changement ;
- calculer les versions cibles ;
- déterminer les renommages nécessaires ;
- déterminer les mises à jour de références inter-Core ;
- produire un plan de release exploitable par `07B`.

Principe opératoire :
- comparer chaque Core patché validé avec son équivalent dans `docs/cores/current/`
- déterminer, pour chaque Core :
  - si le contenu est strictement identique ou non ;
  - si l’évolution est `none`, `editorial`, `minor` ou `major` ;
  - si le `core_id` doit rester stable ou être renommé ;
  - si la `version` interne doit être conservée ou incrémentée ;
- déterminer la cohérence d’ensemble :
  - compatibilité Constitution / Référentiel ;
  - compatibilité LINK avec les deux Core cibles ;
  - alignement des références inter-Core ;
- calculer une release bundle unique et immuable.

Règles de classification :
- `none` :
  - aucun changement logique ou structurel détectable ;
  - aucune nouvelle release nécessaire
- `editorial` :
  - correction de texte ;
  - `description`, `human_readable`, `source_anchor` ;
  - reformulation sans effet logique ;
  - peut donner lieu à une release documentaire seulement si explicitement souhaité
- `minor` :
  - ajout compatible d’objets ;
  - ajout de bindings explicites ;
  - ajout de paramètres, règles, événements, contraintes compatibles ;
  - explicitation inter-Core sans rupture de contrat
- `major` :
  - modification d’un invariant ;
  - suppression ou renommage d’ID ;
  - changement de logique métier ;
  - rupture de compatibilité inter-Core ;
  - déplacement injustifié de logique entre Constitution / Référentiel / LINK

Décisions attendues :
- `release_required: true|false`
- `change_depth: none | editorial | minor | major`
- `target_versions`
- `required_renames`
- `required_reference_updates`
- `link_updates`
- `release_id`
- `release_path`
- `promotion_candidate: true|false`

Output canonique :
- `work/07_release/release_plan.yaml`

Structure attendue :
- `RELEASE_PLAN`
  - `status`
  - `release_required`
  - `change_depth`
  - `validated_inputs`
  - `compared_against_current`
  - `target_versions`
  - `required_renames`
  - `required_reference_updates`
  - `link_updates`
  - `release_bundle`
  - `notes`

#### 07B_RELEASE_MATERIALIZATION

Objectif :
- matérialiser une release immuable à partir du plan calculé en `07A` ;
- produire les fichiers Core finalisés de release ;
- produire un manifest de release ;
- produire des notes de release candidate ;
- ne jamais modifier `docs/cores/current/` à ce stage.

Précondition :
- `work/07_release/release_plan.yaml` doit être en `status: PASS`
- `release_required` doit être explicitement renseigné

Principe opératoire :
- si `release_required: false`
  - ne pas créer de nouvelle release ;
  - produire une note explicite de non-matérialisation
- si `release_required: true`
  - créer un répertoire immuable sous `docs/cores/releases/<release_id>/`
  - copier les Core patchés validés dans cette release
  - appliquer les renommages et mises à jour de versions décidés par `07A`
  - appliquer les mises à jour de références inter-Core décidées par `07A`
  - produire un manifest de release
  - produire les notes de release candidate
- la release matérialisée devient la source de vérité publiable
- `docs/cores/current/` ne doit jamais être modifié à ce stage

Convention de nommage recommandée :
- répertoire de release :
  - `docs/cores/releases/<release_id>/`
- format recommandé pour `release_id` :
  - `CORE_RELEASE_YYYY_MM_DD_RNN`

Commandes de référence :
- créer la racine de release :
  - `mkdir -p ./docs/cores/releases/<release_id>`
- copier les Core patchés validés :
  - `cp ./docs/pipelines/constitution/work/05_apply/patched/constitution.yaml ./docs/cores/releases/<release_id>/constitution.yaml`
  - `cp ./docs/pipelines/constitution/work/05_apply/patched/referentiel.yaml ./docs/cores/releases/<release_id>/referentiel.yaml`
  - `cp ./docs/pipelines/constitution/work/05_apply/patched/link.yaml ./docs/cores/releases/<release_id>/link.yaml`
- écrire le manifest :
  - `./docs/cores/releases/<release_id>/manifest.yaml`
- écrire les notes de release candidate :
  - `./docs/pipelines/constitution/outputs/release_candidate_notes.md`

Outputs :
- `work/07_release/release_plan.yaml`
- `docs/cores/releases/<release_id>/constitution.yaml`
- `docs/cores/releases/<release_id>/referentiel.yaml`
- `docs/cores/releases/<release_id>/link.yaml`
- `docs/cores/releases/<release_id>/manifest.yaml`
- `outputs/release_candidate_notes.md`

Règle opératoire :
- `07A_RELEASE_CLASSIFICATION` produit la décision de versioning et de release
- `07B_RELEASE_MATERIALIZATION` produit une release immuable
- aucun fichier de `docs/cores/current/` ne doit être modifié par le Stage 07
- toute bascule vers `current/` doit être réalisée dans un stage de promotion explicite ultérieur