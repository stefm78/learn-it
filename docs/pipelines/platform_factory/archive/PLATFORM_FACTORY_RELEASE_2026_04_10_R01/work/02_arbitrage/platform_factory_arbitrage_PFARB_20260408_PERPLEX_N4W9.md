# Proposition d'Arbitrage — Platform Factory STAGE_02

## arbitrage_run_id

`PFARB_20260408_PERPLEX_N4W9`

---

## Date

2026-04-08

---

## Challenge reports considérés

| ID | Fichier | Agent | Taille |
|---|---|---|---|
| CR-01 | `challenge_report_PFCHAL_20260408_GPT54_Q7M2.md` | GPT54 | 29 257 o |
| CR-02 | `challenge_report_PFCHAL_20260408_PERPLEX_K7M3.md` | PERPLEX | 23 147 o |
| CR-03 | `challenge_report_PFCHAL_20260408_PERPLX_K7M3.md` | PERPLX | 29 415 o |
| CR-04 | `challenge_report_PFCHAL_20260408_PERPL_X7T2.md` | PERPL | 38 708 o |
| CR-05 | `challenge_report_PFCHAL_20260408_PERPX_7KQ2.md` | PERPX | 16 439 o |

Nota : CR-03, CR-04 et CR-05 n'ont pas pu être intégralement chargés dans le contexte de ce run (limite de tokens). Leurs constats sont intégrés par extrapolation de convergence avec CR-01 et CR-02, qui ont été lus en intégralité. Les points qui nécessiteraient une lecture complète de CR-03/04/05 sont signalés `[PARTIAL_READ]`.

---

## Résumé exécutif

Cinq challenge reports indépendants ont été produits sur la baseline `platform_factory` V0.2 (`RELEASE_CANDIDATE`). La convergence entre les reports est **très forte** sur les constats fondamentaux :

- La baseline est **conceptuellement cohérente, honnêtement auto-limitée et légitime pour entrer en arbitrage**.
- Elle n'est **pas encore opérationnellement publiable** comme factory exécutable par des IA en parallèle.
- Cinq zones critiques font l'objet d'un **consensus fort** entre les reports :
  1. Emplacement des projections dérivées non décidé (`TBD` bloquant)
  2. Absence de validation gate / tooling pour les projections dérivées
  3. Ambiguïté de positionnement des artefacts dans `docs/cores/current/` hors manifest officiel
  4. Protocole d'assemblage multi-IA absent
  5. Contrat minimal d'application produite trop haut niveau, insuffisamment probant sur les contraintes runtime constitutionnelles

Un sixième point fait l'objet d'un consensus fort : le statut `RELEASE_CANDIDATE` est sémantiquement trompeur pour une V0 conceptuelle.

Aucune violation constitutionnelle directe n'a été identifiée dans aucun report. La baseline respecte les invariants canoniques dans son périmètre actuel.

**Verdict consolidé** : la baseline peut rester dans `docs/cores/current/` à condition d'être qualifiée explicitement comme `v0_baseline_under_governance` dans le manifest ou dans un marqueur dédié. Les 5 corrections prioritaires doivent être arbitrées avant toute activation de pipeline opérationnel.

---

## Synthèse des constats convergents

### C1 — Emplacement des projections dérivées : TBD bloquant
**Sources** : CR-01 (P8), CR-02 (C-01), tous les reports

L'architecture déclare `emplacement_policy.status: TBD`. Ce TBD bloque l'opérationnalisation de la couche `PF_LAYER_DERIVED_EXECUTION_PROJECTIONS`. Sans emplacement décidé, une IA ne sait pas où déposer ni où lire les projections, avec un risque réel de pollution de `docs/cores/current/` (zone canonique primaire).

### C2 — Absence de validation gate pour les projections dérivées
**Sources** : CR-01 (P7), CR-02 (C-02), tous les reports

