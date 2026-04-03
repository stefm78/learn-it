# ARBITRAGE — Constitution Pipeline STAGE_02_ARBITRAGE

**Arbitre :** Claude (sans mode thinking étendu)
**Date :** 2026-04-01
**Pipeline :** constitution
**Stage :** STAGE_02_ARBITRAGE
**Périmètre :** consolidation de 6 rapports de challenge STAGE_01

---

## Résumé exécutif

L'arbitrage consolide **7 rapports de challenge** (`challenge_NemoTron.md`, `challenge_report_01_ClaudeThink.md`, `challenge_report_01_ClaudeWoThink.md`, `challenge_report_01_GPTThink.md`, `challenge_report_01_sonar.md`, `challenge_report_GPTwoThink.md`, `challenge_report_Gemini.md`) couvrant 3 Cores : Constitution V1.9, Référentiel V1.0, LINK V1.9/V1.0.

**Décisions globales :**
- `corriger_maintenant` : **14 points**
- `reporter` : **7 points**
- `rejeter` : **3 points**
- `hors_perimetre` : **2 points**

Les 14 corrections immédiates couvrent les risques critiques et élevés structurellement vérifiables et opérationnellement ciblés. Les reportés concernent des chantiers structurants à périmètre large (versioning inter-Core, gouvernance LINK synchrone, refonte partielle). Les rejetés correspondent à des pseudo-risques ou à des reformulations éditoriales sans impact moteur.

---

## Périmètre analysé

### Fichiers de challenge considérés
- `challenge_NemoTron.md`
- `challenge_report_01_ClaudeThink.md`
- `challenge_report_01_ClaudeWoThink.md`
- `challenge_report_01_GPTThink.md`
- `challenge_report_01_sonar.md`
- `challenge_report_GPTwoThink.md`
- `challenge_report_Gemini.md` *(lu en contexte, synthèse intégrée)*

### Notes humaines
Aucune note humaine fournie pour ce run.

### Limites de périmètre
- Le LINK est fourni dans le corpus de certains challengers (NemoTron) mais pas de tous. Les constats LINK de NemoTron sont arbitrés avec attention ; les constats des challengers sans LINK sont traités sous réserve.
- Le document d'arbitrage `[ARBITRAGE_2026_04_01]` n'est pas accessible dans le workspace courant. Les éléments ayant pour source_anchor `[ARBITRAGE_2026_04_01]` sont traités comme élément actuel de la Constitution — leur remise en cause structurelle est hors périmètre.

---

## Arbitrage détaillé

---

### Point ARB-01 — Binding LINK manquant : `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

- **Source(s) :** NemoTron [AX1-01 CRITIQUE], ClaudeWoThink [MOD-01], ClaudeThink [F1.1], sonar [1.1 modéré], GPTwoThink [F-1.4 élevée]
- **Constat synthétique :** L'EVENT constitutionnel dépend d'un seuil référentiel (`PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`) mais aucun `TYPE_BINDING` dans le LINK ne matérialise cette résolution. La dépendance est déclarative (human_readable) mais non structurelle. Un moteur ne peut pas résoudre le seuil de façon déterministe, ce qui viole le principe de fermeture locale.
- **Nature :** structurelle, intercore_reference
- **Gravité :** critique (NemoTron) à modérée (autres) — alignement sur critique compte tenu de l'impact moteur
- **Impact :** applicabilité runtime, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Risque d'état indéfini runtime sur un mécanisme central (détection de divergence MSC/perception). Correction additive et ciblée dans le LINK. Impact_scope faible.
- **Conséquence pour le patch :** Ajouter `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` dans le LINK, bindant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` vers `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`.

---

### Point ARB-02 — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` non déclaré

