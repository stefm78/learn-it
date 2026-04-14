# PIPELINE — constitution

id: constitution
version: 1.4
scope: core-governance

## AI startup note

For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
In no-run-id entry mode, the canonical sequence is: `OPEN_NEW_RUN.action.yaml` for entry decision, then `MATERIALIZE_NEW_RUN.action.yaml` for deterministic run materialization, then stop before `STAGE_01_CHALLENGE` unless explicit continuation is requested.

## Goal

Challenger les Core actifs, arbitrer les corrections, produire un patch, le valider, l'appliquer dans une zone de travail et préparer la promotion.
En mode multi-runs parallèles, consolider les résultats des runs avant release.

## Operating modes

Le pipeline `constitution` supporte désormais quatre régimes opératoires :

### Mode nominal global
- aucun `scope_manifest` fourni ;
- aucun `run_id` fourni ;
- le pipeline s'exécute sur le périmètre canonique complet ;
- le comportement reste celui du pipeline historique.

### Mode borné historique de transition
- un `scope_manifest` est fourni dans `inputs/` ;
- le pipeline travaille sur un sous-ensemble borné ;
- le layout plat historique reste utilisé ;
- ce mode est transitoire.

### Mode borné par run (`bounded_local_run`)
- un `run_id` est fourni ;
- le pipeline travaille à partir d'un scope catalogué matérialisé dans `runs/<run_id>/...` ;
- le droit de modifier est gouverné par le `scope_manifest` du run ;
- le devoir de lecture du voisinage logique est gouverné par le `impact_bundle` du run ;
- tout passage vers release/promotion reste soumis au `integration_gate` du run.

### Mode consolidation multi-runs (`parallel_consolidation`)
- plusieurs runs sur scopes disjoints ont été exécutés et clôturés ;
- STAGE_06B_CONSOLIDATION fusionne leurs sandboxes dans `work/consolidation/` ;
- STAGE_07 lit `work/consolidation/` au lieu d'un sandbox individuel ;
- la promotion reste un acte centralisé et explicite via STAGE_08.

Règle structurante :
- un succès local en mode borné n'est jamais équivalent à une cohérence canonique globale acquise ;
- la promotion de `current/` reste un acte centralisé et explicite.


### Mode de maintenance optionnel `partition_refresh`
- aucun `run_id` actif ne doit exister ;
- ce mode sert uniquement à réviser le partitionnement sémantique des scopes avant ouverture de nouveaux runs ;
- l'analyse de partition suit une chaîne mixte : script déterministe obligatoire, puis revue sémantique assistée par IA, puis arbitrage humain ;
- la publication reste déterministe et passe par mise à jour des policy/decisions canonisés puis régénération du catalogue.

## Canonical resources

### Prompts

- Scope partition review: `docs/prompts/shared/Make00ConstitutionScopePartitionReview.md`
- Challenge: `docs/prompts/shared/Challenge_constitution.md`
- Arbitrage: `docs/prompts/shared/Make04ConstitutionArbitrage.md`
- Patch synthesis: `docs/prompts/shared/Make05CorePatch.md`
- Patch validation: `docs/prompts/shared/Make06PatchValidation.md`
- Core validation: `docs/prompts/shared/Make02CoreValidation.md`
- Execution review: `docs/prompts/shared/Make08PatchExecutionReview.md`
- Release: `docs/prompts/shared/Make07CoreRelease.md`

### Spec and tools

- Analyze scope partition: `docs/patcher/shared/analyze_constitution_scope_partition.py`
- Generate constitution scopes: `docs/patcher/shared/generate_constitution_scopes.py`
- **Materialize run inputs: `docs/patcher/shared/materialize_run_inputs.py`** ← à exécuter avant STAGE_01_CHALLENGE
- Patch DSL: `docs/specs/patch-dsl/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`
- `Build release plan: docs/patcher/shared/build_release_plan.py`
- `Materialize release: docs/patcher/shared/materialize_release.py`
- `Validate release plan: docs/patcher/shared/validate_release_plan.py`
- `Closeout pipeline run: docs/patcher/shared/closeout_pipeline_run.py`
- **Consolidate parallel runs: `docs/patcher/shared/consolidate_parallel_runs.py`** ← STAGE_06B uniquement

