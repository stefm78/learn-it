# Current cores

Ce dossier contient les copies canoniques actives des Core Learn-it.

## Statut actuel

Les fichiers suivants sont désormais des copies promues, et non plus des pointeurs descriptifs :

- `constitution.yaml`
- `referentiel.yaml`
- `link.yaml`

## Règle

Les pipelines doivent consommer directement ces fichiers comme sources canoniques courantes.

## Promotion

Toute mise à jour de `docs/cores/current/` doit passer par le pipeline `release` et un `RELEASE_PATCH_SET`.
