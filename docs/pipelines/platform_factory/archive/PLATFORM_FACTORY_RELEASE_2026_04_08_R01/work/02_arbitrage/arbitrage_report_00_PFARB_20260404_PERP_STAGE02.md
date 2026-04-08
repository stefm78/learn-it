# STAGE_02_FACTORY_ARBITRAGE_MULTI — Rapport d'arbitrage

**arbitrage_run_id :** `PFARB_20260404_PERP_STAGE02`
**date :** 2026-04-04
**agent :** PERP (Perplexity AI — Sonnet 4.6)
**pipeline :** `docs/pipelines/platform_factory/pipeline.md` — STAGE_02_FACTORY_ARBITRAGE
**challenge_reports consolidés :**
- `PFCHAL_20260404_PERPLX_A1J77P`
- `PFCHAL_20260404_PERP_K7X2`
- `PFCHAL_20260404_PPLXAI_5LVBSV`
- `PFCHAL_20260404_PXADV_BB1MZX`

---

## Résumé d'arbitrage

Quatre rapports de challenge convergent sur une même anatomie de risques. La baseline V0.1 est constitutionnellement compatible dans sa structure prescriptive, honnête dans son état constatif, et exploitable pour le cycle de patch. Les désaccords entre rapports sont mineurs et portent sur la gravité relative de certains findings, pas sur leur existence. Deux zones divergent légèrement : le report `PERPLX_A1J77P` soulève un binding constitutionnel plus granulaire (5 invariants non propagés vs 3–4 dans les autres), et `PXADV_BB1MZX` est le seul à identifier explicitement `STAGE_05` sans contrat d'atomicité comme risque élevé indépendant. Les deux angles sont confirmés.

**Résultat : 8 décisions d'arbitrage. 5 retenues maintenant (dont 2 critiques). 2 reportées avec re-wording obligatoire. 1 clarification requise avant patch.**

---

## Findings consolidés

### Convergence totale (4/4 rapports)

| ID consolidé | Sujet | Gravité consensus |
|---|---|---|
| **FC-01** | Contrat minimal d'application : absence d'attestation des invariants constitutionnels runtime (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`) | **Critique** |
| **FC-02** | Projections dérivées : emplacement TBD, validateur absent, protocole de régénération absent | **Critique / Élevé** |
| **FC-03** | Multi-IA : exigence premier rang déclarée, protocole d'assemblage et de résolution de conflits entièrement absents | **Élevé** |
| **FC-04** | Artefacts V0 dans `docs/cores/current/` mais hors manifest officiel — statut ambigu | **Modéré / Critique** |
| **FC-05** | Maturité surdéclarée : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` classée `capabilities_present` alors que le mécanisme opérationnel est entièrement absent | **Élevé** |

### Divergences tranchées

**D1 — Gravité de FC-04 (artefacts hors manifest)**

- `PPLXAI_5LVBSV` et `PXADV_BB1MZX` : **critique**
- `PERP_K7X2` : **basse-moyenne**
- `PERPLX_A1J77P` : **structurel**

**Arbitrage D1 :** Gravité retenue = **modérée**. Les artefacts sont dans `current/` et le pipeline les traite explicitement comme baseline released (Rule 3). L'ambiguïté est reconnue, bornée, et n'expose pas à une violation constitutionnelle active. Correction graduée : wording dans le state + décision d'un chemin de régularisation, sans exiger un STAGE_07/08 complet dans ce cycle.

**D2 — STAGE_05 sans atomicité (présent dans `PXADV_BB1MZX` uniquement)**

**Arbitrage D2 :** Finding confirmé indépendamment. `INV_NO_PARTIAL_PATCH_STATE` est un invariant constitutionnel. Retenu comme finding supplémentaire **FC-06**.

**D3 — `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` surdéclaré**

**Arbitrage D3 :** Sur-déclaration de wording, pas d'erreur normative. Retenu comme finding **FC-07** de gravité modérée — reporté, traitement dans le state lors d'un prochain cycle de maintenance.

**D4 — Binding supplémentaires (`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`)**

**Arbitrage D4 :** Absorbés dans FC-01. La correction de FC-01 doit couvrir l'ensemble des invariants runtime et patch-lifecycle. La liste étendue est retenue comme périmètre de FC-01.

**D5 — Absence de critères de sortie de maturité V0→V1**

**Arbitrage D5 :** Valide. Retenu comme finding **FC-08** de gravité modérée. Reporté (REP-01).

---

## Décisions immédiates

### DEC-01 — Axe constitutionnel runtime dans le contrat minimal

| Champ | Valeur |
|---|---|
| **Finding source** | FC-01 (4/4 rapports) + D4 |
| **Décision** | `retained_now` |
| **Lieu principal** | `platform_factory_architecture.yaml` — section `contracts.produced_application_minimum_contract.minimum_validation_contract` |
| **Lieu secondaire** | `platform_factory_state.yaml` — mise à jour de `produced_application_contract_status` |
| **Priorité** | **Critique** |
| **Justification** | Un contrat minimal qui ne propage pas les invariants constitutionnels runtime crée une zone de violation silencieuse. Ce n'est pas une incomplétude V0 normale : c'est un trou de gouvernance actif dès le premier usage. Le patch doit ajouter un axe nommé `runtime_constitutional_constraints` (ou équivalent) dans `minimum_axes`, listant les invariants à attester. |
| **Arbitrage sur le niveau de preuve** | Pour une V0, le niveau accepté est **déclaratif** — le manifest d'une application produite doit contenir une attestation explicite. Un validateur outillé est un objectif V1. |
| **Périmètre exact de l'axe à créer** | Obligatoires : `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`. Conditionnels (si l'application embarque un mécanisme de patch ou délègue une évaluation de seuil) : `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE`, `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`. |
| **Impact si non traité** | Une application produite par la factory peut être déclarée conforme tout en violant des invariants constitutionnels fondamentaux, sans qu'aucun mécanisme ne le détecte. |
| **Pré-condition** | Aucune |

