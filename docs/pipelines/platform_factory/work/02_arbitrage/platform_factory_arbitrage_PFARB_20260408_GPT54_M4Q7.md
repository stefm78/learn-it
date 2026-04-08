# Proposition d’arbitrage — Platform Factory Stage 02

## arbitrage_run_id

`PFARB_20260408_GPT54_M4Q7`

## Date

2026-04-08

## Challenge reports considérés

- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_7K2R.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260408_GPT54_Q7M2.md`

## Note de méthode

Les quatre rapports du 2026-04-04 challengent une baseline `V0.1 / CURRENT_V0`.  
Le rapport du 2026-04-08 challenge la baseline courante `V0.2 / RELEASE_CANDIDATE`.  
La présente proposition d’arbitrage consolide tous les findings disponibles, mais tranche à partir de l’état réel actuel du repo et des artefacts en `main` au 2026-04-08.

En particulier, les findings anciens signalant des prompts ou specs “potentiellement absents” ont été recontrôlés contre le repo actuel avant décision.

---

## Résumé exécutif

Consensus fort sur quatre sujets structurants :

1. **Le contrat minimal d’application produite doit être renforcé maintenant sur la preuve constitutionnelle runtime.** La factory ne peut pas rester dans un état où une application produite peut paraître valide sans attestation explicite de localité runtime, d’absence de génération runtime interdite, et de gouvernance patch conforme.

2. **Le mécanisme de `validated_derived_execution_projection` doit être fermé minimalement avant tout usage opérationnel fort.** Le principe est bon ; son instrumentation minimale manque encore : décision de stockage, protocole de régénération, définition de validation, traçabilité de version/source.

3. **La multi-IA readiness doit être requalifiée comme exigence juste mais encore insuffisamment opérable.** Il faut au minimum une convention de décomposition, d’assemblage et de résolution de conflits, sans exiger encore une sophistication V1.

4. **La posture release/current/manifest doit être clarifiée.** Les artefacts `platform_factory_*` sont bien dans `current/`, mais l’absence d’intégration au manifest officiel courant crée une ambiguïté de statut qu’il faut gouverner explicitement.

En revanche, plusieurs findings du 2026-04-04 ne doivent **pas** être retenus tels quels car ils sont désormais dépassés par l’état du repo :

- l’idée que `STAGE_07` et `STAGE_08` reposeraient sur des specs absentes est infirmée ;
- l’idée que les prompts partagés requis seraient possiblement manquants est trop faible pour justifier un patch canonique à ce stade ;
- l’idée qu’il faudrait forcément séparer `Make23` en deux prompts distincts n’est pas retenue, car le prompt actuel documente explicitement ses deux modes.

Le patch courant doit donc se concentrer sur :
- **preuve constitutionnelle minimale** ;
- **gouvernance minimale des projections dérivées** ;
- **honnêteté de maturité dans le state** ;
- **protocole multi-IA minimal** ;
- **clarification de posture release/current/manifest**.

---

## Synthèse des constats convergents

### Convergences fortes

- La baseline est utile, cohérente, et patchable ; elle ne doit pas être rejetée ni refondue.
- La séparation `architecture` / `state` est globalement correcte et doit être préservée.
- La séparation générique / spécifique est globalement correcte et ne doit pas être affaiblie.
- Le contrat minimal d’application produite reste trop peu probant sur les invariants constitutionnels runtime.
- Les `validated_derived_execution_projections` restent le point le plus exposé à la dérive normative silencieuse.
- La multi-IA readiness est correctement reconnue comme exigence de premier rang, mais pas encore suffisamment gouvernée.
- Le statut `current` des artefacts `platform_factory_*` reste ambigu tant que le dispositif officiel de manifest courant ne les intègre pas.

### Convergences moyennes

- Certaines capacités du `state` sont surévaluées, surtout autour des projections dérivées.
- Le pipeline V0 est utilisable, mais encore trop dépendant du prompt et pas assez outillé.
- Le contrat minimal a besoin d’un meilleur niveau de précision probante sans exiger encore le schéma final complet.

### Convergences faibles ou conflictuelles

- Le reclassement de `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` en `partial` n’est pas consensuel.
- La nécessité d’un prompt distinct pour STAGE_04 vs STAGE_06 n’est pas démontrée dans l’état actuel du repo.
- L’exigence d’un vrai artefact de release formel dès maintenant pour la baseline V0 n’est pas totalement tranchée : le besoin de clarification est réel, mais le mécanisme exact peut relever d’une gouvernance de release transverse plutôt que d’un patch canonique immédiat.

---

## Propositions d’arbitrage par thème

### Thème A — Preuve constitutionnelle minimale du contrat d’application produite

**Décision proposée : retained_now**  
Il faut renforcer maintenant le `produced_application_minimum_contract` pour que la factory puisse exiger au minimum une preuve explicite de :
- localité runtime ;
- absence de génération runtime interdite ;
- gouvernance patch compatible avec la Constitution ;
- dépendances canoniques suffisamment auditables.

**Raison** : c’est le point le plus critique parce qu’il conditionne directement la possibilité de produire une application apparemment valide mais constitutionnellement fautive.

### Thème B — Gouvernance minimale des projections dérivées

**Décision proposée : retained_now**  
Le principe des projections dérivées validées est conservé, mais leur usage comme contexte IA unique doit être conditionné plus explicitement à des garde-fous minimaux. Il faut ajouter ou clarifier :
- décision de stockage ;
- protocole de régénération ;
- définition minimale de validation ;
- traçabilité version/source/scope ;
- politique explicite de non-promotion comme source primaire.

**Raison** : consensus fort et risque élevé de dérive normative silencieuse.

### Thème C — Maturité et honnêteté du `state`

**Décision proposée : retained_now**  
Le `state` doit être réaligné avec la réalité opérationnelle sur les sujets projections dérivées et readiness multi-IA. En particulier, il faut corriger ce qui donne l’impression qu’une capacité est présente alors qu’elle n’est encore que déclarative ou partiellement instrumentée.

**Raison** : éviter un faux sentiment de fermeture.

### Thème D — Multi-IA parallèle

**Décision proposée : retained_now**  
Il ne faut pas exiger une architecture V1 complète, mais il faut fermer un minimum de protocole :
- découpage/scopes bornés ;
- point d’assemblage ;
- convention minimale de résolution de conflits ;
- traçabilité des outputs IA.

**Raison** : l’exigence multi-IA est de premier rang ; sans minimum opérable, elle reste trop narrative.

### Thème E — Release / current / manifest

**Décision proposée : clarification_required** sur le mécanisme exact, mais **retained_now** sur le besoin de clarification explicite.  
Le besoin de clarifier la posture est retenu maintenant. En revanche, il faut éviter de forcer trop tôt un mécanisme unique non arbitré entre :
- extension du manifest officiel courant ;
- manifest séparé spécifique à `platform_factory` ;
- maintien provisoire d’une traçabilité via report de promotion et release materialization.

**Raison** : besoin réel, mais lieu principal = release governance transverse plus que contenu canonique pur.

### Thème F — Findings anciens sur prompts/specs supposés manquants

**Décision proposée : rejected**  
Le repo actuel contient bien les specs détaillées de `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`, ainsi que les prompts partagés centraux `Make22PlatformFactoryPatch.md` et `Make23PlatformFactoryValidation.md`. Les findings du 2026-04-04 sur leur absence ne doivent donc pas être propagés dans l’arbitrage courant.

**Raison** : finding dépassé par l’état réel du repo.

---

## Décisions immédiates

### PFARB-DEC-01
- **Sujet** : Renforcer le contrat minimal d’application produite sur les invariants constitutionnels runtime
- **Sources** : PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PXADV_BB1MZX, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `validator/tooling`
- **Priorité** : `critique`
- **Consensus perçu** : `strong`
- **Justification** : convergence forte sur l’insuffisance probante du contrat minimal vis-à-vis de `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, de la gouvernance patch et de la traçabilité de dépendances canoniques.
- **Impact si non traité** : la factory peut valider une application produite non conforme à des invariants constitutionnels critiques.
- **Pré-condition éventuelle** : aucune clarification bloquante sur le principe.
- **Note de séquencement** : traiter avant toute extension détaillée du schéma final du manifest.

