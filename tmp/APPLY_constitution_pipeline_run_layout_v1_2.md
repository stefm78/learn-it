# Apply — constitution pipeline run-aware v1.2

Depuis la racine du repo, reconstituer puis remplacer `docs/pipelines/constitution/pipeline.md` avec :

```bash
cat \
  ./tmp/constitution_pipeline_run_layout_v1_2/01_header_to_resolution.md \
  ./tmp/constitution_pipeline_run_layout_v1_2/02_stage03_to_stage06.md \
  ./tmp/constitution_pipeline_run_layout_v1_2/03_stage07_to_end.md \
  > ./docs/pipelines/constitution/pipeline.md
```

Puis vérifier le diff :

```bash
git diff -- docs/pipelines/constitution/pipeline.md docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
```

Objectif de ce remplacement :
- rendre le pipeline `constitution` réellement compatible avec un `run_id` ;
- faire du layout `runs/<run_id>/...` l'unité primaire d'exécution des runs bornés ;
- conserver le layout plat historique comme régime nominal global et comme transition bornée seulement ;
- préparer la dépréciation progressive du layout plat pour les runs bornés.

Après application du remplacement, la prochaine action recommandée est :
- synchroniser les fichiers de suivi centraux ;
- puis adapter les chemins d'exécution réels d'un premier run vers `runs/<run_id>/work/...`.
