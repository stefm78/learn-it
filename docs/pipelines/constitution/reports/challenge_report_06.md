# Core Validation Report — STAGE_06

**Pipeline:** constitution  
**Stage:** STAGE_06_CORE_VALIDATION  
**Prompt appliqué :** `docs/prompts/shared/Make02CoreValidation.md`  
**Cores validés :**
- `docs/pipelines/constitution/work/05_apply/patched/constitution.yaml`
- `docs/pipelines/constitution/work/05_apply/patched/referentiel.yaml`
- `docs/pipelines/constitution/work/05_apply/patched/link.yaml`

---

## Résultat global

```yaml
VALIDATION:
  status: FAIL
  anomalies:
    - id: ANO_06_01
      severity: BLOQUANT
      core: REFERENTIEL (patché)
      test: "11 — références inter-Core explicites"
      description: >
        L'ID de référence inter-Core vers la Constitution est toujours
        REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL dans le fichier
        patché work/05_apply/patched/referentiel.yaml.
        Le human_readable indique également « v1.7 » alors que la Constitution
        active est CORE_LEARNIT_CONSTITUTION_V1_8.
        Toutes les dépendances du Référentiel (TYPES, INVARIANTS, RULES)
        pointent vers cet ID v1.7, rendant la chaîne d'autorité inter-Core
        incohérente dans la version patchée.
    - id: ANO_06_02
      severity: BLOQUANT
      core: REFERENTIEL (patché)
      test: "12 — absence de collision d'id"
      description: >
        Le Référentiel patché contient encore l'ID
        REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL.
        Si un renommage en V1_8 était prévu par le patch,
        il n'a pas été appliqué. L'ID V1_7 coexiste avec le
        CORE_ID de la Constitution qui est V1_8, créant une
        asymétrie structurelle auditable.
    - id: ANO_06_03
      severity: BLOQUANT
      core: REFERENTIEL (patché)
      test: "2 — aucune dépendance orpheline"
      description: >
        TYPE_REFERENTIEL_GRAPH_PROPAGATION_OPERATIONAL_NOTE déclare
        une relation derives_from vers REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL.
        Si ce nœud doit pointer vers V1_8 après patch, cette relation
        pointe vers un nœud ID qui ne correspond plus à la référence
        canonique attendue en V1_8. La dépendance est résolvable
        localement mais incohérente inter-Core.
  corrections:
    - id: COR_06_01
      cible: REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL
      action: >
        Renommer l'ID en REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL
        dans le Référentiel patché et propager la réécriture de toutes
        les références dépendantes via rewrite_references dans le patchset.
      couche: Référentiel
    - id: COR_06_02
      cible: human_readable de REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL
      action: >
        Corriger le human_readable de « v1.7 » en « v1.8 »
        après renommage de l'ID.
      couche: Référentiel
    - id: COR_06_03
      cible: TYPE_REFERENTIEL_GRAPH_PROPAGATION_OPERATIONAL_NOTE.relations
      action: >
        Mettre à jour la relation derives_from pour cibler
        REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL
        après renommage de l'ID source.
      couche: Référentiel
```

---

## Détail des 12 tests

### Test 1 — Aucune règle dupliquée

- **Constitution :** ✅ PASS — Aucun doublon d'ID constaté dans TYPES, INVARIANTS, RULES, PARAMETERS, CONSTRAINTS, EVENTS, ACTIONS.
- **Référentiel :** ✅ PASS — Aucun doublon d'ID constaté.
- **LINK :** ✅ PASS — Aucun doublon d'ID constaté.

### Test 2 — Aucune dépendance orpheline

- **Constitution :** ✅ PASS — Toutes les `depends_on` internes sont résolues localement ou vers des références inter-Core explicites déclarées.
- **Référentiel :** ⚠️ ANOMALIE (ANO_06_03) — `TYPE_REFERENTIEL_GRAPH_PROPAGATION_OPERATIONAL_NOTE` déclare `derives_from: REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL`. L'ID cible existe localement mais est incohérent vis-à-vis du versioning inter-Core attendu post-patch.
- **LINK :** ✅ PASS — Toutes les `depends_on` résolues vers les deux refs inter-Core déclarées.

### Test 3 — Aucune relation implicite

- **Constitution :** ✅ PASS — Toutes les relations utilisent des champs `type` et `target.id` explicites.
- **Référentiel :** ✅ PASS — Idem. Les `relations: []` vides sont acceptables.
- **LINK :** ✅ PASS — Les bindings sont tous déclarés via `type: binds` avec `target.id` explicite.

### Test 4 — Invariants non patchables

- **Constitution :** ✅ PASS — Tous les invariants marqués `patchable: false` ont `parameterizable: false`. Aucune tentative de modification constatée.
- **Référentiel :** ✅ PASS — `INV_REFERENTIEL_CONSTITUTIONAL_AND_LOGIC_NOT_MODIFIABLE_HERE`, `INV_REFERENTIEL_GRAPH_ONE_HOP_NOT_MODIFIABLE_HERE`, `INV_REFERENTIEL_PATCH_QUALITY_CHECKLIST_NOT_MODIFIABLE_HERE`, `INV_REFERENTIEL_CREATIVE_R_FALLBACK_IS_X1`, `INV_REFERENTIEL_VC_UNKNOWN_MEANS_NO_INFERENCE`, `INVARIANT_ISOLATED_LOW_VC_MEANS_NO_ACTION`, `INV_REFERENTIEL_SESSION_INTENTION_NON_PENALIZED` sont tous `patchable: false` et intacts.
- **LINK :** ✅ PASS — `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` est `patchable: false` et intacte.

