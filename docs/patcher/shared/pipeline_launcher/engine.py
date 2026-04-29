#!/usr/bin/env python3
"""Registry-aware bootstrap launcher with runtime view + entry action contracts.

Compact prompt candidate:
- keeps --parallel-runs support
- consumes run_context.task_view when available
- avoids proposing continue on terminal closed runs
- loads canonical entry action contracts from docs/pipelines/<id>/entry_actions/
- renders compact entry prompts that reference the canonical contract + instance bindings

Scope of contract binding in this candidate:
- constitution entry actions only
- OPEN_NEW_RUN / CONTINUE_ACTIVE_RUN / RECONCILE_RUN / DISAMBIGUATE / INSPECT / PARTITION_REFRESH

Still experimental: kept in tmp/ until hardened and promoted.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

# Support direct execution as `python docs/patcher/shared/pipeline_launcher/engine.py`
# while importing modules from the repository root.
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.maturity import (
    MATURITY_AXES_COUNT,
    MATURITY_GATED_LEVELS,
    MATURITY_LEVELS,
    MATURITY_MAX_SCORE,
    MATURITY_MINIMUM_LEVEL,
    maturity_level_from_score,
    maturity_pct,
)

from docs.patcher.shared.pipeline_launcher.governance_backlog import (
    attach_governance_backlog_signal,
    build_governance_backlog_scope_summary,
    compact_governance_backlog_signal,
    empty_governance_backlog_signal,
)

from docs.patcher.shared.pipeline_launcher.bounded_preflight import (
    attach_bounded_run_preflight_signal,
    build_bounded_run_preflight_summary,
    compact_bounded_run_preflight_signal,
    empty_bounded_run_preflight_signal,
)

from docs.patcher.shared.pipeline_launcher.entry_actions import (
    load_entry_action_contract,
    load_entry_actions_index,
    render_entry_action_prompt,
    resolve_entry_action_ref,
)

from docs.patcher.shared.pipeline_launcher.run_context import (
    build_stage_prompt,
    ensure_prompt_mentions_branch,
    probe_run_context,
)

from docs.patcher.shared.pipeline_launcher.consolidation import (
    build_bootstrap_command,
    detect_abnormal_state,
    detect_consolidation_ready,
    probe_integration_gate,
)

from docs.patcher.shared.pipeline_launcher.registry import discover_pipelines_from_registry
from docs.patcher.shared.pipeline_launcher.pipeline_state import (
    discover_constitution,
    discover_generic_pipeline,
)

from docs.patcher.shared.pipeline_launcher.yaml_io import load_yaml

CONSOLIDATION_PENDING_STAGES = {
    "STAGE_06_CORE_VALIDATION",
    "STAGE_06B_CONSOLIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
}
_IN_PROGRESS_STALE_THRESHOLD_S = 6 * 3600




def _scope_choice_entry(s: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "scope_key": s["scope_key"],
        "maturity_pct": maturity_pct(s["maturity_score"]),
        "maturity_level": s["maturity_level"],
        "available": s["maturity_available_for_run"],
    }
    if not s["maturity_available_for_run"]:
        entry["gate_reason"] = s["maturity_gate_reason"]
    return entry


def build_continue_actions(
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
                "status": "entry_resolution_available",
                "meaning": "OPEN_NEW_RUN entry prompt is available; this launcher does not authorize, materialize, or start a run.",
                "run_opening_authorized": False,
                "run_materialization_authorized": False,
                "requires_open_new_run_decision": True,
                "requires_human_confirmation_before_materialization": True,
                "reason": anomaly_detected,
            },
            "new_run": {
                "status": "entry_resolution_available" if other_scope_choices else "unavailable_now",
                "meaning": "OPEN_NEW_RUN entry prompt is available; this launcher does not authorize, materialize, or start a run.",
                "run_opening_authorized": False,
                "run_materialization_authorized": False,
                "requires_open_new_run_decision": True,
                "requires_human_confirmation_before_materialization": True,
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


def build_open_new_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    all_scopes = state.get("published_scopes", [])
    scope_choices = [_scope_choice_entry(s) for s in all_scopes]
    available_choices = [c for c in scope_choices if c["available"]]
    gated_choices = [c for c in scope_choices if not c["available"]]
    top_choice = available_choices[0] if available_choices else {}
    entry_prompt = (
        render_entry_action_prompt(
            repo_root,
            branch=branch,
            pipeline_id=pipeline_id,
            pipeline_path=pipeline_path,
            action_id="OPEN_NEW_RUN",
            bindings={
                "scope_key": top_choice.get("scope_key", ""),
                "maturity_pct": top_choice.get("maturity_pct", ""),
                "maturity_level": top_choice.get("maturity_level", ""),
            },
        )
        if available_choices
        else "Aucun scope disponible — publie des scopes d'abord."
    )
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "new_run",
            "active_run": "",
            "active_scope": "",
            "active_stage": "",
        },
        "action_menu": [
            {
                "key": "new_run",
                "label": "Open new run on a published scope",
                "available": bool(available_choices),
                "recommended": True,
                "scope_choices": scope_choices,
                "recommended_scope": top_choice.get("scope_key", ""),
            }
        ],
        "next_best_actions": {
            "new_run": {
                "status": "entry_resolution_available" if available_choices else "unavailable_now",
                "meaning": "OPEN_NEW_RUN entry prompt is available; this launcher does not authorize, materialize, or start a run.",
                "run_opening_authorized": False,
                "run_materialization_authorized": False,
                "requires_open_new_run_decision": True,
                "requires_human_confirmation_before_materialization": True,
                "scope_choices_available": available_choices,
                "scope_choices_gated": gated_choices,
                "entry_prompt": entry_prompt,
            }
        },
    }


def build_disambiguation_actions(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    shortlist = [f"{r.get('run_id','')}:{r.get('scope_key','')}:{r.get('current_stage','')}" for r in state.get("active_runs", [])]
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "disambiguate",
            "active_run": "multiple",
            "active_scope": "multiple",
            "active_stage": "multiple",
        },
        "action_menu": [
            {
                "key": "disambiguate",
                "label": "Choose one active run before any deep read",
                "available": True,
                "recommended": True,
            }
        ],
        "next_best_actions": {
            "disambiguate": {
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pipeline_id,
                    pipeline_path=pipeline_path,
                    action_id="DISAMBIGUATE",
                    bindings={"active_runs_shortlist": shortlist},
                )
            }
        },
    }


def build_consolidate_actions(state: dict[str, Any]) -> dict[str, Any]:
    pipeline_id = state.get("pipeline_id", "constitution")
    probe = state.get("consolidation_probe", {})
    is_solo_promote = probe.get("is_solo_promote", False)
    active_stage = "STAGE_08_PROMOTE_CURRENT" if is_solo_promote else "STAGE_06B_CONSOLIDATION"
    return {
        "decision_summary": {
            "pipeline_id": pipeline_id,
            "recommended_default": "consolidate",
            "active_run": "",
            "active_scope": "pipeline-level",
            "active_stage": active_stage,
            "is_solo_promote": is_solo_promote,
            "all_integration_gates_cleared": probe.get("all_integration_gates_cleared", False),
            "eligible_runs_count": probe.get("eligible_runs_count", 0),
        },
        "action_menu": [
            {
                "key": "consolidate",
                "label": "Run STAGE_08_PROMOTE_CURRENT (solo run)" if is_solo_promote else "Run STAGE_06B consolidation then STAGE_07 and STAGE_08",
                "available": True,
                "recommended": True,
                "is_solo_promote": is_solo_promote,
                "eligible_runs": probe.get("eligible_runs", []),
                "all_gates_cleared": probe.get("all_integration_gates_cleared", False),
                "pending_gates": probe.get("pending_gates", []),
            }
        ],
        "next_best_actions": {
            "consolidate": {
                "consolidation_dry_run_cmd": probe.get("consolidation_dry_run_cmd", ""),
                "consolidation_cmd": probe.get("consolidation_cmd", ""),
                "stage_prompt": probe.get("stage_prompt", ""),
                "guidance": "clear_pending_integration_gates_first" if probe.get("pending_gates") else ("run_stage_08_promote_current_directly" if is_solo_promote else "run_dry_run_then_real_consolidation_then_07_then_08"),
            }
        },
    }


def build_menu(
    repo_root: Path, branch: str, state: dict[str, Any], pipeline_path: str
) -> dict[str, Any]:
    action = state.get("recommended_action")
    if action == "consolidate":
        return build_consolidate_actions(state)
    if action == "CONTINUE_ACTIVE_RUN":
        return build_continue_actions(repo_root, branch, state, pipeline_path)
    if action == "OPEN_NEW_RUN":
        return build_open_new_actions(repo_root, branch, state, pipeline_path)
    return build_disambiguation_actions(repo_root, branch, state, pipeline_path)


def build_parallel_slots(
    repo_root: Path,
    branch: str,
    pipelines: list[dict[str, str]],
    pipeline_states: dict[str, dict[str, Any]],
    n: int,
) -> dict[str, Any]:
    slots: list[dict[str, Any]] = []
    slot_index = 0
    pipelines_with_consolidation_slot: set[str] = set()

    for pipeline_info in pipelines:
        if slot_index >= n:
            break
        pid = pipeline_info.get("pipeline_id", "")
        state = pipeline_states.get(pid, {})
        consolidation_probe = state.get("consolidation_probe")
        if not consolidation_probe:
            continue
        if state.get("active_runs_count", 0) > 0:
            continue
        slots.append(
            {
                "slot": slot_index + 1,
                "pipeline_id": pid,
                "action": "consolidate",
                "is_solo_promote": consolidation_probe.get("is_solo_promote", False),
                "eligible_runs": consolidation_probe.get("eligible_runs", []),
                "all_integration_gates_cleared": consolidation_probe.get("all_integration_gates_cleared", False),
                "pending_gates": consolidation_probe.get("pending_gates", []),
                "consolidation_dry_run_cmd": consolidation_probe.get("consolidation_dry_run_cmd", ""),
                "consolidation_cmd": consolidation_probe.get("consolidation_cmd", ""),
                "stage_prompt": consolidation_probe.get("stage_prompt", ""),
            }
        )
        pipelines_with_consolidation_slot.add(pid)
        slot_index += 1

    for pipeline_info in pipelines:
        pid = pipeline_info.get("pipeline_id", "")
        ppath = pipeline_info.get("path", f"docs/pipelines/{pid}/pipeline.md")
        state = pipeline_states.get(pid, {})
        active_runs = state.get("active_runs", [])
        pipeline_root = repo_root / "docs" / "pipelines" / pid

        for run in active_runs:
            if slot_index >= n:
                break
            run_id = run.get("run_id", "")
            scope_key = run.get("scope_key", "")
            current_stage = run.get("current_stage", "")
            ids_first = run.get("ids_first", {})
            run_status = run.get("run_status", "active")

            if ids_first.get("task_view_status") == "terminal_closed":
                continue

            run_manifest_path = pipeline_root / "runs" / run_id / "run_manifest.yaml"
            anomaly = detect_abnormal_state(run, ids_first, run_manifest_path)
            slot: dict[str, Any] = {
                "slot": slot_index + 1,
                "pipeline_id": pid,
                "action": "continue",
                "run_id": run_id,
                "scope_key": scope_key,
                "current_stage": current_stage,
                "current_stage_source": run.get("current_stage_source", "index.yaml"),
                "ids_first_ready": ids_first.get("ids_first_ready", False),
                "task_view_status": ids_first.get("task_view_status", ""),
                "entry_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=pid,
                    pipeline_path=ppath,
                    action_id="CONTINUE_ACTIVE_RUN",
                    bindings={
                        "run_id": run_id,
                        "scope_key": scope_key,
                        "current_stage": current_stage,
                    },
                ) if pid == "constitution" else "",
                "stage_prompt": build_stage_prompt(branch, pid, ppath, run_id, scope_key, current_stage, ids_first),
            }
            if anomaly:
                slot["anomaly_detected"] = anomaly["reason"]
                slot["bootstrap_command"] = build_bootstrap_command(pid, run_id, current_stage, run_status, anomaly)
            slots.append(slot)
            slot_index += 1

    if slot_index < n:
        active_run_scope_keys: set[str] = set()
        for pid, state in pipeline_states.items():
            for run in state.get("active_runs", []):
                sk = run.get("scope_key", "")
                if sk:
                    active_run_scope_keys.add(f"{pid}:{sk}")

        open_candidates: list[dict[str, Any]] = []
        for pipeline_info in pipelines:
            pid = pipeline_info.get("pipeline_id", "")
            ppath = pipeline_info.get("path", f"docs/pipelines/{pid}/pipeline.md")
            state = pipeline_states.get(pid, {})
            has_consolidation_slot = pid in pipelines_with_consolidation_slot
            if state.get("consolidation_probe") and not has_consolidation_slot:
                continue
            for scope in state.get("published_scopes", []):
                sk = scope.get("scope_key", "")
                if not scope.get("maturity_available_for_run", False):
                    continue
                if f"{pid}:{sk}" in active_run_scope_keys:
                    continue
                candidate: dict[str, Any] = {
                    "pipeline_id": pid,
                    "pipeline_path": ppath,
                    "scope_key": sk,
                    "maturity_score": scope.get("maturity_score", 0),
                    "maturity_level": scope.get("maturity_level", ""),
                    "maturity_pct": maturity_pct(scope.get("maturity_score", 0)),
                }
                if has_consolidation_slot:
                    candidate["parallel_with_consolidation"] = True
                open_candidates.append(candidate)
        open_candidates.sort(key=lambda x: -x["maturity_score"])

        for candidate in open_candidates:
            if slot_index >= n:
                break
            slot_entry: dict[str, Any] = {
                "slot": slot_index + 1,
                "pipeline_id": candidate["pipeline_id"],
                "action": "open_new_run",
                "scope_key": candidate["scope_key"],
                "maturity_level": candidate["maturity_level"],
                "maturity_pct": candidate["maturity_pct"],
                "open_run_prompt": render_entry_action_prompt(
                    repo_root,
                    branch=branch,
                    pipeline_id=candidate["pipeline_id"],
                    pipeline_path=candidate["pipeline_path"],
                    action_id="OPEN_NEW_RUN",
                    bindings={
                        "scope_key": candidate["scope_key"],
                        "maturity_pct": candidate["maturity_pct"],
                        "maturity_level": candidate["maturity_level"],
                    },
                ) if candidate["pipeline_id"] == "constitution" else (
                    f"Dans le repo learn-it, sur la branche {branch}, ouvre un nouveau run sur le pipeline {candidate['pipeline_path']} pour le scope {candidate['scope_key']} ({candidate['maturity_pct']} — {candidate['maturity_level']})."
                ),
            }
            if candidate.get("parallel_with_consolidation"):
                slot_entry["parallel_with_consolidation"] = True
                slot_entry["isolation_note"] = (
                    f"Ce run s'exécute en parallèle d'une consolidation en cours sur ce pipeline. "
                    f"Il doit produire ses livrables uniquement sous docs/pipelines/{candidate['pipeline_id']}/runs/<new_run_id>/. "
                    f"Ne pas toucher docs/cores/current avant que la consolidation soit terminée."
                )
            slots.append(slot_entry)
            slot_index += 1

    return {
        "parallel_slots_requested": n,
        "parallel_slots_available": len(slots),
        "parallelism_safe": True,
        "slots": slots,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--branch", default="feat/core-modularization-bootstrap")
    parser.add_argument("--parallel-runs", type=int, default=None, metavar="N")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    pipelines = discover_pipelines_from_registry(registry_path)

    print("PIPELINE_REGISTRY_STATE:")
    print(yaml.safe_dump({"pipelines": pipelines}, sort_keys=False, allow_unicode=True).rstrip())
    print()

    if args.parallel_runs is not None:
        pipeline_states: dict[str, dict[str, Any]] = {}
        for pipeline_info in pipelines:
            pid = pipeline_info.get("pipeline_id", "")
            if pid == "constitution":
                pipeline_states[pid] = discover_constitution(repo_root)
            else:
                pipeline_states[pid] = discover_generic_pipeline(repo_root, pid)
        parallel = build_parallel_slots(repo_root=repo_root, branch=args.branch, pipelines=pipelines, pipeline_states=pipeline_states, n=args.parallel_runs)
        print("PIPELINE_PARALLEL_SLOTS:")
        print(yaml.safe_dump(parallel, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    pipeline_path = next((p.get("path", "") for p in pipelines if p.get("pipeline_id") == args.pipeline), f"docs/pipelines/{args.pipeline}/pipeline.md")
    if args.pipeline != "constitution":
        print("PIPELINE_LAUNCH_MENU:")
        print(yaml.safe_dump({
            "decision_summary": {"pipeline_id": args.pipeline, "recommended_default": "unsupported"},
            "action_menu": [],
            "next_best_actions": {"unsupported": {"guidance": "use constitution entry action contracts pattern as template"}},
        }, sort_keys=False, allow_unicode=True).rstrip())
        return 0

    state = discover_constitution(repo_root)
    menu = build_menu(repo_root, args.branch, state, pipeline_path)
    print("PIPELINE_LAUNCHER_STATE:")
    print(yaml.safe_dump(state, sort_keys=False, allow_unicode=True).rstrip())
    print()
    print("PIPELINE_LAUNCH_MENU:")
    print(yaml.safe_dump(menu, sort_keys=False, allow_unicode=True).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
