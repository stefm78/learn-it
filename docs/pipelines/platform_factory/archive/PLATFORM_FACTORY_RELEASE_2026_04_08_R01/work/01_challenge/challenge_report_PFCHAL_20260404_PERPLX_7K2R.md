# Challenge Report — Platform Factory

## Métadonnées

| Champ | Valeur |
|---|---|
| **title** | Challenge Report — Platform Factory Baseline V0 |
| **challenge_run_id** | PFCHAL_20260404_PERPLX_7K2R |
| **date** | 2026-04-04 |
| **stage** | STAGE_01_CHALLENGE |
| **pipeline** | docs/pipelines/platform_factory/pipeline.md |
| **prompt principal** | docs/prompts/shared/Challenge_platform_factory.md |
| **posture** | Challenge d'une baseline released en current — pas un audit de découverte |

---

## Artefacts challengés

| Artefact | Rôle | Statut |
|---|---|---|
| `docs/cores/current/platform_factory_architecture.yaml` (PLATFORM_FACTORY_ARCHITECTURE_V0_1) | Prescriptif générique | CURRENT_V0 |
| `docs/cores/current/platform_factory_state.yaml` (PLATFORM_FACTORY_STATE_V0_1) | Constatif | CURRENT_V0 |
| `docs/pipelines/platform_factory/pipeline.md` | Gouvernance d'exécution | V0 skeleton |

Artefacts de référence lus :
- `docs/cores/current/constitution.yaml` (CORE_LEARNIT_CONSTITUTION_V2_0)
- `docs/cores/current/referentiel.yaml` (CORE_LEARNIT_REFERENTIEL_V2_0)
- `docs/cores/current/link.yaml` (CORE_LINK_LEARNIT_CONSTITUTION_V2_0__REFERENTIEL_V2_0)

---

## Résumé exécutif

La Platform Factory V0 pose une base conceptuelle et architecturale crédible pour lancer sa gouvernance. La séparation prescriptif/constatif est correctement tenue, le principe de non-duplication normative est déclaré, et l'exigence multi-IA est explicitement formulée.

Cependant, **cinq zones de risque sérieux émergent** :

1. **La conformité constitutionnelle d'une application produite n'est pas vérifiable de bout en bout** : le contrat minimal d'application ne contient aucune obligation explicite et auditabie de compatibilité avec `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` et `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`. Une application produite pourrait paraître valide selon le contrat factory tout en violant ces invariants constitutionnels forts.

2. **Les `validated_derived_execution_projections` ne sont pas opérationnalisées** : aucun stockage, aucun validateur, aucun protocole de régénération. L'usage autorisé ("unique artefact fourni à une IA") repose donc sur un mécanisme déclaré mais non instrumenté, ce qui ouvre un risque de dérive normative silencieuse.

3. **La maturité déclarée dans `platform_factory_state.yaml` surdéclare partiellement la situation réelle** : plusieurs `capabilities_present` sont en réalité des intentions correctement posées mais sans schéma, validateur, ni preuve tangible.

4. **Le protocole d'assemblage multi-IA est absent** : la granularité modulaire, la résolution de conflits d'assemblage et le protocole de coordination entre sorties IA parallèles ne sont pas définis. La factory pourrait produire des fragments incompatibles sans mécanisme de détection.

5. **La gouvernance release est insuffisamment fermée** : les artefacts platform_factory sont dans `docs/cores/current/` mais explicitement hors manifest officiel actuel. La frontière entre "artefact current posé" et "artefact officiellement dans le dispositif de release" est un trou de gouvernance documenté mais non résolu.

Ces cinq points sont les **corrections à arbitrer avant patch** les plus critiques. Ils ne remettent pas en cause la viabilité de la V0, mais ils doivent être traités pour permettre un cycle crédible de correction et d'exploitation.

---

## Carte de compatibilité constitutionnelle

### Invariants constitutionnels touchés directement par la factory