### Test 5 — Logique non contradictoire

- **Constitution :** ✅ PASS — Aucune contradiction logique nouvelle détectée dans la version patchée.
- **Référentiel :** ✅ PASS — Les nouvelles règles du patch (PATCH_V0_6) sont cohérentes entre elles. `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` est `patchable: false` et `parameterizable: true` ce qui est licite.
- **LINK :** ✅ PASS — Pas de logique métier autonome introduite.

### Test 6 — source_anchor présent

- **Constitution :** ✅ PASS — Tous les éléments ont un `source_anchor` non vide.
- **Référentiel :** ✅ PASS — Tous les éléments ont un `source_anchor` non vide, y compris les nouveaux éléments PATCH_V0_6.
- **LINK :** ✅ PASS — Tous les `source_anchor` sont présents.

### Test 7 — Relations cohérentes

- **Constitution :** ✅ PASS — Les types de relations (`governs`, `validates`, `constrains`, `triggers`, `derives_from`, `requires`, `instantiates`, `binds`) sont utilisés de façon sémantiquement cohérente.
- **Référentiel :** ✅ PASS — Idem. Les `relations: []` vides sur les règles sont licites.
- **LINK :** ✅ PASS — Les `type: binds` sont tous justifiés par les bindings inter-Core déclarés.

### Test 8 — Graphe connexe

- **Constitution :** ✅ PASS — Le graphe des dépendances internes forme un ensemble connexe par les chaînes de `depends_on` et `relations`.
- **Référentiel :** ✅ PASS — Le nœud racine `REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL` est atteint par la quasi-totalité des TYPES, INVARIANTS et RULES. Les éléments sans `depends_on` (paramètres terminaux) sont des feuilles légitimes.
- **LINK :** ✅ PASS — Les deux nœuds racines (`LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_V0_6`) sont atteints depuis tous les bindings.

### Test 9 — Ré-inflation possible

- **Constitution :** ✅ PASS — Tous les éléments ont les attributs requis permettant une ré-inflation canonique (`id`, `authority`, `core_type`, `source_anchor`, `patchable`, `parameterizable`, `human_readable`, `logic`).
- **Référentiel :** ✅ PASS — Idem.
- **LINK :** ✅ PASS — Idem.

### Test 10 — core_type cohérent avec le fichier cible

- **Constitution :** ✅ PASS — Tous les éléments déclarent `core_type: CONSTITUTION`.
- **Référentiel :** ✅ PASS — Tous les éléments déclarent `core_type: REFERENTIEL`.
- **LINK :** ✅ PASS — Tous les éléments déclarent `core_type: LINK`.

### Test 11 — Références inter-Core explicites ou assumées

- **Constitution :** ✅ PASS — La référence vers le Référentiel est déclarée explicitement sous `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION`.
- **Référentiel :** ❌ **FAIL — ANO_06_01** — La référence inter-Core est déclarée sous `REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL` alors que la Constitution patchée est `CORE_LEARNIT_CONSTITUTION_V1_8`. L'ID porte encore l'ancien numéro de version `V1_7`.
- **LINK :** ✅ PASS — Les deux refs inter-Core (`LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_V0_6`) sont cohérentes avec les Cores déclarés.

### Test 12 — Absence de collision d'id

- **Constitution :** ✅ PASS — Aucune collision d'ID.
- **Référentiel :** ❌ **FAIL — ANO_06_02** — L'ID `REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL` crée une asymétrie structurelle : la Constitution active est en V1_8 et le LINK pointe vers `LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8`, mais le Référentiel patché maintient un ID V1_7 comme nœud racine. La cohérence des IDs inter-Core est rompue.
- **LINK :** ✅ PASS — Aucune collision d'ID.

---

## Synthèse

| Core | Tests PASS | Tests FAIL | Statut |
|------|-----------|-----------|--------|
| Constitution (patchée) | 12/12 | 0/12 | ✅ PASS |
| Référentiel (patché) | 9/12 | 3/12 | ❌ FAIL |
| LINK (patché) | 12/12 | 0/12 | ✅ PASS |

**Verdict global : FAIL**

---

## Action requise avant promotion

Le pipeline est **bloqué au STAGE_06**. Retour obligatoire au STAGE_03_PATCH_SYNTHESIS pour corriger le patchset :

1. Ajouter une opération `rename` dans le patchset ciblant `REF_CORE_LEARNIT_CONSTITUTION_V1_7_IN_REFERENTIEL` → `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL`.
2. Ajouter une opération `rewrite_references` propageant ce renommage sur toutes les `depends_on` et `relations.target.id` du Référentiel.
3. Ajouter une opération `replace_field` pour corriger le `human_readable` de v1.7 en v1.8.
4. Re-passer le STAGE_04_PATCH_VALIDATION puis STAGE_05_APPLY avant nouvelle validation STAGE_06.
