# Learn-it

Moteur d'apprentissage adaptatif basé sur une architecture constitutionnelle formelle.

## Point d'entrée

Le point d'entrée opérationnel du repo est :

- `docs/README.md`

Pour comprendre ou faire évoluer le dépôt, suivre ensuite :

1. `docs/registry/operating_model.md`
2. `docs/registry/pipelines.md`
3. `docs/registry/resources.md`
4. le `pipeline.md` du pipeline concerné

## Vue d'ensemble

Learn-it est un système d'apprentissage adaptatif gouverné par pipelines.

Le repo n'est plus organisé comme un simple dépôt documentaire.
Il est structuré autour de :

- `docs/registry/` pour les règles d'exploitation
- `docs/pipelines/` pour les chemins de transformation explicites
- `docs/cores/current/` pour l'état canonique courant
- `docs/cores/releases/` pour les snapshots promus
- `legacy/` pour l'historique, la traçabilité et la migration

## Autorité

L'autorité du repo se lit dans cet ordre :

1. `docs/cores/current/`
2. `docs/cores/releases/`
3. `docs/registry/`
4. `docs/pipelines/`
5. `docs/prompts/shared/` et `docs/patcher/shared/`
6. `docs/architecture/`
7. `legacy/`

## Règle d'interprétation

Quand deux artefacts semblent se contredire :

- privilégier `docs/cores/current/`
- puis `docs/registry/`
- puis le pipeline concerné
- et considérer `legacy/` comme non autoritatif sauf besoin explicite de rétrospection

## Legacy

Le dossier `legacy/` est conservé pour :

- l'historique
- la traçabilité
- la migration

Règle :

> Legacy peut informer. Legacy ne gouverne pas.

## Licence

À définir.
