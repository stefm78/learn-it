# CHALLENGE REPORT — Constitution V1_9
<!-- generated: 2026-04-01 | model: Gemini | stage: STAGE_01_CHALLENGE -->

id: challenge_report_Gemini
core_audited: CORE_LEARNIT_CONSTITUTION_V1_9
date: 2026-04-01
auditor: Gemini (adversarial)

---

## Résumé exécutif

La Constitution V1_9 présente un niveau de maturité élevé : la séparation des couches est globalement respectée, les invariants sont nombreux, les événements et actions sont bien câblés. Cependant, plusieurs zones de risque subsistent :

1. **Couplage implicite fort** entre Constitution et Référentiel, non entièrement résolu par la seule référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` — le moteur dépend de paramètres référentiels pour évaluer des règles constitutionnelles fondamentales (seuils R, fenêtre PARAM, seuil VC, seuil AR-réfractaire), sans que les bornes minimales soient déclarées localement.
2. **Ambiguïté d'états moteur** autour de `unknown/absent/non-observable` : la règle `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` est sous-spécifiée quant aux priorités de réponse moteur selon le régime d'autonomie.
3. **Lacune de gouvernance** sur les conflits multi-invariants non couverts par GF-08 : la règle `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` ne hiérarchise pas les invariants constitutionnels eux-mêmes.
4. **Absence de définition formelle** du concept de *divergence persistante* (nombre de sessions, fenêtre temporelle) au niveau constitutionnel pour `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — délégation totale au Référentiel sans borne constitutionnelle minimale.
5. **Risque de dérive patchabilité** : plusieurs actions (ex. `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`) sont déclarées `patchable: true` alors qu'elles déclenchent des révisions pédagogiques structurantes — la frontière action/patch mérite clarification.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### 1.1 Dépendances implicites vers le Référentiel non bornées constitutionnellement

Les éléments suivants déclarent `depends_on: REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` pour des décisions constitutionnelles fondamentales, sans borne plancher dans la Constitution :

- `TYPE_MASTERY_COMPONENT_R` — seuils et multiplicateurs entièrement délégués au Référentiel.
- `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` — seuil `seuil_R` uniquement référentiel.
- `EVENT_PERSISTENT_LOW_VC` — seuil de persistance uniquement référentiel.
- `EVENT_AR_REFRACTORY_PROFILE_DETECTED` — fenêtre de non-réponse uniquement référentiel.
- `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` uniquement référentiel.

**Risque :** Si le Référentiel est absent, corrompu, ou dans une version incompatible, le moteur peut prendre des décisions constitutionnelles (déclencher un patch de relevance, démarrer une reprise diagnostique) sur base de seuils indéfinis. La Constitution ne pose aucun filet de sécurité constitutionnel minimal.

**Placement :** Problème de séparation Constitution/Référentiel — les seuils opératoires relèvent bien du Référentiel, mais une borne constitutionnelle plancher (ou un invariant de présence du Référentiel avant tout calcul) devrait exister.

#### 1.2 Binding manquant : `TYPE_LEARNER_STATE_MODEL` ↔ `TYPE_AUTONOMY_REGIME`

`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` permet à un axe de rester `unknown`. Mais il n'existe aucun binding explicite entre le régime `unknown` d'un axe et le `TYPE_AUTONOMY_REGIME` actif. En régime **assisté** ou **hybride bloquant**, l'absence d'AR-N1 peut déclencher `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`, mais l'impact sur `TYPE_HUMAN_CHECKPOINT` n'est pas formalisé lorsque l'axe reste `unknown` de façon durable.

**Risque :** Oscillation moteur — un axe `unknown` persistant en régime hybride bloquant pourrait ne jamais déclencher de checkpoint humain obligatoire.

#### 1.3 Conflit potentiel entre `INV_RUNTIME_FULLY_LOCAL` et `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`

L'effet de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` inclut : *"escalade vers révision du design du contenu — notification externe obligatoire"*. Or `INV_RUNTIME_FULLY_LOCAL` interdit tout appel réseau en usage apprenant. Si la notification externe est déclenchée pendant une session active, un conflit d'invariant se produit.

**Risque :** État interdit non documenté — le moteur peut tenter une notification externe en runtime, violant `INV_RUNTIME_FULLY_LOCAL`.

