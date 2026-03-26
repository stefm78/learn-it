# Core Pipeline Repo Layout

## Canonical layout

- `docs/pipeline.md`
- `docs/registry/`
- `docs/specs/patch-dsl/`
- `docs/prompts/shared/`
- `docs/patcher/shared/`
- `docs/cores/current/`
- `docs/cores/releases/`
- `docs/pipelines/constitution/`
- `docs/pipelines/release/`
- `docs/pipelines/migration/`
- `docs/architecture/`
- `docs/legacy/`

## Intent

Cette structure sépare :
- la gouvernance globale ;
- les ressources partagées ;
- les Core courants ;
- les pipelines spécialisés ;
- l'historique legacy.

## Key rule

Le pipeline ne consomme que les chemins canoniques `current/`, `shared/` et son propre dossier.
Le legacy reste lisible mais non prioritaire.
