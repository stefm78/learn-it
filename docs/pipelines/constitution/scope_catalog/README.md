# Constitution scope catalog

## Rôle

Ce répertoire porte les **définitions publiées des scopes** du pipeline `constitution`.

Un scope catalogué est :
- un périmètre logique stable ;
- dérivé de la Constitution active ;
- versionné ;
- réutilisable pour plusieurs runs.

Un scope catalogué n'est pas un run.

## Structure cible

- `manifest.yaml` : index du catalogue publié.
- `scope_definitions/*.yaml` : définitions individuelles des scopes.

## Origine

Le catalogue doit être extrait ou régénéré à partir de l'état gouverné de :
- `docs/cores/current/constitution.yaml`
- et, si nécessaire pour les dépendances de lecture :
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

## Méthode de génération recommandée

Méthode cible :
- extraction automatique assistée ;
- validation gouvernée ;
- publication du catalogue.

## Usage

Les runs dans `docs/pipelines/constitution/runs/<run_id>/` doivent sélectionner un `scope_id` provenant de ce catalogue.
