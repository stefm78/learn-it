# Constitution scope evolution preview

## Purpose

`scope_evolution_preview.yaml` is a pre-release diagnostic report produced at
`STAGE_06_CORE_VALIDATION`.

It complements the final `scope_evolution_score.yaml` produced at `STAGE_09_CLOSEOUT_AND_ARCHIVE`.

## Position in the pipeline

```text
MATERIALIZE_NEW_RUN
  └─ baseline_scope_state.yaml

STAGE_06_CORE_VALIDATION
  ├─ core_validation.yaml
  └─ scope_evolution_preview.yaml

STAGE_07_RELEASE_MATERIALIZATION
  └─ build_release_plan.py remains authoritative for material release_required

STAGE_09_CLOSEOUT_AND_ARCHIVE
  └─ scope_evolution_score.yaml
```

## Questions answered

The preview answers:

- What was the scope state before STAGE_01?
- What is proved after the sandbox patch and core validation?
- Is it reasonable to proceed to STAGE_07?
- Is the expected progress mainly operational or structural?
- Is backlog pressure increasing before closeout?

## Non-goals

The preview does not:

- update maturity in `policy.yaml`;
- update `decisions.yaml`;
- write Core files;
- materialize or promote release bundles;
- replace `build_release_plan.py`.

## Release relationship

`scope_evolution_preview.yaml` can recommend `proceed_to_stage_07_release_plan`, but it cannot itself declare `release_required: true`.

The material release decision remains owned by:

```text
docs/patcher/shared/build_release_plan.py
```

The conceptual distinction is:

```text
release_required = is there a material artifact change to publish?
scope_evolution_preview = does the validated sandbox change appear useful enough to proceed toward release?
```
