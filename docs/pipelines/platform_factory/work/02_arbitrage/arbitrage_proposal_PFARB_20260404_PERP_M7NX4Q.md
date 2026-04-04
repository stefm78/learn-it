# Proposition d'arbitrage — Platform Factory Baseline V0

## arbitrage_run_id

`PFARB_20260404_PERP_M7NX4Q`

---

## Date

2026-04-04

## Agent

PERP (Perplexity AI — Sonnet 4.6)

## Pipeline

`docs/pipelines/platform_factory/pipeline.md` — STAGE_02_FACTORY_ARBITRAGE

## Prompt canonique utilisé

`docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

---

## Challenge reports considérés

| Run ID | Agent | Fichier |
|---|---|---|
| PFCHAL_20260404_PERPLX_A1J77P | PERPLX | `work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md` |
| PFCHAL_20260404_PERP_K7X2 | PERP | `work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md` |
| PFCHAL_20260404_PPLXAI_5LVBSV | PPLXAI | `work/01_challenge/challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md` |
| PFCHAL_20260404_PXADV_BB1MZX | PXADV | `work/01_challenge/challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md` |
| PFCHAL_20260404_PERPLX_7K2R | PERPLX | `work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_7K2R.md` |
| PFCHAL_20260404_GPT54_X7K2Q | GPT54 | `work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md` |

---

## Résumé exécutif

Les six challenge reports convergent sur une lecture commune : la Platform Factory V0.1 constitue une fondation conceptuelle légitime, honnête dans son auto-diagnostic, et viable pour lancer un cycle de correction. Aucun rapport ne la déclare bloquante ou fondamentalement incorrecte.

Trois sujets concentrent un consensus fort entre tous les agents challengers :

1. **Le contrat minimal d'application produite ne projette pas les invariants constitutionnels critiques de runtime dans ses axes de validation.** Une application peut passer la validation factory tout en violant `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`. Ce n'est pas une incomplétude V0 normale — c'est un trou de conformité constitutionnelle.

2. **Les projections dérivées validées sont autorisées comme artefact unique pour une IA alors que leur mécanisme opérationnel (validateur, emplacement, protocole de régénération) est entièrement absent.** Ce principe d'usage dépasse le niveau réel d'outillage.

3. **Les artefacts platform_factory sont dans `docs/cores/current/` mais hors manifest officiel.** Cette ambiguïté de statut release est reconnue mais non résolue.

Deux sujets font consensus fort à un niveau élevé (non critique) :

4. **L'absence de protocole d'assemblage multi-IA** rend la promesse de premier rang non opérationnelle.
5. **La maturité surdéclarée** dans `capabilities_present` pour `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` peut induire une confiance injustifiée.

Un sujet présente un désaccord modéré de gravité entre les agents, traité en section dédiée.

Ce rapport propose une arbitrage opérationnel, structuré par thème, prêt à alimenter un cycle de patch propre.

---

## Synthèse des constats convergents

### CC-01 — Contrat minimal sans attestation constitutionnelle runtime
**Niveau de consensus : FORT (6/6 agents)**

Tous les agents identifient que `minimum_validation_contract.minimum_axes` (structure, minimum_contract_conformance, traceability, packaging) ne couvre pas les invariants constitutionnels de runtime critiques. Les formulations varient (axe manquant, absence de binding, brèche possible) mais la conclusion est identique : une application produite peut être factory-valide et constitutionnellement invalide.

Les invariants concernés, cités de façon convergente :
- `INV_RUNTIME_FULLY_LOCAL`
- `INV_NO_RUNTIME_CONTENT_GENERATION`
- `INV_NO_RUNTIME_FEEDBACK_GENERATION` / `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`
- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
- `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
- `INV_NO_PARTIAL_PATCH_STATE` (cité par 4 agents)

Désaccord mineur de périmètre : PERPLX_A1J77P distingue binding absent vs binding explicite pour `INV_NO_PARTIAL_PATCH_STATE` (binding faible via `package_must_be_classifiable`). PXADV_BB1MZX et PERPLX_7K2R le classifient absent. **L'arbitrage retient : absent de facto dans le contrat minimal — le binding faible de l'architecture n'est pas suffisant pour une validation formelle.**

### CC-02 — Projections dérivées : mécanisme déclaré, outillage absent
**Niveau de consensus : FORT (6/6 agents)**

Le principe `execution_projection_contract` est jugé correct et normatif. Mais l'autorisation d'usage comme artefact unique pour une IA (Rule 4 du pipeline) précède les trois conditions de sécurité (validateur, emplacement fixe, protocole de régénération), toutes absentes ou TBD.

