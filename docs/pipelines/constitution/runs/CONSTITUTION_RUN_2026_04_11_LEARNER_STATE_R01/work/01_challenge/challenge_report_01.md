# Challenge report — bounded run `learner_state`

## Résumé exécutif

Mode utilisé : `bounded`.

Le sous-ensemble `learner_state` est globalement cohérent et suffisamment fermé pour un pilote borné utile. Le principal point exploitable immédiatement dans le scope est une ambiguïté constitutionnelle locale sur la règle `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` : l’expression « plusieurs axes critiques » reste interprétable et peut produire des implémentations divergentes. 

Le principal point de risque plus élevé ne relève pas d’un patch constitutionnel isolé sûr dans ce run : la chaîne d’autorité entre `RULE_AR_N1_OVERRIDES_PROXY` côté Constitution et le reweighting temporaire d’AR-N1 par AR-N3 côté Référentiel, documenté par le LINK, crée une tension inter-Core qui doit être arbitrée explicitement avant toute correction plus large.

## Périmètre de challenge

### Artefacts lus
- `docs/pipelines/constitution/pipeline.md`
- `docs/prompts/shared/Challenge_constitution.md`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/run_manifest.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/integration_gate.yaml`
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/transformations/core_modularization/PILOT_01_CONSTITUTION_LEARNER_STATE.md`

### Scope déclaré
Fichier modifiable autorisé :
- `docs/cores/current/constitution.yaml`

Modules et ids visés :
- `learner_state`
- `self_report`
- `conservative_entry_logic`
- `TYPE_LEARNER_STATE_MODEL`
- `TYPE_STATE_AXIS_CALIBRATION`
- `TYPE_STATE_AXIS_ACTIVATION`
- `TYPE_STATE_AXIS_VALUE_COST`
- `TYPE_SELF_REPORT_AR_N1`
- `TYPE_SELF_REPORT_AR_N2`
- `TYPE_SELF_REPORT_AR_N3`
- `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`
- `INV_VC_NOT_GENERAL_MOTIVATION_PROXY`
- `RULE_AR_N1_OVERRIDES_PROXY`
- `RULE_SESSION_INTENTION_NON_BLOCKING`
- `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`
- `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
- `EVENT_ACTIVATION_DISTRESS_PERSISTENCE_ESCALATION`
- `RULE_ACTIVATION_DISTRESS_PERSISTENCE_ESCALATION_OFFSESSION`

### Limites
- Aucun correctif silencieux hors `constitution.yaml` n’est recevable dans ce run.
- Toute correction exigeant un ajustement coordonné avec `referentiel.yaml` ou `link.yaml` doit être classée `needs_scope_extension` ou `out_of_scope_but_relevant`.

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### Point solide
Le triplet `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` + `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` + `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` donne une architecture prudente cohérente : absence d’observabilité n’est pas transformée en valeur forcée, et le moteur adopte une entrée sûre plutôt qu’une complétion cachée.

#### Zone de risque
`RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` reste sémantiquement ouverte sur la quantité minimale d’axes concernés. « Plusieurs axes critiques » est compréhensible humainement mais insuffisamment déterministe pour une implémentation homogène. Deux implémenteurs peuvent en déduire respectivement « au moins deux axes » ou « quasi-absence globale d’observabilité ». 

- Élément concerné : `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
- Nature du problème : complétude / implémentabilité
- Type de problème : gouvernance locale de règle
- Impact moteur : entrée conservative non déclenchée au même moment selon les implémentations
- Statut de périmètre : `in_scope`
- Correction à arbitrer : expliciter le seuil constitutionnel minimal, sans déplacer ce seuil dans le Référentiel si l’intention est structurelle.

#### Angle mort
La frontière « unknown » / « non-observable » / « absent » est bien protégée, mais la Constitution ne formalise pas davantage la hiérarchie entre ces trois statuts. Cela n’est pas bloquant ici, car les règles de sûreté traitent déjà ces états comme non-inférables.

- Élément concerné : `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`
- Nature du problème : éditorial / précision conceptuelle
- Type de problème : faible
- Impact moteur : limité tant que les trois statuts restent traités conservativement
- Statut de périmètre : `reporter`
- Correction à arbitrer : possible normalisation lexicale ultérieure, sans urgence.

### Axe 2 — Solidité théorique

