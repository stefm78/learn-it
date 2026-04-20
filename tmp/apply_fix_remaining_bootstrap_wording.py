from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

path = Path("docs/pipelines/constitution/pipeline.md")
text = path.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1) AI startup note
# -------------------------------------------------------------------
old = """## AI startup note

For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
In no-run-id entry mode, the canonical sequence is: `OPEN_NEW_RUN.action.yaml` for entry decision, then `MATERIALIZE_NEW_RUN.action.yaml` for deterministic run materialization, then stop before `STAGE_01_CHALLENGE` unless explicit continuation is requested.
The first act must stop after the decision, but must also emit the next canonical action to the chat. When `OPEN_NEW_RUN` returns `open_new_run_authorized`, the next canonical action is `MATERIALIZE_NEW_RUN`.
"""

new = """## AI startup note

For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
In no-run-id entry mode, the canonical sequence is: `OPEN_NEW_RUN.action.yaml` for entry decision, then `MATERIALIZE_NEW_RUN.action.yaml` for deterministic run materialization, then stop before `STAGE_01_CHALLENGE` unless explicit continuation is requested.
The first act must stop after the decision, but must also emit the next canonical action to the chat. When `OPEN_NEW_RUN` returns `open_new_run_authorized`, the next canonical action is `MATERIALIZE_NEW_RUN`.
In run_id_mode, canonical run handling may also pass through `RECONCILE_RUN.action.yaml` before any stage restart, when a run must be brought back into line against the current stable contracts.
"""

text = replace_once(text, old, new, "AI startup note")

# -------------------------------------------------------------------
# 2) Spec and tools
# -------------------------------------------------------------------
old = """- `Closeout pipeline run: docs/patcher/shared/closeout_pipeline_run.py`
- **Consolidate parallel runs: `docs/patcher/shared/consolidate_parallel_runs.py`** ← STAGE_06B uniquement
"""

new = """- `Closeout pipeline run: docs/patcher/shared/closeout_pipeline_run.py`
- **Reconcile run: `docs/patcher/shared/reconcile_run.py`** ← à exécuter en run_id_mode pour remettre un run en ligne sans rejouer les stages métier
- **Consolidate parallel runs: `docs/patcher/shared/consolidate_parallel_runs.py`** ← STAGE_06B uniquement
"""

text = replace_once(text, old, new, "Spec and tools")

# -------------------------------------------------------------------
# 3) Canonical entry actions section
# -------------------------------------------------------------------
old = """## Canonical entry actions

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
"""

new = """## Canonical entry actions

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
"""

text = replace_once(text, old, new, "Canonical entry actions section")

path.write_text(text, encoding="utf-8")
print("OK: pipeline.md mis à jour pour RECONCILE_RUN")