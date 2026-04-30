# Pipeline hardening reference model

## Purpose

This document extracts a reusable hardening model from the Constitution pipeline.

The Constitution pipeline is the current level-4 reference because it separates:

- entry decision;
- run materialization;
- deterministic input generation;
- stage execution;
- validation;
- release materialization;
- promotion;
- closeout;
- post-run evolution scoring.

The goal is not to copy the Constitution pipeline everywhere. The goal is to apply the right
hardening level to each pipeline according to its risk.

## Core principle

```text
The harder the write surface, the harder the pipeline contract must be.
```

## Hardening levels

### L1 — Exploratory pipeline

Use when the pipeline only helps humans inspect or prototype.

Required:

- `pipeline.md`;
- clear goal and non-goals;
- declared output directory;
- no canonical writes;
- no release or promotion.

### L2 — Governed diagnostic pipeline

Use when the pipeline produces reports that may influence future decisions.

Required on top of L1:

- `state.yaml` or equivalent status surface;
- validation script for generated reports;
- explicit mutation policy;
- explicit forbidden write surface;
- report status values.

### L3 — Managed execution pipeline

Use when the pipeline has durable state, runs, requests, or staged execution.

Required on top of L2:

- entry actions;
- run or request identifiers;
- deterministic materialization script;
- explicit stage contracts;
- owner scripts for generated state;
- no direct AI writes to owned state;
- reconciliation or restart rule.

### L4 — Critical canonical pipeline

Use when the pipeline can affect canonical Core files, generated scope catalog, releases,
promotion, cross-core contracts, or backlog closure.

Required on top of L3:

- strict AI protocol;
- forbidden direct writes;
- baseline capture;
- pre-release or pre-apply preview;
- final closeout score or evidence report;
- explicit release/promotion authority;
- explicit human decision points;
- strong recovery/reconciliation path;
- validation gates before any canonical write;
- clear distinction between local success and global consistency.

The Constitution pipeline is the reference L4 pipeline.

## Reusable hardening dimensions

```yaml
hardening_dimensions:
  entry_control:
    question: Can the pipeline start only through an explicit entry decision?
    reference: Constitution OPEN_NEW_RUN then MATERIALIZE_NEW_RUN

  owned_state:
    question: Are generated state files owned by deterministic scripts?
    reference: Constitution AI_PROTOCOL forbidden_direct_writes

  read_surface:
    question: Are primary and fallback reads declared?
    reference: Constitution stage skill primary_reads / fallback_reads

  write_surface:
    question: Are allowed and forbidden writes declared?
    reference: Constitution and cross_core_contract controlled write surfaces

  required_scripts:
    question: Can a required script be skipped or simulated?
    reference: Constitution deterministic_script_policy forbids simulated execution

  stage_evidence:
    question: Does every stage define completion evidence and not_sufficient cases?
    reference: STAGE_06_CORE_VALIDATION.skill.yaml

  release_authority:
    question: Is release_required decided by a deterministic release plan, not a chat summary?
    reference: build_release_plan.py remains authoritative

  promotion_authority:
    question: Is promotion explicit, centralized and validated?
    reference: Constitution STAGE_08 promotion flow

  before_after_diagnostics:
    question: Does the pipeline capture baseline, preview and final score when useful?
    reference: baseline_scope_state, scope_evolution_preview, scope_evolution_score

  closeout:
    question: Does the pipeline close or archive with durable evidence?
    reference: Constitution STAGE_09 closeout
```

## Recommended adoption rule

```yaml
adoption_rule:
  report_only_pipeline: L1_or_L2
  governance_or_intake_pipeline: L2_or_L3
  stateful_execution_pipeline: L3
  canonical_write_pipeline: L4
  release_or_promotion_pipeline: L4
  cross_core_pipeline: L3_initially_then_L4_before_any_core_write
```

## Constitution reference patterns to reuse

```yaml
patterns_to_reuse:
  - two_step_startup_decision_then_materialization
  - forbidden_direct_writes_with_owner_script
  - deterministic_script_policy
  - explicit_primary_reads_and_fallback_reads
  - expected_outputs_and_completion_evidence
  - not_sufficient_conditions
  - pre_release_preview
  - final_closeout_score
  - no_local_success_equals_global_consistency
  - human_action_required_before_transition
```

## Anti-patterns

```yaml
anti_patterns:
  - chat_summary_as_pass
  - script_declared_but_not_executed
  - direct_ai_write_to_state_file
  - implicit_release_required
  - promotion_claim_without_promotion_report
  - closing_backlog_without_validated_resolution
  - core_write_authorized_by_request_creation
  - copying_L4_complexity_to_L1_pipeline_without_need
```
