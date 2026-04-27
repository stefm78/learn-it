# Scope graph clustering approach

Status: draft implementation note  
Pipeline: `constitution`  
Scope: core modularization / scope partitioning

## 1. Purpose

This document captures the intended approach for redesigning and validating the scoping of the Learn-It Constitution using a graph-based clustering analysis.

The goal is not to replace human semantic arbitration with automatic clustering. The goal is to use the graph as a diagnostic and validation instrument to discover natural clusters, boundary pressure, missing dependencies, candidate nodes, candidate links, and reconstruction risks before publishing a canonical scope catalog.

The target outcome is a scope partition that is:

- semantically understandable by a human;
- coherent with the real dependency graph of the canonical cores;
- compatible with bounded local runs;
- reproducible through deterministic generation;
- validated as a bijection over the canonical `constitution`, `referentiel`, and `link` cores.

## 2. Context

The current scoping model is based on governed scope generation inputs:

- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`

The generated outputs are:

- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml`

The canonical source of truth remains:

- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

The scope catalog must remain a generated artifact. It must not become a second source of truth.

Current test runs may be interrupted or destroyed while the correct scoping approach is still being designed. They must not force the scope partition to remain stable if the project is still in a scope-design phase.

## 3. Core principle

The graph-based approach distinguishes two layers:

```text
canonical scope partition = governed ownership model
cluster graph analysis    = diagnostic, discovery, and validation model
```

The graph may suggest new scopes, new neighbors, missing nodes, missing links, or boundary changes. It does not publish them directly.

All canonical changes must go through explicit decisions, patches, deterministic regeneration, and validation.

## 4. Graph model

### 4.1 Nodes

Each canonical entry with an ID becomes a graph node.

Sources:

- `constitution.yaml`
- `referentiel.yaml`
- `link.yaml`

Candidate sections include, at minimum:

- `SYSTEM`
- `TYPES`
- `INVARIANTS`
- `RULES`
- `PARAMETERS`
- `CONSTRAINTS`
- `EVENTS`
- `ACTIONS`
- inter-core references and bindings where represented as ID-bearing entries

A node should carry metadata such as:

```yaml
node:
  id: RULE_EXAMPLE
  source_core: constitution
  source_section: RULES
  current_owner_scope: patch_lifecycle
  logic_scope: patch_layer
  raw_entry_fingerprint: <normalized_entry_hash>
```

### 4.2 Edges

Edges represent explicit dependencies or relations between nodes.

Initial edge sources:

- `depends_on`
- `relations.target`
- `relations.source` where applicable
- explicit inter-core bindings
- explicit references already represented in the canonical YAML

An edge should carry metadata such as:

```yaml
edge:
  source: RULE_EXAMPLE
  target: INV_EXAMPLE
  edge_type: depends_on
  source_core: constitution
  target_core: constitution
  source_scope: patch_lifecycle
  target_scope: patch_lifecycle
  status: canonical
```

## 5. Cluster model

A cluster is a candidate coherent group discovered from the graph.

A cluster is not automatically a canonical scope.

A cluster report should include:

```yaml
cluster:
  cluster_id: GRAPH_CLUSTER_001
  node_ids: []
  dominant_current_scope: patch_lifecycle
  internal_edge_count: 0
  external_edge_count: 0
  incoming_edge_count: 0
  outgoing_edge_count: 0
  bridge_nodes: []
  boundary_pressure: low|medium|high
  candidate_label: patch_structure_and_quality
  recommendation: keep|split|merge|declare_neighbors|review
```

The clustering analysis should support at least:

- connected components;
- weakly connected components for directed graphs;
- strongly connected components where meaningful;
- bridge nodes;
- bridge edges;
- internal density;
- incoming and outgoing boundary pressure;
- dominant current scope ratio.

Advanced algorithms may be added later, but the first implementation should remain deterministic and explainable.

## 6. Ownership closure vs dependency closure

The partition must distinguish ownership from read dependency.

### 6.1 Ownership closure

Ownership must be strict.

Each canonical ID must be either:

- owned by exactly one canonical scope; or
- explicitly classified as a shared/global/non-owned construct by policy, if such a category is introduced.

