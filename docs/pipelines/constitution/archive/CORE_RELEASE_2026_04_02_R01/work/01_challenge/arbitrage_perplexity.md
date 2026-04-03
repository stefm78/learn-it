# ARBITRAGE — Constitution CORE_LEARNIT_CONSTITUTION_V1_9
<!-- stage: STAGE_02_ARBITRAGE -->
<!-- arbitre: perplexity -->
<!-- date: 2026-04-01 -->
<!-- sources: challenge_NemoTron.md | challenge_report_01_ClaudeThink.md | challenge_report_01_ClaudeWoThink.md | challenge_report_01_GPTThink.md | challenge_report_GPTwoThink.md | challenge_report_Gemini.md | challenge_report_01_sonar.md -->

---

## Périmètre d'arbitrage

Cet arbitrage consolide les 7 rapports de challenge produits lors du STAGE_01_CHALLENGE sur `CORE_LEARNIT_CONSTITUTION_V1_9`. Il statue sur chaque finding selon le statut : **RETENU**, **REJETÉ**, **DIFFÉRÉ**, ou **HORS_SCOPE**.

Chaque décision est catégorisée par couche cible (`Constitution`, `Référentiel`, `LINK`, `Gouvernance`) et par priorité de patch (`P1` = critique bloquant · `P2` = élevé · `P3` = modéré · `P4` = faible).

---

## Consolidation des findings convergents

Cinq familles de risques ont été soulevées de façon convergente par ≥ 3 rapporteurs. Elles sont traitées en premier.

---

### FC-01 — Notification externe de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` potentiellement déclenchée en runtime

**Sources :** Gemini (CRITIQUE-01), ClaudeThink (F3.2 partiel), GPTwoThink (F-1.4 partiel)

**Constat consolidé :** Le step 2 de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` prévoit une *"notification externe obligatoire"*. Or `INV_RUNTIME_FULLY_LOCAL` interdit tout appel réseau pendant une session apprenant active. L'absence de contrainte de scope hors-session sur ce step crée un conflit d'invariant primaire.

**Décision : RETENU — P1**

Correction : Ajouter dans la logique de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` une condition explicite `scope: post_session_only` pour le step d'escalade. La notification doit être produite comme artefact de fin de session, pas déclenchée en temps réel.

**Couche :** Constitution

---

### FC-02 — Dépendances seuils référentiels sans fallback constitutionnel

**Sources :** GPTThink (C-01 CRITIQUE), GPTwoThink (F-1.3 CRITIQUE), Gemini (ÉLEVÉ-01), NemoTron (AX1-01 CRITIQUE), ClaudeThink (F1.1 CRITIQUE partiel), ClaudeWoThink (partiel), sonar (RISK-03)

**Constat consolidé :** Plusieurs éléments constitutionnels (`TYPE_MASTERY_COMPONENT_P/R/A`, `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) délèguent leurs seuils au Référentiel sans aucun invariant de présence obligatoire du Référentiel avant évaluation, ni borne plancher constitutionnelle.

**Décision : RETENU — P1**

Correction : Introduire un invariant `INV_REFERENTIEL_REQUIRED_BEFORE_THRESHOLD_EVALUATION` stipulant que le Référentiel doit être chargé et compatible avant toute évaluation d'un seuil délégué. En absence du Référentiel, le moteur bascule en comportement conservateur global (non en état indéterminé).

**Couche :** Constitution

---

### FC-03 — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` non déclaré

**Sources :** NemoTron (implicite), ClaudeThink (F1.2 ÉLEVÉ), ClaudeWoThink (HIGH-01 ÉLEVÉ + A3-1), GPTThink (dérivé de C-03), GPTwoThink (partiel)

**Constat consolidé :** Le paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` fait référence à `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans son human_readable, mais cet event n'est déclaré dans aucun bloc EVENTS de la Constitution ni du Référentiel. Le moteur ne peut pas l'activer. Le puits conservateur est sans sortie formalisée après N sessions.

**Décision : RETENU — P1**

Correction : Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel, câblé à une action d'escalade hors session (notification externe, checkpoint humain selon le régime d'autonomie). Le scope doit être `runtime_state` / `patch_governance`.

