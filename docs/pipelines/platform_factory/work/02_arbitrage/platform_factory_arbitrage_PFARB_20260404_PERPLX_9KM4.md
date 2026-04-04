# Proposition d'arbitrage — Platform Factory STAGE_02

## arbitrage_run_id

`PFARB_20260404_PERPLX_9KM4`

## Date

2026-04-04

## Agent

PERPLX (Perplexity AI — Sonnet 4.6)

---

## Challenge reports considérés

| # | challenge_run_id | Agent | Taille |
|---|---|---|---|
| 1 | PFCHAL_20260404_GPT54_X7K2Q | GPT54 | ~600 lignes |
| 2 | PFCHAL_20260404_PERPLX_7K2R | PERPLX | ~444 lignes |
| 3 | PFCHAL_20260404_PERPLX_A1J77P | PERPLX | ~379 lignes |
| 4 | PFCHAL_20260404_PERP_K7X2 | PERP | ~335 lignes |
| 5 | PFCHAL_20260404_PPLXAI_5LVBSV | PPLXAI | ~425 lignes |
| 6 | PFCHAL_20260404_PXADV_BB1MZX | PXADV | ~384 lignes |

Tous les 6 challenge reports présents dans `work/01_challenge/` ont été lus intégralement.

---

## Résumé exécutif

La baseline Platform Factory V0.1 est **constitutionnellement cohérente dans ses intentions et légitime comme baseline released**. Sa séparation prescriptif/constatif est saine, ses dépendances canoniques sont déclarées, et sa posture V0 est honnête. Elle est **exploitable pour STAGE_03_FACTORY_PATCH_SYNTHESIS**.

Six familles de risques convergent dans tous les challenge reports et nécessitent une décision d'arbitrage avant patch :

1. **Contrat minimal d'application produite insuffisant pour prouver la conformité constitutionnelle runtime** — risque le plus sévère, présent dans les 6 rapports avec gravité critique/élevée.
2. **Projections dérivées non opérationnalisées** (emplacement TBD, validateur absent, protocole de régénération absent) — présent dans les 6 rapports.
3. **Protocole d'assemblage multi-IA absent** — exigence de premier rang déclarée mais non tenue opérationnellement, présent dans les 6 rapports.
4. **Gouvernance release/manifest/current ambiguë** — les artefacts V0 sont dans `current/` sans intégration au manifest officiel ni matérialisation formelle de release.
5. **Sur-déclaration de maturité dans `capabilities_present`** — certaines capacités classées "présentes" ne sont que des règles déclarées sans outillage.
6. **STAGE_05 sans contrat d'atomicité/rollback** — risque de violation de `INV_NO_PARTIAL_PATCH_STATE` lors d'un apply partiel (relevé dans 2 rapports, confirmé constitutionnellement).

Les schémas fins (manifest exact, runtime typology, configuration schema, packaging schema) sont des incomplétudes V0 normales, reconnues dans le state, acceptables sans correction urgente.

---

## Synthèse des constats convergents

### Convergence forte (≥5/6 rapports)

**CONV-01 — Contrat minimal insuffisant pour prouver la conformité constitutionnelle runtime**
- Tous les rapports (6/6) identifient que `produced_application_minimum_contract` ne couvre pas les invariants `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`.
- Une application produite peut être validée par la factory tout en violant ces invariants critiques.
- Les rapports GPT54, PERPLX_A1J77P, PPLXAI et PXADV qualifient ce point de "critique".

**CONV-02 — Projections dérivées règle posée, mécanisme absent**
- Tous les rapports (6/6) convergent : `emplacement_policy: TBD`, validateur absent, protocole de régénération absent.
- Le risque est une dérive normative silencieuse si des IAs utilisent des projections non vérifiables.
- L'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est déclaré mais non instrumenté.

**CONV-03 — Protocole multi-IA absent**
- 6/6 rapports identifient l'absence de `decomposition_protocol` et d'`ai_output_assembly_protocol`.
- La promesse "multi-IA first-rank" reste purement déclarative.
- Risque de collision silencieuse lors d'un travail parallèle.

**CONV-04 — Gouvernance release/manifest ambiguë**
- 6/6 rapports identifient que les artefacts sont dans `current/` mais hors manifest officiel courant.
- Statut ambigu entre "présent en current" et "officiellement gouverné par release".

