# Shared patcher status

## Current canonical paths

- `docs/patcher/shared/apply_patch.py`
- `docs/patcher/shared/validate_patchset.py`
- `docs/patcher/shared/apply_patch.sh`
- `docs/patcher/shared/apply_patch_v4.py`
- `docs/patcher/shared/validate_patchset_v4.py`
- `docs/patcher/shared/apply_release_patch.py`
- `docs/patcher/shared/validate_release_patch.py`

## Status

### apply_patch.py
Version canonique synchronisée avec le moteur partagé v4.

### validate_patchset.py
Version canonique synchronisée avec le validateur Patch DSL v4.

### apply_release_patch.py
Moteur de promotion/release au niveau dépôt.

### validate_release_patch.py
Validateur du Release Patch DSL.

## Rule

Les pipelines doivent utiliser les chemins canoniques sans dépendre du legacy patcher.
