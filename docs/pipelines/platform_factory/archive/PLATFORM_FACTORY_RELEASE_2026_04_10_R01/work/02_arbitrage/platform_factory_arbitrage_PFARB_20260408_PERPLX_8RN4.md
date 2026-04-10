# Proposition d'arbitrage — Platform Factory STAGE_02

## arbitrage_run_id

`PFARB_20260408_PERPLX_8RN4`

## Date

2026-04-08

## Challenge reports considérés

| ID | Fichier | Taille |
|---|---|---|
| PFCHAL_20260408_GPT54_Q7M2 | challenge_report_PFCHAL_20260408_GPT54_Q7M2.md | 29 257 octets |
| PFCHAL_20260408_PERPLEX_K7M3 | challenge_report_PFCHAL_20260408_PERPLEX_K7M3.md | 23 147 octets |
| PFCHAL_20260408_PERPLX_K7M3 | challenge_report_PFCHAL_20260408_PERPLX_K7M3.md | 29 415 octets |
| PFCHAL_20260408_PERPL_X7T2 | challenge_report_PFCHAL_20260408_PERPL_X7T2.md | 38 708 octets |
| PFCHAL_20260408_PERPX_7KQ2 | challenge_report_PFCHAL_20260408_PERPX_7KQ2.md | 16 439 octets |

Tous les 5 rapports ont été lus et croisés. Les rapports PERPLX_K7M3 et PERPL_X7T2 sont les plus volumineux et les plus structurés (11 axes complets). GPT54_Q7M2 est comparable en couverture. PERPLEX_K7M3 et PERPX_7KQ2 sont plus synthétiques mais couvrent les mêmes thèmes majeurs.

---

## Résumé d'arbitrage

La convergence entre les 5 rapports est forte sur les 4 thèmes structurants. Aucun rapport ne contredit les autres sur les risques critiques. Les désaccords sont de formulation, de granularité ou de priorisation relative, non de fond.

**4 décisions immédiates à retenir pour patch :**

1. Ajouter un axe de validation `runtime_policy_conformance` dans le contrat minimal d'application (critique, unanime).
2. Fermer ou borner le mécanisme des `validated_derived_execution_projections` (emplacement, protocole, validator) (critique, unanime).
3. Aligner la sémantique `RELEASE_CANDIDATE` / baseline released / manifest officiel (élevé, unanime).
4. Recalibrer les `capabilities_present` qui surdéclarent la maturité dans le state (élevé, unanime).

**3 décisions différées avec wording à préciser :**

5. Protocole multi-IA opérationnel — différé mais avec exit_condition à poser.
6. Schémas détaillés (manifest, configuration, packaging) — différé V0 assumé.
7. Frontière probante factory / pipeline d'instanciation — différé V0 avec clarification de responsabilité minimale.

**Points sans consensus fort nécessitant consolidation humaine :**

- Lieu exact de stockage des projections dérivées : les rapports suggèrent des emplacements différents (sous `work/`, sous `docs/pipelines/platform_factory/projections/`, etc.). L'arbitrage final doit décider un emplacement canonique.
- Degré de correction à appliquer immédiatement sur `minimum_validation_contract` vs différer l'outillage : deux positions — corriger l'architecture maintenant + différer le validator vs corriger les deux en même temps.

---

## Synthèse des constats convergents

### Convergence 1 — Contrat minimal non probant sur les invariants constitutionnels runtime

**Présent dans :** GPT54 (Problème 1, Critique), PERPLX_K7M3 (C1+M1, Critique), PERPL_X7T2 (critique), PERPLEX_K7M3 (axe 1), PERPX_7KQ2 (axe 1+4).

**Formulation consolidée :** `minimum_validation_contract.minimum_axes` ne contient pas d'axe couvrant la conformité aux invariants runtime constitutionnels (runtime 100 % local, absence d'appel réseau temps réel, absence de génération runtime interdite). Une application produite peut passer toute la validation factory sans que ces invariants soient vérifiés. Le `minimum_observability_contract` ne contient pas non plus de signal dédié.