### Convergence modérée (3-4/6 rapports)

**CONV-05 — Sur-déclaration de maturité `capabilities_present`**
- Relevé par PERPLX_A1J77P, PPLXAI, PXADV : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` et `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` sont classées comme capacités présentes alors que leur outillage est totalement absent.

**CONV-06 — STAGE_05 sans atomicité/rollback documenté**
- Relevé explicitement par PXADV et PERPLX_7K2R. Confirmé constitutionnellement vis-à-vis de `INV_NO_PARTIAL_PATCH_STATE`.

**CONV-07 — Handoff contract factory → instanciation implicite**
- Relevé par GPT54, PERPLX_A1J77P : la frontière entre contrat minimal factory et responsabilités du pipeline d'instanciation aval n'est pas matérialisée.

### Convergence faible (1-2/6 rapports)

**CONV-08 — Critères de sortie de maturité absents**
- Relevé par PERP_K7X2 et partiellement par PPLXAI : le state ne définit pas de critères de progression V0 → V0.2 ou V1.

**CONV-09 — STAGE_04 vs STAGE_06 même prompt, distinction d'objet insuffisante**
- Relevé par PPLXAI uniquement : les deux stages utilisent `Make23PlatformFactoryValidation.md` sans différenciation explicite de l'objet de validation.

---

## Propositions d'arbitrage par thème

---

### THEME_A — Contrat minimal et compatibilité constitutionnelle runtime

#### ARB-A1 — Ajouter un axe `runtime_constitutional_compliance` dans `minimum_validation_contract`

- **Élément concerné** : `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Aucun axe de validation du contrat minimal ne couvre les invariants `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE`.
- **Statut proposé** : `retained`
- **Gravité** : critique
- **Justification** : Convergence 6/6 rapports. Sans cet axe, la factory ne peut pas certifier qu'une application produite respecte les invariants fondamentaux de la Constitution. C'est une brèche normative, pas une incomplétude V0 normale. La correction est ciblée et ne nécessite pas de réécriture profonde.
- **Dépendance** : ARB-A2 (le mode de satisfaction de l'axe — déclaratif ou probatoire — peut être arbitré séparément)
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus** : `strong`
- **Note d'arbitrage** : L'humain doit arbitrer si l'axe est **déclaratif** (le manifest d'une app produite doit asserter sa conformité) ou **probatoire** (un validateur doit le vérifier). Pour une V0.1 patchée, le mode déclaratif est acceptable, à condition que le mode probatoire soit déclaré comme objectif de V0.2 ou V1.

#### ARB-A2 — Mode de satisfaction de `runtime_constitutional_compliance` : déclaratif V0, probatoire V1

