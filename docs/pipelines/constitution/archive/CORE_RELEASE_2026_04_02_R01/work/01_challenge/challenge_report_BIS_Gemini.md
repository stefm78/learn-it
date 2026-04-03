# Challenge Report — Constitution Pipeline
**ID agent** : Gemini
**Stage** : STAGE_01_CHALLENGE
**Date** : 2026-04-01
**Cores challengés** :
- `CORE_LEARNIT_CONSTITUTION_V1_9` (V1_9_FINAL)
- `CORE_LEARNIT_REFERENTIEL_V1_0` (V1_0_FINAL)
- `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0` (V1_9__V1_0_FINAL)

---

## Résumé exécutif

Le système Learn-it présente une architecture de gouvernance sérieuse, bien cloisonnée, avec un moteur 100 % local fermé théoriquement solide. Plusieurs invariants critiques protègent les composantes fondamentales (MSC AND-strict, propagation 1-saut, séparation Constitution/Référentiel). Cependant, l'analyse adversariale révèle **six zones de risque significatives** : (1) des états indéfinis ou oscillatoires dans la résolution du modèle apprenant multi-sources, (2) une dépendance sémantique implicite dans le scoring SIS sans mécanisme déterministe pleinement spécifié, (3) une sous-spécification critique de la composante A (autonomie) dans les KU créatives, (4) un risque de blocage moteur sur les scénarios Bloom ≥ 4 lors du design progressif, (5) une ambiguïté de frontière dans la gestion des rétrogradations secondaires différées, et (6) une incomplétude du LINK sur les bindings relatifs à la gouvernance de déploiement (TYPE_AUTONOMY_REGIME / checkpoints humains).

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

