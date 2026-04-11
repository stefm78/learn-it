### STAGE_07_RELEASE_MATERIALIZATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

- Rule:
  - `STAGE_07_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07
  - in bounded mode, no release materialization may be treated as promotable if the `integration_gate` is not explicitly cleared

### STAGE_08_PROMOTE_CURRENT
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_08_PROMOTE_CURRENT.md`

- Rule:
  - `STAGE_08_PROMOTE_CURRENT.md` is the canonical specification for Stage 08
  - in bounded mode, promotion remains blocked until global checks required by the `integration_gate` are explicitly satisfied


### STAGE_09_CLOSEOUT_AND_ARCHIVE
Objectif :
- clôturer explicitement le run du pipeline après promotion réussie
- archiver le run terminé sous `docs/pipelines/constitution/archive/<release_id>/`
- réinitialiser `docs/pipelines/constitution/work/` pour rendre le pipeline immédiatement prêt à une nouvelle exécution
- conserver une trace finale de clôture exploitable humainement et techniquement

Inputs :
- `docs/pipelines/constitution/reports/promotion_report.yaml`
- `docs/cores/current/manifest.yaml`
- `docs/pipelines/constitution/work/07_release/release_plan.yaml`
- `docs/pipelines/constitution/reports/release_materialization_report.yaml`
- `docs/pipelines/constitution/reports/patch_execution_report.yaml`
- `docs/pipelines/constitution/work/06_core_validation/core_validation.yaml`

Préconditions :
- `reports/promotion_report.yaml` doit être en `status: PASS`
- `docs/cores/current/manifest.yaml` doit être valide
- `docs/cores/current/manifest.yaml` doit pointer vers la release promue par le Stage 08

Principe opératoire :
- vérifier que la promotion Stage 08 constitue bien l’état actif final du run
- produire `reports/closeout_report.yaml` et `outputs/final_run_summary.md`
- archiver une copie complète du run terminé sous `docs/pipelines/constitution/archive/<release_id>/` avec :
  - `work/`
  - `reports/`
  - `outputs/`
- considérer `work/` comme un workspace transitoire et non comme une archive canonique
- supprimer puis recréer `docs/pipelines/constitution/work/` vide
- ne modifier ni `docs/cores/releases/` ni `docs/cores/current/`

Archive attendue :
- `archive/<release_id>/work/`
- `archive/<release_id>/reports/`
- `archive/<release_id>/outputs/`

Commandes de référence :
- vérifier l’état courant final :
  - `python docs/patcher/shared/validate_current_manifest.py ./docs/cores/current/manifest.yaml ./docs/specs/core-release/current_manifest.schema.yaml`
- vérifier la traçabilité de promotion :
  - `python docs/patcher/shared/validate_promotion_report.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/specs/core-release/promotion_report.schema.yaml`
- clôturer, archiver et réinitialiser le workspace :
  - `python docs/patcher/shared/closeout_pipeline_run.py ./docs/pipelines/constitution/reports/promotion_report.yaml ./docs/cores/current/manifest.yaml ./docs/pipelines/constitution/reports/closeout_report.yaml ./docs/pipelines/constitution/outputs/final_run_summary.md ./docs/pipelines/constitution/archive`

Outputs :
- `reports/closeout_report.yaml`
- `outputs/final_run_summary.md`
- `archive/<release_id>/`
- `work/` recréé vide

Règle opératoire :
- `docs/cores/releases/` reste l’archive métier immuable
- `docs/cores/current/` reste uniquement la vue active promue
- `docs/pipelines/constitution/work/` est un workspace transitoire du run courant
- l’archive des runs terminés se trouve sous `docs/pipelines/constitution/archive/`
- le Stage 09 ne laisse pas l’historique d’un run uniquement dans `work/`
- le Stage 09 clôture, archive et réinitialise ; il ne recalcule aucun contenu métier

## Success criteria

- No stage may be skipped
- No file in `current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under `work/05_apply/`
- Any release materialization must write immutable artifacts under `docs/cores/releases/`
- Promotion to `current/` must remain explicit and occur in a dedicated stage
- Any successful promotion should be followed by an explicit archive-and-reset closeout stage
- Any completed run should be archived under `docs/pipelines/constitution/archive/<release_id>/`
- `docs/pipelines/constitution/work/` should be reset after closeout to prepare the next execution
- In bounded mode, no silent out-of-scope modification is allowed
- In bounded mode, no promotion may occur until the `integration_gate` is explicitly cleared
