# CHALLENGE REPORT — NemoTron
## STAGE_01_CHALLENGE · Pipeline Constitution

- **Challenger:** NemoTron (auditeur adversarial)
- **Cores analysés:**
  - Constitution: `CORE_LEARNIT_CONSTITUTION_V1_9`
  - LINK: `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`
  - Référentiel: `CORE_LEARNIT_REFERENTIEL_V1_0` *(référencé, non inspecté en détail)*
- **Date:** 2026-04-01

---

## Résumé exécutif

Le système est globalement bien structuré : la séparation Constitution / Référentiel / LINK est tenue, la gouvernance patch est défensive, et les invariants constitutionnels sont clairement non-patchables. Néanmoins, plusieurs zones de fragilité ont été identifiées lors de l'audit adversarial :

1. **La divergence MSC/perception (nouvel EVENT + RULE)** introduite par `ARBITRAGE_2026_04_01` est fonctionnellement incomplète : le `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dépend d'un `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` qui n'est pas encore bindé dans le LINK, exposant un état indéfini moteur.
2. **La composante T (transférabilité)** est déclarée séparée de la maîtrise de base, mais aucune règle ne précise comment elle est *déclenchée* (observable, planifiable) ni ce qu'il advient si T n'est jamais évalué. Aucun EVENT ne couvre le cas `T_never_evaluated`.
3. **Le MODE_PROBATOIRE** de la gamification (`RULE_UNVERIFIED_GAMIFICATION_PROBATION`) ne définit pas de condition de sortie ni de durée. Le moteur peut rester indéfiniment en mode probatoire sans escalade.
4. **`INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`** déclare une escalade obligatoire mais ne définit pas le canal d'escalade, ni l'acteur destinataire. Cela reste lettre morte en runtime.
5. **Bindings LINK partiels sur le nouveau binding `MSC_PERCEPTION_DIVERGENCE`** : le LINK V1_9__V1_0 ne contient pas de `TYPE_BINDING` reliant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` au `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`, ce qui signifie que la résolution du seuil est implicite et non auditables.
6. **`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`** (introduite en PATCH_V1_9__STAGE03) n'a pas de CONSTRAINT correspondante interdisant explicitement la complétion implicite des axes au niveau du Référentiel. Le LINK ne porte pas ce binding de protection.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### [AX1-01] `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — Paramètre référentiel non bindé dans le LINK

- **Localisation Constitution :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`
- **Dépendance déclarée :** `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
- **Constat :** Ce paramètre est référencé dans la `depends_on` de l'EVENT mais aucun `TYPE_BINDING` dans le LINK ne matérialise la résolution de ce seuil vers le Référentiel.
- **Risque :** Si le moteur cherche à évaluer le trigger (`N sessions consécutives`), aucune chaîne d'autorité explicite ne pointe vers la valeur effective. La résolution reste implicite et dépend d'une inférence sémantique — ce qui est interdit par `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.
- **Sévérité :** **CRITIQUE**
- **Couche :** LINK (binding manquant), Constitution (event fonctionnellement fermé)

---

#### [AX1-02] Composante T — Absence de déclencheur d'évaluation et d'EVENT `T_never_evaluated`

- **Localisation Constitution :** `TYPE_MASTERY_COMPONENT_T`, `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`
- **Constat :** T est déclarée séparée de la maîtrise de base, évaluée uniquement sur maîtrise de base acquise. Or :
  - Aucune règle ne décrit *quand* ou *comment* une évaluation T est déclenchée.
  - Aucun EVENT ne gère le cas où T n'a jamais été évalué après N sessions post-maîtrise de base.
  - Le moteur ignore donc si T est `unknown`, `pending`, `never_scheduled` ou `deferred`.
- **Risque :** État indéfini silencieux : l'apprenant reste indéfiniment avec une maîtrise de base sans que le système déclenche un cycle de transfert. Ce n'est pas forcément un bug moteur, mais une lacune de gouvernance pédagogique.
- **Sévérité :** **ÉLEVÉ**
- **Couche :** Constitution (règle et event manquants)

---

#### [AX1-03] `RULE_UNVERIFIED_GAMIFICATION_PROBATION` — Absence de condition de sortie du mode probatoire

- **Localisation Constitution :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION`
- **Constat :** La règle est déclenchée à l'entrée mais aucun mécanisme (EVENT, RULE, PARAM) ne couvre :
  - La durée maximale du mode probatoire
  - Les critères de validation permettant de sortir du mode probatoire
  - L'escalade en cas de non-résolution
- **Risque :** Mode probatoire permanent sans issue définie. Le moteur ne peut pas sauter automatiquement à un état stable.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Constitution (complétion logique manquante), Référentiel (paramétrage possible mais non relié)

---

#### [AX1-04] `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` — Canal d'escalade indéfini

