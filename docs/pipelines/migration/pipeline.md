# PIPELINE — migration

id: migration
version: 1
scope: structural-migration

## Goal

Servir de pipeline réservé aux migrations structurelles de Core, prompts, specs ou patchers.

## Current status

Skeleton only. This pipeline is intentionally minimal until a concrete migration use case is formalized.

## Inputs
- `docs/pipelines/migration/inputs/`

## Outputs
- `docs/pipelines/migration/outputs/`
- `docs/pipelines/migration/reports/`

## Rule
Aucune migration ne doit être opérée directement sur `current/` sans patch validé.
