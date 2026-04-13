# docs/cores/staging/

Zone de consolidation des résultats de runs parallèles sur scopes disjoints.

## Rôle

Ce répertoire reçoit les Core files consolidés produits par `consolidate_parallel_runs.py`
après exécution de N runs parallèles sur des scopes disjoints.

Il constitue l'entrée de STAGE_07_RELEASE_MATERIALIZATION lorsqu'une consolidation
multi-runs a été effectuée.

## Contenu attendu après consolidation

- `constitution.yaml` — Core Constitution consolidé
- `referentiel.yaml` — Core Référentiel consolidé
- `link.yaml` — Core LINK consolidé
- `consolidation_report.yaml` — rapport de consolidation (runs participants, IDs merged, statut)

## Règles

- Ce répertoire est transitoire : il est écrasé à chaque nouvelle consolidation
- Il ne remplace jamais `docs/cores/current/` directement
- La promotion vers `current/` reste un acte explicite via STAGE_08_PROMOTE_CURRENT
- Ce répertoire ne doit pas être archivé tel quel ; seule la release matérialisée
  sous `docs/cores/releases/` est immuable
- Si un seul run est actif, `staging/` peut être alimenté directement depuis
  le sandbox du run sans passer par `consolidate_parallel_runs.py`

## Référence

- Jalon : `docs/transformations/core_modularization/J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md`
- Script : `docs/patcher/shared/consolidate_parallel_runs.py`
