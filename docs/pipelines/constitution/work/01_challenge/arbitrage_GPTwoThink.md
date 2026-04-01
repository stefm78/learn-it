# ARBITRAGE — Constitution Pipeline STAGE_02
## Metadata
- pipeline: constitution
- stage: STAGE_02_ARBITRAGE
- arbitre: GPTwoThink
- date: 2026-04-01
- challenges_analysés:
  - challenge_report_01_ClaudeThink.md
  - challenge_report_01_ClaudeWoThink.md
  - challenge_NemoTron.md
  - challenge_report_GPTwoThink.md

---

## Résumé exécutif

L'arbitrage consolide **52 constats bruts** issus de 4 rapports de challenge en **25 points distincts**, après fusion des redondances (18 groupes fusionnés). 

Bilan des décisions :
- **`corriger_maintenant` : 14 points** — tous portent sur des états moteur indéfinis, des bindings inter-Core manquants ou des risques de blocage silencieux avérés.
- **`reporter` : 6 points** — améliorations théoriques ou éditoriales sans impact moteur immédiat.
- **`rejeter` : 2 points** — absences volontaires ou non-problèmes structurels.
- **`hors_perimetre` : 3 points** — nécessitent une décision de gouvernance humaine préalable ou sont liés à des absences d'input (LINK non fourni dans un rapport, arbitrage précédent non matérialisé).

---

## Périmètre analysé

### Fichiers de challenge considérés
- `challenge_report_01_ClaudeThink.md` (ClaudeThink — 15 constats, 2 critiques)
- `challenge_report_01_ClaudeWoThink.md` (ClaudeWoThink — 11 constats, 2 critiques)
- `challenge_NemoTron.md` (NemoTron — 11 constats, 1 critique)
- `challenge_report_GPTwoThink.md` (GPTwoThink — 18 constats, 2 critiques)

### Notes humaines d'arbitrage
Aucune note humaine supplémentaire fournie pour ce run.

