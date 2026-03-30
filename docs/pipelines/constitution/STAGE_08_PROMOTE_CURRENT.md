### STAGE_08_PROMOTE_CURRENT

Objectif :
- promouvoir explicitement une release matérialisée vers `docs/cores/current/`
- faire de `current/` une vue active dérivée d’une release immuable
- produire une trace canonique de promotion
- garantir l’idempotence de la promotion
- ne promouvoir qu’une release complète, cohérente et prête

Inputs :
- `work/07_release/release_plan.yaml`
- `reports/release_materialization_report.yaml`
- release matérialisée :
  - `docs/cores/releases/<release_id>/constitution.yaml`
  - `docs/cores/releases/<release_id>/referentiel.yaml`
  - `docs/cores/releases/<release_id>/link.yaml`
  - `docs/cores/releases/<release_id>/manifest.yaml`
- état actif éventuel :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`
  - `docs/cores/current/manifest.yaml`

Préconditions :
- `work/07_release/release_plan.yaml` doit être en `status: PASS`
- `reports/release_materialization_report.yaml` doit être en `status: PASS`
- la release ciblée doit exister physiquement sous `docs/cores/releases/<release_id>/`
- le manifest de release doit être présent et lisible
- la release doit être marquée comme promotion candidate si cette notion est utilisée dans le manifest ou le release plan

Principe opératoire :
- lire le `release_id` cible depuis le plan de release et/ou le manifest de release
- vérifier la complétude de la release :
  - présence de `constitution.yaml`
  - présence de `referentiel.yaml`
  - présence de `link.yaml`
  - présence de `manifest.yaml`
- vérifier la cohérence minimale avant promotion :
  - les `core_id` promus correspondent à ceux attendus par la release
  - les `version` promues correspondent à celles du manifest
  - les références inter-Core attendues sont déjà synchronisées dans la release
- si `docs/cores/current/` pointe déjà sur cette release cible, ne pas réécrire inutilement les fichiers :
  - promotion idempotente
  - produire un report `PASS` avec note `already_current`
- sinon :
  - copier la release cible vers `docs/cores/current/`
  - écrire ou mettre à jour `docs/cores/current/manifest.yaml`
  - valider le manifest courant et le report de promotion avant clôture du stage
  - produire la trace canonique de promotion

Portée des modifications :
- seuls les fichiers de `docs/cores/current/` peuvent être mis à jour à ce stage
- aucun fichier de `docs/cores/releases/<release_id>/` ne doit être modifié par ce stage
- aucune réécriture logique des Core ne doit avoir lieu à ce stage :
  - la promotion copie une release déjà finalisée
  - elle ne recalcule ni versions ni références

Idempotence attendue :
- promouvoir deux fois la même release doit produire un résultat stable
- une promotion répétée de la release déjà active ne doit pas créer de divergence
- le report doit indiquer explicitement si la promotion était :
  - `applied`
  - `already_current`

Commandes de référence :
- vérifier la présence de la release cible :
  - `test -f ./docs/cores/releases/<release_id>/constitution.yaml`
  - `test -f ./docs/cores/releases/<release_id>/referentiel.yaml`
  - `test -f ./docs/cores/releases/<release_id>/link.yaml`
  - `test -f ./docs/cores/releases/<release_id>/manifest.yaml`
- valider le manifest de release avant promotion :
  - `python docs/patcher/shared/validate_release_manifest.py ./docs/cores/releases/<release_id>/manifest.yaml ./docs/specs/core-release/release_manifest.schema.yaml`
- promouvoir la release vers current :
  - `python docs/patcher/shared/promote_current.py ./docs/pipelines/constitution/work/07_release/release_plan.yaml ./docs/pipelines/constitution/reports/release_materialization_report.yaml ./docs/pipelines/constitution/reports/promotion_report.yaml`
- valider le manifest courant après promotion :
  - `python docs/patcher/shared/validate_current_manifest.py ./docs/cores/current/manifest.yaml ./docs/specs/core-release/current_manifest.schema.yaml`
- valider le report de promotion :
  - `python docs/patcher/shared/validate_promotion_report.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/specs/core-release/promotion_report.schema.yaml`

Validation attendue :
- `validate_release_manifest.py` doit retourner `status: PASS` avant promotion
- `promote_current.py` doit :
  - copier la release promue dans `docs/cores/current/`
  - écrire `docs/cores/current/manifest.yaml`
  - produire `docs/pipelines/constitution/reports/promotion_report.yaml`
  - gérer correctement le cas idempotent `already_current`
- `validate_current_manifest.py` doit retourner `status: PASS` après promotion
- `validate_promotion_report.py` doit retourner `status: PASS` après promotion

Artefacts validés à l’issue du Stage 08 :
- `docs/cores/current/manifest.yaml`
- `docs/pipelines/constitution/reports/promotion_report.yaml`

Validation scriptée recommandée (version courte) :
- `python docs/patcher/shared/validate_release_manifest.py ./docs/cores/releases/<release_id>/manifest.yaml ./docs/specs/core-release/release_manifest.schema.yaml`
- `python docs/patcher/shared/validate_current_manifest.py ./docs/cores/current/manifest.yaml ./docs/specs/core-release/current_manifest.schema.yaml`
- `python docs/patcher/shared/validate_promotion_report.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/specs/core-release/promotion_report.schema.yaml`

Outputs :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/cores/current/manifest.yaml`
- `reports/promotion_report.yaml`

Trace canonique :
- produire une trace de promotion indiquant :
  - le `release_id` promu
  - le chemin source de la release
  - le statut final de promotion
  - si la promotion a été effectivement appliquée ou si la release était déjà courante
  - les fichiers mis à jour dans `current/`
- cette trace est canonisée dans :
  - `reports/promotion_report.yaml`

Structure attendue :
- `PROMOTION_REPORT`
  - `status`
  - `release_id`
  - `source_release_path`
  - `promotion_mode`
  - `files_promoted`
  - `current_manifest_updated`
  - `notes`

Précision sur le manifest courant :
- `docs/cores/current/manifest.yaml` doit être écrit à partir du `manifest.yaml` de la release promue
- il doit reprendre fidèlement :
  - le `release_id`
  - le `source_release_path`
  - les `core_id` actifs
  - les `version` actives
  - la provenance de la release source
- seuls les champs propres à l’état courant peuvent être ajoutés ou mis à jour localement, par exemple :
  - la date ou l’horodatage de promotion
  - le statut actif
  - le mode de promotion
- aucune recomposition libre du contenu métier ou des versions ne doit être faite à partir des Core promus eux-mêmes
- `docs/cores/current/manifest.yaml` est un manifest dérivé de la release promue, pas un manifest recalculé indépendamment

Règle opératoire :
- `docs/cores/releases/` est la source de vérité des releases publiées
- `docs/cores/current/` est uniquement la vue active de la release promue
- aucune promotion ne doit s’effectuer depuis `work/05_apply/patched/`
- aucune promotion ne doit s’effectuer sans release matérialisée complète
- toute promotion doit être explicitement traçable dans `reports/promotion_report.yaml`