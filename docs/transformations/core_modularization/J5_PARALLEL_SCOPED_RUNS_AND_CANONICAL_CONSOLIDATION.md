# J5 — Parallel Scoped Runs and Canonical Consolidation

## Principle

When multiple constitution runs execute in parallel on distinct scopes, each run produces
a **full patched copy** of the Core files inside its own isolated sandbox
(`runs/<run_id>/work/05_apply/sandbox/docs/cores/current/`).

These sandbox results are **independent by construction**: the scope catalog guarantees
that no two published scopes share the same writable IDs. As long as scope disjointness
is enforced, the sandbox outputs of N parallel runs can be deterministically merged
into a single new canonical version without conflict resolution.

This J5 chantier specifies the consolidation stage and its contract.

## Architecture

```
RUN_A/work/05_apply/sandbox/  ←  patched scope A (IDs: S_A_*)
RUN_B/work/05_apply/sandbox/  ←  patched scope B (IDs: S_B_*)
RUN_C/work/05_apply/sandbox/  ←  patched scope C (IDs: S_C_*)
         │
         ▼
docs/cores/staging/           ←  consolidated result (all scopes merged)
         │
         ▼  (after global integration_gate cleared)
docs/cores/current/           ←  new canonical version (STAGE_08 promotion)
```

## Preconditions for consolidation

- All participating runs must be in status `closed` with STAGE_06_CORE_VALIDATION `PASS`
- The `integration_gate` of each participating run must be explicitly cleared
- No active run may exist when consolidation starts
- Scope disjointness must be verified by `consolidate_parallel_runs.py` before any merge

## STAGE_10_CONSOLIDATE_PARALLEL_RUNS (to be added to pipeline)

### Objective
- Collect the N validated sandbox outputs from closed parallel runs
- Verify scope disjointness (no overlapping writable IDs across runs)
- Merge patched IDs into a single consolidated Core set under `docs/cores/staging/`
- Produce a `consolidation_report.yaml` summarizing merged runs, merged IDs, and any conflicts
- Gate: consolidation must not proceed if any scope overlap or integration_gate violation is detected

### Inputs
- `runs/<run_id>/work/05_apply/sandbox/` for each participating run
- `runs/<run_id>/inputs/scope_manifest.yaml` for each participating run (disjointness check)
- `runs/<run_id>/inputs/integration_gate.yaml` for each participating run (clearance check)
- `docs/cores/current/` as the base reference for non-patched IDs

### Output
- `docs/cores/staging/constitution.yaml`
- `docs/cores/staging/referentiel.yaml`
- `docs/cores/staging/link.yaml`
- `docs/cores/staging/consolidation_report.yaml`

### Script (to be created)
- `docs/patcher/shared/consolidate_parallel_runs.py`
  - `--runs RUN_A RUN_B RUN_C` (one or more run IDs)
  - `--base docs/cores/current`
  - `--output docs/cores/staging`
  - Verifies disjointness, merges, produces report
  - Execution is mandatory; result cannot be simulated

### Position in pipeline
- After all participating runs reach STAGE_09_CLOSEOUT_AND_ARCHIVE
- Before STAGE_07_RELEASE_MATERIALIZATION (which reads from `staging/` instead of a single sandbox)
- STAGE_10 is optional if only one run was executed (staging = sandbox output directly)

## Scope disjointness guarantee

The scope catalog (`scope_catalog/manifest.yaml`) is generated deterministically from
canon + policy. The `scope_definitions/<scope_key>.yaml` files declare the explicit
lists of writable IDs per scope. `consolidate_parallel_runs.py` must cross-check
these lists before merging and abort with a conflict report if any ID appears in
two or more participating scopes.

## Relationship with existing jalons

| Jalon | Contribution to J5 |
|---|---|
| J1 — Scoped Run Contract | defines run isolation and scope_manifest |
| J2 — Effective Read Surface Reduction | ids-first reads feed the patched scope slice |
| J3 — Canonical Reconstruction | J5 extends J3: reconstruction from N parallel sandbox outputs |
| J4 — Generated Scopes from Canon and Policy | guarantees disjointness of scope IDs used by J5 |

## Status

- `J5` concept: **documented** (this file)
- STAGE_10 spec: **pending** — to be added to `docs/pipelines/constitution/pipeline.md`
- `consolidate_parallel_runs.py`: **pending** — to be created in `docs/patcher/shared/`
- `docs/cores/staging/` area: **pending** — to be created when first consolidation runs
- Pipeline rule update (STAGE_07 reads staging when available): **pending**
