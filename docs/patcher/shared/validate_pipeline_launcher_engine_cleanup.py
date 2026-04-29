#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import py_compile
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
OFFICIAL = Path("docs/patcher/shared/pipeline_launcher/cli.py")
TMP = Path("tmp/pipeline_launcher.py")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, cwd=str(REPO_ROOT), check=False, text=True, capture_output=True, timeout=30)
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def build_report() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []

    for path in [ENGINE, OFFICIAL, TMP]:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "path": str(path)})
            continue
        try:
            py_compile.compile(str(full), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "path": str(path), "detail": str(exc)})

    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""

    obsolete_snippets = [
        "Still experimental: kept in tmp/ until hardened and promoted.",
        "MATURITY_AXES_COUNT",
        "MATURITY_GATED_LEVELS",
        "MATURITY_LEVELS",
        "MATURITY_MAX_SCORE",
        "MATURITY_MINIMUM_LEVEL",
        "maturity_level_from_score",
        "maturity_pct",
        "attach_governance_backlog_signal",
        "build_governance_backlog_scope_summary",
        "compact_governance_backlog_signal",
        "empty_governance_backlog_signal",
        "attach_bounded_run_preflight_signal",
        "build_bounded_run_preflight_summary",
        "compact_bounded_run_preflight_signal",
        "empty_bounded_run_preflight_signal",
        "load_entry_action_contract",
        "load_entry_actions_index",
        "render_entry_action_prompt",
        "resolve_entry_action_ref",
        "build_stage_prompt",
        "ensure_prompt_mentions_branch",
        "probe_run_context",
        "build_bootstrap_command",
        "detect_abnormal_state",
        "detect_consolidation_ready",
        "probe_integration_gate",
        "load_yaml",
        "CONSOLIDATION_PENDING_STAGES",
        "_IN_PROGRESS_STALE_THRESHOLD_S",
    ]

    for snippet in obsolete_snippets:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_STILL_CONTAINS_OBSOLETE_IMPORT_OR_TEXT", "severity": "blocking", "snippet": snippet})

    required_snippets = [
        "from docs.patcher.shared.pipeline_launcher.registry import discover_pipelines_from_registry",
        "from docs.patcher.shared.pipeline_launcher.pipeline_state import (",
        "discover_constitution",
        "discover_generic_pipeline",
        "from docs.patcher.shared.pipeline_launcher.launch_menu import (",
        "build_menu",
        "build_parallel_slots",
        "def main() -> int:",
    ]
    for snippet in required_snippets:
        if snippet not in engine_text:
            findings.append({"finding_id": "ENGINE_MISSING_REQUIRED_SNIPPET", "severity": "blocking", "snippet": snippet})

    official_rc, official_out, official_err = run([sys.executable, str(OFFICIAL)])
    engine_rc, engine_out, engine_err = run([sys.executable, str(ENGINE)])
    tmp_rc, tmp_out, tmp_err = run([sys.executable, str(TMP)])
    raw_rc, raw_out, raw_err = run([sys.executable, str(OFFICIAL), "--raw-signals-overlay"])
    parallel_rc, parallel_out, parallel_err = run([sys.executable, str(ENGINE), "--parallel-runs", "1"])

    for name, rc, err in [
        ("official", official_rc, official_err),
        ("engine", engine_rc, engine_err),
        ("tmp", tmp_rc, tmp_err),
        ("raw", raw_rc, raw_err),
        ("parallel", parallel_rc, parallel_err),
    ]:
        if rc != 0:
            findings.append({"finding_id": "COMMAND_FAILED", "severity": "blocking", "command": name, "returncode": rc, "stderr_excerpt": err[:500]})

    if "PIPELINE_REGISTRY_STATE:" not in engine_out:
        findings.append({"finding_id": "ENGINE_MISSING_REGISTRY_STATE", "severity": "blocking"})
    if "PIPELINE_LAUNCH_MENU:" not in engine_out or "PIPELINE_SIGNALS_REVIEW:" in engine_out:
        findings.append({"finding_id": "ENGINE_OUTPUT_INVALID", "severity": "blocking"})
    if "PIPELINE_PARALLEL_SLOTS:" not in parallel_out:
        findings.append({"finding_id": "ENGINE_PARALLEL_OUTPUT_INVALID", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in official_out:
        findings.append({"finding_id": "OFFICIAL_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_out:
        findings.append({"finding_id": "TMP_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_out:
        findings.append({"finding_id": "RAW_MISSING_SIGNALS_OVERLAY", "severity": "blocking"})

    return {
        "pipeline_launcher_engine_cleanup_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D10",
            "purpose": "Clean obsolete imports, constants, and promoted-out-of-tmp docstring from the reduced launcher engine.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "imports_and_docstring_cleaned",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {"ref": str(path).replace("\\", "/"), "sha256": sha256(REPO_ROOT / path)}
                for path in [ENGINE, OFFICIAL, TMP]
                if (REPO_ROOT / path).exists()
            ],
            "blocking_findings": findings,
            "result_summary": {
                "engine_docstring_promoted_runtime": "promoted pipeline launcher runtime" in engine_text,
                "obsolete_import_snippet_count": sum(1 for snippet in obsolete_snippets if snippet in engine_text),
                "engine_keeps_required_runtime_imports": all(snippet in engine_text for snippet in required_snippets),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "engine_parallel_slots_still_work": "PIPELINE_PARALLEL_SLOTS:" in parallel_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D11_OR_STOP",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_engine_cleanup_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_engine_cleanup_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Engine docstring promoted runtime: {summary['engine_docstring_promoted_runtime']}")
    print(f"Obsolete import snippet count: {summary['obsolete_import_snippet_count']}")
    print(f"Engine keeps required runtime imports: {summary['engine_keeps_required_runtime_imports']}")
    print(f"Engine parallel slots still work: {summary['engine_parallel_slots_still_work']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
