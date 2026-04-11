# Constitution — run entry hardening notes

## Pourquoi ce document

Second retour observé sur un lancement IA du pipeline `constitution` sans `run_id` explicite :
- l'IA a bien compris qu'il fallait rattacher l'exécution à l'état réel de la branche ;
- mais elle a encore dérivé trop tôt vers des lectures profondes (`constitution.yaml`, `referentiel.yaml`, prompts détaillés) ;
- elle n'a pas stoppé sa progression après la simple décision d'entrée `continue existing run` vs `new run`.

Ce document durcit donc encore le comportement attendu.

---

## Diagnostic

### Ce qui était bon
- vérification de la branche ;
- compréhension qu'il fallait identifier un run existant ;
- volonté d'éviter d'écrire au mauvais endroit.

### Ce qui n'était pas assez bon
- recherche et lecture de fichiers profonds avant levée du doute ;
- lecture du layout plat historique (`docs/pipelines/constitution/inputs/...`) alors que la décision d'entrée n'était pas encore formellement terminée ;
- lecture de `constitution.yaml` et `referentiel.yaml` avant la simple question utilisateur `continuer ou nouveau run ?`.

---

## Règle durcie

Quand **aucun `run_id` n'est fourni** :

1. lire seulement les artefacts légers de résolution :
   - `docs/pipelines/constitution/pipeline.md`
   - `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
   - `docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md`
   - `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
   - `docs/pipelines/constitution/runs/index.yaml`
   - `docs/pipelines/constitution/scope_catalog/manifest.yaml`
2. ne pas lire `constitution.yaml`, `referentiel.yaml`, `link.yaml` ;
3. ne pas lire les prompts détaillés de stage ;
4. ne pas lire le layout plat historique ;
5. produire d'abord une **décision d'entrée** ou une **question de choix** ;
6. ne charger le contexte profond qu'après réponse explicite de l'utilisateur ou résolution sans ambiguïté.

---

## Sortie attendue à ce stade

En absence de `run_id`, l'IA devrait idéalement s'arrêter après une réponse de ce type :

- `Je vois un run actif : CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 sur learner_state, actuellement positionné sur STAGE_01_CHALLENGE. On le continue ou tu veux ouvrir un nouveau run ?`

Ou, si aucun run n'est actif :

- `Aucun run actif n'est ouvert. Meilleure action : créer un nouveau run à partir d'un scope du catalogue.`

---

## Anti-pattern explicite

Le démarrage suivant est considéré comme incorrect :
- vérifier la branche ;
- puis partir lire `constitution.yaml`, `referentiel.yaml`, les paramètres référentiels ou les prompts détaillés ;
- puis seulement ensuite demander s'il faut continuer ou ouvrir un nouveau run.

L'ordre correct est l'inverse.

---

## Décision de design

Pour `constitution`, **la décision d'entrée est un mini-état terminal en soi** : tant qu'elle n'est pas levée, l'IA ne doit pas commencer l'analyse métier profonde du scope ou du stage.
