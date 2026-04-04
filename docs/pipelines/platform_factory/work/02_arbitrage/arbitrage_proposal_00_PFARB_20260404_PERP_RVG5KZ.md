# Proposition d'arbitrage — STAGE_02_FACTORY_ARBITRAGE

## arbitrage_run_id

`PFARB_20260404_PERP_RVG5KZ`

## Date

2026-04-04

## Agent

PERP (Perplexity AI — Sonnet 4.6)

---

## Challenge reports considérés

| challenge_run_id | Agent | Fichier |
|---|---|---|
| `PFCHAL_20260404_PERP_K7X2` | PERP (Perplexity AI — Sonnet 4.6) | `work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md` |
| `PFCHAL_20260404_PPLXAI_5LVBSV` | PPLXAI (Perplexity AI) | `work/01_challenge/challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md` |

---

## Résumé exécutif

Les deux challenge reports convergent sur une baseline V0 constituonnellement saine dans ses déclarations de principes, mais présentant des lacunes opérationnelles réelles. Le consensus entre rapports est fort sur les sujets critiques : absence de mécanisme de validation des projections dérivées, absence de schéma de manifest finalisé, opérationnalisation inexistante du multi-IA, et ambiguïté de gouvernance release des artefacts V0 déjà en `current/`.

Le rapport PPLXAI_5LVBSV apporte un angle complémentaire essentiel absent dans PERP_K7X2 : **l'absence de propagation des invariants constitutionnels de runtime dans les axes de validation du contrat minimal** (C-01). C'est un risque constitutionnel de premier rang qui doit être retenu immédiatement.

La baseline est exploitable pour un cycle de patch borné. Le périmètre du patch doit rester limité : corriger les trous normatifs dangereux, mettre à jour honnêtement le constat de maturité, décider des points TBD bloquants, reporter les schémas fins et l'outillage complet.

**Propositions d'arbitrage résultantes :** 6 retenus maintenant (dont 2 critiques), 2 reportés avec wording honnête, 3 classés hors périmètre factory V0.

---

## Synthèse des constats convergents

### Consensus fort (présent dans les deux rapports)

| Sujet | Source K7X2 | Source 5LVBSV | Niveau consensus |
|---|---|---|---|
| Projections dérivées sans emplacement, sans validateur, sans invalidation post-patch | C2, C1 | C-02 | **fort** |
| Absence de schéma de manifest finalisé | C1 (manifest_schema) | C-01, E-01 (partiellement) | **fort** |
| Multi-IA : absence de protocole d'assemblage | C3 | E-02 | **fort** |
| Sur-déclaration de maturité dans `capabilities_present` | C4 (absence critères sortie) | E-03 | **fort** |
| Gouvernance release : artefacts V0 hors manifest officiel | C6 | C-03 | **fort** |
| Prompts partagés non vérifiés / pipeline partiellement instrumenté | C5 | Implicite (M-01) | **moyen** |

### Finding exclusif à PPLXAI_5LVBSV — Non couvert par PERP_K7X2

| Sujet | Source | Niveau consensus |
|---|---|---|
| Invariants constitutionnels runtime non propagés dans les axes de validation du contrat minimal (C-01) | C-01 | **non contradictoire** — PERP_K7X2 ne l'a pas relevé mais aucun des deux rapports ne le réfute |
| Ambiguïté STAGE_04 vs STAGE_06 même prompt | M-01 | faible |
| Absence de lien d'appartenance run dans les challenge reports | M-02 | faible |
| Obligations contrat minimal non définies : fingerprints, bootstrap_contract | E-01 | moyen |

### Points de désaccord ou de formulation divergente

**Aucun désaccord de fond identifié.** Les deux rapports traitent la même baseline sans contradiction sur les constats. Les divergences sont de granularité : PPLXAI_5LVBSV est plus détaillé sur l'axe constitutionnel runtime et les scénarios adversariaux ; PERP_K7X2 est plus structuré sur la gouvernance de maturité.