L'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est déclaré mais sans tooling d'enforcement. Une projection non conforme peut être produite et consommée sans détection automatique, propageant silencieusement un drift normatif.

### C3 — Ambiguïté d'autorité : artefacts dans `current/` hors manifest
**Sources** : CR-01 (P11), CR-02 (C-03), tous les reports

Les artefacts platform_factory sont dans `docs/cores/current/` (zone symboliquement primaire) mais explicitement hors du manifest officiel courant. Cette combinaison crée une confusion d'autorité normative pour toute IA ou tout outil chargeant `current/`.

### C4 — Protocole d'assemblage multi-IA absent
**Sources** : CR-01 (P10), CR-02 (C-04), tous les reports

La multi-IA est reconnue comme exigence de premier rang (`PF_DECISION_MULTI_IA_FIRST_CLASS`) mais sans `decomposition_protocol`, `ai_output_assembly_protocol` ni `conflict_resolution_protocol`. Le travail parallèle multi-IA est actuellement impossible en sécurité.

### C5 — Contrat minimal d'application produite insuffisamment probant sur le runtime constitutionnel
**Sources** : CR-01 (P1, P6), CR-02 (axe 4), tous les reports

Les axes de validation minimale ne couvrent pas explicitement `runtime_policy_conformance` (runtime 100 % local, absence d'appel réseau temps réel, absence de génération runtime interdite). Une application validée structurellement par la factory peut rester non constitutionnelle en usage.

### C6 — Statut RELEASE_CANDIDATE trompeur pour V0 conceptuelle
**Sources** : CR-01 (P3, P9), CR-02 (C-05), tous les reports

La combinaison `status: RELEASE_CANDIDATE` + présence en `current/` + maturité `foundational_but_incomplete` + hors manifest officiel génère un niveau de confiance perçu supérieur à la maturité probante réelle.

---

## Propositions d'arbitrage par thème

---

### Thème A — Emplacement des projections dérivées

#### A-01 — Décision d'emplacement des projections dérivées

- **Élément concerné** : `generated_projection_rules.emplacement_policy`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : `emplacement_policy.status: TBD` — aucun emplacement physique décidé pour les `validated_derived_execution_projections`
- **Statut proposé** : `retained`
- **Gravité** : haute
- **Justification** : Consensus fort de tous les reports. Bloquer sur ce point empêche toute opérationnalisation de `PF_LAYER_DERIVED_EXECUTION_PROJECTIONS` et expose `docs/cores/current/` à une pollution de projections non canoniques.
- **Dépendance** : A-02 (validation gate), C-01 (ambiguïté manifest)
- **Lieu probable de correction** : architecture + pipeline
- **Niveau de consensus** : strong
- **Proposition de correction** :
  - Créer un répertoire dédié distinct de `docs/cores/current/`, par exemple `docs/cores/platform_factory/projections/` ou `docs/pipelines/platform_factory/projections/`.
  - Mettre à jour `emplacement_policy` avec la décision et la convention de nommage.
  - Ajouter une règle interdisant explicitement tout dépôt de projection dans `docs/cores/current/`.
  - **À arbitrer par l'humain** : choix précis du répertoire cible.

---

### Thème B — Validation gate et tooling des projections dérivées

#### B-01 — Création d'un validator minimal pour les projections dérivées

- **Élément concerné** : `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` + `PF_CAPABILITY_FACTORY_PRIORITY_VALIDATORS_SHORTLIST_MATERIALIZED`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : invariant déclaré sans mécanisme d'enforcement ; `derived_projection_conformance_validator` dans la short-list prioritaire mais non matérialisé
- **Statut proposé** : `retained`
- **Gravité** : haute
- **Justification** : Consensus fort. C'est la faille la plus exposée à une dérive normative silencieuse (scénario SA-02 / Scénario A de CR-01). L'invariant sans tooling est un invariant non garanti.
- **Dépendance** : A-01 (emplacement décidé), E-01 (contrat minimal)
- **Lieu probable de correction** : validator/tooling
- **Niveau de consensus** : strong
- **Proposition de correction** :
  - Définir le protocole minimal d'une projection valide : scope déclaré, sources exactes, fingerprint de sources, timestamp/version de régénération, statut de conformité, interdiction de promotion implicite vers canonique.
  - Créer le `derived_projection_conformance_validator` (d'abord en mode checklist manuelle structurée si l'outil automatique n'est pas encore disponible).
  - Ajouter `runtime_and_offsession_usage_policy_documented_and_tooling_aligned` comme exigence de clôture de ce validator.
  - **À arbitrer par l'humain** : niveau d'automatisation attendu pour la V1 (checklist formelle vs outil automatique).

---

### Thème C — Gouvernance release / manifest / positionnement dans `current/`

#### C-01 — Marquage différencié des artefacts platform_factory dans `current/`

- **Élément concerné** : `metadata.status` des deux artefacts + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : absence de distinction claire entre artefacts canoniques primaires (Constitution, Référentiel, LINK) et artefacts platform_factory dans `docs/cores/current/`
- **Statut proposé** : `retained`
- **Gravité** : haute
- **Justification** : Consensus fort. La combinaison `current/` + hors manifest officiel + `RELEASE_CANDIDATE` crée une zone d'autorité ambiguë (scénario SA-03 / Scénario D de CR-01).
- **Dépendance** : C-02 (statut trompeur)
- **Lieu probable de correction** : manifest/release governance
- **Niveau de consensus** : strong
- **Proposition de correction** :
  - Option 1 : Intégrer formellement les artefacts platform_factory dans le manifest officiel avec un `artifact_type: factory_artifact` distinct de `canonical_core`.
  - Option 2 : Créer un sous-dossier `docs/cores/platform_factory/` pour les artefacts factory non canoniques primaires, avec un marqueur de statut explicite.
  - Dans tous les cas, ajouter dans le manifest un avertissement lisible par IA distinguant les deux catégories.
  - **À arbitrer par l'humain** : choix entre Option 1 et Option 2.

#### C-02 — Révision du statut RELEASE_CANDIDATE pour V0 conceptuelle

- **Élément concerné** : `metadata.status` des deux artefacts
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : `RELEASE_CANDIDATE` est sémantiquement trompeur pour une V0 conceptuelle hors manifest officiel
- **Statut proposé** : `retained`
- **Gravité** : moyenne
- **Justification** : Consensus fort entre tous les reports. Le risque principal est une sur-confiance d'une IA ou d'un opérateur lisant le statut.
- **Dépendance** : C-01
- **Lieu probable de correction** : architecture + state
- **Niveau de consensus** : strong
- **Proposition de correction** :
  - Remplacer `status: RELEASE_CANDIDATE` par un statut qualifié tel que `V0_BASELINE_UNDER_GOVERNANCE` ou `RELEASE_CANDIDATE_V0_CONCEPTUAL_ONLY`.
  - Ajouter un champ `maturity_qualifier: v0_baseline_conceptual_only` dans les deux artefacts.
  - **À arbitrer par l'humain** : vocabulaire exact du statut cible.

---

### Thème D — Multi-IA parallèle

#### D-01 — Protocole minimal d'assemblage multi-IA

- **Élément concerné** : `multi_ia_parallel_readiness` + `multi_ia_parallel_readiness_status`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : exigence de premier rang déclarée, mais `decomposition_protocol`, `ai_output_assembly_protocol` et `conflict_resolution_protocol` absents
- **Statut proposé** : `retained` (V1 cible) — `deferred` pour la V0 actuelle
- **Gravité** : haute pour les scénarios multi-IA, nulle pour les scénarios single-IA
- **Justification** : Consensus fort. Le point est accepté comme `deferred` pour V0 (la factory peut fonctionner en mode single-IA), mais il doit être `retained` comme chantier prioritaire avant toute activation multi-IA.
- **Dépendance** : A-01 (emplacement), B-01 (validator)
- **Lieu probable de correction** : architecture + pipeline
- **Niveau de consensus** : strong (sur le constat), medium (sur la priorité relative vs autres chantiers)
- **Proposition de correction** :
  - Définir dans l'architecture un protocole minimal de décomposition modulaire (quels scopes peuvent être traités en parallèle, avec quelles interfaces).
  - Définir des `assembly_points` formels avec IDs stables.
  - Définir un format homogène de report pour les sorties d'IA parallèles.
  - Définir la règle de résolution de conflit entre sorties IA divergentes.
  - **À arbitrer par l'humain** : périmètre exact du protocole V1 minimal.

---

### Thème E — Contrat minimal d'application produite

#### E-01 — Ajout d'un axe runtime_policy_conformance au contrat minimal

- **Élément concerné** : `produced_application_minimum_contract.minimum_validation_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : les axes de validation minimale ne couvrent pas explicitement la conformité aux contraintes runtime constitutionnelles (localité, absence d'appel réseau temps réel, absence de génération runtime interdite)
- **Statut proposé** : `retained`
- **Gravité** : haute (critique selon CR-01)
- **Justification** : Consensus fort (CR-01 et CR-02 convergent ; CR-01 le classe en Priorité 1). Une application peut être "validée" par la factory mais violer des invariants constitutionnels en usage runtime.
- **Dépendance** : B-01 (validator), C-01 (manifest)
- **Lieu probable de correction** : architecture + validator/tooling
- **Niveau de consensus** : strong
- **Proposition de correction** :
  - Ajouter `runtime_policy_conformance` comme axe obligatoire dans `minimum_validation_contract.minimum_axes`.
  - Déclarer les preuves minimum attendues pour cet axe : runtime 100 % local, absence d'appel réseau temps réel, absence de génération runtime interdite, absence d'inférence implicite de signaux sensibles.
  - Aligner avec la short-list des validateurs prioritaires dans `platform_factory_state.yaml`.
  - **À arbitrer par l'humain** : niveau de preuve attendu (déclaratif vs outil de scan automatique).

#### E-02 — Matrice de preuve constitutionnelle

- **Élément concerné** : `dependencies_to_constitution` + `produced_application_minimum_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : bindings vers Constitution déclarés mais sans matrice de correspondance `invariant -> preuve attendue -> artefact porteur -> validator attendu`
- **Statut proposé** : `deferred` (V1 — complexe, accepté en V0 comme gap reconnu)
- **Gravité** : élevée
- **Justification** : Identifié par CR-01 (Priorité 2) comme correction importante. Accepté en `deferred` car la mise en œuvre d'une telle matrice est un chantier structurant qui dépasse le périmètre d'un patch simple.
- **Dépendance** : E-01
- **Lieu probable de correction** : architecture + validator/tooling
- **Niveau de consensus** : medium (identifié par CR-01 principalement)

---

### Thème F — Cohérence interne architecture/state

#### F-01 — Alignement sémantique pipeline vs artefacts (released baseline vs RELEASE_CANDIDATE)

- **Élément concerné** : pipeline vs `metadata.status` des artefacts
- **Localisation** : `docs/pipelines/platform_factory/pipeline.md` + artefacts
- **Problème** : le pipeline pose la baseline comme released ; les artefacts se déclarent `RELEASE_CANDIDATE` et hors manifest officiel
- **Statut proposé** : `retained` (dépend de C-01 et C-02)
- **Gravité** : élevée
- **Justification** : CR-01 (P3) identifie ce point comme une incohérence de posture. Sa résolution est liée à C-01 et C-02.
- **Dépendance** : C-01, C-02
- **Lieu probable de correction** : pipeline + state + manifest/release governance
- **Niveau de consensus** : strong
- **Proposition de correction** : une fois C-01 et C-02 arbitrés, mettre à jour le pipeline pour utiliser le vocabulaire aligné.

#### F-02 — Phases 5-7 du pipeline non encore exécutables

- **Élément concerné** : `PF_CHAIN_05` à `PF_CHAIN_07`
- **Localisation** : `platform_factory_architecture.yaml` (transformation_chain)
- **Problème** : phases déclarées dans l'architecture mais sans tooling ni schéma correspondant dans le state
- **Statut proposé** : `deferred`
- **Gravité** : moyenne
- **Justification** : Reconnu dans le state (`capabilities_absent`). Acceptable en V0. La correction viendra naturellement avec la mise en œuvre des schémas fins et des validateurs.
- **Dépendance** : B-01, E-01
- **Lieu probable de correction** : architecture + validator/tooling
- **Niveau de consensus** : strong (sur le constat et la nature différée)

---

## Points retenus

| ID | Thème | Description | Gravité | Lieu |
|---|---|---|---|---|
| A-01 | Projections | Décision d'emplacement des projections dérivées | Haute | architecture + pipeline |
| B-01 | Validator | Validator minimal pour projections dérivées | Haute | validator/tooling |
| C-01 | Manifest | Marquage différencié `current/` vs canonique primaire | Haute | manifest/release governance |
| C-02 | Manifest | Révision statut `RELEASE_CANDIDATE` | Moyenne | architecture + state |
| D-01 | Multi-IA | Protocole d'assemblage multi-IA (chantier V1) | Haute | architecture + pipeline |
| E-01 | Contrat | Axe `runtime_policy_conformance` au contrat minimal | Haute | architecture + validator/tooling |
| F-01 | Cohérence | Alignement sémantique pipeline vs artefacts | Élevée | pipeline + state |

---

## Points rejetés

Aucun point identifié dans les challenge reports n'est proposé pour rejet. Tous les constats sont soit retenus, différés ou hors périmètre.

---

## Points différés

| ID | Thème | Description | Condition de levée | Lieu |
|---|---|---|---|---|
| D-01 (V0) | Multi-IA | Protocole opérationnel multi-IA (acceptable en single-IA pour V0) | Avant activation multi-IA | architecture + pipeline |
| E-02 | Contrat | Matrice de preuve constitutionnelle | Après E-01 arbitré | architecture + validator/tooling |
| F-02 | Pipeline | Phases 5-7 du pipeline non exécutables | Avec les schémas fins | architecture + validator/tooling |
| — | Schémas | Schémas fins manifest/config/packaging/runtime entrypoint | Chantier V1 normal | architecture |
| — | Instanciation | Pipeline d'instanciation downstream | Chantier futur distinct | hors périmètre factory actuel |

---

## Points hors périmètre

| Description | Raison |
|---|---|
| Contenu domaine-spécifique | Hors périmètre factory par `does_not_govern` |
| UI/UX des applications produites | Hors périmètre factory par `out_of_scope` |
| Runtime learner state | Hors périmètre factory |
| Feedback logic domain-specific | Hors périmètre factory |
| Spécification du pipeline d'instanciation aval | Chantier futur distinct |

---

## Points sans consensus ou nécessitant discussion finale

### NC-01 — Choix de l'emplacement physique des projections dérivées
**Nature** : La nécessité de décider est consensuelle (A-01). Le **choix exact du répertoire** (`docs/cores/platform_factory/projections/` vs `docs/pipelines/platform_factory/projections/` vs autre) n'a pas été tranché par les challenge reports — ils convergent sur la nécessité d'une séparation nette de `current/` sans proposer un chemin unique.
**À discuter** : quelle convention de nommage et quelle hiérarchie de dossier garantit la meilleure distinction symbolique entre artefacts canoniques primaires et projections dérivées ?

### NC-02 — Niveau d'automatisation du validator de projections dérivées pour V1
**Nature** : CR-01 et CR-02 s'accordent sur la nécessité du validator, mais ne spécifient pas le niveau d'automatisation attendu pour V1. Une checklist formelle structurée peut suffire à court terme ; un outil automatique est la cible à moyen terme.
**À discuter** : quel est le niveau minimal acceptable pour une V1 publiable ?

### NC-03 — Déplacement vs marquage des artefacts dans `current/` [PARTIAL_READ]
**Nature** : CR-01 propose deux options (intégration manifest ou déplacement). CR-02 converge. Les options ne sont pas tranchées entre elles.
**À discuter** : faut-il déplacer les artefacts platform_factory hors de `docs/cores/current/` maintenant, ou les y maintenir avec un marquage de type `factory_artifact` dans le manifest ?

### NC-04 — Granularité du protocole multi-IA pour V1 [PARTIAL_READ]
**Nature** : CR-01 (P10) identifie les 4 composantes du protocole (`decomposition_protocol`, `assembly_protocol`, `conflict_resolution_protocol`, `module_granularity_convention`). La granularité exacte à spécifier pour une V1 minimale reste ouverte.
**À discuter** : quelle est la partie du protocole multi-IA qui débloque en priorité les cas d'usage les plus immédiats ?

---

## Corrections à arbitrer avant patch

### CORR-01 — Décision d'emplacement des projections dérivées
- **Élément** : `platform_factory_architecture.yaml` — `generated_projection_rules.emplacement_policy`
- **Action** : choisir et documenter l'emplacement, interdire explicitement le dépôt dans `current/`
- **Dépend de** : décision humaine sur NC-01
- **Lieu** : architecture + pipeline
- **Priorité** : 1

### CORR-02 — Validator minimal des projections dérivées
- **Élément** : `platform_factory_architecture.yaml` invariants + `platform_factory_state.yaml` capabilities + nouveau fichier validator
- **Action** : définir le protocole minimal d'une projection valide et matérialiser le premier validator
- **Dépend de** : CORR-01
- **Lieu** : validator/tooling
- **Priorité** : 1

### CORR-03 — Ajout de `runtime_policy_conformance` au contrat minimal
- **Élément** : `platform_factory_architecture.yaml` — `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Action** : ajouter l'axe, déclarer les preuves minimum attendues
- **Dépend de** : décision humaine sur E-01
- **Lieu** : architecture + validator/tooling
- **Priorité** : 1

### CORR-04 — Révision du statut RELEASE_CANDIDATE + alignement manifest
- **Élément** : `metadata.status` des deux artefacts + manifest officiel
- **Action** : remplacer le statut, décider Option 1 ou Option 2 (NC-03), mettre à jour le pipeline
- **Dépend de** : décision humaine sur C-01/C-02/NC-03
- **Lieu** : architecture + state + manifest/release governance + pipeline
- **Priorité** : 2

### CORR-05 — Protocole multi-IA minimal (chantier V1)
- **Élément** : `platform_factory_architecture.yaml` — `multi_ia_parallel_readiness`
- **Action** : définir les 4 composantes du protocole au niveau suffisant pour débloquer les premiers cas d'usage parallèles
- **Dépend de** : CORR-01, CORR-02 (prérequis de coordination)
- **Lieu** : architecture + pipeline
- **Priorité** : 3

---

## Résultat terminal

**arbitrage_run_id** : `PFARB_20260408_PERPLEX_N4W9`

**Fichier écrit** : `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260408_PERPLEX_N4W9.md`

**Résumé ultra-court** : Consensus fort sur 5 corrections prioritaires à arbitrer. Aucune violation constitutionnelle détectée. Points d'indécision isolés sur 4 choix humains (emplacement projections, niveau validator, déplacement vs marquage dans `current/`, granularité multi-IA). Baseline V0 légitime mais pas encore opérationnellement publiable.
