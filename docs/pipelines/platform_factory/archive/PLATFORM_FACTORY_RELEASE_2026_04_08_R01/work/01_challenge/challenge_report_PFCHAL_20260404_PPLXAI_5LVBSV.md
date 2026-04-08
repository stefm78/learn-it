# Challenge Report — Platform Factory

## title

Challenge de la baseline V0 Platform Factory Learn-it — Rapport STAGE_01_CHALLENGE

---

## challenge_run_id

```
PFCHAL_20260404_PPLXAI_5LVBSV
```

---

## date

2026-04-04

---

## artefacts challengés

| Artefact | Version | Statut |
|---|---|---|
| `docs/cores/current/platform_factory_architecture.yaml` | 0.1.0 | CURRENT_V0 |
| `docs/cores/current/platform_factory_state.yaml` | 0.1.0 | CURRENT_V0 |

Sources normatives de référence lues :

- `docs/cores/current/constitution.yaml` — CORE_LEARNIT_CONSTITUTION_V2_0 (autorité primaire)
- `docs/cores/current/referentiel.yaml` — CORE_LEARNIT_REFERENTIEL_V2_0
- `docs/cores/current/link.yaml` — CORE_LINK_LEARNIT_CONSTITUTION_V2_0__REFERENTIEL_V2_0
- `docs/pipelines/platform_factory/pipeline.md` — pipeline V0

---

## Résumé exécutif

La baseline V0 de la Platform Factory pose des fondements conceptuels solides et une séparation prescriptif/constatif correctement initiée. Les invariants les plus critiques de la Constitution (runtime 100 % local, pas de génération contenu runtime, pas de réseau temps réel, pas de génération feedback hors templates) ne sont **pas positivement propagés** dans le contrat minimal d'application produite. La factory déclare des obligations sans fournir les schémas ou validateurs permettant de les vérifier, créant un écart entre déclaration d'intention et vérifiabilité réelle.

**3 risques critiques** ont été identifiés :

1. **Absence de binding vérifiable des invariants de runtime** dans le contrat minimal d'application produite — une application pourrait être produite "conforme" sans que la conformité constitutionnelle locale soit auditablement prouvée.
2. **Projections dérivées sans emplacement, sans validateur, sans protocole de régénération déterministe** — le mécanisme central d'alimentation des IA est déclaré mais entièrement non opérationnalisé, avec un risque de dérive normative silencieuse.
3. **Absence du manifest officiel** — les artefacts sont dans `docs/cores/current/` mais explicitement hors du manifest courant, créant une zone grise de gouvernance de release.

**3 risques élevés** : absence de protocole d'assemblage multi-IA, contrat minimal d'application sans axes d'audit constitutionnel positifs, état de maturité partiellement surdéclaré sur les capacités "partial".

La baseline est **exploitable pour lancer le cycle challenge/arbitrage/patch**, mais ne peut pas encore être considérée comme un dispositif de production sûr d'applications constitutionnellement conformes.

---

## Carte de compatibilité constitutionnelle

| Invariant constitutionnel | Élément factory concerné | Binding | Risque portant sur | Application produite pourrait violer ? |
|---|---|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | `produced_application_minimum_contract` | Implicite / absent dans les axes de validation | architecture + contrat minimal | **Oui** — aucun axe de validation ne vérifie positivement l'absence de call réseau |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | `minimum_validation_contract` (axes: structure, conformance, traceability, packaging) | Absent | contrat minimal + pipeline | **Oui** — aucun axe de validation ne couvre l'interdiction de génération runtime |
| `INV_NO_RUNTIME_FEEDBACK_GENERATION` | `minimum_validation_contract` | Absent | contrat minimal | **Oui** — non vérifié dans les axes définis |
| `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | `contracts.execution_projection_contract.invariants` | Explicite (no_new_rule, no_normative_divergence) mais pas borné sur la patch layer de l'application | projections dérivées | Partiellement — seul le contrat de projection, pas le contrat d'application |
| `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` | Non mentionné dans le contrat minimal d'application | Absent | contrat minimal | **Oui** — rien n'oblige l'application produite à respecter cette contrainte |
| `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | `design_principles.PF_PRINCIPLE_NO_NORM_DUPLICATION` | Explicite et fort | architecture | Faible risque |
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Hors scope factory (domaine) | N/A — correctement hors périmètre | — | Hors périmètre factory : acceptable V0 |
| `INV_CANONICAL_TRACEABILITY` (principe PF) | `produced_application_minimum_contract.canonical_dependency_contract` | Explicite mais schéma absent | contrat minimal + packaging | Risque modéré — déclaration requise sans schéma de vérification |
| `INV_NO_PARTIAL_PATCH_STATE` | Non mappé dans le contrat minimal | Absent | contrat minimal | **Oui** — rien n'impose la gestion atomique de l'application produite |
| `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` | Absent du contrat | Absent | contrat minimal + projections dérivées | **Oui** — une projection dérivée pourrait implicitement introduire une inférence IA si non contrôlée |
| `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION` | `source_of_authority` déclare les dépendances | Implicite | architecture | Risque modéré — pas de mécanisme de fallback explicite si le Référentiel est absent lors d'une projection |

