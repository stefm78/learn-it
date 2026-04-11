# Apply — constitution run-aware pipeline + first run bootstrap

Depuis la racine du repo, appliquer les changements préparés et initialiser le premier run avec les commandes suivantes.

## 1. Remplacer `docs/pipelines/constitution/pipeline.md`

```bash
cat \
  ./tmp/constitution_pipeline_run_layout_v1_2/01_header_to_resolution.md \
  ./tmp/constitution_pipeline_run_layout_v1_2/02_stage03_to_stage06.md \
  ./tmp/constitution_pipeline_run_layout_v1_2/03_stage07_to_end.md \
  > ./docs/pipelines/constitution/pipeline.md
```

## 2. Vérifier le diff principal

```bash
git diff -- \
  ./docs/pipelines/constitution/pipeline.md \
  ./docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
```

## 3. Synchroniser les fichiers centraux de suivi

```bash
cp ./tmp/core_modularization_status_after_run_layout.yaml ./docs/transformations/core_modularization/STATUS.yaml
cp ./tmp/core_modularization_worklog_after_run_layout.md ./docs/transformations/core_modularization/WORKLOG.md
```

## 4. Créer les répertoires de travail du premier run

```bash
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/01_challenge
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/02_arbitrage
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/03_patch
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/04_patch_validation
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/05_apply
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/06_core_validation
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/07_release
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/reports
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/outputs
mkdir -p ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/archive
```

## 5. Vérifier l'état final avant exécution du pilote

```bash
git diff -- \
  ./docs/pipelines/constitution/pipeline.md \
  ./docs/transformations/core_modularization/STATUS.yaml \
  ./docs/transformations/core_modularization/WORKLOG.md \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01
```

## 6. Commencer le pilote run-aware

Lire dans cet ordre :
1. `docs/pipelines/constitution/pipeline.md`
2. `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
3. `docs/prompts/shared/Challenge_constitution.md`
4. `docs/prompts/shared/Make04ConstitutionArbitrage.md`
5. `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/run_manifest.yaml`
6. les trois inputs du run sous `runs/.../inputs/`

Puis produire les premiers artefacts dans :
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/01_challenge/`
- puis `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/work/02_arbitrage/`

## 7. Si tout est bon

```bash
git status --short
```

Puis commit et push selon ton flux habituel.
