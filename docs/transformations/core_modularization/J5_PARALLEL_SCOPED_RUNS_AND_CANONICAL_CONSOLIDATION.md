# J5 — Parallel Scoped Runs and Canonical Consolidation

## Principle

When multiple constitution runs execute in parallel on distinct scopes, each run produces
a **full patched copy** of the Core files inside its own isolated sandbox
(`runs/<run_id>/work/05_apply/sandbox/`).

These sandbox results are **independent by construction**: the scope catalog guarantees
that no two published scopes share the same writable IDs. As long as scope disjointness
is enforced, the sandbox outputs of N parallel runs can be deterministically merged
into a single consolidated work area without conflict resolution.

This J5 chantier specifies the consolidation stage and its contract.

## Architecture

```
RUN_A/work/05_apply/sandbox/   ←  patched scope A (IDs: S_A_*)
RUN_B/work/05_apply/sandbox/   ←  patched scope B (IDs: S_B_*)
RUN_C/work/05_apply/sandbox/   ←  patched scope C (IDs: S_C_*)
         │
         ▼  STAGE_06B_CONSOLIDATION
docs/pipelines/constitution/work/consolidation/   ←  artefact pipeline (non canonique)
         │
         ▼  STAGE_07_RELEASE_MATERIALIZATION
docs/cores/releases/<release_id>/   ←  release immuable
         │
         ▼  STAGE_08_PROMOTE_CURRENT
docs/cores/current/   ←  nouvelle version canonique
```

`docs/cores/` ne reçoit jamais rien d'intermédiaire.
Seul STAGE_08 promeut vers `current/`.

## Préconditions pour la consolidation

- Tous les runs participants doivent être en statut `closed` avec STAGE_06_CORE_VALIDATION `PASS`
- L'`integration_gate` de chaque run participant doit être explicitement cleared
- Aucun run actif ne doit exister quand la consolidation démarre
- La disjonction des scopes est vérifiée par `consolidate_parallel_runs.py` avant toute écriture

## STAGE_06B_CONSOLIDATION

### Objectif
- Collecter les N sandbox validées des runs clos
- Vérifier la disjonction des scopes (pas d'IDs chevauchants)
- Merger les IDs patchés dans un ensemble Core unique sous `work/consolidation/`
- Produire un `consolidation_report.yaml` résumant runs participants, IDs mergés, conflits éventuels
- Gate : abort si chevauchement de scope ou integration_gate non cleared

### Inputs
- `runs/<run_id>/work/05_apply/sandbox/` pour chaque run
- `runs/<run_id>/inputs/scope_manifest.yaml` (vérification disjonction)
- `runs/<run_id>/inputs/integration_gate.yaml` (vérification clearance)
- `docs/cores/current/` comme base de référence pour les IDs non patchés

### Output
- `docs/pipelines/constitution/work/consolidation/constitution.yaml`
- `docs/pipelines/constitution/work/consolidation/referentiel.yaml`
- `docs/pipelines/constitution/work/consolidation/link.yaml`
- `docs/pipelines/constitution/work/consolidation/consolidation_report.yaml`

### Script
- `docs/patcher/shared/consolidate_parallel_runs.py`
  - `--runs RUN_A RUN_B RUN_C`
  - `--base docs/cores/current`
  - `--output docs/pipelines/constitution/work/consolidation`
  - `--pipeline constitution`
  - Vérifie disjonction, merge, produit rapport
  - Exécution réelle obligatoire ; résultat ne peut pas être simulé

### Position
- Après STAGE_06_CORE_VALIDATION de tous les runs participants (tous PASS)
- Après STAGE_09_CLOSEOUT_AND_ARCHIVE de tous les runs
- Avant STAGE_07_RELEASE_MATERIALIZATION
- Optionnel si un seul run actif (STAGE_07 lit directement le sandbox)

## Calcul de release en mode consolidation

`build_release_plan.py` compare un ensemble patché vs `current/`.
En mode consolidation, STAGE_07 lui passe `work/consolidation/` comme `patched_root`
au lieu de `work/05_apply/patched/`.
La logique de versioning ne change pas — c'est la source qui change.

```
# mode run unique
build_release_plan.py  runs/<run_id>/work/05_apply/patched  docs/cores/current  ...

# mode consolidation
build_release_plan.py  docs/pipelines/constitution/work/consolidation  docs/cores/current  ...
```

Le `consolidation_report.yaml` (liste des runs participants) est ajouté dans les
`validated_inputs` du `release_plan.yaml` pour la traçabilité.

## Garantie de disjonction des scopes

Le scope catalog (`scope_catalog/manifest.yaml`) est généré déterministement depuis
canon + policy. Les `scope_definitions/<scope_key>.yaml` déclarent les listes explicites
d'IDs par scope. `consolidate_parallel_runs.py` croise ces listes avant fusion
et abort avec un rapport de conflit si un ID apparaît dans deux scopes ou plus.

## Relation avec les jalons existants

| Jalon | Contribution à J5 |
|---|---|
| J1 — Scoped Run Contract | définit l'isolation du run et le scope_manifest |
| J2 — Effective Read Surface Reduction | ids-first feeds the patched scope slice |
| J3 — Canonical Reconstruction | J5 étend J3 : reconstruction depuis N sandbox parallèles |
| J4 — Generated Scopes from Canon and Policy | garantit la disjonction des IDs utilisés par J5 |

## Status

- `J5` concept : **documenté** (ce fichier)
- STAGE_06B spec : **done** — `docs/pipelines/constitution/STAGE_06B_CONSOLIDATION.md`
- STAGE_06B dans `pipeline.md` : **done**
- `consolidate_parallel_runs.py` : **done** — `docs/patcher/shared/consolidate_parallel_runs.py`
- `work/consolidation/` : **done** — répertoire pipeline créé
- Adaptation STAGE_07 (lit `work/consolidation/` si disponible) : **done** — dans `pipeline.md`
- `build_release_plan.py` en mode consolidation : **à valider** lors du premier run multi-scopes réel
