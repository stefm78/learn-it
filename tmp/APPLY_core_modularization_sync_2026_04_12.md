# Apply — synchronisation centrale core_modularization — 2026-04-12

## Fichiers préparés

- `tmp/STATUS_core_modularization_sync_2026_04_12.yaml`
- `tmp/WORKLOG_core_modularization_sync_2026_04_12_short.md`

## Commandes de remplacement

```bash
cp ./tmp/STATUS_core_modularization_sync_2026_04_12.yaml \
  ./docs/transformations/core_modularization/STATUS.yaml

cp ./tmp/WORKLOG_core_modularization_sync_2026_04_12_short.md \
  ./docs/transformations/core_modularization/WORKLOG.md
```

## Vérification recommandée

```bash
git diff -- \
  ./docs/transformations/core_modularization/STATUS.yaml \
  ./docs/transformations/core_modularization/WORKLOG.md
```

## Intention

Cette synchronisation centrale aligne les fichiers de suivi principaux avec :
- la clarification `scope extraction vs effective read surface` ;
- J2 sur la réduction de la surface de lecture effective ;
- J3 sur la reconstruction canonique bidirectionnelle.
