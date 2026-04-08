# Rapport d'arbitrage — Platform Factory STAGE_02_FACTORY_ARBITRAGE

## Métadonnées

| Champ | Valeur |
|---|---|
| **title** | Proposition d'arbitrage — Platform Factory Baseline V0 |
| **arbitrage_run_id** | `PFARB_20260404_PERPLX_9KR4` |
| **date** | 2026-04-04 |
| **stage** | STAGE_02_FACTORY_ARBITRAGE |
| **pipeline** | docs/pipelines/platform_factory/pipeline.md |
| **prompt d'arbitrage** | docs/prompts/shared/Make21PlatformFactoryArbitrage.md |
| **posture** | Proposition d'arbitrage indépendante — contribution à la consolidation finale humaine-assistée |

---

## Challenge reports considérés

| challenge_run_id | Agent | Fichier |
|---|---|---|
| PFCHAL_20260404_GPT54_X7K2Q | GPT-5-4 | challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md |
| PFCHAL_20260404_PERPLX_7K2R | Perplexity (PERPLX) | challenge_report_PFCHAL_20260404_PERPLX_7K2R.md |
| PFCHAL_20260404_PERPLX_A1J77P | Perplexity (PERPLX) | challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md |
| PFCHAL_20260404_PERP_K7X2 | Perplexity (PERP) | challenge_report_PFCHAL_20260404_PERP_K7X2.md |
| PFCHAL_20260404_PPLXAI_5LVBSV | Perplexity AI (PPLXAI) | challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md |
| PFCHAL_20260404_PXADV_BB1MZX | Perplexity Advanced (PXADV) | challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md |

---

## Résumé exécutif

Les 6 challenge reports présentent un **niveau de consensus exceptionnellement fort** sur les zones de risque principales. Aucune contradiction de fond n'a été détectée entre les rapports. Les divergences observées sont des différences de formulation ou de granularité, non des désaccords normatifs.

La baseline Platform Factory V0 est **légitime pour passer à STAGE_03_FACTORY_PATCH** après arbitrage, sous réserve de cinq décisions immédiates critiques ou élevées, et de trois points à reporter explicitement avec wording honnête.

**Le diagnostic convergent à 6 agents :**

1. **Binding constitutionnel incomplet** : le contrat minimal d'application produite ne projette pas les invariants constitutionnels de runtime critiques (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE`) dans ses axes de validation ni dans ses signaux d'observabilité. Une application produite peut violer ces invariants sans que la factory le détecte. **Consensus fort à 6/6.**

2. **Projections dérivées déclarées mais non opérationnalisées** : l'emplacement est TBD, le validateur est absent, le protocole de régénération n'existe pas. L'usage autorisé (projection comme unique contexte IA) est déclaré avant que les gardes-fous soient posés. **Consensus fort à 6/6.**

3. **Gouvernance release/manifest incomplètement fermée** : les artefacts `platform_factory_*` sont dans `docs/cores/current/` mais explicitement hors manifest officiel. Le pipeline ne contient pas de hook garantissant la mise à jour du manifest lors de STAGE_08. **Consensus fort à 5/6** (GPT54 plus centré sur les implications que sur le mécanisme de correction).

