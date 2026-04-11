# Constitution — entry prompt template without explicit run id

## Objet

Ce document fournit une formulation courte pour lancer une IA sur le pipeline `constitution` **sans préciser de run_id**, tout en forçant l'IA à décider d'abord entre :
- continuer un run existant ;
- ou ouvrir un nouveau run.

---

## Template

```text
Dans le repo learn-it, sur la branche <BRANCH>, exécute le pipeline docs/pipelines/constitution/pipeline.md.

Startup obligatoire à faible contexte :
- ne fais pas de recherche large dans le repo ;
- n'utilise pas compare_commits ;
- ne lis pas les Core complets tant que le point d'entrée n'est pas résolu ;
- lis seulement :
  1. docs/pipelines/constitution/pipeline.md
  2. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  3. docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md
  4. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  5. docs/pipelines/constitution/runs/index.yaml
  6. docs/pipelines/constitution/scope_catalog/manifest.yaml

Puis détermine s'il existe déjà un run actif à reprendre.
S'il y a un run actif évident, propose explicitement de le continuer ou d'ouvrir un nouveau run.
S'il y a ambiguïté, ne charge pas plus de contexte : propose la next best action la plus courte possible.
Ne commence réellement l'exécution d'un stage qu'après levée du doute.
```

---

## Exemple concret

```text
Dans le repo learn-it, sur la branche feat/core-modularization-bootstrap, exécute le pipeline docs/pipelines/constitution/pipeline.md.

Startup obligatoire à faible contexte :
- ne fais pas de recherche large dans le repo ;
- n'utilise pas compare_commits ;
- ne lis pas les Core complets tant que le point d'entrée n'est pas résolu ;
- lis seulement :
  1. docs/pipelines/constitution/pipeline.md
  2. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  3. docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md
  4. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  5. docs/pipelines/constitution/runs/index.yaml
  6. docs/pipelines/constitution/scope_catalog/manifest.yaml

Puis détermine s'il existe déjà un run actif à reprendre.
S'il y a un run actif évident, propose explicitement de le continuer ou d'ouvrir un nouveau run.
S'il y a ambiguïté, ne charge pas plus de contexte : propose la next best action la plus courte possible.
Ne commence réellement l'exécution d'un stage qu'après levée du doute.
```