**1.1 — Paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` sans event constitutionnel dédié**

- Élément concerné : `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` (Référentiel, `[ARBITRAGE_2026_04_01][MOT-01]`) + `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` (Constitution, `[S7]`)
- Le Référentiel déclare un paramètre d'escalade après N sessions en mode conservateur sans AR-N1. Or, la Constitution ne contient aucun `EVENT_` correspondant à ce déclencheur (`EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` est mentionné dans la `human_readable` du paramètre mais absent du catalogue constitutionnel d'EVENTS).
- Type : **complétude / gouvernance**
- Impact moteur : l'escalade référentielle est orpheline ; aucune règle constitutionnelle ne la reçoit. Le moteur ne sait pas quelle action déclencher à l'issue de cette fenêtre.
- Correction à arbitrer : créer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` en Constitution (ou documenter explicitement l'action associée dans le Référentiel avec un binding LINK).

**1.2 — `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` mentionnée mais absente**

- Élément concerné : `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` (Référentiel, `[ARBITRAGE_2026_04_01][GOV-02]`) fait référence à `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` (phrase : *"autorisée constitutionnellement par RULE_VC_AXIS_DEACTIVATION_AUTHORIZED"*).
- Cette règle est **absente** du Core Constitution V1_9.
- Type : **complétude / gouvernance**
- Impact moteur : la désactivation de l'axe VC repose sur une autorisation constitutionnelle fantôme. La règle `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` (Référentiel) devient potentiellement non autorisée formellement.
- Correction à arbitrer : créer `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` en Constitution, ou corriger la `human_readable` du paramètre pour supprimer cette référence croisée invalide.

**1.3 — Binding manquant : `TYPE_AUTONOMY_REGIME` / `TYPE_HUMAN_CHECKPOINT` non liés au LINK**

- Élément concerné : `TYPE_AUTONOMY_REGIME` et `TYPE_HUMAN_CHECKPOINT` (Constitution) — bindings LINK absents.
- Le LINK couvre les chaînes MSC, signal état apprenant, feedback coverage, patch governance, et AR-N3/calibration. Il ne contient aucun binding explicite reliant le régime d'autonomie constitutionnel aux paramètres de déploiement ou aux checkpoints humains.
- Type : **complétude**
- Impact moteur : la résolution opérationnelle des modes Autonome/Hybride/Assisté ne passe par aucun binding inter-Core. Si le Référentiel introduit un jour des paramètres d'activation de checkpoints, la chaîne ne sera pas fermée.
- Correction à arbitrer : ajouter un TYPE_BINDING dans le LINK couvrant `TYPE_AUTONOMY_REGIME` ↔ `TYPE_HUMAN_CHECKPOINT` ↔ déploiement.

**1.4 — `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` dépend de `PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_SHORT` mais pas de `_DELAY_MEDIUM`**

- Élément concerné : `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` (Référentiel, `[S2]`)
- La logique : *"Référence 2 échecs consécutifs"* après délai R atteint. Mais le délai R peut être court (3 j) ou moyen (7 j) selon le type de KU — or seul le délai court est déclaré en `depends_on`. Pour des KU déclaratives vs. procédurales, le comportement de révocation post-maîtrise peut devenir incohérent.
- Type : **implémentabilité**
- Impact moteur : une KU procédurale (R multiplié ×2–3) déclenchera une révocation sur un délai court, alors que la règle `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` suppose une fenêtre temporelle configurée.
- Correction à arbitrer : ajouter `PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_MEDIUM` en `depends_on`, ou clarifier que le paramètre de révocation s'applique toujours au délai de référence du type KU courant.

---

### Axe 2 — Solidité théorique

**2.1 — Charge cognitive**
- Point solide : le garde-fou `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL` (25 min) et la restriction multimodale pour KU procédurales/perceptuelles (`INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL`) adressent correctement la charge intrinsèque.
- Zone de risque : aucun mécanisme ne gère la charge extrinsèque cumulée sur une session longue impliquant plusieurs types de KU hétérogènes (mix déclaratif + procédural + formel). La fatigue peut survenir avant 25 min sans trigger.
- Angle mort : pas de paramètre d'intervalle entre types de KU dans une même session.

**2.2 — Mémoire / consolidation**
- Point solide : le MSC AND-strict P×R×A et les multiplicateurs R par type de KU constituent une implémentation locale robuste de la théorie de l'espacement.
- Zone de risque : la révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) distingue bien rétrogradation courante et révocation stabilisée, mais la "fenêtre temporelle et les répétitions configurées" pour la révocation ne sont pas paramétrées explicitement dans le Référentiel — seul `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` est présent.
- Angle mort : absence de traitement de l'oubli partiel (partial forgetting) entre sessions proches ; le moteur ne distingue pas un oubli bénin d'une dégradation réelle sans signal R.

**2.3 — Motivation**
- Point solide : l'axe VC avec non-pénalisation, le patch relevance et la distinction VC/détresse (`INV_VC_NOT_GENERAL_MOTIVATION_PROXY`) sont théoriquement alignés avec la théorie Valeur-Attente (Eccles & Wigfield).
- Zone de risque : le patch relevance déclenché par VC basse persistante ne peut pas ajuster la difficulté (`CONSTRAINT_REFERENTIEL_NO_DIFFICULTY_ADJUSTMENT_FROM_VC_PATCH`). Or, une difficulté perçue excessivement haute peut elle-même déprimer la VC — cette interaction n'est pas couverte.
- Angle mort : aucun mécanisme de "quick win" ou de récompense intrinsèque de progression pour apprenant en état sous-défi non détectable (VC normale + MSC non atteint).

**2.4 — Métacognition / SRL**
- Point solide : l'intention de session (AR-N2), non bloquante, et le bilan AR-N3 dérivé d'AEQ structurent un cycle SRL forethought-performance-reflection minimaliste et cohérent.
- Zone de risque : l'intention de session est collectée *inter-session* (`TYPE_REFERENTIEL_SESSION_INTENTION_CONFIGURATION`, trigger: "Préparation inter-session") mais la Constitution déclare AR-N2 comme un *mini-sondage de fin de session* (`[S11]`). Il y a une ambiguïté temporelle sur le moment de collecte de l'intention.
- Angle mort : aucun mécanisme de restitution de l'intention à l'apprenant en début de session suivante (feedback de cohérence SRL).