---

### DEC-02 — Projections dérivées : décision de localisation et de protocole minimal

| Champ | Valeur |
|---|---|
| **Finding source** | FC-02 (4/4 rapports) |
| **Décision globale** | `retained_now` — partiellement |

**Sous-décision 2a — Emplacement**

| Champ | Valeur |
|---|---|
| **Décision** | `retained_now` |
| **Arbitrage** | Emplacement décidé : `docs/pipelines/platform_factory/projections/` — isolé du core, accessible au pipeline, traçable par git, non confondu avec `docs/cores/current/`. Le patch doit clore le TBD en remplaçant `status: TBD` par ce chemin et les règles associées (naming, version, invalidation post-patch). |
| **Lieu principal** | `platform_factory_architecture.yaml` — `generated_projection_rules.emplacement_policy` |
| **Lieu secondaire** | `platform_factory_state.yaml` — `derived_projection_conformity_status` |

**Sous-décision 2b — Validateur**

| Champ | Valeur |
|---|---|
| **Décision** | `deferred` — V1 |
| **Obligation immédiate** | Le state doit indiquer que `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` reste `absent` et que l'usage de projections avant validation outillée impose une revue manuelle de conformité. L'architecture doit ajouter un bloc `validation_protocol_minimum` textuel. |

**Sous-décision 2c — Invalidation post-patch**

| Champ | Valeur |
|---|---|
| **Décision** | `retained_now` |
| **Règle à poser** | Toute projection dérivée est invalidée et doit être régénérée après tout patch d'un artefact canonique source dans son scope. Cette règle est textuelle dans l'architecture V0 ; son outillage est V1. |
| **Lieu principal** | `platform_factory_architecture.yaml` — `generated_projection_rules` |

| **Priorité globale** | **Élevé** |
|---|---|
| **Impact si non traité** | Dérive normative silencieuse active dès le premier usage de projections par des agents IA |

---

### DEC-03 — Multi-IA : protocole d'assemblage minimal