- **Localisation Constitution :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
- **Constat :** L'invariant déclare `effect: Escalade obligatoire hors session vers la chaîne d'analyse/correction` mais ne précise pas :
  - La cible de l'escalade (qui/quoi reçoit la notification)
  - Le format ou canal (log, notification externe, queue)
  - Si une ACTION est associée à cette escalade
- **Risque :** L'invariant est déclaré mais inopérant en runtime : aucun acteur ne peut le traiter de façon déterministe.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Constitution (action manquante ou action existante non bindée)

---

#### [AX1-05] `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` — Absence de CONSTRAINT miroir côté Référentiel/LINK

- **Localisation Constitution :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`
- **Constat :** Cette règle interdit la complétion implicite des axes d'état au niveau constitutionnel. Cependant :
  - Le LINK ne porte pas de `TYPE_BINDING` ou `CONSTRAINT` protégeant explicitement cette interdiction côté Référentiel.
  - Rien n'empêche un Référentiel futur de définir un mécanisme de fallback implicite pour les axes inconnus.
- **Risque :** La protection constitutionnelle n'est pas propagée formellement dans le système fédéré.
- **Sévérité :** **MODÉRÉ**
- **Couche :** LINK (binding de protection manquant)

---

### Axe 2 — Solidité théorique

#### [AX2-01] Composante R (robustesse temporelle) — Seuil `seuil_R` indéfini côté Constitution

- **Localisation Constitution :** `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `TYPE_MASTERY_COMPONENT_R`
- **Constat :** `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` référence `seuil_R` délégué au Référentiel. Le LINK porte un binding MSC mais ne lie pas explicitement `seuil_R` de l'EVENT_LONG_INTERRUPTION au Référentiel. L'interruption de la chaîne de délégation est partielle.
- **Risque :** Lors d'une reprise diagnostique, la condition de déclenchement est non-résolvable sans inférence si le LINK ne couvre pas ce paramètre.
- **Sévérité :** **MODÉRÉ**
- **Couche :** LINK (binding `EVENT_LONG_INTERRUPTION → PARAM_REFERENTIEL_seuil_R` absent)

#### [AX2-02] Axe Calibration (`TYPE_STATE_AXIS_CALIBRATION`) — Sources autorisées non déclarées au niveau Constitution

- **Localisation Constitution :** `TYPE_STATE_AXIS_CALIBRATION`
- **Constat :** L'axe Calibration dépend d'`indices de calibration disponibles` mais aucune liste normative des sources autorisées n'est déclarée dans la Constitution (contrairement à l'axe Activation qui liste explicitement AR-N1, ou VC qui liste AR-N2). La délégation au Référentiel est implicite.
- **Risque :** Si AR-N3 est la source principale de calibration (comme suggéré par le LINK binding `AR-N3 → TYPE_STATE_AXIS_CALIBRATION`), ce binding n'est pas ancré dans la Constitution elle-même, créant une asymétrie de gouvernance.
- **Sévérité :** **FAIBLE**
- **Couche :** Constitution (incomplétude de la déclaration de sources autorisées)

---

### Axe 3 — États indéfinis moteur

#### [AX3-01] `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — Condition de trigger non évaluable sans binding LINK

*Cf. AX1-01 — Risque moteur direct : oscillation indéfinie entre maîtrise déclarée et perception persistante.*

#### [AX3-02] Composante T — Statut `unknown` jamais résolu → absence de fermeture locale

- Si T n'est jamais évalué, le moteur ne sait pas si T est `unknown` (jamais tenté), `deferred` (délibérément reporté), ou `not_applicable`. L'absence d'EVENT couvrant cette situation peut générer une dérive silencieuse.

#### [AX3-03] Mode probatoire gamification — Boucle ouverte

- Si la gamification reste en mode probatoire sans déclenchement de sortie, le moteur reste dans un état stable de surface mais potentiellement incohérent avec les objectifs pédagogiques réels. Aucune alerte n'est prévue.

---

### Axe 4 — Dépendances IA implicites

#### [AX4-01] `ACTION_LOG_AR_PROXY_DISCORDANCE` — Interprétation des poids proxy

- La règle `RULE_AR_N1_OVERRIDES_PROXY` logue la discordance et pointe vers une `révision des poids proxy`. Cette révision est implicitement sémantique : aucun mécanisme automatique déterministe ne définit comment les poids sont révisés. L'inférence reste humaine/externe.
- **Sévérité :** **FAIBLE** (attendu, mais non documenté comme hors-portée locale)

#### [AX4-02] `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE` — Périmètre non explicitement listé

- L'interdiction d'inférence psychologique autonome est déclarée comme CONSTRAINT mais sans liste des inférences interdites. Un moteur implémenteur devra inférer lui-même ce qui est couvert.
- **Sévérité :** **FAIBLE**

---

### Axe 5 — Gouvernance

#### [AX5-01] LINK — VERSION non synchronisée avec la Constitution si la Constitution est patchée sans patch LINK parallèle

