# Handover — Scope modularization post-pilot control-plane

## Repository context

```yaml
repository: stefm78/learn-it
branch: feat/core-modularization-bootstrap
pipeline: constitution
handover_date: 2026-04-29
handover_status: ready_to_resume_later
current_phase:
  phase_id: NO_ACTIVE_PHASE
  label: awaiting_next_human_decision
  status: paused
```

This handover summarizes the current state of the `core_modularization` / `scope graph clustering`
work after the bounded pilot run, post-pilot control-plane phases, bounded-run preflight
integration, active-document compaction, OPEN_NEW_RUN preflight gate validation, launcher preflight display hardening, and launcher new-run semantics clarification.

No Constitution pipeline run is currently open.

## Current state

```yaml
scope_modularization:
  status: paused_cleanly
  active_pipeline_run: none
  new_bounded_run_opened_now: false
  last_completed_pipeline_integration_phase: PHASE_22
  last_completed_cleanup_phase: PHASE_23A
  last_completed_validation_phase: PHASE_23B
  last_completed_launcher_hardening_phase: PHASE_24
  last_completed_launcher_semantics_phase: PHASE_25
  last_completed_phase: PHASE_25
  last_completed_phase_label: launcher_new_run_semantics_clarification
  current_recommendation: do_not_open_new_bounded_run_now
```

Compact active tracker:

```text
docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
```

Full historical tracker snapshot:

```text
docs/transformations/core_modularization/archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_PROGRESS_FULL_2026_04_29.md
```

Compact approach doctrine:

```text
docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
```

Full historical approach snapshot:

```text
docs/transformations/core_modularization/archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_APPROACH_FULL_2026_04_29.md
```

## What was completed

### 1. Scope Lab and graph-based scoping redesign

Completed:

- graph extraction;
- cluster detection;
- closure analysis;
- scope alignment review;
- redesign candidate generation;
- human arbitration;
- canonical policy/decisions patching;
- deterministic scope catalog regeneration;
- bijection and reconstruction validation;
- scope/neighbor extract validation.

Key outputs:

```text
tmp/scope_lab/
docs/pipelines/constitution/policies/scope_generation/policy.yaml
docs/pipelines/constitution/policies/scope_generation/decisions.yaml
docs/pipelines/constitution/scope_catalog/manifest.yaml
docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml
```

### 2. Pilot bounded local run

The serious pilot bounded run completed:

```yaml
phase_id: PHASE_13
run_id: CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01
scope: patch_lifecycle
status: PASS
run_status: closed
final_stage: STAGE_09_CLOSEOUT_AND_ARCHIVE
release_id: CORE_RELEASE_2026_04_28_R01
promoted_to_current: true
active_constitution_core_id: CORE_LEARNIT_CONSTITUTION_V5_0
active_constitution_version: V5_0_FINAL
governance_backlog_exported: true
```

This was a real Constitution pipeline run.

The later PHASE_14 through PHASE_25 work was control-plane, governance, tooling,
validation, launcher hardening, launcher semantics clarification, or documentation work. It was not another full stage 01 → 09 pipeline run.

### 3. Governance backlog integration

PHASE_14 completed the generic governance backlog mechanism:

```yaml
governance_backlog:
  canonical_store: docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
  produced_by: STAGE_02 local candidates
  exported_by: STAGE_09 closeout
  consumed_by: STAGE_00
  surfaced_by: launcher / entry resolution
  lifecycle_statuses:
    - open
    - addressed
    - wont_fix
```

Key files:

```text
docs/pipelines/constitution/scope_catalog/governance_backlog.yaml
docs/specs/constitution_governance_backlog_lifecycle.md
docs/patcher/shared/validate_governance_backlog_lifecycle.py
docs/patcher/shared/report_governance_backlog.py
docs/pipelines/constitution/reports/governance_backlog_report.yaml
docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml
```

### 4. Maturity scoring and score publication

PHASE_15 introduced deterministic post-scoping maturity scoring.

PHASE_16 resolved the Constitution neighbor-ID under-declaration signal.

PHASE_17 migrated score publication authority so computed maturity scores can be applied
to `policy.yaml` through a gated deterministic patcher.

Final expected scoring state:

```yaml
scope_maturity_scoring_report:
  status: PASS
  blocking_finding_count: 0
  warning_count: 0
  computed_lower_than_published_count: 0
  computed_delta_non_blocking_count: 0
```

