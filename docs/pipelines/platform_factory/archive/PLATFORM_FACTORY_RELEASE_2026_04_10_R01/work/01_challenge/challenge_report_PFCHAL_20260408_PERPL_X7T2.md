# CHALLENGE REPORT — STAGE_01_CHALLENGE — Platform Factory

## challenge_run_id

`PFCHAL_20260408_PERPL_X7T2`

## Date

2026-04-08

## Artefacts challengés

- `docs/cores/current/platform_factory_architecture.yaml` (PLATFORM_FACTORY_ARCHITECTURE_V0_2)
- `docs/cores/current/platform_factory_state.yaml` (PLATFORM_FACTORY_STATE_V0_2)

## Socle canonique lu

- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/pipelines/platform_factory/pipeline.md`

---

## Résumé exécutif

La Platform Factory V0.2 constitue une base conceptuelle et architecturale cohérente, intentionnellement V0, posée dans `docs/cores/current/`. Son périmètre est bien délimité : elle gouverne le HOW générique de production d'applications Learn-it, le contrat minimal d'application produite, et le modèle de projections dérivées. La séparation prescriptif/constatif est respectée entre les deux artefacts. La dépendance explicite au trio canonique (Constitution + Référentiel + LINK) est déclarée.

Cependant, l'analyse adversariale révèle **quatre zones de fragilité structurelle** qui méritent arbitrage avant tout patch :

1. **Brèche de traçabilité constitutionnelle dans le contrat minimal d'application produite** : le contrat actuel ne permet pas de prouver qu'une application produite respecte les invariants constitutionnels critiques (runtime 100 % local, absence de génération runtime, absence de dépendance IA continue). Aucune obligation de validation constitutionnelle n'est exprimée dans les axes de validation minimale.

2. **Projections dérivées : mécanisme déclaré mais non gouverné** : les `validated_derived_execution_projections` sont définies en principe avec de bonnes règles d'invariant, mais l'absence de protocole de validation, de localisation de stockage, et de règle de régénération déterministe les rend aujourd'hui inopérables sans improvisation IA — ce qui contredit leur propre contrat d'usage.

3. **Maturité partiellement surdéclarée dans `platform_factory_state.yaml`** : plusieurs capacités listées comme `capabilities_present` sont en réalité intentionnelles ou déclaratives, non instrumentées. L'absence de démarcation claire entre « capability définie » et « capability opérationnelle » génère un faux sentiment de complétude.

4. **Trou de gouvernance manifest/release** : les artefacts platform_factory sont dans `docs/cores/current/` mais explicitement hors du manifest officiel courant. Aucune procédure de fermeture de ce gap n'est formalisée dans le pipeline, ce qui crée un risque de promotion implicite non gouvernée.

Ces problèmes ne bloquent pas l'usage de la baseline pour lancer un cycle de challenge/arbitrage/patch. Ils doivent néanmoins être arbitrés avant de déclarer un état plus avancé ou avant de déployer des projections dérivées en production IA.

---

## Carte de compatibilité constitutionnelle

| Invariant constitutionnel | Élément factory concerné | Binding | Risque |
|---|---|---|---|
| Runtime 100 % local | `produced_application_minimum_contract` → `minimum_validation_contract` | Absent | Une application produite peut passer le contrat minimal sans prouver l'absence de dépendance réseau runtime |
| Absence d'appel IA continu / dépendance réseau temps réel | `minimum_validation_contract` / `minimum_observability_contract` | Absent | Aucun axe de validation ni signal d'observabilité ne couvre cet invariant |
| Absence de génération de contenu runtime | `minimum_validation_contract` | Absent | Idem — aucun axe explicite |
| Absence de génération de feedback runtime hors templates | `minimum_validation_contract` | Absent | Idem |
| Séparation inviolable Constitution / Référentiel | `design_principles` (PF_PRINCIPLE_NO_NORM_DUPLICATION) + `invariants` | Explicite, solide | Faible — bien couvert en principe |
| Validation locale déterministe des patchs | `build_and_packaging_rules` | Implicite faible | Pas d'axe de validation dédié dans le contrat minimal d'application produite |
| Artefacts patch précomputés hors session | Hors périmètre factory déclaré | Non couvert, correctement out-of-scope | Acceptable en V0 si la frontière reste explicite |
| Absence de duplication normative | `PF_INV_FACTORY_DOES_NOT_DUPLICATE_NORM` | Explicite | Solide |
| Traçabilité explicite dépendances canoniques | `canonical_dependency_contract` (required: true) | Explicite | Présent mais non schématisé — risque de contrat creux |
| Absence d'état partiel interdit | `CONSTRAINT_REFERENTIEL_DOUBLE_BUFFER_REQUIRED_FOR_PATCH` (Référentiel) | Non relié au contrat minimal factory | L'architecture factory ne reprend pas cette contrainte pour les transformations internes factory |

**Verdict carte** : Les invariants constitutionnels les plus critiques pour le runtime (local, IA-free, no-generation) ne sont pas couverts par le contrat minimal d'application produite. Ils sont implicitement attendus mais non auditables depuis le manifest ou la validation minimale.

---

## Analyse détaillée par axe

---

### Axe 1 — Compatibilité constitutionnelle

**Point 1.1 — Invariants runtime non reflétés dans le contrat minimal d'application produite**

- **Élément concerné** : `produced_application_minimum_contract` → `minimum_validation_contract` → `minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`, section `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Constat** : Les axes minimaux de validation déclarés sont `structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment`. Aucun axe ne couvre la conformité aux invariants constitutionnels critiques suivants : runtime 100 % local, absence de dépendance IA continue, absence de génération runtime.
- **Nature** : absence de binding explicite entre contrat minimal et invariants constitutionnels opérationnels
- **Type de problème** : compatibilité constitutionnelle + complétude
- **Gravité** : élevée
- **Impact factory** : La factory peut valider une application produite comme conforme sans vérifier sa compatibilité constitutionnelle réelle.
- **Impact application produite** : Une application peut passer le minimum_contract tout en violant des invariants constitutionnels forts.
- **Impact IA** : Une IA chargée de valider une application produite à partir du contrat minimal factory ne dispose pas de critères suffisants.
- **Impact gouvernance/release** : Un release de factory peut certifier une conformité qui n'en est pas une.
- **Correction à arbitrer** : Ajouter un axe explicite `constitutional_invariant_conformance` (ou équivalent) dans `minimum_validation_contract.minimum_axes`, listant au minimum les invariants constitutionnels critiques que toute application produite doit démontrer.
- **Lieu probable** : architecture

