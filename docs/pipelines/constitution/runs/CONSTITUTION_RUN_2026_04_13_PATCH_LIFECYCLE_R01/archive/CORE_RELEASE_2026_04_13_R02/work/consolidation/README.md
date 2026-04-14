# docs/pipelines/constitution/work/consolidation/

Zone de travail de consolidation des résultats de runs parallèles sur scopes disjoints.

## Rôle

Ce répertoire reçoit les Core files consolidés produits par `consolidate_parallel_runs.py`
après exécution de N runs parallèles sur des scopes disjoints.

C'est un artefact de pipeline — pas un artefact Core canonique.
Il suit la même logique que `work/05_apply/sandbox/` : zone de travail intermédiaire,
jamais promue directement, toujours soumise à validation avant release.

## Contenu attendu après consolidation

- `constitution.yaml` — Core Constitution consolidé
- `referentiel.yaml` — Core Référentiel consolidé
- `link.yaml` — Core LINK consolidé
- `consolidation_report.yaml` — rapport (runs participants, IDs merged, statut)

## Règles

- Ce répertoire est transitoire : écrasé à chaque nouvelle consolidation
- Il ne remplace jamais `docs/cores/current/` directement
- La promotion vers `current/` reste un acte explicite via STAGE_08_PROMOTE_CURRENT
- STAGE_07 lit ce répertoire si `consolidation_report.yaml` est présent et `status: PASS`
- Si un seul run est actif, ce répertoire n'est pas utilisé (STAGE_07 lit le sandbox du run)

## Référence

- Jalon : `docs/transformations/core_modularization/J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md`
- Script : `docs/patcher/shared/consolidate_parallel_runs.py`
