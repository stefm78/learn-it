# Apply — constitution scope catalog V0.2

Depuis la racine du repo, remplacer le manifeste du catalogue de scopes par la version étendue V0.2 :

```bash
cp ./tmp/constitution_scope_catalog_manifest_v0_2.yaml ./docs/pipelines/constitution/scope_catalog/manifest.yaml
```

Puis vérifier :

```bash
git diff -- \
  ./docs/pipelines/constitution/scope_catalog/manifest.yaml \
  ./docs/pipelines/constitution/scope_catalog/scope_definitions/mastery_model.yaml \
  ./docs/pipelines/constitution/scope_catalog/scope_definitions/knowledge_graph.yaml
```

Effet attendu :
- le catalogue `constitution` publie désormais trois scopes :
  - `learner_state`
  - `mastery_model`
  - `knowledge_graph`
- le launcher peut proposer un vrai `new_run` sur un autre scope publié.