**Couche :** Référentiel

---

### FC-04 — Composante T orpheline (déclencheur d'évaluation absent, binding LINK manquant)

**Sources :** NemoTron (AX1-02 ÉLEVÉ), ClaudeThink (F1.3 ÉLEVÉ), ClaudeWoThink (A4-2), GPTThink (partiel), GPTwoThink (F-1.1 ÉLEVÉ — relation manquante `TYPE_MASTERY_MODEL → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`)

**Constat consolidé :**
- Aucune règle ne définit quand/comment une évaluation de T est déclenchée après maîtrise de base acquise.
- `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` n'est pas référencé depuis `TYPE_MASTERY_MODEL` (relation non traversable).
- Aucun EVENT ne couvre le cas `T_never_evaluated`.

**Décision : RETENU — P2**

Corrections à arbitrer :
- (a) Ajouter une relation `TYPE_MASTERY_MODEL → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` pour rendre la contrainte traversable.
- (b) Déclarer un `EVENT_T_EVALUATION_OVERDUE` déclenché après N sessions post-maîtrise de base sans évaluation T, paramétré par le Référentiel.
- (c) Décider si T reçoit un binding LINK minimal ou reste constitutionnellement non lié — documenter explicitement la décision.

**Couche :** Constitution (a, b), LINK (c à statuer)

---

### FC-05 — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ne couvre pas les modifications incrémentielles post-chargement

**Sources :** GPTwoThink (F-1.2 CRITIQUE), GPTThink (C-07 MODÉRÉ), Gemini (AX5-D FAIBLE)

**Constat consolidé :** Le trigger actuel est `Validation design ou chargement du graphe`. Un patch de graphe après chargement initial peut réintroduire un cycle sans déclencher l'invariant.

**Décision : RETENU — P2**

Correction : Étendre le trigger de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` à `Validation design, chargement du graphe, ou modification incrémentielle du graphe par patch`. Déclarer un `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` associé à une `ACTION_BLOCK_GRAPH_LOAD`.

**Couche :** Constitution

---

## Findings additionnels retenus (convergence ≥ 2 rapporteurs ou sévérité solitaire critique)

---

### FA-01 — Oscillation `unknown` persistant sans transition constitutionnelle

**Sources :** Gemini (CRITIQUE-02), GPTThink (C-03 ÉLEVÉ), sonar (RISK-01 CRITIQUE)

**Constat :** Si ≥ 1 axe learner state reste `unknown` pendant plusieurs sessions consécutives avec patch bloqué, le moteur n'a pas de transition constitutionnelle vers un état stable. Il oscille indéfiniment entre scaffolding conservateur et escalade impossible.

**Décision : RETENU — P1**

Correction : Introduire un invariant ou une règle constitutionnelle définissant le comportement composite lorsque ≥ 2 axes sont simultanément `unknown` sur N sessions consécutives. Prévoir au minimum une transition vers un checkpoint humain ou une réduction de régime d'autonomie. Le seuil N est paramétrisé dans le Référentiel.

**Couche :** Constitution

---

### FA-02 — `INV_MSC_AND_STRICT` : comportement non défini si une composante P/R/A est non calculable

**Sources :** sonar (RISK-02 CRITIQUE), GPTwoThink (F-2.2 ÉLEVÉ), ClaudeThink (partiel)

**Constat :** Si R est non observable (ex. : première session sans historique temporel) ou si P/A est en attente, le AND strict ne peut pas être évalué. La Constitution ne définit pas si la maîtrise est alors `false`, `unknown` ou `deferred`.

**Décision : RETENU — P1**

Correction : Ajouter dans `INV_MSC_AND_STRICT` ou via un invariant complémentaire : si une composante est non calculable, la maîtrise est `deferred` (non déclarée, pas `false`). L'état `deferred` bloque la propagation de maîtrise mais ne génère pas de rétrogradation.

**Couche :** Constitution

---

### FA-03 — `INV_RUNTIME_FULLY_LOCAL` vs notification externe : conflit d'invariants primaires

**Sources :** Gemini (CRITIQUE-01 — cf. FC-01), NemoTron (implicite via AX1-01)

Traité en FC-01. Statut : **FUSIONNÉ AVEC FC-01**.

---

### FA-04 — Boucle sémantique `TYPE_INTEGRITY_MODES → SIS → NC-MSC → moteur`

**Sources :** sonar (RISK-04 ÉLEVÉ)

**Constat :** La boucle sémantique `IntegrityMode → SIS → NC-MSC → décisions moteur → contexte mode` est réelle mais n'est pas un cycle YAML interdit. Elle ne produit pas d'état bloquant identifiable, seulement un risque de comportement émergent non borné.

**Décision : DIFFÉRÉ — P3**

Motif : Pas de scénario de blocage identifié de façon précise dans les rapports. À monitorer lors de l'implémentation. Un invariant de borne pourra être introduit en V2 si le comportement oscillant est observé en simulation.

---

### FA-05 — Régime oscillatoire `Consolidation + Exploration` sans borne de durée ni sortie de secours

**Sources :** ClaudeWoThink (A1-4 ÉLEVÉ + A3-2), ClaudeThink (F3.2 partiel)

**Constat :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` décrit un régime oscillatoire dont la sortie est conditionnée à `R atteint`, sans borne maximale de cycles ni condition de secours si R n'est jamais atteint.

