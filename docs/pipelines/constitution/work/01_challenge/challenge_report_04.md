# CHALLENGE REPORT — constitution pipeline
# STAGE_01_CHALLENGE — Run 04

pipeline: constitution
stage: STAGE_01_CHALLENGE
run: 04
date: 2026-03-31
inputs:
  - docs/cores/current/constitution.yaml (CORE_LEARNIT_CONSTITUTION_V1_8)
  - docs/cores/current/referentiel.yaml (CORE_LEARNIT_REFERENTIEL_V0_6)
  - docs/cores/current/link.yaml (LINK_CONSTITUTION_V1_8__REFERENTIEL_V0_6)
focus_note: none

---

## Résumé exécutif

Ce run 04 adopte un angle complémentaire aux runs 02, 03 et 05 : il se concentre sur les **failles de fermeture logique au niveau des boucles de décision moteur** plutôt que sur les lacunes de binding ou de versioning. L'audit révèle **neuf risques**, dont deux critiques — distincts de ceux déjà identifiés dans les runs précédents.

Les deux critiques portent sur :
1. **L'absence de garde-fou à la divergence entre état MSC calculé et état MSC perçu par l'apprenant** : le moteur peut maintenir un état apprenant stabilisé que l'apprenant conteste, sans mécanisme de résolution formalisé.
2. **La non-spécification du comportement moteur lorsque plusieurs règles d'activation de régime adaptatif se déclenchent simultanément** (matrice 3×3 : cas de cellule de frontière).

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### CRITIQUE — Divergence état MSC calculé / état perçu par l'apprenant sans mécanisme de résolution

- La Constitution définit `ACTION_INFORM_LEARNER` comme action disponible, mais uniquement déclenché sur patch/rejet (`scope: patch_architecture`).
- Aucune règle ne précise le comportement si un apprenant soumet un AR-N1 déclarant un état fortement discordant avec le MSC calculé (ex. P=high calculé, AR-N1 = "total blocage").
- `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER` priorise AR-N1 pour l'axe Activation, mais le MSC (composante P) ne s'appuie que sur des performances objectives — les deux systèmes peuvent diverger durablement sans que cette tension soit nommée ni résolue.
- Un apprenant avec P=atteint mais Activation=détresse persistante peut recevoir des tâches de niveau autonome tout en signalant en boucle un état de blocage. Aucun event ni règle ne capture cette contradiction MSC↔état.
- **Ancrage** : `ACTION_INFORM_LEARNER`, `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER`, `TYPE_MASTERY_COMPONENT_P`, `TYPE_STATE_AXIS_ACTIVATION`
- **Couche** : Constitution + Référentiel

#### CRITIQUE — Matrice de régimes adaptatifs 3×3 : cellules de frontière non spécifiées

- `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` déclare une matrice 3×3 avec activation progressive.
- La matrice a nécessairement des cellules de frontière (ex. simultanément sous-défi sur Activation ET détresse sur VC ET calibration haute). Aucune règle de priorité entre régimes n'est définie pour les cas où deux ou trois axes franchissent simultanément des seuils opposés.
- `RULE_REFERENTIEL_ADAPTIVE_REGIME_DETECTION_MIN_PROXIES` exige 2 proxys franchissant leur seuil, mais ne précise pas le comportement si les proxys signalent des régimes contradictoires (ex. proxy 1 → sous-défi, proxy 2 → détresse).
- **Ancrage** : `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX`, `RULE_REFERENTIEL_ADAPTIVE_REGIME_DETECTION_MIN_PROXIES`
- **Couche** : Référentiel

#### Élevé — Condition d'activation de l'interleaving de contenus : séquencement non garanti

- `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A` conditionne l'interleaving de contenus à P∧A atteints sur les KU concernées, avec stabilité minimale.
- Mais si deux KU éligibles à l'interleaving ont des dates de dernière présentation très différentes, `RULE_REFERENTIEL_COVERAGE_REBALANCING_ACTIVATION` peut forcer un rééquilibrage de couverture qui réintroduit une KU non encore stabilisée.
- Ces deux règles peuvent produire des séquençages contradictoires sur le même cycle sans règle de résolution explicite.
- **Ancrage** : `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A`, `RULE_REFERENTIEL_COVERAGE_REBALANCING_ACTIVATION`
- **Couche** : Référentiel

#### Modéré — `INV_NO_CONTEXT_FREE_EVALUATION_HIGH_BLOOM` : portée non bornée sur les tâches diagnostiques