Key files:

```text
docs/specs/constitution_scope_maturity_scoring.md
docs/patcher/shared/score_constitution_scope_maturity.py
docs/patcher/shared/apply_constitution_scope_maturity_scores.py
docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml
```

### 5. Neighbor declaration and multi-owner review

PHASE_18 completed MACRO_005 neighbor declaration review.

Accepted doctrine:

```yaml
neighbor_declarations:
  role: read_authority_not_ownership_authority
  canonical_inputs:
    - policy.yaml
    - decisions.yaml
  generated_outputs:
    - scope_catalog/manifest.yaml
    - scope_catalog/scope_definitions/*.yaml
  run_materialized_views:
    - scope_manifest.yaml
    - impact_bundle.yaml
    - scope_extract.yaml
    - neighbor_extract.yaml
```

PHASE_19 completed MACRO_004 multi-owner cluster review.

Result:

```yaml
multi_owner_review:
  validation_status: PASS_NO_PATCH_REQUIRED
  ownership_transfer: false
  policy_decisions_patch_required: false
  catalog_regeneration_required: false
```

### 6. Post-macro closeout and remaining backlog decision

PHASE_20 reconciled the original six pilot backlog entries:

```yaml
before:
  open: 6
after:
  addressed: 2
  open: 4
```

PHASE_21A decided not to open a new bounded run immediately:

```yaml
recommended_decision: do_not_open_new_bounded_run_now
new_pipeline_run_recommended_now: false
```

### 7. Bounded-run preflight integration

PHASE_22 generalized the PHASE_21A reasoning into the pipeline.

Completed:

```yaml
PHASE_22:
  label: bounded_run_preflight_pipeline_integration
  status: done
  subtasks:
    PHASE_22A_STAGE00_PREFLIGHT_CONTRACT: done
    PHASE_22B_PREFLIGHT_TOOLING_AND_FIRST_REPORT: done
    PHASE_22C_OPEN_NEW_RUN_PREFLIGHT_GATE: done
```

Key files:

```text
docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md
docs/pipelines/constitution/stages/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.skill.yaml
docs/patcher/shared/prepare_bounded_run_preflight.py
docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml
docs/pipelines/constitution/reports/bounded_run_preflight.md
docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml
```

Current preflight state:

```yaml
bounded_run_preflight:
  mode: run_candidate_preflight
  requested_scope_key: patch_lifecycle
  status: PREFLIGHT_DEFER_TO_STAGE00_REVIEW
  active_run_count: 0
  matching_open_entry_count: 4
  recommendation: defer_to_stage00_backlog_review
  new_bounded_run_recommended_now: false
```

Meaning:

```yaml
open_new_run_default:
  authorized: false
  reason: >-
    Open backlog entries exist, but they are reviewed design follow-ups, not urgent
    pipeline blockers. A new run requires explicit human override or a future
    PREFLIGHT_READY_TO_OPEN_RUN.
```

### 8. Active-document compaction

PHASE_23A compacted the two large active documents:

```yaml
compacted_active_docs:
  - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
  - docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md

archived_full_snapshots:
  - docs/transformations/core_modularization/archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_PROGRESS_FULL_2026_04_29.md
  - docs/transformations/core_modularization/archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_APPROACH_FULL_2026_04_29.md
```

The active files should now remain short. Detailed execution history belongs in the
archived snapshots unless a specific detail must be promoted back.

### 9. OPEN_NEW_RUN preflight gate validation

PHASE_23B created and validated the deterministic OPEN_NEW_RUN preflight gate validator.

```yaml
PHASE_23B:
  label: open_new_run_preflight_gate_validation
  status: done
  validator: docs/patcher/shared/validate_open_new_run_preflight_gate.py
  report: docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml
  report_status: PASS
  open_new_run_authorized_by_default_when_defer: false
  recommended_entry_decision_when_defer: partition_refresh_preferred_or_open_new_run_blocked
```

Meaning:

```yaml
open_new_run_gate:
  current_preflight_status: PREFLIGHT_DEFER_TO_STAGE00_REVIEW
  default_authorization: false
  human_override_required_to_authorize: true
```

### 10. Launcher preflight display hardening

PHASE_24 updated the experimental launcher so OPEN_NEW_RUN prompts surface the bounded-run
preflight signal alongside the governance backlog signal.