#### Charge cognitive et entrée sûre
Point solide : la combinaison unknown + scaffolding léger réversible protège contre une sur-réaction système en contexte d’observabilité faible. Cela reste compatible avec une lecture prudente de la charge cognitive.

Zone de risque : si le déclenchement de l’entrée conservative varie selon l’implémentation, la protection cognitive devient inégale d’un moteur à l’autre.

Angle mort : la Constitution ne dit pas si l’axe calibration doit peser autant que activation et value_cost dans le passage à l’entrée sûre. Le point mérite un cadrage minimal mais pas forcément une sophistication supérieure à ce stade.

#### Motivation / engagement
Point solide : `INV_VC_NOT_GENERAL_MOTIVATION_PROXY` et `RULE_SESSION_INTENTION_NON_BLOCKING` évitent des dérives classiques où le système sur-interprète la motivation ou punit l’absence de projection.

Zone de risque : aucune faille locale critique détectée dans le scope.

Angle mort : l’effet combiné faible VC + unknown généralisé reste surtout cadré par le Référentiel et le LINK, donc non corrigeable localement dans ce run.

#### Métacognition / SRL
Point solide : `RULE_SESSION_INTENTION_NON_BLOCKING` maintient une collecte informative sans effet punitif, ce qui est cohérent avec une aide au forethought SRL non coercitive.

Zone de risque : faible.

Angle mort : pas de point prioritaire à patcher dans le scope actuel.

#### Émotions / engagement
Point solide : la priorité structurelle donnée à la détresse, couplée à l’escalade hors session, est conforme à une gouvernance prudente des états d’activation.

Zone de risque : la confirmation de la détresse dépend d’une chaîne plus large de signaux et de seuils référentiels. Ce n’est pas un défaut constitutionnel local, mais une dépendance inter-Core à surveiller.

### Axe 3 — États indéfinis moteur

#### Point retenu
Le cas « deux axes unknown, un axe observable » n’est pas indéfini sur le fond, mais il l’est partiellement sur le seuil de déclenchement de l’entrée conservative.

- Élément concerné : `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
- Nature du problème : implémentabilité
- Type de problème : modéré
- Impact moteur : variations de comportement au démarrage, à la reprise ou lors de mises à jour incomplètes de l’état
- Statut de périmètre : `in_scope`
- Correction à arbitrer : expliciter « au moins deux des trois axes critiques ».

### Axe 4 — Dépendances IA implicites

#### Point solide
Le scope `learner_state` évite largement les dépendances à une IA continue : les statuts unknown, non-observable, conservateur et escalade sont définis de manière compatible avec un moteur local.

#### Zone de risque majeure
La chaîne AR-N1 / AR-N3 / proxys présente une tension documentaire :
- Constitution : `RULE_AR_N1_OVERRIDES_PROXY`
- Référentiel : `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`
- LINK : `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` et `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING`

Le fond n’est pas forcément contradictoire, mais la formulation reste suffisamment tendue pour produire deux lectures :
1. AR-N1 prime toujours strictement ;
2. AR-N1 prime par défaut mais peut être temporairement repondéré par une exception référentielle explicitement gouvernée.

Cette tension n’exige pas une IA continue, mais elle exige une clarification inter-Core pour éviter un glissement silencieux d’autorité.

- Élément concerné : `RULE_AR_N1_OVERRIDES_PROXY` + règles référentielles et bindings associés
- Nature du problème : séparation des couches / cohérence inter-documents
- Type de problème : gouvernance
- Impact moteur : conflit d’interprétation possible sur la chaîne d’autorité des signaux
- Statut de périmètre : `needs_scope_extension`
- Correction à arbitrer : arbitrage explicite sur le statut de l’exception AR-N3 avant tout patch coordonné Constitution/Référentiel/LINK.

### Axe 5 — Gouvernance

#### Point solide
La séparation Constitution/Référentiel/LINK est globalement respectée sur ce scope. Les seuils restent référentiels et la Constitution garde les invariants de sûreté.

#### Zone de risque
Le run borné autorise bien la lecture de voisinage logique, mais la tension AR-N1/AR-N3 montre qu’un patch uniquement constitutionnel pourrait être incomplet ou trompeur si l’on cherchait à résoudre ce point sans toucher les artefacts voisins.

- Élément concerné : chaîne d’autorité des signaux
- Nature du problème : cohérence inter-documents
- Type de problème : élevé
- Impact moteur : patch local potentiellement faux-ami
- Statut de périmètre : `needs_scope_extension`
- Correction à arbitrer : ne pas corriger localement ce point dans ce run sans décision d’extension.

### Axe 6 — Scénarios adversariaux

#### Scénario 1 — Reprise avec observabilité lacunaire
Un apprenant reprend après interruption. Activation et VC sont non observables, calibration est partielle. Selon l’interprétation du mot « plusieurs », le moteur peut soit appliquer l’entrée conservative, soit tenter une reprise plus affirmée.

- Mécanismes activés : `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`, `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
- Limite révélée : seuil constitutionnel insuffisamment explicite
- Statut : `in_scope`