**Décision : RETENU — P2**

Correction : Ajouter dans le Référentiel un paramètre `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` et une condition de sortie de secours (ex. retour en mode conservateur après N cycles). La Constitution n'est pas modifiée — c'est un problème de complétion référentielle.

**Couche :** Référentiel

---

### FA-06 — Maîtrise provisoire : expiration de fenêtre sans EVENT ni traitement constitutionnel

**Sources :** ClaudeThink (F1.4 MODÉRÉ), ClaudeWoThink (A3-3 ÉLEVÉ), GPTwoThink (F-5.1 MODÉRÉ), GPTThink (partiel)

**Constat :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est déclaré mais l'expiration sans confirmation ne génère aucun event. La sémantique moteur de cette expiration (révoquer, geler, escalader) est indéfinie.

**Décision : RETENU — P2**

Correction : Déclarer un `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` et une règle associée. Le comportement par défaut est : basculement en `deferred` (cohérent avec FA-02), déclenchement d'une tâche diagnostique courte. La révocation automatique est rejetée comme trop punitive.

**Couche :** Constitution

---

### FA-07 — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` : scope `design_runtime` ambigu

**Sources :** sonar (RISK-05 ÉLEVÉ), ClaudeThink (F4.1 ÉLEVÉ), GPTwoThink (F-4.1 MODÉRÉ), ClaudeWoThink (A4-1 MODÉRÉ)

**Constat :** Le flag `misconception` sur une KU peut être interprété comme posé en runtime, ce qui violerait `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`.

**Décision : RETENU — P2**

Correction : Préciser dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` et dans `TYPE_KNOWLEDGE_UNIT` que le flag `misconception` est exclusivement un attribut de design ou d'outillage off-session. Jamais inféré en runtime. Ajouter une contrainte ou une précision dans la logique du TYPE.

**Couche :** Constitution

---

### FA-08 — Binding LINK manquant : `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

**Sources :** NemoTron (AX1-01 CRITIQUE), ClaudeWoThink (A1-3 MODÉRÉ), GPTwoThink (F-1.5 MODÉRÉ), sonar (RISK-08 MODÉRÉ)

**Constat :** La résolution du seuil de divergence MSC/perçu n'est pas matérialisée dans le LINK. La chaîne d'autorité depuis l'EVENT vers le paramètre référentiel est implicite.

**Décision : RETENU — P2**

