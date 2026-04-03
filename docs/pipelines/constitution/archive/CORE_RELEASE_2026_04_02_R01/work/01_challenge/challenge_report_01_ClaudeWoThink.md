# Challenge Report 01 — Constitution Pipeline STAGE_01_CHALLENGE

**Auteur :** Claude (sans mode thinking étendu)
**Date :** 2026-04-01
**Core challengés :** CORE_LEARNIT_CONSTITUTION_V1_9 × CORE_LEARNIT_REFERENTIEL_V1_0 × LINK (non fourni — traité en absence)
**Note de focalisation :** aucune

---

## Résumé exécutif

Le système Constitution + Référentiel V1.9/V1.0 est architecturalement solide et présente une séparation des couches bien tenue. Cependant, l'audit révèle **sept zones de risque structurel** réparties sur les axes de cohérence interne, de solidité théorique et de robustesse moteur. Trois risques sont classés **critiques ou élevés** et nécessitent arbitrage avant tout patch :

1. **CRIT-01 — Absence du LINK dans le corpus d'analyse** : le LINK n'était pas fourni en input. Aucun binding inter-Core ne peut être vérifié. Cela bloque la validation de la séparation des couches et l'audit des `[INTERCORE]` réels.
2. **HIGH-01 — Opérationnalisation manquante de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` et `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`** : ces règles issues de l'arbitrage `[ARBITRAGE_2026_04_01]` sont présentes dans les Cores mais leurs conditions de déclenchement composite et leurs états de sortie restent sous-spécifiés côté moteur.
3. **HIGH-02 — Paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` sans event ni action de sortie explicitement nommés** : le Référentiel déclare le paramètre et cite `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` mais cet event n'est pas déclaré dans le corpus.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### A1-1 : LINK absent du corpus (CRIT-01)

- **Support :** `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`, `REF_CORE_LEARNIT_CONSTITUTION_V1_9_IN_REFERENTIEL`, `source_anchor: [INTERCORE]` dans les deux Cores
- **Problème :** Le Core LINK (`link.yaml`) n'est pas inclus dans le corpus fourni. Les bindings `[INTERCORE]` sont déclarés des deux côtés mais les nœuds de liaison réels sont invisibles. Toute faille de mauvais placement Constitution/Référentiel/LINK est indétectable.
- **Risque moteur :** Si le LINK contient de la logique métier qui duplique ou contredit un invariant constitutionnel, ce conflit est silencieux.
- **Scope :** `intercore_reference` / `governance`
- **Priorité :** **Critique**

#### A1-2 : `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` non déclaré (HIGH-02)

- **Support :** `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` (`[ARBITRAGE_2026_04_01][MOT-01]`) cite cet event dans son human_readable mais l'event n'est présent dans aucune section `EVENTS` du Référentiel ou de la Constitution.
- **Problème :** Un paramètre borne un seuil d'escalade vers un event inexistant. L'escalade ne peut pas être déclenchée techniquement.
- **Risque moteur :** L'apprenant peut rester indéfiniment en mode conservateur sans sortie déclarée.
- **Scope :** `runtime_state` / `patch_governance`
- **Priorité :** **Élevé**

#### A1-3 : Asymétrie de binding entre `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`

- **Support :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dans la Constitution déclenche `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` ; `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` est dans le Référentiel.
- **Problème :** Le paramètre de seuil est référentiel (`PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`) mais l'event le citant (`EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) mentionne le paramètre via son human_readable et sa condition, sans `depends_on` formel vers ce paramètre dans la Constitution. La dépendance est déclarative mais pas structurelle.
- **Risque moteur :** Lors d'un patch du seuil dans le Référentiel, l'event constitutionnel n'est pas automatiquement signalé comme affecté dans une chaîne de validation.
- **Scope :** `intercore_reference` / `runtime_evaluation`
- **Priorité :** **Modéré**

#### A1-4 : `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` — états de sortie du régime oscillatoire non bornés en durée