#### Scénario 2 — AR-N1 disponible mais calibration AR historiquement basse
Un AR-N1 récent indique un état, mais plusieurs bilans AR-N3 ont établi une calibration basse. Un moteur lit la Constitution au pied de la lettre et fait primer AR-N1 strictement ; un autre applique le reweighting référentiel.

- Mécanismes activés : `RULE_AR_N1_OVERRIDES_PROXY`, `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`, bindings LINK
- Limite révélée : tension inter-Core sur la chaîne d’autorité
- Statut : `needs_scope_extension`

#### Scénario 3 — Détresse non confirmable faute de signal exploitable
AR-N1 manque, les proxys sont insuffisants, plusieurs axes restent unknown, mais le contexte laisse soupçonner une détresse. Le système reste prudemment conservateur puis escalade hors session si la persistance est atteinte.

- Mécanismes activés : `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`, `EVENT_ACTIVATION_DISTRESS_PERSISTENCE_ESCALATION`, `RULE_ACTIVATION_DISTRESS_PERSISTENCE_ESCALATION_OFFSESSION`
- Limite révélée : dépendance forte à la bonne articulation Référentiel/LINK pour la supervision de persistance
- Statut : `out_of_scope_but_relevant`

### Axe 7 — Priorisation

#### Critique
Aucun point critique détecté dans le scope strict du run.

#### Élevé
- Tension documentaire entre `RULE_AR_N1_OVERRIDES_PROXY` et le reweighting temporaire AR-N3 documenté côté Référentiel/LINK.
  - Statut : `needs_scope_extension`

#### Modéré
- Ambiguïté sur le seuil de déclenchement de `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`.
  - Statut : `in_scope`

#### Faible
- Normalisation lexicale possible entre `unknown`, `absent`, `non-observable`.
  - Statut : `reporter`

## Risques prioritaires

1. **À corriger maintenant dans le scope**
   - Clarifier `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` en remplaçant « plusieurs axes critiques » par une condition constitutionnelle minimale explicitement lisible.

2. **À ne pas corriger localement sans extension**
   - Clarifier la place exacte du reweighting AR-N3 vis-à-vis de `RULE_AR_N1_OVERRIDES_PROXY`.

## Corrections à arbitrer avant patch

### C01 — Clarification du seuil multi-axis unknown
- Élément concerné : `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
- Nature du problème : implémentabilité / complétude
- Type de problème : modéré
- Impact moteur : divergence de déclenchement de l’entrée sûre
- Statut de périmètre : `in_scope`
- Correction à arbitrer : expliciter que le déclenchement vaut lorsque **au moins deux des trois axes critiques** (`calibration`, `activation`, `value_cost`) sont simultanément `unknown`, absents ou non-observables.

### C02 — Clarification de la chaîne d’autorité AR-N1 / AR-N3
- Élément concerné : `RULE_AR_N1_OVERRIDES_PROXY` et voisins logiques inter-Core
- Nature du problème : séparation des couches / cohérence inter-Core
- Type de problème : élevé
- Impact moteur : conflit d’interprétation sur l’autorité signal
- Statut de périmètre : `needs_scope_extension`
- Correction à arbitrer : arbitrage inter-Core explicite avant tout patch coordonné.

### C03 — Normalisation lexicale des statuts d’absence d’observation
- Élément concerné : `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`
- Nature du problème : éditorial
- Type de problème : faible
- Impact moteur : faible, principalement documentaire
- Statut de périmètre : `in_scope`
- Correction à arbitrer : possible report pour ne pas élargir inutilement le patch du pilote.