**Accord unanime** sur le caractère critique.

### Convergence 2 — Mécanisme des validated_derived_execution_projections non fermé

**Présent dans :** GPT54 (Problème 7+8, Critique+Élevé), PERPLX_K7M3 (P1+P2+P3, Élevé), PERPL_X7T2 (critique), PERPLEX_K7M3 (axe 5), PERPX_7KQ2 (axe 5).

**Formulation consolidée :** le principe est solide mais aucun des mécanismes qui le rendraient sûr n'est implémenté : pas de validator, pas d'emplacement de stockage décidé (`emplacement_policy: TBD`), pas de protocole de régénération, pas de fingerprint de sources. La déclaration d'usage comme "unique artefact fourni à une IA" est prématurée.

**Accord unanime** sur le caractère critique ou très élevé.

### Convergence 3 — Tension RELEASE_CANDIDATE / baseline released / hors manifest officiel

**Présent dans :** GPT54 (Problème 3+11, Élevé+Critique), PERPLX_K7M3 (G1+G2), PERPL_X7T2 (élevé), PERPLEX_K7M3 (axe 8), PERPX_7KQ2 (axe 8).

**Formulation consolidée :** le pipeline doctrine traite les artefacts comme une "released baseline", les artefacts se déclarent `RELEASE_CANDIDATE`, et l'état reconnaît qu'ils sont hors manifest officiel courant. Ces trois statuts sont contradictoires. L'absence de borne de durée pour ce déséquilibre est un trou de gouvernance.

**Note de désaccord mineur :** GPT54 classe "présence en current sans manifest" en **critique** ; les rapports Perplexity le classent en **élevé**. L'arbitrage retient **élevé** mais avec correction immédiate.

### Convergence 4 — Maturité surdéclarée dans platform_factory_state.yaml

**Présent dans :** GPT54 (Problème 9), PERPLX_K7M3 (I1+I2+S1), PERPLEX_K7M3 (axe 6), PERPX_7KQ2 (axe 6).

