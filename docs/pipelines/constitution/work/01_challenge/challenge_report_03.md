# CHALLENGE REPORT — constitution pipeline
# STAGE_01_CHALLENGE — Run 03

pipeline: constitution
stage: STAGE_01_CHALLENGE
run: 03
date: 2026-03-31
inputs:
  - docs/cores/current/constitution.yaml (CORE_LEARNIT_CONSTITUTION_V1_8)
  - docs/cores/current/referentiel.yaml (CORE_LEARNIT_REFERENTIEL_V0_6)
  - docs/cores/current/link.yaml (LINK_CONSTITUTION_V1_8__REFERENTIEL_V0_6)
focus_note: none

---

## Résumé exécutif

Le système est architecturalement solide dans ses grandes lignes : séparation Constitution/Référentiel/LINK correctement déclarée, invariants constitutionnels bien ancrés, gouvernance patch formalisée. Cependant, l'audit adversarial révèle **sept risques exploitables**, dont deux critiques.

Le principal point de fragilité est l'**absence de spécification du comportement moteur si le LINK est absent ou partiellement chargé** : le LINK déclare des bindings mais aucun invariant ne contractualise ce cas de défaillance. Le second critique est une **incohérence de version** entre les `id` (V1_8) et les `human_readable` (v1.7) dans les références croisées des trois Cores.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### CRITIQUE — Incohérence de version dans les références croisées

- `constitution.yaml` déclare `id: CORE_LEARNIT_CONSTITUTION_V1_8`
- `link.yaml` déclare `LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` avec `human_readable: "Référence vers le Core Constitution Learn-it v1.7"`
- `referentiel.yaml` déclare `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL` avec `human_readable: "Référence vers le Core Constitution Learn-it v1.7"`
- L'`id` et le `version` disent V1_8 ; les `human_readable` disent v1.7. Cette ambiguïté rend toute validation de fédération non-déterministe : un système qui s'appuie sur les labels humains pour router les dépendances peut pointer vers une mauvaise version.
- **Ancrage** : `LINK.references`, `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL`
- **Couche** : Constitution + Référentiel + LINK

#### Élevé — Autorité `derived` sur les bindings LINK sans critère mécanique

- Tous les `TYPE_BINDING_*` du LINK sont en `authority: derived`. Aucune règle ne précise ce que `derived` interdit concrètement pour un binding.
- `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` est le seul garde-fou, mais il est rédigé en termes intentionnels ("logique métier autonome"), non structurels. Le moteur ne peut pas vérifier mécaniquement cette contrainte — elle repose sur une revue humaine sémantique, ce qui contredit `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.
- **Ancrage** : `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
- **Couche** : LINK

#### Modéré — Dépendance circulaire implicite dans les RULES de propagation

- `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` dépend de `INV_GRAPH_PROPAGATION_ONE_HOP` et `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED`, mais les deux invariants dépendent eux-mêmes de `TYPE_KNOWLEDGE_GRAPH`, qui doit être acyclique (`INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC`).
- Si le graphe contient un cycle non détecté avant le runtime, la règle de propagation peut s'appliquer à un état interdit sans blocage préalable garanti — l'ordre de validation n'est pas spécifié.
- **Ancrage** : `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS`, `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC`
- **Couche** : Constitution

#### Modéré — `TYPE_MASTERY_COMPONENT_T` sans dépendance inverse sur `INV_MSC_AND_STRICT`

- `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` contraint `TYPE_MASTERY_MODEL` mais n'est pas listé dans `depends_on` de `TYPE_MASTERY_COMPONENT_T`.
- Si T est évalué avant que la maîtrise de base soit établie, l'invariant est déclaré mais la dépendance d'ordre n'est pas enforçable mécaniquement.
- **Ancrage** : `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`, `TYPE_MASTERY_COMPONENT_T`
- **Couche** : Constitution

---

### Axe 2 — Solidité théorique

#### Élevé — Mastery Learning : absence de "mastery gate" pour T en régime provisoire

