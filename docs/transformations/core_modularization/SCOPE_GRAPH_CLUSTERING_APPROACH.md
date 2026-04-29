# Scope graph clustering approach

Status: compact implemented approach note  
Pipeline: `constitution`  
Scope: core modularization / scope partitioning  
Full historical snapshot: `archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_APPROACH_FULL_2026_04_29.md`

## Purpose

This document is the compact doctrine for graph-based scope modularization.

The previous long-form approach note is preserved verbatim in:

```text
docs/transformations/core_modularization/archive/full_snapshots/SCOPE_GRAPH_CLUSTERING_APPROACH_FULL_2026_04_29.md
```

Snapshot integrity:

```yaml
archived_full_approach_sha256: 1a92e334eeb94768cbb3e4d05bd7cd9916e45f1cb4d78f380fb44e42842ef275
```

## Core doctrine

```yaml
doctrine:
  canonical_scope_partition: governed ownership model
  graph_cluster_analysis: diagnostic_and_validation_model
  generated_scope_catalog: generated_output_not_source_of_truth
  human_arbitration_required: true
```

The graph can discover natural clusters, boundary pressure, missing dependencies,
candidate nodes, candidate edges and reconstruction risks. It must not publish
canonical scope changes directly.

## Authoritative inputs and generated outputs

```yaml
canonical_inputs:
  cores:
    - docs/cores/current/constitution.yaml
    - docs/cores/current/referentiel.yaml
    - docs/cores/current/link.yaml
  scope_generation:
    - docs/pipelines/constitution/policies/scope_generation/policy.yaml
    - docs/pipelines/constitution/policies/scope_generation/decisions.yaml

generated_outputs:
  scope_catalog:
    - docs/pipelines/constitution/scope_catalog/manifest.yaml
    - docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml
```

## Ownership vs dependency

```yaml
ownership_closure:
  rule: every canonical owned ID must have exactly one owner scope unless explicitly classified otherwise
  write_perimeter: target.ids

dependency_closure:
  rule: read dependencies may cross scope boundaries if declared explicitly
  read_perimeter: default_neighbors_to_read
```

A scope can be:

```text
write-closed
read-open
```

## Canonicalization flow

```yaml
canonicalization_flow:
  - record candidate in Scope Lab or backlog report
  - arbitrate as accept/reject/backlog/wont_fix
  - patch governed inputs or canonical cores only through approved path
  - regenerate scope catalog deterministically
  - validate ownership bijection
  - validate full reconstruction
  - validate scope and neighbor extracts
  - only then open serious bounded local runs
```

## Validation gates

```yaml
required_gates:
  - ownership_bijection
  - neighbor_validation
  - normalized_structural_reconstruction
  - scope_extract_validation
  - neighbor_extract_validation
  - governance_backlog_lifecycle_validation
  - bounded_run_preflight_when_backlog_impacts_scope
```

## Current implemented state

```yaml
implemented_state:
  scope_catalog_regenerated: true
  bijection_validation_passed: true
  reconstruction_validation_passed: true
  patch_lifecycle_pilot_run_passed: true
  pilot_release_promoted: CORE_RELEASE_2026_04_28_R01
  governance_backlog_integrated: true
  maturity_scoring_publishable: true
  neighbor_declaration_model_stabilized: true
  multi_owner_review_completed: true
  bounded_run_preflight_integrated: true
```

## Active companion docs

```text
docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_PROGRESS.md
docs/transformations/core_modularization/HANDOVER_SCOPE_MODULARIZATION_POST_PILOT.md
docs/transformations/core_modularization/REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md
docs/specs/constitution_scope_maturity_scoring.md
docs/specs/constitution_neighbor_declaration_model.md
docs/specs/constitution_governance_backlog_lifecycle.md
```

## Non-goals

```yaml
non_goals:
  - direct edits to generated scope definitions as authority
  - silent cross-core reallocation
  - graph candidates becoming canonical without arbitration
  - requiring every dependency to live inside the same scope
  - replacing human semantic judgment with automatic clustering
  - validating partition without reconstruction
```
