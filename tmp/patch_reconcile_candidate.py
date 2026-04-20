#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/patcher/shared/reconcile_run.py")


NEW_PARSE_ARGS = '''
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile a constitution run.")
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the reconciliation plan materially.",
    )
    parser.add_argument(
        "--output-mode",
        choices=("full", "compact"),
        default="full",
        help="Select reconciliation payload verbosity.",
    )
    return parser.parse_args()
'''


NEW_COMPACT_HELPER = '''
def build_compact_reconciliation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
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
'''


NEW_RESULT_BLOCK = '''
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
'''


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

    replacement = new_block.strip("\n").splitlines(keepends=True)
    replacement = [line if line.endswith("\n") else line + "\n" for line in replacement]
    replacement.append("\n")

    new_lines = lines[:start] + replacement + lines[end:]
    return "".join(new_lines)


def insert_helper_before_main(source: str, helper_block: str) -> str:
    marker = "def main() -> int:\n"
    idx = source.find(marker)
    if idx == -1:
        raise RuntimeError("main() marker not found")

    if helper_block.strip() in source:
        return source

    helper_text = helper_block.strip("\n") + "\n\n"
    return source[:idx] + helper_text + source[idx:]


def replace_result_block(source: str, new_block: str) -> str:
    lines = source.splitlines(keepends=True)

    start = None
    for i, line in enumerate(lines):
        if line == '    result = {\n':
            start = i
            break
    if start is None:
        raise RuntimeError("Result block start not found")

    end = None
    for i in range(start, len(lines)):
        if lines[i] == '    print(json.dumps(result, indent=2, ensure_ascii=False))\n':
            end = i + 1
            break
    if end is None:
        raise RuntimeError("Result block end not found")

    replacement = new_block.strip("\n").splitlines(keepends=True)
    replacement = [line if line.endswith("\n") else line + "\n" for line in replacement]
    replacement.append("\n")

    new_lines = lines[:start] + replacement + lines[end:]
    return "".join(new_lines)


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    text = replace_top_level_function(text, "parse_args", NEW_PARSE_ARGS)
    text = insert_helper_before_main(text, NEW_COMPACT_HELPER)
    text = replace_result_block(text, NEW_RESULT_BLOCK)

    TARGET.write_text(text, encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()