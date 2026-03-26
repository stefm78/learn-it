# Patch DSL v4

## Objectif

Patch DSL v4 étend le DSL v3 avec deux capacités majeures :

1. **réécriture textuelle contrôlée** dans les métadonnées et dans les champs texte des objets Core ;
2. **reporting enrichi d’exécution**, exploitable pour audit, CI et release notes.

Le DSL reste :
- déterministe,
- atomique,
- auditable,
- centré sur les Cores,
- plus puissant sans devenir un éditeur YAML libre.

## Principes

- atomicité totale du patch ;
- cibles explicites ;
- validation avant écriture ;
- reporting structuré ;
- minimisation des changements ;
- refus des opérations ambiguës.

## Structure canonique

```yaml
PATCH_SET:
  id: PATCH_EXAMPLE_V4
  patch_dsl_version: "4.0"
  atomic: true
  description: Exemple Lot 4
  report:
    enabled: true
    path: patch_execution_report.yaml
  files:
    - file: Constitution.yaml
      expected_core_id: CORE_LEARNIT_CONSTITUTION_V1_7
      operations:
        - op: assert
          target:
            section: TYPES
            id: TYPE_PATCH_ARTIFACT
```

## Opérations supportées

Compatibilité ascendante :
- assert
- append
- replace
- replace_field
- remove
- rename
- append_field_list
- remove_field_list_item
- move
- ensure_exists
- ensure_absent
- assert_meta
- replace_meta_field
- rewrite_references
- note
- no_change

Ajout v4 :
- replace_text

## replace_text

`replace_text` permet de modifier du texte dans une cible strictement définie.

### Modes de ciblage

#### 1. meta_field
```yaml
- op: replace_text
  target:
    scope: meta_field
    field: description
  old: "v1.6"
  new: "v1.7"
```

#### 2. object_field
```yaml
- op: replace_text
  target:
    scope: object_field
    section: INVARIANTS
    id: INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC
    field: human_readable
  old: "acyclique"
  new: "strictement acyclique"
```

#### 3. section_fields
```yaml
- op: replace_text
  target:
    scope: section_fields
    section: RULES
    fields:
      - human_readable
      - logic.effect
  old: "temporaire"
  new: "bornée"
```

#### 4. all_strings
```yaml
- op: replace_text
  target:
    scope: all_strings
    include_meta: true
  old: "V1_6"
  new: "V1_7"
```

### Modes de remplacement

#### Littéral
```yaml
old: "foo"
new: "bar"
```

#### Regex
```yaml
regex: true
pattern: "V1_(6|7)"
replacement: "V1_8"
```

### Garde-fous
- `require_match: true|false`
- `max_replacements: <int>` optionnel
- `section_fields` doit lister explicitement les champs autorisés
- `all_strings` est puissant ; à réserver aux opérations de gouvernance/versioning

## Reporting

Le patcher v4 peut produire un rapport YAML :

```yaml
PATCH_EXECUTION_REPORT:
  patch_id: ...
  patch_dsl_version: "4.0"
  atomic: true
  whatif: true
  status: PASS
  files:
    - file: ...
      expected_core_id: ...
      actual_core_id: ...
      changed: true
      backups_created: []
      operations:
        - op: replace_text
          status: applied
          message: "replace_text object_field ..."
  summary:
    files_total: 3
    files_changed: 2
    operations_total: 9
    operations_applied: 7
    operations_skipped: 2
```

Le chemin du rapport peut venir :
- du champ `PATCH_SET.report.path`,
- ou d’un argument CLI explicite.

## CLI recommandée

```bash
python apply_learnit_core_patch_v4.py ./patchset_v4.yaml . true
python apply_learnit_core_patch_v4.py ./patchset_v4.yaml . false ./patch_execution_report.yaml
```

## Cas d’usage Lot 4

- propagation large des changements de version ;
- renommage assisté de références textuelles ;
- préparation de release notes ;
- exécution CI avec rapport machine-lisible ;
- revue de patch plus fine avant commit.
