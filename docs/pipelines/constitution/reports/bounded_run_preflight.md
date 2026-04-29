# Bounded run preflight

Stage: `STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN`
Mode: `run_candidate_preflight`
Status: `PREFLIGHT_DEFER_TO_STAGE00_REVIEW`
Requested scope: `patch_lifecycle`

## Decision

- Recommendation: `defer_to_stage00_backlog_review`
- New bounded run recommended now: `false`
- Next action: `keep_backlog_open_with_review_metadata`

Open backlog entries exist for the requested scope, but they are reviewed design follow-ups rather than urgent pipeline blockers. Do not open a new bounded run now unless a human explicitly overrides the preflight.

## Backlog signal

- Matching open backlog entries: `4`
- Active constitution runs: `0`

## Entries

| Rank | Candidate | Type | Inclusion |
|---:|---|---|---|
| 1 | `GBC_PATCH_LIFECYCLE_FULL_STATE_MACHINE_R01` | `scope_gap` | `include_first_if_run_opened` |
| 2 | `GBC_PATCH_LIFECYCLE_PRIORITY_QUEUE_R01` | `scope_gap` | `include_first_if_run_opened` |
| 3 | `GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R01` | `scope_extension_needed` | `include_conditionally_after_state_machine_design` |
| 4 | `GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01` | `scope_gap` | `exclude_from_constitution_only_run` |

## Guardrails

- This report does not open a run.
- Do not mutate policy.yaml or decisions.yaml from preflight.
- Do not regenerate the scope catalog from preflight.
- Do not close backlog entries from preflight; use the lifecycle validator and an explicit lifecycle patch.
- Do not include cross-core referentiel dependencies in a Constitution-only run without a cross-core contract.