- **Élément concerné** : `contracts.produced_application_minimum_contract.minimum_validation_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Sans outillage de validation, un axe ajouté reste virtuel si son mode de satisfaction n'est pas tranché.
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : Décision de mode de satisfaction nécessaire pour que l'axe ajouté (ARB-A1) soit utilisable dans le patch. Proposé : mode déclaratif obligatoire dans le manifest pour V0.1 + obligation de probatoire à instrumenter dans un cycle ultérieur.
- **Dépendance** : ARB-A1
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus** : `strong`

#### ARB-A3 — Handoff contract factory → instanciation

- **Élément concerné** : `platform_layers.transformation_chain.contracts` / frontière factory/instanciation
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : La frontière entre ce que la factory garantit et ce que le pipeline d'instanciation doit compléter n'est pas matérialisée.
- **Statut proposé** : `deferred`
- **Gravité** : modéré
- **Justification** : Relevé par 2/6 rapports (GPT54, PERPLX_A1J77P). La V0.1 est acceptable sans handoff contract formalisé tant que le pipeline d'instanciation n'existe pas encore. À formaliser au moment de la création du pipeline d'instanciation.
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus** : `medium`

---

### THEME_B — Projections dérivées

#### ARB-B1 — Décider l'emplacement des projections dérivées (`emplacement_policy: TBD`)

- **Élément concerné** : `generated_projection_rules.emplacement_policy`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : TBD non résolu, bloquant la traçabilité et l'exploitabilité IA des projections.
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : Convergence 6/6. Sans emplacement fixe, les IAs ne savent pas où produire ni où chercher les projections. C'est un prérequis à tout usage opérationnel, même minimal.
- **Lieu probable de correction** : `architecture` + `state`
- **Niveau de consensus** : `strong`
- **Note d'arbitrage** : L'humain doit décider du chemin de stockage (proposition : `docs/pipelines/platform_factory/projections/` ou `work/projections/`). Ce choix ne nécessite pas de restructuration architecturale.

#### ARB-B2 — Définir un protocole minimal de validation avant usage d'une projection

- **Élément concerné** : `contracts.execution_projection_contract`, `derived_projection_conformity_status`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : Aucun mécanisme ne permet de valider qu'une projection est conforme avant usage par une IA.
- **Statut proposé** : `retained` (protocole déclaratif minimal) / `deferred` (validator outillé)
- **Gravité** : élevé
- **Justification** : Sans protocole de validation, l'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est inopposable. Pour V0.1 : poser un critère de validation déclaratif (la projection doit référencer la version canonique source et la date de génération). Outillage : différé V1.
- **Dépendance** : ARB-B1
- **Lieu probable de correction** : `architecture` + `validator/tooling`
- **Niveau de consensus** : `strong`

#### ARB-B3 — Définir un mécanisme minimal d'invalidation post-patch canonique

- **Élément concerné** : `generated_projection_rules`, `derived_projection_conformity_status`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : Après un patch canonique, une projection périmée peut continuer à être utilisée sans signal d'invalidation.
- **Statut proposé** : `retained` (règle déclarative) / `deferred` (outillage automatique)
- **Gravité** : élevé
- **Justification** : Pour V0.1 : ajouter une règle dans `generated_projection_rules` stipulant qu'une projection est invalidée si la version canonique source a changé. Mécanisme automatique : différé.
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus** : `strong`

---

### THEME_C — Multi-IA parallel readiness

#### ARB-C1 — Poser un protocole d'assemblage minimal (scope, identification, point d'assemblage)

- **Élément concerné** : `multi_ia_parallel_readiness`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : `decomposition_protocol` et `ai_output_assembly_protocol` sont absents. Deux IAs en parallèle peuvent produire des sorties incompatibles sans aucun mécanisme de détection ou d'arbitrage.
- **Statut proposé** : `retained` (protocole minimal) — protocole complet : `deferred`
- **Gravité** : élevé
- **Justification** : Convergence 6/6. Exigence déclarée "first-rank" non tenue est une incohérence interne grave. Pour V0.1 : poser un bloc `multi_ia_decomposition_minimum_protocol` avec au minimum (1) règle de découpage de scope borné, (2) règle d'identification des sorties par `challenge_run_id` ou `arbitrage_run_id`, (3) point d'assemblage désigné (un humain ou un stage dédié).
- **Lieu probable de correction** : `architecture` + `pipeline`
- **Niveau de consensus** : `strong`

#### ARB-C2 — Promouvoir `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker explicite

- **Élément concerné** : `blockers` dans `platform_factory_state.yaml`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Ce gap est reconnu mais non classé comme blocker, ce qui en minimise la visibilité opérationnelle pour une exigence de premier rang.
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : Cohérent avec la posture du pipeline ("multi-IA readiness is a first-rank design constraint"). La promotion en blocker `medium` avec condition de résolution explicite est une correction de gouvernance légère.
- **Lieu probable de correction** : `state`
- **Niveau de consensus** : `strong`

---

### THEME_D — Gouvernance release / manifest / current

#### ARB-D1 — Documenter explicitement le régime transitoire de gouvernance de la baseline V0