| Invariant constitutionnel | Élément factory concerné | Binding | Risque |
|---|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | Contrat minimal application — section `minimum_observability_contract` | **Absent** dans le contrat factory | Une application produite pourrait introduire un appel réseau non détecté par la factory |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | Contrat minimal — manifest, validation minimale | **Absent** explicitement | La factory ne requiert pas de preuve d'absence de génération runtime dans le manifest de l'application produite |
| `INV_NO_RUNTIME_FEEDBACK_GENERATION` (CONSTRAINT) | Contrat minimal — section feedback/validation | **Absent** | La factory ne pose pas d'axe de validation spécifique à ce point |
| `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` | Architecture factory — transformation chain, validation | **Implicite faible** (mentionné dans les principes, non contraint dans le contrat applicatif) | Une application produite pourrait implémenter un patch partiel ou en-session sans que la factory le détecte |
| `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | Contrat minimal — `minimum_validation_contract` | **Absent** explicitement | L'axe validation minimale ne mentionne pas l'exigence de déterminisme local |
| `INV_NO_PARTIAL_PATCH_STATE` | Contrat minimal — packaging, validation | **Absent** | Aucun axe de validation ne contrôle l'atomicité des patchs dans l'application produite |
| `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | Architecture factory — `PF_PRINCIPLE_NO_NORM_DUPLICATION` | **Explicite** — solide | Risque faible ici |
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Hors scope direct de la factory (domaine) | **N/A direct** mais non mentionné dans le contrat application comme exigence de validation | Une projection dérivée couvrant le graphe pourrait omettre cette contrainte |
| `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | `validated_derived_execution_projections` — invariants du contrat | **Implicite** via `no_normative_divergence` | Une projection qui paraphrase la règle sans citer l'invariant crée un risque d'omission |
| `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` | Projections dérivées — scope et contenu | **Absent** | Une projection pourrait implicitement autoriser une inférence IA locale non prévue |
| `INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN` | Contrat application — aucune mention | **Absent** | Application produite pourrait traiter la détresse sans respecter la priorité structurelle |

### Résumé de posture

- **Bindings explicites et solides** : séparation Constitution/Référentiel (PF_PRINCIPLE_NO_NORM_DUPLICATION), dépendance canonique déclarée.
- **Bindings implicites mais faibles** : runtime local, patch off-session (mentionnés dans les principes d'architecture, non répercutés dans le contrat application ni dans les axes de validation minimale).
- **Bindings absents et risqués** : déterminisme de validation locale, absence de génération runtime, atomicité des patchs, conformité des projections dérivées vis-à-vis des invariants de sécurité.

---

## Analyse détaillée par axe

---

### Axe 1 — Compatibilité constitutionnelle

**Point solide :** La dépendance canonique est déclarée (`source_of_authority`, `dependencies_to_constitution`). Le principe de non-duplication normative est posé. La factory ne tente pas de réécrire la Constitution.

**Zone de risque principale :** Le `produced_application_minimum_contract` ne projette pas les invariants constitutionnels de sécurité critique dans ses axes de validation. En particulier :
- `minimum_validation_contract.minimum_axes` liste : structure, minimum_contract_conformance, traceability, packaging — **mais pas** : local_runtime_conformance, no_runtime_generation, deterministic_patch_validation.
- `minimum_observability_contract.minimum_signals` ne contient aucun signal permettant d'auditer l'absence d'appel réseau ou de génération runtime.

**Conséquence :** Une application produite conforme au contrat factory n'est pas nécessairement conforme à la Constitution sur ses invariants les plus critiques. La factory crée un faux sentiment de complétude de validation.

**Angle mort :** La factory ne pose aucune exigence que le manifest de l'application produite référence explicitement les invariants constitutionnels applicables (par ID). Sans cette traçabilité, un auditeur ou une IA ne peut pas vérifier la conformité constitutionnelle par lecture du seul manifest.

---

### Axe 2 — Cohérence interne de la factory

**Contradictions identifiées :**

1. `platform_factory_architecture.yaml` déclare `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` comme capacité présente dans le state. Or le state lui-même note : `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` est **absent**. L'architecture dit "intent défini = capacité présente" ; le state dit "pas complètement matérialisé". La nuance est correcte mais la frontière entre ces deux déclarations est floue — une IA lisant le state seul pourrait conclure que le pipeline est opérationnel.

2. La section `generated_projection_rules.emplacement_policy` porte le statut `TBD` dans l'architecture. Le state dit que `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` est **absent**. C'est cohérent. Mais le contrat des projections dérivées autorise déjà leur usage comme "unique artefact fourni à une IA" — **alors que le lieu de stockage et le validateur n'existent pas encore**. C'est une inversion de séquence : le droit d'usage est déclaré avant que les gardes-fous d'usage soient posés.

3. `platform_factory_architecture.yaml` liste `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` comme invariant. Mais aucun mécanisme de vérification de cet invariant n'est présent ou même partiellement instrumenté. L'invariant est déclaré, non garanti.

**Séparation prescriptif / constatif :** Correctement tenue. Pas de contamination entre les deux artefacts.

**Séparation générique / spécifique :** Correctement tenue dans les déclarations. Risque résiduel : la factory ne contraint pas comment une projection dérivée indique quels éléments relèvent du générique vs du domaine — ce point sera un angle mort pour le pipeline d'instanciation.

---

### Axe 3 — Portée et frontières

**Point solide :** La factory délimite explicitement son périmètre (in_scope / out_of_scope dans l'architecture, assessed_scope dans le state). La frontière avec le futur pipeline d'instanciation est correctement identifiée. Aucune absorption visible de logique métier domaine.

**Zone de risque :** La factory déclare gouverner `validated_derived_execution_projections` mais n'a pas encore défini la règle qui dit **quelle IA produit** ces projections, **quand**, **avec quel prompt**, et **qui les valide**. La frontière entre "la factory produit des projections" et "une IA externe produit une projection pour la factory" est floue. Cela crée un risque de confusion de responsabilité en contexte multi-IA.

**Angle mort :** Le `pipeline.md` gouverne la factory comme couche. Mais rien n'indique qui gouverne les projections produites *par* la factory pour d'autres pipelines. C'est un trou de gouvernance entre la factory et ses consommateurs aval.

---

### Axe 4 — Contrat minimal d'une application produite

**Obligations manquantes (critiques) :**

- **Absence de déclaration explicite de conformité aux invariants constitutionnels de runtime** : le contrat n'oblige pas l'application produite à déclarer dans son manifest que `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION` et `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` ont été vérifiés.
- **Absence d'axe de validation `local_runtime_conformance`** : les `minimum_axes` de validation ne couvrent pas ce point.
- **Absence d'axe de validation `deterministic_patch_path`** : aucune validation ne porte sur le fait que le chemin de patch de l'application produite satisfait `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.
- **Absence de traçabilité des projections dérivées utilisées dans la validation** : `minimum_observability_contract` mentionne `derived_projections_used` — mais aucune obligation de vérifier que ces projections étaient à jour et strictement conformes au moment de leur usage.

