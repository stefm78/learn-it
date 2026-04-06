# Platform Factory — Prompt usage

Ce document complète `pipeline.md` en indiquant :
- quel prompt partagé pilote le raisonnement métier ;
- quel launch prompt pipeline-local sert à exécuter concrètement chaque stage ;
- quels scripts déterministes doivent être utilisés lorsque le stage ne doit pas reposer sur une simple interprétation IA.

Il ne remplace pas le pipeline.
Il en précise le mode opératoire côté IA et côté exécution outillée.

---

## Vue d'ensemble

### Shared prompts métier

- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

### Launch prompts pipeline-locaux

- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_02_FACTORY_ARBITRAGE_MULTI.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_02_FACTORY_ARBITRAGE_CONSOLIDATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_03_FACTORY_PATCH_SYNTHESIS.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

### Scripts déterministes dédiés

- `docs/patcher/shared/validate_platform_factory_patchset.py`
- `docs/patcher/shared/apply_platform_factory_patchset.py`
- `docs/patcher/shared/validate_platform_factory_core.py`
- `docs/patcher/shared/build_platform_factory_release_plan.py`
- `docs/patcher/shared/materialize_platform_factory_release.py`
- `docs/patcher/shared/promote_platform_factory_current.py`
- `docs/patcher/shared/closeout_platform_factory_run.py`

---

## Mapping recommandé par stage

### STAGE_01_CHALLENGE
Shared prompt principal :
- `docs/prompts/shared/Challenge_platform_factory.md`

Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`

But :
- challenger la baseline release actuelle de la factory ;
- produire un ou plusieurs challenge reports indépendants.

---

### STAGE_02_FACTORY_ARBITRAGE
Shared prompt principal :
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

Launch prompts :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_02_FACTORY_ARBITRAGE_MULTI.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_02_FACTORY_ARBITRAGE_CONSOLIDATION.md`

But :
- produire plusieurs arbitrages intermédiaires ;
- consolider ensuite un arbitrage canonique unique ;
- réserver les points non consensuels à discussion humaine.

---

### STAGE_03_FACTORY_PATCH_SYNTHESIS
Shared prompt principal :
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`

Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_03_FACTORY_PATCH_SYNTHESIS.md`

But :
- produire le patchset YAML final du stage ;
- rester strictement fidèle à l’arbitrage canonique.

---

### STAGE_04_FACTORY_PATCH_VALIDATION
Shared prompt principal :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`

Script déterministe obligatoire :
- `docs/patcher/shared/validate_platform_factory_patchset.py`

But :
- produire la trace canonique automatique de validation structurelle ;
- compléter par une lecture humaine de cohérence pré-apply.

---

### STAGE_05_FACTORY_APPLY
Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`

Script déterministe obligatoire :
- `docs/patcher/shared/apply_platform_factory_patchset.py`

But :
- appliquer le patchset en sandbox ;
- exiger un dry-run PASS avant apply réel ;
- matérialiser les artefacts patchés dans `work/05_apply/patched/`.

---

### STAGE_06_FACTORY_CORE_VALIDATION
Shared prompt principal :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`

Script déterministe obligatoire :
- `docs/patcher/shared/validate_platform_factory_core.py`

But :
- produire la trace canonique automatique de validation post-apply ;
- compléter par une lecture humaine de l’état patché.

---

### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

Scripts déterministes obligatoires :
- `docs/patcher/shared/build_platform_factory_release_plan.py`
- `docs/patcher/shared/materialize_platform_factory_release.py`

But :
- calculer de manière déterministe le release plan ;
- matérialiser une release immuable ;
- ne jamais modifier `docs/cores/current/`.

---

### STAGE_08_FACTORY_PROMOTE_CURRENT
Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`

Script déterministe obligatoire :
- `docs/patcher/shared/promote_platform_factory_current.py`

But :
- promouvoir explicitement la release matérialisée vers `docs/cores/current/` ;
- garantir l’idempotence ;
- produire le report canonique de promotion.

---

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
Shared prompt principal :
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

Launch prompt :
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

Script déterministe obligatoire :
- `docs/patcher/shared/closeout_platform_factory_run.py`

But :
- clôturer explicitement le run ;
- archiver `work/`, `reports/` et `outputs/` ;
- réinitialiser `work/` pour une nouvelle exécution.

---

## Règles d’usage

- Le point d’entrée normal d’un run `platform_factory` est le challenge de la baseline release active.
- Le pipeline ne prévoit pas de stage d’audit initial ni de stage de scan séparé dans son flux nominal.
- La release materialization reste distincte de la promotion.
- Toute étape outillée par script déterministe doit interdire la simulation de résultat.
- Si le script n’est pas exécuté dans le tour, l’IA doit le dire explicitement dans le chat et fournir la commande exacte à lancer.

---

## Posture V0

Ce mapping est volontairement plus opérationnel que la première version de `PROMPT_USAGE.md`.
Il reflète la réalité actuelle du pipeline `platform_factory` :
- launch prompts dédiés par stage ;
- scripts dédiés pour les étapes déterministes ;
- garde-fous anti-simulation.