### Core inputs

Canonical inputs:
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Historical flat bounded-run control inputs:
- `docs/pipelines/constitution/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/inputs/integration_gate.yaml`

Run-based bounded-run control inputs:
- `docs/pipelines/constitution/runs/<run_id>/run_manifest.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/runs/<run_id>/inputs/integration_gate.yaml`

Consolidation work inputs (mode parallel_consolidation uniquement) :
- `docs/pipelines/constitution/work/consolidation/constitution.yaml`
- `docs/pipelines/constitution/work/consolidation/referentiel.yaml`
- `docs/pipelines/constitution/work/consolidation/link.yaml`
- `docs/pipelines/constitution/work/consolidation/consolidation_report.yaml`

## Layout resolution

Reference companion:
- `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`

Resolution rules:
- if `run_id` is provided and the run exists, the pipeline must resolve paths from `docs/pipelines/constitution/runs/<run_id>/...`
- else if `inputs/scope_manifest.yaml` exists, the pipeline may run in bounded transition mode using the historical flat layout
- else the pipeline runs in nominal global mode
- bounded runs should no longer open new artifacts in the flat historical layout except during explicit transition handling

Consolidation resolution rule (STAGE_07 only) :
- if `docs/pipelines/constitution/work/consolidation/consolidation_report.yaml` exists
  and its `consolidation_report.status` is `PASS`,
  STAGE_07 must read Core inputs from `work/consolidation/` instead of individual run sandboxes ;
- otherwise STAGE_07 reads from the resolved run sandbox as usual.

## Staging

Historical flat layout:
- inputs: `docs/pipelines/constitution/inputs/`
- work/01_challenge: `docs/pipelines/constitution/work/01_challenge/`
- work/02_arbitrage: `docs/pipelines/constitution/work/02_arbitrage/`
- work/03_patch: `docs/pipelines/constitution/work/03_patch/`
- work/04_patch_validation: `docs/pipelines/constitution/work/04_patch_validation/`
- work/05_apply: `docs/pipelines/constitution/work/05_apply/`
- work/06_core_validation: `docs/pipelines/constitution/work/06_core_validation/`
- work/consolidation: `docs/pipelines/constitution/work/consolidation/` (mode parallel_consolidation uniquement)
- work/07_release: `docs/pipelines/constitution/work/07_release/`
- outputs: `docs/pipelines/constitution/outputs/`
- reports: `docs/pipelines/constitution/reports/`
- archive: `docs/pipelines/constitution/archive/`

Run-based layout:
- `docs/pipelines/constitution/runs/<run_id>/inputs/`
- `docs/pipelines/constitution/runs/<run_id>/work/01_challenge/`
- `docs/pipelines/constitution/runs/<run_id>/work/02_arbitrage/`
- `docs/pipelines/constitution/runs/<run_id>/work/03_patch/`
- `docs/pipelines/constitution/runs/<run_id>/work/04_patch_validation/`
- `docs/pipelines/constitution/runs/<run_id>/work/05_apply/`
- `docs/pipelines/constitution/runs/<run_id>/work/06_core_validation/`
- `docs/pipelines/constitution/runs/<run_id>/work/07_release/`
- `docs/pipelines/constitution/runs/<run_id>/reports/`
- `docs/pipelines/constitution/runs/<run_id>/outputs/`
- `docs/pipelines/constitution/runs/<run_id>/archive/`

## Scope control artifacts

### `scope_manifest`
Déclare le périmètre modifiable autorisé du run.
En mode borné, ce qui n'est pas dans le scope ne peut pas être modifié implicitement.

### `impact_bundle`
Déclare le voisinage logique à relire pour travailler sûrement.
Il étend le devoir de lecture, pas le droit de modifier.

### `integration_gate`
Déclare les contrôles globaux à rejouer avant release/promotion.
En mode borné, il bloque toute promotion implicite d'un succès local.