- **Source(s) :** ClaudeWoThink [HIGH-01, A1-2, A3-1], ClaudeThink [F1.2 ÉLEVÉ]
- **Constat synthétique :** Le paramètre référentiel `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` cite `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans son human_readable et dans sa logique d'escalade, mais cet event n'est défini dans aucun bloc EVENTS de la Constitution, du Référentiel ou du LINK. L'escalade constitue un puits sans sortie formalisée.
- **Nature :** structurelle, runtime_state
- **Gravité :** élevée
- **Impact :** applicabilité moteur, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Event référencé mais absent = état moteur non atteignable. Correction additive (déclarer l'event et une action/rule de traitement).
- **Conséquence pour le patch :** Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel (couche appropriée = détection hors-session) avec une `ACTION` ou une `RULE` de traitement associée (escalade vers la chaîne d'analyse design). Ancrer dans le LINK si nécessaire.

---

### Point ARB-03 — Régime oscillatoire `Consolidation/Exploration` sans borne de durée ni sortie de secours

- **Source(s) :** ClaudeWoThink [HIGH-02, A1-4, A3-2]
- **Constat synthétique :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` décrit un régime oscillatoire dont la condition de sortie est `R atteint`. Aucune borne temporelle maximale ni compteur de cycles n'est déclaré. Si R n'est jamais atteint, le régime est potentiellement infini, bloquant la progression vers les KU dépendantes.
- **Nature :** structurelle, runtime_state
- **Gravité :** élevée
- **Impact :** applicabilité moteur, maintenabilité
- **Décision :** `corriger_maintenant`
- **Justification :** État de boucle ouverte à impact direct sur la trajectoire apprenant. Correction minimale : ajouter un paramètre référentiel de borne maximale de cycles.
- **Conséquence pour le patch :** Ajouter `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` dans le Référentiel, et une condition de sortie de secours dans `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (retour en mode conservateur après N cycles si R non atteint).

---

### Point ARB-04 — Maîtrise provisoire : expiration de fenêtre sans event ni rule de traitement

- **Source(s) :** ClaudeWoThink [HIGH-03, A3-3], ClaudeThink [F1.4 MODÉRÉ], sonar [2.2 MODÉRÉ], GPTwoThink [5.1 MODÉRÉ]
- **Constat synthétique :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` déclare une fenêtre de vérification de la maîtrise provisoire héritée, mais l'expiration de cette fenêtre sans confirmation ne génère aucun EVENT déclaré. Aucune règle ne définit si la maîtrise doit être révoquée, maintenue ou escaladée.
- **Nature :** structurelle, runtime_evaluation
- **Gravité :** modérée à élevée selon l'impact apprenant
- **Impact :** applicabilité moteur, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Incohérence silencieuse du modèle apprenant. Correction ciblée : déclarer l'event d'expiration et une règle de traitement.
- **Conséquence pour le patch :** Déclarer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` dans la Constitution + `RULE_PROVISIONAL_MASTERY_EXPIRED_TRIGGERS_DIAGNOSTIC` associée (logique : déclenche une session diagnostique courte, ou rétrogradation conservative si aucune session diagnostique disponible). Paramètre de durée à borner dans le Référentiel si absent.

---

### Point ARB-05 — `INV_MSC_AND_STRICT` : comportement indéfini si une composante MSC est non-calculable

- **Source(s) :** sonar [RISK-02 CRITIQUE], GPTThink [C-02 ÉLEVÉ], GPTwoThink [F-2.2 ÉLEVÉE]
- **Constat synthétique :** Si R est non-observable (première session, apprenant nouveau) ou une autre composante est `unknown`, le AND strict ne peut être évalué. La Constitution ne définit pas si la maîtrise résultante est `false`, `unknown`, ou `deferred`. Cette ambiguïté peut provoquer des oscillations de trajectoire et des implémentations divergentes.
- **Nature :** structurelle, runtime_evaluation
- **Gravité :** critique (sonar), élevée (autres)
- **Impact :** applicabilité, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Ambiguïté fondamentale sur l'invariant central du système (MSC AND strict). Correction minimale : préciser que si une composante est `unknown`, la maîtrise est `deferred` (non `false` pour ne pas pénaliser l'apprenant, non `true` pour préserver la rigueur).
- **Conséquence pour le patch :** Ajouter dans `INV_MSC_AND_STRICT` (ou en invariant complémentaire) : si P, R ou A est `unknown` (non calculable), l'état MSC est `deferred` et non indéterminé. Définir l'état `deferred` dans `TYPE_MASTERY_MODEL`.

---

### Point ARB-06 — Comportement composite indéfini si plusieurs axes learner state sont simultanément `unknown`

- **Source(s) :** sonar [RISK-01 CRITIQUE], GPTThink [C-03 ÉLEVÉ], ClaudeThink [F3.1 CRITIQUE]
- **Constat synthétique :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise chaque axe à rester `unknown` indépendamment, mais aucune règle constitutionnelle ne couvre le comportement combiné quand ≥2 axes sont simultanément `unknown`. Les règles conservatrices mono-axe ne se composent pas en règle composite documentée.
- **Nature :** structurelle, runtime_evaluation
- **Gravité :** critique
- **Impact :** applicabilité moteur, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Comportement composite indéfini sur des chemins courants (apprenants nouveaux, absence d'AR-N1 + VC non observée). Correction minimale : ajouter un invariant ou une règle composite.
- **Conséquence pour le patch :** Ajouter `INV_MULTI_AXIS_UNKNOWN_CONSERVATIVE_MAXIMUM` (ou équivalent) : si ≥2 axes sont simultanément `unknown`, la réponse moteur est la réponse conservatrice maximale définie (scaffolding léger réversible + inhibition des actions adaptatives non-sûres). Pas de compositing implicite.

---

### Point ARB-07 — Composante T : absence de déclencheur d'évaluation et d'EVENT `T_overdue`

- **Source(s) :** NemoTron [AX1-02 ÉLEVÉ], ClaudeThink [F1.3 ÉLEVÉ], sonar [RISK-07 MODÉRÉ], GPTwoThink [F-1.1 ÉLEVÉE]
- **Constat synthétique :** T est constitutionnellement séparée de la maîtrise de base, mais aucune règle ne définit quand une évaluation T est déclenchée après l'établissement de la maîtrise de base, ni ce que le moteur fait si T n'est jamais évaluée. L'état `unknown` de T est silencieusement stable.
- **Nature :** structurelle, logique
- **Gravité :** élevée
- **Impact :** applicabilité pédagogique, gouvernance
- **Décision :** `corriger_maintenant`
- **Justification :** T est une composante active du modèle MSC. Son cycle de vie non gouverné est une lacune réelle. Correction additive et ciblée.
- **Conséquence pour le patch :** Déclarer `EVENT_T_EVALUATION_OVERDUE` dans la Constitution (déclencheur : maîtrise de base établie depuis N sessions sans évaluation T). Ajouter `RULE_T_EVALUATION_SCHEDULE` décrivant comment le moteur planifie une session d'évaluation de transfert. Paramètres de fenêtre dans le Référentiel.

---

### Point ARB-08 — Seuils Référentiel sans fallback constitutionnel si le Référentiel est absent ou invalide

- **Source(s) :** GPTThink [C-01 CRITIQUE], GPTwoThink [F-1.3 CRITIQUE], sonar [RISK-03 ÉLEVÉ], ClaudeThink [F1.1], ClaudeWoThink [A1-3]
- **Constat synthétique :** La Constitution délègue de nombreux seuils critiques au Référentiel (divergence MSC, profil AR-réfractaire, VC basse persistante, interruption longue) sans définir le comportement de défaut constitutionnel si le Référentiel ne fournit pas ces valeurs (absent, invalide, version incompatible).
- **Nature :** structurelle, gouvernance, sécurité logique
- **Gravité :** critique
- **Impact :** sécurité logique, applicabilité, stabilité du système
- **Décision :** `corriger_maintenant`
- **Justification :** Le risque d'état moteur indéfini sur des décisions critiques est systémique. Correction minimale : ajouter un invariant de défaut constitutionnel.
- **Conséquence pour le patch :** Ajouter `INV_MISSING_REFERENTIEL_THRESHOLD_FORCES_CONSERVATIVE_FALLBACK` : si un seuil attendu du Référentiel est absent ou invalide, le moteur adopte le comportement conservateur le plus restrictif défini pour le contexte (scaffolding léger, inhibition des actions adaptatives, log de l'anomalie). Pas de comportement par inférence implicite.

---

### Point ARB-09 — Détresse activation persistante : absence de protocole d'escalade constitutionnel

- **Source(s) :** sonar [RISK-06 ÉLEVÉ], GPTwoThink [F-2.2 indirect]
- **Constat synthétique :** La Constitution traite la détresse par `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` (scaffolding conservateur), mais aucun mécanisme ne prévoit une escalade si la détresse activation persiste sur N sessions consécutives malgré le scaffolding. Il y a une asymétrie avec `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` qui, elle, escalade la divergence MSC persistante.
- **Nature :** structurelle, logique
- **Gravité :** élevée
- **Impact :** applicabilité pédagogique, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Asymétrie documentée avec une règle existante. Correction par symétrie avec le protocole de divergence MSC.
- **Conséquence pour le patch :** Ajouter `RULE_PERSISTENT_ACTIVATION_DISTRESS_ESCALATION` : si l'axe Activation reste en détresse sur N sessions consécutives (paramètre référentiel) malgré le scaffolding, déclencher une escalade hors-session vers la chaîne d'analyse design. Paramètre de seuil N dans le Référentiel.

---

### Point ARB-10 — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` : scope du flagging misconception ambigu