**Obligations trop floues :**

- `runtime_entrypoint_contract` déclare des champs obligatoires (`runtime_entrypoint_id`, `bootstrap_contract`, etc.) mais sans schéma ni contrainte sur leur contenu. Une IA produisant un manifest peut remplir ces champs de façon formellement conforme mais sémantiquement vide.
- `minimum_configuration_contract` liste des blocs (`identity`, `module_activation`, etc.) sans définir ce que chacun doit minimalement contenir pour être validable.

**Obligations mal placées :**

- La factory déclare `generic_module_reuse_contract` comme obligatoire mais ne définit pas encore les modules génériques disponibles. Cette obligation est prématurée — elle ne peut pas être vérifiée tant que les modules ne sont pas définis.

**Obligations non auditables :**

- `minimum_validation_contract` impose un axe `structure` sans définir ce que "structure valide" signifie dans ce contexte. Un validateur ne peut pas implémenter ce critère.

---

### Axe 5 — Validated derived execution projections

**Risques identifiés :**

1. **Risque de divergence normative silencieuse** : l'invariant `no_normative_divergence` est déclaré mais non instrumenté. Une projection produite par paraphrase peut rater une nuance d'un invariant constitutionnel (ex. : `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` dont le libellé est subtil). Aucun test de régression n'est défini.

2. **Risque d'omission dans le scope déclaré** : l'invariant `no_omission_within_declared_scope` est correct en intention mais il n'existe pas de liste de référence des éléments qui doivent figurer dans une projection pour un scope donné. Un générateur de projection ne sait pas quand il a tout couvert.

3. **Risque de promotion implicite** : `prohibited` liste `promotion_as_primary_canonical_artifact`. Mais sans mécanisme de marquage clair des projections dérivées dans les artefacts produits, une IA consommatrice peut traiter une projection comme source primaire sans que rien ne l'en empêche.

