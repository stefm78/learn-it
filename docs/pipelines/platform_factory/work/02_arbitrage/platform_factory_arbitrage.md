# Platform Factory — Arbitrage Canonique Final

## arbitrage_id

`PFARB_FINAL_20260410_CONSOLIDATION`

## Date

2026-04-10

## Statut

`APPROVED` — validé explicitement par l'humain le 2026-04-10.

---

## Challenge reports considérés

| ID | Fichier |
|---|---|
| PFCHAL_20260408_GPT54_Q7M2 | challenge_report_PFCHAL_20260408_GPT54_Q7M2.md |
| PFCHAL_20260408_PERPLEX_K7M3 | challenge_report_PFCHAL_20260408_PERPLEX_K7M3.md |
| PFCHAL_20260408_PERPLX_K7M3 | challenge_report_PFCHAL_20260408_PERPLX_K7M3.md |
| PFCHAL_20260408_PERPL_X7T2 | challenge_report_PFCHAL_20260408_PERPL_X7T2.md |
| PFCHAL_20260408_PERPX_7KQ2 | challenge_report_PFCHAL_20260408_PERPX_7KQ2.md |

## Propositions d'arbitrage considérées

| ID | Fichier |
|---|---|
| PFARB_20260408_GPT54_M4Q7 | platform_factory_arbitrage_PFARB_20260408_GPT54_M4Q7.md |
| PFARB_20260408_PERPLEX_N4W9 | platform_factory_arbitrage_PFARB_20260408_PERPLEX_N4W9.md |
| PFARB_20260408_PERPLX_8RN4 | platform_factory_arbitrage_PFARB_20260408_PERPLX_8RN4.md |
| PFARB_20260408_PERPLX_N2R8 | platform_factory_arbitrage_PFARB_20260408_PERPLX_N2R8.md |
| PFARB_20260408_PERPL_Z9K4 | platform_factory_arbitrage_PFARB_20260408_PERPL_Z9K4.md |
| PFARB_20260408_PERPX_A1B2 | platform_factory_arbitrage_PFARB_20260408_PERPX_A1B2.md |

---

## Résumé exécutif

La baseline Platform Factory V0.2 `RELEASE_CANDIDATE` est conceptuellement cohérente,
honnêtement bornée, et alignée sur la Constitution. Elle est légitime pour entrer en
cycle de patch. Elle n'est pas encore opérationnellement publiable comme factory
exécutable par des IAs en parallèle.

Aucune violation constitutionnelle directe n'a été détectée dans les 5 challenge reports.

Le cycle d'arbitrage a produit 8 corrections retenues, 3 points différés, et 3 points
soumis à décision humaine (PC-1, PC-2, PC-3). Les trois ont été tranchés par l'humain
le 2026-04-10 et sont intégrés dans cet arbitrage canonique.

---

## Décisions humaines actées (2026-04-10)

### PC-1 — Emplacement des projections dérivées

**Décision :** `docs/cores/platform_factory/projections/`

Raisonnement :
- Les projections sont des ressources de référence stables, partagées entre toutes les
  applications spécifiques futures — elles appartiennent à la couche factory, pas à un
  pipeline de travail.
- Elles ne peuvent pas être dans `docs/cores/current/` (zone des canoniques primaires).
- Elles ne peuvent pas être dans `work/` (éphémère, nettoyé après chaque cycle).
- `docs/cores/platform_factory/projections/` est stable, centralisé, accessible en
  lecture par tous les pipelines aval, clairement séparé des canoniques primaires.
- Règle absolue à inscrire dans l'architecture : aucune projection dérivée ne peut
  être déposée dans `docs/cores/current/`.

### PC-2 — Matrice constitutional_conformance

**Décision Question A :** Fichier séparé `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`,
référencé depuis `platform_factory_architecture.yaml` par un champ dédié.

