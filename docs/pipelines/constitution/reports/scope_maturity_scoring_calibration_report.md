# Scope maturity scoring calibration report

Status: calibration_required
Source report: `docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml`
Authority: diagnostic only — no policy rewrite

## 1. Calibration purpose

This report records the first calibration pass after the deterministic post-scoping maturity scorer produced a `FAIL` diagnostic. The `FAIL` is treated as a governed calibration signal, not as permission to rewrite `policy.yaml`.

## 2. First scoring report summary

```yaml
status: FAIL
scope_count: 5
computed_lower_than_published_count: 4
computed_delta_non_blocking_count: 1
policy_authority_unchanged: true
```

## 3. Scope deltas

| scope | published | computed V1 | delta | level delta | severity |
| --- | --- | --- | --- | --- | --- |
| deployment_governance | 19 / L3_operational | 13 / L2_usable_with_care | -6 | computed_lower_than_published | fail |
| knowledge_and_design | 17 / L3_operational | 15 / L2_usable_with_care | -2 | computed_lower_than_published | fail |
| learner_state | 17 / L3_operational | 14 / L2_usable_with_care | -3 | computed_lower_than_published | fail |
| mastery_evaluation | 18 / L3_operational | 17 / L3_operational | -1 | none | warn |
| patch_lifecycle | 16 / L2_usable_with_care | 12 / L1_fragile | -4 | computed_lower_than_published | fail |

## 4. Calibration findings

### Finding A — `dependency_explicitness` is the main blocking axis

| scope | dep score | outgoing | covered | uncovered | neighbor ids | neighbor files |
| --- | --- | --- | --- | --- | --- | --- |
| deployment_governance | 0 | 7 | 0 | 7 | 1 | 2 |
| knowledge_and_design | 0 | 2 | 0 | 2 | 1 | 2 |
| learner_state | 0 | 3 | 0 | 3 | 1 | 2 |
| mastery_evaluation | 2 | 6 | 3 | 3 | 5 | 2 |
| patch_lifecycle | 0 | 6 | 0 | 6 | 1 | 2 |

Interpretation: this is mostly a real governance signal, not merely a display issue. Most Constitution-to-Constitution outgoing dependencies are not declared as explicit `default_neighbors_to_read.ids`. The generated scopes generally declare external `referentiel` and `link` files, but few concrete Constitution neighbor IDs. The scorer is therefore correctly surfacing missing explicit neighbor declarations.

Calibration decision: **do not neutralize this axis**. Future adjustment should make the evidence more granular, not automatically raise the score.

### Finding B — `internal_coherence` is probably too harsh for composite but cohesive scopes

| scope | current score | dominant logic ratio | internal edge ratio | preview score |
| --- | --- | --- | --- | --- |
| deployment_governance | 2 | 0.368 | 0.611 | 2 |
| knowledge_and_design | 2 | 0.35 | 0.931 | 3 |
| learner_state | 2 | 0.538 | 0.929 | 3 |
| mastery_evaluation | 3 | 0.552 | 0.882 | 3 |
| patch_lifecycle | 2 | 0.409 | 0.846 | 3 |

Interpretation: several scopes intentionally aggregate multiple `logic.scope` values, but still show strong internal edge cohesion. A pure dominant-label rule penalizes valid semantic aggregates.

Calibration hypothesis H2: keep the dominant label signal, but allow a score floor of 3 when internal edge cohesion is high enough.

### Finding C — `inter_release_stability` mixes maturity and confidence

| scope | current score | preview score | open backlog entries |
| --- | --- | --- | --- |
| deployment_governance | 2 | 2 | 2 |
| knowledge_and_design | 2 | 3 | 0 |
| learner_state | 2 | 2 | 2 |
| mastery_evaluation | 2 | 3 | 0 |
| patch_lifecycle | 2 | 2 | 6 |

Interpretation: the V1 scorer correctly marks release-history evidence as limited, but the absence of a dedicated release-to-release history should be represented as confidence limitation before becoming a universal score penalty.

Calibration hypothesis H3: split `inter_release_stability.score` from `inter_release_stability.confidence`. Keep backlog-based penalties, but avoid lowering all scopes only because history evidence is not yet consumed.

## 5. Calibrated preview

| scope | published | computed V1 | calibrated preview |
| --- | --- | --- | --- |
| deployment_governance | 19 / L3_operational | 13 / L2_usable_with_care | 13 / L2_usable_with_care |
| knowledge_and_design | 17 / L3_operational | 15 / L2_usable_with_care | 17 / L3_operational |
| learner_state | 17 / L3_operational | 14 / L2_usable_with_care | 15 / L2_usable_with_care |
| mastery_evaluation | 18 / L3_operational | 17 / L3_operational | 18 / L3_operational |
| patch_lifecycle | 16 / L2_usable_with_care | 12 / L1_fragile | 13 / L2_usable_with_care |

The preview is not a new authority. It is only a deterministic calibration aid. `policy.yaml` remains the published authority until an explicit arbitration updates it.

## 6. Recommended next implementation changes

Recommended for scorer V1.1:

1. Keep `dependency_explicitness` strict, but split evidence into:
   - `constitution_neighbor_id_coverage`;
   - `external_core_file_coverage`;
   - `external_core_id_coverage`;
   - `uncovered_constitution_neighbor_ids`.
2. Adjust `internal_coherence` to weight internal edge cohesion alongside dominant `logic.scope` ratio.
3. Split `inter_release_stability` into score and confidence, or keep the score but emit `evidence_limited` without a universal penalty.
4. Keep report status `FAIL` when computed level is lower than published level, but label this as `calibration_required` until V1.1 is validated.
5. Do not modify `policy.yaml` from this calibration pass.

## 7. Calibration decisions

```yaml
calibration_decisions:
  - decision_id: CALIBRATION_001_KEEP_POLICY_AUTHORITY
    status: accepted
    decision: Keep policy.yaml authoritative for published maturity.
  - decision_id: CALIBRATION_002_KEEP_DEPENDENCY_EXPLICITNESS_STRICT
    status: accepted
    decision: Keep dependency explicitness as a real governance signal, but improve evidence granularity.
  - decision_id: CALIBRATION_003_ADJUST_INTERNAL_COHERENCE
    status: candidate
    decision: Allow high internal edge cohesion to compensate for composite logic.scope distribution.
  - decision_id: CALIBRATION_004_SPLIT_STABILITY_SCORE_AND_CONFIDENCE
    status: candidate
    decision: Treat missing release history as limited confidence rather than automatic maturity loss.
next_action: implement scorer V1.1 candidate, rerun report, compare with current diagnostic
```