**Placement :** Constitution — conflit interne entre deux invariants/règles.

#### 1.4 `source_anchor` non cohérent pour `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` et `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`

Ces deux éléments référencent `[ARBITRAGE_2026_04_01][DIVMSC-01]` comme `source_anchor`. Ce n'est pas une ancre du corpus constitutionnel original mais une référence à un arbitrage opérationnel. La Constitution doit s'ancrer dans ses propres sources structurelles — une source de type `[ARBITRAGE_...]` introduit une dépendance de traçabilité fragile.

**Placement :** Gouvernance / versioning.

---

### Axe 2 — Solidité théorique

#### 2.1 Mastery Learning : absence de fenêtre constitutionnelle de vérification provisoire

`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est déclaré, mais seul le Référentiel en borne la valeur. En théorie du mastery learning, la confirmation d'une maîtrise provisoire héritée sans fenêtre minimale garantie ouvre la possibilité d'un apprentissage mal fondé durable. La Constitution ne pose aucun plancher (ex. "au moins N sessions").

#### 2.2 Métacognition / SRL : `RULE_SESSION_INTENTION_NON_BLOCKING` sous-spécifiée

La règle déclare que l'intention de session est *"informative, non bloquante et non pénalisée"* et qu'elle *"support[e] de forethought SRL"*. Mais aucun TYPE ou RULE ne formalise ce que le moteur fait réellement de cette information — il n'y a aucun ACTION câblé à `RULE_SESSION_INTENTION_NON_BLOCKING`. L'intention de session est collectée mais inopérante dans la Constitution.

**Risque :** La composante SRL forethought est déclarée mais non actionnée — risque de sur-promesse pédagogique.

#### 2.3 Émotions / Engagement : asymétrie AR-N1 / AR-N3

`TYPE_SELF_REPORT_AR_N1` a des relations explicites (`validates TYPE_STATE_AXIS_ACTIVATION`), mais `TYPE_SELF_REPORT_AR_N3` n'a aucune `relation` déclarée et aucun câblage vers un TYPE ou une RULE. Son effet se limite à *"indice de calibration auto-rapport"* — sans action constitutionnelle associée.

**Risque :** AR-N3 constitue un instrument de mesure déclaré mais sans effet systémique formalisé dans la Constitution.

#### 2.4 Charge cognitive : absence de contrainte sur le cumul de micro-sondages

Les budgets AR-N1, AR-N2, AR-N3 sont déclarés comme paramètres référentiels, mais la Constitution n'impose aucune règle de non-accumulation ou de protection contre la surcharge de sollicitation AR en session courte (ex. AR-N1 + AR-N2 déclenchés simultanément).

---

### Axe 3 — États indéfinis moteur

#### 3.1 Oscillation sur `unknown` persistant

Si `TYPE_STATE_AXIS_ACTIVATION` reste `unknown` plusieurs sessions consécutives (AR-N1 absent), le moteur applique `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` (scaffolding léger) indéfiniment. Il n'existe pas de transition constitutionnelle vers un état stable alternatif (ex. escalade checkpoint humain, changement de régime).

**Scénario de blocage :** Un apprenant AR-réfractaire en régime autonome accumule des sessions `unknown` → le patch de sollicitation est déclenché (`EVENT_AR_REFRACTORY_PROFILE_DETECTED`) → mais si le patch est rejeté ou impossible, `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` prévoit une escalade hors session. Le moteur ne sait pas quoi faire *pendant* les sessions intermédiaires.

#### 3.2 Indétermination entre `EVENT_GF08_UNCOVERED_CONFLICT` et invariants constitutionnels en conflit

`RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` s'applique aux conflits *inter-principes* non couverts. Mais si deux invariants constitutionnels (`patchable: false`, `authority: primary`) entrent en contradiction directe (ex. `INV_RUNTIME_FULLY_LOCAL` vs notification externe du protocole DIVMSC-01), l'issue est indéfinie : aucun mécanisme de résolution constitutionnel n'est prévu entre invariants primaires.

#### 3.3 Bloom 2 comme plafond universel de `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4`

L'effet de `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4` est *"plafonnement à Bloom 2"*. Il n'existe pas de niveau intermédiaire Bloom 3 sans contexte authentique — ce qui peut conduire à un plafonnement excessif pour des missions procédurales légitimes à Bloom 3 qui ne nécessitent pas nécessairement un contexte authentique de niveau Bloom 4+.

---

### Axe 4 — Dépendances IA implicites

#### 4.1 `TYPE_FEEDBACK_COVERAGE_MATRIX` : livrables de design supposent une inférence sémantique de mapping

La Matrice déclare `patchable: true` et sa logique (`trigger: Phase Design`, `condition: KU formelles ou procédurales présentes`) suppose que les concepteurs ont classifié les KU *avant* de construire la matrice. Mais la Constitution ne précise pas comment distinguer une erreur *couverte* d'une erreur *hors-taxonomie* au runtime — ce jugement implique une inférence sémantique qui peut dépendre de l'IA hors session.

#### 4.2 `INV_CONSTITUTION_REFERENTIAL_SEPARATION` : aucun mécanisme de détection de violation

L'invariant est déclaré comme inviolable mais il n'y a aucun EVENT ni ACTION associé à sa violation. Si un patch introduit de la logique métier dans la Constitution, il n'existe pas de déclencheur constitutionnel pour la détecter et la bloquer.

---

### Axe 5 — Gouvernance

#### 5.1 Versioning : `source_anchor` mixant corpus original et arbitrages opérationnels

Plusieurs éléments récents (`RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`) utilisent des ancres de type `[PATCH_V1_9__STAGE03]` ou `[ARBITRAGE_2026_04_01]`. Cela signifie que la traçabilité de la Constitution dépend de l'historique d'exécution du pipeline — fragilité pour un audit externe.

#### 5.2 Patchabilité incohérente sur les ACTIONs

`ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` sont déclarées `patchable: true`. Or ce sont des *déclencheurs d'actions pédagogiques structurantes*, non des paramètres. Si ces actions sont patchées, leurs effets pédagogiques changent sans passer par la QA pédagogique obligatoire définie dans `TYPE_PATCH_QUALITY_GATE`. La logique `patchable: true` sur une ACTION (vs un PARAM ou un TYPE) est à préciser.

#### 5.3 Absence de mécanisme de détection de version incompatible Référentiel

La Constitution référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` de façon statique. Si le Référentiel est patché vers une version V1_1 ou V2_0, la Constitution n'a aucun INVARIANT ni EVENT qui détecte et bloque l'usage d'un Référentiel hors-version déclarée.

