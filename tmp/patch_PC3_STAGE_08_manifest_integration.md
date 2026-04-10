# Patch PC-3 — STAGE_08_FACTORY_PROMOTE_CURRENT.md

## Fichiers cibles
- `docs/pipelines/platform_factory/STAGE_08_FACTORY_PROMOTE_CURRENT.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`

---

## Patch A — STAGE_08_FACTORY_PROMOTE_CURRENT.md

### Section concernée
`Note V0 importante` (fin du fichier)

### Texte actuel

```
Note V0 importante :
- contrairement au pipeline `constitution`, la promotion `platform_factory` ne doit pas encore supposer
  par défaut une mise à jour de `docs/cores/current/manifest.yaml` tant que le modèle et le tooling
  de manifest courant n'ont pas été explicitement étendus à `platform_factory`
- en V0, la provenance et l'état de promotion doivent donc être garantis au minimum par
  `platform_factory_promotion_report.yaml` et par la release matérialisée elle-même
```

### Texte de remplacement

```
Note sur la mise à jour manifest :
- La mise à jour de `docs/cores/current/manifest.yaml` est une étape explicite et obligatoire de ce stage.
- Elle constitue l'acte formel d'intégration des artefacts platform_factory au manifest officiel courant.
- Elle lève le blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` une fois complétée avec succès.
- Si le schema du manifest officiel ne permet pas encore d'intégrer les artefacts factory, ce stage doit :
  - produire un report `WARN` indiquant que la mise à jour manifest est bloquée par un schema insuffisant,
  - documenter explicitement dans le report les champs manquants dans le schema,
  - ne pas considérer STAGE_08 comme `PASS` complet tant que la mise à jour manifest n'est pas effective.
- En l'absence d'un schema manifest adapté, un manifest séparé `docs/cores/platform_factory/manifest.yaml`
  peut être produit comme solution transitoire tracée, en attendant l'extension du manifest officiel.
```

### Ajout dans `Principe opératoire` (après l'étape de copie vers `current/`)

```
- après la copie vers `docs/cores/current/`, tenter la mise à jour de `docs/cores/current/manifest.yaml` :
  - si le schema courant du manifest supporte les artefacts factory :
    - mettre à jour et tracer dans le report (`manifest_update_status: applied`)
  - si le schema est insuffisant :
    - produire `docs/cores/platform_factory/manifest.yaml` comme solution transitoire
    - documenter le gap schema dans le report (`manifest_update_status: blocked_schema_insufficient`)
    - lister les champs manquants dans `manifest_update_notes`
    - statut STAGE_08 = `WARN` (pas `PASS` complet)
```

---

## Patch B — LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md

### Section concernée
`## Préconditions obligatoires` — ajouter une précondition

### Ajout

```
- Avoir vérifié l'état du manifest officiel courant pour déterminer si son schema
  supporte déjà les artefacts platform_factory (présence de `artifact_type: factory_artifact`).
- Si le schema ne le supporte pas, préparer la production de `docs/cores/platform_factory/manifest.yaml`
  comme solution transitoire.
```

### Section concernée
`## Fichiers de sortie obligatoires` — ajouter un output conditionnel

### Ajout

```
- `docs/cores/current/manifest.yaml` (si schema compatible) OU
  `docs/cores/platform_factory/manifest.yaml` (si solution transitoire)
```

### Section concernée
`## Vérification obligatoire après exécution` — ajouter vérification manifest

### Ajout

```
- Vérifier explicitement dans le report :
  - `manifest_update_status` : `applied` | `blocked_schema_insufficient` | `skipped`
  - `manifest_update_notes` : description du gap ou confirmation de mise à jour
- Si `manifest_update_status: blocked_schema_insufficient` :
  - vérifier que `docs/cores/platform_factory/manifest.yaml` a bien été produit
  - le stage est en `WARN`, pas en `PASS` complet
```

---

## Justification
Arbitrage PC-3 — 2026-04-10.
La mise à jour du manifest lors de STAGE_08 est l'acte formel qui lève
`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`. Ce patch rend ce comportement
explicite, obligatoire, et tracé dans le report de promotion.
La solution transitoire (`docs/cores/platform_factory/manifest.yaml`) permet
de ne pas bloquer le pipeline si le schema officiel n'est pas encore prêt,
tout en garantissant une traçabilité minimale immédiate.

## Statut
Prêt pour application dans les fichiers cibles.
À appliquer avant le prochain cycle de challenge.
