# Apply — scoped constitution pipeline v1.1

Depuis la racine du repo, reconstituer puis remplacer `docs/pipelines/constitution/pipeline.md` avec :

```bash
cat \
  ./tmp/constitution_pipeline_scoped_v1_1/01_header_to_stage03.md \
  ./tmp/constitution_pipeline_scoped_v1_1/02_stage04_to_stage06.md \
  ./tmp/constitution_pipeline_scoped_v1_1/03_stage07_to_end.md \
  > ./docs/pipelines/constitution/pipeline.md
```

Puis vérifier le diff :

```bash
git diff -- docs/pipelines/constitution/pipeline.md
```

Objectif de ce remplacement :
- introduire un mode `bounded_local_run` dans le pipeline `constitution` ;
- ajouter les artefacts de scope (`scope_manifest`, `impact_bundle`, `integration_gate`) ;
- conserver le flux nominal historique quand aucun scope n'est fourni ;
- bloquer toute promotion implicite d'un succès local.

Après application du remplacement, la prochaine action recommandée est :
- mettre à jour `docs/transformations/core_modularization/STATUS.yaml` ;
- ajouter une nouvelle entrée dans `docs/transformations/core_modularization/WORKLOG.md` ;
- puis ajuster les prompts `Challenge_constitution.md` et `Make04ConstitutionArbitrage.md` pour prendre en charge le mode borné.