### PFARB-DEC-02
- **Sujet** : Fermer le mécanisme minimal des `validated_derived_execution_projections`
- **Sources** : PFCHAL_20260404_PERP_K7X2, PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PXADV_BB1MZX, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `state`, `validator/tooling`, `manifest/release governance`
- **Priorité** : `critique`
- **Consensus perçu** : `strong`
- **Justification** : tous les rapports convergent sur le fait que le principe est bon mais non encore fermé par des garde-fous opérationnels minimaux.
- **Impact si non traité** : drift normatif silencieux, projections obsolètes, usage IA non gouverné.
- **Pré-condition éventuelle** : clarification légère sur le lieu de stockage exact, mais pas sur le besoin.
- **Note de séquencement** : traiter en parallèle de PFARB-DEC-03.

### PFARB-DEC-03
- **Sujet** : Réaligner le `state` sur la maturité réelle des projections dérivées
- **Sources** : PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PXADV_BB1MZX, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `state`
- **Lieu(x) secondaire(s)** : `architecture`
- **Priorité** : `élevé`
- **Consensus perçu** : `strong`
- **Justification** : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est trop optimiste en `capabilities_present` si le stockage, la régénération et la validation restent absents.
- **Impact si non traité** : faux sentiment de capacité présente ; arbitrages futurs biaisés.
- **Pré-condition éventuelle** : aucune.
- **Note de séquencement** : aligner après PFARB-DEC-02 pour décrire précisément ce qui est encore absent vs partiellement traité.