| Champ | Valeur |
|---|---|
| **Finding source** | FC-03 (4/4 rapports) |
| **Décision** | `retained_now` — niveau minimal |
| **Arbitrage de niveau** | Un protocole complet (granularité modulaire, résolution de conflits fine) reste différé — V1. En revanche, un protocole minimal d'assemblage doit être posé dans l'architecture maintenant : (1) règle de source de vérité unique pour la version canonique déclarée dans les outputs IA parallèles ; (2) obligation de déclarer le `run_id` et le `scope_id` dans chaque output IA ; (3) point d'assemblage désigné (rôle humain ou agent désigné au STAGE_02). |
| **Re-wording du state obligatoire** | `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` doit être promu en `blockers` avec sévérité `medium`. |
| **Lieu principal** | `platform_factory_architecture.yaml` — section `multi_ia_parallel_readiness` |
| **Lieu secondaire** | `platform_factory_state.yaml` — section `blockers` + `multi_ia_parallel_readiness_status` |
| **Priorité** | **Élevé** |
| **Pré-condition** | Aucune — le minimum posé ici est textuel et ne requiert pas d'outillage |
| **Impact si non traité** | Collision silencieuse d'outputs multi-IA non gouvernée dès le premier run parallèle réel |

---

### DEC-04 — Maturité surdéclarée : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`

| Champ | Valeur |
|---|---|
| **Finding source** | FC-05 (4/4 rapports) |
| **Décision** | `retained_now` |
| **Arbitrage** | `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` doit passer de `capabilities_present` à `capabilities_partial`. Description corrigée : _"La règle d'usage des projections dérivées validées est définie dans l'architecture. Le mécanisme opérationnel (stockage, validateur, protocole de régénération) est partiellement résolu dans ce cycle (emplacement et règle d'invalidation) et partiellement différé (validateur outillé)."_ |
| **Lieu principal** | `platform_factory_state.yaml` — section `capabilities_present` → déplacer vers `capabilities_partial` |
| **Lieu secondaire** | Aucun |
| **Priorité** | **Élevé** |
| **Justification** | Le classement `present` d'une capacité sans mécanisme opérationnel expose les agents IA à une hallucination de capacité — erreur active, pas cosmétique |

---

### DEC-05 — Gouvernance release : régularisation statut V0 en current

| Champ | Valeur |
|---|---|
| **Finding source** | FC-04 (4/4 rapports) |
| **Décision** | `retained_now` — niveau minimal |
| **Arbitrage de traitement** | Option retenue : documenter explicitement dans le state que l'intégration au manifest officiel est l'objet du premier cycle STAGE_07 complet. Ajouter dans `platform_factory_state.yaml` un bloc `release_regularization_plan` minimal précisant : (a) statut actuel = _baseline released par décision de pipeline (Rule 3), non encore intégrée au manifest officiel_ ; (b) action de régularisation = _intégrer au manifest lors du premier STAGE_07 complet_. |
| **Ne pas faire dans ce cycle** | Modifier le manifest officiel — c'est STAGE_07. |
| **Lieu principal** | `platform_factory_state.yaml` — section `blockers` ou nouvelle section `release_regularization_plan` |
| **Lieu secondaire** | `platform_factory_architecture.yaml` — note metadata optionnelle |
| **Priorité** | **Modéré** |

---

### DEC-06 — STAGE_05 : absence de règle d'atomicité

| Champ | Valeur |
|---|---|
| **Finding source** | FC-06 (`PXADV_BB1MZX`) — confirmé |
| **Décision** | `retained_now` |
| **Arbitrage** | `INV_NO_PARTIAL_PATCH_STATE` est un invariant constitutionnel fort. STAGE_05 (apply) doit déclarer une règle d'atomicité minimale. Le patch relève du **pipeline**, pas du contenu canonique. Règle minimale à ajouter : _"L'application du patchset est atomique. En cas d'échec sur un artefact, aucun artefact du patchset n'est considéré comme appliqué. L'état de `work/05_apply/patched/` doit être soit le patchset complet soit l'état antérieur complet."_ |
| **Lieu principal** | `docs/pipelines/platform_factory/pipeline.md` — section STAGE_05 |
| **Lieu secondaire** | Aucun |
| **Priorité** | **Élevé** |
| **Impact si non traité** | Violation constitutionnelle possible sur `INV_NO_PARTIAL_PATCH_STATE` lors de l'application d'un patchset multi-fichiers |

