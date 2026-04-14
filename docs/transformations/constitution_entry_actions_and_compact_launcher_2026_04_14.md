# Constitution — entry actions + compact launcher binding

Date: 2026-04-14
Branch: `feat/core-modularization-bootstrap`
Scope: `docs/pipelines/constitution/*`

## Intent

Stabiliser la couche d'entrée du pipeline `constitution` sans regonfler le launcher.

Le principe retenu est désormais le suivant:

- les **stages** restent décrits par `docs/pipelines/constitution/stages/*.skill.yaml`
- les **actions d'entrée** sont décrites par `docs/pipelines/constitution/entry_actions/*.action.yaml`
- `run_context.yaml` porte la **task view dérivée** pour les runs actifs
- le launcher ne doit plus spécifier les règles métier d'entrée; il doit seulement:
  - choisir l'action adaptée au contexte
  - charger le contrat canonique correspondant
  - injecter les bindings d'instance
  - produire un prompt compact qui **référence** le contrat canonique

## Changes introduced

### 1. Canonical entry action contracts

Création de la famille:

- `docs/pipelines/constitution/entry_actions/ENTRY_ACTIONS_INDEX.yaml`
- `docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml`
- `docs/pipelines/constitution/entry_actions/CONTINUE_ACTIVE_RUN.action.yaml`
- `docs/pipelines/constitution/entry_actions/DISAMBIGUATE.action.yaml`
- `docs/pipelines/constitution/entry_actions/INSPECT.action.yaml`
- `docs/pipelines/constitution/entry_actions/PARTITION_REFRESH.action.yaml`

Point important:
les fichiers ont été corrigés pour respecter une structure imbriquée compatible avec le launcher:

- `ENTRY_ACTIONS_INDEX.yaml` doit porter `entry_actions` **dans** `entry_actions_index`
- chaque `*.action.yaml` doit porter `mission`, `entry_binding`, `allowed_reads`, etc. **dans** `entry_action`

### 2. Runtime derived view for active runs

`docs/patcher/shared/build_run_context.py` a été promu depuis le candidat validé.

Le `run_context.yaml` enrichi expose notamment:

- `current_stage_canonical`
- `next_executable_stage_canonical`
- `terminal_closed`
- `task_view.status`
- `task_view.raw_stage_id`
- `task_view.stage_id`
- `task_view.skill_ref`
- `task_view.compact_execution_prompt`

Le comportement terminal fermé a été validé sur un run clos de `patch_lifecycle`.

### 3. Compact launcher candidate

Un launcher fusionné compact a été ajouté sous:

- `tmp/pipeline_launcher_fused_compact_candidate.py`

Ce candidat conserve:

- la logique `--parallel-runs`
- la consommation de `run_context.task_view`
- le non-proposition de `continue` quand `task_view.status == terminal_closed`

Mais il modifie la forme des prompts d'entrée:

- avant: le launcher dépliait le contrat inline
- maintenant: le launcher produit un prompt court qui:
  - référence le contrat canonique (`entry_actions/*.action.yaml`)
  - référence l'ancre de protocole (`AI_PROTOCOL.yaml`)
  - injecte seulement les bindings d'instance
  - ordonne explicitement de ne pas étendre le contrat ni sortir de sa surface autorisée

## Current status

Le socle conceptuel est maintenant aligné:

- `stages/` = contrats de stage
- `entry_actions/` = contrats d'entrée
- `run_context` = vue dérivée d'instance
- `pipeline_launcher` = orchestration légère + binding

Le prochain travail n'est plus de redéfinir la fermeture, mais de:

1. valider le launcher compact sur les cas principaux
2. promouvoir le launcher compact si les tests sont concluants
3. étendre le même pattern aux autres pipelines si confirmé

## Suggested tests

### A. Single launcher mode

```bash
python ./tmp/pipeline_launcher_fused_compact_candidate.py --repo-root . --pipeline constitution
```

Vérifier:

- `recommended_action` cohérent avec l'état réel
- `entry_prompt` compact
- référence explicite au contrat canonique `entry_actions/*.action.yaml`
- absence de dépliage complet du contrat dans le prompt

### B. Parallel launcher mode

```bash
python ./tmp/pipeline_launcher_fused_compact_candidate.py --repo-root . --parallel-runs 4
```

Vérifier:

- slots déterministes
- `open_run_prompt` compacts
- conservation de l'ordre des scopes par maturité décroissante

### C. Active run mode (à exécuter après ouverture d'un run)

Précondition:
- ouvrir un run `constitution`
- matérialiser son `run_context.yaml`

Puis tester:

```bash
python ./tmp/pipeline_launcher_fused_compact_candidate.py --repo-root . --pipeline constitution
```

Vérifier:

- `recommended_action = CONTINUE_ACTIVE_RUN` si un unique run actif exécutable existe
- `next_best_actions.continue.stage_prompt` issu de `run_context.task_view.compact_execution_prompt`
- `entry_prompt` de continuation compact et référencé sur `CONTINUE_ACTIVE_RUN.action.yaml`

## Architectural note

Le launcher ne doit pas devenir un deuxième protocole.
La source de vérité doit rester portée par les contrats canoniques (`stages/` et `entry_actions/`).
Le launcher doit rester un sélecteur de contexte et un injecteur de bindings.
