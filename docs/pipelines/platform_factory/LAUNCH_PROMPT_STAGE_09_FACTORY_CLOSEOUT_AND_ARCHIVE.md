# LAUNCH PROMPT — STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

Promotion réussie :
- `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`

Traçabilité release :
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

Script dédié :
- `docs/patcher/shared/closeout_platform_factory_run.py`

## Préconditions obligatoires

- `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml` doit être en `status: PASS`.
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`.
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml` doit être en `status: PASS`.
- La release promue doit exister réellement sous `docs/cores/releases/<release_id>/`.
- Ne pas simuler un closeout si le script n’a pas tourné.

## Contexte d’exécution obligatoire

- Le Stage 09 clôture explicitement le run terminé.
- Il archive `work/`, `reports/` et `outputs/` sous `docs/pipelines/platform_factory/archive/<release_id>/`.
- Il recrée un `work/` vide, prêt pour une nouvelle exécution.
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

- `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
- `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
- `docs/pipelines/platform_factory/archive/<release_id>/`
- `docs/pipelines/platform_factory/work/` recréé vide

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

- Lire `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
- Vérifier explicitement :
  - `status`
  - `release_id`
  - `source_release_path`
  - `promotion_mode`
  - `archive_path`
  - `work_reset`
- Lire `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
- Vérifier que `docs/pipelines/platform_factory/work/` a bien été recréé vide.
- Si le report n’est pas en `status: PASS`, le pipeline ne peut pas être considéré comme proprement clôturé.

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
- Le livrable attendu est constitué des fichiers et répertoires écrits dans le repo. Le retour chat doit être très succinct.

## Résultat terminal attendu

À la fin de l’exécution, si le script a bien été exécuté et les artefacts bien écrits, afficher uniquement :
1. les chemins exacts des artefacts écrits
2. le statut final du report de closeout : PASS | WARN | FAIL
3. un résumé ultra-court
