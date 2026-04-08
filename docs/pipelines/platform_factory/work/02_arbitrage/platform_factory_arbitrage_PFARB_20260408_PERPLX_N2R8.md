# Proposition d'arbitrage — Platform Factory Baseline V0.2

**arbitrage_run_id :** `PFARB_20260408_PERPLX_N2R8`  
**Date :** 2026-04-08  
**IA :** PERPLX (Perplexity / Claude Sonnet)  
**Stage :** STAGE_02_FACTORY_ARBITRAGE  
**Pipeline :** `docs/pipelines/platform_factory/pipeline.md`

> **Note :** Cette proposition est une contribution indépendante destinée à la consolidation finale humaine-assistée. Elle ne constitue pas l'arbitrage canonique final du stage.

---

## Challenge reports considérés

| ID | IA | Taille | Socle canonique lu |
|---|---|---|---|
| `PFCHAL_20260408_GPT54_Q7M2` | GPT-4 | 29 257 oct. | Constitution + Référentiel + LINK + pipeline |
| `PFCHAL_20260408_PERPLEX_K7M3` | Perplexity (run précédent) | 23 147 oct. | Constitution (Référentiel + LINK non chargés) |
| `PFCHAL_20260408_PERPLX_K7M3` | Perplexity (ce run) | 29 415 oct. | Constitution (Référentiel + LINK non chargés) |
| `PFCHAL_20260408_PERPL_X7T2` | Perplexity (run long) | 38 708 oct. | À lire — non chargé dans ce run d'arbitrage |
| `PFCHAL_20260408_PERPX_7KQ2` | Perplexity (run court) | 16 439 oct. | À lire — non chargé dans ce run d'arbitrage |

> **Note de run :** Les rapports `PERPL_X7T2` et `PERPX_7KQ2` n'ont pas été chargés dans ce run d'arbitrage (limite de tokens). Les constats issus de `GPT54_Q7M2`, `PERPLEX_K7M3` et `PERPLX_K7M3` couvrent déjà une surface de convergence forte. Les deux rapports non lus devront être intégrés lors de la consolidation finale. Tout point qui n'apparaît que dans ces deux rapports sera donc absent de la présente proposition — ce fait est signalé explicitement.

---

## Résumé exécutif

Les trois rapports lus convergent sur un diagnostic commun clair : la Platform Factory V0.2 est **fondatrice, honnête dans son auto-évaluation, et légitime à entrer en cycle de correction**, mais elle n'est **pas encore probante** sur les dimensions les plus critiques.

Quatre zones de risque font consensus fort à travers tous les rapports lus :

1. **Le contrat minimal d'application produite ne vérifie pas les invariants constitutionnels runtime** — une application peut paraître conforme sans que son runtime local, son absence de génération et la gestion off-session de ses patches aient été vérifiés.
2. **Le mécanisme de `validated_derived_execution_projections` est déclaré opérationnel en principe mais non instrumenté** — pas de validateur, pas d'emplacement, pas de protocole de régénération : activable prématurément avec risque de dérive normative silencieuse.
3. **La gouvernance release est hybride et non fermée** — artefacts dans `docs/cores/current/` mais hors manifest officiel, sans critère de promotion, avec un vocabulaire contradictoire entre pipeline et artefacts.
4. **La readiness multi-IA est une exigence déclarée, non une capacité opérable** — protocole de décomposition, d'assemblage, de résolution de conflit absents.

Les lacunes restantes (schémas fins, typologies, outillage détaillé) sont des manques V0 normaux et acceptables tant qu'ils restent reconnus et bornés.

Le chantier prioritaire avant patch n'est pas d'élargir le périmètre de la factory, mais de **fermer la preuve constitutionnelle**, **fermer la gouvernance des projections dérivées**, et **fermer la sémantique release/current/manifest**.

---

## Synthèse des constats convergents

