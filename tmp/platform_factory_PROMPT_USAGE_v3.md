# Platform Factory — Prompt usage

Ce document complète `pipeline.md` en indiquant quel prompt partagé utiliser à chaque étape du pipeline `platform_factory`.

Il ne remplace pas le pipeline.
Il en précise le mode opératoire côté IA.

---

## Vue d'ensemble

Prompts disponibles :
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

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
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- valider la cohérence du patch avant application.

---

### STAGE_05_FACTORY_APPLY
Prompt recommandé :
- aucun prompt spécialisé obligatoire

But :
- appliquer le patch ;
- matérialiser les artefacts ;
- générer les reports techniques.

---

### STAGE_06_FACTORY_CORE_VALIDATION
Prompt principal :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- vérifier la cohérence finale du couple architecture / state et du rapport au socle canonique.

---

### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
Prompt recommandé :
- aucun prompt spécialisé obligatoire

But :
- matérialiser une release immutable avant toute promotion ;
- préparer les artefacts de release et leurs reports.

---

### STAGE_08_FACTORY_PROMOTION
Prompt recommandé :
- aucun prompt spécialisé obligatoire

But :
- promouvoir les artefacts validés ;
- produire le report de promotion.

---

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
Prompt principal :
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

But :
- produire une appréciation de clôture ;
- capitaliser les décisions ;
- préparer le prochain cycle.

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