```yaml
PHASE_24:
  label: launcher_preflight_display
  status: done
  artifact: tmp/pipeline_launcher.py
  report: docs/pipelines/constitution/reports/launcher_preflight_display_validation.yaml
  report_status: PASS
  launcher_surfaces_preflight_signal: true
  defer_status_displayed_as_non_authorizing: true
  open_new_run_authorized_by_default_when_defer: false
```

The launcher remains experimental under `tmp/`; this phase only prevents ambiguous run-opening
prompts from hiding the current non-authorizing preflight status.

### 11. Launcher new-run semantics clarification

PHASE_25 clarified the meaning of `next_best_actions.new_run` in the experimental launcher.

```yaml
PHASE_25:
  label: launcher_new_run_semantics_clarification
  status: done
  artifact: tmp/pipeline_launcher.py
  report: docs/pipelines/constitution/reports/launcher_new_run_semantics_validation.yaml
  report_status: PASS
  new_run_status: entry_resolution_available
  run_opening_authorized_by_launcher: false
  run_materialization_authorized_by_launcher: false
  requires_open_new_run_decision: true
  requires_human_confirmation_before_materialization: true
```

Meaning:

```yaml
launcher_boundary:
  role: diagnostic_and_entry_prompt_helper
  not_authority_for:
    - run_opening
    - run_materialization
    - bypassing_OPEN_NEW_RUN
    - bypassing_bounded_run_preflight
```

The authoritative decision remains in the Constitution entry action and bounded-run preflight
contracts. The launcher remains intentionally simple.

## Remaining open backlog entries

Four reviewed backlog entries remain open intentionally:

```yaml
remaining_open_backlog_entries:
  - candidate_id: GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01
    topic: canonical patch lifecycle state machine
    recommended_treatment: keep_open_until_explicit_design_run
    rank_if_future_run_opened: 1

  - candidate_id: GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01
    topic: deterministic priority lanes for patch serialization
    recommended_treatment: keep_open_until_explicit_design_run
    rank_if_future_run_opened: 2

  - candidate_id: GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01
    topic: escalation boundary across patch_lifecycle, learner_state and deployment_governance
    recommended_treatment: include_conditionally_after_state_machine_design
    rank_if_future_run_opened: 3

  - candidate_id: GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
    topic: external-read-only referentiel parameter dependency for patch escalation threshold
    recommended_treatment: exclude_from_constitution_only_run / separate cross-core follow-up
    rank_if_future_run_opened: 4
```

These entries remain visible through:

```text
docs/pipelines/constitution/reports/governance_backlog_report.yaml
docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml
docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml
docs/pipelines/constitution/reports/launcher_preflight_display_validation.yaml
docs/pipelines/constitution/reports/launcher_new_run_semantics_validation.yaml
tmp/pipeline_launcher.py
STAGE_00 run_candidate_preflight
OPEN_NEW_RUN preflight gate
```

## Recommended next options

### Option A — Stop here

Recommended if the goal is to pause safely.

```yaml
decision: stop_here
reason: >-
  The control plane is compact, documented, and no run is open.
```

### Option B — PHASE_23B validate OPEN_NEW_RUN preflight gate

Completed.

```yaml
PHASE_23B:
  status: done
  artifact: docs/patcher/shared/validate_open_new_run_preflight_gate.py
  report: docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml
  report_status: PASS
  preflight_status: PREFLIGHT_DEFER_TO_STAGE00_REVIEW
  open_new_run_authorized_by_default: false
  recommended_entry_decision: partition_refresh_preferred_or_open_new_run_blocked
```

### Option C — Later open a targeted patch_lifecycle run

Only if a human explicitly decides to turn the remaining design follow-ups into a run.

```yaml
future_run:
  requires:
    - no active run
    - bounded_run_preflight_report available
    - explicit human override or future PREFLIGHT_READY_TO_OPEN_RUN
    - OPEN_NEW_RUN action
  recommended_scope_key: patch_lifecycle
  recommended_theme: patch_lifecycle_state_machine_and_priority_lanes
  include_first:
    - GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01
    - GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01
  conditional:
    - GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01
  separate_follow_up:
    - GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01
```

### Option D — Update launcher behavior

Completed in PHASE_24.

```yaml
PHASE_24:
  status: done
  artifact: tmp/pipeline_launcher.py
  report: docs/pipelines/constitution/reports/launcher_preflight_display_validation.yaml
  report_status: PASS
  launcher_surfaces_preflight_signal: true
  defer_status_displayed_as_non_authorizing: true
  open_new_run_authorized_by_default_when_defer: false
```