### C-01 — Contrat minimal non probant sur les invariants runtime constitutionnels
**Présent dans :** GPT54_Q7M2 (critique, Problème 1), PERPLEX_K7M3 (critique, CC-01 à CC-05), PERPLX_K7M3 (critique, R-01, C-01)  
**Formulation convergente :** Le `minimum_validation_contract` couvre structure, traceability, packaging et conformité au contrat — mais aucun axe ne porte sur la vérification des invariants constitutionnels runtime critiques : `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.  
**Niveau de consensus :** **fort**

### C-02 — Mécanisme de projections dérivées non instrumenté
**Présent dans :** GPT54_Q7M2 (critique, Problèmes 7 et 8), PERPLEX_K7M3 (élevé, R-02), PERPLX_K7M3 (élevé, R-02, C-02)  
**Formulation convergente :** Le principe du mécanisme est solide et bien déclaré (`no_new_rule`, `no_normative_divergence`, etc.), mais les opérationnalisations manquantes sont identiques dans tous les rapports : validator, protocole de régénération, emplacement de stockage, politique d'usage runtime/off-session.  
**Niveau de consensus :** **fort**

### C-03 — Gouvernance release/current/manifest non fermée
**Présent dans :** GPT54_Q7M2 (critique, Problème 11 + élevé Problème 3), PERPLEX_K7M3 (élevé, R-03), PERPLX_K7M3 (élevé, R-03, C-03)  
**Formulation convergente :** Les artefacts V0.2 sont dans `docs/cores/current/` avec statut `RELEASE_CANDIDATE` mais hors manifest officiel courant. Le pipeline les traite comme released. Cette contradiction crée un risque d'autorité ambiguë, d'usage prématuré comme canonique, et de traçabilité brisée.  
**Niveau de consensus :** **fort**

### C-04 — Multi-IA readiness : exigence reconnue, capacité non opérable
**Présent dans :** GPT54_Q7M2 (élevé, Problème 10), PERPLEX_K7M3 (modéré, R-05), PERPLX_K7M3 (modéré, R-05, Axe 7)  
**Formulation convergente :** Les cinq principes multi-IA (`bounded_scope`, `stable_identifiers`, `explicit_dependencies`, `clear_assembly_points`, `homogeneous_reports`) sont déclarés mais non instrumentés. Il manque : protocole de décomposition, protocole d'assemblage, résolution de conflit, convention de granularité modulaire.  
**Niveau de consensus :** **fort**

### C-05 — Contrat minimal trop haut niveau pour être probant
**Présent dans :** GPT54_Q7M2 (élevé, Problème 6), PERPLX_K7M3 (Axe 4)  
**Formulation convergente :** Les blocs du contrat minimal (identity, manifest, runtime entrypoint, configuration, packaging, validation, observabilité) sont bien identifiés mais restent intentionnels. Les fingerprints de reproductibilité, les preuves de dépendances canoniques, et la déclaration de politique runtime ne sont pas exigés comme éléments probants obligatoires.  
**Niveau de consensus :** **moyen** (présent dans 2/3 rapports lus)

### C-06 — Vocabulaire contradictoire released/RELEASE_CANDIDATE
**Présent dans :** GPT54_Q7M2 (élevé, Problème 3 + Problème 4), PERPLX_K7M3 (implicite via R-03)  
**Formulation convergente :** Le pipeline pose les artefacts comme baseline released. Les artefacts eux-mêmes se déclarent `RELEASE_CANDIDATE`. L'état reconnaît une présence hors manifest. Ces trois positions sont incohérentes entre elles.  
**Niveau de consensus :** **moyen**

### C-07 — Frontière factory/pipeline d'instanciation non instrumentée
**Présent dans :** GPT54_Q7M2 (modéré, Problème 5), PERPLX_K7M3 (modéré, R-04, Axe 3)  
**Formulation convergente :** La frontière est bien déclarée en intention (`does_not_govern`, `out_of_scope`, `forbidden_variability`), mais aucun mécanisme de détection de franchissement n'existe dans la `transformation_chain`.  
**Niveau de consensus :** **moyen**

### C-08 — Evidence du state circulaire
**Présent dans :** PERPLX_K7M3 (faible, R-07), PERPLEX_K7M3 (implicite)  
**Formulation convergente :** Les deux éléments d'evidence du state pointent vers les artefacts eux-mêmes. Ce n'est pas une preuve externe de validation.  
**Niveau de consensus :** **faible** (présent dans 2/3 mais comme point secondaire)

---

## Propositions d'arbitrage par thème

---

### Thème 1 — Conformité constitutionnelle du contrat minimal

#### ARB-01 — Ajouter un axe `runtime_policy_conformance` dans le contrat minimal d'application produite

| Champ | Valeur |
|---|---|
| **Élément concerné** | `produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Aucun axe ne vérifie les invariants constitutionnels runtime critiques. Une application peut être structurellement valide mais violer `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`. |
| **Statut proposé** | **retained** |
| **Gravité** | critique |
| **Justification** | Consensus fort (3/3 rapports lus). L'absence de cet axe permet une fausse conformité constitutionnelle. C'est le risque le plus direct sur l'intégrité normative du dispositif. |
| **Dépendance** | ARB-05 (validator) |
| **Lieu probable de correction** | architecture |
| **Niveau de consensus** | strong |