Risques convergents identifiés par tous les agents :
- dérive normative silencieuse par paraphrase ou omission
- projection périmée utilisée sans détection (invalidation post-patch absente)
- promotion implicite d'une projection en source canonique

Désaccord de nuance : PERPLX_A1J77P propose un mécanisme d'interdiction temporaire de l'usage fort mono-contexte. PERP_K7X2 propose simplement de résoudre l'emplacement et le validateur. GPT54_X7K2Q propose de conditionner explicitement l'usage fort à un gate documenté. **L'arbitrage retient la formulation de gate conditionnel explicite (GPT54, confirmé par PERPLX_7K2R CORR-01).**

### CC-03 — Artefacts factory hors manifest officiel
**Niveau de consensus : FORT (6/6 agents)**

Tous reconnaissent `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` comme réel. La situation — artefacts dans `current/` mais hors manifest — crée une ambiguïté d'interprétation pour tout acteur (humain ou IA) lisant le dispositif.

Désaccord de gravité : PERPLX_A1J77P classe ce point en risque structurel de premier plan (Axe 8). PERP_K7X2 le classe gravité basse-moyenne. GPT54 et PXADV_BB1MZX le classent élevé. PPLXAI_5LVBSV le classe critique. **L'arbitrage retient : élevé mais non bloquant immédiatement pour le patch, à condition de décision explicite de régularisation.**

### CC-04 — Protocole d'assemblage multi-IA absent
**Niveau de consensus : FORT (6/6 agents)**

L'absence de `decomposition_protocol`, `ai_output_assembly_protocol` et `conflict_resolution_protocol` est identifiée par tous. Les scénarios adversariaux convergent (collision multi-IA, manifests incompatibles).

Désaccord de classification : PXADV_BB1MZX propose de promouvoir `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker de niveau haut. PERP_K7X2 le classe modéré-élevé. PERPLX_A1J77P le classe modéré. **L'arbitrage retient : modéré-élevé, à traiter dans ce cycle mais non bloquant avant patch si une règle minimale d'assemblage est définie.**

### CC-05 — Maturité surdéclarée : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
**Niveau de consensus : FORT (5/6 agents)**

PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PERPLX_7K2R et PXADV_BB1MZX identifient que classer cette capacité en `present` alors que le mécanisme est entièrement non outillé crée une fausse lecture de maturité. GPT54_X7K2Q soulève la même tension sans nommer explicitement la reclassification. **Consensus fort.**

### CC-06 — Critères de sortie de maturité V0 absents
**Niveau de consensus : MOYEN (4/6 agents)**

PERP_K7X2, PPLXAI_5LVBSV, PERPLX_A1J77P et partiellement PERPLX_7K2R indiquent que l'état ne contient pas de `exit_criteria` ou `next_maturity_target`. GPT54 et PXADV ne l'identifient pas explicitement comme correction. **Consensus modéré — à retenir mais avec priorité basse.**

---

## Propositions d'arbitrage par thème

---

### ARB-01 — Contrat minimal : axes de validation constitutionnelle runtime manquants

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Les invariants constitutionnels critiques de runtime ne sont pas inclus comme axes de validation du contrat minimal d'une application produite |
| **Statut proposé** | **retained** |
| **Gravité** | CRITIQUE |
| **Justification** | Consensus 6/6. Une application factory-valide peut être constitutionnellement invalide sans que cela soit détectable. Ce n'est pas une incomplétude V0 acceptable — c'est un trou de conformité affectant la garantie fondamentale de la factory. |
| **Correction proposée** | Ajouter dans `minimum_axes` un axe nommé `constitutional_runtime_compliance` couvrant au minimum : `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`. Ajouter dans le `manifest.minimum_contents` une section `constitutional_invariant_attestation` listant les IDs d'invariants applicables avec statut d'attestation. |
| **Niveau de correction** | Déclaratif (assertif) pour la V0 : l'application déclare la conformité dans son manifest. Le mode probatoire (validateur automatique) est différé. |
| **Lieu principal de correction** | architecture |
| **Lieu secondaire** | state (mise à jour `produced_application_contract_status` + capacity) |
| **Niveau de consensus** | strong |
| **Dépendance** | Aucune — peut être patché en autonomie |
| **Impact si non traité** | La factory ne peut pas certifier la conformité constitutionnelle de ses produits — invalidation de la raison d'être de la couche factory |

---

### ARB-02 — Contrat minimal : absence de binding sur `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` et `INV_NO_PARTIAL_PATCH_STATE`

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.produced_application_minimum_contract` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Ces deux invariants ne sont pas couverts dans les axes de validation ni dans le manifest requis |
| **Statut proposé** | **retained** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Identifiés par 4/6 agents. Distincts de ARB-01 en ce qu'ils portent sur la gestion des patchs de l'application produite, pas sur son runtime nominal. Leur absence expose à un état partiel d'application non détecté. |
| **Correction proposée** | Intégrer `deterministic_patch_validation` et `atomic_patch_state` dans l'axe `constitutional_runtime_compliance` créé en ARB-01. |
| **Lieu principal de correction** | architecture |
| **Niveau de consensus** | medium |
| **Dépendance** | Dépend de ARB-01 (même lieu de correction) |

