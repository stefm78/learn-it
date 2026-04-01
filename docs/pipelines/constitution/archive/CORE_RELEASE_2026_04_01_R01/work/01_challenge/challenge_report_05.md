# CHALLENGE REPORT — Constitution V1_8
## Métadonnées

- pipeline: constitution
- stage: STAGE_01_CHALLENGE
- core_audité: CORE_LEARNIT_CONSTITUTION_V1_8
- date: 2026-03-31
- statut: PRODUIT

---

## Résumé exécutif

La Constitution `CORE_LEARNIT_CONSTITUTION_V1_8` est architecturalement solide et couvre bien les axes pédagogiques fondamentaux. Cependant, cinq zones de fragilité significatives ont été identifiées :

1. Une dépendance inter-Core asymétrique sur les seuils sans contrat explicite
2. Plusieurs états moteur potentiellement indéfinis sur des combinaisons d'axes `unknown`
3. Une logique de composante `T` dont la séparation n'est pas opérationnellement outillée
4. Des règles de gouvernance patch dont le déterminisme reste partiel
5. Une absence de couverture explicite du cas KU créative + mode non-autonome

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### Binding Constitution → Référentiel non contractualisé

Les composantes `TYPE_MASTERY_COMPONENT_P`, `R`, `A` déclarent toutes `depends_on: REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` avec la condition *"Seuils fournis par le Référentiel"*, mais la Constitution ne formalise nulle part un **contrat d'interface** listant exactement quels paramètres sont attendus du Référentiel (seuils P, multiplicateurs R, seuil_R d'interruption, seuil VC, fenêtre AR-réfractaire).

Le type `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` est `patchable: false` et `parameterizable: false`, ce qui empêche toute mise à jour de l'interface même si le Référentiel évolue.

**Risque** : drift silencieux entre versions des deux Cores.

#### Cycle potentiel implicite sur TYPE_MASTERY_COMPONENT_T

`TYPE_MASTERY_COMPONENT_T` déclare `derives_from: TYPE_MASTERY_MODEL`, et `TYPE_MASTERY_MODEL` dépend des composantes P, R, A, T. La relation `derives_from` n'est pas une `depends_on`, mais un lecteur moteur naïf pourrait interpréter cette bidirectionnalité comme un cycle.

L'invariant `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` s'applique au graphe des KU, pas aux Types internes — une clarification explicite est manquante.

#### `patchable: false` généralisé sur les Types constitutionnels

Presque tous les `TYPES` sont `patchable: false`. C'est cohérent avec la philosophie constitutionnelle, mais `TYPE_FEEDBACK_COVERAGE_MATRIX` et `TYPE_AUTHENTIC_CONTEXT` sont `patchable: true` sans qu'une règle gouverne **qui** peut les patcher et sous quelles conditions de pipeline. Ce traitement asymétrique crée une zone grise de gouvernance.

---

### Axe 2 — Solidité théorique

#### Composante A (autonomie) sous-spécifiée

`TYPE_MASTERY_COMPONENT_A` est définie comme *"transitions sans aide observées"*, mais la Constitution ne précise pas ce qui constitue une aide observable vs. un scaffolding réversible (`ACTION_APPLY_LIGHT_REVERSIBLE_SCAFFOLDING`).

Un scaffolding léger déclenché par `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` invalide-t-il la composante A ? Ce cas n'est pas couvert — risque de dégradation non intentionnelle du MSC lors de sessions conservatrices.

#### SRL et forethought partiellement couverts

`RULE_SESSION_INTENTION_NON_BLOCKING` couvre bien le forethought de clôture via AR-N2, mais la phase de **planification amont** (goal-setting, intention pré-session) est absente de la Constitution.

Le SRL Zimmerman distingue forethought, performance, et self-reflection — seule la self-reflection (AR-N3) et la performance monitoring (AR-N1, SIS) sont couvertes.

#### Mastery Learning et nombre d'essais

La Constitution ne pose aucune contrainte sur le **nombre maximum de tentatives** avant une rétrogradation ou une escalade. Le modèle mastery learning classique (Bloom, 1968) implique des cycles correctifs bornés.

En l'absence de borne, un apprenant peut boucler indéfiniment sur une KU sans déclenchement de `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`.

---

### Axe 3 — États indéfinis moteur

#### Combinaison d'axes `unknown` non résolue

`RULE_LEARNER_STATE_MODEL` autorise un axe à rester `unknown`. Mais aucune règle ne couvre le cas où **les trois axes** (Calibration, Activation, Value-Cost) sont simultanément `unknown/absent`.

La règle `RULE_NO_CALIBRATION_CONSERVATIVE_START` couvre l'initialisation sans calibration mais pas les sessions ultérieures avec un état total inconnu.