Le rapport PPLXAI_5LVBSV classifie C-03 (artefacts en current hors manifest) comme **critique**, contre **basse-moyenne** dans PERP_K7X2 (C6). L'arbitrage tranche en faveur du niveau ÉLEVÉ : le risque est réel mais pas immédiatement bloquant pour un cycle de patch interne, car la promesse multi-IA en externe n'est pas encore activée. La clarification reste requise avant tout usage d'un pipeline de promotion formel.

---

## Propositions d'arbitrage par thème

---

### ARB-01 — Invariants constitutionnels runtime absents des axes de validation du contrat minimal

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-01 |
| **Sujet** | `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` ne couvre pas les invariants constitutionnels de runtime |
| **Source(s)** | PPLXAI_5LVBSV C-01 ; PERP_K7X2 (non nommé explicitement mais impliqué dans Axe 4) |
| **Statut proposé** | `retained_now` |
| **Lieu principal** | architecture (`platform_factory_architecture.yaml`) |
| **Lieu(x) secondaire(s)** | state (mise à jour constatative de `minimum_contract_axes_status`) |
| **Priorité** | CRITIQUE |
| **Justification** | Un contrat minimal qui ne couvre pas `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE` peut produire des applications déclarées conformes tout en violant la Constitution. C'est un trou normatif actif, pas une incomplétude V0 acceptable. |
| **Impact si non traité** | Une IA utilisant le contrat comme guide de validation ne sait pas qu'elle doit vérifier les invariants runtime constitutionnels. Scénario B (PPLXAI_5LVBSV) démontré. |
| **Pré-condition** | Aucune — le patch peut être fait directement dans l'architecture en ajoutant un axe `runtime_constitutional_constraints` dans `minimum_axes`. |
| **Note de séquencement** | Ce patch est indépendant des autres ; peut être traité en premier. |
| **Niveau de consensus** | **medium** — fort sur la nécessité, mais PERP_K7X2 n'a pas nommé ce trou. La consolidation le confirme. |
| **Arbitrage de modalité** | L'axe de validation doit être **déclaratif dans cette V0** (le manifest doit asserter la conformité) ; la vérification probatoire (validator outillé) est reportée V0→V1. Ce point doit être explicitement noté dans l'architecture comme « déclaratif_only_in_v0 ». |

---

### ARB-02 — Projections dérivées : décider emplacement + poser protocole minimal de validation

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-02 |
| **Sujet** | `generated_projection_rules.emplacement_policy.status: TBD` + absence de validateur + absence d'invalidation post-patch |
| **Source(s)** | PERP_K7X2 C2, C1 ; PPLXAI_5LVBSV C-02 |
| **Statut proposé** | `retained_now` pour (a) décision d'emplacement et (b) protocole minimal de validation ; `deferred` pour (c) outillage complet et validateur automatisé |
| **Lieu principal** | architecture |
| **Lieu(x) secondaire(s)** | state (mise à jour `derived_projection_conformity_status` + `emplacement_policy`) ; validator/tooling (deferred) |
| **Priorité** | CRITIQUE |
| **Justification** | Le TBD sur l'emplacement est un bloqueur direct : des IAs ne peuvent pas stocker ni retrouver des projections. L'absence de tout protocole de validation rend la règle « strictement conforme » non vérifiable. Il ne s'agit pas d'une exigence de schéma fin, mais d'une décision d'architecture minimale. |
| **Impact si non traité** | Scénario SA-01 (PERP_K7X2) et Scénario A (PPLXAI_5LVBSV) : dérive normative silencieuse non détectable, projections périmées utilisées sans le savoir. |
| **Pré-condition** | Décision humaine sur l'emplacement (proposition : `docs/pipelines/platform_factory/projections/`). Le patch peut être fait ensuite. |
| **Note de séquencement** | (a) emplacement → (b) protocole minimal dans l'architecture → (c) mise à jour state. L'outillage complet (validator automatisé) est ARB-09 (deferred). |
| **Niveau de consensus** | **fort** |

---