---

### ARB-03 — Projections dérivées : gate conditionnel avant usage fort mono-contexte

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.execution_projection_contract` + `generated_projection_rules.emplacement_policy` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | L'usage comme artefact unique pour une IA est autorisé alors que validateur, emplacement et protocole de régénération sont tous absents |
| **Statut proposé** | **retained** |
| **Gravité** | CRITIQUE |
| **Justification** | Consensus 6/6. Le mécanisme est théoriquement puissant et normativement correct, mais l'autorisation d'usage fort précède les gardes-fous de sécurité. C'est une inversion de séquence. |
| **Correction proposée** | Ajouter dans l'architecture un bloc `usage_conditions` dans `execution_projection_contract` précisant que l'usage fort (artefact unique pour IA) est conditionné à : (a) un emplacement stable décidé, (b) un protocole de validation minimal défini, (c) un protocole de régénération déclaré. Tant que ces conditions ne sont pas remplies, l'usage fort est explicitement interdit par la factory, pas simplement non recommandé. |
| **Lieu principal de correction** | architecture |
| **Lieu secondaire** | state (mise à jour `derived_projection_conformity_status` pour refléter la condition explicite) |
| **Niveau de consensus** | strong |
| **Dépendance** | Doit précéder ARB-04 (emplacement) et ARB-05 (validateur) qui lèveront le gate |
| **Impact si non traité** | Risque de dérive normative silencieuse sur tout travail IA utilisant une projection |

---

### ARB-04 — Projections dérivées : décision d'emplacement

| Champ | Valeur |
|---|---|
| **Élément concerné** | `generated_projection_rules.emplacement_policy` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | `emplacement_policy.status: TBD` — aucune localisation stable des projections |
| **Statut proposé** | **retained** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Consensus 6/6. Sans emplacement stable, les projections ne sont pas localisables, versionnables, ni invalidables après patch canonique. C'est une condition préalable à tout usage opérationnel. |
| **Correction proposée** | Décider d'un emplacement dans ce cycle. Proposition recommandée par consensus des agents : `docs/pipelines/platform_factory/projections/` avec sous-dossiers par scope. Mettre à jour `emplacement_policy.status` → décidé, documenter le chemin. Mettre à jour `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` dans le state. |
| **Lieu principal de correction** | architecture |
| **Lieu secondaire** | state |
| **Niveau de consensus** | strong |
| **Dépendance** | Pré-condition pour lever ARB-03 |

---

### ARB-05 — Projections dérivées : définition d'un protocole de validation minimal

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.execution_projection_contract.invariants` + `derived_projection_conformity_status` |
| **Localisation** | `platform_factory_architecture.yaml` + `platform_factory_state.yaml` |
| **Problème** | `validator_definition` est absent ; `deterministic_regeneration_required` est déclaré mais non instrumenté |
| **Statut proposé** | **retained — niveau minimum pour ce cycle** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Consensus 6/6. Un protocole de validation minimal est une condition de sécurité pour autoriser l'usage fort (ARB-03). |
| **Correction proposée** | Définir dans l'architecture un `validation_minimum_protocol` pour les projections dérivées, comprenant au minimum : (a) référence au canonique source (version + SHA), (b) vérification de non-divergence déclarée (par l'IA productrice à la génération), (c) date de génération. Le protocole V0 peut rester déclaratif. Un validateur outillé est reporté (voir ARB-14). |
| **Lieu principal de correction** | architecture |
| **Lieu secondaire** | state |
| **Niveau de consensus** | strong |
| **Dépendance** | Pré-condition pour lever ARB-03 ; indépendant de ARB-04 |

---

### ARB-06 — Gouvernance release : régularisation du statut current/manifest

