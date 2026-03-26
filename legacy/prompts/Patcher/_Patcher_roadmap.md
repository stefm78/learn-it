Voici la suite concrète : **Patch DSL v2** puis **patcher v2**.

# 1) Spécification Patch DSL v2

## 1.1 Objectif

Le Patch DSL v2 sert à modifier des Cores YAML de manière :

* expressive,
* déterministe,
* transactionnelle,
* validable,
* réversible.

Il ne doit pas être un éditeur YAML générique.
Il doit être un **langage de migration contrôlée pour vos Cores**.

---

## 1.2 Principes

### P1 — atomicité

Un patch est appliqué entièrement ou pas du tout.

### P2 — déterminisme

Une opération doit produire exactement un résultat attendu.

### P3 — explicitation

Aucune cible ne doit être “devinée”.

### P4 — traçabilité

Le patch doit être lisible, versionné, auditable.

### P5 — minimisation

On modifie le moins possible.

### P6 — sûreté

Le patcher doit refuser un patch ambigu, incomplet ou dangereux.

---

## 1.3 Structure canonique

```yaml
PATCH_SET:
  id: PATCH_LEARNIT_XXXX
  patch_dsl_version: "2.0"
  atomic: true
  description: ...
  files:
    - file: ...
      expected_core_id: ...
      operations:
        - op: ...
```

---

## 1.4 Métadonnées obligatoires

### Au niveau `PATCH_SET`

* `id`
* `patch_dsl_version`
* `atomic`
* `description`
* `files`

### Au niveau `file`

* `file`
* `expected_core_id`
* `operations`

### Au niveau `operation`

* `op`
* `target` sauf pour `no_change`
* champs additionnels selon l’opération

---

# 2) Modèle cible des fichiers Core

Le patcher v2 doit connaître explicitement les sections autorisées :

```yaml
TYPES
INVARIANTS
RULES
PARAMETERS
DEPENDENCIES
CONSTRAINTS
EVENTS
ACTIONS
```

Et accepter les deux racines :

* racine directe
* racine `CORE:`

---

# 3) Opérations Patch DSL v2

## 3.1 `assert`

Vérifie un prérequis.
Ne modifie rien.

### But

* garantir qu’un objet existe avant modification
* garantir qu’une section existe
* verrouiller une hypothèse structurelle

### Exemple

```yaml
- op: assert
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
```

### Échec

Le patch entier échoue si `atomic: true`.

---

## 3.2 `append`

Ajoute un nouvel objet dans une section.

### Exemple

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

### Règles

* refuse si l’id existe déjà
* sauf si mode explicitement permissif, ce que je déconseille

---

## 3.3 `replace`

Remplace un objet entier identifié par `id`.

### Exemple

```yaml
- op: replace
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
  value:
    ...
```

### Usage

À utiliser quand l’objet change substantiellement.

---

## 3.4 `replace_field`

Remplace un champ précis d’un objet existant.

### Exemple

```yaml
- op: replace_field
  target:
    section: TYPES
    id: TYPE_PATCH_ARTIFACT
    field: logic.condition
  value: >
    Bornes respectées...
```

### Support requis

* chemins par points
* ex. `logic.condition`
* ex. `human_readable`
* ex. `relations`

### Usage

Très utile pour :

* ajuster `depends_on`
* corriger un `source_anchor`
* mettre à jour une condition
* renommer version/description sans réécrire l’objet complet

---

## 3.5 `remove`

Supprime un objet d’une section.

### Exemple

```yaml
- op: remove
  target:
    section: RULES
    id: RULE_OLD
```

### Règle de sécurité

Par défaut, le patcher doit vérifier si l’objet supprimé est référencé ailleurs.

Deux modes possibles :

* strict : refuse si référencé
* forcé : autorise seulement avec `force: true`

Je recommande le mode strict par défaut.

---

## 3.6 `rename`

Renomme l’id d’un objet.

### Exemple

```yaml
- op: rename
  target:
    section: PARAMETERS
    id: PARAM_OLD
  new_id: PARAM_NEW
```

### Danger

Le renommage casse les références si elles ne sont pas propagées.

### Recommandation

Deux comportements possibles :

#### a. `rename` simple

Renomme seulement l’objet.
Le patch doit alors inclure explicitement les `replace_field` nécessaires.

#### b. `rename` + `rewrite_references`

Plus pratique, mais plus complexe.

Je recommande :

* v2 minimale : `rename` simple
* v3 : `rename` avec propagation optionnelle

---

## 3.7 `append_field_list`

Ajoute un élément à une liste interne.

### Exemple

```yaml
- op: append_field_list
  target:
    section: INVARIANTS
    id: INV_X
    field: depends_on
  value: TYPE_NEW
```

Ou pour `relations` :

