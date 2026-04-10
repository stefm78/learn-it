# STAGE_01_CHALLENGE — Rapport de challenge Platform Factory

**challenge_run_id :** `PFCHAL_20260410_PERPLX_K7R2`  
**Date :** 2026-04-10  
**IA :** PERPLX (Perplexity)  
**Artefacts challengés :**
- `docs/cores/current/platform_factory_architecture.yaml` (PLATFORM_FACTORY_ARCHITECTURE_V0_4)
- `docs/cores/current/platform_factory_state.yaml` (PLATFORM_FACTORY_STATE_V0_4)

**Socle canonique de référence :**
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

**Pipeline référence :** `docs/pipelines/platform_factory/pipeline.md`

---

## Résumé exécutif

La Platform Factory V0.4 pose une fondation architecturale et constatative solide, bien séparée du socle canonique, avec une doctrine multi-IA et une chaîne de transformation lisibles. Le cadre de gouvernance release est explicitement reconnu comme incomplet, ce qui est légitime en V0.

Cependant, plusieurs risques structurels **non triviaux** subsistent, indépendamment des lacunes V0 assumées :

1. **Le contrat minimal d'application ne suffit pas à prouver la conformité constitutionnelle** des invariants clés (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`) : les bindings existent mais restent non-déterministes tant que les validateurs sont absents.
2. **Les `validated_derived_execution_projections` portent un statut `validated` non auditable** en l'état, avec un risque documenté mais non borné de dérive normative silencieuse.
3. **Le multi-IA parallèle est déclaré exigence structurante mais son protocole d'assemblage est totalement absent** — c'est un bloqueur opérationnel reconnu, mais son impact sur la gouvernance de release n'est pas suffisamment contraint.
4. **Le `bootstrap_contract`** du runtime entrypoint est `TBD` obligatoire : aucune application ne peut passer la validation complète du contrat minimal en l'état.
5. **La `constitutional_conformance_matrix`** est absente (`PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`) alors que plusieurs champs d'observabilité et de validation la référencent comme obligatoire.

Ces cinq points constituent les risques à arbitrer avant tout cycle de patch.

---

## Carte de compatibilité constitutionnelle

| Invariant constitutionnel | Élément factory concerné | Binding | Risque |
|---|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | `runtime_policy_conformance` axis + `no_network_dependency_at_runtime` | Explicite dans le contrat minimal mais **non auditable** (validator absent) | Une application produite pourrait déclarer PASS sans vérification réelle |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | `no_runtime_content_generation` item + observabilité `constitutional_invariants_checked` | Explicite mais **conditionné à `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`** absent | Signal non émissible de façon probante |
| Séparation Constitution / Référentiel | `PF_INV_FACTORY_DOES_NOT_DUPLICATE_NORM` + `dependencies_to_constitution/referentiel/link` | Explicite, solide structurellement | Risque faible tant que la factory ne génère pas de logique métier — à surveiller lors des projections |
| Validation locale déterministe des patchs | `STAGE_04_FACTORY_PATCH_VALIDATION` avec script Python obligatoire | Explicite dans le pipeline | Solide en intention, mais le script `validate_platform_factory_patchset.py` **n'est pas matérialisé** (`PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` absent) |
| Artefacts patch précomputés hors session | Architecture et pipeline cohérents | Implicitement protégé | Pas de risque direct identifié |
| Traçabilité explicite des dépendances canoniques | `reproducibility_fingerprints` dans le contrat minimal | Explicite | Fragile : le schéma fin n'est pas finalisé — fingerprint déclaré en intention seulement |
| Absence d'état partiel interdit lors d'une transformation | Sandbox `work/05_apply/`, séparation apply/promote | Explicite dans les règles pipeline | Solide structurellement |

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

**Point solide :** La factory reprend explicitement `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` dans le `minimum_validation_contract` et le signal `constitutional_invariants_checked`. La séparation Constitution / Référentiel / factory est structurellement propre.

