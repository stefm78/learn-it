### STAGE_08_FACTORY_PROMOTE_CURRENT

Objectif :
- promouvoir explicitement une release matérialisée vers `docs/cores/current/`
- faire de `current/` une vue active dérivée d’une release immuable
- produire une trace canonique de promotion
- garantir l’idempotence de la promotion
- ne promouvoir qu’une release complète, cohérente et prête

Inputs :
- `work/07_release/platform_factory_release_plan.yaml`
- `reports/platform_factory_release_materialization_report.yaml`
- release matérialisée :
  - `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
  - `docs/cores/releases/<release_id>/platform_factory_state.yaml`
  - `docs/cores/releases/<release_id>/manifest.yaml`
- état actif éventuel :
  - `docs/cores/current/platform_factory_architecture.yaml`
  - `docs/cores/current/platform_factory_state.yaml`

Préconditions :
- `work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`
- `reports/platform_factory_release_materialization_report.yaml` doit être en `status: PASS`
- la release ciblée doit exister physiquement sous `docs/cores/releases/<release_id>/`
- le manifest de release doit être présent et lisible
- la release doit être marquée comme promotion candidate si cette notion est utilisée dans le manifest ou le release plan

Principe opératoire :
- lire le `release_id` cible depuis le plan de release et/ou le manifest de release
- vérifier la complétude de la release :
  - présence de `platform_factory_architecture.yaml`
  - présence de `platform_factory_state.yaml`
  - présence de `manifest.yaml`
- vérifier la cohérence minimale avant promotion :
  - les `artifact_id` promus correspondent à ceux attendus par la release
  - les `version` promues correspondent à celles du manifest
  - les références attendues sont déjà synchronisées dans la release
- si `docs/cores/current/` pointe déjà sur cette release cible, ne pas réécrire inutilement les fichiers :
  - promotion idempotente
  - produire un report `PASS` avec note `already_current`
- sinon :
  - copier la release cible vers `docs/cores/current/`
  - produire la trace canonique de promotion

Portée des modifications :
- seuls les fichiers de `docs/cores/current/` peuvent être mis à jour à ce stage
- aucun fichier de `docs/cores/releases/<release_id>/` ne doit être modifié par ce stage
- aucune réécriture logique des artefacts ne doit avoir lieu à ce stage :
  - la promotion copie une release déjà finalisée
  - elle ne recalcule ni versions ni références

Idempotence attendue :
- promouvoir deux fois la même release doit produire un résultat stable
- une promotion répétée de la release déjà active ne doit pas créer de divergence
- le report doit indiquer explicitement si la promotion était :
  - `applied`
  - `already_current`

Outputs :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`
- `reports/platform_factory_promotion_report.yaml`

Trace canonique :
- produire une trace de promotion indiquant :
  - le `release_id` promu
  - le chemin source de la release
  - le statut final de promotion
  - si la promotion a été effectivement appliquée ou si la release était déjà courante
  - les fichiers mis à jour dans `current/`
- cette trace est canonisée dans :
  - `reports/platform_factory_promotion_report.yaml`

Structure attendue :
- `PROMOTION_REPORT`
  - `status`
  - `release_id`
  - `source_release_path`
  - `promotion_mode`
  - `files_promoted`
  - `notes`

Règle opératoire :
- `docs/cores/releases/` est la source de vérité des releases publiées
- `docs/cores/current/` est uniquement la vue active de la release promue
- aucune promotion ne doit s’effectuer depuis `work/05_apply/patched/`
- aucune promotion ne doit s’effectuer sans release matérialisée complète
- toute promotion doit être explicitement traçable dans `reports/platform_factory_promotion_report.yaml`

Note V0 importante :
- contrairement au pipeline `constitution`, la promotion `platform_factory` ne doit pas encore supposer par défaut une mise à jour de `docs/cores/current/manifest.yaml` tant que le modèle et le tooling de manifest courant n’ont pas été explicitement étendus à `platform_factory`
- en V0, la provenance et l’état de promotion doivent donc être garantis au minimum par `platform_factory_promotion_report.yaml` et par la release matérialisée elle-même
