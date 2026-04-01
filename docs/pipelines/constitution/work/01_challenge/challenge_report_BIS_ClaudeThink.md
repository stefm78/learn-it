# Challenge Report — BIS

**ID:** ClaudeThink  
**Stage:** STAGE_01_CHALLENGE  
**Pipeline:** constitution  
**Date:** 2026-04-01  
**Cores challengés :** Constitution V1.9 · Référentiel V1.0 · LINK V1.9__V1.0  
**Note de focalisation :** aucune (challenge général)

---

## Résumé exécutif

Le système Constitution/Référentiel/LINK est structurellement bien formé et présente une séparation des couches claire. La gouvernance patch est particulièrement robuste. Cependant, l'audit révèle **sept zones de risque non triviales**, dont deux critiques :

1. **Critique — Paramètre fantôme** : `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` référence `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` qui n'existe dans aucun des trois cores (ni Constitution, ni Référentiel, ni LINK).
2. **Critique — Binding LINK manquant** : `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` et `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` sont datés `[ARBITRAGE_2026_04_01]` (aujourd'hui) et **ne sont pas encore bindés** dans le LINK_CORE alors que le LINK a été clôturé avant cet ajout.
3. **Élevé — Zone d'état indéfini** : le protocole de divergence MSC/perçu enchaîne deux étapes mais **ne définit pas la condition d'arrêt** entre l'étape 1 (diagnostique) et l'étape 2 (escalade) — un moteur déterministe ne peut pas trancher seul.
4. **Élevé — Conflit de règle** : `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (datée `[ARBITRAGE_2026_04_01][MATRIX-01]`) ajoute un **régime oscillatoire** Consolidation↔Exploration non décrit dans le Référentiel d'origine ; le TYPE sous-jacent (`TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX`) n'a aucun paramètre pour la durée d'oscillation.
5. **Modéré — Angle mort SRL forethought** : la Constitution capture l'intention de session (AR-N2 + `RULE_SESSION_INTENTION_NON_BLOCKING`) mais ne définit jamais ce que le moteur fait concrètement de ce signal — usage déclaré « informatif » sans aucune règle de traitement.
6. **Modéré — Dépendance IA implicite résiduelle** : `ACTION_INFORM_LEARNER` est déclenchée sur « changement visible » et exige une rédaction explicative — le contenu de la notification n'est ni préindexé ni défini, ce qui exige une génération sémantique à la volée.
7. **Faible — Paramètre orphelin** : `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_WINDOW` est mentionné en texte dans `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` (« fenêtre configurée ») mais n'est déclaré nulle part dans les blocs PARAMETERS du Référentiel.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### 1.1 Paramètre fantôme : `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

- **Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` [Constitution, `source_anchor: [ARBITRAGE_2026_04_01][DIVMSC-01]`]
- **Nature :** Le champ `depends_on` de l'événement et sa description textuelle (`human_readable`) citent explicitement `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` comme seuil de détection de la divergence. Ce paramètre est **absent du Référentiel V1.0** (aucun `id` correspondant dans la liste PARAMETERS).
- **Type de problème :** complétude / gouvernance
- **Impact moteur :** Le moteur ne peut pas évaluer la condition de déclenchement de la divergence. La règle `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` reste inopérable.
- **Correction à arbitrer :** Ajouter `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel avec ses bornes (nombre de sessions consécutives). Mettre à jour le LINK pour binder cet événement et ce paramètre.

#### 1.2 Binding LINK absent pour les éléments `[ARBITRAGE_2026_04_01]`

- **Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` + `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` (Constitution) et `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (Référentiel)
- **Nature :** Ces trois éléments portent tous `source_anchor: [ARBITRAGE_2026_04_01]` et ont été ajoutés **après** la clôture du LINK (dont le dernier binding daté est `[ARBITRAGE_2026_04_01][AR3-01][SIG-01]`, soit le même arbitrage mais un groupe différent). Aucun `TYPE_BINDING_*` dans le LINK ne couvre la chaîne MSC-divergence ni la table de conflit de régime.
- **Type de problème :** gouvernance / complétude
- **Impact moteur :** La fédération inter-Core est incomplète. Un audit de cohérence automatique (LINK) signalerait des éléments flottants sans binding.
- **Correction à arbitrer :** Ajouter deux nouveaux bindings dans le LINK : un pour la chaîne `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED → RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL → PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`, et un pour `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION → TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX`.

#### 1.3 Paramètre orphelin de l'investigation systémique

- **Élément concerné :** `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` [Référentiel, `source_anchor: [PATCH_V1_0]`]
- **Nature :** La règle mentionne « escalade hors session si persistance sur la fenêtre configurée » mais aucun `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_*` n'est déclaré dans les PARAMETERS.
- **Type de problème :** complétude
- **Impact moteur :** Le moteur ne peut pas vérifier la fenêtre de persistance d'investigation de façon déterministe.
- **Correction à arbitrer :** Déclarer explicitement le paramètre de fenêtre dans le Référentiel (nombre de sessions), avec borne et valeur de référence.

---

### Axe 2 — Solidité théorique

#### 2.1 Charge cognitive

- **Point solide :** La Constitution limite explicitement les sondages AR (budget d'interaction déclaré pour N1, N2, N3 — `PARAM_AR_N*_INTERACTION_BUDGET`), ce qui est aligné sur les principes de faible charge extrinsèque.
- **Zone de risque :** Le calibrage initial peut atteindre 15 KU (`PARAM_REFERENTIEL_CALIBRATION_UNITS_MAX`, borne haute). Pour des KU procédurales (1–5 min chacune), cela représente jusqu'à 75 minutes de diagnostic — charge cognitive élevée pour un démarrage.
- **Angle mort :** Aucune règle ne segmente le calibrage initial sur plusieurs sessions si le budget cognitif est dépassé.

#### 2.2 Mémoire / consolidation

- **Point solide :** Le système R avec multiplicateurs par type KU (déclaratif, procédural, perceptuel) est théoriquement bien fondé — aligné sur la théorie de l'oubli différentiel.
- **Zone de risque :** La révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) exige « une fenêtre temporelle et des répétitions configurées » mais ces paramètres ne sont pas tous déclarés explicitement (seul `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` est visible).
- **Angle mort :** La durée de la fenêtre post-maîtrise pour la révocation n'est pas paramétrée distinctement de R — risque de confusion entre R et la fenêtre de révocation.

#### 2.3 Motivation

- **Point solide :** La distinction explicite VC ≠ motivation générale (`INV_VC_NOT_GENERAL_MOTIVATION_PROXY`) évite les sur-inférences. La règle de relevance patch pour VC basse persistante est correctement ciblée.
- **Zone de risque :** En l'absence de VC (axe unknown), la Constitution ne spécifie aucun signal de substitution motivationnel — le moteur est aveugle à la motivation tant que VC n'est pas renseignée.
- **Angle mort :** Les théories SDT (autonomie, compétence, appartenance) ne sont pas représentées. Seule la dimension valeur/coût est capturée, sans levier de sentiment de compétence ou d'autonomie.

#### 2.4 Métacognition / SRL

- **Point solide :** AR-N3 capture un bilan périodique et alimente l'axe calibration — cohérent avec le cycle SRL de Zimmerman (auto-évaluation).
- **Zone de risque :** L'intention de session (forethought SRL) est collectée mais le moteur n'a **aucune règle opérationnelle** pour en faire usage (`RULE_SESSION_INTENTION_NON_BLOCKING` la déclare uniquement « informative »). La phase forethought reste orpheline.
- **Angle mort :** Aucune boucle de performance review structurée côté apprenant (pas de feedback récapitulatif de session visible dans les règles).

#### 2.5 Émotions / engagement

- **Point solide :** AR-N1 distingue confusion/frustration/anxiété — aligné sur AEQ (Achievement Emotions Questionnaire) sur lequel AR-N3 est également basé.
- **Zone de risque :** La réponse à la **détresse** (anxiété/frustration persistante) est couverte uniquement par le régime conservateur (scaffolding léger). Il n'existe pas de protocole d'escalade émotionnelle vers un acteur humain si la détresse persiste.
- **Angle mort :** Le régime « Détresse » est priorisé dans la matrice de conflit (`RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`) mais sa durée maximale avant escalade hors moteur n'est pas bornée.

#### 2.6 Mastery learning

- **Point solide :** L'agrégation AND stricte (P∧R∧A) est bien alignée sur le mastery learning de Bloom — pas de déclaration de maîtrise sur précision seule.
- **Zone de risque :** Le composant T (transférabilité) est correctement séparé, mais il n'existe aucune règle définissant comment T est évalué localement sans génération de contenu (contrainte `INV_NO_RUNTIME_CONTENT_GENERATION`).
- **Angle mort :** Les KU créatives ont un fallback R=×1 figé (invariant), mais aucune alternative d'évaluation de A pour ce type de KU n'est décrite — comment observer « réussite autonome » sur une KU créative sans génération ?

#### 2.7 Ingénierie pédagogique

- **Point solide :** Le typage KU (déclaratif/formel/procédural/perceptuel/créatif) et l'invariant multimodal (`INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL`) sont solides.
- **Zone de risque :** Le contexte authentique (`TYPE_AUTHENTIC_CONTEXT`) est obligatoire pour Bloom ≥ 4 mais n'est défini que qualitativement. Aucun critère opérationnel ne permet au moteur de vérifier si un contexte déclaré est suffisamment « authentique ».
- **Angle mort :** La phase ADDIE n'est pas représentée de bout en bout ; la phase Évaluation formative est absente du cycle governance.

---

### Axe 3 — États indéfinis moteur

#### 3.1 Indéfini dans le protocole de divergence MSC/perçu

- **Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`
- **Description :** La règle décrit deux étapes (diagnostique → escalade si persistance). Mais : (a) la condition de passage à l'étape 2 est « si divergence persiste après diagnostique » sans définir combien de sessions diagnostiques constituent une persistance ; (b) si l'escalade est déclenchée **et que l'acteur externe ne répond pas**, le moteur est dans un état indéfini — aucune règle de fallback n'est décrite.
- **Risque :** Oscillation sur l'étape 1 sans sortie déterministe.

#### 3.2 Indéfini dans le régime oscillatoire Consolidation↔Exploration

- **Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel]
- **Description :** Le régime oscillatoire est défini comme « alternance 1 session consolidation → 1 session exploration → retour consolidation, sortie quand R atteint ». Mais : (a) si R n'est jamais atteint pendant l'oscillation, aucune condition d'arrêt n'est déclarée ; (b) si AR-N1 signale détresse pendant une session exploration dans ce régime, la priorité détresse prime — mais le moteur doit-il réinitialiser le compteur d'oscillation ?
- **Risque :** Blocage en oscillation infinie ou conflit de priorité non résolu.

#### 3.3 Indéfini sur la KU sans type à la frontière

- **Élément concerné :** `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK` + `INV_KU_TYPING_REQUIRED`
- **Description :** Une KU sans type déclenche un mode sécurité (feedback générique, pas d'adaptation fine). Mais si la **majorité** des KU d'une session sont non typées, le moteur tourne en mode dégradé complet — aucune règle ne définit un seuil d'alerte ou de blocage de session.
- **Risque :** Session fonctionnellement vide sans signal d'erreur visible.

---

### Axe 4 — Dépendances IA implicites

#### 4.1 `ACTION_INFORM_LEARNER` — contenu de notification non défini

- **Élément concerné :** `ACTION_INFORM_LEARNER` [Constitution, `[S14]`]
- **Description :** L'action est déclenchée sur « patch, rejet ou changement visible » avec effet « notification explicite ». Le contenu de la notification n'est ni préindexé ni balisé — une implémentation déterministe locale exige des templates de notification préexistants.
- **Alternative locale :** Déclarer une table de templates de notification par type d'événement (patch appliqué, patch rejeté, rétrogradation MSC, reprise diagnostique) dans les artefacts de conception.

#### 4.2 Évaluation du contexte authentique

- **Élément concerné :** `TYPE_AUTHENTIC_CONTEXT` + `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4`
- **Description :** Le moteur doit vérifier si un contexte authentique est présent. Cette vérification est structurelle (booléen déclaré en Analyse), mais la **qualité** du contexte authentique (est-il réellement authentique ?) requiert un jugement sémantique hors moteur. Risque de validation formelle d'un contexte creux.
- **Alternative locale :** Checklist de validation du contexte authentique en phase Analyse, complétée par un acteur humain hors session, avec flag booléen auditée.

#### 4.3 Classification des proxys comportementaux

- **Élément concerné :** `TYPE_REFERENTIEL_MINIMAL_BEHAVIORAL_PROXY_SET` [Référentiel]
- **Description :** Les proxys sont listés avec « statut empirique explicite » mais leur seuil de franchissement est déclaré paramétrable. En l'absence de données empiriques pour un déploiement donné, la calibration des seuils proxy requiert une analyse statistique légère — ce qui présuppose un outillage analytique hors session pas décrit dans le pipeline.
- **Alternative locale :** Déclaration explicite des seuils proxy par défaut dans le Référentiel avec annotation « à calibrer localement avant déploiement ».

---

### Axe 5 — Gouvernance

#### 5.1 Versioning des éléments `[ARBITRAGE_2026_04_01]`

- **Élément concerné :** Trois éléments portent ce source_anchor dans Constitution (×2) et Référentiel (×1), sans équivalent dans le LINK.
- **Nature :** Ces éléments ont été ajoutés lors d'un arbitrage en cours de run. Le LINK n'a pas été mis à jour de façon synchrone. Le manifest de version (si existant) doit être vérifié pour cohérence.
- **Type de problème :** gouvernance
- **Correction :** Synchroniser le LINK avec les éléments de l'arbitrage du 2026-04-01.

#### 5.2 Invariant `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` — vérification non décrite dans le pipeline

- **Élément concerné :** `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` [Constitution, `[PATCH_V1_9]`]
- **Nature :** L'invariant déclare que tout cycle de dépendance bloque le déploiement, mais aucune étape du pipeline (STAGE_01 à STAGE_09) ne décrit une validation d'acyclicité du graphe. La vérification repose sur un outillage externe non documenté.
- **Type de problème :** gouvernance / implémentabilité
- **Correction :** Documenter l'outillage de détection de cycles dans le pipeline (validation en Analyse/Design, pas en runtime).

#### 5.3 Séparation Constitution/Référentiel partiellement fragilisée

- **Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel]
- **Nature :** Cette règle introduit une logique de résolution de conflits complexe avec un régime oscillatoire. Elle dépasse le rôle du Référentiel (« borne le combien/comment ») et empiète sur le « quoi » (architecture adaptative des régimes). La Constitution déclare les régimes (`TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` est dans le Référentiel, mais la politique de conflit entre régimes constitue une décision d'architecture adaptative).
- **Type de problème :** gouvernance / mauvais placement
- **Correction à arbitrer :** Évaluer si la table de priorité des conflits de régimes doit migrer vers la Constitution (comme politique de gouvernance adaptative) en laissant au Référentiel uniquement les bornes numériques.

---

### Axe 6 — Scénarios adversariaux

#### Scénario A — « Le bon élève invisible »

**Description :** Un apprenant obtient MSC P∧R∧A validés sur 5 KU, mais répond systématiquement « blocage total » à AR-N1 après chaque session. AR-N1 prime sur les proxys (`RULE_AR_N1_OVERRIDES_PROXY`). La divergence MSC/perçu est détectée après N sessions (`EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`).

**Mécanismes activés :** `INV_MSC_AND_STRICT` + `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` + `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`

**Limite révélée :** La condition de fin de la phase diagnostique n'est pas définie (cf. Axe 3.1). Si l'apprenant continue de répondre « blocage » même pendant la phase diagnostique (bonnes performances objectives mais persistance de l'AR-N1 négatif), le moteur oscille entre étape 1 et étape 2 sans critère d'arrêt déterministe. **`PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` est absent du Référentiel** — la condition de déclenchement elle-même est indéterminable.

#### Scénario B — « La session de reprise en territoire mixte »

**Description :** Un apprenant reprend après 10 jours d'interruption (> seuil R). Il a des KU en état Consolidation et d'autres en Exploration. Le moteur déclenche une reprise diagnostique (`RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`). Pendant la reprise, les performances sont mixtes : certaines KU échouent, déclenchant une rétrogradation MSC et marquage des dépendantes. Simultanément, le régime global est détecté comme Consolidation+Exploration (conflit de frontière).

**Mécanismes activés :** `EVENT_LONG_INTERRUPTION` + `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` + `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` + `INV_SECONDARY_RETROGRADATION_IS_NEW_EVENT`

**Limite révélée :** La rétrogradation secondaire est un « nouvel événement autonome » — mais pendant une session de reprise diagnostique, plusieurs rétrogradations secondaires peuvent s'empiler. La règle de conflit de régime s'applique-t-elle à chaque rétrogradation indépendamment ou à la session globale ? Aucune règle ne le précise. Risque de plans de session incohérents (diagnostique de reprise + régime oscillatoire simultanément).

#### Scénario C — « La gamification probatoire en détresse »

**Description :** Un déploiement active un mécanisme de gamification en mode probatoire (`RULE_UNVERIFIED_GAMIFICATION_PROBATION`). Un apprenant entre en régime Détresse (AR-N1 persistant) pendant la période probatoire. La Constitution priorise la Détresse dans la matrice de conflit (`RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` : « Détresse l'emporte toujours »). Le mode probatoire implique que la gamification continue d'être active.

**Mécanismes activés :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` + `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` + `TYPE_STATE_AXIS_ACTIVATION` (détresse)

**Limite révélée :** La règle du mode probatoire ne spécifie pas de suspension automatique de la gamification en cas de Détresse — il est possible que la gamification aggrave la détresse pendant la période d'observation. Aucune contrainte d'interaction entre probation et Détresse n'est déclarée. La détresse « prime » sur les régimes adaptatifs mais pas sur le mode de déploiement probatoire.

---

### Axe 7 — Priorisation des risques

| # | Risque | Couche | Type | Priorité |
|---|--------|--------|------|----------|
| R1 | `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` absent | Référentiel | Complétude | **Critique** |
| R2 | Bindings LINK manquants pour éléments `[ARBITRAGE_2026_04_01]` | LINK | Gouvernance | **Critique** |
| R3 | Condition d'arrêt indéfinie dans le protocole divergence MSC/perçu | Constitution | Implémentabilité | **Élevé** |
| R4 | Régime oscillatoire sans condition d'arrêt ni reset sur détresse | Référentiel | Implémentabilité | **Élevé** |
| R5 | Intention de session (forethought SRL) sans règle de traitement | Constitution | Complétude/Théorique | **Modéré** |
| R6 | `ACTION_INFORM_LEARNER` sans templates de notification préindexés | Constitution | Implémentabilité/IA implicite | **Modéré** |
| R7 | Paramètre orphelin `SYSTEMIC_INVESTIGATION_WINDOW` | Référentiel | Complétude | **Faible** |

---

## Corrections à arbitrer avant patch

### C1 — Ajouter `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` [Critique]

- **Élément concerné :** Référentiel PARAMETERS
- **Nature :** Paramètre manquant référencé explicitement dans la Constitution
- **Type :** Complétude
- **Impact moteur :** Règle `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` et événement `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` inopérables sans ce paramètre
- **Correction :** Ajouter dans le Référentiel : `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` avec valeur de référence (ex. 3 sessions), fourchette (2–5), lié à `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`

### C2 — Ajouter deux bindings LINK post-arbitrage 2026-04-01 [Critique]

- **Élément concerné :** LINK_CORE — section TYPES
- **Nature :** Bindings inter-Core absents pour les éléments de l'arbitrage du jour
- **Type :** Gouvernance
- **Impact moteur :** Fédération incomplète, cohérence inter-Core non garantie
- **Correction :** Ajouter dans le LINK : (a) `TYPE_BINDING_MSC_DIVERGENCE_PROTOCOL_CHAIN` bindant Constitution→Référentiel sur la chaîne divergence ; (b) `TYPE_BINDING_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` bindant Référentiel→Constitution sur la table de conflit des régimes

### C3 — Préciser les conditions d'arrêt du protocole divergence [Élevé]

- **Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` (Constitution)
- **Nature :** État indéfini — critère de passage étape 1→étape 2 absent
- **Type :** Implémentabilité
- **Impact moteur :** Oscillation possible sans sortie déterministe
- **Correction :** Paramétrer le nombre de cycles diagnostiques avant escalade (référencer `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` ou ajouter un second paramètre dédié). Déclarer un fallback si l'escalade externe reste sans réponse.

### C4 — Borner le régime oscillatoire Consolidation↔Exploration [Élevé]

- **Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (Référentiel)
- **Nature :** Oscillation sans condition d'arrêt temporelle et sans règle de reset sur détresse
- **Type :** Implémentabilité
- **Impact moteur :** Blocage en oscillation infinie sur KU à R difficile à atteindre
- **Correction :** Ajouter un paramètre de nombre maximal de cycles d'oscillation avant escalade en mode Conservateur. Clarifier le comportement si détresse survient pendant un cycle Exploration (reset du compteur ? suspension de l'oscillation ?)

### C5 — Déclarer les templates de notification pour `ACTION_INFORM_LEARNER` [Modéré]

- **Élément concerné :** `ACTION_INFORM_LEARNER` (Constitution) + artefacts de conception
- **Nature :** Dépendance IA implicite dans la rédaction des notifications
- **Type :** Implémentabilité
- **Impact moteur :** Notifications impossibles sans génération sémantique à la volée (violant `INV_NO_RUNTIME_CONTENT_GENERATION`)
- **Correction :** Créer une table de templates de notification préindexés par type d'événement (livrables de design hors session)

### C6 — Déclarer `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_WINDOW` [Faible]

- **Élément concerné :** `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` (Référentiel)
- **Nature :** Paramètre orphelin
- **Type :** Complétude
- **Impact moteur :** Fenêtre de persistance indéterminable pour l'investigation systémique
- **Correction :** Déclarer le paramètre dans le Référentiel avec valeur de référence et fourchette

---

*Rapport produit par ID=ClaudeThink dans le cadre du STAGE_01_CHALLENGE — pipeline constitution.*