- L'invariant interdit l'évaluation hors contexte authentique pour Bloom ≥ 4.
- Le pipeline de calibrage (`TYPE_REFERENTIEL_KU_CALIBRATION_FORMAT_TABLE`) peut inclure des tâches diagnostiques initiales sur des KU dont le niveau Bloom cible n'est pas encore établi — si le type est Bloom ≥ 4, l'invariant s'applique dès le calibrage initial.
- Mais aucune règle ne précise si cet invariant s'applique aussi aux tâches diagnostiques (calibrage, vérification provisoire) ou seulement aux tâches d'entraînement et d'évaluation.
- **Ancrage** : `INV_NO_CONTEXT_FREE_EVALUATION_HIGH_BLOOM`, `TYPE_REFERENTIEL_KU_CALIBRATION_FORMAT_TABLE`
- **Couche** : Constitution + Référentiel

---

### Axe 2 — Solidité théorique

#### Élevé — Modèle de Valeur-Coût : asymétrie de mise à jour non traitée

- Le modèle VC est correctement fondé sur Eccles & Wigfield.
- Cependant, la Constitution et le Référentiel traitent VC comme un signal de session, sans distinguer la valeur instrumentale (utilité perçue à long terme) de la valeur intrinsèque (intérêt immédiat).
- Les deux composantes peuvent diverger dans les temps : VC intrinsèque basse persistante alors que VC instrumentale reste haute. Le système détecte une VC basse globale et déclenche un patch relevance, alors qu'une réponse pédagogique ciblée sur la motivation intrinsèque serait différente.
- **Ancrage** : `TYPE_STATE_AXIS_VALUE_COST`, `RULE_REFERENTIEL_VC_PERSISTENCE_TRIGGERS_RELEVANCE_PATCH`
- **Couche** : Constitution + Référentiel

#### Modéré — Autonomie (composante A) : absence de distinction "autonomie guidée" vs "autonomie complète"

- `TYPE_MASTERY_COMPONENT_A` est déclarée comme binaire : atteint / non-atteint.
- La littérature SRL distingue autonomie guidée (appui sur ressources externes disponibles) et autonomie complète (sans ressource). Ces deux niveaux produisent des bascules pédagogiques différentes.
- Le système peut passer en mode interleaving ou tâche autonome alors que l'apprenant n'a atteint qu'une autonomie guidée.
- **Ancrage** : `TYPE_MASTERY_COMPONENT_A`, `RULE_REFERENTIEL_INTERLEAVING_ACTIVATION`
- **Couche** : Constitution + Référentiel

#### Modéré — Gamification en période probatoire : effet sur les signaux comportementaux non isolé

- `RULE_REFERENTIEL_UNVALIDATED_GAMIFICATION_PROBATION` place en probatoire une mécanique gamifiée non validée.
- Mais les proxys comportementaux (`TYPE_REFERENTIEL_MINIMAL_BEHAVIORAL_PROXY_SET`) sont mesurés sur les comportements de session. Si une mécanique gamifiée en probatoire modifie les comportements (temps de réponse, taux de complétion, nombre de tentatives), les proxys peuvent être contaminés sans que le moteur le détecte.
- Aucune règle ne prévoit la mise en quarantaine des proxys affectés pendant la période probatoire.
- **Ancrage** : `RULE_REFERENTIEL_UNVALIDATED_GAMIFICATION_PROBATION`, `TYPE_REFERENTIEL_MINIMAL_BEHAVIORAL_PROXY_SET`
- **Couche** : Référentiel

---

### Axe 3 — États indéfinis moteur

#### Élevé — Rétrogradation secondaire + cycle de révision de couverture feedback simultanés

- Scénario : KU_A est rétrogradée → KU_B marquée comme dépendante directe → au même cycle, la `TYPE_REFERENTIEL_FEEDBACK_COVERAGE_METRIC` déclenche un event de sous-couverture sur KU_B.
- L'event de sous-couverture (`EVENT_REFERENTIEL_FEEDBACK_COVERAGE_LOW`) peut déclencher une révision de design sur KU_B au moment même où KU_B est en attente de réentrée diagnostique suite à rétrogradation secondaire.
- Ces deux états concurrents (KU en diagnostic de propagation + KU en révision de couverture) ne sont pas arbitrés.
- **Ancrage** : `RULE_REFERENTIEL_SECONDARY_RETROGRADATION_DEFERRED_REENTRY`, `EVENT_REFERENTIEL_FEEDBACK_COVERAGE_LOW`
- **Couche** : Référentiel

#### Modéré — Profil AR-réfractaire détecté sur un apprenant en investigation systémique

- `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION` déclenche un flag profil-ar-réfractaire sur N sessions sans réponse AR-N1.
- Si l'investigation systémique (`RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`) est en cours, les ajustements sont gelés.
- La détection du profil AR-réfractaire survient mais aucune action n'est possible. Aucune règle ne précise si le flag est mis en attente, ignoré, ou s'il crée une exception à l'investigation systémique.
- **Ancrage** : `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION`, `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`
- **Couche** : Référentiel