### PFARB-DEC-04
- **Sujet** : Définir un protocole multi-IA minimal opérable
- **Sources** : PFCHAL_20260404_PERP_K7X2, PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PXADV_BB1MZX, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `state`, `pipeline`
- **Priorité** : `élevé`
- **Consensus perçu** : `strong`
- **Justification** : il existe un consensus sur l’absence de protocole d’assemblage, de résolution de conflit et de granularité minimale utilisable.
- **Impact si non traité** : collisions silencieuses entre outputs IA ; promesse multi-IA non gouvernée.
- **Pré-condition éventuelle** : aucune sur le besoin ; la forme exacte peut rester minimale.
- **Note de séquencement** : traiter avant toute revendication plus forte de readiness multi-IA.

### PFARB-DEC-05
- **Sujet** : Clarifier la posture `current` / `released baseline` / `hors manifest officiel`
- **Sources** : PFCHAL_20260404_PERP_K7X2, PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PXADV_BB1MZX, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `clarification_required`
- **Lieu principal de traitement** : `manifest/release governance`
- **Lieu(x) secondaire(s)** : `state`, `pipeline`
- **Priorité** : `élevé`
- **Consensus perçu** : `strong`
- **Justification** : le problème est réel et stable dans tous les rapports, mais le bon mécanisme de fermeture relève d’une décision transverse de gouvernance plus que d’un simple wording local.
- **Impact si non traité** : ambiguïté de statut, promotion implicite, audit courant incomplet.
- **Pré-condition éventuelle** : arbitrage humain sur le mécanisme exact de raccord au manifest officiel.
- **Note de séquencement** : clarifier avant tout patch qui modifierait la sémantique de release ou promotion.

### PFARB-DEC-06
- **Sujet** : Ne pas retenir comme findings courants l’absence de specs Stage 07/08 ou de prompts partagés centraux
- **Sources** : PFCHAL_20260404_PERP_K7X2, PFCHAL_20260404_PERPLX_7K2R
- **Décision** : `rejected`
- **Lieu principal de traitement** : `pipeline`
- **Lieu(x) secondaire(s)** : none
- **Priorité** : `faible`
- **Consensus perçu** : `conflicting`
- **Justification** : le repo actuel contient bien `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`, `STAGE_08_FACTORY_PROMOTE_CURRENT.md`, `Make22PlatformFactoryPatch.md` et `Make23PlatformFactoryValidation.md`.
- **Impact si non traité** : bruit d’arbitrage et patch inutile.
- **Pré-condition éventuelle** : aucune.
- **Note de séquencement** : n/a.

### PFARB-DEC-07
- **Sujet** : Ne pas imposer la séparation de `Make23` en deux prompts distincts à ce stade
- **Sources** : PFCHAL_20260404_PERPLX_A1J77P
- **Décision** : `rejected`
- **Lieu principal de traitement** : `pipeline`
- **Lieu(x) secondaire(s)** : none
- **Priorité** : `faible`
- **Consensus perçu** : `weak`
- **Justification** : le prompt actuel `Make23PlatformFactoryValidation.md` documente explicitement deux modes (`PRE_APPLY_PATCH_VALIDATION` et `POST_APPLY_CORE_VALIDATION`). Le finding initial n’est plus suffisamment fondé.
- **Impact si non traité** : aucun blocage crédible du patch courant.
- **Pré-condition éventuelle** : aucune.
- **Note de séquencement** : n/a.

