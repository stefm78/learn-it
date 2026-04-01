# CHALLENGE REPORT — Constitution System

**ID:** Sonar  
**Stage:** STAGE_01_CHALLENGE  
**Pipeline:** constitution  
**Date:** 2026-04-01  
**Cores analysés :**
- `CORE_LEARNIT_CONSTITUTION_V1_9` (version V1_9_FINAL)
- `CORE_LEARNIT_REFERENTIEL_V1_0` (version V1_0_FINAL)
- Note de focalisation : aucune

---

## Résumé exécutif

Le système Constitution + Référentiel présente une architecture de gouvernance solide, avec une séparation des couches claire et un ensemble d'invariants bien protégés. Les patchs récents issus de l'arbitrage `ARBITRAGE_2026_04_01` comblent plusieurs angles morts identifiables. Cependant, l'analyse adversariale révèle des zones de fragilité significatives, notamment autour : (1) de l'absence du Core LINK dans les entrées effectives de certaines règles ; (2) d'états moteur potentiellement non déterministes sur la gestion simultanée des dépendances MSC et de la propagation graphe ; (3) de la maturité empirique des proxys comportementaux dans un moteur posé comme 100 % local ; (4) et de l'absence de règle de priorité explicite en cas de collision entre RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL et les mécanismes de rétrogradation actifs simultanément.

Deux risques sont classés **critiques**, trois **élevés**, quatre **modérés**.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### 1.1 — Référence inter-Core LINK absente des inputs effectifs

**Élément concerné :** `CORE_LEARNIT_CONSTITUTION_V1_9`, `CORE_LEARNIT_REFERENTIEL_V1_0`  
**Nature du problème :** Les deux Cores déclarent des références inter-Core (`REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`, `REF_CORE_LEARNIT_CONSTITUTION_V1_9_IN_REFERENTIEL`) mais aucun des deux ne déclare de référence vers un Core LINK. Plusieurs éléments du Référentiel manipulent des `PARAM_REFERENTIEL_ADAPTIVE_REGIME_*` et une `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` dont la matrice 3×3 (9 états, activation 3→5→9) est définie paramètriquement — mais la liaison vers le Core LINK qui devrait matérialiser les bindings fins entre états et règles adaptatives est entièrement implicite dans ces deux Cores.  
**Type :** gouvernance  
**Impact moteur :** Si le LINK n'est pas lu conjointement, le moteur peut exécuter des transitions de régime en ignorant des bindings déclarés dans le LINK. Aucune détection d'incohérence n'est possible depuis la Constitution ou le Référentiel seuls.  
**Correction à arbitrer :** Déclarer une référence explicite `REF_CORE_LEARNIT_LINK_VX_IN_REFERENTIEL` dans le Référentiel, à minima pour les blocs `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` et `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE`.

---

#### 1.2 — Bindings manquants sur RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL

**Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` [ARBITRAGE_2026_04_01][DIVMSC-01], `EVENT_MSC_DOWNGRADE`  
**Nature du problème :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` dépend de `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et déclenche `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`. Mais `EVENT_MSC_DOWNGRADE` déclenche aussi `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` qui déclenche également `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`. Il n'existe aucune règle de priorité ou de fusion entre ces deux chemins quand ils s'activent simultanément (MSC calculé OK mais perçu NOK → diagnostique via DIVMSC, ET rétrogradation simultanée d'une composante → diagnostique via DOWNGRADE).  
**Type :** implémentabilité  
**Impact moteur :** Double déclenchement de `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` sur la même KU en une session. Risque de surcharge de l'apprenant ou de boucle diagnostique non terminée avant la fin de session.  
**Correction à arbitrer :** Introduire une règle de fusion ou de priorité explicite entre les deux chemins diagnostiques sur la même KU, dans la Constitution ou dans une note opérationnelle du Référentiel.

---

#### 1.3 — Paramètre orphelin PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW

**Élément concerné :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` [S2][S20]  
**Nature du problème :** Ce paramètre est déclaré dans la Constitution (scope `runtime_evaluation`) mais aucune règle, aucun invariant et aucun événement dans la Constitution **ni** dans le Référentiel ne le consomme explicitement. Le Référentiel mentionne la maîtrise provisoire via `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` mais ne référence pas ce paramètre.  
**Type :** complétude  
**Impact moteur :** Fenêtre de vérification de maîtrise provisoire sans consommateur déclaré = paramètre inopérant ; les maîtrises héritées peuvent ne jamais être vérifiées moteur.  
**Correction à arbitrer :** Créer un EVENT ou une RULE consommatrice dans le Référentiel, ou supprimer le paramètre de la Constitution si sa gestion est entièrement déléguée au LINK.

