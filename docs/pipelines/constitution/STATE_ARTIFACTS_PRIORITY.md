# Constitution — why AIs miss the right state files

## Objet

Ce document explique pourquoi, malgré la présence de plusieurs artefacts donnant l'état des runs, une IA sans contexte peut encore partir lire les mauvais fichiers ou explorer trop largement le repo.

But :
- rendre ce problème explicite ;
- expliquer qu'il ne s'agit pas d'un manque d'information mais d'un manque de hiérarchie opératoire ;
- fixer les ajustements nécessaires.

---

## Réponse courte

Les IA ne s'en servent pas spontanément pour quatre raisons principales :

1. **les fichiers d'état existent, mais leur priorité n'est pas encore assez impérative** ;
2. **le repo garde encore des chemins historiques plats qui attirent l'attention** ;
3. **les outils de search poussent naturellement vers l'exploration large plutôt que vers la résolution déterministe** ;
4. **la plupart des IA exécutent la tâche demandée trop tôt, au lieu de traiter d'abord la résolution du point d'entrée comme une étape à part entière.**

---

## Les trois niveaux d'état à distinguer

Pour un lancement `constitution`, l'état utile n'est pas dans un seul fichier mais dans une petite chaîne :

### 1. État léger global des runs
- `docs/pipelines/constitution/runs/index.yaml`

Rôle :
- dire quels runs sont actifs ;
- sur quel scope ;
- à quel stage ;
- avec quel statut global.

### 2. État détaillé d'un run donné
- `docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml`

Rôle :
- identité du run ;
- scope lié ;
- mode ;
- état d'exécution détaillé ;
- chemins résolus.

### 3. État d'entrée du run
- `docs/pipelines/constitution/runs/<run_id>/inputs/`
  - `scope_manifest.yaml`
  - `impact_bundle.yaml`
  - `integration_gate.yaml`

Rôle :
- dire ce que le run a le droit de traiter ;
- ce qu'il doit relire ;
- et sous quelles conditions il pourra intégrer globalement.

---

## Pourquoi les IA ratent ces fichiers

### A. Le repo contient encore deux régimes en parallèle
Il existe à la fois :
- le layout historique plat ;
- le layout `runs/<run_id>/...`.

Même si le second est la cible, la coexistence des deux régimes crée une concurrence d'attention.

### B. Les protocoles sont encore documentaires plus qu'exécutoires
Aujourd'hui :
- `RUN_STARTUP_PROTOCOL.md`
- `RUN_ENTRY_DECISION_PROTOCOL.md`
- `RUN_LAYOUT_RESOLUTION.md`

expliquent quoi faire.

Mais si l'IA n'obéit pas strictement à ces documents, rien ne l'empêche encore d'aller explorer plus largement.

### C. Les outils de recherche favorisent l'exploration opportuniste
Quand une IA voit `exécute le pipeline`, elle peut être tentée de :
- chercher des fichiers de travail ;
- chercher des rapports ;
- lire les Core complets ;
- reconstruire globalement l'état.

Ce réflexe est naturel mais coûteux et souvent mauvais ici.

### D. La résolution d'entrée n'est pas encore perçue comme un mini-état terminal
Beaucoup d'IA considèrent encore que :
- résoudre l'entrée est juste un préambule ;
- puis il faut tout de suite commencer à exécuter.

Alors que dans ce design, la bonne règle est :
- **résoudre l'entrée est déjà un état suffisant pour s'arrêter et demander confirmation.**

---

## Ce qu'il faut faire pour corriger cela

### 1. Déclarer les artefacts d'état comme autoritatifs
Quand aucun `run_id` n'est fourni, l'IA doit lire seulement :
- `pipeline.md`
- `RUN_STARTUP_PROTOCOL.md`
- `RUN_ENTRY_DECISION_PROTOCOL.md`
- `RUN_LAYOUT_RESOLUTION.md`
- `runs/index.yaml`
- `scope_catalog/manifest.yaml`

Quand un `run_id` est fourni, elle doit ensuite lire seulement :
- `runs/<run_id>/run_manifest.yaml`
- `runs/<run_id>/inputs/...`

### 2. Faire de la décision d'entrée un vrai point d'arrêt
Sans `run_id`, la bonne sortie n'est pas l'exécution du stage.
La bonne sortie est souvent :
- `continuer ce run ?`
- ou `ouvrir un nouveau run ?`

### 3. Utiliser `update_run_tracking.py` dès la levée du doute
Une fois le point d'entrée résolu, un premier appel du script permet de rendre l'état visible immédiatement.

### 4. Déprécier réellement le layout plat pour les runs bornés
Tant que le layout plat existe comme possibilité visible, certaines IA continueront à y tomber.

---

## Décision de design

Pour `constitution`, les fichiers d'état ne doivent plus être vus comme de simples documents utiles parmi d'autres, mais comme la **chaîne autoritative de résolution d'entrée**.

Ordre de priorité :
1. `runs/index.yaml`
2. `runs/<run_id>/run_manifest.yaml`
3. `runs/<run_id>/inputs/*`
4. ensuite seulement le contexte profond du stage.