- **Source(s) :** sonar [RISK-05 ÉLEVÉ], GPTwoThink [F-4.1 MODÉRÉ], ClaudeWoThink [A4-1 MODÉRÉ], NemoTron [indirect]
- **Constat synthétique :** La règle se déclenche sur une KU flaggée `misconception` mais le processus de flagging n'est pas contraint dans la Constitution. Si ce flagging est réalisé par inférence IA en runtime, il viole `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`. Le `scope: design_runtime` laisse un espace d'ambiguïté.
- **Nature :** structurelle, dépendance IA implicite
- **Gravité :** élevée
- **Impact :** sécurité logique, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** L'ambiguïté scope peut légitimer une inférence runtime non autorisée. Clarification constitutionnelle minimale et non-régressive.
- **Conséquence pour le patch :** Ajouter dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` ou dans `TYPE_KNOWLEDGE_UNIT` une contrainte explicite : le flag `misconception` est un attribut de design exclusivement — posé par un humain ou un outil d'analyse off-session autorisé. Jamais inféré en runtime.

---

### Point ARB-11 — `RULE_UNVERIFIED_GAMIFICATION_PROBATION` : absence de condition de sortie du mode probatoire

- **Source(s) :** NemoTron [AX1-03 MODÉRÉ], GPTThink [C-12 MODÉRÉ], ClaudeThink [F2.2 indirect]
- **Constat synthétique :** Le mode probatoire de gamification est déclenché mais aucun mécanisme ne définit la durée maximale, les critères de validation ou l'escalade si la gamification reste en mode probatoire indéfiniment.
- **Nature :** structurelle, logique
- **Gravité :** modérée
- **Impact :** applicabilité moteur
- **Décision :** `corriger_maintenant`
- **Justification :** Boucle ouverte identique à ARB-03. Correction additive ciblée.
- **Conséquence pour le patch :** Ajouter `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS` dans le Référentiel. Ajouter dans `RULE_UNVERIFIED_GAMIFICATION_PROBATION` une condition de sortie automatique : après N sessions sans effet négatif mesuré, passage au mode validé + log.

---

### Point ARB-12 — `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` : canal d'escalade indéfini

- **Source(s) :** NemoTron [AX1-04 MODÉRÉ], GPTThink [C-04 ÉLEVÉ]
- **Constat synthétique :** L'invariant déclare une escalade obligatoire mais ne précise ni la cible, ni le format, ni le délai maximal. Il est déclaratif mais inopérant en runtime.
- **Nature :** structurelle, gouvernance
- **Gravité :** modérée à élevée
- **Impact :** applicabilité, maintenabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Invariant déclaratif non exécutable. Correction minimale : définir les attributs du signal d'escalade dans la Constitution.
- **Conséquence pour le patch :** Modifier `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` pour déclarer les attributs minimaux du signal : format log structuré, délai maximal (référentiel), cible = canal d'analyse externe. Ou déléguer explicitement au Référentiel via un binding LINK dédié.

---

### Point ARB-13 — Graphe de KU : `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ne couvre pas les mises à jour incrémentielles