#### 5.4 `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` : scope `knowledge_model` mais sans EVENT associé

L'invariant déclare un état interdit (cycle détecté = déploiement bloqué) mais n'a pas d'EVENT associé. Le déclenchement de la détection de cycle reste implicite — aucune trace constitutionnelle formelle de l'événement *"cycle détecté"*.

---

### Axe 6 — Priorisation

| ID | Description | Priorité |
|----|-------------|----------|
| AX1-C | Conflit `INV_RUNTIME_FULLY_LOCAL` ↔ notification externe DIVMSC-01 | **Critique** |
| AX3-A | Oscillation `unknown` persistant sans transition constitutionnelle | **Critique** |
| AX1-A | Dépendances seuils référentiels sans borne constitutionnelle plancher | **Élevé** |
| AX5-B | Patchabilité incohérente sur ACTIONs déclenchantes | **Élevé** |
| AX5-C | Absence de détection de version Référentiel incompatible | **Élevé** |
| AX1-B | Binding manquant `unknown` ↔ `TYPE_HUMAN_CHECKPOINT` en régime bloquant | **Élevé** |
| AX3-B | Indétermination entre invariants primaires en conflit direct | **Élevé** |
| AX2-B | `RULE_SESSION_INTENTION_NON_BLOCKING` inopérante (SRL forethought non câblé) | **Modéré** |
| AX2-C | `TYPE_SELF_REPORT_AR_N3` sans relations ni actions constitutionnelles | **Modéré** |
| AX3-C | Plafonnement Bloom 2 excessif (Bloom 3 légitime sans contexte authentique) | **Modéré** |
| AX5-A | `source_anchor` opérationnels dans la Constitution | **Modéré** |
| AX4-B | Absence d'EVENT sur violation `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | **Modéré** |
| AX5-D | Absence d'EVENT associé à `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | **Faible** |
| AX2-A | Absence de plancher constitutionnel `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` | **Faible** |
| AX2-D | Absence de règle de non-accumulation des micro-sondages AR | **Faible** |

