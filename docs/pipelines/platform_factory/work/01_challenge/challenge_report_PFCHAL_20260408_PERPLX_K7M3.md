# Challenge Report — Platform Factory Baseline V0.2

**challenge_run_id :** `PFCHAL_20260408_PERPLX_K7M3`  
**Date :** 2026-04-08  
**IA :** PERPLX (Perplexity / Claude Sonnet)  
**Stage :** STAGE_01_CHALLENGE  
**Pipeline :** `docs/pipelines/platform_factory/pipeline.md`

---

## Artefacts challengés

- `docs/cores/current/platform_factory_architecture.yaml` (PLATFORM_FACTORY_ARCHITECTURE_V0_2, status: RELEASE_CANDIDATE)
- `docs/cores/current/platform_factory_state.yaml` (PLATFORM_FACTORY_STATE_V0_2, status: RELEASE_CANDIDATE)

## Socle canonique lu

- `docs/cores/current/constitution.yaml` (CORE_LEARNIT_CONSTITUTION_V2_0)
- `docs/cores/current/referentiel.yaml` *(non lu dans ce run : non fourni dans les artefacts de launch — signalé ci-dessous)*
- `docs/cores/current/link.yaml` *(non lu dans ce run : non fourni dans les artefacts de launch — signalé ci-dessous)*

> **Note de run :** Le présent challenge a été exécuté avec la Constitution comme socle primaire lu, et les artefacts platform_factory V0.2. Referentiel.yaml et link.yaml n'ont pas été chargés dans ce run faute de pagination. Ce manque est signalé explicitement dans la carte de compatibilité constitutionnelle (voir Axe 1, point RC-01). Il ne compromet pas la validité du challenge sur les axes structurels, architecturaux et gouvernance, mais affaiblit légèrement la couverture des axes liés aux seuils délégués (Référentiel) et à la résolution inter-Core (LINK).

---

## Résumé exécutif

