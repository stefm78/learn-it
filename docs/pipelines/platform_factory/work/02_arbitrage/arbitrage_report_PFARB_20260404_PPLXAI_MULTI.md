# Arbitrage Report — Platform Factory Baseline V0

| Champ | Valeur |
|---|---|
| **arbitrage_run_id** | PFARB_20260404_PPLXAI_MULTI |
| **date** | 2026-04-04 |
| **stage** | STAGE_02_FACTORY_ARBITRAGE |
| **agent** | PPLXAI (Perplexity AI — Sonnet 4.6) |
| **prompt_principal** | docs/prompts/shared/Make21PlatformFactoryArbitrage.md |
| **destinataire_stage_suivant** | STAGE_03_FACTORY_PATCH_SYNTHESIS |

## Challenge reports consolidés

| challenge_run_id | Agent | Fichier source |
|---|---|---|
| PFCHAL_20260404_PERPLX_A1J77P | PERPLX | work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md |
| PFCHAL_20260404_PERP_K7X2 | PERP | work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md |
| PFCHAL_20260404_PPLXAI_5LVBSV | PPLXAI | work/01_challenge/challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md |
| PFCHAL_20260404_PXADV_BB1MZX | PXADV | work/01_challenge/challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md |
| PFCHAL_20260404_GPT54_X7K2Q | GPT54 | work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md |
| PFCHAL_20260404_PERPLX_7K2R | PERPLX | work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_7K2R.md |

---

## Résumé d'arbitrage

La Platform Factory V0 est constitutionnellement valide dans sa posture d'autorité : elle ne redéfinit pas la Constitution, ne duplique pas le Référentiel, et maintient la séparation prescriptif/constatif. Elle est patchable et exploitable pour STAGE_03.

**Six sujets dominent l'ensemble des 6 rapports avec convergence quasi-totale :**

1. **Contrat minimal d'application ne couvre pas les invariants constitutionnels de runtime** — critique, tous les rapports s'accordent.
2. **Projections dérivées autorisées comme unique contexte IA sans validateur, stockage ni protocole** — critique, tous les rapports s'accordent.
3. **Artefacts factory dans `docs/cores/current/` hors manifest officiel** — divergence de gravité entre rapports (critique vs modéré) — arbitrage : **élevé**.
4. **Absence de protocole d'assemblage multi-IA** — élevé, consensus.
5. **Surdéclaration de maturité dans `capabilities_present`** — modéré à élevé, consensus.
6. **Absence de critères de sortie de maturité V0 → V0.2** — modéré, relevé par 3 rapports.

**Sujets propres à un ou deux rapports, arbitrés en regard du contexte :**

- **STAGE_05 sans atomicité/rollback** (PXADV, PPLXAI) : retenu comme correction pipeline — élevé.
- **Fingerprints de reproductibilité non définis** (PXADV, PPLXAI, PERPLX_7K2R) : retenu — modéré.
- **STAGE_07/STAGE_08 délèguent à des specs possiblement absentes** (PERPLX_7K2R, PPLXAI_5LVBSV) : retenu comme vérification requise — élevé.
- **Handoff contract factory → instanciation aval** (GPT54) : reporté V0.2 — acceptable V0.
- **Prompts partagés non vérifiés** (PERP_K7X2, PPLXAI_5LVBSV) : clarification requise — modéré.
- **Lien d'appartenance run dans les reports** (PPLXAI_5LVBSV) : retenu comme amélioration pipeline — faible.
- **Même prompt STAGE_04 et STAGE_06** (PPLXAI_5LVBSV, PXADV) : retenu — modéré.

---

## Axe 1 — Consolidation des findings

### F-01 — Contrat minimal sans axe de conformité constitutionnelle runtime

**Sources :** PERPLX_A1J77P (Axe 4), PERP_K7X2 (C1), PPLXAI_5LVBSV (C-01), PXADV_BB1MZX (C1), GPT54_X7K2Q (CORR-01), PERPLX_7K2R (CORR-02) — **consensus 6/6**.

**Formulations concordantes :** Les `minimum_validation_axes` (`structure`, `minimum_contract_conformance`, `traceability`, `packaging`) ne couvrent pas les invariants constitutionnels de runtime : `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE`.

**Désaccords à trancher :**
- PERPLX_A1J77P décompose le problème en 6 bindings absents distincts (dont `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`).
- PXADV_BB1MZX classe ce risque comme "critique".
- GPT54_X7K2Q classe ce risque comme "élevé" (non "critique").
- **Arbitrage :** critique retenu, conforme à la majorité (4/6 classent critique ou équivalent).

**Périmètre du finding :** Le finding porte sur le `produced_application_minimum_contract` dans `platform_factory_architecture.yaml`. Il ne s'agit pas d'un manque de la Constitution elle-même. L'absence de propagation vers le contrat minimal est une lacune de la factory.

---

### F-02 — Projections dérivées : usage autorisé sans garde-fous opérationnels

**Sources :** tous les 6 rapports — **consensus 6/6**.

