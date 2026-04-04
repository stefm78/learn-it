# Rapport d'arbitrage — Platform Factory STAGE_02

| Champ | Valeur |
|---|---|
| **title** | Arbitrage de la baseline Platform Factory V0 — STAGE_02_FACTORY_ARBITRAGE |
| **arbitrage_run_id** | PFARB_20260404_PERPLX_K9T3 |
| **date** | 2026-04-04 |
| **pipeline** | docs/pipelines/platform_factory/pipeline.md — STAGE_02_FACTORY_ARBITRAGE |
| **agent** | PERPLX (Perplexity AI — Sonnet 4.6) |
| **challenge_reports_traités** | PFCHAL_20260404_PERPLX_A1J77P · PFCHAL_20260404_PERP_K7X2 · PFCHAL_20260404_PPLXAI_5LVBSV · PFCHAL_20260404_PXADV_BB1MZX |
| **destinataire** | STAGE_03_FACTORY_PATCH_SYNTHESIS |

---

## Résumé d'arbitrage

L'ensemble des quatre challenge reports convergent sur les mêmes familles de risques. Aucune contradiction majeure n'existe entre eux — les divergences portent sur le niveau de gravité de certains sujets et sur la granularité d'analyse, non sur l'existence des problèmes.

**Sept décisions majeures sont retenues pour patch immédiat.** Elles couvrent quatre zones critiques : (1) l'absence d'attestation constitutionnelle runtime dans le contrat minimal d'application, (2) l'absence d'opérationnalisation des projections dérivées, (3) la maturité surdéclarée dans l'état, et (4) l'ambiguïté de gouvernance release sur les artefacts V0 en `current/`. S'y ajoutent trois corrections de niveau élevé : protocole d'assemblage multi-IA minimal, atomicité STAGE_05, et correction du wording du blocker multi-IA dans le state.

**Trois sujets sont reportés de façon assumée** avec un wording plus honnête dans le state. **Aucun finding n'est rejeté.** Deux sujets nécessitent une clarification préalable avant patch.

---

## Findings consolidés

### Famille A — Contrat minimal d'application produite : binding constitutionnel runtime absent

**Sources convergentes :** A1J77P (points 1, 2, 3 de son résumé), K7X2 (C1), 5LVBSV (C-01), BB1MZX (C1)

Tous les rapports confirment que les axes de validation minimaux du contrat d'application produite (`minimum_validation_axes`) ne couvrent pas les invariants constitutionnels critiques : `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE`.

**Désaccord de formulation :** A1J77P insiste sur l'absence de binding comme rupture constitutionnelle, 5LVBSV et BB1MZX posent un axe dédié `runtime_constitutional_compliance` ou `constitutional_runtime_constraints` à ajouter, K7X2 est le plus opérationnel en listant 4 obligations manquantes avec leur impact précis. Pas de contradiction de fond — BB1MZX est retenu comme formulation principale pour la décision.

**Finding fusionné FA-01 :** Le contrat minimal d'application produite ne requiert pas d'attestation positive de conformité aux invariants constitutionnels runtime critiques. Une application peut être validée conforme factory tout en violant ces invariants.

---

### Famille B — Projections dérivées : mécanisme non opérationnalisé

**Sources convergentes :** A1J77P (points 3, 5), K7X2 (C1, C2), 5LVBSV (C-02), BB1MZX (C2)

Consensus absolu : l'emplacement est TBD, le validateur est absent, le protocole de régénération est absent, l'invalidation post-patch canonique n'existe pas.

**Désaccord de gravité :** 5LVBSV et BB1MZX classent ce sujet en critique. K7X2 en moyenne-haute. A1J77P en critique. L'arbitrage retient le niveau critique pour l'absence d'emplacement et de protocole de validation, élevé pour l'invalidation post-patch.

**Finding fusionné FB-01 :** Les projections dérivées sont déclarées comme mécanisme central d'alimentation des IA mais leur emplacement, leur validation et leur cycle de vie sont entièrement non opérationnalisés. L'usage opérationnel de projections avant résolution expose à une dérive normative silencieuse.

---

### Famille C — Maturité surdéclarée dans le state

**Sources convergentes :** A1J77P (point 4), K7X2 (C3, E3), 5LVBSV (E-03), BB1MZX (C6)

Tous les rapports signalent que `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` et `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` (ou `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`) sont classées en `capabilities_present` alors que leur outillage est entièrement absent.