### `run_manifest`
Déclare l'identité du run, son `scope_id`, ses chemins d'exécution et la référence vers la scope definition source.

## Canonical entry actions

When the user does not provide a `run_id`, entry is resolved through two distinct canonical actions:

- `docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml`
  - resolves whether opening a new run is authorized
  - must stop after the entry decision
  - must not write tracking files directly

- `docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml`
  - materially opens the run through deterministic tracking
  - materially generates run inputs via `materialize_run_inputs.py`
  - must stop before `STAGE_01_CHALLENGE`

Structured rule:
- no-run-id startup must not jump directly from entry decision to STAGE_01
- run tracking materialization and input materialization are separate mandatory bootstrap acts
- STAGE_01_CHALLENGE may start only after the run has been materially opened and its inputs materially generated

## Stages


### STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md`

- Rules:
  - `STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md` is the canonical specification for Stage 00
  - Stage 00 is optional
  - Stage 00 is forbidden if any run is active in `docs/pipelines/constitution/runs/index.yaml`
  - any deterministic script declared by the Stage 00 specification is mandatory and must be actually executed before the stage can be declared `done`
  - the AI must never simulate or assume execution of `analyze_constitution_scope_partition.py` or `generate_constitution_scopes.py`
  - Stage 00 must not be declared `done` without real production of `docs/pipelines/constitution/reports/scope_partition_review_report.yaml` by actual execution of `analyze_constitution_scope_partition.py`
  - the scope catalog regeneration must not be declared done without actual execution of `generate_constitution_scopes.py --apply` and real production of `tmp/constitution_scope_generation_report.yaml`
  - if the AI cannot execute the required scripts itself, it must provide the exact commands to the user and keep the stage non-final until real execution feedback is available
  - any AI semantic review remains advisory until policy/decisions are updated and the scope catalog is regenerated deterministically

### STAGE_01_CHALLENGE

- Pre-condition (bounded_local_run mode only):
  - `runs/<run_id>/inputs/scope_manifest.yaml`, `impact_bundle.yaml` and `integration_gate.yaml` must exist before this stage starts.
  - If they are absent, run the deterministic materialization script first:
    `python docs/patcher/shared/materialize_run_inputs.py --run-id <run_id>`
  - The AI must never simulate or assume execution of `materialize_run_inputs.py`.
  - If the AI cannot execute the script itself, it must provide the exact command and keep the stage non-started until the user confirms execution.

- Inputs:
  - current cores
  - optional focus note
  - optional `run_id`
  - optional run-scoped inputs under `runs/<run_id>/inputs/`
  - optional flat `inputs/scope_manifest.yaml`
  - optional flat `inputs/impact_bundle.yaml`
- Prompt:
  - `docs/prompts/shared/Challenge_constitution.md`
- Rules:
  - if `run_id` is present, the stage runs in bounded run mode and writes in `runs/<run_id>/work/01_challenge/`
  - else if `scope_manifest.yaml` is present, the stage runs in bounded transition mode in the flat layout
  - else the stage runs in nominal global mode
  - any impact, weakness, contradiction or required change detected outside the declared scope must be explicitly flagged as `out_of_scope`
  - no hidden recommendation of out-of-scope modification is allowed
- Output:
  - flat mode: `work/01_challenge/challenge_report_##.md`
  - run mode: `runs/<run_id>/work/01_challenge/challenge_report_##.md`

### STAGE_02_ARBITRAGE

- Inputs:
  - challenge reports from the resolved challenge directory
  - optional human arbitrage notes
  - optional `run_id`
  - optional resolved `scope_manifest`
  - optional resolved `impact_bundle`
- Prompt:
  - `docs/prompts/shared/Make04ConstitutionArbitrage.md`
- Rule:
  - every `challenge_report*.md` file present in the resolved challenge directory must be considered during arbitrage
  - the arbitrage must consolidate all retained, rejected, deferred, or out-of-scope findings into a single decision record
  - in bounded mode, the arbitrage must distinguish retained in-scope findings, retained out-of-scope findings, and deferred findings caused by scope limits
  - any required scope extension must be made explicit
