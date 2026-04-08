# Platform Factory — Operator runbook

Ce document sert de companion opérateur pour une IA sans contexte historique du repo.

Il ne remplace ni `pipeline.md`, ni les launch prompts.
Il donne le chemin le plus court pour faire avancer le pipeline proprement, en donnant au bon moment la commande exacte à exécuter, puis en relisant le report effectivement produit.

---

## Règle cardinale

Ne jamais simuler le résultat d’un script déterministe.

Pour tout stage scripté :
1. lire le prompt du stage ;
2. donner la commande exacte ;
3. attendre l’exécution humaine ;
4. relire le YAML ou le report réellement écrit ;
5. annoncer seulement le statut constaté et la suite immédiate.

---

## Ordre minimal de lecture pour une IA sans contexte

1. `docs/pipelines/platform_factory/pipeline.md`
2. `docs/pipelines/platform_factory/PROMPT_USAGE.md`
3. le prompt principal du stage en cours
4. les fichiers d’entrée réellement présents dans `work/`, `reports/`, `outputs/` ou `docs/cores/current/`

---

## Format de réponse recommandé

### Cas A — stage sans script obligatoire

Répondre de manière courte avec :
- le chemin du fichier à écrire ;
- soit le contenu complet prêt à déposer ;
- soit un patch / remplacement exact si l’IA ne peut pas écrire directement.

### Cas B — stage avec script déterministe

Répondre sous cette forme :

```text
Commande déterministe à exécuter
```

puis un unique bloc bash, puis une seule phrase demandant de coller la sortie du terminal ou de confirmer le fichier YAML produit.

Après exécution, répondre seulement avec :
1. chemins écrits ;
2. statut ;
3. suite immédiate.

---

## Mapping rapide par stage

### STAGE_01_CHALLENGE
- Prompt : `docs/prompts/shared/Challenge_platform_factory.md`
- Sortie attendue : `docs/pipelines/platform_factory/work/01_challenge/challenge_report_<ID>.md`
- Commande shell : aucune obligatoire

### STAGE_02_FACTORY_ARBITRAGE
- Prompt : `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- Sortie attendue : `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
- Commande shell : aucune obligatoire

### STAGE_03_FACTORY_PATCH_SYNTHESIS
- Prompt : `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- Sortie attendue : `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`
- Commande shell : aucune obligatoire

### STAGE_04_FACTORY_PATCH_VALIDATION
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
- YAML attendu : `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_patch_validation_report.md`
- Commande :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/04_patch_validation
python docs/patcher/shared/validate_platform_factory_patchset.py           ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml           > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml
```

### STAGE_05_FACTORY_APPLY
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`
- Artefacts patchés attendus :
  - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
  - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`
- Commandes :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current
cp ./docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml
cp ./docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml
python docs/patcher/shared/apply_platform_factory_patchset.py           ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml           ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml           ./docs/pipelines/platform_factory/work/05_apply/sandbox           true           ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
```

Puis, seulement si le dry-run est `PASS` :

```bash
python docs/patcher/shared/apply_platform_factory_patchset.py           ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml           ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml           ./docs/pipelines/platform_factory/work/05_apply/sandbox           false           ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
mkdir -p ./docs/pipelines/platform_factory/work/05_apply/patched
cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml
cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml
```

### STAGE_06_FACTORY_CORE_VALIDATION
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
- YAML attendu : `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_core_validation_report.md`
- Commande :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/06_core_validation
python docs/patcher/shared/validate_platform_factory_core.py           ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml           ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml           > ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml
```

### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
- Plan attendu : `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`
- Commandes :

```bash
mkdir -p ./docs/pipelines/platform_factory/work/07_release
mkdir -p ./docs/pipelines/platform_factory/outputs
python docs/patcher/shared/build_platform_factory_release_plan.py           ./docs/pipelines/platform_factory/work/05_apply/patched           ./docs/cores/current           ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
```

Puis, seulement si `RELEASE_PLAN.status: PASS` et `RELEASE_PLAN.release_required: true` :

```bash
python docs/patcher/shared/materialize_platform_factory_release.py           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml           ./docs/pipelines/platform_factory/work/05_apply/patched           ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml           ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
```

### STAGE_08_FACTORY_PROMOTE_CURRENT
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`
- Commande :

```bash
python docs/patcher/shared/promote_platform_factory_current.py           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml
```

### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
- Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`
- Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
- Summary attendu : `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
- Commande :

```bash
python docs/patcher/shared/closeout_platform_factory_run.py           ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml           ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml           ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml           ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md           ./docs/pipelines/platform_factory/archive
```

---

## Discipline de sortie minimale

Pour les stages 04 à 09, l’IA ne doit pas noyer l’utilisateur.

Après exécution d’une commande, la sortie attendue côté chat doit tenir en trois éléments :
1. chemins écrits ;
2. statut lu dans le YAML ou report produit ;
3. prochaine action immédiate.