- **Support :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (`[ARBITRAGE_2026_04_01][MATRIX-01]`) décrit un régime oscillatoire "1 session consolidation → 1 session exploration → retour consolidation, sortie quand R atteint".
- **Problème :** La condition de sortie du régime oscillatoire est `R atteint`, mais aucune borne temporelle maximale ou compteur de cycles n'est déclaré. Si R n'est jamais atteint (KU créative sans multiplicateur R robuste), le régime oscillatoire est potentiellement infini.
- **Risque moteur :** Oscillation sans fin, bloquant la progression vers des KU dépendantes.
- **Scope :** `runtime_state`
- **Priorité :** **Élevé**

---

### Axe 2 — Solidité théorique

#### A2-1 : `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` — absence de paramètres opérationnels Référentiel

- **Support :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est déclaré dans la Constitution (`[S2][S20]`), `patchable: true`, mais aucun paramètre numérique correspondant (fourchette, référence) n'est défini dans le Référentiel.
- **Problème :** Le paramètre constitutionnel est déclaré comme "fenêtre constitutionnellement déclarée" mais la valeur opérationnelle reste indéterminée. L'implémentation doit inférer ou fixer une valeur sans support référentiel.
- **Risque théorique :** La maîtrise provisoire héritée peut être vérifiée sur une fenêtre arbitraire selon l'implémentation, violant le principe de fermeture locale.
- **Scope :** `runtime_evaluation`
- **Priorité :** **Modéré**

#### A2-2 : AR-N3 et calibration — effet borné sur AR-N1 mais absence de borne maximale de reweighting

- **Support :** `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` et `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS`
- **Problème :** La règle précise que le reweighting est "borné" et "temporaire", et que `PARAM_REFERENTIEL_PROXY_MIN_WEIGHT` (0.2) donne un seuil bas pour les proxys. Cependant, il n'existe pas de borne haute explicite sur l'ampleur du relèvement des proxys ni sur la réduction du poids d'AR-N1 pendant ce cycle.
- **Risque théorique :** Un reweighting non borné supérieurement pourrait dégrader AR-N1 à un poids quasi-nul, inversant la hiérarchie de signaux, ce qui contredit `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`.
- **Scope :** `runtime_state`
- **Priorité :** **Modéré**

#### A2-3 : KU créative — absence de chemin de feedback déterministe comme précondition de calibrage

- **Support :** `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` (Constitution) bloque le régime autonome si le feedback déterministe est absent. Mais `PARAM_REFERENTIEL_KU_CALIBRATION_CREATIVE_DURATION` (5–15 min) décrit le calibrage d'une KU créative sans vérifier que cette précondition de feedback est satisfaite.
- **Problème :** Le Référentiel peut calibrer une KU créative sans que la précondition constitutionnelle de chemin de feedback soit vérifiée au moment du calibrage.
- **Risque moteur :** Une KU créative peut passer le calibrage et être intégrée au graphe avant que son feedback déterministe soit déclaré, générant un état interdit en déploiement autonome.
- **Scope :** `analysis_design` / `runtime_calibration`
- **Priorité :** **Modéré**

---

### Axe 3 — États indéfinis moteur

#### A3-1 : Régime conservateur sans AR-N1 et sans proxys — sortie indéfinie (HIGH-02 complémentaire)

- **Support :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` + `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` + `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` (absent)
- **Problème :** Lorsque l'apprenant n'a pas d'AR-N1 ET que les proxys sont insuffisants (< 2 proxys franchissant leur seuil selon `RULE_REFERENTIEL_ADAPTIVE_REGIME_DETECTION_MIN_PROXIES`), le moteur applique un scaffolding conservateur. Le paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` borne la durée à 5 sessions avant escalade — mais l'event d'escalade n'existe pas. L'état est donc techniquement un puits sans sortie formalisée.
- **Risque moteur :** Blocage silencieux, jamais visible dans les logs sauf journalisation manuelle.
- **Scope :** `runtime_state`
- **Priorité :** **Élevé**