#### ARB-02 — Déclarer une matrice de correspondance invariant → preuve attendue → artefact porteur

| Champ | Valeur |
|---|---|
| **Élément concerné** | `dependencies_to_constitution` + `produced_application_minimum_contract` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Les dépendances constitutionnelles sont nommées mais sans binding probant. Les invariants ne sont pas reliés à des preuves attendues dans le manifest, la configuration ou la validation. |
| **Statut proposé** | **retained** |
| **Gravité** | élevé |
| **Justification** | Présent dans GPT54 (Problème 2). Renforce directement la vérifiabilité de ARB-01. Sans cette matrice, l'axe `runtime_policy_conformance` reste creux. |
| **Dépendance** | ARB-01 |
| **Lieu probable de correction** | architecture |
| **Niveau de consensus** | medium |

---

### Thème 2 — Mécanisme des projections dérivées

#### ARB-03 — Définir un protocole minimal obligatoire pour toute `validated_derived_execution_projection`

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.execution_projection_contract` + `generated_projection_rules` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Le principe est solide mais le mécanisme est non instrumenté : pas de validator, pas de protocole de régénération, pas de politique d'usage runtime/off-session. Une projection non validée activable comme unique contexte IA = risque de dérive normative silencieuse. |
| **Statut proposé** | **retained** |
| **Gravité** | critique |
| **Justification** | Consensus fort (3/3). Identificateur de risque systémique : c'est le point d'entrée le plus exposé à la perte de fidélité normative. |
| **Dépendance** | ARB-04 (emplacement), ARB-05 (validator) |
| **Lieu probable de correction** | architecture + validator/tooling |
| **Niveau de consensus** | strong |

#### ARB-04 — Arrêter l'emplacement de stockage des projections dérivées

| Champ | Valeur |
|---|---|
| **Élément concerné** | `generated_projection_rules.emplacement_policy` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | L'emplacement est explicitement `TBD`. Le risque : projections stockées dans `docs/cores/current/` ou dans un espace non gouverné, avec risque de confusion d'autorité ou d'obsolescence silencieuse. |
| **Statut proposé** | **retained** |
| **Gravité** | élevé |
| **Justification** | Présent dans GPT54 (Problème 8) et PERPLX (Axe 5). La bonne séparation entre canonique, outputs de pipeline et projections de travail IA est une condition de gouvernance non négociable. |
| **Dépendance** | ARB-03 |
| **Lieu probable de correction** | architecture + manifest/release governance |
| **Niveau de consensus** | strong |

#### ARB-05 — Conditionner l'activation des projections comme unique contexte IA à l'existence d'un validateur minimal

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.execution_projection_contract` / activation condition |
| **Localisation** | `platform_factory_architecture.yaml` + state |
| **Problème** | Le principe "une projection peut être l'unique artefact fourni à une IA" est dangereux à activer sans validateur. Deux options : gate d'activation formelle, ou déclaration explicite "usage non garanti tant que validateur absent". |
| **Statut proposé** | **retained** (arbitrage sur l'option à retenir : gate vs déclaration) |
| **Gravité** | élevé |
| **Justification** | Présent dans PERPLX (C-02) et GPT54 (implicite Problème 7). Sans cette décision, toute IA peut utiliser une projection non validée avec une fausse impression de conformité. |
| **Dépendance** | ARB-03 |
| **Lieu probable de correction** | architecture |
| **Niveau de consensus** | medium — la question porte sur l'option (gate vs déclaration), pas sur la nécessité |

---

### Thème 3 — Gouvernance release / current / manifest

#### ARB-06 — Résoudre la contradiction released/RELEASE_CANDIDATE entre pipeline et artefacts

| Champ | Valeur |
|---|---|
| **Élément concerné** | `metadata.status` (artefacts) vs doctrine pipeline |
| **Localisation** | `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, `pipeline.md` |
| **Problème** | Le pipeline traite les artefacts comme baseline released. Les artefacts se déclarent `RELEASE_CANDIDATE`. L'état indique une présence hors manifest officiel. Ces trois positions sont incohérentes. |
| **Statut proposé** | **retained** |
| **Gravité** | élevé |
| **Justification** | Présent dans GPT54 (Problème 3) et implicite dans PERPLX (R-03). Risque immédiat d'ingestion non gouvernée par une IA. |
| **Dépendance** | ARB-07 |
| **Lieu probable de correction** | state + architecture + pipeline + manifest/release governance |
| **Niveau de consensus** | strong |

#### ARB-07 — Matérialiser un signal de gouvernance externe pour "present in current but not officially integrated"

| Champ | Valeur |
|---|---|
| **Élément concerné** | Présence dans `docs/cores/current/` hors manifest officiel |
| **Localisation** | `platform_factory_state.yaml` metadata + gouvernance repo |
| **Problème** | La distinction "present in current" vs "officially integrated in manifest" n'est visible que dans les `notes` du metadata. Une IA lisant `docs/cores/current/` peut considérer ces artefacts comme faisant partie du socle canonique officiel. Il n'existe pas de signal de gouvernance structurel. |
| **Statut proposé** | **retained** |
| **Gravité** | critique |
| **Justification** | Consensus fort (3/3). C'est le risque de gouvernance le plus immédiat. Un fichier de statut dédié, une entrée dans un registry de factory, ou une note structurée dans le pipeline devrait matérialiser cette distinction. |
| **Dépendance** | ARB-06 |
| **Lieu probable de correction** | manifest/release governance |
| **Niveau de consensus** | strong |

#### ARB-08 — Définir des critères de promotion RELEASE_CANDIDATE → released/manifested

| Champ | Valeur |
|---|---|
| **Élément concerné** | Cycle de vie des artefacts platform_factory |
| **Localisation** | `platform_factory_state.yaml` + `pipeline.md` |
| **Problème** | Aucun critère de promotion n'est défini. La progression vers une release officielle est opaque. |
| **Statut proposé** | **retained** |
| **Gravité** | élevé |
| **Justification** | Présent dans GPT54 (Priorité 3). Sans critères explicites, la promotion peut rester indéfiniment implicite. |
| **Dépendance** | ARB-07 |
| **Lieu probable de correction** | pipeline + manifest/release governance |
| **Niveau de consensus** | medium |

---

### Thème 4 — Multi-IA en parallèle

#### ARB-09 — Définir un protocole minimal de décomposition modulaire, d'assemblage et de résolution de conflit

| Champ | Valeur |
|---|---|
| **Élément concerné** | `multi_ia_parallel_readiness` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Les cinq principes multi-IA sont déclarés mais non instrumentés. Absence : protocole de décomposition, protocole d'assemblage, résolution de conflit, convention de granularité modulaire, format homogène de report. |
| **Statut proposé** | **retained** (avec temporalité différée acceptable V0) |
| **Gravité** | modéré |
| **Justification** | Consensus fort (3/3). Risque opérationnel réel dès que plusieurs IA travaillent en parallèle. Peut être différé temporellement par rapport aux critiques, mais doit être borné dans le temps. |
| **Dépendance** | ARB-03, ARB-04 |
| **Lieu probable de correction** | architecture + pipeline |
| **Niveau de consensus** | strong |

---

### Thème 5 — Chaîne de transformation et pipeline

#### ARB-10 — Bloquer PF_CHAIN_06 tant que le validator est absent

| Champ | Valeur |
|---|---|
| **Élément concerné** | `transformation_chain.PF_CHAIN_06_VALIDATE_APPLICATION_MIN_CONTRACT` |
| **Localisation** | `platform_factory_architecture.yaml` + pipeline |
| **Problème** | `PF_CHAIN_06` suppose un validator qui n'existe pas encore. La phase est en pratique non exécutable de façon déterministe. |
| **Statut proposé** | **retained** |
| **Gravité** | modéré |
| **Justification** | Présent dans PERPLX (Axe 9) et GPT54 (Priorité 5). Sans bloquer cette phase explicitement, une IA peut l'exécuter par jugement, annulant le déterminisme exigé. |
| **Dépendance** | ARB-05 |
| **Lieu probable de correction** | pipeline + validator/tooling |
| **Niveau de consensus** | medium |

#### ARB-11 — Ajouter un mécanisme de détection de franchissement frontière générique/spécifique

| Champ | Valeur |
|---|---|
| **Élément concerné** | `transformation_chain` + `variant_governance.forbidden_variability` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | La frontière est déclarée mais aucun mécanisme ne détecte son franchissement. Un contenu domaine peut être introduit dans un module générique sans signal. |
| **Statut proposé** | **retained** (différable après ARB-01, ARB-03) |
| **Gravité** | modéré |
| **Justification** | Présent dans PERPLX (R-04) et GPT54 (Problème 5). Risque structurel à long terme. |
| **Dépendance** | ARB-01, ARB-03 |
| **Lieu probable de correction** | architecture + validator/tooling |
| **Niveau de consensus** | medium |

---

### Thème 6 — Maturité et preuves du state

#### ARB-12 — Distinguer "intent declared" et "operationally present" dans les capabilities_present

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present` (notamment `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`) |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Classer une capacité comme "present" alors qu'elle n'est que définie en intention peut induire une maturité perçue supérieure à la maturité probante réelle. |
| **Statut proposé** | **retained** |
| **Gravité** | faible |
| **Justification** | Présent dans PERPLX (R-08) et GPT54 (Problème 9). Correction de wording à faible coût, impact sur la fiabilité du state comme signal de maturité. |
| **Dépendance** | aucune |
| **Lieu probable de correction** | state |
| **Niveau de consensus** | medium |

#### ARB-13 — Reconnaître explicitement le caractère circulaire des evidences actuelles

| Champ | Valeur |
|---|---|
| **Élément concerné** | `evidence` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Les deux éléments d'evidence pointent vers les artefacts eux-mêmes. Ce n'est pas une preuve externe de validation. |
| **Statut proposé** | **retained** (correction de wording) |
| **Gravité** | faible |
| **Justification** | Présent dans PERPLX (R-07). Le state doit reconnaître explicitement que les preuves disponibles sont auto-référentielles à ce stade. |
| **Dépendance** | aucune |
| **Lieu probable de correction** | state |
| **Niveau de consensus** | weak |

---

## Points retenus

| ID | Thème | Gravité | Consensus |
|---|---|---|---|
| ARB-01 | Axe `runtime_policy_conformance` dans contrat minimal | critique | strong |
| ARB-03 | Protocole minimal projections dérivées | critique | strong |
| ARB-07 | Signal de gouvernance "present not integrated" | critique | strong |
| ARB-02 | Matrice invariant → preuve → artefact | élevé | medium |
| ARB-04 | Emplacement stockage projections | élevé | strong |
| ARB-05 | Condition d'activation projections comme unique contexte IA | élevé | medium |
| ARB-06 | Résolution contradiction released/RELEASE_CANDIDATE | élevé | strong |
| ARB-08 | Critères de promotion RELEASE_CANDIDATE → released | élevé | medium |
| ARB-09 | Protocole minimal multi-IA (avec temporalité différable) | modéré | strong |
| ARB-10 | Bloquer PF_CHAIN_06 sans validator | modéré | medium |
| ARB-11 | Détection franchissement frontière générique/spécifique | modéré | medium |
| ARB-12 | Wording capabilities_present | faible | medium |
| ARB-13 | Reconnaissance circularité evidences | faible | weak |

---

## Points rejetés

Aucun point des challenge reports lus n'est proposé au rejet. Les challenge reports sont cohérents et leurs critiques sont ancrées dans les artefacts. Aucune critique ne repose sur une interprétation hors périmètre factory ou sur un standard non applicable à une V0.

---

## Points différés

| Point | Justification du report | Condition de retour |
|---|---|---|
| Schémas YAML fins (manifest, configuration, packaging) | Manques V0 normaux, explicitement reconnus | Dès que ARB-01 et ARB-03 sont traités |
| Granularité optimale multi-IA | Différable après protocole minimal ARB-09 | Avant premières sessions multi-IA réelles |
| Typologies fines runtime entrypoint | Acceptable V0, sans risque immédiat | Dès que ARB-01 et ARB-05 sont stabilisés |
| Tooling complet de validation | Attendu V0 | Priorité à la short-list validators (ARB-05, ARB-10) |
| Pipeline d'instanciation aval | Hors périmètre factory actuel | Géré dans le pipeline d'instanciation domaine |

---

## Points hors périmètre factory

- Logique de contenu domaine spécifique (feedback, exercices, graphe de connaissances)
- Runtime d'une application particulière
- Schémas d'instanciation domaine
- Logique métier propre à chaque application Learn-it
- Invariants du graphe (acyclicité, MSC scoring) — relèvent de la Constitution/Référentiel, pas de la factory

---

## Points sans consensus ou nécessitant discussion finale

### Point D-01 — Option pour ARB-05 : gate formel ou déclaration d'usage non garanti
**Nature :** choix d'implémentation entre deux approches valides  
**Position A (gate formel) :** conditionner l'activation du mécanisme à l'existence d'un validateur opérationnel — plus sûr, mais bloquant pour les usages anticipatoires  
**Position B (déclaration explicite) :** permettre l'usage précoce avec une déclaration explicite "non garanti tant que validateur absent" dans chaque projection — plus flexible mais requiert une discipline forte  
**Recommandation pour consolidation :** demander à l'humain-arbitre de trancher ce point, car il reflète une décision de politique de gouvernance qui dépasse le technique

### Point D-02 — Traitement de la présence dans `docs/cores/current/`
**Nature :** choix de gouvernance entre deux approches  
**Position A (intégration manifest) :** accélérer l'intégration au manifest officiel courant en étendant le schéma de release  
**Position B (déplacement temporaire) :** sortir les artefacts de `docs/cores/current/` dans une zone de staging tant qu'ils ne sont pas officiellement intégrés  
**Recommandation pour consolidation :** l'arbitre humain doit trancher selon la faisabilité de l'extension du schéma manifest et l'urgence de stabiliser la zone current

### Point D-03 — Rapports non lus (PERPL_X7T2 et PERPX_7KQ2)
**Nature :** incomplétude de cet arbitrage  
**Risque :** des points présents uniquement dans ces deux rapports ne sont pas couverts par la présente proposition  
**Recommandation pour consolidation :** intégrer ces deux rapports lors de la consolidation finale et vérifier s'ils contiennent des points non couverts dans ARB-01 à ARB-13

---

## Corrections à arbitrer avant patch

### Correction A-01 — Axe `runtime_policy_conformance` dans le contrat minimal (CRITIQUE)

- **Élément concerné :** `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** Absence de vérification des invariants constitutionnels runtime
- **Type de problème :** Compatibilité constitutionnelle
- **Gravité :** Critique
- **Impact factory :** La factory peut produire des applications non constitutionnellement conformes sans le détecter
- **Impact application produite :** Violation potentielle de `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
- **Impact IA :** Une IA validant une application produite ne peut pas vérifier ces invariants
- **Impact gouvernance/release :** Aucune release d'application ne peut être certifiée constitutionnellement compatible
- **Correction à arbitrer :** Ajouter un axe `runtime_policy_conformance` dans `minimum_validation_contract.minimum_axes` couvrant au minimum les invariants listés ci-dessus
- **Lieu probable de correction :** architecture

### Correction A-02 — Protocole minimal projections dérivées (CRITIQUE)

- **Élément concerné :** `contracts.execution_projection_contract` + `generated_projection_rules`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** Mécanisme déclaré opérationnel mais non instrumenté
- **Type de problème :** Exploitabilité IA + gouvernance
- **Gravité :** Critique
- **Impact factory :** Projection dérivée activable prématurément sans garantie de fidélité normative
- **Impact application produite :** Dérive normative silencieuse possible
- **Impact IA :** Une IA travaillant sur une projection non validée opère sur une base non fiable
- **Impact gouvernance/release :** Impossibilité d'auditer la conformité des projections utilisées
- **Correction à arbitrer :** Définir un protocole minimal obligatoire : scope déclaré, sources exactes, fingerprint, timestamp/version, validator de conformité, statut de promotion interdit vers canonique, politique d'usage explicite
- **Lieu probable de correction :** architecture + validator/tooling

### Correction A-03 — Signal de gouvernance release (CRITIQUE)

- **Élément concerné :** Présence dans `docs/cores/current/` hors manifest officiel
- **Localisation :** `platform_factory_state.yaml` metadata + gouvernance repo
- **Problème :** Statut hybride non signalé structurellement
- **Type de problème :** Gouvernance + traçabilité
- **Gravité :** Critique
- **Impact factory :** Utilisation non gouvernée des artefacts comme référence canonique avant promotion officielle
- **Impact application produite :** Traçabilité brisée si correction ultérieure
- **Impact IA :** Une IA lisant `docs/cores/current/` peut considérer ces artefacts comme faisant partie du socle canonique officiel
- **Impact gouvernance/release :** Absence de critère de promotion explicite
- **Correction à arbitrer :** Décider entre intégration manifest ou déplacement temporaire hors `current/` (voir Point D-02). Dans les deux cas, matérialiser un signal structurel externe aux `notes` metadata.
- **Lieu probable de correction :** manifest/release governance

### Correction A-04 — Résolution contradiction vocabulaire released (ÉLEVÉ)

- **Élément concerné :** `metadata.status` artefacts + doctrine pipeline
- **Localisation :** `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, `pipeline.md`
- **Problème :** Incohérence released/RELEASE_CANDIDATE entre pipeline et artefacts
- **Type de problème :** Cohérence architecturale + gouvernance
- **Gravité :** Élevé
- **Correction à arbitrer :** Aligner le vocabulaire. Option recommandée : adopter un statut transitoire gouverné distinct de "released current official" — ex. `current_under_challenge_governance` ou `baseline_released_under_governance_exception`
- **Lieu probable de correction :** state + architecture + pipeline

### Correction A-05 — Protocole minimal multi-IA (MODÉRÉ, différable)

- **Élément concerné :** `multi_ia_parallel_readiness`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** Exigences déclarées mais non instrumentées
- **Type de problème :** Exploitabilité IA + implémentabilité
- **Gravité :** Modéré
- **Correction à arbitrer :** Définir un protocole minimal de décomposition, d'assemblage, de résolution de conflit et de format de report homogène. Peut être traité en cycle suivant après A-01 à A-04.
- **Lieu probable de correction :** architecture + pipeline

---

## Résultat terminal

1. **arbitrage_run_id :** `PFARB_20260408_PERPLX_N2R8`
2. **Fichier écrit :** `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260408_PERPLX_N2R8.md`
3. **Résumé ultra-court :** 3/5 rapports lus. Consensus fort sur 4 zones critiques. 13 arbitrages proposés (3 critiques, 5 élevés, 4 modérés, 2 faibles). Aucun point rejeté. 2 points nécessitent un choix humain (ARB-05 gate vs déclaration, ARB-07 intégration manifest vs déplacement). Les 2 rapports non lus (PERPL_X7T2, PERPX_7KQ2) doivent être intégrés en consolidation finale.
