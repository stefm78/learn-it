# Current core aliases

Ce dossier définit les points d'entrée canoniques pour les Core actifs.

## Statut actuel

La promotion complète des Core vers `docs/cores/current/` n'est pas encore finalisée.
Les fichiers ci-dessous sont donc des alias descriptifs pointant vers les sources legacy actuellement actives :

- `constitution.yaml`
- `referentiel.yaml`
- `link.yaml`

## Règle

Un pipeline doit d'abord lire le descripteur alias, puis charger le `source_path` indiqué tant que la promotion définitive n'a pas eu lieu.