Raisonnement :
- Approche granulaire maîtrisée : une IA d'audit peut charger uniquement ce fichier
  ciblé sans charger tout l'architecture.
- Cohérent avec le principe de séparation déjà appliqué (architecture / state).
- Taille estimée : ~100-120 lignes YAML pour ~12 invariants — gérable.

**Décision Question B :** Report de l'embarquement filtré dans les projections.

Critère de relance : non lié à un numéro de version, mais à la **maturité suffisante**,
definie comme : le mécanisme de génération de projections est outillé ET le premier
usage de projection comme contexte unique d'une IA est envisagé.

En attendant :
- Chaque projection inclut un champ `conformance_matrix_ref` pointant vers le fichier central.
- Le champ `usage_as_sole_context` est marqué `blocked` dans l'architecture jusqu'à ce
  que la maturité soit atteinte.
- Ce point doit ressortir automatiquement lors du prochain challenge si le mécanisme
  de génération de projections est outillé.

### PC-3 — Intégration manifest officiel

**Décision :** Intégration au manifest officiel via STAGE_08, gouvernée par le pipeline
factory. Patches pipeline appliqués le 2026-04-10 :
- `docs/pipelines/platform_factory/pipeline.md` Rule 3 : statut baseline clarifié.
- `docs/pipelines/platform_factory/STAGE_08_FACTORY_PROMOTE_CURRENT.md` : mise à jour
  manifest rendue explicite, obligatoire, tracée, avec solution transitoire si schema insuffisant.

Ces corrections sont hors cycle de patch canonique (STAGE_03). Le mini-patch state
(exit_condition blocker) reste dans le scope STAGE_03.

---

## Décisions consolidées

### ARB-01 — Ajouter runtime_policy_conformance dans minimum_validation_contract

