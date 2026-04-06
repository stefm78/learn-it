# LAUNCH PROMPT — STAGE_02_FACTORY_ARBITRAGE_CONSOLIDATION

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter la consolidation finale du `STAGE_02_FACTORY_ARBITRAGE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

- tous les challenge reports présents dans :
  - `docs/pipelines/platform_factory/work/01_challenge/`
- tous les fichiers `.md` présents dans :
  - `docs/pipelines/platform_factory/work/02_arbitrage/`
  - en excluant strictement `platform_factory_arbitrage.md`
- le pipeline :
  - `docs/pipelines/platform_factory/pipeline.md`
- le prompt métier canonique d’arbitrage :
  - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- éventuellement des notes ou arbitrages humains complémentaires s’ils sont fournis dans `work/02_arbitrage/` ou `inputs/`

## Contexte d’exécution obligatoire

- Cette exécution est la consolidation finale du stage.
- Son rôle est de transformer plusieurs propositions d’arbitrage en un arbitrage canonique unique.
- Elle doit conserver les convergences fortes.
- Elle doit expliciter les zones sans consensus.
- Elle doit préparer la discussion humaine sur les points encore ouverts.
- Le résultat attendu ne doit pas être écrit immédiatement dans `platform_factory_arbitrage.md`.
- Avant validation humaine explicite, le travail doit rester dans les échanges et servir à instruire les arbitrages.
- `platform_factory_arbitrage.md` n’est écrit qu’avec l’approbation explicite de l’humain.

## Fichier de sortie canonique final

Le fichier canonique final de stage est :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`

Mais ce fichier ne doit être écrit qu’après approbation explicite de l’humain.

## Travail attendu

À partir de tous les challenge reports et de tous les fichiers `.md` disponibles dans `work/02_arbitrage/` sauf `platform_factory_arbitrage.md`, produire la consolidation finale d’arbitrage.

L’arbitrage final doit au minimum :
- consolider les convergences majeures ;
- trancher lorsque le consensus est suffisant ;
- préserver explicitement les points non consensuels ;
- formuler la discussion requise sur les désaccords restants ;
- distinguer les points retenus, rejetés, différés et hors périmètre ;
- préparer le passage au patch pour les points suffisamment arbitrés ;
- préparer la discussion humaine pour les points non suffisamment arbitrés.

## Contraintes

- Lire tous les `challenge_report*.md` présents dans `work/01_challenge/`.
- Lire tous les fichiers `.md` présents dans `work/02_arbitrage/`, sauf `platform_factory_arbitrage.md`.
- Ne pas ignorer un challenge report ou un fichier `.md` d’arbitrage disponible.
- Ne pas produire de patch YAML.
- Utiliser `docs/prompts/shared/Make21PlatformFactoryArbitrage.md` comme cadre principal de raisonnement et de structuration.
- Toute décision consolidée importante doit être reliée explicitement à un ou plusieurs challenge reports et, si utile, à une ou plusieurs propositions d’arbitrage.
- Les points sans consensus ne doivent pas être masqués.
- Les points non tranchables automatiquement doivent être explicitement envoyés en discussion humaine.
- Tant que l’humain n’a pas explicitement validé la consolidation finale, ne pas écrire `platform_factory_arbitrage.md`.

## Structure minimale obligatoire du travail de consolidation

Le contenu préparatoire ou final doit contenir au minimum :

- Titre
- Date
- Liste des challenge reports considérés
- Liste des arbitrage reports considérés
- Résumé exécutif
- Décisions consolidées
- Points retenus
- Points rejetés
- Points différés
- Points hors périmètre
- Points sans consensus
- Discussion humaine requise
- Corrections à arbitrer avant patch

## Discussion humaine obligatoire

Pour chaque point sans consensus ou insuffisamment tranché, produire une section explicite contenant au minimum :
- Élément concerné
- Localisation
- Nature du désaccord
- Positions principales observées
- Risques si l’on tranche trop vite
- Option A
- Option B
- éventuellement Option C
- Recommandation provisoire
- Décision humaine attendue
- Lieu probable de correction après décision

## Format de décision recommandé

Pour chaque arbitrage important, préciser si possible :
- Élément concerné
- Localisation
- Problème ou question
- Statut final : retained | rejected | deferred | out_of_scope | pending_human_decision
- Gravité
- Justification consolidée
- Dépendance éventuelle à d’autres arbitrages
- Lieu probable de correction
- Niveau de consensus final : strong | medium | weak | conflicting

## Résultat terminal attendu

Tant qu’il n’y a pas d’approbation humaine explicite :
- ne pas écrire `platform_factory_arbitrage.md`
- poursuivre la discussion d’arbitrage avec l’humain
- fournir les éléments nécessaires pour trancher les désaccords

Après approbation humaine explicite :
1. écrire `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
2. afficher le chemin exact du fichier écrit
3. afficher un résumé ultra-court
