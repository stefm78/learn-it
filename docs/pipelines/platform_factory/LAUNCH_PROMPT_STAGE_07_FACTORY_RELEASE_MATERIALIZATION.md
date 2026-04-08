# LAUNCH PROMPT — STAGE_07_FACTORY_RELEASE_MATERIALIZATION

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_07_FACTORY_RELEASE_MATERIALIZATION` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`
- spécification détaillée :
  - `docs/pipelines/platform_factory/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

## Sous-étapes obligatoires

- `07A_FACTORY_RELEASE_CLASSIFICATION`
- `07B_FACTORY_RELEASE_MATERIALIZATION`

## Inputs obligatoires

Artefacts patchés validés :
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`

Validation et exécution amont :
- `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`

État courant de référence :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Scripts dédiés :
- `docs/patcher/shared/build_platform_factory_release_plan.py`
- `docs/patcher/shared/materialize_platform_factory_release.py`

## Préconditions obligatoires

- `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml` doit être en `status: PASS`.
- Les artefacts patchés de `work/05_apply/patched/` doivent exister réellement.
- Le report d’exécution Stage 05 doit exister réellement.
- Ne pas simuler une release plan ou une release matérialisée si les scripts n’ont pas tourné.

## Contexte d’exécution obligatoire

- Le calcul de release doit être déterministe.
- L’IA peut commenter ou relire le résultat, mais ne doit pas remplacer le calcul par une estimation libre.
- `docs/cores/current/` ne doit jamais être modifié à ce stage.
- Le résultat attendu doit être écrit dans le repo, dans les chemins de sortie imposés ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

## Règle anti-simulation obligatoire

- Ne jamais simuler le résultat d’un script déterministe.
- Ne jamais annoncer un `release_required`, `change_depth`, `release_id`, `release_path` ou `status` comme si les scripts avaient été exécutés si ce n’est pas le cas.
- Ne jamais prétendre qu’une release immuable existe sous `docs/cores/releases/` si elle n’a pas été réellement matérialisée.
- Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
- Dans ce cas, il faut donner clairement la ou les commandes exactes à exécuter.
- Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme un résultat déjà constaté des scripts.

## Fichiers de sortie obligatoires

Sorties de `07A_FACTORY_RELEASE_CLASSIFICATION` :
- `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`

Sorties de `07B_FACTORY_RELEASE_MATERIALIZATION` :
- `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
- `docs/cores/releases/<release_id>/platform_factory_state.yaml`
- `docs/cores/releases/<release_id>/manifest.yaml`
- `docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md`
- `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

## Étapes d’exécution obligatoires

### 1. Préparer le répertoire de travail release

Exécuter :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/07_release
mkdir -p ./docs/pipelines/platform_factory/outputs
```

### 2. Exécuter 07A_FACTORY_RELEASE_CLASSIFICATION

Exécuter :

```bash
python docs/patcher/shared/build_platform_factory_release_plan.py           ./docs/pipelines/platform_factory/work/05_apply/patched           ./docs/cores/current           ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
```

### 3. Vérifier le release plan

- Lire `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
- Vérifier explicitement la racine `RELEASE_PLAN` :
  - `status`
  - `release_required`
  - `change_depth`
  - `release_bundle.release_id`
  - `release_bundle.release_path`
  - `release_bundle.promotion_candidate`
- Si `RELEASE_PLAN.status` n’est pas `PASS`, arrêter ici.
- Si `RELEASE_PLAN.release_required` vaut `false`, arrêter ici sans lancer 07B.
- Dans ce cas, ne pas créer de release sous `docs/cores/releases/` et ne pas passer au Stage 08.

### 4. Exécuter 07B_FACTORY_RELEASE_MATERIALIZATION

Seulement si le release plan est exploitable et si `RELEASE_PLAN.release_required: true`, exécuter :

```bash
python docs/patcher/shared/materialize_platform_factory_release.py           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml           ./docs/pipelines/platform_factory/work/05_apply/patched           ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml           ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
```

### 5. Vérifier le report de matérialisation

- Lire `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`
- Vérifier explicitement la racine `PLATFORM_FACTORY_RELEASE_MATERIALIZATION` :
  - `status`
  - `release_required`
  - `release_id`
  - `release_path`
  - `files_written`
- Si `PLATFORM_FACTORY_RELEASE_MATERIALIZATION.status` n’est pas `PASS`, le stage ne franchit pas 07.
- Ne pas passer à la promotion tant que la matérialisation n’est pas proprement fermée.

## Si une commande doit être exécutée par l’humain dans le chat

Avant toute interprétation du résultat, dire explicitement :
- qu’il s’agit d’une commande déterministe à exécuter ;
- que le résultat automatique n’est pas encore disponible ;
- que tout statut de release reste non confirmé tant que les fichiers de sortie n’ont pas été réellement produits.

## Contraintes

- Ne pas modifier `docs/cores/current/` à ce stage.
- Ne pas inventer un `release_id` à la place du script.
- Ne pas créer de release immuable si `RELEASE_PLAN.release_required: false`.
- Ne pas remplacer les scripts dédiés par une interprétation libre.
- Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

## Résultat terminal attendu

À la fin de l’exécution, si les scripts ont bien été exécutés et les artefacts bien écrits, afficher uniquement :
1. les chemins exacts des artefacts écrits
2. le statut final du release plan et du report de matérialisation : PASS | WARN | FAIL
3. un résumé ultra-court
