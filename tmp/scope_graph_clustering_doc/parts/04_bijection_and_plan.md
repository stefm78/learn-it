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