### ARB-03 — Multi-IA : poser un protocole minimal d'assemblage

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-03 |
| **Sujet** | Absence de `decomposition_protocol`, `ai_output_assembly_protocol` et `conflict_resolution_protocol` dans `multi_ia_parallel_readiness` |
| **Source(s)** | PERP_K7X2 C3, Axe 7 ; PPLXAI_5LVBSV E-02, Axe 7 |
| **Statut proposé** | `retained_now` pour un protocole **minimal** (règles de découpage de scope, source de vérité unique pour version canonique, règle de précédence en conflit) ; `deferred` pour granularité optimale et protocole d'assemblage complet |
| **Lieu principal** | architecture |
| **Lieu(x) secondaire(s)** | state (mise à jour `multi_ia_parallel_readiness_status`) ; pipeline (règles de séquencement) |
| **Priorité** | ÉLEVÉ |
| **Justification** | `PF_PRINCIPLE_MULTI_IA_READY` est déclaré exigence de premier rang. En l'état, deux IAs parallèles peuvent produire des manifests incompatibles. Le protocole n'a pas besoin d'être complet pour V0 mais doit exister en version minimale opérationnable. |
| **Impact si non traité** | Scénario SA-02 (PERP_K7X2) et Scénario C (PPLXAI_5LVBSV) : collision de versions canoniques entre IAs parallèles, manifest final incohérent. |
| **Pré-condition** | Aucune pré-condition normative. Décision sur le niveau de formalisme minimal acceptable. |
| **Note de séquencement** | Après ARB-02 (emplacement projections), car le protocole multi-IA référence probablement les projections comme point de synchronisation. |
| **Niveau de consensus** | **fort** |

---

### ARB-04 — Contrat minimal : obligations fingerprints et bootstrap_contract non définies

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-04 |
| **Sujet** | `produced_instance_identity.reproducibility_fingerprints` et `runtime_entrypoint_contract.bootstrap_contract` : requis mais contenu non défini |
| **Source(s)** | PPLXAI_5LVBSV E-01 ; implicite dans PERP_K7X2 Axe 4 |
| **Statut proposé** | `retained_now` pour définir un contenu minimum attendu ; `deferred` pour schéma complet |
| **Lieu principal** | architecture |
| **Lieu(x) secondaire(s)** | state (mise à jour `produced_application_contract_status`) |
| **Priorité** | ÉLEVÉ |
| **Justification** | Une obligation requise sans définition de contenu est une obligation non vérifiable. Un manifest peut satisfaire le contrat avec des champs vides. La définition minimale (ex. « fingerprints = hash des versions des cores canoniques utilisés en input ; bootstrap_contract = liste des prérequis runtime déclarés ») est atteignable dans ce patch. |
| **Impact si non traité** | Les applications produites ont une reproductibilité non auditée. Deux IAs produisent des fingerprints incomparables. |
| **Pré-condition** | Décision humaine sur le contenu minimal de chaque obligation. |
| **Niveau de consensus** | **medium** — PPLXAI_5LVBSV le nomme explicitement ; PERP_K7X2 le signale implicitement. |

---

### ARB-05 — Sur-déclaration de maturité dans `capabilities_present`

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-05 |
| **Sujet** | `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` classées en `capabilities_present` alors qu'elles couvrent des intentions ou règles sans outillage |
| **Source(s)** | PPLXAI_5LVBSV E-03 ; PERP_K7X2 Axe 6 (« maturité reconnue vs maturité réelle ») |
| **Statut proposé** | `retained_now` — reclassification en `capabilities_partial` avec wording distinguant « principe déclaré » de « capacité opérationnelle présente » |
| **Lieu principal** | state |
| **Lieu(x) secondaire(s)** | aucun |
| **Priorité** | ÉLEVÉ |
| **Justification** | Une sur-déclaration de maturité est une forme de fausse norme : une IA lit l'état et suppose une capacité disponible qui n'existe pas. C'est un défaut de wording constatif, corrigeable sans impact sur l'architecture. La règle « séparation prescriptif/constatif » impose que le state reflète la réalité, pas l'intention. |
| **Impact si non traité** | Risque d'hallucination de capacité par une IA lisant l'état. |
| **Pré-condition** | Aucune. |
| **Niveau de consensus** | **fort** |

---