| Champ | Valeur |
|---|---|
| **Élément concerné** | `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` |
| **Localisation** | `platform_factory_state.yaml` + `platform_factory_architecture.yaml` metadata.notes |
| **Problème** | Les artefacts sont dans `docs/cores/current/` mais hors manifest officiel — zone grise de gouvernance release |
| **Statut proposé** | **retained — décision de régularisation requise dans ce cycle** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Consensus 6/6. La situation est reconnue mais non résolue. Une décision explicite doit être prise pour éviter une ambiguïté de statut lors de l'usage opérationnel. |
| **Correction proposée** | Décision d'arbitrage à choisir (soumettre à humain) : Option A — documenter dans le state un régime transitoire explicite (\"baseline V0 en current, intégration manifest prévue au prochain STAGE_07\") avec date ou condition déclenchante. Option B — créer immédiatement une entrée minimale dans un `releases/` registry ou companion manifest. **L'arbitrage propose l'Option A comme plus simple pour ce cycle.** |
| **Lieu principal de correction** | state (documentation du régime transitoire) |
| **Lieu secondaire** | manifest/release governance |
| **Niveau de consensus** | strong |
| **Dépendance** | Aucune |
| **Note de séquencement** | À traiter avant tout patch YAML pour éviter qu'un cycle de patch soit lancé sur un statut ambigu |

---

### ARB-07 — Multi-IA : protocole d'assemblage minimal

| Champ | Valeur |
|---|---|
| **Élément concerné** | `multi_ia_parallel_readiness` |
| **Localisation** | `platform_factory_architecture.yaml` + `platform_factory_state.yaml` |
| **Problème** | `decomposition_protocol`, `ai_output_assembly_protocol`, `conflict_resolution_protocol` absents |
| **Statut proposé** | **retained — protocole minimal pour ce cycle** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Consensus 6/6. La factory déclare le multi-IA de premier rang mais ne fournit aucun mécanisme pour garantir la cohérence des outputs. Les scénarios adversariaux de collision d'assemblage sont identifiés comme plausibles et immédiats dans plusieurs rapports. |
| **Correction proposée** | Définir dans l'architecture un bloc `multi_ia_assembly_minimum_protocol` comprenant au minimum : (a) règle de non-chevauchement de scope (une IA par scope borné), (b) convention d'identification des outputs (run_id + scope_id), (c) règle de précédence en cas de conflit (latest validated wins, sinon escalade humain). Mettre à jour le state sur `ai_output_assembly_protocol`. |
| **Lieu principal de correction** | architecture |
| **Lieu secondaire** | state + pipeline (pour le reporting homogène) |
| **Niveau de consensus** | strong |
| **Dépendance** | Aucune — peut être patché en autonomie |

---

### ARB-08 — Maturité surdéclarée : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → reclasser en `partial`

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | La règle est déclarée dans l'architecture, mais le mécanisme opérationnel est entièrement absent. Classer en `present` crée une fausse lecture de maturité. |
| **Statut proposé** | **retained** |
| **Gravité** | MODÉRÉ |
| **Justification** | Consensus 5/6. L'erreur de classification peut amener une IA ou un arbitre à surestimer la disponibilité des projections. |
| **Correction proposée** | Déplacer vers `capabilities_partial` avec description : \"Règle d'usage définie dans l'architecture. Mécanisme opérationnel (validateur, emplacement, protocole de régénération) absent — usage fort conditionnel suspendu (voir gate ARB-03).\" |
| **Lieu principal de correction** | state |
| **Niveau de consensus** | strong |
| **Dépendance** | Cohérent avec ARB-03 |

---

### ARB-09 — Maturité surdéclarée : `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` vs open_points

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present.PF_CAPABILITY_FACTORY_SCOPE_DEFINED` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | 6 open_points structurants non résolus dans l'architecture contredisent une capacité de scope déclarée comme entièrement présente |
| **Statut proposé** | **retained — correction de wording** |
| **Gravité** | MODÉRÉ |
| **Justification** | Identifié par PERPLX_A1J77P (Axe 2). Cohérent avec la philosophie de l'état honnête. |
| **Correction proposée** | Conserver en `capabilities_present` mais modifier la description pour préciser que le scope est défini au niveau principes mais comporte 6 open_points non résolus (listés). Ou déplacer vers `capabilities_partial`. |
| **Lieu principal de correction** | state |
| **Niveau de consensus** | medium |

---

### ARB-10 — STAGE_05 pipeline : absence de règle d'atomicité/rollback

| Champ | Valeur |
|---|---|
| **Élément concerné** | `STAGE_05_FACTORY_APPLY` |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md` |
| **Problème** | La description de STAGE_05 ne précise aucun mécanisme garantissant l'atomicité de l'application du patchset ni le comportement en cas d'échec partiel (`INV_NO_PARTIAL_PATCH_STATE`) |
| **Statut proposé** | **retained** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Identifié explicitement par PXADV_BB1MZX [C4] et PERPLX_7K2R de façon implicite. Ratifié par la carte constitutionnelle de PPLXAI_5LVBSV. Un patch partiellement appliqué crée un état expressément interdit par la Constitution. |
| **Correction proposée** | Ajouter dans STAGE_05 une règle d'atomicité minimale : \"Soit tous les fichiers du patchset sont écrits avec succès, soit aucun n'est écrit. En cas d'échec partiel, l'IA doit : (a) ne pas modifier les fichiers déjà écrits, (b) créer un fichier `STAGE_05_ABORTED_<run_id>.md` dans `work/05_apply/` documentant l'état d'avancement et la cause.\" |
| **Lieu principal de correction** | pipeline |
| **Niveau de consensus** | medium |
| **Dépendance** | Aucune |

