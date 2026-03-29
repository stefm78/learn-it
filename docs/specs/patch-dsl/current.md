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
  federation:
    CORE_REF_ALIAS:
      file:
      expected_core_id:
  files:
    - file:
      expected_core_id:
      operations:
```

## Fédération inter-Core

Le bloc `federation` est optionnel.

Il devient requis dès qu'un patch référence explicitement, depuis un Core, un objet situé dans un autre Core.

Chaque entrée de `federation` déclare :

- un alias de Core (`REF_CORE_*` ou `LINK_REF_CORE_*`) ;
- le fichier canonique à ouvrir dans la racine d'application ;
- le `expected_core_id` attendu pour verrouiller la résolution.

Exemple :

```yaml
federation:
  LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_7:
    file: docs/cores/current/constitution.yaml
    expected_core_id: CORE_LEARNIT_CONSTITUTION_V1_7
  LINK_REF_CORE_LEARNIT_REFERENTIEL_V0_6:
    file: docs/cores/current/referentiel.yaml
    expected_core_id: CORE_LEARNIT_REFERENTIEL_V0_6
```

## Références inter-Core qualifiées

### Forme chaîne

Dans `depends_on` ou dans `relations.target.id`, une référence inter-Core fine s'écrit :

```yaml
LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_7::TYPE_STATE_AXIS_ACTIVATION
```

La partie gauche est l'alias déclaré dans `federation`.
La partie droite est l'id de l'objet cible dans le Core externe.

### Forme structurée

Dans une relation, on peut aussi écrire :

```yaml
relations:
  - type: binds
    target:
      core_ref: LINK_REF_CORE_LEARNIT_REFERENTIEL_V0_6
      id: RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER
```

Cette forme est strictement équivalente à la forme chaîne.
Elle est recommandée quand la cible externe doit rester visuellement explicite.

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
- validation des alias déclarés dans `federation`
- validation des références inter-Core qualifiées contre les Core réellement ouverts

## Dry-run exécutable

Le dry-run n'est pas un simple contrôle de forme.
Il doit vérifier que :

- toutes les opérations sont applicables ;
- les références locales restent résolubles ;
- les références inter-Core qualifiées restent résolubles via `federation` ;
- l'application réelle pourra être exécutée sans modification implicite supplémentaire.

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