- Output:
  - flat mode: `work/02_arbitrage/arbitrage.md`
  - run mode: `runs/<run_id>/work/02_arbitrage/arbitrage.md`
### STAGE_03_PATCH_SYNTHESIS

- Inputs:
  - current cores
  - challenge report from the resolved challenge directory
  - arbitrage from the resolved arbitrage directory
  - optional `run_id`
  - optional resolved `scope_manifest`
- Prompt:
  - `docs/prompts/shared/Make05CorePatch.md`
- Rules:
  - in nominal mode, patch synthesis remains global
  - in bounded mode, the patch must remain inside the declared writable scope
  - any dependency outside the scope that cannot be ignored must be flagged explicitly
  - no silent out-of-scope modification is allowed
- Output:
  - flat mode: `work/03_patch/patchset.yaml`
  - run mode: `runs/<run_id>/work/03_patch/patchset.yaml`

### STAGE_04_PATCH_VALIDATION
Objectif :
- vérifier que le patch synthétisé au Stage 03 est structurellement valide
- vérifier qu'il reste minimal, cohérent et compatible avec la séparation Constitution / Référentiel / LINK
- en mode borné, vérifier qu'il n'écrit pas hors du scope déclaré
- décider s'il est autorisé ou non à passer au Stage 05_APPLY

Inputs :
- patchset depuis le répertoire résolu de Stage 03
- contexte d'arbitrage depuis le répertoire résolu de Stage 02
- optional `run_id`
- optional resolved `scope_manifest`
- éventuellement le prompt de revue :
  - `docs/prompts/shared/Make06PatchValidation.md`

Commandes de référence :
- validation structurelle automatique du patchset en layout plat :
  - `python docs/patcher/shared/validate_patchset.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml > ./docs/pipelines/constitution/work/04_patch_validation/patch_validation.yaml`
- validation structurelle automatique du patchset en layout run :
  - `python docs/patcher/shared/validate_patchset.py ./docs/pipelines/constitution/runs/<run_id>/work/03_patch/patchset.yaml > ./docs/pipelines/constitution/runs/<run_id>/work/04_patch_validation/patch_validation.yaml`

Vérifications attendues :
- présence de `PATCH_SET`
- `patch_dsl_version` déclaré et compatible
- `atomic` déclaré
- présence de `files`
- opérations supportées uniquement
- cohérence minimale des opérations `rename`, `rewrite_references`, `replace_field`, `replace_text`
- cohérence du bloc `federation` si des références inter-Core fines sont utilisées
- absence d'anomalie bloquante dans la structure du patchset
- en mode borné, absence d'écriture hors du périmètre autorisé ou signalement explicite du dépassement

Revue logique attendue en complément :
- patch sûr
- patch minimal
- patch cohérent avec la répartition Constitution / Référentiel / LINK
- absence de logique métier autonome introduite dans le LINK
- absence de régression évidente de gouvernance
- absence de déplacement injustifié de logique entre couches
- réécriture des références prévue si nécessaire
- en mode borné, cohérence du patch avec le `scope_manifest`

Interprétation du résultat :
- si `patch_validation.yaml` retourne `status: PASS`, le patch peut être considéré comme structurellement recevable pour le Stage 05
- si `patch_validation.yaml` retourne `status: FAIL`, le pipeline s'arrête ici et le patch doit être corrigé dans le répertoire résolu de Stage 03 avant nouvelle validation
- un `PASS` structurel n'exonère pas d'une revue logique ciblée si le patch modifie des bindings inter-Core sensibles
- le dry-run du Stage 05 constitue la validation exécutable finale avant apply réel
- en mode borné, un PASS local ne vaut pas clearance globale d'intégration

Tools :
- `docs/patcher/shared/validate_patchset.py`
- `docs/prompts/shared/Make06PatchValidation.md`