### PFARB-DEC-08
- **Sujet** : Reclasser `PF_CAPABILITY_FACTORY_SCOPE_DEFINED`
- **Sources** : PFCHAL_20260404_PERPLX_A1J77P
- **Décision** : `rejected`
- **Lieu principal de traitement** : `state`
- **Lieu(x) secondaire(s)** : none
- **Priorité** : `faible`
- **Consensus perçu** : `weak`
- **Justification** : la portée de la factory est effectivement définie ; les gaps ouverts concernent surtout schémas, tooling et protocoles, pas l’absence de scope. Le reclassement en `partial` sur ce point sur-corrigerait la V0.
- **Impact si non traité** : faible.
- **Pré-condition éventuelle** : aucune.
- **Note de séquencement** : n/a.

### PFARB-DEC-09
- **Sujet** : Formaliser maintenant les schémas finaux du manifest, runtime entrypoint, configuration et packaging
- **Sources** : PFCHAL_20260404_PERP_K7X2, PFCHAL_20260404_PERPLX_7K2R, PFCHAL_20260404_PERPLX_A1J77P, PFCHAL_20260408_GPT54_Q7M2
- **Décision** : `deferred`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `state`
- **Priorité** : `modéré`
- **Consensus perçu** : `medium`
- **Justification** : ces manques sont réels mais restent des incomplétudes V0 acceptables tant qu’on ferme maintenant les exigences probantes minimales et l’honnêteté de maturité.
- **Impact si non traité** : ralentit l’industrialisation, mais ne doit pas bloquer le patch courant si les points critiques sont traités.
- **Pré-condition éventuelle** : aucune.
- **Note de séquencement** : après PFARB-DEC-01 et PFARB-DEC-02.

### PFARB-DEC-10
- **Sujet** : Renforcer maintenant le pipeline sur l’atomicité/rollback de STAGE_05
- **Sources** : PFCHAL_20260404_PXADV_BB1MZX
- **Décision** : `deferred`
- **Lieu principal de traitement** : `pipeline`
- **Lieu(x) secondaire(s)** : `validator/tooling`
- **Priorité** : `modéré`
- **Consensus perçu** : `medium`
- **Justification** : le risque est valable, mais le repo actuel a déjà renforcé STAGE_05 par sandbox, dry-run obligatoire et règle anti-simulation. Le hardening supplémentaire sur rollback/atomicité reste souhaitable, sans devoir polluer le patch canonique courant.
- **Impact si non traité** : pipeline encore partiellement dépendant du script et de la discipline opérateur.
- **Pré-condition éventuelle** : lecture/outillage du script dédié si ce sujet remonte plus tard.
- **Note de séquencement** : pipeline hardening ultérieur.

---

## Clarifications requises avant patch

1. **Release/current/manifest** : faut-il étendre le manifest officiel courant pour intégrer `platform_factory`, ou formaliser un mécanisme transitoire distinct mais stable ?
2. **Projections dérivées** : le lieu de stockage exact doit-il être arbitré dans le canonique maintenant, ou d’abord dans une gouvernance/release rule transverse ?
3. **Preuve constitutionnelle dans le contrat minimal** : faut-il exiger une simple attestation déclarative, ou un bloc de validation/observabilité explicitement structuré dès ce cycle ?

Ces clarifications ne remettent pas en cause les décisions retenues ; elles portent sur la forme exacte du patch, pas sur le besoin d’intervention.

---

## Reports assumés

1. **Schéma final complet du manifest d’application produite** : report assumé.
2. **Typologie runtime exacte** : report assumé.
3. **Schéma détaillé de configuration** : report assumé.
4. **Schéma détaillé de packaging** : report assumé.
5. **Granularité optimale V1 des modules/projections multi-IA** : report assumé.
6. **Industrialisation complète des validators** : report assumé, tout en gardant une exigence minimale sur la définition de validation des projections.

---

## Répartition par lieu de correction

### Architecture
- renforcer les obligations probantes du contrat minimal ;
- clarifier les exigences minimales des projections dérivées ;
- poser un protocole multi-IA minimal ;
- éventuellement renforcer la traçabilité canonique minimale attendue dans les artefacts produits.