### ARB-06 — Gouvernance release : statut des artefacts V0 en `current` hors manifest officiel

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-06 |
| **Sujet** | Les deux artefacts factory sont dans `docs/cores/current/` mais hors du manifest officiel courant |
| **Source(s)** | PERP_K7X2 C6 ; PPLXAI_5LVBSV C-03 |
| **Statut proposé** | `retained_now` — documenter explicitement dans le state que la régularisation du manifest est l'objet d'un STAGE_07 futur ; interdire toute promotion supplémentaire sans pipeline formel |
| **Lieu principal** | state (note et blocker explicite) |
| **Lieu(x) secondaire(s)** | manifest/release governance (STAGE_07 futur) |
| **Priorité** | ÉLEVÉ |
| **Justification** | La situation est antérieure au mécanisme de promotion formelle. Elle crée une ambiguïté réelle sur le statut de « current » selon la lecture (manifest vs. répertoire). La correction V0 n'est pas d'intégrer les artefacts au manifest (trop lourd sans pipeline formalisé), mais de rendre la note explicite et contraignante : « ne pas promouvoir d'autres artefacts dans current/ avant STAGE_07 opérationnel ». |
| **Désaccord entre rapports** | PPLXAI_5LVBSV le classe CRITIQUE, PERP_K7X2 BASSE-MOYENNE. **Arbitrage : ÉLEVÉ.** Le risque est réel mais maîtrisable par un wording explicite sans patch d'architecture. |
| **Pré-condition** | Aucune. |
| **Niveau de consensus** | **fort sur la réalité du problème** ; **medium sur la gravité** |

---

### ARB-07 — Critères de sortie de maturité V0 vers version suivante

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-07 |
| **Sujet** | Absence de `exit_criteria` ou `next_maturity_target` dans `maturity_by_layer` et `last_assessment` |
| **Source(s)** | PERP_K7X2 C4 |
| **Statut proposé** | `deferred` — mais avec wording explicite dans le state que l'absence de critères de sortie est un gap connu, et décision assumée de les fixer lors du prochain run |
| **Lieu principal** | state |
| **Lieu(x) secondaire(s)** | pipeline (clause de gouvernance de run) |
| **Priorité** | MODÉRÉ |
| **Justification** | L'absence de critères de sortie est un risque de pilotage, pas un trou normatif immédiat. Une V0 peut légitimement ne pas avoir de critères de progression formalisés. Cependant, un report non assumé risque de laisser ce point ouvert indéfiniment. Le patch V0 doit ajouter dans `last_assessment` une déclaration explicite : « exit_criteria will be defined in next run ». |
| **Pré-condition** | Aucune. |
| **Niveau de consensus** | **medium** — présent dans PERP_K7X2, non nommé dans PPLXAI_5LVBSV. |

---

### ARB-08 — Vérification et formalisation des prompts partagés requis

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-08 |
| **Sujet** | Prompts partagés (`Challenge_platform_factory.md`, `Make21` à `Make24`) référencés dans le pipeline mais non vérifiés |
| **Source(s)** | PERP_K7X2 C5 ; implicite dans PPLXAI_5LVBSV Axe 9 |
| **Statut proposé** | `retained_now` pour vérification d'existence ; `deferred` pour complétion éventuelle de prompts manquants |
| **Lieu principal** | pipeline (note dans `pipeline.md`) |
| **Lieu(x) secondaire(s)** | hors périmètre factory stricto sensu (concerne `docs/prompts/shared/`) |
| **Priorité** | MODÉRÉ |
| **Justification** | Un pipeline qui référence des prompts non vérifiés n'est pas entièrement exécutable. La vérification est une action légère et bloquante pour STAGE_03+. Si un prompt est absent, un stub ou flag `PROMPT_MISSING` doit être posé. |
| **Pré-condition** | Accès au répertoire `docs/prompts/shared/` — hors scope du patch factory lui-même. |
| **Niveau de consensus** | **moyen** |

---