**Formulation consolidée :** `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est dans `capabilities_present` alors que le mécanisme complet est absent. `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` est dans `capabilities_present` alors que le pipeline est V0 non outillé. Ces deux entrées devraient passer en `capabilities_partial`.

**Accord fort.**

### Convergence 5 — Multi-IA : exigence posée, opérabilité absente

**Présent dans :** GPT54 (Problème 10), PERPLX_K7M3 (MA1+MA2), PERPLEX_K7M3 (axe 7), PERPX_7KQ2 (axe 7).

**Formulation consolidée :** granularité modulaire, protocole d'assemblage, résolution de conflit, format homogène de report sont tous absents ou différés. L'exigence est juste, mais la capacité est non opérable.

**Accord sur le niveau élevé, différé V0 acceptable si exit_condition posée.**

### Convergence 6 — bootstrap_contract et reproducibility_fingerprints non définis

**Présent dans :** PERPLX_K7M3 (M2+M3), PERPL_X7T2 (élevé), GPT54 (Problème 6, élevé).

**Formulation consolidée :** deux termes sont requis dans le contrat minimal (`bootstrap_contract`, `reproducibility_fingerprints`) sans être définis dans l'architecture ni dans le socle canonique. Toute IA instanciant ce contrat devra improviser.

**Accord élevé.**

---

## Propositions d'arbitrage par thème

---

### ARB-01 — Ajouter runtime_policy_conformance dans minimum_validation_contract

- **Élément concerné :** `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** absence d'axe de validation couvrant les invariants runtime constitutionnels
- **Statut proposé :** `retained_now`
- **Gravité :** critique
- **Justification :** unanimité des 5 rapports. Sans cet axe, aucune application produite ne peut être certifiée constitutionnellement conforme. La correction est localisée (ajout d'un axe dans une liste), ne déplace pas l'autorité normative et ne crée pas de nouvelle règle constitutionnelle.
- **Dépendance :** aucune dépendance bloquante. Le validator dédié peut venir plus tard (ARB-08).
- **Lieu principal :** architecture
- **Lieux secondaires :** state (mettre à jour `capabilities_partial`), validator/tooling (validator dédié différé)
- **Niveau de consensus :** strong
- **Note de séquencement :** à traiter en priorité 1 dans le patch.

---

### ARB-02 — Ajouter constitutional_invariants_checked dans minimum_observability_contract

- **Élément concerné :** `produced_application_minimum_contract.minimum_observability_contract.minimum_signals`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** aucun signal d'observabilité ne permet de vérifier la conformité aux invariants runtime constitutionnels
- **Statut proposé :** `retained_now`
- **Gravité :** critique (corollaire de ARB-01)
- **Justification :** corollaire direct de ARB-01. Sans signal d'observabilité correspondant, l'axe de validation serait déclaré mais non observable. Les rapports GPT54, PERPLX_K7M3 et PERPLEX_K7M3 le mentionnent explicitement.
- **Dépendance :** ARB-01
- **Lieu principal :** architecture
- **Niveau de consensus :** strong
- **Note de séquencement :** à traiter en même temps que ARB-01.

---

### ARB-03 — Définir bootstrap_contract et reproducibility_fingerprints

- **Élément concerné :** `runtime_entrypoint_contract.must_declare.bootstrap_contract` et `identity.required_blocks.reproducibility_fingerprints`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** termes requis sans définition dans l'architecture ni dans le socle canonique
- **Statut proposé :** `retained_now`
- **Gravité :** élevé
- **Justification :** termes imposés comme obligatoires dans le contrat minimal sans définition ≡ obligation non implémentable. Correction minimaliste : soit définir brièvement dans l'architecture, soit marquer `TBD` explicitement avec périmètre borné. Les rapports PERPLX_K7M3, PERPL_X7T2 et GPT54 convergent.
- **Clarification requise :** l'arbitrage doit décider entre (a) définir maintenant à haut niveau ou (b) marquer explicitement `TBD` avec une condition de déblocage. Recommandation : option (a) pour `reproducibility_fingerprints` (définition simple = empreinte canonique des artefacts sources utilisés + hash de version), option (b) pour `bootstrap_contract` (lié à la future typologie runtime, encore ouverte).
- **Lieu principal :** architecture
- **Niveau de consensus :** medium (formulation varie selon les rapports, fond convergent)

---

### ARB-04 — Résoudre emplacement_policy: TBD pour les projections dérivées

- **Élément concerné :** `generated_projection_rules.emplacement_policy`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** emplacement non décidé bloquant toute utilisation pratique
- **Statut proposé :** `retained_now`
- **Gravité :** élevé
- **Justification :** un `TBD` sur l'emplacement de stockage des projections rend impossible leur usage opérationnel par une IA. Les 5 rapports le signalent. La décision d'emplacement est préalable à tout validator.
- **Clarification requise avant patch :** l'arbitrage humain doit décider entre :
  - option A : `docs/pipelines/platform_factory/projections/` (zone dédiée, séparée de `current/`)
  - option B : `docs/pipelines/platform_factory/work/projections/` (zone de travail)
  - option C : emplacement paramétrable par application, déclaré dans le manifest
  - La recommandation de cet arbitrage est **option A** : zone dédiée et stable, distincte des zones de travail éphémères et distincte de `docs/cores/current/`.
- **Dépendance :** ARB-05 (protocole de projection)
- **Lieu principal :** architecture
- **Lieux secondaires :** state (mise à jour `PF_BLOCKER_PROJECTION_LOCATION_PENDING`), pipeline (mise à jour de la zone d'écriture déclarée)
- **Niveau de consensus :** strong sur la nécessité, medium sur le choix exact d'emplacement

---

### ARB-05 — Poser un protocole minimal des validated_derived_execution_projections

- **Élément concerné :** `execution_projection_contract`, `generated_projection_rules`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** principe déclaré mais aucun mécanisme de sûreté implémenté (validator, fingerprint, protocole de régénération)
- **Statut proposé :** `retained_now` (principe minimal) + `deferred` (outillage complet)
- **Gravité :** critique → élevé après décision de séquencement
- **Justification :** une déclaration de capacité qui précède toutes les conditions de sa sûreté est un faux niveau de maturité et un risque réel (scénario A confirmé dans les 5 rapports).
  - Ce qui doit être retenu maintenant dans l'architecture : ajouter les champs minimaux obligatoires d'une projection (scope, sources exactes, version/fingerprint, statut de validation, interdiction explicite de promotion comme source canonique, politique d'usage runtime/offsession).
  - Ce qui peut être différé : le validator outillé, le protocole de régénération automatisé.
- **Dépendance :** ARB-04 (emplacement)
- **Lieu principal :** architecture
- **Lieux secondaires :** state (recalibrer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`), validator/tooling (différé)
- **Niveau de consensus :** strong

---

### ARB-06 — Aligner la sémantique RELEASE_CANDIDATE / baseline released / manifest officiel

- **Élément concerné :** metadata des artefacts + pipeline Rule 3 + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation :** `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, `pipeline.md`
- **Problème :** trois statuts contradictoires coexistent sans décision explicite de gouvernance
- **Statut proposé :** `retained_now`
- **Gravité :** élevé
- **Justification :** le désaccord mineur entre GPT54 (critique) et les autres (élevé) est arbitré en **élevé avec correction immédiate** : le risque n'est pas encore une violation normative active, mais une ambiguïté de gouvernance qui peut en produire une. Solution minimale :
  1. Clarifier dans les métadonnées des artefacts que le statut est `CURRENT_BASELINE_UNDER_GOVERNANCE` (ou équivalent explicite) et non `RELEASE_CANDIDATE` au sens d'une release officielle imminente.
  2. Ajouter dans `platform_factory_state.yaml` une `exit_condition` au blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` : "Ce blocker doit être levé avant toute promotion V1 vers le manifest officiel courant."
  3. Aligner le wording de `pipeline.md` Rule 3 : "The current artifacts are a governed working baseline, not yet an officially manifest-integrated release."
- **Dépendance :** aucune dépendance bloquante
- **Lieu principal :** state
- **Lieux secondaires :** architecture (metadata), pipeline, manifest/release governance
- **Niveau de consensus :** strong

---

### ARB-07 — Recalibrer les capabilities_present surdéclarant la maturité

- **Élément concerné :** `capabilities_present[PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED]` et `capabilities_present[PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED]`
- **Localisation :** `platform_factory_state.yaml`
- **Problème :** deux capacités classées "présentes" alors que le mécanisme sous-jacent est absent ou incomplet
- **Statut proposé :** `retained_now`
- **Gravité :** élevé
- **Justification :** GPT54, PERPLX_K7M3, PERPLEX_K7M3 convergent. `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` doit passer en `capabilities_partial` avec description des manques (validator, storage, régénération). `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` doit rester en `capabilities_present` mais avec wording précisant "intent only, not yet tooled execution framework" — ce wording existe déjà dans `pipeline.md` mais pas dans le state.
- **Dépendance :** ARB-05
- **Lieu principal :** state
- **Niveau de consensus :** strong

---

### ARB-08 — Ajouter une matrice invariant → preuve attendue → artefact porteur

- **Élément concerné :** `dependencies_to_constitution`, `produced_application_minimum_contract`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** les dépendances constitutionnelles sont nommées mais non reliées à des preuves attendues auditable
- **Statut proposé :** `clarification_required`
- **Gravité :** élevé
- **Justification :** GPT54 (Problème 2) et PERPLEX_K7M3 (axe 1) convergent. Cependant la forme exacte de cette matrice (YAML séparé, section dans l'architecture, table dans le manifest) n'est pas encore arbitrée. Recommandation : décider d'abord le format avant le patch. Option recommandée : section dédiée dans l'architecture (`constitutional_conformance_proof_requirements`) listant par invariant les preuves minimales attendues dans le manifest et dans la validation.
- **Clarification requise :** format de la matrice à décider par l'humain avant patch.
- **Lieu principal :** architecture
- **Lieu secondaire :** validator/tooling
- **Niveau de consensus :** medium (fond convergent, forme à décider)

---

### ARB-09 — Clarifier la règle de priorité entre LAUNCH_PROMPT et companion prompt (STAGE_04, STAGE_06)

- **Élément concerné :** pipeline stages 04 et 06
- **Localisation :** `pipeline.md`
- **Problème :** deux prompts par stage sans protocole de priorité
- **Statut proposé :** `retained_now`
- **Gravité :** modéré
- **Justification :** PERPLX_K7M3 (PL2) et PERPL_X7T2 convergent. Correction simple : ajouter une note dans le pipeline précisant que le `LAUNCH_PROMPT` est le contrat d'entrée opérateur et que le `companion prompt` est l'instruction métier IA. En cas de conflit, le `companion prompt` prime pour le contenu, le `LAUNCH_PROMPT` prime pour le format de sortie.
- **Lieu principal :** pipeline
- **Niveau de consensus :** medium

---

### ARB-10 — Protocole multi-IA opérationnel

- **Élément concerné :** `multi_ia_parallel_readiness`, `multi_ia_parallel_readiness_status`
- **Localisation :** `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème :** exigence posée, opérabilité absente (granularité, assemblage, résolution de conflit)
- **Statut proposé :** `deferred`
- **Gravité :** élevé
- **Justification :** les 5 rapports le signalent comme élevé mais différable. L'état reconnaît déjà les manques. La priorité V0 est de fermer les risques constitutionnels et la gouvernance des projections avant d'instrumenter le multi-IA. Différer avec exit_condition : "Ce sujet doit être traité avant toute utilisation effective de plusieurs IA en parallèle sur la factory."
- **Condition de sortie du report :** première instance de travail multi-IA réel sur ce pipeline.
- **Lieu principal :** architecture
- **Lieu secondaire :** state, pipeline
- **Niveau de consensus :** strong sur le différé

---

### ARB-11 — Schémas détaillés (manifest, configuration, packaging, runtime typology)

- **Élément concerné :** multiples blocs du contrat minimal
- **Localisation :** `platform_factory_architecture.yaml`, `platform_factory_state.yaml`
- **Problème :** schémas détaillés non finalisés
- **Statut proposé :** `deferred` (V0 assumé)
- **Gravité :** modéré
- **Justification :** point ouvert reconnu dans tous les rapports, classé V0 acceptable. Différé sans condition de sortie précise pour l'instant, mais ne doit pas bloquer ARB-01 à ARB-09.
- **Niveau de consensus :** strong sur le différé

---

### ARB-12 — Frontière probante factory / pipeline d'instanciation

- **Élément concerné :** `PF_LAYER_APPLICATION_INSTANTIATION`, obligations du contrat minimal vs obligations d'instanciation
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** responsabilités non encore réparties explicitement entre factory et pipeline aval
- **Statut proposé :** `deferred` avec note explicite
- **Gravité :** modéré
- **Justification :** GPT54 (Problème 5), PERPLEX_K7M3 (axe 3) convergent. Le pipeline aval n'existe pas encore — la frontière ne peut pas être fermée maintenant. Ajouter une note dans l'architecture reconnaissant ce point ouvert et sa condition de fermeture.
- **Condition de sortie du report :** conception du premier pipeline d'instanciation domaine.
- **Lieu principal :** architecture
- **Niveau de consensus :** strong sur le différé

---

## Points retenus

| ID | Sujet | Priorité | Lieu principal |
|---|---|---|---|
| ARB-01 | Ajouter axe `runtime_policy_conformance` dans `minimum_validation_contract` | Critique | architecture |
| ARB-02 | Ajouter signal `constitutional_invariants_checked` dans `minimum_observability_contract` | Critique | architecture |
| ARB-03 | Définir ou borner `bootstrap_contract` et `reproducibility_fingerprints` | Élevé | architecture |
| ARB-04 | Résoudre `emplacement_policy: TBD` pour les projections dérivées | Élevé | architecture |
| ARB-05 | Poser protocole minimal des projections (champs obligatoires) | Élevé | architecture |
| ARB-06 | Aligner sémantique RELEASE_CANDIDATE / baseline / manifest | Élevé | state |
| ARB-07 | Recalibrer capabilities_present surdéclarant la maturité | Élevé | state |
| ARB-09 | Clarifier priorité LAUNCH_PROMPT vs companion prompt | Modéré | pipeline |

---

## Points rejetés

Aucun finding des 5 rapports n'est rejeté. Tous les problèmes soulevés ont une base explicite dans les artefacts ou dans le socle canonique.

---

## Points différés

| ID | Sujet | Condition de sortie | Priorité |
|---|---|---|---|
| ARB-10 | Protocole multi-IA opérationnel (granularité, assemblage, résolution de conflit) | Première instance de travail multi-IA réel | Élevé |
| ARB-11 | Schémas détaillés (manifest, configuration, packaging, runtime typology) | Décision de V1 | Modéré |
| ARB-12 | Frontière probante factory / pipeline d'instanciation | Conception du premier pipeline d'instanciation domaine | Modéré |

---

## Points hors périmètre factory

- Design du contenu de tout domaine spécifique.
- Runtime d'une application Learn-it particulière.
- Logique métier de feedback domaine.
- Définition du pipeline d'instanciation lui-même.

---

## Points sans consensus ou nécessitant discussion finale

### PC-1 — Emplacement exact des projections dérivées

**Contexte :** les rapports convergent sur la nécessité d'un emplacement distinct de `docs/cores/current/`, mais proposent des zones différentes.
**Position de cet arbitrage :** option A (`docs/pipelines/platform_factory/projections/`).
**Décision finale requise :** confirmation ou choix alternatif par l'humain avant patch ARB-04.

### PC-2 — Forme de la matrice invariant → preuve → artefact (ARB-08)

**Contexte :** fond unanime mais forme non décidée (section YAML dans l'architecture, document séparé, table dans le manifest).
**Décision finale requise :** choix du format avant que le patch ARB-08 soit rédigé. Si non décidé avant STAGE_03, ARB-08 est différé à la prochaine itération.

### PC-3 — Criticité de la présence hors manifest (GPT54: critique vs autres: élevé)

**Arbitrage de cet arbitrage :** retenu comme **élevé** avec correction immédiate (ARB-06). Le classement critique de GPT54 est recevable si la baseline est effectivement consommée comme released par des outils ou des pipelines avals. À surveiller en consolidation finale.

---

## Corrections à arbitrer avant patch

### Priorité 1 — Fermer la preuve constitutionnelle minimale (critique)

- **ARB-01 :** ajouter `runtime_policy_conformance` dans `minimum_validation_contract.minimum_axes`.
- **ARB-02 :** ajouter `constitutional_invariants_checked` dans `minimum_observability_contract.minimum_signals`.
- **Périmètre du patch :** architecture uniquement. Le validator dédié est différé.

### Priorité 2 — Fermer le mécanisme des projections dérivées (élevé)

- **ARB-04 :** résoudre `emplacement_policy: TBD` → décision d'emplacement préalable requise (PC-1).
- **ARB-05 :** ajouter dans `execution_projection_contract` les champs minimaux obligatoires d'une projection : `scope`, `sources_exact`, `version_fingerprint`, `validation_status`, `promotion_to_canonical_forbidden: true`, `usage_policy` (runtime/offsession).
- **Périmètre du patch :** architecture. Validator différé.

### Priorité 3 — Aligner la sémantique de statut (élevé)

- **ARB-06 :** 3 modifications coordonnées (metadata architecture, state blocker exit_condition, pipeline Rule 3).
- **ARB-07 :** recalibrer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` vers `capabilities_partial`.

### Priorité 4 — Définir les termes non définis du contrat minimal (élevé)

- **ARB-03 :** définir `reproducibility_fingerprints` à haut niveau dans l'architecture. Marquer `bootstrap_contract` comme `TBD` avec condition de déblocage explicite.

### Priorité 5 — Clarifier le pipeline (modéré)

- **ARB-09 :** ajouter note de priorité entre LAUNCH_PROMPT et companion prompt dans STAGE_04 et STAGE_06.

### Clarification requise avant patch (bloquante pour ARB-08)

- **ARB-08 :** décider du format de la matrice invariant → preuve → artefact. Sans cette décision, l'arbitrage ARB-08 reste en `clarification_required` et ne génère pas de patch dans ce cycle.

---

## Répartition par lieu de correction

### Architecture (platform_factory_architecture.yaml)

- ARB-01 : ajout axe `runtime_policy_conformance`
- ARB-02 : ajout signal `constitutional_invariants_checked`
- ARB-03 : définition de `reproducibility_fingerprints`, bornage de `bootstrap_contract`
- ARB-04 : résolution `emplacement_policy`
- ARB-05 : ajout champs obligatoires dans `execution_projection_contract`
- ARB-08 : (si format décidé en consolidation) matrice invariant → preuve
- ARB-10 différé : protocole multi-IA (futur)
- ARB-12 différé : frontière factory/instanciation (futur)

### State (platform_factory_state.yaml)

- ARB-06 : correction metadata statut + exit_condition blocker
- ARB-07 : recalibrage capabilities

### Pipeline (pipeline.md)

- ARB-06 secondaire : mise à jour Rule 3 wording
- ARB-09 : note de priorité prompts

### Validator/tooling

- ARB-01, ARB-02, ARB-05 : validators correspondants (différés, chantier suivant)
- ARB-08 différé : validator de conformité constitutionnelle

### Manifest/release governance

- ARB-06 : exit_condition sur blocker manifest

### Hors périmètre factory

- Tout ce qui relève du domaine spécifique, du pipeline d'instanciation, du runtime d'une application particulière.

---

## Séquencement recommandé

1. Validation humaine des points PC-1 (emplacement projections) et PC-2 (format matrice ARB-08) avant que STAGE_03 commence.
2. ARB-01 + ARB-02 en premier (critique, indépendants, localisés).
3. ARB-04 + ARB-05 en deuxième (dépendance ARB-04 → ARB-05).
4. ARB-06 + ARB-07 en troisième (cohérence state, indépendant de 1-3).
5. ARB-03 + ARB-09 en quatrième (modéré, non bloquants).
6. ARB-08 en cinquième si et seulement si PC-2 est décidé en consolidation.
7. ARB-10, ARB-11, ARB-12 différés.

---

## Priorités de patch

| Priorité | ID | Sujet |
|---|---|---|
| Critique | ARB-01 | Axe runtime_policy_conformance |
| Critique | ARB-02 | Signal constitutional_invariants_checked |
| Élevé | ARB-04 | Emplacement projections dérivées |
| Élevé | ARB-05 | Protocole minimal projections |
| Élevé | ARB-06 | Alignement sémantique statut |
| Élevé | ARB-07 | Recalibrage capabilities_present |
| Élevé | ARB-03 | Définition termes contrat minimal |
| Élevé | ARB-08 | Matrice invariant → preuve (si format décidé) |
| Modéré | ARB-09 | Priorité prompts pipeline |
| Différé | ARB-10 | Protocole multi-IA |
| Différé | ARB-11 | Schémas détaillés |
| Différé | ARB-12 | Frontière factory/instanciation |