---

**Point 1.2 — Observabilité minimale ne couvre pas les invariants constitutionnels**

- **Élément concerné** : `minimum_observability_contract.minimum_signals`
- **Localisation** : `platform_factory_architecture.yaml`, section `contracts.produced_application_minimum_contract.minimum_observability_contract`
- **Constat** : Les signaux minimaux d'observabilité listés sont `build_identity`, `activated_modules`, `derived_projections_used`, `validation_status`, `traceability_references`, `produced_application_minimum_contract_conformance_status`. Aucun signal ne porte sur la conformité constitutionnelle (runtime local, absence génération).
- **Nature** : incomplétude de l'observabilité vis-à-vis de l'autorité canonique
- **Type de problème** : compatibilité constitutionnelle + gouvernance
- **Gravité** : modérée (découle du Point 1.1)
- **Correction à arbitrer** : Ajouter un signal `constitutional_invariant_compliance_status` dans les signaux minimaux d'observabilité.
- **Lieu probable** : architecture

---

**Point 1.3 — Absence de reprise de la contrainte double-buffer pour les transformations internes factory**

- **Élément concerné** : `transformation_chain` + `build_and_packaging_rules`
- **Localisation** : `platform_factory_architecture.yaml`
- **Constat** : La Constitution et le Référentiel (`CONSTRAINT_REFERENTIEL_DOUBLE_BUFFER_REQUIRED_FOR_PATCH`) imposent un mécanisme de double-buffer et swap atomique pour toute application de patch. La factory ne reprend pas cette contrainte pour ses propres transformations internes (phases PF_CHAIN_03 à PF_CHAIN_07). Il n'est pas clair si cette contrainte s'applique à la factory elle-même ou seulement à ses applications produites.
- **Nature** : ambiguïté de périmètre d'un invariant constitutionnel
- **Type de problème** : compatibilité constitutionnelle + cohérence architecturale
- **Gravité** : modérée
- **Correction à arbitrer** : Clarifier explicitement si le double-buffer s'applique aux transformations internes factory (PF_CHAIN_05_INSTANTIATE) et, si oui, l'inscrire dans les `build_requirements`.
- **Lieu probable** : architecture

---

### Axe 2 — Cohérence interne de la factory

**Point 2.1 — Contradiction entre `capabilities_present` et absence d'instrumentation**

