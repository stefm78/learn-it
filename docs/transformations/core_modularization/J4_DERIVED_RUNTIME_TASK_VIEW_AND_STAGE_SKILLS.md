# J4 — Derived runtime task view and stage skills

## Intention

Faire évoluer le régime d'exécution des pipelines depuis un couple
`pipeline.md` + `AI_PROTOCOL.yaml` vers un modèle plus léger pour les IA de
stage :

- règles stables portées par des **skills de stage** génériques au niveau du pipeline ;
- état canonique du run toujours porté par `run_manifest.yaml` + `runs/index.yaml` ;
- vue runtime exécutable dérivée portée par `run_context.yaml` ;
- orchestration globale gardée par un launcher externe.

La cible n'est **pas** d'ajouter des `*.task.yaml` persistés par étape dans
chaque run. La cible recommandée est une **task view dérivée** dans
`run_context.yaml`, reconstruite automatiquement à partir de l'état canonique
et des skills de stage.

## Décision de design

### 1. Pas de duplication massive de capsules de tâche

Les règles de stage ne doivent pas être dupliquées dans chaque run.

On distingue :
- **skill générique de stage** : contrat stable, versionné, réutilisable ;
- **task view dérivée** : contexte minimum vital résolu pour le run courant.

### 2. `update_run_tracking.py` reste sobre

`docs/patcher/shared/update_run_tracking.py` reste responsable de :
- mise à jour de `run_manifest.yaml` ;
- mise à jour de `runs/index.yaml` ;
- écriture d'un record de stage ;
- déclenchement du rebuild de `run_context.yaml`.

Il ne doit pas devenir un moteur de résolution métier des stages.

### 3. `build_run_context.py` devient le constructeur du runtime exécutable

`docs/patcher/shared/build_run_context.py` doit évoluer pour produire une vue
runtime suffisante pour exécuter la tâche courante sans relire de longs
fichiers centraux.

Cette vue devra inclure au minimum :
- `next_executable_stage` ;
- `skill_ref` ;
- `resolved_inputs` ;
- `execution_paths` ;
- `required_scripts` et leur statut ;
- `forbidden_actions` ;
- `completion_evidence` ;
- `allowed_transitions`.

### 4. L'orchestration reste externe

Le launcher choisit :
- quel pipeline est actionnable ;
- quel run est actionnable ;
- si l'action est `continue`, `open_new_run`, `consolidate`, `promote`, etc.

Le launcher ne doit pas re-spécifier toute la logique interne de stage si
`run_context.yaml` expose déjà la task view dérivée.

## Livrables cibles

### A. Modèle pipeline minimal

Nouveau fichier cible :
- `docs/pipelines/constitution/PIPELINE_MODEL.yaml`

But : décrire la machine à états minimale du pipeline :
- stages ;
- transitions autorisées ;
- stages optionnels ;
- stages nécessitant des scripts déterministes ;
- points d'orchestration externes.

### B. Skills de stage

Nouveau répertoire cible :
- `docs/pipelines/constitution/stages/`

Nouveaux fichiers cibles :
- `STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.skill.yaml`
- `STAGE_01_CHALLENGE.skill.yaml`
- ...
- `STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml`

### C. Run context enrichi

Évolution cible :
- `docs/pipelines/constitution/runs/<run_id>/inputs/run_context.yaml`

Le `run_context` ne sera plus seulement un résumé d'état, mais la vue runtime
résolue d'une tâche exécutable.

## Ordre recommandé d'implémentation

1. Poser `PIPELINE_MODEL.yaml` pour `constitution`.
2. Poser un premier skill pilote : `STAGE_01_CHALLENGE.skill.yaml`.
3. Faire évoluer `build_run_context.py` pour référencer ce skill et produire une
   première task view dérivée.
4. Adapter le launcher pour consommer en priorité cette task view.
5. Réduire ensuite le rôle de `pipeline.md` et `AI_PROTOCOL.yaml` sans rupture.
6. Une fois `constitution` stabilisé, factoriser le mécanisme vers les autres pipelines.

## Guardrails

- `run_context.yaml` reste une **vue dérivée**, jamais la source canonique.
- Les skills de stage ne doivent pas embarquer l'état du run.
- Aucun script déterministe obligatoire ne peut être simulé par l'IA.
- Le passage aux autres pipelines ne commence qu'après validation end-to-end sur `constitution`.
