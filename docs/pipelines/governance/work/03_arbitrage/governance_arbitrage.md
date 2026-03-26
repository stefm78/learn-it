# Governance Arbitrage

## 1. Résumé exécutif

Le repo est opérable et aucune anomalie ne justifie une refonte ni un release patch.  
Les corrections immédiates doivent rester limitées à l’alignement de la couche `registry/` sur la réalité du repo.  
La séparation operating / releases / architecture / legacy doit être conservée telle quelle.  
Les `.bak` dans `docs/registry/` sont une ambiguïté visible à traiter sans chantier lourd.  
Le bruit terminal dans `repo_inventory.md` doit être nettoyé, mais c’est un point de qualité d’entrée, pas un sujet d’architecture.  
La doctrine patcher est suffisamment exploitable à court terme grâce aux alias canoniques déjà documentés.  
Les sujets de politique générale (`archive/`, exhaustivité du registre, doctrine complète des backups) sont à reporter.  
Le prochain patch doit donc être petit, documentaire, centré sur `pipelines.md` et `resources.md`.  
Aucun changement de `docs/cores/current/` ou `docs/cores/releases/` n’est requis à ce stade.  
Le passage au STAGE_04 est possible, mais dans un périmètre strictement limité.

## 2. Corrections à engager maintenant

### Point 1
- priorité : haute
- fichiers concernés : `docs/registry/pipelines.md`
- décision : correction nécessaire
- justification : le registre pipelines ne reflète pas exactement la portée réelle du repo ni du pipeline `governance` ; c’est une source de confusion directe pour la navigation humaine et IA
- type de traitement : patch standard

Décision détaillée :
- réaligner les `Global rules` sur les couches réellement gouvernées
- remplacer la référence générique à `archive/` par une formulation cohérente avec la séparation réelle autour de `legacy/`
- remonter `governance` dans `## Available pipelines` au même niveau que les autres pipelines

### Point 2
- priorité : haute
- fichiers concernés : `docs/registry/resources.md`
- décision : correction nécessaire
- justification : le registre des ressources contient des chemins legacy inexacts, omet des ressources réellement présentes, et emploie un libellé ambigu sur une zone legacy
- type de traitement : patch standard

Décision détaillée :
- corriger `legacy/referentiel/` en chemin réel sous `legacy/docs/referentiel/`
- ajouter les ressources réellement visibles dans `docs/patcher/shared/` qui servent à la navigation opératoire, notamment `apply_patch_v4.py`, `validate_patchset_v4.py` et `README.md`
- renommer `Legacy active Core location` vers un libellé explicitement non ambigu et non actif

### Point 3
- priorité : haute
- fichiers concernés :
  - `docs/registry/operating_model.md.bak`
  - `docs/registry/resources.md.bak`
- décision : correction nécessaire
- justification : ces fichiers sont des parasites visibles dans une couche d’autorité ; ils brouillent inutilement la source de vérité
- type de traitement : edit manuel limité

Décision détaillée :
- sortir ces `.bak` de `docs/registry/`
- soit les supprimer si inutiles
- soit les déplacer vers `legacy/` ou un espace de travail non autoritatif
- ne pas mobiliser de release patch pour ce point

### Point 4
- priorité : moyenne
- fichiers concernés : `docs/pipelines/governance/work/01_scan/repo_inventory.md`
- décision : correction nécessaire
- justification : le préfixe de contrôle terminal pollue une entrée de pipeline ; c’est un défaut de propreté opérationnelle, pas un problème de doctrine
- type de traitement : edit manuel limité

Décision détaillée :
- nettoyer le fichier actuel ou le régénérer proprement
- ne pas étendre ce point à une refonte du pipeline tant qu’aucune autre instabilité de scan n’est observée

## 3. Corrections à reporter

### Point 1 — Doctrine générale des patchers partagés
- raison du report : amélioration souhaitable, mais non prioritaire ; la situation est déjà praticable tant que les alias canoniques restent synchronisés avec v4
- impact : faible risque d’hésitation documentaire, sans blocage opérationnel immédiat
- condition de réouverture : réouvrir uniquement si un pipeline commence à référencer directement les variantes `v4`, si les alias canoniques divergent, ou si plusieurs opérateurs n’emploient plus les mêmes entrées par défaut

### Point 2 — Politique explicite sur les fichiers de sauvegarde
- raison du report : le cas visible peut être traité localement sans transformer immédiatement ce besoin en règle générale de gouvernance
- impact : risque modéré de réapparition future de `.bak` dans une zone autoritative
- condition de réouverture : réouvrir si de nouveaux backups réapparaissent hors `legacy/` ou hors espaces `work/`

### Point 3 — Clarification des chemins `archive/` dans `docs/registry/conventions.md`
- raison du report : sujet de cohérence documentaire réel mais mineur ; ces chemins peuvent relever d’une convention réservée et non d’un usage actif
- impact : légère ambiguïté de lecture sur les zones de versionnement documentaire
- condition de réouverture : réouvrir si des dossiers `archive/` sont effectivement instanciés ou si `conventions.md` est de toute façon retouché dans un patch voisin

### Point 4 — Doctrine de complétude de `resources.md`
- raison du report : amélioration souhaitable, mais non prioritaire ; le plus important est d’abord de corriger les omissions et ambiguïtés concrètes déjà visibles
- impact : de futures omissions peuvent rester discutables entre “oubli” et “choix éditorial”
- condition de réouverture : réouvrir si un prochain audit reproduit le même type d’écart malgré la correction immédiate

## 4. Points explicitement ignorés

### Point 1 — Écart verbal léger entre `docs/README.md` et `docs/registry/operating_model.md`
- raison : no_change ; les deux documents convergent sur le fond et racontent la même hiérarchie pratique, avec seulement un niveau de formulation différent
- risque accepté : hétérogénéité rédactionnelle mineure sans impact réel sur l’autorité du repo

### Point 2 — Besoin de requalifier davantage `docs/architecture/`
- raison : no_change ; le `README` qualifie déjà cette couche comme documentation de compréhension et non source de vérité
- risque accepté : faible risque de lecture trop large par un lecteur inattentif, jugé acceptable à ce stade

### Point 3 — Marquage supplémentaire des sous-zones legacy
- raison : non prioritaire ; la frontière principale `legacy/` est déjà claire et suffit pour la navigation par défaut
- risque accepté : ambiguïté locale possible en usage rétrospectif, mais pas de confusion structurelle majeure pour le repo courant

## 5. Périmètre du prochain patch

- mettre à jour `docs/registry/pipelines.md` pour :
  - réaligner les `Global rules` sur le repo réel
  - remplacer la logique `archive/` par une formulation cohérente avec `legacy/`
  - repositionner `governance` dans `## Available pipelines`
- mettre à jour `docs/registry/resources.md` pour :
  - corriger le chemin legacy du référentiel
  - ajouter les ressources partagées réellement présentes dans `docs/patcher/shared/`
  - supprimer le vocabulaire ambigu `Legacy active Core location`
- exclure explicitement du patch :
  - toute refonte d’architecture
  - tout changement dans `docs/cores/current/`
  - tout changement dans `docs/cores/releases/`
  - tout release patch
- traiter hors patch, par action manuelle limitée :
  - retrait/déplacement des `.bak` de `docs/registry/`
  - nettoyage de `docs/pipelines/governance/work/01_scan/repo_inventory.md`

## 6. Recommandation finale

YES_WITH_LIMITS
