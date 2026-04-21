#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/patcher/shared/reconcile_run.py")


NEW_PARSE_ARGS = '''def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile a constitution run.")
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=False)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the reconciliation plan materially.",
    )
    parser.add_argument(
        "--output",
        choices=("human", "json"),
        default="human",
        help="Select output format. In dashboard modes, default is human.",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Render a dashboard view from runs/index.yaml.",
    )
    parser.add_argument(
        "--dashboard-probe",
        action="store_true",
        help="Render a dashboard enriched with compact reconciliation probes for active runs.",
    )
    parser.add_argument(
        "--output-mode",
        choices=("full", "compact"),
        default="full",
        help="Select reconciliation payload verbosity.",
    )
    return parser.parse_args()
'''


NEW_PROBE_HELPERS = '''def probe_reconcile_run_state(
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
) -> Dict[str, Any]:
    pipeline_root = repo_root / "docs" / "pipelines" / pipeline_id
    run_root = pipeline_root / "runs" / run_id
    run_manifest_path = run_root / "run_manifest.yaml"

    if not run_root.exists():
        return {
            "probe_status": "error",
            "probe_error": "missing_run_root",
            "reconciliation_status": "",
            "trusted_prefix_end_stage": "",
            "restart_stage": "",
            "repairable_missing_artifacts": [],
            "invalidated_downstream_stage_set": [],
            "would_change_material_state": False,
            "next_best_action": "INSPECT",
        }

    if not run_manifest_path.exists():
        return {
            "probe_status": "error",
            "probe_error": "missing_run_manifest",
            "reconciliation_status": "",
            "trusted_prefix_end_stage": "",
            "restart_stage": "",
            "repairable_missing_artifacts": [],
            "invalidated_downstream_stage_set": [],
            "would_change_material_state": False,
            "next_best_action": "INSPECT",
        }

    manifest_data = load_yaml(run_manifest_path)
    run_manifest_root = manifest_data.get("run_manifest", {})
    mode = str(run_manifest_root.get("mode", ""))

    if mode != "bounded_local_run":
        return {
            "probe_status": "unsupported_mode",
            "probe_error": f"unsupported_mode:{mode}",
            "reconciliation_status": "",
            "trusted_prefix_end_stage": "",
            "restart_stage": "",
            "repairable_missing_artifacts": [],
            "invalidated_downstream_stage_set": [],
            "would_change_material_state": False,
            "next_best_action": "INSPECT",
        }

    repairable_missing_artifacts = [
        str(path)
        for path in (DERIVABLE_INPUTS + DERIVABLE_EXTRACTS + DERIVABLE_CONTEXT)
        if not (run_root / path).exists()
    ]

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
                pipeline_id=pipeline_id,
                run_id=run_id,
                stage_id=stage_id,
                mode=mode,
            )
        return stage_contract_cache[stage_id]

    trusted_prefix: List[str] = []
    stage_missing_map: Dict[str, List[str]] = {}
    first_non_trusted_stage: Optional[str] = None
    restart_stage: Optional[str] = None

    for stage in claimed_prefix:
        stage_contract = get_stage_contract(stage)
        ok, missing = stage_evidence_status(run_root, stage_contract["evidence_patterns"])
        if ok:
            trusted_prefix.append(stage)
        else:
            first_non_trusted_stage = stage
            stage_missing_map[stage] = missing
            restart_stage = stage_contract["missing_evidence_restart_stage"]
            break

    if first_non_trusted_stage is None:
        if current_stage in STAGE_ORDER and last_stage_status == "blocked":
            current_contract = get_stage_contract(current_stage)
            restart_stage = current_contract["blocked_restart_stage"]
        elif current_stage in STAGE_ORDER and last_stage_status == "failed":
            current_contract = get_stage_contract(current_stage)
            restart_stage = current_contract["fail_restart_stage"]
        elif current_stage in STAGE_ORDER and last_stage_status == "in_progress":
            restart_stage = current_stage
        elif next_stage in STAGE_ORDER:
            restart_stage = next_stage
        elif trusted_prefix:
            restart_stage = next_stage_after(trusted_prefix[-1])
        else:
            restart_stage = "STAGE_01_CHALLENGE"

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

    would_change_material_state = bool(
        repairable_missing_artifacts or invalidated_stages
    )

    return {
        "probe_status": "ok",
        "reconciliation_status": reconciliation_status,
        "trusted_prefix_end_stage": trusted_prefix[-1] if trusted_prefix else "",
        "restart_stage": restart_stage or "",
        "missing_evidence_by_stage": stage_missing_map,
        "repairable_missing_artifacts": repairable_missing_artifacts,
        "invalidated_downstream_stage_set": invalidated_stages,
        "would_change_material_state": would_change_material_state,
        "next_best_action": "CONTINUE_ACTIVE_RUN" if restart_stage else "INSPECT",
    }


def attach_dashboard_probes(
    repo_root: Path,
    pipeline_id: str,
    rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []

    for row in rows:
        row_copy = dict(row)
        if row_copy.get("bucket") == "active":
            row_copy["probe"] = probe_reconcile_run_state(
                repo_root=repo_root,
                pipeline_id=pipeline_id,
                run_id=str(row_copy.get("run_id", "")),
            )
        else:
            row_copy["probe"] = None
        enriched.append(row_copy)

    return enriched
'''


