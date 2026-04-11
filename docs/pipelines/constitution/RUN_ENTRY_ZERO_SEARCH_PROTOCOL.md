# Constitution — run entry zero-search protocol

## Objet

Ce document durcit encore le démarrage d'une IA sur `constitution` quand l'utilisateur demande simplement :
- `Exécute le pipeline docs/pipelines/constitution/pipeline.md`

sans fournir de `run_id`.

La règle nouvelle est simple :

**pour décider `continuer un run existant` vs `ouvrir un nouveau run`, l'IA ne doit lancer aucun search.**

---

## Réponse courte

Oui :
- pas de `search` ;
- pas de `compare_commits` ;
- pas de lecture des Core complets ;
- pas de lecture des prompts détaillés ;
- seulement quelques `fetch_file` directs sur des chemins connus.

---

## Pourquoi

Même un search "raisonnable" dérive facilement vers :
- exploration large du repo ;
- lecture d'artefacts historiques plats ;
- chargement prématuré du contexte métier ;
- pseudo-exécution avant que la décision d'entrée soit levée.

Or la question initiale n'est pas encore métier.
Elle est seulement :
- existe-t-il déjà un run actif à reprendre ?
- ou faut-il ouvrir un nouveau run ?

---

## Lecture autorisée

Quand aucun `run_id` n'est fourni, l'IA doit utiliser **uniquement** des lectures directes sur chemins connus :

1. `docs/pipelines/constitution/pipeline.md`
2. `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
3. `docs/pipelines/constitution/RUN_ENTRY_DECISION_PROTOCOL.md`
4. `docs/pipelines/constitution/RUN_ENTRY_GATE.md`
5. `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
6. `docs/pipelines/constitution/runs/index.yaml`
7. `docs/pipelines/constitution/scope_catalog/manifest.yaml`

---

## Lecture interdite à ce stade

Interdit avant levée de la décision d'entrée :
- tout `search`
- tout `compare_commits`
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- prompts détaillés de stage
- artefacts plats historiques de `inputs/`, `work/`, `reports/`

---

## Algorithme minimal

### Étape 1
Lire `runs/index.yaml`.

### Étape 2
- s'il n'y a aucun run actif : proposer d'ouvrir un nouveau run ;
- s'il y a un seul run actif : proposer explicitement de le continuer ou d'ouvrir un nouveau run ;
- s'il y a plusieurs runs actifs : proposer une shortlist très courte.

### Étape 3
**S'arrêter.**

Ne pas continuer vers le contenu profond du pipeline ou du scope tant que l'utilisateur n'a pas levé le doute.

---

## Sortie attendue

Exemple correct :

- `Je vois un run actif : CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 sur learner_state, actuellement sur STAGE_01_CHALLENGE. On le continue ou tu veux ouvrir un nouveau run ?`

Exemple correct sans run actif :

- `Aucun run actif n'est ouvert. Veux-tu que j'ouvre un nouveau run à partir d'un scope du catalogue ?`

---

## Décision de design

Pour `constitution`, la décision d'entrée sans `run_id` doit être résolue en mode **zero-search**. Toute lecture profonde ou recherche libre avant cette résolution est considérée comme un anti-pattern.