- `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` sépare T de la maîtrise de base, mais aucune règle ne précise le comportement si T est sollicité sur une KU en état de maîtrise provisoire non confirmée (`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`).
- Un apprenant en fenêtre provisoire peut-il accéder à des missions T ? Le système peut osciller entre autoriser et bloquer selon l'implémentation.
- **Ancrage** : `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`, `TYPE_MASTERY_COMPONENT_T`
- **Couche** : Constitution + Référentiel

#### Modéré — AR-N3 absent de la hiérarchie de précédence des signaux

- `TYPE_SELF_REPORT_AR_N3` alimente `TYPE_STATE_AXIS_CALIBRATION`. Le Référentiel définit `TYPE_REFERENTIEL_AR_N3_CONFIGURATION` mais aucun paramètre ne borne le poids de AR-N3 sur l'axe.
- `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER` / `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY` liste : AR-N1 > AR-N2 > proxys > tendances — AR-N3 est absent de cette hiérarchie.
- En cas de bilan fortement discordant (AR-N3 déclare haute compétence, proxys indiquent faiblesse), aucune règle de précédence ne s'applique.
- **Ancrage** : `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`, `TYPE_REFERENTIEL_AR_N3_CONFIGURATION`
- **Couche** : Référentiel

#### Modéré — Charge cognitive transversale multi-KU non agrégée

- Le modèle d'état apprenant gère l'activation par KU mais le système ne dispose d'aucun agrégateur de charge cognitive transversale sur une session impliquant de multiples KU de types distincts.
- L'axe Activation peut être "productif" sur chaque KU isolément tout en générant un overload global non détecté.
- **Ancrage** : `TYPE_STATE_AXIS_ACTIVATION`, `TYPE_LEARNER_STATE`
- **Couche** : Constitution

---

### Axe 3 — États indéfinis moteur

#### CRITIQUE — Comportement moteur non spécifié si le LINK est absent ou partiellement chargé

- Le LINK est le seul mécanisme de fermeture inter-Core, mais aucun invariant ne précise le comportement système si le LINK est absent, corrompu, ou si les deux Cores sont présents mais le LINK non chargé.
- Le système peut fonctionner en mode "local seulement" sans détecter l'incomplétude. Aucun `EVENT` ne capture ce cas de défaillance.
- **Ancrage** : `LINK.metadata`, `INV_RUNTIME_FULLY_LOCAL`
- **Couche** : LINK + Constitution

#### Élevé — Oscillation sur KU créative reclassifiée post-déploiement

- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` bloque le déploiement autonome si aucun feedback déterministe n'est disponible.
- Si une KU est reclassifiée comme créative par patch après déploiement, la règle ne précise pas si les sessions en cours sont immédiatement suspendues ou si l'interdiction est prospective seulement.
- Le moteur peut se retrouver avec une KU déployée en régime autonome et un invariant nouvellement violé.
- **Ancrage** : `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`
- **Couche** : Constitution

#### Modéré — Axes `unknown` persistants sans mécanisme d'escalade

- Un axe peut rester `unknown` indéfiniment. Aucune règle ne déclenche une escalade si plusieurs axes restent `unknown` sur une fenêtre prolongée.
- Combiné à `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`, le système peut rester indéfiniment en mode conservateur sans signal d'anomalie vers la chaîne de correction.
- **Ancrage** : `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`, `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`
- **Couche** : Constitution

---

### Axe 4 — Dépendances IA implicites

#### Élevé — `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` non-mécanique

- Vérifier qu'un binding LINK ne contient pas de "logique métier autonome" requiert une inférence sémantique continue — exactement ce qu'interdit `INV_RUNTIME_FULLY_LOCAL`.
- Cette contrainte ne peut être validée que par un humain ou un outil externe hors session, mais ce prérequis n'est pas documenté dans le pipeline de validation patch du LINK.
- **Ancrage** : `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`, `INV_RUNTIME_FULLY_LOCAL`
- **Couche** : LINK

#### Modéré — `TYPE_FEEDBACK_COVERAGE_MATRIX` : "applicable" non-déterministe

- `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK` se déclenche si "aucune entrée matrice applicable". Déterminer si une entrée est "applicable" à une erreur concrète peut nécessiter un matching sémantique, pas seulement structurel.
- Ce matching n'est pas spécifié comme déterministe.
- **Ancrage** : `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK`, `TYPE_FEEDBACK_COVERAGE_MATRIX`
- **Couche** : Référentiel

---

### Axe 5 — Gouvernance

#### Élevé — Absence de règle de succession de version inter-Core

- Constitution V1_8 référence Référentiel V0_6 ; Référentiel V0_6 référence Constitution V1_8 (via labels mentionnant v1.7).
- Si une nouvelle version d'un Core est émise, aucune règle ne précise si le LINK doit être republié, si l'ancien LINK reste valide, ou comment le moteur détecte une désynchronisation de versions.
- Le pipeline de release (STAGE_07, STAGE_08) est référencé mais sa spec n'est pas dans ce Core.
- **Ancrage** : `LINK.metadata.constitution_version`, `LINK.metadata.referentiel_version`
- **Couche** : Constitution + LINK

#### Modéré — `patchable: false` sur les références inter-Core sans documentation intentionnelle

- `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` a `patchable: false`. Si la version du Référentiel évolue, la mise à jour de cette référence dans la Constitution nécessite une opération hors patch standard.
- Cette contrainte n'est pas documentée comme intentionnelle dans le pipeline.
- **Ancrage** : `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION.patchable`
- **Couche** : Constitution

#### Faible — Anchors `[tables]` non tracés vers document source

- Le Référentiel utilise `[tables]` comme anchor (ex. `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE`) alors que la Constitution utilise des anchors numérotés `[S14]`.
- Les anchors `[tables]` ne sont pas tracés vers un document source identifié, ce qui fragilise l'auditabilité.
- **Ancrage** : `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE.source_anchor`
- **Couche** : Référentiel

---

## Risques prioritaires

| Priorité | Risque | Core concerné |
|---|---|---|
| **CRITIQUE** | Incohérence V1_7/V1_8 dans les labels des références croisées | Constitution + Référentiel + LINK |
| **CRITIQUE** | Comportement moteur non spécifié si LINK absent ou non chargé | LINK + Constitution |
| **Élevé** | AR-N3 absent de la hiérarchie de précédence des signaux | Référentiel |
| **Élevé** | `derived` authority sur bindings LINK sans critère mécanique vérifiable | LINK |
| **Élevé** | Absence de règle de succession de version inter-Core | Constitution + LINK |
| **Élevé** | KU créative reclassifiée post-déploiement : comportement sessions actives indéfini | Constitution |
| **Élevé** | Mastery provisoire + évaluation T : état non spécifié | Constitution + Référentiel |
| **Modéré** | Axes `unknown` persistants sans escalade | Constitution |
| **Modéré** | Validation de `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` non-mécanique | LINK |
| **Modéré** | Ordre de validation graphe acyclique avant propagation non garanti | Constitution |
| **Modéré** | Charge cognitive transversale non agrégée | Constitution |
| **Faible** | Anchors `[tables]` non tracés vers document source | Référentiel |

---

## Corrections à arbitrer avant patch

- **Arbitrage A1** : Corriger les labels `human_readable` des références croisées vers "v1.8" dans les trois Cores — ou figer volontairement à "v1.7" et aligner l'`id` — mais décider d'une convention stable et unique.
- **Arbitrage A2** : Définir un comportement système contractuel en absence du LINK : état interdit (bloquant au chargement), ou mode dégradé autorisé avec périmètre borné ? Relève de la Constitution.
- **Arbitrage A3** : Décider si AR-N3 est intégré dans la hiérarchie de précédence des signaux (et à quel rang) ou s'il alimente l'axe Calibration via un mécanisme séparé entièrement documenté. Décision Référentiel, impact Constitution.
- **Arbitrage A4** : Spécifier l'effet temporel d'un patch de reclassification KU créative sur les sessions actives : suspension immédiate ou effet prospectif seulement ? Relève de la Constitution (scope: patch_architecture).
- **Arbitrage A5** : Définir un seuil de fenêtre `unknown` persistant et son escalade — paramètre candidat Référentiel, règle associée Constitution.