**Formulations concordantes :** l'usage d'une projection comme "unique artefact fourni à une IA" est autorisé par l'architecture, mais trois conditions préalables sont absentes ou TBD :
1. Emplacement de stockage (`emplacement_policy.status: TBD`)
2. Validator de conformité normative (`validator_definition: missing`)
3. Protocole de régénération déterministe (`regeneration_protocol: missing`)

**Désaccord notable :** PERPLX_A1J77P signale en plus un risque de "paraphrase dangereuse" et de "promotion implicite" comme angle mort distinct ; PERPLX_7K2R souligne l'inversion de séquence (droit d'usage déclaré avant les gardes-fous). Ces deux angles sont complémentaires, non contradictoires.

**Arbitrage :** Ces deux angles sont fusionnés en un seul finding F-02 avec trois sous-composantes : (a) emplacement TBD, (b) validator absent, (c) inversion usage/sécurité.

---

### F-03 — Artefacts factory hors manifest officiel

**Sources :** tous les 6 rapports — **consensus 6/6**.

**Divergence de gravité :**
- PPLXAI_5LVBSV, PERPLX_7K2R, PXADV_BB1MZX : **critique** ou **élevé**.
- PERP_K7X2, GPT54_X7K2Q : **élevé**.
- PERPLX_A1J77P : **modéré** (bloqueur medium dans le state est correctement nommé).

**Arbitrage :** **Élevé.** La situation est reconnue dans l'état, bornée explicitement. Elle crée une ambiguïté gouvernance réelle mais ne bloque pas immédiatement un cycle de patch. Elle doit être résolue avant toute release formelle (STAGE_07).

---

### F-04 — Protocole d'assemblage multi-IA absent

**Sources :** PERPLX_A1J77P (Axe 7), PERP_K7X2 (C3), PPLXAI_5LVBSV (E-02), PXADV_BB1MZX (C3), GPT54_X7K2Q (CORR-05), PERPLX_7K2R (CORR-04) — **consensus 6/6**.

**Concordance :** absence de decomposition_protocol, module_granularity_convention, ai_output_assembly_protocol, conflict_resolution_protocol.

**Désaccord :** PXADV_BB1MZX recommande de promouvoir le gap en blocker ; PERP_K7X2 le classe en "corrections à arbitrer" sans forcer ce reclassement. **Arbitrage :** le reclassement en blocker de sévérité `medium` dans le state est retenu (voir décision D-04 ci-dessous).

---

### F-05 — Surdéclaration de maturité dans capabilities_present

**Sources :** PERPLX_A1J77P (Axe 6), PERP_K7X2 (C4 / E-03), PPLXAI_5LVBSV (E-03), PXADV_BB1MZX (C6), GPT54_X7K2Q (Axe 6), PERPLX_7K2R (CORR-05) — **consensus 6/6**.

**Capacités concernées :**
- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` : classée `present`, devrait être `partial` (règle définie, mécanisme absent).
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` : discussion entre rapports — PPLXAI_5LVBSV et PERPLX_7K2R questionnent le classement `present`, les autres l'acceptent sous la lecture "l'intention est posée".

