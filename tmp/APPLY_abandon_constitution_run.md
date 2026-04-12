# Apply — abandon constitution run

Depuis la racine du repo, ce script ferme explicitement un run `constitution`, écrit une trace d'abandon, puis déplace le dossier du run vers `docs/pipelines/constitution/archive/runs/`.

## Exemple

```bash
python ./tmp/abandon_constitution_run.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --summary "Run abandoned by operator decision before completion."
```

## Effets attendus

- le run disparaît de `docs/pipelines/constitution/runs/index.yaml > active_runs`
- le run est ajouté à `closed_runs` avec :
  - `closure_mode: abandoned`
  - `archived_run_manifest_ref: ...`
- le manifeste du run passe en `status: closed`
- un record `stage_completion_RUN_ABANDONED.yaml` est écrit dans les reports du run
- le dossier complet du run est déplacé sous :
  - `docs/pipelines/constitution/archive/runs/<run_id>/`

## Point de vigilance

Le script archive le run.
Il ne le supprime pas définitivement.
C'est volontaire pour préserver la traçabilité et éviter les références mortes dans le suivi.
