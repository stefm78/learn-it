# Release Candidate Notes — CORE_RELEASE_2026_04_13_R01

## Identité

- **release_id** : `CORE_RELEASE_2026_04_13_R01`
- **run_id** : `CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01`
- **scope_key** : `patch_lifecycle`
- **date** : 2026-04-13
- **pipeline** : constitution — STAGE_07_RELEASE_MATERIALIZATION
- **mode** : bounded_local_run

## Classification du changement

| Core | Changement | Profondeur |
|---|---|---|
| `constitution.yaml` | Oui — 4 modifications | `minor` |
| `referentiel.yaml` | Non | `none` |
| `link.yaml` | Non | `none` |

**change_depth global : `minor`**

## Modifications de `constitution.yaml`

### 1. `TYPE_PATCH_IMPACT_SCOPE.logic` — précision déterministe

La condition du `logic` a été précisée : l'`impact_scope` est désormais défini comme
l'ensemble structurel des IDs affectés par le patch, **calculable par diff déterministe**
sur les fichiers cibles. Toute évaluation sémantique ou pédagogique est explicitement
exclue de ce calcul et déléguée à la chaîne hors session de QA pédagogique.

**Motivation** : renforcer la compatibilité avec `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.

---

### 2. `ACTION_ROLLBACK_PATCH.logic` — précision opératoire

La condition précise la définition de la *partialité* (toute interruption avant commit
atomique complet). L'effet impose la capture d'un snapshot pré-application et la
restauration intégrale en cas de détection. Traçabilité dans le rapport d'exécution requise.

**Motivation** : rendre `INV_NO_PARTIAL_PATCH_STATE` exécutable et auditable.

---

### 3. `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED.logic` — condition complémentaire

Ajout d'une **condition complémentaire (boucle d'inefficacité)** : si N patches successifs
du même type sont appliqués sans disparition du signal de dérive, une escalade hors session
est obligatoire, indépendamment de la condition primaire (patch rejeté ou impossible).
Le paramètre N est délégué au Référentiel (`PARAM_REFERENTIEL_MAX_PATCH_ITERATIONS_BEFORE_ESCALATION`).

**Motivation** : fermer le cas où des patches localement valides mais inefficaces
pourraient maintenir un état de dérive non traité indéfiniment.

---

### 4. `RULE_PATCH_SERIALIZATION` — nouvelle règle ajoutée

Source anchor : `[PATCH_LIFECYCLE_R01][C01]`

Un **seul patch actif** par apprenant à un instant donné. Tout déclenchement concurrent
(via `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` ou tout
autre `TYPE_PATCH_ARTIFACT`) est **sérialisé en file d'attente FIFO**. L'état apprenant
ne peut être modifié que par un seul patch actif à la fois, garantissant le déterminisme
de l'état résultant.

**Motivation** : empêcher les états non déterministes résultant de patches concurrents.

---

## Versionnement

| Core | Version courante | Version release |
|---|---|---|
| constitution | `V2_0_FINAL` | `V2_0_PATCH_LIFECYCLE_R01` |
| referentiel | inchangé | inchangé |
| link | inchangé | inchangé |

## Compatibilité inter-Core

- Aucun `core_id` renommé ou supprimé.
- `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` inchangé.
- Aucune rupture de contrat avec `referentiel.yaml` ou `link.yaml`.
- Le paramètre `PARAM_REFERENTIEL_MAX_PATCH_ITERATIONS_BEFORE_ESCALATION` est **délégué
  au Référentiel** (référencé dans `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`) ;
  sa déclaration effective dans `referentiel.yaml` devra être vérifiée à l'occasion du
  prochain run de scope `referentiel`.

## Statut de promotion

> ⚠️ **Promotion bloquée** — `integration_gate` ouvert (6 checks, 0 cleared).
>
> Cette release est un **candidat à la promotion**, non une promotion effective.
> La bascule vers `docs/cores/current/` reste un acte centralisé et explicite du STAGE_08,
> conditionné à la clearance de l'integration_gate.

## Artefacts de la release

```
docs/cores/releases/CORE_RELEASE_2026_04_13_R01/
  constitution.yaml    ← Core patché, version V2_0_PATCH_LIFECYCLE_R01
  manifest.yaml        ← Manifest immuable de la release
```

## Commandes de validation déterministe (à exécuter)

```bash
# 1. Reconstruire le plan de release (déterministe)
python docs/patcher/shared/build_release_plan.py \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/05_apply/sandbox/docs/cores/current \
  ./docs/cores/current \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/06_core_validation/core_validation.yaml \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/reports/patch_execution_report.yaml \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/07_release/release_plan.yaml

# 2. Valider le plan de release
python docs/patcher/shared/validate_release_plan.py \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/07_release/release_plan.yaml \
  ./docs/specs/core-release/release_plan.schema.yaml

# 3. Matérialiser la release
python docs/patcher/shared/materialize_release.py \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/07_release/release_plan.yaml \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/05_apply/sandbox/docs/cores/current \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/reports/release_materialization_report.yaml \
  ./docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/outputs/release_candidate_notes.md

# 4. Valider le manifest de release
python docs/patcher/shared/validate_release_manifest.py \
  ./docs/cores/releases/CORE_RELEASE_2026_04_13_R01/manifest.yaml \
  ./docs/specs/core-release/release_manifest.schema.yaml
```