- **Élément concerné** : `capabilities_present` dans `platform_factory_state.yaml`
- **Localisation** : `platform_factory_state.yaml`, section `capabilities_present`
- **Constat** : Cinq capacités sont déclarées comme `capabilities_present`, notamment `PF_CAPABILITY_FACTORY_SCOPE_DEFINED`, `PF_CAPABILITY_MINIMUM_APPLICATION_CONTRACT_DEFINED_AT_HIGH_LEVEL`, `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`. Ces capacités sont réelles comme déclarations intentionnelles, mais leur description ("définie", "posée") correspond à un niveau déclaratif/intentionnel, non opérationnel. La frontière entre `capabilities_present` (intentionnel) et `capabilities_partial` (partiellement instrumenté) est floue.
- **Nature** : maturité surdéclarée
- **Type de problème** : faux niveau de maturité + cohérence architecturale
- **Gravité** : modérée
- **Impact factory** : Donne un faux sentiment de complétude sur les éléments fondamentaux.
- **Impact IA** : Une IA consultant l'état pour décider si elle peut opérer indépendamment pourrait surestimer la maturité réelle.
- **Correction à arbitrer** : Introduire une distinction explicite dans `platform_factory_state.yaml` entre `capability_declared` (intention posée), `capability_defined` (schéma ou règle posée), et `capability_operational` (instrumentée et vérifiable). Ou à défaut, ajouter un attribut `evidence_level` sur chaque capacité.
- **Lieu probable** : state

---

**Point 2.2 — Séparation prescriptif/constatif globalement bien tenue — signal positif**

La séparation entre `platform_factory_architecture.yaml` (prescriptif) et `platform_factory_state.yaml` (constatif) est globalement respectée. Les `validated_decisions`, `known_gaps`, `blockers` et `capabilities_*` sont dans le state. Les principes, contrats et invariants sont dans l'architecture. Ce mécanisme est **solide en V0**.

---

**Point 2.3 — Tension entre `PF_LAYER_FACTORY_STATE` déclaré comme `v0_defined` et `last_assessment.result: foundational_but_incomplete`**

- **Élément concerné** : `maturity_by_layer` + `last_assessment`
- **Localisation** : `platform_factory_state.yaml`
- **Constat** : La maturity du layer `PF_LAYER_FACTORY_STATE` est déclarée `v0_defined`, ce qui semble cohérent. Mais l'assessment final dit `foundational_but_incomplete`. Il n'y a pas de contradiction formelle, mais l'absence d'une grille normalisée de correspondance entre les labels de maturity (`v0_defined`, `concept_defined_not_yet_operationalized`, `boundary_defined_only`) et le verdict global crée une zone de lecture ambiguë.
- **Nature** : incohérence de vocabulaire de maturité
- **Type de problème** : gouvernance + cohérence architecturale
- **Gravité** : faible
- **Correction à arbitrer** : Documenter explicitement la grille de correspondance entre labels de maturity par layer et état global admissible.
- **Lieu probable** : state

---

### Axe 3 — Portée et frontières

**Point solide** : La factory déclare explicitement ce qu'elle ne gouverne pas (`does_not_govern`, `out_of_scope`). La frontière avec le futur pipeline d'instanciation domaine est correctement posée comme `boundary_defined_only`. Ce positionnement est sain pour une V0.

**Zone de risque** : La `transformation_chain` inclut une phase `PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS`. En incluant cette phase dans la factory, l'architecture fabrique une dépendance implicite à ce qui est déclaré hors scope. Une IA exécutant la chaîne de transformation complète devrait gérer une phase dont le périmètre exact est non spécifié.

