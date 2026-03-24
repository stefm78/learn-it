# MANIFEST — Constitution Learn-it v1.6 (modules atomiques)

`[HASH_SOURCE:C4D9A3F2]`
Date    : 2026-03-24
Source  : ../Constitution_Learn-it_v1_6_DSL.md

---

## Modules

| Fichier                      | Contenu                                                          | Taille |
|------------------------------|------------------------------------------------------------------|--------|
| `01_gouvernance.md`          | Header 2DSL, versioning, gouvernance Constitution/Referentiel    | 2 Ko   |
| `02_fondamentaux_P0-P6.md`   | Principes P0–P6 : calibrage, graphe KU, mémoire, personnalisa.  | 8 Ko   |
| `03_mecanismes_P7-P15.md`    | Principes P7–P15 : moteur, feedback, patchs, intégrité           | 10 Ko  |
| `04_invariants_P16-P19.md`   | Invariants P16–P19 : AND-MSC, propagation, VC, contexte auth.   | 4 Ko   |
| `05_addie_tables.md`         | Cycle ADDIE + toutes les tables récapitulatives                  | 5,5 Ko |
| `06_glossaire_theories.md`   | Glossaire sigles + cadres théoriques + seuils/bornes critiques   | 4,4 Ko |
| `07_meta_dsl.md`             | Checklists DSL (✅ ❌ ⚠️ 📐) — audit traçabilité inter-versions  | 6,4 Ko |

---

## Routing LLM — Chargement conditionnel

> Règle fondamentale : ne charger que les modules nécessaires à la tâche.
> Ne jamais inférer le contenu d'un module non chargé.

| Tâche LLM                          | Modules à charger                                              |
|------------------------------------|----------------------------------------------------------------|
| Vérification conformité patch      | `04_invariants_P16-P19.md` + Référentiel                       |
| Audit ADDIE-0 (phase Analyse)      | `02_fondamentaux_P0-P6.md` + `05_addie_tables.md`             |
| Génération missions                | `03_mecanismes_P7-P15.md` + `04_invariants_P16-P19.md`        |
| Vérification feedback KU           | `03_mecanismes_P7-P15.md` + `05_addie_tables.md`              |
| Révision constitutionnelle         | TOUS les modules                                               |
| Lookup rapide / RAG                | `06_glossaire_theories.md`                                     |
| Audit DSL / traçabilité            | `07_meta_dsl.md`                                               |

---

## Ordre de priorité en cas de conflit entre modules

```
04_invariants > 03_mecanismes > 02_fondamentaux > 01_gouvernance > 05_addie_tables > 06_glossaire > 07_meta_dsl
```

---

## Règles de gouvernance des modules

- Chaque module est autonome et contient son propre contexte de lecture.
- Toute modification d'un module → incrément de version du module + MAJ du HASH ici.
- Le fichier source `../Constitution_Learn-it_v1_6_DSL.md` reste la référence
  canonique jusqu'à migration complète validée.
- Un LLM **NE DOIT PAS** inférer le contenu d'un module non chargé.
- Périmètre patchable : `02`, `03`, `05`, `06` — dans les fourchettes Référentiel.
- Périmètre **non patchable** : `04_invariants_P16-P19.md` — révision constitutionnelle uniquement.
- `07_meta_dsl.md` — usage audit/traçabilité uniquement, jamais chargé en contexte opérationnel.

---

## Dépendances externes

| Référence                        | Utilisée dans          |
|----------------------------------|------------------------|
| Référentiel v0.4                 | `03`, `04`, `05`       |
| Merrill's First Principles 2002  | `04` (P19)             |
| ADDIE-0 (protocole typage KU)    | `05`                   |
