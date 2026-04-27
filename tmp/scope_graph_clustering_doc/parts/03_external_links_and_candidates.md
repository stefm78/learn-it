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