### State
- réaligner la maturité déclarée des projections dérivées ;
- expliciter proprement ce qui est présent, partiel, absent ou bloqué ;
- éventuellement durcir le wording sur la posture transitoire release/current/manifest.

### Pipeline
- aucun patch canonique obligatoire immédiat sur l’existence des specs ou prompts partagés ;
- hardening ultérieur possible sur STAGE_05 et sur certains outputs homogènes.

### Validator / Tooling
- définition minimale de validation des projections dérivées ;
- à terme, outillage de validation du contrat minimal renforcé.

### Manifest / Release governance
- clarification du statut des artefacts platform_factory dans `current/` ;
- décision sur le raccord au dispositif officiel de manifest/release.

### Hors périmètre factory
- pipeline d’instanciation domaine complet ;
- logique domaine spécifique ;
- validation métier détaillée des artefacts applicatifs domaine.

---

## Priorités de patch

### Critique
- PFARB-DEC-01
- PFARB-DEC-02

### Élevé
- PFARB-DEC-03
- PFARB-DEC-04
- PFARB-DEC-05

### Modéré
- PFARB-DEC-09
- PFARB-DEC-10

### Faible
- PFARB-DEC-06
- PFARB-DEC-07
- PFARB-DEC-08

---

## Points retenus

- Renforcer maintenant la preuve constitutionnelle minimale du contrat d’application produite.
- Renforcer maintenant la gouvernance minimale des projections dérivées.
- Corriger maintenant l’honnêteté de maturité du `state` sur les projections.
- Poser maintenant un protocole multi-IA minimal.
- Retenir le besoin de clarification sur la posture release/current/manifest.

## Points rejetés

- Propager comme findings courants l’absence supposée des specs Stage 07/08.
- Imposer la séparation de `Make23` en deux prompts distincts.
- Reclasser `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` en capacité seulement partielle.

## Points différés

- Schémas finaux détaillés manifest/runtime/configuration/packaging.
- Hardening pipeline complémentaire sur STAGE_05 si nécessaire.
- Industrialisation complète des validators.

## Points hors périmètre

- Définition complète du futur pipeline d’instanciation domaine.
- Contraintes métier spécifiques d’une application particulière.
- Gouvernance détaillée des artefacts domaine en aval.

## Points sans consensus ou nécessitant discussion finale

1. **Mécanisme exact de raccord au manifest officiel courant** : extension du manifest principal vs mécanisme séparé mais relié.
2. **Niveau exact de formalisation requis dès maintenant pour l’attestation de conformité runtime** : simple bloc déclaratif vs bloc de validation/observabilité plus structuré.
3. **Lieu exact de stockage des projections dérivées** : décision à prendre sans brouiller `docs/cores/current/` ni précipiter une architecture de stockage trop lourde.

---

## Corrections à arbitrer avant patch

1. **Architecture** — ajouter au contrat minimal des exigences explicites de conformité runtime constitutionnelle.
2. **Architecture + state + tooling** — fermer minimalement les projections dérivées (stockage, validation, régénération, traçabilité).
3. **State** — réaligner les capacités projections dérivées avec la maturité réelle.
4. **Architecture + pipeline** — poser un protocole multi-IA minimal d’assemblage et de résolution de conflit.
5. **Release governance + state/pipeline** — clarifier explicitement la posture transitoire release/current/manifest avant de prétendre à une baseline “released” au sens fort.

---

## Séquencement recommandé

1. Arbitrer la forme minimale de PFARB-DEC-01.
2. Arbitrer la forme minimale de PFARB-DEC-02.
3. Aligner immédiatement le `state` (PFARB-DEC-03).
4. Poser le protocole multi-IA minimal (PFARB-DEC-04).
5. Ouvrir la clarification gouvernance release/current/manifest (PFARB-DEC-05), sans bloquer le reste du patch canonique si une formulation transitoire claire est retenue.

---

## Verdict d’arbitrage proposé

La baseline `platform_factory` doit être **consolidée**, pas refondue.  
L’arbitrage doit **retenir les corrections probantes et de gouvernance minimales**, **rejeter les findings devenus obsolètes**, et **différer les schémas finaux détaillés** qui relèvent encore d’une maturation V0→V1.