**Faiblesse principale :** Le signal `constitutional_invariants_checked` ne peut être émis de façon auditable que si `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` est présent — ce qui est reconnu absent. La note dans `minimum_observability_contract` le documente, mais elle ne borne pas la conséquence : en V0, **aucune application produite ne peut prouver sa conformité constitutionnelle de façon déterministe**. Ce n'est pas un défaut de design mais un trou de validation probatoire qui doit être arbitré comme bloqueur de promotion à `current/` officielle.

**Brèche potentielle :** L'item `declared_autonomy_regime_respected` dans `runtime_policy_conformance` n'est pas relié à un invariant constitutionnel explicite. Il pourrait masquer une dérive si le "régime d'autonomie déclaré" dans le manifest d'une application produite n'est jamais confronté à un invariant source.

---

### Axe 2 — Cohérence interne de la factory

**Point solide :** La séparation `platform_factory_architecture.yaml` (prescriptif) / `platform_factory_state.yaml` (constatif) est bien tenue. Les deux artefacts ne se contredisent pas sur les périmètres.

**Tension identifiée :** Le `platform_factory_state.yaml` classe `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` comme **partielle**, ce qui est juste. Mais la description de cette capacité liste des éléments encore absents (validator dédié, protocole de régénération automatisé) tout en affirmant que "la règle d'usage est définie". Cette formulation peut laisser croire que la règle est opérationnelle alors qu'elle est seulement documentée. Risque de **maturité surdéclarée sur cet axe spécifique**.

**Incohérence de wording :** Dans `platform_factory_state.yaml`, `capabilities_partial` pour `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` dit "le pipeline est gouverné et exécutable manuellement mais non automatisé". Or `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` est classé **absent**. Le script `validate_platform_factory_patchset.py` n'existe pas encore, donc STAGE_04 ne peut pas s'exécuter. La formulation "exécutable manuellement" est **partiellement inexacte** pour les stages à script obligatoire.

---

### Axe 3 — Portée et frontières

**Point solide :** La factory ne gouverne pas le contenu domaine spécifique, n'absorbe pas de logique métier Learn-it, reste explicitement séparée du pipeline d'instanciation aval.

**Zone de risque :** La frontière entre `PF_LAYER_DERIVED_EXECUTION_PROJECTIONS` et `PF_LAYER_APPLICATION_INSTANTIATION` n'est pas suffisamment précisée pour les projections à portée mixte. Une IA pourrait produire une projection ciblant "runtime + offsession" sans que la factory impose une déclaration de frontière explicite entre ce qui relève de la factory et ce qui relève du pipeline d'instanciation. Le champ `usage_policy` est obligatoire par projection mais son contenu attendu reste flou.

**Angle mort :** La factory ne se prononce pas sur ce qui se passe si une projection dérivée est utilisée **à la fois** comme contexte IA pour la factory et comme input d'instanciation domaine. Le scope `usage_as_sole_context` est bloqué en V0, mais une utilisation partielle non bornée reste possible sans détection.

---

### Axe 4 — Contrat minimal d'une application produite

**Obligations présentes et solides :**
- Identity, manifest, canonical_dependency_contract, minimum_validation_axes, minimum_observability — tous présents à haut niveau.
- `reproducibility_fingerprints` défini conceptuellement.

**Obligations trop floues ou non auditables :**

- **`bootstrap_contract` : TBD obligatoire.** Aucune application ne peut passer la validation complète du `runtime_entrypoint_contract`. Bloqueur `high` correctement reconnu (`PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED`), mais son impact cascade sur les axes `structure_and_state_alignment` et `runtime_policy_conformance` n'est pas formalisé.

- **`reproducibility_fingerprints` :** défini comme "hash ou identifiant de version stable". Cette définition est intentionnelle mais pas assez contrainte : elle ne précise pas si un hash de fichier, un tag Git, ou une autre forme est attendu. Deux IA pourraient produire des fingerprints de format incompatible.

