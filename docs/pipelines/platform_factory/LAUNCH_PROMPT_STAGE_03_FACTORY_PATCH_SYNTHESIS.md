# LAUNCH PROMPT — STAGE_03_FACTORY_PATCH_SYNTHESIS

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_03_FACTORY_PATCH_SYNTHESIS` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

Source décisionnelle principale :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`

Artefacts gouvernés à patcher :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Socle canonique de contrôle :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Contexte d’exécution :
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- éventuellement une note de focalisation patch dans `docs/pipelines/platform_factory/inputs/`

## Contexte d’exécution obligatoire

- `platform_factory_arbitrage.md` est la source de vérité du stage.
- Les challenge reports historiques peuvent être relus si nécessaire pour traceabilité, mais ils ne doivent pas supplanter l’arbitrage final.
- Le résultat attendu doit être écrit dans le repo, dans le fichier YAML de sortie imposé ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.
- Le but est de produire un patchset exploitable au Stage 04, pas de réouvrir l’arbitrage.

## Fichier de sortie obligatoire

Écrire exactement un fichier dans le repo :
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`

## Ordre de lecture obligatoire

1. `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
2. `docs/cores/current/constitution.yaml`
3. `docs/cores/current/referentiel.yaml`
4. `docs/cores/current/link.yaml`
5. `docs/cores/current/platform_factory_architecture.yaml`
6. `docs/cores/current/platform_factory_state.yaml`
7. `docs/pipelines/platform_factory/pipeline.md`
8. `docs/prompts/shared/Make22PlatformFactoryPatch.md`
9. éventuellement la note de focalisation patch

## Objectif exact

Produire directement le patchset YAML final du stage, sous forme d’un fichier :
- borné
- traçable
- cohérent avec l’arbitrage final
- sans réouverture des décisions
- sans mélange illégitime entre :
  - architecture
  - state
  - pipeline
  - validator/tooling
  - manifest/release governance

## Exigences de contenu

Le patchset doit :
- ne contenir que des changements supportés explicitement par `platform_factory_arbitrage.md`
- exclure explicitement les sujets :
  - rejetés
  - différés
  - hors périmètre
  - relevant d’un validator/tooling plutôt que du canonique
  - relevant du pipeline plutôt que du canonique
  - relevant de la gouvernance release/manifest plutôt que du canonique
  - nécessitant encore une clarification humaine
- préserver strictement la séparation entre :
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
- rester proportionné à une baseline V0 déjà released
- être directement exploitable au Stage 04 de validation

## Règles de synthèse obligatoires

Pour chaque changement inclus dans le patchset, il faut pouvoir retrouver implicitement ou explicitement :
- la source décisionnelle dans `platform_factory_arbitrage.md`
- l’artefact cible principal
- la localisation probable
- le type d’opération attendu
- l’effet recherché
- le risque évité

Si un sujet est ambigu ou insuffisamment arbitré :
- ne pas improviser
- ne pas l’ajouter au patchset
- le laisser hors du patchset courant

## Contraintes

- Ne pas réouvrir l’arbitrage.
- Ne pas produire une simple analyse markdown à la place du YAML attendu.
- Ne pas écrire plusieurs fichiers.
- Ne pas modifier `docs/cores/current/` directement.
- Ne pas introduire un besoin de patch non arbitrée.
- Ne pas faire porter au canonique ce qui relève d’un validator, du pipeline ou de la gouvernance de release.
- Le livrable attendu est le fichier YAML écrit dans le repo. Le retour chat doit être très succinct.

## Structure attendue du fichier YAML

Produire un patchset YAML structuré, directement exploitable au stage suivant.

Le patchset doit au minimum :
- identifier clairement le patchset
- déclarer les fichiers cibles
- décrire des opérations suffisamment atomiques
- permettre de comprendre sans ambiguïté :
  - quoi changer
  - où
  - pourquoi
  - dans quel ordre si nécessaire

## Résultat terminal attendu

À la fin de l’exécution, afficher uniquement :
1. le chemin exact du fichier écrit
2. un résumé ultra-court