Outputs :
- flat mode: `work/04_patch_validation/patch_validation.yaml`, `reports/patch_validation_report.md`
- run mode: `runs/<run_id>/work/04_patch_validation/patch_validation.yaml`, `runs/<run_id>/reports/patch_validation_report.md`

Règle opératoire :
- `patch_validation.yaml` est la trace canonique de validation automatique du Stage 04
- `patch_validation_report.md` est une trace de lecture humaine complémentaire, utile si une revue logique explicite est produite
- aucun passage à l'apply réel du Stage 05 ne doit avoir lieu sans validation `PASS`
- l'exécution réelle de `docs/patcher/shared/validate_patchset.py` est obligatoire ; la validation structurelle ne peut jamais être simulée, supposée ou remplacée par une simple lecture du patchset
- le Stage 04 ne peut pas être déclaré `done` tant que `patch_validation.yaml` n'a pas été produit par exécution effective du script de validation sur le patchset cible
- si l'IA ne peut pas exécuter elle-même le script, elle doit fournir explicitement à l'utilisateur la commande exacte à lancer et ne pas conclure le stage comme entièrement validé avant retour du résultat
- la revue logique humaine ou assistée par IA vient seulement en complément de la validation structurelle automatique, jamais en substitution

### STAGE_05_APPLY
Objectif :
- appliquer le patch validé dans une zone de travail isolée
- produire une trace d'exécution exploitable
- matérialiser les Core patchés sans modifier directement `docs/cores/current/`

Inputs :
- patchset depuis le répertoire résolu de Stage 03
- patch validation depuis le répertoire résolu de Stage 04
- copies de référence issues de :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

Précondition :
- la validation du répertoire résolu Stage 04 doit être en `status: PASS`

Principe opératoire :
- le patchset peut continuer à référencer les chemins canoniques `docs/cores/current/*.yaml`
- l'application réelle du patch se fait sur une racine sandbox située sous le répertoire résolu `work/05_apply/`
- la sandbox reproduit la structure canonique du repo pour éviter toute réécriture du patchset d'exécution
- `docs/cores/current/` ne doit jamais être modifié directement par ce stage
- en mode borné, le succès d'apply reste un succès local tant que le `integration_gate` n'est pas clarifié

Commandes de référence layout plat :
- préparer la racine sandbox :
  - `mkdir -p ./docs/pipelines/constitution/work/05_apply/sandbox/docs/cores/current`
- dry-run :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml ./docs/pipelines/constitution/work/05_apply/sandbox true ./docs/pipelines/constitution/reports/patch_execution_report.yaml`
- apply :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/work/03_patch/patchset.yaml ./docs/pipelines/constitution/work/05_apply/sandbox false ./docs/pipelines/constitution/reports/patch_execution_report.yaml`

Commandes de référence layout run :
- préparer la racine sandbox :
  - `mkdir -p ./docs/pipelines/constitution/runs/<run_id>/work/05_apply/sandbox/docs/cores/current`
