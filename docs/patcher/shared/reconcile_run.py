#!/usr/bin/env python3
"""
Contract-aware reconciliation candidate for constitution runs.

Intended use:
- save as tmp/reconcile_run_contract_upgrade_candidate.py
- compare with docs/patcher/shared/reconcile_run.py
- optionally replace the central script after review

Scope:
- pipeline: constitution
- mode: bounded_local_run only
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml
import fnmatch\n

STAGE_ORDER: List[str] = [
    "STAGE_01_CHALLENGE",
    "STAGE_02_ARBITRAGE",
    "STAGE_03_PATCH_SYNTHESIS",
    "STAGE_04_PATCH_VALIDATION",
    "STAGE_05_APPLY",
    "STAGE_06_CORE_VALIDATION",
    "STAGE_07_RELEASE_MATERIALIZATION",
    "STAGE_08_PROMOTE_CURRENT",
    "STAGE_09_CLOSEOUT_AND_ARCHIVE",
]

STAGE_ALIASES: Dict[str, str] = {
    "STAGE_05_PATCH_APPLICATION": "STAGE_05_APPLY",
    "STAGE_09_CLOSEOUT": "STAGE_09_CLOSEOUT_AND_ARCHIVE",
}

STAGE_EVIDENCE_FALLBACK: Dict[str, List[str]] = {
    "STAGE_01_CHALLENGE": [
        "work/01_challenge/challenge_report_*.md",
    ],
    "STAGE_02_ARBITRAGE": [
        "work/02_arbitrage/arbitrage.md",
    ],
    "STAGE_03_PATCH_SYNTHESIS": [
        "work/03_patch/patchset.yaml",
    ],
    "STAGE_04_PATCH_VALIDATION": [
        "work/04_patch_validation/patch_validation.yaml",
    ],
    "STAGE_05_APPLY": [
        "reports/patch_execution_report.yaml",
    ],
    "STAGE_06_CORE_VALIDATION": [
        "work/06_core_validation/core_validation.yaml",
    ],
    "STAGE_07_RELEASE_MATERIALIZATION": [
        "work/07_release/release_plan.yaml",
        "reports/release_materialization_report.yaml",
    ],
    "STAGE_08_PROMOTE_CURRENT": [
        "reports/promotion_report.yaml",
        "reports/current_manifest_validation.yaml",
        "reports/promotion_report_validation.yaml",
    ],
    "STAGE_09_CLOSEOUT_AND_ARCHIVE": [
        "reports/closeout_report.yaml",
        "outputs/final_run_summary.md",
    ],
}

DERIVABLE_INPUTS = [
    "inputs/scope_manifest.yaml",
    "inputs/impact_bundle.yaml",
    "inputs/integration_gate.yaml",
]

DERIVABLE_EXTRACTS = [
    "inputs/scope_extract.yaml",
    "inputs/neighbor_extract.yaml",
]

DERIVABLE_CONTEXT = [
    "inputs/run_context.yaml",
]

STAGE_ID_TOKEN_RE = re.compile(r"STAGE_[0-9]{2}(?:_[A-Z0-9]+)+")
PATH_KEY_SUFFIXES = ("_root", "_dir", "_path")


class ReconciliationError(Exception):
    pass


def canonical_stage_id(stage_id: str) -> str:
    return STAGE_ALIASES.get(stage_id, stage_id)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_yaml_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )



\ndef parse_args() -> argparse.Namespace:
\n    parser = argparse.ArgumentParser(description="Reconcile a constitution run.")
\n    parser.add_argument("--pipeline", required=True)
\n    parser.add_argument("--run-id", required=False)
\n    parser.add_argument("--repo-root", default=".")
\n    parser.add_argument(
\n        "--apply",
\n        action="store_true",
\n        help="Apply the reconciliation plan materially.",
\n    )
\n    parser.add_argument(
\n        "--output",
\n        choices=("human", "json"),
\n        default="human",
\n        help="Select output format. In this step, it affects dashboard mode.",
\n    )
\n    parser.add_argument(
\n        "--dashboard",
\n        action="store_true",
\n        help="Render a dashboard view from runs/index.yaml.",
\n    )
\n    parser.add_argument(
\n        "--dashboard-probe",
\n        action="store_true",
\n        help="Reserved for the next step: dashboard enriched with reconciliation probes.",
\n    )
\n    parser.add_argument(
\n        "--output-mode",
\n        choices=("full", "compact"),
\n        default="full",
\n        help="Select reconciliation payload verbosity.",
\n    )
\n    return parser.parse_args()
\n\ndef run_script(cmd: List[str], *, apply: bool, cwd: Path) -> Dict[str, Any]:
    if not apply:
        return {
            "planned": True,
            "applied": False,
            "command": " ".join(cmd),
            "returncode": None,
        }

    result = subprocess.run(cmd, cwd=str(cwd), capture_output=False, text=True)
    if result.returncode != 0:
        raise ReconciliationError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}"
        )
    return {
        "planned": True,
        "applied": True,
        "command": " ".join(cmd),
        "returncode": result.returncode,
    }


def stage_index(stage_id: str) -> int:
    return STAGE_ORDER.index(stage_id)


def next_stage_after(stage_id: str) -> Optional[str]:
    idx = stage_index(stage_id)
    if idx + 1 >= len(STAGE_ORDER):
        return None
    return STAGE_ORDER[idx + 1]


def matches_any_glob(base: Path, pattern: str) -> bool:
    return any(base.glob(pattern))


def stage_skill_path(repo_root: Path, pipeline_id: str, stage_id: str) -> Path:
    return (
        repo_root
        / "docs"
        / "pipelines"
        / pipeline_id
        / "stages"
        / f"{stage_id}.skill.yaml"
    )


def normalize_run_relative_pattern(pattern: str, pipeline_id: str, run_id: str) -> str:
    prefixes = [
        f"docs/pipelines/{pipeline_id}/runs/<run_id>/",
        f"docs/pipelines/{pipeline_id}/runs/{run_id}/",
    ]
    normalized = pattern.strip()
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :]
            break

    # Les placeholders skill comme <id> doivent être traités comme des globs,
    # pas comme des chemins littéraux.
    normalized = re.sub(r"<[^/<>]+>", "*", normalized)

    return normalized.strip()

def normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def split_token_fragments(value: str) -> List[str]:
    normalized = normalize_token(value)
    return [fragment for fragment in normalized.split("_") if fragment]


def extract_stage_ids_from_text(value: str) -> List[str]:
    stages: List[str] = []
    seen: Set[str] = set()
    for token in STAGE_ID_TOKEN_RE.findall(value or ""):
        stage_id = canonical_stage_id(token.rstrip("_"))
        if stage_id in STAGE_ORDER and stage_id not in seen:
            stages.append(stage_id)
            seen.add(stage_id)
    return stages


def derive_restart_stage_from_transition(
    *,
    stage_id: str,
    transition_block: Any,
    fallback_stage: str,
) -> Tuple[str, List[str], str]:
    if not isinstance(transition_block, dict):
        return fallback_stage, [], "default_fallback_stage"

    transition_values = [
        str(transition_block.get("next_stage", "")),
        str(transition_block.get("next_action", "")),
        str(transition_block.get("precondition", "")),
        str(transition_block.get("note", "")),
    ]
    transition_text = " ".join(part for part in transition_values if part).strip()
    normalized_text = normalize_token(transition_text)

    if "retry_same_stage" in normalized_text or "same_stage" in normalized_text:
        return stage_id, [stage_id], "transition_retry_same_stage"

    candidates = extract_stage_ids_from_text(transition_text)
    if len(candidates) == 1:
        return candidates[0], candidates, "transition_single_stage"
    if len(candidates) > 1:
        return fallback_stage, candidates, "transition_ambiguous_fallback_stage"

    return fallback_stage, [], "default_fallback_stage"


def execution_path_required_by_contract(path_key: str, required_tokens: List[str]) -> Optional[str]:
    normalized_key = normalize_token(path_key)

    def trim_suffixes(value: str) -> str:
        trimmed = value
        for suffix in PATH_KEY_SUFFIXES:
            if trimmed.endswith(suffix):
                trimmed = trimmed[: -len(suffix)]
                break
        return trimmed.strip("_")

    base_key = trim_suffixes(normalized_key)

    # Aliases explicites pour les cas réellement voulus par les skills actuels.
    explicit_aliases = {
        "sandbox_root": {
            "sandbox_or_output_tree_materialized",
            "sandbox_root_materialized",
            "sandbox_materialized",
        },
        "execution_report": {
            "patch_execution_report_materialized",
            "execution_report_materialized",
        },
    }

    allowed_tokens = {normalize_token(token) for token in explicit_aliases.get(normalized_key, set())}

    for required_token in required_tokens:
        normalized_required = normalize_token(required_token)

        # On ne dérive un execution_path comme preuve que pour un token de
        # matérialisation explicite, jamais pour un simple *_executed_for_real.
        if "materialized" not in normalized_required:
            continue

        # 1) Cas explicitement autorisés.
        if normalized_required in allowed_tokens:
            return required_token

        # 2) Fallback conservateur :
        #    on n'accepte que des correspondances quasi exactes sur le nom du
        #    chemin déclaré, après retrait du suffixe _root/_dir/_path.
        if base_key:
            if normalized_required == f"{base_key}_materialized":
                return required_token
            if normalized_required.startswith(f"{base_key}_") and normalized_required.endswith("_materialized"):
                return required_token
            if normalized_required.endswith(f"_{base_key}_materialized"):
                return required_token

    return None

def derive_stage_contract(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    stage_id: str,
    mode: str,
) -> Dict[str, Any]:
    skill_path = stage_skill_path(repo_root, pipeline_id, stage_id)
    skill_data = load_yaml_optional(skill_path)

    expected_outputs = skill_data.get("expected_outputs", {})
    if not isinstance(expected_outputs, dict):
        expected_outputs = {}

    mode_outputs = expected_outputs.get(mode, {})
    if not isinstance(mode_outputs, dict):
        mode_outputs = {}

    script_execution_contract = skill_data.get("script_execution_contract", {})
    if not isinstance(script_execution_contract, dict):
        script_execution_contract = {}

    required_before_pass_or_fail = script_execution_contract.get(
        "required_before_pass_or_fail", []
    )
    if not isinstance(required_before_pass_or_fail, list):
        required_before_pass_or_fail = []

    execution_paths = skill_data.get("execution_paths", {})
    if not isinstance(execution_paths, dict):
        execution_paths = {}

    mode_execution_paths = execution_paths.get(mode, {})
    if not isinstance(mode_execution_paths, dict):
        mode_execution_paths = {}

    evidence_items: List[Dict[str, Any]] = []
    derived_patterns: List[str] = []

    for key in ("report_path_pattern", "primary_output_path_pattern"):
        value = mode_outputs.get(key)
        if isinstance(value, str) and value.strip():
            normalized_pattern = normalize_run_relative_pattern(value, pipeline_id, run_id)
            if normalized_pattern:
                evidence_items.append(
                    {
                        "source": "expected_outputs",
                        "key": key,
                        "pattern": normalized_pattern,
                    }
                )
                derived_patterns.append(normalized_pattern)

    raw_artifacts = mode_outputs.get("required_raw_artifacts", [])
    if isinstance(raw_artifacts, list):
        for value in raw_artifacts:
            if isinstance(value, str) and value.strip():
                normalized_pattern = normalize_run_relative_pattern(value, pipeline_id, run_id)
                if normalized_pattern:
                    evidence_items.append(
                        {
                            "source": "expected_outputs",
                            "key": "required_raw_artifacts",
                            "pattern": normalized_pattern,
                        }
                    )
                    derived_patterns.append(normalized_pattern)

    for path_key, raw_path in mode_execution_paths.items():
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue

        matched_token = execution_path_required_by_contract(
            path_key, required_before_pass_or_fail
        )
        if not matched_token:
            continue

        normalized_pattern = normalize_run_relative_pattern(raw_path, pipeline_id, run_id)
        if not normalized_pattern:
            continue

        evidence_items.append(
            {
                "source": "execution_paths",
                "key": path_key,
                "pattern": normalized_pattern,
                "required_by_contract_token": matched_token,
            }
        )
        derived_patterns.append(normalized_pattern)

    normalized_patterns = sorted(set(derived_patterns))
    evidence_derivation_source = "skill_contract"

    if not normalized_patterns:
        normalized_patterns = STAGE_EVIDENCE_FALLBACK.get(stage_id, [])
        evidence_items = [
            {
                "source": "fallback",
                "key": "stage_evidence_fallback",
                "pattern": pattern,
            }
            for pattern in normalized_patterns
        ]
        evidence_derivation_source = "fallback"

    allowed_transitions = skill_data.get("allowed_transitions", {})
    if not isinstance(allowed_transitions, dict):
        allowed_transitions = {}

    blocked_transition = allowed_transitions.get("on_blocked", {})
    fail_transition = allowed_transitions.get("on_fail", {})

    blocked_restart_stage, blocked_candidates, blocked_policy_source = (
        derive_restart_stage_from_transition(
            stage_id=stage_id,
            transition_block=blocked_transition,
            fallback_stage=stage_id,
        )
    )
    fail_restart_stage, fail_candidates, fail_policy_source = (
        derive_restart_stage_from_transition(
            stage_id=stage_id,
            transition_block=fail_transition,
            fallback_stage=stage_id,
        )
    )

    if script_execution_contract.get("blocked_if_missing_evidence") is True:
        missing_evidence_restart_stage = blocked_restart_stage
        missing_evidence_candidates = blocked_candidates
        missing_evidence_policy_source = (
            f"blocked_if_missing_evidence::{blocked_policy_source}"
        )
    else:
        missing_evidence_restart_stage = stage_id
        missing_evidence_candidates = [stage_id]
        missing_evidence_policy_source = "default_same_stage_no_blocked_if_missing_evidence"

    return {
        "stage_id": stage_id,
        "skill_path": str(skill_path),
        "evidence_patterns": normalized_patterns,
        "evidence_items": evidence_items,
        "evidence_derivation_source": evidence_derivation_source,
        "blocked_if_missing_evidence": script_execution_contract.get(
            "blocked_if_missing_evidence", False
        )
        is True,
        "missing_evidence_restart_stage": missing_evidence_restart_stage,
        "missing_evidence_restart_stage_candidates": missing_evidence_candidates,
        "missing_evidence_policy_source": missing_evidence_policy_source,
        "blocked_restart_stage": blocked_restart_stage,
        "blocked_restart_stage_candidates": blocked_candidates,
        "blocked_policy_source": blocked_policy_source,
        "fail_restart_stage": fail_restart_stage,
        "fail_restart_stage_candidates": fail_candidates,
        "fail_policy_source": fail_policy_source,
    }


def stage_evidence_status(
    run_root: Path,
    evidence_patterns: List[str],
) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for pattern in evidence_patterns:
        if "*" in pattern or "?" in pattern or "[" in pattern:
            if not matches_any_glob(run_root, pattern):
                missing.append(pattern)
        else:
            if not (run_root / pattern).exists():
                missing.append(pattern)
    return len(missing) == 0, missing


def derive_claimed_done_stages(run_manifest_root: Dict[str, Any]) -> List[str]:
    exec_state = run_manifest_root.get("execution_state", {})
    completed = exec_state.get("completed_stages", [])
    if not isinstance(completed, list):
        completed = []

    normalized: List[str] = []
    seen: Set[str] = set()

    for stage in completed:
        if not isinstance(stage, str):
            continue
        c_stage = canonical_stage_id(stage)
        if c_stage in STAGE_ORDER and c_stage not in seen:
            normalized.append(c_stage)
            seen.add(c_stage)

    current_stage = canonical_stage_id(str(exec_state.get("current_stage", "")))
    last_stage_status = str(exec_state.get("last_stage_status", ""))

    if current_stage in STAGE_ORDER and last_stage_status == "done" and current_stage not in seen:
        normalized.append(current_stage)

    normalized.sort(key=stage_index)
    return normalized


def contiguous_claimed_prefix(claimed_done: List[str]) -> List[str]:
    prefix: List[str] = []
    claimed_set = set(claimed_done)
    for stage in STAGE_ORDER:
        if stage in claimed_set:
            prefix.append(stage)
        else:
            break
    return prefix


def repair_derivable_inputs(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    run_root: Path,
    apply: bool,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    repaired: List[str] = []
    commands: List[Dict[str, Any]] = []

    missing_inputs = [p for p in DERIVABLE_INPUTS if not (run_root / p).exists()]
    if missing_inputs:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "materialize_run_inputs.py"),
            "--pipeline",
            pipeline_id,
            "--run-id",
            run_id,
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_inputs)

    missing_extracts = [p for p in DERIVABLE_EXTRACTS if not (run_root / p).exists()]
    if missing_extracts:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "extract_scope_slice.py"),
            "--pipeline",
            pipeline_id,
            "--run-id",
            run_id,
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_extracts)

    missing_context = [p for p in DERIVABLE_CONTEXT if not (run_root / p).exists()]
    if missing_context:
        cmd = [
            sys.executable,
            str(repo_root / "docs" / "patcher" / "shared" / "build_run_context.py"),
            "--pipeline",
            pipeline_id,
            "--run-id",
            run_id,
            "--repo-root",
            str(repo_root),
        ]
        commands.append(run_script(cmd, apply=apply, cwd=repo_root))
        repaired.extend(missing_context)

    return repaired, commands


def delete_path(path: Path, *, apply: bool) -> bool:
    if not path.exists():
        return False
    if not apply:
        return True
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def invalidate_downstream_artifacts(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    mode: str,
    run_root: Path,
    invalidated_stages: List[str],
    apply: bool,
    stage_contract_cache: Dict[str, Dict[str, Any]],
) -> List[str]:
    removed: List[str] = []

    def get_stage_contract(stage_id: str) -> Dict[str, Any]:
        if stage_id not in stage_contract_cache:
            stage_contract_cache[stage_id] = derive_stage_contract(
                repo_root=repo_root,
                pipeline_id=pipeline_id,
                run_id=run_id,
                stage_id=stage_id,
                mode=mode,
            )
        return stage_contract_cache[stage_id]

    for stage in invalidated_stages:
        stage_contract = get_stage_contract(stage)
        evidence_patterns = stage_contract["evidence_patterns"]

        for pattern in evidence_patterns:
            if "*" in pattern or "?" in pattern or "[" in pattern:
                for match in run_root.glob(pattern):
                    if delete_path(match, apply=apply):
                        removed.append(str(match.relative_to(run_root)).replace("\\", "/"))
            else:
                path = run_root / pattern
                if delete_path(path, apply=apply):
                    removed.append(str(path.relative_to(run_root)).replace("\\", "/"))

        stage_record = run_root / "reports" / f"stage_completion_{stage}.yaml"
        if delete_path(stage_record, apply=apply):
            removed.append(str(stage_record.relative_to(run_root)).replace("\\", "/"))

    return sorted(set(removed))


def rewrite_manifest_for_reconciliation(
    manifest_data: Dict[str, Any],
    *,
    trusted_prefix: List[str],
    restart_stage: Optional[str],
) -> Dict[str, Any]:
    root = manifest_data.setdefault("run_manifest", {})
    exec_state = root.setdefault("execution_state", {})

    if trusted_prefix:
        current_stage = trusted_prefix[-1]
        last_stage_status = "done"
    else:
        current_stage = "RUN_BOOTSTRAP"
        last_stage_status = "done"

    if restart_stage is None and trusted_prefix and trusted_prefix[-1] == "STAGE_09_CLOSEOUT_AND_ARCHIVE":
        run_status = "closed"
        next_stage = ""
    else:
        run_status = "active"
        next_stage = restart_stage or ""

    root["status"] = run_status
    exec_state["current_stage"] = current_stage
    exec_state["last_stage_status"] = last_stage_status
    exec_state["next_stage"] = next_stage
    exec_state["completed_stages"] = trusted_prefix

    stage_history = exec_state.get("stage_history", [])
    if isinstance(stage_history, list):
        exec_state["stage_history"] = [
            item
            for item in stage_history
            if isinstance(item, dict)
            and canonical_stage_id(str(item.get("stage_id", ""))) in trusted_prefix
        ]

    return manifest_data


def rewrite_runs_index_for_reconciliation(
    index_data: Dict[str, Any],
    *,
    manifest_data: Dict[str, Any],
    run_id: str,
) -> Dict[str, Any]:
    root = index_data.setdefault("runs_index", {})
    active_runs = root.setdefault("active_runs", [])
    closed_runs = root.setdefault("closed_runs", [])

    if not isinstance(active_runs, list):
        active_runs = []
        root["active_runs"] = active_runs
    if not isinstance(closed_runs, list):
        closed_runs = []
        root["closed_runs"] = closed_runs

    run_manifest = manifest_data.get("run_manifest", {})
    exec_state = run_manifest.get("execution_state", {})

    scope_binding = run_manifest.get("scope_binding", {})
    scope_id = scope_binding.get("scope_id", "")
    scope_key = run_manifest.get("scope_key", "")
    run_status = run_manifest.get("status", "active")
    current_stage = exec_state.get("current_stage", "")
    next_stage = exec_state.get("next_stage", "")

    displayed_stage = next_stage if next_stage else current_stage

    updated_entry = {
        "run_id": run_id,
        "scope_id": scope_id,
        "scope_key": scope_key,
        "run_status": run_status,
        "current_stage": displayed_stage,
        "mode": run_manifest.get("mode", "bounded_local_run"),
        "run_manifest_ref": f"docs/pipelines/constitution/runs/{run_id}/run_manifest.yaml",
    }

    active_runs[:] = [entry for entry in active_runs if entry.get("run_id") != run_id]
    closed_runs[:] = [entry for entry in closed_runs if entry.get("run_id") != run_id]

    if run_status == "closed":
        closed_runs.append(updated_entry)
    else:
        active_runs.append(updated_entry)

    return index_data


def rebuild_run_context(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    apply: bool,
) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        str(repo_root / "docs" / "patcher" / "shared" / "build_run_context.py"),
        "--pipeline",
        pipeline_id,
        "--run-id",
        run_id,
        "--repo-root",
        str(repo_root),
    ]
    return run_script(cmd, apply=apply, cwd=repo_root)


def summarize_stage_contract(contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "evidence_patterns": contract.get("evidence_patterns", []),
        "evidence_items": contract.get("evidence_items", []),
        "evidence_derivation_source": contract.get("evidence_derivation_source", ""),
        "blocked_if_missing_evidence": contract.get("blocked_if_missing_evidence", False),
        "missing_evidence_restart_stage": contract.get(
            "missing_evidence_restart_stage", ""
        ),
        "missing_evidence_policy_source": contract.get(
            "missing_evidence_policy_source", ""
        ),
        "blocked_restart_stage": contract.get("blocked_restart_stage", ""),
        "blocked_policy_source": contract.get("blocked_policy_source", ""),
        "fail_restart_stage": contract.get("fail_restart_stage", ""),
        "fail_policy_source": contract.get("fail_policy_source", ""),
        "fail_restart_stage_candidates": contract.get(
            "fail_restart_stage_candidates", []
        ),
    }



\ndef build_dashboard_rows(index_data: Dict[str, Any], pattern: str) -> List[Dict[str, Any]]:
\n    runs_index = index_data.get("runs_index", {})
\n    active_runs = runs_index.get("active_runs", [])
\n    closed_runs = runs_index.get("closed_runs", [])
\n
\n    normalized_pattern = (pattern or "*").upper()
\n
\n    def matches(entry: Dict[str, Any]) -> bool:
\n        candidates = [
\n            str(entry.get("run_id", "")),
\n            str(entry.get("scope_key", "")),
\n            str(entry.get("scope_id", "")),
\n        ]
\n        return any(
\n            candidate and fnmatch.fnmatchcase(candidate.upper(), normalized_pattern)
\n            for candidate in candidates
\n        )
\n
\n    rows: List[Dict[str, Any]] = []
\n
\n    if isinstance(active_runs, list):
\n        for entry in active_runs:
\n            if not isinstance(entry, dict):
\n                continue
\n            if not matches(entry):
\n                continue
\n            rows.append(
\n                {
\n                    "bucket": "active",
\n                    "run_id": str(entry.get("run_id", "")),
\n                    "scope_key": str(entry.get("scope_key", "")),
\n                    "scope_id": str(entry.get("scope_id", "")),
\n                    "run_status": str(entry.get("run_status", "")),
\n                    "current_stage": str(entry.get("current_stage", "")),
\n                    "mode": str(entry.get("mode", "")),
\n                }
\n            )
\n
\n    if isinstance(closed_runs, list):
\n        for entry in closed_runs:
\n            if not isinstance(entry, dict):
\n                continue
\n            if not matches(entry):
\n                continue
\n            rows.append(
\n                {
\n                    "bucket": "closed",
\n                    "run_id": str(entry.get("run_id", "")),
\n                    "scope_key": str(entry.get("scope_key", "")),
\n                    "scope_id": str(entry.get("scope_id", "")),
\n                    "run_status": str(entry.get("run_status", "")),
\n                    "current_stage": str(entry.get("current_stage", "")),
\n                    "mode": str(entry.get("mode", "")),
\n                }
\n            )
\n
\n    rows.sort(key=lambda item: (0 if item["bucket"] == "active" else 1, item["run_id"]))
\n    return rows
\n
\n
\ndef build_dashboard_payload(
\n    index_data: Dict[str, Any],
\n    rows: List[Dict[str, Any]],
\n    pattern: str,
\n) -> Dict[str, Any]:
\n    runs_index = index_data.get("runs_index", {})
\n    active_runs = runs_index.get("active_runs", [])
\n    closed_runs = runs_index.get("closed_runs", [])
\n
\n    matched_active = sum(1 for row in rows if row.get("bucket") == "active")
\n    matched_closed = sum(1 for row in rows if row.get("bucket") == "closed")
\n
\n    payload = {
\n        "runs_dashboard": {
\n            "pipeline_id": str(runs_index.get("pipeline_id", "")),
\n            "last_updated": str(runs_index.get("last_updated", "")),
\n            "filter": pattern or "*",
\n            "counts": {
\n                "total_runs": (len(active_runs) if isinstance(active_runs, list) else 0)
\n                + (len(closed_runs) if isinstance(closed_runs, list) else 0),
\n                "active_runs": len(active_runs) if isinstance(active_runs, list) else 0,
\n                "closed_runs": len(closed_runs) if isinstance(closed_runs, list) else 0,
\n                "matched_runs": len(rows),
\n                "matched_active_runs": matched_active,
\n                "matched_closed_runs": matched_closed,
\n            },
\n            "items": rows,
\n        }
\n    }
\n    return payload
\n
\n
\ndef render_dashboard_human(
\n    index_data: Dict[str, Any],
\n    rows: List[Dict[str, Any]],
\n    pattern: str,
\n) -> str:
\n    runs_index = index_data.get("runs_index", {})
\n    active_runs = runs_index.get("active_runs", [])
\n    closed_runs = runs_index.get("closed_runs", [])
\n
\n    total_runs = (len(active_runs) if isinstance(active_runs, list) else 0) + (
\n        len(closed_runs) if isinstance(closed_runs, list) else 0
\n    )
\n    active_count = len(active_runs) if isinstance(active_runs, list) else 0
\n    closed_count = len(closed_runs) if isinstance(closed_runs, list) else 0
\n
\n    lines: List[str] = []
\n    if pattern and pattern != "*":
\n        lines.append(f"FILTER {pattern}")
\n    lines.append(
\n        f"PIPELINE {runs_index.get('pipeline_id', '')}  |  LAST_UPDATED {runs_index.get('last_updated', '')}"
\n    )
\n    lines.append(
\n        f"TOTAL {total_runs}  |  ACTIVE {active_count}  |  CLOSED {closed_count}  |  MATCHED {len(rows)}"
\n    )
\n    lines.append("")
\n    lines.append(
\n        f"{'RUN_ID':<52} {'SCOPE_KEY':<22} {'STATUS':<15} {'STAGE':<30} {'MODE'}"
\n    )
\n
\n    for row in rows:
\n        lines.append(
\n            f"{row.get('run_id', ''):<52} "
\n            f"{row.get('scope_key', ''):<22} "
\n            f"{row.get('run_status', ''):<15} "
\n            f"{row.get('current_stage', ''):<30} "
\n            f"{row.get('mode', '')}"
\n        )
\n
\n    if not rows:
\n        lines.append("(no run matched the current filter)")
\n
\n    return "\n".join(lines) + "\n"
\n\ndef build_compact_reconciliation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    repaired_artifacts = payload.get("repaired_artifacts", [])
    invalidated_downstream_stage_set = payload.get("invalidated_downstream_stage_set", [])

    would_change_material_state = bool(
        repaired_artifacts or invalidated_downstream_stage_set
    )

    compact_payload = {
        "status": payload.get("status", ""),
        "apply": payload.get("apply", False),
        "pipeline_id": payload.get("pipeline_id", ""),
        "run_id": payload.get("run_id", ""),
        "mode": payload.get("mode", ""),
        "reconciliation_status": payload.get("reconciliation_status", ""),
        "trusted_prefix_end_stage": payload.get("trusted_prefix_end_stage", ""),
        "restart_stage": payload.get("restart_stage", ""),
        "repaired_artifacts": repaired_artifacts,
        "invalidated_downstream_stage_set": invalidated_downstream_stage_set,
        "run_status_after_reconciliation": payload.get("run_status_after_reconciliation", ""),
        "current_stage_after_reconciliation": payload.get("current_stage_after_reconciliation", ""),
        "next_stage_after_reconciliation": payload.get("next_stage_after_reconciliation", ""),
        "next_best_action": payload.get("next_best_action", ""),
        "next_best_action_reason": payload.get("next_best_action_reason", ""),
        "would_change_material_state": would_change_material_state,
    }

    return {"reconcile_run": compact_payload}

def main() -> int:
    args = parse_args()
    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline for now: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline

    if args.dashboard or args.dashboard_probe:
        if args.dashboard_probe:
            raise SystemExit(
                "--dashboard-probe is reserved for the next step. Use --dashboard first."
            )

        runs_index_path = pipeline_root / "runs" / "index.yaml"
        if not runs_index_path.exists():
            raise SystemExit(f"runs/index.yaml missing: {runs_index_path}")

        index_data = load_yaml(runs_index_path)
        filter_pattern = args.run_id or "*"
        rows = build_dashboard_rows(index_data, filter_pattern)

        if args.output == "json":
            payload = build_dashboard_payload(index_data, rows, filter_pattern)
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(render_dashboard_human(index_data, rows, filter_pattern), end="")
        return 0

    if not args.run_id:
        raise SystemExit("--run-id is required outside dashboard mode")

    run_root = pipeline_root / "runs" / args.run_id
    run_manifest_path = run_root / "run_manifest.yaml"
    runs_index_path = pipeline_root / "runs" / "index.yaml"

    if not run_root.exists():
        raise SystemExit(f"Run root does not exist: {run_root}")
    if not run_manifest_path.exists():
        raise SystemExit(f"run_manifest.yaml missing: {run_manifest_path}")

    manifest_data = load_yaml(run_manifest_path)
    index_data = load_yaml(runs_index_path)
    run_manifest_root = manifest_data.get("run_manifest", {})
    mode = run_manifest_root.get("mode", "")

    if mode != "bounded_local_run":
        raise SystemExit(
            f"Unsupported mode for this initial version: {mode!r}. "
            "This implementation supports bounded_local_run only."
        )

    repaired_artifacts, repair_commands = repair_derivable_inputs(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        run_root=run_root,
        apply=args.apply,
    )

    manifest_data = load_yaml(run_manifest_path)
    run_manifest_root = manifest_data.get("run_manifest", {})
    exec_state = run_manifest_root.get("execution_state", {})

    claimed_done = derive_claimed_done_stages(run_manifest_root)
    claimed_prefix = contiguous_claimed_prefix(claimed_done)

    current_stage = canonical_stage_id(str(exec_state.get("current_stage", "")))
    last_stage_status = str(exec_state.get("last_stage_status", ""))
    next_stage = (
        canonical_stage_id(str(exec_state.get("next_stage", "")))
        if exec_state.get("next_stage")
        else ""
    )

    stage_contract_cache: Dict[str, Dict[str, Any]] = {}

    def get_stage_contract(stage_id: str) -> Dict[str, Any]:
        if stage_id not in stage_contract_cache:
            stage_contract_cache[stage_id] = derive_stage_contract(
                repo_root=repo_root,
                pipeline_id=args.pipeline,
                run_id=args.run_id,
                stage_id=stage_id,
                mode=mode,
            )
        return stage_contract_cache[stage_id]

    trusted_prefix: List[str] = []
    stage_missing_map: Dict[str, List[str]] = {}
    first_non_trusted_stage: Optional[str] = None
    restart_stage: Optional[str] = None
    restart_stage_reason = ""
    restart_stage_policy_source = ""

    for stage in claimed_prefix:
        stage_contract = get_stage_contract(stage)
        ok, missing = stage_evidence_status(run_root, stage_contract["evidence_patterns"])
        if ok:
            trusted_prefix.append(stage)
        else:
            first_non_trusted_stage = stage
            stage_missing_map[stage] = missing
            restart_stage = stage_contract["missing_evidence_restart_stage"]
            restart_stage_reason = f"missing_evidence_in_{stage}"
            restart_stage_policy_source = stage_contract["missing_evidence_policy_source"]
            break

    if first_non_trusted_stage is None:
        if current_stage in STAGE_ORDER and last_stage_status == "blocked":
            current_contract = get_stage_contract(current_stage)
            restart_stage = current_contract["blocked_restart_stage"]
            restart_stage_reason = f"current_stage_blocked_{current_stage}"
            restart_stage_policy_source = current_contract["blocked_policy_source"]
        elif current_stage in STAGE_ORDER and last_stage_status == "failed":
            current_contract = get_stage_contract(current_stage)
            restart_stage = current_contract["fail_restart_stage"]
            restart_stage_reason = f"current_stage_failed_{current_stage}"
            restart_stage_policy_source = current_contract["fail_policy_source"]
        elif current_stage in STAGE_ORDER and last_stage_status == "in_progress":
            restart_stage = current_stage
            restart_stage_reason = f"current_stage_in_progress_{current_stage}"
            restart_stage_policy_source = "current_stage_in_progress"
        elif next_stage in STAGE_ORDER:
            restart_stage = next_stage
            restart_stage_reason = f"manifest_next_stage_{next_stage}"
            restart_stage_policy_source = "manifest_next_stage"
        elif trusted_prefix:
            restart_stage = next_stage_after(trusted_prefix[-1])
            restart_stage_reason = (
                f"next_stage_after_trusted_prefix_{trusted_prefix[-1]}"
                if restart_stage
                else "trusted_prefix_complete"
            )
            restart_stage_policy_source = "trusted_prefix_successor"
        else:
            restart_stage = "STAGE_01_CHALLENGE"
            restart_stage_reason = "no_trusted_stage_default_entry"
            restart_stage_policy_source = "default_entry"

    if trusted_prefix and trusted_prefix[-1] == "STAGE_09_CLOSEOUT_AND_ARCHIVE" and restart_stage is None:
        invalidated_stages: List[str] = []
        reconciliation_status = "run_reconciled_without_truncation"
    else:
        invalidated_stages = []
        if restart_stage in STAGE_ORDER:
            restart_idx = stage_index(restart_stage)
            for stage in claimed_done:
                if stage_index(stage) >= restart_idx:
                    invalidated_stages.append(stage)
            if current_stage in STAGE_ORDER and stage_index(current_stage) >= restart_idx:
                invalidated_stages.append(current_stage)

        invalidated_stages = sorted(set(invalidated_stages), key=stage_index)
        reconciliation_status = (
            "run_truncated_to_restart_stage"
            if invalidated_stages
            else "run_reconciled_without_truncation"
        )

    removed_artifacts = invalidate_downstream_artifacts(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        mode=mode,
        run_root=run_root,
        invalidated_stages=invalidated_stages,
        apply=args.apply,
        stage_contract_cache=stage_contract_cache,
    )

    manifest_data = rewrite_manifest_for_reconciliation(
        manifest_data,
        trusted_prefix=trusted_prefix,
        restart_stage=restart_stage,
    )
    index_data = rewrite_runs_index_for_reconciliation(
        index_data,
        manifest_data=manifest_data,
        run_id=args.run_id,
    )

    if args.apply:
        dump_yaml(run_manifest_path, manifest_data)
        dump_yaml(runs_index_path, index_data)

    run_context_command = rebuild_run_context(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        apply=args.apply,
    )

    inspected_stages = list(claimed_done)
    if current_stage in STAGE_ORDER and current_stage not in inspected_stages:
        inspected_stages.append(current_stage)
    inspected_stages = sorted(inspected_stages, key=stage_index)

    stage_contract_summary = {
        stage: summarize_stage_contract(get_stage_contract(stage))
        for stage in inspected_stages
    }

    final_manifest = manifest_data.get("run_manifest", {})
    final_exec_state = final_manifest.get("execution_state", {})

    full_result = {
        "reconcile_run": {
            "status": "DONE",
            "apply": args.apply,
            "pipeline_id": args.pipeline,
            "run_id": args.run_id,
            "mode": mode,
            "reconciliation_status": reconciliation_status,
            "trusted_prefix_end_stage": trusted_prefix[-1] if trusted_prefix else "",
            "restart_stage": restart_stage or "",
            "restart_stage_reason": restart_stage_reason,
            "restart_stage_policy_source": restart_stage_policy_source,
            "claimed_done_stages": claimed_done,
            "trusted_prefix": trusted_prefix,
            "evidence_derivation_mode": (
                "skill_expected_outputs_plus_required_execution_paths_with_fallback"
            ),
            "missing_evidence_by_stage": stage_missing_map,
            "repaired_artifacts": repaired_artifacts,
            "repair_commands": repair_commands,
            "invalidated_downstream_stage_set": invalidated_stages,
            "removed_artifacts": removed_artifacts,
            "stage_contract_summary": stage_contract_summary,
            "run_status_after_reconciliation": final_manifest.get("status", ""),
            "current_stage_after_reconciliation": final_exec_state.get("current_stage", ""),
            "next_stage_after_reconciliation": final_exec_state.get("next_stage", ""),
            "run_context_rebuild": run_context_command,
            "next_best_action": "CONTINUE_ACTIVE_RUN" if restart_stage else "INSPECT",
            "next_best_action_reason": (
                f"Run repositioned on {restart_stage}."
                if restart_stage
                else "Run is fully reconciled and does not require stage restart."
            ),
        }
    }

    result = (
        build_compact_reconciliation_payload(full_result["reconcile_run"])
        if args.output_mode == "compact"
        else full_result
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())