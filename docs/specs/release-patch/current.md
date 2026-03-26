# Release Patch DSL v1

## Objectif

Le Release Patch DSL décrit des opérations de promotion et de synchronisation au niveau du dépôt.
Il sert à finaliser une release ou une promotion de branche en remplaçant des artefacts provisoires par des artefacts canoniques.

## Portée

Le Release Patch DSL s'applique aux fichiers du repo, pas au contenu logique interne des Core.
Il complète le Patch DSL v4, qui reste le DSL de transformation des Core.

## Principes

- atomicité : tout passe ou rien ne s'écrit ;
- explicitation : aucune cible ne doit être devinée ;
- promotion contrôlée : toute bascule vers `current/` est traçable ;
- compatibilité : les artefacts legacy sont conservés tant que la promotion n'est pas validée ;
- auditabilité : chaque promotion doit produire un rapport.

## Structure canonique

```yaml
RELEASE_PATCH_SET:
  id:
  version: "1.0"
  atomic: true
  description:
  operations:
```

## Opérations supportées

### promote_file
Copie le contenu d'un fichier source vers une destination canonique.

```yaml
- op: promote_file
  from: docs/cores/releases/constitution_v1_7.yaml
  to: docs/cores/current/constitution.yaml
```

### sync_copy
Copie un fichier source vers une destination secondaire de manière déclarative.

```yaml
- op: sync_copy
  from: docs/patcher/shared/apply_patch_v4.py
  to: docs/patcher/shared/apply_patch.py
```

### replace_text
Réécrit du texte dans un fichier markdown, yaml ou script texte.

```yaml
- op: replace_text
  file: docs/architecture/Passage2_Promotion_Status.md
  old: restent des pointeurs descriptifs
  new: sont désormais des copies canoniques promues
```

### assert_file_exists
Vérifie qu'un fichier existe avant promotion.

```yaml
- op: assert_file_exists
  path: docs/cores/releases/referentiel_v0_6.yaml
```

### assert_file_contains
Vérifie qu'un fichier contient un fragment textuel attendu.

```yaml
- op: assert_file_contains
  path: docs/cores/releases/link_v1_7__v0_6.yaml
  text: CORE_LINK_LEARNIT_CONSTITUTION_V1_7__REFERENTIEL_V0_6
```

### note
N'écrit rien ; documente un choix ou une limite.

### no_change
Déclare explicitement qu'aucun changement n'est requis.

## Garde-fous

- toute source d'une promotion doit exister ;
- `promote_file` et `sync_copy` refusent un contenu vide ;
- `replace_text` échoue si la cible n'existe pas ;
- `replace_text` peut être strict ou permissif ;
- le moteur doit pouvoir produire un rapport YAML ;
- si `atomic: true`, aucun fichier n'est écrit tant que toutes les opérations n'ont pas réussi.

## Rapport d'exécution

Le moteur de release patch doit produire un rapport YAML indiquant :
- les opérations exécutées ;
- les fichiers promus ;
- les fichiers synchronisés ;
- les remplacements textuels ;
- le statut final.

## Usage recommandé

1. produire un `RELEASE_PATCH_SET` depuis le pipeline `release`
2. valider ce patch avec un validateur dédié
3. l'appliquer en dry-run
4. l'appliquer en réel
5. relire le rapport d'exécution
