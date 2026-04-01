# ARBITRAGE — STAGE_02_ARBITRAGE
<!-- pipeline: constitution -->
<!-- stage: STAGE_02_ARBITRAGE -->
<!-- arbitre: Perplexity (Sonnet 4.6) -->
<!-- date: 2026-04-01 -->
<!-- sources_challenge: 7 fichiers challenge_*.md — voir §Périmètre analysé -->

---

## Résumé exécutif

L'arbitrage consolide **7 rapports de challenge** adversariaux produits par des modèles distincts (NemoTron, ClaudeThink, ClaudeWoThink, GPTThink, GPTwoThink, Gemini, Sonar) sur les Cores `CORE_LEARNIT_CONSTITUTION_V1_9`, `CORE_LEARNIT_REFERENTIEL_V1_0` et `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`.

Les rapports sont globalement convergents sur les zones de risque prioritaires. Plusieurs constats critiques ou élevés sont redondants entre 3 à 6 rapports, ce qui renforce leur légitimité. Quelques divergences mineures sur la qualification de sévérité ont été tranchées.

**Synthèse des décisions :**

| Décision | Nombre de points |
|---|---|
| `corriger_maintenant` | 14 |
| `reporter` | 7 |
| `rejeter` | 4 |
| `hors_perimetre` | 3 |

**Points critiques retenus pour correction immédiate :**
- Conflit `INV_RUNTIME_FULLY_LOCAL` ↔ notification externe de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`
- États `unknown` multi-axes sans règle de comportement composite
- Composante MSC non calculable en première session (AND strict non résolu)
- Binding LINK manquant sur `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
- Absence de fallback constitutionnel si le Référentiel est absent ou incompatible
- Cycle graphe non détecté post-patch (INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC sous-couvert)

---

## Périmètre analysé

### Fichiers de challenge considérés
- `challenge_NemoTron.md` (NemoTron, 2026-04-01)
- `challenge_report_01_ClaudeThink.md` (ClaudeThink, 2026-04-01)
- `challenge_report_01_ClaudeWoThink.md` (ClaudeWoThink, 2026-04-01)
- `challenge_report_01_GPTThink.md` (GPT adversarial avec thinking, 2026-04-01)
- `challenge_report_GPTwoThink.md` (GPTwoThink, 2026-04-01)
- `challenge_report_Gemini.md` (Gemini adversarial, 2026-04-01)
- `challenge_report_01_sonar.md` (Sonar/Perplexity adversarial, 2026-04-01)

### Notes humaines
Aucune note humaine d'arbitrage supplémentaire fournie. L'instruction d'entrée précise uniquement le répertoire de destination du fichier d'arbitrage.

### Limites de périmètre
- Le LINK n'était pas accessible à ClaudeWoThink lors de son audit (CRIT-01 de ce rapport) ; les autres auditeurs l'ont audité. Les constats LINK sont donc couverts par les autres rapports et restent valides.
- L'arbitrage ne produit pas de patch YAML.
- L'arbitrage ne réécrit pas les Cores.

---

## Points consolidés avant arbitrage détaillé

### Regroupements effectués

**CLUSTER-A — Dépendances seuils Référentiel sans fallback constitutionnel**
Convergence sur 5 rapports (ClaudeThink F1.1, GPTThink 1.1, GPTwoThink 1.3, Gemini AX1-A, Sonar RISK-03, NemoTron AX2-01 partiel).
Constat central : des règles et événements constitutionnels (`RULE_LONG_INTERRUPTION`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) délèguent leurs seuils au Référentiel sans qu'aucun invariant constitutionnel ne définisse le comportement si le Référentiel est absent, incompatible ou corrompu.

**CLUSTER-B — Binding LINK manquant sur `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` / `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`**
Convergence sur 4 rapports (NemoTron AX1-01, ClaudeWoThink A1-3, GPTwoThink 1.5, Sonar RISK-08).
Constat central : le binding LINK entre l'EVENT et le paramètre référentiel de seuil est absent, rendant la résolution non déterministe et violant `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.

**CLUSTER-C — États `unknown` multi-axes sans règle de comportement composite**
Convergence sur 4 rapports (Sonar RISK-01, GPTThink C-03, ClaudeWoThink implicite, Gemini CRITIQUE-02/AX1-B).
Constat central : `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise un axe `unknown`, mais aucune règle ne couvre le cas ≥2 axes simultanément `unknown`, ni la persistance prolongée sans transition.

**CLUSTER-D — INV_MSC_AND_STRICT avec composante non calculable (première session)**
Convergence sur 2 rapports (Sonar RISK-02, GPTwoThink 2.2 partiel).
Constat central : si R est non observable (première session, apprenant nouveau), l'invariant AND strict ne peut être évalué — l'état résultant (`false`, `deferred`, `unknown`) n'est pas déclaré constitutionnellement.

**CLUSTER-E — Composante T : opérationnellement orpheline (déclencheur, EVENT, binding LINK)**
Convergence sur 5 rapports (NemoTron AX1-02, ClaudeThink F1.3, ClaudeWoThink A4-2, GPTThink impliqué, Sonar RISK-07 partiel).
Constat central : T est constitutionnellement correcte mais sans déclencheur d'évaluation, sans EVENT `T_never_evaluated`, sans binding LINK opérationnel.

**CLUSTER-F — Conflit `INV_RUNTIME_FULLY_LOCAL` ↔ notification externe DIVMSC-01**
Convergence sur 1 rapport principal (Gemini CRITIQUE-01), non identifié par les autres.
Constat central : l'effet de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` mentionne une "notification externe obligatoire" sans préciser que cette notification est exclusivement hors-session, créant un conflit d'invariant.