### Limites de périmètre
- Le LINK (`link.yaml`) n'était pas disponible pour ClaudeWoThink. Les constats CRIT-01/CRIT-02 de ce rapport sont traités en `hors_perimetre` pour la partie vérification, mais les corrections LINK prescrites par les autres challengers sont retenues.
- L'arbitrage `[ARBITRAGE_2026_04_01]` n'est pas matérialisé dans `work/02_arbitrage/` — ce point est traité en `hors_perimetre` (traçabilité rétroactive, sans impact moteur).
- Le présent arbitrage porte uniquement sur les éléments adressables par un patch YAML aux Cores. Les décisions de gouvernance organisationnelle (canal d'escalade humaine, process de review inter-Core) sont signalées mais placées hors périmètre patch.

---

## Arbitrage détaillé

---

### Point A — Binding LINK manquant : `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

- **Source(s) :** NemoTron AX1-01 (CRITIQUE), ClaudeWoThink A1-3 (MODÉRÉ), GPTwoThink 1.4 (ÉLEVÉ)
- **Constat synthétique :** Le seuil de déclenchement de `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` est référencé dans la Constitution mais aucun `TYPE_BINDING` dans le LINK ne matérialise la résolution formelle vers `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`. La dépendance est déclarative, pas structurelle. NemoTron classe cela CRITIQUE (violation de `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`), ClaudeWoThink MODÉRÉ (dépendance non structurelle), GPTwoThink ÉLEVÉ.
- **Nature :** structurelle — binding inter-Core manquant
- **Gravité :** critique (arbitrage : convergence NemoTron + GPTwoThink sur l'impact moteur)
- **Impact :** applicabilité, sécurité logique — évaluation du trigger non déterministe sans binding explicite
- **Décision :** `corriger_maintenant`
- **Justification :** Trois rapports convergent. Le moteur ne peut pas résoudre le seuil de façon déterministe. Correction minimale : ajouter un `TYPE_BINDING` dans le LINK pointant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` vers `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`. La correction ClaudeWoThink de formaliser un `depends_on` dans l'EVENT peut être incluse en complément.
- **Conséquence pour le patch :** Patch LINK — ajout d'un binding `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` ; patch Constitution optionnel — ajout d'un `depends_on` formel dans l'EVENT.

---

### Point B — Composante T : opérationnellement orpheline (pas de déclencheur, pas de binding LINK, pas d'EVENT `T_never_evaluated`)

- **Source(s) :** NemoTron AX1-02 (ÉLEVÉ), ClaudeThink F1.3 (ÉLEVÉ), ClaudeWoThink A4-2 (FAIBLE), GPTwoThink 1.1 (ÉLEVÉ)
- **Constat synthétique :** La composante T est constitutionnellement séparée de la maîtrise de base, mais : (a) `TYPE_MASTERY_MODEL` ne déclare aucune relation vers `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` (GPTwoThink), (b) aucun EVENT ne couvre le cas où T n'est jamais évalué après N sessions post-maîtrise de base (NemoTron), (c) aucun binding LINK n'explicite comment T est consommée dans la chaîne décisionnelle (ClaudeThink), (d) aucun paramètre référentiel de seuil T n'existe (ClaudeThink).
- **Nature :** structurelle + gouvernance — relation de graphe manquante, EVENT manquant, binding LINK manquant
- **Gravité :** élevée
- **Impact :** maintenabilité, applicabilité — dérive silencieuse possible si T n'est jamais planifiée
- **Décision :** `corriger_maintenant` (partiel — voir justification)
- **Justification :** Deux corrections minimales sont retenues : (1) ajouter la relation `governs → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` depuis `TYPE_MASTERY_MODEL` dans la Constitution (correction de traversabilité graphe — coût nul, impact élevé) ; (2) ajouter un EVENT `EVENT_T_EVALUATION_OVERDUE` dans la Constitution avec une RULE de signalement. Le binding LINK complet et la paramétrie T dans le Référentiel sont reportés (voir Point B-suite) car ils requièrent des décisions de conception plus larges (nature de l'évaluation T, contexte de transfert).
- **Conséquence pour le patch :** Patch Constitution — ajout relation `TYPE_MASTERY_MODEL → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` + EVENT `EVENT_T_EVALUATION_OVERDUE` + RULE de déclenchement conditionnelle paramétrisée vers le Référentiel.

---

### Point B-suite — Binding LINK T et paramétrie Référentiel T

- **Source(s) :** ClaudeThink F1.3 (ÉLEVÉ)
- **Constat synthétique :** Paramétrie T manquante dans le Référentiel (seuil de qualification, multiplicateur R adapté, Bloom minimal imposé).
- **Nature :** gouvernance — décision de conception requise avant patch
- **Gravité :** élevée
- **Impact :** applicabilité — ne peut être patchée sans décision de conception sur la nature opérationnelle de T
- **Décision :** `reporter`
- **Justification :** Cette correction nécessite une décision explicite sur ce que T évalue opérationnellement (contexte de transfert, format, seuil). Reporter à un run de pipeline dédié à T.

---

### Point C — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` et `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` : événements référencés mais non déclarés

- **Source(s) :** ClaudeThink F1.2 (ÉLEVÉ), ClaudeWoThink HIGH-01 + A3-1 (ÉLEVÉ)
- **Constat synthétique :** Deux événements sont nommés dans les `human_readable` de paramètres référentiels (`PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`) mais ne sont déclarés dans aucun bloc `EVENTS`. Le paramètre de scaffolding borde un seuil d'escalade vers un event inexistant → puits sans sortie formalisée.
- **Nature :** logique — dépendances implicites non déclarées
- **Gravité :** élevée
- **Impact :** sécurité logique — l'apprenant peut rester indéfiniment en mode conservateur sans sortie déclarée
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale et additive : déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` et `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` dans le Référentiel avec leurs conditions d'entrée et actions associées (escalade hors-session). Pas de refonte requise.
- **Conséquence pour le patch :** Patch Référentiel — ajout de deux blocs EVENT avec conditions et actions minimalistes.

---

### Point D — Régime oscillatoire `Consolidation + Exploration` : absence de borne de durée et de sortie de secours

- **Source(s) :** ClaudeWoThink A1-4 + A3-2 (ÉLEVÉ), ClaudeWoThink HIGH-02
- **Constat synthétique :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` décrit un régime oscillatoire avec condition de sortie `R atteint`, sans borne maximale de cycles ni sortie de secours si R n'est jamais atteint.
- **Nature :** logique — état moteur potentiellement infini
- **Gravité :** élevée
- **Impact :** sécurité logique — oscillation sans fin bloquant la progression
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` (borne paramétrable) et une condition de sortie de secours dans la RULE (retour en mode conservateur après N cycles si R non atteint).
- **Conséquence pour le patch :** Patch Référentiel — ajout d'un paramètre + mise à jour de la RULE avec condition de sortie de secours.

---

### Point E — Maîtrise provisoire : expiration de fenêtre sans EVENT ni chemin de traitement

- **Source(s) :** ClaudeThink F1.4 (MODÉRÉ), ClaudeWoThink A3-3 + HIGH-03 (ÉLEVÉ), ClaudeWoThink A2-1 (MODÉRÉ)
- **Constat synthétique :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est déclaré dans la Constitution (patchable) mais : (a) aucun EVENT d'expiration n'est déclaré, (b) le comportement moteur post-expiration sans confirmation est indéfini (révoquer ? escalader ? geler ?), (c) aucun paramètre numérique référentiel ne fixe la valeur opérationnelle de la fenêtre.
- **Nature :** logique + structurelle — état moteur indéfini à l'expiration
- **Gravité :** élevée (ClaudeWoThink HIGH-03) / modérée (ClaudeThink)
- **Impact :** sécurité logique, maintenabilité
- **Décision :** `corriger_maintenant` (partiel)
- **Justification :** (1) Déclarer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` dans la Constitution avec action d'escalade diagnostique. (2) Déclarer le paramètre numérique de durée de fenêtre dans le Référentiel. La sémantique de l'expiration (révocation vs escalade diagnostique) est arbitrée en faveur de l'escalade diagnostique — aligné avec `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` et le principe de conservation.
- **Conséquence pour le patch :** Patch Constitution — EVENT + action ; Patch Référentiel — paramètre numérique de durée.

---

### Point F — Ordre de priorité entre escalades concurrentes (DIVMSC-01 / MOT-01 / SYST-01)

- **Source(s) :** ClaudeThink F1.1 (CRITIQUE)
- **Constat synthétique :** Trois mécanismes d'escalade hors-session peuvent se déclencher simultanément sans table de priorité explicite. `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` s'applique en fallback générique, inadapté aux escalades pédagogiques critiques.
- **Nature :** logique — ordre d'exécution non déterministe sous concurrence
- **Gravité :** critique
- **Impact :** sécurité logique, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Décision d'arbitrage : SYST-01 absorbe les deux autres si actif (signaux redondants) ; si SYST-01 inactif, DIVMSC-01 prime sur MOT-01. Cette table de priorité doit être déclarée dans la Constitution comme règle de résolution de conflits d'escalade, minimale et additive. Pas de refonte des trois mécanismes.
- **Conséquence pour le patch :** Patch Constitution — ajout d'une RULE `RULE_ESCALATION_PRIORITY_ORDER` déclarant la table de priorité SYST-01 > DIVMSC-01 > MOT-01.

---

### Point G — Blocage silencieux : VC désactivée + AR-réfractaire + MSC divergent

- **Source(s) :** ClaudeThink F3.2 (CRITIQUE)
- **Constat synthétique :** En combinaison VC désactivée + AR-réfractaire + divergence MSC, le moteur n'a plus de signal auto-rapport exploitable et `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` ne peut pas se déclencher correctement (dépend d'AR-N1 pour détecter le blocage perçu). L'apprenant est en difficulté sans que le moteur le détecte.
- **Nature :** logique — état composite non couvert
- **Gravité :** critique
- **Impact :** sécurité logique — blocage silencieux indéfini
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter une RULE de détection dégradée dans la Constitution qui autorise les proxys comportementaux comme source alternative de détection de divergence MSC quand AR-N1 est réfractaire et VC désactivée. La divergence MSC-proxy (sans AR-N1) est déclarée suffisante pour déclencher une version allégée du protocole DIVMSC-01 (escalade directe sans diagnostique préalable, puisque les signaux directs sont épuisés).
- **Conséquence pour le patch :** Patch Constitution — ajout d'une règle de détection dégradée + condition alternative de déclenchement de DIVMSC-01.

---

### Point H — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ne couvre pas les mises à jour incrémentielles

- **Source(s) :** GPTwoThink F-1.2 (CRITIQUE)
- **Constat synthétique :** Le trigger de l'invariant couvre uniquement la construction initiale ou le chargement. Un patch sur le graphe peut réintroduire un cycle sans déclencher l'invariant.
- **Nature :** structurelle — couverture incomplète de l'invariant
- **Gravité :** critique
- **Impact :** sécurité logique — cycle possible post-patch sans blocage moteur
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : étendre le champ `trigger` de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` pour inclure `validation_post_patch_graphe` en plus de `validation_design` et `chargement_graphe`. Non-patchable sur le fond (invariant protégé), mais le trigger est un attribut de l'invariant — à clarifier avec le DSL patch si la modification d'un invariant non-patchable est autorisée sur ses métadonnées.
- **Conséquence pour le patch :** Patch Constitution — extension du `trigger` de l'invariant. Si le DSL interdit la modification d'un invariant non-patchable, ajouter un invariant complémentaire `INV_KNOWLEDGE_GRAPH_ACYCLICITY_PRESERVED_ON_PATCH` dans la Constitution.

---

### Point I — Délégation sans fallback constitutionnel si le Référentiel est absent ou malformé

- **Source(s) :** GPTwoThink F-1.3 (CRITIQUE)
- **Constat synthétique :** Plusieurs règles et événements conditionnels (`RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) ne s'activent que sur seuil Référentiel, mais aucun invariant constitutionnel ne définit le comportement si le Référentiel est absent, incompatible ou si le paramètre est manquant.
- **Nature :** structurelle — précondition de déploiement non déclarée
- **Gravité :** critique
- **Impact :** sécurité logique — moteur peut osciller indéfiniment sur trigger non évaluable
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter un invariant constitutionnel `INV_REFERENTIEL_PARAMETERS_MUST_BE_RESOLVABLE_BEFORE_ACTIVATION` déclarant que tous les paramètres Référentiel requis par les règles et événements de la Constitution doivent être résolvables avant l'activation du moteur. En l'absence de résolution, le moteur bascule en mode conservateur global (aligné avec `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`).
- **Conséquence pour le patch :** Patch Constitution — ajout d'un invariant de précondition de déploiement.