### Option E — Clarify launcher new-run semantics

Completed in PHASE_25.

```yaml
PHASE_25:
  status: done
  artifact: tmp/pipeline_launcher.py
  report: docs/pipelines/constitution/reports/launcher_new_run_semantics_validation.yaml
  report_status: PASS
  new_run_status: entry_resolution_available
  run_opening_authorized_by_launcher: false
  run_materialization_authorized_by_launcher: false
  requires_open_new_run_decision: true
  requires_human_confirmation_before_materialization: true
```

Next default remains Option A — stop here / keep NO_ACTIVE_PHASE.

## Operational checks for resuming later

```bash
git status --short

python docs/patcher/shared/validate_governance_backlog_lifecycle.py \
  --backlog docs/pipelines/constitution/scope_catalog/governance_backlog.yaml \
  --report docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml

python docs/patcher/shared/report_governance_backlog.py \
  --backlog docs/pipelines/constitution/scope_catalog/governance_backlog.yaml \
  --report docs/pipelines/constitution/reports/governance_backlog_report.yaml \
  --status open

python docs/patcher/shared/prepare_bounded_run_preflight.py \
  --scope-key patch_lifecycle \
  --report docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml \
  --markdown docs/pipelines/constitution/reports/bounded_run_preflight.md

python docs/patcher/shared/validate_open_new_run_preflight_gate.py \
  --report docs/pipelines/constitution/reports/open_new_run_preflight_gate_validation.yaml

python -m py_compile tmp/pipeline_launcher.py

python tmp/pipeline_launcher.py
```

## Guardrails

Do not do any of the following without an explicit new human decision:

```yaml
forbidden_without_new_decision:
  - open a new bounded_local_run
  - mutate policy.yaml
  - mutate decisions.yaml
  - regenerate scope catalog as a side effect of handover
  - close the four remaining backlog entries
  - treat read-neighbor declarations as ownership transfers
  - fold referentiel parameter dependency into a Constitution-only run
  - ignore PREFLIGHT_DEFER_TO_STAGE00_REVIEW when opening a backlog-driven run
  - expand the compact progress/approach files back into large journals
```

## Handoff prompt for a future conversation

```text
Repo learn-it, branch feat/core-modularization-bootstrap.

We are resuming after the scope modularization post-pilot control-plane was paused cleanly.
Current tracker state is NO_ACTIVE_PHASE / awaiting_next_human_decision.

Read first:
- docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
- docs/transformations/core_modularization/HANDOVER_SCOPE_MODULARIZATION_POST_PILOT.md
- docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
- docs/pipelines/constitution/reports/governance_backlog_report.yaml
- docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml
- docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml

Important state:
- The serious bounded pilot run was CONSTITUTION_RUN_2026_04_27_PATCH_LIFECYCLE_R01.
- It completed and promoted CORE_RELEASE_2026_04_28_R01.
- PHASE_14 through PHASE_25 were post-pilot control-plane, governance, tooling, validation, launcher hardening, launcher semantics clarification, or documentation work, not new full pipeline runs.
- PHASE_22 integrated bounded-run preflight into STAGE_00 and OPEN_NEW_RUN.
- PHASE_23B validated that OPEN_NEW_RUN does not authorize a backlog-driven run by default when preflight is PREFLIGHT_DEFER_TO_STAGE00_REVIEW.
- PHASE_24 surfaced the bounded-run preflight signal in tmp/pipeline_launcher.py.
- PHASE_25 clarified that next_best_actions.new_run means entry-resolution availability, not run authorization or run materialization.
- Current bounded-run preflight status for patch_lifecycle is PREFLIGHT_DEFER_TO_STAGE00_REVIEW.
- Four patch_lifecycle backlog entries remain open intentionally.
- Do not mutate policy.yaml, decisions.yaml, scope catalog, or governance_backlog.yaml unless a new explicit phase/run decision is made.
- Do not open a backlog-driven run without bounded-run preflight and explicit human confirmation/override.

Recommended next step:
Stop here by default. Open a future patch_lifecycle run only after a future PREFLIGHT_READY_TO_OPEN_RUN
or after explicit human override of the current PREFLIGHT_DEFER_TO_STAGE00_REVIEW recommendation.
```