### ARB-09 — Outillage complet (validators automatisés, pipeline complet)

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-09 |
| **Sujet** | Validators non implémentés, pipeline skeleton incomplet, schémas fins manquants |
| **Source(s)** | PERP_K7X2 multiple ; PPLXAI_5LVBSV multiple |
| **Statut proposé** | `deferred` — ces éléments sont reconnus dans `capabilities_absent` et sont normaux pour un V0 |
| **Lieu principal** | validator/tooling (futur) |
| **Lieu(x) secondaire(s)** | state (déjà correctement déclaré) |
| **Priorité** | FAIBLE pour ce run |
| **Justification** | La V0 est un skeleton assumé. Les validators, schémas fins et pipeline complet relèvent des cycles suivants. Le state le documente correctement. Aucun patch supplémentaire n'est nécessaire sur ce sujet. |
| **Niveau de consensus** | **fort** |

---

### ARB-10 — Ambiguïté STAGE_04 / STAGE_06 même prompt

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-10 |
| **Sujet** | STAGE_04 et STAGE_06 utilisent le même prompt `Make23PlatformFactoryValidation.md` sans différenciation |
| **Source(s)** | PPLXAI_5LVBSV M-01 |
| **Statut proposé** | `deferred` — acceptable V0 si le prompt est paramétré à l'appel avec l'objet de la validation |
| **Lieu principal** | pipeline |
| **Priorité** | FAIBLE |
| **Justification** | Un prompt générique paramétré est une pratique acceptable. Le risque est documentaire, pas normatif. Le pipeline peut ajouter une note distinguant l'objet de chaque stage dans l'appel. |
| **Niveau de consensus** | **weak** — non repris dans PERP_K7X2. |

---

### ARB-11 — Absence de lien d'appartenance run dans les challenge reports (STAGE_02 rule)

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-11 |
| **Sujet** | Les challenge reports ne sont pas liés à un `run_id`, ce qui peut polluer les runs futurs |
| **Source(s)** | PPLXAI_5LVBSV M-02 |
| **Statut proposé** | `retained_now` — ajouter un champ `pipeline_run_id` dans le format de challenge report et dans les règles STAGE_02 |
| **Lieu principal** | pipeline |
| **Priorité** | MODÉRÉ |
| **Justification** | Le scénario D (PPLXAI_5LVBSV) est plausible : un report d'un run antérieur peut être consommé en STAGE_02 sans que l'opérateur sache que la correction a déjà été traitée. Un champ `pipeline_run_id` dans chaque report, et une règle dans STAGE_02 « ne considérer que les reports du run courant ou les reports explicitement marqués actifs », suffit. C'est un patch léger de pipeline. |
| **Niveau de consensus** | **medium** — non repris par PERP_K7X2 mais non contradictoire. |

---

## Points retenus maintenant

| ARB-ID | Sujet | Lieu principal | Priorité |
|---|---|---|---|
| ARB-01 | Invariants constitutionnels runtime absents des axes de validation | architecture | CRITIQUE |
| ARB-02 | Projections dérivées : emplacement + protocole minimal | architecture + state | CRITIQUE |
| ARB-03 | Multi-IA : protocole minimal d'assemblage | architecture + state | ÉLEVÉ |
| ARB-04 | Contrat minimal : fingerprints + bootstrap_contract | architecture | ÉLEVÉ |
| ARB-05 | Sur-déclaration de maturité reclassification | state | ÉLEVÉ |
| ARB-06 | Gouvernance release : note contraignante artefacts V0 current | state | ÉLEVÉ |
| ARB-08 | Vérification existence prompts partagés | pipeline (hors factory) | MODÉRÉ |
| ARB-11 | Lien run_id dans challenge reports | pipeline | MODÉRÉ |

---

## Points reportés (deferred)

| ARB-ID | Sujet | Justification du report |
|---|---|---|
| ARB-07 | Critères de sortie de maturité V0→V1 | Acceptable V0 ; décision assumée explicitement dans state |
| ARB-09 | Outillage complet (validators, schémas fins, pipeline complet) | V0 skeleton assumé ; correctement déclaré dans state |
| ARB-10 | Ambiguïté STAGE_04/STAGE_06 même prompt | Risque documentaire, pas normatif ; acceptable V0 |

---

## Points hors périmètre factory

