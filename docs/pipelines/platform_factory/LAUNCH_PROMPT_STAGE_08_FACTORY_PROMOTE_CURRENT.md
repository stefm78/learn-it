# LAUNCH PROMPT — STAGE_08_FACTORY_PROMOTE_CURRENT

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_08_FACTORY_PROMOTE_CURRENT` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`
- spécification détaillée :
  - `docs/pipelines/platform_factory/STAGE_08_FACTORY_PROMOTE_CURRENT.md`

## Inputs obligatoires

Plan et report Stage 07 :
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

Release matérialisée :
- `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
- `docs/cores/releases/<release_id>/platform_factory_state.yaml`
- `docs/cores/releases/<release_id>/manifest.yaml`

État courant éventuel :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Script dédié :
- `docs/patcher/shared/promote_platform_factory_current.py`

## Préconditions obligatoires

- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`.
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml` doit être en `status: PASS`.
- La release ciblée doit exister physiquement sous `docs/cores/releases/<release_id>/`.
- Le manifest de release doit être présent et lisible.
- Ne pas promouvoir depuis `work/05_apply/patched/`.
- Ne pas simuler une promotion si le script n’a pas tourné.

## Contexte d’exécution obligatoire

- `docs/cores/releases/` est la source de vérité des releases publiées.
- `docs/cores/current/` est uniquement la vue active de la release promue.
- Ce stage ne doit modifier que `docs/cores/current/` et le report de promotion.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.
- La promotion doit rester idempotente.
- Il ne faut pas modifier `docs/cores/current/manifest.yaml` par défaut à ce stade V0.

## Règle anti-simulation obligatoire

- Ne jamais simuler le résultat d’un script déterministe.
- Ne jamais annoncer qu’une release a été promue si le script n’a pas réellement tourné.
- Ne jamais annoncer un `promotion_mode`, un `release_id` promu ou un `status` comme si la promotion avait été constatée si ce n’est pas le cas.
- Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
- Dans ce cas, il faut donner clairement la commande exacte à exécuter.
- Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme le résultat réel du script.

## Fichiers de sortie obligatoires

- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`

## Étape d’exécution obligatoire

Exécuter :

```bash
python docs/patcher/shared/promote_platform_factory_current.py \
  ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
  ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
  ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml
```

## Vérification obligatoire après exécution

- Lire `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`
- Vérifier explicitement :
  - `status`
  - `release_id`
  - `source_release_path`
  - `promotion_mode`
  - `files_promoted`
- Si le report n’est pas en `status: PASS`, le stage ne franchit pas 08.
- Si `promotion_mode: already_current`, considérer la promotion comme idempotente et valide.

## Si une commande doit être exécutée par l’humain dans le chat

Avant toute interprétation du résultat, dire explicitement :
- qu’il s’agit d’une commande déterministe à exécuter ;
- que le résultat automatique n’est pas encore disponible ;
- que tout statut de promotion reste non confirmé tant que le report YAML n’a pas été réellement produit.

## Contraintes

- Ne pas promouvoir depuis `work/05_apply/patched/`.
- Ne pas réécrire la logique des artefacts pendant la promotion.
- Ne pas modifier `docs/cores/releases/<release_id>/`.
- Ne pas modifier `docs/cores/current/manifest.yaml` par défaut dans ce Stage 08 V0.
- Ne pas remplacer le script dédié par une interprétation libre.
- Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

## Résultat terminal attendu

À la fin de l’exécution, si le script a bien été exécuté et les artefacts bien écrits, afficher uniquement :
1. les chemins exacts des artefacts écrits
2. le statut final du report de promotion : PASS | WARN | FAIL
3. un résumé ultra-court