- **Élément :** `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation :** `platform_factory_architecture.yaml`
- **Statut :** `retained_now`
- **Gravité :** critique
- **Consensus :** strong (5/5 rapports)
- **Justification :** sans cet axe, aucune application produite ne peut être certifiée
  constitutionnellement conforme. Une app peut passer toute la validation factory sans
  que ses invariants runtime (100% local, no-generation, no-AI-continuous) aient été vérifiés.
- **Dépendance :** aucune bloquante. Validator dédié différé (ARB-08).
- **Lieu :** architecture
- **Séquencement :** priorité 1

### ARB-02 — Ajouter constitutional_invariants_checked dans minimum_observability_contract

- **Élément :** `produced_application_minimum_contract.minimum_observability_contract.minimum_signals`
- **Localisation :** `platform_factory_architecture.yaml`
- **Statut :** `retained_now`
- **Gravité :** critique
- **Consensus :** strong
- **Justification :** corollaire direct de ARB-01. Sans signal d'observabilité correspondant,
  l'axe de validation serait déclaré mais non observable.
- **Dépendance :** ARB-01
- **Lieu :** architecture
- **Séquencement :** priorité 1, en même temps que ARB-01

### ARB-03 — Définir bootstrap_contract et reproducibility_fingerprints

- **Élément :** `runtime_entrypoint_contract.must_declare.bootstrap_contract` et
  `identity.required_blocks.reproducibility_fingerprints`
- **Localisation :** `platform_factory_architecture.yaml`
- **Statut :** `retained_now`
- **Gravité :** élevé
- **Consensus :** medium (fond convergent, formulation variable)
- **Justification :** termes imposés comme obligatoires dans le contrat minimal sans
  définition = obligation non implémentable par une IA.
- **Décision :**
  - `reproducibility_fingerprints` : définir à haut niveau dans l'architecture
    (empreinte canonique des artefacts sources + hash de version).
  - `bootstrap_contract` : marquer explicitement `TBD` avec condition de déblocage
    (lié à la future typologie runtime, encore ouverte).
- **Lieu :** architecture
- **Séquencement :** priorité 4

### ARB-04 — Résoudre emplacement_policy: TBD pour les projections dérivées

- **Élément :** `generated_projection_rules.emplacement_policy`
- **Localisation :** `platform_factory_architecture.yaml`
- **Statut :** `retained_now`
- **Gravité :** élevé
- **Consensus :** strong sur la nécessité, décision humaine PC-1 actée
- **Décision :** `docs/cores/platform_factory/projections/`
- **Règle à inscrire :** aucune projection dérivée ne peut être déposée dans
  `docs/cores/current/`.
- **Dépendance :** ARB-05
- **Lieu :** architecture
- **Séquencement :** priorité 2

### ARB-05 — Poser le protocole minimal des validated_derived_execution_projections

- **Élément :** `execution_projection_contract`, `generated_projection_rules`
- **Localisation :** `platform_factory_architecture.yaml`
- **Statut :** `retained_now` (principe minimal) + `deferred` (outillage complet)
- **Gravité :** critique → élevé après séquencement
- **Consensus :** strong
- **Champs minimaux obligatoires à ajouter dans l'architecture :**
  - `scope`
  - `sources_exact`
  - `version_fingerprint`
  - `validation_status`
  - `promotion_to_canonical_forbidden: true`
  - `usage_policy` (runtime/offsession)
  - `conformance_matrix_ref` (référence vers `constitutional_conformance_matrix.yaml`)
  - `usage_as_sole_context: blocked` (jusqu'à maturité suffisante — décision PC-2/B)
- **Dépendance :** ARB-04
- **Lieu :** architecture
- **Séquencement :** priorité 2

### ARB-06 — Aligner la sémantique RELEASE_CANDIDATE / baseline / manifest

- **Élément :** metadata des artefacts + pipeline Rule 3 + blocker manifest
- **Localisation :** `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, `pipeline.md`
- **Statut :** `retained_now` (partiellement appliqué hors cycle via patches PC-3)
- **Gravité :** élevé
- **Consensus :** strong
- **Décision :**
  1. Changer `status: RELEASE_CANDIDATE` → `status: CURRENT_BASELINE_UNDER_GOVERNANCE`
     dans les métadonnées des artefacts.
  2. Ajouter dans `platform_factory_state.yaml` une `exit_condition` au blocker
     `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` :
     *"Ce blocker est levé uniquement quand STAGE_08 complète sa première exécution
     formelle avec mise à jour du manifest officiel."*
  3. Rule 3 de `pipeline.md` : déjà patchée le 2026-04-10.
- **Lieu principal :** state (mini-patch dans STAGE_03) + architecture
- **Séquencement :** priorité 3

### ARB-07 — Recalibrer les capabilities_present surdéclarant la maturité

- **Élément :** `capabilities_present[PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED]`
  et `capabilities_present[PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED]`
- **Localisation :** `platform_factory_state.yaml`
- **Statut :** `retained_now`
- **Gravité :** élevé
- **Consensus :** strong
- **Décision :**
  - `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` → `capabilities_partial`
    avec description : validator absent, storage non décidé (résolu ARB-04),
    protocole de régénération manquant.
  - `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` → reste en `capabilities_present`
    mais avec wording précisant `intent only, not yet tooled execution framework`.
- **Dépendance :** ARB-05
- **Lieu :** state
- **Séquencement :** priorité 3

### ARB-08 — Matrice constitutional_conformance

- **Élément :** nouveau fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
  + champ `constitutional_conformance_matrix_ref` dans l'architecture
- **Localisation :** architecture (référence) + nouveau fichier dédié
- **Statut :** `retained_now`
- **Gravité :** élevé
- **Consensus :** medium (fond unanime, forme tranchée par décision humaine PC-2/A)
- **Décision :** fichier séparé référencé depuis l'architecture (approche granulaire
  maîtrisée). Structure minimale par invariant : `invariant_id`, `preuve_minimale`,
  `artefact_porteur`, `signal_observabilite`, `validator_attendu`.
