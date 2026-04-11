# Constitution — run startup protocol

## Objet

Ce document définit le **premier réflexe** attendu d'une IA sans contexte lorsqu'on lui demande de lancer, reprendre ou continuer un travail sur le pipeline `constitution`.

But :
- réduire au minimum le contexte à charger ;
- éviter les démarrages ambigus ;
- permettre des prompts de lancement courts mais déterministes ;
- produire une `next best action` explicite si la résolution n'est pas triviale.

---

## Principe général

Une IA sans contexte ne doit pas commencer directement à exécuter un stage.

Son premier réflexe doit être :
1. découvrir les runs existants ;
2. déterminer si la demande correspond clairement à un run existant, à un scope publié, ou à une demande ambiguë ;
3. choisir entre :
   - `resume_existing_run`
   - `create_new_run`
   - `request_disambiguation`
   - `suggest_next_best_action`

---

## Lecture minimale obligatoire

Pour garder le coût de contexte bas, l'IA ne doit lire en premier lieu que :

1. `docs/pipelines/constitution/pipeline.md`
2. `docs/pipelines/constitution/RUN_LAUNCH_PROTOCOL.md`
3. `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
4. `docs/pipelines/constitution/scope_catalog/manifest.yaml`
5. `docs/pipelines/constitution/runs/index.yaml`

Ces 5 artefacts doivent suffire à décider s'il faut créer, reprendre, ou demander une clarification.

---

## Définitions utiles

### `scope_id`
Identifiant canonique stable d'un scope publié.
Exemple : `CONSTITUTION_SCOPE_LEARNER_STATE`

### `scope_key`
Clé courte, lisible, pratique pour les prompts humains.
Exemple : `learner_state`

Règle :
- un `scope_key` n'est pas l'identifiant canonique ;
- il doit résoudre vers un `scope_id` unique dans le catalogue.

### `run_id`
Identifiant canonique d'une instance de run.
Exemple : `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`

---

## Algorithme de démarrage

### Cas A — le prompt contient un `run_id`
1. vérifier l'existence du run dans `runs/index.yaml` ;
2. si le run existe et est compatible avec le stage demandé : `resume_existing_run` ;
3. sinon : `request_disambiguation` ou `suggest_next_best_action`.

### Cas B — le prompt contient un `scope_id`
1. vérifier que le scope existe dans `scope_catalog/manifest.yaml` ;
2. regarder dans `runs/index.yaml` s'il existe un run ouvert pour ce scope ;
3. si un seul run ouvert compatible existe : `resume_existing_run` ;
4. si aucun run ouvert n'existe : `create_new_run` ;
5. si plusieurs runs compatibles existent : `request_disambiguation` avec shortlist.

### Cas C — le prompt contient un `scope_key`
1. résoudre `scope_key -> scope_id` via le catalogue ;
2. appliquer ensuite le cas B.

### Cas D — le prompt contient seulement une description libre
1. tenter un matching sémantique vers un scope publié ;
2. si le matching est univoque et fort : continuer comme cas C ;
3. sinon : `suggest_next_best_action`.

---

## Politique d'ambiguïté

Quand il y a ambiguïté, l'IA ne doit pas demander une question large ou vague.

Elle doit produire une **next best action** courte et orientée décision, par exemple :
- `Deux runs ouverts existent pour learner_state : ... Choisis R01 pour reprendre ou demande un nouveau run.`
- `Aucun scope publié ne correspond de façon fiable à "état motivationnel". Meilleure action : choisir parmi learner_state / mastery_model.`
- `Le stage 03 a été demandé sans run ni scope résolu. Meilleure action : fournir run_id ou scope_id.`

---

## Règles de sortie du startup

Le startup doit produire un diagnostic très léger, avec :
- `resolution_status`: `resolved` | `ambiguous` | `insufficient_input`
- `resolved_pipeline_id`
- `resolved_stage_id`
- `resolved_scope_id` si disponible
- `resolved_run_id` si disponible
- `action`: `resume_existing_run` | `create_new_run` | `request_disambiguation` | `suggest_next_best_action`
- `next_best_action`

---

## Pourquoi cela réduit le contexte

Parce que l'IA n'a pas besoin de relire immédiatement :
- les Core complets ;
- les prompts détaillés ;
- les workdirs de plusieurs runs ;
- les historiques entiers de challenge.

Elle peut d'abord résoudre le point de départ sur la base de :
- catalogue de scopes ;
- index des runs ;
- protocole de lancement.

Le chargement profond ne commence qu'après levée du doute.

---

## Décision de design

Pour `constitution`, la règle retenue est :

**avant d'exécuter un stage, une IA sans contexte doit d'abord résoudre le bon point d'entrée à partir du catalogue de scopes et d'un index léger des runs, puis seulement charger le contexte profond du run retenu.**