---

### ARB-11 — Pipeline : lien d'appartenance run entre challenge reports et runs

| Champ | Valeur |
|---|---|
| **Élément concerné** | STAGE_02 règle \"every challenge_report*.md must be considered\" |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md` |
| **Problème** | Les challenge reports ne sont pas liés à un run_id de pipeline. Un rapport d'un run antérieur peut polluer un run ultérieur. |
| **Statut proposé** | **retained — correction légère** |
| **Gravité** | MODÉRÉ |
| **Justification** | Identifié par PPLXAI_5LVBSV [M-02]. |
| **Correction proposée** | Ajouter dans STAGE_01 la convention : le `challenge_run_id` doit être préfixé d'un `pipeline_run_id` partagé. Ajouter dans STAGE_02 la règle : \"Ne considérer que les challenge reports dont le `pipeline_run_id` correspond au run courant, sauf si aucun run_id n'est déclaré (compatibilité V0).\" |
| **Lieu principal de correction** | pipeline |
| **Niveau de consensus** | medium |

---

### ARB-12 — Pipeline : même prompt STAGE_04 et STAGE_06 — ambiguïté

| Champ | Valeur |
|---|---|
| **Élément concerné** | STAGE_04 + STAGE_06 — prompt `Make23PlatformFactoryValidation.md` |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md` |
| **Problème** | Deux stages de validation aux objets distincts partagent le même prompt sans différenciation |
| **Statut proposé** | **deferred — acceptable V0, à clarifier avant usage industriel** |
| **Gravité** | MODÉRÉ |
| **Justification** | Identifié par PPLXAI [M-01] et PPLXAI_5LVBSV [Axe 9]. Acceptable en V0 si la différence d'objet est précisée dans le prompt lui-même ou dans les inputs passés au prompt. Non bloquant pour ce cycle. |
| **Correction différée** | Lors d'un prochain cycle, distinguer les deux prompts ou paramétrer explicitement l'objet de validation à l'appel. |
| **Lieu probable de correction** | pipeline |
| **Niveau de consensus** | medium |

---

### ARB-13 — Critères de sortie de maturité V0 absents dans le state

| Champ | Valeur |
|---|---|
| **Élément concerné** | `maturity_by_layer` + `last_assessment` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Aucun `exit_criteria` ni `next_maturity_target` n'est défini par couche |
| **Statut proposé** | **retained — correction légère** |
| **Gravité** | MODÉRÉ |
| **Justification** | Consensus 4/6. Sans critères de sortie, le state peut rester `foundational_but_incomplete` indéfiniment sans signal de progression. C'est un défaut de gouvernance de maturité, pas un trou normatif. |
| **Correction proposée** | Ajouter dans le state un bloc `maturity_progression_policy` indiquant : (a) comment une couche passe de `boundary_defined_only` à un niveau supérieur, (b) quelle autorité décide, (c) quel artefact est produit lors d'une progression de maturité. V0 acceptable : déclaration d'intention, pas de critères fins par couche. |
| **Lieu principal de correction** | state |
| **Niveau de consensus** | medium |

---

### ARB-14 — Validators dédiés : à reporter avec condition déclenchante explicite

| Champ | Valeur |
|---|---|
| **Élément concerné** | `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Absence totale de validators outillés |
| **Statut proposé** | **deferred — avec condition déclenchante** |
| **Gravité** | MODÉRÉ |
| **Justification** | Tous les agents reconnaissent cette absence comme normale en V0. Acceptable tant qu'aucun pipeline d'instanciation n'est lancé. |
| **Condition de déclenchement** | À créer avant le premier usage opérationnel de projections dérivées (lève ARB-03). Minimum : validator de projection dérivée (conformité normative, vérification de non-divergence). |
| **Lieu probable de correction** | validator/tooling + pipeline |
| **Niveau de consensus** | strong (accord sur le report) |

