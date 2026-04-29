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

from docs.patcher.shared.pipeline_launcher.entry_actions import (
    render_entry_action_prompt,
    resolve_entry_action_ref,
)
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/entry_actions.py")
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

    for path in [ENGINE, MODULE, OFFICIAL, TMP]:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "path": str(path)})
            continue
        try:
            py_compile.compile(str(full), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "path": str(path), "detail": str(exc)})

    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""
    module_text = (REPO_ROOT / MODULE).read_text(encoding="utf-8") if (REPO_ROOT / MODULE).exists() else ""

    # After PHASE_28D10 engine cleanup, engine.py no longer needs to import
    # entry_actions.py directly. D4 must only ensure that entry action helpers
    # were extracted out of engine.py and remain available through entry_actions.py.
    if "def render_entry_action_prompt" in engine_text:
        findings.append({"finding_id": "ENGINE_STILL_DEFINES_ENTRY_ACTION_RENDERER", "severity": "blocking"})
    if "def render_entry_action_prompt" not in module_text:
        findings.append({"finding_id": "MODULE_MISSING_ENTRY_ACTION_RENDERER", "severity": "blocking"})

    action_ref = resolve_entry_action_ref(REPO_ROOT, "constitution", "OPEN_NEW_RUN")
    if action_ref != "docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml":
        findings.append({"finding_id": "OPEN_NEW_RUN_REF_UNEXPECTED", "severity": "blocking", "actual": action_ref})

    prompt = render_entry_action_prompt(
        REPO_ROOT,
        branch="feat/core-modularization-bootstrap",
        pipeline_id="constitution",
        pipeline_path="docs/pipelines/constitution/pipeline.md",
        action_id="OPEN_NEW_RUN",
        bindings={
            "scope_key": "knowledge_and_design",
            "maturity_pct": "92%",
            "maturity_level": "L4_strong",
            "governance_backlog_signal": {"warning": "none"},
            "bounded_run_preflight_signal": {"warning": "none"},
        },
    )
    for snippet in [
        "OPEN_NEW_RUN",
        "OPEN_NEW_RUN.action.yaml",
        "target_scope_key=knowledge_and_design",
        "target_scope_maturity_pct=92%",
        "bounded_run_preflight_signal=none",
        "Arrête-toi après la décision d'entrée.",
    ]:
        if snippet not in prompt:
            findings.append({"finding_id": "PROMPT_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

    official_rc, official_out, official_err = run([sys.executable, str(OFFICIAL)])
    engine_rc, engine_out, engine_err = run([sys.executable, str(ENGINE)])
    tmp_rc, tmp_out, tmp_err = run([sys.executable, str(TMP)])
    raw_rc, raw_out, raw_err = run([sys.executable, str(OFFICIAL), "--raw-signals-overlay"])

    for name, rc, err in [
        ("official", official_rc, official_err),
        ("engine", engine_rc, engine_err),
        ("tmp", tmp_rc, tmp_err),
        ("raw", raw_rc, raw_err),
    ]:
        if rc != 0:
            findings.append({"finding_id": "COMMAND_FAILED", "severity": "blocking", "command": name, "returncode": rc, "stderr_excerpt": err[:500]})

    if "PIPELINE_SIGNALS_REVIEW:" not in official_out:
        findings.append({"finding_id": "OFFICIAL_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_LAUNCH_MENU:" not in engine_out or "PIPELINE_SIGNALS_REVIEW:" in engine_out:
        findings.append({"finding_id": "ENGINE_OUTPUT_INVALID", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_out:
        findings.append({"finding_id": "TMP_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_out:
        findings.append({"finding_id": "RAW_MISSING_SIGNALS_OVERLAY", "severity": "blocking"})
    if "entry_prompt:" not in engine_out:
        findings.append({"finding_id": "ENGINE_MISSING_ENTRY_PROMPT", "severity": "blocking"})

    return {
        "pipeline_launcher_entry_actions_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D4",
            "purpose": "Extract entry action contract helpers from engine.py into entry_actions.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "entry_action_helpers_extracted",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {"ref": str(path).replace("\\", "/"), "sha256": sha256(REPO_ROOT / path)}
                for path in [ENGINE, MODULE, OFFICIAL, TMP]
                if (REPO_ROOT / path).exists()
            ],
            "prompt_sample": prompt,
            "blocking_findings": findings,
            "result_summary": {
                "entry_actions_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_entry_actions_module": "from docs.patcher.shared.pipeline_launcher.entry_actions import" in engine_text,
                "engine_defines_entry_action_renderer": "def render_entry_action_prompt" in engine_text,
                "open_new_run_ref": action_ref,
                "open_new_run_prompt_contains_contract": "OPEN_NEW_RUN.action.yaml" in prompt,
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D5",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_entry_actions_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_entry_actions_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Entry actions module created: {summary['entry_actions_module_created']}")
    print(f"Engine imports entry actions module: {summary['engine_imports_entry_actions_module']}")
    print(f"Engine defines entry action renderer: {summary['engine_defines_entry_action_renderer']}")
    print(f"OPEN_NEW_RUN ref: {summary['open_new_run_ref']}")
    print(f"Prompt contains contract: {summary['open_new_run_prompt_contains_contract']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
