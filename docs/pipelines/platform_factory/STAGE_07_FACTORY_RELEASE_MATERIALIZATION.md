### STAGE_07_FACTORY_RELEASE_MATERIALIZATION

Objectif :
- classifier la profondeur d’évolution des artefacts `platform_factory` patchés validés ;
- calculer les versions cibles et les éventuels renommages nécessaires ;
- matérialiser une release immuable sous `docs/cores/releases/` ;
- produire une note de release candidate exploitable ;
- préparer une promotion explicite ultérieure sans modifier `docs/cores/current/`.

Sous-étapes :
- `07A_FACTORY_RELEASE_CLASSIFICATION`
- `07B_FACTORY_RELEASE_MATERIALIZATION`

Inputs :
- `work/05_apply/patched/platform_factory_architecture.yaml`
- `work/05_apply/patched/platform_factory_state.yaml`
- `work/06_core_validation/platform_factory_core_validation.yaml`
- `reports/platform_factory_execution_report.yaml`
- état actif courant :
  - `docs/cores/current/platform_factory_architecture.yaml`
  - `docs/cores/current/platform_factory_state.yaml`

Précondition :
- `work/06_core_validation/platform_factory_core_validation.yaml` doit être en `status: PASS`
- `reports/platform_factory_execution_report.yaml` doit être en `status: PASS`

Outillage déterministe attendu :
- `docs/patcher/shared/build_platform_factory_release_plan.py`
- `docs/patcher/shared/materialize_platform_factory_release.py`

Règle d’exécution déterministe :
- le calcul de classification et de release doit être produit par script déterministe ;
- l’IA peut commenter, challenger et interpréter les résultats ;
- l’IA ne doit pas simuler les sorties de script ;
- toute commande à exécuter doit être explicitement donnée comme commande shell.

#### 07A_FACTORY_RELEASE_CLASSIFICATION

Objectif :
- comparer les artefacts patchés validés avec l’état actif de `current/` ;
- déterminer s’il existe une évolution réelle ;
- qualifier la profondeur du changement ;
- calculer les versions cibles ;
- déterminer les renommages nécessaires ;
- déterminer les mises à jour de références utiles à la release ;
- produire un plan de release exploitable par `07B`.

Principe opératoire :
- comparer chaque artefact patché validé avec son équivalent dans `docs/cores/current/`
- déterminer, pour chaque artefact :
  - si le contenu est strictement identique ou non ;
  - si l’évolution est `none`, `editorial`, `minor` ou `major` ;
  - si l’`artifact_id` doit rester stable ou être renommé ;
  - si la `version` interne doit être conservée ou incrémentée ;
- déterminer la cohérence d’ensemble :
  - compatibilité architecture / state ;
  - compatibilité avec les dépendances explicites vers Constitution / Référentiel / LINK ;
  - cohérence des références et dépendances déclarées ;
- calculer une release bundle unique et immuable.
- le calcul de release doit être produit par un mécanisme déterministe à partir de :
  - `work/05_apply/patched/`
  - `docs/cores/current/`
  - `work/06_core_validation/platform_factory_core_validation.yaml`
  - `reports/platform_factory_execution_report.yaml`
- ce calcul ne doit pas reposer uniquement sur les `artifact_id` ou les `version`
- il doit comparer le contenu réel des artefacts patchés et courants avant toute décision de versioning
- le résultat canonique de ce calcul est `work/07_release/platform_factory_release_plan.yaml`

Règles de classification :
- `none` :
  - aucun changement logique ou structurel détectable ;
  - aucune nouvelle release nécessaire
- `editorial` :
  - correction de texte ;
  - `description`, `human_readable`, `notes` ;
  - reformulation sans effet logique ;
  - peut donner lieu à une release documentaire seulement si explicitement souhaité
- `minor` :
  - ajout compatible de sections, contraintes, contrats ou précisions ;
  - explicitation sans rupture de contrat ;
  - enrichissement compatible des règles de gouvernance ou de traçabilité
- `major` :
  - modification d’un invariant ;
  - suppression ou renommage d’ID structurants ;
  - changement de logique de gouvernance ;
  - rupture de compatibilité entre architecture et state ;
  - rupture des dépendances explicites au socle canonique

Décisions attendues :
- `release_required: true|false`
- `change_depth: none | editorial | minor | major`
- `target_versions`
- `required_renames`
- `required_reference_updates`
- `release_id`
- `release_path`
- `promotion_candidate: true|false`

Output canonique :
- `work/07_release/platform_factory_release_plan.yaml`

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
  - `release_bundle`
  - `notes`