- **Lieu :** nouveau fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
- **Séquencement :** priorité 2 (lié à ARB-01)

### ARB-09 — Clarifier la priorité LAUNCH_PROMPT vs companion prompt (STAGE_04, STAGE_06)

- **Élément :** pipeline stages 04 et 06
- **Localisation :** `pipeline.md`
- **Statut :** `retained_now`
- **Gravité :** modéré
- **Consensus :** medium
- **Décision :** ajouter une note dans le pipeline :
  *"Le `LAUNCH_PROMPT` est le contrat d'entrée opérateur. Le `companion prompt` est
  l'instruction métier IA. En cas de conflit : le `companion prompt` prime pour le
  contenu, le `LAUNCH_PROMPT` prime pour le format de sortie."*
- **Lieu :** pipeline
- **Séquencement :** priorité 5

---

## Points retenus

| ID | Sujet | Gravité | Lieu | Priorité |
|---|---|---|---|---|
| ARB-01 | Axe `runtime_policy_conformance` dans `minimum_validation_contract` | Critique | architecture | 1 |
| ARB-02 | Signal `constitutional_invariants_checked` dans `minimum_observability_contract` | Critique | architecture | 1 |
| ARB-08 | Fichier `constitutional_conformance_matrix.yaml` + référence architecture | Élevé | architecture + nouveau fichier | 2 |
| ARB-04 | Emplacement projections → `docs/cores/platform_factory/projections/` | Élevé | architecture | 2 |
| ARB-05 | Protocole minimal projections (champs obligatoires) | Élevé | architecture | 2 |
| ARB-06 | Statut `CURRENT_BASELINE_UNDER_GOVERNANCE` + exit_condition blocker | Élevé | state + architecture | 3 |
| ARB-07 | Recalibrage `capabilities_partial` | Élevé | state | 3 |
| ARB-03 | Définition `reproducibility_fingerprints` + bornage `bootstrap_contract` | Élevé | architecture | 4 |
| ARB-09 | Priorité prompts pipeline STAGE_04 et STAGE_06 | Modéré | pipeline | 5 |

---

## Points rejetés

Aucun finding des 5 challenge reports n'est rejeté.
Tous les problèmes soulevés ont une base explicite dans les artefacts ou dans le socle canonique.

---

## Points différés

| ID | Sujet | Condition de levée | Gravité |
|---|---|---|---|
| ARB-10 | Protocole multi-IA opérationnel (granularité, assemblage, résolution de conflit) | Première instance de travail multi-IA réel sur ce pipeline | Élevé |
| ARB-11 | Schémas détaillés (manifest, configuration, packaging, runtime typology) | Décision de passage à une version de maturité suffisante | Modéré |
| ARB-12 | Frontière probante factory / pipeline d'instanciation | Conception du premier pipeline d'instanciation domaine | Modéré |
| PC-2/B | Embarquement filtré de la matrice dans chaque projection | Maturité suffisante : mécanisme de génération outillé + premier usage comme contexte unique envisagé | Élevé |

**Note sur PC-2/B :** le critère de relance est la maturité opérationnelle, pas un numéro de version.
Ce point doit ressortir automatiquement lors du prochain challenge si le mécanisme de
génération de projections est outillé.

---

## Points hors périmètre factory

- Design du contenu de tout domaine spécifique.
- Runtime d'une application Learn-it particulière.
- Logique métier de feedback domaine.
- Définition du pipeline d'instanciation lui-même.

---

## Points sans consensus résolus par décision humaine

Les trois points sans consensus (PC-1, PC-2, PC-3) ont été soumis à discussion humaine
et tranchés le 2026-04-10. Ils sont intégrés dans les décisions ARB ci-dessus.
Aucun point sans consensus ne reste ouvert.

---

## Corrections à arbitrer avant patch (STAGE_03)

### Priorité 1 — Preuve constitutionnelle minimale (critique)

