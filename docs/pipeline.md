# PIPELINE GATEWAY — Learn-it

Point d'entrée unique pour une IA opérant sur le framework de pipelines Learn-it.

## Objectif

Ce fichier sert à :
- découvrir les pipelines disponibles ;
- retrouver les ressources canoniques courantes ;
- savoir où écrire les artefacts intermédiaires ;
- éviter l'usage direct des chemins legacy.

## Règle de lecture

Une IA doit suivre cet ordre :

1. Charger `docs/registry/pipelines.md`
2. Identifier le pipeline demandé
3. Charger le `pipeline.md` du pipeline cible
4. Charger uniquement les ressources référencées par ce pipeline
5. Écrire tous les artefacts temporaires dans les répertoires `inputs/`, `work/`, `outputs/` et `reports/` du pipeline cible
6. Ne jamais écrire dans `archive/`, `releases/` ou les chemins legacy
7. Ne promouvoir un résultat vers `current/` qu'après validation explicite

## Ressources canoniques courantes

- Registry : `docs/registry/pipelines.md`
- Resources : `docs/registry/resources.md`
- Conventions : `docs/registry/conventions.md`
- Patch DSL courant : `docs/specs/patch-dsl/current.md`
- Cores courants :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

## Pipelines disponibles

- `constitution` → audit, patch, validation, promotion des Core
- `release` → bump de version, synchronisation inter-Core, notes de release
- `migration` → pipeline réservé aux migrations de structure ou de format

## Legacy

Les chemins suivants restent disponibles pour compatibilité et archivage :
- `docs/Current_Constitution/`
- `docs/constitution/`
- `docs/referentiel/`
- `docs/make_constitution/`
- `prompts/`

Ils ne doivent plus être utilisés comme point d'entrée principal par une IA sans instruction explicite.
