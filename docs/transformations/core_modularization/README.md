# Core modularization transformation

Status: active transformation index  
Branch: `feat/core-modularization-bootstrap`  
Pipeline primarily concerned: `constitution`

## Purpose

This directory tracks the core modularization and scope partitioning transformation.

It is not the canonical execution source of the Constitution pipeline. Canonical
pipeline behavior lives under:

- `docs/pipelines/constitution/`
- `docs/patcher/shared/`
- `docs/specs/`
- `docs/cores/current/`
- `docs/pipelines/constitution/scope_catalog/`

This directory exists to preserve the transformation rationale, progress tracker,
open follow-ups, and historical design notes.

## Current reading order

For a human or AI resuming the transformation, read in this order:

1. `SCOPE_GRAPH_CLUSTERING_PROGRESS.md` — compact current state and resume options
2. `HANDOVER_SCOPE_MODULARIZATION_POST_PILOT.md` — standalone handover
3. `SCOPE_GRAPH_CLUSTERING_APPROACH.md` — compact implemented doctrine
4. `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md`
5. `POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md`
6. Full historical snapshots only if deep traceability is needed:
   - `archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_PROGRESS_FULL_2026_04_29.md`
   - `archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_APPROACH_FULL_2026_04_29.md`
7. Active J-files only if needed:
   - `J1_SCOPED_RUN_CONTRACT.md`
   - `J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`
   - `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md`

Archived journals under `archive/journals/` are historical and non-canonical.

## Active transformation documents

| File | Role | Status |
|---|---|---|
| `SCOPE_GRAPH_CLUSTERING_PROGRESS.md` | Main phase tracker and handoff state | active |
| `SCOPE_GRAPH_CLUSTERING_APPROACH.md` | Implemented graph-based scoping doctrine | reference |
| `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md` | Doctrine for treating `referentiel` and `link` as read-only external cores during Constitution runs | open doctrine |
| `POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md` | Non-canonical triage of backlog entries exported by the patch_lifecycle pilot | historical analysis, still useful |
| `J1_SCOPED_RUN_CONTRACT.md` | Bounded run contract: `scope_manifest`, `impact_bundle`, `integration_gate` | active because still referenced |
| `J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md` | Minimal Constitution pipeline delta for bounded runs | active supporting note |
| `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md` | Parallel scoped run consolidation model | active until first real multi-scope consolidation validation |

## Archived transformation journals

The following intermediate journals have been archived under:

```text
docs/transformations/core_modularization/archive/journals/
```

Archived files:

- `J2_EFFECTIVE_READ_SURFACE_REDUCTION.md`
- `J3_CANONICAL_RECONSTRUCTION_FROM_INTEGRATED_SCOPED_RESULTS.md`
- `J4_DERIVED_RUNTIME_TASK_VIEW_AND_STAGE_SKILLS.md`
- `J4_GENERATED_SCOPES_FROM_CANON_AND_POLICY.md`

They are preserved for traceability only. Their stabilized decisions are now carried
by pipeline specs, stage skills, deterministic scripts, generated scope catalog
artifacts, and validation reports.

## Current macro state

The graph-based scope partitioning approach has been implemented, pilot-validated,
and promoted through the `patch_lifecycle` bounded run.

PHASE_17 is closed:

- deterministic maturity scoring exists;
- computed maturity scores are publishable through a gated policy patcher;
- `policy.yaml` has been synchronized;
- scope catalog regeneration passes;
- final maturity scoring passes;
- the score patcher dry-run is idempotent.

The next selected follow-up is:

```text
PHASE_18 — MACRO_005_NEIGHBOR_DECLARATION_REVIEW
```

This should normally run before:

```text
MACRO_004_MULTI_OWNER_CLUSTER_REVIEW
```

because the repository has just stabilized the neighbor declaration and maturity
score publication loop.

## Governance rules

1. Do not treat archived journals as active inputs.
2. Do not edit generated scope catalog files manually.
3. Treat `docs/pipelines/constitution/policies/scope_generation/policy.yaml` and
   `decisions.yaml` as governed inputs for scope generation.
4. Treat `docs/pipelines/constitution/scope_catalog/` as generated output.
5. Use deterministic scripts for generation, validation, score publication, and run
   lifecycle transitions.
6. Keep this README as the entry index, not as a replacement for the active tracker.

## Cleanup policy

The first-level directory should remain small.

Keep active:

- current tracker;
- current approach / doctrine documents;
- active open follow-up documents;
- still-referenced J-files.

Archive:

- intermediate design journals once their decisions are implemented elsewhere;
- post-analysis documents once their backlog entries are resolved;
- J-files once they have been absorbed into specs or stage contracts.

Delete only when:

- the file is unreferenced;
- the content is fully absorbed elsewhere;
- a worklog entry records the removal rationale.
