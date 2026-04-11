# Constitution — run layout resolution rules

## Objet

Ce document définit comment le pipeline `constitution` doit résoudre ses chemins d'entrée et de travail lorsque le layout `runs/<run_id>/...` est utilisé.

Il complète `pipeline.md` et prépare la transition depuis le layout plat historique.

---

## Modes de résolution

### Mode global nominal
Aucun `run_id` n'est fourni.

Le pipeline lit alors dans le layout historique :
- `docs/pipelines/constitution/inputs/`
- `docs/pipelines/constitution/work/`
- `docs/pipelines/constitution/reports/`
- `docs/pipelines/constitution/outputs/`

### Mode borné par run
Un `run_id` est fourni.

Le pipeline lit alors prioritairement dans :
- `docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/`
- `docs/pipelines/constitution/runs/<run_id>/work/`
- `docs/pipelines/constitution/runs/<run_id>/reports/`
- `docs/pipelines/constitution/runs/<run_id>/outputs/`
- `docs/pipelines/constitution/runs/<run_id>/archive/`

---

## Règle de priorité

La règle est :

1. si `run_id` est fourni et que le run existe, le pipeline doit utiliser le layout du run ;
2. sinon, le pipeline reste en layout historique ;
3. un run borné ne doit pas écrire dans le layout plat historique sauf en transition explicitement documentée.

---

## Entrées minimales attendues en mode run

- `run_manifest.yaml`
- `inputs/scope_manifest.yaml`
- `inputs/impact_bundle.yaml`
- `inputs/integration_gate.yaml`

Le `run_manifest.yaml` devient le point d'entrée d'identité du run.

---

## Convention de chemins par stage

### STAGE_01_CHALLENGE
- `runs/<run_id>/work/01_challenge/`

### STAGE_02_ARBITRAGE
- `runs/<run_id>/work/02_arbitrage/`

### STAGE_03_PATCH_SYNTHESIS
- `runs/<run_id>/work/03_patch/`

### STAGE_04_PATCH_VALIDATION
- `runs/<run_id>/work/04_patch_validation/`

### STAGE_05_APPLY
- `runs/<run_id>/work/05_apply/`

### STAGE_06_CORE_VALIDATION
- `runs/<run_id>/work/06_core_validation/`

### STAGE_07_RELEASE_MATERIALIZATION
- `runs/<run_id>/work/07_release/`

Les rapports et sorties doivent, en mode run, être écrits sous le répertoire du run.

---

## Transition

Tant que le pipeline n'est pas totalement adapté :
- le layout plat historique reste supporté ;
- le layout `runs/<run_id>/...` devient la cible pour les runs bornés.

Le layout plat doit être considéré comme transitoire pour les runs bornés.

---

## Décision de design

Le `run_id` devient l'unité primaire d'exécution pour les runs bornés du pipeline `constitution`.
