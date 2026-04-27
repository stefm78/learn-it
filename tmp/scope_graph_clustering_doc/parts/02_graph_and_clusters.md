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