---

### Axe 4 — Dépendances IA implicites

#### Modéré — `TYPE_REFERENTIEL_KU_CALIBRATION_FORMAT_TABLE` : sélection du format diagnostique

- La table conditionne le format de calibrage au type de KU.
- Les formats diagnostiques possibles pour une KU créative incluent nécessairement une composante d'appréciation qualitative qui ne peut être réduite à un score déterministe sans intervention sémantique.
- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` l'interdit en mode autonome, mais la phase de calibrage initiale n'est pas exclue de cette contrainte de manière explicite.
- **Ancrage** : `TYPE_REFERENTIEL_KU_CALIBRATION_FORMAT_TABLE`, `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`
- **Couche** : Référentiel + Constitution

---

### Axe 5 — Gouvernance

#### Modéré — `EVENT_REFERENTIEL_PATCH_TRIGGER_THRESHOLD_CROSSED` : absence de fenêtre de déduplication

- `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE` définit des déclencheurs de patch basés sur des franchissements de seuils.
- Si un indicateur oscille autour de son seuil (alternance rapide above/below), plusieurs events de trigger peuvent être émis sur une courte fenêtre, générant plusieurs tentatives de patch sur le même objet.
- Aucune fenêtre de déduplication ni règle de cooldown inter-patch n'est définie.
- **Ancrage** : `EVENT_REFERENTIEL_PATCH_TRIGGER_THRESHOLD_CROSSED`, `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE`
- **Couche** : Référentiel

---

## Risques prioritaires

| Priorité | Risque | Core concerné |
|---|---|---|
| **CRITIQUE** | Divergence MSC calculé / état perçu sans mécanisme de résolution | Constitution + Référentiel |
| **CRITIQUE** | Matrice régimes adaptatifs : cellules de frontière non spécifiées | Référentiel |
| **Élevé** | Interleaving vs rééquilibrage de couverture : séquençage contradictoire possible | Référentiel |
| **Élevé** | Rétrogradation secondaire + event sous-couverture feedback simultanés | Référentiel |
| **Élevé** | Valeur-Coût : asymétrie intrinsèque / instrumentale non traitée | Constitution + Référentiel |
| **Élevé** | `INV_NO_CONTEXT_FREE_EVALUATION_HIGH_BLOOM` non borné aux tâches diagnostiques | Constitution + Référentiel |
| **Modéré** | Composante A binaire : autonomie guidée vs complète non distinguées | Constitution + Référentiel |
| **Modéré** | Gamification en probatoire : proxys comportementaux contaminés non isolés | Référentiel |
| **Modéré** | Profil AR-réfractaire détecté pendant investigation systémique : état bloqué | Référentiel |
| **Modéré** | Event patch trigger sans déduplication / cooldown inter-patch | Référentiel |
| **Modéré** | KU créative : format diagnostique calibrage vs contrainte déterministe | Référentiel + Constitution |

---

## Corrections à arbitrer avant patch

- **Arbitrage B1** : Définir un mécanisme de résolution de la divergence MSC calculé / état perçu (AR-N1 persistant discordant) : event dédié, seuil de persistance avant escalade, ou règle de coexistence explicite. Relève de la Constitution + Référentiel.

- **Arbitrage B2** : Spécifier la règle de priorité entre régimes adaptatifs pour les cellules de frontière de la matrice 3×3 (ex. détresse prime sur sous-défi, ou règle de vote majoritaire). Relève du Référentiel.

- **Arbitrage B3** : Arbitrer la précédence entre `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A` et `RULE_REFERENTIEL_COVERAGE_REBALANCING_ACTIVATION` sur un même cycle. Une règle de résolution explicite (ex. interleaving prime si les conditions A∧P sont remplies) évite l'oscillation.

- **Arbitrage B4** : Préciser si `INV_NO_CONTEXT_FREE_EVALUATION_HIGH_BLOOM` s'applique aux tâches diagnostiques de calibrage (et si oui, comment le calibrage initial est praticable pour une KU Bloom ≥ 4 sans contexte authentique disponible).

- **Arbitrage B5** : Décider si la composante A doit rester binaire ou être subdivisée (guidée / complète) — impact direct sur les règles d'activation de l'interleaving et des tâches autonomes.

- **Arbitrage B6** : Ajouter une fenêtre de déduplication (cooldown inter-patch) sur `EVENT_REFERENTIEL_PATCH_TRIGGER_THRESHOLD_CROSSED` pour prévenir les patch storms sur indicateur oscillant. Relève du Référentiel.

- **Arbitrage B7** : Préciser le comportement du flag profil-ar-réfractaire quand une investigation systémique est en cours : mise en file, suspension, ou exception. Relève du Référentiel.