- dry-run :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/runs/<run_id>/work/03_patch/patchset.yaml ./docs/pipelines/constitution/runs/<run_id>/work/05_apply/sandbox true ./docs/pipelines/constitution/runs/<run_id>/reports/patch_execution_report.yaml`
- apply :
  - `python docs/patcher/shared/apply_patch.py ./docs/pipelines/constitution/runs/<run_id>/work/03_patch/patchset.yaml ./docs/pipelines/constitution/runs/<run_id>/work/05_apply/sandbox false ./docs/pipelines/constitution/runs/<run_id>/reports/patch_execution_report.yaml`

Outputs :
- flat mode: `work/05_apply/sandbox/`, `work/05_apply/patched/`, `reports/patch_execution_report.yaml`
- run mode: `runs/<run_id>/work/05_apply/sandbox/`, `runs/<run_id>/work/05_apply/patched/`, `runs/<run_id>/reports/patch_execution_report.yaml`

Règle opératoire supplémentaire :
- l'exécution réelle de `docs/patcher/shared/apply_patch.py` en dry-run est obligatoire avant tout apply réel
- si l'apply réel fait partie du stage courant, son exécution réelle est également obligatoire ; elle ne peut jamais être simulée, supposée ou remplacée par une simple lecture du patchset
- le Stage 05 ne peut pas être déclaré `done` tant que `reports/patch_execution_report.yaml` n'a pas été produit par exécution effective du script sur la sandbox cible
- si l'IA ne peut pas exécuter elle-même le script, elle doit fournir explicitement à l'utilisateur les commandes exactes à lancer et ne pas conclure le stage comme entièrement exécuté avant retour du résultat réel
- aucune matérialisation de `sandbox/` ou `patched/` ne doit être décrite comme faite si elle n'a pas été effectivement produite par l'exécution du script et les copies attendues

### STAGE_06_CORE_VALIDATION

- Inputs:
  - patched cores from the resolved apply directory
  - optional `run_id`
  - optional resolved `scope_manifest`
  - optional resolved `integration_gate`
- Prompt:
  - `docs/prompts/shared/Make02CoreValidation.md`
- Rules:
  - in nominal mode, this stage remains the standard post-apply core validation
  - in bounded mode, this stage must distinguish local scope validation from full global validation
  - any unmet global recheck requirement must be propagated to the `integration_gate`
- Outputs:
  - flat mode: `work/06_core_validation/core_validation.yaml`, `reports/core_validation_report.md`
  - run mode: `runs/<run_id>/work/06_core_validation/core_validation.yaml`, `runs/<run_id>/reports/core_validation_report.md`

### STAGE_06B_CONSOLIDATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_06B_CONSOLIDATION.md`

- Rules:
  - `STAGE_06B_CONSOLIDATION.md` is the canonical specification for Stage 06B
  - Stage 06B is **optionnel** si un seul run a été exécuté (STAGE_07 lit le sandbox du run directement)
  - Stage 06B est **obligatoire** avant STAGE_07 quand deux runs parallèles ou plus sur scopes disjoints ont été complétés
  - Stage 06B ne peut pas tourner tant qu'un run actif existe dans `runs/index.yaml`
  - l'exécution réelle de `consolidate_parallel_runs.py` est obligatoire ; la consolidation ne peut pas être simulée ou supposée
  - si `work/consolidation/consolidation_report.yaml` retourne `status: FAIL`, le pipeline s'arrête et les conflits de scope doivent être résolus avant nouvelle tentative
  - si l'IA ne peut pas exécuter le script elle-même, elle doit fournir les commandes exactes à l'utilisateur et garder le stage non final jusqu'à retour du résultat réel

### STAGE_07_RELEASE_MATERIALIZATION
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_07_RELEASE_MATERIALIZATION.md`

- Rule:
  - `STAGE_07_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07
  - in bounded mode, no release materialization may be treated as promotable if the resolved `integration_gate` is not explicitly cleared
  - **input resolution rule** : if `docs/pipelines/constitution/work/consolidation/consolidation_report.yaml`
    exists and its `consolidation_report.status` is `PASS`, this stage must read Core inputs
    from `work/consolidation/` instead of the individual run sandbox `work/05_apply/patched/` ;
    otherwise the stage reads from the resolved run sandbox as usual
  - any deterministic script declared by the Stage 07 specification is mandatory and must be actually executed before the stage can be declared `done`
  - the AI may comment or challenge the script outputs, but must never replace their execution with a simulated result
  - if the AI cannot execute the required scripts itself, it must provide the exact commands to the user and keep the stage non-final until real outputs are available
  - Stage 07 must not be declared `done` without real production of the required script artifacts, including at minimum `work/07_release/release_plan.yaml` and the materialization/validation traces required by the Stage 07 specification

### STAGE_08_PROMOTE_CURRENT
- Spec détaillée :
  - `docs/pipelines/constitution/STAGE_08_PROMOTE_CURRENT.md`

