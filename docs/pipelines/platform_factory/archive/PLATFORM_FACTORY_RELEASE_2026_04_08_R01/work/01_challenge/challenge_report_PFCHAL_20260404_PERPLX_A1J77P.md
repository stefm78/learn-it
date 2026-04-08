# Platform Factory Challenge Report

**title:** Challenge adversarial de la baseline Platform Factory V0  
**challenge_run_id:** PFCHAL_20260404_PERPLX_A1J77P  
**date:** 2026-04-04  
**pipeline:** docs/pipelines/platform_factory/pipeline.md — STAGE_01_CHALLENGE  
**agent:** PERPLX  
**destinataire_stage_suivant:** STAGE_02_FACTORY_ARBITRAGE

---

## Artefacts challengés

| Artefact | artifact_id | version | status |
|---|---|---|---|
| `docs/cores/current/platform_factory_architecture.yaml` | PLATFORM_FACTORY_ARCHITECTURE_V0_1 | 0.1.0 | CURRENT_V0 |
| `docs/cores/current/platform_factory_state.yaml` | PLATFORM_FACTORY_STATE_V0_1 | 0.1.0 | CURRENT_V0 |

Artefacts canoniques de référence lus :
- `docs/cores/current/constitution.yaml` — CORE_LEARNIT_CONSTITUTION_V2_0 (V2_0_FINAL)
- `docs/cores/current/referentiel.yaml` — CORE_LEARNIT_REFERENTIEL_V2_0
- `docs/cores/current/link.yaml` — CORE_LINK_LEARNIT_CONSTITUTION_V2_0__REFERENTIEL_V2_0
- `docs/pipelines/platform_factory/pipeline.md`

---

## Résumé exécutif

La Platform Factory V0 constitue une fondation conceptuelle valide. Sa séparation architecture/state est tenue, sa dépendance explicite au socle canonique est déclarée, ses périmètres in/out sont bornés, et ses lacunes (schémas, validateurs, emplacement des projections, protocole multi-IA) sont reconnues dans `platform_factory_state.yaml`.

**Cependant, six faiblesses structurelles dépassent le seuil du manque V0 normal et doivent être arbitrées avant patch :**

1. **Absence de binding constitutionnel sur le runtime 100 % local dans le contrat minimal d'application produite.** Un manifest d'application produite peut être déclaré conforme sans jamais attester qu'il ne contient aucun appel réseau runtime ni génération de contenu — violation potentielle de `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`.

2. **Absence de binding explicit sur `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` dans le contrat minimal.** Le contrat minimal d'application produite ne demande pas de prouver que ses patchs seront pré-calculés hors session.

3. **Emplacement des `validated_derived_execution_projections` non décidé (`TBD`).** L'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est déclaré mais non instrumenté. Une IA peut recevoir une projection sans que son adresse, sa version, sa régénérabilité ou sa date de validation soient vérifiables.

4. **Maturité surdéclarée sur `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` et `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`.** Ces capacités sont marquées `capabilities_present` alors que leur instrumentalisation est absente.

5. **Protocole d'assemblage multi-IA non défini.** Les exigences sont posées comme `requirement_defined_not_yet_operationalized` mais aucun élément architecturé ne permet d'empêcher des collisions entre outputs IA parallèles.

6. **Le `platform_factory_architecture.yaml` est dans `docs/cores/current/` mais hors manifest officiel.** Cette ambiguïté rend le statut de la baseline indéterminé vis-à-vis du cycle de release.

**La baseline est challengeable et patchable. Elle n'est pas bloquante pour STAGE_02, mais les six points ci-dessus doivent être arbitrés.**

---

## Carte de compatibilité constitutionnelle