4. **Risque lié à l'absence de stockage** : `emplacement_policy.status = TBD`. Si plusieurs IA génèrent des projections pour un même scope et les stockent différemment, il n'existe pas de mécanisme pour détecter les doublons ou les projections obsolètes.

5. **Risque de régénération non déterministe** : l'invariant `deterministic_regeneration_required` est déclaré mais le protocole de régénération n'existe pas. Deux régénérations successives par deux IA différentes pourraient produire des projections légèrement différentes, sans qu'aucune soit détectée comme divergente.

6. **Risque majeur de principe autorisé avant garde-fous** : la factory autorise déjà qu'une projection soit "l'unique artefact fourni à une IA pour un travail donné" — mais les trois conditions de sécurité (validateur, stockage, protocole de régénération) sont toutes `absent` ou `TBD`. C'est le risque le plus important de cet axe.

---

### Axe 6 — État reconnu, maturité et preuves

**Cohérence interne du state :**

- `validated_decisions` : 5 décisions cohérentes, bien documentées. Pas de sur-déclaration.
- `capabilities_present` : 5 capacités listées. **Surdéclaration partielle** :
  - `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` : décrit une *intention* de pipeline, pas une capacité opérationnelle. La nuance "intent" dans le libellé est honnête mais la classification en `capabilities_present` plutôt qu'en `capabilities_partial` est discutable.
  - `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` : la règle est définie mais le mécanisme de validation de son application est absent. Classer cette capacité comme "présente" masque l'absence totale des gardes-fous associés.

- `capabilities_partial` : 7 entrées. Toutes correctement identifiées comme partielles.
- `capabilities_absent` : 5 entrées. Correctement reconnues — pas de dissimulation.
- `blockers` : 3 blockers identifiés, tous severity `medium`. Le blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` est correctement posé mais sa severity `medium` peut être sous-estimée : tant que la factory n'est pas dans le manifest officiel, elle est outside le dispositif de release, ce qui est un trou de gouvernance non trivial.
- `evidence` : seulement 2 preuves, toutes deux internes au repo. Aucune preuve de validation externe, de test, ou de review par un pair. Pour un artefact V0 c'est acceptable, mais l'evidence est très mince pour justifier les `capabilities_present`.

---

### Axe 7 — Multi-IA en parallèle

**Points faibles structurels :**

1. **Absence de convention de granularité modulaire** : les exigences sont posées (`bounded_scopes`, `stable_identifier_principle`) mais sans protocole opérationnel. Deux IA travaillant en parallèle sur des scopes adjacents n'ont pas de règle pour décider où commence et où finit leur zone de responsabilité.

2. **Absence de protocole d'assemblage** : `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` est reconnu. Mais sans protocole, la factory ne peut pas garantir que deux outputs IA sont compatibles. Le seul mécanisme actuel est la traçabilité par identifiants stables — nécessaire mais insuffisant.

3. **Absence de protocole de résolution de conflit** : non listé dans `known_gaps`, mais absent des mécanismes définis. Si deux IA produisent des projections dérivées légèrement différentes pour un même scope, il n'y a pas de règle de résolution.

4. **Scopes trop larges** : la factory ne définit pas encore la granularité d'une "projection dérivée pour une tâche bornée". Un scope trop large force une IA à travailler sur un contexte dont elle ne maîtrise pas toutes les dépendances canoniques, augmentant le risque d'omission.

5. **Reports non homogènes à ce stade** : le pipeline V0 définit des outputs par stage mais sans schéma fin pour chaque output. Deux IA exécutant le même stage produiront des reports dont la comparaison sera difficile.

---

### Axe 8 — Gouvernance release, manifest et traçabilité

**Problèmes identifiés :**

1. **Artefacts dans current mais hors manifest officiel** (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`) : c'est un trou de gouvernance explicitement reconnu mais non résolu. La factory est dans le dispositif "current" sans être dans le dispositif de release. La traçabilité entre l'état current et une future release formelle est absente.

2. **Absence de version tag sur la baseline challengée** : les artefacts portent `version: 0.1.0` mais il n'y a pas de tag git correspondant, pas de release GitHub, pas d'entrée dans un changelog. La baseline est "current" par positionnement de fichier, non par gouvernance de release.

