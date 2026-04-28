# Constitution neighbor declaration model — specification V0.1

## Purpose

Define the canonical model for declaring, generating, materializing and validating
neighbor read surfaces for bounded `constitution` pipeline runs.

This specification closes PHASE_18 / MACRO_005 by making explicit which artifacts are
sources of authority, which artifacts are generated, and which artifacts are runtime
views derived for a specific run.

## Core principle

Neighbor declarations are **read authority**, not ownership authority.

A neighbor declaration may require an AI stage to read an ID or file before working on
a scope, but it does not transfer ownership of that ID and does not authorize writes
outside the run scope.

## Artifact roles

```yaml
neighbor_declaration_model:
  schema_version: 0.1
  canonical_inputs:
    policy_yaml:
      path: docs/pipelines/constitution/policies/scope_generation/policy.yaml
      role: >-
        Declares shared read-surface defaults, fallback files, external read-only core
        files, and per-scope neighbor files.
      owns:
        - shared_defaults.read_surface
        - declared_scopes[].neighbor_files
        - core_role_classification
        - id_classification_contract
    decisions_yaml:
      path: docs/pipelines/constitution/policies/scope_generation/decisions.yaml
      role: >-
        Declares governed scope assignments, governed logical neighbor IDs, external
        read-only core classification, diagnostic subclusters, and superseded decisions.
      owns:
        - assign_ids_to_scope decisions
        - force_logical_neighbors decisions
        - classify_external_read_only_cores decisions
        - record_diagnostic_subcluster decisions
        - superseded decision traceability
  generated_outputs:
    scope_catalog_manifest:
      path: docs/pipelines/constitution/scope_catalog/manifest.yaml
      role: Generated catalog index. Not manually authoritative.
    scope_definitions:
      path: docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml
      role: >-
        Generated scope definitions containing target IDs and
        default_neighbors_to_read. Not manually authoritative.
  run_materialized_views:
    scope_manifest:
      path: docs/pipelines/constitution/runs/<RUN_ID>/inputs/scope_manifest.yaml
      role: Run-specific writable perimeter derived from the generated scope catalog.
    impact_bundle:
      path: docs/pipelines/constitution/runs/<RUN_ID>/inputs/impact_bundle.yaml
      role: Run-specific mandatory read surface derived from default neighbors and impact rules.
    scope_extract:
      path: docs/pipelines/constitution/runs/<RUN_ID>/inputs/scope_extract.yaml
      role: Derived content view for writable IDs. Not authoritative.
    neighbor_extract:
      path: docs/pipelines/constitution/runs/<RUN_ID>/inputs/neighbor_extract.yaml
      role: Derived content view for mandatory read IDs. Not authoritative.
```

## Canonical neighbor declaration surfaces

### 1. File-level neighbor declarations

Canonical sources:

```yaml
policy_yaml:
  shared_defaults.read_surface.fallback_files: global fallback files
  declared_scopes[].neighbor_files: per-scope default external files
  core_role_classification.external_read_only_core_files: cross-core readable files
```

Semantics:

- `neighbor_files` are read-only files for bounded Constitution runs.
- They are propagated to generated `default_neighbors_to_read.files`.
- They do not authorize cross-core writes.
- Referentiel and Link are external read-only for Constitution runs unless an explicit
  cross-core governed run contract says otherwise.

### 2. ID-level logical neighbor declarations

Canonical sources:

```yaml
decisions_yaml:
  decisions[].decision_type: force_logical_neighbors
  decisions[].status: approved
  decisions[].target_ids: explicit read-neighbor IDs
```

Semantics:

- `force_logical_neighbors` with `status: approved` is the canonical way to force ID-level
  read neighbors into generated scope definitions.
- These IDs are generated into `scope_definitions/*.yaml` under
  `default_neighbors_to_read.ids`.
- Ownership remains with the owner scope of the ID.
- `status` values that are not `approved` must not generate neighbor IDs.

### 3. External read-only core declarations

Canonical source:

```yaml
decisions_yaml:
  decision_type: classify_external_read_only_cores
```

Semantics:

- This is metadata used by validation and interpretation.
- It does not directly add target IDs or neighbor IDs to generated scope definitions.
- It defines which external core IDs can be read without becoming Constitution-owned.

### 4. Diagnostic subcluster declarations