---

### ARB-15 — STAGE_07 et STAGE_08 : vérification de l'existence des specs

| Champ | Valeur |
|---|---|
| **Élément concerné** | `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` + `STAGE_08_FACTORY_PROMOTE_CURRENT.md` |
| **Localisation** | `docs/pipelines/platform_factory/` |
| **Problème** | Ces stages critiques référencent des specs détaillées dont l'existence n'est pas confirmée |
| **Statut proposé** | **retained — vérification obligatoire avant clôture du cycle** |
| **Gravité** | ÉLEVÉ |
| **Justification** | Identifié par PERPLX_7K2R [CORR-03] et PPLXAI_5LVBSV [Axe 9]. Sans ces specs, le cycle complet ne peut pas être mené à terme formellement. |
| **Correction proposée** | Vérifier l'existence de ces deux fichiers. Si absents, créer des stubs minimaux avant de lancer STAGE_03. |
| **Lieu principal de correction** | pipeline |
| **Niveau de consensus** | medium |

---

### ARB-16 — `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` : wording à clarifier

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Classer une \"intention posée\" comme capacité présente peut être lu comme \"pipeline opérationnel\" |
| **Statut proposé** | **retained — correction de wording** |
| **Gravité** | MODÉRÉ |
| **Justification** | Identifié par PPLXAI_5LVBSV [E-03] et PERPLX_A1J77P [Axe 6]. |
| **Correction proposée** | Modifier la description pour expliciter : \"L'intention de pipeline est posée. Le pipeline est un squelette V0 non entièrement outillé.\" Ou déplacer vers `capabilities_partial`. |
| **Lieu principal de correction** | state |
| **Niveau de consensus** | medium |

---

### ARB-17 — Fingerprints de reproductibilité : contenu minimal non défini

| Champ | Valeur |
|---|---|
| **Élément concerné** | `produced_application_minimum_contract.identity.required_blocks.reproducibility_fingerprints` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Bloc requis sans définition de contenu minimal |
| **Statut proposé** | **retained — niveau minimum** |
| **Gravité** | MODÉRÉ |
| **Justification** | Identifié par PXADV_BB1MZX [C5], PPLXAI_5LVBSV [E-01], PERPLX_7K2R [CORR-06]. |
| **Correction proposée** | Définir dans l'architecture un contenu minimal pour `reproducibility_fingerprints` : SHA des artefacts canoniques sources utilisés à la production (Constitution, Référentiel, LINK, versions), liste des projections dérivées utilisées avec leur identifiant de version. |
| **Lieu principal de correction** | architecture |
| **Niveau de consensus** | medium |

---

### ARB-18 — Sujet non consensuel : `INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN` dans le contrat minimal

| Champ | Valeur |
|---|---|
| **Élément concerné** | `produced_application_minimum_contract` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | PPLXAI_5LVBSV et PERPLX_7K2R signalent l'absence de binding pour cet invariant. Les autres agents ne le citent pas. |
| **Statut proposé** | **clarification requise avant patch** |
| **Gravité** | À déterminer |
| **Justification** | Le sujet n'est pas consensuel. L'invariant est fort constitutionnellement mais son impact direct sur le contrat minimal de la factory n'est pas établi de façon convergente. |
| **Question d'arbitrage** | La factory doit-elle imposer une attestation de gestion du régime détresse dans le contrat minimal d'une application générique, ou ce point relève-t-il du pipeline d'instanciation domaine ? |
| **Niveau de consensus** | conflicting |

---

### ARB-19 — Sujet non consensuel : handoff contract factory → instanciation

| Champ | Valeur |
|---|---|
| **Élément concerné** | Frontière factory / pipeline d'instanciation |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | GPT54_X7K2Q propose un handoff contract explicite. Les autres agents n'identifient pas ce point comme correction de ce cycle. |
| **Statut proposé** | **deferred** |
| **Gravité** | MODÉRÉ |
| **Justification** | Le handoff contract est conceptuellement pertinent mais le pipeline d'instanciation n'existe pas encore. Définir un handoff avant le destinataire est prématuré. À reporter au cycle d'instanciation. |
| **Lieu probable de correction** | architecture (lors du cycle instanciation) |
| **Niveau de consensus** | weak |

---

### ARB-20 — Points hors périmètre factory