**Arbitrage :**
- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → reclassement en `capabilities_partial` — **retenu**.
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` → maintenu en `capabilities_present` avec wording précisant "intention posée, pas capacité opérationnelle" — **retenu (correction de wording uniquement)**.
- `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` → le finding de PERPLX_A1J77P (6 open_points non résolus) est valide : ce n'est pas un reclassement global mais une précision dans la description — **retenu (correction de wording)**.

---

### F-06 — Absence de critères de sortie de maturité V0 → V0.2

**Sources :** PERP_K7X2 (C4), PPLXAI_5LVBSV (Axe 6), PERPLX_7K2R (Axe 6 implicite) — **consensus 3/6**.

**Arbitrage :** Retenu comme correction modérée dans le state. Absence de `exit_criteria` par couche rend la gouvernance de maturité non pilotable. Acceptable V0 si explicitement reconnu, mais un stub minimal est patchable maintenant.

---

### F-07 — STAGE_05 sans contrat d'atomicité / rollback

**Sources :** PXADV_BB1MZX (C4), PPLXAI_5LVBSV (implicite M-01) — **2/6 rapports**.

**Arbitrage :** Retenu — élevé. `INV_NO_PARTIAL_PATCH_STATE` est un invariant constitutionnel fort. L'absence de règle d'atomicité dans STAGE_05 est un trou réel. Correction dans pipeline.md.

---

### F-08 — Fingerprints de reproductibilité non définis

**Sources :** PXADV_BB1MZX (C5), PPLXAI_5LVBSV (E-01), PERPLX_7K2R (CORR-06) — **3/6 rapports**.

**Arbitrage :** Retenu — modéré. `reproducibility_fingerprints` est requis dans le contrat mais sans contenu minimal défini. Correction dans architecture.

---

### F-09 — STAGE_07 / STAGE_08 délèguent à des specs potentiellement absentes

**Sources :** PERPLX_7K2R (CORR-03), PPLXAI_5LVBSV (Axe 9), PERP_K7X2 (C5) — **3/6 rapports**.

**Arbitrage :** Clarification requise avant patch. Vérifier l'existence de `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`. Si absents, créer des stubs. Lieu : pipeline.

---

### F-10 — Prompts partagés non vérifiés (Make21-Make24)

**Sources :** PERP_K7X2 (C5), PPLXAI_5LVBSV (Axe 9) — **2/6 rapports**.

**Arbitrage :** Clarification requise. Ce rapport est lui-même produit avec Make21 comme cadre, donc Make21 existe. Les prompts Make22, Make23, Make24 et Challenge_platform_factory.md doivent être vérifiés. Lieu : pipeline / prompts shared.

---

### F-11 — Handoff contract factory → instanciation aval

**Source :** GPT54_X7K2Q (CORR-04) — **1/6 rapports**.

**Arbitrage :** Reporté V0.2. La frontière est correctement tracée dans l'architecture. L'absence d'un handoff contract explicite est acceptable pour une V0 dont le pipeline d'instanciation n'existe pas encore.

---

### F-12 — Même prompt STAGE_04 et STAGE_06

**Sources :** PPLXAI_5LVBSV (M-01), PXADV et PERPLX_7K2R (Axe 9 implicite) — **2/6 rapports**.

**Arbitrage :** Retenu — modéré. Risque de confusion opérateur / IA entre validation patchset (STAGE_04) et validation core (STAGE_06). Une clarification dans pipeline.md est nécessaire. Si les deux usages sont intentionnellement partagés, l'invoquer doit être documenté comme un appel paramétré.

---

### F-13 — Absence de lien d'appartenance run dans les challenge reports

**Source :** PPLXAI_5LVBSV (M-02) — **1/6 rapports**.

**Arbitrage :** Retenu — faible. Une convention de run_id dans les noms de fichiers de challenge est déjà partiellement en place (le run_id est dans le nom du fichier). Une règle explicite dans STAGE_02 filtrant par run_id courant est utile mais pas urgente.

---

## Axe 2 — Décisions immédiates

| ID | Sujet | Décision | Priorité |
|---|---|---|---|
| D-01 | Ajouter un axe `runtime_constitutional_compliance` dans `minimum_validation_axes` | retained_now | critique |
| D-02a | Décider l'emplacement des projections dérivées | retained_now | critique |
| D-02b | Bloquer ou conditionner l'usage "artefact unique" jusqu'à instrumentation minimale | retained_now | critique |
| D-02c | Poser un protocole minimal de validation de projection avant usage | retained_now | critique |
| D-03 | Documenter explicitement le régime transitoire current/manifest V0 | retained_now | élevé |
| D-04 | Poser un protocole minimal d'assemblage multi-IA et reclasser le gap en blocker | retained_now | élevé |
| D-05a | Reclasser `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `partial` | retained_now | élevé |
| D-05b | Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | retained_now | modéré |
| D-06 | Ajouter des `exit_criteria` minimaux par couche dans le state | retained_now | modéré |
| D-07 | Ajouter une règle d'atomicité minimale dans STAGE_05 | retained_now | élevé |
| D-08 | Définir le contenu minimal de `reproducibility_fingerprints` | retained_now | modéré |
| D-09 | Vérifier et compléter les specs STAGE_07 et STAGE_08 | clarification_required | élevé |
| D-10 | Vérifier l'existence des prompts partagés Make22-Make24 | clarification_required | modéré |
| D-11 | Handoff contract factory → instanciation | deferred | acceptable V0 |
| D-12 | Clarifier le partage STAGE_04 / STAGE_06 dans pipeline.md | retained_now | modéré |
| D-13 | Convention run_id dans les reports STAGE_01 | retained_now | faible |

---

## Axe 3 — Répartition architecture / state

| ID | Lieu principal | Lieu secondaire | Justification |
|---|---|---|---|
| D-01 | architecture | state (mise à jour capacité) | Ajout d'axe dans `minimum_validation_axes` = règle prescriptive ; le state enregistre la mise à jour de maturité |
| D-02a | architecture | state | Décision emplacement = règle architecturale ; state reflète `PF_BLOCKER_PROJECTION_LOCATION_PENDING` résolu |
| D-02b | architecture | pipeline | Conditionner l'usage autorisé = règle architecturale ; le pipeline peut ajouter un gate |
| D-02c | architecture | state + validator/tooling | Définition du protocole = règle prescriptive ; state reflète `derived_projection_conformity_status` |
| D-03 | state | architecture (note metadata) | Le régime transitoire est un constat de gouvernance ; la note metadata de l'architecture est mise à jour en cohérence |
| D-04 | architecture | state + pipeline | Le protocole multi-IA = principe prescriptif ; state reflète le reclassement en blocker ; pipeline peut intégrer une règle d'assemblage |
| D-05a/b | state | — | Correction du classement et du wording de capacités = constatif |
| D-06 | state | — | `exit_criteria` = constat de pilotage de maturité |
| D-07 | pipeline | — | Règle d'atomicité STAGE_05 = gouvernance d'exécution |
| D-08 | architecture | — | Définition du contenu minimal = contrat prescriptif |
| D-09 | pipeline | — | Vérification et création des specs = exécutabilité pipeline |
| D-10 | pipeline | — | Vérification des prompts = exécutabilité pipeline |
| D-12 | pipeline | — | Clarification d'usage prompt = gouvernance d'exécution |
| D-13 | pipeline | — | Convention de report = gouvernance d'exécution |