3. **Absence de définition de ce que serait une "release" de la factory** : le pipeline définit `STAGE_07_FACTORY_RELEASE_MATERIALIZATION` et `STAGE_08_FACTORY_PROMOTE_CURRENT` avec référence à des specs détaillées — mais ces specs (`STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md`) n'ont pas été vérifiées comme existantes dans le cadre de ce challenge. Si elles n'existent pas, les deux stages les plus critiques de gouvernance release sont des stubs.

4. **Traçabilité canonique de la factory vers les Cores** : correctement déclarée dans `source_of_authority`. Mais aucun mécanisme n'oblige les artefacts produits par la factory à référencer les versions exactes des Cores au moment de leur production.

---

### Axe 9 — Implémentabilité pipeline

**Points solides :**
- Structure de stages claire et séquentielle.
- Doctrine opérationnelle explicite (6 règles).
- Zones d'écriture correctement identifiées.
- Prompts requis listés.

**Manques identifiés :**

1. **STAGE_07 et STAGE_08 délèguent à des specs externes** dont l'existence n'est pas garantie. Si ces fichiers n'existent pas, les stages les plus critiques (release et promotion) n'ont pas de contrat d'exécution.

2. **Aucun schéma d'output défini** pour les stages 01 à 06 : le présent rapport prouve que STAGE_01 peut produire un output, mais le pipeline ne contraint pas son contenu minimum au-delà de la liste de sections du prompt. Un stage suivant ne peut pas valider formellement un challenge report.

3. **Absence de validator dédié** : `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` est absent. Sans validateur, les étapes de validation (STAGE_04, STAGE_06) reposent entièrement sur l'IA — ce qui est circulaire et non déterministe.

4. **Règle 4 (projections strictement conformes) non testable** dans le pipeline actuel : aucun stage ne produit de preuve de conformité d'une projection ; le pipeline accepte implicitement que "produite selon les règles = conforme".

5. **L'archivage et le reset final (STAGE_09)** dépendent du prompt `Make24PlatformFactoryReview.md` mais le pipeline ne définit pas le critère de succès d'un cycle complet — ce qui empêche de savoir quand STAGE_09 est complètement terminé.

---

### Axe 10 — Scénarios adversariaux

#### Scénario 1 — Dérive d'une projection dérivée

**Description :** Une IA reçoit comme unique contexte une projection dérivée couvrant le scope "règles d'adaptation du moteur". Cette projection paraphrase `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` en omettant l'interdiction d'inférence IA implicite locale. L'IA produit un module d'adaptation qui autorise une inférence LLM locale pour qualifier un signal de gouvernance.

**Mécanismes activés :** `execution_projection_contract` (no_normative_divergence), `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT`.

**Faiblesse révélée :** Aucun validateur ne vérifie la fidélité de la projection. L'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est déclaré mais non instrumenté. La dérive est silencieuse.

**Origine :** Projections dérivées.

---

#### Scénario 2 — Application produite apparemment valide mais non-conforme

**Description :** Une application produite déclare un manifest conforme au contrat factory (identity, origin, canonical_dependencies, validation_statuses). Mais elle intègre un mécanisme de feedback qui génère dynamiquement des messages d'erreur en appelant un LLM local via API REST au runtime.

**Mécanismes activés :** `produced_application_minimum_contract`, `minimum_observability_contract`.

**Faiblesse révélée :** Le contrat minimal ne requiert pas de signal observable qui prouve l'absence d'appel réseau runtime. `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` ne sont pas vérifiés par le contrat factory. L'application passe la validation factory mais viole deux invariants constitutionnels critiques.

**Origine :** Contrat minimal d'application.

---

#### Scénario 3 — Collision multi-IA à l'assemblage

**Description :** Deux IA travaillent en parallèle. IA-A produit un module `session_integrity` basé sur une projection dérivée V1. IA-B produit un module `patch_governance` basé sur une projection dérivée V2 (régénérée après une correction mineure). Les deux projections divergent sur le comportement de `INV_NO_PARTIAL_PATCH_STATE`. Les deux modules sont assemblés sans que le trou soit détecté. L'application produite a un comportement incohérent en cas de patch échoué.

**Mécanismes activés :** `multi_ia_parallel_readiness`, `generated_projection_rules`, `PF_CAPABILITY_MULTI_IA_DECOMPOSITION` (partial).