#### Composante T sans événement déclencheur clair

`TYPE_MASTERY_COMPONENT_T` est évaluée lors d'une *"évaluation de transfert"* mais il n'existe aucun `EVENT` ni `RULE` qui déclenche explicitement cette évaluation.

Le moteur peut ne jamais évaluer T sans signal externe, laissant des apprenants éternellement en *"maîtrise de base"* sans qualification supérieure.

#### Conflit GF-08 avec état apprenant dégradé

`EVENT_GF08_UNCOVERED_CONFLICT` déclenche une réponse conservatrice + log. Mais si ce conflit survient simultanément à un `EVENT_MSC_DOWNGRADE`, quelle règle prime ?

La Constitution ne définit aucune hiérarchie de priorité entre événements concurrents.

---

### Axe 4 — Dépendances IA implicites

#### `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` requiert de la détection sémantique

La règle est déclenchée sur *"KU flaggée misconception"*, ce qui suppose qu'un mécanisme détecte et flag les misconceptions.

En mode `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`, cette détection ne peut être que pré-calculée en design. Ce point n'est pas explicité dans la Constitution — risque d'inférence sémantique implicite en runtime.

#### Scoring de `TYPE_CORPUS_CONFIDENCE_ICC` non défini

L'ICC *"qualifie la confiance d'analyse"* lors de la construction du graphe, mais aucun critère déterministe de calcul n'est fourni.

Un calcul sémantique hors-session est implicitement requis — il manque un ancrage dans la chaîne de validation.

---

### Axe 5 — Gouvernance

#### Version de release figée dans l'ID du Core

L'ID `CORE_LEARNIT_CONSTITUTION_V1_8` encode la version. Si un patch incrémental produit une V1.9, l'ID du Core change — mais `patchable: false` sur `SYSTEM_LEARNIT` et sur `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` signifie que la référence vers le Référentiel devra être mise à jour manuellement à chaque release.

Ce couplage fort ID/version fragilise la patchabilité automatique.

#### `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` et `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` partiellement redondants

Les deux invariants couvrent des angles différents (préparation hors-session vs. déterminisme) mais se recoupent sans que leur relation soit explicitement posée.

En cas de conflit d'interprétation lors d'une validation, lequel prime ?

---

## Risques prioritaires

| Priorité | ID | Axe | Description |
|---|---|---|---|
| **Critique** | R-01 | Axe 1 | Absence de contrat d'interface Constitution→Référentiel sur les seuils des composantes P, R, A |
| **Critique** | R-02 | Axe 3 | Combinaison triple-unknown de l'état apprenant sans règle de fallback post-initialisation |
| **Élevé** | R-03 | Axe 3 | Absence d'événement déclencheur pour l'évaluation de la composante T |
| **Élevé** | R-04 | Axe 2 | Scaffolding léger (INV_CONSERVATIVE) potentiellement invalidant pour la composante A |
| **Élevé** | R-05 | Axe 5 | Couplage fort ID/version rendant les mises à jour de références inter-Core manuelles |
| **Modéré** | R-06 | Axe 1 | Ambiguïté du cycle implicite derives_from sur TYPE_MASTERY_COMPONENT_T |
| **Modéré** | R-07 | Axe 4 | Détection des misconceptions en runtime implicitement sémantique |
| **Modéré** | R-08 | Axe 2 | Absence de borne sur les cycles correctifs (mastery learning sans cap) |
| **Modéré** | R-09 | Axe 3 | Priorité non définie entre événements moteur concurrents (GF-08 + MSC downgrade) |
| **Faible** | R-10 | Axe 5 | Redondance partielle entre INV_PATCH_ARTIFACTS et INV_PATCH_LOCAL_VALIDATION |

---

## Corrections à arbitrer avant patch

1. **R-01** — Faut-il introduire un `TYPE_INTERCORE_CONTRACT` dans la Constitution listant les paramètres attendus du Référentiel, ou ce contrat relève-t-il du Référentiel uniquement ?
2. **R-02** — Quelle est la politique moteur en cas d'état apprenant totalement inconnu après la session initiale ? Réinitialisation conservatrice ? Escalade humaine ?
3. **R-03** — L'évaluation de T doit-elle être déclenchée par un `EVENT_MASTERY_BASE_REACHED` dédié, ou est-ce intentionnellement laissé à la discrétion du design ?
4. **R-04** — Un scaffolding déclenché par conservation (sans AR-N1) doit-il être exclu du compteur "aides observées" pour préserver la composante A ?
5. **R-05** — La référence `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` doit-elle devenir `patchable: true` avec une règle de mise à jour contrôlée lors des releases ?