---

## Axe 4 — Répartition factory / instanciation / hors périmètre

| ID | Domaine | Justification |
|---|---|---|
| D-01 | factory générique | Le contrat minimal d'application produite est le périmètre central de la factory |
| D-02a/b/c | factory générique | Les projections dérivées sont le mécanisme de liaison factory → IA |
| D-03 | release/manifest transverse | Gouvernance release dépassant la couche factory seule |
| D-04 | factory générique + pipeline | Le multi-IA est une exigence de la factory ; le protocole d'assemblage est à cheval factory/pipeline |
| D-05a/b | factory générique (state) | Constat interne à la factory |
| D-06 | factory générique (state) | Gouvernance de maturité interne |
| D-07 | pipeline factory | Règle d'exécution pipeline |
| D-08 | factory générique | Contrat minimal d'application produite |
| D-09 | pipeline factory | Specs de stages manquantes |
| D-10 | pipeline factory | Prompts d'exécution |
| D-11 | futur pipeline instanciation | La frontière handoff relève du pipeline d'instanciation qui n'existe pas encore |
| D-12 | pipeline factory | Gouvernance d'exécution |
| D-13 | pipeline factory | Gouvernance d'exécution |

---

## Axe 5 — Répartition contenu / pipeline / validator / release governance

| ID | Lieu principal | Lieu secondaire | Séquence |
|---|---|---|---|
| D-01 | artefact canonique (architecture) | validator/tooling (futur) | Architecture d'abord, validator dans un prochain cycle |
| D-02a | artefact canonique (architecture) | state | Décision de stockage en architecture, reflet dans state |
| D-02b | artefact canonique (architecture) | pipeline | Architecture conditionne, pipeline matérialise le gate |
| D-02c | artefact canonique (architecture) | validator/tooling | Protocole minimal en architecture, implémentation validator V0.2 |
| D-03 | release governance | architecture (note) | Statut current/manifest clarif dans state + note architecture |
| D-04 | artefact canonique (architecture) | pipeline | Principe en architecture, protocole d'assemblage en pipeline |
| D-05a/b | artefact canonique (state) | — | Correction state seule |
| D-06 | artefact canonique (state) | — | Correction state seule |
| D-07 | pipeline | — | Règle pipeline |
| D-08 | artefact canonique (architecture) | — | Définition dans architecture |
| D-09 | pipeline | — | Vérification et complétion |
| D-10 | pipeline | — | Vérification |
| D-12 | pipeline | — | Clarification |
| D-13 | pipeline | — | Convention |

---

## Axe 6 — Arbitrage de compatibilité constitutionnelle

### Sujet : invariants runtime non propagés dans le contrat minimal (D-01)

**Invariants concernés :**
- `INV_RUNTIME_FULLY_LOCAL` : une application produite ne doit pas dépendre d'un réseau en runtime.
- `INV_NO_RUNTIME_CONTENT_GENERATION` : pas de génération de contenu en session.
- `INV_NO_RUNTIME_FEEDBACK_GENERATION` (`CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`) : pas de feedback généré hors templates.
- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` : patchs précomputés hors session.
- `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` : validation locale déterministe.
- `INV_NO_PARTIAL_PATCH_STATE` : état interdit de patch partiel.

**Décision d'arbitrage :**
- Ces invariants doivent être **propagés explicitement dans les axes de validation minimaux** du contrat application produite.
- Le mode de propagation retenu est **déclaratif dans un premier temps** : le manifest doit asserter la conformité à chacun de ces invariants par leur ID. La preuve automatique (validator) est différée à V0.2.
- Un axe nommé `constitutional_runtime_compliance` est ajouté dans `minimum_validation_axes`.
- L'observabilité minimale doit inclure un signal `local_runtime_mode: boolean` attestant l'absence d'appel réseau runtime.

**Autorité normative préservée :** Cette correction ne réécrit pas les invariants. Elle crée une exigence de référencement explicite des IDs d'invariants dans le manifest de l'application. L'autorité reste dans la Constitution. La factory impose uniquement la traçabilité déclarative.

---

### Sujet : projections dérivées (D-02)

**Invariants concernés :** `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT`, `INV_RUNTIME_FULLY_LOCAL` (via projection), `no_normative_divergence`.

**Décision d'arbitrage :**
- **D-02a** : l'emplacement des projections est décidé — **`docs/pipelines/platform_factory/projections/`** — dossier dédié, hors `docs/cores/current/`, versionné avec le run_id d'émission.
- **D-02b** : l'usage "artefact unique pour une IA" est **conditionnel** : il ne s'active que si les trois conditions sont remplies (emplacement stable, protocole de validation minimal, run_id traçable). Tant que validator complet est absent, le protocole minimal de validation est : comparaison diff textuelle avec le canonique source par l'IA productrice avant livraison.
- **D-02c** : le protocole minimal de validation d'une projection est défini dans l'architecture : (1) scope déclaré, (2) sources canoniques référencées par version, (3) attestation de non-paraphrase normative par l'IA productrice, (4) run_id traçable.

---

## Axe 7 — Lecture V0 et niveau de maturité

### Ce qui est acceptable en V0 (ne doit pas être patchté maintenant)

- Schémas fins non finalisés : manifest schema, runtime typology, configuration schema, packaging schema.
- Validators dédiés non implémentés.
- Pipeline d'instanciation absent.
- Granularité modulaire et taille optimale des projections non définis.
- Handoff contract factory → instanciation.
- Evidence mince pour le state V0.

### Ce qui doit être corrigé malgré le statut V0

- Axe de conformité constitutionnelle runtime dans le contrat minimal (D-01) — car sans cela, une application produite peut naître inconstitutionnelle sans détection, ce qui est un risque actif, pas théorique.
- Emplacement des projections (D-02a) — car sans adresse stable, le principe multi-IA est inopérable.
- Condition d'usage des projections (D-02b) — car l'architecture autorise déjà un usage fort avant les gardes-fous.

### Ce qui doit être reporté mais avec wording plus honnête

- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → reclassé `partial` (D-05a).
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` → wording précisant "intention posée, outillage absent" (D-05b).
- `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` → description ajoutant "6 open_points structurants non résolus" (D-05b étendu).

