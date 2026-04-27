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
