# PIPELINE REGISTRY — Learn-it

## Available pipelines

### constitution
- Path: `docs/pipelines/constitution/pipeline.md`
- Goal: challenger les Core, synthétiser un patch, valider et préparer la promotion
- Canonical state: `docs/pipelines/constitution/state.yaml`

### release
- Path: `docs/pipelines/release/pipeline.md`
- Goal: synchroniser versions internes, références inter-Core et notes de release
- Canonical state: `docs/pipelines/release/state.yaml`

### migration
- Path: `docs/pipelines/migration/pipeline.md`
- Goal: migrations structurelles ou de format sur les Core, prompts ou patchers
- Canonical state: `docs/pipelines/migration/state.yaml`

## Global rules

- Un pipeline ne lit jamais directement un fichier dans `archive/`
- Un pipeline consomme uniquement :
  - `docs/registry/`
  - `docs/specs/patch-dsl/current.md`
  - `docs/prompts/shared/`
  - `docs/patcher/shared/`
  - `docs/cores/current/`
  - son propre dossier `docs/pipelines/<id>/`
- Les artefacts temporaires doivent rester dans le pipeline qui les a produits
- Toute promotion vers `current/` ou `releases/` exige validation explicite

### governance
- Path: `docs/pipelines/governance/pipeline.md`
- Goal: maintenir la cohérence opératoire du repo, des registres, des pipelines, des chemins canoniques et de la séparation operating / release / legacy
- Canonical state: `docs/pipelines/governance/state.yaml`