---

## Axe 8 — Pré-conditions de patch

| ID | Pré-condition manquante | Nature | Clarification requise |
|---|---|---|---|
| D-01 | Liste exhaustive des invariants constitutionnels applicables à une application produite | Fond normatif | Non — le socle canonique est suffisamment lu pour extraire cette liste |
| D-02a | Emplacement décidé | Fond / lieu | Non — décision arbitrée ici : `docs/pipelines/platform_factory/projections/` |
| D-02b | Définition des "trois conditions" | Schéma | Non — définies dans D-02c |
| D-02c | Protocole minimal de validation | Fond | Non — protocole minimal défini à l'axe 6 |
| D-03 | Décision sur la voie de régularisation current/manifest | Fond | Oui — l'humain doit décider entre deux options : (A) intégration au manifest existant, (B) création d'un companion manifest platform_factory |
| D-07 | Définition de "tout ou rien" dans STAGE_05 | Schéma | Non — règle simple : si un patch échoue, nommer le fichier `FAILED_<nom>` et arrêter le stage |
| D-09 | Existence des specs STAGE_07 et STAGE_08 | Preuve constatative | Oui — vérifier l'existence dans le dépôt avant de patcher pipeline.md |

---

## Axe 9 — Priorisation

| Priorité | ID | Sujet | Lieu |
|---|---|---|---|
| **critique** | D-01 | Axe constitutional_runtime_compliance dans minimum_validation_axes | architecture |
| **critique** | D-02a | Emplacement des projections dérivées | architecture |
| **critique** | D-02b | Conditionner l'usage "artefact unique" | architecture |
| **critique** | D-02c | Protocole minimal de validation de projection | architecture |
| **élevé** | D-03 | Régime transitoire current/manifest | state + architecture (note) |
| **élevé** | D-04 | Protocole minimal assemblage multi-IA + reclassement blocker | architecture + state |
| **élevé** | D-05a | Reclassement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en partial | state |
| **élevé** | D-07 | Règle d'atomicité STAGE_05 | pipeline |
| **élevé** | D-09 | Vérification/création specs STAGE_07 et STAGE_08 | pipeline |
| **modéré** | D-05b | Wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et `SCOPE_DEFINED` | state |
| **modéré** | D-06 | Exit_criteria minimaux par couche | state |
| **modéré** | D-08 | Contenu minimal reproducibility_fingerprints | architecture |
| **modéré** | D-10 | Vérification prompts Make22-Make24 | pipeline |
| **modéré** | D-12 | Clarification STAGE_04 vs STAGE_06 (prompt partagé) | pipeline |
| **faible** | D-11 | Handoff contract factory → instanciation | reporté |
| **faible** | D-13 | Convention run_id dans reports STAGE_01 | pipeline |

---

## Décisions détaillées

---

