# AI skill governance patterns

Status: design note  
Branch: `feat/core-modularization-bootstrap`  
Scope: `core_modularization` transformation  
Canonical status: non-canonical reference note

## Purpose

This note preserves governance ideas observed from the `garrytan/gstack` skill model and translates them into the `learn-it` context.

The goal is not to adopt gstack directly. The goal is to keep the useful patterns for future hardening of `learn-it` AI workflows, especially long-running sessions, handover, bounded edits, stage routing, and mutation authorization.

This document is a design note only. It does not authorize core mutation, release promotion, referentiel/link mutation, or pipeline execution.

## Simple principle

A coding agent should not just receive a prompt and improvise.

For `learn-it`, the agent should know:

- where it is allowed to read;
- where it is allowed to write;
- which pipeline contract applies;
- which facts are observed;
- which conclusions are inferred;
- which actions require human authorization;
- which deterministic scripts provide proof.

## Pattern 1 — Context save

A context save is a structured handover file.

It should preserve the working state when a session is long, compacted, or handed to another AI session.

It should not be treated as a commit and should not be treated as deterministic proof.

Recommended `learn-it` fields:

```yaml
observed_state:
  branch: feat/core-modularization-bootstrap
  git_status: unknown
  active_run: none
  current_phase: NO_ACTIVE_PHASE

verified_by_script:
  - script: docs/patcher/shared/example_validator.py
    report: docs/registry/reports/example_report.yaml
    status: PASS

inferred_context:
  current_goal: preserve AI workflow governance ideas
  likely_next_steps:
    - decide whether to formalize these patterns into a contract

human_decisions_required:
  - whether these ideas become a new spec, a pipeline extension, or remain notes

forbidden_without_gate:
  - mutate docs/cores/current
  - promote a core release
  - mutate referentiel/link
  - open a new Constitution run outside OPEN_NEW_RUN
```

Key rule: separate facts from inference.

## Pattern 2 — Context restore

A context restore reads the latest saved state and lets a new session resume without reconstructing everything from chat history.

For `learn-it`, restore should answer in plain terms:

```text
Where are we?
What is verified?
What is only inferred?
What is blocked?
What is the next allowed action?
```

A restore flow should prefer repo artifacts over conversation memory.

Candidate read order:

1. active handover document;
2. active transformation README;
3. compact progress tracker;
4. relevant pipeline signals;
5. latest deterministic reports;
6. saved context files, if present.

## Pattern 3 — Skill routing

Skill routing means mapping a user phrase to a governed contract instead of letting the AI choose freely.

Example mappings for `learn-it`:

```yaml
routing:
  "sync, continue": CONTINUE_ACTIVE_TRANSFORMATION
  "handover": CONTEXT_SAVE
  "resume": CONTEXT_RESTORE
  "open new run": OPEN_NEW_RUN
  "stage00": STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN
  "mutation réelle": CROSS_CORE_MUTATION_GATE
  "promote current": STAGE_08_PROMOTE_CURRENT
```

This is close to the role already played by `AI_PROTOCOL.yaml` and entry action contracts.

The routing rule should be conservative: when in doubt, inspect and stop before mutation.

## Pattern 4 — Freeze scope

A freeze scope limits edits to a declared directory or file set.

For `learn-it`, this is useful because the repository contains sensitive areas that should not be modified incidentally.

Examples:

```text
Allowed write scope:
docs/transformations/core_modularization/

Forbidden unless explicitly authorized:
docs/cores/current/
docs/cores/releases/
docs/pipelines/constitution/scope_catalog/
docs/pipelines/constitution/governance_backlog.yaml
```

Freeze should block accidental edits. It is not enough to merely warn.

A weaker initial implementation can be procedural: every stage contract declares `allowed_writes` and the AI must report a violation instead of writing.

A stronger implementation can add tool hooks or deterministic preflight checks.

## Pattern 5 — Guard mode

Guard mode is freeze scope plus destructive-command caution.

It is appropriate before sensitive phases such as:

- applying a patch;
- materializing a release;
- promoting current;
- mutating cross-core contracts;
- touching referentiel/link;
- running cleanup operations.

For `learn-it`, guard mode should make the AI state:

```yaml
guard_mode:
  allowed_writes:
    - path/or/glob
  destructive_commands: warn_or_block
  core_mutation_authorized: false
  promotion_authorized: false
  cross_core_mutation_authorized: false
```

