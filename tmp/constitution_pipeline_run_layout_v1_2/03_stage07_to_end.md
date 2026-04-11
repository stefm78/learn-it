### STAGE_07_RELEASE_MATERIALIZATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

- Rule:
  - `STAGE_07_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07
  - in bounded mode, no release materialization may be treated as promotable if the resolved `integration_gate` is not explicitly cleared

### STAGE_08_PROMOTE_CURRENT
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_08_PROMOTE_CURRENT.md`

- Rule:
  - `STAGE_08_PROMOTE_CURRENT.md` is the canonical specification for Stage 08
  - in bounded mode, promotion remains blocked until global checks required by the resolved `integration_gate` are explicitly satisfied

### STAGE_09_CLOSEOUT_AND_ARCHIVE
Objectif :
- clôturer explicitement le run du pipeline après promotion réussie
- archiver le run terminé sous un répertoire d'archive cohérent avec le layout résolu
- réinitialiser l'espace de travail du run courant
- conserver une trace finale de clôture exploitable humainement et techniquement

Inputs :
- promotion report depuis le répertoire résolu de reports
- `docs/cores/current/manifest.yaml`
- release plan depuis le répertoire résolu de `work/07_release/`
- release materialization report depuis le répertoire résolu de reports
- patch execution report depuis le répertoire résolu de reports
- core validation depuis le répertoire résolu de `work/06_core_validation/`

Préconditions :
- le promotion report résolu doit être en `status: PASS`
- `docs/cores/current/manifest.yaml` doit être valide
- `docs/cores/current/manifest.yaml` doit pointer vers la release promue par le Stage 08

Principe opératoire :
- vérifier que la promotion Stage 08 constitue bien l’état actif final du run
- produire le closeout report et le final run summary dans le layout résolu
- archiver une copie complète du run terminé sous le répertoire d'archive résolu
- considérer l'espace `work/` du run comme transitoire et non comme archive canonique
- ne modifier ni `docs/cores/releases/` ni `docs/cores/current/`

Règle opératoire :
- en layout plat, le comportement historique reste valable
- en layout run, l'archive et le reset s'appliquent au run courant sous `runs/<run_id>/...`
- le Stage 09 clôture, archive et réinitialise ; il ne recalcule aucun contenu métier

## Success criteria

- No stage may be skipped
- No file in `current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under the resolved `work/05_apply/`
- Any release materialization must write immutable artifacts under `docs/cores/releases/`
- Promotion to `current/` must remain explicit and occur in a dedicated stage
- Any successful promotion should be followed by an explicit archive-and-reset closeout stage
- In bounded mode, no silent out-of-scope modification is allowed
- In bounded mode, no promotion may occur until the `integration_gate` is explicitly cleared
- In run mode, the run instance is the primary execution unit and its own `work/`, `reports/`, `outputs/` and `archive/` directories are authoritative for the local cycle