```yaml
- op: append_field_list
  target:
    section: RULES
    id: RULE_X
    field: relations
  value:
    type: requires
    target:
      id: INV_Y
```

### Usage

Beaucoup plus propre que `replace` sur tout l’objet.

---

## 3.8 `remove_field_list_item`

Supprime un élément d’une liste interne.

### Exemple

```yaml
- op: remove_field_list_item
  target:
    section: RULES
    id: RULE_X
    field: depends_on
  value: TYPE_OLD
```

---

## 3.9 `move`

Déplace un objet d’une section à une autre.

### Exemple

```yaml
- op: move
  target:
    section: PARAMETERS
    id: PARAM_X
  destination:
    section: TYPES
```

### Usage

Utile pour corriger des mauvais placements.

### Règle

* l’id reste identique
* la section source doit contenir l’objet
* la section destination ne doit pas contenir le même id

---

## 3.10 `ensure_exists`

Ajoute un objet seulement s’il n’existe pas.

### Exemple

```yaml
- op: ensure_exists
  target:
    section: PARAMETERS
    id: PARAM_X
  value:
    ...
```

### Usage

Pratique pour des patchs ré-exécutables.

---

## 3.11 `ensure_absent`

Vérifie qu’un objet n’existe pas, ou le supprime si politique permissive.

Je recommande :

* v2 : mode vérification seulement

### Exemple

```yaml
- op: ensure_absent
  target:
    section: RULES
    id: RULE_DEPRECATED
```

---

## 3.12 `merge_fields`

Fusionne partiellement un objet.

### Exemple

```yaml
- op: merge_fields
  target:
    section: TYPES
    id: TYPE_X
  value:
    patchable: false
    parameterizable: true
```

### Usage

Pratique, mais potentiellement ambigu.

Je le mettrais plutôt en v3, pas en v2 minimale.

---

## 3.13 `note`

Ne modifie rien ; documente une action non patchable directement.

### Exemple

```yaml
- op: note
  target:
    section: RULES
    id: RULE_X
  value:
    reason: "Conflit logique à arbitrer"
```

---

## 3.14 `no_change`

Déclare explicitement qu’aucune modification n’est requise.

---

# 4) Niveaux de version du patcher

## v2 minimale

Supporte :

* `assert`
* `append`
* `replace`
* `replace_field`
* `remove`
* `rename`
* `note`
* `no_change`
* `atomic`

## v2.5 utile

Ajoute :

* `append_field_list`
* `remove_field_list_item`
* `ensure_exists`
* `ensure_absent`
* `move`

## v3

Ajoute :

* `rewrite_references`
* `merge_fields`
* transactions multi-op plus riches
* rollback détaillé
* plan d’exécution / preview complet

---

# 5) Sémantique transactionnelle

## 5.1 `atomic: true`

Si une opération échoue :

* aucun fichier n’est écrit.

### Implémentation

* charger tous les fichiers en mémoire
* appliquer toutes les opérations sur copies
* faire les validations post-patch
* écrire seulement si tout passe

## 5.2 `atomic: false`

Je déconseille fortement ce mode, sauf debug local.

---

# 6) Garde-fous obligatoires du patcher

## 6.1 Préchecks

Avant toute écriture :

* fichier existe
* YAML chargeable
* `expected_core_id` cohérent
* sections valides
* ids présents si requis
* aucune opération inconnue

## 6.2 Contrôles structurels

Après patch mémoire :

* pas de doublon d’id dans une même section
* pas de section invalide
* champs obligatoires présents sur tout nouvel objet
* `core_type` cohérent avec le fichier cible

## 6.3 Contrôles de cohérence minimale

Je recommande au moins :

* toutes les références `depends_on` pointent vers un id existant ou un ref_core connu
* toutes les `relations.target.id` pointent vers un id existant ou un ref_core connu
* pas de suppression d’objet encore référencé
* pas de `rename` collision

## 6.4 Contrôles inter-Core

Optionnels mais très utiles :

* le LINK ne doit pas porter de logique métier autonome
* les objets `core_type: CONSTITUTION` n’atterrissent pas dans le Référentiel
* symétriquement pour REFERENTIEL / LINK

---

# 7) Spécification de `replace_field`

C’est l’opération la plus utile.

## 7.1 Champ cible

Le champ est défini par un chemin :

* `human_readable`
* `logic.condition`
* `logic.effect`
* `relations`
* `depends_on`

## 7.2 Règle

* tous les segments intermédiaires doivent exister, sauf si `create_missing: true`
* par défaut, je conseille `create_missing: false`

## 7.3 Exemple

```yaml
- op: replace_field
  target:
    section: CONSTRAINTS
    id: CONSTRAINT_REFERENTIEL_LOCAL_VERIFICATION_REQUIRED_BEFORE_PATCH_APPLY
    field: logic.effect
  value: >
    Vérification locale déterministe requise...
```