- **`declared_autonomy_regime_respected` :** obligation dans `runtime_policy_conformance` sans référence à un invariant constitutionnel source. Cette obligation est **non auditable constitutionnellement** en l'état.

- **Absence d'obligation explicite sur le format de rapport de validation.** Les axes minimaux sont listés mais la structure du rapport de sortie n'est pas définie. Deux IA produiraient deux rapports non comparables.

---

### Axe 5 — Validated derived execution projections

**Risques identifiés :**

1. **Dérive de paraphrase :** Le champ `no_normative_divergence` est un invariant de projection, mais sans validator dédié, une IA peut paraphraser une règle constitutionnelle sans détecter la divergence.

2. **Omission dans un scope déclaré :** Le `conformance_matrix_ref` pointe vers un fichier absent (`constitutional_conformance_matrix.yaml`). Une projection déclarant couvrir un scope donné ne peut pas être vérifiée contre la matrice de conformité. C'est le **risque le plus direct et concret** de toute la factory en V0.

3. **Régénération non déterministe :** L'invariant `deterministic_regeneration_required` est posé mais le "protocole de régénération déterministe" est listé comme absent dans `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`. Toute régénération en V0 est donc **non déterministe de fait**.

4. **Promotion implicite silencieuse :** `promotion_to_canonical_forbidden: true` est déclaré dans les champs obligatoires de projection, mais il n'existe pas de garde-fou automatique empêchant qu'une IA utilise une projection comme source primaire si elle lui est fournie sans contexte suffisant.

5. **Cycle de déblocage sans point d'entrée clair :** `usage_as_sole_context: blocked` est conditionné à `validator_dédié_implementé`, lui-même bloqué par l'absence de la `constitutional_conformance_matrix`.

---

### Axe 6 — État reconnu, maturité et preuves

**Cohérence globale** `capabilities_present` / `capabilities_partial` / `capabilities_absent` : correcte et honnête sur la majorité des points.

**Zones de sur-déclaration partielle :**
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` classée **partielle** avec "exécutable manuellement" : trop optimiste pour les stages avec script obligatoire (voir Axe 2).
- `PF_CAPABILITY_MINIMUM_VALIDATION_MODEL` classée **partielle** : les axes sont posés mais les "reports exacts" sont absents. La formulation ne signale pas que les rapports ne sont actuellement pas comparables entre deux exécutions parallèles.

**Preuves (`evidence`) :** deux entrées seulement — normal en V0 mais à enrichir dès le premier cycle formel.

**`validated_decisions` :** cohérentes et bien ancrées dans l'architecture.

---

### Axe 7 — Multi-IA en parallèle

**`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` est correctement classé bloqueur opérationnel.**

**Risques non explicitement bornés dans l'architecture :**

- **Granularité des scopes de projection :** aucune règle ne dit qu'une projection ne doit pas couvrir simultanément plusieurs STAGES du pipeline.
- **Points d'assemblage :** les `clear_assembly_points` sont listés comme exigence mais aucun point d'assemblage concret n'est défini dans l'architecture.
- **Reports non homogènes :** l'architecture pose `homogeneous_reports` comme exigence mais la structure des reports n'est pas définie.

---

### Axe 8 — Gouvernance release, manifest et traçabilité

**Point solide :** La séparation release / promotion est explicite dans la Rule 6 du pipeline. Le blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` est correctement documenté avec une exit condition précise (STAGE_08).

**Risque principal :** La release `PLATFORM_FACTORY_RELEASE_2026_04_10_R01` est mentionnée dans le state, mais si son manifest de release n'est pas accessible ou vérifiable indépendamment des artefacts `current/`, la traçabilité de la baseline repose uniquement sur ces artefacts — ce qui est **circulaire**.

