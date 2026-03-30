# STAGE 07–08 — commandes d’exécution

Ce document fournit les commandes de référence scriptées pour :
- `07A_RELEASE_CLASSIFICATION` / validation du `release_plan.yaml`
- `07B_RELEASE_MATERIALIZATION`
- `STAGE_08_PROMOTE_CURRENT`

## Pré-requis

- les Core patchés validés existent sous :
  - `docs/pipelines/constitution/work/05_apply/patched/`
- la validation Stage 06 est en `PASS`
- un `release_plan.yaml` a été produit sous :
  - `docs/pipelines/constitution/work/07_release/release_plan.yaml`

## Validation du release plan

```bash
python docs/patcher/shared/validate_release_plan.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/specs/core-release/release_plan.schema.yaml
```

## Matérialisation de la release

```bash
python docs/patcher/shared/materialize_release.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/work/05_apply/patched \
  ./docs/pipelines/constitution/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/outputs/release_candidate_notes.md
```

Effets attendus :
- création de la release immuable sous `docs/cores/releases/<release_id>/`
- écriture de `manifest.yaml`
- écriture de `release_materialization_report.yaml`
- écriture de `release_candidate_notes.md`

## Promotion vers current

```bash
python docs/patcher/shared/promote_current.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/reports/promotion_report.yaml
```

Effets attendus :
- copie de la release promue dans `docs/cores/current/`
- écriture de `docs/cores/current/manifest.yaml`
- écriture de `promotion_report.yaml`
- comportement idempotent si la release est déjà active

## Séquence recommandée

```bash
python docs/patcher/shared/validate_release_plan.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/specs/core-release/release_plan.schema.yaml

python docs/patcher/shared/materialize_release.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/work/05_apply/patched \
  ./docs/pipelines/constitution/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/outputs/release_candidate_notes.md

python docs/patcher/shared/promote_current.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/reports/promotion_report.yaml
```
