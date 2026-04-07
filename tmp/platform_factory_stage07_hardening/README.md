# Platform Factory Stage 07 hardening

Ce répertoire contient des remplacements prêts à copier pour fiabiliser la chaîne Stage 07/08 du pipeline `platform_factory`.

## Fichiers fournis

- `build_platform_factory_release_plan.py`
- `materialize_platform_factory_release.py`
- `promote_platform_factory_current.py`
- `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

## Commandes de remplacement

```bash
cp -f ./tmp/platform_factory_stage07_hardening/build_platform_factory_release_plan.py ./docs/patcher/shared/build_platform_factory_release_plan.py
cp -f ./tmp/platform_factory_stage07_hardening/materialize_platform_factory_release.py ./docs/patcher/shared/materialize_platform_factory_release.py
cp -f ./tmp/platform_factory_stage07_hardening/promote_platform_factory_current.py ./docs/patcher/shared/promote_platform_factory_current.py
cp -f ./tmp/platform_factory_stage07_hardening/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md ./docs/pipelines/platform_factory/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md
```

## Pourquoi ces remplacements

- éviter que `release_required: false` produise un faux `WARN` de pipeline ;
- garantir une note explicite de non-matérialisation ;
- rendre le manifest de release suffisamment riche pour la promotion ;
- renforcer les contrôles de cohérence entre release plan, release matérialisée et manifest ;
- normaliser les chemins de repo pour éviter des incohérences `/` vs `\\`.
