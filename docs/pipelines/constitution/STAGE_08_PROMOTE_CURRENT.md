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
- préparer `current/` :
  - `mkdir -p ./docs/cores/current`
- promouvoir la release :
  - `cp ./docs/cores/releases/<release_id>/constitution.yaml ./docs/cores/current/constitution.yaml`
  - `cp ./docs/cores/releases/<release_id>/referentiel.yaml ./docs/cores/current/referentiel.yaml`
  - `cp ./docs/cores/releases/<release_id>/link.yaml ./docs/cores/current/link.yaml`
- écrire le manifest courant :
  - `./docs/cores/current/manifest.yaml`

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

Manifest courant recommandé :
- `docs/cores/current/manifest.yaml` doit au minimum indiquer :
  - le `release_id` actif
  - la date ou l’horodatage de promotion
  - les `core_id` et `version` actifs
  - la provenance de la release source

Règle opératoire :
- `docs/cores/releases/` est la source de vérité des releases publiées
- `docs/cores/current/` est uniquement la vue active de la release promue
- aucune promotion ne doit s’effectuer depuis `work/05_apply/patched/`
- aucune promotion ne doit s’effectuer sans release matérialisée complète
- toute promotion doit être explicitement traçable dans `reports/promotion_report.yaml`