### D-01 — Ajouter `constitutional_runtime_compliance` dans `minimum_validation_axes`

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-01 |
| **Sujet** | Axe de conformité constitutionnelle runtime dans le contrat minimal d'application |
| **Sources** | PERPLX_A1J77P, PERP_K7X2 (C1), PPLXAI_5LVBSV (C-01), PXADV_BB1MZX (C1), GPT54_X7K2Q (CORR-01), PERPLX_7K2R (CORR-02) |
| **Décision** | retained_now |
| **Lieu principal** | architecture — `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Lieu secondaire** | architecture — `minimum_observability_contract.minimum_signals` ; state (mise à jour maturité) |
| **Priorité** | critique |
| **Justification** | Invariant constitutionnel fort (`INV_RUNTIME_FULLY_LOCAL` etc.) non propagé dans le contrat application = risque actif qu'une application soit factory-conforme et constitutionnellement non conforme. La factory serait responsible d'une fausse attestation. |
| **Impact si non traité** | La factory ne peut pas certifier la conformité constitutionnelle des applications qu'elle produit. |
| **Correction à appliquer** | Ajouter dans `minimum_axes` : `constitutional_runtime_compliance` (couvre INV_RUNTIME_FULLY_LOCAL, INV_NO_RUNTIME_CONTENT_GENERATION, INV_NO_RUNTIME_FEEDBACK_GENERATION, INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION, INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC, INV_NO_PARTIAL_PATCH_STATE). Mode : déclaratif (manifest asserter la conformité par ID d'invariant). Ajouter dans `minimum_observability_contract.minimum_signals` : `local_runtime_mode`. |
| **Note de séquencement** | Prérequis pour D-02c |

---

### D-02 — Gouvernance des projections dérivées

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-02 |
| **Sujet** | Emplacement, conditions d'usage, protocole minimal de validation des projections dérivées |
| **Sources** | tous les 6 rapports |
| **Décision** | retained_now (3 sous-décisions) |
| **Lieu principal** | architecture |
| **Lieu secondaire** | state, pipeline |
| **Priorité** | critique |
| **Justification** | Le mécanisme de projection est le vecteur central de liaison factory → IA. Son absence d'encadrement crée le risque de dérive normative silencieuse le plus élevé de la baseline. |
| **Impact si non traité** | Une IA travaillant sur une projection périmée, non validée, stockée dans un emplacement arbitraire peut produire des artefacts constitutionnellement non conformes sans détection. |
| **Corrections :** | |
| D-02a | **Emplacement** : décider dans `generated_projection_rules.emplacement_policy` que les projections sont stockées dans `docs/pipelines/platform_factory/projections/`, nommées `projection_{scope}_{run_id}.yaml`. Mettre à jour `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` de `absent` vers `present` dans le state. |
| D-02b | **Condition d'usage** : ajouter dans `execution_projection_contract` une `usage_gate` : l'usage comme "artefact unique pour IA" est conditionnel à : (1) fichier présent dans l'emplacement déclaré, (2) run_id traçable, (3) protocole minimal de validation exécuté par l'IA productrice. |
| D-02c | **Protocole minimal** : définir dans `generated_projection_rules.validation_protocol_minimal` : (1) scope déclaré explicitement, (2) sources canoniques référencées par `artifact_id` + version, (3) attestation `no_normative_divergence` signée par l'IA productrice dans les métadonnées de la projection, (4) run_id présent dans les métadonnées. |
| **Note de séquencement** | D-02a avant D-02c ; D-02c avant D-02b |

---

### D-03 — Régime transitoire current/manifest

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-03 |
| **Sujet** | Artefacts platform_factory dans `docs/cores/current/` hors manifest officiel |
| **Sources** | tous les 6 rapports |
| **Décision** | retained_now — mais **clarification humaine requise** avant patch |
| **Lieu principal** | state — `blockers.PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` |
| **Lieu secondaire** | architecture (note metadata) |
| **Priorité** | élevé |
| **Justification** | La situation actuelle est reconnue et explicitement documentée. Elle ne bloque pas le cycle de patch, mais elle doit être résolue avant STAGE_07. |
| **Pré-condition** | **Humain doit arbitrer** entre deux options : (A) Étendre le manifest officiel (`manifest.yaml`) pour inclure les artefacts platform_factory ; (B) Créer un `manifest_platform_factory.yaml` companion dans `docs/cores/current/`. |
| **Correction à appliquer** | Selon choix humain : mettre à jour `platform_factory_state.yaml` — `blockers` avec la décision + ETA de résolution ; mettre à jour la note metadata des deux artefacts. |
| **Impact si non traité** | Statut officiel ambigu des artefacts au moment de STAGE_07/STAGE_08. |

---

### D-04 — Protocole minimal d'assemblage multi-IA

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-04 |
| **Sujet** | Absence de protocole d'assemblage, de granularité modulaire et de résolution de conflits multi-IA |
| **Sources** | PERPLX_A1J77P (Axe 7), PERP_K7X2 (C3), PPLXAI_5LVBSV (E-02), PXADV_BB1MZX (C3), GPT54_X7K2Q (CORR-05), PERPLX_7K2R (CORR-04) |
| **Décision** | retained_now |
| **Lieu principal** | architecture — section `multi_ia_parallel_readiness` |
| **Lieu secondaire** | state (reclassement gap en blocker medium) |
| **Priorité** | élevé |
| **Justification** | L'exigence multi-IA est déclarée "premier rang" mais sans protocole opérationnel. Cette présente run d'arbitrage elle-même mobilise 6 IAs en parallèle — ce déficit est immédiatement concret, pas théorique. |
| **Impact si non traité** | Deux IAs travaillant en parallèle sur des scopes adjacents peuvent produire des outputs incompatibles sans mécanisme de détection. |
| **Correction à appliquer** | Ajouter dans architecture `multi_ia_parallel_readiness.minimum_assembly_protocol` : (1) chaque IA déclare son scope dans les métadonnées de son output, (2) les outputs sont identifiés par `[run_id]_[scope]_[agent_id]`, (3) point d'assemblage désigné = STAGE_02 (arbitrage humain ou IA arbitre désigné), (4) règle de résolution de conflit : l'arbitre décide en cas de contradiction sur un même scope. Mettre à jour state : `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` reclassé en `blockers` avec `severity: medium`. |

---

### D-05 — Corrections de maturité dans le state

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-05 |
| **Sujet** | Surdéclaration de maturité dans `capabilities_present` |
| **Sources** | PERPLX_A1J77P (Axe 6), PERP_K7X2 (E-03), PPLXAI_5LVBSV (E-03), PXADV_BB1MZX (C6), GPT54_X7K2Q (Axe 6), PERPLX_7K2R (CORR-05) |
| **Décision** | retained_now |
| **Lieu** | state |
| **Priorité** | élevé (D-05a), modéré (D-05b) |
| **Corrections :** | |
| D-05a | `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → reclasser de `capabilities_present` vers `capabilities_partial`. Wording : "La règle d'usage des projections dérivées est définie dans l'architecture. Le mécanisme opérationnel (validateur, emplacement, protocole de régénération) est absent — traité par D-02." |
| D-05b | `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` → maintenir en `capabilities_present` mais ajouter : "L'intention de pipeline est posée. Les fichiers de prompt requis sont partiellement vérifiés. L'outillage opérationnel est absent." |
| D-05c | `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` → ajouter dans la description : "6 open_points structurants restent non résolus (manifest schema, runtime entrypoint typology, configuration schema, packaging schema, projection storage location, granularity for multi-AI work)." |

