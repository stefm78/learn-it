# Constitution runs

## Rôle

Ce répertoire porte les **instances de run** du pipeline `constitution`.

Chaque run dispose de :
- son `run_id` ;
- son `scope_id` ;
- ses inputs matérialisés ;
- son `work/` propre ;
- ses `reports/` ;
- ses `outputs/`.

## Pourquoi

Le layout plat historique (`inputs/`, `work/01_challenge/`, etc.) convient à un seul run actif à la fois.

Le layout `runs/<run_id>/...` permet :
- plusieurs runs parallèles ;
- plusieurs scopes parallèles ;
- plusieurs runs sur un même scope ;
- une meilleure traçabilité.

## Structure cible d'un run

```text
<run_id>/
  run_manifest.yaml
  inputs/
    scope_manifest.yaml
    impact_bundle.yaml
    integration_gate.yaml
  work/
    01_challenge/
    02_arbitrage/
    03_patch/
    04_patch_validation/
    05_apply/
    06_core_validation/
    07_release/
  reports/
  outputs/
  archive/
```

## Règle

Les trois fichiers :
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`

sont des artefacts de run, pas des fichiers globaux permanents du pipeline.