**Angle mort :** La factory ne définit pas comment un changement de version de `constitution.yaml` ou `referentiel.yaml` invalide les projections dérivées existantes. Le `version_fingerprint` est obligatoire par projection mais le mécanisme de comparaison (comparé à quoi, par qui, quand) est absent.

---

### Axe 9 — Implémentabilité pipeline

**Points solides :** Stage map lisible, inputs/outputs de chaque stage déclarés, zones d'écriture bornées. STAGE_07 et STAGE_08 ont leurs specs détaillées présentes dans le repo.

**Gaps critiques :**

1. **STAGE_04 : script `validate_platform_factory_patchset.py` absent.** Ce script est déclaré "obligatoire, à exécuter en premier". STAGE_04 est non exécutable dans sa forme canonique.

2. **Output `work/01_challenge/challenge_report_##.md` :** le `##` dans `pipeline.md` suggère un numéro de run, mais le launch prompt `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md` définit une convention `challenge_run_id` avec format `PFCHAL_YYYYMMDD_AGENTTAG_RAND`. La convention dans `pipeline.md` est donc **obsolète par rapport au launch prompt** — incohérence mineure à corriger.

3. **Companion prompts** (`Make21`, `Make22`, `Make23`) : référencés dans le pipeline, leur existence dans `docs/prompts/shared/` n'est pas vérifiée dans ce challenge.

---

### Axe 10 — Scénarios adversariaux

**Scénario 1 — Dérive silencieuse d'une projection dérivée**

Une IA génère une projection pour STAGE_03 couvrant les règles de patch du Référentiel. Elle paraphrase `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` en omettant la condition "trois régimes actifs ou plus → investigation systémique". La projection est taguée `validation_status: validated` (tag non bloqué formellement en V0). Une IA travaillant sur cette projection produit un patchset qui ne déclenche jamais d'investigation systémique là où la Constitution l'exige. La non-conformité est indétectable jusqu'à exécution runtime.

- Mécanismes activés : `validated_derived_execution_projection` + `minimum_validation_contract`
- Faiblesse révélée : absence de `constitutional_conformance_matrix` + validator absent
- Localisation : architecture (contrat projection) + state (validator absent) + pipeline (STAGE_04 non exécutable)

**Scénario 2 — Application produite paraissant valide mais violant `INV_RUNTIME_FULLY_LOCAL`**

Une application produite déclare `no_network_dependency_at_runtime: checked`. L'axe `runtime_policy_conformance` passe PASS. Mais le validateur étant absent, la vérification est faite par inspection manuelle d'une IA. L'IA rate un import indirect vers une API tierce dans un module de configuration. L'application est promue comme conforme. Elle appelle le réseau au runtime.

- Mécanismes activés : `runtime_policy_conformance` + `constitutional_invariants_checked`
- Faiblesse révélée : validation non déterministe + signal `constitutional_invariants_checked` non probant
- Localisation : contrat minimal application + validator/tooling

**Scénario 3 — Collision multi-IA sur STAGE_01 + STAGE_03**

Deux IA travaillent en parallèle : IA-A sur STAGE_01 (challenge), IA-B sur STAGE_03 (patch synthesis) d'un cycle précédent non encore fermé. IA-B produit un patchset qui corrige un blocker que IA-A vient précisément d'identifier comme nécessitant une décision humaine préalable. Les deux outputs atterrissent dans le repo sans mécanisme de détection de conflit. L'humain valide par erreur le patchset de IA-B qui n'intègre pas les conclusions du challenge de IA-A.

- Mécanismes activés : `multi_ia_parallel_readiness` + `clear_assembly_points`
- Faiblesse révélée : absence de protocole d'assemblage + absence de convention de nommage de run dans `pipeline.md`
- Localisation : pipeline + multi-IA readiness

**Scénario 4 — Promotion implicite d'artefacts current non manifest-intégrés**