| Invariant constitutionnel | Élément factory concerné | Binding | Risque si application produite |
|---|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | `produced_application_minimum_contract` → `minimum_observability_contract` | **Absent** — non requis dans le manifest | Une app produite peut être déclarée valide sans audit de ses appels réseau |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | `produced_application_minimum_contract` → `minimum_validation_contract` | **Absent** — non couvert dans les axes de validation | La factory ne vérifie pas l'absence de génération runtime dans l'app produite |
| `INV_NO_PARTIAL_PATCH_STATE` | Architecture → `build_and_packaging_rules` | **Implicite faible** — `package_must_be_classifiable_complete_or_incomplete_or_invalid` approche le sujet | Pas d'obligation explicite de rollback en cas de patch partiel |
| `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` | `produced_application_minimum_contract` | **Absent** | Une app produite peut intégrer des mécanismes de patch on-session sans que la factory le détecte |
| `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | `produced_application_minimum_contract` → `minimum_validation_contract` | **Absent** | Le contrat minimal ne demande pas que la validation des patchs de l'app soit déterministe |
| `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | Architecture → `dependencies_to_constitution` / `dependencies_to_referentiel` | **Explicite** — les dépendances sont déclarées séparément | Risque faible — bien tenu |
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Hors périmètre factory (domaine) | N/A — correctement exclu | Risque hors scope factory |
| `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` | `generated_projection_rules` | **Déclaré, non instrumenté** | Une projection peut être utilisée comme artefact unique par une IA sans vérification d'intégrité |
| `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION` | Architecture → `dependencies_to_referentiel` | **Déclaré par référence, non vérifié dans le contrat minimal** | Une app produite peut fonctionner sans Référentiel valide si le contrat ne le requiert pas |

---

## Analyse détaillée par axe

### Axe 1 — Carte de compatibilité constitutionnelle

*Cf. carte ci-dessus.*

Points solides : la séparation Constitution/Référentiel est bien préservée par la factory (`no_direct_redefinition_of_constitution`, `dependencies_to_constitution.mode: explicit_reference_only`). Le LINK est référencé pour la résolution inter-Core.

Risque principal : le **contrat minimal d'une application produite** (`produced_application_minimum_contract`) ne demande pas explicitement de prouver la conformité aux invariants constitutionnels `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`. Un manifest d'app produite peut donc être validé conformément à la factory sans jamais avoir attesté de sa compatibilité constitutionnelle sur ces points critiques.

### Axe 2 — Cohérence interne de la factory

**Points solides :**
- La séparation prescriptif (`architecture`) / constatif (`state`) est tenue et lisible.
- Les `validated_decisions` dans l'état sont cohérentes avec les principes architecturaux.
- Les `capabilities_absent` sont clairement nommées.