**Désaccord de périmètre :** 5LVBSV inclut `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` dans les surdéclarations. BB1MZX identifie `PF_CAPABILITY_MULTI_IA_AS_REQUIREMENT` comme glissement entre exigence déclarée et capacité opérationnelle. L'arbitrage tranche : seules les capacités effectivement non outillées sont reclassées ; une exigence correctement déclarée comme exigence reste acceptable en `present` si son wording est précis.

**Finding fusionné FC-01 :** Deux capacités sont mal classées : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` doit passer de `present` à `partial` ; `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` doit avoir son wording précisé pour ne pas masquer les 6 points ouverts.

---

### Famille D — Gouvernance release / manifest / statut current des artefacts V0

**Sources convergentes :** A1J77P (point 6), K7X2 (C6), 5LVBSV (C-03), BB1MZX (C7)

Consensus : les artefacts sont dans `docs/cores/current/` mais hors manifest officiel. Aucun artefact de release ne matérialise leur statut.

**Désaccord de gravité :** 5LVBSV et A1J77P classent en critique. K7X2 en basse-moyenne. BB1MZX en modéré. L'arbitrage retient un niveau élevé (non critique) : le risque d'ambiguïté est réel mais non immédiatement bloquant pour le patch.

**Finding fusionné FD-01 :** Les artefacts factory V0 sont dans `current/` sans intégration manifest ni release record formel. Une clarification de statut dans le state est nécessaire. La régularisation complète est reportée à STAGE_07/STAGE_08.

---

### Famille E — Multi-IA : protocole d'assemblage absent, classé gap mais pas blocker

**Sources convergentes :** A1J77P (point 5), K7X2 (C3), 5LVBSV (E-02), BB1MZX (C3)

Tous les rapports confirment que `decomposition_protocol`, `ai_output_assembly_protocol` et `conflict_resolution_protocol` sont absents. BB1MZX note que le gap n'est pas promu en blocker malgré son statut d'exigence de premier rang — point crucial pour l'arbitrage.

**Finding fusionné FE-01 :** L'absence de protocole d'assemblage multi-IA est correctement nommée en `known_gaps` mais n'est pas promue en blocker dans le state, ce qui sous-évalue le risque pour une exigence déclarée de premier rang.

---

### Famille F — Atomicité STAGE_05 (apply) absente

**Sources :** BB1MZX uniquement (C4), avec référence implicite à `INV_NO_PARTIAL_PATCH_STATE` dans A1J77P et 5LVBSV.

**Finding fusionné FF-01 :** STAGE_05 du pipeline ne précise pas de règle d'atomicité ni de comportement en cas d'échec partiel. `INV_NO_PARTIAL_PATCH_STATE` constitutionnel exige une garantie de cohérence. Ce sujet est strictement pipeline.

---

### Famille G — Sujets V0 acceptables reconnus dans tous les rapports

Consensus sur les éléments suivants, acceptables comme état V0 : schémas fins non finalisés, pipeline d'instanciation hors périmètre, validateurs non implémentés, granularité modulaire déférée, `deferred_challenges` correctement nommés. Ces points ne font pas l'objet de décisions de patch.

---

### Famille H — Sujets spécifiques non redondants (rapports individuels)

**H1 — Binding absent sur `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` dans le contrat minimal** (A1J77P point 2). Confirmé par 5LVBSV et BB1MZX. Fusionné dans FA-01.

**H2 — Même prompt STAGE_04 et STAGE_06** (5LVBSV M-01). Confirmé par 5LVBSV uniquement. Arbitrage : sujet de pipeline modéré, retenu pour clarification.

**H3 — Absence de lien d'appartenance run dans les challenge reports** (5LVBSV M-02). Confirmé par BB1MZX (axe 9). Arbitrage : sujet de gouvernance pipeline modéré, reporté.

**H4 — Fingerprints de reproductibilité non définis** (BB1MZX C5, K7X2 partiellement). Arbitrage : élevé, retenu pour patch.

**H5 — Critères de sortie de maturité par couche absents** (K7X2 C4). Arbitrage : modéré, retenu comme correction de state.

---

## Décisions immédiates

---

### DEC-01 — Ajout d'un axe de validation constitutionnel runtime dans le contrat minimal

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-01 |
| **Finding source** | FA-01 |
| **Sources** | A1J77P · K7X2 · 5LVBSV · BB1MZX |
| **Décision** | `retained_now` |
| **Lieu principal** | architecture (`platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes`) |
| **Lieu secondaire** | architecture → `produced_application_minimum_contract.minimum_observability_contract` |
| **Priorité** | critique |
| **Justification** | Cinq invariants constitutionnels forts ne sont pas propagés dans le contrat minimal. Une application peut être déclarée conforme factory tout en les violant. Ce trou est normatif, non V0 acceptable. La correction est déclarative — un axe `runtime_constitutional_compliance` dans `minimum_axes` exige une attestation dans le manifest et l'observabilité minimale. |
| **Nature de la correction** | Correction de contenu canonique (architecture) — ajout d'un axe de validation, liste des invariants à couvrir, nature de l'attestation (déclarative dans le manifest, niveau V0). |
| **Impact si non traité** | Une application produite peut violer les invariants constitutionnels fondamentaux sans détection factory. |
| **Note de séquencement** | Corriger avant les sujets FB-01 et FD-01 car cet axe est la précondition d'audit des projections et de la release. |

---

### DEC-02 — Décision d'emplacement des projections dérivées et ajout d'un protocole minimal de validation

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-02 |
| **Finding source** | FB-01 |
| **Sources** | A1J77P · K7X2 · 5LVBSV · BB1MZX |
| **Décision** | `retained_now` (emplacement + validation minimale) / `deferred` (invalidation automatique post-patch) |
| **Lieu principal** | architecture (`generated_projection_rules.emplacement_policy` + `contracts.execution_projection_contract`) |
| **Lieu secondaire** | state (`derived_projection_conformity_status`) |
| **Priorité** | critique |
| **Justification** | L'emplacement TBD bloque tout usage multi-IA des projections. Un chemin stable est nécessaire maintenant. La validation automatique complète est V0-acceptable en différé, mais un protocole minimal de validation avant usage (ex. : vérification de version, déclaration de scope, date de génération) est patchable dès maintenant. L'invalidation automatique post-patch canonique est reportée — elle nécessite de l'outillage. |
| **Nature de la correction** | Architecture : décider `emplacement_policy` (chemin proposé : `docs/pipelines/platform_factory/projections/`) + ajouter bloc `pre_usage_minimum_check` dans `execution_projection_contract`. State : mettre à jour `derived_projection_conformity_status` pour refléter l'emplacement décidé. |
| **Impact si non traité** | Les IAs ne peuvent pas localiser de façon déterministe les projections. Le drift normatif silencieux reste probable dès le premier usage. |
| **Précondition** | Aucune pour l'emplacement. La validation nécessite que DEC-01 soit finalisé (les invariants à couvrir conditionnent ce que vérifie un `pre_usage_check`). |

---

### DEC-03 — Reclassement de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` de `present` à `partial`

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-03 |
| **Finding source** | FC-01 |
| **Sources** | A1J77P · K7X2 · 5LVBSV · BB1MZX |
| **Décision** | `retained_now` |
| **Lieu principal** | state (`platform_factory_state.yaml` → `capabilities_present` → déplacer vers `capabilities_partial`) |
| **Lieu secondaire** | aucun |
| **Priorité** | élevé |
| **Justification** | La règle est définie dans l'architecture (c'est une capacité déclarative présente), mais le mécanisme opérationnel est entièrement absent (pas de validator, pas d'emplacement, pas de protocole). Classer `present` crée un risque d'hallucination de capacité par les IAs. Le wording `partial` avec description explicite `rule_defined_mechanism_absent` est plus honnête et sans risque de déclassement normatif. |
| **Nature de la correction** | Correction d'état constatif (state uniquement). |
| **Impact si non traité** | Une IA lisant l'état peut considérer les projections comme utilisables sans validation. Confiance excessive dans une capacité non opérationnelle. |

---

### DEC-04 — Précision du wording de `PF_CAPABILITY_FACTORY_SCOPE_DEFINED`

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-04 |
| **Finding source** | FC-01 (partie 2) |
| **Sources** | A1J77P · K7X2 |
| **Décision** | `retained_now` |
| **Lieu principal** | state (`platform_factory_state.yaml` → `capabilities_present.PF_CAPABILITY_FACTORY_SCOPE_DEFINED`) |
| **Lieu secondaire** | aucun |
| **Priorité** | modéré |
| **Justification** | Le scope est correctement défini en tant que périmètre délimité — conserver en `present` est acceptable. Mais le wording actuel ne mentionne pas les 6 `open_points_for_challenge` non résolus. Ajouter une note `open_points_count: 6` dans la description de cette capacité pour éviter une lecture surévaluée. |
| **Nature de la correction** | Correction de wording dans le state. |

---

### DEC-05 — Promotion de `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` au niveau blocker dans le state

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-05 |
| **Finding source** | FE-01 |
| **Sources** | BB1MZX · 5LVBSV · K7X2 |
| **Décision** | `retained_now` |
| **Lieu principal** | state (`platform_factory_state.yaml` → `blockers`) |
| **Lieu secondaire** | state → `multi_ia_parallel_readiness_status` |
| **Priorité** | élevé |
| **Justification** | L'exigence multi-IA est déclarée de premier rang. Laisser l'absence de protocole d'assemblage uniquement en `known_gaps` sans blocker correspondant est une incohérence de gouvernance. Un blocker `PF_BLOCKER_MULTI_IA_ASSEMBLY_PROTOCOL_UNDEFINED` de sévérité `high` doit être ajouté. Pas de patch sur l'architecture — la décision de fond (protocole d'assemblage) est reportée (V0 acceptable), mais l'honnêteté du state est corrigeable maintenant. |
| **Nature de la correction** | Correction d'état constatif (state uniquement). |
| **Impact si non traité** | Le système sous-évalue un risque de premier rang ; une IA lisant l'état peut croire que le travail multi-IA est plus sûr qu'il ne l'est. |

---

### DEC-06 — Ajout d'une règle d'atomicité minimale dans STAGE_05 du pipeline

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-06 |
| **Finding source** | FF-01 |
| **Sources** | BB1MZX · 5LVBSV (implicite) |
| **Décision** | `retained_now` |
| **Lieu principal** | pipeline (`docs/pipelines/platform_factory/pipeline.md` → STAGE_05_FACTORY_APPLY) |
| **Lieu secondaire** | aucun |
| **Priorité** | élevé |
| **Justification** | `INV_NO_PARTIAL_PATCH_STATE` constitutionnel exige une atomicité ou un rollback. STAGE_05 ne précise aucune règle en ce sens. La correction est strictement pipeline — ajouter une règle minimale : \"l'application du patchset est atomique ; en cas d'échec partiel, le répertoire `work/05_apply/patched/` est invalidé et signalé par un fichier `APPLY_FAILED.flag` avant toute transmission à STAGE_06\". Correction légère, sans impact sur l'architecture. |
| **Nature de la correction** | Correction de pipeline. |
| **Impact si non traité** | Un patch partiellement appliqué crée un état interdit constitutionnellement. |

---

### DEC-07 — Définition du contenu minimal des fingerprints de reproductibilité

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-07 |
| **Finding source** | H4 |
| **Sources** | BB1MZX · K7X2 (partiel) |
| **Décision** | `retained_now` |
| **Lieu principal** | architecture (`produced_application_minimum_contract.identity.required_blocks.reproducibility_fingerprints`) |
| **Lieu secondaire** | aucun |
| **Priorité** | élevé |
| **Justification** | `reproducibility_fingerprints` est requis mais sans définition minimale de contenu. Une IA ne peut pas construire un fingerprint conforme. La définition minimale proposée pour V0 : SHA des artefacts canoniques sources utilisés, version des projections dérivées consommées, hash du manifest produit. Cette définition est patchable sans outillage supplémentaire. |
| **Nature de la correction** | Correction de contenu canonique (architecture). |

---

### DEC-08 — Ajout de critères de sortie de maturité minimaux par couche dans le state

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-08 |
| **Finding source** | H5 |
| **Sources** | K7X2 |
| **Décision** | `retained_now` |
| **Lieu principal** | state (`platform_factory_state.yaml` → `maturity_by_layer`) |
| **Lieu secondaire** | aucun |
| **Priorité** | modéré |
| **Justification** | Sans critères de sortie, la factory reste `foundational_but_incomplete` indéfiniment. Ajouter pour chaque couche un champ `next_maturity_target` minimal permettant de piloter les cycles de patch ultérieurs. Acceptable en version déclarative courte pour V0. |
| **Nature de la correction** | Correction d'état constatif (state). |

---

### DEC-09 — Clarification du statut release des artefacts V0 dans le state

| Champ | Valeur |
|---|---|
| **Decision ID** | DEC-09 |
| **Finding source** | FD-01 |
| **Sources** | A1J77P · K7X2 · 5LVBSV · BB1MZX |
| **Décision** | `retained_now` (clarification dans le state) / `deferred` (régularisation manifest et release record formel) |
| **Lieu principal** | state (`metadata.notes`) |
| **Lieu secondaire** | pipeline (à traiter en STAGE_07/STAGE_08) |
| **Priorité** | élevé |
| **Justification** | La situation de la baseline V0 (dans `current/` hors manifest) est une zone grise reconnue. La correction maintenant consiste à ajouter dans le state une déclaration explicite : \"les artefacts V0 sont dans `docs/cores/current/` en tant que baseline released initiale, en attente de régularisation formelle par un premier cycle complet STAGE_07/STAGE_08. Leur autorité est celle d'une baseline released mais non encore manifest-tracked.\". La régularisation formelle (intégration manifest, release tag) est reportée à la fin du premier cycle pipeline complet. |
| **Nature de la correction** | Correction d'état constatif (state) + note de séquencement pipeline. |

---

## Clarifications requises avant patch

---

### CLR-01 — Nature de l'attestation de conformité constitutionnelle runtime

| Champ | Valeur |
|---|---|
| **Clarification ID** | CLR-01 |
| **Lié à** | DEC-01 |
| **Question** | L'axe `runtime_constitutional_compliance` dans `minimum_axes` doit-il être : (a) une assertion déclarative dans le manifest produit par une IA (\"l'application déclare ne faire aucun appel réseau\"), ou (b) une obligation probatoire (le pipeline de validation doit vérifier mécaniquement l'absence) ? |
| **Impact sur le patch** | En mode (a), la correction est légère et immédiate. En mode (b), elle nécessite un validator dédié non encore défini — elle ne peut pas être patchée dans ce cycle. |
| **Décision par défaut si non clarifiée** | Retenir le mode (a) — déclarative — pour ce cycle V0. Le mode (b) est une évolution de maturité V1. Cette clarification peut être levée par Stéphane avant le début du patch synthesis. |

---

### CLR-02 — Ambiguïté STAGE_04 vs STAGE_06 : même prompt, objectifs différents

| Champ | Valeur |
|---|---|
| **Clarification ID** | CLR-02 |
| **Lié à** | H2 (5LVBSV M-01) |
| **Question** | L'usage du même prompt `Make23PlatformFactoryValidation.md` en STAGE_04 et STAGE_06 est-il intentionnel (le prompt est conçu pour être utilisé dans les deux contextes avec un paramétrage d'appel différent) ou est-ce un oubli de différenciation ? |
| **Impact sur le patch** | Si intentionnel, pas de patch — mais ajouter une note explicative dans `pipeline.md`. Si non intentionnel, deux prompts distincts sont nécessaires — hors périmètre de ce cycle de patch. |
| **Décision par défaut si non clarifiée** | Traiter comme intentionnel pour ce cycle. Ajouter une note pipeline distinguant l'objet de chaque validation. |

---

## Reports assumés

---

### REP-01 — Invalidation automatique des projections post-patch canonique

**Finding source :** FB-01 (partie 2)  
**Décision :** `deferred`  
**Justification :** Nécessite un outillage de suivi de version canonique non disponible en V0. Le risk est réel mais le mécanisme d'invalidation automatique ne peut pas être patché dans ce cycle sans outillage.  
**Wording dans le state :** Ajouter dans `derived_projection_conformity_status.missing` une entrée `invalidation_protocol_post_canonical_patch` marquée `deferred_requires_tooling`.

---

### REP-02 — Protocole d'assemblage multi-IA et granularité modulaire

**Finding source :** FE-01 (partie 2 — fond du protocole)  
**Décision :** `deferred`  
**Justification :** Correctement classé dans `deferred_challenges` de l'architecture. Le patch de ce cycle se limite à la promotion au niveau blocker dans le state (DEC-05). Le fond du protocole est une évolution structurelle post-V0.  
**Wording dans le state :** Le blocker `PF_BLOCKER_MULTI_IA_ASSEMBLY_PROTOCOL_UNDEFINED` (DEC-05) constitue la trace formelle de ce déféré.

---

### REP-03 — Lien d'appartenance run entre challenge reports et runs de pipeline

**Finding source :** H3 (5LVBSV M-02)  
**Décision :** `deferred`  
**Justification :** Sujet de gouvernance pipeline modéré. Résoudre ce point nécessite d'ajouter un `run_id` aux rapports de challenge et de modifier le pipeline pour filtrer par run. C'est une évolution de pipeline post-V0. Acceptable car le premier run est traçable manuellement.  
**Condition de levée :** à adresser avant le deuxième cycle pipeline complet.

---

## Répartition par lieu de correction

### À corriger dans `platform_factory_architecture.yaml`
- **DEC-01** — Ajout axe `runtime_constitutional_compliance` dans `minimum_validation_axes` + liste des invariants à couvrir + attestation dans `minimum_observability_contract`
- **DEC-02** — Décision `emplacement_policy` + ajout bloc `pre_usage_minimum_check` dans `execution_projection_contract`
- **DEC-07** — Définition minimale du contenu de `reproducibility_fingerprints`

### À corriger dans `platform_factory_state.yaml`
- **DEC-03** — Reclassement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → `capabilities_partial`
- **DEC-04** — Wording `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` + note `open_points_count: 6`
- **DEC-05** — Ajout blocker `PF_BLOCKER_MULTI_IA_ASSEMBLY_PROTOCOL_UNDEFINED` (sévérité: high)
- **DEC-08** — Ajout `next_maturity_target` par couche dans `maturity_by_layer`
- **DEC-09** — Clarification `metadata.notes` sur le statut release V0
- **REP-01** — Ajout de `invalidation_protocol_post_canonical_patch` dans `derived_projection_conformity_status.missing`

### À corriger dans `pipeline.md`
- **DEC-06** — Règle d'atomicité minimale dans STAGE_05 + signal `APPLY_FAILED.flag`
- **CLR-02** (si levée par défaut) — Note explicative distinguant STAGE_04 et STAGE_06 dans le pipeline

### Hors périmètre de ce cycle
- Intégration au manifest officiel et release record formel → STAGE_07/STAGE_08 (DEC-09 partie 2)
- Invalidation automatique post-patch → outillage futur (REP-01)
- Protocole d'assemblage multi-IA complet → évolution post-V0 (REP-02)
- Différenciation des prompts STAGE_04/STAGE_06 si non intentionnelle → hors cycle (CLR-02)
- Lien d'appartenance run des rapports → évolution pipeline (REP-03)

---

## Séquencement recommandé

```
Étape 1 : DEC-01 (axe runtime constitutionnel) — précondition des autres corrections d'architecture
Étape 2 : DEC-02 (emplacement projections + pre_usage_check) — dépend de la liste d'invariants établie en DEC-01
Étape 3 : DEC-07 (fingerprints) — indépendant, peut être parallélisé avec Étape 2
Étape 4 : DEC-03, DEC-04, DEC-05, DEC-08, DEC-09 + REP-01 wording → state en une seule passe
Étape 5 : DEC-06 + CLR-02 (si levée) → pipeline
```

---

## Priorités de patch

| Priorité | Decision ID | Sujet | Lieu |
|---|---|---|---|
| **CRITIQUE** | DEC-01 | Axe de validation constitutionnel runtime dans le contrat minimal | architecture |
| **CRITIQUE** | DEC-02 | Emplacement projections + pre_usage_check | architecture + state |
| **ÉLEVÉ** | DEC-03 | Reclassement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `partial` | state |
| **ÉLEVÉ** | DEC-05 | Promotion multi-IA assembly protocol en blocker high | state |
| **ÉLEVÉ** | DEC-06 | Atomicité STAGE_05 | pipeline |
| **ÉLEVÉ** | DEC-07 | Contenu minimal fingerprints | architecture |
| **ÉLEVÉ** | DEC-09 | Clarification statut release V0 | state |
| **MODÉRÉ** | DEC-04 | Wording `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` | state |
| **MODÉRÉ** | DEC-08 | Critères de sortie de maturité | state |
| **MODÉRÉ** | CLR-01 | Nature attestation constitutionnelle (à lever avant DEC-01) | — |
| **MODÉRÉ** | CLR-02 | Ambiguïté STAGE_04 vs STAGE_06 | pipeline |

---

## Résultat terminal

**arbitrage_run_id :** `PFARB_20260404_PERPLX_K9T3`  
**Fichier écrit :** `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_report_PFARB_20260404_PERPLX_K9T3.md`  
**Challenge reports traités :** 4 (A1J77P · K7X2 · 5LVBSV · BB1MZX)  
**Décisions retenues maintenant :** 9 (DEC-01 à DEC-09)  
**Clarifications requises avant patch :** 2 (CLR-01 · CLR-02)  
**Reports assumés :** 3 (REP-01 · REP-02 · REP-03)  
**Rejets :** 0  
**Destinataire :** STAGE_03_FACTORY_PATCH_SYNTHESIS

_Rapport généré par PERPLX (Perplexity AI) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04_  
_Ce rapport ne contient aucun patch YAML. Toute modification d'artefact relève de STAGE_03._
