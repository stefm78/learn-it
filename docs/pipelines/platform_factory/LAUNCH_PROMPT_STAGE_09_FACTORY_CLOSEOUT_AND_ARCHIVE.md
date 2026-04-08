# LAUNCH PROMPT — STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

Le but de ce stage est de clôturer proprement un run déjà promu, d’archiver son état d’exécution, de produire le report final de closeout, de produire le résumé final, puis de réinitialiser `work/` pour un prochain run.

## Inputs obligatoires

Promotion réussie :
- `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`

Traçabilité release :
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

Script dédié :
- `docs/patcher/shared/closeout_platform_factory_run.py`

## Préconditions obligatoires

- `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml` doit porter `PROMOTION_REPORT.status: PASS`.
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml` doit porter `RELEASE_PLAN.status: PASS`.
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml` doit porter `PLATFORM_FACTORY_RELEASE_MATERIALIZATION.status: PASS`.
- `PROMOTION_REPORT.promotion_mode` doit être compatible avec un closeout post-promotion (`applied` ou `already_current`).
- La release promue doit exister réellement sous `docs/cores/releases/<release_id>/`.
- Le manifest de release doit être présent.
- Ne pas simuler un closeout si le script n’a pas tourné.

## Contexte d’exécution obligatoire

- Le Stage 09 clôture explicitement le run terminé.
- Il archive le run sous `docs/pipelines/platform_factory/archive/<release_id>/`.
- Il archive :
  - `docs/pipelines/platform_factory/work/`
  - `docs/pipelines/platform_factory/reports/`
  - `docs/pipelines/platform_factory/outputs/`
- Il recrée ensuite `docs/pipelines/platform_factory/work/` vide, prêt pour une nouvelle exécution.
- Il réécrit ensuite le report final de closeout et le résumé final dans les emplacements actifs du pipeline.
- Il ne modifie ni la release immuable sous `docs/cores/releases/`, ni la promotion déjà en place sous `docs/cores/current/`.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

## Règle anti-simulation obligatoire

- Ne jamais simuler le résultat d’un script déterministe.
- Ne jamais annoncer qu’un run est clôturé et archivé si le script n’a pas réellement tourné.
- Ne jamais prétendre que `work/` a été réinitialisé si ce n’est pas réellement le cas.
- Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
- Dans ce cas, il faut donner clairement la commande exacte à exécuter.
- Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme le résultat réel du script.

## Fichiers et répertoires de sortie obligatoires

Sorties actives attendues après exécution :
- `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
- `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
- `docs/pipelines/platform_factory/work/` recréé vide

Archive attendue :
- `docs/pipelines/platform_factory/archive/<release_id>/`

## Étape d’exécution obligatoire

Exécuter :

```bash
python docs/patcher/shared/closeout_platform_factory_run.py \
  ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml \
  ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
  ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
  ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml \
  ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md \
  ./docs/pipelines/platform_factory/archive
```

## Vérification obligatoire après exécution

Lire :
- `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
- `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`

Vérifier explicitement dans la racine YAML `PLATFORM_FACTORY_CLOSEOUT_REPORT` :
- `status`
- `release_id`
- `source_release_path`
- `promotion_mode`
- `manifest_path`
- `archive_path`
- `archived_paths`
- `work_reset`
- `run_closed`

Vérifier aussi :
- que `docs/pipelines/platform_factory/work/` existe bien encore après exécution ;
- qu’il est recréé vide ;
- que `docs/pipelines/platform_factory/archive/<release_id>/` existe réellement.

Si `PLATFORM_FACTORY_CLOSEOUT_REPORT.status` n’est pas `PASS`, le pipeline ne peut pas être considéré comme proprement clôturé.

## Si une commande doit être exécutée par l’humain dans le chat

Avant toute interprétation du résultat, dire explicitement :
- qu’il s’agit d’une commande déterministe à exécuter ;
- que le résultat automatique n’est pas encore disponible ;
- que tout statut de closeout reste non confirmé tant que le report YAML n’a pas été réellement produit.

## Contraintes

- Ne pas recalculer de contenu métier dans ce Stage 09.
- Ne pas modifier `docs/cores/releases/`.
- Ne pas modifier `docs/cores/current/`.
- Ne pas remplacer le script dédié par une interprétation libre.
- Ne pas considérer les copies archivées comme un substitut du report final actif.
- Le livrable attendu est constitué des fichiers et répertoires écrits dans le repo. Le retour chat doit être très succinct.

## Résultat terminal attendu

À la fin de l’exécution, si le script a bien été exécuté et les artefacts bien écrits, afficher uniquement :
1. les chemins exacts des artefacts écrits ;
2. le statut final du report de closeout : PASS | WARN | FAIL ;
3. un résumé ultra-court.