Correction : Ajouter dans le LINK un `TYPE_BINDING` reliant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` au `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`.

**Couche :** LINK

---

### FA-09 — Patchabilité incohérente sur `ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`

**Sources :** Gemini (ÉLEVÉ-02), GPTwoThink (F-5.4 MODÉRÉ)

**Constat :** Ces deux ACTIONs sont déclarées `patchable: true` alors qu'elles déclenchent des révisions pédagogiques structurantes. Un patch sur ces actions contourne la QA pédagogique.

**Décision : RETENU — P3**

Correction : Passer à `patchable: false`. Les aspects effectivement paramétrables (ex. seuil de déclenchement) doivent être isolés dans un PARAM dédié.

**Couche :** Constitution

---

### FA-10 — `AR-N3` orphelin sans relation ni action constitutionnelle

**Sources :** GPTThink (C-06 MODÉRÉ), Gemini (AX2-C MODÉRÉ)

**Constat :** `TYPE_SELF_REPORT_AR_N3` n'a aucune `relation` déclarée dans la Constitution. Son output (indice de calibration) n'est consommé par aucun TYPE, RULE ni INV au niveau constitutionnel.

**Décision : RETENU — P3**

Correction : Arbitrage de couche requis — soit déclarer la consommation de l'indice AR-N3 dans la Constitution (relation vers `TYPE_STATE_AXIS_CALIBRATION`), soit documenter explicitement que cette consommation est référentielle et ajouter le binding LINK correspondant.

**Couche :** Constitution ou LINK (à décider en patch)

---

### FA-11 — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` sans EVENT associé (couverture du déclenchement)

Traité dans FC-05. Statut : **FUSIONNÉ AVEC FC-05**.

---

### FA-12 — Détection de version Référentiel incompatible absente

**Sources :** Gemini (AX5-C ÉLEVÉ), ClaudeThink (F5.2 MODÉRÉ), GPTwoThink (F-5.3 ÉLEVÉ), sonar (RISK-03)

**Constat :** La Constitution référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` de façon statique (`patchable: false`). Aucun invariant ne détecte ou bloque l'usage d'un Référentiel hors-version déclarée.

**Décision : RETENU — P2**

Correction : Introduire un mécanisme de release coordonnée inter-Core (à spécifier dans la gouvernance pipeline). Au niveau constitutionnel, ajouter une mention dans `INV_CONSTITUTION_REFERENTIAL_SEPARATION` indiquant que toute promotion de version du Référentiel requiert une re-validation explicite du LINK et de la Constitution avant activation.

**Couche :** Constitution + Gouvernance pipeline

---

### FA-13 — `source_anchor` d'arbitrage dans la Constitution (`[ARBITRAGE_2026_04_01]`)

**Sources :** GPTThink (C-16 FAIBLE), Gemini (AX5-A MODÉRÉ), NemoTron (AX5-02 MODÉRÉ)

**Constat :** Les éléments introduits par arbitrage portent `source_anchor: '[ARBITRAGE_2026_04_01][...]'` — ancres opérationnelles non normatives.

**Décision : DIFFÉRÉ — P4**

Motif : La convention est fonctionnelle et traçable pour l'instant. Une normalisation vers `[Sxx]` représente un coût de refactoring sans bénéfice moteur immédiat. À traiter lors de la prochaine revue de gouvernance de versioning.

---

### FA-14 — Détresse activation chronique sans protocole d'escalade

**Sources :** sonar (RISK-06 ÉLEVÉ)

**Constat :** Par symétrie avec `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, la détresse d'activation persistante sur N sessions consécutives malgré le scaffolding conservateur ne génère pas d'escalade constitutionnelle.

**Décision : RETENU — P2** (fusionné avec FA-01 pour le patch)

La règle de transition constitutionnelle après N sessions `unknown`/détresse (FA-01) doit couvrir également la détresse activation persistante.

**Couche :** Constitution

---

### FA-15 — Gamification probatoire sans condition de sortie ni durée bornée

**Sources :** NemoTron (AX1-03 MODÉRÉ), ClaudeThink (F2.3 FAIBLE), GPTThink (C-12 MODÉRÉ), GPTwoThink (dérivé)