---

### D-06 — Exit criteria minimaux par couche

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-06 |
| **Sujet** | Absence de critères de sortie V0 → V0.2 dans le state |
| **Sources** | PERP_K7X2 (C4), PPLXAI_5LVBSV (Axe 6), PERPLX_7K2R (Axe 6) |
| **Décision** | retained_now |
| **Lieu** | state — section `maturity_by_layer` |
| **Priorité** | modéré |
| **Correction à appliquer** | Ajouter dans chaque entrée de `maturity_by_layer` un bloc `exit_criteria_for_next_maturity` avec au minimum 1-2 conditions mesurables pour chaque couche. Exemple pour `PF_LAYER_FACTORY_ARCHITECTURE` : "validator_definition présent ET emplacement projections finalisé ET protocole assemblage multi-IA défini." |

---

### D-07 — Règle d'atomicité STAGE_05

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-07 |
| **Sujet** | STAGE_05 sans contrat d'atomicité |
| **Sources** | PXADV_BB1MZX (C4), PPLXAI_5LVBSV (implicite) |
| **Décision** | retained_now |
| **Lieu** | pipeline.md — section STAGE_05 |
| **Priorité** | élevé |
| **Justification** | `INV_NO_PARTIAL_PATCH_STATE` est un invariant constitutionnel fort. STAGE_05 est le seul point du pipeline où cet invariant peut être violé. |
| **Correction à appliquer** | Ajouter dans STAGE_05 une règle opérationnelle : "En cas d'échec d'application d'un fichier de patchset, nommer le fichier `FAILED_[nom]` dans `work/05_apply/patched/`, arrêter le stage, et ne pas continuer vers STAGE_06. L'opérateur (humain ou IA arbitre) doit corriger le patchset et relancer STAGE_05 depuis le début." |

---

### D-08 — Contenu minimal de reproducibility_fingerprints

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-08 |
| **Sujet** | `reproducibility_fingerprints` requis sans définition de contenu |
| **Sources** | PXADV_BB1MZX (C5), PPLXAI_5LVBSV (E-01), PERPLX_7K2R (CORR-06) |
| **Décision** | retained_now |
| **Lieu** | architecture — `contracts.produced_application_minimum_contract.identity.required_blocks.reproducibility_fingerprints` |
| **Priorité** | modéré |
| **Correction à appliquer** | Définir le contenu minimal : (1) `canonical_dependencies_at_build_time` : liste des `artifact_id` + version des Cores utilisés, (2) `derived_projections_used` : liste des projections dérivées avec leur `run_id`, (3) `build_timestamp` : date ISO 8601. |

---

### D-09 — Vérification specs STAGE_07 et STAGE_08

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-09 |
| **Sujet** | STAGE_07 et STAGE_08 délèguent à des specs potentiellement absentes |
| **Sources** | PERPLX_7K2R (CORR-03), PPLXAI_5LVBSV (Axe 9), PERP_K7X2 (C5) |
| **Décision** | clarification_required |
| **Lieu** | pipeline.md (si stubs à créer) |
| **Priorité** | élevé |
| **Pré-condition** | Vérifier l'existence de `docs/pipelines/platform_factory/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`. Si absents, créer des stubs avec au minimum les sections `OBJECTIF`, `INPUT`, `OUTPUT`, `RÈGLES`. |
| **Note** | Cette vérification doit être effectuée par l'opérateur avant de lancer STAGE_03. Elle n'est pas un patch YAML des artefacts canoniques. |

---

### D-10 — Vérification prompts partagés

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-10 |
| **Sujet** | Prompts Make22, Make23, Make24 et Challenge_platform_factory non vérifiés |
| **Sources** | PERP_K7X2 (C5), PPLXAI_5LVBSV (Axe 9) |
| **Décision** | clarification_required |
| **Lieu** | docs/prompts/shared/ |
| **Priorité** | modéré |
| **Pré-condition** | Vérifier l'existence de chaque prompt requis par pipeline.md. Si manquant, créer un stub ou marquer dans `PROMPT_USAGE.md`. |