La Platform Factory V0.2 pose une base conceptuelle et architecturale explicite et cohérente avec la logique générale de Learn-it. Les principes fondamentaux (séparation générique/spécifique, fidélité normative des projections dérivées, contrat minimal d'application, multi-IA) sont identifiés et bornés. L'auto-déclaration du state comme `foundational_but_incomplete` est honnête et appropriée à un V0.

Cependant, le challenge identifie **quatre zones de risque non triviales** qui méritent arbitrage avant patch :

1. **L'absence de binding explicite entre les invariants constitutionnels critiques et les obligations du contrat minimal d'application produite** — une application peut sortir de la factory en apparence conforme sans que la factory ait réellement vérifié la conformité constitutionnelle (runtime local, absence de génération runtime, patch hors session).

2. **Le mécanisme de `validated_derived_execution_projections` n'est pas opérationnel** — le principe est posé, mais l'absence de validateur, de protocole de régénération et de localisation de stockage rend le mécanisme non fiable en l'état. Une IA travaillant à partir d'une projection dérivée non validée peut introduire une dérive normative silencieuse.

3. **La frontière entre le rôle de la factory et le futur pipeline d'instanciation domaine est bien déclarée en intention, mais non matérialisée comme garde-fou** — le risque de glissement est réel dès que les premières instanciations commencent.

4. **La gouvernance de release est incomplète** — les artefacts V0.2 sont dans `docs/cores/current/` mais hors manifest officiel courant. Ce statut hybride ("present but not officially integrated") est un trou de traçabilité accepté mais non borné dans le temps.

Le reste des lacunes (schémas YAML fins, outillage, granularité multi-IA) sont des manques V0 normaux, reconnus, sans risque immédiat tant qu'ils restent explicitement bornés.

---

## Carte de compatibilité constitutionnelle

| # | Invariant constitutionnel | Élément factory concerné | Binding | Risque |
|---|---|---|---|---|
| CC-01 | `INV_RUNTIME_FULLY_LOCAL` | `produced_application_minimum_contract` / `minimum_validation_contract` | **implicite faible** | Le contrat minimal ne contient pas d'axe de validation explicite "absence d'appel réseau runtime". Une application produite pourrait ne pas être vérifiée sur ce point. |
| CC-02 | `INV_NO_RUNTIME_CONTENT_GENERATION` | `produced_application_minimum_contract` | **absent** | Aucune obligation dans le contrat minimal ne force la vérification que l'application produite n'effectue pas de génération de contenu runtime. |
| CC-03 | `INV_NO_RUNTIME_FEEDBACK_GENERATION` (CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION) | `produced_application_minimum_contract` | **absent** | Même lacune que CC-02 pour le feedback généré à la volée. |
| CC-04 | `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` | `produced_application_minimum_contract` | **absent** | Le contrat minimal ne vérifie pas que l'application produite respecte l'obligation de patch précomputé hors session. |
| CC-05 | `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | `produced_application_minimum_contract` | **absent** | Même lacune. |
| CC-06 | `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | `source_of_authority` / `dependencies_to_referentiel` | **explicite** | Bien séparé. Binding solide. |
| CC-07 | `INV_FACTORY_DOES_NOT_DUPLICATE_NORM` (PF_INV) | `design_principles.PF_PRINCIPLE_NO_NORM_DUPLICATION` | **explicite** | Déclaré. Risque résiduel si une projection dérivée paraphrase implicitement. |
| CC-08 | `INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` | `contracts.execution_projection_contract` | **explicite** | Bien borné en principe. Risque opérationnel : sans validateur ni protocole de régénération, la conformité reste déclarative. |
| CC-09 | `INV_NO_PARTIAL_PATCH_STATE` | `transformation_chain` / `build_and_packaging_rules` | **implicite faible** | Aucun mécanisme de rollback ou d'atomicité n'est explicité dans les règles de transformation de la factory. |
| CC-10 | `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | hors périmètre factory (domaine) | N/A | Correctement hors scope. |
| RC-01 | Dépendances Référentiel / LINK | `dependencies_to_referentiel` / `dependencies_to_link` | **déclaré mais non chargé ce run** | Référentiel.yaml et link.yaml non lus. Les seuils délégués et résolutions inter-Core ne sont pas challengés dans ce run. |

**Synthèse constitutionnelle :** Les invariants liés à la séparation des couches normatives et à la non-duplication sont bien protégés. Les invariants liés au **runtime local** et aux **obligations de patch** ne sont **pas traçables** dans le contrat minimal d'application produite. C'est la faiblesse constitutionnelle principale.

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

Voir la carte ci-dessus.

**Point critique :** `produced_application_minimum_contract.minimum_validation_contract` définit cinq axes minimaux (`structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment`), mais aucun axe ne couvre explicitement la conformité aux invariants runtime-critiques de la Constitution (local, pas de génération, patch hors session). Une application produite peut passer le contrat minimal sans que son respect de `INV_RUNTIME_FULLY_LOCAL` ou `INV_NO_RUNTIME_CONTENT_GENERATION` ait été vérifié.

### Axe 2 — Cohérence interne de la factory

**Cohérence architecture/state :** Bonne cohérence générale. Les capacités `present`, `partial` et `absent` du state correspondent aux éléments présents dans l'architecture. Pas de contradiction flagrante.

**Signal de maturité surdéclarée (modéré) :** `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` et `PF_CAPABILITY_MINIMUM_APPLICATION_CONTRACT_DEFINED_AT_HIGH_LEVEL` sont listés comme `capabilities_present`. La distinction "defined at high level" est honnête, mais "present" dans une liste de capacités peut être lu comme opérationnel. Il serait plus rigoureux de distinguer entre "intent declared" et "operationally present".

**Séparation prescriptif/constatif :** Bien séparée entre les deux artefacts. Architecture = prescriptif, State = constatif. Pas de mélange observé.

**Séparation générique/spécifique :** Bien déclarée en intention (`does_not_govern`, `out_of_scope`, `forbidden_variability`). Non encore instrumentée — aucun mécanisme ne prévient activement qu'un contenu domaine soit introduit dans les modules génériques.

### Axe 3 — Portée et frontières

**Point solide :** La liste `does_not_govern` dans `purpose` est explicite et bien bornée (pas de contenu domaine, pas de logique feedback spécifique, pas de runtime d'une application particulière). Le `PF_LAYER_APPLICATION_INSTANTIATION` est clairement identifié comme couche aval distincte.

**Zone de risque :** La frontière entre `PF_LAYER_DERIVED_EXECUTION_PROJECTIONS` et `PF_LAYER_APPLICATION_INSTANTIATION` est floue opérationnellement. Une IA qui produit une projection dérivée pourrait empiéter sur le pipeline d'instanciation si le scope de la projection n'est pas strictement borné. L'emplacement policy (`status: TBD`) dans `generated_projection_rules.emplacement_policy` est le signal de ce risque.

**Angle mort :** La factory ne définit pas comment elle-même détecte qu'une transformation a franchi la frontière générique/spécifique. Il n'existe pas de signal de violation de frontière dans la chaîne de transformation (`transformation_chain`).

### Axe 4 — Contrat minimal d'une application produite

**Obligations présentes et bien posées :** identity, manifest principle, canonical dependency contract, runtime entrypoint (en intention), configuration minimale (en intention), validation minimale (axes), packaging minimal (principe), observabilité minimale, traceability.

**Obligations manquantes ou trop floues :**

- **Absence d'axe de validation constitutionnelle runtime.** Voir CC-01 à CC-05. C'est le manque le plus important.
- **`runtime_entrypoint_contract` déclaré obligatoire mais `exact_runtime_typology` absent.** Une IA ne peut pas vérifier qu'une application produite a un entrypoint valide tant que la typologie n'est pas définie.
- **`fingerprints de reproductibilité` mentionnés dans `identity.required_blocks` mais non définis.** Ce qui constitue un fingerprint valide n'est pas spécifié.
- **`minimum_observability_contract.minimum_signals` inclut `produced_application_minimum_contract_conformance_status`** — mais ce signal ne peut être calculé tant que le schéma de validation du contrat minimal n'est pas finalisé.

**Obligation non auditable :**
- `canonical_dependency_contract: required: true` — déclaré mais le mécanisme de vérification de la présence effective de cette déclaration dans un livrable produit n'est pas défini.

### Axe 5 — Validated derived execution projections

**Faiblesse principale : mécanisme non opérationnel.**

Le principe est solide (`contracts.execution_projection_contract` avec ses invariants `no_new_rule`, `no_normative_divergence`, etc.), mais :

- Aucun validateur n'existe (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED : absent`).
- L'emplacement de stockage est `TBD`.
- Le protocole de régénération est absent (`missing: regeneration_protocol` dans `derived_projection_conformity_status`).
- La politique d'usage runtime/offsession est notée comme manquante (`runtime_and_offsession_usage_policy_documented_and_tooling_aligned`).

