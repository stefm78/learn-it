# Constitution — zero-search entry prompt

## Objet

Ce document fournit un prompt court pour lancer une IA sur `constitution` sans `run_id`, en forçant un démarrage zéro-search et un arrêt immédiat après la décision d'entrée.

---

## Prompt

```text
Dans le repo learn-it, sur la branche <BRANCH>, exécute le pipeline docs/pipelines/constitution/pipeline.md.

Mais pour l'instant, ne décide que du point d'entrée.

Mode obligatoire : zero-search, zero-deep-read.
- n'utilise aucun search ;
- n'utilise pas compare_commits ;
- ne lis pas les Core complets ;
- ne lis pas les prompts détaillés ;
- fais seulement des lectures directes de :
  1. docs/pipelines/constitution/pipeline.md
  2. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  3. docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md
  4. docs/pipelines/constitution/RUN_ENTRY_GATE.md
  5. docs/pipelines/constitution/RUN_ENTRY_ZERO_SEARCH_PROTOCOL.md
  6. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  7. docs/pipelines/constitution/runs/index.yaml
  8. docs/pipelines/constitution/scope_catalog/manifest.yaml

Puis arrête-toi après avoir répondu seulement :
- quel run actif existe déjà, s'il y en a un ;
- et si la meilleure action est de continuer ce run ou d'ouvrir un nouveau run.

Ne commence aucun stage tant que cette décision n'est pas levée.
```

---

## Exemple concret

```text
Dans le repo learn-it, sur la branche feat/core-modularization-bootstrap, exécute le pipeline docs/pipelines/constitution/pipeline.md.

Mais pour l'instant, ne décide que du point d'entrée.

Mode obligatoire : zero-search, zero-deep-read.
- n'utilise aucun search ;
- n'utilise pas compare_commits ;
- ne lis pas les Core complets ;
- ne lis pas les prompts détaillés ;
- fais seulement des lectures directes de :
  1. docs/pipelines/constitution/pipeline.md
  2. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  3. docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md
  4. docs/pipelines/constitution/RUN_ENTRY_GATE.md
  5. docs/pipelines/constitution/RUN_ENTRY_ZERO_SEARCH_PROTOCOL.md
  6. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  7. docs/pipelines/constitution/runs/index.yaml
  8. docs/pipelines/constitution/scope_catalog/manifest.yaml

Puis arrête-toi après avoir répondu seulement :
- quel run actif existe déjà, s'il y en a un ;
- et si la meilleure action est de continuer ce run ou d'ouvrir un nouveau run.

Ne commence aucun stage tant que cette décision n'est pas levée.
```
