# Policies — constitution

## Objet

Ce répertoire porte les **entrées canonisées et gouvernantes** du pipeline
`constitution` lorsqu'un comportement déterministe ne peut pas être inféré du
canon seul.

Ces artefacts ne sont pas des notes temporaires de transformation.
Ils définissent des règles ou décisions structurées consommables par l'outillage
partagé et par les étapes déterministes du pipeline.

## Principe d'autorité

Pour `constitution` :
- les Core publiés restent dans `docs/cores/current/` ;
- les règles structurantes du pipeline vivent dans `docs/pipelines/constitution/` ;
- les politiques et décisions de modularisation déterministe sont canonisées ici.

`docs/transformations/core_modularization/` peut documenter la transformation,
mais ne doit pas rester la source durable des décisions gouvernantes.

## Domaines retenus

- `scope_generation/`
- `integration/`
- `canonical_rebuild/`

Chaque domaine peut distinguer :
- une **policy** durable ;
- des **decisions** humaines normalisées et versionnées.

## Règle

Les scripts déterministes ne doivent pas dépendre d'un raisonnement implicite de
conversation. Ils doivent consommer :
- le canon ;
- ces fichiers de politique/décision ;
- éventuellement des résultats de pipeline déjà structurés.
