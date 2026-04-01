# CHALLENGE REPORT — NemoTron bis
## STAGE_01_CHALLENGE · Pipeline Constitution

- **Challenger:** NemoTron (auditeur adversarial, second passage)
- **Angle spécifique :** Cohérence Référentiel ↔ Constitution, complétude des événements systémiques issus de `ARBITRAGE_2026_04_01`, fermeture des chaînes d'escalade
- **Cores analysés :**
  - Constitution: `CORE_LEARNIT_CONSTITUTION_V1_9`
  - Référentiel: `CORE_LEARNIT_REFERENTIEL_V1_0`
  - LINK: `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`
- **Date:** 2026-04-01

---

## Résumé exécutif

Ce second challenge cible spécifiquement les éléments issus de l'arbitrage du `2026-04-01` qui ont été injectés dans les Cores sans que la chaîne complète soit fermée. Le Référentiel V1.0 contient plusieurs PARAMs et EVENTs référencés par `ARBITRAGE_2026_04_01` qui ont leur pendant dans la Constitution, mais dont les bindings LINK et les actions moteur restent incomplets ou absents. En outre, le système d'investigation systémique introduit dans le Référentiel est orphelin côté Constitution : aucune règle constitutionnelle ne gouverne son déclenchement ni sa clôture.

**Principaux risques :**
1. `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` est référencé dans `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` mais absent du Référentiel comme EVENT déclaré.
2. `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` est patchable mais son homologue constitutionnel (la logique de résolution de conflits entre régimes) n'est pas déclaré comme RULE ou INVARIANT dans la Constitution.
3. `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` référence une `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans la Constitution — mais cette RULE n'existe pas dans la Constitution V1.9.
4. `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` déclenche un `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` qui n'est pas déclaré dans le Référentiel.
5. Le Référentiel décrit une `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` qui introduit la notion de **révocation post-maîtrise** — concept absent de la Constitution, créant une logique métier autonome dans le Référentiel sans ancrage constitutionnel.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### [BX1-01] `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` — EVENT déclenché mais non déclaré

- **Localisation Référentiel :** `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`
- **Constat :** Ce paramètre décrit explicitement un `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` comme effet (`effect: Référence 5 sessions... avant déclenchement de l'EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`). Or cet EVENT n'est déclaré dans ni le Référentiel ni la Constitution.
- **Risque :** Déclencheur orphelin. Le moteur ne peut pas réagir à un EVENT qu'il ne connaît pas. La chaîne de réaction (escalade après scaffolding conservateur prolongé) est brisée.
- **Sévérité :** **CRITIQUE**
- **Couche :** Référentiel (EVENT manquant)

---

#### [BX1-02] `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` — EVENT référencé mais non déclaré

- **Localisation Référentiel :** `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD`
- **Constat :** Le paramètre décrit l'effet comme `déclenchement de EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED`. Cet EVENT n'apparaît pas dans la section `EVENTS` du Référentiel. Il n'existe pas non plus dans la Constitution.
- **Risque :** Même nature que BX1-01. La supervision multi-signaux n'a pas de sortie moteur formalisée.
- **Sévérité :** **CRITIQUE**
- **Couche :** Référentiel (EVENT manquant)

---

#### [BX1-03] `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` — Référence à `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` absente de la Constitution

- **Localisation Référentiel :** `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING`
- **Constat :** La `human_readable` de cette règle indique explicitement `autorisée constitutionnellement par RULE_VC_AXIS_DEACTIVATION_AUTHORIZED`. Cette RULE n'existe pas dans la Constitution V1.9. La désactivation de l'axe VC est donc présentée comme constitutionnellement autorisée sans l'ancrage effectif.
- **Risque :** Un auditeur ou implémenteur se fiera à une autorisation constitutionnelle inexistante. Lors d'un patch Constitution futur, ce pointage fantôme passera inapercu.
- **Sévérité :** **ÉLEVÉ**
- **Couche :** Référentiel (référence fantôme vers la Constitution)

---

#### [BX1-04] `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` — Logique métier autonome dans le Référentiel