---

# 8) Spécification de `rename`

## 8.1 Forme

```yaml
- op: rename
  target:
    section: PARAMETERS
    id: PARAM_OLD
  new_id: PARAM_NEW
```

## 8.2 Préconditions

* l’ancien id existe
* le nouvel id n’existe pas dans la section cible

## 8.3 Effet

* change l’id de l’objet
* ne réécrit pas automatiquement les références en v2 minimale

## 8.4 Bonne pratique

Toujours faire précéder d’un `assert`.

---

# 9) Spécification de `remove`

## 9.1 Forme

```yaml
- op: remove
  target:
    section: RULES
    id: RULE_OLD
```

## 9.2 Préconditions

* l’objet existe
* aucune référence active ne le cible

## 9.3 Variante

```yaml
force: true
```

Je déconseille au début.

---

# 10) Format recommandé pour `Make05CorePatch.md`

Pour être compatible avec le patcher v2, le prompt doit demander ce format exact :

```yaml
PATCH_SET:
  id: ...
  patch_dsl_version: "2.0"
  atomic: true
  description: ...
  files:
    - file: ...
      expected_core_id: ...
      operations:
        - op: assert
          target:
            section: ...
            id: ...
        - op: replace_field
          target:
            section: ...
            id: ...
            field: ...
          value: ...
```

---

# 11) Pipeline final détaillé

## Étape 1 — Challenge

Entrées :

* Constitution
* Référentiel
* LINK

Sortie :

* audit critique structuré

Prompt :

* `Challenge_constitution.md`

---

## Étape 2 — Arbitrage

Entrée :

* audit

Sortie :

* liste des corrections retenues / rejetées

Mode :

* humain ou prompt d’arbitrage

---

## Étape 3 — Synthesis patch

Entrées :

* les 3 cores
* l’audit
* l’arbitrage

Prompt :

* `Make05CorePatch.md`

Sortie :

* `patchset.yaml`

---

## Étape 4 — Validation du patch

Entrée :

* `patchset.yaml`

Prompt :

* `Make06PatchValidation.md`

Sortie :

* PASS / FAIL patch-level

---

## Étape 5 — Dry run technique

Commande :

```bash
python apply_learnit_core_patch_v2.py patchset.yaml . true
```

Sortie :

* journal d’applicabilité
* aucun fichier écrit

---

## Étape 6 — Application réelle

Commande :

```bash
python apply_learnit_core_patch_v2.py patchset.yaml . false
```

Sortie :

* backups
* fichiers patchés

---

## Étape 7 — Validation Core

Entrées :

* cores patchés

Prompt :

* `Make02CoreValidation.md`

Sortie :

* PASS / FAIL structurel et logique

---

## Étape 8 — Release

Entrées :

* cores patchés validés

Prompt :

* `Make07CoreRelease.md`

Sortie :

* bump de version
* renommages internes
* sync inter-core
* note de release

---

# 12) Schéma du pipeline

```text
[Constitution.yaml]   [Referentiel.yaml]   [Link.yaml]
          \                 |                 /
           \                |                /
            ---- Challenge_constitution.md ----
                           |
                        [Audit]
                           |
                      [Arbitrage]
                           |
                    Make05CorePatch.md
                           |
                      [PATCH_SET YAML]
                           |
                 Make06PatchValidation.md
                           |
                 [PASS patch-level ?]
                           |
                apply_learnit_core_patch_v2.py
                     |                |
                  dry-run          apply
                     |                |
                     ------[Patched Cores]------
                                   |
                        Make02CoreValidation.md
                                   |
                            [PASS / FAIL]
                                   |
                           Make07CoreRelease.md
                                   |
                              [Release Plan]
```

---

# 13) Priorité d’implémentation

Je vous conseille cet ordre :

### Lot 1

* spécification Patch DSL v2
* `Make05CorePatch.md`
* patcher v2 avec :

  * `assert`
  * `replace_field`
  * `remove`
  * `rename`
  * `atomic`

### Lot 2

* `Make06PatchValidation.md`
* `append_field_list`
* `remove_field_list_item`
* `move`

### Lot 3

* `Make07CoreRelease.md`
* propagation optionnelle de références
* reporting enrichi

---

# 14) Résultat attendu après cette évolution

Vous pourrez passer de :

> “le challenge détecte des problèmes, puis on les retraduit à la main”

à :

> “le challenge alimente un patch formel, que le moteur applique et que la validation contrôle”.

C’est exactement ce qu’il faut pour rendre les Cores beaucoup plus faciles à faire évoluer par IA sans tomber dans l’arbitraire.

## Étape suivante logique

Je peux maintenant vous donner directement la **v2 du patcher Python**, avec support de :

* `assert`
* `replace_field`
* `remove`
* `rename`
* `atomic`