**CLUSTER-G — Gamification probatoire sans condition de sortie ni durée bornée**
Convergence sur 4 rapports (NemoTron AX1-03, ClaudeThink F2.3, GPTThink C-12, ClaudeWoThink indirectement).
Constat central : `RULE_UNVERIFIED_GAMIFICATION_PROBATION` n'a pas de durée maximale, de critère de sortie, ni d'escalade en cas de non-résolution.

**CLUSTER-H — `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` : canal d'escalade indéfini**
Convergence sur 3 rapports (NemoTron AX1-04, GPTThink C-04, Gemini implicite).
Constat central : l'escalade est obligatoire selon l'invariant, mais la cible, le format et le délai de l'escalade ne sont pas définis.

**CLUSTER-I — Cycle graphe : `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ne couvre pas les mises à jour post-chargement**
Convergence sur 3 rapports (GPTThink C-07, GPTwoThink F-1.2, Gemini AX5-D partiel).
Constat central : l'invariant se déclenche sur le chargement initial, mais pas sur un patch incrémental du graphe.

**CLUSTER-J — Versioning inter-Core : aucun mécanisme de détection de version incompatible**
Convergence sur 5 rapports (NemoTron AX5-01, ClaudeThink F5.2, ClaudeWoThink A5-1, GPTwoThink F-5.3, Sonar RISK-03 partiel, Gemini AX5-C).
Constat central : la Constitution référence le Référentiel en `V1_0` statique, mais aucun invariant ne détecte l'usage d'un Référentiel hors-version ou ne force une revalidation du LINK lors d'un changement de version.

**CLUSTER-K — Événements référencés mais non déclarés (`EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`, `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED`)**
Convergence sur 2 rapports (ClaudeThink F1.2, ClaudeWoThink HIGH-01 / A1-2 / A3-1).
Constat central : deux événements sont nommés dans les `human_readable` de paramètres référentiels mais n'existent dans aucun bloc EVENTS.

**CLUSTER-L — Rétrogradation MSC partielle : état intermédiaire non défini**
Convergence sur 2 rapports (GPTwoThink F-2.2, Sonar RISK-02 partiel).
Constat central : si seule la composante R dégrade, le moteur ne sait pas si la maîtrise est entièrement révoquée, suspendue ou partiellement maintenue.

**CLUSTER-M — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` : flagging misconception non formalisé**
Convergence sur 4 rapports (ClaudeThink F4.1, ClaudeWoThink A4-1, GPTwoThink F-4.1, Sonar RISK-05).
Constat central : la règle suppose un flag `misconception` sur une KU sans formaliser comment ce flag est attribué ni si c'est autorisé en runtime.

**CLUSTER-N — AR-N3 orphelin constitutionnellement**
Convergence sur 3 rapports (GPTThink C-06, GPTwoThink 4.3 partiel, Gemini AX2-C).
Constat central : `TYPE_SELF_REPORT_AR_N3` n'a aucune relation ni action constitutionnelle explicitement câblée.

**CLUSTER-O — Régime oscillatoire `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` : absence de borne de durée**
Convergence sur 2 rapports (ClaudeWoThink A1-4 / A3-2 / HIGH-02, GPTThink implicite).
Constat central : le cycle alternant consolidation/exploration n'a pas de borne de cycles ni de sortie de secours si R n'est jamais atteint.

### Contradictions entre rapports

**Sur la sévérité du CLUSTER-B (binding LINK manquant sur seuil divergence MSC) :**
- NemoTron le classe CRITIQUE, Sonar le classe MODÉRÉ (RISK-08). 
- **Tranchement :** la classification CRITIQUE est retenue car une résolution non déterministe d'un paramètre de seuil d'un EVENT constitutionnel fondamental viole directement `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`. Le classement MODÉRÉ de Sonar semble traiter uniquement le risque de règle orpheline (donc un sous-cas du problème).

**Sur CRIT-01 ClaudeWoThink (LINK absent) :**
- Ce "risque" est spécifique au run de ClaudeWoThink qui n'avait pas le LINK en input. Il ne représente pas un défaut du système mais une limite d'input de ce run.
- **Tranchement :** non retenu comme point à corriger.

---

## Arbitrage détaillé

---

### Point ARB-01 — Conflit `INV_RUNTIME_FULLY_LOCAL` ↔ notification externe DIVMSC-01

