# PHASE_03 — Graph extraction summary

Status: PASS  
Generated from: `tmp/scope_lab/constitution_graph_report.yaml`  
Scope Lab phase: full graph extraction

## Result

The first graph extraction succeeded.

```yaml
node_count: 246
edge_count: 402
missing_target_edge_count: 0
duplicate_node_id_count: 0
status: PASS
```

## Node distribution

```yaml
nodes_by_core:
  constitution: 118
  referentiel: 112
  link: 16

nodes_by_owner_scope:
  UNOWNED: 131
  deployment_governance: 19
  knowledge_and_design: 20
  learner_state: 26
  mastery_evaluation: 29
  patch_lifecycle: 21
```

## Edge distribution

```yaml
edges_by_classification:
  internal_scope_edge: 167
  cross_scope_edge: 27
  unowned_or_unscoped_edge: 208
```

## First interpretation

The extraction is structurally healthy:

- no missing target ID was detected;
- no duplicate graph node ID was detected;
- explicit relations and dependencies can be used as a basis for clustering.

The large `UNOWNED` area is expected but important. Current generated constitution scopes mostly own Constitution IDs. The future bijection validator must therefore explicitly decide how `referentiel` and `link` IDs are owned, shared, or classified.

## Boundary pressure signals

The strongest visible cross-scope pairs are:

```yaml
- learner_state -> patch_lifecycle: 4
- patch_lifecycle -> learner_state: 4
- deployment_governance -> knowledge_and_design: 3
- deployment_governance -> mastery_evaluation: 3
- mastery_evaluation -> knowledge_and_design: 3
```

The `learner_state` / `patch_lifecycle` reciprocal pressure confirms that `patch_lifecycle` is a good stress-test scope for the next phases.

## Next phase

Proceed to PHASE_04:

```text
natural_cluster_detection
```

Expected next artifact:

```text
tmp/scope_lab/constitution_graph_clusters.yaml
```
