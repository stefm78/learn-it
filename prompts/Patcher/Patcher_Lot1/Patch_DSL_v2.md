# Patch DSL v2 — Spécification

## Objet

Le Patch DSL v2 est un langage déclaratif de migration contrôlée pour les Core YAML.
Il vise à permettre des modifications fines et auditables, sans transformer le patcher en éditeur YAML générique.

## Principes

1. **Atomicité** — un patch s'applique entièrement ou pas du tout.
2. **Déterminisme** — aucune cible ne doit être devinée.
3. **Traçabilité** — chaque patch est versionné, relisible, validable.
4. **Minimisation** — on modifie le moins possible.
5. **Sécurité** — le patcher doit refuser les opérations ambiguës ou dangereuses.

## Racine canonique

```yaml
PATCH_SET:
  id: PATCH_LEARNIT_XXXX
  patch_dsl_version: "2.0"
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

Le patcher cible uniquement les sections Core suivantes :

- `TYPES`
- `INVARIANTS`
- `RULES`
- `PARAMETERS`
- `DEPENDENCIES`
- `CONSTRAINTS`
- `EVENTS`
- `ACTIONS`

Les fichiers peuvent être à racine directe ou encapsulés sous `CORE:`.

## Opérations supportées — Lot 1

### `assert`
Vérifie l'existence d'une cible avant la suite du patch.

```yaml
- op: assert
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
```

Options :
- `field` : vérifie aussi qu'un champ interne existe (`logic.condition`, etc.)

### `append`
Ajoute un nouvel objet à une section.

```yaml
- op: append
  target:
    section: INVARIANTS
  value:
    id: INV_NEW
    authority: primary
    core_type: CONSTITUTION
    source_anchor: "[PATCH]"
    depends_on: []
    relations: []
    patchable: false
    parameterizable: false
    human_readable: ...
    logic:
      trigger: ...
      condition: ...
      effect: ...
      scope: ...
```

Variantes autorisées :
- `value`
- `values` (liste)

### `replace`
Remplace un objet complet identifié par `id`.

```yaml
- op: replace
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
  value:
    ...
```

### `replace_field`
Remplace un champ précis d'un objet existant.

```yaml
- op: replace_field
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
    field: logic.condition
  value: >
    Bornes respectées, impact_scope calculable...
```

Options :
- `create_missing: true|false` — par défaut `false`

### `remove`
Supprime un objet d'une section.

```yaml
- op: remove
  target:
    section: RULES
    id: RULE_OLD_DEPRECATED
```

Règle de sécurité :
- le patcher refuse la suppression si l'objet est encore référencé.

### `rename`
Renomme l'id d'un objet.

```yaml
- op: rename
  target:
    section: PARAMETERS
    id: PARAM_OLD
  new_id: PARAM_NEW
```

Règles :
- l'ancien id doit exister
- le nouvel id ne doit pas exister
- en v2, les références ne sont **pas** réécrites automatiquement
- le patcher vérifie après patch que les références restantes sont cohérentes

### `note`
Ne modifie rien ; documente un point non patchable directement.

### `no_change`
Déclare explicitement qu'aucun changement n'est requis pour ce fichier.

## Champs obligatoires pour les nouveaux objets Core

Pour toute nouvelle entrée ajoutée dans une section Core, inclure :

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
7. `core_type` cohérent avec le fichier cible :
   - Constitution → `CONSTITUTION`
   - Référentiel → `REFERENTIEL`
   - LINK → `LINK`

## Notes de compatibilité

Le patcher v2 doit rester compatible avec les patchsets v1 existants :
- `patch_dsl_version` absent → accepté avec warning
- `append` avec `values` → accepté

## Recommandation de pipeline

1. `Challenge_constitution.md` → audit
2. arbitrage humain ou semi-automatique
3. `Make05CorePatch.md` → `PATCH_SET`
4. dry-run patcher v2
5. application patcher v2
6. `Make02CoreValidation.md`
7. release / bump de version