NEW_RENDER_DASHBOARD_HUMAN = '''def render_dashboard_human(
    index_data: Dict[str, Any],
    rows: List[Dict[str, Any]],
    pattern: str,
) -> str:
    runs_index = index_data.get("runs_index", {})
    active_runs = runs_index.get("active_runs", [])
    closed_runs = runs_index.get("closed_runs", [])

    total_runs = (len(active_runs) if isinstance(active_runs, list) else 0) + (
        len(closed_runs) if isinstance(closed_runs, list) else 0
    )
    active_count = len(active_runs) if isinstance(active_runs, list) else 0
    closed_count = len(closed_runs) if isinstance(closed_runs, list) else 0
    include_probe = any(isinstance(row.get("probe"), dict) for row in rows)

    def s(value: Any) -> str:
        return "" if value is None else str(value)

    def probe_label(row: Dict[str, Any]) -> str:
        probe = row.get("probe")
        if not isinstance(probe, dict):
            return ""
        probe_status = s(probe.get("probe_status", ""))
        if probe_status and probe_status != "ok":
            return probe_status
        reconciliation_status = s(probe.get("reconciliation_status", ""))
        if reconciliation_status == "run_reconciled_without_truncation":
            return "ok"
        if reconciliation_status == "run_truncated_to_restart_stage":
            return "truncate"
        return reconciliation_status

    def probe_trusted_end(row: Dict[str, Any]) -> str:
        probe = row.get("probe")
        if not isinstance(probe, dict):
            return ""
        return s(probe.get("trusted_prefix_end_stage", ""))

    def probe_restart(row: Dict[str, Any]) -> str:
        probe = row.get("probe")
        if not isinstance(probe, dict):
            return ""
        return s(probe.get("restart_stage", ""))

    def probe_change(row: Dict[str, Any]) -> str:
        probe = row.get("probe")
        if not isinstance(probe, dict):
            return ""
        return "yes" if bool(probe.get("would_change_material_state", False)) else "no"

    columns = [
        ("run_id", "RUN_ID"),
        ("scope_key", "SCOPE_KEY"),
        ("run_status", "STATUS"),
        ("current_stage", "STAGE"),
        ("mode", "MODE"),
    ]

    if include_probe:
        columns.extend(
            [
                ("probe_label", "PROBE"),
                ("trusted_end", "TRUSTED_END"),
                ("restart", "RESTART"),
                ("change", "CHANGE"),
            ]
        )

    widths: Dict[str, int] = {}
    for key, header in columns:
        widths[key] = len(header)

    for row in rows:
        widths["run_id"] = max(widths["run_id"], len(s(row.get("run_id", ""))))
        widths["scope_key"] = max(widths["scope_key"], len(s(row.get("scope_key", ""))))
        widths["run_status"] = max(widths["run_status"], len(s(row.get("run_status", ""))))
        widths["current_stage"] = max(widths["current_stage"], len(s(row.get("current_stage", ""))))
        widths["mode"] = max(widths["mode"], len(s(row.get("mode", ""))))
        if include_probe:
            widths["probe_label"] = max(widths["probe_label"], len(probe_label(row)))
            widths["trusted_end"] = max(widths["trusted_end"], len(probe_trusted_end(row)))
            widths["restart"] = max(widths["restart"], len(probe_restart(row)))
            widths["change"] = max(widths["change"], len(probe_change(row)))

    def format_row(values: Dict[str, str]) -> str:
        parts = []
        for key, _header in columns:
            parts.append(f"{values.get(key, ''):<{widths[key]}}")
        return " | ".join(parts)

    lines: List[str] = []
    if pattern and pattern != "*":
        lines.append(f"FILTER {pattern}")
    lines.append(
        f"PIPELINE {runs_index.get('pipeline_id', '')}  |  LAST_UPDATED {runs_index.get('last_updated', '')}"
    )
    lines.append(
        f"TOTAL {total_runs}  |  ACTIVE {active_count}  |  CLOSED {closed_count}  |  MATCHED {len(rows)}"
    )
    lines.append("")

    header_values = {key: header for key, header in columns}
    lines.append(format_row(header_values))
    lines.append("-+-".join("-" * widths[key] for key, _header in columns))

    for row in rows:
        row_values = {
            "run_id": s(row.get("run_id", "")),
            "scope_key": s(row.get("scope_key", "")),
            "run_status": s(row.get("run_status", "")),
            "current_stage": s(row.get("current_stage", "")),
            "mode": s(row.get("mode", "")),
        }
        if include_probe:
            row_values["probe_label"] = probe_label(row)
            row_values["trusted_end"] = probe_trusted_end(row)
            row_values["restart"] = probe_restart(row)
            row_values["change"] = probe_change(row)

        lines.append(format_row(row_values))

    if not rows:
        lines.append("(no run matched the current filter)")

    return "\\n".join(lines) + "\\n"
'''


