# CHALLENGE REPORT — Constitution Learn-it
## Metadata
- pipeline: constitution
- stage: STAGE_01_CHALLENGE
- run_date: 2026-04-01
- author: ClaudeThink (auditeur adversarial automatisé)
- cores_audited:
  - CORE_LEARNIT_CONSTITUTION_V1_9
  - CORE_LEARNIT_REFERENTIEL_V1_0
  - CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0

---

## Résumé exécutif

Le système tri-Core Constitution / Référentiel / LINK est structurellement solide dans son architecture de gouvernance et sa séparation des couches. Les invariants fondamentaux (AND strict du MSC, propagation 1 saut, localité runtime) sont cohérents et bien protégés.

Cependant, l'audit adversarial identifie **7 risques significatifs** dans les domaines suivants :

1. **Moteur indéfini** : absence d'un protocole clair de résolution de conflits quand plusieurs événements d'escalade sont simultanément actifs (`DIVMSC-01`, `MOT-01`, `SYST-01`)
2. **Gouvernance de la composante T** : T est constitutionnellement déclarée comme séparée mais aucun binding LINK n'explicite comment T est consommée dans la chaîne de décision pédagogique
3. **État initial et maîtrise provisoire** : le circuit de vérification de la maîtrise provisoire héritée (`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`) ne dispose pas d'un chemin d'escalade explicite en cas d'expiration non résolue
4. **Cycle KU créative en mode autonome** : la contrainte `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` est correcte mais le chemin de désactivation runtime d'une KU créative sans feedback local n'est pas borné opérationnellement
5. **VC unobservable et désactivation** : la règle `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` désactive l'axe VC mais il manque un binding LINK explicite pour documenter comment la réactivation est signalée au moteur constitutionnel
6. **Séparation couches : logique métier résiduelle dans le LINK** : `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` décrit un flux de cause-à-effet avec plusieurs étapes conditionnelles — frontière avec logique métier discutable
7. **Absence de KU type "conceptuel"** : le référentiel définit des multiplicateurs R pour `déclaratif`, `formel`, `procédural`, `perceptuel`, `créatif`, mais la Constitution ne fait pas mention d'une KU "conceptuelle" ou "épistémique" pourtant impliquée par le terme "épistémologique" dans `TYPE_KNOWLEDGE_UNIT`

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### F1.1 — Conflit d'autorité entre escalades concurrentes [CRITIQUE]
**Ancrage** : `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` (MOT-01), `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS` (SYST-01)

Le système possède trois mécanismes d'escalade hors-session distincts pouvant se déclencher simultanément sur un même apprenant :
- `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` → diagnostique ciblé puis escalade design
- MOT-01 → `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` (référencé dans PARAM mais absent en EVENT déclaré dans le Référentiel)
- SYST-01 → `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` (idem : référencé mais non déclaré comme EVENT formel)

**Risque moteur** : aucune règle de priorité explicite entre ces trois escalades concurrentes. Si les trois sont simultanément déclenchées, le moteur n'a pas d'ordre d'exécution déterministe. La règle GF-08 (`RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE`) s'applique en fallback mais constitue une réponse conservatrice générique, non adaptée à des escalades pédagogiques critiques.

**Placement** : Constitution (logique de gouvernance runtime) et Référentiel (paramétrie des seuils).

#### F1.2 — Événements référencés mais non déclarés [ÉLEVÉ]
**Ancrage** : `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`

Deux événements sont nommés dans les `human_readable` de paramètres référentiels :
- `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`
- `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED`

Ces identifiants ne sont définis dans aucun bloc EVENTS (ni Constitution, ni Référentiel, ni LINK). Il s'agit de dépendances implicites qui rendent impossible une validation structurelle complète du graphe d'événements.

**Placement** : Référentiel (correction des EVENTS manquants requis).

#### F1.3 — Binding manquant pour la composante T [ÉLEVÉ]
**Ancrage** : `TYPE_MASTERY_COMPONENT_T`, `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`