| Sujet | Source | Justification |
|---|---|---|
| Schémas fins (manifest_schema, runtime_typology, configuration_schema, packaging_schema) | PERP_K7X2 Axe 4 ; PPLXAI_5LVBSV | Hors périmètre V0 ; dans `capabilities_absent` ; seront traités dans les cycles suivants |
| Granularité modulaire optimale + protocole d'assemblage IA complet | Both | Explicitement déférés dans `deferred_challenges` de l'architecture |
| Contenu domaine-spécifique (knowledge graph, MSC, seuils) | Both | `does_not_govern` dans architecture |

---

## Points sans consensus ou nécessitant discussion finale

| Sujet | Tension | Recommandation pour consolidation |
|---|---|---|
| Niveau de gravité de l'anomalie manifest/current (ARB-06) | PPLXAI_5LVBSV : CRITIQUE vs PERP_K7X2 : BASSE-MOYENNE | Arbitrage retenu : ÉLEVÉ. Confirmer si la voie de régularisation STAGE_07 est acceptable sans intégration immédiate au manifest. |
| Niveau de formalisme du protocole minimal multi-IA (ARB-03) | PPLXAI_5LVBSV plus exigeant sur le scope du protocole | Décider si le protocole minimal suffit à déclarer la readiness ou si un déféré assumé est préférable. |
| ARB-01 modalité déclarative vs. probatoire | Recommandation : déclarative V0 ; confirmer avec l'humain | La décision de reporter la vérification probatoire à V1 doit être arbitrée explicitement. |

---

## Corrections à arbitrer avant patch

### Patch-1 (CRITIQUE — architecture) — Ajouter axe `runtime_constitutional_constraints` dans `minimum_axes`

- **Élément concerné :** `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation :** `platform_factory_architecture.yaml`
- **Action :** Ajouter un axe `runtime_constitutional_constraints` listant les invariants à asserter (runtime_local, no_runtime_content_generation, no_runtime_feedback_generation, patch_precomputed_off_session, no_partial_patch_state). Marquer `validation_mode: declarative_only_in_v0`.
- **Dépendance :** ARB-01 indépendant.

### Patch-2 (CRITIQUE — architecture + state) — Décider emplacement et poser protocole minimal de validation des projections

- **Élément concerné :** `generated_projection_rules.emplacement_policy` + `contracts.execution_projection_contract` + `derived_projection_conformity_status`
- **Localisation :** architecture + state
- **Action :** Décider l'emplacement (proposition : `docs/pipelines/platform_factory/projections/`) et l'inscrire dans `emplacement_policy`. Définir dans l'architecture un bloc `projection_validation_minimum_protocol` minimal (règles de marquage, d'invalidation post-patch canonique, de version). Mettre à jour le state.
- **Pré-condition :** Décision humaine sur l'emplacement retenu.

### Patch-3 (ÉLEVÉ — architecture + state) — Protocole minimal d'assemblage multi-IA

- **Élément concerné :** `multi_ia_parallel_readiness` (architecture) + `multi_ia_parallel_readiness_status` (state)
- **Localisation :** architecture + state
- **Action :** Ajouter dans l'architecture un bloc `multi_ia_decomposition_minimum_protocol` avec : règles de découpage de scope (un scope par IA, no_overlap requis), source de vérité unique pour la version canonique (version du run au démarrage), règle de précédence en cas de conflit (dernière projection validée prime sauf instruction explicite). Mettre à jour le state.
- **Dépendance :** Après Patch-2 (projections définies comme point de synchronisation).

### Patch-4 (ÉLEVÉ — architecture) — Définir contenu minimal de fingerprints et bootstrap_contract

- **Élément concerné :** `produced_instance_identity.reproducibility_fingerprints` + `runtime_entrypoint_contract.bootstrap_contract`
- **Localisation :** architecture
- **Action :** Définir `reproducibility_fingerprints` minimum = {versions des cores canoniques utilisés en input, date du run, agent_id} ; définir `bootstrap_contract` minimum = {liste des prérequis runtime déclarés, type d'entrypoint}. Marquer les deux comme `schema_v0_minimal`.

### Patch-5 (ÉLEVÉ — state) — Reclassification `capabilities_present` → `capabilities_partial`

- **Élément concerné :** `capabilities_present.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` + `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Localisation :** state uniquement
- **Action :** Déplacer vers `capabilities_partial` avec wording distinguant « principe/intention déclarée » de « capacité opérationnelle ». Ajouter note explicative sur chaque capacité.