4. **Maturité partiellement surdéclarée** : principalement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` classée en `capabilities_present` alors que le mécanisme est entièrement non outillé. **Consensus fort à 5/6** (PERP_K7X2 moins explicite sur ce point).

5. **Protocole d'assemblage multi-IA absent** : la factory pose l'exigence multi-IA de premier rang mais ne définit ni la granularité modulaire, ni le protocole d'assemblage, ni la résolution de conflits. **Consensus fort à 5/6** (GPT54 aborde le sujet sous l'angle de la tension gouvernance plutôt que comme CORR explicite).

---

## Synthèse des constats convergents

### Zone 1 — Conformité constitutionnelle des applications produites (Critique, 6/6)

Tous les rapports identifient que `minimum_validation_contract.minimum_axes` (structure, minimum_contract_conformance, traceability, packaging) ne couvre pas les invariants constitutionnels de runtime. Le pattern est systémique : la factory déclare les bonnes dépendances dans `source_of_authority.required_bindings` mais ne les projette pas dans les axes de validation ni dans les signaux d'observabilité du contrat application. Une application produite peut satisfaire le contrat factory tout en violant `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` et `INV_NO_PARTIAL_PATCH_STATE`.

Les scénarios adversariaux produits par PXADV_BB1MZX (scénarios A et B) illustrent concrètement comment cette absence de binding peut conduire à la promotion d'une application constitutionnellement non conforme.

**Décision d'arbitrage : ARB-01 — Retenu maintenant, correction dans architecture, priorité critique.**

### Zone 2 — Projections dérivées non opérationnalisées (Critique, 6/6)

Convergence forte sur la nature du problème : inversion de séquence entre droit d'usage déclaré et absence des gardes-fous. Les rapports divergent légèrement sur la correction proposée :
- PERPLX_7K2R, PERP_K7X2, PPLXAI_5LVBSV : ajouter un emplacement et un validateur dans l'architecture + state.
- GPT54_X7K2Q : également bloquer l'usage opérationnel des projections jusqu'à instrumentation.
- PERPLX_A1J77P, PXADV_BB1MZX : poser une condition explicite d'activation de l'usage autorisé.

**Arbitrage sur la divergence** : les deux formulations sont compatibles. Il convient de (a) décider l'emplacement de stockage, (b) poser le protocole minimal de validation pré-usage, (c) conditionner l'usage opérationnel à la disponibilité du validateur. La décision de bloquer formellement ou de conditionner est un point de clarification humaine.

**Décision d'arbitrage : ARB-02 — Retenu maintenant (emplacement + condition d'usage), clarification requise avant patch sur le niveau de blocage formel.**

### Zone 3 — Gouvernance release/manifest (Élevée, 5/6)

Convergence sur le problème : les artefacts sont dans `current/` mais hors manifest officiel. Le pipeline (STAGE_08) ne contient pas de hook de mise à jour du manifest. Divergence mineure : PERP_K7X2 et PXADV_BB1MZX posent le scénario de promotion silencieuse comme risque de gouvernance critique ; GPT54_X7K2Q traite le point comme un trou de traçabilité sans qualification de criticité urgente.

**Arbitrage sur la divergence** : le risque de promotion silencieuse (scénario D de PXADV_BB1MZX) est réel et documenté. Ce point doit être retenu maintenant dans le state avec wording corrigé, et un report documentaire explicite doit être ajouté si la correction du manifest schema ne peut pas être immédiate.

**Décision d'arbitrage : ARB-03 — Partiellement retenu maintenant (correction wording state, report documentaire explicite), clarification requise sur le timing de correction du manifest schema.**

### Zone 4 — Maturité surdéclarée (Modérée, 5/6)

`PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est classée en `capabilities_present` alors que le mécanisme est entièrement non outillé (emplacement TBD, validateur absent, protocole de régénération absent). Convergence à 5/6. Rapports PERPLX_7K2R et PPLXAI_5LVBSV notent également la surdéclaration sur `PF_CAPABILITY_MULTI_IA_AS_REQUIREMENT` (exigence déclarée ≠ capacité opérationnelle).

**Décision d'arbitrage : ARB-04 — Retenu maintenant, correction dans state uniquement, priorité modérée.**

### Zone 5 — Protocole assemblage multi-IA (Modérée, 5/6)

Convergence sur l'absence du protocole. PERP_K7X2 demande un bloc `multi_ia_decomposition_minimum_protocol` dans l'architecture. GPT54_X7K2Q traite le sujet comme une tension gouvernance. Les autres rapports citent les `known_gaps` du state (granularité modulaire, résolution de conflits) comme acceptables en V0 si le wording est honnête sur l'absence.

