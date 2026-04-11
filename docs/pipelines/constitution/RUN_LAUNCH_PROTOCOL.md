# Constitution — run launch protocol

## Objet

Ce document définit comment une demande courte adressée à une IA doit être résolue en exécution de pipeline fiable pour `constitution`.

Exemples de demandes humaines visées :
- `Exécute le pipeline constitution stage 01 sur le scope CONSTITUTION_SCOPE_LEARNER_STATE`
- `Lance le challenge constitution sur learner_state`
- `Reprends le run CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 au stage 02`

Le but est de permettre une formulation concise **sans laisser l'IA deviner silencieusement** la gouvernance, le scope ou le run.

---

## Principe

Une demande courte ne doit pas être exécutée directement comme une simple instruction libre.
Elle doit être résolue selon un protocole déterministe.

Le protocole transforme une demande humaine en :
- un `pipeline_id` ;
- un `stage_id` ;
- un `scope_id` ou un `run_id` ;
- une décision `create` ou `resume` ;
- un chemin d'exécution résolu.

---

## Formes de requête acceptées

### A. Requête par `run_id`
Exemple :
- `Exécute constitution STAGE_02_ARBITRAGE run_id=CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`

Usage :
- reprise d'un run déjà existant.

### B. Requête par `scope_id`
Exemple :
- `Exécute constitution STAGE_01_CHALLENGE scope_id=CONSTITUTION_SCOPE_LEARNER_STATE`

Usage :
- créer un nouveau run ou reprendre un run ouvert, selon la politique de résolution.

### C. Requête par `scope_key`
Exemple :
- `Lance le challenge constitution sur learner_state`

Usage :
- forme courte conviviale.
- nécessite résolution vers un `scope_id` canonique.

### D. Requête libre par description sémantique
Exemple :
- `Lance le challenge constitution sur le scope état apprenant et auto-reports`

Usage :
- toléré comme confort utilisateur ;
- ne doit pas devenir l'identifiant canonique ;
- exige un matching explicite vers un scope publié.

---

## Politique de résolution

### Étape 1 — résoudre le pipeline
- `constitution` doit pointer vers `docs/pipelines/constitution/pipeline.md`

### Étape 2 — résoudre le stage
Valeurs attendues :
- `STAGE_01_CHALLENGE`
- `STAGE_02_ARBITRAGE`
- `STAGE_03_PATCH_SYNTHESIS`
- `STAGE_04_PATCH_VALIDATION`
- `STAGE_05_APPLY`
- `STAGE_06_CORE_VALIDATION`
- `STAGE_07_RELEASE_MATERIALIZATION`
- `STAGE_08_PROMOTE_CURRENT`
- `STAGE_09_CLOSEOUT_AND_ARCHIVE`

### Étape 3 — résoudre la cible
#### Cas 1 — `run_id` fourni
- utiliser directement le run s'il existe.

#### Cas 2 — `scope_id` fourni
- vérifier que le scope existe dans le catalogue ;
- appliquer la politique `create_or_resume`.

#### Cas 3 — `scope_key` fourni
- résoudre vers un `scope_id` unique dans le catalogue ;
- si ambigu, ne pas exécuter silencieusement.

#### Cas 4 — description libre
- tenter une résolution sémantique vers un scope publié ;
- si le matching n'est pas suffisamment fiable, demander clarification ou produire un diagnostic de non-résolution.

---

## Politique `create_or_resume`

Règle bootstrap recommandée pour `constitution` :

### Par défaut
- si un run ouvert existe déjà pour le `scope_id` visé, le reprendre ;
- sinon, créer un nouveau run.

### Cas de création forcée
- si l'utilisateur demande explicitement un nouveau run ;
- si le run existant est déjà clôturé ;
- si le run existant est dans un état incompatible avec le stage demandé.

### Cas de reprise forcée
- si `run_id` est explicitement fourni.

---

## Politique de nommage des runs

Format recommandé :
- `CONSTITUTION_RUN_YYYY_MM_DD_<scope_key>_R##`

Exemple :
- `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`

Le compteur `R##` doit permettre plusieurs runs successifs sur le même scope.

---

## Résultat attendu d'une résolution

Une requête correctement résolue doit produire au minimum :
- `pipeline_id`
- `stage_id`
- `scope_id` ou `run_id`
- `resolution_mode` : `resolved_by_run_id` | `resolved_by_scope_id` | `resolved_by_scope_key` | `resolved_by_semantic_match`
- `action` : `resume_existing_run` | `create_new_run`
- `resolved_paths_root`

---

## Règle de sûreté

Aucune IA ne doit :
- inventer un scope non publié sans le signaler ;
- reprendre silencieusement un mauvais run ;
- créer silencieusement plusieurs runs incohérents pour le même scope ;
- traiter une description libre comme identifiant canonique sans résolution explicite.

---

## Décision de design

Pour `constitution`, une demande courte du type :
- `Exécute stage 01 sur learner_state`

est considérée comme **une requête de lancement à résoudre**, pas comme une autorisation de comportement implicite libre.
