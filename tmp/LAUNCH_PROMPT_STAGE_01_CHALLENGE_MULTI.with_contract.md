---
CONTRAT_ORCHESTRATEUR:
  stage: STAGE_01_CHALLENGE
  pipeline_spec: docs/pipelines/platform_factory/pipeline.md

  # Fichiers que l'orchestrateur doit fournir au contexte de travail
  inputs:
    - path: docs/cores/current/constitution.yaml
      required: true
    - path: docs/cores/current/referentiel.yaml
      required: true
    - path: docs/cores/current/link.yaml
      required: true
    - path: docs/cores/current/platform_factory_architecture.yaml
      required: true
    - path: docs/cores/current/platform_factory_state.yaml
      required: true

  # Fichiers que l'orchestrateur doit considérer comme sortie canonique
  outputs:
    canonical_report_dir: docs/pipelines/platform_factory/work/01_challenge/
    canonical_report_pattern: challenge_report_*.md
    allow_additional_files: true   # laisser l'IA être créative, mais ignorer ces fichiers côté pipeline

  # Ce que l'orchestrateur doit récupérer sur stdout à la fin
  stdout_contract:
    ordered_lines:
      - name: challenge_run_id
        description: "Identifiant unique du run (PFCHAL_...)"
      - name: report_path
        description: "Chemin exact du fichier de rapport canonique écrit"
      - name: ultra_short_summary
        description: "Résumé très court en une ou deux phrases"

  # Politique de langue
  language:
    input_reading: FR|EN
    report_writing: FR
    tags_and_severity: EN
---

# LAUNCH PROMPT — STAGE_01_CHALLENGE

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_01_CHALLENGE` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Artefacts à challenger

- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

## Socle canonique à lire avant challenge

- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

## Prompt métier canonique à utiliser

- `docs/prompts/shared/Challenge_platform_factory.md`

## Contexte d’exécution obligatoire

- La baseline `platform_factory` est déjà released et déjà posée dans `docs/cores/current/`.
- Ne pas faire de scan exploratoire.
- Ne pas faire d’audit de découverte.
- Faire un challenge ciblé d’une baseline released.
- Le but est de produire un rapport de challenge exploitable pour `STAGE_02_FACTORY_ARBITRAGE`.

## Génération obligatoire d’un identifiant unique

Avant toute rédaction, générer un identifiant unique nommé `challenge_run_id`.

Format obligatoire :
- `PFCHAL_YYYYMMDD_AGENTTAG_RAND`

Contraintes :
- `YYYYMMDD` = date du jour au format compact
- `AGENTTAG` = identifiant court de l’IA, en majuscules, 3 à 8 caractères, sans espace
- `RAND` = suffixe alphanumérique aléatoire de 4 à 8 caractères, en majuscules

Exemples valides :
- `PFCHAL_20260404_GPT54_7KQ2`
- `PFCHAL_20260404_CLAUDE_X91M`
- `PFCHAL_20260404_GEMINI_A8T4Z`

Tu dois :
1. afficher d’abord le `challenge_run_id` choisi ;
2. l’utiliser dans le nom du fichier de sortie ;
3. le rappeler en tête du rapport.

## Fichier de sortie obligatoire

Écrire exactement un fichier :
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_<challenge_run_id>.md`

Exemple :
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_7KQ2.md`

## Ordre de lecture obligatoire

1. `docs/cores/current/constitution.yaml`
2. `docs/cores/current/referentiel.yaml`
3. `docs/cores/current/link.yaml`
4. `docs/cores/current/platform_factory_architecture.yaml`
5. `docs/cores/current/platform_factory_state.yaml`
6. `docs/pipelines/platform_factory/pipeline.md`

## Ce qu’il faut produire

Un challenge structuré portant au minimum sur :
- compatibilité constitutionnelle
- cohérence interne architecture/state
- frontières de couche
- contrat minimal d’application produite
- validated derived execution projections
- maturité reconnue vs maturité réelle
- multi-IA parallel readiness
- gouvernance release / manifest / traçabilité
- implémentabilité du pipeline
- scénarios adversariaux plausibles
- priorisation des risques

## Contraintes

- Ne pas produire de patch YAML.
- Ne pas arbitrer à la place de l’humain.
- Ne pas proposer de scan ou d’audit initial.
- Ne pas ignorer Constitution / Référentiel / LINK.
- Ne pas écrire plusieurs fichiers.
- Ne pas réutiliser un nom de fichier générique susceptible d’entrer en collision.
- Toute critique importante doit être ancrée dans un élément explicite des artefacts ou du pipeline.
- Utiliser `docs/prompts/shared/Challenge_platform_factory.md` comme cadre principal de raisonnement et de structuration.

## Structure minimale obligatoire du rapport

Le fichier de sortie doit contenir au minimum :

- Titre
- `challenge_run_id`
- Date
- Artefacts challengés
- Résumé exécutif
- Carte de compatibilité constitutionnelle
- Analyse détaillée par axe
- Risques prioritaires
- Points V0 acceptables
- Corrections à arbitrer avant patch

Pour chaque problème important, préciser si possible :
- Élément concerné
- Localisation
- Nature du problème
- Type de problème
- Gravité
- Impact sur la factory
- Impact sur une application produite
- Impact sur le travail des IA
- Impact sur la gouvernance/release
- Correction à arbitrer
- Lieu probable de correction :
  - architecture
  - state
  - pipeline
  - validator/tooling
  - manifest/release governance
  - hors périmètre factory

## Résultat terminal attendu

À la fin de l’exécution, afficher uniquement :
1. le `challenge_run_id`
2. le chemin exact du fichier écrit
3. un résumé ultra-court