- **Source(s) :** GPTwoThink [F-1.2 CRITIQUE], GPTThink [C-07 MODÉRÉ]
- **Constat synthétique :** L'invariant protège la construction initiale du graphe mais pas les mises à jour incrémentielles post-chargement. Un patch de graphe peut réintroduire un cycle sans déclencher l'invariant.
- **Nature :** structurelle, logique
- **Gravité :** critique (GPTwoThink)
- **Impact :** sécurité logique, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Lacune de couverture sur un invariant de sécurité fondamental. Correction minimale : étendre le trigger de l'invariant.
- **Conséquence pour le patch :** Étendre `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` pour inclure `validation post-patch de graphe` dans son trigger, en plus de la validation initiale. Ou ajouter `INV_KNOWLEDGE_GRAPH_PATCH_REQUIRES_ACYCLICITY_RECHECK` dédié.

---

### Point ARB-14 — `TYPE_FEEDBACK_COVERAGE_MATRIX` : obligation non étendue aux KU perceptuelles

- **Source(s) :** GPTwoThink [F-2.4 MODÉRÉ]
- **Constat synthétique :** La matrice de couverture feedback est obligatoire pour les KU formelles et procédurales, mais les KU perceptuelles ne sont pas listées dans la condition — alors qu'`INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` les traite au même niveau sur le plan du traitement multimodal.
- **Nature :** logique, cohérence interne
- **Gravité :** modérée
- **Impact :** applicabilité, cohérence documentaire
- **Décision :** `corriger_maintenant`
- **Justification :** Incohérence entre deux invariants. Correction éditoriale minimale.
- **Conséquence pour le patch :** Étendre la condition d'obligation de `TYPE_FEEDBACK_COVERAGE_MATRIX` aux KU perceptuelles, en alignement avec `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL`.

