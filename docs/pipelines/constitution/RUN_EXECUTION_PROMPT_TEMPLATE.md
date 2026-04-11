# Constitution — run execution prompt template

## Objet

Ce document fournit une formulation courte mais robuste pour lancer une IA sur un run `constitution` déjà identifié, avec un coût de contexte minimal.

---

## Template — run_id déjà connu

```text
Dans le repo learn-it, sur la branche <BRANCH>, exécute le pipeline docs/pipelines/constitution/pipeline.md au <STAGE_ID> en mode run-aware pour run_id=<RUN_ID>.

Startup obligatoire à faible contexte :
- ne fais pas de recherche large dans le repo ;
- n'utilise pas compare_commits ;
- n'utilise pas le layout plat historique sauf échec explicite de résolution du run ;
- lis seulement, dans cet ordre :
  1. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  2. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  3. docs/pipelines/constitution/runs/index.yaml
  4. docs/pipelines/constitution/runs/<RUN_ID>/run_manifest.yaml
  5. docs/pipelines/constitution/runs/<RUN_ID>/inputs/scope_manifest.yaml
  6. docs/pipelines/constitution/runs/<RUN_ID>/inputs/impact_bundle.yaml
  7. docs/pipelines/constitution/runs/<RUN_ID>/inputs/integration_gate.yaml

Si le run est résolu sans ambiguïté, exécute le stage demandé et écris uniquement dans docs/pipelines/constitution/runs/<RUN_ID>/...
Si le run n'est pas résolu, n'explore pas largement le repo : donne une next best action courte et déterministe.
À la fin, donne-moi la commande update_run_tracking.py à exécuter.
```

---

## Exemple concret

```text
Dans le repo learn-it, sur la branche feat/core-modularization-bootstrap, exécute le pipeline docs/pipelines/constitution/pipeline.md au STAGE_01_CHALLENGE en mode run-aware pour run_id=CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01.

Startup obligatoire à faible contexte :
- ne fais pas de recherche large dans le repo ;
- n'utilise pas compare_commits ;
- n'utilise pas le layout plat historique sauf échec explicite de résolution du run ;
- lis seulement, dans cet ordre :
  1. docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md
  2. docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md
  3. docs/pipelines/constitution/runs/index.yaml
  4. docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/run_manifest.yaml
  5. docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/scope_manifest.yaml
  6. docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/impact_bundle.yaml
  7. docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/inputs/integration_gate.yaml

Si le run est résolu sans ambiguïté, exécute le STAGE_01_CHALLENGE et écris uniquement dans docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/...
Si le run n'est pas résolu, n'explore pas largement le repo : donne une next best action courte et déterministe.
À la fin, donne-moi la commande update_run_tracking.py à exécuter.
```
