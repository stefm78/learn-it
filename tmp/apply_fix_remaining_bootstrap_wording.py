from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

path = Path("tmp/pipeline_launcher.py")
text = path.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1) Docstring: annoncer RECONCILE_RUN
# -------------------------------------------------------------------
text = replace_once(
    text,
    """Scope of contract binding in this candidate:
- constitution entry actions only
- OPEN_NEW_RUN / CONTINUE_ACTIVE_RUN / DISAMBIGUATE / INSPECT / PARTITION_REFRESH
""",
    """Scope of contract binding in this candidate:
- constitution entry actions only
- OPEN_NEW_RUN / CONTINUE_ACTIVE_RUN / RECONCILE_RUN / DISAMBIGUATE / INSPECT / PARTITION_REFRESH
""",
    "docstring entry actions scope",
)

# -------------------------------------------------------------------
# 2) render_entry_action_prompt: prendre en charge RECONCILE_RUN
# -------------------------------------------------------------------
old = """    elif action_id == "CONTINUE_ACTIVE_RUN":
        instance_parts.append(f"run_id={bindings.get('run_id', '')}")
        instance_parts.append(f"scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"current_stage={bindings.get('current_stage', '')}")
    elif action_id == "DISAMBIGUATE":
"""

new = """    elif action_id == "CONTINUE_ACTIVE_RUN":
        instance_parts.append(f"run_id={bindings.get('run_id', '')}")
        instance_parts.append(f"scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"current_stage={bindings.get('current_stage', '')}")
    elif action_id == "RECONCILE_RUN":
        instance_parts.append(f"run_id={bindings.get('run_id', '')}")
        instance_parts.append(f"scope_key={bindings.get('scope_key', '')}")
        instance_parts.append(f"current_stage={bindings.get('current_stage', '')}")
    elif action_id == "DISAMBIGUATE":
"""

text = replace_once(text, old, new, "render_entry_action_prompt RECONCILE_RUN binding")

# -------------------------------------------------------------------
# 3) discover_constitution: enrichir chaque run avec anomaly_detected / code
# -------------------------------------------------------------------
old = """    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if probe.get("effective_current_stage"):
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        merged_run["task_view_status"] = probe.get("task_view_status", "")
        merged_run["terminal_closed"] = probe.get("terminal_closed", False)
        merged_run["compact_execution_prompt"] = probe.get("compact_execution_prompt", "")
        enriched_runs.append({**merged_run, "ids_first": probe})
"""

new = """    enriched_runs = []
    for run in active_runs:
        run_id = run.get("run_id", "")
        probe = probe_run_context(pipeline_root, run_id)
        merged_run = {**run}
        if probe.get("effective_current_stage"):
            merged_run["current_stage"] = probe["effective_current_stage"]
            merged_run["current_stage_source"] = "run_context.yaml"
        else:
            merged_run["current_stage_source"] = "index.yaml"
        merged_run["task_view_status"] = probe.get("task_view_status", "")
        merged_run["terminal_closed"] = probe.get("terminal_closed", False)
        merged_run["compact_execution_prompt"] = probe.get("compact_execution_prompt", "")
        run_manifest_path = pipeline_root / "runs" / run_id / "run_manifest.yaml"
        anomaly = detect_abnormal_state(run, probe, run_manifest_path)
        if anomaly:
            merged_run["anomaly_detected"] = anomaly["reason"]
            merged_run["anomaly_code"] = anomaly["code"]
            merged_run["recommended_entry_action"] = "RECONCILE_RUN"
        else:
            merged_run["recommended_entry_action"] = "CONTINUE_ACTIVE_RUN"
        enriched_runs.append({**merged_run, "ids_first": probe})
"""

text = replace_once(text, old, new, "discover_constitution enriched_runs anomaly annotation")

# -------------------------------------------------------------------
# 4) discover_constitution: remonter l'anomalie du run recommandé
# -------------------------------------------------------------------
old = """    elif len(executable_active_runs) == 1:
        run = executable_active_runs[0]
        other_scopes = [s for s in enriched_scopes if s.get("scope_key") != run.get("scope_key")]
        result.update(
            {
                "recommended_action": "CONTINUE_ACTIVE_RUN",
                "recommended_run_id": run.get("run_id"),
                "recommended_scope_key": run.get("scope_key"),
                "recommended_current_stage": run.get("current_stage"),
                "recommended_ids_first": run.get("ids_first", {}),
                "other_available_scopes": other_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in other_scopes),
            }
        )
"""

new = """    elif len(executable_active_runs) == 1:
        run = executable_active_runs[0]
        other_scopes = [s for s in enriched_scopes if s.get("scope_key") != run.get("scope_key")]
        result.update(
            {
                "recommended_action": "CONTINUE_ACTIVE_RUN",
                "recommended_run_id": run.get("run_id"),
                "recommended_scope_key": run.get("scope_key"),
                "recommended_current_stage": run.get("current_stage"),
                "recommended_ids_first": run.get("ids_first", {}),
                "recommended_entry_action": run.get("recommended_entry_action", "CONTINUE_ACTIVE_RUN"),
                "recommended_anomaly_detected": run.get("anomaly_detected", ""),
                "recommended_anomaly_code": run.get("anomaly_code", ""),
                "other_available_scopes": other_scopes,
                "can_open_new_run_on_other_scope_now": any(s["maturity_available_for_run"] for s in other_scopes),
            }
        )
"""

text = replace_once(text, old, new, "discover_constitution recommended run anomaly propagation")