- **Localisation Référentiel :** `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`
- **Constat :** Cette règle distingue `rétrogradation courante` et `révocation post-maîtrise`. La **révocation post-maîtrise** est un concept inexistant dans la Constitution. La Constitution ne définit que `EVENT_MSC_DOWNGRADE`. Le Référentiel introduit ici une catégorie épistemique autonome sans ancrage constitutionnel, ce qui viole `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` (même si la CONSTRAINT cible le LINK, le principe s'étend à tout Core non-autoritaire).
- **Risque :** Le moteur pourrait implémenter deux logiques de dégradation divergentes sans arbitre constitutionnel. La Constitution ne peut pas invalider la révocation post-maîtrise si elle ne la définit pas.
- **Sévérité :** **ÉLEVÉ**
- **Couche :** Référentiel (logique métier autonome), Constitution (concept non ancré)

---

#### [BX1-05] `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` — Règle patchable sans INVARIANT constitutionnel gouvernant le cadre de résolution de conflits

- **Localisation Référentiel :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`
- **Constat :** Cette règle est marquée `patchable: true` et définit une table de priorité entre régimes adaptatifs. La Constitution déclare les régimes adaptatifs (`TYPE_AUTONOMY_REGIME`) mais ne définit aucune règle gouvernant leur résolution de conflit. Le Référentiel peut donc être patché pour modifier la priorité Conserver/Explorer/Détresse sans aucun garde-fou constitutionnel.
- **Risque :** Un patch Référentiel pourrait inverser la priorité Détresse (actuellement toujours dominante) sans violation formelle des invariants.
- **Sévérité :** **ÉLEVÉ**
- **Couche :** Constitution (invariant de priorité régime manquant)

---

#### [BX1-06] `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` — Binding LINK absent

- **Localisation Référentiel :** `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`
- **Constat :** Ce paramètre gouverne la désactivation de l'axe VC constitutionnel (`TYPE_STATE_AXIS_VALUE_COST`). Le LINK ne porte pas de `TYPE_BINDING` reliant ce paramètre référentiel à l'axe constitutionnel concerné.
- **Risque :** Même famille que AX1-01 du premier challenge : résolution implicite, non auditable.
- **Sévérité :** **MODÉRÉ**
- **Couche :** LINK (binding manquant)

---

### Axe 2 — Solidité théorique

#### [BX2-01] `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` — `patchable: false` mais `parameterizable: true` — tension interne

- **Constat :** Cette règle est `patchable: false` (la logique ne peut pas être modifiée) mais `parameterizable: true` (les paramètres peuvent être ajustés). Cependant, aucun PARAM de cette règle n'est explicitement listé dans sa `depends_on`. Les paramètres affectés (`PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS`, `PARAM_REFERENTIEL_PROXY_MIN_WEIGHT`) sont référencés dans `depends_on` mais ne sont pas paramétriquement contraints par une fourchette minimale de protection.
- **Risque :** Un patch portant `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS` à 1 rend le reweighting quasi-permanent, modifiant de facto la hiérarchie de confiance des signaux de façon significative sans toucher la logique.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Référentiel (borne inférieure manquante sur le paramètre)

#### [BX2-02] Interleaving de contenus — Condition `A au seuil` sans définition du seuil A dans la règle

- **Localisation Référentiel :** `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A`
- **Constat :** La condition exige `composante A au seuil sur les KU concernées` mais ne pointe pas vers `PARAM_REFERENTIEL_MSC_AUTONOMY_SUCCESS_COUNT` comme valeur de référence. C'est une dépendance implicite.
- **Risque :** Un implémenteur peut choisir un seuil A arbitraire pour l'interleaving, différent de celui validé pour le MSC.
- **Sévérité :** **FAIBLE**
- **Couche :** Référentiel (dépendance implicite)

---

### Axe 3 — États indéfinis moteur

#### [BX3-01] Investigation systémique — Entrée définie, sortie indéfinie

- `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` décrit le comportement pendant l'investigation (mode minimal, gel des ajustements agressifs, journalisation renforcée). Mais :
  - La **clôture** de l'investigation systémique n'est pas décrite : ni EVENT de clôture, ni RULE de sortie, ni PARAM de durée maximale.
  - L'escalade hors session est mentionnée (`si persistance sur la fenêtre configurée`) mais la `fenêtre configurée` n'est pas liée à un PARAM dédié.
- **Risque :** Le moteur peut rester indéfiniment en mode investigation systémique sans mécanisme de résolution.
- **Sévérité :** **ÉLEVÉ**
- **Couche :** Référentiel (cycle d'état non fermé)

#### [BX3-02] Mode régime oscillatoire (Consolidation + Exploration) — Condition de sortie vague

- **Localisation Référentiel :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`
- **Constat :** Le régime oscillatoire `Consolidation + Exploration` est décrit comme `sortie quand R atteint`. Mais `R atteint` dépend du MSC de quelle KU ? Dans un graphe multi-KU, plusieurs KU peuvent être en état de régime oscillatoire simultanément avec des statuts R différents. La règle ne spécifie pas si la sortie est locale (par KU) ou globale (ensemble des KU actives).
- **Risque :** État oscillatoire potentiellement permanent si aucune KU individuelle n'atteint R, ou sortie prématurée si une seule KU atteint R.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Référentiel (granularité de sortie non définie)

---

### Axe 4 — Dépendances IA implicites

#### [BX4-01] `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` — `cause locale non résolue` est un critère sémantique

- La condition `Cause locale non résolue ou dérive transversale suspectée` nécessite une inférence sémantique pour être évaluée. Ce critère ne peut pas être déterminé localement sans mécanisme de diagnostic automatique. Il repose implicitement sur une analyse humaine hors session.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Référentiel (critère non déterministe)

---

### Axe 5 — Gouvernance

#### [BX5-01] `ARBITRAGE_2026_04_01` — Couverture partielle des décisions dans les Cores

- Les éléments tagés `[ARBITRAGE_2026_04_01]` dans les trois Cores sont :
  - **Constitution :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`
  - **Référentiel :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`, `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS`, `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`, `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS`, `PARAM_REFERENTIEL_SYSTEMIC_INVESTIGATION_SESSION_THRESHOLD`, `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
  - **LINK :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING`
- **Constat :** L'arbitrage a produit des éléments sur 3 couches, mais plusieurs éléments sont orphelins (EVENTs non déclarés, références fantômes). Il manque un binding LINK pour `MSC_PERCEPTION_DIVERGENCE` (déjà couvert en AX1-01 du premier challenge) et un binding LINK pour la désactivation VC.
- **Sévérité :** **ÉLEVÉ** (impact cumulatif)
- **Couche :** Gouvernance inter-Core

#### [BX5-02] Référentiel `patchable: false` sur `PARAM_REFERENTIEL_R_MULTIPLIER_CREATIVE_FALLBACK` — Cohérence avec Constitution

- Ce paramètre est `patchable: false` et `parameterizable: false` dans le Référentiel (valeur fixée à ×1). Cependant, `TYPE_MASTERY_COMPONENT_R` dans la Constitution est `parameterizable: true`, ce qui suggère que les seuils R peuvent être ajustés. La rigidité du fallback créatif n'est pas justifiée par un invariant constitutionnel explicite.
- **Sévérité :** **FAIBLE**
- **Couche :** Gouvernance (asymétrie de patchabilité non documentée)

---

### Axe 6 — Priorisation des risques

| Priorité | ID | Titre court | Couche |
|---|---|---|---|
| **CRITIQUE** | BX1-01 | `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` déclaré dans PARAM mais absent de tout Core | Référentiel |
| **CRITIQUE** | BX1-02 | `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` déclaré dans PARAM mais absent de tout Core | Référentiel |
| **ÉLEVÉ** | BX1-03 | Référence fantôme `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans Référentiel | Référentiel / Constitution |
| **ÉLEVÉ** | BX1-04 | Révocation post-maîtrise — logique métier autonome sans ancrage constitutionnel | Référentiel / Constitution |
| **ÉLEVÉ** | BX1-05 | Pas d'invariant constitutionnel protégeant la priorité Détresse dans la matrice régimes | Constitution |
| **ÉLEVÉ** | BX3-01 | Investigation systémique sans condition de clôture ni EVENT de sortie | Référentiel |
| **ÉLEVÉ** | BX5-01 | Couverture partielle de `ARBITRAGE_2026_04_01` — impact cumulatif | Gouvernance |
| **MODÉRÉ** | BX1-06 | Binding LINK manquant `VC_UNOBSERVABLE_WINDOW → TYPE_STATE_AXIS_VALUE_COST` | LINK |
| **MODÉRÉ** | BX2-01 | Borne inférieure manquante sur `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS` | Référentiel |
| **MODÉRÉ** | BX3-02 | Régime oscillatoire Consolidation+Exploration : granularité de sortie non définie | Référentiel |
| **MODÉRÉ** | BX4-01 | Critère `cause locale non résolue` non déterministe dans investigation systémique | Référentiel |
| **FAIBLE** | BX2-02 | Dépendance implicite `seuil A interleaving` vs `PARAM MSC_AUTONOMY_SUCCESS_COUNT` | Référentiel |
| **FAIBLE** | BX5-02 | Asymétrie patchabilité `R_MULTIPLIER_CREATIVE_FALLBACK` non justifiée par invariant | Gouvernance |

---

## Risques prioritaires

### CRITIQUE — BX1-01 + BX1-02

> Deux EVENTs référencés dans des PARAMs référentiels issus de `ARBITRAGE_2026_04_01` n'existent pas en tant qu'ENTITEs déclarées dans les Cores : `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` et `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED`. Les chaînes de réaction correspondantes sont brisées.

**Corrections à arbitrer :** Déclarer ces deux EVENTs dans le Référentiel avec leurs `depends_on`, `relations` et `logic` adéquats.

---

### ÉLEVÉ — BX1-03

> `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` invoque une autorisation constitutionnelle inexistante. Ce pointage fantôme crée une fausse sécurité de gouvernance.

**Correction à arbitrer :** Soit ajouter `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans la Constitution, soit retirer la mention de cette autorisation dans le Référentiel et la remplacer par une référence à un invariant existant.

---

### ÉLEVÉ — BX1-04

> La révocation post-maîtrise est un concept métier autonome dans le Référentiel sans définition constitutionnelle. Le Référentiel ne peut pas créer de catégories épistémiques non prévues par la Constitution.

**Correction à arbitrer :** Soit ancrer `post-mastery revocation` dans la Constitution comme concept dérivé de `EVENT_MSC_DOWNGRADE`, soit reformuler la règle référentielle comme un cas particulier de rétrogradation MSC.

---

## Corrections à arbitrer avant patch

| Priorité | Correction proposée | Couche cible | Impact_scope estimé |
|---|---|---|---|
| CRITIQUE | Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans Référentiel | Référentiel | Faible, additive |
| CRITIQUE | Déclarer `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` dans Référentiel | Référentiel | Faible, additive |
| ÉLEVÉ | Ajouter `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans Constitution OU corriger la référence dans Référentiel | Constitution ou Référentiel | Faible |
| ÉLEVÉ | Ancrer la révocation post-maîtrise dans la Constitution comme dérivé de `EVENT_MSC_DOWNGRADE` | Constitution | Modéré |
| ÉLEVÉ | Ajouter INV constitutionnel protégeant la priorité Détresse dans la résolution de conflits régimes | Constitution | Faible, additive |
| ÉLEVÉ | Ajouter EVENT de clôture d'investigation systémique + PARAM de durée max dans Référentiel | Référentiel | Faible, additive |
| MODÉRÉ | Ajouter binding LINK `PARAM_VC_UNOBSERVABLE_WINDOW → TYPE_STATE_AXIS_VALUE_COST` | LINK | Faible, additive |
| MODÉRÉ | Définir borne inférieure protectrice sur `PARAM_REFERENTIEL_LOW_AR_CALIBRATION_CONSECUTIVE_BILANS` | Référentiel | Faible |
| MODÉRÉ | Préciser la granularité de sortie (par KU ou globale) du régime oscillatoire | Référentiel | Faible |
