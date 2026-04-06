# LAUNCH PROMPT — STAGE_05_FACTORY_APPLY

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_05_FACTORY_APPLY` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

Patchset validé :
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`

Validation préalable obligatoire :
- `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`

Artefacts source courants :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Script d’exécution dédié :
- `docs/patcher/shared/apply_platform_factory_patchset.py`

## Précondition obligatoire

- `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml` doit être en `status: PASS`.
- Si le statut n’est pas `PASS`, ne pas appliquer le patchset.
- Ne pas improviser d’apply manuel si la validation n’est pas fermée.

## Contexte d’exécution obligatoire

- Le patchset peut continuer à référencer les chemins canoniques sous `docs/cores/current/`.
- L’application réelle doit se faire dans une sandbox sous `docs/pipelines/platform_factory/work/05_apply/`.
- `docs/cores/current/` ne doit jamais être modifié directement à ce stage.
- Le résultat attendu doit être écrit dans le repo, dans les chemins de sortie imposés ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

## Règle anti-simulation obligatoire

- Ne jamais simuler le résultat d’un script déterministe.
- Ne jamais annoncer un `PASS`, `WARN` ou `FAIL` comme si le script avait été exécuté si ce n’est pas le cas.
- Ne jamais prétendre qu’un dry-run, un apply réel ou un report d’exécution a eu lieu s’il n’a pas réellement eu lieu.
- Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
- Dans ce cas, il faut donner clairement la ou les commandes exactes à exécuter.
- Toute lecture complémentaire du patchset ou des chemins de sortie doit être présentée comme préparatoire ou conditionnelle, jamais comme un résultat d’exécution déjà constaté.

## Fichiers et répertoires de sortie obligatoires

- `docs/pipelines/platform_factory/work/05_apply/sandbox/`
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`

## Étapes d’exécution obligatoires

### 1. Préparer la sandbox

Exécuter :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current
cp ./docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml
cp ./docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml
```

### 2. Exécuter un dry-run obligatoire

Exécuter :

```bash
python docs/patcher/shared/apply_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
  ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml \
  ./docs/pipelines/platform_factory/work/05_apply/sandbox \
  true \
  ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
```

### 3. Vérifier le report de dry-run

- Lire `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`
- Si le report n’est pas en `status: PASS`, arrêter ici.
- Ne pas lancer l’apply réel.

### 4. Exécuter l’apply réel

Seulement si le dry-run est `PASS`, exécuter :

```bash
python docs/patcher/shared/apply_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
  ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml \
  ./docs/pipelines/platform_factory/work/05_apply/sandbox \
  false \
  ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
```

### 5. Matérialiser la sortie patchée

Exécuter :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/05_apply/patched
cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml
cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml
```

## Si une commande doit être exécutée par l’humain dans le chat

Avant toute interprétation du résultat, dire explicitement :
- qu’il s’agit d’une commande déterministe à exécuter ;
- que le résultat automatique n’est pas encore disponible ;
- que tout statut du report d’exécution reste non confirmé tant que le script n’a pas réellement tourné et écrit son YAML.

## Contraintes

- Ne pas modifier `docs/cores/current/` directement.
- Ne pas sauter le dry-run.
- Ne pas faire l’apply réel si le dry-run n’est pas `PASS`.
- Ne pas remplacer le script dédié par une interprétation libre du patchset.
- Le livrable attendu est constitué des fichiers et répertoires écrits dans le repo. Le retour chat doit être très succinct.

## Résultat terminal attendu

À la fin de l’exécution, si les scripts ont bien été exécutés et les artefacts bien écrits, afficher uniquement :
1. les chemins exacts des artefacts écrits
2. le statut final du report d’exécution : PASS | WARN | FAIL
3. un résumé ultra-court
