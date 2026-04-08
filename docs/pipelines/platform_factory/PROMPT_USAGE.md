# Platform Factory — Prompt usage

Ce document complète `pipeline.md` en indiquant quel prompt utiliser à chaque étape du pipeline `platform_factory`.

Il ne remplace pas le pipeline.
Il en précise le mode opératoire côté IA.

---

## Vue d'ensemble

Prompts disponibles :
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

Companion opérateur :
- `docs/pipelines/platform_factory/OPERATOR_RUNBOOK.md`

---

## Mapping recommandé par stage

### STAGE_01_CHALLENGE
Prompt principal :
- `docs/prompts/shared/Challenge_platform_factory.md`

But :
- challenger la baseline release actuelle de la factory ;
- identifier faiblesses, ambiguïtés, contradictions, trous de contrat ou dérives ;
- préparer les findings pour arbitrage.

---

### STAGE_02_FACTORY_ARBITRAGE
Prompt principal :
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

Input attendu :
- un ou plusieurs challenge reports ;
- éventuellement des arbitrages humains complémentaires.

---

### STAGE_03_FACTORY_PATCH_SYNTHESIS
Prompt principal :
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`

But :
- préparer la synthèse de patch en gardant la séparation architecture / state.

---

### STAGE_04_FACTORY_PATCH_VALIDATION
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`

Prompt compagnon :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- exécuter la validation pré-apply ;
- produire le YAML automatique de validation ;
- produire le report markdown humain cohérent avec ce YAML.

---

### STAGE_05_FACTORY_APPLY
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`

But :
- préparer la sandbox ;
- exécuter le dry-run puis l’apply réel ;
- matérialiser les artefacts patchés et le report d’exécution.

---

### STAGE_06_FACTORY_CORE_VALIDATION
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`

Prompt compagnon :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- exécuter la validation post-apply ;
- produire le YAML automatique de validation ;
- produire le report markdown humain cohérent avec ce YAML.

---

### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

But :
- calculer le release plan déterministe ;
- ne matérialiser une release que si `release_required: true` ;
- produire le report de matérialisation et les release notes.

---

### STAGE_08_FACTORY_PROMOTE_CURRENT
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`

But :
- promouvoir la release matérialisée vers `docs/cores/current/` ;
- produire le report de promotion ;
- rester idempotent si la release est déjà current.

---

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
Prompt principal :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

But :
- exécuter le closeout déterministe du run ;
- archiver `work/`, `reports/` et `outputs/` ;
- produire `platform_factory_closeout_report.yaml` et `platform_factory_summary.md` ;
- réinitialiser `work/` pour le prochain cycle.

---

## Mode opératoire recommandé pour une IA sans contexte

1. Lire d’abord `docs/pipelines/platform_factory/pipeline.md`.
2. Lire ensuite ce document.
3. Lire ensuite le prompt principal du stage visé.
4. Si le stage implique un script déterministe, donner d’abord la commande exacte à exécuter, sans simuler le résultat.
5. Après exécution humaine de la commande, relire le YAML ou le report réellement produit, puis annoncer seulement :
   - les chemins écrits ;
   - le statut ;
   - la suite immédiate.

Pour les Stages 01 à 03, il n’y a pas de commande shell obligatoire : l’IA doit écrire directement le livrable dans le repo, ou fournir un contenu prêt à déposer exactement au bon chemin.

---

## Règle d'usage

Le point d'entrée normal d'un run `platform_factory` est le challenge de la baseline release active.
Le pipeline ne prévoit pas de stage d'audit initial ni de stage de scan séparé dans son flux nominal.
La release materialization reste distincte de la promotion, comme dans les autres pipelines de gouvernance du repo.

---

## Posture V0

Ce mapping est volontairement simple.
Il est suffisant pour lancer des premiers cycles cohérents de gouvernance `platform_factory`.
Il pourra être raffiné après quelques runs réels.
