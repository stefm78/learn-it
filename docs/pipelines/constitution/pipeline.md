# PIPELINE — constitution

id: constitution
version: 1.4
scope: core-governance

## AI startup note

For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
In no-run-id entry mode, the canonical sequence is: `OPEN_NEW_RUN.action.yaml` for entry decision, then `MATERIALIZE_NEW_RUN.action.yaml` for deterministic run materialization, then stop before `STAGE_01_CHALLENGE` unless explicit continuation is requested.
The first act must stop after the decision, but must also emit the next canonical action to the chat. When `OPEN_NEW_RUN` returns `open_new_run_authorized`, the next canonical action is `MATERIALIZE_NEW_RUN`.
In run_id_mode, canonical run handling may also pass through `RECONCILE_RUN.action.yaml` before any stage restart, when a run must be brought back into line against the current stable contracts.

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
- Score constitution scope maturity: `docs/patcher/shared/score_constitution_scope_maturity.py`
- Apply computed maturity scores: `docs/patcher/shared/apply_constitution_scope_maturity_scores.py`
- Report Constitution neighbor IDs governance: `docs/patcher/shared/report_constitution_neighbor_ids_governance.py`
- Prepare Constitution neighbor IDs arbitration: `docs/patcher/shared/prepare_constitution_neighbor_ids_arbitration.py`
- Validate Constitution neighbor IDs arbitration: `docs/patcher/shared/validate_constitution_neighbor_ids_arbitration.py`
- Apply Constitution neighbor IDs arbitration: `docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py`
- Report Constitution neighbor declaration inventory: `docs/patcher/shared/report_constitution_neighbor_declaration_inventory.py`
- **Materialize run inputs: `docs/patcher/shared/materialize_run_inputs.py`** ← à exécuter pendant MATERIALIZE_NEW_RUN et avant STAGE_01_CHALLENGE
- **Extract ids-first scope slices: `docs/patcher/shared/extract_scope_slice.py`** ← à exécuter pendant MATERIALIZE_NEW_RUN après `materialize_run_inputs.py` et avant `build_run_context.py`
- **Build run context: `docs/patcher/shared/build_run_context.py`** ← à exécuter pendant MATERIALIZE_NEW_RUN après génération des extraits ids-first
- Patch DSL: `docs/specs/patch-dsl/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`
- `Build release plan: docs/patcher/shared/build_release_plan.py`
- `Materialize release: docs/patcher/shared/materialize_release.py`
- `Validate release plan: docs/patcher/shared/validate_release_plan.py`
- `Closeout pipeline run: docs/patcher/shared/closeout_pipeline_run.py`
- **Reconcile run: `docs/patcher/shared/reconcile_run.py`** ← à exécuter en run_id_mode pour remettre un run en ligne sans rejouer les stages métier
- **Consolidate parallel runs: `docs/patcher/shared/consolidate_parallel_runs.py`** ← STAGE_06B uniquement

## Canonical entry actions

### No-run-id startup actions

When the user does not provide a `run_id`, entry is resolved through two distinct canonical actions:

- `docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml`
  - resolves whether opening a new run is authorized
  - must stop after the entry decision
  - must not write tracking files directly
  - must emit the next canonical action in the chat

- `docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml`
  - materially opens the run through deterministic tracking
  - materially generates run inputs via `materialize_run_inputs.py`
  - materially generates ids-first extracts via `extract_scope_slice.py`
  - materially generates `run_context.yaml` via `build_run_context.py`
  - must stop before `STAGE_01_CHALLENGE`
  - must emit `CONTINUE_ACTIVE_RUN` as the next canonical action when bootstrap succeeds

Structured rule:
- no-run-id startup must not jump directly from entry decision to STAGE_01
- run tracking materialization, input materialization, ids-first extract materialization, and run_context materialization are mandatory bootstrap acts
- `OPEN_NEW_RUN` stops on execution, not on guidance: after a successful decision it must point explicitly to `MATERIALIZE_NEW_RUN`
- STAGE_01_CHALLENGE may start only after the run has been materially opened, its inputs materially generated, its ids-first extracts materially generated, and `run_context.yaml` materially generated

### Run-id actions

When a `run_id` is already known, canonical handling may use dedicated run-scoped actions instead of jumping directly into stage execution:

- `docs/pipelines/constitution/entry_actions/CONTINUE_ACTIVE_RUN.action.yaml`
  - resolves continuation of a known active run
  - must stop after the continue-or-not decision
  - must not deep-read wider than the identified run

- `docs/pipelines/constitution/entry_actions/RECONCILE_RUN.action.yaml`
  - reconciles a known run against the latest stable contracts
  - repairs derivable artifacts through owner scripts only
  - truncates downstream state that is no longer materially justifiable
  - must stop before any restarted business stage begins

Structured rule:
- run reconciliation is not a business stage and must not be modeled as one
- reconciliation must compute the longest trusted prefix still justified by current contracts
- what is derivable may be rebuilt deterministically; what is no longer justifiable must be cut
- after successful reconciliation, the next canonical action is usually `CONTINUE_ACTIVE_RUN`
