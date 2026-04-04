# Challenge Report — Platform Factory Baseline V0.1

## challenge_run_id

`PFCHAL_20260404_PERP_K7X2`

## Date

2026-04-04

## Agent

PERP (Perplexity AI — Sonnet 4.6)

---

## Artefacts challengés

| Artefact | artifact_id | version | status |
|---|---|---|---|
| `docs/cores/current/platform_factory_architecture.yaml` | PLATFORM_FACTORY_ARCHITECTURE_V0_1 | 0.1.0 | CURRENT_V0 |
| `docs/cores/current/platform_factory_state.yaml` | PLATFORM_FACTORY_STATE_V0_1 | 0.1.0 | CURRENT_V0 |

## Socle canonique lu

| Core | id | version |
|---|---|---|
| Constitution | CORE_LEARNIT_CONSTITUTION_V2_0 | V2_0_FINAL |
| Référentiel | CORE_LEARNIT_REFERENTIEL_V2_0 | V2_0_FINAL |
| LINK | CORE_LINK_LEARNIT_CONSTITUTION_V2_0__REFERENTIEL_V2_0 | V2_0__V2_0_FINAL |

## Pipeline lu

`docs/pipelines/platform_factory/pipeline.md`

---

## Résumé exécutif

La baseline V0.1 de la Platform Factory présente une fondation conceptuelle cohérente et bien bornée. Elle est constitutionnellement compatible sur l'essentiel : séparation prescriptif/constatif, non-duplication de la norme, traçabilité explicite, exigence multi-IA reconnue comme premier rang. Elle est saine pour lancer STAGE_02_FACTORY_ARBITRAGE.

Cependant, elle présente **six familles de risques réels** qui méritent arbitrage avant tout patch :