| Sujet | Statut | Justification |
|---|---|---|
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` dans le contrat application | **out_of_scope** | Invariant domaine, correctement exclu de la factory par tous les agents |
| Contenu des schemas fins (manifest, configuration, packaging, runtime entrypoint) | **out_of_scope V0** | Correctement reconnu comme `missing` dans l'état. Objet des prochains cycles. |
| Granularité optimale des projections | **out_of_scope V0** | Déféré dans `deferred_challenges` de l'architecture. Acceptable. |
| Taille optimale des projections | **out_of_scope V0** | Idem. |
| Pipeline d'instanciation domaine | **out_of_scope** | Explicitement hors périmètre factory — correctement borné. |

---

## Corrections à arbitrer avant patch — Vue consolidée

| # | ARB | Sujet | Statut | Gravité | Lieu principal | Dépendance |
|---|---|---|---|---|---|---|
| 1 | ARB-01 | Axe validation constitutionnelle runtime dans le contrat minimal | **retained** | CRITIQUE | architecture | Aucune |
| 2 | ARB-02 | Binding `INV_NO_PARTIAL_PATCH_STATE` + déterminisme patch | **retained** | ÉLEVÉ | architecture | ARB-01 |
| 3 | ARB-03 | Gate conditionnel sur usage fort des projections dérivées | **retained** | CRITIQUE | architecture | Levé par ARB-04+ARB-05 |
| 4 | ARB-04 | Décision d'emplacement des projections | **retained** | ÉLEVÉ | architecture + state | Pré-condition ARB-03 |
| 5 | ARB-05 | Protocole de validation minimal des projections | **retained** | ÉLEVÉ | architecture + state | Pré-condition ARB-03 |
| 6 | ARB-06 | Régularisation statut current/manifest | **retained** | ÉLEVÉ | state | Aucune |
| 7 | ARB-07 | Protocole d'assemblage multi-IA minimal | **retained** | ÉLEVÉ | architecture + state | Aucune |
| 8 | ARB-08 | Reclassifier `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → partial | **retained** | MODÉRÉ | state | Cohérent ARB-03 |
| 9 | ARB-09 | Wording `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` | **retained** | MODÉRÉ | state | Aucune |
| 10 | ARB-10 | Règle d'atomicité STAGE_05 | **retained** | ÉLEVÉ | pipeline | Aucune |
| 11 | ARB-11 | Lien pipeline_run_id dans challenge reports | **retained** | MODÉRÉ | pipeline | Aucune |
| 12 | ARB-12 | Même prompt STAGE_04/STAGE_06 | **deferred** | MODÉRÉ | pipeline | — |
| 13 | ARB-13 | Critères de sortie de maturité | **retained** | MODÉRÉ | state | Aucune |
| 14 | ARB-14 | Validators dédiés | **deferred** | MODÉRÉ | validator/tooling | Conditionné par ARB-03 |
| 15 | ARB-15 | Vérification STAGE_07/STAGE_08 specs | **retained** | ÉLEVÉ | pipeline | Avant STAGE_03 |
| 16 | ARB-16 | Wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | **retained** | MODÉRÉ | state | Aucune |
| 17 | ARB-17 | Fingerprints de reproductibilité : contenu minimal | **retained** | MODÉRÉ | architecture | Aucune |
| 18 | ARB-18 | `INV_DISTRESS_REGIME` dans contrat minimal | **clarification requise** | À déterminer | — | Humain |
| 19 | ARB-19 | Handoff contract factory → instanciation | **deferred** | MODÉRÉ | architecture | Cycle instanciation |
| 20 | ARB-20 | Points hors périmètre (cf. liste) | **out_of_scope** | — | — | — |

---

## Répartition par lieu de correction

### Architecture (`platform_factory_architecture.yaml`)
- ARB-01 : Axe `constitutional_runtime_compliance` dans `minimum_axes`
- ARB-02 : Extension de ARB-01 avec invariants patch
- ARB-03 : Bloc `usage_conditions` avec gate conditionnel dans `execution_projection_contract`
- ARB-04 : `emplacement_policy.status` → décidé + chemin
- ARB-05 : Bloc `validation_minimum_protocol` dans `execution_projection_contract`
- ARB-07 : Bloc `multi_ia_assembly_minimum_protocol`
- ARB-17 : Contenu minimal de `reproducibility_fingerprints`