---

### Point ARB-15 — AR-N3 orphelin : consommation constitutionnelle non définie

- **Source(s) :** GPTThink [C-06 MODÉRÉ], sonar [indirect], GPTwoThink [indirect]
- **Constat synthétique :** `TYPE_SELF_REPORT_AR_N3` est déclaré et collecté mais aucune règle constitutionnelle ne définit ce que le moteur fait de l'indice de calibration AR-N3. Le LINK porte un binding AR-N3 → axe Calibration, mais la Constitution ne déclare pas la consommation.
- **Nature :** logique, gouvernance
- **Gravité :** modérée
- **Impact :** maintenabilité, compréhension
- **Décision :** `reporter`
- **Justification :** Le binding LINK couvre partiellement la consommation. La correction complète (déclarer la consommation constitutionnelle ou le déléguer formellement au Référentiel) mérite un arbitrage plus approfondi avec le LINK visible. Impact moteur immédiat limité.

---

### Point ARB-16 — Dégradation de la composante R non déclarée constitutionnellement

- **Source(s) :** GPTThink [C-02 ÉLEVÉ], NemoTron [AX2-01 MODÉRÉ]
- **Constat synthétique :** R qualifie la robustesse temporelle mais la Constitution ne déclare pas explicitement que R est soumis à une décroissance temporelle. Un moteur conforme peut maintenir R constant indéfiniment.
- **Nature :** logique, solidité théorique
- **Gravité :** élevée
- **Impact :** applicabilité pédagogique
- **Décision :** `reporter`
- **Justification :** La décroissance de R est pédagogiquement fondée mais sa formalisation constitutionnelle est un chantier structurant qui dépasse le périmètre d'un patch minimal. À inscrire dans le prochain cycle de patch après réflexion sur les paramètres de dégradation.

---

### Point ARB-17 — Compatibilité de version inter-Core : absence de mécanisme de release coordonnée