**2.5 — Émotions / engagement**
- Point solide : la distinction AR-N1 confusion/frustration/anxiété (`TYPE_SELF_REPORT_AR_N1`) et la règle conservatrice en absence de signal (`INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`) protègent contre les interventions punitives.
- Zone de risque : le profil AR-réfractaire est traité uniquement comme un problème de sollicitation (`ACTION_TRIGGER_AR_SOLLICITATION_PATCH`). Un apprenant genuinement en détresse émotionnelle chronique qui ne répond pas aux AR-N1 est traité de manière identique à un apprenant indifférent — pas de différenciation.
- Angle mort : pas de signal de détresse émotionnelle persistante escaladable vers humain hors session (seul le mode Assisté implique un tutorat, mais sans lien causal avec l'état émotionnel détecté).

**2.6 — Mastery learning**
- Point solide : l'AND-strict P×R×A est une implémentation conservatrice et protégée du mastery learning de Bloom/Carroll. La séparation T (`INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`) est théoriquement juste.
- Zone de risque : la composante A (autonomie = réussites sans aide) est sous-définie pour les KU créatives. Pour une KU créative, "l'aide" est difficile à objectiver localement (pas de correction déterministe), ce que `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` adresse partiellement mais en bloquant tout plutôt qu'en proposant une alternative.
- Angle mort : aucune définition de la notion d'aide pour les KU créatives déployables en mode hybride recommandé.

**2.7 — Ingénierie pédagogique**
- Point solide : le cycle ADDIE est implicitement respecté (Analyse avec ICC, Design avec Feedback Coverage Matrix, déploiement progressif).
- Zone de risque : la matrice de feedback (`TYPE_FEEDBACK_COVERAGE_MATRIX`) est déclarée comme livrable obligatoire uniquement pour les KU "formelles ou procédurales". Les KU déclaratives ne sont pas explicitement couvertes par cette obligation.
- Angle mort : pas de standard de granularité pour la matrice (pas de minimum d'entrées par KU, pas de format imposé).

---

### Axe 3 — États indéfinis moteur

**3.1 — Oscillation dans la résolution Consolidation vs Exploration**

- La `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (`[ARBITRAGE_2026_04_01][MATRIX-01]`) introduit un *régime oscillatoire* pour Consolidation + Exploration : "alternance 1 session consolidation satisfaisante → 1 session exploration → retour consolidation, sortie quand R atteint".
- **État indéfini** : si la session de consolidation n'est pas "satisfaisante" (définition absente), l'alternance est bloquée. Le moteur doit décider sans règle applicable ce que signifie "consolidation satisfaisante" dans ce contexte oscillatoire.
- Impact moteur : risque de gel du régime ou de boucle infinie sur ce type de KU.

**3.2 — Session de calibrage sans type KU disponible**

- La `TYPE_REFERENTIEL_KU_CALIBRATION_FORMAT_TABLE` présuppose un "type de KU connu". Or, `INV_KU_TYPING_REQUIRED` stipule que toute KU non typée déclenche un mode de sécurité (`INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK`).
- **État indéfini** : lors d'une session de calibrage initial pour une KU non encore typée, le moteur ne peut pas sélectionner un format de calibrage (tableau par type) tout en étant en mode fallback sécurisé.
- Impact moteur : blocage du calibrage initial ou format par défaut non spécifié.

**3.3 — Rétrogradation secondaire différée sans KU disponible dans la fenêtre**

- `RULE_REFERENTIEL_SECONDARY_RETROGRADATION_DEFERRED_REENTRY` stipule un réentrée "au prochain cycle autorisé". `PARAM_REFERENTIEL_PROPAGATION_CHECK_MAX_DELAY_SESSIONS` fixe la fenêtre à 1 session. Mais si la KU dépendante marquée n'a pas de tâche planifiable (ex. KU sans contenu disponible, tâche en attente de patch), la fenêtre expire sans action.
- **État indéfini** : que fait le moteur à l'expiration de la fenêtre sans exécution possible ? Pas de règle de gestion de ce cas dégénéré.
- Impact moteur : accumulation silencieuse de flags de rétrogradation secondaire sans résolution.

---

### Axe 4 — Dépendances IA implicites

**4.1 — Session Integrity Score (SIS) : inférence comportementale sans spécification déterministe**

- Élément concerné : `TYPE_SESSION_INTEGRITY_SCORE` (`[S15][S20]`), `TYPE_INTEGRITY_MODES`
- La Constitution déclare que le SIS est calculé à partir d'*"indices d'intégrité disponibles"* (`condition`), mais ne liste nulle part ces indices ni leur formule de calcul dans le Core.
- **Dépendance implicite** : évaluer l'intégrité d'une session (multi-profil, invité, évaluation externe) requiert vraisemblablement une inférence comportementale non triviale (comparaison de patterns, détection d'anomalies de timing, etc.) qui dépasse un calcul purement déterministe local.
- Alternative sans IA continue : liste fermée d'indices binaires déclarés (ex. : switch de profil détecté O/N, durée atypique O/N, contexte d'évaluation active O/N) avec pondération statique configurable par paramètre.
- Correction à arbitrer : formaliser les indices SIS comme des paramètres déterministes dans le Référentiel, ou documenter explicitement que le SIS est calculé par un module hors-session précompilé.

**4.2 — Détection du profil AR-réfractaire : frontière flou entre non-réponse intentionnelle et indisponibilité**

- Élément concerné : `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION`, `PARAM_REFERENTIEL_AR_REFRACTORY_SESSIONS_REFERENCE`
- La détection est purement basée sur la non-réponse sur N sessions consécutives. Aucune distinction entre non-réponse technique (bug UX, timing) et refus délibéré n'est possible sans inférence contextuelle.
- **Dépendance implicite** : distinguer ces cas requiert du contexte sémantique ou des signaux corrélés (ex. : l'apprenant a-t-il interagi avec d'autres éléments de la session ?).
- Alternative : déclarer explicitement que la détection est comportementale pure (comptage de non-réponses) sans distinction d'intention — ce qui est implicitement le cas mais non explicité.
- Correction à arbitrer : ajouter en Constitution ou Référentiel une règle explicite stipulant que la détection AR-réfractaire est intentionnellement agnostique de la cause.

---

### Axe 5 — Gouvernance

**5.1 — Versioning inter-Core non symétrique**

- La Constitution référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` (version V1_0). Le Référentiel référence `REF_CORE_LEARNIT_CONSTITUTION_V1_9_IN_REFERENTIEL` (version V1_9). Le LINK déclare `version: V1_9__V1_0_FINAL`.
- **Risque de gouvernance** : si l'un des Cores est patché (ex. Constitution passe en V1_10), la référence croisée dans le Référentiel devient obsolète, et le LINK doit être mis à jour manuellement — sans mécanisme de détection automatique de désynchronisation.
- Type : **gouvernance**
- Impact moteur : le système peut fonctionner avec des références de version incohérentes sans signal d'alerte.
- Correction à arbitrer : définir une règle de mise à jour synchronisée des références inter-Core lors de tout bump de version majeur, ou introduire un mécanisme de validation de cohérence de versions dans le pipeline.

**5.2 — Invariants LINK vides : protection incomplète**

- Le LINK déclare `INVARIANTS: []`, `RULES: []`, `PARAMETERS: []`, `EVENTS: []`, `ACTIONS: []`.
- Si le LINK ne doit contenir aucune logique métier, il devrait néanmoins porter des **invariants de structure** (ex. : "le LINK ne contient que des TYPE_BINDING de type `derived`", "tout binding doit référencer au moins un élément de chaque Core").
- Type : **gouvernance**
- Impact moteur : un futur patch pourrait introduire un TYPE_BINDING avec `authority: primary` sans violation explicite d'une règle LINK.
- Correction à arbitrer : ajouter des invariants structurels dans le LINK limitant les types d'éléments autorisés.

**5.3 — Maîtrise provisoire héritée sans mécanisme de supervision explicite**

- Élément concerné : `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` (Constitution, `[S2][S20]`) — déclare une "fenêtre constitutionnellement déclarée pour vérifier une maîtrise provisoire héritée".
- Cette fenêtre n'est reliée à aucun EVENT constitutionnel ou référentiel. Aucun `EVENT_PROVISIONAL_MASTERY_EXPIRED` n'existe.
- Type : **complétude**
- Impact moteur : une maîtrise provisoire héritée peut expirer silencieusement sans déclenchement d'une action moteur. Incluse dans les 4 signaux de l'investigation systémique (`PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`), mais uniquement comme signal candidat sans mécanisme propre.
- Correction à arbitrer : créer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` en Constitution avec action associée, ou clarifier que la supervision est exclusivement portée par l'investigation systémique.

---

### Axe 6 — Scénarios adversariaux

**Scénario A — KU créative en régime autonome, AR-N1 absent, VC basse persistante**

- Contexte : déploiement autonome ; KU créative avec feedback déterministe formalisé (condition `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` satisfaite). L'apprenant ne répond pas à AR-N1 sur 5 sessions (profil réfractaire). VC reste inobservable (AR-N2 incomplet).
- Mécanismes activés : `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` → mode conservateur. `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` → axe VC désactivé après 5 sessions. `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION` → profil réfractaire détecté.
- **Limite non documentée** : le moteur est en mode conservateur indéfini, avec axe VC désactivé et profil réfractaire actif simultanément. La table de résolution de conflits ne couvre pas ce triple état. L'escalade conservatrice (`PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`) est déclenchée, mais son destinataire est un EVENT absent. **Blocage moteur probable.**

**Scénario B — Design progressif avec introduction tardive du contexte authentique pour Bloom ≥ 4**

- Contexte : un instructeur conçoit un module en commençant par des KU Bloom 1–3, puis souhaite introduire une KU Bloom 4 après plusieurs sessions d'apprentissage. Le contexte authentique est ajouté tardivement en phase Design.
- Mécanismes activés : `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4` + `EVENT_HIGH_BLOOM_WITHOUT_AUTHENTIC_CONTEXT` → blocage et plafonnement à Bloom 2 si le contexte n'est pas déclaré avant le déploiement de la KU.
- **Limite non documentée** : aucune procédure de mise à jour du graphe existant pour ajouter rétrospectivement un `TYPE_AUTHENTIC_CONTEXT` sur des KU déjà déployées. Un patch sur une KU existante pour ajouter le contexte authentique modifie-t-il l'`impact_scope` ? Aucun mécanisme de rétro-correction de graphe sans rechargement complet n'est spécifié.

**Scénario C — Investigation systémique auto-ouverte avec patch en attente**

- Contexte : investigation systémique ouverte automatiquement (`EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` — absent mais référencé dans le Référentiel). Simultanément, un patch relevance VC est éligible (`EVENT_REFERENTIEL_PATCH_TRIGGER_THRESHOLD_CROSSED`).
- Mécanismes activés : `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` → gel des ajustements agressifs. `ACTION_REFERENTIEL_TRIGGER_RELEVANCE_PATCH` → patch éligible.
- **Limite non documentée** : le patch relevance est-il considéré comme un "ajustement agressif" gelé par l'investigation ? Aucune hiérarchie explicite entre le gel de l'investigation et l'éligibilité du patch n'est déclarée. Le moteur peut soit appliquer un patch pendant une investigation (risque de pollution des données d'investigation), soit geler un patch éligible sans règle de persistance.

---

### Axe 7 — Priorisation des risques

| ID | Élément | Nature | Type | Criticité |
|----|---------|--------|------|-----------|
| R-01 | `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` absente en Constitution | Référence croisée invalide | Gouvernance | **Critique** |
| R-02 | `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` absent | Paramètre orphelin | Complétude | **Critique** |
| R-03 | SIS sans indices déterministes formalisés | Dépendance IA implicite potentielle | Implémentabilité | **Élevé** |
| R-04 | Scénario A : triple état conservateur + VC désactivé + réfractaire (blocage moteur) | État indéfini | Implémentabilité | **Élevé** |
| R-05 | `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans EVENT propre | Paramètre orphelin | Complétude | **Élevé** |
| R-06 | Oscillation Consolidation/Exploration sans définition "satisfaisante" | État indéfini | Implémentabilité | **Élevé** |
| R-07 | Versioning inter-Core non synchronisé | Invariant mal protégé | Gouvernance | **Modéré** |
| R-08 | LINK sans invariants structurels | Absence de protection | Gouvernance | **Modéré** |
| R-09 | KU créative : composante A indéfinie (aide non objectivable) | Sous-spécification | Théorique / Implémentabilité | **Modéré** |
| R-10 | `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` depends_on incomplet | Incohérence opérationnelle | Implémentabilité | **Modéré** |
| R-11 | Scénario C : hiérarchie investigation systémique vs. patch éligible absente | Conflit de gouvernance | Gouvernance | **Modéré** |
| R-12 | Scénario B : rétro-correction de graphe pour contexte authentique non spécifiée | Complétude procédurale | Complétude | **Modéré** |
| R-13 | `TYPE_FEEDBACK_COVERAGE_MATRIX` : obligation limitée aux KU formelles/procédurales | Couverture partielle | Complétude | **Faible** |
| R-14 | Intention de session : ambiguïté temporelle inter-session vs. fin de session | Incohérence Constitution/Référentiel | Théorique | **Faible** |
| R-15 | Binding LINK manquant pour `TYPE_AUTONOMY_REGIME` / `TYPE_HUMAN_CHECKPOINT` | Binding manquant | Complétude | **Faible** |

---

## Corrections à arbitrer avant patch

### C-01 [R-01 — Critique]
- **Élément** : `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`
- **Nature** : référence à `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` absente en Constitution
- **Type** : gouvernance / complétude
- **Impact moteur** : la désactivation de l'axe VC n'a pas d'autorisation constitutionnelle explicite
- **Correction** : créer `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` en Constitution (scope: runtime_state, condition: axe VC non observable sur fenêtre configurée, effect: désactivation autorisée et réversible), ou supprimer la référence de la `human_readable` du paramètre et documenter l'autorisation dans le LINK.

### C-02 [R-02 — Critique]
- **Élément** : `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`
- **Nature** : event `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` référencé mais absent
- **Type** : complétude
- **Impact moteur** : escalade après N sessions conservatrices sans destinataire constitutionnel
- **Correction** : créer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` en Constitution avec `RULE_` associée déclenchant une escalade hors-session, et binding LINK correspondant.

### C-03 [R-03 — Élevé]
- **Élément** : `TYPE_SESSION_INTEGRITY_SCORE`
- **Nature** : indices SIS non formalisés localement
- **Type** : implémentabilité
- **Impact moteur** : SIS potentiellement non calculable de façon déterministe
- **Correction** : déclarer dans le Référentiel un `TYPE_REFERENTIEL_SESSION_INTEGRITY_INDEX_SET` listant les indices SIS admissibles (binaires, déterministes) avec leurs pondérations de référence.

### C-04 [R-05 — Élevé]
- **Élément** : `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`
- **Nature** : fenêtre sans EVENT propre
- **Type** : complétude
- **Impact moteur** : maîtrise provisoire expirée silencieusement sans action
- **Correction** : créer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` en Constitution avec action associée (au minimum : déclassement MSC provisoire ou tâche diagnostique).

### C-05 [R-06 — Élevé]
- **Élément** : `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` — régime oscillatoire
- **Nature** : "consolidation satisfaisante" indéfinie
- **Type** : implémentabilité
- **Impact moteur** : blocage potentiel du régime oscillatoire
- **Correction** : définir dans le Référentiel les critères déterministes d'une "session de consolidation satisfaisante" (ex. : au moins 1 item P validé, ou composante A ≥ 1 réussite sans aide).

---

*Rapport produit en application stricte du prompt `Challenge_constitution.md` — aucun patch YAML proposé à ce stade.*