- **Élément concerné** : metadata + notes dans les deux artefacts + Rule 3 du pipeline
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml` + `pipeline.md`
- **Problème** : Les artefacts sont dans `current/` et déclarés "released baseline" par Rule 3 sans artefact de release formel (tag, manifest entry, release record minimal).
- **Statut proposé** : `retained` (documentation explicite du régime transitoire) / `deferred` (extension du manifest officiel, intégration formelle via STAGE_07/STAGE_08)
- **Gravité** : modéré
- **Justification** : Convergence 6/6. Pour V0.1 : ajouter dans le state la mention explicite que les artefacts V0 ont été posés hors cycle pipeline formel (régime d'initialisation) et que leur régularisation est l'objet d'un prochain STAGE_07. Cela supprime l'ambiguïté sans nécessiter d'intégration manifest immédiate.
- **Lieu probable de correction** : `state` + `manifest/release governance`
- **Niveau de consensus** : `strong`

#### ARB-D2 — Extension du manifest officiel ou companion manifest

- **Élément concerné** : manifest officiel courant + artefacts `platform_factory`
- **Localisation** : `manifest/release governance`
- **Problème** : Les artefacts ne sont pas référencés dans le manifest officiel.
- **Statut proposé** : `deferred` — à traiter dans STAGE_07_FACTORY_RELEASE_MATERIALIZATION
- **Gravité** : modéré
- **Justification** : STAGE_07 et STAGE_08 existent précisément pour cette opération. Forcer une intégration manifest dans ce cycle serait hors périmètre du STAGE_02. Le régime transitoire (ARB-D1) couvre l'ambiguïté immédiate.
- **Lieu probable de correction** : `manifest/release governance`
- **Niveau de consensus** : `strong`

---

### THEME_E — Maturité déclarée vs maturité réelle

#### ARB-E1 — Reclasser `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `capabilities_partial`

- **Élément concerné** : `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Règle déclarée dans l'architecture, mais mécanisme opérationnel (emplacement, validator, régénération) totalement absent. Classement en `present` induit une surestimation de maturité.
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : Convergence PERPLX_A1J77P, PPLXAI, PXADV. Correction légère, sans impact fonctionnel direct mais essentielle pour l'honnêteté de l'état. La description doit distinguer "règle déclarée" (✓ présent) de "mécanisme opérationnel" (✗ absent → `partial`).
- **Lieu probable de correction** : `state`
- **Niveau de consensus** : `strong`

#### ARB-E2 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément concerné** : `capabilities_present.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : "Intention de pipeline définie" ≠ pipeline entièrement exécutable (plusieurs prompts requis non encore vérifiés présents).
- **Statut proposé** : `retained` (correction de wording uniquement)
- **Gravité** : modéré
- **Justification** : Relevé par PPLXAI, cohérent avec PERP_K7X2. Correction de wording sans restructuration.
- **Lieu probable de correction** : `state`
- **Niveau de consensus** : `medium`

#### ARB-E3 — Ajouter des critères de sortie de maturité par couche

- **Élément concerné** : `maturity_by_layer`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Aucun critère de progression de V0 vers une version plus mature.
- **Statut proposé** : `deferred`
- **Gravité** : modéré
- **Justification** : Relevé par PERP_K7X2 principalement. Nécessite décision humaine sur les objectifs de maturité cibles. À inclure dans un cycle de révision du state après stabilisation du premier run complet du pipeline.
- **Lieu probable de correction** : `state`
- **Niveau de consensus** : `medium`

---

### THEME_F — Pipeline et atomicité

#### ARB-F1 — Ajouter une règle d'atomicité minimale dans STAGE_05

- **Élément concerné** : `STAGE_05_FACTORY_APPLY` dans `pipeline.md`
- **Localisation** : `pipeline.md`
- **Problème** : STAGE_05 ne précise aucun mécanisme garantissant l'atomicité de l'application du patchset. `INV_NO_PARTIAL_PATCH_STATE` exige un rollback en cas de patch partiellement appliqué.
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : Relevé par PXADV et PERPLX_7K2R. Violation constitutionnelle potentielle. Correction légère dans `pipeline.md` : ajouter une règle "tout ou rien" dans la description de STAGE_05, avec instruction de nommage ou de signal en cas d'échec partiel.
- **Lieu probable de correction** : `pipeline`
- **Niveau de consensus** : `medium`

#### ARB-F2 — Clarifier la distinction d'objet STAGE_04 vs STAGE_06

- **Élément concerné** : `STAGE_04_FACTORY_PATCH_VALIDATION` et `STAGE_06_FACTORY_CORE_VALIDATION` dans `pipeline.md`
- **Localisation** : `pipeline.md`
- **Problème** : Les deux stages utilisent le même prompt `Make23PlatformFactoryValidation.md` sans différenciation explicite de l'objet de validation.
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : Relevé par PPLXAI (M-01). Risque de confusion opérateur/IA. Correction simple dans `pipeline.md` : préciser que STAGE_04 valide le patchset (avant application) et STAGE_06 valide les artefacts patched (après application).
- **Lieu probable de correction** : `pipeline`
- **Niveau de consensus** : `medium`

