# Patch DSL v3.0 — Spécification

## Objet

Le Patch DSL v3.0 étend le Lot 2 avec deux capacités critiques pour la maintenance réelle des Core :
- la **propagation contrôlée des renommages et références** ;
- l'édition des **métadonnées de Core** (`CORE.id`, `CORE.version`, `CORE.description`, etc.).

L'objectif n'est toujours pas de devenir un éditeur YAML générique, mais un langage de migration
contrôlée pour les Core Learn-it.

## Principes

1. **Atomicité** — un patch s'applique entièrement ou pas du tout.
2. **Déterminisme** — aucune cible ne doit être devinée.
3. **Traçabilité** — chaque patch est versionné, relisible, validable.
4. **Minimisation** — on modifie le moins possible.
5. **Sécurité** — le patcher refuse les opérations ambiguës ou dangereuses.
6. **Propagation explicite** — un renommage n'implique jamais une réécriture implicite non déclarée.

## Racine canonique

```yaml
PATCH_SET:
  id: PATCH_LEARNIT_XXXX
  patch_dsl_version: "3.0"
  atomic: true
  description: ...
  files:
    - file: Constitution_Learn-it_v1_7.yaml
      expected_core_id: CORE_LEARNIT_CONSTITUTION_V1_7
      operations:
        - op: assert_meta
          target:
            field: id
```

## Sections supportées

- `TYPES`
- `INVARIANTS`
- `RULES`
- `PARAMETERS`
- `DEPENDENCIES`
- `CONSTRAINTS`
- `EVENTS`
- `ACTIONS`

Les fichiers peuvent être à racine directe ou encapsulés sous `CORE:`.

## Opérations supportées — v3.0

### Héritées de v2.5
- `assert`
- `append`
- `replace`
- `replace_field`
- `remove`
- `rename`
- `append_field_list`
- `remove_field_list_item`
- `move`
- `ensure_exists`
- `ensure_absent`
- `note`
- `no_change`

### Nouvelles opérations Lot 3

#### `assert_meta`
Vérifie l'existence ou la valeur d'un champ de métadonnée au niveau racine du Core.

Exemple :
```yaml
- op: assert_meta
  target:
    field: id
  equals: CORE_LEARNIT_CONSTITUTION_V1_6
```

#### `replace_meta_field`
Remplace un champ de métadonnée au niveau racine du Core.

Exemple :
```yaml
- op: replace_meta_field
  target:
    field: version
  value: V1_7_FINAL
```

#### `rewrite_references`
Réécrit explicitement les références locales exactes d'un `old_id` vers un `new_id` dans le fichier courant.

Par défaut, la réécriture porte sur :
- `depends_on`
- `relations[].target.id`

Exemple :
```yaml
- op: rewrite_references
  target:
    old_id: LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_6
    new_id: LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_7
```

Options :
- `rewrite_depends_on: true|false` (défaut `true`)
- `rewrite_relations: true|false` (défaut `true`)
- `rewrite_text_fields:` liste de chemins texte à réécrire par substitution exacte ou textuelle

Exemple avec champs texte :
```yaml
- op: rewrite_references
  target:
    old_id: CORE_LEARNIT_CONSTITUTION_V1_6
    new_id: CORE_LEARNIT_CONSTITUTION_V1_7
  rewrite_text_fields:
    - description
```

## Champs obligatoires pour les nouveaux objets complets

Pour toute nouvelle entrée Core complète :
- `id`
- `authority`
- `core_type`
- `source_anchor`
- `depends_on`
- `relations`
- `patchable`
- `parameterizable`
- `human_readable`
- `logic`

## Validation minimale après patch

Le patcher doit contrôler au minimum :
1. `expected_core_id` cohérent avec le résultat final du fichier
2. sections valides
3. pas de doublons d'id
4. suppression non référencée
5. renommage sans collision
6. références locales encore résolues après patch
7. `core_type` cohérent avec le fichier cible
8. `rewrite_references` limité au fichier courant sauf patch déclaré dans les autres fichiers
9. les champs meta ciblés existent ou sont créables selon l'opération

## Cas d'usage visés

- bump de version interne des Core
- renommage des `REF_CORE_*` et `LINK_REF_CORE_*`
- synchronisation des bindings LINK après montée de version
- réécriture contrôlée des références locales après `rename`
- préparation d'une release cohérente sans édition manuelle large