---

## Clarifications requises avant patch

### CLAR-01 — Format homogène des challenge reports et lien d'appartenance run

| Champ | Valeur |
|---|---|
| **Finding source** | `PPLXAI_5LVBSV` (M-02), `PXADV_BB1MZX` (F-01) |
| **Décision** | `clarification_required` |
| **Question à trancher** | Le pipeline doit-il imposer un schéma minimal de challenge report (sections obligatoires) en STAGE_01, et les reports doivent-ils être liés à un `run_id` pour éviter qu'un STAGE_02 ultérieur consomme des reports d'un run antérieur ? |
| **Pourquoi non tranchée maintenant** | La réponse conditionne à la fois le format des outputs STAGE_01 et les règles de lecture de STAGE_02. Ce sujet touche la gouvernance du pipeline et requiert une décision humaine sur le niveau de formalisme V0 acceptable. |
| **Lieu si retenu** | `pipeline.md` — STAGE_01 + STAGE_02 |
| **Impact si non adressé** | Reports de runs antérieurs réinjectés dans un STAGE_02 futur — findings déjà traités recyclés comme actifs |

---

## Reports assumés

### REP-01 — Critères de sortie de maturité V0→V1 (FC-08)

| Champ | Valeur |
|---|---|
| **Finding source** | `PERP_K7X2` (C4), `PPLXAI_5LVBSV` (Axe 6) |
| **Décision** | `deferred` |
| **Justification** | Des critères de sortie de maturité sont utiles mais prématurés avant d'avoir complété un premier cycle de patch. Leur définition dépend du résultat du patch V0→V0.1. Ils doivent être l'objet du STAGE_02 du cycle suivant. |
| **Obligation de re-wording** | Le state doit indiquer explicitement que les critères de progression sont différés au prochain cycle d'arbitrage. |
| **Lieu si retenu dans le prochain cycle** | `platform_factory_state.yaml` — section `maturity_by_layer` |

### REP-02 — Validateur outillé pour projections dérivées

| Champ | Valeur |
|---|---|
| **Décision** | `deferred` — V1 |
| **Justification** | Un validateur mécanique est une cible d'architecture correcte mais hors périmètre V0. Cela ne supprime pas l'obligation de définir une règle textuelle de validation minimale (incluse dans DEC-02). |

### REP-03 — Schémas fins (manifest, configuration, packaging, runtime entrypoint)

| Champ | Valeur |
|---|---|
| **Décision** | `deferred` — reconnu dans l'état, acceptable V0 |
| **Justification** | Consensus 4/4 rapports. Le state les liste déjà comme `capabilities_absent`. Aucun re-wording nécessaire. |

### REP-04 — Granularité modulaire et protocole de résolution de conflits multi-IA

| Champ | Valeur |
|---|---|
| **Décision** | `deferred` — V1 |
| **Justification** | Seul le minimum d'assemblage est retenu maintenant (DEC-03). La granularité fine et la résolution de conflits algorithmique restent différées. |

### REP-05 — `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` wording (FC-07)

| Champ | Valeur |
|---|---|
| **Décision** | `deferred` — faible priorité |
| **Justification** | Wording légèrement ambigu mais sans risque opérationnel actif. À corriger lors d'un prochain cycle de maintenance du state si jugé pertinent. |

---

## Répartition par lieu de correction

### `platform_factory_architecture.yaml`

