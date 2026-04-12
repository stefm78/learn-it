# Arbitrage — bounded run `learner_state`

## Résumé exécutif

Mode utilisé : `bounded`.

Le challenge du run `learner_state` fait émerger un seul point à corriger immédiatement dans le scope courant : la règle `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` doit être rendue plus déterministe pour éviter des implémentations divergentes du déclenchement d’entrée conservative.

Le second point important, concernant la chaîne d’autorité entre `RULE_AR_N1_OVERRIDES_PROXY` côté Constitution et le reweighting temporaire documenté côté Référentiel/LINK, est confirmé comme pertinent mais non patchable sûrement dans ce run sans élargissement explicite de scope.

La normalisation lexicale entre `unknown`, `absent` et `non-observable` est retenue comme piste utile mais non prioritaire pour le pilote ; elle est reportée pour préserver la minimalité du patch.

Décisions :
- `corriger_maintenant` : 1
- `reporter` : 1
- `rejeter` : 0
- `hors_perimetre` : 0
- `necessite_extension_scope` : 1

## Périmètre analysé

### Fichiers de challenge considérés
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/01_challenge/challenge_report_01.md`

### Notes humaines prises en compte
- aucune

### Scope déclaré
- run_id : `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`
- scope_id : `CONSTITUTION_SCOPE_LEARNER_STATE`
- fichier modifiable autorisé : `docs/cores/current/constitution.yaml`
- modules visés : `learner_state`, `self_report`, `conservative_entry_logic`

### Limites de périmètre
- aucun correctif silencieux hors `docs/cores/current/constitution.yaml` n’est recevable dans ce run ;
- toute correction exigeant une modification coordonnée de `referentiel.yaml` ou `link.yaml` doit être classée `necessite_extension_scope`.

## Arbitrage détaillé

### Point P01 — Clarification du seuil multi-axis unknown / non-observable
- Source(s) : `challenge_report_01.md` — sections « Axe 1 », « Axe 3 », « Axe 7 », correction `C01`
- Constat synthétique : la formule « plusieurs axes critiques » dans `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` reste trop ouverte et peut conduire à des implémentations différentes du déclenchement d’entrée conservative.
- Nature : logique ; complétude ; implémentabilité
- Gravité : modéré
- Impact : applicabilité ; homogénéité d’implémentation ; stabilité du comportement moteur au démarrage et à la reprise
- Statut de périmètre : `in_scope`
- Décision : `corriger_maintenant`
- Justification : le problème est local, bien circonscrit, déjà suffisamment qualifié par le challenge, et peut être corrigé par une formulation plus déterministe sans élargir le scope ni déplacer de logique dans le Référentiel.
- Conséquence attendue pour l’étape patch : produire un patch minimal dans `constitution.yaml` qui remplace la formulation ambiguë par une condition constitutionnelle explicitement lisible, de type « au moins deux des trois axes critiques ». Le patch doit rester strictement local à la règle ciblée.

### Point P02 — Tension AR-N1 / AR-N3 dans la chaîne d’autorité des signaux
- Source(s) : `challenge_report_01.md` — sections « Axe 4 », « Axe 5 », « Axe 7 », correction `C02`
- Constat synthétique : la lecture combinée de `RULE_AR_N1_OVERRIDES_PROXY` avec le reweighting temporaire d’AR-N1 par AR-N3 documenté côté Référentiel/LINK laisse place à deux interprétations d’autorité, ce qui crée une tension inter-Core non résoluble proprement dans le seul scope `learner_state`.
- Nature : gouvernance ; séparation des couches ; cohérence inter-documents
- Gravité : élevé
- Impact : sécurité logique ; cohérence inter-Core ; risque de patch local trompeur ; stabilité documentaire
- Statut de périmètre : `needs_scope_extension`
- Décision : `necessite_extension_scope`
- Justification : un patch constitutionnel isolé serait potentiellement faux-ami. Le point exige un arbitrage explicite sur la place exacte de l’exception référentielle et donc une lecture-action coordonnée Constitution / Référentiel / LINK.
- Conséquence attendue pour l’étape patch : ne rien patcher sur ce point dans le run courant. Le patchset du run doit explicitement exclure ce sujet. Le point doit être tracé comme dépendance d’un futur run élargi ou d’un arbitrage inter-Core dédié.

### Point P03 — Normalisation lexicale des statuts `unknown` / `absent` / `non-observable`
- Source(s) : `challenge_report_01.md` — sections « Axe 1 », « Axe 7 », correction `C03`
- Constat synthétique : une légère hétérogénéité lexicale subsiste entre plusieurs statuts d’absence d’observation, sans effet critique immédiat tant que le traitement moteur reste conservatif.
- Nature : éditoriale ; précision conceptuelle
- Gravité : faible
- Impact : compréhension ; maintenabilité ; lisibilité doctrinale
- Statut de périmètre : `in_scope`
- Décision : `reporter`
- Justification : le bénéfice documentaire existe, mais le pilote borné gagne à préserver un patch minimal centré sur le point P01. Ajouter cette normalisation au même patch augmenterait la surface de changement sans nécessité immédiate.
- Conséquence attendue pour l’étape patch : ne pas inclure ce point dans le patchset du run courant. Le consigner comme amélioration rédactionnelle ultérieure, à traiter séparément si besoin.

## Points consolidés

- Les constats sur l’ambiguïté de `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` issus des axes « cohérence interne », « états indéfinis moteur » et « scénarios adversariaux » sont consolidés en un seul point P01.
- Les constats sur la chaîne AR-N1 / AR-N3 issus des axes « dépendances IA implicites », « gouvernance » et « scénarios adversariaux » sont consolidés en un seul point P02.
- Aucun doublon contradictoire n’a été détecté dans le challenge considéré.
- Aucune divergence inter-rapport n’est à arbitrer, car un seul `challenge_report*.md` est présent dans le répertoire résolu du run.

## Décisions à transmettre au patch

### À traduire en patch
1. **Priorité P1** — Corriger `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY`
   - contrainte : patch minimal ;
   - contrainte : modification strictement locale à `constitution.yaml` ;
   - contrainte : ne pas introduire de seuil caché dépendant du Référentiel ;
   - objectif : rendre la condition de déclenchement explicitement déterministe.

### À exclure explicitement du patch courant
2. **Priorité hors patch courant** — sujet AR-N1 / AR-N3
   - ne pas corriger localement ;
   - tracer comme `necessite_extension_scope`.

3. **Priorité différée** — normalisation lexicale des statuts d’observation
   - ne pas intégrer dans le patch courant ;
   - conserver comme amélioration documentaire reportée.

## Décisions explicitement non retenues

### Reportés
- P03 — normalisation lexicale `unknown` / `absent` / `non-observable`
  - justification : utile mais non prioritaire ; préserver la minimalité du patch du pilote.

### Nécessitant extension de scope
- P02 — clarification de la chaîne d’autorité AR-N1 / AR-N3
  - justification : dépend d’un arbitrage coordonné Constitution / Référentiel / LINK ; non patchable sûrement dans le run courant.

### Rejetés
- aucun

### Hors périmètre
- aucun point autonome supplémentaire, les éléments hors patch du challenge étant soit consolidés dans P02, soit déjà couverts par le report P03.