**Risque de dérive silencieuse.** Si une IA reçoit une projection dérivée non encore validée (ce qui est possible dans le contexte actuel), elle peut travailler sur un document qui a glissé normativement sans le savoir. Le principe "une projection peut être l'unique artefact fourni à une IA" est donc **dangereux à activer en l'état** tant que le validateur et le protocole ne sont pas en place.

**Risque de paraphrase dangereuse.** L'interdit `uncontrolled_paraphrase` est déclaré dans le contrat de projection, mais aucun mécanisme ne permet de le détecter. Une paraphrase qui perd une nuance constitutionnelle (ex. : oublier le caractère "AND strict" du MSC, ou oublier la règle de non-génération runtime) ne sera pas signalée automatiquement.

**Risque de promotion implicite.** `prohibited: promotion_as_primary_canonical_artifact` est bien déclaré. Mais si une projection dérivée est stockée dans `docs/cores/current/` (ce que l'architecture interdit par `must_not_blur_docs_cores_current`), la confusion est possible dès que le pipeline est partiellement matérialisé et que l'emplacement reste TBD.

### Axe 6 — État reconnu, maturité et preuves

**Cohérence interne du state :** Les `validated_decisions` (5 décisions), `blockers` (3), `known_gaps` (4) et `evidence` (2 éléments) sont cohérents entre eux. Le wording `foundational_but_incomplete` dans `last_assessment` est juste et non sur-vendu.

**Tension modérée sur `capabilities_present` :** Cinq capacités sont classées "present". Parmi elles, `PF_CAPABILITY_MINIMUM_APPLICATION_CONTRACT_DEFINED_AT_HIGH_LEVEL` porte dans son nom la nuance "at high level" — ce qui est honnête. Mais `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` comme "present" alors que le pipeline n'est pas encore matérialisé (`PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE : absent`) pourrait induire en erreur sur la capacité réelle d'exécution.

**Evidence insuffisante :** Deux éléments d'evidence seulement. Le `PF_EVIDENCE_ARCHITECTURE_V0` pointe vers lui-même (l'artefact qui fait référence à l'artefact). Ce n'est pas une preuve externe de validation. Un état V0 qui ne pointe que vers ses propres artefacts comme preuves doit être explicitement reconnu comme tel.

### Axe 7 — Multi-IA en parallèle

**Exigences posées, non opérationnalisées.** Les cinq principes (`bounded_scope`, `stable_identifiers`, `explicit_dependencies`, `clear_assembly_points`, `homogeneous_reports`) sont listés dans `minimum_requirements` mais aucun n'est instrumenté.

**Manques critiques pour un travail multi-IA fiable :**
- Pas de protocole d'assemblage entre outputs IA (`ai_output_assembly_protocol : missing`).
- Pas de convention de granularité modulaire (`module_granularity_convention : missing`).
- Pas de protocole de résolution de conflit (`conflict_resolution_protocol : missing`).
- La granularité modulaire est classée dans `deferred_challenges` — ce qui est acceptable V0, mais doit être borné temporellement.

**Risque spécifique :** Si deux IA travaillent sur des projections dérivées de scopes qui se chevauchent, sans protocole d'assemblage, leur combinaison peut produire un état incohérent dans l'application produite. Ce risque est reconnu (`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`) mais sans borne ni plan de résolution.

### Axe 8 — Gouvernance release, manifest et traçabilité

**Trou de gouvernance principal :** Les artefacts V0.2 sont dans `docs/cores/current/` avec statut `RELEASE_CANDIDATE`, mais explicitement hors manifest officiel courant (`Non encore intégré au current manifest tant que le schéma core-release reste limité au trio constitution/referentiel/link`). Ce statut hybride crée un risque :

- Une IA lisant `docs/cores/current/` peut considérer ces artefacts comme faisant partie du socle canonique courant.
- La distinction entre "present in current" et "officially integrated in manifest" n'est visible que dans les `notes` du metadata — pas dans la structure de gouvernance elle-même.
- Il n'existe pas de fichier ou de signal de gouvernance qui matérialise explicitement cette distinction pour les IA et les pipelines.

**Risque de promotion implicite non gouvernée :** La progression de `RELEASE_CANDIDATE` vers une release officielle n'est pas décrite dans les artefacts challengés. Aucun critère de promotion n'est défini. Ce n'est pas bloquant V0, mais c'est un trou de traçabilité.

### Axe 9 — Implémentabilité pipeline

*Note : `pipeline.md` non chargé dans ce run. Cet axe est challengé sur la base de ce qui est visible dans les artefacts architecture/state.*

**Ce qui est visible :** La `transformation_chain` en 7 phases (`PF_CHAIN_01` à `PF_CHAIN_07`) est bien séquencée. Les phases couvrent lecture canonique, règles factory, génération de projections, préparation de modules, instanciation, validation du contrat minimal et packaging/traçage.

**Ce qui manque ou est flou :**
- Aucun critère de sortie de phase n'est défini. Une IA exécutant la chaîne ne sait pas quand une phase est "done".
- `PF_CHAIN_06_VALIDATE_APPLICATION_MIN_CONTRACT` suppose un validateur qui n'existe pas encore (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED : absent`). Cette phase est en pratique non exécutable.
- `PF_CHAIN_03_GENERATE_EXECUTION_PROJECTIONS` suppose un protocole de validation de projection qui n'existe pas.
- Les outputs de chaque phase ne sont pas définis. Un assemblage entre IA parallèles est donc non gouverné dans la chaîne elle-même.

### Axe 10 — Scénarios adversariaux

#### Scénario 1 — Dérive d'une projection dérivée

**Contexte :** Une IA reçoit une `validated_derived_execution_projection` couvrant le contrat minimal d'application pour produire un module de feedback. La projection a été générée manuellement avant que le validateur soit en place, et contient une paraphrase de `INV_NO_RUNTIME_CONTENT_GENERATION` affaiblie : "les contenus sont de préférence préexistants".

**Mécanismes activés :** `execution_projection_contract.no_normative_divergence` (déclaré mais non vérifié), `PF_CHAIN_03` (génération de projection sans validateur).

**Résultat :** L'IA produit un module qui génère des feedbacks à la volée en cas d'absence de template. Le module est packagé, le manifest est présent, le contrat minimal est passé. L'application paraît valide. `INV_NO_RUNTIME_CONTENT_GENERATION` est violé silencieusement.

**Faiblesse révélée :** Absence de validateur de projection + absence d'axe constitutionnel dans la validation du contrat minimal.

#### Scénario 2 — Application produite apparemment valide mais non locale

**Contexte :** Une application produite passe tous les axes de `minimum_validation_contract` (`structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment`). Son `runtime_entrypoint_contract` est déclaré. Mais son bootstrap effectue un appel réseau vers un service de scoring externe pour calculer la composante R du MSC, car la définition du runtime entrypoint ne précise pas l'interdiction d'appel réseau.

**Mécanismes activés :** `produced_application_minimum_contract.runtime_entrypoint_contract` (déclaré obligatoire mais typologie non finalisée), `minimum_validation_contract` (aucun axe constitutionnel runtime).

**Résultat :** `INV_RUNTIME_FULLY_LOCAL` est violé. La factory ne l'a pas détecté.

**Faiblesse révélée :** Absence d'axe de validation constitutionnelle runtime dans le contrat minimal + typologie de runtime entrypoint non finalisée.

#### Scénario 3 — Collision multi-IA

**Contexte :** Deux IA travaillent en parallèle sur deux modules génériques de la factory. IA-A produit un module de configuration minimale. IA-B produit un module de manifest. Les deux modules ont des blocs d'identité avec des conventions de nommage différentes (IA-A utilise `logical_identity`, IA-B utilise `application_id`). L'assemblage produit une application avec des fingerprints incohérents.

**Mécanismes activés :** `multi_ia_parallel_readiness.minimum_requirements.homogeneous_reports` (exigé mais non défini), `multi_ia_parallel_readiness.missing.ai_output_assembly_protocol`.

**Résultat :** La validation structurelle passe partiellement. La traçabilité est cassée silencieusement. Aucun mécanisme de la factory ne détecte la collision.

**Faiblesse révélée :** Absence de protocole d'assemblage + absence de convention de nommage entre modules produits par IA en parallèle.

#### Scénario 4 — Promotion release non gouvernée

**Contexte :** Un opérateur constate que `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` avec statut `RELEASE_CANDIDATE`. Il les considère comme suffisamment stables et les utilise comme référence canonique dans un nouveau pipeline sans passer par une promotion officielle. Une mise à jour ultérieure de ces artefacts (correction d'un trou) crée une divergence silencieuse avec le pipeline déjà en production.

**Mécanismes activés :** `status: RELEASE_CANDIDATE` dans metadata (non bloquant par aucun mécanisme factory), `notes` (hors manifest officiel — visible seulement dans les notes).

**Résultat :** La divergence entre la version utilisée et la version corrigée n'est pas traçable. Aucun signal de promotion officielle n'a été émis.

**Faiblesse révélée :** Absence de critère de promotion RELEASE_CANDIDATE → released + absence de signal de gouvernance externe au fichier metadata.

---

## Risques prioritaires

| # | Risque | Criticité | Artefact concerné |
|---|---|---|---|
| R-01 | Absence d'axes de validation constitutionnelle (runtime local, pas de génération, patch hors session) dans le contrat minimal d'application produite | **Critique** | architecture (contrat minimal) |
| R-02 | Mécanisme de `validated_derived_execution_projections` déclaré opérationnel en principe mais non instrumenté — risque de dérive normative silencieuse | **Élevé** | architecture + state |
| R-03 | Gouvernance de release hybride : artefacts dans `current` mais hors manifest officiel, sans critère de promotion ni signal externe | **Élevé** | state + release governance |
| R-04 | Frontière générique/spécifique non instrumentée — aucun mécanisme de détection de franchissement dans la transformation chain | **Modéré** | architecture |
| R-05 | Multi-IA : protocole d'assemblage et convention de granularité absents — travail parallèle non gouverné en pratique | **Modéré** | architecture + state |
| R-06 | `PF_CHAIN_06` (validation du contrat minimal) non exécutable sans validateur — phase de pipeline bloquée | **Modéré** | pipeline |
| R-07 | Evidence du state circulaire — les artefacts se pointent eux-mêmes comme preuves | **Faible** | state |
| R-08 | `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` classé "present" alors que le pipeline n'est pas matérialisé — légère surdéclaration | **Faible** | state |

---

## Points V0 acceptables

Les éléments suivants sont des manques normaux et acceptables pour une baseline V0 explicitement déclarée `foundational_but_incomplete` :

- Schéma YAML fin du manifest d'application non arrêté (`PF_GAP_EXACT_YAML_SCHEMA_NOT_FINALIZED`) — normal V0, sans impact immédiat tant que le principe est posé.
- Emplacement de stockage des projections dérivées TBD (`PF_BLOCKER_PROJECTION_LOCATION_PENDING`) — bloquant pour l'opérationnalisation, pas pour la gouvernance.
- Granularité modulaire multi-IA différée (`deferred_challenges`) — acceptable tant que la décomposition parallèle n'est pas encore démarrée.
- Typologies fines non arrêtées (runtime entrypoint, configuration, packaging) — acceptables V0 tant que les obligations de principe sont posées.
- Absence d'outillage de validation (`PF_GAP_VALIDATION_TOOLING_MISSING`) — expected V0.
- Pipeline non entièrement matérialisé (`PF_GAP_FACTORY_PIPELINE_NOT_MATERIALIZED`) — attendu, tant que les stages sont définis en intention.
- Hors manifest officiel courant (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`) — acceptable V0 si borné temporellement.

---

## Corrections à arbitrer avant patch

### Correction C-01 — Ajouter des axes constitutionnels runtime dans le contrat minimal d'application

**Élément concerné :** `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`  
**Localisation :** `platform_factory_architecture.yaml`, section `contracts.produced_application_minimum_contract.minimum_validation_contract`  
**Nature :** Absence de vérification de conformité aux invariants runtime-critiques de la Constitution  
**Type :** Compatibilité constitutionnelle  
**Gravité :** Critique  
**Impact factory :** La factory peut produire des applications non constitutionnellement conformes sans le détecter  
**Impact application produite :** Violation potentielle de `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`  
**Impact IA :** Une IA validant une application produite ne peut pas vérifier ces invariants avec les axes actuels  
**Impact gouvernance/release :** Aucune release d'application ne peut être certifiée constitutionnellement compatible  
**Correction à arbitrer :** Ajouter un axe `constitutional_runtime_conformance` dans `minimum_validation_contract.minimum_axes` couvrant au minimum les invariants listés ci-dessus  
**Lieu probable de correction :** architecture

---

### Correction C-02 — Borner l'activation du mécanisme de projections dérivées à un état opérationnel minimal

**Élément concerné :** `contracts.execution_projection_contract` / `generated_projection_rules`  
**Localisation :** `platform_factory_architecture.yaml` + `platform_factory_state.yaml` (derived_projection_conformity_status)  
**Nature :** Mécanisme déclaré opérationnel en principe mais non instrumenté — activation prématurée risquée  
**Type :** Implémentabilité + gouvernance  
**Gravité :** Élevé  
**Impact factory :** Une projection dérivée peut être utilisée comme unique contexte IA sans garantie de fidélité normative  
**Impact application produite :** Dérive normative silencieuse possible  
**Impact IA :** Une IA recevant une projection non validée travaille sur une base non fiable  
**Impact gouvernance/release :** Impossibilité d'auditer la conformité des projections utilisées  
**Correction à arbitrer :** Décider si l'activation des projections dérivées comme unique contexte IA doit être conditionnée à l'existence d'un validateur minimal. Option A : gate d'activation formelle. Option B : déclaration explicite de "usage non garanti tant que validateur absent" dans chaque projection.  
**Lieu probable de correction :** architecture + validator/tooling

---

### Correction C-03 — Matérialiser la distinction release governance entre "present in current" et "officially integrated"

**Élément concerné :** `metadata.status: RELEASE_CANDIDATE` + `notes` (hors manifest officiel)  
**Localisation :** `platform_factory_architecture.yaml` et `platform_factory_state.yaml`, section `metadata`  
**Nature :** Trou de gouvernance de release — statut hybride non signalé structurellement  
**Type :** Gouvernance + traçabilité  
**Gravité :** Élevé  
**Impact factory :** Utilisation non gouvernée des artefacts comme référence canonique avant promotion officielle  
**Impact application produite :** Applications construites sur une version non officiellement promue — traçabilité brisée si correction ultérieure  
**Impact IA :** Une IA lisant `docs/cores/current/` peut considérer ces artefacts comme faisant partie du socle canonique officiel  
**Impact gouvernance/release :** Absence de critère de promotion explicite ; dérive silencieuse possible entre version utilisée et version corrigée  
**Correction à arbitrer :** Définir un signal de gouvernance externe au metadata (ex. : fichier de statut dédié, entrée dans un registry de factory, ou note dans le pipeline) qui matérialise explicitement l'état "present but not officially integrated" et les conditions de promotion  
**Lieu probable de correction :** manifest/release governance + pipeline

---

### Correction C-04 — Définir un signal de détection de franchissement de frontière générique/spécifique dans la transformation chain

**Élément concerné :** `transformation_chain` / `variant_governance.forbidden_variability`  
**Localisation :** `platform_factory_architecture.yaml`, sections `transformation_chain` et `variant_governance`  
**Nature :** Frontière déclarée mais non instrumentée — aucun mécanisme de détection dans la chaîne  
**Type :** Cohérence architecturale + implémentabilité  
**Gravité :** Modéré  
**Impact factory :** Du contenu domaine peut être introduit dans les modules génériques sans trigger  
**Impact application produite :** Modules prétendument génériques contenant en réalité du contenu spécifique  
**Impact IA :** Une IA ne peut pas détecter qu'elle franchit la frontière générique/spécifique  
**Impact gouvernance/release :** Contamination silencieuse du générique par le spécifique  
**Correction à arbitrer :** Décider si un critère de détection de franchissement doit être ajouté dans la phase `PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS` ou dans un validator dédié  
**Lieu probable de correction :** architecture + validator/tooling

---

## Résultat terminal

1. **challenge_run_id :** `PFCHAL_20260408_PERPLX_K7M3`
2. **Fichier écrit :** `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260408_PERPLX_K7M3.md`
3. **Résumé ultra-court :** Base V0.2 honnête et cohérente. Risque critique : contrat minimal d'application ne vérifie pas les invariants constitutionnels runtime. Risque élevé : projections dérivées non instrumentées activables prématurément. Risque élevé : gouvernance de release hybride sans signal externe. 4 corrections à arbitrer avant patch.