- Rule:
  - `STAGE_08_PROMOTE_CURRENT.md` is the canonical specification for Stage 08
  - in bounded mode, promotion remains blocked until global checks required by the resolved `integration_gate` are explicitly satisfied
  - any deterministic script declared by the Stage 08 specification is mandatory and must be actually executed before the stage can be declared `done`
  - the AI must never simulate promotion, manifest validation, or promotion report validation
  - if the AI cannot execute the required scripts itself, it must provide the exact commands to the user and keep the stage non-final until real outputs are available
  - Stage 08 must not be declared `done` without real production of `docs/cores/current/manifest.yaml`, `reports/promotion_report.yaml`, and the required validation outputs defined by the Stage 08 specification

### STAGE_09_CLOSEOUT_AND_ARCHIVE
Objectif :
- clôturer explicitement le run du pipeline après promotion réussie
- archiver le run terminé sous un répertoire d'archive cohérent avec le layout résolu
- réinitialiser l'espace de travail du run courant
- conserver une trace finale de clôture exploitable humainement et techniquement

Inputs :
- promotion report depuis le répertoire résolu de reports
- `docs/cores/current/manifest.yaml`
- release plan depuis le répertoire résolu de `work/07_release/`
- release materialization report depuis le répertoire résolu de reports
- patch execution report depuis le répertoire résolu de reports
- core validation depuis le répertoire résolu de `work/06_core_validation/`

Préconditions :
- le promotion report résolu doit être en `status: PASS`
- `docs/cores/current/manifest.yaml` doit être valide
- `docs/cores/current/manifest.yaml` doit pointer vers la release promue par le Stage 08

Principe opératoire :
- vérifier que la promotion Stage 08 constitue bien l'état actif final du run
- produire le closeout report et le final run summary dans le layout résolu
- archiver une copie complète du run terminé sous le répertoire d'archive résolu
- considérer l'espace `work/` du run comme transitoire et non comme archive canonique
- ne modifier ni `docs/cores/releases/` ni `docs/cores/current/`

Règle opératoire :
- en layout plat, le comportement historique reste valable
- en layout run, l'archive et le reset s'appliquent au run courant sous `runs/<run_id>/...`
- le Stage 09 clôture, archive et réinitialise ; il ne recalcule aucun contenu métier
- si `docs/patcher/shared/closeout_pipeline_run.py` est utilisé comme script canonique de clôture, son exécution réelle est obligatoire avant de déclarer le stage `done`
- l'IA ne doit jamais simuler une clôture, une archive ou un reset de workspace si les artefacts correspondants n'ont pas été effectivement produits
- si l'IA ne peut pas exécuter le script de clôture elle-même, elle doit fournir la commande exacte à l'utilisateur et garder le stage non final tant que le résultat réel n'est pas disponible

## Success criteria

- No stage may be skipped
- Stage 00 partition review may only run when no active run exists and must never mutate the published partition without deterministic regeneration
- Stage 00 must not be declared `done` without real production of `scope_partition_review_report.yaml` by actual execution of `analyze_constitution_scope_partition.py` and real production of `tmp/constitution_scope_generation_report.yaml` by actual execution of `generate_constitution_scopes.py --apply`
- No file in `current/` may be modified directly before explicit promotion
- Any patch application must occur in a sandbox root under the resolved `work/05_apply/`
- Any release materialization must write immutable artifacts under `docs/cores/releases/`
- Promotion to `current/` must remain explicit and occur in a dedicated stage
- Any successful promotion should be followed by an explicit archive-and-reset closeout stage
- In bounded mode, no silent out-of-scope modification is allowed
- In bounded mode, no promotion may occur until the `integration_gate` is explicitly cleared
- In run mode, the run instance is the primary execution unit and its own `work/`, `reports/`, `outputs/` and `archive/` directories are authoritative for the local cycle
- Any stage that depends on a mandatory deterministic script must not be declared `done` until that script has been actually executed and its expected artifacts have been materially produced
- In bounded_local_run mode, `materialize_run_inputs.py` must be executed before STAGE_01_CHALLENGE; its execution cannot be simulated or assumed
- In parallel_consolidation mode, `consolidate_parallel_runs.py` must produce `work/consolidation/consolidation_report.yaml` with `status: PASS` before STAGE_07 may start