#### ARB-F3 — Vérifier l'existence et la complétude des prompts partagés requis

- **Élément concerné** : `Required shared prompts` dans `pipeline.md`
- **Localisation** : `docs/prompts/shared/`
- **Problème** : Dépendance non vérifiée à des artefacts externes au pipeline. Un stage peut être bloqué si un prompt est absent.
- **Statut proposé** : `deferred` (vérification à réaliser avant STAGE_03)
- **Gravité** : modéré
- **Justification** : Relevé par PERP_K7X2 (C5). Hors périmètre de la factory architecture elle-même, mais bloquant pour l'exécutabilité du pipeline.
- **Lieu probable de correction** : `hors périmètre factory` (repo prompts)
- **Niveau de consensus** : `medium`

---

### THEME_G — Reproductibilité et fingerprints

#### ARB-G1 — Définir le contenu minimal de `reproducibility_fingerprints`

- **Élément concerné** : `produced_application_minimum_contract.identity.required_blocks.reproducibility_fingerprints`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Bloc déclaré requis mais sans définition de contenu minimal. Un manifest peut satisfaire l'obligation par une clé vide.
- **Statut proposé** : `deferred`
- **Gravité** : modéré
- **Justification** : Relevé par PPLXAI et PXADV. Incomplétude réelle mais acceptable en V0 tant que le pipeline d'instanciation n'existe pas encore. La définition de contenu dépend des choix du pipeline d'instanciation aval.
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus** : `medium`

---

## Points retenus (summary)

| # | Arbitrage | Localisation | Gravité | Consensus |
|---|---|---|---|---|
| ARB-A1 | Ajouter axe `runtime_constitutional_compliance` dans `minimum_validation_contract` | architecture | critique | strong |
| ARB-A2 | Mode déclaratif V0, mode probatoire V1 pour ARB-A1 | architecture | élevé | strong |
| ARB-B1 | Décider l'emplacement des projections dérivées | architecture + state | élevé | strong |
| ARB-B2 | Protocole minimal de validation des projections (déclaratif V0) | architecture + validator/tooling | élevé | strong |
| ARB-B3 | Règle d'invalidation post-patch canonique (déclarative V0) | architecture | élevé | strong |
| ARB-C1 | Protocole d'assemblage multi-IA minimal | architecture + pipeline | élevé | strong |
| ARB-C2 | Promouvoir `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker | state | modéré | strong |
| ARB-D1 | Documenter le régime transitoire de gouvernance de la baseline V0 | state + manifest/release governance | modéré | strong |
| ARB-E1 | Reclasser `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `partial` | state | modéré | strong |
| ARB-E2 | Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | state | modéré | medium |
| ARB-F1 | Règle d'atomicité STAGE_05 (tout ou rien, signal d'échec) | pipeline | élevé | medium |
| ARB-F2 | Clarifier la distinction STAGE_04 vs STAGE_06 dans `pipeline.md` | pipeline | modéré | medium |

---

## Points rejetés

| # | Élément | Justification du rejet |
|---|---|---|
| — | Sur-correction de la compatibilité constitutionnelle au-delà du contrat minimal | La factory ne doit pas réécrire la Constitution ni dupliquer ses règles. L'axe déclaratif dans le contrat minimal est suffisant pour V0.1. Aller plus loin violerait `PF_PRINCIPLE_NO_NORM_DUPLICATION`. |
| — | Réécriture profonde de l'architecture prescriptive V0 | La baseline V0 est assumée. Les corrections ciblées sont préférables à une réécriture. Un trop grand delta de patch fragilise la traçabilité et le pipeline aval. |

---

## Points différés

