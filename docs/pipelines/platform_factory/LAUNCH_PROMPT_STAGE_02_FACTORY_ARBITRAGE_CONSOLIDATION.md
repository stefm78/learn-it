# LAUNCH PROMPT — STAGE_02_FACTORY_ARBITRAGE_CONSOLIDATION

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter la consolidation finale du `STAGE_02_FACTORY_ARBITRAGE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

- tous les challenge reports présents dans :
  - `docs/pipelines/platform_factory/work/01_challenge/`
- toutes les propositions d’arbitrage présentes dans :
  - `docs/pipelines/platform_factory/work/02_arbitrage/`
  - plus précisément tous les fichiers `arbitrage_proposal_*.md`
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

## Génération obligatoire d’un identifiant unique

Avant toute rédaction, générer un identifiant unique nommé `arbitrage_consolidation_run_id`.

Format obligatoire :
- `PFARBCON_YYYYMMDD_AGENTTAG_RAND`

Contraintes :
- `YYYYMMDD` = date du jour au format compact
- `AGENTTAG` = identifiant court de l’IA, en majuscules, 3 à 8 caractères, sans espace
- `RAND` = suffixe alphanumérique aléatoire de 4 à 8 caractères, en majuscules

Exemples valides :
- `PFARBCON_20260404_GPT54_7KQ2`
- `PFARBCON_20260404_CLAUDE_X91M`
- `PFARBCON_20260404_GEMINI_A8T4Z`

Tu dois :
1. afficher d’abord le `arbitrage_consolidation_run_id` choisi ;
2. le rappeler en tête du rapport final.

## Fichier de sortie obligatoire

Écrire exactement un fichier canonique :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`

## Travail attendu

À partir de tous les challenge reports et de toutes les propositions d’arbitrage disponibles, produire l’arbitrage consolidé canonique du stage.

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
- Lire tous les `arbitrage_proposal_*.md` présents dans `work/02_arbitrage/`.
- Ne pas ignorer un challenge report ou une proposition d’arbitrage disponible.
- Ne pas produire de patch YAML.
- Utiliser `docs/prompts/shared/Make21PlatformFactoryArbitrage.md` comme cadre principal de raisonnement et de structuration.
- Toute décision consolidée importante doit être reliée explicitement à un ou plusieurs challenge reports et, si utile, à une ou plusieurs propositions d’arbitrage.
- Les points sans consensus ne doivent pas être masqués.
- Les points non tranchables automatiquement doivent être explicitement envoyés en discussion humaine.

## Structure minimale obligatoire du rapport final

Le fichier de sortie doit contenir au minimum :

- Titre
- `arbitrage_consolidation_run_id`
- Date
- Liste des challenge reports considérés
- Liste des arbitrage proposals considérées
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

À la fin de l’exécution, afficher uniquement :
1. le `arbitrage_consolidation_run_id`
2. le chemin exact du fichier écrit
3. un résumé ultra-court