- **Source(s) :** Gemini CRITIQUE-01 (C01)
- **Constat synthétique :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` prévoit une "notification externe obligatoire" sans préciser que cette notification se déclenche exclusivement hors session. En session active, cela violerait `INV_RUNTIME_FULLY_LOCAL`.
- **Nature :** cohérence interne — conflit d'invariants
- **Gravité :** critique
- **Impact :** sécurité logique du moteur, applicabilité, état interdit possible en runtime
- **Décision :** `corriger_maintenant`
- **Justification :** Ce conflit d'invariants primaires est le seul point identifié par Gemini seul mais il est structurellement fondé. `INV_RUNTIME_FULLY_LOCAL` est un invariant `patchable: false` de premier rang. La correction est minimale : ajouter une condition de scope `hors_session` sur l'effet de notification de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`.
- **Conséquence pour le patch :** Ajouter `condition: hors_session_uniquement` sur l'effet d'escalade externe de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`. Aucune modification de l'invariant `INV_RUNTIME_FULLY_LOCAL` lui-même.

---

### Point ARB-02 — Binding LINK manquant sur `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

- **Source(s) :** NemoTron AX1-01 (CRITIQUE), ClaudeWoThink A1-3 (MODÉRÉ), GPTwoThink 1.5, Sonar RISK-08
- **Constat synthétique :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dépend de `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` pour évaluer son trigger, mais aucun `TYPE_BINDING` dans le LINK ne matérialise cette dépendance. La résolution du seuil est implicite et non déterministe.
- **Nature :** structurelle — LINK binding manquant
- **Gravité :** critique (retenu sur tranchement de divergence, cf. Points consolidés)
- **Impact :** applicabilité moteur, violation de `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
- **Décision :** `corriger_maintenant`
- **Justification :** Sans ce binding, le moteur ne peut pas résoudre le seuil de déclenchement de l'EVENT de façon déterministe. Correction additive dans le LINK uniquement.
- **Conséquence pour le patch :** Ajouter `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` dans le LINK, reliant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` au `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` du Référentiel.

---

### Point ARB-03 — États `unknown` multi-axes : comportement composite indéfini

- **Source(s) :** Sonar RISK-01 (CRITIQUE), GPTThink C-03 (ÉLEVÉ), Gemini CRITIQUE-02 partiel, ClaudeThink implicite
- **Constat synthétique :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise un axe en `unknown`, mais le moteur n'a aucune règle pour le cas ≥2 axes simultanément `unknown`. Le comportement composite est indéfini.
- **Nature :** logique — état moteur indéfini
- **Gravité :** critique
- **Impact :** sécurité logique, applicabilité, stabilité du système
- **Décision :** `corriger_maintenant`
- **Justification :** Le scénario multi-axe `unknown` est réaliste (AR-réfractaire + VC non observable). La correction minimale est d'ajouter un invariant de comportement conservateur maximal dans ce cas, sans restructurer la règle existante.
- **Conséquence pour le patch :** Ajouter `INV_MULTI_AXIS_UNKNOWN_REQUIRES_MAXIMUM_CONSERVATIVE_RESPONSE` dans la Constitution : si ≥2 axes sont simultanément `unknown`, le moteur applique la réponse conservatrice maximale (scaffolding léger réversible + escalade checkpoint humain si N sessions consécutives dépassent un seuil référentiel dédié).

---

### Point ARB-04 — `INV_MSC_AND_STRICT` : composante non calculable en première session