| # | Arbitrage | Justification | Condition de résolution |
|---|---|---|---|
| ARB-A3 | Handoff contract factory → instanciation | Pipeline d'instanciation inexistant. Formaliser lors de sa création. | Création du pipeline d'instanciation |
| ARB-B2 (partie probatoire) | Outillage validator pour projections | Dépend d'un outillage non encore défini. | Cycle V1, après premier run complet du pipeline |
| ARB-B3 (partie outillage) | Mécanisme automatique d'invalidation | Idem | Cycle V1 |
| ARB-C1 (protocole complet) | Protocole complet d'assemblage multi-IA | Le protocole complet dépend de l'expérience opérationnelle. | Après premier usage multi-IA réel |
| ARB-D2 | Extension du manifest officiel | Objet de STAGE_07 et STAGE_08 du pipeline. | STAGE_07_FACTORY_RELEASE_MATERIALIZATION |
| ARB-E3 | Critères de sortie de maturité | Décision humaine sur objectifs cibles nécessaire. | Après premier run pipeline complet |
| ARB-F3 | Vérification des prompts partagés | Hors périmètre factory architecture, mais à réaliser avant STAGE_03. | Avant lancement STAGE_03 |
| ARB-G1 | Contenu minimal `reproducibility_fingerprints` | Dépend du pipeline d'instanciation aval. | Création du pipeline d'instanciation |

---

## Points hors périmètre