---

### Point J — Mode probatoire gamification : absence de condition de sortie et de durée bornée

- **Source(s) :** NemoTron AX1-03 (MODÉRÉ), ClaudeThink F2.3 (FAIBLE), ClaudeWoThink A2-3 (indirectement)
- **Constat synthétique :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` (Constitution + Référentiel) est ouverte à gauche (entrée possible) sans sortie déterministe. Ni durée maximale, ni critère de validation, ni escalade en cas de non-résolution.
- **Nature :** logique — règle incomplète
- **Gravité :** modérée
- **Impact :** maintenabilité — mode probatoire permanent théoriquement possible
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS` et un EVENT de sortie du mode probatoire dans le Référentiel (validation par absence d'effet négatif observable sur N sessions, ou escalade si non-résolution).
- **Conséquence pour le patch :** Patch Référentiel — paramètre + EVENT de sortie probatoire.

---

### Point K — `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` : canal d'escalade indéfini

- **Source(s) :** NemoTron AX1-04 (MODÉRÉ)
- **Constat synthétique :** L'invariant déclare une escalade obligatoire mais ne précise ni la cible, ni le format, ni le canal. Inopérant en runtime.
- **Nature :** éditoriale + logique — invariant incomplet
- **Gravité :** modérée
- **Impact :** applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter une ACTION associée à l'invariant définissant l'effet concret de l'escalade (`ACTION_LOG_ESCALATION_BLOCKED_DRIFT` ou référence à une action existante), sans définir le canal humain (hors périmètre patch).
- **Conséquence pour le patch :** Patch Constitution — ajout d'une ACTION ou référence d'action dans l'invariant.

---

### Point L — `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` : absence de binding LINK miroir de protection

- **Source(s) :** NemoTron AX1-05 (MODÉRÉ)
- **Constat synthétique :** La règle constitutionnelle interdit la complétion implicite des axes, mais le LINK ne porte pas de binding ou CONSTRAINT protégeant cette interdiction côté Référentiel.
- **Nature :** structurelle — protection non propagée dans le système fédéré
- **Gravité :** modérée
- **Impact :** maintenabilité — Référentiel futur peut contourner implicitement la règle
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter un `CONSTRAINT` dans le LINK interdisant explicitement aux Référentiels liés de définir un mécanisme de complétion implicite des axes d'état.
- **Conséquence pour le patch :** Patch LINK — ajout de CONSTRAINT.

---

### Point M — Versioning inter-Core : aucune règle de re-validation LINK sur changement de version

- **Source(s) :** NemoTron AX5-01 (MODÉRÉ), ClaudeThink F5.2 (MODÉRÉ), GPTwoThink F-5.3 (ÉLEVÉ)
- **Constat synthétique :** Trois rapports convergent : la Constitution référence `V1_0` du Référentiel en dur (patchable: false), mais aucun mécanisme ne force une re-validation du LINK lors d'un changement de version d'un Core lié. Toute promotion du Référentiel vers V1_1 crée une incohérence de référence sans blocage déclaré.
- **Nature :** gouvernance — couplage de version non contraint
- **Gravité :** élevée (GPTwoThink) / modérée (NemoTron, ClaudeThink)
- **Impact :** maintenabilité, stabilité — désynchronisation possible sans détection
- **Décision :** `corriger_maintenant` (partiel)
- **Justification :** La Constitution ne peut pas modifier `patchable: false` sur la référence inter-Core (invariant). Correction minimale atteignable : ajouter un invariant constitutionnel `INV_LINK_REVALIDATION_REQUIRED_ON_CORE_VERSION_CHANGE` déclarant l'obligation de re-validation du LINK lors de tout changement de version d'un Core référencé. Le mécanisme de release coordonnée (process pipeline) est reporté.
- **Conséquence pour le patch :** Patch Constitution — ajout d'un invariant de gouvernance inter-Core.

---

### Point N — Binding LINK `seuil_R` interruption longue manquant

- **Source(s) :** NemoTron AX2-01 (MODÉRÉ)
- **Constat synthétique :** Le LINK ne lie pas `EVENT_LONG_INTERRUPTION` au `PARAM_REFERENTIEL_seuil_R`. La délégation du seuil d'interruption longue est partielle.
- **Nature :** structurelle — binding inter-Core partiel
- **Gravité :** modérée
- **Impact :** applicabilité — condition de déclenchement non résolvable sans inférence
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale et additive : ajouter le binding manquant dans le LINK.
- **Conséquence pour le patch :** Patch LINK — ajout d'un binding `EVENT_LONG_INTERRUPTION → PARAM_REFERENTIEL_seuil_R`.

---

### Point O — `TYPE_FEEDBACK_COVERAGE_MATRIX` et `TYPE_AUTHENTIC_CONTEXT` : patchable sans protection anti-régression

- **Source(s) :** GPTwoThink F-5.2 (ÉLEVÉ)
- **Constat synthétique :** Ces deux types sont `patchable: true`. Un patch pourrait réduire la couverture d'erreurs (matrice) ou affaiblir la condition Bloom ≥ 4 (contexte authentique). Aucune CONSTRAINT dédiée n'interdit les patchs régressifs sur ces éléments.
- **Nature :** gouvernance — absence de garde-fou anti-régression
- **Gravité :** élevée
- **Impact :** sécurité logique, maintenabilité pédagogique
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter une CONSTRAINT constitutionnelle `CONSTRAINT_NO_REGRESSIVE_PATCH_ON_FEEDBACK_MATRIX_OR_AUTHENTIC_CONTEXT` interdisant tout patch abaissant le niveau de couverture de la matrice ou le seuil Bloom du contexte authentique.
- **Conséquence pour le patch :** Patch Constitution — ajout d'une CONSTRAINT.

---

### Point P — KU créative déployée dont le feedback devient indisponible en runtime

- **Source(s) :** ClaudeThink F3.1 (ÉLEVÉ), ClaudeWoThink A2-3 (MODÉRÉ)
- **Constat synthétique :** `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` bloque le déploiement autonome sans feedback local. Mais si une KU créative déjà déployée voit son feedback devenir indisponible post-patch, le chemin de désactivation runtime n'est pas défini.
- **Nature :** logique — état intermédiaire non défini
- **Gravité :** élevée
- **Impact :** sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : ajouter un invariant ou une règle de désactivation runtime déclarant que si le feedback local d'une KU créative active devient indisponible, le moteur bascule cette KU en mode hybride bloquant (action : `ACTION_FREEZE_CREATIVE_KU_PENDING_FEEDBACK_RESTORATION`).
- **Conséquence pour le patch :** Patch Constitution — invariant ou RULE de désactivation runtime + ACTION associée.

---

### Point Q — Binding AR-N3 ambigu : logique métier dans le LINK

- **Source(s) :** ClaudeThink F5.1 (ÉLEVÉ)
- **Constat synthétique :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` décrit un flux multi-étapes conditionnel approchant la frontière logique métier, explicitement interdite par `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`.
- **Nature :** gouvernance — frontière couche LINK/Constitution potentiellement violée
- **Gravité :** élevée
- **Impact :** maintenabilité, séparation des couches
- **Décision :** `corriger_maintenant`
- **Justification :** Refactoring minimal du binding : séparer en deux bindings simples — `BINDING_AR_N3_TO_CALIBRATION_AXIS` et `BINDING_CALIBRATION_TO_SIGNAL_REWEIGHTING`. La logique conditionnelle reste dans la RULE référentielle existante, le LINK ne fait que pointer.
- **Conséquence pour le patch :** Patch LINK — refactoring du binding en deux bindings simples.

---

### Point R — `TYPE_FEEDBACK_COVERAGE_MATRIX` non obligatoire pour KU perceptuelles

- **Source(s) :** GPTwoThink F-2.4 (MODÉRÉ)
- **Constat synthétique :** La condition d'obligation de la matrice feedback couvre KU formelles et procédurales, mais pas les perceptuelles, alors que `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` les identifie comme nécessitant un traitement multimodal spécifique.
- **Nature :** logique — incohérence entre invariant et condition d'obligation
- **Gravité :** modérée
- **Impact :** applicabilité — KU perceptuelle déployable sans matrice
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : étendre la condition d'obligation de `TYPE_FEEDBACK_COVERAGE_MATRIX` aux KU perceptuelles.
- **Conséquence pour le patch :** Patch Constitution — mise à jour de la condition d'obligation.

---

### Point S — Proxys comportementaux non définis constitutionnellement

- **Source(s) :** GPTwoThink F-4.3 (MODÉRÉ)
- **Constat synthétique :** `RULE_AR_N1_OVERRIDES_PROXY` mentionne les proxys comme source alternative mais la Constitution ne les liste ni ne les contraint. Leur nature reste implicite.
- **Nature :** éditoriale + logique
- **Gravité :** modérée
- **Impact :** maintenabilité — risque d'inférence non encadrée
- **Décision :** `reporter`
- **Justification :** Les proxys comportementaux sont un concept transversal dont la définition exhaustive dépasse le scope d'un patch minimal. Reporter à un run dédié à la formalisation des signaux d'état apprenant.

---

### Point T — Flagging `misconception` : dépendance IA ou humaine implicite

- **Source(s) :** ClaudeThink F4.1 (ÉLEVÉ), ClaudeWoThink A4-1 (MODÉRÉ), GPTwoThink F-4.1 (MODÉRÉ)
- **Constat synthétique :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` se déclenche sur `KU flaggée misconception` mais le processus de flagging n'est pas décrit. Si ce flagging est automatique, cela peut violer `INV_RUNTIME_FULLY_LOCAL`. Les trois rapports convergent sur la modération du risque mais divergent sur la gravité (ÉLEVÉ vs MODÉRÉ).
- **Nature :** logique + dépendance IA implicite
- **Gravité :** modérée (arbitrage)
- **Impact :** applicabilité, séparation runtime/design
- **Décision :** `corriger_maintenant` (minimal)
- **Justification :** Correction minimale : clarifier dans la Constitution que le flag `misconception` est exclusivement posé en phase Design (annotation humaine ou IA offline), jamais en runtime. Ajouter une CONSTRAINT ou note normative dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`.
- **Conséquence pour le patch :** Patch Constitution — clarification normative (annotation ou CONSTRAINT) dans la RULE.

---

### Point U — ICC (`TYPE_CORPUS_CONFIDENCE_ICC`) : concept déclaré sans seuil minimal de déploiement

- **Source(s) :** ClaudeThink F3.3 (FAIBLE), GPTwoThink F-4.2 (MODÉRÉ)
- **Constat synthétique :** L'ICC qualifie la confiance du corpus mais aucun seuil minimal de déploiement n'est déclaré constitutionnellement ou référentiellement. Un ICC très bas peut autoriser un déploiement non fiable.
- **Nature :** logique — chaîne causale incomplète
- **Gravité :** modérée
- **Impact :** sécurité logique
- **Décision :** `reporter`
- **Justification :** La définition d'un seuil ICC implique une décision de conception sur la mesure de confiance (qualitatif/quantitatif, source). Reporter à un run dédié.

---

### Point V — Rollback et cohérence LINK post-rollback

- **Source(s) :** ClaudeThink F5.3 (FAIBLE)
- **Constat synthétique :** En cas de rollback d'un patch ayant créé un nouveau binding LINK, le rollback du patch Core ne garantit pas la cohérence du LINK. Le LINK n'a pas de mécanisme de versioning ou rollback propre.
- **Nature :** gouvernance
- **Gravité :** faible
- **Impact :** maintenabilité
- **Décision :** `reporter`
- **Justification :** Correction non urgente et complexe (mécanisme de versioning LINK). Reporter à un run de gouvernance inter-Core dédié.

---

### Point W — Fréquence AR-N1 non bornée constitutionnellement

- **Source(s) :** GPTwoThink F-2.1 (FAIBLE)
- **Constat synthétique :** En présence de nombreux événements déclencheurs simultanés, le moteur peut empiler des AR-N1 sans limite de fréquence.
- **Nature :** logique
- **Gravité :** faible
- **Impact :** expérience apprenant (charge extrinsèque)
- **Décision :** `reporter`
- **Justification :** Le paramètre `PARAM_AR_N1_INTERACTION_BUDGET` existe déjà. La borne de fréquence peut être traitée dans le Référentiel sans modification constitutionnelle urgente.

---

### Point X — `ARBITRAGE_2026_04_01` non matérialisé dans `work/02_arbitrage/`

- **Source(s) :** NemoTron AX5-02 (MODÉRÉ), ClaudeWoThink A5-2 (MODÉRÉ)
- **Constat synthétique :** Les éléments portant `source_anchor: '[ARBITRAGE_2026_04_01]'` n'ont pas de document d'arbitrage correspondant dans `work/02_arbitrage/`. Traçabilité déclarative uniquement.
- **Nature :** traçabilité
- **Gravité :** modérée
- **Impact :** maintenabilité, auditabilité
- **Décision :** `hors_perimetre`
- **Justification :** Aucun impact moteur. La matérialisation rétroactive d'un arbitrage passé est une opération de traçabilité documentaire, non un patch de Core. À traiter séparément par le responsable du pipeline.

---

### Point Y — LINK non fourni pour ClaudeWoThink : bindings inter-Core non vérifiables

- **Source(s) :** ClaudeWoThink CRIT-01, CRIT-02
- **Constat synthétique :** Le LINK n'était pas dans le corpus de ClaudeWoThink. Les constats CRIT-01 et CRIT-02 portent sur l'impossibilité de vérifier les bindings inter-Core et la cohérence de version LINK/Constitution depuis ce rapport.
- **Nature :** limite d'audit — input manquant au moment du challenge
- **Gravité :** critique (conditionnelle au corpus)
- **Impact :** auditabilité uniquement pour ce run partiel
- **Décision :** `hors_perimetre`
- **Justification :** Les autres challengers (ClaudeThink, NemoTron, GPTwoThink) avaient accès au LINK. Les bindings inter-Core identifiés comme manquants par ces trois rapports sont couverts dans les Points A, L, N du présent arbitrage. Le constat de ClaudeWoThink est validé par convergence mais sa catégorie "input manquant" ne génère pas de correction supplémentaire.

---

### Point Z — Mécanisme de release coordonnée inter-Core (process pipeline)

- **Source(s) :** GPTwoThink F-5.3 (ÉLEVÉ) — aspect process
- **Constat synthétique :** Aucun mécanisme de process pipeline ne décrit comment mettre à jour `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` lors d'une promotion de version du Référentiel, sans violer `patchable: false`.
- **Nature :** gouvernance pipeline — décision organisationnelle
- **Gravité :** élevée
- **Impact :** maintenabilité à long terme
- **Décision :** `hors_perimetre`
- **Justification :** Ce point requiert une décision de gouvernance humaine sur le process de release coordonnée (STAGE_07/STAGE_08). L'invariant de gouvernance inter-Core (Point M) couvre la partie patchable. Le process pipeline complet est hors périmètre du présent run.

---

## Points consolidés

### Groupes fusionnés (18 fusions sur 52 constats bruts)

| Groupe | Points fusionnés | Décision |
|--------|-----------------|----------|
| A | NemoTron AX1-01, ClaudeWoThink A1-3, GPTwoThink 1.4 | corriger_maintenant |
| B | NemoTron AX1-02, ClaudeThink F1.3, ClaudeWoThink A4-2, GPTwoThink 1.1 | corriger_maintenant (partiel) |
| C | ClaudeThink F1.2, ClaudeWoThink HIGH-01 + A3-1 | corriger_maintenant |
| D | ClaudeWoThink A1-4 + A3-2 + HIGH-02 | corriger_maintenant |
| E | ClaudeThink F1.4, ClaudeWoThink A3-3 + HIGH-03 + A2-1 | corriger_maintenant |
| J | NemoTron AX1-03, ClaudeThink F2.3 | corriger_maintenant |
| M | NemoTron AX5-01, ClaudeThink F5.2, GPTwoThink F-5.3 | corriger_maintenant |
| T | ClaudeThink F4.1, ClaudeWoThink A4-1, GPTwoThink F-4.1 | corriger_maintenant |
| X | NemoTron AX5-02, ClaudeWoThink A5-2 | hors_perimetre |

### Divergences résolues

- **Gravité de T (misconception)** : ClaudeThink ÉLEVÉ vs GPTwoThink/ClaudeWoThink MODÉRÉ → arbitré en MODÉRÉ, car la correction est éditoriale et non structurelle.
- **Gravité de M (versioning)** : GPTwoThink ÉLEVÉ vs NemoTron/ClaudeThink MODÉRÉ → arbitré en correction immédiate (invariant constitutionnel minimal), sans attendre un run dédié.
- **Sémantique expiration maîtrise provisoire** : révocation vs escalade diagnostique → arbitré en escalade diagnostique (principe de conservation).

---

## Décisions à transmettre au patch

| Priorité | Point | Titre court | Core(s) cibles |
|----------|-------|-------------|----------------|
| CRITIQUE | A | Binding LINK MSC_PERCEPTION_DIVERGENCE_THRESHOLD | LINK + Constitution |
| CRITIQUE | F | Table de priorité escalades concurrentes SYST-01 > DIVMSC-01 > MOT-01 | Constitution |
| CRITIQUE | G | Règle de détection dégradée VC+AR+MSC | Constitution |
| CRITIQUE | H | Extension trigger INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC post-patch | Constitution |
| CRITIQUE | I | Invariant précondition déploiement paramètres Référentiel | Constitution |
| ÉLEVÉ | B | Relation TYPE_MASTERY_MODEL → INV_TRANSFER + EVENT_T_EVALUATION_OVERDUE | Constitution |
| ÉLEVÉ | C | Déclarer EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION + EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED | Référentiel |
| ÉLEVÉ | D | PARAM_OSCILLATION_MAX_CYCLES + condition sortie de secours régime oscillatoire | Référentiel |
| ÉLEVÉ | E | EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED + paramètre durée fenêtre | Constitution + Référentiel |
| ÉLEVÉ | M | INV_LINK_REVALIDATION_REQUIRED_ON_CORE_VERSION_CHANGE | Constitution |
| ÉLEVÉ | O | CONSTRAINT_NO_REGRESSIVE_PATCH_ON_FEEDBACK_MATRIX_OR_AUTHENTIC_CONTEXT | Constitution |
| ÉLEVÉ | P | Invariant/RULE désactivation runtime KU créative + ACTION_FREEZE_CREATIVE_KU | Constitution |
| ÉLEVÉ | Q | Refactoring binding AR-N3 en deux bindings simples | LINK |
| MODÉRÉ | J | PARAM_GAMIFICATION_PROBATION_MAX_SESSIONS + EVENT sortie probatoire | Référentiel |
| MODÉRÉ | K | ACTION pour escalade INV_PERSISTENT_DRIFT | Constitution |
| MODÉRÉ | L | CONSTRAINT protection RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED | LINK |
| MODÉRÉ | N | Binding EVENT_LONG_INTERRUPTION → PARAM_seuil_R | LINK |
| MODÉRÉ | R | Extension condition obligation matrice feedback aux KU perceptuelles | Constitution |
| MODÉRÉ | T | Clarification normative flagging misconception = Design-time uniquement | Constitution |

### Contraintes de minimalité pour le patch
- Préférer les ajouts additifs (nouveaux EVENTs, CONSTRAINTs, BINDINGs) aux modifications de blocs existants patchable: false.
- Pour Point H : si le DSL patch interdit la modification d'un invariant non-patchable, introduire un invariant complémentaire plutôt que de modifier le trigger de l'invariant existant.
- Pour Point G : la règle de détection dégradée doit rester constitutionnellement distincte du protocole DIVMSC-01 principal (ne pas modifier la règle existante, ajouter une règle de fallback).
- Chaque point doit faire l'objet d'au moins un bloc patch YAML distinct pour la traçabilité.

---

## Décisions explicitement non retenues

### Points reportés

| Point | Titre | Justification |
|-------|-------|---------------|
| B-suite | Paramétrie Référentiel T et binding LINK T complet | Décision de conception requise sur la nature opérationnelle de T |
| S | Proxys comportementaux non définis | Scope trop large pour un patch minimal ; run dédié requis |
| U | ICC sans seuil minimal de déploiement | Décision de mesure requise ; run dédié |
| V | Rollback et cohérence LINK post-rollback | Complexité de versioning LINK ; run dédié |
| W | Fréquence AR-N1 non bornée | Traitable dans le Référentiel sans urgence constitutionnelle |
| NemoTron AX2-02 | Sources autorisées Calibration non listées | Asymétrie de gouvernance faible, run dédié |
| ClaudeThink F2.2 | Forethought SRL sans effet moteur | Décision de conception délibérée à clarifier ; run dédié |
| ClaudeWoThink A2-2 | Borne haute reweighting AR-N1 | Modéré, traitable dans le Référentiel ; run dédié |
| GPTwoThink F-2.1 | Fréquence AR-N1 | Couvert partiellement par PARAM_AR_N1_INTERACTION_BUDGET existant |
| GPTwoThink F-3.4 | AR-N2 sans priorité — fallback manquant | Faible, run dédié |
| GPTwoThink F-5.4 | Fréquence déclenchement patches relevance/AR | Modéré, run dédié |
| ClaudeWoThink MOD-04 | KU créative calibrage sans précondition feedback | Partiellement couvert par Point P ; reste mineur |

### Points rejetés

| Point | Titre | Justification |
|-------|-------|---------------|
| GPTwoThink F-2.3 | Scaffolding conservatif non stratifié par type d'activation | Sans AR-N1, la stratification requiert exactement le signal absent ; le conservatisme uniforme est un choix délibéré cohérent avec les invariants existants |
| ClaudeWoThink A4-2 (partiel) | Sélection contexte transfert non locale | La sélection du contexte de transfert est par nature offline (phase Design) ; aucune inférence runtime n'est requise si T est correctement conçue |

### Points hors périmètre

| Point | Titre | Justification |
|-------|-------|---------------|
| X | ARBITRAGE_2026_04_01 non matérialisé | Traçabilité documentaire, pas de patch Core |
| Y | LINK absent corpus ClaudeWoThink | Limite d'audit couverte par les autres challengers |
| Z | Release coordonnée inter-Core — process pipeline | Décision de gouvernance humaine, hors périmètre patch |