**Arbitrage** : il n'est pas raisonnable d'exiger un protocole d'assemblage complet en V0. En revanche, l'absence doit être traduite en `capabilities_absent` explicite avec wording clair que l'usage multi-IA reste non garanti jusqu'à l'instrumentation de ce protocole.

**Décision d'arbitrage : ARB-05 — Reporté (protocole complet), retenu maintenant uniquement la correction du wording state, priorité modérée.**

---

## Propositions d'arbitrage par thème

---

### ARB-01 — Binding constitutionnel : ajout d'axes de validation runtime dans le contrat minimal d'application produite

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-01 |
| **Sujet** | Absence d'axes de validation constitutionnels runtime dans `produced_application_minimum_contract` |
| **Source(s)** | GPT54_X7K2Q (Axe 1), PERPLX_7K2R (CORR-02), PERPLX_A1J77P (CORR-01/02), PERP_K7X2 (C1 partiel), PPLXAI_5LVBSV (C-01), PXADV_BB1MZX (scénarios A, B) |
| **Décision** | **retained_now** |
| **Lieu principal de traitement** | architecture (`platform_factory_architecture.yaml`) |
| **Lieu(x) secondaire(s)** | validator/tooling (définition d'un axe de validation dédié à terme) |
| **Priorité** | **critique** |
| **Justification** | Convergence 6/6. Pattern systémique : les invariants constitutionnels de sécurité critique ne sont pas projetés dans les axes de validation ni les signaux d'observabilité. Une application produite peut être déclarée conforme en violant `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE`. Ce n'est pas une exigence prématurée V0 — c'est le contrat minimal que toute factory doit poser pour que ses sorties soient auditables constitutionnellement. |
| **Invariants constitutionnels concernés** | `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE` |
| **Correction à arbitrer** | (1) Ajouter dans `minimum_validation_contract.minimum_axes` un axe `runtime_constitutional_constraints` listant les invariants à vérifier par ID. (2) Ajouter dans `minimum_observability_contract.minimum_signals` au moins un signal `runtime_locality_attestation`. (3) Ajouter dans `manifest.minimum_contents` une obligation de référencer explicitement les invariants constitutionnels applicables. |
| **Note** | L'arbitrage humain doit trancher si ces axes sont "déclaratifs" (le manifest atteste) ou "probatoires" (un validateur doit vérifier). Cette clarification est pré-condition du patch précis. Voir ARB-06. |
| **Impact si non traité** | La factory peut certifier des applications constitutionnellement non conformes. Risque de promotion silencieuse de violations constitutionnelles critiques. |
| **Pré-condition éventuelle** | Clarification du niveau de formalisme attendu (déclaratif vs probatoire) — voir ARB-06. Le patch peut commencer sur la partie déclarative sans attendre la réponse sur la partie probatoire. |
| **Niveau de consensus** | **strong (6/6)** |

---

### ARB-02 — Projections dérivées : emplacement, condition d'usage, validateur minimal

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-02 |
| **Sujet** | Projections dérivées déclarées mais non opérationnalisées — emplacement TBD, validateur absent, usage autorisé sans gardes-fous |
| **Source(s)** | GPT54_X7K2Q (Axe 2, 3e risque dominant), PERPLX_7K2R (CORR-01, inversion de séquence), PERPLX_A1J77P (CORR-04), PERP_K7X2 (C1 + C2), PPLXAI_5LVBSV (C-02), PXADV_BB1MZX (zone 2, scénario A) |
| **Décision** | **retained_now (emplacement + condition d'activation) + clarification_required (niveau de blocage formel)** |
| **Lieu principal de traitement** | architecture (`platform_factory_architecture.yaml`) — section `generated_projection_rules` et `contracts.execution_projection_contract` |
| **Lieu(x) secondaire(s)** | state (`platform_factory_state.yaml`) — `derived_projection_conformity_status` + `capabilities_partial/absent` ; validator/tooling |
| **Priorité** | **critique** |
| **Justification** | Convergence 6/6 sur le problème. L'inversion de séquence (droit d'usage déclaré avant gardes-fous) est le risque le plus grave pour la dérive normative silencieuse. Le mécanisme des projections est central pour le travail multi-IA. Son absence d'instrumentation compromet la multi-IA readiness réelle. Ce n'est pas un simple point de complétude V0 — c'est un trou de gouvernance qui peut invalider l'ensemble des outputs IA. |
| **Correction à arbitrer** | (1) Décider l'emplacement de stockage des projections validées (ex. `docs/pipelines/platform_factory/projections/` ou `docs/cores/derived_projections/`). (2) Conditionner explicitement dans l'architecture l'usage opérationnel des projections comme unique contexte IA à la disponibilité d'un validateur et d'un emplacement fixe. (3) Décider si l'état actuel (pas de validateur) implique un statut de blocage formel ou une note de précaution. (4) Dans le state, mettre à jour `derived_projection_conformity_status` avec la décision d'emplacement et le statut de validateur. |
| **Impact si non traité** | Risque de dérive normative silencieuse sur toute application produite via projection. Aucun auditeur ne peut vérifier la conformité d'une projection utilisée. |
| **Pré-condition éventuelle** | Décision humaine sur l'emplacement de stockage (arbitrage architectural). |
| **Note de séquencement** | ARB-02 doit être traité avant tout autre patch utilisant des projections dérivées comme inputs. |
| **Niveau de consensus** | **strong (6/6)** |

---

### ARB-03 — Gouvernance release : artefacts platform_factory dans current mais hors manifest officiel

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-03 |
| **Sujet** | Ambiguïté de statut : artefacts dans `docs/cores/current/` mais explicitement hors manifest officiel courant. Pipeline STAGE_08 sans hook manifest. |
| **Source(s)** | GPT54_X7K2Q (3e risque dominant), PERPLX_7K2R (CORR-05), PERPLX_A1J77P (CORR-05), PERP_K7X2 (C partiel), PPLXAI_5LVBSV (C-03), PXADV_BB1MZX (zone 4, scénario D) |
| **Décision** | **retained_now (correction wording state) + deferred (mise à jour du manifest schema) + pipeline (ajout hook STAGE_08)** |
| **Lieu principal de traitement** | state (`platform_factory_state.yaml`) — wording sur le statut release actuel |
| **Lieu(x) secondaire(s)** | pipeline (`pipeline.md`) — STAGE_08 ; manifest/release governance |
| **Priorité** | **élevée** |
| **Justification** | Convergence 5/6. Scénario D (PXADV_BB1MZX) illustre qu'un STAGE_08 correctement exécuté peut promouvoir dans current sans jamais corriger le manifest, rendant les artefacts invisibles à un outil de validation basé sur le manifest. Ce n'est pas un point de complétude V0 acceptable en silence — c'est un trou de traçabilité de release documenté qui doit être explicitement assumé avec wording honnête et une condition de résolution. |
| **Correction à arbitrer** | (1) Dans le state : corriger le wording sur le statut release pour être explicite sur le gap manifest (blocker ou note assumée). (2) Dans le pipeline STAGE_08 : ajouter une étape ou une condition de mise à jour du manifest officiel avant promotion finale. (3) Reporter la mise à jour du manifest schema réel jusqu'à décision humaine sur l'architecture du manifest officiel. |
| **Impact si non traité** | Risque de promotion silencieuse d'artefacts non officiellement gouvernés. Impossibilité d'auditer la baseline via le manifest officiel. |
| **Pré-condition éventuelle** | Connaissance de la structure du manifest officiel actuel et de la décision sur son évolution. |
| **Niveau de consensus** | **strong (5/6)** |

---

### ARB-04 — Maturité surdéclarée dans platform_factory_state.yaml

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-04 |
| **Sujet** | `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` classée en `capabilities_present` alors que le mécanisme est non outillé. `PF_CAPABILITY_MULTI_IA_AS_REQUIREMENT` lue potentiellement comme capacité opérationnelle. |
| **Source(s)** | PERPLX_7K2R (Axe 2), PERPLX_A1J77P (CORR-06), PERP_K7X2 (Axe 2), PPLXAI_5LVBSV (Axe 2), PXADV_BB1MZX (Axe 2) |
| **Décision** | **retained_now** |
| **Lieu principal de traitement** | state (`platform_factory_state.yaml`) |
| **Lieu(x) secondaire(s)** | Aucun — correction purement constatative |
| **Priorité** | **modérée** |
| **Justification** | Convergence 5/6. Le risque de surdéclaration est réel : une IA lisant le state seul peut conclure que les projections dérivées sont opérationnellement disponibles alors qu'elles ne le sont pas. Ce glissement peut induire des dérives silencieuses dans le travail multi-IA. La correction est mineure (wording dans le state) mais son impact de gouvernance est réel. |
| **Correction à arbitrer** | (1) Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` de `capabilities_present` vers `capabilities_partial` avec une note précisant "règle définie, non outillée, usage opérationnel conditionnel". (2) Vérifier si `PF_CAPABILITY_MULTI_IA_AS_REQUIREMENT` doit être accompagnée d'une note explicite précisant "exigence déclarée, pas de protocole d'assemblage opérationnel". |
| **Impact si non traité** | Dérive normative silencieuse possible si une IA traite le state comme guide de disponibilité opérationnelle. |
| **Pré-condition éventuelle** | Aucune — correction directement réalisable. |
| **Niveau de consensus** | **strong (5/6)** |

---

### ARB-05 — Protocole d'assemblage multi-IA : report assumé avec wording honnête

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-05 |
| **Sujet** | Absence de protocole d'assemblage multi-IA (`decomposition_protocol`, `ai_output_assembly_protocol`, résolution de conflits) |
| **Source(s)** | PERPLX_7K2R (Axe 4), PERPLX_A1J77P (scénario C), PERP_K7X2 (C3), PPLXAI_5LVBSV (Axe 3), PXADV_BB1MZX (zone 3) |
| **Décision** | **deferred (protocole complet) + retained_now (correction wording state sur capacités absentes)** |
| **Lieu principal de traitement** | state (wording `known_gaps` + `capabilities_absent`) |
| **Lieu(x) secondaire(s)** | architecture (note explicite dans `multi_ia_parallel_readiness`) ; pipeline (note de précaution sur STAGE_03) |
| **Priorité** | **modérée** |
| **Justification** | Un protocole d'assemblage multi-IA complet est une exigence de maturité post-V0. Le reporter est légitime pour une V0. Mais l'absence doit être traduite en `capabilities_absent` explicite — pas en `known_gaps` passif. L'assemblage humain reste nécessaire pour tout work multi-IA jusqu'à instrumentation. |
| **Correction à arbitrer** | (1) Dans state : ajouter `PF_CAPABILITY_MULTI_IA_ASSEMBLY_PROTOCOL` en `capabilities_absent` avec note "assemblage humain requis jusqu'à instrumentation". (2) Dans architecture : ajouter dans `multi_ia_parallel_readiness` une note conditionnelle explicite "usage multi-IA actuellement conditionné à un assemblage humain". (3) Reporter la spécification du protocole complet à une V0.2 ou V1. |
| **Impact si non traité** | Collisions multi-IA non détectées lors des stages de patch (STAGE_03). Assemblage ad hoc sans cadre. |
| **Pré-condition éventuelle** | Aucune pour le wording state. Décision de roadmap pour le protocole complet. |
| **Niveau de consensus** | **strong (5/6)** |

---

### ARB-06 — Clarification préalable au patch : niveau de formalisme des axes de validation constitutionnels

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-06 |
| **Sujet** | Pour ARB-01 : les axes de validation constitutionnels à ajouter sont-ils "déclaratifs" (manifest asserte la conformité) ou "probatoires" (un validateur doit vérifier) ? |
| **Source(s)** | PPLXAI_5LVBSV (C-01, note d'arbitrage humain), PERPLX_7K2R (CORR-02), PXADV_BB1MZX (zone 1) |
| **Décision** | **clarification_required** |
| **Lieu principal de traitement** | architecture |
| **Priorité** | **élevée** (bloque la précision du patch ARB-01) |
| **Justification** | La formulation exacte de l'axe `runtime_constitutional_constraints` dans `minimum_validation_contract.minimum_axes` dépend de si l'on exige une attestation déclarative (acceptable V0) ou une preuve validateur (requiert tooling). La décision détermine si le patch est immédiatement implémentable ou requiert un chantier validator additionnel. |
| **Question à trancher** | L'humain arbitre : "Pour V0, accepte-t-on que les axes constitutionnels soient uniquement déclaratifs dans le manifest, avec la promesse que des validateurs seront ajoutés en V0.2 ?" |
| **Niveau de consensus** | **medium (3/6 explicite)** |

---

### ARB-07 — Définition schéma fin des contrats manifest, configuration, packaging, runtime entrypoint

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-07 |
| **Sujet** | Les contrats manifest, configuration, packaging et runtime entrypoint sont définis en intention mais pas en schéma fin. `bootstrap_contract` non défini. |
| **Source(s)** | PERP_K7X2 (famille 1 du résumé), PPLXAI_5LVBSV (Axe 4), PXADV_BB1MZX (Axe 4 manques) |
| **Décision** | **deferred — acceptable V0 explicitement assumée** |
| **Lieu principal de traitement** | architecture (à terme) + state (note assumée) |
| **Priorité** | **faible** (pour V0) |
| **Justification** | Convergence 4/6 comme point V0 acceptable. La V0 est explicitement posée comme baseline d'intention. Les schémas fins sont des livables V0.2 normaux. En revanche, le report doit être explicitement documenté dans le state (open_points) avec une condition de résolution. |
| **Correction à arbitrer** | Aucune correction architecture immédiate. Dans le state : vérifier que `PF_GAP_EXACT_YAML_SCHEMA_NOT_FINALIZED` et les gaps associés ont des descriptions honnêtes de leur statut actuel. |
| **Niveau de consensus** | **strong (4/6 explicite comme V0 acceptable)** |

---

### ARB-08 — Prompt Make23 partagé STAGE_04 et STAGE_06 — ambiguïté pipeline

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-08 |
| **Sujet** | Le prompt `Make23PlatformFactoryValidation.md` est référencé pour STAGE_04 (validation patchset) et STAGE_06 (validation core). Deux stages à objectifs distincts utilisant le même prompt. |
| **Source(s)** | PERPLX_A1J77P (CORR-07), PXADV_BB1MZX (implicite Axe 9) |
| **Décision** | **deferred — acceptable V0 avec note dans le pipeline** |
| **Lieu principal de traitement** | pipeline (`pipeline.md`) |
| **Priorité** | **faible** |
| **Justification** | Deux rapports sur six (PERPLX_A1J77P et PXADV_BB1MZX) signalent ce point. Les autres ne le traitent pas. La convergence est faible. Pour V0, un prompt partagé est acceptable si les deux stages définissent clairement leurs inputs et outputs distincts dans le pipeline. La correction (deux prompts séparés) est reportable en V0.2. |
| **Correction à arbitrer** | Ajouter une note dans `pipeline.md` distinguant explicitement les inputs et outputs de STAGE_04 vs STAGE_06, même si le prompt référencé est identique. |
| **Niveau de consensus** | **weak (2/6)** |

---

### ARB-09 — Absence de format minimal des challenge reports (STAGE_01 → STAGE_02)

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-09 |
| **Sujet** | Le pipeline ne définit pas de sections minimales requises pour les challenge reports. STAGE_02 doit les agréger sans savoir dans quel format les lire. |
| **Source(s)** | PERPLX_A1J77P (P10), PPLXAI_5LVBSV (implicite) |
| **Décision** | **deferred** |
| **Lieu principal de traitement** | pipeline (`pipeline.md`) |
| **Priorité** | **faible** |
| **Justification** | Deux rapports sur six soulèvent le point. L'expérience de ce stage lui-même (6 challenge reports avec des structures variées mais lisibles) montre que le gap est réel mais gérable pour V0. Une convention minimale serait utile mais n'est pas un bloqueur de patch V0. |
| **Niveau de consensus** | **weak (2/6)** |

---

## Points retenus maintenant

| ID | Sujet | Lieu | Priorité |
|---|---|---|---|
| ARB-01 | Ajout axes de validation constitutionnels runtime dans contrat application | architecture | critique |
| ARB-02 (partiel) | Décision emplacement projections dérivées + condition d'activation usage | architecture + state | critique |
| ARB-03 (partiel) | Correction wording state sur statut release/manifest | state | élevée |
| ARB-04 | Correction maturité surdéclarée `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` | state | modérée |
| ARB-05 (partiel) | Correction wording state sur protocole multi-IA absent | state | modérée |

---

## Points rejetés

Aucun finding majeur des 6 challenge reports n'est rejeté. Tous les findings importants sont soit retenus, soit reportés de manière assumée, soit classés comme clarification requise.

**Point rejeté mineur** : la proposition de bloquer entièrement toute future use des projections dérivées jusqu'à la V0.2 (formulée de façon radicale par GPT54_X7K2Q) est rejetée en tant que telle. La correction ciblée (conditionner l'usage à la disponibilité d'un validateur et d'un emplacement, pas interdire la règle elle-même) est plus proportionnée.

---

## Points différés

| ID | Sujet | Justification du report | Condition de reprise |
|---|---|---|---|
| ARB-05 (protocole complet) | Protocole assemblage multi-IA complet | Exigence post-V0 ; assemblage humain reste possible | V0.2 ou V1 — décision de roadmap |
| ARB-07 | Schémas fins manifest, configuration, packaging, bootstrap_contract | V0 assumée ; point de complétude normal | Avant industrialisation |
| ARB-08 | Prompt Make23 séparé pour STAGE_04 vs STAGE_06 | Acceptable V0 avec note pipeline | V0.2 pipeline refactoring |
| ARB-09 | Convention format challenge reports | V0 gérable ; faible consensus challenge | V0.2 pipeline |

---

## Points hors périmètre factory

| Sujet | Raison |
|---|---|
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Invariant de domaine — correctement hors scope factory (6/6 convergence) |
| Gouvernance des applications spécifiques (logique métier, domaine) | Factory gouverne le contrat générique, pas le contenu domaine |
| Pipeline d'instanciation aval (`PF_CAPABILITY_APPLICATION_INSTANTIATION_PIPELINE`) | Périmètre aval explicitement hors factory — classé `capabilities_absent`, acceptable |
| Schéma du manifest officiel actuel | Artefact transverse hors périmètre factory — bloqueur externe documenté (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`) |