| # | Élément | Justification |
|---|---|---|
| — | Contenu domaine spécifique (graphe de connaissances, MSC, contenus d'apprentissage) | Explicitement hors périmètre `platform_factory` par `out_of_scope` dans l'architecture. |
| — | Logique de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Domaine-spécifique, hors périmètre factory. |
| — | Pipeline d'instanciation d'une application spécifique | Explicitement hors périmètre. Les responsabilités factory s'arrêtent au contrat minimal et au handoff (non encore formalisé). |
| — | Révision du socle canonique (Constitution, Référentiel, LINK) | Hors périmètre. La factory ne peut que référencer et opérationnaliser, jamais redéfinir. |
| — | Choix de stack technique de l'application produite | Hors périmètre factory. Gouverné par le pipeline d'instanciation aval. |

---

## Points sans consensus ou nécessitant discussion finale

| # | Point | Nature de l'ambiguïté | Proposition d'arbitrage | Consensus perçu |
|---|---|---|---|---|
| NC-01 | Mode déclaratif vs probatoire pour `runtime_constitutional_compliance` | 6 rapports posent le problème mais ne convergent pas sur le mode de résolution acceptable pour V0.1. Certains suggèrent un axe "déclaratif asserté par le manifest", d'autres un axe "validé mécaniquement". | Proposé : déclaratif obligatoire en V0.1, probatoire en V1. L'humain valide cette temporisation. | `medium` — à confirmer en consolidation |
| NC-02 | Niveau de formalisme minimal acceptable pour le protocole d'assemblage multi-IA | Certains rapports (GPT54, PERP_K7X2) accepteraient un protocole très court en V0.1, d'autres (PERPLX_A1J77P) jugent que toute lacune sur ce sujet est une non-conformité de premier rang. | Proposé : bloc `multi_ia_decomposition_minimum_protocol` minimal ajouté dans architecture, protocole complet différé. | `medium` — à confirmer |
| NC-03 | Traitement de la baseline V0 hors manifest : régularisation immédiate vs différée | PPLXAI classe ce point "critique", PERP_K7X2 "basse-moyenne". Désaccord sur l'urgence. | Proposé : ARB-D1 (documentation régime transitoire dans ce cycle) + ARB-D2 (intégration manifest différée à STAGE_07). | `medium` |

---

## Corrections à arbitrer avant patch

### PATCH-01 — Ajouter axe `runtime_constitutional_compliance` dans `minimum_validation_contract` (architecture)

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Invariants constitutionnels runtime absents des axes de validation minimaux |
| **Statut proposé** | `retained` |
| **Gravité** | critique |
| **Justification** | Convergence 6/6. Brèche normative non acceptable en V0. |
| **Dépendance** | PATCH-02 (mode de satisfaction) |
| **Lieu probable de correction** | `architecture` |
| **Consensus** | `strong` |

### PATCH-02 — Préciser le mode de satisfaction de l'axe PATCH-01 en V0 (déclaratif)

| Champ | Valeur |
|---|---|
| **Élément concerné** | `contracts.produced_application_minimum_contract.minimum_validation_contract` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Sans mode de satisfaction explicite, l'axe ajouté reste virtuel |
| **Statut proposé** | `retained` |
| **Gravité** | élevé |
| **Justification** | Nécessaire pour l'exploitabilité de PATCH-01 en V0.1 |
| **Dépendance** | PATCH-01 |
| **Lieu probable de correction** | `architecture` |
| **Consensus** | `strong` |

### PATCH-03 — Décider et formaliser l'emplacement des projections dérivées

| Champ | Valeur |
|---|---|
| **Élément concerné** | `generated_projection_rules.emplacement_policy` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | `TBD` bloquant toute opérationnalisation |
| **Statut proposé** | `retained` |
| **Gravité** | élevé |
| **Justification** | Convergence 6/6. Prérequis à tout usage opérationnel des projections |
| **Lieu probable de correction** | `architecture` + `state` |
| **Consensus** | `strong` |

### PATCH-04 — Ajouter règle de validation et d'invalidation déclaratives des projections

| Champ | Valeur |
|---|---|
| **Élément concerné** | `generated_projection_rules`, `execution_projection_contract` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Absence de critères de validation avant usage et d'invalidation post-patch canonique |
| **Statut proposé** | `retained` (règles déclaratives) |
| **Gravité** | élevé |
| **Justification** | Nécessaire pour rendre l'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` opposable |
| **Dépendance** | PATCH-03 |
| **Lieu probable de correction** | `architecture` |
| **Consensus** | `strong` |

### PATCH-05 — Ajouter un bloc `multi_ia_decomposition_minimum_protocol` dans architecture

| Champ | Valeur |
|---|---|
| **Élément concerné** | `multi_ia_parallel_readiness` |
| **Localisation** | `platform_factory_architecture.yaml` |
| **Problème** | Protocole d'assemblage absent pour une exigence déclarée first-rank |
| **Statut proposé** | `retained` (protocole minimal) |
| **Gravité** | élevé |
| **Justification** | Convergence 6/6. Incohérence interne entre déclaration et capacité réelle |
| **Lieu probable de correction** | `architecture` + `pipeline` |
| **Consensus** | `strong` |

### PATCH-06 — Promouvoir `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker dans state

| Champ | Valeur |
|---|---|
| **Élément concerné** | `blockers` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Gap non classé blocker pour une exigence de premier rang |
| **Statut proposé** | `retained` |
| **Gravité** | modéré |
| **Lieu probable de correction** | `state` |
| **Consensus** | `strong` |

### PATCH-07 — Documenter le régime transitoire de gouvernance baseline V0 dans le state

| Champ | Valeur |
|---|---|
| **Élément concerné** | metadata + notes |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Ambiguïté sur le statut officiel de la baseline V0 |
| **Statut proposé** | `retained` |
| **Gravité** | modéré |
| **Lieu probable de correction** | `state` |
| **Consensus** | `strong` |

### PATCH-08 — Reclasser `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` en `partial`

| Champ | Valeur |
|---|---|
| **Élément concerné** | `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` |
| **Localisation** | `platform_factory_state.yaml` |
| **Problème** | Règle déclarée ≠ capacité opérationnelle |
| **Statut proposé** | `retained` |
| **Gravité** | modéré |
| **Lieu probable de correction** | `state` |
| **Consensus** | `strong` |

### PATCH-09 — Ajouter règle d'atomicité minimale dans STAGE_05 du pipeline

| Champ | Valeur |
|---|---|
| **Élément concerné** | `STAGE_05_FACTORY_APPLY` |
| **Localisation** | `pipeline.md` |
| **Problème** | Risque de violation de `INV_NO_PARTIAL_PATCH_STATE` |
| **Statut proposé** | `retained` |
| **Gravité** | élevé |
| **Lieu probable de correction** | `pipeline` |
| **Consensus** | `medium` |

### PATCH-10 — Clarifier la distinction STAGE_04 vs STAGE_06 dans pipeline.md

| Champ | Valeur |
|---|---|
| **Élément concerné** | Descriptions STAGE_04 et STAGE_06 |
| **Localisation** | `pipeline.md` |
| **Problème** | Même prompt, objet non différencié documentairement |
| **Statut proposé** | `retained` |
| **Gravité** | modéré |
| **Lieu probable de correction** | `pipeline` |
| **Consensus** | `medium` |

---

*Rapport produit par PERPLX dans le cadre du STAGE_02_FACTORY_ARBITRAGE_MULTI.*  
*Statut : proposition d'arbitrage indépendante — non canonique — à consolider humain-assisté.*
