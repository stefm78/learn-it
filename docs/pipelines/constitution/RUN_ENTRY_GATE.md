# Constitution — run entry gate

## Objet

Ce document définit une règle simple et dure :

**tant que la décision d'entrée n'est pas levée, l'IA n'a pas le droit de charger le contexte profond du pipeline.**

Cette règle répond aux dérives observées où l'IA :
- identifie bien qu'un run actif existe ;
- mais continue ensuite à lire `constitution.yaml`, `referentiel.yaml`, `link.yaml`, des prompts détaillés ou d'anciens artefacts plats ;
- alors qu'elle aurait dû s'arrêter pour demander : `on continue ce run ou on en ouvre un nouveau ?`

---

## Règle d'arrêt obligatoire

Quand l'utilisateur demande :
- `exécute le pipeline docs/pipelines/constitution/pipeline.md`

et qu'aucun `run_id` n'est fourni, l'IA doit :

1. résoudre la branche ;
2. lire seulement les artefacts légers de startup ;
3. détecter s'il existe un run actif ;
4. produire une **décision d'entrée** ;
5. **s'arrêter**.

Elle ne doit pas continuer tant que l'utilisateur n'a pas confirmé :
- `continuer le run existant`
- ou `ouvrir un nouveau run`

sauf si un seul choix est strictement non ambigu et explicitement autorisé par le protocole.

---

## Lecture autorisée avant la gate

Autorisé :
- `docs/pipelines/constitution/pipeline.md`
- `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
- `docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md`
- `docs/pipelines/constitution/RUN_ENTRY_GATE.md`
- `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
- `docs/pipelines/constitution/runs/index.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`

---

## Lecture interdite avant la gate

Interdit avant levée de la décision d'entrée :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- prompts détaillés de stage
- anciens artefacts plats historiques
- scans/search larges du repo
- `compare_commits`

---

## Sortie attendue

La sortie correcte avant la gate est une réponse de ce type :

- `Je vois un run actif : CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 sur learner_state, actuellement sur STAGE_01_CHALLENGE. On le continue ou tu veux ouvrir un nouveau run ?`

Ou, si aucun run n'existe :

- `Aucun run actif n'est ouvert. Veux-tu que j'ouvre un nouveau run à partir d'un scope du catalogue ?`

---

## Décision de design

Pour `constitution`, la résolution d'entrée n'est pas un préambule flou mais une **gate**. Tant qu'elle n'est pas levée, l'IA doit rester en contexte minimal.