#### A3-2 : Oscillation `Consolidation + Exploration` sans condition de sortie d'urgence

Identique à A1-4 (voir ci-dessus).

#### A3-3 : Maîtrise provisoire non confirmée — comportement moteur non spécifié après expiration de la fenêtre

- **Support :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` — la fenêtre expire mais aucun event, rule ou action n'est déclaré pour traiter l'expiration sans confirmation.
- **Problème :** L'expiration de la fenêtre de maîtrise provisoire non confirmée ne génère aucun événement déclaré. Le moteur ne sait pas si la maîtrise doit être révoquée, maintenue ou escaladée.
- **Risque moteur :** Incohérence du modèle apprenant avec perte silencieuse d'information.
- **Scope :** `runtime_evaluation`
- **Priorité :** **Élevé**

---

### Axe 4 — Dépendances IA implicites

#### A4-1 : `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` — identification de la misconception

- **Support :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` (Constitution) suppose qu'une KU est "flaggée misconception". Aucun type, invariant ou rule ne décrit comment une misconception est détectée ou flaggée.
- **Problème :** Le flag `misconception` sur une KU implique une inférence sémantique (analyse du corpus, annotation experte, ou analyse de réponses) qui n'est pas formalisée dans le Core. Si ce flag est attribué par inférence IA en dehors des phases de design approuvées, cela viole `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`.
- **Scope :** `design_runtime` / `runtime_architecture`
- **Priorité :** **Modéré**

#### A4-2 : Évaluation de la composante T (transférabilité)

- **Support :** `TYPE_MASTERY_COMPONENT_T` — "Évaluation de transfert" avec comme condition "Maîtrise de base déjà établie."
- **Problème :** La transférabilité implique structurellement une évaluation dans un contexte différent du contexte d'apprentissage initial. Aucune procédure déterministe de sélection du "contexte de transfert" n'est formalisée. Le risque est que cette sélection nécessite une inférence contextuelle non locale.
- **Scope :** `runtime_evaluation` / `design`
- **Priorité :** **Faible**

---

### Axe 5 — Gouvernance

#### A5-1 : Version Constitution V1_9_FINAL et Référentiel V1_0_FINAL — cohérence de version non vérifiable sans LINK

- **Support :** La Constitution se réfère à `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` ; le Référentiel se réfère à `REF_CORE_LEARNIT_CONSTITUTION_V1_9_IN_REFERENTIEL`. Ces références croisées sont correctes et cohérentes.
- **Problème :** Sans le LINK, la version du LINK et sa compatibilité avec V1.9/V1.0 ne peuvent être vérifiées. Les patches issus de `[ARBITRAGE_2026_04_01]` apparaissent dans les deux Cores (nouvelles rules et events) mais il n'est pas possible de confirmer que ces patches ont été intégralement répercutés dans le LINK.
- **Scope :** `governance` / `versioning`
- **Priorité :** **Critique** (conditionnel à CRIT-01)

#### A5-2 : `[ARBITRAGE_2026_04_01]` — trace d'arbitrage non archivée dans le corpus

- **Support :** Plusieurs éléments portent `source_anchor: '[ARBITRAGE_2026_04_01][...]'` : `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`, `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS`, `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`, `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`.
- **Problème :** L'arbitrage `2026_04_01` est référencé mais son document source (`work/02_arbitrage/arbitrage.md` du run précédent ou un document d'inputs) n'est pas visible dans le corpus de ce run. La traçabilité est déclarative uniquement.
- **Scope :** `governance` / `versioning`
- **Priorité :** **Modéré**

---

### Axe 6 — Priorisation consolidée