Suite à un STAGE_05 appliqué correctement en sandbox, un opérateur humain copie manuellement les fichiers patchés directement dans `docs/cores/current/` sans passer par STAGE_08 (promotion formelle) ni STAGE_07 (release materialization). Les artefacts `current/` sont mis à jour, mais aucune release n'est matérialisée, aucun manifest de release n'est créé, et le `platform_factory_state.yaml` n'est pas mis à jour. Le repo contient une baseline non traçable.

- Mécanismes activés : pipeline Rule 6 + `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- Faiblesse révélée : absence de garde-fou technique empêchant la modification directe de `current/`
- Localisation : pipeline + manifest/release governance

---

## Risques prioritaires

| Priorité | Risque | Localisation |
|---|---|---|
| **Critique** | `constitutional_conformance_matrix.yaml` absent — conformité non auditable pour toute projection et tout signal `constitutional_invariants_checked` | Architecture + state + validator/tooling |
| **Critique** | `bootstrap_contract` TBD — aucune application ne peut passer la validation complète du contrat minimal | Architecture |
| **Critique** | Validator dédié absent — `validation_status: validated` sur toute projection est non déterministe | State + validator/tooling |
| **Élevé** | Script `validate_platform_factory_patchset.py` absent — STAGE_04 non exécutable dans sa forme canonique | Pipeline |
| **Élevé** | Absence de protocole d'assemblage multi-IA — bloqueur opérationnel non borné dans l'architecture | Architecture + pipeline |
| **Élevé** | `version_fingerprint` sans mécanisme de détection de dérive canonique — projections non invalidées automatiquement lors d'un update canonique | Architecture (contrat projection) |
| **Modéré** | `declared_autonomy_regime_respected` sans référence invariant constitutionnel source | Contrat minimal application |
| **Modéré** | Incohérence convention nommage challenge report entre `pipeline.md` (`##`) et launch prompt (`PFCHAL_...`) | Pipeline |
| **Modéré** | Formulation "exécutable manuellement" inexacte pour les stages avec script obligatoire | State |
| **Faible** | Preuves (`evidence`) limitées à deux entrées | State |

---

## Points V0 acceptables

- Schémas fins du manifest, de la configuration, du packaging, du runtime entrypoint non finalisés : incomplétude normale, reconnue, sans risque immédiat.
- `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` : correctement signalé comme bloqueur opérationnel. Pas de travail multi-IA réel sans ce protocole, donc pas de dérive silencieuse tant qu'on opère en séquentiel.
- Absence de `docs/cores/platform_factory/projections/` physiquement : décision prise, emplacement défini, opérationnalisation à faire — acceptable.
- Evidence limitée à deux entrées : normal pour un premier cycle.
- Pipeline V0 non automatisé : acceptable. L'intention et la structure gouvernée suffisent pour ce cycle.
- STAGE_07 et STAGE_08 : leurs specs détaillées sont présentes dans le repo — risque levé.

---

## Corrections à arbitrer avant patch

### C1 — Matérialiser `constitutional_conformance_matrix.yaml`

- **Élément concerné :** `constitutional_conformance_matrix_ref` dans l'architecture + signal `constitutional_invariants_checked`
- **Localisation :** `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
- **Nature :** Artefact référencé obligatoire, absent
- **Type :** Complétude + compatibilité constitutionnelle + implémentabilité
- **Gravité :** Critique
- **Impact factory :** Toute projection dérivée est non auditable. Tout signal d'observabilité `constitutional_invariants_checked` est non probant.
- **Impact application produite :** Aucune application ne peut prouver sa conformité constitutionnelle de façon déterministe.
- **Impact IA :** Les IA ne peuvent pas vérifier la complétude d'une projection dans son scope déclaré.
- **Impact gouvernance/release :** `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` bloque la condition de déblocage de `usage_as_sole_context`.
- **Correction :** Créer le fichier avec au minimum les invariants constitutionnels touchés par la factory et leur statut de couverture.
- **Lieu :** `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` — pipeline dédié ou STAGE_02/03 du prochain cycle

---

### C2 — Définir le `bootstrap_contract` ou borner explicitement son absence

- **Élément concerné :** `runtime_entrypoint_contract.bootstrap_contract` dans l'architecture
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.runtime_entrypoint_contract`
- **Nature :** Champ obligatoire déclaré TBD
- **Type :** Complétude + implémentabilité
- **Gravité :** Critique
- **Impact application produite :** Aucune application ne peut passer la validation complète du contrat minimal.
- **Impact IA :** Une IA ne peut pas vérifier la conformité d'un runtime entrypoint sans ce contrat.
- **Correction :** Soit définir une première version du `bootstrap_contract` (même minimale), soit arbitrer que les axes de validation dépendants sont en état `DEFERRED_UNTIL_BOOTSTRAP_DEFINED` et l'inscrire explicitement dans le contrat minimal.
- **Lieu :** Architecture

