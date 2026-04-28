# Constitution governance backlog lifecycle

Status: canonical lifecycle specification  
Pipeline: `constitution`  
Backlog source of truth: `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`

## Purpose

Define the deterministic lifecycle of governance backlog entries generated during
Constitution runs and consumed during STAGE_00 scope partition review.

This specification belongs to PHASE_14F of the scope graph clustering transformation:
`backlog_status_lifecycle`.

## Status values

Only three canonical status values are allowed:

```yaml
allowed_status_values:
  - open
  - addressed
  - wont_fix
```

### `open`

The entry is active and must continue to be surfaced by STAGE_00, launcher / entry
resolution, and governance backlog reports.

An entry may remain `open` after a STAGE_00 review, but only if the review records
why it remains open. This is a deferral, but it is not a separate status.

### `addressed`

The entry was resolved by a later STAGE_00, run, policy/decisions update, cross-core
change, or documented governance action.

Required resolution metadata:

```yaml
required_fields:
  - resolved_at
  - resolved_by
  - resolution_note
```

### `wont_fix`

The entry was explicitly rejected as a planned correction.

Required resolution metadata:

```yaml
required_fields:
  - resolved_at
  - resolved_by
  - resolution_note
```

The `resolution_note` must state why the issue is intentionally not fixed.

## Deferral policy

`deferred`, `reported`, `report_decided`, or equivalent values are not status values.

A deferred item remains:

```yaml
status: open
```

and may optionally include review metadata:

```yaml
last_reviewed_at: "<ISO-8601 timestamp>"
last_reviewed_by: "STAGE_00_<date> or run_id"
review_note: "Why it remains open"
next_review_trigger: "When / why it must be reviewed again"
```

If one of those review metadata fields is present, all four must be present.

## Allowed transitions

```yaml
transitions:
  - from: open
    to: addressed
    requires:
      - resolved_at
      - resolved_by
      - resolution_note

  - from: open
    to: wont_fix
    requires:
      - resolved_at
      - resolved_by
      - resolution_note

  - from: open
    to: open
    meaning: deferred_after_review
    optional_metadata_group:
      - last_reviewed_at
      - last_reviewed_by
      - review_note
      - next_review_trigger
```

Direct transitions from `addressed` or `wont_fix` back to `open` are not forbidden by
the file format, but they must be treated as a new governance decision and documented
with a new `resolution_note` or review note. They must not happen silently.

## Deterministic validation

Canonical validator:

```bash
python docs/patcher/shared/validate_governance_backlog_lifecycle.py \
  --backlog docs/pipelines/constitution/scope_catalog/governance_backlog.yaml \
  --report docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml
```

The validator checks:

- root shape;
- allowed statuses;
- rejected pseudo-statuses such as `deferred`;
- unique `entry_id`;
- known entry types;
- mandatory resolution metadata for `addressed` / `wont_fix`;
- atomic review metadata for deferred-but-still-open entries.

The validator does not modify the backlog.
