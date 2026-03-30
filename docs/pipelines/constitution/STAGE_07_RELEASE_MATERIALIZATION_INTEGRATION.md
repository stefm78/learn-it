# Stage 07 integration — build_release_plan.py

Ce document fournit les blocs exacts à intégrer dans les fichiers canoniques du pipeline pour rendre le calcul de release explicite, scripté et reproductible.

---

## 1) `docs/pipelines/constitution/pipeline.md`

### Dans `### Spec and tools`

Ajouter :

- `Build release plan: docs/patcher/shared/build_release_plan.py`
- `Materialize release: docs/patcher/shared/materialize_release.py`
- `Validate release plan: docs/patcher/shared/validate_release_plan.py`

---

## 2) `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

### Dans `Principe opératoire` de `07A_RELEASE_CLASSIFICATION`

Ajouter après le bloc qui décrit la comparaison :

- le calcul de release doit être produit par un script déterministe à partir de :
  - `work/05_apply/patched/`
  - `docs/cores/current/`
  - `work/06_core_validation/core_validation.yaml`
  - `reports/patch_execution_report.yaml`
- ce calcul ne doit pas reposer uniquement sur les `core_id` ou les `version`
- il doit comparer le contenu réel des Core patchés et courants avant toute décision de versioning
- le résultat canonique de ce calcul est `work/07_release/release_plan.yaml`

### Remplacer le bloc `Commandes de référence` par :

- construire le plan de release :
  - `python docs/patcher/shared/build_release_plan.py ./docs/pipelines/constitution/work/05_apply/patched ./docs/cores/current ./docs/pipelines/constitution/work/06_core_validation/core_validation.yaml ./docs/pipelines/constitution/reports/patch_execution_report.yaml ./docs/pipelines/constitution/work/07_release/release_plan.yaml`
- valider le plan de release :
  - `python docs/patcher/shared/validate_release_plan.py ./docs/pipelines/constitution/work/07_release/release_plan.yaml ./docs/specs/core-release/release_plan.schema.yaml`
- matérialiser la release :
  - `python docs/patcher/shared/materialize_release.py ./docs/pipelines/constitution/work/07_release/release_plan.yaml ./docs/pipelines/constitution/work/05_apply/patched ./docs/pipelines/constitution/reports/release_materialization_report.yaml ./docs/pipelines/constitution/outputs/release_candidate_notes.md`
- valider le manifest de release matérialisé :
  - `python docs/patcher/shared/validate_release_manifest.py ./docs/cores/releases/<release_id>/manifest.yaml ./docs/specs/core-release/release_manifest.schema.yaml`

### Dans `Validation attendue`

Ajouter avant la validation du plan :

- `build_release_plan.py` doit produire un `release_plan.yaml` cohérent avec les différences réelles entre `patched/` et `current/`
- en cas de différence de contenu, le script doit recalculer `change_depth`, `target_versions`, `required_renames`, `required_reference_updates` et `release_bundle`
- un simple maintien des mêmes `core_id` / `version` ne suffit pas à conclure à `change_depth: none`

### Dans `Règle opératoire`

Ajouter :

- la décision de release de `07A` doit être calculée par script ; l’IA peut commenter ou challenger le résultat, mais ne doit pas remplacer le calcul déterministe

---

## 3) Commandes à exécuter après intégration

```bash
python docs/patcher/shared/build_release_plan.py \
  ./docs/pipelines/constitution/work/05_apply/patched \
  ./docs/cores/current \
  ./docs/pipelines/constitution/work/06_core_validation/core_validation.yaml \
  ./docs/pipelines/constitution/reports/patch_execution_report.yaml \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml

python docs/patcher/shared/validate_release_plan.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/specs/core-release/release_plan.schema.yaml
```

Puis, si `release_required: true` :

```bash
python docs/patcher/shared/materialize_release.py \
  ./docs/pipelines/constitution/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/work/05_apply/patched \
  ./docs/pipelines/constitution/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/outputs/release_candidate_notes.md
```