NEW_MAIN = '''def main() -> int:
    args = parse_args()
    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline for now: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline

    if args.dashboard or args.dashboard_probe:
        runs_index_path = pipeline_root / "runs" / "index.yaml"
        if not runs_index_path.exists():
            raise SystemExit(f"runs/index.yaml missing: {runs_index_path}")

        index_data = load_yaml(runs_index_path)
        filter_pattern = args.run_id or "*"
        rows = build_dashboard_rows(index_data, filter_pattern)

        if args.dashboard_probe:
            rows = attach_dashboard_probes(repo_root, args.pipeline, rows)

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
'''


def detect_newline(text: str) -> str:
    if "\\r\\n" in text:
        return "\\r\\n"
    if "\\r" in text:
        return "\\r"
    return "\\n"


def normalize_newlines(text: str) -> str:
    return text.replace("\\r\\n", "\\n").replace("\\r", "\\n")


def restore_newlines(text: str, newline: str) -> str:
    return text.replace("\\n", newline)


def replace_top_level_function(source: str, func_name: str, new_block: str) -> str:
    lines = source.splitlines(keepends=True)

    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"def {func_name}("):
            start = i
            break
    if start is None:
        raise RuntimeError(f"Function not found: {func_name}")

    end = None
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.startswith("def ") or line.startswith('if __name__ == "__main__":'):
            end = i
            break
    if end is None:
        end = len(lines)

    replacement = new_block.strip("\\n").splitlines(keepends=True)
    replacement = [line if line.endswith("\\n") else line + "\\n" for line in replacement]
    replacement.append("\\n")

    return "".join(lines[:start] + replacement + lines[end:])


def insert_before_marker(source: str, marker: str, block: str) -> str:
    if block.strip() in source:
        return source
    if marker not in source:
        raise RuntimeError(f"Marker not found: {marker}")
    return source.replace(marker, block.strip("\\n") + "\\n\\n" + marker, 1)


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    raw = TARGET.read_text(encoding="utf-8")
    newline = detect_newline(raw)
    text = normalize_newlines(raw)

    text = replace_top_level_function(text, "parse_args", NEW_PARSE_ARGS)
    text = insert_before_marker(
        text,
        "def build_compact_reconciliation_payload(",
        NEW_PROBE_HELPERS,
    )
    text = replace_top_level_function(text, "render_dashboard_human", NEW_RENDER_DASHBOARD_HUMAN)
    text = replace_top_level_function(text, "main", NEW_MAIN)

    TARGET.write_text(restore_newlines(text, newline), encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()