# Patch DSL v2.5 — Spécification

## Objet

Le Patch DSL v2.5 est un langage déclaratif de migration contrôlée pour les Core YAML.
Il étend le Lot 1 avec des opérations plus fines sur les listes et sur le placement des objets,
sans devenir un éditeur YAML générique.

## Principes

1. **Atomicité** — un patch s'applique entièrement ou pas du tout.
2. **Déterminisme** — aucune cible ne doit être devinée.
3. **Traçabilité** — chaque patch est versionné, relisible, validable.
4. **Minimisation** — on modifie le moins possible.
5. **Sécurité** — le patcher refuse les opérations ambiguës ou dangereuses.

## Racine canonique

```yaml
PATCH_SET:
  id: PATCH_LEARNIT_XXXX
  patch_dsl_version: "2.5"
  atomic: true
  description: ...
  files:
    - file: Constitution_Learn-it_v1_7.yaml
      expected_core_id: CORE_LEARNIT_CONSTITUTION_V1_7
      operations:
        - op: assert
          target:
            section: TYPES
            id: TYPE_PATCH_ARTIFACT
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

## Opérations supportées — Lot 2

### `assert`
Vérifie l'existence d'une cible et, optionnellement, d'un champ interne.

### `append`
Ajoute un nouvel objet complet à une section.

### `replace`
Remplace un objet complet identifié par `id`.

### `replace_field`
Remplace un champ précis d'un objet existant.

Exemple :
```yaml
- op: replace_field
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
    field: logic.condition
  value: >
    Bornes respectées...
```

### `remove`
Supprime un objet, sauf s'il reste référencé.

### `rename`
Renomme l'id d'un objet.
En v2.5, les références ne sont toujours pas réécrites automatiquement.
Le patcher valide ensuite la cohérence locale.

### `append_field_list`
Ajoute un item à un champ liste interne.

Exemple :
```yaml
- op: append_field_list
  target:
    section: RULES
    id: RULE_X
    field: depends_on
  value: INV_Y
```

Options :
- `create_missing: true|false`
- `unique: true|false` (défaut `true`)

### `remove_field_list_item`
Supprime un item d'un champ liste interne.

Exemple :
```yaml
- op: remove_field_list_item
  target:
    section: RULES
    id: RULE_X
    field: depends_on
  value: INV_OLD
```

Options :
- `all_matches: true|false` (défaut `false`)

### `move`
Déplace un objet d'une section à une autre dans le même fichier.

Exemple :
```yaml
- op: move
  target:
    section: PARAMETERS
    id: PARAM_X
  destination:
    section: TYPES
```

### `ensure_exists`
Ajoute un objet seulement s'il n'existe pas déjà.

### `ensure_absent`
Vérifie qu'un objet est absent.
Optionnellement, peut le supprimer avec `remove_if_present: true`.

### `note`
Ne modifie rien ; documente un point non patchable directement.

### `no_change`
Déclare explicitement qu'aucun changement n'est requis pour ce fichier.

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
1. `expected_core_id` cohérent
2. sections valides
3. pas de doublons d'id
4. suppression non référencée
5. renommage sans collision
6. références locales encore résolues après patch
7. `core_type` cohérent avec le fichier cible
8. `move` ne crée pas un mauvais placement évident de `core_type`

## Compatibilité

Le patcher v2.5 reste compatible avec les patchsets v2.0/legacy qui utilisent seulement :
- `assert`
- `append`
- `replace`
- `replace_field`
- `remove`
- `rename`
- `note`
- `no_change`