A canonical ID must never be silently unowned or owned by multiple scopes.

### 6.2 Dependency closure

Dependency closure may be open, but it must be explicit.

A scope may depend on nodes outside its owned cluster. In that case, the external nodes must be declared as neighbors, not silently copied into the scope.

```text
target.ids                 = owned write perimeter
default_neighbors_to_read  = explicit read perimeter
```

This means a cluster can be:

```text
write-closed
read-open
```

## 7. Handling links to nodes outside a cluster

A link from a node inside a cluster to a node outside the cluster is allowed, but it must be classified.

Expected classifications:

```text
internal_edge
  source and target are both inside the cluster.

outgoing_neighbor_edge
  source is inside the cluster, target is outside and must be read as a neighbor.

incoming_neighbor_edge
  source is outside the cluster, target is inside and may indicate another scope depends on this cluster.

bridge_edge
  edge is structurally important enough to question the boundary.

missing_target_edge
  target ID is referenced but not found in constitution/referentiel/link.

candidate_edge
  edge is not yet canonical but appears necessary based on semantic or structural analysis.
```

Example:

```yaml
cluster_closure:
  cluster_id: GRAPH_CLUSTER_PATCH_TRIGGER
  owned_candidate_ids:
    - RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH
    - EVENT_PERSISTENT_LOW_VC
    - ACTION_TRIGGER_RELEVANCE_PATCH
  outgoing_neighbor_edges:
    - source: RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH
      target: TYPE_STATE_AXIS_VALUE_COST
      target_scope: learner_state
      recommendation: declare_neighbor
  missing_target_edges: []
  candidate_edges:
    - source: RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH
      target: INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION
      recommendation: discuss_add_depends_on
```

## 8. Candidate nodes and candidate links

The graph analysis may reveal that a missing concept or missing relation should exist.

This is allowed in the Scope Lab, but candidate nodes and candidate links must not become canonical automatically.

### 8.1 Candidate node

A candidate node represents a concept that appears necessary but is not yet present in the canonical cores.

```yaml
candidate_node:
  candidate_id: CAND_NODE_PATCH_TRIGGER_GOVERNANCE
  proposed_core: constitution
  proposed_section: TYPES
  proposed_id: TYPE_PATCH_TRIGGER_GOVERNANCE
  rationale: >-
    Several patch lifecycle rules implicitly rely on a governed trigger concept,
    but no canonical TYPE currently represents it.
  status: proposed
```

### 8.2 Candidate edge

A candidate edge represents a dependency or relation that appears necessary but is not yet declared canonically.

```yaml
candidate_edge:
  candidate_id: CAND_EDGE_RULE_A_TO_INV_B
  source: RULE_A
  target: INV_B
  edge_type: depends_on
  rationale: >-
    RULE_A appears to operationalize INV_B, but the dependency is not explicit.
  status: proposed
```

Candidate nodes and edges must be arbitrated by a human before canonicalization.

## 9. Canonicalization flow for new nodes and links

If the Scope Lab proposes new nodes or links, the canonicalization flow is:

1. record the candidate in a Scope Lab report;
2. arbitrate the candidate as `accept`, `reject`, `defer`, or `backlog`;
3. if accepted, patch the relevant canonical core file;
4. update `scope_generation/decisions.yaml` to assign ownership or neighbor status;
5. regenerate the scope catalog deterministically;
6. validate ownership bijection;
7. validate full reconstruction of `constitution`, `referentiel`, and `link`;
8. only then allow serious bounded local runs.

A candidate must never be added directly to a generated `scope_extract`, `neighbor_extract`, or scope catalog file without being added to the canonical source of truth.

## 10. Bijection and full reconstruction gate

The scope partition must pass a blocking bijection gate before it can be considered valid.

### 10.1 Ownership bijection

The validation must check:

- every canonical ID is owned exactly once, unless explicitly classified otherwise by policy;
- no canonical ID is owned by multiple scopes;
- no scope owns an ID absent from the canonical cores;
- no neighbor points to an ID absent from the canonical cores;
- shared or forced-neighbor cases are explicit and traceable.

### 10.2 Full reconstruction

The validation must prove that the union of the published partition can reconstruct the three canonical cores structurally:

- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

The comparison should be structural rather than byte-for-byte. YAML formatting, ordering, and comments may differ, but normalized content must match.

Expected validation artifact:

```yaml
scope_partition_bijection_validation:
  status: PASS|FAIL
  ownership_bijection:
    status: PASS|FAIL
    missing_owned_ids: []
    duplicate_owned_ids: []
    extra_owned_ids_not_in_canon: []
  neighbor_validation:
    status: PASS|FAIL
    neighbor_ids_not_in_canon: []
    neighbor_ids_without_owner: []
  recomposition:
    status: PASS|FAIL
    constitution:
      status: PASS|FAIL
      source_normalized_fingerprint: <hash>
      reconstructed_normalized_fingerprint: <hash>
    referentiel:
      status: PASS|FAIL
      source_normalized_fingerprint: <hash>
      reconstructed_normalized_fingerprint: <hash>
    link:
      status: PASS|FAIL
      source_normalized_fingerprint: <hash>
      reconstructed_normalized_fingerprint: <hash>
  blocking_findings: []
  warnings: []
```

## 11. Proposed implementation plan

1. Stop, abandon, or purge disposable test runs.
2. Free Stage 00 or the Scope Lab from disposable run constraints.
3. Create `tmp/scope_lab/`.
4. Build a full graph from `constitution`, `referentiel`, and `link`.
5. Detect natural graph clusters.
6. Analyze cluster closure: internal edges, outgoing neighbors, incoming dependencies, missing targets, candidate nodes, and candidate edges.
7. Compare clusters with the current canonical scopes.
8. Produce explicit redesign candidates.
9. Record human arbitration.
10. Patch canonical cores and scope generation inputs if needed.
11. Regenerate the scope catalog deterministically.
12. Validate ownership bijection and full reconstruction.
13. Validate scope and neighbor extracts.
14. Relaunch one serious pilot bounded local run.

Recommended first stress-test scope:

```text
patch_lifecycle
```

because it is likely the most transverse and boundary-sensitive scope.

## 12. Required scripts to implement or evolve

Existing scripts to reuse:

- `docs/patcher/shared/analyze_constitution_scope_partition.py`
- `docs/patcher/shared/generate_constitution_scopes.py`
- `docs/patcher/shared/extract_scope_slice.py`

Experimental scripts proposed first:

```text
tmp/analyze_constitution_dependency_graph.py
tmp/validate_scope_partition_bijection.py
```

Promote later when stable:

```text
docs/patcher/shared/analyze_constitution_dependency_graph.py
docs/patcher/shared/validate_scope_partition_bijection.py
```

## 13. Open design decisions

- Should shared/global IDs be allowed, or should every canonical ID have exactly one owner?
- Should forced neighbors be allowed without ownership by another scope?
- Should candidate nodes and candidate edges be stored in a dedicated backlog artifact?
- Should Stage 00 distinguish `canonical` active runs from `experimental` active runs?
- Should `link.yaml` be treated as a first-class graph source or only as cross-core metadata?
- Should cluster labels be deterministic, human-assigned, or both?

## 14. Tracking checklist

```yaml
implementation_tracking:
  scope_lab_workspace_created: false
  disposable_runs_cleaned_or_abandoned: false
  full_graph_script_created: false
  graph_nodes_edges_generated: false
  cluster_detection_generated: false
  cluster_closure_report_generated: false
  scope_alignment_report_generated: false
  redesign_candidates_generated: false
  human_arbitration_recorded: false
  canonical_core_patches_applied_if_needed: false
  scope_generation_decisions_updated: false
  scope_catalog_regenerated: false
  bijection_validator_created: false
  ownership_bijection_passed: false
  full_reconstruction_passed: false
  extract_tests_passed: false
  pilot_bounded_local_run_opened: false
```

## 15. Non-goals

This approach does not:

- allow direct edits to generated scope definitions as source of truth;
- allow silent cross-core reallocation;
- allow graph candidates to become canonical without arbitration;
- require every dependency to be inside the same scope;
- replace human semantic judgment with automatic clustering;
- validate a scope partition without reconstructing `constitution`, `referentiel`, and `link`.