Sémantique de statut attendue :
- `status: PASS` signifie que la classification déterministe s’est exécutée correctement, y compris si `release_required: false`
- l’absence de release à matérialiser n’est pas un warning de pipeline
- `status: FAIL` signifie qu’une précondition, une entrée ou le calcul déterministe lui-même est invalide

Commande recommandée :
```bash
mkdir -p ./docs/pipelines/platform_factory/work/07_release

python docs/patcher/shared/build_platform_factory_release_plan.py \
  ./docs/pipelines/platform_factory/work/05_apply/patched \
  ./docs/cores/current \
  ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml \
  ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
  ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
```

#### 07B_FACTORY_RELEASE_MATERIALIZATION

Objectif :
- matérialiser une release immuable à partir du plan calculé en `07A` ;
- produire les fichiers finalisés de release ;
- produire un manifest de release ou équivalent de traçabilité de release ;
- produire les notes de release candidate ;
- ne jamais modifier `docs/cores/current/` à ce stage.

Précondition :
- `work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`
- `release_required` doit être explicitement renseigné

Principe opératoire :
- si `release_required: false`
  - ne pas créer de nouvelle release ;
  - produire une note explicite de non-matérialisation ;
  - produire un report `PASS` indiquant qu’aucune release n’était requise
- si `release_required: true`
  - créer un répertoire immuable sous `docs/cores/releases/<release_id>/`
  - copier les artefacts patchés validés dans cette release comme base de matérialisation
  - appliquer, sur les copies de release uniquement, les renommages et mises à jour de versions décidés par `07A`
  - appliquer, sur les copies de release uniquement, les mises à jour de références décidées par `07A`
  - produire un manifest de release ou équivalent de traçabilité
  - produire les notes de release candidate
- la release matérialisée devient la source de vérité publiable
- `docs/cores/current/` ne doit jamais être modifié à ce stage

Trace de matérialisation :
- produire une trace de matérialisation indiquant :
  - le `release_id`
  - le répertoire créé
  - les fichiers effectivement écrits
  - le statut final de matérialisation

Portée des transformations :
- les renommages d’`artifact_id`, les mises à jour de `version` et les synchronisations de références décidés par `07A_FACTORY_RELEASE_CLASSIFICATION` s’appliquent uniquement aux fichiers écrits sous `docs/cores/releases/<release_id>/`
- les fichiers source de `work/05_apply/patched/` sont utilisés comme base de matérialisation et ne doivent pas être modifiés en place par `07B`
- les fichiers de `docs/cores/current/` ne doivent jamais être modifiés à ce stage

Convention de nommage recommandée :
- répertoire de release :
  - `docs/cores/releases/<release_id>/`
- format recommandé pour `release_id` :
  - `PLATFORM_FACTORY_RELEASE_YYYY_MM_DD_RNN`

Manifest de release attendu :
- `docs/cores/releases/<release_id>/manifest.yaml`
- racine :
  - `PLATFORM_FACTORY_RELEASE_MANIFEST`
- contenu minimal :
  - `release_id`
  - `release_path`
  - `status`
  - `promotion_candidate`
  - `change_depth`
  - `materialized_at`
  - `source_release_plan`
  - `artifacts`
- chaque entrée de `artifacts` doit au minimum porter :
  - `role`
  - `file`
  - `artifact_id`
  - `version`
  - `status`
  - `sha256`

Outputs :
- `work/07_release/platform_factory_release_plan.yaml`
- `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
- `docs/cores/releases/<release_id>/platform_factory_state.yaml`
- `docs/cores/releases/<release_id>/manifest.yaml`
- `outputs/platform_factory_release_candidate_notes.md`
- `reports/platform_factory_release_materialization_report.yaml`

Commande recommandée :
```bash
python docs/patcher/shared/materialize_platform_factory_release.py \
  ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
  ./docs/pipelines/platform_factory/work/05_apply/patched \
  ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
  ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
```

Règle opératoire :
- `07A_FACTORY_RELEASE_CLASSIFICATION` produit la décision de versioning et de release
- `07B_FACTORY_RELEASE_MATERIALIZATION` produit une release immuable
- aucun fichier de `docs/cores/current/` ne doit être modifié par le Stage 07
- toute bascule vers `current/` doit être réalisée dans un stage de promotion explicite ultérieur
- la décision de release de `07A` doit être calculée de manière déterministe ; l’IA peut commenter ou challenger le résultat, mais ne doit pas remplacer ce calcul

Note V0 importante :
- contrairement au pipeline `constitution`, le tooling de release `platform_factory` reste spécifique à ses deux artefacts dédiés et à leur manifest de release
- ce stage est exécutable avec l’outillage scripté dédié ci-dessus
- la mise à jour éventuelle de `docs/cores/current/manifest.yaml` ne fait pas partie de ce Stage 07