**Constat :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` n'a ni durée bornée ni critère de validation de sortie.

**Décision : DIFFÉRÉ — P3**

Motif : Le risque est réel mais limité — le mode probatoire ne cause pas de blocage moteur critique. La correction est référentielle (paramétrer la durée et le critère de validation). À inclure dans un patch Référentiel ultérieur.

**Couche :** Référentiel

---

### FA-16 — Absence de contrainte sur la densité cumulée des sollicitations AR par session

**Sources :** GPTThink (C-08 MODÉRÉ), GPTwoThink (F-2.1 FAIBLE), Gemini (AX2-D FAIBLE)

**Constat :** Plusieurs AR-N1 peuvent s'empiler en session sans limite constitutionnelle.

**Décision : DIFFÉRÉ — P4**

Motif : Le risque est de charge cognitive extrinsèque. La correction relève d'une règle référentielle de budget cumulé, pas d'un invariant constitutionnel fondamental.

**Couche :** Référentiel

---

### FA-17 — `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` patchable sans borne anti-dérive

**Sources :** GPTwoThink (F-5.1 MODÉRÉ)

**Constat :** Ce paramètre est `patchable: true` sans contrainte de borne.

**Décision : RETENU — P3**

Correction : Déclarer une contrainte `CONSTRAINT_PROVISIONAL_MASTERY_WINDOW_MUST_BE_BOUNDED` précisant que la valeur de la fenêtre doit rester dans une plage définie par le Référentiel.

**Couche :** Constitution

---

### FA-18 — Findings HORS_SCOPE ou REJETÉS

| Ref source | Libellé | Décision | Motif |
|---|---|---|---|
| ClaudeWoThink CRIT-01 | LINK absent du corpus d'analyse | REJETÉ | Le LINK est bien présent dans le repo ; absence dans le corpus de ce challenger uniquement, pas une faille Core |
| GPTThink C-15 | Dépendance circulaire T ↔ MasteryModel (ordre de résolution) | HORS_SCOPE | La relation `derives_from` est descriptive, non instanciatrice. Pas de cycle YAML. |
| GPTwoThink F-2.3 | `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` non stratifiée par type d'activation | REJETÉ | Le niveau constitutionnel n'a pas vocation à stratifier les réponses conservatrices — c'est le rôle du Référentiel. |
| Gemini AX3-C | Plafonnement Bloom 2 excessif (Bloom 3 légitime sans contexte authentique) | DIFFÉRÉ — P4 | La décision de plafonner à Bloom 2 est délibérée. Une révision éventuelle à Bloom 3 nécessite un arbitrage pédagogique séparé. |
| GPTThink C-10 | GF-08 réponse conservatrice non définie opérationnellement | REJETÉ | Le scope de GF-08 est explicitement générique par construction. La sémantique conservatrice est suffisamment définie ailleurs. |

---

## Tableau de décision consolidé

| ID | Libellé court | Décision | Priorité | Couche |
|---|---|---|---|---|
| FC-01 | Notification externe DIVMSC-01 doit être hors session | RETENU | P1 | Constitution |
| FC-02 | INV Référentiel présent avant évaluation seuils | RETENU | P1 | Constitution |
| FC-03 | EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION manquant | RETENU | P1 | Référentiel |
| FA-01 | Transition après N sessions unknown/détresse + patch bloqué | RETENU | P1 | Constitution |
| FA-02 | MSC AND strict — composante non calculable → mastery deferred | RETENU | P1 | Constitution |
| FC-04 | Composante T orpheline — déclencheur + binding LINK | RETENU | P2 | Constitution + LINK |
| FC-05 | INV_KNOWLEDGE_GRAPH acyclique étendu aux patchs incrémentiels | RETENU | P2 | Constitution |
| FA-05 | Régime oscillatoire sans borne de cycles ni sortie de secours | RETENU | P2 | Référentiel |
| FA-06 | EVENT expiration maîtrise provisoire + règle de traitement | RETENU | P2 | Constitution |
| FA-07 | Flag misconception exclusivement off-session | RETENU | P2 | Constitution |
| FA-08 | Binding LINK EVENT_MSC_DIVERGENCE → PARAM seuil | RETENU | P2 | LINK |
| FA-12 | Mécanisme détection version Référentiel incompatible | RETENU | P2 | Constitution + Gouvernance |
| FA-14 | Détresse activation chronique → escalade (fusionné FA-01) | RETENU | P2 | Constitution |
| FA-09 | ACTION déclenchantes patchable: false | RETENU | P3 | Constitution |
| FA-10 | AR-N3 orphelin — relation constitutionnelle ou binding LINK | RETENU | P3 | Constitution ou LINK |
| FA-17 | PARAM fenêtre provisoire — contrainte de borne anti-dérive | RETENU | P3 | Constitution |
| FA-15 | Gamification probatoire — condition de sortie | DIFFÉRÉ | P3 | Référentiel |
| FA-04 | Boucle sémantique IntegrityMode/SIS/NC-MSC | DIFFÉRÉ | P3 | — |
| FA-13 | Normalisation source_anchor arbitrages | DIFFÉRÉ | P4 | Gouvernance |
| FA-16 | Densité cumulée AR par session | DIFFÉRÉ | P4 | Référentiel |
| Gemini AX3-C | Plafonnement Bloom 3 vs Bloom 2 | DIFFÉRÉ | P4 | — |
| ClaudeWoThink CRIT-01 | LINK absent du corpus | REJETÉ | — | — |
| GPTThink C-15 | Circularité T ↔ MasteryModel | REJETÉ | — | — |
| GPTwoThink F-2.3 | Stratification réponse conservatrice | REJETÉ | — | — |
| GPTThink C-10 | GF-08 sémantique non définie | REJETÉ | — | — |

---

## Résumé des corrections autorisées à passer au STAGE_03_PATCH_SYNTHESIS

### Patch Constitution (P1)
1. `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` — ajouter `scope: post_session_only` sur le step d'escalade externe
2. Nouvel invariant `INV_REFERENTIEL_REQUIRED_BEFORE_THRESHOLD_EVALUATION`
3. Nouvelle règle ou invariant : transition constitutionnelle après N sessions `unknown`/détresse persistante + patch bloqué (covers FA-01 + FA-14)
4. Compléter `INV_MSC_AND_STRICT` : mastery = `deferred` si une composante est non calculable

### Patch Constitution (P2)
5. Ajouter relation `TYPE_MASTERY_MODEL → INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`
6. Déclarer `EVENT_T_EVALUATION_OVERDUE`
7. Étendre trigger de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` + déclarer `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` + `ACTION_BLOCK_GRAPH_LOAD`
8. Déclarer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` + règle de traitement (→ deferred + tâche diagnostique)
9. Préciser dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` et `TYPE_KNOWLEDGE_UNIT` : flag misconception exclusivement off-session
10. Ajouter mention dans `INV_CONSTITUTION_REFERENTIAL_SEPARATION` : promotion de version Référentiel requiert re-validation explicite

### Patch Constitution (P3)
11. `ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` → `patchable: false`
12. Décider couche de `TYPE_SELF_REPORT_AR_N3` (Constitution ou LINK)
13. Déclarer `CONSTRAINT_PROVISIONAL_MASTERY_WINDOW_MUST_BE_BOUNDED`

### Patch Référentiel (P1)
14. Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` avec action d'escalade associée

### Patch Référentiel (P2)
15. Ajouter `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` et condition de sortie de secours du régime oscillatoire

### Patch LINK (P2)
16. Ajouter binding `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED → PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
17. Statuer sur binding T (FC-04.c)

---

## Note opératoire

Cet arbitrage est produit par l'agent Perplexity (Sonar) dans le cadre du STAGE_02_ARBITRAGE du pipeline Constitution. Il constitue le document d'entrée canonique du STAGE_03_PATCH_SYNTHESIS. Tout élément DIFFÉRÉ ou REJETÉ ne doit pas être intégré dans le patchset de ce run.
