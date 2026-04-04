# LAUNCH PROMPT — STAGE_02_FACTORY_ARBITRAGE_MULTI

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter une proposition d’arbitrage pour le `STAGE_02_FACTORY_ARBITRAGE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

- tous les challenge reports présents dans :
  - `docs/pipelines/platform_factory/work/01_challenge/`
- le pipeline :
  - `docs/pipelines/platform_factory/pipeline.md`
- le prompt métier canonique d’arbitrage :
  - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

## Contexte d’exécution obligatoire

- Plusieurs IA peuvent exécuter ce launch prompt en parallèle.
- Chaque IA produit une proposition d’arbitrage indépendante.
- Cette proposition n’est pas encore l’arbitrage canonique final du stage.
- Le but est de fournir une contribution exploitable par une consolidation finale humaine-assistée.
- Le résultat attendu doit être écrit dans le repo, dans le fichier de sortie imposé ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

## Génération obligatoire d’un identifiant unique

Avant toute rédaction, générer un identifiant unique nommé `arbitrage_run_id`.

Format obligatoire :
- `PFARB_YYYYMMDD_AGENTTAG_RAND`

Contraintes :
- `YYYYMMDD` = date du jour au format compact
- `AGENTTAG` = identifiant court de l’IA, en majuscules, 3 à 8 caractères, sans espace
- `RAND` = suffixe alphanumérique aléatoire de 4 à 8 caractères, en majuscules

Exemples valides :
- `PFARB_20260404_GPT54_7KQ2`
- `PFARB_20260404_CLAUDE_X91M`
- `PFARB_20260404_GEMINI_A8T4Z`

Tu dois :
1. afficher d’abord le `arbitrage_run_id` choisi ;
2. l’utiliser dans le nom du fichier de sortie ;
3. le rappeler en tête du rapport.

## Fichier de sortie obligatoire

Écrire exactement un fichier dans le repo :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_<arbitrage_run_id>.md`

Exemple :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260404_GPT54_7KQ2.md`

## Travail attendu

À partir de tous les challenge reports disponibles, produire une proposition d’arbitrage structurée.

L’arbitrage doit au minimum :
- consolider les constats récurrents entre challenge reports ;
- distinguer les points retenus, rejetés, différés et hors périmètre ;
- indiquer les corrections à arbitrer avant patch ;
- préciser le lieu probable de correction :
  - architecture
  - state
  - pipeline
  - validator/tooling
  - manifest/release governance
  - hors périmètre factory
- identifier les points de consensus forts ;
- identifier les points non consensuels ou ambigus qui devront être discutés en consolidation finale.

## Contraintes

- Lire tous les `challenge_report*.md` présents dans `work/01_challenge/`.
- Ne pas ignorer un challenge report disponible.
- Ne pas produire de patch YAML.
- Ne pas écrire l’arbitrage canonique final du stage.
- Ne pas écraser un autre fichier d’arbitrage.
- Utiliser `docs/prompts/shared/Make21PlatformFactoryArbitrage.md` comme cadre principal de raisonnement et de structuration.
- Toute décision importante doit être reliée explicitement à un ou plusieurs challenge reports.
- Une réponse chat seule n’est pas un livrable suffisant : le livrable attendu est le fichier écrit dans le repo.

## Structure minimale obligatoire du rapport

Le fichier de sortie doit contenir au minimum :

- Titre
- `arbitrage_run_id`
- Date
- Liste des challenge reports considérés
- Résumé exécutif
- Synthèse des constats convergents
- Propositions d’arbitrage par thème
- Points retenus
- Points rejetés
- Points différés
- Points hors périmètre
- Points sans consensus ou nécessitant discussion finale
- Corrections à arbitrer avant patch

Pour chaque arbitrage important, préciser si possible :
- Élément concerné
- Localisation
- Problème ou question
- Statut proposé : retained | rejected | deferred | out_of_scope
- Gravité
- Justification
- Dépendance éventuelle à d’autres arbitrages
- Lieu probable de correction
- Niveau de consensus perçu : strong | medium | weak | conflicting

## Résultat terminal attendu

À la fin de l’exécution, afficher uniquement :
1. le `arbitrage_run_id`
2. le chemin exact du fichier écrit
3. un résumé ultra-court