- **Source(s) :** sonar [RISK-03], GPTwoThink [F-5.3 ÉLEVÉE], GPTThink [C-14], NemoTron [AX5-01]
- **Constat synthétique :** La Constitution référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` fixée à V1_0, marquée `patchable: false`. Aucun mécanisme constitutionnel de release coordonnée n'est défini. Une promotion du Référentiel en V1_1 ne peut pas être couverte par un patch simple.
- **Nature :** gouvernance, versioning
- **Gravité :** élevée
- **Impact :** maintenabilité, stabilité documentaire
- **Décision :** `reporter`
- **Justification :** Chantier de gouvernance inter-Core qui dépasse le périmètre d'un patch correctif. Nécessite une spécification dédiée. À inscrire comme sujet prioritaire du prochain cycle de gouvernance.

---

### Point ARB-18 — Boucle sémantique `TYPE_INTEGRITY_MODES` ↔ `TYPE_SESSION_INTEGRITY_SCORE` ↔ `TYPE_NC_MSC`

- **Source(s) :** sonar [RISK-04 ÉLEVÉ]
- **Constat synthétique :** La logique sémantique crée une boucle : mode d'intégrité → SIS → NC-MSC → décisions moteur → contexte mode d'intégrité. Ce n'est pas un cycle YAML interdit mais un état oscillant potentiel au niveau moteur.
- **Nature :** logique, runtime_evaluation
- **Gravité :** élevée
- **Impact :** sécurité logique
- **Décision :** `reporter`
- **Justification :** La boucle est sémantique, pas structurelle dans le YAML. Son traitement nécessite une analyse approfondie du moteur runtime, hors périmètre d'un patch documentaire. À soumettre à analyse de conception moteur séparée.

---

### Point ARB-19 — Gouvernance du LINK : absence de politique constitutionnelle de gouvernance

- **Source(s) :** sonar [RISK-09 MODÉRÉ], NemoTron [AX1-05 MODÉRÉ]
- **Constat synthétique :** La Constitution déclare la séparation Constitution/Référentiel mais ne mentionne pas le LINK comme entité soumise à des règles constitutionnelles de gouvernance. Aucun invariant n'exige un patch LINK synchrone lors d'un patch Constitution modifiant des bindings inter-Core.
- **Nature :** gouvernance, structurelle
- **Gravité :** modérée
- **Impact :** maintenabilité, gouvernance
- **Décision :** `reporter`
- **Justification :** Important mais chantier de gouvernance inter-Core. Lié à ARB-17. Reporter au même cycle de gouvernance.

---

### Point ARB-20 — Densité cumulée des sollicitations AR-N* non bornée constitutionnellement

- **Source(s) :** GPTThink [C-08 MODÉRÉ], GPTwoThink [F-2.1 FAIBLE], ClaudeThink [F2.1 MODÉRÉ]
- **Constat synthétique :** Il n'existe pas de règle constitutionnelle bornant la fréquence cumulée de toutes les sollicitations AR par session. Un moteur conforme peut saturer l'apprenant avec des micro-sondages.
- **Nature :** logique, charge cognitive
- **Gravité :** modérée
- **Impact :** applicabilité pédagogique
- **Décision :** `reporter`
- **Justification :** Réel mais non critique en l'état actuel (les budgets par type AR-N* existent déjà). Borne cumulative nécessite une calibration empirique. Reporter au prochain cycle de paramétrie.

---

### Point ARB-21 — `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` sans paramètre numérique de durée dans le Référentiel

- **Source(s) :** ClaudeWoThink [MOD-02, A2-1], GPTwoThink [F-5.1]
- **Constat synthétique :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est constitutionnel mais sa valeur opérationnelle numérique n'est pas définie dans le Référentiel. Inclus dans ARB-04 pour la maîtrise provisoire. Pour les autres fenêtres sans valeur numérique : reporter.
- **Nature :** logique, paramétrie
- **Gravité :** modérée
- **Impact :** applicabilité
- **Décision :** `reporter`
- **Justification :** Les bornes numériques manquantes sur les fenêtres de paramètres patchables seront traitées lors de la prochaine révision du Référentiel. Non bloquant si la fenêtre dispose d'un comportement de défaut conservateur.

---

### Point ARB-22 — `source_anchor: [ARBITRAGE_2026_04_01]` hétérogène (non normalisé en [Sxx])

- **Source(s) :** GPTThink [C-16 FAIBLE], sonar [1.1 MODÉRÉ]
- **Constat synthétique :** Plusieurs éléments portent `source_anchor: '[ARBITRAGE_2026_04_01][...]'` au lieu d'une ancre `[Sxx]` normalisée. Hétérogénéité de traçabilité.
- **Nature :** éditoriale, traçabilité
- **Gravité :** faible
- **Impact :** maintenabilité
- **Décision :** `rejeter`
- **Justification :** La convention d'ancrage par arbitrage daté est délibérée et correcte — elle trace l'origine des éléments introduits par arbitrage. La normalisation en `[Sxx]` n'est appropriée que pour les sources primaires constitutionnelles. Pas de risque moteur.

---

### Point ARB-23 — Dépendance circulaire T ↔ `TYPE_MASTERY_MODEL` (ordre de résolution)

- **Source(s) :** GPTThink [C-15 FAIBLE], GPTwoThink [F-1.1 ÉLEVÉE — version spécifique : relation `governs` manquante]
- **Constat synthétique :** Deux lectures divergentes : GPTThink qualifie la dépendance T ↔ MasteryModel de circulaire faible (sémantique, pas d'instanciation). GPTwoThink signale que `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` n'est pas traversable depuis `TYPE_MASTERY_MODEL` via les relations.
- **Nature :** structurelle (relation manquante), logique (ordre résolution)
- **Gravité :** faible à modérée selon la lecture
- **Impact :** compréhension, applicabilité éventuelle
- **Décision :** `corriger_maintenant` pour la relation manquante (version GPTwoThink) / `rejeter` pour la circularité d'ordre de résolution (version GPTThink)
- **Justification :** La relation `governs` manquante entre `TYPE_MASTERY_MODEL` et `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` est une lacune réelle de traversabilité des relations. La circularité YAML est semantiquement normale. Correction minimale : ajouter la relation.
- **Conséquence pour le patch (partie corriger_maintenant) :** Ajouter dans `TYPE_MASTERY_MODEL` une relation `governs → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` pour rendre la contrainte de séparation de T traversable depuis le type racine.

---

### Point ARB-24 — Registre structuré des patches appliqués absent

- **Source(s) :** GPTThink [C-17 FAIBLE]
- **Constat synthétique :** Les patches appliqués sont traçables via les `source_anchor` mais pas via un bloc structuré `APPLIED_PATCHES` dans le Core.
- **Nature :** gouvernance, traçabilité
- **Gravité :** faible
- **Impact :** maintenabilité
- **Décision :** `hors_perimetre`
- **Justification :** La traçabilité par `source_anchor` est la convention documentaire en vigueur. Un registre `APPLIED_PATCHES` est une amélioration gouvernance à inscrire dans la spécification du Core DSL, pas dans un patch correctif Constitution.

---

### Point ARB-25 — ICC (`TYPE_CORPUS_CONFIDENCE_ICC`) : seuil minimal de déploiement non défini constitutionnellement

- **Source(s) :** GPTwoThink [F-4.2 MODÉRÉ]
- **Constat synthétique :** L'ICC qualifie la confiance d'analyse mais les critères de calcul et le seuil minimal de déploiement autorisé sont entièrement délégués. Un ICC très bas peut autoriser un déploiement pédagogiquement non fiable sans invariant constitutionnel bloquant.
- **Nature :** logique, dépendance IA implicite
- **Gravité :** modérée
- **Impact :** sécurité logique
- **Décision :** `hors_perimetre`
- **Justification :** L'ICC est un concept d'analyse et de design. Sa formalisation constitutionnelle implique de définir une sémantique de calcul qui dépasse le périmètre du Core gouvernance. À traiter dans les spécifications d'analyse.

---

## Points consolidés

### Regroupements effectués

- **ARB-01 + ARB-08** : deux faces du même problème de délégation implicite Référentiel. ARB-01 est la correction ciblée sur un binding LINK précis ; ARB-08 est la correction systémique via invariant de fallback.
- **ARB-02 + ARB-12** : events ou canaux manquants sur des mécanismes d'escalade. Traités séparément car ARB-02 = event moteur absent, ARB-12 = canal d'escalade non défini sur un invariant existant.
- **ARB-03 + ARB-11** : boucles ouvertes sans condition de sortie. Traités séparément car couches distinctes (régime osciltatoire = Référentiel, gamification probatoire = Constitution + Référentiel).
- **ARB-04 + ARB-21** : maîtrise provisoire. ARB-04 couvre l'expiration sans traitement (correction immédiate) ; ARB-21 couvre les bornes numériques manquantes (reporter).

### Doublons fusionnés

- La faille `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → seuil Référentiel apparaît dans 5 challengers sous des angles différents. Arbitrage unique ARB-01 couvre le binding LINK + ARB-08 couvre le fallback systémique.
- La composante T orpheline apparaît dans ClaudeThink, NemoTron, GPTwoThink avec des nuances (déclencheur, relation manquante, cycle de vie). Traité via ARB-07 (cycle de vie) + ARB-23 (relation manquante).

