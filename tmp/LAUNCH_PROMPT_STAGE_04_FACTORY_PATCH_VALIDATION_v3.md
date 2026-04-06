# LAUNCH PROMPT — STAGE_04_FACTORY_PATCH_VALIDATION

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_04_FACTORY_PATCH_VALIDATION` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Mode de validation attendu

- Mode attendu : `PRE_APPLY_PATCH_VALIDATION`
- Il s’agit ici de valider le patchset avant application.
- Il ne s’agit pas de valider un état post-apply.

## Inputs obligatoires

Source décisionnelle :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`

Patchset à valider :
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`

Artefacts courants de référence :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Socle canonique de contrôle :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Contexte d’exécution :
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/patcher/shared/validate_platform_factory_patchset.py`
- éventuellement une note de focalisation validation dans `docs/pipelines/platform_factory/inputs/`

## Contexte d’exécution obligatoire

- `platform_factory_arbitrage.md` est la source de vérité sur ce qui devait être retenu, rejeté, différé ou laissé hors périmètre.
- `platform_factory_patchset.yaml` est l’objet principal à valider.
- Le résultat attendu doit être écrit dans le repo, dans les fichiers de sortie imposés ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.
- Le but est de décider si le patchset peut franchir le stage avant apply.
- Ne pas réouvrir l’arbitrage.
- Ne pas compenser une ambiguïté par une réécriture implicite.

## Règle anti-simulation obligatoire

- Ne jamais simuler le résultat d’un script déterministe.
- Ne jamais annoncer un `PASS`, `WARN` ou `FAIL` comme si le script avait été exécuté si ce n’est pas le cas.
- Ne jamais prétendre qu’un fichier de sortie automatique existe si le script ne l’a pas réellement généré.
- Si le script n’est pas réellement exécuté dans le repo au cours de ce tour, il faut l’indiquer explicitement dans le chat.
- Dans ce cas, il faut donner clairement la ou les commandes exactes à exécuter.
- Toute conclusion métier complémentaire doit être présentée comme une lecture préparatoire ou conditionnelle, jamais comme le résultat du script.

## Fichiers de sortie obligatoires

Écrire exactement les fichiers suivants dans le repo :
- `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_patch_validation_report.md`

## Ordre de lecture obligatoire

1. `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`
2. `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
3. `docs/cores/current/constitution.yaml`
4. `docs/cores/current/referentiel.yaml`
5. `docs/cores/current/link.yaml`
6. `docs/cores/current/platform_factory_architecture.yaml`
7. `docs/cores/current/platform_factory_state.yaml`
8. `docs/pipelines/platform_factory/pipeline.md`
9. `docs/prompts/shared/Make23PlatformFactoryValidation.md`
10. `docs/patcher/shared/validate_platform_factory_patchset.py`
11. éventuellement la note de focalisation validation

## Étape automatique obligatoire

Commencer par exécuter la validation structurelle automatique suivante :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/04_patch_validation
python docs/patcher/shared/validate_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
  > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml
```

Cette sortie YAML constitue la trace canonique automatique du Stage 04.

## Si le script n’est pas exécuté dans ce tour

Avant toute autre réponse, écrire explicitement dans le chat :
- qu’il s’agit d’une commande déterministe à exécuter ;
- que le résultat automatique n’est pas encore disponible ;
- que tout statut global restera non confirmé tant que le fichier YAML n’aura pas été réellement produit.

## Objectif exact

Valider que `platform_factory_patchset.yaml` est :
- fidèle à l’arbitrage
- cohérent avec la séparation architecture / state
- compatible avec le socle canonique
- assez précis, borné et traçable pour être appliqué
- exempt de mélange avec des sujets relevant en réalité :
  - du pipeline
  - des validators / tooling
  - de la release governance
  - d’un sujet encore non clarifié humainement

## Vérifications obligatoires

La validation doit au minimum couvrir :
- adéquation au mode PRE_APPLY
- fidélité à l’arbitrage
- séparation architecture / state
- cohérence interne et cohérence croisée
- compatibilité avec Constitution / Référentiel / LINK
- cohérence du contrat minimal d’application produite
- gouvernabilité des projections dérivées
- maintien de la posture multi-IA
- validabilité opérationnelle du patchset
- anomalies, warnings et sévérité

## Contraintes

- Être explicite sur : `PASS`, `WARN`, `FAIL`.
- Ne pas produire un nouveau patch complet ici.
- Ne pas écrire une simple analyse chat à la place des livrables attendus.
- Ne pas inventer des inputs ou des conclusions non supportées.
- Ne pas réouvrir les arbitrages déjà fermés.
- Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

## Structure attendue du YAML de validation

Le fichier :
- `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`

Doit être la sortie du validateur automatique dédié.

## Structure attendue du report markdown

Le fichier :
- `docs/pipelines/platform_factory/reports/platform_factory_patch_validation_report.md`

Doit être une lecture humaine cohérente du YAML de validation, avec au minimum :
- Résumé exécutif
- Qualification du contexte de validation
- Décision globale
- Vérifications par axe
- Anomalies bloquantes
- Warnings
- Conditions éventuelles avant apply

## Résultat terminal attendu

À la fin de l’exécution, si le script a bien été exécuté et les fichiers bien écrits, afficher uniquement :
1. les chemins exacts des fichiers écrits
2. le statut global : PASS | WARN | FAIL
3. un résumé ultra-court
