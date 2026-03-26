# MANIFEST — Référentiel de defaults pédagogiques Learn-it v0.5 (modules atomiques)

`[HASH_SOURCE:B_E7B2D841]`  
Date    : 2026-03-24  
Source  : ../referentiel_defaults_v0_5_DSL.md

---

## Modules


| Fichier                         | Contenu                                                                 | Taille est. |
| ------------------------------- | ----------------------------------------------------------------------- | ----------- |
| `01_gouvernance_referentiel.md` | Header 2DSL, versioning, principe Constitution/Référentiel              | ~2 Ko       |
| `02_fondamentaux_MSC.md`        | Modèle MSC, seuils P/R/A/deg, logique AND                               | ~2 Ko       |
| `03_mecanismes_DA.md`           | Calibrage, interleaving, multiplicateurs R, inertie, AR-N2, sessions    | ~5 Ko       |
| `04_gardefous_limites.md`       | Fatigue cognitive, gamification, métacognition, intégrité, feedback     | ~2 Ko       |
| `05_tables_declencheurs.md`     | Table déclencheurs patch + périmètre autorisé/interdit                  | ~2 Ko       |
| `06_sections_S16-S19.md`        | VC persistance, AR-réfractaire, couverture feedback, propagation graphe | ~5 Ko       |
| `07_seuils_invariants.md`       | Seuils/bornes critiques v0.5 + invariants structurels (GF-01, GF-02)    | ~2 Ko       |
| `08_meta_dsl.md`                | Checklists DSL (✅ ❌ ⚠️ ASSERT) — audit traçabilité inter-versions       | ~3 Ko       |


---

## Routing LLM — Chargement conditionnel

> Règle fondamentale : ne charger que les modules nécessaires à la tâche.  
> Ne jamais inférer le contenu d'un module non chargé.


| Tâche LLM                              | Modules à charger                                       |
| -------------------------------------- | ------------------------------------------------------- |
| Vérification seuils d'un patch         | `02_fondamentaux_MSC.md` + `07_seuils_invariants.md`    |
| Vérification conformité patch complète | `05_tables_declencheurs.md` + `07_seuils_invariants.md` |
| Audit VC / AR-réfractaire / feedback   | `06_sections_S16-S19.md`                                |
| Génération/validation missions         | `03_mecanismes_DA.md` + `06_sections_S16-S19.md`        |
| Déclenchement et ciblage d'un patch    | `05_tables_declencheurs.md` + `06_sections_S16-S19.md`  |
| Lookup seuil rapide                    | `07_seuils_invariants.md`                               |
| Révision complète du Référentiel       | TOUS les modules                                        |
| Audit DSL / traçabilité inter-versions | `08_meta_dsl.md`                                        |


---

## Ordre de priorité en cas de conflit entre modules

```
07_seuils_invariants > 06_sections_S16-S19 > 05_tables_declencheurs > 02_fondamentaux_MSC
> 03_mecanismes_DA > 04_gardefous_limites > 01_gouvernance > 08_meta_dsl
```

---

## Règles de gouvernance des modules

- Le Référentiel définit les **valeurs** de seuils et fourchettes — jamais la logique de combinaison (Constitution).
- Tout paramètre modifiable est borné : toute valeur hors fourchette → patch rejeté intégralement (GF-02).
- `06_sections_S16-S19.md` contient les paramètres les plus récents (v0.5) — priorité de chargement en cas de doute.
- `07_seuils_invariants.md` est le fichier de référence rapide pour tout LLM en vérification de conformité.
- Les invariants constitutionnels documentés ici (propagation 1-saut, AND-MSC) sont **non modifiables par patch** — référence autoritaire : Constitution `04_invariants_P16-P19.md`.
- `08_meta_dsl.md` — usage audit/traçabilité uniquement, jamais chargé en contexte opérationnel.

---

## Dépendances externes


| Référence                               | Utilisée dans                   |
| --------------------------------------- | ------------------------------- |
| Constitution v1.6 `[HASH:C4D9A3F2]`     | Tous les modules                |
| Constitution `04_invariants_P16-P19.md` | `06`, `07` (P16, P17, P18, P19) |
| Constitution `03_mecanismes_P7-P15.md`  | `05`, `06` (P12 liste contrôle) |
| ADDIE-0 protocole typage KU             | `03_mecanismes_DA.md`           |