### State (`platform_factory_state.yaml`)
- ARB-04 : `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` → absent → présent
- ARB-05 : `derived_projection_conformity_status` mise à jour
- ARB-06 : Documentation régime transitoire current/manifest + note sur blocker
- ARB-07 : `multi_ia_parallel_readiness_status.ai_output_assembly_protocol` → partial
- ARB-08 : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → capabilities_partial
- ARB-09 : Description `PF_CAPABILITY_FACTORY_SCOPE_DEFINED`
- ARB-13 : Bloc `maturity_progression_policy`
- ARB-16 : Description `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

### Pipeline (`pipeline.md`)
- ARB-10 : Règle d'atomicité STAGE_05
- ARB-11 : Convention pipeline_run_id dans STAGE_01 et STAGE_02
- ARB-15 : Vérification/création stubs STAGE_07 + STAGE_08

### Validator/Tooling
- ARB-14 (différé) : validator projection dérivée (pré-condition levée par ARB-04+ARB-05)

### Manifest/Release Governance
- ARB-06 (secondaire) : Formalisation du régime transitoire

---

## Séquencement recommandé

```
Phase 1 — Pré-conditions (avant STAGE_03) :
  ARB-06  → clarifier statut release/manifest
  ARB-15  → vérifier STAGE_07/STAGE_08 specs

Phase 2 — Patch architecture (priorité critique) :
  ARB-01  → axe constitutional_runtime_compliance
  ARB-02  → extension invariants patch (peut être fusionné avec ARB-01)
  ARB-03  → gate conditionnel projections dérivées
  ARB-04  → emplacement projections
  ARB-05  → protocole validation minimal projections

Phase 3 — Patch architecture (priorité élevée) :
  ARB-07  → protocole assemblage multi-IA
  ARB-17  → fingerprints contenu minimal
  ARB-10  → atomicité STAGE_05

Phase 4 — Patch state :
  ARB-08  → reclassifier PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED
  ARB-09  → wording PF_CAPABILITY_FACTORY_SCOPE_DEFINED
  ARB-13  → maturity_progression_policy
  ARB-16  → wording PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED

Phase 4 bis — Pipeline :
  ARB-11  → pipeline_run_id convention

Phase 5 — Clarification humaine requise avant patch :
  ARB-18  → décision sur INV_DISTRESS_REGIME dans contrat minimal

Reporté hors cycle :
  ARB-12  → distinct STAGE_04/STAGE_06 prompts
  ARB-14  → validators outillés
  ARB-19  → handoff contract instanciation
```

---

## Points sans consensus ou nécessitant discussion finale

### DIS-01 — Gravité de `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`

Désaccord entre agents sur la gravité (basse-moyenne → critique). L'arbitrage propose élevé. À confirmer en consolidation finale.

### DIS-02 — Traitement de `INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN`

Seuls 2/6 agents citent cet invariant. La question de son inclusion dans le contrat minimal factory vs pipeline d'instanciation doit être tranchée par l'humain en consolidation.

### DIS-03 — Niveau de formalisme du protocole de validation des projections dérivées (ARB-05)

Certains agents proposent une approche déclarative (assertion IA à la génération). D'autres proposent un protocole de diff outillé. L'arbitrage propose le niveau déclaratif pour V0.1 et outillé pour V1. À confirmer.

### DIS-04 — Reclassification de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

2 agents proposent `capabilities_partial`, 1 accepte le maintien en `present` avec ajustement de wording. Décision d'arbitrage : wording ajusté en `present`. Si la consolidation préfère `partial`, les deux sont valides.

---

## Résultat terminal

**arbitrage_run_id** : `PFARB_20260404_PERP_M7NX4Q`

**Fichier écrit** : `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_proposal_PFARB_20260404_PERP_M7NX4Q.md`

**Résumé ultra-court** : 6 challenge reports consolidés → 20 arbitrages proposés. 15 retenus pour ce cycle (2 critiques, 7 élevés, 6 modérés), 3 différés, 1 hors périmètre, 1 en clarification humaine. Points critiques : axe validation constitutionnelle runtime dans le contrat minimal (ARB-01/02) et gate conditionnel usage fort des projections dérivées (ARB-03). Corrections prioritaires avant patch : ARB-06 (release status), ARB-15 (STAGE_07/08 vérification), puis ARB-01→ARB-05 en phase architecture. Proposition exploitable pour consolidation finale STAGE_02.

---

_Rapport produit par PERP (Perplexity AI — Sonnet 4.6) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04_
_Ce rapport est une proposition d'arbitrage. Il ne contient aucun patch YAML. Il ne remplace pas la consolidation finale humaine-assistée du STAGE_02._
_Destiné à la consolidation finale STAGE_02_FACTORY_ARBITRAGE._