---

### D-12 — Clarification STAGE_04 vs STAGE_06

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-12 |
| **Sujet** | Même prompt `Make23PlatformFactoryValidation.md` pour STAGE_04 et STAGE_06 |
| **Sources** | PPLXAI_5LVBSV (M-01), PXADV_BB1MZX (Axe 9) |
| **Décision** | retained_now |
| **Lieu** | pipeline.md — sections STAGE_04 et STAGE_06 |
| **Priorité** | modéré |
| **Correction à appliquer** | Ajouter dans pipeline.md pour STAGE_04 et STAGE_06 une note précisant les paramètres d'invocation différents : STAGE_04 valide le **patchset** (entrée : `work/03_patch/patchset/`), STAGE_06 valide les **artefacts patched** (entrée : `work/05_apply/patched/`). Si le partage est intentionnel, documenter explicitement "prompt paramétré, cf. note d'invocation". |

---

### D-13 — Convention run_id dans reports STAGE_01

| Champ | Valeur |
|---|---|
| **Decision_ID** | D-13 |
| **Sujet** | Absence de lien d'appartenance run dans les challenge reports |
| **Sources** | PPLXAI_5LVBSV (M-02) |
| **Décision** | retained_now |
| **Lieu** | pipeline.md — section STAGE_02 |
| **Priorité** | faible |
| **Correction à appliquer** | Ajouter dans la règle STAGE_02 : "Les reports consommés sont ceux du run courant, identifiés par `challenge_run_id` correspondant à l'exécution en cours. Les reports d'un run antérieur qui n'ont pas encore été arbitrés peuvent être inclus si l'opérateur le décide explicitement." |

---

## Reports assumés

| ID | Sujet | Motif de report | Condition de déclenchement |
|---|---|---|---|
| D-11 | Handoff contract factory → instanciation | Pipeline d'instanciation inexistant — no V0 need | Création du premier pipeline d'instanciation |
| — | Schémas fins (manifest, runtime, config, packaging) | Complexité disproportionnée V0 | Cycle V0.2 après que le contrat minimal de base soit stabilisé |
| — | Validators automatisés dédiés | Dépend des schémas fins | Après stabilisation des schémas |
| — | Granularité modulaire optimale | Dépend des premiers usages réels | Après 1 cycle d'instanciation |
| — | Taille optimale des projections | Idem | Idem |

---

## Répartition par lieu de correction (synthèse)

### architecture (`platform_factory_architecture.yaml`)
- D-01 : ajout axe `constitutional_runtime_compliance` + signal `local_runtime_mode`
- D-02a : décision emplacement projections → `docs/pipelines/platform_factory/projections/`
- D-02b : ajout `usage_gate` dans `execution_projection_contract`
- D-02c : ajout `validation_protocol_minimal` dans `generated_projection_rules`
- D-08 : définition contenu minimal `reproducibility_fingerprints`

### state (`platform_factory_state.yaml`)
- D-03 : mise à jour `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` avec décision humaine
- D-04 : reclassement `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker medium ; ajout capacité multi-IA protocol
- D-05a : reclassement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `capabilities_partial`
- D-05b : corrections wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et `SCOPE_DEFINED`
- D-05c : description étendue `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` avec 6 open_points
- D-06 : ajout `exit_criteria_for_next_maturity` par couche

### pipeline (`pipeline.md`)
- D-04 : ajout règle `minimum_assembly_protocol`
- D-07 : ajout règle d'atomicité STAGE_05
- D-12 : clarification STAGE_04 vs STAGE_06
- D-13 : convention run_id STAGE_02
- D-09 : vérification/création specs STAGE_07 et STAGE_08 (pré-condition)
- D-10 : vérification prompts partagés (pré-condition)

### architecture ET state (co-modification)
- D-02a : architecture (emplacement_policy) + state (`PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED`)
- D-04 : architecture (protocole) + state (reclassement gap en blocker)

---

## Séquencement recommandé pour STAGE_03

1. **Avant patch YAML :** l'opérateur vérifie D-09 (specs STAGE_07/STAGE_08) et D-10 (prompts partagés).
2. **Avant patch D-01 :** l'opérateur confirme la liste des invariants constitutionnels à propager (peut utiliser ce rapport comme liste de référence).
3. **Avant patch D-03 :** l'opérateur arbitre l'option A ou B pour le manifest (voir Axe 8 — D-03).
4. **Ordre de patch recommandé :** D-02a → D-02c → D-02b → D-01 → D-04 → D-05 → D-06 → D-07 → D-08 → D-03 (après décision humaine) → D-12 → D-13.

---

_Rapport d'arbitrage généré par PPLXAI (Perplexity AI) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04_
_Ce rapport ne contient aucun patch YAML._
_Il ne se substitue pas aux décisions humaines sur D-03, D-09, D-10._
_Destiné à STAGE_03_FACTORY_PATCH_SYNTHESIS._
