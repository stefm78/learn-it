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

from docs.patcher.shared.pipeline_launcher.run_context import build_stage_prompt, probe_run_context
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/run_context.py")
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

    if "from docs.patcher.shared.pipeline_launcher.run_context import" not in engine_text:
        findings.append({"finding_id": "ENGINE_IMPORT_MISSING", "severity": "blocking"})
    for snippet in ["def probe_run_context", "def build_stage_prompt", "def ensure_prompt_mentions_branch"]:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_STILL_DEFINES_RUN_CONTEXT_HELPER", "severity": "blocking", "snippet": snippet})
        if snippet not in module_text:
            findings.append({"finding_id": "MODULE_MISSING_RUN_CONTEXT_HELPER", "severity": "blocking", "snippet": snippet})

    prompt = build_stage_prompt(
        branch="feat/core-modularization-bootstrap",
        pipeline_id="constitution",
        pipeline_path="docs/pipelines/constitution/pipeline.md",
        run_id="CONSTITUTION_RUN_TEST",
        scope_key="knowledge_and_design",
        current_stage="STAGE_01_CHALLENGE",
        ids_first={
            "ids_first_ready": True,
            "scope_extract_complete": True,
            "neighbor_extract_complete": True,
        },
    )
    required_prompt_snippets = [
        "STAGE_01_CHALLENGE",
        "CONSTITUTION_RUN_TEST",
        "run_context.yaml",
        "scope_extract.yaml",
        "neighbor_extract.yaml",
    ]
    for snippet in required_prompt_snippets:
        if snippet not in prompt:
            findings.append({"finding_id": "STAGE_PROMPT_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

    if "ids-first" not in prompt.lower():
        findings.append({"finding_id": "STAGE_PROMPT_MISSING_SNIPPET", "severity": "blocking", "snippet": "ids-first"})

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

    return {
        "pipeline_launcher_run_context_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D5",
            "purpose": "Extract run_context probing and stage prompt helpers from engine.py into run_context.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "run_context_helpers_extracted",
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
            "stage_prompt_sample": prompt,
            "blocking_findings": findings,
            "result_summary": {
                "run_context_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_run_context_module": "from docs.patcher.shared.pipeline_launcher.run_context import" in engine_text,
                "engine_defines_run_context_helpers": "def probe_run_context" in engine_text or "def build_stage_prompt" in engine_text,
                "stage_prompt_contains_ids_first": "ids-first" in prompt.lower(),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D6",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_run_context_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_run_context_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Run context module created: {summary['run_context_module_created']}")
    print(f"Engine imports run context module: {summary['engine_imports_run_context_module']}")
    print(f"Engine defines run context helpers: {summary['engine_defines_run_context_helpers']}")
    print(f"Stage prompt contains ids-first: {summary['stage_prompt_contains_ids_first']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