**Problème 1 — Maturité surdéclarée :**
`PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est listée en `capabilities_present` avec la description _"La règle d'usage des projections dérivées validées est définie."_ Or `derived_projection_conformity_status` dans l'état indique `defined_in_principle_not_yet_tooling_backed` et liste comme manquants : validator_definition, storage_location_decision, regeneration_protocol. Une règle dont le mécanisme d'exécution est entièrement absent n'est pas une capacité présente — c'est une capacité intentionnelle.

**Problème 2 — `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` vs open_points_for_challenge :**
La section `open_points_for_challenge` dans l'architecture liste 6 points non résolus (manifest schema, runtime entrypoint typology, configuration schema, packaging schema, projection storage location, granularity for multi-AI work). Dire que la portée est "présente" et capable alors que 6 de ses composants clés restent ouverts masque une incomplétude réelle.

**Problème 3 — Contrainte `no_domain_specific_content_inside_factory_architecture` non verifiable :**
Elle est déclarée comme contrainte mais il n'existe aucun validateur ni axe de validation du contrat minimal qui vérifie qu'une application produite ne laisse pas entrer du contenu domaine dans le layer factory.

### Axe 3 — Portée et frontières

**Point solide :** La délimitation entre `in_scope` et `out_of_scope` est nette et correctement positionnée. Le pipeline d'instanciation downstream est explicitement hors périmètre.

**Zone de risque :** Le `runtime_entrypoint_contract` dans le contrat minimal exige `bootstrap_contract` et `runtime_prerequisites` mais ne dit pas si ces éléments doivent attester d'une architecture 100 % locale. L'entrée runtime d'une application produite est un point d'injection possible d'un runtime non local, sans que la factory le détecte.

**Angle mort :** Les `validated_derived_execution_projections` peuvent contenir des hypothèses implicites sur un runtime particulier (par ex. une stack Cloud) sans que la factory ne l'interdise dans leur invariant `no_normative_divergence`. L'invariant cible la fidélité normative textuelle, pas la conformité à `INV_RUNTIME_FULLY_LOCAL`.

### Axe 4 — Contrat minimal d'une application produite

Le contrat est structurellement bien pensé. Ses blocs sont clairement définis à haut niveau.

**Obligations manquantes (non liées à l'incomplétude V0 normale) :**

1. **Attestation de localité runtime.** Aucun bloc du manifest ou de l'observabilité ne requiert de déclarer explicitement l'absence d'appel réseau runtime (`INV_RUNTIME_FULLY_LOCAL`).

2. **Attestation d'absence de génération runtime.** Aucun axe de `minimum_validation_contract` ne vérifie l'absence de génération de contenu ou de feedback à la volée (`INV_NO_RUNTIME_CONTENT_GENERATION`, `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`).

3. **Attestation de précomputation des patchs hors session.** Si l'application produite embarque un mécanisme de patch, rien dans le contrat minimal ne requiert qu'il soit conforme à `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`.

4. **Compatibilité Référentiel valide.** Le `canonical_dependency_contract` est requis mais ne spécifie pas qu'un Référentiel valide et compatible doit être déclaré pour les évaluations déléguées (cf. `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`).

**Obligations trop floues :**

5. **`runtime_entrypoint_contract.bootstrap_contract`** n'est pas défini. Son contenu reste TBD. Une IA produisant une application ne sait pas quoi y écrire.

6. **`minimum_validation_contract.minimum_axes`** liste `minimum_contract_conformance` sans dire comment auditer cette conformance ni contre quelles règles.

**Obligations non auditables :**

7. **`traceability_metadata`** dans le manifest est requis mais sans schéma. Une IA peut remplir n'importe quoi dans ce bloc sans être détectée.

### Axe 5 — Validated derived execution projections

La règle d'usage est correctement posée dans `execution_projection_contract`. Les invariants `no_new_rule`, `no_normative_divergence`, `no_omission_within_declared_scope` sont déclarés.

**Risques identifiés :**

1. **Emplacement TBD** (`emplacement_policy.status: TBD`). Une projection n'a pas d'adresse stable. Une IA ne peut pas vérifier qu'elle lit la dernière version validée. Ce TBD est qualifié de "ne pas polluer `docs/cores/current/`" mais aucune alternative n'est posée. C'est un **trou de gouvernance**.

2. **Absence de protocole de validation.** L'invariant `deterministic_regeneration_required` est déclaré mais il n'existe pas de validator dédié. Une projection peut être produite une seule fois, utilisée plusieurs fois, et personne ne détecte une dérive entre sa version et le canonique mis à jour.

3. **Risque de paraphrase dangereuse.** `prohibited: uncontrolled_paraphrase` est déclaré mais il n'y a pas de mécanisme pour le détecter. Si une IA paraphrase `INV_RUNTIME_FULLY_LOCAL` de façon légèrement incorrecte dans une projection, la factory n'a aucun moyen de le détecter.

4. **Risque de promotion implicite.** `prohibited: promotion_as_primary_canonical_artifact` est déclaré. Mais rien dans le pipeline (stages 01 à 09) ne vérifie que l'IA qui travaille à partir d'une projection ne la traite pas comme source primaire. L'interdit est sémantique, pas opérationnel.

5. **Dépendance cachée.** Une projection bornée à un scope (ex. packaging) peut implicitement supposer un runtime entrypoint type non encore défini. Aucun mécanisme ne force la déclaration des hypothèses hors-scope embarquées.

### Axe 6 — État reconnu, maturité et preuves

La structure de l'état est bonne (present / partial / absent / blockers / known_gaps). La section `delta_since_previous` est honnête (`previous_state: none`).

**Maturité surdéclarée :**

| Capacité | Niveau déclaré | Problème |
|---|---|---|
| `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` | `capabilities_present` | Le mécanisme est entièrement absent (pas de validator, pas de storage, pas de protocole de régénération) |
| `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` | `capabilities_present` | 6 open_points structurants non résolus dans l'architecture |
| `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | `capabilities_present` | Le pipeline V0 est un squelette intentionnel sans outillage |