Le LINK explicite le binding P/R/A → paramètres référentiels dans `TYPE_BINDING_MSC_COMPONENTS_TO_REFERENTIEL_PARAMETERS`. La composante T est délibérément absente (car séparée de la maîtrise de base). Cependant, aucun binding inter-Core n'explicite :
- comment T est qualifiée au niveau opérationnel (paramètre de seuil ? absent du Référentiel)
- quelle action moteur T déclenche une fois satisfaite
- si T requiert une configuration référentielle propre (multiplicateur R adapté ? Bloom minimal ? Contexte authentique imposé ?)

T est constitutionnellement correcte mais opérationnellement orpheline.

**Placement** : LINK (binding T manquant), Référentiel potentiel (absence de paramétrie T).

#### F1.4 — Maîtrise provisoire : chemin d'expiration incomplet [MODÉRÉ]
**Ancrage** : `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` (Constitution)

La Constitution déclare une fenêtre de vérification pour la maîtrise provisoire héritée. Mais :
- le chemin de vérification (déclenchement d'une tâche diagnostique courte après expiration) est implicitement couvert par `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` — ce n'est pas la même sémantique
- l'expiration de la fenêtre sans résolution ne génère pas d'EVENT déclaré
- aucune règle ne spécifie ce que le moteur doit faire si la vérification de maîtrise provisoire échoue (rétrograder ? geler ? escalader ?)

**Placement** : Constitution (règle de gestion de la fenêtre provisoire) et Référentiel (paramètre de durée de la fenêtre non déclaré).

---

### Axe 2 — Solidité théorique

#### F2.1 — Charge cognitive : absence de signal d'alerte composite [MODÉRÉ]
**Ancrage** : `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL` (25 min), `TYPE_STATE_AXIS_ACTIVATION`, `TYPE_SELF_REPORT_AR_N1`

Le garde-fou de 25 minutes est un signal temporel univariate. Or la littérature sur la charge cognitive (CLT — Sweller) distingue trois composantes : intrinsèque, extrinsèque et germane. Le système ne dispose pas d'indicateur composite de charge cognitive croisant :
- la durée session
- le type de KU (formelle/procédurale → charge intrinsèque plus élevée)
- le régime d'activation (détresse ou sous-défi)
- la densité des tâches dans la séquence

Le risque est de déclencher un arrêt de session sans discrimination de la source de fatigue, ou à l'inverse de ne pas détecter une surcharge pour des sessions courtes mais intenses (procédural + détresse).

**Placement** : Référentiel (évolution du paramètre ou nouvelle règle composite).

#### F2.2 — Métacognition / SRL : AR-N2 "intention" vs "forethought" SRL [MODÉRÉ]
**Ancrage** : `RULE_SESSION_INTENTION_NON_BLOCKING` (Constitution), `TYPE_REFERENTIEL_SESSION_INTENTION_CONFIGURATION` (Référentiel)

L'intention de session est qualifiée de "support de forethought SRL" mais reste uniquement informative et sans effet moteur déclaré. Or dans les modèles SRL (Zimmerman, Pintrich), la phase de forethought informe l'adaptation de la difficulté et du séquencement. L'absence totale d'effet moteur de l'intention de session contraste avec la sophistication du reste du système. Il n'est pas clair si cette absence est un choix délibéré (conservatisme) ou une lacune de conception.

Ce point mérite arbitrage explicite : est-ce un principe constitutionnel ou une contrainte provisoire ?

**Placement** : Constitution (clarification d'intention de conception).

#### F2.3 — Gamification : probatoire sans durée bornée [FAIBLE]
**Ancrage** : `RULE_UNVERIFIED_GAMIFICATION_PROBATION` (Constitution), `RULE_REFERENTIEL_UNVALIDATED_GAMIFICATION_PROBATION` (Référentiel)

Le mode probatoire de la gamification est déclaré dans les deux cores, mais aucun n'indique :
- la durée du probatoire
- le critère de sortie (validation de non-nuisance : comment, par qui ?)
- ce qui se passe si la validation ne vient jamais

C'est une règle ouverte à gauche (entrée possible) et sans sortie déterministe.

**Placement** : Référentiel (paramètres de durée et critère de validation).

---

### Axe 3 — États indéfinis moteur

#### F3.1 — KU créative en mode autonome : désactivation non bornée [ÉLEVÉ]
**Ancrage** : `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`, `TYPE_AUTONOMY_REGIME`

L'invariant interdit le déploiement autonome d'une KU créative sans feedback local déterministe. Mais :
- si une KU créative est déjà déployée dans un graphe actif et que son feedback local devient indisponible (suite à un patch par exemple), que se passe-t-il ?
- le moteur doit-il geler la KU ? Interrompre la session ? Basculer en mode hybride bloquant ?
- il n'existe pas de chemin d'état de désactivation runtime clairement défini pour cette situation

**Risque** : état intermédiaire non défini — la KU est "en cours" mais le feedback est absent, le moteur oscille.

**Placement** : Constitution (invariant de désactivation runtime requis).

#### F3.2 — Convergence VC désactivée + AR-réfractaire + MSC divergent [CRITIQUE]
**Ancrage** : `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING`, `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION`, `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`

Scénario : un apprenant est simultanément en :
- axe VC désactivé (non observable sur ≥5 sessions)
- profil AR-réfractaire (non-réponse AR-N1 sur ≥5 sessions)
- divergence MSC calculé vs perçu

Dans ce scénario, le moteur n'a plus de signal auto-rapport exploitable (VC désactivé, AR-N1 réfractaire) et rencontre une divergence MSC. Le protocole `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` requiert un retour diagnostique ciblé — mais cette règle dépend d'`EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` qui dépend lui-même d'`AR-N1` pour détecter le "blocage total signalé persistant". Si AR-N1 est réfractaire, l'EVENT ne peut pas se déclencher correctement.

**Risque** : blocage silencieux — l'apprenant est en difficulté, le moteur ne le voit pas et continue en mode conservateur indéfiniment.

**Placement** : Constitution (règle de détection dégradée) et Référentiel (condition de déclenchement de DIVMSC-01 en absence d'AR-N1).

#### F3.3 — Indice ICC non relié au reste du pipeline runtime [FAIBLE]
**Ancrage** : `TYPE_CORPUS_CONFIDENCE_ICC`

L'ICC (Indice de confiance du corpus) est déclaré en Constitution comme type à portée `analysis`. Aucune règle, événement ou paramètre ne définit :
- comment une ICC basse influence le moteur runtime
- si une ICC basse peut bloquer le déploiement
- quel seuil ICC est acceptable

C'est un concept déclaré sans chaîne causale complète.

**Placement** : Référentiel (paramètre ICC minimal) ou Constitution (règle de blocage déploiement sur ICC insuffisant).

---

### Axe 4 — Dépendances IA implicites

#### F4.1 — Détection de misconception : processus non spécifié [ÉLEVÉ]
**Ancrage** : `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`

La règle impose une mission de conflit cognitif quand une KU est flaggée `misconception`. Mais :
- comment une KU est-elle flaggée `misconception` ? Ce flag est-il posé lors de l'Analyse (phase Design) ou peut-il être posé en runtime ?
- si c'est en runtime : comment le moteur détecte-t-il une misconception sans inférence sémantique continue (interdite par `INV_RUNTIME_FULLY_LOCAL`) ?
- si c'est uniquement en Analyse : le système est dépendant d'une annotation humaine experte, ce qui constitue une dépendance implicite non déclarée

**Risque** : la règle est constitutionnellement solide mais son activation runtime repose soit sur une IA d'analyse hors-session non mentionnée, soit sur une annotation humaine dont la qualité n'est pas bornée.

**Placement** : Constitution (clarification du scope de détection) et Référentiel (paramètre de qualité de l'annotation misconception).

#### F4.2 — Feedback Coverage Matrix : génération Design-time implicitement IA-dépendante [MODÉRÉ]
**Ancrage** : `TYPE_FEEDBACK_COVERAGE_MATRIX`, `INV_NO_RUNTIME_CONTENT_GENERATION`

La matrice de couverture feedback est un livrable obligatoire de la phase Design pour KU formelles ou procédurales. Sa construction nécessite une anticipation exhaustive des erreurs et la création de templates de feedback. Cette construction :
- est typiquement assistée par LLM en pratique (pour un volume de KU non trivial)
- n'est pas qualifiée comme "offline AI-generated artifact" dans le système
- est potentiellement de qualité très variable selon le processus de production

Le système ne déclare pas de contrainte de qualité minimale sur la matrice elle-même (seul `PARAM_REFERENTIEL_FEEDBACK_COVERAGE_REFERENCE_THRESHOLD` à 70% existe, mais en couverture quantitative, pas qualitative).

**Placement** : Référentiel (contrainte de qualité de la matrice).

---

### Axe 5 — Gouvernance

#### F5.1 — Frontière LINK / logique métier : binding AR-N3 ambigu [ÉLEVÉ]
**Ancrage** : `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING`

Ce binding LINK décrit un flux en plusieurs étapes conditionnelles :
1. AR-N3 disponible → alimente `TYPE_STATE_AXIS_CALIBRATION`
2. si calibration basse sur N bilans → active `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`
3. → reweighting temporaire borné d'AR-N1

Ce flux multi-étapes avec conditions intermédiaires approche la frontière avec une logique métier autonome, explicitement interdite par `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`. Un LINK doit documenter des bindings, pas orchestrer des cascades conditionnelles.

**Risque** : si ce binding est interprété comme autorité sur l'orchestration, il crée une logique métier dans le LINK.

**Placement** : LINK (refactoring du binding en simple pointage) ; la logique conditionnelle doit rester dans Constitution/Référentiel.

#### F5.2 — Versioning inter-Core : couplage de version non contraint [MODÉRÉ]
**Ancrage** : `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` (Constitution), `REF_CORE_LEARNIT_CONSTITUTION_V1_9_IN_REFERENTIEL` (Référentiel), LINK header

Le système déclare des références inter-Core avec versions explicites (V1_9, V1_0). Cependant :
- aucune règle de compatibilité de version n'est déclarée : que se passe-t-il si le Référentiel est patchée vers V1_1 sans re-validation du LINK ?
- le LINK identifie dans son `id` les deux versions liées, mais aucun mécanisme ne force une re-validation du LINK lors d'un changement de version d'un Core lié
- la Constitution référence `V1_0` du Référentiel en dur : toute promotion de version du Référentiel crée une incohérence de référence dans la Constitution

**Placement** : Gouvernance pipeline (règle de re-validation LINK obligatoire sur changement de version), Constitution et Référentiel (paramètre de version de référence patchable).

#### F5.3 — Rollback de patch : chemin de restauration LINK non spécifié [FAIBLE]
**Ancrage** : `ACTION_ROLLBACK_PATCH`, `CONSTRAINT_REFERENTIEL_DOUBLE_BUFFER_REQUIRED_FOR_PATCH`

Le rollback de patch est déclaré (Constitution) et le double-buffer technique est requis (Référentiel). Mais en cas de patch qui aurait modifié un élément qui crée un nouveau binding LINK, le rollback du patch ne garantit pas la cohérence du LINK. Le LINK n'a pas de mécanisme de versioning ou de rollback propre.

**Placement** : Gouvernance pipeline (règle de cohérence LINK post-rollback).

---

### Axe 6 — Priorisation des risques

| ID | Titre | Axe | Sévérité | Core(s) |
|----|-------|-----|----------|---------|
| F1.1 | Escalades concurrentes sans ordre de priorité | Cohérence interne | **CRITIQUE** | Constitution + Référentiel |
| F3.2 | VC désactivée + AR-réfractaire + MSC divergent = blocage silencieux | États indéfinis | **CRITIQUE** | Constitution + Référentiel |
| F1.2 | Événements CONSERVATIVE_ESCALATION et SYSTEMIC_INVESTIGATION non déclarés | Cohérence interne | **ÉLEVÉ** | Référentiel |
| F1.3 | Composante T : binding LINK manquant et paramétrie absente | Cohérence interne | **ÉLEVÉ** | LINK + Référentiel |
| F3.1 | KU créative déployée dont le feedback devient indisponible en runtime | États indéfinis | **ÉLEVÉ** | Constitution |
| F4.1 | Détection misconception : dépendance IA ou humaine implicite | Dépendances IA | **ÉLEVÉ** | Constitution + Référentiel |
| F5.1 | Binding AR-N3 : frontière LINK/logique métier ambiguë | Gouvernance | **ÉLEVÉ** | LINK |
| F2.1 | Garde-fou fatigue : signal univariate insuffisant | Solidité théorique | **MODÉRÉ** | Référentiel |
| F2.2 | Forethought SRL : absence d'effet moteur non justifiée | Solidité théorique | **MODÉRÉ** | Constitution |
| F1.4 | Maîtrise provisoire : expiration sans chemin d'escalade | Cohérence interne | **MODÉRÉ** | Constitution + Référentiel |
| F4.2 | Feedback Coverage Matrix : qualité non bornée | Dépendances IA | **MODÉRÉ** | Référentiel |
| F5.2 | Versioning inter-Core : couplage sans règle de compatibilité | Gouvernance | **MODÉRÉ** | Constitution + Référentiel + LINK |
| F3.3 | ICC : concept déclaré sans chaîne causale runtime | États indéfinis | **FAIBLE** | Référentiel |
| F5.3 | Rollback : cohérence LINK post-rollback non garantie | Gouvernance | **FAIBLE** | Gouvernance pipeline |
| F2.3 | Gamification probatoire : durée et critère de sortie indéfinis | Solidité théorique | **FAIBLE** | Référentiel |

---

## Corrections à arbitrer avant patch

### Priorité CRITIQUE — arbitrage requis en premier

**[C1] — Ordre de priorité entre escalades concurrentes**
- Décider d'une table de priorité explicite entre `DIVMSC-01`, `MOT-01` et `SYST-01` quand déclenchés simultanément
- Décider si `SYST-01` absorbe les deux autres ou si les trois coexistent avec priorité ordonnée
- Recommandation : SYST-01 absorbe les deux autres (signaux redondants) ; si SYST-01 non actif, DIVMSC-01 prime sur MOT-01

**[C2] — Blocage silencieux VC+AR+MSC**
- Décider d'un chemin de détection dégradé de `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` quand AR-N1 est réfractaire
- Option : utiliser les proxys comportementaux comme source alternative de détection de "blocage perçu"
- Décider si une divergence MSC-proxy (sans AR-N1) est suffisante pour déclencher le protocole DIVMSC-01

### Priorité ÉLEVÉ — arbitrage requis avant patch

**[C3] — Déclarer les deux événements manquants**
- `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel
- `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` dans le Référentiel

**[C4] — Composante T : décider de son traitement opérationnel**
- Soit T reste uniquement constitutionnel (quoi/pourquoi) sans paramétrie référentielle → binding LINK explicitement "T non lié au Référentiel, par conception"
- Soit T reçoit un paramètre référentiel minimal (seuil de qualification T) et un binding LINK

**[C5] — KU créative sans feedback en runtime**
- Ajouter un invariant de désactivation runtime : si feedback local disparaît pour une KU créative active, le moteur bascule en hybride bloquant sur cette KU
- Définir l'action associée : `ACTION_FREEZE_CREATIVE_KU_PENDING_FEEDBACK_RESTORATION`

**[C6] — Misconception : clarifier la source de détection**
- Décider si la détection de misconception est exclusivement Design-time (annotation humaine)
- Si oui : documenter la contrainte explicitement et définir un critère de qualité minimal
- Si hybride (Design + runtime via pattern d'erreurs répétées) : définir la règle de détection runtime sans inférence sémantique

**[C7] — Refactoring du binding AR-N3**
- Séparer le binding `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` en deux bindings simples :
  - BINDING_AR_N3_TO_CALIBRATION_AXIS (Constitution → Constitution)
  - BINDING_CALIBRATION_TO_SIGNAL_REWEIGHTING (Constitution → Référentiel)
- La logique conditionnelle reste dans la règle référentielle