- **Source(s) :** Sonar RISK-02 (CRITIQUE), GPTwoThink F-2.2 (ÉLEVÉ)
- **Constat synthétique :** Si R est non calculable (pas d'historique temporel, première session), le AND strict ne peut être évalué. L'état résultant (`mastery = false`, `deferred`, `unknown`) n'est pas déclaré constitutionnellement.
- **Nature :** logique — état moteur indéfini
- **Gravité :** critique
- **Impact :** applicabilité, sécurité logique, cohérence inter-sessions
- **Décision :** `corriger_maintenant`
- **Justification :** Ce cas est inévitable pour tout apprenant nouveau. Une correction minimale et additive suffit : déclarer que si une composante est `non_calculable` (distinct de `insuffisante`), la maîtrise est `deferred` et non `false`, avec relance automatique de l'évaluation à la session suivante.
- **Conséquence pour le patch :** Ajouter dans `INV_MSC_AND_STRICT` (ou dans un invariant complémentaire `INV_MSC_COMPONENT_UNCALCULABLE_DEFERRED`) la sémantique : composante `non_calculable` → maîtrise `deferred` (non `false`, non `unknown`). Paramétrer via le Référentiel le seuil de sessions avant que `deferred` devienne `false` par défaut.

---

### Point ARB-05 — Fallback constitutionnel absent si Référentiel manquant ou incompatible

- **Source(s) :** CLUSTER-A — ClaudeThink F1.1, GPTThink C-01, GPTwoThink F-1.3, Gemini AX1-A, Sonar RISK-03
- **Constat synthétique :** Plusieurs règles et événements constitutionnels délèguent leurs seuils au Référentiel sans qu'aucun invariant ne définisse le comportement si le Référentiel est absent, incompatible ou corrompu. Le moteur peut osciller ou ne jamais déclencher des règles de sécurité critiques.
- **Nature :** structurelle — séparation de couches, robustesse moteur
- **Gravité :** élevé (convergence forte, mais les correctifs spécifiques restent CLUSTER-A niveau constitution)
- **Impact :** sécurité logique, applicabilité, stabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : un invariant de précondition de déploiement qui exige que le Référentiel soit chargé et valide avant toute évaluation de seuil constitutionnel.
- **Conséquence pour le patch :** Ajouter `INV_REFERENTIEL_MUST_BE_LOADED_AND_VALID_BEFORE_THRESHOLD_EVALUATION` dans la Constitution : si le Référentiel est absent ou dans une version incompatible, tout déploiement est bloqué (état : `deployment_blocked`). Cela s'applique avant l'évaluation de tout seuil constitutionnel délégué.

---

### Point ARB-06 — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` : non couvert pour les patches incrémentiels

- **Source(s) :** GPTThink C-07 (MODÉRÉ), GPTwoThink F-1.2 (CRITIQUE), Gemini AX5-D (FAIBLE)
- **Constat synthétique :** L'invariant se déclenche sur `Validation design ou chargement du graphe`, mais pas sur un patch incrémental du graphe. Un cycle peut être réintroduit via un patch localement valide.
- **Nature :** logique — invariant sous-couvert
- **Gravité :** critique (retenu sur la qualification GPTwoThink, le scénario étant concret et le risque moteur direct)
- **Impact :** sécurité logique, stabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : étendre le trigger de l'invariant pour couvrir les patches modifiant le graphe.
- **Conséquence pour le patch :** Modifier le trigger de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` pour inclure `patch_modifying_knowledge_graph` en plus de `Validation design ou chargement du graphe`. Ajouter un EVENT `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` et une `ACTION_BLOCK_GRAPH_LOAD` associés.

---

### Point ARB-07 — Composante T : opérationnellement orpheline

- **Source(s) :** CLUSTER-E — NemoTron AX1-02 (ÉLEVÉ), ClaudeThink F1.3 (ÉLEVÉ), ClaudeWoThink A4-2 (FAIBLE), Sonar RISK-07 (MODÉRÉ)
- **Constat synthétique :** T est constitutionnellement déclarée et séparée de la maîtrise de base, mais sans déclencheur d'évaluation, sans EVENT couvrant l'état `T_never_evaluated`, et sans binding LINK opérationnel.
- **Nature :** structurelle — composante déclarée sans cycle de vie
- **Gravité :** élevé
- **Impact :** applicabilité, maintenabilité
- **Décision :** `corriger_maintenant`
- **Justification :** La correction est additive et ciblée. Un EVENT et une RULE minimaux suffisent à clore le cycle de vie de T sans toucher à l'invariant de séparation.
- **Conséquence pour le patch :** Ajouter `EVENT_T_EVALUATION_OVERDUE` (déclenchement après N sessions post-maîtrise de base sans évaluation T, N paramétré dans le Référentiel) et une `RULE_T_EVALUATION_SCHEDULING` associée dans la Constitution. Ajouter dans le LINK un binding minimal documentant que T n'est pas liée à un paramètre de seuil Référentiel commun aux composantes P/R/A (binding explicitement vide, par conception).

---

### Point ARB-08 — Événements référencés mais non déclarés

- **Source(s) :** CLUSTER-K — ClaudeThink F1.2 (ÉLEVÉ), ClaudeWoThink A1-2 / A3-1 (ÉLEVÉ)
- **Constat synthétique :** `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` et `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` sont nommés dans les `human_readable` de paramètres référentiels mais n'existent dans aucun bloc EVENTS.
- **Nature :** structurelle — dépendances implicites non déclarées
- **Gravité :** élevé
- **Impact :** applicabilité, validation structurelle du graphe d'événements
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : déclarer formellement ces deux événements dans le Référentiel (ou la Constitution selon la couche appropriée) avec leurs actions associées. Alternative : si l'escalade est traitée par une ACTION externe existante, retirer les références et documenter explicitement.
- **Conséquence pour le patch :** Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel (lié à `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`) avec une ACTION d'escalade hors-session associée. Déclarer `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` dans le Référentiel lié à `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`.

---

### Point ARB-09 — Canal d'escalade de `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` non défini

- **Source(s) :** CLUSTER-H — NemoTron AX1-04 (MODÉRÉ), GPTThink C-04 (ÉLEVÉ), Gemini implicite
- **Constat synthétique :** L'invariant impose une escalade mais ne définit pas la cible, le format ni le délai. L'invariant est inopérant en runtime.
- **Nature :** logique — invariant déclaratif sans applicabilité technique
- **Gravité :** modéré (retenu malgré une qualification ÉLEVÉ de GPTThink car la correction est simple et additive)
- **Impact :** applicabilité, maintenabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Une ACTION dédiée à l'escalade peut être ajoutée sans toucher à l'invariant lui-même.
- **Conséquence pour le patch :** Ajouter `ACTION_ESCALATE_PERSISTENT_DRIFT_HORS_SESSION` dans la Constitution, déclarant : cible = `external_analysis_chain` (log structuré ou queue), format = `structured_event_log`, délai = `before_next_session_start`. L'invariant `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` gagnera une relation `triggers → ACTION_ESCALATE_PERSISTENT_DRIFT_HORS_SESSION`.

---

### Point ARB-10 — Gamification probatoire sans condition de sortie

- **Source(s) :** CLUSTER-G — NemoTron AX1-03 (MODÉRÉ), ClaudeThink F2.3 (FAIBLE), GPTThink C-12 (MODÉRÉ), ClaudeWoThink indirectement
- **Constat synthétique :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` déclare un mode probatoire sans durée maximale, critère de sortie ni mécanisme d'escalade.
- **Nature :** logique — règle ouverte sans fermeture
- **Gravité :** modéré
- **Impact :** applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Correction additive : ajouter un PARAM de durée maximale dans le Référentiel et un EVENT/RULE de sortie du mode probatoire.
- **Conséquence pour le patch :** Ajouter `PARAM_GAMIFICATION_PROBATION_MAX_DURATION` dans le Référentiel et un EVENT `EVENT_GAMIFICATION_PROBATION_EXPIRED` avec une RULE de sortie (validation automatique si aucun effet négatif détecté sur N sessions, ou escalade si non résolu).

---

### Point ARB-11 — `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` : régime oscillatoire sans borne constitutionnelle

- **Source(s) :** GPTwoThink F-1.4 (ÉLEVÉ), ClaudeWoThink A1-4 (ÉLEVÉ)
- **Constat synthétique :** La condition de "persistance après diagnostique" déclenchant l'escalade n'est pas déclarée dans `depends_on`, créant une boucle diagnostique→escalade→diagnostique potentiellement non bornée.
- **Nature :** logique — état oscillatoire non borné
- **Gravité :** élevé
- **Impact :** stabilité moteur, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Correction ciblée : ajouter une référence constitutionnelle à un paramètre Référentiel déclarant la fenêtre de persistance post-diagnostique, et un état terminal constitutionnel.
- **Conséquence pour le patch :** Ajouter `depends_on: PARAM_REFERENTIEL_DIVMSC_PERSISTENCE_AFTER_DIAGNOSTIC` dans `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, et déclarer ce paramètre dans le Référentiel. Ajouter un état terminal constitutionnel `DIVMSC_ESCALATION_FINAL` après N cycles diagnostique-escalade.

---

### Point ARB-12 — Rétrogradation MSC partielle : état intermédiaire non défini

- **Source(s) :** GPTwoThink F-2.2 (ÉLEVÉ), Sonar RISK-02 partiel
- **Constat synthétique :** Si seule R dégrade, le moteur ne sait pas si la maîtrise est entièrement révoquée ou si seul R est marqué insuffisant. Implémentations divergentes possibles.
- **Nature :** logique — état moteur indéfini
- **Gravité :** élevé
- **Impact :** applicabilité, cohérence inter-sessions
- **Décision :** `corriger_maintenant`
- **Justification :** La correction est additionnelle à ARB-04 (mais distincte : concerne la dégradation post-maîtrise, non la première session). Décision d'arbitrage : seule la composante insuffisante est marquée — la maîtrise globale passe en `degraded_pending_review` et non en `false`.
- **Conséquence pour le patch :** Ajouter l'état `degraded_pending_review` dans `TYPE_MASTERY_MODEL` (ou un TYPE complémentaire) et préciser dans `INV_MSC_AND_STRICT` que cet état est le résultat d'une dégradation partielle (composante R uniquement insuffisante après maîtrise établie). Distinguer la révocation (toutes composantes) de la dégradation partielle.

---

### Point ARB-13 — Versioning inter-Core : absence de mécanisme de détection de version incompatible

- **Source(s) :** CLUSTER-J — NemoTron AX5-01 (MODÉRÉ), ClaudeThink F5.2 (MODÉRÉ), GPTwoThink F-5.3 (ÉLEVÉ), Gemini AX5-C (ÉLEVÉ), Sonar RISK-03 (ÉLEVÉ), ClaudeWoThink A5-1 partiel
- **Constat synthétique :** La Constitution référence `V1_0` du Référentiel de façon statique. Aucun invariant ne détecte l'usage d'un Référentiel hors-version déclarée. La convergence sur ce point est forte.
- **Nature :** gouvernance — versioning inter-Core
- **Gravité :** élevé (convergence forte : 5 rapports)
- **Impact :** maintenabilité, stabilité, capacité de patch/release
- **Décision :** `corriger_maintenant`
- **Justification :** La correction minimale est un invariant de vérification de compatibilité de version avant activation du moteur, sans changer le mécanisme de référence statique.
- **Conséquence pour le patch :** Ajouter `INV_REFERENTIEL_VERSION_COMPATIBILITY_REQUIRED` dans la Constitution : lors du chargement du Référentiel, sa version déclarée doit correspondre à la version attendue dans `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`. Toute promotion de version du Référentiel doit déclencher une revalidation du LINK (ajouter une RULE de gouvernance correspondante).

---

### Point ARB-14 — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` : flagging misconception non formalisé

- **Source(s) :** CLUSTER-M — ClaudeThink F4.1 (ÉLEVÉ), ClaudeWoThink A4-1 (MODÉRÉ), GPTwoThink F-4.1 (MODÉRÉ), Sonar RISK-05 (ÉLEVÉ)
- **Constat synthétique :** Le flag `misconception` sur une KU est utilisé par la règle mais son mode d'attribution n'est pas formalisé. Si attribué en runtime, cela violerait `INV_NO_RUNTIME_CONTENT_GENERATION`.
- **Nature :** logique — dépendance IA implicite, ambiguïté de scope
- **Gravité :** élevé (convergence forte sur 4 rapports)
- **Impact :** sécurité logique, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Clarification minimale dans la Constitution : le flag est exclusivement un attribut posé en phase Design ou par outillage off-session. La RULE reste inchangée.
- **Conséquence pour le patch :** Ajouter dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` ou dans `TYPE_KNOWLEDGE_UNIT` une CONSTRAINT déclarant que le flag `misconception` est exclusivement un attribut `scope: design_offline`. Jamais inféré en runtime.

---

### Point ARB-15 — Régime oscillatoire Consolidation/Exploration sans borne de cycles

- **Source(s) :** CLUSTER-O — ClaudeWoThink HIGH-02 / A1-4, GPTThink implicite
- **Constat synthétique :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` définit un régime oscillatoire dont la sortie est `R atteint`, sans borne maximale de cycles ni sortie de secours.
- **Nature :** logique — état indéfini moteur
- **Gravité :** élevé
- **Impact :** stabilité moteur, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Correction additive : ajouter un PARAM de borne maximale dans le Référentiel et une condition de sortie de secours.
- **Conséquence pour le patch :** Ajouter `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` dans le Référentiel et une condition de sortie de secours dans `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` : après N cycles sans atteindre R, le moteur bascule en mode conservateur (non plus oscillatoire).

---

## Points reportés

### REPORT-01 — AR-N3 orphelin constitutionnellement

- **Source(s) :** CLUSTER-N — GPTThink C-06, Gemini AX2-C, GPTwoThink 4.3
- **Constat :** `TYPE_SELF_REPORT_AR_N3` n'a aucune relation constitutionnelle câblée.
- **Décision :** `reporter`
- **Justification :** Le binding AR-N3 est partiellement couvert dans le LINK (`TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING`). La Constitution n'a pas besoin de tout câbler si le LINK documente le binding. Ce point mérite une analyse plus fine lors du prochain cycle de challenge/patch, une fois les corrections critiques stabilisées.

---

### REPORT-02 — Binding AR-N3 : frontière LINK/logique métier

- **Source(s) :** ClaudeThink F5.1 (ÉLEVÉ)
- **Constat :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` décrit un flux multi-étapes conditionnel qui approche la logique métier.
- **Décision :** `reporter`
- **Justification :** Ce refactoring du LINK est pertinent mais non urgent et pourrait déstabiliser des bindings actuellement fonctionnels. À traiter dans un prochain cycle dédié au LINK.

---

### REPORT-03 — Dégradation temporelle de R non déclarée constitutionnellement

- **Source(s) :** GPTThink C-02 (ÉLEVÉ)
- **Constat :** R ne dispose pas de mécanisme constitutionnel de décroissance temporelle explicite.
- **Décision :** `reporter`
- **Justification :** Ce point est délégué au Référentiel (multiplicateurs R). La décroissance est implicitement gérée via `EVENT_LONG_INTERRUPTION` et `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`. Une déclaration constitutionnelle explicite est souhaitable mais pas urgente si le Référentiel couvre déjà la décroissance via ses paramètres.

---

### REPORT-04 — KU créative avec feedback devenu indisponible en runtime

- **Source(s) :** ClaudeThink F3.1 (ÉLEVÉ)
- **Constat :** Si une KU créative est déployée et que son feedback local devient indisponible post-patch, le chemin de désactivation n'est pas borné.
- **Décision :** `reporter`
- **Justification :** Ce scénario est réel mais peu probable avant stabilisation du moteur. La correction impliquerait un invariant de désactivation runtime qui nécessite d'abord de clarifier ARB-06 (cycle graphe) et ARB-07 (T orpheline). À traiter dans un prochain cycle.

---

### REPORT-05 — Maîtrise provisoire : expiration de fenêtre sans traitement

- **Source(s) :** ClaudeThink F1.4 (MODÉRÉ), ClaudeWoThink HIGH-03 (ÉLEVÉ), GPTwoThink 5.1 (MODÉRÉ)
- **Constat :** L'expiration de `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` ne génère pas d'EVENT déclaré.
- **Décision :** `reporter`
- **Justification :** Lié à ARB-04 (composante non calculable). Une fois l'état `deferred` défini (ARB-04), ce point devient partiellement couvert. À compléter dans le prochain cycle après stabilisation d'ARB-04.

---

### REPORT-06 — `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` : absence de CONSTRAINT LINK miroir

- **Source(s) :** NemoTron AX1-05 (MODÉRÉ)
- **Constat :** La protection constitutionnelle n'est pas propagée formellement dans le LINK.
- **Décision :** `reporter`
- **Justification :** Ce point est secondaire par rapport aux corrections du LINK prioritaires (ARB-02, ARB-07). À intégrer lors du prochain cycle de refactoring LINK.

---

### REPORT-07 — Charge cognitive : absence de contrainte sur cumul de sollicitations AR

- **Source(s) :** GPTThink C-08 (MODÉRÉ), GPTwoThink F-2.1 (FAIBLE), Gemini AX2-D (FAIBLE)
- **Constat :** Aucune règle ne borne la fréquence cumulée des sollicitations AR-N1/N2/N3 par session.
- **Décision :** `reporter`
- **Justification :** Risque réel mais de niveau faible à modéré. Les budgets AR par type existent déjà (PARAM_AR_N*_INTERACTION_BUDGET). Une contrainte constitutionnelle de cumul nécessite une décision de design pédagogique préalable sur les valeurs acceptables. À traiter lors d'un cycle dédié à l'ergonomie AR.

---

## Points rejetés

### REJET-01 — Dépendance circulaire implicite T ↔ TYPE_MASTERY_MODEL (ordre de résolution)

- **Source(s) :** GPTThink C-15 (FAIBLE), GPTwoThink 1.1 partiel
- **Décision :** `rejeter`
- **Justification :** La relation `derives_from` est documentée comme descriptive, non d'instanciation. L'ordre de résolution au chargement n'est pas ambiguë en pratique dès lors que T est traité séparément du AND strict. Un commentaire de documentation suffit; aucun changement structurel n'est justifié.

---

### REJET-02 — Plafonnement Bloom 2 excessif (Bloom 3 légitime sans contexte authentique)

- **Source(s) :** Gemini AX3-C (MODÉRÉ)
- **Décision :** `rejeter`
- **Justification :** Ce point remet en question une règle pédagogique intentionnelle (`INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4`). Le plafonnement à Bloom 2 en l'absence de contexte authentique est un choix de design pédagogique délibéré, non une erreur. Une révision éventuelle relèverait d'un arbitrage pédagogique de fond, hors périmètre du pipeline de patch courant.

---

### REJET-03 — `RULE_SESSION_INTENTION_NON_BLOCKING` inopérante (SRL forethought non câblé)

- **Source(s) :** ClaudeThink F2.2 (MODÉRÉ), Gemini AX2-B (MODÉRÉ)
- **Décision :** `rejeter`
- **Justification :** La règle est délibérément non-bloquante. L'absence d'effet moteur est un choix conservateur explicite (la règle dit "informative, non bloquante"). ClaudeThink lui-même note que l'absence peut être "un choix délibéré (conservatisme)". Aucun correctif structurel n'est justifié dans ce cycle.

---

### REJET-04 — Traçabilité `ARBITRAGE_2026_04_01` non matérialisée dans `work/02_arbitrage/`

- **Source(s) :** NemoTron AX5-02 (MODÉRÉ), ClaudeWoThink A5-2 (MODÉRÉ)
- **Décision :** `hors_perimetre` (reclassé depuis `rejeter`)
- **Justification :** Ce point sera résolu par la production du présent document d'arbitrage et des suivants dans le pipeline. Ce n'est pas un défaut des Cores mais une lacune de traçabilité du pipeline précédent.

---

## Points hors périmètre

### HP-01 — `source_anchor` mixant ancres constitutionnelles et opérationnelles

- **Source(s) :** GPTThink C-16 (FAIBLE), Gemini AX5-A (MODÉRÉ), Sonar 1.1
- **Décision :** `hors_perimetre`
- **Justification :** La politique de nommage des `source_anchor` relève d'une décision de gouvernance documentaire globale, non d'un défaut des Cores. À décider hors pipeline de patch.

---

### HP-02 — Compatibilité descendante entre versions de Core (règle de dépréciation)

- **Source(s) :** GPTThink C-14 (MODÉRÉ)
- **Décision :** `hors_perimetre`
- **Justification :** Introduire une règle de compatibilité descendante et un cycle de dépréciation représente un chantier de gouvernance majeur. Hors périmètre de ce patch cycle.

---

### HP-03 — Registre structuré des patches appliqués (bloc APPLIED_PATCHES)

- **Source(s) :** GPTThink C-17 (FAIBLE)
- **Décision :** `hors_perimetre`
- **Justification :** Chantier de gouvernance documentaire. La traçabilité actuelle via `source_anchor` est suffisante pour les besoins du moteur. Un registre structuré est souhaitable à terme mais hors périmètre.

---

## Décisions à transmettre au patch

| Priorité | ID Arbitrage | Titre court | Core(s) cible(s) | Type de correction |
|---|---|---|---|---|
| CRITIQUE | ARB-01 | Conflit `INV_RUNTIME_FULLY_LOCAL` ↔ notification DIVMSC-01 | Constitution | Ajout condition scope sur effet de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` |
| CRITIQUE | ARB-02 | Binding LINK manquant seuil divergence MSC | LINK | Ajout `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` |
| CRITIQUE | ARB-03 | États `unknown` multi-axes sans règle composite | Constitution | Ajout `INV_MULTI_AXIS_UNKNOWN_REQUIRES_MAXIMUM_CONSERVATIVE_RESPONSE` |
| CRITIQUE | ARB-04 | `INV_MSC_AND_STRICT` : composante `non_calculable` → `deferred` | Constitution | Ajout invariant complémentaire `INV_MSC_COMPONENT_UNCALCULABLE_DEFERRED` |
| CRITIQUE | ARB-05 | Fallback constitutionnel si Référentiel absent/incompatible | Constitution | Ajout `INV_REFERENTIEL_MUST_BE_LOADED_AND_VALID_BEFORE_THRESHOLD_EVALUATION` |
| CRITIQUE | ARB-06 | Cycle graphe non couvert post-patch | Constitution | Extension trigger `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` + `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` |
| ÉLEVÉ | ARB-07 | Composante T orpheline | Constitution + LINK | `EVENT_T_EVALUATION_OVERDUE` + `RULE_T_EVALUATION_SCHEDULING` + binding LINK vide explicite |
| ÉLEVÉ | ARB-08 | Événements référencés non déclarés | Référentiel | Déclaration `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` + `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` |
| ÉLEVÉ | ARB-09 | Canal escalade dérive patch indéfini | Constitution | Ajout `ACTION_ESCALATE_PERSISTENT_DRIFT_HORS_SESSION` |
| ÉLEVÉ | ARB-11 | Boucle `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` non bornée | Constitution + Référentiel | Ajout `depends_on` formel + paramètre `PARAM_REFERENTIEL_DIVMSC_PERSISTENCE_AFTER_DIAGNOSTIC` |
| ÉLEVÉ | ARB-12 | Rétrogradation MSC partielle : état `degraded_pending_review` | Constitution | Ajout état intermédiaire dans `TYPE_MASTERY_MODEL` |
| ÉLEVÉ | ARB-13 | Versioning inter-Core : détection incompatibilité | Constitution | Ajout `INV_REFERENTIEL_VERSION_COMPATIBILITY_REQUIRED` |
| ÉLEVÉ | ARB-14 | Flagging misconception : CONSTRAINT `scope: design_offline` | Constitution | Ajout CONSTRAINT sur `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` ou `TYPE_KNOWLEDGE_UNIT` |
| ÉLEVÉ | ARB-15 | Régime oscillatoire sans borne de cycles | Référentiel | Ajout `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES` + condition de sortie de secours |
| MODÉRÉ | ARB-10 | Gamification probatoire sans fermeture | Référentiel | Ajout `PARAM_GAMIFICATION_PROBATION_MAX_DURATION` + `EVENT_GAMIFICATION_PROBATION_EXPIRED` |

### Contraintes de minimalité à respecter pour le patch

1. **Aucune modification des invariants `patchable: false`** (ARB-01 modifie une RULE, pas un invariant primaire).
2. **Préférer les ajouts à la suppression** : tous les correctifs ci-dessus sont additifs.
3. **ARB-04 et ARB-12 sont complémentaires** et doivent être cohérents entre eux dans le patch (définir `non_calculable` vs `degraded_pending_review` de façon mutuellement exclusive).
4. **ARB-05 et ARB-13 sont partiellement redondants** : l'invariant ARB-05 peut absorber ARB-13 si sa condition couvre la vérification de version. À décider lors de la synthèse de patch.
5. **ARB-08 requiert une décision sur la couche** : les deux EVENTs manquants sont dans les `human_readable` du Référentiel → les déclarer dans le Référentiel (pas la Constitution).

---

## Décisions explicitement non retenues

### Points reportés (7)
- REPORT-01 : AR-N3 orphelin — couverture partielle via LINK existant, reporter au prochain cycle
- REPORT-02 : Binding AR-N3 frontière LINK/logique métier — reporter au cycle de refactoring LINK
- REPORT-03 : Dégradation temporelle de R — implicitement couvert par le Référentiel, reporter
- REPORT-04 : KU créative feedback indisponible runtime — dépend de ARB-06/ARB-07, reporter
- REPORT-05 : Maîtrise provisoire expiration sans EVENT — partiellement couvert par ARB-04, reporter
- REPORT-06 : CONSTRAINT LINK miroir pour `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` — reporter au cycle LINK
- REPORT-07 : Cumul sollicitations AR — décision de design pédagogique préalable requise, reporter

### Points rejetés (3) et hors périmètre (3)
- REJET-01 : Dépendance circulaire T ↔ TYPE_MASTERY_MODEL — relation descriptive, non structurelle
- REJET-02 : Bloom 2 plafonnement — choix pédagogique délibéré
- REJET-03 : SRL forethought non câblé — conservatisme délibéré
- HP-01 : Politique `source_anchor` — gouvernance documentaire hors pipeline
- HP-02 : Compatibilité descendante — chantier gouvernance majeur hors périmètre
- HP-03 : Registre APPLIED_PATCHES — hors périmètre, souhaitable à terme
- HP-CRIT01-ClaudeWoThink : LINK absent du run ClaudeWoThink — limite d'input du run, non un défaut Core
