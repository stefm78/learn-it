# Constitution — run launch hardening notes

## Pourquoi ce document

Premier retour observé sur un lancement IA du pipeline `constitution` :
- l'IA a bien perçu qu'il fallait raccrocher le run au bon état ;
- mais elle a commencé par des recherches GitHub larges et du scanning diffus ;
- elle a consulté des artefacts plats historiques avant les artefacts légers de résolution ;
- elle n'a pas appliqué immédiatement le principe de **startup à faible contexte**.

Ce document fixe donc les ajustements de design et de prompt à appliquer.

---

## Diagnostic

### Ce qui était bon
- réflexe de ne pas rejouer aveuglément ;
- volonté de reconstruire l'état réel avant exécution ;
- prise en compte de la branche.

### Ce qui n'était pas assez bon
- recherche large dans le repo avant lecture des artefacts légers de startup ;
- usage de `compare_commits` trop tôt ;
- consultation d'artefacts plats historiques alors qu'un `run_id` était déjà fourni ;
- coût de contexte trop élevé avant résolution du bon point d'entrée.

---

## Règle durcie

Quand un `run_id` est fourni dans la requête :

1. **ne pas lancer de recherche large dans le repo en première intention** ;
2. **ne pas utiliser `compare_commits` en startup** ;
3. **ne pas consulter le layout plat historique** sauf si le run ne peut pas être résolu ;
4. lire d'abord, dans cet ordre :
   - `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
   - `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`
   - `docs/pipelines/constitution/runs/index.yaml`
   - `docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml`
   - les trois inputs du run
5. ne charger le prompt détaillé de stage qu'après validation du bon run.

---

## Anti-patterns explicites

Au startup d'un run identifié, éviter :
- `search` large sur des mots-clés de repo ;
- `compare_commits` branche vs main ;
- lecture opportuniste de fichiers plats historiques ;
- reconstruction globale du chantier ;
- exploration du repo entier pour trouver le point d'entrée.

---

## Next best action attendue

Si le `run_id` existe et est cohérent :
- passer directement à la lecture du `run_manifest` et des inputs du run.

Si le `run_id` n'existe pas ou n'est pas cohérent :
- produire une `next best action` courte du type :
  - `Run introuvable. Meilleure action : vérifier runs/index.yaml ou fournir un scope_id.`

---

## Décision de design

Pour `constitution`, un `run_id` fourni par l'utilisateur doit court-circuiter toute exploration large du repo au démarrage.