### Patch-6 (ÉLEVÉ — state) — Note contraignante sur artefacts V0 en current hors manifest

- **Élément concerné :** `metadata.notes` + `blockers` dans state
- **Localisation :** state
- **Action :** Remplacer la note informative par une contrainte explicite : « Aucun artefact supplémentaire ne doit être ajouté dans docs/cores/current/ avant que STAGE_07 et STAGE_08 soient opérationnels ». Référencer comme `PF_CONSTRAINT_NO_PROMOTION_BEFORE_STAGE_07_OPERATIONAL`.

### Patch-7 (MODÉRÉ — pipeline) — Ajouter champ `pipeline_run_id` dans le format de challenge report

- **Élément concerné :** Structure des challenge reports + règle STAGE_02 dans `pipeline.md`
- **Localisation :** pipeline
- **Action :** Ajouter dans le template de challenge report un champ `pipeline_run_id`. Ajouter dans STAGE_02 une règle : « ne considérer que les reports appartenant au run courant ou explicitement marqués valides pour ce run ».

---

## Répartition par lieu de correction

| Lieu | ARB-IDs |
|---|---|
| `platform_factory_architecture.yaml` | ARB-01, ARB-02, ARB-03, ARB-04 |
| `platform_factory_state.yaml` | ARB-02, ARB-03, ARB-05, ARB-06, ARB-07 (deferred — wording) |
| `pipeline.md` | ARB-08, ARB-10 (deferred), ARB-11 |
| `validator/tooling` | ARB-09 (deferred) |
| `manifest/release governance` | ARB-06 (secondaire) |
| `hors périmètre factory` | schémas fins, granularité modulaire, contenu domaine |

---

## Séquencement recommandé

1. **Patch-1** — Axe constitutionnel runtime (indépendant, peut être fait en premier)
2. **Patch-5** — Reclassification maturité (indépendant, léger)
3. **Patch-6** — Note contraignante release (indépendant, léger)
4. **Patch-2** — Emplacement + protocole minimal projections (pré-condition humaine requise)
5. **Patch-3** — Protocole multi-IA minimal (après Patch-2)
6. **Patch-4** — Fingerprints + bootstrap_contract (indépendant mais après Patch-2 pour cohérence)
7. **Patch-7** — Pipeline run_id (indépendant, hors factory)

---

## Priorités de patch

| Priorité | ARB-IDs | Justification |
|---|---|---|
| CRITIQUE | ARB-01, ARB-02 | Trous normatifs actifs : une application peut être produite en violation de la Constitution ou d'une projection périmée |
| ÉLEVÉ | ARB-03, ARB-04, ARB-05, ARB-06 | Risques opérationnels directs : multi-IA non praticable, contrat non vérifiable, maturité surdéclarée, statut release ambigu |
| MODÉRÉ | ARB-08, ARB-11 | Risques de traçabilité et d'exécutabilité pipeline ; correctifs légers |
| FAIBLE/DÉFÉRÉ | ARB-07, ARB-09, ARB-10 | Acceptables V0 ; reportés avec wording honnête |

---

## Résultat terminal

**arbitrage_run_id :** `PFARB_20260404_PERP_RVG5KZ`

**Fichier écrit :** `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_proposal_PFARB_20260404_PERP_RVG5KZ.md`

**Résumé ultra-court :** 2 challenge reports consolidés. Aucun désaccord de fond. 6 corrections retenues maintenant (2 critiques, 4 élevées) + 2 modérées + 3 reportées. Séquencement en 7 patches proposé. Pré-condition humaine requise uniquement sur ARB-02 (emplacement des projections dérivées).

---

_Rapport généré par PERP (Perplexity AI — Sonnet 4.6) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04_
_Ce rapport est une proposition d'arbitrage indépendante. Il ne constitue pas l'arbitrage canonique final du stage._
_Destiné à la consolidation finale humaine-assistée._