- **Constat :** Les deux derniers patches de la Constitution (PATCH_V1_9, ARBITRAGE_2026_04_01) ont tous les deux produit de nouveaux éléments dans la Constitution et le LINK. Cependant, il n'existe pas d'invariant ou de règle exigeant un patch LINK systématique à chaque patch Constitution modifiant des éléments inter-Core.
- **Risque :** Désynchronisation version LINK/Constitution lors d'un futur patch Constitution qui oublie de mettre à jour le LINK.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Gouvernance inter-Core

#### [AX5-02] `source_anchor: '[ARBITRAGE_2026_04_01]'` — Traçabilité d'arbitrage non liée à un fichier d'arbitrage canonique

- **Constat :** Les éléments issus de l'arbitrage du 2026-04-01 portent `source_anchor: '[ARBITRAGE_2026_04_01]'` mais il n'y a pas de fichier d'arbitrage correspondant dans `work/02_arbitrage/` (le pipeline a peut-être été court-circuité). La traçabilité est nominale mais non matérialisée.
- **Sévérité :** **MODÉRÉ**
- **Couche :** Traçabilité / Gouvernance

---

### Axe 6 — Priorisation des risques

| Priorité | ID | Titre court | Couche |
|---|---|---|---|
| **CRITIQUE** | AX1-01 | Binding LINK manquant sur `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` | LINK |
| **ÉLEVÉ** | AX1-02 | Composante T sans déclencheur ni EVENT `T_never_evaluated` | Constitution |
| **MODÉRÉ** | AX1-03 | Gamification probatoire sans condition de sortie | Constitution |
| **MODÉRÉ** | AX1-04 | Escalade dérive patch sans canal défini | Constitution |
| **MODÉRÉ** | AX1-05 | `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` sans binding LINK miroir | LINK |
| **MODÉRÉ** | AX2-01 | `seuil_R` interruption longue non bindé dans LINK | LINK |
| **MODÉRÉ** | AX5-01 | Pas d'invariant exigeant patch LINK synchrone au patch Constitution | Gouvernance |
| **MODÉRÉ** | AX5-02 | `ARBITRAGE_2026_04_01` non matérialisé dans `work/02_arbitrage/` | Traçabilité |
| **FAIBLE** | AX2-02 | Sources autorisées Calibration non listées dans Constitution | Constitution |
| **FAIBLE** | AX4-01 | Révision poids proxy implicitement sémantique | Constitution |
| **FAIBLE** | AX4-02 | Périmètre CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE non listé | Constitution |

---

## Risques prioritaires

### CRITIQUE — AX1-01

> Le binding LINK entre `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` est absent. Le moteur ne peut pas résoudre le seuil de divergence de façon déterministe. Ce risque viole directement `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` et expose un état indéfini runtime.

**Correction à arbitrer :** Ajouter un `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` dans le LINK, bindant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` au `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` référentiel.

---

### ÉLEVÉ — AX1-02

> La composante T est déclarée mais son cycle de vie (planification, déclenchement, état `unknown` persistant) n'est pas gouverné. Le moteur n'a aucun signal pour initier une évaluation de transfert.

**Correction à arbitrer :** Déclarer un EVENT `EVENT_T_EVALUATION_OVERDUE` et une RULE associée permettant de signaler ou déclencher une session d'évaluation de transfert après maîtrise de base établie. Paramétrer via le Référentiel la fenêtre d'activation.

---

## Corrections à arbitrer avant patch

| Priorité | Correction proposée | Couche cible | Impact_scope estimé |
|---|---|---|---|
| CRITIQUE | Ajouter `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` dans LINK | LINK | Faible, additive |
| ÉLEVÉ | Ajouter `EVENT_T_EVALUATION_OVERDUE` + RULE de déclenchement T dans Constitution | Constitution | Faible, additive |
| MODÉRÉ | Ajouter `PARAM_GAMIFICATION_PROBATION_MAX_DURATION` + EVENT de sortie probatoire | Constitution + Référentiel | Faible, additive |
| MODÉRÉ | Formaliser canal d'escalade de `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` via ACTION dédiée | Constitution | Faible, additive |
| MODÉRÉ | Ajouter CONSTRAINT ou BINDING LINK protégeant `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` côté Référentiel | LINK | Faible, additive |
| MODÉRÉ | Ajouter binding LINK `EVENT_LONG_INTERRUPTION → PARAM_REFERENTIEL_seuil_R` | LINK | Faible, additive |
| MODÉRÉ | Ajouter INV ou RULE dans Constitution exigeant patch LINK synchrone si patch Constitution modifie bindings inter-Core | Constitution / Gouvernance | Modéré |
| MODÉRÉ | Matérialiser l'arbitrage `ARBITRAGE_2026_04_01` dans `work/02_arbitrage/` rétroactivement | Traçabilité | Nul sur le moteur |