---

## Risques prioritaires

### CRITIQUE-01 — Violation d'invariant : notification externe runtime vs `INV_RUNTIME_FULLY_LOCAL`

**Élément :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` + `INV_RUNTIME_FULLY_LOCAL`  
**Description :** La règle DIVMSC-01 prévoit une *"notification externe obligatoire"* en étape 2, sans préciser que cette notification est exclusivement hors session. Le moteur peut déclencher cette notification pendant une session apprenant active, violant l'invariant fondamental de localité.  
**Recommandation :** Ajouter une condition explicite *"notification déclenchée uniquement hors session"* ou un INVARIANT dédié sur le scope d'escalade.

### CRITIQUE-02 — Oscillation moteur : axe `unknown` persistant sans transition constitutionnelle

**Élément :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` + `EVENT_AR_REFRACTORY_PROFILE_DETECTED` + `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`  
**Description :** Un apprenant AR-réfractaire en régime autonome peut accumuler indéfiniment des sessions `unknown` si le patch de sollicitation est bloqué ou rejeté. La Constitution ne définit pas de comportement moteur stabilisé dans cet état intermédiaire.  
**Recommandation :** Définir une règle ou un événement constitutionnel de transition après N sessions `unknown` consécutives avec patch impossible (ex. forcer checkpoint humain ou réduction de régime d'autonomie).

### ÉLEVÉ-01 — Absence de borne constitutionnelle sur les seuils référentiels critiques

**Élément :** `TYPE_MASTERY_COMPONENT_R`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`  
**Description :** Ces éléments délèguent entièrement leurs seuils opératoires au Référentiel sans qu'aucun INVARIANT ne garantisse la présence et la compatibilité du Référentiel avant leur évaluation.  
**Recommandation :** Ajouter un INVARIANT `INV_REFERENTIEL_MUST_BE_LOADED_BEFORE_THRESHOLD_EVALUATION` ou équivalent.

### ÉLEVÉ-02 — Patchabilité incorrecte sur ACTIONs déclenchantes

**Élément :** `ACTION_TRIGGER_RELEVANCE_PATCH` (`patchable: true`), `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` (`patchable: true`)  
**Description :** Déclarer une ACTION déclenchante `patchable: true` permet de modifier son comportement sans passer par la QA pédagogique. Ce n'est pas cohérent avec la gouvernance patch de la Constitution.  
**Recommandation :** Passer ces deux ACTIONs à `patchable: false` et prévoir un PARAM dédié pour les aspects effectivement paramétrables de leur comportement.

---

## Corrections à arbitrer avant patch

| Ref | Élément concerné | Nature | Couche | Décision requise |
|-----|-----------------|--------|--------|-----------------|
| C01 | `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` | Ajout condition scope hors-session pour notification externe | Constitution | Arbitrage requis |
| C02 | Nouveau RULE ou EVENT | Transition constitutionnelle après N sessions `unknown` + patch bloqué | Constitution | Arbitrage requis |
| C03 | Nouveau INVARIANT | Présence et compatibilité Référentiel avant évaluation seuils | Constitution ou LINK | Arbitrage requis — couche à décider |
| C04 | `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` | Passage à `patchable: false` | Constitution | Arbitrage requis |
| C05 | `RULE_SESSION_INTENTION_NON_BLOCKING` | Câblage d'une ACTION SRL forethought ou suppression de la promesse | Constitution | Arbitrage requis |
| C06 | `TYPE_SELF_REPORT_AR_N3` | Ajout de relations/actions ou clarification du rôle constitutionnel | Constitution | Arbitrage requis |
| C07 | `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Ajout d'un EVENT `EVENT_CYCLE_DETECTED` associé | Constitution | Faible priorité — à arbitrer |
| C08 | `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | Ajout d'EVENT ou RULE de détection de violation | Constitution | Modérée priorité — à arbitrer |
| C09 | Ancres `[ARBITRAGE_...]` dans Constitution | Politique de traçabilité : ancres opérationnelles acceptées ou à normaliser | Gouvernance | Décision de politique |