## Pattern 6 — Multi-review autoplan

An autoplan is not just a plan generator. It is a plan passed through several review lenses.

For `learn-it`, useful reviewers would be:

```yaml
reviewers:
  scope_reviewer: checks that the work is bounded
  protocol_reviewer: checks entry action and pipeline contract
  proof_reviewer: checks required deterministic scripts and reports
  mutation_reviewer: checks whether mutation is authorized
  backlog_reviewer: checks referentiel/link or cross-core open items
  release_reviewer: checks release and promotion impact
```

Only unresolved decisions should be escalated to the human.

## Pattern 7 — Structured human decisions

When a human decision is needed, the question should be explicit and bounded.

Bad:

```text
Do you want to continue?
```

Good:

```text
D1 — Should we authorize a real cross-core mutation now?
Context: the generic pipeline is ready, but no concrete request is authorized.
Recommendation: no, prepare a concrete change request first.
Default: 1
Options:
1. Keep mutation blocked and prepare a concrete request.
2. Authorize a real mutation now.
3. Keep the item in backlog until the next release gate.
Risk if wrong: a core or downstream contract may change without sufficient proof.
```

This matches the existing `learn-it` preference for numbered choices and default answers.

## Pattern 8 — Learnings memory

A learning is a reusable rule discovered across sessions.

It is not a proof and it is not a current-state report.

Examples:

```yaml
learned_rules:
  - Do not claim a deterministic script was executed unless the user actually ran it.
  - Normalize Windows paths to POSIX-style paths in YAML reports.
  - STAGE_00 is not allowed while an active Constitution run exists.
  - Referentiel and Link are read-only external cores during bounded Constitution runs.
  - Cross-core mutation requires explicit human authorization and passing gates.
```

Potential future location:

```text
docs/registry/ai_learnings.yaml
```

or, if transformation-local:

```text
docs/transformations/core_modularization/AI_LEARNINGS.md
```

## Pattern 9 — Avoid automatic WIP commits for governed pipelines

Continuous checkpoints can be useful in normal software development, but they are risky for `learn-it` because the repository distinguishes:

- AI notes;
- deterministic proof;
- validation reports;
- human decisions;
- core mutations;
- release promotion.

Recommendation: prefer explicit context saves and human-reviewed commits.

Do not introduce automatic WIP commits into governed pipeline phases until the commit semantics are formally specified.

## Pattern 10 — Generated runtime prompts from canonical contracts

A useful pattern is:

```text
canonical contract -> generated runtime prompt -> execution report -> validation report
```

For `learn-it`, this means the YAML contract remains authoritative and any AI prompt should be a generated or derived runtime artifact, not a second source of truth.

Candidate examples:

```text
OPEN_NEW_RUN.action.yaml
  -> generated OPEN_NEW_RUN runtime prompt
  -> entry_decision_report.yaml

STAGE_05_APPLY.skill.yaml
  -> generated stage execution prompt
  -> patch_execution_report.yaml
  -> validation report
```

## Pattern 11 — Four-way separation

The central hardening idea is to separate four categories:

```yaml
observed:
  meaning: directly read from repo, git, or report files

verified_by_script:
  meaning: produced by deterministic script output

inferred:
  meaning: AI interpretation or recommendation

authorized:
  meaning: explicit human or pipeline permission to mutate
```

A future context-save or handover format should not collapse these categories.

## Pattern 12 — Minimal candidate skill set for learn-it

A future `learn-it` skill layer could start with a small set:

```text
/lt-context-save
/lt-context-restore
/lt-entry-action
/lt-stage-run
/lt-freeze-scope
/lt-guard
/lt-handover
/lt-learn
```

Each skill should be bound to existing repo contracts rather than inventing new behavior.

## Recommended next step

Keep this as a design note until a human explicitly decides one of the following:

1. turn the ideas into a formal spec under `docs/specs/`;
2. integrate part of them into `AI_PROTOCOL.yaml`;
3. create a dedicated context-save/context-restore contract;
4. leave them as transformation-local notes.

Default recommendation: keep as transformation-local reference for now.

## Non-goals

This note does not:

- install gstack;
- add runtime hooks;
- modify pipeline behavior;
- change `AI_PROTOCOL.yaml`;
- authorize mutation;
- create or close a run;
- update any core current or release artifact.
