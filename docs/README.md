# Docs — Learn-it

Ce dossier contient la **structure opérationnelle canonique** du repo.

## Point de départ

Pour comprendre ou faire évoluer le repo, commencez ici, dans cet ordre :

1. `docs/registry/operating_model.md`
2. `docs/registry/pipelines.md`
3. `docs/registry/resources.md`
4. le `pipeline.md` du pipeline concerné

## Structure

### `docs/registry/`

Définit les règles d’exploitation du repo :

* operating model
* conventions
* pipelines
* ressources

### `docs/specs/`

Contient les spécifications formelles utilisées par les pipelines :

* Patch DSL
* Release Patch DSL

### `docs/prompts/shared/`

Contient les prompts partagés utilisés par les pipelines.

### `docs/patcher/shared/`

Contient les outils partagés de patch, validation et promotion.

### `docs/cores/current/`

Contient l’état canonique courant du système.

Fichiers autoritatifs :

* `constitution.yaml`
* `referentiel.yaml`
* `link.yaml`

### `docs/cores/releases/`

Contient les snapshots promus et historisés.

### `docs/pipelines/`

Contient les pipelines actifs du repo, chacun avec :

* `pipeline.md`
* `state.yaml`
* ses inputs / work / outputs / reports si nécessaires

### `docs/architecture/`

Contient les documents d’architecture et de transition utiles à la compréhension du framework.
Ces documents éclairent le système, mais ne remplacent pas les fichiers canoniques de `registry/`, `specs/`, `cores/current/` ou `pipelines/`.

## Autorité

L’autorité du repo se lit dans cet ordre :

1. `docs/cores/current/`
2. `docs/cores/releases/`
3. `docs/registry/`
4. `docs/pipelines/`
5. `docs/prompts/shared/` et `docs/patcher/shared/`
6. `docs/architecture/`
7. `legacy/`

## Legacy

Le dossier `legacy/` est conservé pour :

* l’historique
* la traçabilité
* la migration

Règle :

> Legacy peut informer. Legacy ne gouverne pas.

Une IA ou un contributeur ne doit pas utiliser `legacy/` comme point d’entrée par défaut.

## Règle opérationnelle

Le repo n’est plus un dépôt documentaire libre.
Il est gouverné par pipelines.

Toute évolution importante doit suivre un chemin explicite :

* `constitution`
* `release`
* `migration`
* ou maintenance de gouvernance/registry

## Conseil pratique

Quand un doute existe entre deux fichiers :

* privilégier `docs/cores/current/`
* puis `docs/registry/`
* puis le pipeline concerné
* et considérer `legacy/` comme non autoritatif sauf besoin explicite de rétrospection.


## Governance

Le pipeline `governance` maintient la cohérence opératoire du repo lui-même.