# -------------------------------------------------------------------
# 5) build_continue_actions: ajouter l'option reconcile
# -------------------------------------------------------------------
old = """def build_continue_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    ids_first = state.get("recommended_ids_first", {})
    other_scopes = state.get("other_available_scopes", [])
    other_scope_choices = [_scope_choice_entry(s) for s in other_scopes]
    pipeline_id = state.get("pipeline_id", "constitution")
    continue_available = ids_first.get("task_view_status") != "terminal_closed"

    entry_prompt = render_entry_action_prompt(
        repo_root,
        branch=branch,
        pipeline_id=pipeline_id,
        pipeline_path=pipeline_path,
        action_id="CONTINUE_ACTIVE_RUN",
        bindings={
            "run_id": run_id,
            "scope_key": scope_key,
            "current_stage": current_stage,
        },
    )
    stage_prompt = build_stage_prompt(
        branch, pipeline_id, pipeline_path, run_id, scope_key, current_stage, ids_first
    )

    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "continue" if continue_available else "inspect",
            "active_run": run_id,
            "active_scope": scope_key,
            "active_stage": current_stage,
            "ids_first_ready": ids_first.get("ids_first_ready", False),
            "task_view_status": ids_first.get("task_view_status", ""),
        },
        "action_menu": [
            {
                "key": "continue",
                "label": "Continue active run",
                "available": continue_available,
                "recommended": continue_available,
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
            },
            {
                "key": "new_run",
                "label": "Open new run on another published scope",
                "available": bool(other_scope_choices),
                "recommended": False,
                "scope_choices": other_scope_choices,
            },
            {
                "key": "inspect",
                "label": "Inspect current run state only",
                "available": True,
                "recommended": not continue_available,
                "run_id": run_id,
            },
        ],
        "next_best_actions": {
            "continue": {
                "entry_prompt": entry_prompt,
                "stage_prompt": stage_prompt,
                "status": "available" if continue_available else "unavailable_terminal_closed",
            },
            "new_run": {
                "status": "available" if other_scope_choices else "unavailable_now",
                "scope_choices": other_scope_choices,
            },
            "inspect": {
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pipeline_id,
                    pipeline_path=pipeline_path,
                    action_id="INSPECT",
                    bindings={"run_id": run_id},
                )
            },
        },
    }
"""

new = """def build_continue_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    run_id = state["recommended_run_id"]
    scope_key = state["recommended_scope_key"]
    current_stage = state["recommended_current_stage"]
    ids_first = state.get("recommended_ids_first", {})
    other_scopes = state.get("other_available_scopes", [])
    other_scope_choices = [_scope_choice_entry(s) for s in other_scopes]
    pipeline_id = state.get("pipeline_id", "constitution")
    continue_available = ids_first.get("task_view_status") != "terminal_closed"
    anomaly_detected = state.get("recommended_anomaly_detected", "")
    anomaly_code = state.get("recommended_anomaly_code", "")
    reconcile_recommended = bool(anomaly_detected)

    entry_prompt = render_entry_action_prompt(
        repo_root,
        branch=branch,
        pipeline_id=pipeline_id,
        pipeline_path=pipeline_path,
        action_id="CONTINUE_ACTIVE_RUN",
        bindings={
            "run_id": run_id,
            "scope_key": scope_key,
            "current_stage": current_stage,
        },
    )
    reconcile_prompt = render_entry_action_prompt(
        repo_root,
        branch=branch,
        pipeline_id=pipeline_id,
        pipeline_path=pipeline_path,
        action_id="RECONCILE_RUN",
        bindings={
            "run_id": run_id,
            "scope_key": scope_key,
            "current_stage": current_stage,
        },
    )
    stage_prompt = build_stage_prompt(
        branch, pipeline_id, pipeline_path, run_id, scope_key, current_stage, ids_first
    )

    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "reconcile" if reconcile_recommended else ("continue" if continue_available else "inspect"),
            "active_run": run_id,
            "active_scope": scope_key,
            "active_stage": current_stage,
            "ids_first_ready": ids_first.get("ids_first_ready", False),
            "task_view_status": ids_first.get("task_view_status", ""),
            "anomaly_detected": anomaly_detected,
            "anomaly_code": anomaly_code,
        },
        "action_menu": [
            {
                "key": "continue",
                "label": "Continue active run",
                "available": continue_available,
                "recommended": continue_available and not reconcile_recommended,
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
            },
            {
                "key": "reconcile",
                "label": "Reconcile active run before resuming",
                "available": True,
                "recommended": reconcile_recommended,
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
                "reason": anomaly_detected,
            },
            {
                "key": "new_run",
                "label": "Open new run on another published scope",
                "available": bool(other_scope_choices),
                "recommended": False,
                "scope_choices": other_scope_choices,
            },
            {
                "key": "inspect",
                "label": "Inspect current run state only",
                "available": True,
                "recommended": not continue_available and not reconcile_recommended,
                "run_id": run_id,
            },
        ],
        "next_best_actions": {
            "continue": {
                "entry_prompt": entry_prompt,
                "stage_prompt": stage_prompt,
                "status": "available" if continue_available else "unavailable_terminal_closed",
            },
            "reconcile": {
                "entry_prompt": reconcile_prompt,
                "status": "available",
                "reason": anomaly_detected,
            },
            "new_run": {
                "status": "available" if other_scope_choices else "unavailable_now",
                "scope_choices": other_scope_choices,
            },
            "inspect": {
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pipeline_id,
                    pipeline_path=pipeline_path,
                    action_id="INSPECT",
                    bindings={"run_id": run_id},
                )
            },
        },
    }
"""

text = replace_once(text, old, new, "build_continue_actions reconcile support")

path.write_text(text, encoding="utf-8")
print("OK: tmp/pipeline_launcher.py mis à jour pour RECONCILE_RUN")