Canonical source:

```yaml
decisions_yaml:
  decision_type: record_diagnostic_subcluster
```

Semantics:

- A diagnostic subcluster is an analysis aid.
- It does not change ownership.
- It does not directly add target IDs or neighbor IDs.
- It can inform future human arbitration.

### 5. Superseded decisions

Canonical source:

```yaml
decisions_yaml:
  status: superseded_by_<phase_or_decision>
  decision_payload.superseded_by_decision_id: <decision_id>
```

Semantics:

- A superseded decision is closed traceability.
- It must not generate target IDs or neighbor IDs.
- It must not appear as an open placeholder in inventory reports.
- It should preserve rationale for why it was superseded.

## Generated representation

The generated representation of neighbor declarations is:

```yaml
scope_definition:
  default_neighbors_to_read:
    files:
      - docs/cores/current/referentiel.yaml
      - docs/cores/current/link.yaml
    ids:
      - REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION
      - ...
```

Rules:

- `default_neighbors_to_read.files` is generated from policy-level neighbor files.
- `default_neighbors_to_read.ids` is generated from approved force-logical-neighbor decisions.
- Generated scope definitions must not be edited manually.
- If generated outputs diverge from policy/decisions, regenerate instead of patching outputs.

## Run materialization representation

During `MATERIALIZE_NEW_RUN`:

```yaml
scope_manifest:
  writable_perimeter.ids: owned scope IDs

impact_bundle:
  mandatory_reads.ids: generated neighbor IDs and additional gated reads

scope_extract:
  target_ids: scope_manifest.writable_perimeter.ids

neighbor_extract:
  target_ids: impact_bundle.mandatory_reads.ids
```

Rules:

- `scope_extract.yaml` is a derived content view of writable IDs.
- `neighbor_extract.yaml` is a derived content view of mandatory read IDs.
- Missing IDs must be explicit and trigger bounded fallback reads.
- Extracts are preferred over full-core reads for AI stages, but they are not new sources of truth.

## Mutation rules

```yaml
mutation_rules:
  policy_yaml:
    may_change:
      - read surface defaults
      - per-scope neighbor files
      - external core classification contract
    change_gate: explicit human-governed policy patch
  decisions_yaml:
    may_change:
      - assign_ids_to_scope
      - force_logical_neighbors
      - classify_external_read_only_cores
      - record_diagnostic_subcluster
      - superseded decision metadata
    change_gate: explicit human-governed decisions patch
  scope_catalog:
    may_change: generated only
    change_gate: generate_constitution_scopes.py --apply
  run_extracts:
    may_change: generated only
    change_gate: materialize/extract scripts during run bootstrap or reconciliation
```

## Validation expectations

Inventory validation should report `PASS` when:

- `pipeline.md` references current canonical scripts;
- `STAGE_00` references score publication and neighbor IDs governance;
- no non-approved, non-superseded `force_logical_neighbors` placeholder remains open;
- generated scope definitions contain the expected `default_neighbors_to_read` surface;
- external read-only cores are declared explicitly.

A remaining open finding is allowed only when it is intentionally governed as a future
arbitration item and is not silently treated as generated authority.

## Accepted PHASE_18 decisions

```yaml
accepted_decisions:
  - decision_id: PHASE_18_DECISION_001
    decision: pipeline.md must list the recent STAGE_00 scoring and neighbor-governance scripts.
    status: done
  - decision_id: PHASE_18_DECISION_002
    decision: SGEN_DECISION_011 is superseded by PHASE_16 exact neighbor arbitration.
    status: done
  - decision_id: PHASE_18_DECISION_003
    decision: default_neighbors_to_read is the generated catalog surface for neighbor declarations.
    status: accepted
  - decision_id: PHASE_18_DECISION_004
    decision: scope_extract and neighbor_extract are derived run views, not canonical declaration surfaces.
    status: accepted
```

## Handoff to MACRO_004

After this model is accepted, `MACRO_004_MULTI_OWNER_CLUSTER_REVIEW` can proceed with a cleaner
foundation:

- ownership review is separate from read-neighbor review;
- diagnostic subclusters do not imply ownership changes;
- generated default neighbors do not imply ownership transfer;
- any proposed multi-owner exception must be explicit, not inferred from read dependencies.