| ID | Libellé | Couche | Priorité |
|---|---|---|---|
| CRIT-01 | LINK absent — bindings inter-Core non vérifiables | Intercore | **Critique** |
| CRIT-02 | LINK non-patché pour `[ARBITRAGE_2026_04_01]` vérifiable | Gouvernance | **Critique** (conditionnel) |
| HIGH-01 | `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` non déclaré | Référentiel / Constitution | **Élevé** |
| HIGH-02 | Régime oscillatoire `Consolidation+Exploration` sans borne de durée ni sortie de secours | Référentiel | **Élevé** |
| HIGH-03 | Maîtrise provisoire — expiration de fenêtre sans event de traitement | Constitution | **Élevé** |
| MOD-01 | `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — dépendance vers seuil Référentiel non structurelle | Constitution | **Modéré** |
| MOD-02 | `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` — pas de paramètre numérique Référentiel | Constitution / Référentiel | **Modéré** |
| MOD-03 | Reweighting AR-N1 — absence de borne haute sur la réduction du poids AR-N1 | Référentiel | **Modéré** |
| MOD-04 | KU créative — calibrage possible sans précondition de feedback déterministe | Référentiel | **Modéré** |
| MOD-05 | Trace de l'arbitrage `[ARBITRAGE_2026_04_01]` non accessible dans le corpus actuel | Gouvernance | **Modéré** |
| MOD-06 | Misconception flag — procédure d'attribution non formalisée | Constitution | **Modéré** |
| FAIBLE-01 | Composante T — sélection du contexte de transfert potentiellement non locale | Constitution | **Faible** |

---

## Risques prioritaires

### CRIT-01 — LINK absent
**Action requise :** Fournir `docs/cores/current/link.yaml` en input du pipeline avant de passer à STAGE_02_ARBITRAGE. Sans cela, aucune validation de séparation des couches n'est possible.

### HIGH-01 — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` manquant
**Action requise :** Déclarer l'event dans le Référentiel (ou la Constitution selon la couche appropriée), ou retirer la référence dans `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` si l'escalade est traitée différemment (action externe, log uniquement).

### HIGH-02 — Régime oscillatoire sans borne de durée
**Action requise :** Ajouter un paramètre référentiel de borne maximale de cycles oscillatoires (ex. `PARAM_REFERENTIEL_OSCILLATION_MAX_CYCLES`) et une condition de sortie de secours (ex. retour en mode conservateur après N cycles si R non atteint).

### HIGH-03 — Maîtrise provisoire — expiration sans traitement
**Action requise :** Déclarer un event d'expiration de fenêtre de maîtrise provisoire non confirmée et une rule de traitement (révocation, mise en attente diagnostique, ou escalade).

---

## Corrections à arbitrer avant patch

1. **CRIT-01** : Obtenir le LINK et relancer un challenge complet incluant le LINK.
2. **HIGH-01** : Arbitrer entre (a) déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel avec son action associée, ou (b) remplacer la référence par une action directe déjà déclarée (`ACTION_APPLY_LIGHT_REVERSIBLE_SCAFFOLDING` ne couvre pas la sortie d'escalade).
3. **HIGH-02** : Arbitrer la borne maximale du régime oscillatoire — dans le Référentiel (paramètre) ou dans la Constitution (invariant).
4. **HIGH-03** : Arbitrer la sémantique de l'expiration de maîtrise provisoire — révocation automatique ou escalade diagnostique. Cette décision a un impact sur la composante R (robustesse) et sur `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`.
5. **MOD-01** : Arbitrer l'ajout d'un `depends_on` formel dans `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` vers `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` via une référence intercore structurelle.
6. **MOD-02** : Arbitrer si `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` doit recevoir des bornes numériques dans le Référentiel (nouveau paramètre) ou si sa gestion opérationnelle relève du LINK.
7. **MOD-03** : Arbitrer l'introduction d'un paramètre de borne haute sur le reweighting AR-N1 (ex. `PARAM_REFERENTIEL_AR_N1_MIN_WEIGHT_FLOOR` ou borne implicite dans `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`).
