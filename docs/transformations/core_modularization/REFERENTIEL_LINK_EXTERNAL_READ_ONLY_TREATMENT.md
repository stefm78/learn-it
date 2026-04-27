# Referentiel and Link treatment in Constitution scoping

Status: draft clarification
Related transformation: `SCOPE_GRAPH_CLUSTERING_APPROACH.md`
Pipeline concerned first: `constitution`

## 1. Decision

For the Constitution challenge/scoping pipeline, `referentiel` and `link` are treated as external read-only cores.

This means:

```text
constitution pipeline may read referentiel/link
constitution pipeline may depend on referentiel/link IDs
constitution pipeline may declare referentiel/link IDs as neighbors
constitution pipeline must not directly patch referentiel.yaml or link.yaml
```

## 2. Rationale

The graph analysis showed that many `referentiel` and `link` IDs are currently `UNOWNED` by the Constitution scope catalog.

This should not be fixed by forcing those IDs into Constitution scopes.

The three cores have different roles:

```text
constitution = governance and invariant/rule ownership
referentiel  = parameters, operational references, calibration tables
link         = inter-core bindings and separation layer
```

A Constitution bounded run should not silently become a cross-core run.

## 3. Consequence for future tasks

The Scope Lab must include explicit follow-up work for `referentiel` and `link`.

Required work items:

```text
1. classify referentiel/link IDs as external_read_only for Constitution scoping
2. define how referentiel/link IDs are represented in the bijection validator
3. define how Constitution scopes declare referentiel/link neighbors
4. define how requested changes to referentiel/link are emitted as backlog or cross-core change requests
5. decide whether separate referentiel/link scoping pipelines are needed
```

## 4. Allowed behavior in Constitution challenge runs

Allowed:

```text
read referentiel.yaml
read link.yaml
include referentiel/link IDs in neighbor extracts
raise candidate_node or candidate_edge requests
raise cross_core_change_request items
raise backlog items for referentiel/link evolution
```

Forbidden by default:

```text
write docs/cores/current/referentiel.yaml
write docs/cores/current/link.yaml
move referentiel/link IDs into Constitution scope ownership
modify generated scope catalog files directly
```

## 5. Exception rule

A Constitution run may modify `referentiel` or `link` only if it is explicitly reclassified as a cross-core governed run.

Such a run must declare:

```text
expanded write surface
cross-core ownership rules
specific validation gates
full reconstruction of constitution/referentiel/link
release and promotion impact
```

Without that explicit contract, `referentiel` and `link` remain read-only external cores.

## 6. Impact on the implementation plan

This clarification adds explicit work to PHASE_09 and PHASE_11.

### PHASE_09 impact

The canonicalization plan must not only update Constitution scope decisions. It must also define how external read-only IDs are classified.

Expected outputs may include:

```text
scope_generation policy update
scope_generation decisions update
cross_core_change_request format
referentiel/link external_read_only classification
```

### PHASE_11 impact

The bijection validator must distinguish at least:

```text
constitution_owned
external_read_only_referentiel
external_read_only_link
shared_or_global
missing_or_invalid
```

A valid Constitution scope partition should not fail merely because `referentiel` or `link` IDs are not owned by Constitution scopes.

It should fail only if those IDs are neither owned nor explicitly classified.

## 7. Open decisions

```yaml
open_decisions:
  - decision_id: RL_001
    question: Should referentiel/link have their own scope catalog family?
    status: pending

  - decision_id: RL_002
    question: Should external_read_only IDs be excluded from ownership bijection or included with a distinct classification?
    status: pending

  - decision_id: RL_003
    question: Should cross-core change requests become a formal artifact of the Constitution pipeline?
    status: pending

  - decision_id: RL_004
    question: Should a dedicated referentiel/link pipeline be introduced before serious bounded Constitution runs?
    status: pending
```