- ARB-01 : ajouter `runtime_policy_conformance` dans `minimum_validation_contract.minimum_axes`.
- ARB-02 : ajouter `constitutional_invariants_checked` dans `minimum_observability_contract.minimum_signals`.
- Périmètre : architecture uniquement. Validator différé.

### Priorité 2 — Matrice et projections dérivées (élevé)

- ARB-08 : créer `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
  avec structure minimale par invariant. Ajouter `constitutional_conformance_matrix_ref`
  dans l'architecture.
- ARB-04 : inscrire `emplacement_policy: docs/cores/platform_factory/projections/`
  dans l'architecture. Ajouter règle d'interdiction de dépôt dans `docs/cores/current/`.
- ARB-05 : ajouter les champs minimaux obligatoires dans `execution_projection_contract` :
  `scope`, `sources_exact`, `version_fingerprint`, `validation_status`,
  `promotion_to_canonical_forbidden: true`, `usage_policy`, `conformance_matrix_ref`,
  `usage_as_sole_context: blocked`.
- Périmètre : architecture + création nouveau fichier. Validator différé.

### Priorité 3 — Alignement sémantique et état (élevé)

- ARB-06 : changer `RELEASE_CANDIDATE` → `CURRENT_BASELINE_UNDER_GOVERNANCE`
  dans les métadonnées. Ajouter `exit_condition` au blocker
  `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`.
- ARB-07 : recalibrer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
  de `capabilities_present` vers `capabilities_partial`.
- Périmètre : state + architecture (metadata).

### Priorité 4 — Définition des termes non définis (élevé)

- ARB-03 : définir `reproducibility_fingerprints` à haut niveau dans l'architecture.
  Marquer `bootstrap_contract` comme `TBD` avec condition de déblocage explicite.

### Priorité 5 — Clarification pipeline (modéré)

- ARB-09 : ajouter note de priorité LAUNCH_PROMPT vs companion prompt
  dans les stages 04 et 06 du pipeline.

### Hors cycle STAGE_03 — Déjà appliqué

- PC-3 : patches `pipeline.md` Rule 3 et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`
  appliqués le 2026-04-10 via `tmp/`.

---

## Séquencement recommandé pour STAGE_03

1. ARB-01 + ARB-02 (critique, indépendants, localisés dans l'architecture).
2. ARB-08 + ARB-04 + ARB-05 (dépendance : ARB-04 avant ARB-05, ARB-08 indépendant).
3. ARB-06 + ARB-07 (cohérence state, indépendant de 1-2).
4. ARB-03 (modéré, non bloquant).
5. ARB-09 (modéré, pipeline uniquement).

---

## Répartition par lieu de correction (STAGE_03)

### platform_factory_architecture.yaml
- ARB-01 : ajout axe `runtime_policy_conformance`
- ARB-02 : ajout signal `constitutional_invariants_checked`
- ARB-03 : définition `reproducibility_fingerprints`, bornage `bootstrap_contract`
- ARB-04 : résolution `emplacement_policy` + règle d'interdiction
- ARB-05 : ajout champs obligatoires `execution_projection_contract`
- ARB-06 : changement statut metadata
- ARB-08 : ajout champ `constitutional_conformance_matrix_ref`

### platform_factory_state.yaml
- ARB-06 : exit_condition blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- ARB-07 : recalibrage capabilities

### docs/cores/platform_factory/constitutional_conformance_matrix.yaml (nouveau fichier)
- ARB-08 : création du fichier avec structure minimale par invariant

### pipeline.md
- ARB-09 : note de priorité prompts STAGE_04 et STAGE_06

### Validator/tooling (différé)
- ARB-01, ARB-02, ARB-05 : validators correspondants
- ARB-08 : validator de conformité constitutionnelle

### Hors périmètre factory
- Tout ce qui relève du domaine spécifique, du pipeline d'instanciation,
  du runtime d'une application particulière.