**Synthèse** : 5 invariants constitutionnels forts ne sont pas positivement propagés dans le contrat minimal d'application produite. La factory peut produire une application qui paraît conforme à ses propres règles tout en violant des contraintes constitutionnelles non testées.

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

Le mapping des invariants ci-dessus révèle un pattern systémique : la factory déclare les bonnes dépendances (`source_of_authority.required_bindings` cite `governing_invariants` et `forbidden_behaviors`) mais **ne les projette pas dans les axes de validation du contrat minimal**. La clé `minimum_validation_axes` liste `structure`, `minimum_contract_conformance`, `traceability`, `packaging` — aucun axe nommé ne couvre explicitement `runtime_constitutional_constraints`. Un validateur qui ne sait pas quoi chercher ne peut pas prouver la conformité.

Point solide : `PF_PRINCIPLE_NO_NORM_DUPLICATION` et la règle d'interdiction de redéfinir la Constitution sont clairement énoncés dans l'architecture.

### Axe 2 — Cohérence interne de la factory

**Contradiction architecture ↔ state** :

- L'architecture déclare `PF_CAPABILITY_MINIMUM_APPLICATION_CONTRACT_DEFINED_AT_HIGH_LEVEL` comme capacité à haut niveau dans son `contracts` block.
- Le state la classe en `capabilities_partial` avec la note "défini en intention mais pas encore en schéma fin" — ce qui est cohérent, mais le wording de l'architecture laisse croire à une définition plus complète que ce que l'état reconnaît réellement.

**Sur-déclaration de maturité partielle** : plusieurs `capabilities_partial` sont en réalité des intentions. `PF_CAPABILITY_DERIVED_PROJECTION_LIFECYCLE` est décrit comme "cycle de vie décrit au niveau principe" — il n'existe pas de cycle de vie matérialisé. Le wording "décrit" surestime légèrement. Cette nuance est importante car elle peut amener une IA à considérer la projection comme utilisable alors qu'elle n'a pas de lifecycle opérationnel.

**Cohérence des `validated_decisions`** : les 5 décisions validées sont cohérentes avec le contenu des deux artefacts. Pas de contradiction interne sur ce point.

**Séparation prescriptif/constatif** : correctement initiée. Le risque est que, au fil des patchs, des éléments constatifs migrent vers l'architecture si aucun gardien ne surveille explicitement cette frontière dans le pipeline.

### Axe 3 — Portée et frontières

**Point solide** : la factory énonce clairement ce qu'elle ne gouverne pas (`does_not_govern`, `out_of_scope`). Le pipeline Rule 3 est explicite sur la posture "released baseline". La frontière avec le pipeline d'instanciation est nommée.

**Zone de risque** : `produced_application_minimum_contract` contient des obligations sur `runtime_entrypoint_contract` qui définissent `bootstrap_contract` et `runtime_prerequisites`. Ces éléments approchent la logique de déploiement runtime d'une application spécifique. Si la factory tente de normaliser le bootstrap au-delà du principe générique, elle risque d'absorber des décisions qui devraient rester dans le pipeline d'instanciation. La frontière exacte n'est pas bornée.

