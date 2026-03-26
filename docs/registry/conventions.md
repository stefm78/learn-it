# CONVENTIONS — Learn-it pipeline framework

## Naming

### Current aliases
Utiliser des noms stables et sans version dans :
- `docs/cores/current/`
- `docs/prompts/shared/`
- `docs/patcher/shared/`

### Releases and archive
Utiliser des noms versionnés dans :
- `docs/cores/releases/`
- `docs/specs/patch-dsl/archive/`
- `docs/prompts/archive/`
- `docs/patcher/archive/`

## Write zones

### Allowed write zones for pipeline execution
- `docs/pipelines/<pipeline_id>/inputs/`
- `docs/pipelines/<pipeline_id>/work/`
- `docs/pipelines/<pipeline_id>/outputs/`
- `docs/pipelines/<pipeline_id>/reports/`

### Forbidden write zones during normal execution
- `docs/cores/current/`
- `docs/cores/releases/`
- `docs/specs/`
- `docs/prompts/shared/`
- `docs/patcher/shared/`

## Validation order

1. Patchset validation
2. Dry-run patch application
3. Real patch application
4. Core validation
5. Release planning
6. Promotion

## Legacy rule

Les chemins legacy sont lisibles mais non canoniques.
Un pipeline ne doit les utiliser que :
- si la ressource n'a pas encore été promue ;
- ou si la tâche vise explicitement l'historique.