---

### C3 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément concerné :** `capabilities_partial` → `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Localisation :** `platform_factory_state.yaml`
- **Nature :** Maturité surdéclarée — "exécutable manuellement" inexact pour les stages à script obligatoire
- **Type :** Faux niveau de maturité
- **Gravité :** Modéré
- **Impact gouvernance :** Un opérateur lisant le state croit pouvoir exécuter STAGE_04 manuellement alors que le script est absent.
- **Correction :** Préciser "exécutable manuellement pour les stages sans script obligatoire ; STAGE_04 bloqué par absence de `validate_platform_factory_patchset.py`".
- **Lieu :** State

---

### C4 — Borner le mécanisme de détection de dérive canonique pour les projections

- **Élément concerné :** `version_fingerprint` dans les champs obligatoires de projection
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.execution_projection_contract.mandatory_fields_per_projection`
- **Nature :** Champ défini sans mécanisme de comparaison
- **Type :** Gouvernance + exploitabilité IA
- **Gravité :** Élevé
- **Impact projections :** Une mise à jour de `constitution.yaml` n'invalide pas automatiquement les projections existantes.
- **Correction :** Ajouter dans l'architecture une règle décrivant le mécanisme de comparaison attendu et la responsabilité de cette vérification.
- **Lieu :** Architecture + pipeline (STAGE_01 ou STAGE_04)

---

### C5 — Relier `declared_autonomy_regime_respected` à un invariant constitutionnel source

- **Élément concerné :** `declared_autonomy_regime_respected` dans `runtime_policy_conformance`
- **Localisation :** `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract.runtime_policy_conformance_definition`
- **Nature :** Obligation sans invariant source constitutionnel
- **Type :** Compatibilité constitutionnelle + gouvernance
- **Gravité :** Modéré
- **Impact application produite :** L'obligation est non auditable constitutionnellement.
- **Correction :** Ajouter un `invariant_ref` explicite vers la Constitution pour cet item, ou supprimer l'item si aucun invariant ne le couvre directement.
- **Lieu :** Architecture

---

### C6 — Corriger l'incohérence de convention de nommage des challenge reports

- **Élément concerné :** Convention nommage `work/01_challenge/challenge_report_##.md` dans `pipeline.md`
- **Localisation :** `docs/pipelines/platform_factory/pipeline.md` → STAGE_01_CHALLENGE outputs
- **Nature :** Incohérence entre `pipeline.md` (format `##`) et `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md` (format `PFCHAL_YYYYMMDD_AGENTTAG_RAND`)
- **Type :** Gouvernance + exploitabilité IA
- **Gravité :** Modéré
- **Impact IA :** Risque de collision ou d'ambiguïté si le pipeline.md est lu sans le launch prompt.
- **Correction :** Aligner `pipeline.md` sur la convention `challenge_run_id` définie dans le launch prompt.
- **Lieu :** Pipeline

---

*Fin du rapport — `PFCHAL_20260410_PERPLX_K7R2`*