---

## Points sans consensus ou nécessitant discussion finale

| ID | Sujet | Nature du désaccord | Recommandation |
|---|---|---|---|
| ARB-06 | Niveau de formalisme des axes de validation constitutionnels (déclaratif vs probatoire) | 3/6 explicites ; les autres convergent sur l'ajout sans préciser le niveau | Décision humaine requise avant patch précis ARB-01 |
| ARB-02 (niveau de blocage) | Bloquer formellement les projections ou conditionner avec note de précaution | GPT54 plus strict, autres plus nuancés | Décision humaine sur le niveau de blocage formel |
| ARB-03 (timing manifest) | Timing et mécanisme de correction du manifest officiel | Dépend de l'architecture du manifest officiel non connue dans ce périmètre | Point de discussion consolidation finale |

---

## Corrections à arbitrer avant patch

Classées par séquencement recommandé :

### PRE-PATCH-1 (critique, bloquer avant tout patch) — ARB-06

Clarifier avec l'humain : les axes de validation constitutionnels dans le contrat application sont-ils déclaratifs (manifest atteste) ou probatoires (validateur vérifie) pour V0 ?

### PRE-PATCH-2 (critique) — ARB-01

Ajouter dans `platform_factory_architecture.yaml` :
- Dans `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` : un axe `runtime_constitutional_constraints` listant les invariants applicables (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE`).
- Dans `contracts.produced_application_minimum_contract.minimum_observability_contract.minimum_signals` : un signal `runtime_locality_attestation`.
- Dans `contracts.produced_application_minimum_contract.manifest.minimum_contents` : une obligation de référencer les invariants constitutionnels applicables par ID.

**Lieu : architecture**

### PRE-PATCH-3 (critique) — ARB-02

Décider l'emplacement de stockage des projections dérivées et conditionner l'usage :
- Mettre à jour `generated_projection_rules.emplacement_policy` avec l'emplacement décidé.
- Ajouter dans `contracts.execution_projection_contract` une condition d'activation explicite de l'usage opérationnel.
- Mettre à jour `platform_factory_state.yaml` section `derived_projection_conformity_status`.

**Lieu : architecture + state**

### PRE-PATCH-4 (élevée) — ARB-03 + ARB-04 + ARB-05

Corrections constatatives dans `platform_factory_state.yaml` :
- Corriger wording sur le statut release/manifest (ARB-03).
- Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` vers `capabilities_partial` (ARB-04).
- Ajouter `PF_CAPABILITY_MULTI_IA_ASSEMBLY_PROTOCOL` en `capabilities_absent` (ARB-05).

**Lieu : state uniquement**

---

## Répartition par lieu de correction

| Lieu de correction | Arbitrages |
|---|---|
| `platform_factory_architecture.yaml` | ARB-01, ARB-02 (emplacement + condition d'usage) |
| `platform_factory_state.yaml` | ARB-02 (derived_projection_conformity_status), ARB-03 (wording release), ARB-04 (capability reclassification), ARB-05 (capabilities_absent) |
| `pipeline.md` | ARB-03 (hook STAGE_08 — reporté), ARB-08 (note STAGE_04/06 — reporté), ARB-09 (reporté) |
| validator/tooling | ARB-02 (à terme, validateur projections), ARB-01 (à terme, validateur probatoire) |
| Hors périmètre / report documentaire | ARB-07, `INV_KNOWLEDGE_GRAPH`, pipeline d'instanciation |

---

## Séquencement recommandé

1. **Clarification humaine ARB-06** — déclaratif vs probatoire — avant rédaction du patch ARB-01 précis.
2. **Décision humaine ARB-02** — emplacement de stockage des projections — avant tout patch architecture.
3. **Patch architecture** — ARB-01 (axes validation) + ARB-02 (emplacement + condition d'usage).
4. **Patch state** — ARB-02 (statut) + ARB-03 (wording release) + ARB-04 (capability reclassification) + ARB-05 (capabilities_absent). Ces corrections sont indépendantes et peuvent être batchées.
5. **Reports documentaires** — ARB-07, ARB-08, ARB-09 — pris en compte dans la roadmap V0.2.

---

## Priorités de patch

| Priorité | Arbitrages | Note |
|---|---|---|
| **critique** | ARB-01, ARB-02 | Conditionnent la conformité constitutionnelle et la gouvernance des projections |
| **élevée** | ARB-03, ARB-06 | Gouvernance release et clarification pré-patch |
| **modérée** | ARB-04, ARB-05 | Corrections constatatives wording state |
| **faible** | ARB-07, ARB-08, ARB-09 | Reports assumés V0 |