**Faiblesse révélée :** Absence de protocole d'assemblage, absence de protocole de résolution de conflit entre projections dérivées de versions différentes. L'identifiant de version des projections n'est pas tracé dans les modules produits.

**Origine :** Architecture factory (multi-IA) + projections dérivées.

---

#### Scénario 4 — Gouvernance release insuffisamment fermée

**Description :** Un cycle pipeline complet est exécuté. STAGE_05 produit des artefacts patchés dans `work/05_apply/patched/`. STAGE_06 valide. Mais STAGE_07 et STAGE_08 ne sont pas exécutés (les specs n'existent pas encore). Un humain copie manuellement les fichiers patchés dans `docs/cores/current/` en pensant que "la validation Stage 06 suffit". La release est implicite, non gouvernée.

**Mécanismes activés :** Pipeline Rules 6 ("Release and promotion are distinct acts"), `STAGE_07_FACTORY_RELEASE_MATERIALIZATION`, `STAGE_08_FACTORY_PROMOTE_CURRENT`.

**Faiblesse révélée :** L'absence des specs de STAGE_07 et STAGE_08 crée un vide qui incite à court-circuiter la gouvernance release. Le pipeline déclare la règle mais ne la rend pas opérationnellement impossible à contourner.

**Origine :** Pipeline + manifest/release governance.

---

### Axe 11 — Priorisation des risques

| # | Risque | Gravité | Origine |
|---|---|---|---|
| R1 | Contrat application ne projette pas les invariants constitutionnels critiques (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`) | **Critique** | Architecture — contrat minimal |
| R2 | Projections dérivées autorisées comme unique contexte IA sans validateur, stockage ni protocole de régénération | **Critique** | Architecture — projections dérivées |
| R3 | STAGE_07 et STAGE_08 délèguent à des specs potentiellement absentes | **Élevé** | Pipeline |
| R4 | Absence de protocole d'assemblage multi-IA | **Élevé** | Architecture — multi-IA |
| R5 | Surdéclaration partielle des `capabilities_present` dans le state | **Modéré** | State |
| R6 | Artefacts factory hors manifest officiel (blocker reconnu) | **Modéré** | Manifest/release governance |
| R7 | `minimum_validation_contract` non implémentable sans schéma des axes | **Modéré** | Architecture — contrat minimal |
| R8 | Absence de traçabilité de version des projections dans les modules produits | **Modéré** | Projections dérivées |
| R9 | Absence de critère de succès global du cycle pipeline | **Faible** | Pipeline |
| R10 | Séparation générique/spécifique non bornée pour les projections | **Faible** | Architecture |

---

## Points V0 acceptables

Les points suivants sont des incomplétudes V0 normales, reconnues et sans risque immédiat, qui n'appellent pas de correction avant le prochain patch :

- **Schémas fins non encore finalisés** (`exact_manifest_schema`, `exact_runtime_typology`, `exact_configuration_schema`, `exact_packaging_schema`) : correctement documentés comme `missing` dans le state et comme `open_points_for_challenge` dans l'architecture.
- **Absence de validateurs implémentés** (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent) : reconnu, borné, sans risque immédiat tant qu'aucun pipeline d'instanciation n'est lancé.
- **Absence du pipeline d'instanciation** (`PF_CAPABILITY_APPLICATION_INSTANTIATION_PIPELINE` absent) : correctement hors scope de la factory.
- **Granularité modulaire non optimale** : défi reconnu, déféré (`deferred_challenges`).
- **Absence de taille optimale pour les projections** : idem.
- **Taille des projections non bornée** : acceptable V0 si aucune projection n'est encore utilisée opérationnellement.
- **`last_assessment` de type `initial_baseline`** : cohérent avec le V0.
- **Evidence mince** : acceptable pour un premier état constatif sans test ni review externe.

---

## Corrections à arbitrer avant patch

---

### CORR-01 — Projections autorisées sans garde-fous opérationnels

| Champ | Valeur |
|---|---|
| **Élément concerné** | `execution_projection_contract` dans `platform_factory_architecture.yaml` |
| **Localisation** | Section `contracts.execution_projection_contract` |
| **Nature du problème** | Le contrat autorise l'usage des projections comme unique contexte IA alors que le validateur, l'emplacement de stockage et le protocole de régénération sont tous absents ou TBD |
| **Type de problème** | Gouvernance + complétude + exploitabilité IA |
| **Gravité** | Critique |
| **Impact factory** | Le mécanisme central de la factory (projections dérivées) est théoriquement autorisé sans que les conditions de sécurité soient remplies |
| **Impact application produite** | Indirect : une application produite à partir d'une projection non validée peut hériter d'une divergence normative sans le savoir |
| **Impact IA** | Une IA peut utiliser une projection non conforme en pensant être dans le périmètre autorisé |
| **Impact gouvernance/release** | Toute release produite via ce mécanisme est non auditable |
| **Correction à arbitrer** | Soit bloquer explicitement l'usage des projections comme unique contexte jusqu'à ce que le validateur et le protocole de régénération soient définis ; soit ajouter dans l'architecture une note claire que l'usage autorisé est conditionnel et ne s'active qu'après instrumentation |
| **Lieu probable de correction** | Architecture + validator/tooling |

---

### CORR-02 — Contrat application ne couvre pas les invariants constitutionnels critiques

| Champ | Valeur |
|---|---|
| **Élément concerné** | `produced_application_minimum_contract` dans `platform_factory_architecture.yaml` |
| **Localisation** | Sections `minimum_validation_contract.minimum_axes`, `minimum_observability_contract.minimum_signals`, `manifest.minimum_contents` |
| **Nature du problème** | Le contrat minimal ne requiert aucune preuve de conformité aux invariants constitutionnels de runtime et de patch (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`) |
| **Type de problème** | Compatibilité constitutionnelle + gouvernance |
| **Gravité** | Critique |
| **Impact factory** | La factory ne peut pas certifier qu'une application produite est constitutionnellement conforme |
| **Impact application produite** | Une application peut être factory-conforme et constitutionnellement non-conforme sans détection |
| **Impact IA** | Une IA produisant une application selon le contrat factory peut livrer quelque chose d'invalide |
| **Impact gouvernance/release** | Toute release d'une application produite par la factory est non certifiable sur les invariants les plus critiques |
| **Correction à arbitrer** | Ajouter dans `minimum_validation_contract.minimum_axes` : `local_runtime_conformance` (vérifie `INV_RUNTIME_FULLY_LOCAL` + `INV_NO_RUNTIME_CONTENT_GENERATION`), `deterministic_patch_path` (vérifie `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`). Ajouter dans `minimum_observability_contract.minimum_signals` : un signal permettant d'auditer l'absence d'appel réseau. Ajouter dans `manifest.minimum_contents` : une section `constitutional_invariant_conformance` référençant les IDs d'invariants applicables |
| **Lieu probable de correction** | Architecture |

---

### CORR-03 — STAGE_07 et STAGE_08 reposent sur des specs possiblement absentes

| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` — sections STAGE_07 et STAGE_08 |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md`, lignes STAGE_07 et STAGE_08 |
| **Nature du problème** | Les deux stages les plus critiques pour la release et la promotion délèguent entièrement à des fichiers specs (`STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`, `STAGE_08_FACTORY_PROMOTE_CURRENT.md`) dont l'existence n'a pas été vérifiée |
| **Type de problème** | Implémentabilité + gouvernance |
| **Gravité** | Élevé |
| **Impact factory** | Si ces fichiers n'existent pas, le cycle de correction ne peut pas être mené à terme de façon gouvernée |
| **Impact application produite** | Indirect : pas de release formelle possible |
| **Impact IA** | Une IA exécutant le pipeline jusqu'à STAGE_06 ne sait pas comment finaliser le cycle |
| **Impact gouvernance/release** | Risque de promotion informelle des artefacts sans passer par le dispositif officiel |
| **Correction à arbitrer** | Vérifier l'existence de ces deux fichiers et les créer ou les compléter si nécessaires avant de lancer un cycle complet |
| **Lieu probable de correction** | Pipeline |

---

### CORR-04 — Absence de protocole d'assemblage multi-IA

| Champ | Valeur |
|---|---|
| **Élément concerné** | `multi_ia_parallel_readiness` dans `platform_factory_architecture.yaml` |
| **Localisation** | Section `multi_ia_parallel_readiness.deferred_challenges` et `platform_factory_state.yaml` — `capabilities_absent` |
| **Nature du problème** | La granularité modulaire, le protocole d'assemblage et le protocole de résolution de conflit sont tous absents ou déférés. La factory déclare le multi-IA comme exigence de premier rang mais n'a pas les mécanismes pour le garantir |
| **Type de problème** | Exploitabilité IA + complétude |
| **Gravité** | Élevé |
| **Impact factory** | Deux IA travaillant en parallèle peuvent produire des fragments incompatibles sans détection |
| **Impact application produite** | Assemblage potentiellement incohérent des modules produits en parallèle |
| **Impact IA** | Chaque IA doit improviser les conventions d'assemblage, ce qui génère de la dérive |
| **Impact gouvernance/release** | Impossible de certifier qu'une application multi-IA est cohérente |
| **Correction à arbitrer** | Définir a minima : (1) une convention de nommage et de versionning des projections dérivées par scope, (2) un protocole minimal d'assemblage (séquence ou règles de merge), (3) une règle de résolution de conflit en cas de projections divergentes pour un même scope |
| **Lieu probable de correction** | Architecture + pipeline |

---

### CORR-05 — Surdéclaration de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` comme capacité présente

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present` dans `platform_factory_state.yaml` |
| **Localisation** | Section `capabilities_present`, entrée `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` |
| **Nature du problème** | La règle d'usage est définie, mais le validateur, le protocole de régénération et l'emplacement de stockage sont absents. Classer cela comme "capacité présente" crée un faux sentiment de complétude |
| **Type de problème** | Faux niveau de maturité |
| **Gravité** | Modéré |
| **Impact factory** | Masque partiellement un gap important dans la lecture du state |
| **Impact application produite** | Indirect |
| **Impact IA** | Une IA lisant le state peut conclure que les projections sont utilisables sans précaution |
| **Impact gouvernance/release** | Un arbitrage basé sur le state peut sous-estimer l'effort restant |
| **Correction à arbitrer** | Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` vers `capabilities_partial` avec description précisant que la règle est définie mais non instrumentée |
| **Lieu probable de correction** | State |

---

### CORR-06 — Absence de traçabilité canonique par version dans les artefacts produits

| Champ | Valeur |
|---|---|
| **Élément concerné** | `manifest.minimum_contents` dans `produced_application_minimum_contract` |
| **Localisation** | Section `contracts.produced_application_minimum_contract.manifest` |
| **Nature du problème** | Le contrat exige `canonical_dependencies` dans le manifest mais ne précise pas que ces dépendances doivent inclure les versions exactes (ou hashs) des Cores au moment de la production |
| **Type de problème** | Gouvernance + traçabilité |
| **Gravité** | Modéré |
| **Impact factory** | Impossible de vérifier rétrospectivement avec quelle version de la Constitution une application a été produite |
| **Impact application produite** | Une application peut être obsolète vis-à-vis d'un Core patché sans détection |
| **Impact IA** | Une IA comparant deux applications produites à des moments différents ne peut pas détecter de dérive constitutionnelle |
| **Impact gouvernance/release** | Traçabilité incomplète entre application produite et socle canonique |
| **Correction à arbitrer** | Ajouter dans `manifest.minimum_contents` une exigence de `canonical_dependencies_at_build_time` avec versioning exact (version ID + hash ou commit ref) |
| **Lieu probable de correction** | Architecture |

---

## Conclusion du challenge

La Platform Factory V0 est une base solide et honnêtement posée. Elle mérite d'être avancée, pas réécrite.

Les corrections à arbitrer sont toutes adressables dans un cycle V0→V0.2 sans remettre en cause les décisions validées. La priorité absolue avant tout usage opérationnel des projections dérivées est **CORR-01** et **CORR-02**.

Ce rapport est produit pour exploitation directe par **STAGE_02_FACTORY_ARBITRAGE**.

---

## Fin de rapport

```
challenge_run_id : PFCHAL_20260404_PERPLX_7K2R
output file      : docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_7K2R.md
```

**Résumé ultra-court :**
5 corrections critiques/élevées identifiées : projections dérivées utilisables sans garde-fous (CORR-01, critique), contrat application ne couvre pas les invariants constitutionnels de runtime (CORR-02, critique), specs release STAGE_07/08 potentiellement absentes (CORR-03, élevé), protocole multi-IA absent (CORR-04, élevé), surdéclaration maturité projections dans le state (CORR-05, modéré). V0 viable mais non exploitable en production sans arbitrage sur CORR-01 et CORR-02.