### Contradictions entre rapports résolues

- **Sévérité du binding LINK MSC/perception :** NemoTron = CRITIQUE ; ClaudeWoThink = MODÉRÉ. Arbitrage : CRITIQUE retenu compte tenu du risque moteur d'état indéfini.
- **Dépendance T ↔ MasteryModel :** GPTThink = FAIBLE (circulaire mais sémentiquement justifiée) ; GPTwoThink = ÉLEVÉE (relation manquante dans les `relations`). Résolution : les deux lectures sont compatibles — la circularité est normale (rejeter), la relation manquante est réelle (corriger).

---

## Décisions à transmettre au patch

| Priorité | ID arbitrage | Couche(s) cible | Description courte |
|---|---|---|---|
| CRITIQUE | ARB-05 | Constitution | `INV_MSC_AND_STRICT` : définir `deferred` si composante `unknown` |
| CRITIQUE | ARB-06 | Constitution | Invariant composite multi-axe `unknown` |
| CRITIQUE | ARB-08 | Constitution | `INV_MISSING_REFERENTIEL_THRESHOLD_FORCES_CONSERVATIVE_FALLBACK` |
| CRITIQUE | ARB-13 | Constitution | Étendre `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` aux mises à jour incrémentielles |
| ÉLEVÉ | ARB-01 | LINK | Binding `MSC_PERCEPTION_DIVERGENCE` → `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` |
| ÉLEVÉ | ARB-02 | Référentiel + Constitution | Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` + rule associée |
| ÉLEVÉ | ARB-03 | Référentiel | `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` + condition de sortie de secours |
| ÉLEVÉ | ARB-04 | Constitution + Référentiel | `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` + rule de traitement |
| ÉLEVÉ | ARB-07 | Constitution + Référentiel | `EVENT_T_EVALUATION_OVERDUE` + `RULE_T_EVALUATION_SCHEDULE` |
| ÉLEVÉ | ARB-09 | Constitution + Référentiel | `RULE_PERSISTENT_ACTIVATION_DISTRESS_ESCALATION` |
| ÉLEVÉ | ARB-10 | Constitution | Contrainte explicite : flag `misconception` = design only, jamais runtime |
| MODÉRÉ | ARB-11 | Référentiel + Constitution | `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS` + condition de sortie |
| MODÉRÉ | ARB-12 | Constitution | Attributs minimaux du signal d'escalade pour dérive persistante |
| MODÉRÉ | ARB-14 | Constitution | Étendre `TYPE_FEEDBACK_COVERAGE_MATRIX` aux KU perceptuelles |
| MODÉRÉ | ARB-23 | Constitution | Relation `governs → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` dans `TYPE_MASTERY_MODEL` |

### Contraintes de minimalité pour le patch
- Toutes les corrections sont additives sauf ARB-05 (modification d'invariant existant), ARB-10 (ajout d'une contrainte dans un type ou une rule existante), ARB-13 (extension du trigger d'un invariant existant), ARB-23 (ajout d'une relation dans un type existant).
- Aucune correction ne déplace de logique métier entre couches.
- Les nouvelles déclarations dans le LINK (ARB-01) ne doivent pas introduire de logique métier autonome.

---

## Décisions explicitement non retenues

### Reportées

| ID | Raison du report |
|---|---|
| ARB-15 (AR-N3 orphelin) | Binding LINK partiel couvre le besoin immédiat ; correction complète nécessite LINK visible |
| ARB-16 (Dégradation R) | Chantier structurant pédagogique, hors périmètre patch minimal |
| ARB-17 (Versioning inter-Core) | Chantier gouvernance inter-Core dédié requis |
| ARB-18 (Boucle intégrité) | Analyse de conception moteur runtime requise, hors patch documentaire |
| ARB-19 (Gouvernance LINK) | Lié à ARB-17 ; traiter ensemble |
| ARB-20 (Densité AR cumulative) | Calibration empirique requise ; budgets par type existent déjà |
| ARB-21 (Bornes numériques fenêtres) | Non bloquant si fallback conservateur en place ; révision Référentiel à part |

### Rejetées

| ID | Raison du rejet |
|---|---|
| ARB-22 (source_anchor hétérogène) | Convention délibérée et correcte ; pas de risque moteur |
| ARB-23 (circularité T ↔ MasteryModel — version ordre résolution) | Circulaire sémantiquement justifié ; pas de cycle YAML |

### Hors périmètre

| ID | Raison |
|---|---|
| ARB-24 (Registre APPLIED_PATCHES) | Amélioration Core DSL, pas patch correctif Constitution |
| ARB-25 (ICC seuil minimal) | Sémantique de calcul appartient aux specs d'analyse |
