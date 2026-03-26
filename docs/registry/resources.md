# RESOURCES REGISTRY — Learn-it

## Canonical current resources

### Patch DSL
- `docs/specs/patch-dsl/current.md`

### Release Patch DSL
- `docs/specs/release-patch/current.md`

### Shared prompts
- `docs/prompts/shared/Make12GovernanceReview.md`
- `docs/prompts/shared/Make11GovernancePatch.md`
- `docs/prompts/shared/Make10GovernanceAudit.md`
- `docs/prompts/shared/Challenge_constitution.md`
- `docs/prompts/shared/Make02CoreValidation.md`
- `docs/prompts/shared/Make05CorePatch.md`
- `docs/prompts/shared/Make06PatchValidation.md`
- `docs/prompts/shared/Make07CoreRelease.md`
- `docs/prompts/shared/Make08PatchExecutionReview.md`
- `docs/prompts/shared/Make09ReleasePatch.md`

### Shared patchers
- `docs/patcher/shared/apply_patch.py`
- `docs/patcher/shared/validate_patchset.py`
- `docs/patcher/shared/apply_patch.sh`
- `docs/patcher/shared/apply_release_patch.py`
- `docs/patcher/shared/validate_release_patch.py`

### Current cores
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

## Legacy resources preserved in `legacy/`

### Legacy modular docs
- `legacy/00_ROUTING_GLOBAL.md`
- `legacy/constitution/`
- `legacy/referentiel/`

### Legacy patch workspace
- `legacy/make_constitution/`

### Legacy active Core location
- `legacy/Current_Constitution/`

### Legacy prompts collection
- `legacy/prompts/`

## Promotion rule

Un fichier `shared/` ou `current/` ne doit être remplacé qu'après :

1. dry-run du patcher
2. validation patch-level
3. validation structurelle des Core
4. décision explicite de promotion