| Decision | Section cible |
|---|---|
| DEC-01 | `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` — ajouter axe `runtime_constitutional_constraints` |
| DEC-02a | `generated_projection_rules.emplacement_policy` — remplacer TBD par `docs/pipelines/platform_factory/projections/` + règles de naming et invalidation |
| DEC-02b (partiel) | `generated_projection_rules` — ajouter bloc `validation_protocol_minimum` (textuel, sans outillage) |
| DEC-02c | `generated_projection_rules` — ajouter règle d'invalidation post-patch canonique |
| DEC-03 | `multi_ia_parallel_readiness` — ajouter `minimum_assembly_protocol` (source de vérité canonique unique, `run_id` + `scope_id` obligatoires dans outputs) |

### `platform_factory_state.yaml`

| Decision | Section cible |
|---|---|
| DEC-01 | `produced_application_contract_status` — mettre à jour pour refléter l'ajout de l'axe constitutionnel |
| DEC-02a | `derived_projection_conformity_status` — clore le TBD emplacement |
| DEC-03 | `blockers` — ajouter `PF_BLOCKER_MULTI_IA_ASSEMBLY_PROTOCOL_ABSENT` (sévérité `medium`) ; `multi_ia_parallel_readiness_status` — mise à jour |
| DEC-04 | `capabilities_present` → `capabilities_partial` pour `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` avec description corrigée |
| DEC-05 | Ajouter `release_regularization_plan` ou note dans `blockers` sur le statut current/manifest |
| REP-01 | Indiquer explicitement que les critères de sortie maturité sont différés au prochain cycle |

### `pipeline.md`

| Decision | Section cible |
|---|---|
| DEC-06 | STAGE_05 — ajouter règle d'atomicité et comportement en cas d'échec partiel |
| CLAR-01 | STAGE_01 + STAGE_02 — à traiter si la clarification est tranchée par l'humain |

---

## Séquencement recommandé pour STAGE_03

1. Patcher `platform_factory_architecture.yaml` en premier (DEC-01, DEC-02a, DEC-02b, DEC-02c, DEC-03) — les corrections architecturales sont les plus structurantes.
2. Patcher `platform_factory_state.yaml` ensuite (DEC-01 mise à jour, DEC-02a mise à jour, DEC-03 blocker, DEC-04, DEC-05, REP-01 note différement).
3. Patcher `pipeline.md` en dernier (DEC-06).
4. CLAR-01 est séparé — à traiter après décision humaine, peut ne pas bloquer STAGE_03.

---

## Priorités de patch

| Priorité | Decision ID | Sujet |
|---|---|---|
| **Critique** | DEC-01 | Axe `runtime_constitutional_constraints` dans le contrat minimal |
| **Élevé** | DEC-02 | Projections dérivées : emplacement, règle d'invalidation, protocole de validation textuel |
| **Élevé** | DEC-03 | Multi-IA : minimum assembly protocol + promotion en blocker |
| **Élevé** | DEC-04 | Reclassification maturité `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` |
| **Élevé** | DEC-06 | STAGE_05 atomicité (pipeline) |
| **Modéré** | DEC-05 | Release regularization plan dans le state |
| **Différé** | REP-01 | Critères de sortie de maturité |
| **Différé** | REP-02 | Validateur outillé projections |
| **Différé** | REP-03 | Schémas fins |
| **Différé** | REP-04 | Granularité multi-IA + résolution conflits |
| **Clarification** | CLAR-01 | Format challenge reports + lien run_id |

---

## Notes finales

Ce rapport ne contient aucun patch YAML.
Il ne réécrit aucun contenu d'artefact canonique.
Tout patch relève de STAGE_03_FACTORY_PATCH_SYNTHESIS.
Ce rapport est l'unique artefact de STAGE_02 pour ce run.

**challenge_run_id source :** `PFCHAL_20260404_PERPLX_A1J77P` · `PFCHAL_20260404_PERP_K7X2` · `PFCHAL_20260404_PPLXAI_5LVBSV` · `PFCHAL_20260404_PXADV_BB1MZX`
**Fichier écrit :** `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_report_PFARB_20260404_PERP_STAGE02.md`
**Destinataire :** STAGE_03_FACTORY_PATCH_SYNTHESIS

_Rapport généré par PERP (Perplexity AI) — STAGE_02_FACTORY_ARBITRAGE_MULTI — 2026-04-04_
