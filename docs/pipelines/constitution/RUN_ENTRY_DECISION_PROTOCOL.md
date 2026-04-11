# Constitution — run entry decision protocol

## Objet

Ce document définit le comportement attendu d'une IA lorsqu'un utilisateur demande simplement :
- `Exécute le pipeline docs/pipelines/constitution/pipeline.md`
- ou une variante courte équivalente,

sans préciser de `run_id`, de `scope_id` ou de `scope_key`.

Le but est que l'IA :
- commence par détecter les runs déjà ouverts ;
- propose naturellement de continuer un run existant ou d'en créer un nouveau ;
- ne charge presque aucun contexte profond avant que ce choix soit levé.

---

## Principe

Quand aucun `run_id` n'est fourni, l'IA ne doit **pas** commencer à exécuter un stage ni scanner largement le repo.

Son premier réflexe doit être :
1. lire les artefacts légers de startup ;
2. détecter les runs actifs ;
3. déterminer s'il existe un choix évident ;
4. sinon proposer la `next best action` la plus courte possible.

---

## Lecture minimale obligatoire

En absence de `run_id`, lire uniquement :
1. `docs/pipelines/constitution/pipeline.md`
2. `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
3. `docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md`
4. `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
5. `docs/pipelines/constitution/runs/index.yaml`
6. `docs/pipelines/constitution/scope_catalog/manifest.yaml`

Ne pas lire les Core complets ni les prompts détaillés tant que le choix d'entrée n'est pas levé.

---

## Algorithme de décision d'entrée

### Cas A — aucun run actif
Action par défaut :
- proposer la création d'un nouveau run ;
- si le catalogue ne contient qu'un scope clairement pertinent au contexte utilisateur, le suggérer ;
- sinon proposer un choix bref entre scopes publiés.

### Cas B — un seul run actif
Action par défaut :
- proposer de reprendre ce run ;
- formuler explicitement l'alternative de créer un nouveau run si l'utilisateur le souhaite.

Exemple :
- `Un run actif existe déjà : CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 sur learner_state. Meilleure action : le reprendre, sauf si tu veux ouvrir un nouveau run.`

### Cas C — plusieurs runs actifs
Action par défaut :
- ne pas choisir silencieusement ;
- proposer une shortlist très courte ;
- recommander la reprise la plus vraisemblable si un signal est plus fort que les autres.

### Cas D — run actif mais stage non évident
Action par défaut :
- proposer la reprise du run ;
- indiquer le stage courant connu depuis l'index ;
- recommander l'action suivante la plus probable.

---

## Règle conversationnelle attendue

Quand aucun `run_id` n'est fourni, l'IA doit répondre dans cet esprit :

- `Je vois déjà un run actif sur ce pipeline. On le continue ou on ouvre un nouveau run ?`

Si le choix évident est très fort, l'IA peut ajouter une recommandation courte :

- `Je recommande de continuer CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01, actuellement positionné sur STAGE_01_CHALLENGE.`

---

## Anti-patterns

En absence de `run_id`, éviter :
- de scanner largement le repo ;
- de relire les Core complets ;
- de déduire silencieusement qu'il faut créer un nouveau run ;
- d'exécuter un stage sans avoir d'abord résolu `continue` vs `new run`.

---

## Next best action

Le startup doit toujours produire une `next best action` courte, par exemple :
- `Continuer le run actif CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01.`
- `Choisir entre reprendre learner_state R01 ou créer un nouveau run.`
- `Aucun run actif : choisir un scope dans le catalogue pour ouvrir un nouveau run.`

---

## Décision de design

Pour `constitution`, en absence de `run_id`, l'IA doit d'abord résoudre si l'utilisateur veut **continuer un run existant** ou **ouvrir un nouveau run**, avant de charger le contexte profond ou d'exécuter un stage.