1. **Sous-spécification structurée des schémas** : les contrats manifest, configuration, packaging et runtime entrypoint sont définis en intention mais pas en schéma fin. Ceci n'est pas en soi une faiblesse constitutionnelle, mais c'est un bloqueur d'implémentabilité réelle du pipeline.
2. **Absence de localisation des validated_derived_execution_projections** : la règle d'usage est posée mais `emplacement_policy: status: TBD` crée une zone de non-décision qui compromet la multi-IA readiness opérationnelle.
3. **Absence de protocole d'assemblage des sorties IA** : la multi-IA readiness est déclarée exigence mais le protocole d'assemblage n'existe pas encore, ce qui rend la promesse non tenue au niveau opérationnel.
4. **Tension entre maturité reconnue et maturité réelle** : le state décrit fidèlement les lacunes (c'est un point fort), mais il ne contient pas de critères de sortie explicites vers V0.2, ce qui rend le pilotage de maturité difficile.
5. **Absence d'un manifest_schema formalisé** : le contrat minimal d'application est défini à haut niveau mais l'absence de schéma fin expose à une divergence silencieuse entre applications produites.
6. **Pipeline partiellement instrumenté** : plusieurs prompts partagés référencés dans `pipeline.md` ne sont pas encore confirmés présents ou complets, ce qui rend le pipeline non entièrement exécutable à ce stade.

---

## Carte de compatibilité constitutionnelle

| Axe constitutionnel | Évaluation | Notes |
|---|---|---|
| Non-duplication de la norme | ✅ CONFORME | PF_INV_FACTORY_DOES_NOT_DUPLICATE_NORM explicitement déclaré et respecté |
| Séparation Constitution/Référentiel | ✅ CONFORME | Binding via LINK_CORE, références explicites uniquement |
| Traçabilité inter-core | ✅ CONFORME | `dependencies_to_constitution/referentiel/link` présents |
| Autorité canonique primaire | ✅ CONFORME | `authority_rule: canonical_dependencies_remain_primary_authority` |
| Déterminisme des transformations | ✅ CONFORME déclaré / ⚠️ non instrumenté | PF_PRINCIPLE_DETERMINISTIC_TRANSFORMATIONS posé mais pas toolé |
| Projections dérivées strictement conformes | ✅ CONFORME en règle / ⚠️ non validé outillage | Règles posées, validator absent |
| Manifest obligatoire | ✅ CONFORME en principe / ⚠️ schéma absent | `no_application_without_manifest` déclaré, schema non finalisé |
| Multi-IA readiness | ✅ CONFORME comme exigence / ⚠️ non opérationnalisé | Premier rang déclaré, protocole assemblage absent |
| Séparation générique/spécifique | ✅ CONFORME | `forbidden_variability` bien borné |
| Inhibition de dérive normative | ✅ CONFORME | `no_derived_projection_with_normative_drift` dans constraints |

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

**Résultat : CONFORME**

L'architecture ne redéfinit pas la Constitution. Elle référence explicitement les trois cores canoniques via `source_of_authority.canonical_dependencies`. La séparation des couches est bien matérialisée dans `platform_layers`. Le principe `PF_PRINCIPLE_NO_NORM_DUPLICATION` est posé et cohérent avec `INV_CONSTITUTION_REFERENTIAL_SEPARATION` du Core Constitution.

Aucune règle constitutionnelle n'est contradite ou ignorée. La factory ne tente pas de modifier la logique AND du MSC, la propagation 1-saut, ni la philosophie adaptative.

### Axe 2 — Cohérence interne architecture/state

**Résultat : COHÉRENT avec tensions de complétude**

L'architecture et le state sont mutuellement cohérents sur :
- La liste des couches (`platform_layers` dans architecture vs `maturity_by_layer` dans state)
- Les capacités présentes/partielles/absentes qui correspondent aux `open_points_for_challenge` de l'architecture
- Les décisions validées (`validated_decisions`) qui reflètent des choix architecturaux posés

**Tensions relevées :**

T1 — L'architecture déclare `emplacement_policy: status: TBD` pour les projections dérivées. Le state enregistre `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` comme `capabilities_absent`. C'est cohérent dans le constat mais la TBD n'est pas accompagnée d'un critère de clôture dans aucun des deux artefacts.

T2 — L'architecture déclare `PF_PRINCIPLE_REGENERABLE_EXECUTION_PROJECTIONS` comme principe actif, mais le state indique `derived_projection_conformity_status: status: defined_in_principle_not_yet_tooling_backed`. La cohérence principe/état est correctement nommée, mais elle n'est pas accompagnée d'une borne de résolution.

T3 — Le state (`multi_ia_parallel_readiness_status`) liste 4 éléments présents et 4 absents. L'absence de `decomposition_protocol` et `conflict_resolution_protocol` signifie qu'un travail multi-IA aujourd'hui pourrait produire des conflits d'assemblage non gouvernés.

### Axe 3 — Frontières de couche

**Résultat : BIEN DÉFINI avec un point de vigilance**

La séparation `PF_LAYER_CANONICAL_FOUNDATION` / `PF_LAYER_FACTORY_ARCHITECTURE` / `PF_LAYER_FACTORY_STATE` / `PF_LAYER_DERIVED_EXECUTION_PROJECTIONS` / `PF_LAYER_APPLICATION_INSTANTIATION` est claire et explicite.

**Point de vigilance :**

Le pipeline.md référence des prompts partagés dans `docs/prompts/shared/` (Challenge_platform_factory.md, Make21 à Make24) comme instruments de pipeline. Ces prompts sont hors scope de la factory architecture et du factory state, mais leur existence conditionne l'exécutabilité réelle du pipeline. Leur absence ou incomplétude crée une dépendance non gouvernée par le pipeline lui-même.

La limite `out_of_scope` est bien formalisée dans architecture et state — aucune contamination domaine-spécifique détectée.

### Axe 4 — Contrat minimal d'application produite

**Résultat : POSÉ MAIS INCOMPLÈTEMENT SPÉCIFIÉ**

Le contrat est défini à haut niveau avec les blocs attendus :
- `identity` ✅
- `manifest_principle` ✅
- `canonical_dependency_contract` ✅
- `runtime_entrypoint_principle` ✅
- `minimum_configuration_blocks` ✅
- `minimum_validation_axes` ✅
- `minimum_packaging_principle` ✅
- `minimum_observability` ✅

**Manquants (dans state, `produced_application_contract_status.missing`) :**
- `exact_manifest_schema` — sans cela, la conformité d'une application produite ne peut pas être vérifiée mécaniquement
- `exact_runtime_typology` — l'entrypoint runtime est obligatoire (`required: true`) mais sa typologie n'est pas définie, ce qui expose à une interprétation divergente entre IAs
- `exact_configuration_schema` — même risque
- `exact_packaging_schema` — même risque

**Impact critique :** deux IAs travaillant en parallèle sur l'instanciation d'applications pourraient produire des manifests structurellement incompatibles en l'état actuel.

### Axe 5 — Validated derived execution projections

**Résultat : RÈGLE POSÉE, MÉCANISME ABSENT**

Le contrat `execution_projection_contract` est bien défini dans architecture. Les invariants (no_new_rule, no_normative_divergence, no_omission_within_declared_scope, canonical_source_remains_primary_authority, deterministic_regeneration_required) sont corrects et constitutionnellement compatibles.

**Lacunes structurelles :**
- Pas de validator défini ou implémenté (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent`)
- Pas d'emplacement de stockage défini (`emplacement_policy: TBD`)
- Pas de protocole de régénération défini

En l'état, la règle est présente mais **non vérifiable** et **non appliquée mécaniquement**. Une IA pourrait produire une projection avec dérive normative non détectée.

### Axe 6 — Maturité reconnue vs maturité réelle

**Résultat : HONNÊTE MAIS SANS CRITÈRES DE SORTIE**

Le state est un point fort de la baseline : il est auto-critique, liste explicitement les `capabilities_absent`, `blockers` et `known_gaps`. L'assessment `foundational_but_incomplete` est exact et approprié.

**Ce qui manque :**
- Aucun critère de progression de V0 vers V0.2 ou V1 n'est défini dans aucun des deux artefacts
- Aucun `target_maturity_by_layer` n'est déclaré
- Aucune borne temporelle ou d'événement déclencheur de révision du state n'est présente

Sans ces critères, le state risque de rester `foundational_but_incomplete` indéfiniment sans signal explicite de progression.

### Axe 7 — Multi-IA parallel readiness

**Résultat : EXIGENCE DE PREMIER RANG POSÉE, OPÉRATIONNALISATION ABSENTE**

`PF_PRINCIPLE_MULTI_IA_READY` et `PF_DECISION_MULTI_IA_FIRST_CLASS` sont correctement déclarés. Les `minimum_requirements` dans `multi_ia_parallel_readiness` sont bien listés.

**Gaps critiques :**
- `decomposition_protocol` absent : comment diviser un travail factory entre plusieurs IAs n'est pas défini
- `module_granularity_convention` absent : la granularité des modules réutilisables n'est pas fixée, rendant le découpage parallèle non déterministe
- `ai_output_assembly_protocol` absent : comment assembler les sorties de plusieurs IAs sans conflit n'est pas défini
- `conflict_resolution_protocol` absent : en cas de sorties contradictoires entre IAs, aucune règle de résolution n'existe

En l'état, lancer un travail multi-IA réel expose à des divergences d'assemblage non gouvernées.

### Axe 8 — Gouvernance release / manifest / traçabilité

**Résultat : PRINCIPE CORRECT, SCHEMA MANQUANT**

La règle `Rule 6 — Release and promotion are distinct acts` est correcte et cohérente avec l'architecture. Les stages 07 et 08 du pipeline sont correctement séparés. Le principe `no_application_without_manifest` est posé.

**Tensions :**
- L'architecture note que les artefacts V0 sont dans `docs/cores/current/` mais **hors manifest officiel actuel** (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`). Ce bloqueur est bien nommé mais non résolu. Il crée une ambiguïté sur le statut "current" réel des artefacts.
- Le schema de manifest d'application final n'est pas défini → impossible de vérifier mécaniquement la traçabilité d'une application produite.

### Axe 9 — Implémentabilité du pipeline

**Résultat : PARTIELLEMENT IMPLÉMENTABLE**

Les stages 01 à 06 sont suffisamment définis pour être exécutés avec les prompts partagés. Les stages 07 (Release) et 08 (Promote) renvoient à des specs détaillées dans `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md` — dont l'existence et la complétude n'ont pas été vérifiées dans ce challenge (hors scope de la lecture requise).

**Risque de non-implémentabilité :**
- 5 prompts partagés référencés (`Challenge_platform_factory.md`, `Make21` à `Make24`) — leur présence dans `docs/prompts/shared/` n'a pas été vérifiée
- `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE: absent` dans state confirme ce risque
- Stage 05 (`STAGE_05_FACTORY_APPLY`) n'a pas de prompt requis (`none required`) — c'est correct pour une étape technique pure, mais cela suppose un outillage ou une procédure manuelle documentée qui n'est pas précisée

### Axe 10 — Scénarios adversariaux plausibles

**SA-01 — Dérive silencieuse de projection**
Une IA reçoit une `validated_derived_execution_projection` déclarée conforme mais produite sans validator. Elle produit un artefact avec une règle implicite ajoutée. L'absence de validator déterministe rend cette dérive indétectable mécaniquement.
→ Impact : violation de `no_new_rule` et `no_normative_divergence` sans détection.

**SA-02 — Manifests incompatibles entre IAs parallèles**
Deux IAs reçoivent un scope bounded et produisent chacune un manifest pour une application. En l'absence de `exact_manifest_schema`, leurs structures sont incompatibles. L'assemblage échoue ou produit un manifest hybride non conforme.
→ Impact : violation de `PF_INV_MINIMUM_APPLICATION_CONTRACT_MUST_ALWAYS_BE_DECLARED`.

**SA-03 — Promotion prématurée**
Un opérateur confond la fin du stage 05 (patched state en sandbox) avec la fin du stage 08 (promoted to current). Les artefacts V0.1 patched sont promus sans passer par les stages 06-07-08.
→ Impact : violation de `Rule 6 — Release and promotion are distinct acts` et `no file in docs/cores/current/ may be modified directly before explicit promotion`.

**SA-04 — Régression de maturité non détectée**
Le state V0.1 est remplacé par un état patchté qui améliore certains blocs mais dégrade silencieusement la description de `capabilities_absent`. Une lacune critique disparaît du state sans avoir été résolue.
→ Impact : perte d'intégrité du constat; le state ne reflète plus la réalité.

**SA-05 — Pipeline exécuté sur des prompts manquants**
Un agent lance STAGE_03_FACTORY_PATCH_SYNTHESIS en utilisant un prompt approximatif parce que `Make22PlatformFactoryPatch.md` n'est pas encore présent. Le patchset produit ne respecte pas le cadre contractuel.
→ Impact : invalidation du patchset lors du STAGE_04.

### Axe 11 — Priorisation des risques

| Priorité | Risque | Gravité | Impact IA | Impact factory |
|---|---|---|---|---|
| P1 | Absence de validator pour projections dérivées | HAUTE | Dérive normative non détectable | Projections non fiables |
| P1 | Absence de manifest schema finalisé | HAUTE | Manifests incompatibles entre IAs | Contrat minimal non vérifiable |
| P2 | Absence de decomposition + assembly protocol multi-IA | MOYENNE-HAUTE | Conflits d'assemblage | Multi-IA non opérationnel |
| P2 | TBD sur emplacement projections | MOYENNE | Projections non localisables | Pipeline partiellement exécutable |
| P3 | Absence de critères de sortie de maturité V0→V1 | MOYENNE | Pas de signal de progression | Gouvernance de maturité absente |
| P3 | Prompts partagés non vérifiés | MOYENNE | Stages non exécutables | Pipeline bloqué en aval |
| P4 | Bloqueur manifest schema limitation (current vs. manifest) | BASSE-MOYENNE | Ambiguïté statut current | Traçabilité partielle |

---

## Points V0 acceptables

Les éléments suivants sont **acceptables comme état V0** et ne nécessitent pas de patch immédiat :

- `exact_manifest_schema`, `exact_runtime_typology`, `exact_configuration_schema`, `exact_packaging_schema` : leur absence est correctement reconnue dans le state et dans `open_points_for_challenge`. C'est l'objet des prochains cycles.
- `PF_LAYER_APPLICATION_INSTANTIATION: boundary_defined_only` : normal pour un V0, le pipeline aval n'est pas encore l'objet de cette release.
- `deferred_challenges` dans `multi_ia_parallel_readiness` (`optimal_module_granularity`, `optimal_projection_size`, `assembly_protocol_between_ai_outputs`) : correctement marqués comme deferred.
- L'absence de tooling pipeline complet : la V0 est explicitement déclarée skeleton.
- La non-intégration au manifest officiel actuel : correctement enregistrée comme bloqueur medium.

---

## Corrections à arbitrer avant patch

### C1 — Définir et localiser le validator de projections dérivées

- **Élément concerné :** `contracts.execution_projection_contract`
- **Localisation :** `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Nature :** absence d'un mécanisme de validation déterministe
- **Type :** lacune structurelle de gouvernance
- **Gravité :** HAUTE
- **Impact factory :** les projections produites sont non vérifiables mécaniquement
- **Impact application produite :** les applications peuvent être produites à partir de projections avec dérive normative non détectée
- **Impact IA :** une IA ne peut pas savoir si la projection qu'elle reçoit est réellement conforme
- **Impact gouvernance/release :** la promotion d'une projection comme "validated" n'est pas outillée
- **Correction à arbitrer :** définir un `validator_definition` minimal dans l'architecture + décider d'un emplacement de stockage dans le state ; mettre à jour `derived_projection_conformity_status`
- **Lieu probable :** architecture (définition) + state (statut) + validator/tooling

---

### C2 — Décider l'emplacement des validated_derived_execution_projections

- **Élément concerné :** `generated_projection_rules.emplacement_policy`
- **Localisation :** `platform_factory_architecture.yaml`
- **Nature :** TBD non résolu bloquant l'opérationnalisation
- **Type :** décision d'architecture non prise
- **Gravité :** MOYENNE-HAUTE
- **Impact factory :** les projections ne peuvent pas être produites et stockées de façon stable
- **Impact IA :** les IAs ne savent pas où trouver/déposer les projections
- **Impact gouvernance/release :** la traçabilité des projections est impossible sans emplacement fixe
- **Correction à arbitrer :** décider d'un chemin de stockage (ex. `docs/pipelines/platform_factory/projections/` ou dossier dédié) et mettre à jour `emplacement_policy`
- **Lieu probable :** architecture + state (capability)

---

### C3 — Poser un protocole minimal d'assemblage multi-IA

- **Élément concerné :** `multi_ia_parallel_readiness`
- **Localisation :** `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Nature :** absence de `decomposition_protocol` et `ai_output_assembly_protocol`
- **Type :** lacune opérationnelle de la première exigence de rang
- **Gravité :** MOYENNE-HAUTE
- **Impact IA :** deux IAs parallèles peuvent produire des sorties non assemblables
- **Impact factory :** la promesse multi-IA de premier rang reste non tenue
- **Impact gouvernance :** aucun arbitrage possible en cas de conflits entre sorties IA
- **Correction à arbitrer :** définir dans architecture un bloc `multi_ia_decomposition_minimum_protocol` avec au minimum les règles de découpage de scope, d'identification des sorties et de point d'assemblage ; mettre à jour le state
- **Lieu probable :** architecture (section `multi_ia_parallel_readiness`) + state

---

### C4 — Ajouter des critères de sortie de maturité par couche

- **Élément concerné :** `maturity_by_layer` + `last_assessment`
- **Localisation :** `platform_factory_state.yaml`
- **Nature :** absence de critères de progression vers l'état suivant
- **Type :** lacune de gouvernance de maturité
- **Gravité :** MOYENNE
- **Impact factory :** impossible de savoir quand la factory passe de V0 à une version plus mature sans décision ad hoc
- **Impact gouvernance :** risque de drift silencieux de maturité
- **Correction à arbitrer :** ajouter pour chaque couche un bloc `exit_criteria` ou `next_maturity_target` minimal ; ou déclarer explicitement que les critères de progression seront gouvernés dans une décision séparée
- **Lieu probable :** state

---

### C5 — Vérifier et formaliser l'existence des prompts partagés requis

- **Élément concerné :** `Required shared prompts` dans pipeline.md
- **Localisation :** pipeline.md + `docs/prompts/shared/`
- **Nature :** dépendance non vérifiée à des artefacts externes au pipeline
- **Type :** risque d'exécutabilité
- **Gravité :** MOYENNE
- **Impact IA :** un agent ne peut pas exécuter un stage si le prompt requis est absent ou incomplet
- **Impact pipeline :** blocage silencieux possible en STAGE_02 à STAGE_04
- **Correction à arbitrer :** vérifier l'existence et la complétude de chaque prompt ; si manquant, créer un stub ou un `PROMPT_MISSING` flag dans PROMPT_USAGE.md
- **Lieu probable :** hors périmètre factory (concerne le repo prompts), mais à gouverner dans pipeline.md

---

### C6 — Clarifier le statut "current" des artefacts V0 vis-à-vis du manifest

- **Élément concerné :** `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation :** `platform_factory_state.yaml`
- **Nature :** les artefacts sont dans `docs/cores/current/` mais hors du manifest officiel
- **Type :** ambiguïté de gouvernance release
- **Gravité :** BASSE-MOYENNE
- **Impact gouvernance :** le statut "current" est ambigu ; un agent pourrait traiter ces artefacts différemment selon son interprétation
- **Correction à arbitrer :** soit étendre le manifest pour intégrer les artefacts platform_factory, soit documenter explicitement dans le state que le manifest extension est l'objet d'un futur STAGE_07
- **Lieu probable :** manifest/release governance + state

---

## Résultat terminal

**challenge_run_id :** `PFCHAL_20260404_PERP_K7X2`

**Fichier écrit :** `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md`

**Résumé ultra-court :** Baseline V0.1 constitutionnellement compatible et honnête dans son auto-diagnostic. 6 corrections à arbitrer avant patch : validator projections, emplacement projections, protocole multi-IA, critères de sortie maturité, vérification prompts, clarification statut current/manifest. Exploitable pour STAGE_02_FACTORY_ARBITRAGE.
