# PIPELINE — <pipeline_id>

id: <pipeline_id>
version: 0.1
scope: <pipeline_scope>
hardening_level: L1 | L2 | L3 | L4

## Goal

Describe what this pipeline governs.

## Non-goals

```yaml
non_goals:
  - do_not_patch_core_files_without_explicit_authorization
  - do_not_close_backlog_without_validated_resolution
  - do_not_claim_release_or_promotion_without_reports
```

## Hardening profile

```yaml
hardening_profile:
  target_level: L2
  canonical_write_surface: reports_only
  entry_control: required_if_stateful
  required_scripts_must_execute: true
  direct_ai_writes_to_owned_state: forbidden
```

## Canonical resources

```text
docs/pipelines/<pipeline_id>/pipeline.md
docs/pipelines/<pipeline_id>/state.yaml
docs/pipelines/<pipeline_id>/reports/
```

## Controlled write surface

Allowed:

```text
docs/pipelines/<pipeline_id>/reports/**
docs/pipelines/<pipeline_id>/work/**
docs/pipelines/<pipeline_id>/outputs/**
```

Forbidden unless a later explicit contract authorizes it:

```text
docs/cores/current/**
docs/pipelines/constitution/scope_catalog/**
docs/cores/releases/**
```

## Stages

### STAGE_00_INTAKE

Validate that the request/input is shaped and non-mutating.

### STAGE_01_REVIEW_OR_EXECUTION

Perform the pipeline-specific work.

### STAGE_02_VALIDATION

Validate outputs with deterministic scripts.

### STAGE_03_CLOSEOUT

Materialize summary and final evidence.

## Success criteria

```yaml
success_criteria:
  - declared_outputs_exist
  - required_validation_report_passes
  - forbidden_write_surface_untouched
  - final_summary_exists
```
