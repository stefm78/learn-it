#!/usr/bin/env python3
"""Build an enriched run_context.yaml with derived runtime task view.

Temporary candidate placed under tmp/ before in-place replacement of
`docs/patcher/shared/build_run_context.py`.

Changes in v2:
- fix Windows/pathlib issue when --output-path is relative
- resolve output path against repo_root before relative display
- graceful fallback when displayed path cannot be relativized

Intent:
- keep run_manifest + inputs as canonical state
- keep run_context.yaml derived-only
- avoid persisted per-run `*.task.yaml`
- expose a minimal executable task view for the current/next stage

Current pilot scope:
- pipeline: constitution
- strongest binding implemented: STAGE_01_CHALLENGE
- generic fallback available for other stages
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required.") from exc

STAGE_ALIASES = {
    "STAGE_05_PATCH_APPLICATION": "STAGE_05_APPLY",
    "STAGE_09_CLOSEOUT": "STAGE_09_CLOSEOUT_AND_ARCHIVE",
}

TERMINAL_CLOSED_STAGES = {
    "STAGE_09_CLOSEOUT",
    "STAGE_09_CLOSEOUT_AND_ARCHIVE",
    "RUN_ABANDONED",
}


def canonical_stage_id(stage_id: str) -> str:
    return STAGE_ALIASES.get(stage_id, stage_id)


def is_terminal_closed_run(run_status: str, stage_id: str, last_stage_status: str) -> bool:
    return run_status == "closed" and stage_id in TERMINAL_CLOSED_STAGES and last_stage_status == "done"

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_yaml_optional(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def substitute_run_id(value: Any, run_id: str) -> Any:
    if isinstance(value, str):
        return value.replace("<run_id>", run_id)
    if isinstance(value, list):
        return [substitute_run_id(v, run_id) for v in value]
    if isinstance(value, dict):
        return {k: substitute_run_id(v, run_id) for k, v in value.items()}
    return value


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def derive_next_executable_stage(exec_state: Dict[str, Any], fallback_current_stage: str, run_status: str) -> tuple[str, str, bool]:
    raw_current_stage = exec_state.get("current_stage") or fallback_current_stage
    last_stage_status = exec_state.get("last_stage_status", "unknown")
    raw_next_stage = exec_state.get("next_stage", "")

    raw_actionable = raw_current_stage
    if last_stage_status == "done" and raw_next_stage and raw_next_stage != raw_current_stage:
        raw_actionable = raw_next_stage

    terminal_closed = is_terminal_closed_run(run_status, raw_actionable, last_stage_status)
    canonical_actionable = canonical_stage_id(raw_actionable)
    return raw_actionable, canonical_actionable, terminal_closed

def stage_num(stage_id: str) -> str:
    if stage_id.startswith("STAGE_") and len(stage_id) >= 8:
        return stage_id[6:8]
    return "XX"


def default_work_dir(run_id: str, stage_id: str) -> str:
    mapping = {
        "00": "00_scope_partition",
        "01": "01_challenge",
        "02": "02_arbitrage",
        "03": "03_patch",
        "04": "04_patch_validation",
        "05": "05_apply",
        "06": "06_core_validation",
        "07": "07_release",
        "08": "08_promote",
        "09": "09_closeout",
    }
    suffix = mapping.get(stage_num(stage_id), f"{stage_num(stage_id)}_stage")
    return f"runs/{run_id}/work/{suffix}/"


def default_primary_output(run_id: str, stage_id: str) -> str:
    num = stage_num(stage_id)
    mapping = {
        "01": f"runs/{run_id}/work/01_challenge/challenge_report_<id>.md",
        "02": f"runs/{run_id}/work/02_arbitrage/arbitrage.md",
        "03": f"runs/{run_id}/work/03_patch/patchset.yaml",
        "04": f"runs/{run_id}/work/04_patch_validation/patch_validation.yaml",
        "05": f"runs/{run_id}/reports/patch_execution_report.yaml",
        "06": f"runs/{run_id}/work/06_core_validation/core_validation.yaml",
        "07": f"runs/{run_id}/work/07_release/release_plan.yaml",
        "08": f"runs/{run_id}/reports/promotion_report.yaml",
        "09": f"runs/{run_id}/reports/closeout_report.yaml",
    }
    return mapping.get(num, f"runs/{run_id}/outputs/{stage_id}.out")


def load_pipeline_model(repo_root: Path, pipeline_id: str) -> Dict[str, Any]:
    path = repo_root / "docs" / "pipelines" / pipeline_id / "PIPELINE_MODEL.yaml"
    data = load_yaml_optional(path)
    return data.get("pipeline_model", {}) if data else {}


def load_stage_skill(repo_root: Path, skill_ref: str) -> Dict[str, Any]:
    path = repo_root / skill_ref
    data = load_yaml_optional(path)
    return data.get("stage_skill", {}) if data else {}


def find_stage_spec(pipeline_model: Dict[str, Any], stage_id: str) -> Dict[str, Any]:
    for stage in pipeline_model.get("stages", []) or []:
        if stage.get("stage_id") == stage_id:
            return stage
    return {}


def resolved_stage_inputs(
    skill: Dict[str, Any],
    run_id: str,
    mode: str,
    stage_id: str,
) -> List[str]:
    primary_reads = skill.get("primary_reads", {}) or {}
    stage_inputs = primary_reads.get(mode)
    if stage_inputs:
        return substitute_run_id(stage_inputs, run_id)

    base = [
        f"runs/{run_id}/inputs/run_context.yaml",
        f"runs/{run_id}/inputs/scope_manifest.yaml",
        f"runs/{run_id}/inputs/impact_bundle.yaml",
        f"runs/{run_id}/inputs/integration_gate.yaml",
    ]
    if stage_id == "STAGE_01_CHALLENGE":
        base.insert(1, f"runs/{run_id}/inputs/scope_extract.yaml")
        base.insert(2, f"runs/{run_id}/inputs/neighbor_extract.yaml")
    return base


def derive_required_scripts_status(
    stage_id: str,
    mode: str,
    scope_extract_status: Dict[str, Any],
    neighbor_extract_status: Dict[str, Any],
) -> Dict[str, Any]:
    ids_first_ready = (
        mode == "bounded_local_run"
        and scope_extract_status.get("present", False)
        and neighbor_extract_status.get("present", False)
        and scope_extract_status.get("missing_ids_count", 0) == 0
    )
    status = {
        "scope_extract_present": scope_extract_status.get("present", False),
        "neighbor_extract_present": neighbor_extract_status.get("present", False),
        "ids_first_ready": ids_first_ready,
    }
    if stage_id != "STAGE_01_CHALLENGE":
        status["note"] = "generic runtime status — stage-specific script status not yet bound"
    return status


def derive_compact_execution_prompt(
    pipeline_id: str,
    run_id: str,
    stage_id: str,
    mode: str,
    skill_ref: str,
    resolved_inputs: List[str],
) -> str:
    inputs_text = ", ".join(resolved_inputs)
    return (
        f"Dans le repo learn-it, exécute {stage_id} du pipeline {pipeline_id} "
        f"pour run_id={run_id} en mode {mode}. Lis d'abord {inputs_text}. "
        f"Applique le contrat stable défini dans {skill_ref}. "
        f"Ne produis que les livrables du stage courant et ne simule aucun script requis."
    )


def build_task_view(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    mode: str,
    raw_stage_id: str,
    canonical_stage: str,
    terminal_closed: bool,
    scope_extract_status: Dict[str, Any],
    neighbor_extract_status: Dict[str, Any],
) -> Dict[str, Any]:
    pipeline_model = load_pipeline_model(repo_root, pipeline_id)
    stage_spec = find_stage_spec(pipeline_model, canonical_stage)
    skill_ref = stage_spec.get(
        "primary_skill_ref",
        f"docs/pipelines/{pipeline_id}/stages/{canonical_stage}.skill.yaml",
    )
    skill = load_stage_skill(repo_root, skill_ref)

    resolved_inputs = resolved_stage_inputs(skill, run_id, mode, canonical_stage)
    stage_kind = skill.get("stage_kind", "hybrid")
    closure_level = skill.get("closure_level", "medium")

    expected_outputs = skill.get("expected_outputs", {}) or {}
    mode_outputs = expected_outputs.get(mode, {}) if isinstance(expected_outputs, dict) else {}
    primary_output = (
        mode_outputs.get("report_path_pattern")
        or default_primary_output(run_id, canonical_stage)
    )

    task_view = {
        "status": "terminal_closed" if terminal_closed else "executable",
        "raw_stage_id": raw_stage_id,
        "stage_id": canonical_stage,
        "skill_ref": skill_ref,
        "stage_kind": stage_kind,
        "closure_level": closure_level,
        "resolved_inputs": resolved_inputs,
        "execution_paths": {
            "work_dir": default_work_dir(run_id, canonical_stage),
            "primary_output": substitute_run_id(primary_output, run_id),
            "reports_dir": f"runs/{run_id}/reports/",
        },
        "required_scripts_status": derive_required_scripts_status(
            canonical_stage,
            mode,
            scope_extract_status,
            neighbor_extract_status,
        ),
        "forbidden_actions": skill.get("forbidden_actions", []),
        "completion_evidence": skill.get("completion_evidence", {}).get("required", []),
        "allowed_transitions": skill.get(
            "allowed_transitions",
            stage_spec.get("transitions", {}),
        ),
        "compact_execution_prompt": derive_compact_execution_prompt(
            pipeline_id,
            run_id,
            canonical_stage,
            mode,
            skill_ref,
            resolved_inputs,
        ),
    }

    if terminal_closed:
        task_view["terminal_note"] = (
            "Run closed on a terminal stage. This task view is informative only "
            "and should not be treated as a next executable action."
        )

    return task_view


def build_run_context(
    repo_root: Path,
    run_id: str,
    pipeline_id: str,
    run_manifest: Dict[str, Any],
    scope_manifest: Dict[str, Any],
    impact_bundle: Dict[str, Any],
    integration_gate: Dict[str, Any],
    scope_extract: Optional[Dict[str, Any]],
    neighbor_extract: Optional[Dict[str, Any]],
    inputs_dir: Path,
) -> Dict[str, Any]:
    rm = run_manifest.get("run_manifest", {})
    sm = scope_manifest.get("scope_manifest", {})
    ib = impact_bundle.get("impact_bundle", {})
    ig = integration_gate.get("integration_gate", {})

    exec_state = rm.get("execution_state", {})
    current_stage = exec_state.get("current_stage") or rm.get("current_stage")
    last_stage_status = exec_state.get("last_stage_status", "unknown")
    next_stage = exec_state.get("next_stage", current_stage)
    completed_stages: List[str] = exec_state.get("completed_stages", []) or []
    raw_next_executable_stage, canonical_next_executable_stage, terminal_closed = derive_next_executable_stage(
        exec_state,
        current_stage,
        rm.get("status", "active"),
    )

    scope_ids: List[str] = sm.get("writable_perimeter", {}).get("ids", [])
    neighbor_ids: List[str] = ib.get("mandatory_reads", {}).get("ids", [])

    gate_checks = ig.get("gate_checks", []) or []
    gate_cleared = [c for c in gate_checks if c.get("cleared")]
    gate_summary = {
        "status": ig.get("status", "unknown"),
        "total_checks": len(gate_checks),
        "cleared_checks": len(gate_cleared),
        "promotion_blocked": ig.get("promotion_blocked_until_cleared", True),
    }

    scope_extract_status: Dict[str, Any] = {"present": False}
    neighbor_extract_status: Dict[str, Any] = {"present": False}

    if scope_extract is not None:
        se = scope_extract.get("scope_extract", {})
        scope_extract_status = {
            "present": True,
            "found_ids_count": len(se.get("found_ids", [])),
            "missing_ids_count": len(se.get("missing_ids", [])),
            "missing_ids": se.get("missing_ids", []),
            "ref": f"runs/{run_id}/inputs/scope_extract.yaml",
        }

    if neighbor_extract is not None:
        ne = neighbor_extract.get("neighbor_extract", {})
        neighbor_extract_status = {
            "present": True,
            "found_ids_count": len(ne.get("found_ids", [])),
            "missing_ids_count": len(ne.get("missing_ids", [])),
            "missing_ids": ne.get("missing_ids", []),
            "ref": f"runs/{run_id}/inputs/neighbor_extract.yaml",
        }

    fingerprints: Dict[str, str] = {}
    for fname in [
        "run_manifest.yaml",
        "scope_manifest.yaml",
        "impact_bundle.yaml",
        "integration_gate.yaml",
        "scope_extract.yaml",
        "neighbor_extract.yaml",
    ]:
        fpath = inputs_dir.parent / fname if fname == "run_manifest.yaml" else inputs_dir / fname
        if fpath.exists():
            fingerprints[fname] = sha256_file(fpath)

    mode = rm.get("mode", "bounded_local_run")
    task_view = build_task_view(
        repo_root=repo_root,
        pipeline_id=pipeline_id,
        run_id=run_id,
        mode=mode,
        raw_stage_id=raw_next_executable_stage,
        canonical_stage=canonical_next_executable_stage,
        terminal_closed=terminal_closed,
        scope_extract_status=scope_extract_status,
        neighbor_extract_status=neighbor_extract_status,
    )
    
    return {
        "run_context": {
            "schema_version": 0.2,
            "generated_by": "build_run_context_runtime_view_candidate_v2.py",
            "note": (
                "Fichier synthétique — lire EN PREMIER. Remplace la lecture séquentielle de "
                "run_manifest + scope_manifest + impact_bundle + integration_gate et expose "
                "une task view dérivée pour le stage exécutable. Sources canoniques inchangées."
            ),
            "run_id": run_id,
            "pipeline_id": pipeline_id,
            "mode": mode,
            "status": rm.get("status", "active"),
            "scope_key": rm.get("scope_key"),
            "current_stage": current_stage,
            "current_stage_canonical": canonical_stage_id(current_stage),
            "last_stage_status": last_stage_status,
            "next_stage": next_stage,
            "next_stage_canonical": canonical_stage_id(next_stage) if next_stage else "",
            "next_executable_stage": raw_next_executable_stage,
            "next_executable_stage_canonical": canonical_next_executable_stage,
            "terminal_closed": terminal_closed,
            "completed_stages": completed_stages,
            "completed_stages_canonical": [canonical_stage_id(s) for s in completed_stages],
            "scope_ids": sorted(scope_ids),
            "scope_ids_count": len(scope_ids),
            "neighbor_ids": sorted(neighbor_ids),
            "neighbor_ids_count": len(neighbor_ids),
            "scope_extract": scope_extract_status,
            "neighbor_extract": neighbor_extract_status,
            "integration_gate": gate_summary,
            "canonical_refs": {
                "run_manifest": f"docs/pipelines/{pipeline_id}/runs/{run_id}/run_manifest.yaml",
                "scope_manifest": f"docs/pipelines/{pipeline_id}/runs/{run_id}/inputs/scope_manifest.yaml",
                "impact_bundle": f"docs/pipelines/{pipeline_id}/runs/{run_id}/inputs/impact_bundle.yaml",
                "integration_gate": f"docs/pipelines/{pipeline_id}/runs/{run_id}/inputs/integration_gate.yaml",
            },
            "source_fingerprints": fingerprints,
            "task_view": task_view,
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build enriched run_context.yaml with derived runtime task view."
    )
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output-path",
        default="",
        help="Optional explicit output path. Defaults to runs/<run_id>/inputs/run_context.yaml",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    inputs_dir = run_root / "inputs"

    run_manifest = load_yaml(run_root / "run_manifest.yaml")
    scope_manifest = load_yaml(inputs_dir / "scope_manifest.yaml")
    impact_bundle = load_yaml(inputs_dir / "impact_bundle.yaml")
    integration_gate = load_yaml(inputs_dir / "integration_gate.yaml")
    scope_extract = load_yaml_optional(inputs_dir / "scope_extract.yaml")
    neighbor_extract = load_yaml_optional(inputs_dir / "neighbor_extract.yaml")

    context = build_run_context(
        repo_root=repo_root,
        run_id=args.run_id,
        pipeline_id=args.pipeline,
        run_manifest=run_manifest,
        scope_manifest=scope_manifest,
        impact_bundle=impact_bundle,
        integration_gate=integration_gate,
        scope_extract=scope_extract,
        neighbor_extract=neighbor_extract,
        inputs_dir=inputs_dir,
    )

    if args.output_path:
        out_path = Path(args.output_path)
        if not out_path.is_absolute():
            out_path = (repo_root / out_path).resolve()
        else:
            out_path = out_path.resolve()
    else:
        out_path = (inputs_dir / "run_context.yaml").resolve()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(dump_yaml(context), encoding="utf-8")

    rc = context["run_context"]
    result = {
        "build_run_context_runtime_view_candidate": {
            "status": "DONE",
            "run_id": args.run_id,
            "current_stage": rc["current_stage"],
            "next_executable_stage": rc["next_executable_stage"],
            "task_skill_ref": rc["task_view"]["skill_ref"],
            "scope_extract_present": rc["scope_extract"]["present"],
            "neighbor_extract_present": rc["neighbor_extract"]["present"],
            "path": display_path(out_path, repo_root),
        }
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
