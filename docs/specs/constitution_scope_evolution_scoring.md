# Constitution scope evolution scoring

## Purpose

`scope_evolution_score.yaml` is a post-run diagnostic report.

It answers a different question from scope maturity scoring:

- `scope_maturity_scoring_report.yaml` answers: **what is the structural maturity of the scope now?**
- `scope_evolution_score.yaml` answers: **how much did this run move the scope forward, operationally and structurally?**

The report is intentionally non-publishing. It must not update:

- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- scope catalog outputs
- Core files
- release bundles
- governance backlog entries

## Generic applicability

The scoring script is scope-agnostic:

```bash
python docs/patcher/shared/score_constitution_scope_evolution.py   --run-id <RUN_ID>   --scope-key <SCOPE_KEY>
```

Default outputs:

```text
docs/pipelines/constitution/reports/scope_maturity_scoring_report_post_<RUN_ID>.yaml
docs/pipelines/constitution/runs/<RUN_ID>/reports/scope_evolution_score.yaml
docs/pipelines/constitution/runs/<RUN_ID>/reports/scope_evolution_score.md
```

## Dimensions

The total score is `/100`.

| Dimension | Max | Meaning |
|---|---:|---|
| `stage_chain_integrity` | 20 | Required stage evidence exists and has `PASS` status. |
| `closeout_and_tracking_readiness` | 20 | Closeout evidence exists; tracking is closed or ready to close. |
| `structural_maturity_delta` | 20 | Diagnostic maturity movement versus published governed maturity. |
| `backlog_pressure` | 20 | Penalizes unresolved severe open backlog related to the scope. |
| `cross_scope_alignment_pressure` | 10 | Penalizes unresolved cross-scope / cross-core pressure. |
| `operational_repeatability` | 10 | Evidence needed to replay, audit and understand the run is present. |

## Classification

| Score | Classification |
|---:|---|
| 85–100 | `strong_scope_progress` |
| 70–84 | `positive_progress_with_open_debt` |
| 55–69 | `limited_progress_requires_follow_up` |
| 0–54 | `weak_or_incomplete_progress` |

## Governance rule

This report may inform future scoring publication, but it never publishes maturity itself.

Any change to official scope maturity remains governed by the existing policy/decisions path and must be arbitrated explicitly.
