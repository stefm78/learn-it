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
4. `WORKLOG.md` — append-only factual execution log
5. `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md`
6. `AI_SKILL_GOVERNANCE_PATTERNS.md` — non-canonical design note for future AI workflow hardening
7. `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md` — only if multi-scope consolidation is in scope

Historical files are available only when deep traceability is needed:

- `archive/full_snapshots/`
- `archive/journals/`
- `archive/analyses/`
- `archive/status_snapshots/`

Archived documents are historical and non-canonical.

## Active transformation documents

| File | Role | Status |
|---|---|---|
| `SCOPE_GRAPH_CLUSTERING_PROGRESS.md` | Main phase tracker and handoff state | active |
| `SCOPE_GRAPH_CLUSTERING_APPROACH.md` | Implemented graph-based scoping doctrine | reference |
| `HANDOVER_SCOPE_MODULARIZATION_POST_PILOT.md` | Standalone resume/handover document | active handover |
| `WORKLOG.md` | Append-only factual execution log | active log |
| `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md` | Doctrine for treating `referentiel` and `link` as read-only external cores during Constitution runs | open doctrine |
| `AI_SKILL_GOVERNANCE_PATTERNS.md` | Non-canonical design note translating external AI skill patterns into `learn-it` governance ideas | reference |
| `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md` | Parallel scoped run consolidation model | active until first real multi-scope consolidation validation |

## Archived transformation journals and analyses

Archived intermediate journals live under:

```text
docs/transformations/core_modularization/archive/journals/
```

Archived files include:

- `J1_SCOPED_RUN_CONTRACT.md`
- `J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`
- `J2_EFFECTIVE_READ_SURFACE_REDUCTION.md`
- `J3_CANONICAL_RECONSTRUCTION_FROM_INTEGRATED_SCOPED_RESULTS.md`
- `J4_DERIVED_RUNTIME_TASK_VIEW_AND_STAGE_SKILLS.md`
- `J4_GENERATED_SCOPES_FROM_CANON_AND_POLICY.md`

Archived post-analysis documents live under:

```text
docs/transformations/core_modularization/archive/analyses/
```

Archived analysis files include:

- `POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md`

Historical `STATUS_*` snapshots, when present, are archived under:

```text
docs/transformations/core_modularization/archive/status_snapshots/
```

They are preserved for traceability only. Their stabilized decisions are now carried
by pipeline specs, stage skills, deterministic scripts, generated scope catalog
artifacts, backlog metadata, and validation reports.

## Current macro state

The graph-based scope partitioning approach has been implemented, pilot-validated,
and promoted through the `patch_lifecycle` bounded run.

PHASE_29 is closed:

- the Stage 00 backlog review is complete;
- the four remaining `patch_lifecycle` backlog entries are still `open` but reviewed;
- operational pipeline signals are refreshed deterministically from the reviewed backlog state;
- `bounded_run_preflight_report.yaml` is now `PREFLIGHT_KEEP_BACKLOG_OPEN`;
- the generated scope catalog is aligned with `REF_CORE_LEARNIT_REFERENTIEL_V5_0_IN_CONSTITUTION`;
- `Challenge_constitution.md` and `STAGE_01_CHALLENGE.skill.yaml` now carry generic bounded-scope maturity signals without publishing maturity scores.

Current operational state:

```yaml
current_phase: NO_ACTIVE_PHASE
active_pipeline_run: none
new_bounded_run_opened_now: false
default_next_action: keep_NO_ACTIVE_PHASE
future_targeted_challenge_requires: explicit_human_override
```

The next possible action is a human decision, not an automatic run opening.

A future targeted challenge can be prepared around a reviewed open backlog theme, but
only through the canonical `OPEN_NEW_RUN` flow and with explicit human confirmation
when preflight remains `PREFLIGHT_KEEP_BACKLOG_OPEN`.

## Governance rules

1. Do not treat archived journals as active inputs.
2. Do not edit generated scope catalog files manually.
3. Treat `docs/pipelines/constitution/policies/scope_generation/policy.yaml` and
   `decisions.yaml` as governed inputs for scope generation.
4. Treat `docs/pipelines/constitution/scope_catalog/` as generated output.
5. Use deterministic scripts for generation, validation, score publication, and run
   lifecycle transitions.
6. Keep this README as the entry index, not as a replacement for the active tracker.
7. Treat `AI_SKILL_GOVERNANCE_PATTERNS.md` as a non-canonical design note until a
   later explicit decision promotes any idea into a spec or pipeline contract.

## Cleanup policy

The first-level directory should remain small.

Keep active:

- current tracker;
- current approach / doctrine documents;
- active handover and worklog;
- still-open doctrine documents;
- AI skill governance note until accepted, promoted, or archived by explicit decision;
- J5 until the first real multi-scope consolidation validation.

Archive:

- intermediate design journals once their decisions are implemented elsewhere;
- post-analysis documents once their decisions are reflected in canonical backlog, reports, or signals;
- design notes once accepted into specs or rejected;
- J-files once they have been absorbed into specs or stage contracts.

Delete only when:

- the file is unreferenced;
- the content is fully absorbed elsewhere;
- a worklog entry records the removal rationale.
