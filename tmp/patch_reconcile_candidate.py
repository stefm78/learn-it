#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re


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


NEW_COMPACT_HELPERS = '''
def build_compact_reconciliation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    repaired_artifacts = payload.get("repaired_artifacts", [])
    invalidated_downstream_stage_set = payload.get("invalidated_downstream_stage_set", [])

    would_change_material_state = bool(repaired_artifacts or invalidated_downstream_stage_set)

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


def replace_function(source: str, func_name: str, new_block: str) -> str:
    pattern = rf"def {func_name}\\(.*?(?=^def |^if __name__ == |\\Z)"
    updated, count = re.subn(pattern, new_block.strip() + "\\n\\n", source, flags=re.S | re.M)
    if count != 1:
        raise RuntimeError(f"Unable to replace function {func_name}: count={count}")
    return updated


def insert_helper_before_main(source: str, helper_block: str) -> str:
    marker = "\\ndef main() -> int:\\n"
    if helper_block.strip() in source:
        return source
    if marker not in source:
        raise RuntimeError("main() marker not found")
    return source.replace(marker, "\\n\\n" + helper_block.strip() + "\\n\\n\\ndef main() -> int:\\n", 1)


def replace_result_print_block(source: str) -> str:
    old = '''
    result = {
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

    print(json.dumps(result, indent=2, ensure_ascii=False))
'''
    new = '''
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
    if old not in source:
        raise RuntimeError("Result print block not found")
    return source.replace(old, new, 1)


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")
    text = replace_function(text, "parse_args", NEW_PARSE_ARGS)
    text = insert_helper_before_main(text, NEW_COMPACT_HELPERS)
    text = replace_result_print_block(text)

    TARGET.write_text(text, encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()