**Angle mort** : la factory ne dit pas explicitement quelle autorité (factory ou pipeline d'instanciation) a le dernier mot si une obligation du contrat minimal entre en conflit avec une contrainte domaine-spécifique d'une application instanciée.

### Axe 4 — Contrat minimal d'une application produite

Le contrat liste les blocs obligatoires : identity, manifest, canonical_dependency_contract, runtime_entrypoint_contract, minimum_configuration_contract, generic_module_reuse_contract, instantiated_specific_artifacts_contract, minimum_validation_contract, minimum_packaging_contract, minimum_observability_contract.

**Obligations manquantes** :

- **Pas d'axe de validation constitutionnel runtime** : aucune obligation de prouver qu'une application produite est 100 % locale, sans génération runtime, sans feedback généré à la volée. Les axes `minimum_validation_axes` ne le couvrent pas.
- **Pas d'obligation de traçabilité de la version du Référentiel** utilisée lors de la production : si le Référentiel est patché entre deux builds, aucune obligation ne force à re-déclarer la version utilisée dans le manifest de l'application.
- **Pas d'obligation de déclarer les projections dérivées utilisées** comme inputs traçables dans le manifest — l'observabilité liste `derived_projections_used` mais le manifest block ne le requiert pas explicitement.
- **Fingerprints de reproductibilité** : mentionnés comme blocs requis dans `produced_instance_identity` mais aucune définition du contenu attendu — un manifest vide sur ce point passerait le contrat.

**Obligations trop floues** :

- `bootstrap_contract` dans `runtime_entrypoint_contract` : notion déclarée mais non définie. Une IA ne sait pas ce qu'elle doit produire pour satisfaire cette obligation.
- `minimum_configuration_contract.minimum_blocks` liste `traceability` comme bloc minimal mais sans schéma ni contenu attendu.

**Obligations non auditables** :

- `generic_module_reuse_contract` : requis mais sans liste ni schéma. Un manifest peut déclarer avoir satisfait ce contrat sans qu'un validateur puisse le vérifier.

### Axe 5 — Validated derived execution projections

Le mécanisme est conceptuellement solide dans son intention mais **entièrement non opérationnalisé** :

**Risques identifiés** :

1. **Absence d'emplacement** (`emplacement_policy.status: TBD`) : une projection peut être générée sans localisation stable dans le repo. Une IA peut recevoir une projection dont elle ne sait pas si elle est la version courante ou une version stale.

2. **Absence de protocole de validation** : `derived_projection_conformity_status` dit `defined_in_principle_not_yet_tooling_backed` et liste `validator_definition` comme manquant. Sans validateur, le principe "strictement fidèle" est une déclaration d'intention, pas une garantie.

3. **Risque de paraphrase dangereuse** : sans protocole de régénération déterministe ni outil de diff normative, une projection régénérée à la main par une IA pourrait introduire une reformulation légèrement différente d'un invariant — suffisant pour qu'une application produite à partir de cette projection manque une contrainte.

4. **Risque de promotion implicite** : le pipeline (Rule 4) dit qu'une projection peut être "l'unique artefact fourni à une IA pour un travail donné". Sans mécanisme d'invalidation automatique d'une projection après un patch du canonique, une IA pourrait travailler sur une projection périmée sans le savoir.

5. **Risque de dépendance cachée** : si une projection "scope partiel" omet des invariants constitutionnels hors scope déclaré, mais qu'une IA en déduit implicitement l'absence de contrainte, la violation devient invisible jusqu'à la validation finale — si elle existe.

**Impact sur le principe fondateur** : le principe "une projection peut être l'unique artefact fourni à une IA" ne peut pas être tenu en sécurité tant que les points 1, 2 et 4 ne sont pas résolus. Ce n'est pas un défaut V0 acceptable — c'est un risque actif si des IA commencent à travailler sur des projections.

### Axe 6 — État reconnu, maturité et preuves

**Cohérence blockers/known_gaps/capabilities** : globalement cohérente. Les 3 blockers sont réels et les known_gaps sont bien identifiés.

**Sur-déclaration de maturité** :

- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` classée en `capabilities_present` — "l'intention de pipeline est posée". Classer une intention comme capacité présente est sémantiquement ambigu. Une intention posée n'est pas une capacité opérationnelle. Risque qu'une IA interprète cela comme "le pipeline est opérationnel".
- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `capabilities_present` — la règle est définie mais sans validateur, sans emplacement, sans protocole. La capacité est déclarée présente alors que l'opérationnalisation est absente. C'est au bord de la sur-déclaration.

**Preuves** : seules 2 evidences sont listées (`PF_EVIDENCE_PLAN_V2` et `PF_EVIDENCE_ARCHITECTURE_V0`). Le plan de référence n'est pas dans `docs/cores/current/` — si le fichier est déplacé ou renommé, l'évidence devient un lien mort sans mécanisme d'invalidation.

**Cohérence `last_assessment`** : `result: foundational_but_incomplete` est un constat juste et honnête.

### Axe 7 — Multi-IA en parallèle

La factory reconnaît le multi-IA comme exigence de premier rang mais les mécanismes manquent :

- **Pas de protocole d'assemblage** entre outputs IA : `deferred_challenges` dans l'architecture liste `assembly_protocol_between_ai_outputs` comme déféré — mais sans ce protocole, deux IA produisant des outputs sur des scopes adjacents peuvent créer des incohérences structurelles silencieuses.
- **Pas de convention de granularité modulaire** : `optimal_module_granularity` est aussi en `deferred_challenges`. Sans cela, une IA reçoit un scope trop large ou trop étroit selon l'interprétation, introduisant des chevauchements ou des trous.
- **Identifiants stables** : les IDs dans l'architecture sont stables — point positif.
- **Scopes trop larges** : le contrat minimal d'application est un seul bloc non décomposé pour le multi-IA. Une IA en charge du manifest ne sait pas quelle part est "sienne" vs une autre IA en charge de la validation.
- **Rapports non homogènes** : aucune convention de format de report multi-IA n'est définie. Le pipeline liste des outputs génériques (`*.yaml`, `*.md`) sans structure contractuelle commune.
- **Absence de protocole de résolution de conflit** : si deux IA produisent des outputs incompatibles sur des scopes adjacents, il n'existe pas de mécanisme de résolution.

### Axe 8 — Gouvernance release, manifest et traçabilité

**Anomalie principale** : les deux artefacts factory sont dans `docs/cores/current/` mais **explicitement hors du manifest officiel courant** (`platform_factory_state.yaml` — note: "Artefact V0 ajouté dans docs/cores/current/ sans intégration au manifest officiel actuel"). Cela crée un état de fait ambigu :

- Un acteur qui lit `docs/cores/current/` suppose que le contenu est "current" au sens officiel.
- Un acteur qui lit le manifest officiel ne voit pas ces artefacts.
- Le pipeline Rule 6 sépare release et promotion, mais la situation actuelle est antérieure à ce cadre : les artefacts sont "promus" dans current sans avoir traversé un pipeline de release formel.

**Risques** :
- Promotion implicite déjà effectuée avant que le mécanisme de promotion formel (STAGE_08) ne soit défini.
- Traçabilité incomplète : il n'existe pas de release materialization formelle pour ces artefacts V0.
- Un futur STAGE_07 + STAGE_08 ne sait pas comment traiter des artefacts déjà "dans current" sans provenance de pipeline formelle.

**Trou de gouvernance** : le pipeline définit une gouvernance pour les runs futurs mais ne définit pas comment régulariser la situation de la baseline V0 déjà en current.

### Axe 9 — Implémentabilité pipeline

Le pipeline V0 est suffisant pour lancer le cycle challenge/arbitrage/patch. Les stages sont bien découpés et les inputs/outputs sont nommés.

**Manques identifiés** :

- **STAGE_01** n'a pas de schéma de report obligatoire — le challenge report peut avoir des formats incompatibles entre runs ou entre IA différentes.
- **STAGE_02** règle "every challenge_report*.md must be considered" mais pas de mécanisme de consolidation défini si les reports sont contradictoires.
- **STAGE_04 et STAGE_06** utilisent le même prompt (`Make23PlatformFactoryValidation.md`) — ambiguïté sur la différence de validation entre patch-validation et core-validation. Un opérateur peut confondre les deux.
- **STAGE_07 et STAGE_08** sont déléguées à des specs séparées dont l'existence n'est pas vérifiable ici — risque que ces specs soient absentes ou incomplètes.
- **Pas de validator dédié** : STAGE_04 fait une validation manuelle via prompt. Sans validateur automatique, la détection de dérives normatives reste dépendante de la qualité du prompt utilisé.
- **Pas de définition de l'état "run complété"** : aucune définition de ce qui constitue un run fermé (critère de succès global au niveau pipeline).

### Axe 10 — Scénarios adversariaux

#### Scénario A — Dérive d'une projection dérivée

Une IA reçoit une projection dérivée couvrant le scope "runtime_entrypoint_contract". La projection a été générée manuellement 3 semaines avant un patch du Référentiel. Le Référentiel a été patché (nouveau paramètre opérationnel sur les seuils). La projection n'a pas été invalidée. L'IA produit une application avec les anciens paramètres référentiels. La factory ne détecte pas la dérive car il n'existe pas de mécanisme d'invalidation automatique de projection après patch canonique.

Mécanismes activés : `execution_projection_contract`, `produced_application_minimum_contract`.
Faiblesse révélée : absence de cycle de vie de projection avec invalidation automatique post-patch.
Origine : projections dérivées + pipeline.

#### Scénario B — Application "valide" violant un invariant constitutionnel

Une application produite passe tous les axes du `minimum_validation_contract` (structure, conformance, traceability, packaging). Elle est déclarée conforme. Elle contient un module qui génère du feedback runtime à partir d'un LLM embedé local. Rien dans les 4 axes de validation ne vérifie `INV_NO_RUNTIME_CONTENT_GENERATION` ou `INV_NO_RUNTIME_FEEDBACK_GENERATION`. L'application est livrée comme "constitutionnellement compatible".

Mécanismes activés : `minimum_validation_contract`, `PF_PRINCIPLE_CANONICAL_TRACEABILITY`.
Faiblesse révélée : absence d'un axe de validation `runtime_constitutional_constraints`.
Origine : contrat minimal d'application + architecture.

#### Scénario C — Collision multi-IA

Deux IA travaillent en parallèle : IA-1 sur le manifest, IA-2 sur la configuration minimale. Leurs scopes se chevauchent sur la déclaration des `canonical_dependencies` (présente dans manifest ET dans configuration minimale). IA-1 déclare une version du canonique, IA-2 en déclare une autre (après un patch entre les deux runs). L'assembleur reçoit deux outputs contradictoires sans protocole de résolution. Le manifest final contient une version, la configuration une autre. L'application est incohérente mais passe le packaging.

Mécanismes activés : `multi_ia_parallel_readiness`, `produced_application_minimum_contract`.
Faiblesse révélée : pas de source de vérité unique pour la version canonique déclarée, pas de protocole de résolution de conflit.
Origine : architecture multi-IA + pipeline.

#### Scénario D — Gouvernance/release insuffisante

Un opérateur lance un pipeline run en STAGE_03 directement (sans STAGE_01 ni STAGE_02) en invoquant la clause "released baseline". Il produit un patchset, le valide via STAGE_04, l'applique en STAGE_05 et le promeut en STAGE_08. Le pipeline ne dit pas explicitement qu'un run doit commencer par STAGE_01 si un challenge report est déjà présent de la session précédente. Le fichier du run précédent en `work/01_challenge/` est considéré comme "current" pour le STAGE_02 de ce run. Une correction arbitrée précédemment est silencieusement perdue.

Mécanismes activés : `pipeline.md` Rule 3, STAGE_02 règle "every challenge_report must be considered".
Faiblesse révélée : pas de lien d'appartenance entre challenge reports et runs de pipeline. Un report d'un run antérieur peut polluer un run ultérieur.
Origine : pipeline governance.

### Axe 11 — Priorisation

| Priorité | ID | Description courte |
|---|---|---|
| **CRITIQUE** | C-01 | Invariants constitutionnels runtime non propagés dans les axes de validation du contrat minimal |
| **CRITIQUE** | C-02 | Projections dérivées sans emplacement, sans validateur, sans invalidation post-patch |
| **CRITIQUE** | C-03 | Artefacts dans current hors manifest officiel — zone grise de gouvernance release |
| **ÉLEVÉ** | E-01 | Contrat minimal : obligations de fingerprints et bootstrap_contract non définies |
| **ÉLEVÉ** | E-02 | Absence de protocole d'assemblage multi-IA et de convention de granularité |
| **ÉLEVÉ** | E-03 | Sur-déclaration de maturité : `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en present |
| **MODÉRÉ** | M-01 | Même prompt STAGE_04 et STAGE_06 — ambiguïté sur la différence de validation |
| **MODÉRÉ** | M-02 | Absence de lien d'appartenance run entre challenge reports et exécutions pipeline |
| **MODÉRÉ** | M-03 | Frontière factory/pipeline d'instanciation non bornée sur bootstrap_contract |
| **MODÉRÉ** | M-04 | Evidence `PF_EVIDENCE_PLAN_V2` pointant un fichier hors current — risque de lien mort |
| **FAIBLE** | F-01 | Format de challenge report non contractualisé dans STAGE_01 |
| **FAIBLE** | F-02 | Pas de définition de "run complété" au niveau pipeline |

---

## Risques prioritaires

### C-01 — Invariants constitutionnels runtime non propagés dans le contrat minimal

La factory peut produire une application qui passe sa validation interne tout en violant `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE`.

### C-02 — Projections dérivées non opérationnalisées avec risque de dérive normative active

L'emplacement est TBD, la validation est absente, l'invalidation post-patch n'existe pas. Si des IA commencent à utiliser des projections avant résolution de ces points, la dérive normative silencieuse est probable.

### C-03 — Anomalie de gouvernance release sur les artefacts V0 en current

La factory est dans current sans provenance de pipeline formelle. Le manifest officiel ne les référence pas. Les stages 07 et 08 ne savent pas comment traiter ce cas de régularisation initial.

---

## Points V0 acceptables

Les points suivants sont des incomplétudes V0 normales, reconnues dans l'état et sans risque immédiat de violation :

- Schémas détaillés (manifest, configuration, packaging, runtime entrypoint) non finalisés — reconnus dans `capabilities_absent` et `known_gaps`.
- Granularité modulaire et protocole d'assemblage IA non définis — déférés explicitement dans `deferred_challenges`.
- Validateurs non implémentés — reconnus dans `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` (absent).
- Pipeline d'instanciation non spécifié — correctement hors périmètre.
- `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` — reconnu dans known_gaps.
- Absence de `STAGE_07` et `STAGE_08` matérialisés ici — specs séparées référencées.
- Absence de contenu domaine — correctement hors périmètre.

Ces points ne compromettent pas la capacité à lancer un cycle de correction crédible à partir de cette baseline.

---

## Corrections à arbitrer avant patch

---

### Problème C-01 — Absence d'axe constitutionnel runtime dans les axes de validation

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Localisation** | `platform_factory_architecture.yaml` — section `contracts` |
| **Nature du problème** | Les invariants constitutionnels de runtime (local, pas de génération, pas de réseau, pas de génération feedback hors template) ne sont pas inclus dans les axes minimaux de validation d'une application produite. |
| **Type de problème** | Compatibilité constitutionnelle + complétude + gouvernance |
| **Gravité** | Critique |
| **Impact factory** | La factory ne peut pas prouver qu'une application qu'elle produit respecte les invariants fondamentaux de la Constitution. |
| **Impact application produite** | Une application peut être déclarée conforme tout en violant des invariants constitutionnels non testés. |
| **Impact IA** | Une IA utilisant le contrat comme guide de validation ne sait pas qu'elle doit vérifier ces invariants. |
| **Impact gouvernance/release** | Le dispositif de release ne peut pas certifier la conformité constitutionnelle. |
| **Correction à arbitrer** | Ajouter un axe `runtime_constitutional_constraints` dans `minimum_axes` et définir au minimum les invariants à vérifier : runtime local, pas de génération contenu, pas de génération feedback, patchs précomputés hors session, atomicité. L'humain arbitre si cet axe est une obligation "déclarative" (le manifeste doit asserter la conformité) ou "probatoire" (un validateur doit le vérifier). |
| **Lieu probable de correction** | architecture |

---

### Problème C-02 — Projections dérivées sans opérationnalisation (emplacement, validateur, invalidation)

| Champ | Valeur |
|---|---|
| **Élément concerné** | `generated_projection_rules`, `contracts.execution_projection_contract`, `PLATFORM_FACTORY_STATE.derived_projection_conformity_status` |
| **Localisation** | `platform_factory_architecture.yaml` — section `generated_projection_rules` + `contracts` ; `platform_factory_state.yaml` — section `derived_projection_conformity_status` |
| **Nature du problème** | L'emplacement des projections est TBD, il n'y a pas de validateur, pas de protocole de régénération déterministe, pas d'invalidation automatique post-patch canonique. |
| **Type de problème** | Implémentabilité + gouvernance + exploitabilité IA |
| **Gravité** | Critique |
| **Impact factory** | Le mécanisme central d'interface avec les IA est une déclaration d'intention non opérationnelle. |
| **Impact application produite** | Une application produite à partir d'une projection périmée peut diverger du canonique sans détection. |
| **Impact IA** | Une IA ne peut pas savoir si une projection est courante, valide ou périmée. |
| **Impact gouvernance/release** | Aucun release gate ne peut bloquer une projection non conforme car aucun validateur n'existe. |
| **Correction à arbitrer** | Arbitrer : (a) définir l'emplacement des projections dérivées (`emplacement_policy`) ; (b) définir le protocole minimal de validation avant usage ; (c) définir le mécanisme d'invalidation d'une projection après patch canonique. L'humain arbitre le niveau de formalisme V0 acceptable sur chacun de ces 3 sous-points. |
| **Lieu probable de correction** | architecture + state + validator/tooling |

---

### Problème C-03 — Artefacts V0 en current hors manifest officiel

| Champ | Valeur |
|---|---|
| **Élément concerné** | `metadata.notes` (state), `metadata.notes` (architecture) |
| **Localisation** | `platform_factory_state.yaml` et `platform_factory_architecture.yaml` — notes explicites |
| **Nature du problème** | Les deux artefacts sont dans `docs/cores/current/` mais hors du manifest officiel courant. Cette situation est antérieure au mécanisme de promotion formel du pipeline (STAGE_08). |
| **Type de problème** | Gouvernance + traçabilité |
| **Gravité** | Critique |
| **Impact factory** | Zone grise sur le statut officiel de ces artefacts. Un acteur peut les considérer comme "officiels" ou "non officiels" selon sa lecture. |
| **Impact application produite** | Une application produite en référençant ces artefacts peut ne pas être traçable vers un état de release officiel. |
| **Impact IA** | Une IA ne peut pas savoir si ces artefacts ont autorité officielle ou sont en cours d'intégration. |
| **Impact gouvernance/release** | Le pipeline STAGE_07 et STAGE_08 ne définissent pas comment traiter la régularisation d'artefacts déjà en current sans provenance pipeline formelle. |
| **Correction à arbitrer** | Arbitrer : (a) faut-il intégrer ces artefacts au manifest officiel immédiatement ou attendre un premier cycle pipeline complet ? ; (b) faut-il documenter explicitement la provenance de la baseline V0 dans un release record minimal ? L'humain arbitre la voie de régularisation. |
| **Lieu probable de correction** | manifest/release governance |

---

### Problème E-01 — Obligations contrat minimal non définies (fingerprints, bootstrap_contract)

| Champ | Valeur |
|---|---|
| **Élément concerné** | `produced_instance_identity.reproducibility_fingerprints`, `runtime_entrypoint_contract.bootstrap_contract` |
| **Localisation** | `platform_factory_architecture.yaml` — section `contracts.produced_application_minimum_contract` |
| **Nature du problème** | Ces obligations sont déclarées requises mais sans définition de contenu. Un manifest les satisfait par simple présence d'une clé vide. |
| **Type de problème** | Complétude + implémentabilité |
| **Gravité** | Élevé |
| **Impact factory** | La factory ne peut pas vérifier que ces obligations sont réellement remplies. |
| **Impact application produite** | Une application peut déclarer des fingerprints vides ou un bootstrap_contract non défini et passer le contrat. |
| **Impact IA** | Une IA ne sait pas ce qu'elle doit produire pour satisfaire ces obligations. |
| **Impact gouvernance/release** | La reproductibilité et l'entrée runtime ne sont pas auditables. |
| **Correction à arbitrer** | Définir a minima le contenu attendu de `reproducibility_fingerprints` (hash de build ? version des inputs canoniques ?) et de `bootstrap_contract` (liste de prérequis runtime ? format ? scope ?). L'humain arbitre le niveau de détail V0 acceptable. |
| **Lieu probable de correction** | architecture |

---

### Problème E-02 — Absence de protocole d'assemblage et de granularité multi-IA

| Champ | Valeur |
|---|---|
| **Élément concerné** | `multi_ia_parallel_readiness.deferred_challenges`, `PLATFORM_FACTORY_STATE.multi_ia_parallel_readiness_status.missing` |
| **Localisation** | `platform_factory_architecture.yaml` — section `multi_ia_parallel_readiness` ; `platform_factory_state.yaml` — section `multi_ia_parallel_readiness_status` |
| **Nature du problème** | Assemblage entre outputs IA et granularité modulaire sont explicitement déférés mais sans date ni critère de déclenchement. Si des IA commencent à travailler en parallèle, ces trous produisent des incohérences d'assemblage silencieuses. |
| **Type de problème** | Implémentabilité + gouvernance + exploitabilité IA |
| **Gravité** | Élevé |
| **Impact factory** | Le travail multi-IA en parallèle n'est pas praticable de manière sûre. |
| **Impact application produite** | Des applications produites par IA en parallèle peuvent être incohérentes dans leur manifest ou leur configuration. |
| **Impact IA** | Les IA ne savent pas comment assembler leurs outputs ou résoudre les conflits. |
| **Impact gouvernance/release** | La release peut intégrer des outputs contradictoires. |
| **Correction à arbitrer** | Arbitrer si un protocole minimal d'assemblage (ex : source de vérité unique pour la version canonique, règle de précédence en cas de conflit) doit être posé avant tout usage multi-IA, ou si le déféré est acceptable jusqu'à un prochain run. |
| **Lieu probable de correction** | architecture + pipeline |

---

### Problème E-03 — Sur-déclaration de maturité dans capabilities_present

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`, `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` |
| **Localisation** | `platform_factory_state.yaml` — section `capabilities_present` |
| **Nature du problème** | "Intention posée" et "règle définie sans outillage" sont classées en `capabilities_present`. Une intention ou une règle non outillée n'est pas une capacité opérationnelle présente. |
| **Type de problème** | Faux niveau de maturité |
| **Gravité** | Élevé |
| **Impact factory** | Une IA lisant l'état peut sur-estimer les capacités disponibles et construire dessus. |
| **Impact application produite** | Une application peut être conçue en supposant que les projections sont validables alors qu'elles ne le sont pas. |
| **Impact IA** | Risque d'hallucination de capacité basée sur un état surdéclaré. |
| **Impact gouvernance/release** | Un arbitrage de release peut se baser sur une maturité inexacte. |
| **Correction à arbitrer** | Arbitrer si ces deux capacités doivent être reclassées en `capabilities_partial` (règle définie mais pas outillée) et si le wording doit être ajusté pour distinguer "principe déclaré" de "capacité opérationnelle présente". |
| **Lieu probable de correction** | state |

---

### Problème M-01 — Ambiguïté STAGE_04 vs STAGE_06 même prompt

| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` STAGE_04 et STAGE_06, prompt `Make23PlatformFactoryValidation.md` |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md` |
| **Nature du problème** | Les deux stages utilisent le même prompt sans différenciation. STAGE_04 valide le patchset, STAGE_06 valide les artefacts patched. Un opérateur ou une IA peut ne pas comprendre la différence d'objet entre les deux validations. |
| **Type de problème** | Implémentabilité + gouvernance |
| **Gravité** | Modéré |
| **Impact factory** | Risque de validation redondante sans couverture distincte, ou de confusion sur ce qu'on valide. |
| **Impact gouvernance/release** | Un report de validation STAGE_04 peut être confondu avec un report STAGE_06. |
| **Correction à arbitrer** | Arbitrer si le même prompt est intentionnel (avec paramétrage différent à l'appel) ou si deux prompts distincts sont nécessaires. |
| **Lieu probable de correction** | pipeline |

---

### Problème M-02 — Absence de lien d'appartenance run dans les challenge reports

| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` STAGE_02 règle "every challenge_report*.md must be considered" |
| **Localisation** | `docs/pipelines/platform_factory/pipeline.md` |
| **Nature du problème** | Les challenge reports dans `work/01_challenge/` ne sont pas liés à un run identifié. Un report d'un run antérieur peut être consommé dans un run ultérieur sans que l'opérateur le sache. |
| **Type de problème** | Gouvernance + traçabilité |
| **Gravité** | Modéré |
| **Impact factory** | Arbitrage pollué par des findings d'un run précédent déjà traités ou invalidés. |
| **Impact gouvernance/release** | Traçabilité incomplète entre runs de pipeline. |
| **Correction à arbitrer** | Arbitrer si les reports doivent être liés à un run_id et si le STAGE_02 doit filtrer par run_id ou consommer tous les reports présents intentionnellement. |
| **Lieu probable de correction** | pipeline |

---

_Rapport généré par PPLXAI (Perplexity AI) — STAGE_01_CHALLENGE — 2026-04-04_
_Ce rapport ne contient aucun patch, aucune arbitrage de substitution humain, aucun scan de découverte._
_Destiné à STAGE_02_FACTORY_ARBITRAGE._
