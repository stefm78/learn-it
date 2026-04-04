# Platform Factory — Prompt usage

Ce document complète `pipeline.md` en indiquant quel prompt partagé utiliser à chaque étape du pipeline `platform_factory`.

Il ne remplace pas le pipeline.
Il en précise le mode opératoire côté IA.

---

## Vue d'ensemble

Prompts disponibles :
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make20PlatformFactoryAudit.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

---

## Mapping recommandé par stage

### STAGE_01_FACTORY_SCAN
Prompt recommandé :
- aucun prompt spécialisé obligatoire

But :
- inventorier les artefacts pertinents ;
- préparer l'audit.

---

### STAGE_02_FACTORY_AUDIT
Prompt principal :
- `docs/prompts/shared/Make20PlatformFactoryAudit.md`

Prompt complémentaire possible :
- `docs/prompts/shared/Challenge_platform_factory.md`

Rôle :
- `Make20PlatformFactoryAudit.md` produit l'audit structuré de pipeline ;
- `Challenge_platform_factory.md` peut être utilisé en second passage pour renforcer la recherche de faiblesses adversariales.

---

### STAGE_03_FACTORY_ARBITRAGE
Prompt principal :
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

Input attendu :
- audit structuré ;
- éventuellement challenge adversarial complémentaire.

---

### STAGE_04_FACTORY_PATCH_SYNTHESIS
Prompt principal :
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`

But :
- préparer la synthèse de patch en gardant la séparation architecture / state.

---

### STAGE_05_FACTORY_PATCH_VALIDATION
Prompt principal :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- valider la cohérence du patch avant ou après application selon le mode opératoire retenu.

---

### STAGE_06_FACTORY_APPLY
Prompt recommandé :
- aucun prompt spécialisé obligatoire

But :
- appliquer le patch ;
- matérialiser les artefacts ;
- générer les reports techniques.

---

### STAGE_07_FACTORY_CORE_VALIDATION
Prompt principal :
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

But :
- vérifier la cohérence finale du couple architecture / state et du rapport au socle canonique.

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

## Règle d'usage du challenge adversarial

`Challenge_platform_factory.md` n'est pas le prompt standard de pipeline.
C'est un prompt complémentaire de stress-test.

Usage recommandé :
- avant arbitrage, pour compléter l'audit ;
- ponctuellement, quand un point semble trop vite considéré comme acquis ;
- lors d'un run de challenge renforcé.

---

## Posture V0

Ce mapping est volontairement simple.
Il est suffisant pour lancer des premiers cycles cohérents de gouvernance `platform_factory`.
Il pourra être raffiné après quelques runs réels.
