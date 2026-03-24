# ROUTING GLOBAL — Learn-it v1.6 / Référentiel v0.5

Point d'entrée unique pour tout LLM opérant sur les documents Learn-it.
Charger ce fichier en premier si la tâche couvre plusieurs documents.

Date    : 2026-03-24
Constitution : `constitution/00_MANIFEST.md` [HASH:C4D9A3F2]
Référentiel  : `referentiel/00_MANIFEST.md`  [HASH:B_E7B2D841]

---

## Règle fondamentale

```
Constitution  = quoi / pourquoi   → invariants non modifiables par patch
Référentiel   = combien / comment → paramètres ajustables dans fourchettes
Priorité      : Constitution > Référentiel sur tout conflit
```

---

## Routing combiné — tâches multi-documents

| Tâche LLM                            | Constitution                                        | Référentiel                                              |
|--------------------------------------|-----------------------------------------------------|----------------------------------------------------------|
| Vérification conformité patch        | `constitution/04_invariants_P16-P19.md`             | `referentiel/05_tables_declencheurs.md` + `07_seuils_invariants.md` |
| Audit ADDIE-0 complet                | `constitution/02_fondamentaux_P0-P6.md` + `05_addie_tables.md` | `referentiel/03_mecanismes_DA.md`           |
| Génération et validation missions    | `constitution/03_mecanismes_P7-P15.md` + `04_invariants_P16-P19.md` | `referentiel/03_mecanismes_DA.md` + `06_sections_S16-S19.md` |
| Déclenchement et ciblage d'un patch  | `constitution/04_invariants_P16-P19.md`             | `referentiel/05_tables_declencheurs.md` + `06_sections_S16-S19.md` |
| Audit VC / AR-réfractaire / feedback | `constitution/04_invariants_P16-P19.md`             | `referentiel/06_sections_S16-S19.md`                     |
| Révision constitutionnelle           | TOUS les modules constitution/                      | `referentiel/01_gouvernance_referentiel.md`               |
| Révision complète Référentiel        | `constitution/01_gouvernance.md`                    | TOUS les modules referentiel/                             |
| Lookup seuil rapide                  | —                                                   | `referentiel/07_seuils_invariants.md`                     |
| Audit DSL / traçabilité              | `constitution/07_meta_dsl.md`                       | `referentiel/08_meta_dsl.md`                              |

---

## Routing mono-document

> Si la tâche ne couvre qu'un seul document, utiliser directement son MANIFEST :
> - `constitution/00_MANIFEST.md`
> - `referentiel/00_MANIFEST.md`

---

## Règles de chargement

- Charger uniquement les modules nécessaires à la tâche — jamais l'intégralité par défaut.
- Ne jamais inférer le contenu d'un module non chargé.
- En cas de conflit entre un module Constitution et un module Référentiel : **Constitution prime**.
- Les invariants constitutionnels (AND-MSC P16, propagation 1-saut P17) sont **non modifiables**
  même si le Référentiel les documente à titre opérationnel.
- `07_meta_dsl.md` et `08_meta_dsl.md` — usage audit uniquement, jamais en contexte opérationnel.

---

## Structure du dépôt docs/

```
docs/
├── 00_ROUTING_GLOBAL.md                  ← CE FICHIER
├── Constitution_Learn-it_v1_6_DSL.md     ← source canonique constitution
├── referentiel_defaults_v0_5_DSL.md      ← source canonique référentiel
├── constitution/
│   ├── 00_MANIFEST.md
│   ├── 01_gouvernance.md
│   ├── 02_fondamentaux_P0-P6.md
│   ├── 03_mecanismes_P7-P15.md
│   ├── 04_invariants_P16-P19.md
│   ├── 05_addie_tables.md
│   ├── 06_glossaire_theories.md
│   └── 07_meta_dsl.md
└── referentiel/
    ├── 00_MANIFEST.md
    ├── 01_gouvernance_referentiel.md
    ├── 02_fondamentaux_MSC.md
    ├── 03_mecanismes_DA.md
    ├── 04_gardefous_limites.md
    ├── 05_tables_declencheurs.md
    ├── 06_sections_S16-S19.md
    ├── 07_seuils_invariants.md
    └── 08_meta_dsl.md
```