**Incohérence blockers vs capabilities :**
`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` (severity: medium) reconnaît que les artefacts platform_factory sont hors manifest officiel. Mais `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` est déclaré present. Si le manifest officiel ne couvre pas encore la factory, la portée effective du système de gouvernance est incomplète, ce qui contredit le claim de scope défini.

**Evidence insuffisante :**
Seules deux `evidence` sont listées : le `Platform_Factory_Plan.md` et `platform_factory_architecture.yaml` (qui est lui-même l'artefact évalué). Il n'y a pas d'evidence de tests ou de validation. Acceptable pour un V0 mais à signaler.

### Axe 7 — Multi-IA en parallèle

`PF_DECISION_MULTI_IA_FIRST_CLASS` est une décision validée. Les exigences sont posées dans `multi_ia_parallel_readiness`.

**Problèmes :**

1. **Absence de protocole d'assemblage.** `deferred_challenges` liste `assembly_protocol_between_ai_outputs`. Ce déférement est correct pour un V0 MAIS il n'y a pas de borne temporelle ni de condition déclenchante. Deux IA travaillant en parallèle sur l'architecture et l'état peuvent produire des sorties incompatibles sans mécanisme de détection.

2. **Granularité modulaire non définie.** `optimal_module_granularity` est aussi dans `deferred_challenges`. Sans elle, une IA peut prendre en charge un scope trop large, une autre trop restreint, et l'assemblage devient ambigu.

3. **Rapports non homogènes.** Il n'y a pas de schéma de report uniforme entre IA. Le pipeline définit des noms de fichiers output mais pas leur structure.

4. **Absence de protocole de résolution de conflit.** Si deux IA produisent des patchs contradictoires sur la même section de l'architecture, aucun mécanisme ne tranche. L'arbitrage humain (STAGE_02) est supposé mais non garanti.

### Axe 8 — Gouvernance release, manifest et traçabilité

C'est l'axe le plus risqué structurellement.

**Problème principal :** Les artefacts `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` mais **ne sont pas intégrés au manifest officiel courant** (`manifest.yaml`). La note dans les metadata des deux artefacts le reconnaît : _"Non encore intégré au current manifest tant que le schéma core-release reste limité au trio constitution/referentiel/link."_

Ceci crée une ambiguïté de statut : les artefacts sont **traités comme released** (par le pipeline Rule 3 : "The current platform_factory artifacts are considered a released baseline") mais **non reconnus comme tels** par le dispositif officiel de release. En cas d'audit ou de promotion future, il n'est pas clair si ces artefacts héritent des protections du cycle de release ou s'ils peuvent être modifiés directement sans passage par le pipeline.

**Risques secondaires :**
- Le pipeline interdit toute modification directe de `docs/cores/current/` avant promotion explicite (success criteria). Mais sans intégration au manifest, un commit direct sur ces fichiers ne serait pas détecté comme une violation de gouvernance.
- La séparation release / promotion (Rule 6 du pipeline) est bien posée conceptuellement. Son implémentation reste entièrement procédurale, sans garde-fou automatique.

### Axe 9 — Implémentabilité pipeline

Le pipeline est un squelette V0 suffisant pour lancer le cycle challenge-arbitrage-patch. Les stages sont découpés correctement et le flux de responsabilité est lisible.

**Manques identifiés :**

1. **STAGE_01 → STAGE_02 : aucune convention de format du challenge report.** Le pipeline dit `work/01_challenge/challenge_report_##.md` mais ne définit pas les sections minimales requises. STAGE_02 doit "considérer tous les challenge_report*.md" sans savoir dans quel format les lire.

2. **STAGE_04 validation : le prompt `Make23PlatformFactoryValidation.md` est utilisé à la fois pour STAGE_04 et STAGE_06.** Ce partage de prompt pour deux stages distincts (validation du patchset vs validation du core) est ambigu. Les deux stages ont des entrées différentes et des objectifs différents.

3. **Absence de validator dédié.** Le pipeline liste des prompts pour chaque stage mais aucun validateur outillé. Pour STAGE_04 et STAGE_06, la validation repose entièrement sur le prompt LLM.

4. **STAGE_07 et STAGE_08 déportés vers des specs détaillées séparées.** Ces stages sont les plus critiques (release et promotion). Leur spec est dans des fichiers séparés non lus dans ce challenge. C'est un point de risque pour la complétude du pipeline visible dans `pipeline.md`.

5. **Absence de hook entre `pipeline.md` et le manifest officiel.** Aucune étape du pipeline ne déclenche la mise à jour du manifest officiel. La promotion STAGE_08 peut s'exécuter sans jamais corriger le gap manifest.

### Axe 10 — Scénarios adversariaux

**Scénario A — Dérive d'une projection dérivée (criticité : élevée)**

Une IA reçoit une `validated_derived_execution_projection` pour construire le `runtime_entrypoint_contract` d'une application produite. La projection a été générée avant que `INV_RUNTIME_FULLY_LOCAL` soit vérifié comme invariant impactant le runtime entrypoint. L'IA produit un entrypoint qui inclut un appel à un service réseau externe au démarrage. Le manifest est rempli conformément à la projection. Le `minimum_validation_contract` ne contient pas d'axe vérifiant l'absence d'appel réseau. L'application est packagée et promue. **La violation de `INV_RUNTIME_FULLY_LOCAL` passe à travers toute la factory sans être détectée.**

Mécanismes activés : `execution_projection_contract` (no_normative_divergence non instrumenté) + `minimum_validation_contract` (absence d'axe localité). Faiblesse : Axe 5 (projection) + Axe 4 (contrat minimal).

**Scénario B — Application paraissant valide mais violant une contrainte constitutionnelle forte (criticité : critique)**

Une application produite déclare un manifest complet, une observabilité correcte, une traçabilité des projections utilisées. Elle embarque un mécanisme de patch capable d'appliquer des corrections en session active à partir d'une source distante. Ce mécanisme ne génère pas de contenu — il applique des patchs préparés à distance. Le `minimum_validation_contract` ne vérifie ni `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` ni `INV_RUNTIME_FULLY_LOCAL`. L'application est validée et promue. **Elle viole deux invariants constitutionnels sans que la factory l'ait détecté.**

Mécanismes activés : `produced_application_minimum_contract` + `minimum_validation_contract`. Faiblesse : Axe 4 (obligations manquantes dans le contrat minimal).

**Scénario C — Collision multi-IA (criticité : modérée)**

Deux IA travaillent en parallèle : IA-1 sur `platform_factory_architecture.yaml` (contrat minimal), IA-2 sur `platform_factory_state.yaml` (mise à jour de l'état des capacités). IA-1 ajoute une nouvelle obligation au `produced_application_minimum_contract`. IA-2 met à jour `capabilities_partial` sans tenir compte de cette nouvelle obligation. Lors de l'assemblage pour STAGE_03, les deux outputs sont contradictoires sur le périmètre de `PF_CAPABILITY_APPLICATION_MANIFEST_MODEL`. Il n'existe pas de protocole d'assemblage. L'arbitrage humain est requis mais sans cadre. **Le patch synthétisé en STAGE_03 est incohérent entre architecture et state.**

Mécanismes activés : `multi_ia_parallel_readiness` (protocol undefined) + `PF_DECISION_TWO_ARTIFACTS` (séparation arch/state). Faiblesse : Axe 7 (absence de protocole d'assemblage).

**Scénario D — Baseline hors manifest promue implicitement (criticité : élevée)**

Suite à un STAGE_08 correctement exécuté, `platform_factory_architecture.yaml` est promu dans `docs/cores/current/`. Mais la mise à jour du manifest officiel (`manifest.yaml`) n'est pas incluse dans les outputs du STAGE_08. La baseline est désormais "dans current" mais toujours hors manifest. Un outil de validation automatique basé sur le manifest ne détecte jamais ces artefacts. Lors d'un futur audit, les artefacts sont traités comme non-officiels. **La gouvernance de release est contournée sans acte intentionnel.**

Mécanismes activés : pipeline STAGE_08 (promotion sans hook manifest) + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`. Faiblesse : Axe 8 (gouvernance release/manifest).

### Axe 11 — Priorisation

| # | Problème | Criticité | Axe |
|---|---|---|---|
| P1 | Absence d'attestation de localité runtime dans le contrat minimal d'application | **Critique** | 4, 1 |
| P2 | Absence d'attestation d'absence de génération runtime dans le contrat minimal | **Critique** | 4, 1 |
| P3 | Absence d'obligation de précomputation des patchs hors session dans le contrat minimal | **Élevée** | 4, 1 |
| P4 | Emplacement des projections dérivées TBD sans date ni condition déclenchante | **Élevée** | 5, 8 |
| P5 | Ambiguïté statut baseline : dans current mais hors manifest officiel | **Élevée** | 8 |
| P6 | Maturité surdéclarée sur `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` | **Modérée** | 6 |
| P7 | Absence de protocole d'assemblage multi-IA (non borné temporellement) | **Modérée** | 7 |
| P8 | Prompt partagé Make23 pour STAGE_04 et STAGE_06 — ambiguïté d'usage | **Modérée** | 9 |
| P9 | `bootstrap_contract` du runtime entrypoint non défini | **Modérée** | 4 |
| P10 | Absence de format minimal commun pour les challenge reports (STAGE_01 → STAGE_02) | **Faible** | 9 |
| P11 | Evidence insuffisante dans l'état (plan + architecture uniquement) | **Faible** | 6 |

---

## Points V0 acceptables

Les éléments suivants sont des lacunes normales d'une V0 explicitement assumée, reconnues dans les artefacts, sans risque immédiat sur la conformité constitutionnelle ou la gouvernance release :

- Schéma final du manifest d'application non arrêté (`PF_GAP_EXACT_YAML_SCHEMA_NOT_FINALIZED`) — reconnu dans `known_gaps`.
- Schéma de configuration minimal non finalisé (`exact_configuration_schema` dans `open_points_for_challenge`) — reconnu.
- Schéma de packaging non finalisé — reconnu.
- Granularité modulaire pour multi-IA non définie — dans `deferred_challenges`, acceptable pour V0.
- Validateurs factory non implémentés (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` en `capabilities_absent`) — reconnu.
- Pipeline d'instanciation aval non spécifié (`PF_CAPABILITY_APPLICATION_INSTANTIATION_PIPELINE` en `capabilities_absent`) — hors périmètre factory, correct.
- STAGE_07 et STAGE_08 déportés vers specs séparées — acceptable pour V0 si specs existent.
- Absence d'evidence de tests — normal pour un baseline V0 posé pour la première fois.

---

## Corrections à arbitrer avant patch

---

### CORR-01 — Attestation de localité runtime manquante dans le contrat minimal d'application produite

- **Élément concerné :** `produced_application_minimum_contract` → `minimum_validation_contract` et `minimum_observability_contract`
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract`
- **Nature du problème :** Le contrat minimal ne requiert ni d'attester l'absence d'appels réseau runtime, ni de vérifier la conformité à `INV_RUNTIME_FULLY_LOCAL`.
- **Type de problème :** Compatibilité constitutionnelle
- **Gravité :** Critique
- **Impact factory :** La factory peut valider une application produite non conforme à l'invariant constitutionnel le plus fondamental.
- **Impact application produite :** Une application produite peut violer `INV_RUNTIME_FULLY_LOCAL` tout en étant déclarée conforme par la factory.
- **Impact IA :** Une IA produisant une application ne reçoit pas l'instruction d'auditer la localité runtime.
- **Impact gouvernance/release :** Une promotion peut valider une application non locale sans détection.
- **Correction à arbitrer :** Ajouter dans `minimum_validation_contract.minimum_axes` un axe explicite `local_runtime_conformance` et dans `minimum_observability_contract.minimum_signals` un signal `runtime_locality_attestation`.
- **Lieu probable de correction :** architecture

---

### CORR-02 — Attestation d'absence de génération runtime manquante dans le contrat minimal

- **Élément concerné :** `produced_application_minimum_contract` → `minimum_validation_contract`
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract`
- **Nature du problème :** Aucun axe de validation ne couvre `INV_NO_RUNTIME_CONTENT_GENERATION` et `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`.
- **Type de problème :** Compatibilité constitutionnelle
- **Gravité :** Critique
- **Impact factory :** La factory ne peut pas prouver qu'une application produite respecte l'interdiction de génération runtime.
- **Impact application produite :** Une app produite pourrait générer du contenu ou du feedback en session sans que la factory l'interdise.
- **Impact IA :** L'IA construisant l'app n'est pas contrainte sur ce point.
- **Impact gouvernance/release :** Promotion possible d'une app non conforme.
- **Correction à arbitrer :** Ajouter un axe `no_runtime_generation_conformance` dans `minimum_validation_contract.minimum_axes`.
- **Lieu probable de correction :** architecture

---

### CORR-03 — Absence d'obligation de précomputation des patchs hors session dans le contrat minimal

- **Élément concerné :** `produced_application_minimum_contract` → `minimum_validation_contract`
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract`
- **Nature du problème :** `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` n'est pas couvert dans le contrat minimal. Une application produite peut embarquer un mécanisme de patch on-session.
- **Type de problème :** Compatibilité constitutionnelle
- **Gravité :** Élevée
- **Impact factory :** La factory ne peut pas garantir que les apps produites respectent la gouvernance patch constitutionnelle.
- **Impact application produite :** Risque d'application de patches en session active.
- **Impact IA :** L'IA construisant l'app n'a pas de contrainte explicite sur ce point.
- **Impact gouvernance/release :** Une app avec patchs on-session peut être promue.
- **Correction à arbitrer :** Ajouter dans `minimum_validation_contract.minimum_axes` un axe `patch_governance_conformance` (précomputation hors session, atomicité, rollback).
- **Lieu probable de correction :** architecture

---

### CORR-04 — Emplacement des projections dérivées TBD sans borne temporelle

- **Élément concerné :** `generated_projection_rules.emplacement_policy` — `status: TBD`
- **Localisation :** `platform_factory_architecture.yaml` → `generated_projection_rules.emplacement_policy`
- **Nature du problème :** L'emplacement des `validated_derived_execution_projections` est non décidé, sans date ni condition déclenchante. Les invariants de conformité des projections sont non instrumentables tant que leur localisation n'est pas fixée.
- **Type de problème :** Gouvernance + Exploitabilité IA
- **Gravité :** Élevée
- **Impact factory :** Aucune IA ne peut vérifier qu'elle lit la bonne version d'une projection.
- **Impact application produite :** Une app peut être construite à partir d'une projection obsolète.
- **Impact IA :** Une IA reçoit une projection sans adresse vérifiable ni version contrôlée.
- **Impact gouvernance/release :** Le cycle de release ne peut pas inclure les projections comme artefacts officiels.
- **Correction à arbitrer :** Décider et déclarer l'emplacement cible des projections dérivées (ex. `docs/projections/platform_factory/`), créer un schéma minimal d'identification de projection (id, version, source_hash, generated_at, scope).
- **Lieu probable de correction :** architecture + manifest/release governance

---

### CORR-05 — Ambiguïté de statut : baseline dans current mais hors manifest officiel

- **Élément concerné :** `metadata.notes` des deux artefacts + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation :** `platform_factory_architecture.yaml` et `platform_factory_state.yaml` → `metadata.notes` ; `docs/cores/current/manifest.yaml`
- **Nature du problème :** Les artefacts sont traités comme une "released baseline" par le pipeline (Rule 3) mais sont absents du manifest officiel. Le statut released est déclaratif, non gouverné.
- **Type de problème :** Gouvernance + Release/manifest
- **Gravité :** Élevée
- **Impact factory :** Un audit basé sur le manifest officiel ne détecte pas ces artefacts.
- **Impact application produite :** Une app produite peut référencer des artefacts factory non reconnus officiellement.
- **Impact IA :** Une IA ne peut pas vérifier la légitimité de la baseline qu'elle challenge.
- **Impact gouvernance/release :** La protection des artefacts contre modification directe n'est pas opérationnelle.
- **Correction à arbitrer :** Décider si (a) le manifest est étendu pour inclure les artefacts platform_factory ou (b) un manifest séparé platform_factory est créé et référencé depuis le manifest principal, et planifier cette intégration dans STAGE_07/STAGE_08.
- **Lieu probable de correction :** manifest/release governance

---

### CORR-06 — Maturité surdéclarée : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en capabilities_present

- **Élément concerné :** `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Localisation :** `platform_factory_state.yaml` → `capabilities_present`
- **Nature du problème :** La règle d'usage est définie en intention mais aucun mécanisme d'exécution n'existe (pas de validator, pas de storage, pas de protocole de régénération). Une capacité intentionnelle ne devrait pas figurer en `capabilities_present`.
- **Type de problème :** Faux niveau de maturité
- **Gravité :** Modérée
- **Impact factory :** L'état sur-vend la maturité de la factory sur un point central.
- **Impact application produite :** Aucun direct.
- **Impact IA :** Une IA lisant l'état peut croire que le mécanisme de projection est opérationnel.
- **Impact gouvernance/release :** La décision de passer en V1 peut être prise sur une base de maturité incorrecte.
- **Correction à arbitrer :** Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` de `capabilities_present` vers `capabilities_partial`, avec une description précise de ce qui est présent (règle d'usage) et ce qui est absent (mécanisme).
- **Lieu probable de correction :** state

---

### CORR-07 — Prompt Make23 partagé entre STAGE_04 et STAGE_06 — ambiguïté

- **Élément concerné :** Pipeline STAGE_04 et STAGE_06
- **Localisation :** `docs/pipelines/platform_factory/pipeline.md` → STAGE_04_FACTORY_PATCH_VALIDATION et STAGE_06_FACTORY_CORE_VALIDATION
- **Nature du problème :** Le même prompt `Make23PlatformFactoryValidation.md` est assigné aux deux stages. STAGE_04 valide un patchset (artefact intermédiaire), STAGE_06 valide les artefacts patched finaux. Ces deux objets de validation sont distincts et le prompt partagé peut conduire à une validation inadaptée.
- **Type de problème :** Implémentabilité
- **Gravité :** Modérée
- **Impact factory :** Un stage de validation peut être exécuté avec un prompt non adapté à son objet.
- **Impact application produite :** Aucun direct.
- **Impact IA :** L'IA de validation ne sait pas si elle valide un patch ou un artefact core.
- **Impact gouvernance/release :** Le critère de validation des deux stages est ambigu.
- **Correction à arbitrer :** Soit créer un prompt dédié `Make23PlatformFactoryPatchValidation.md` pour STAGE_04 distinct de `Make23PlatformFactoryValidation.md` pour STAGE_06, soit documenter explicitement dans le prompt Make23 les deux modes d'usage avec leurs objets distincts.
- **Lieu probable de correction :** pipeline

---

*Fin du challenge report PFCHAL_20260404_PERPLX_A1J77P*

---

**challenge_run_id :** `PFCHAL_20260404_PERPLX_A1J77P`  
**Fichier écrit :** `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md`
