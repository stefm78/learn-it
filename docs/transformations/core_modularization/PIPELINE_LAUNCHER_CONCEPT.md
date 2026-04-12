# Pipeline launcher — concept

## Intention

Créer un script simple qui :
- connaît les pipelines publiés via `docs/registry/` ;
- découvre les runs actifs ;
- propose une suite intelligente avec peu de contexte ;
- génère un prompt de lancement court et déterministe ;
- garde toujours la possibilité de continuer un run existant ou d'en ouvrir un nouveau.

## Ce que le launcher doit faire

1. Lister les pipelines connus.
2. Pour un pipeline donné, lire un état léger :
   - index des runs
   - catalogue des scopes
   - éventuellement le stage courant du run actif
3. Produire une décision d'entrée :
   - `continue_active_run`
   - `open_new_run`
   - `disambiguate`
4. Proposer quelques choix par défaut intelligents :
   - s'il n'y a qu'un run actif, recommander sa reprise ;
   - s'il existe d'autres scopes publiés, proposer aussi d'ouvrir un nouveau run sur l'un d'eux ;
   - s'il y a plusieurs runs actifs, proposer une shortlist.
5. Générer soit :
   - un prompt court pour une IA ;
   - soit une commande/outillage de bootstrap pour matérialiser le choix.

## Découpage minimal recommandé

### Étape A — discovery
Lire :
- `docs/registry/pipelines.md`
- `docs/pipelines/<pipeline_id>/AI_PROTOCOL.yaml` si disponible
- `docs/pipelines/<pipeline_id>/runs/index.yaml` si disponible
- `docs/pipelines/<pipeline_id>/scope_catalog/manifest.yaml` si disponible

### Étape B — recommendation
Produire un objet léger du type :
- pipeline_id
- active_runs_count
- recommended_action
- other_available_scopes
- next_best_actions

### Étape C — prompt build
Produire un prompt court selon l'un des cas :
- continuer un run existant ;
- ouvrir un nouveau run sur un scope ;
- demander une courte désambiguïsation.

## Pourquoi c'est une bonne idée

Parce qu'on déplace la complexité :
- hors du prompt utilisateur ;
- hors du contexte profond de l'IA ;
- vers un petit outil déterministe de pré-résolution.

## Première cible

Commencer par `constitution`, puis étendre le même modèle à `platform_factory`.