---

#### 1.4 — RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED vs INV_CONSERVATIVE_RULE_WITHOUT_AR_N1

**Élément concerné :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` [PATCH_V1_9__STAGE03], `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`  
**Nature du problème :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` impose que l'absence d'AR-N1 produise un scaffolding léger réversible. `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` pose qu'un axe peut rester `unknown/absent/non-observable`. Si les deux sont actifs simultanément en absence d'AR-N1 : l'invariant exige une réponse conservatrice, mais la règle autorise l'absence de toute valeur d'axe. Il manque un pont logique précisant lequel prime ou comment ils se combinent.  
**Type :** implémentabilité  
**Impact moteur :** Le moteur peut osciller entre réponse conservatrice (déclenche scaffolding) et état `unknown` (pas d'action). En pratique cela dépend de l'ordre d'évaluation implémentatoire, qui n'est pas spécifié.  
**Correction à arbitrer :** Préciser que `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` prime sur `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` pour l'axe d'activation, ou exclure explicitement l'axe d'activation du périmètre `unknown` autorisé.

---

### Axe 2 — Solidité théorique

#### 2.1 — Charge cognitive

**Point solide :** `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL` (25 min) fournit un garde-fou de dernier recours explicitement borné.  
**Zone de risque :** Aucun mécanisme n'adapte la charge cognitive intra-session (complexité, modalité, séquencement) en fonction du type de KU. `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` protège la modalité mais ne régule pas la densité ou la durée d'exposition par type.  
**Angle mort :** L'effet de la combinaison interleaving + diagnostique forcée (rétrogradation) sur la charge cognitive n'est pas modélisé. Deux mécanismes peuvent s'enchaîner en une session sans garde-fou de saturation.

#### 2.2 — Mémoire / consolidation

**Point solide :** Les multiplicateurs temporels R par type de KU (`TYPE_REFERENTIEL_TEMPORAL_MULTIPLIER_TABLE`) sont bien différenciés (déclaratif, formel, procédural×2–3, perceptuel×0.5, créatif×1).  
**Zone de risque :** Le délai de robustesse moyen terme (`PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_MEDIUM`, 7 jours) et court terme (3 jours) ne sont pas désambiguïsés par rapport au type de KU : qui prend lequel ?  
**Angle mort :** Aucun mécanisme de spacing adaptatif basé sur la courbe d'oubli individuelle. Le moteur opère sur des seuils fixes, pas sur une estimation de l'oubli par apprenant.

#### 2.3 — Motivation

**Point solide :** `INV_VC_NOT_GENERAL_MOTIVATION_PROXY` protège correctement contre la sur-interprétation de l'axe VC.  
**Zone de risque :** Le mécanisme de déclenchement du patch relevance (VC basse persistante → révision enjeux) est bien pensé, mais l'absence de tout mécanisme explicite de support à la motivation intrinsèque (autonomie, compétence perçue, relatedness) au-delà de l'axe VC crée une dépendance excessive à un seul signal.  
**Angle mort :** L'intention de session est collectée mais déclarée non-bloquante et non adaptative (`RULE_SESSION_INTENTION_NON_BLOCKING`). Son potentiel pour le support du forethought SRL (planification, auto-régulation anticipée) est déclaré mais non actionné moteur.

#### 2.4 — Métacognition / SRL

**Point solide :** Le modèle AR-N1/N2/N3 est bien ancré dans les niveaux SRL (événementiel, fin de session, périodique).  
**Zone de risque :** AR-N3 est un bilan périodique mais son effet sur le moteur est borné au reweighting d'AR-N1 via calibration. Il n'existe aucun mécanisme de feedback métacognitif explicite à destination de l'apprenant (« voici votre profil de calibration »). Le SRL reste asymétrique : le moteur apprend sur l'apprenant mais l'apprenant n'est pas outillé pour apprendre sur lui-même.  
**Angle mort :** La régulation de l'effort et la gestion de la valeur-coût ne sont pas reliées aux stratégies d'auto-régulation connues (GTD, planning de session, etc.).

#### 2.5 — Émotions / engagement

**Point solide :** La distinction confusion/frustration/anxiété dans `TYPE_SELF_REPORT_AR_N1` est théoriquement fondée (AEQ-like).  
**Zone de risque :** La réponse à la détresse est conservatrice (scaffolding léger) mais le moteur ne dispose d'aucun outil pour distinguer une détresse productive (zone proximale de développement active) d'une détresse paralysante. La réponse est identique dans les deux cas.  
**Angle mort :** Aucun mécanisme d'escalade ou de notification externe n'est déclenché par une détresse répétée non résolue (ex : 3 sessions consécutives en régime Détresse sans sortie). Ce cas n'est pas couvert explicitement.

#### 2.6 — Mastery learning

**Point solide :** Le AND strict sur P×R×A est une décision pédagogiquement solide et bien protégée (non patchable).  
**Zone de risque :** La composante T (transférabilité) est séparée mais son déclenchement dépend de la maîtrise de base établie. Le système ne spécifie pas quand et comment T est proposée à l'apprenant après établissement de la maîtrise de base.  
**Angle mort :** L'absence d'un indicateur de progression vers la maîtrise (ex : combien d'occurrences sur 5 requises ?) pour l'apprenant prive le système d'un levier de motivation par compétence perçue.

#### 2.7 — Ingénierie pédagogique

**Point solide :** `TYPE_AUTHENTIC_CONTEXT` et `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4` protègent rigoureusement les niveaux supérieurs de Bloom.  
**Zone de risque :** La matrice de couverture feedback (`TYPE_FEEDBACK_COVERAGE_MATRIX`) est un livrable obligatoire pour KU formelles et procédurales, mais son format, son niveau de granularité et ses critères de complétude ne sont pas spécifiés constitutionnellement. La qualité réelle de cette matrice dépend entièrement du designer.  
**Angle mort :** Il n'existe pas de mécanisme de validation de cohérence entre le niveau Bloom déclaré d'une KU et ses artefacts de feedback associés.

---

### Axe 3 — États indéfinis moteur

#### 3.1 — Simultanéité : mode Détresse + rétrogradation MSC active

Le régime Détresse dans la matrice adaptative prime sur tous (`RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`, règle 1). Mais `EVENT_MSC_DOWNGRADE` peut être en cours simultanément, déclenchant `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`. Quelle est la priorité ? Le moteur peut-il planifier une tâche diagnostique en régime Détresse ? La Constitution ne statue pas.  
**Risque :** État indéfini — diagnostique planifiée vs réponse conservatrice de Détresse.

#### 3.2 — Maîtrise provisoire expirée et aucun consommateur déclaré

`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` définit une fenêtre de vérification, mais aucun mécanisme ne ferme cette fenêtre ni ne produit d'état explicite à son expiration. Que se passe-t-il si la maîtrise provisoire n'est pas vérifiée dans la fenêtre ? Aucun état interdit ni fallback n'est déclaré.  
**Risque :** Maîtrise héritée potentiellement invalide jamais détectée.

#### 3.3 — Absence de données de calibrage + KU créative

En mode `RULE_NO_CALIBRATION_CONSERVATIVE_START`, la position initiale est basse. Pour une KU créative, le calibrage dure 5–15 min (`PARAM_REFERENTIEL_KU_CALIBRATION_CREATIVE_DURATION`). Si l'apprenant n'a aucune donnée préalable et que la KU est créative, le moteur démarre en position basse **et** sans multiplicateur R applicable (fallback ×1 via `INV_REFERENTIEL_CREATIVE_R_FALLBACK_IS_X1`). Quelle est la séquence d'actions concrète ? Aucun chemin de sortie du mode conservateur vers le calibrage créatif n'est documenté.  
**Risque :** Blocage fonctionnel ou séquence non déterministe au premier déploiement sur KU créative.

#### 3.4 — Axe VC désactivé pendant une investigation systémique active

`RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` peut désactiver l'axe VC. `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` peut être active simultanément. L'investigation systémique se déclenche sur 2 signaux en anomalie (`PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`), dont VC inobservable fait partie. Si VC est désactivé **avant** que le seuil d'investigation soit atteint, ce signal disparaît du comptage. Le moteur peut potentiellement ne jamais déclencher l'investigation systémique si la désactivation VC intervient trop tôt.  
**Risque :** Sous-détection d'une investigation systémique requise.

---

### Axe 4 — Dépendances IA implicites

#### 4.1 — Détection de misconception

`RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` exige qu'une KU soit "flaggée misconception". Ce flag est supposément posé en phase Analyse/Design, mais aucun critère déterministe de détection de misconception n'est spécifié dans les Cores. En usage, la détection d'une misconception à partir des réponses apprenant requiert une inférence sémantique que le moteur 100 % local ne peut pas exécuter sans modèle statistique ou taxonomy d'erreurs préindexée.  
**Type :** implémentabilité — dépendance IA implicite  
**Alternative sans IA continue :** Exiger que les misconceptions soient exhaustivement préindexées dans la `TYPE_FEEDBACK_COVERAGE_MATRIX` à la conception, avec pattern matching déterministe sur les réponses.

#### 4.2 — Qualité pédagogique du patch

`TYPE_PATCH_QUALITY_GATE` inclut une validation de respect des "principes pédagogiques protégés". Ces principes sont constitutionnels mais leur évaluation concrète sur un patch YAML nécessite une lecture sémantique qui dépasse la validation déterministe locale. `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` interdit d'utiliser un critère sémantique localement — mais cela crée un risque de qualité gate "vide" localement, dont le rôle est entièrement délégué à la chaîne hors-session sans description précise des critères opérationnels.  
**Type :** gouvernance — dépendance IA implicite en chaîne hors-session  
**Alternative :** Formaliser une checklist binaire déterministe des critères pédagogiques protégés, applicable mécaniquement par un outil ou un auditeur humain.

#### 4.3 — Évaluation de la matrice feedback

`PARAM_REFERENTIEL_FEEDBACK_COVERAGE_REFERENCE_THRESHOLD` (70 %) suppose une mesure de couverture. Le calcul de cette couverture nécessite de comparer les erreurs observées aux templates déclarés — mais l'observation et la classification des erreurs dans un moteur 100 % local suppose que toutes les erreurs possibles sont préindexées. La couverture réelle ne peut être connue qu'à la condition que la taxonomie d'erreurs soit fermée, ce qui n'est jamais garanti en cours d'usage réel.  
**Type :** implémentabilité  
**Alternative :** Accepter explicitement que le taux de couverture soit un taux de couverture des erreurs *anticipées*, et documenter cette limitation dans le Référentiel.

---

### Axe 5 — Gouvernance

#### 5.1 — Séparation Constitution/Référentiel : solide mais asymétrique

La protection est forte côté Constitution (invariants non patchables, AND non modifiable, propagation 1-saut verrouillée). Côté Référentiel, les protections sont analogues (`INV_REFERENTIEL_CONSTITUTIONAL_AND_LOGIC_NOT_MODIFIABLE_HERE`, etc.). Point solide.

#### 5.2 — Trou de couverture : la maîtrise provisoire héritée

Le mécanisme de maîtrise provisoire est déclaré paramètriquement (`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`) mais la gouvernance de son cycle de vie complet (ouverture, suivi, expiration, escalade) n'est pas couverte par un EVENT ou une RULE dans l'un ou l'autre des Cores. C'est un invariant mal protégé de fait.

#### 5.3 — Patchabilité des bindings inter-Core

Les éléments déclarés `patchable: false` dans les Cores sont bien protégés. Cependant, `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` est `patchable: true` — ce qui signifie que la matrice des régimes adaptatifs (9 états, logique de résolution) peut être patchée. Les `CONSTRAINT_REFERENTIEL_PATCH_SCOPE_MUST_REMAIN_CONSTITUTIONALLY_BOUNDED` le limite, mais la règle de résolution des conflits de régimes (`RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`) est elle-même `patchable: true`. Un patch mal conçu pourrait altérer la table de priorité de résolution des conflits, ce qui est un invariant de gouvernance de facto.  
**Correction à arbitrer :** Évaluer si la table de priorité de `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` doit être déclarée `patchable: false`.

#### 5.4 — Versioning inter-Core non géré automatiquement

La Constitution V1_9 référence le Référentiel V1_0 et vice-versa. Cette compatibilité de version est déclarée statiquement mais aucun mécanisme de vérification de cohérence de version inter-Core n'est prévu dans les Cores eux-mêmes. Une mise à jour de l'un sans mise à jour de l'autre peut créer une incompatibilité silencieuse.  
**Type :** gouvernance  
**Correction à arbitrer :** Introduire une règle de validation cross-version dans le pipeline de patch ou dans la phase STAGE_04_PATCH_VALIDATION.

---

### Axe 6 — Scénarios adversariaux

#### Scénario 1 — « Le Fantôme de la Maîtrise »

**Description :** Un apprenant hérite d'une maîtrise provisoire sur une KU complexe (procédurale, Bloom 3). La fenêtre de vérification (`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`) s'ouvre mais aucun mécanisme ne force la vérification dans la fenêtre. L'apprenant ne revient pas sur cette KU pendant 14 jours (en dehors des délais R courts déclarés). Le moteur ne dispose d'aucun EVENT pour forcer la vérification ou dégrader la maîtrise.  
**Mécanismes activés :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`, `INV_MSC_AND_STRICT`, `EVENT_LONG_INTERRUPTION`  
**Limite révélée :** La maîtrise provisoire peut persister indéfiniment sans être validée ou révoquée. Contradiction latente avec l'esprit de la robustesse temporelle R.

#### Scénario 2 — « La Tempête Diagnostique »

**Description :** Apprenant en régime Consolidation (maîtrise de base sur 3 KU liées en graphe). Il échoue à une tâche diagnostique sur KU_A → rétrogradation MSC → `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` marque KU_B et KU_C → `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` sur KU_B. Simultanément, le moteur détecte une divergence MSC calculé/perçu sur KU_A (3 sessions consécutives) → `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → nouvelle `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` sur KU_A. Le moteur planifie deux tâches diagnostiques en une session sans garde-fou de fusion.  
**Mécanismes activés :** `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS`, `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`  
**Limite révélée :** Double déclenchement diagnostique en une session. Surcharge cognitive non contrôlée.

#### Scénario 3 — « L'Investigation Silencieuse »

**Description :** Apprenant avec profil AR-réfractaire émergent (4 sessions sans AR-N1) + VC inobservable depuis 4 sessions. Le système devrait détecter 2 signaux en anomalie et déclencher `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` après 3 sessions. Mais `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` désactive l'axe VC après 5 sessions sans donnée. Si les paramètres sont configurés à leurs valeurs de référence, la désactivation VC (5 sessions) intervient **après** le seuil d'investigation (3 sessions) — ce qui semble correct. Mais si `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` est réglé à 3 sessions (borne basse) et `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD` à 4 sessions (borne haute), le signal VC disparaît avant que l'investigation soit déclenchée.  
**Mécanismes activés :** `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD`  
**Limite révélée :** Zone de chevauchement paramétriques entre désactivation VC et investigation systémique. Une combinaison de paramètres dans les fourchettes autorisées peut court-circuiter l'investigation.

---

### Axe 7 — Priorisation des risques

| Priorité | ID du risque | Description synthétique | Type | Couche |
|----------|--------------|------------------------|------|--------|
| **Critique** | RISK-C01 | Double déclenchement `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` (DIVMSC + DOWNGRADE simultanés) | Implémentabilité | Constitution |
| **Critique** | RISK-C02 | Zone de chevauchement paramétrique désactivation VC / investigation systémique (Scénario 3) | Gouvernance | Référentiel |
| **Élevé** | RISK-H01 | `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans consommateur — maîtrise provisoire jamais vérifiée | Complétude | Constitution + Référentiel |
| **Élevé** | RISK-H02 | `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` vs `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` : oscillation moteur | Implémentabilité | Constitution |
| **Élevé** | RISK-H03 | `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` patchable = invariant de gouvernance exposé | Gouvernance | Référentiel |
| **Modéré** | RISK-M01 | Absence de référence inter-Core LINK dans les Cores Constitution et Référentiel | Gouvernance | Constitution + Référentiel |
| **Modéré** | RISK-M02 | Versioning inter-Core statique non vérifié automatiquement | Gouvernance | Pipeline |
| **Modéré** | RISK-M03 | Absence de mécanisme d'escalade sur Détresse répétée non résolue (émotions) | Complétude | Constitution |
| **Modéré** | RISK-M04 | SRL asymétrique : apprenant sans feedback métacognitif sur son propre profil | Théorique | Constitution |
| **Faible** | RISK-F01 | `PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_SHORT` vs `MEDIUM` non affectés par type KU explicitement | Complétude | Référentiel |
| **Faible** | RISK-F02 | Couverture feedback mesurée sur taxonomie fermée — limitation non documentée | Implémentabilité | Référentiel |

---

## Risques prioritaires

### RISK-C01 — Double déclenchement diagnostique

- **Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS`, `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`
- **Nature :** Double activation de la même action sur la même KU en une session
- **Type :** Implémentabilité
- **Impact moteur :** Surcharge de l'apprenant, session non terminée, potentiel blocage moteur
- **Correction à arbitrer :** Ajouter une règle de fusion ou de priorité explicite ; ou ajouter une contrainte `CONSTRAINT_SINGLE_DIAGNOSTIC_PER_KU_PER_SESSION` dans la Constitution

### RISK-C02 — Court-circuit investigation systémique par désactivation VC anticipée

- **Élément concerné :** `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING`, `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD`
- **Nature :** Chevauchement paramétrique légal mais dangereux
- **Type :** Gouvernance
- **Impact moteur :** Investigation systémique non déclenchée malgré signaux critiques
- **Correction à arbitrer :** Ajouter une contrainte explicite : `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` doit être strictement supérieur à `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD`. Ou préserver le signal VC-inobservable dans le compteur d'investigation systémique même après désactivation de l'axe.

### RISK-H01 — Maîtrise provisoire sans lifecycle gouverné

- **Élément concerné :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`
- **Nature :** Paramètre déclaré, lifecycle absent
- **Type :** Complétude
- **Impact moteur :** Maîtrise non vérifiée indefiniment
- **Correction à arbitrer :** Créer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` et sa règle de traitement (rétrogradation automatique ou escalade) dans le Référentiel

---

## Corrections à arbitrer avant patch

| # | Élément | Nature | Type | Impact moteur | Correction proposée |
|---|---------|--------|------|--------------|---------------------|
| CA-01 | `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` + `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` | Double déclenchement `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` | Implémentabilité | Surcharge diagnostique | Règle de fusion ou contrainte `SINGLE_DIAGNOSTIC_PER_KU_PER_SESSION` |
| CA-02 | `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` vs `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD` | Chevauchement paramétrique | Gouvernance | Court-circuit investigation | Contrainte d'ordre entre les deux paramètres |
| CA-03 | `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` | Paramètre orphelin | Complétude | Maîtrise provisoire non vérifiée | Créer EVENT + RULE lifecycle de maîtrise provisoire dans le Référentiel |
| CA-04 | `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` vs `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` | Oscillation moteur possible | Implémentabilité | État indéfini sur axe activation | Préciser la primauté de l'invariant sur la règle pour l'axe activation |
| CA-05 | `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (`patchable: true`) | Invariant de gouvernance exposé au patch | Gouvernance | Altération possible de la table de priorité | Évaluer passage à `patchable: false` |
| CA-06 | Absence référence LINK dans Constitution et Référentiel | Binding inter-Core implicite | Gouvernance | Exécution possible sans LINK | Déclarer `REF_CORE_LEARNIT_LINK_VX_IN_REFERENTIEL` |
| CA-07 | Versioning inter-Core statique | Incompatibilité silencieuse possible | Gouvernance | Drift de version non détecté | Ajouter une vérification cross-version dans STAGE_04_PATCH_VALIDATION |
| CA-08 | Absence d'escalade sur Détresse répétée non résolue | Trou de couverture émotionnel | Complétude | Détresse prolongée sans signal | Créer `EVENT_PERSISTENT_DISTRESS_UNRESOLVED` et escalade |
| CA-09 | Délai R court vs moyen non affecté explicitement par type KU | Ambiguïté de calcul R | Complétude | Calcul R non déterministe selon contexte | Spécifier dans le Référentiel lequel s'applique selon le type KU |

---

*Rapport produit dans le cadre du STAGE_01_CHALLENGE, pipeline constitution. ID challenger : Sonar. Prêt pour STAGE_02_ARBITRAGE.*
