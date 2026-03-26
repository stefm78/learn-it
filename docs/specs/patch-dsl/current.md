# Patch DSL v4

## Objectif

Le Patch DSL sert à décrire des transformations sûres, atomiques et auditables sur les Core Learn-it.

## Principes

- un patch doit être déterministe ;
- un patch doit être validable avant application ;
- un patch doit être applicable en dry-run ;
- un patch doit pouvoir produire un rapport d'exécution ;
- un patch ne doit jamais introduire de logique implicite.

## Structure canonique

```yaml
PATCH_SET:
  id:
  patch_dsl_version: "4.0"
  atomic: true
  description:
  files:
    - file:
      expected_core_id:
      operations:
```

## Opérations supportées

### Noyau
- `assert`
- `append`
- `replace`
- `replace_field`
- `remove`
- `rename`
- `no_change`
- `note`

### Niveau 2
- `append_field_list`
- `remove_field_list_item`
- `move`
- `ensure_exists`
- `ensure_absent`

### Niveau 3 / méta
- `assert_meta`
- `replace_meta_field`
- `rewrite_references`
- `replace_text`

## replace_text

Permet une réécriture textuelle contrôlée avec scope explicite.

Scopes autorisés :
- `meta_field`
- `object_field`
- `section_fields`
- `all_strings`

## Garde-fous

- validation du `expected_core_id`
- refus des sections inconnues
- refus des ids dupliqués
- refus des suppressions encore référencées
- refus des collisions de renommage
- vérification des références cassées après patch
- cohérence `core_type` / fichier cible

## Atomicité

Si `atomic: true`, aucune écriture n'a lieu tant que toutes les opérations et validations n'ont pas réussi.

## Rapport d'exécution

Le patcher peut produire un rapport YAML décrivant :
- les fichiers touchés ;
- les opérations exécutées ;
- les remplacements textuels ;
- les validations post-patch ;
- le statut final.

## Règle d'usage

Le Patch DSL décrit comment modifier.
Il ne remplace ni le challenge, ni l'arbitrage, ni la validation logique des Core.
