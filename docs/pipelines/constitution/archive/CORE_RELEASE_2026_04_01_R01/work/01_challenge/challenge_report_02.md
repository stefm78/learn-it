# Challenge Report — Constitution Learn-it V1_8

```yaml
core_challenged: CORE_LEARNIT_CONSTITUTION_V1_8
pipeline: constitution
stage: STAGE_01_CHALLENGE
date: 2026-03-31
```

---

## Résumé exécutif

La Constitution V1_8 est une architecture bien structurée, avec une séparation constitutionnel/référentiel bien tenue, des invariants non-patchables solides et une couverture des principaux scénarios d'usage. Cependant, plusieurs zones présentent des risques réels : (1) des états moteur potentiellement indéfinis liés à la coexistence d'axes *unknown* et de règles dépendantes d'états connus ; (2) des dépendances implicites vers le Référentiel trop fréquentes et peu formalisées comme contrats ; (3) une faiblesse sur la gouvernance des conflits inter-principes (GF-08) dont la résolution reste entièrement hors-Constitution.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

**[C1-A] Dépendances implicites non contractualisées vers le Référentiel**

Plusieurs types et règles déclarent `depends_on: REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` (ex. `TYPE_MASTERY_COMPONENT_P`, `TYPE_MASTERY_COMPONENT_R`, `TYPE_MASTERY_COMPONENT_A`, `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `EVENT_LONG_INTERRUPTION`). Ces dépendances ne spécifient pas le **contrat minimal attendu** du Référentiel (quels champs ? quels types ? quelles bornes ?). Si le Référentiel évolue ou est remplacé, aucune contrainte constitutionnelle n'empêche une rupture silencieuse.

**Risque :** élevé — rupture silencieuse inter-Core possible lors d'un patch Référentiel.

---

**[C1-B] `INV_CONSTITUTION_REFERENTIAL_SEPARATION` incomplète**

L'invariant déclare une séparation « quoi/pourquoi » vs « combien/comment » mais ne nomme pas les frontières précises pour chaque type de donnée (seuils, multiplicateurs, fenêtres temporelles). En pratique, `TYPE_MASTERY_COMPONENT_R` mentionne « seuils et multiplicateurs fournis ou bornés par le Référentiel » dans sa `logic.condition`, ce qui suppose une connaissance implicite de la structure du Référentiel au niveau constitutionnel.

**Risque :** modéré — ambiguïté de frontière exploitable lors d'un patch.

---

**[C1-C] `TYPE_AUTONOMY_REGIME` — `patchable: false, parameterizable: false`**

Les quatre niveaux d'autonomie sont figés sans aucune capacité d'extension paramétrée. Or l'invariant `INV_ASSISTED_MODE_REQUIRES_TUTORING` et la contrainte `CONSTRAINT_NO_ASSISTED_DEPLOYMENT_WITHOUT_TUTORING` bloquent le mode Assisté en l'absence d'infrastructure tutorale. Aucun mécanisme de fallback n'est prévu si un déploiement commence en Hybride et dérive vers Assisté. L'état de transition entre régimes n'est pas défini.

**Risque :** modéré — état interdit non géré lors d'un changement de régime en cours de déploiement.

---

### Axe 2 — Solidité théorique

**[C2-A] Composante T découplée mais sans condition de révision**

`TYPE_MASTERY_COMPONENT_T` (transférabilité) est séparée de la maîtrise de base par `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`. Mais aucune règle ne définit ce qui se passe si la maîtrise de base est **rétrogradée après** que T a été atteinte. La question de la réversibilité de T n'est pas tranchée au niveau constitutionnel.

**Risque :** élevé — oscillation potentielle du statut de T sans règle déterministe de révision.

---

**[C2-B] `TYPE_LEARNER_STATE_MODEL` — axe VC optionnel mais interprétation non bornée**

`TYPE_STATE_AXIS_VALUE_COST` est déclaré optionnel (`axe optionnel Valeur-Coût perçue`). `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise explicitement l'état *unknown*. Mais `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` présuppose une valeur observable de VC pour déclencher l'événement. La Constitution ne précise pas **comment distinguer** un VC *unknown* (source absente) d'un VC bas persistant. Le moteur peut mal qualifier l'événement `EVENT_PERSISTENT_LOW_VC`.

**Risque :** élevé — état moteur indéfini, faux positif de patch de relevance.

---

**[C2-C] AR-N3 — binding non formalisé**

`TYPE_SELF_REPORT_AR_N3` (bilan périodique AEQ) n'est lié à aucun axe d'état, aucun invariant et aucune règle constitutionnelle. Son seul effet déclaré est de produire un « indice de calibration auto-rapport ». Il n'existe aucune règle précisant **comment cet indice est intégré** dans `TYPE_STATE_AXIS_CALIBRATION`. Ce binding est soit délégué implicitement au Référentiel, soit manquant.

**Risque :** modéré — AR-N3 est un artefact orphelin au niveau constitutionnel.

---

### Axe 3 — États indéfinis moteur

**[C3-A] Coexistence `unknown` et règles conditionnelles dépendantes**

`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise un axe *unknown* mais plusieurs règles présupposent un état connu pour se déclencher (`RULE_AR_N1_OVERRIDES_PROXY`, `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`). Il n'existe pas de table d'interprétation exhaustive des combinaisons d'axes *unknown*. Le moteur peut être dans un état où plusieurs règles conservatrices s'activent simultanément sans priorité déclarée.

**Risque :** élevé — collision de réponses conservatrices sans arbitrage.

---

**[C3-B] Rétrogradation secondaire `INV_SECONDARY_RETROGRADATION_IS_NEW_EVENT` — boucle potentielle**

L'invariant crée des événements indépendants à chaque rétrogradation secondaire. Si un graphe de KU présente une chaîne longue de dépendances directes, chaque rétrogradation primaire peut générer N événements secondaires indépendants à traiter. La Constitution ne borne pas **le nombre maximum d'événements secondaires simultanés** ni leur ordre de traitement.

**Risque :** modéré — surcharge moteur possible sur graphes denses.

---

### Axe 4 — Dépendances IA implicites

**[C4-A] `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` — détection présupposée**

La règle se déclenche sur `KU flaggée misconception`, mais la Constitution ne définit pas **qui ou quoi pose le flag**. Si ce flagging nécessite une inférence sémantique (ex. comparaison d'une réponse à un pattern de misconception), le mode `INV_NO_RUNTIME_CONTENT_GENERATION` et `INV_RUNTIME_FULLY_LOCAL` imposent que cette détection soit pré-calculée hors session. Ce contrat n'est pas formalisé.

**Risque :** modéré — dépendance IA implicite pour le flagging de misconception.

---

**[C4-B] `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE` — périmètre flou**

La contrainte interdit toute inférence psychologique autonome non probatoire, mais ne définit pas le **périmètre exact** de « psychologique ». L'inférence du régime d'activation à partir de proxys comportementaux (sans AR-N1) est-elle psychologique ? La Constitution laisse ce bord ouvert.

**Risque :** faible — ambiguïté de qualification susceptible d'être exploitée dans un patch.

---

### Axe 5 — Gouvernance

**[C5-A] `EVENT_GF08_UNCOVERED_CONFLICT` — résolution entièrement déléguée hors-Constitution**

L'événement déclenche `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` qui journalise pour « futur patch ». Mais la Constitution ne définit aucune **liste des conflits GF-08 déjà couverts**, ce qui rend impossible de vérifier localement si un conflit donné est couvert ou non. La gouvernance de cet axe est lacunaire.

**Risque :** élevé — état de conflit non détectable au niveau constitutionnel.

---

**[C5-B] Versioning du Core Référentiel figé dans `source_anchor`**

La référence `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` est figée sur `V0_6`. Si le Référentiel monte en version, tous les éléments constitutionnels qui en dépendent restent ancrés sur V0_6 sans mécanisme de migration explicite. La `patchable: false` de cette référence rend la montée de version non-patchable.

**Risque :** élevé — blocage de migration inter-Core non géré.

---

### Axe 6 — Priorisation des risques

| ID | Description | Niveau |
|----|-------------|--------|
| C2-A | Réversibilité de T après rétrogradation de base | critique |
| C3-A | Collision de réponses conservatrices sur axes unknown | critique |
| C5-B | Blocage migration Référentiel V0_6 → version suivante | élevé |
| C1-A | Contrats inter-Core non formalisés | élevé |
| C2-B | VC unknown vs VC bas — indistinguables | élevé |
| C5-A | Liste des conflits GF-08 couverts absente | élevé |
| C2-C | AR-N3 orphelin sans binding constitutionnel | modéré |
| C1-B | Frontière Constitution/Référentiel implicite | modéré |
| C3-B | Boucle d'événements secondaires non bornée | modéré |
| C1-C | Transition entre régimes d'autonomie non définie | modéré |
| C4-A | Flagging misconception présuppose inférence hors session | modéré |
| C4-B | Périmètre de l'inférence psychologique flou | faible |

---

## Corrections à arbitrer avant patch

1. **[C2-A]** Définir constitutionnellement la règle de révision de T lors d'une rétrogradation MSC de base.
2. **[C3-A]** Ajouter une règle d'arbitrage explicite pour la coexistence de plusieurs réponses conservatrices simultanées.
3. **[C5-B]** Rendre `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` patchable (au moins son `version`) ou créer un mécanisme de mise à jour déclarative de la référence inter-Core.
4. **[C1-A]** Formaliser un contrat minimal constitutionnel pour chaque dépendance vers le Référentiel (champs attendus, types, bornes acceptables).
5. **[C2-B]** Ajouter une règle ou un invariant distinguant VC *unknown* (source absente) et VC bas persistant (source disponible mais valeur basse).
6. **[C5-A]** Ajouter dans la Constitution (ou dans un bloc dédié) une liste des conflits GF-08 déjà couverts par des règles explicites.
7. **[C2-C]** Formaliser le binding constitutionnel entre AR-N3 et `TYPE_STATE_AXIS_CALIBRATION` (ou déléguer explicitement au Référentiel avec contrat déclaré).