- **Élément concerné** : `transformation_chain.phases[PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS]`
- **Nature** : frontière de couche insuffisamment fermée
- **Type de problème** : cohérence architecturale + implémentabilité
- **Gravité** : modérée
- **Correction à arbitrer** : Soit extraire PF_CHAIN_05 de la transformation_chain factory (elle appartient au futur pipeline d'instanciation), soit la redéfinir explicitement comme un "point de délégation" vers le pipeline aval avec un contrat d'interface formalisé.
- **Lieu probable** : architecture

**Angle mort** : La factory ne définit pas ce qui se passe si un artefact canonique (constitution.yaml, referentiel.yaml, link.yaml) est mis à jour après qu'une application ait été produite. Il n'existe pas de mécanisme de gestion des dépendances canoniques à jour au niveau factory.

---

### Axe 4 — Contrat minimal d'une application produite

**Point 4.1 — `canonical_dependency_contract` requis mais non schématisé**

- **Élément concerné** : `produced_application_minimum_contract.canonical_dependency_contract`
- **Constat** : `required: true` mais aucun contenu, aucun champ minimal, aucun exemple. Le contrat est creux.
- **Nature** : obligation non auditable
- **Type de problème** : complétude + implémentabilité
- **Gravité** : élevée
- **Impact application produite** : Une application peut déclarer une `canonical_dependency_contract` vide ou incomplète sans que la factory puisse la rejeter.
- **Correction à arbitrer** : Définir les champs minimaux obligatoires du `canonical_dependency_contract` (au minimum : constitution_version, referentiel_version, link_version, pinning_mode).
- **Lieu probable** : architecture

---

**Point 4.2 — `runtime_entrypoint_contract` insuffisamment typé**

- **Élément concerné** : `produced_application_minimum_contract.runtime_entrypoint_contract`
- **Constat** : Les champs `runtime_entrypoint_id`, `runtime_entrypoint_type`, `bootstrap_contract`, `runtime_prerequisites` sont listés comme obligations `must_declare`, mais aucune valeur admissible n'est définie pour `runtime_entrypoint_type`. L'état reconnaît ce gap (`PF_CAPABILITY_RUNTIME_ENTRYPOINT_MODEL : partial`).
- **Nature** : obligation présente mais trop floue pour être auditable
- **Type de problème** : complétude + implémentabilité
- **Gravité** : modérée (reconnue en state)
- **Correction à arbitrer** : Définir au moins une liste provisoire des types admissibles de point d'entrée runtime, même non exhaustive, pour borner les implémentations.
- **Lieu probable** : architecture (liste provisoire) + state (mise à jour capacité)

---

**Point 4.3 — Absence d'obligation explicite de compatibilité constitutionnelle dans le contrat minimal** (voir aussi Point 1.1)

- **Élément concerné** : `minimum_validation_contract.minimum_axes`
- **Gravité** : élevée (voir Axe 1)

---

**Point solide** : Le bloc identité (`logical_identity`, `produced_instance_identity`, `reproducibility_fingerprints`) est bien présent comme obligation. Les blocs manifest, packaging et observabilité ont une intention claire. C'est la base minimale correcte pour une V0.

---

### Axe 5 — Validated derived execution projections

**Point 5.1 — Mécanisme déclaré mais entièrement non opérationnel**

- **Élément concerné** : `contracts.execution_projection_contract` + `generated_projection_rules`
- **Constat** : Les règles d'invariants des projections dérivées sont correctement formulées (`no_new_rule`, `no_normative_divergence`, etc.). Mais le stockage, le protocole de validation, et le protocole de régénération sont tous absents (`derived_projection_conformity_status: defined_in_principle_with_explicit_conditions_and_missing_tooling`).
- **Nature** : mécanisme correctement borné en principe mais inopérable en pratique
- **Type de problème** : implémentabilité + gouvernance
- **Gravité** : élevée pour tout usage réel
- **Impact IA** : Une IA qui reçoit une projection dérivée ne peut pas vérifier qu'elle est bien `validated`. Elle doit faire confiance à une étiquette non instrumentée.
- **Risque spécifique** : La règle `rule_of_use` stipule qu'une projection validée peut être le seul artefact fourni à une IA. Si cette règle est appliquée avant que le mécanisme de validation soit instrumenté, le principe de fidelité normative peut être violé silencieusement.
- **Correction à arbitrer** : Définir, même à haut niveau, (a) l'emplacement canonique des projections dérivées, (b) le protocole de validation minimal, (c) le schéma de marquage `validated_derived_execution_projection` dans le manifest produit. Bloquer l'usage comme artefact unique IA jusqu'à ce que ces trois points soient définis.
- **Lieu probable** : architecture + pipeline (étape de génération et de validation des projections) + validator/tooling

---

**Point 5.2 — `emplacement_policy.status: TBD` dans `generated_projection_rules`**

- **Élément concerné** : `generated_projection_rules.emplacement_policy`
- **Constat** : Le statut est explicitement `TBD`. Le risque est que des projections soient placées dans `docs/cores/current/` par défaut, mêlant artefacts canoniques primaires et projections dérivées.
- **Nature** : risque de promotion implicite de projections en artefacts canoniques
- **Type de problème** : gouvernance + compatibilité constitutionnelle
- **Gravité** : élevée
- **Correction à arbitrer** : Décider un emplacement dédié (ex. `docs/projections/`) strictement séparé de `docs/cores/current/`, et documenter l'interdiction de placer des projections dérivées dans l'espace canonique courant.
- **Lieu probable** : architecture + manifest/release governance

---

### Axe 6 — État reconnu, maturité et preuves

**Point 6.1 — `capabilities_present` contient des capacités purement déclaratives**

Voir Point 2.1. Les cinq capacités listées comme `present` sont définies en intention mais ne sont pas instrumentées. Aucune preuve d'implémentation n'est référencée dans `evidence` pour ces capacités. Le seul evidence listé est `PF_EVIDENCE_PLAN_V2` (un document de plan) et `PF_EVIDENCE_ARCHITECTURE_V0` (l'artefact lui-même, ce qui constitue une auto-référence circulaire).

- **Nature** : faux niveau de maturité + preuve insuffisante
- **Gravité** : modérée
- **Correction à arbitrer** : Requalifier les capacités `present` en `declared_only` ou `defined_by_declaration` pour celles qui n'ont pas d'evidence d'implémentation. Ou enrichir l'`evidence` avec des artefacts vérifiables.
- **Lieu probable** : state

---

**Point 6.2 — `last_assessment.assessment_type: initial_baseline` — acceptable**

Le type `initial_baseline` est cohérent et honnête. Le résultat `foundational_but_incomplete` est juste et bien calibré. Ce point est **solide et acceptable en V0**.

---

**Point 6.3 — Cohérence `validated_decisions` / `capabilities` / `blockers` / `gaps`**

Les quatre `validated_decisions` (`PF_DECISION_TWO_ARTIFACTS`, `PF_DECISION_SCOPE_B`, `PF_DECISION_DERIVED_PROJECTIONS`, `PF_DECISION_MULTI_IA_FIRST_CLASS`, `PF_DECISION_DOWNSTREAM_INSTANTIATION`) sont cohérentes avec les capacités présentes, partielles et absentes. Le mapping entre blockers et capabilities absentes est clair. La cohérence interne de l'état est **globalement satisfaisante pour une V0**.

---

### Axe 7 — Multi-IA en parallèle

**Point 7.1 — Exigences posées, décomposition absente**

- **Élément concerné** : `multi_ia_parallel_readiness`
- **Constat** : Les cinq exigences (`bounded_scopes`, `stable_identifiers`, `explicit_dependencies`, `clear_assembly_points`, `homogeneous_reports`) sont bien listées. Mais aucune n'est instrumentée. En particulier, `assembly_protocol_between_ai_outputs` et `optimal_module_granularity` sont des `deferred_challenges` sans date ou décision.
- **Nature** : exigence de premier rang non opérationnalisée
- **Type de problème** : implémentabilité + gouvernance
- **Gravité** : modérée en V0, élevée si plusieurs IA sont mises en parallèle sans ce cadre
- **Correction à arbitrer** : Décider si le cycle V0→V1 inclut la définition du protocole d'assemblage entre sorties IA. Si oui, poser un gap explicite avec une décision de déclenchement.
- **Lieu probable** : state (gap) + architecture (protocole minimal)

---

**Point 7.2 — Projections dérivées non localisées = risque de collision de contexte IA**

Si deux IA reçoivent deux projections dérivées distinctes dont les scopes se chevauchent implicitement (faute de localisation et de schéma finalisés), leurs outputs peuvent entrer en conflit sans que la factory ne le détecte.

- **Nature** : risque de collision multi-IA par absence de gestion des scopes de projections
- **Gravité** : modérée (conditionnelle à l'usage réel multi-IA)
- **Correction à arbitrer** : Lier l'usage multi-IA à la résolution du Point 5.1 (localisation + validation des projections). Interdire formellement l'usage multi-IA sur des projections non localisées et non validées.
- **Lieu probable** : architecture + pipeline

---

### Axe 8 — Gouvernance release, manifest et traçabilité

**Point 8.1 — Artefacts platform_factory dans `current/` mais hors manifest officiel**

- **Élément concerné** : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Constat** : Les artefacts sont dans `docs/cores/current/` mais explicitement exclus du manifest courant. Le blocker est reconnu mais la procédure pour le fermer n'est pas définie dans le pipeline.
- **Nature** : trou de gouvernance release
- **Type de problème** : gouvernance + traçabilité
- **Gravité** : élevée
- **Impact release** : Il n'est pas possible de distinguer un artefact "current" validé d'un artefact "current" hors-manifest sans consulter manuellement le manifest. Un audit automatisé ne peut pas trancher.
- **Correction à arbitrer** : Définir explicitement dans le pipeline (STAGE_08_FACTORY_PROMOTE_CURRENT ou un stage dédié) la procédure de mise à jour du manifest officiel lors d'une promotion. Ou créer un manifest dédié platform_factory en attendant l'évolution du schema core.
- **Lieu probable** : pipeline + manifest/release governance

---

**Point 8.2 — Absence de fingerprint de reproductibilité pour les artefacts platform_factory eux-mêmes**

- **Élément concerné** : `contracts.produced_application_minimum_contract.identity.required_blocks` (reproduciblity_fingerprints requis pour une application produite)
- **Constat** : Le contrat exige des fingerprints pour les applications produites, mais les artefacts platform_factory eux-mêmes (`platform_factory_architecture.yaml`, `platform_factory_state.yaml`) ne déclarent aucun mécanisme de fingerprint ou de hash de version. Leur `version: 0.2.0` et `status: RELEASE_CANDIDATE` ne constituent pas un fingerprint reproductible.
- **Nature** : incohérence entre exigences imposées aux applications et pratique interne factory
- **Type de problème** : gouvernance + traçabilité
- **Gravité** : modérée
- **Correction à arbitrer** : Ajouter un bloc `reproducibility` (ou équivalent) aux métadonnées des artefacts platform_factory eux-mêmes.
- **Lieu probable** : architecture + state

---

### Axe 9 — Implémentabilité pipeline

**Point 9.1 — STAGE_01_CHALLENGE correctement structuré**

Le pipeline déclare correctement les inputs, le prompt à utiliser et l'output attendu pour STAGE_01. C'est le stage en cours d'exécution. **Solide.**

**Point 9.2 — STAGE_04 à STAGE_09 déclarés mais partiellement flous**

- **Élément concerné** : stages STAGE_04 à STAGE_09
- **Constat** : STAGE_04 et STAGE_06 référencent un prompt compagnon `Make23PlatformFactoryValidation.md` sans définir la relation entre le launch prompt et le prompt compagnon (lequel prime, comment ils se combinent). STAGE_07 et STAGE_08 délèguent leur spec à des fichiers `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md` — il faut vérifier que ces fichiers existent et sont complets.
- **Nature** : gouvernance pipeline incomplète sur les stages aval
- **Type de problème** : implémentabilité + gouvernance
- **Gravité** : modérée
- **Correction à arbitrer** : Vérifier l'existence et la complétude de `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`. Clarifier la relation launch prompt / prompt compagnon pour STAGE_04 et STAGE_06.
- **Lieu probable** : pipeline

---

**Point 9.3 — Absence de validator dédié à la conformité des projections dérivées dans le pipeline**

- **Élément concerné** : `PF_CAPABILITY_FACTORY_PRIORITY_VALIDATORS_SHORTLIST_MATERIALIZED`
- **Constat** : La short-list prioritaire de validateurs (`derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`) est définie mais non matérialisée. Aucun stage du pipeline ne référence un validateur implémenté — seulement des prompts.
- **Nature** : absence de tooling critique
- **Type de problème** : implémentabilité + gouvernance
- **Gravité** : élevée pour tout usage de production
- **Correction à arbitrer** : Poser explicitement dans le pipeline la condition de disponibilité des validateurs avant d'autoriser un usage hors sandbox.
- **Lieu probable** : pipeline + validator/tooling

---

### Axe 10 — Scénarios adversariaux

---

**Scénario A — Projection dérivée utilisée comme seul contexte IA avant validation instrumentée**

- **Déclencheur** : Une IA reçoit une projection dérivée étiquetée `validated_derived_execution_projection` pour produire un module d'application. La projection a été générée manuellement depuis les cores canoniques, sans validation automatique.
- **Mécanismes activés** : `execution_projection_contract.rule_of_use` (projection peut être seul artefact) + absence de protocole de validation instrumenté
- **Faiblesse révélée** : La projection peut contenir une omission ou une reformulation déviante d'un invariant constitutionnel. Aucun validateur ne l'a vérifié. L'IA produit un module non conforme en croyant travailler dans le cadre canonique.
- **Source du problème** : projections dérivées (Point 5.1) + validator/tooling (Point 9.3)

---

**Scénario B — Application produite conforme au contrat minimal mais violant un invariant constitutionnel fort**

- **Déclencheur** : Une application Learn-it est produite et validée par la factory. Elle passe tous les axes du `minimum_validation_contract` (structure, conformance, traceability, packaging, state alignment). Elle est promue comme `VALID`.
- **Mécanismes activés** : `minimum_validation_contract.minimum_axes` + `minimum_observability_contract`
- **Faiblesse révélée** : L'application contient une dépendance réseau implicite au runtime (ex. appel à un service de feedback externe). Aucun axe de validation ni signal d'observabilité ne couvre cet invariant constitutionnel. L'application est validée par la factory mais viole le runtime 100 % local.
- **Source du problème** : architecture (Points 1.1 et 1.2)

---

**Scénario C — Collision multi-IA sur scopes de projections dérivées non délimitées**

- **Déclencheur** : Deux IA travaillent en parallèle sur deux modules d'une application Learn-it. Chacune reçoit une projection dérivée distincte. Les deux projections couvrent partiellement les mêmes éléments du Référentiel (ex. le module MSC est dans les deux scopes déclarés différemment).
- **Mécanismes activés** : `multi_ia_parallel_readiness.minimum_requirements` (bounded_scopes) + absence de protocole d'assemblage
- **Faiblesse révélée** : Les deux IA produisent des outputs avec des interprétations divergentes des paramètres MSC. L'assemblage est impossible sans arbitrage humain non prévu. Le protocole d'assemblage entre sorties IA (`assembly_protocol_between_ai_outputs`) est listé comme `deferred_challenge` sans condition de déclenchement.
- **Source du problème** : state (Point 7.1) + architecture (Point 5.2 + Point 7.2)

---

**Scénario D — Promotion implicite d'un artefact platform_factory vers current sans gouvernance manifest**

- **Déclencheur** : Un cycle de patch est terminé. La version patchée de `platform_factory_architecture.yaml` est placée dans `docs/cores/current/` (STAGE_08). Le manifest officiel du repo n'est pas mis à jour (blockers reconnus : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`).
- **Mécanismes activés** : `pipeline.md Rule 6` (release et promotion distincts) + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Faiblesse révélée** : L'artefact promoté est "current" de facto mais pas "current" dans le manifest. Toute IA ou outil qui lit le manifest pour décider de la version canonique courante ignore la nouvelle version. La traçabilité entre release et état canonique est rompue.
- **Source du problème** : pipeline (Point 8.1) + manifest/release governance

---

## Risques prioritaires

| ID | Libellé | Gravité | Source |
|---|---|---|---|
| R01 | Contrat minimal d'application ne couvre pas les invariants constitutionnels critiques (runtime local, no-generation, no-AI-continuous) | Élevée | Points 1.1, 1.2, Scénario B |
| R02 | Projections dérivées déclarées utilisables comme seul artefact IA alors que leur validation n'est pas instrumentée | Élevée | Points 5.1, 9.3, Scénario A |
| R03 | Emplacement TBD des projections dérivées — risque de contamination de l'espace canonique | Élevée | Point 5.2 |
| R04 | Trou de gouvernance manifest : artefacts platform_factory dans current/ mais hors manifest officiel, sans procédure de fermeture | Élevée | Point 8.1, Scénario D |
| R05 | `canonical_dependency_contract` requis mais non schématisé — obligation creuse | Élevée | Point 4.1 |
| R06 | Maturité surdéclarée dans `capabilities_present` — auto-référence circulaire dans evidence | Modérée | Points 2.1, 6.1 |
| R07 | PF_CHAIN_05 en frontière factory/instanciation insuffisamment fermée | Modérée | Axe 3 |
| R08 | Multi-IA : exigences posées mais protocole d'assemblage absent — risque de collision | Modérée | Points 7.1, 7.2, Scénario C |
| R09 | Runtime_entrypoint_type non typé — obligation présente mais non auditable | Modérée | Point 4.2 |
| R10 | Double-buffer pour transformations internes factory non précisé | Modérée | Point 1.3 |
| R11 | Fingerprints factory eux-mêmes absents — incohérence avec exigences imposées aux applications | Modérée | Point 8.2 |
| R12 | Vocabulaire de maturité non normalisé entre labels par layer et verdict global | Faible | Point 2.3 |

---

## Points V0 acceptables

Les éléments suivants sont des incomplétudes V0 normales, reconnues, bornées, et sans risque immédiat critique :

- `PF_GAP_EXACT_YAML_SCHEMA_NOT_FINALIZED` : attendu en V0. La structure ne doit pas être challengée comme un défaut mais comme un point ouvert correctement reconnu.
- `PF_GAP_FACTORY_PIPELINE_NOT_MATERIALIZED` : le pipeline est présent comme gouvernance et intention. L'absence de tooling complet est normale en V0.
- `PF_GAP_VALIDATION_TOOLING_MISSING` : reconnu, borné, sans risque si l'usage de production est conditionné à la résolution.
- `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` : correctement reconnu comme défi différé.
- `capabilities_partial` sur manifest, runtime_entrypoint, configuration, validation, packaging, multi-IA : correctement catégorisées et cohérentes avec les blockers.
- `capabilities_absent` sur validators, pipeline complet, instanciation : correctement reconnues.
- `assessment_type: initial_baseline` et `result: foundational_but_incomplete` : honnêtes et calibrés.
- La séparation prescriptif/constatif entre les deux artefacts : solide et bien tenue.
- Les invariants `PF_INV_*` de l'architecture : bien formulés, couvrent les risques de duplication normative et de non-conformité des projections.
- Le `variant_governance` (allowed/forbidden variability) : clair et bien borné.

---

## Corrections à arbitrer avant patch

---

### [ARBIT-01] Ajouter un axe de validation constitutionnelle dans le contrat minimal d'application produite

- **Élément concerné** : `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : absence de binding explicite avec les invariants constitutionnels critiques
- **Type de problème** : compatibilité constitutionnelle + complétude
- **Gravité** : Élevée
- **Impact factory** : La factory peut valider une application non constitutionnellement conforme
- **Impact application produite** : Application peut violer runtime local, no-generation, no-AI sans être détectée
- **Impact IA** : Validation IA incomplète
- **Impact gouvernance/release** : Release factory peut certifier une fausse conformité
- **Correction à arbitrer** : Ajouter `constitutional_invariant_conformance` (ou équivalent) comme axe obligatoire dans `minimum_axes`, listant les invariants constitutionnels à démontrer
- **Lieu probable** : architecture

---

### [ARBIT-02] Interdire l'usage de projections dérivées comme seul artefact IA tant que le mécanisme de validation n'est pas instrumenté

- **Élément concerné** : `contracts.execution_projection_contract.rule_of_use` + `generated_projection_rules.emplacement_policy`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : mécanisme déclaré opérable mais non instrumenté
- **Type de problème** : gouvernance + implémentabilité
- **Gravité** : Élevée
- **Impact IA** : Risque de non-conformité normative silencieuse sur projections utilisées comme seul contexte
- **Impact gouvernance/release** : Validation de facto sans protocole
- **Correction à arbitrer** : Ajouter dans `execution_projection_contract` une condition préalable explicite : `single_context_usage_requires: [validator_defined, storage_location_decided, regeneration_protocol_defined]`. Et décider l'emplacement des projections.
- **Lieu probable** : architecture + pipeline

---

### [ARBIT-03] Schématiser minimalement le `canonical_dependency_contract`

- **Élément concerné** : `produced_application_minimum_contract.canonical_dependency_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : obligation requise mais creuse
- **Type de problème** : complétude + implémentabilité
- **Gravité** : Élevée
- **Impact application produite** : Contrat déclaré mais non auditable
- **Correction à arbitrer** : Définir les champs minimaux obligatoires (au moins : constitution_version, referentiel_version, link_version)
- **Lieu probable** : architecture

---

### [ARBIT-04] Définir la procédure de fermeture du gap manifest/release dans le pipeline

- **Élément concerné** : STAGE_08_FACTORY_PROMOTE_CURRENT + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation** : `pipeline.md` + `platform_factory_state.yaml`
- **Nature** : trou de gouvernance entre current et manifest officiel
- **Type de problème** : gouvernance + traçabilité
- **Gravité** : Élevée
- **Impact gouvernance/release** : Promotion implicite non gouvernée possible
- **Correction à arbitrer** : Définir dans STAGE_08 la procédure de mise à jour du manifest lors d'une promotion, ou créer un manifest platform_factory dédié en attendant l'évolution du schema core
- **Lieu probable** : pipeline + manifest/release governance

---

### [ARBIT-05] Requalifier les `capabilities_present` ne disposant pas d'evidence d'implémentation

- **Élément concerné** : `capabilities_present` dans `platform_factory_state.yaml`
- **Localisation** : `platform_factory_state.yaml`
- **Nature** : maturité surdéclarée / auto-référence circulaire dans evidence
- **Type de problème** : faux niveau de maturité
- **Gravité** : Modérée
- **Impact IA** : Surestimation de la maturité par une IA qui consulte l'état
- **Correction à arbitrer** : Introduire un attribut `evidence_level` (déclaratif / défini / opérationnel) sur chaque capacité, ou requalifier les capacités sans evidence instrumentée en `declared_only`
- **Lieu probable** : state

---

### [ARBIT-06] Clarifier le statut de PF_CHAIN_05 par rapport à la frontière factory/instanciation

- **Élément concerné** : `transformation_chain.phases[PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS]`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : frontière de couche insuffisamment fermée
- **Type de problème** : cohérence architecturale + implémentabilité
- **Gravité** : Modérée
- **Correction à arbitrer** : Redéfinir PF_CHAIN_05 comme un "point de délégation" avec interface formalisée vers le pipeline aval, ou l'extraire de la transformation_chain factory
- **Lieu probable** : architecture

---

### [ARBIT-07] Conditionner l'usage multi-IA à la résolution du protocole d'assemblage

- **Élément concerné** : `multi_ia_parallel_readiness.deferred_challenges`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Nature** : exigence de premier rang non opérationnalisée
- **Type de problème** : implémentabilité + gouvernance
- **Gravité** : Modérée (conditionnelle)
- **Correction à arbitrer** : Décider si la V0→V1 inclut la définition minimale d'un protocole d'assemblage. Si différé, poser une condition de blocage explicite sur l'usage multi-IA en production.
- **Lieu probable** : state (gap) + architecture (protocole minimal)

---

*Fin du rapport de challenge PFCHAL_20260408_PERPL_X7T2*
