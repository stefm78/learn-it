# Shared patcher status

## Current canonical paths

- `docs/patcher/shared/apply_patch.py`
- `docs/patcher/shared/validate_patchset.py`
- `docs/patcher/shared/apply_patch.sh`
- `docs/patcher/shared/validate_patchset_v4.py`

## Status

### apply_patch.py
Wrapper provisoire vers le patcher legacy tant que le vrai moteur v4 n'est pas promu en remplacement.

### validate_patchset.py
Validateur minimal de forme externe, utile comme garde-fou d'entrée.

### validate_patchset_v4.py
Validateur v4 promu, adapté au Patch DSL v4.

## Next target

Promouvoir le vrai moteur `apply_patch_v4.py` dans ce même dossier et basculer les pipelines dessus.
