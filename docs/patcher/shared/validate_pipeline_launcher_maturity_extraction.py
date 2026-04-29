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
MATURITY = Path("docs/patcher/shared/pipeline_launcher/maturity.py")
OFFICIAL = Path("docs/patcher/shared/pipeline_launcher/cli.py")
TMP = Path("tmp/pipeline_launcher.py")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, cwd=str(REPO_ROOT), check=False, text=True, capture_output=True, timeout=30)
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def build_report() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []

    for path in [ENGINE, MATURITY, OFFICIAL, TMP]:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "path": str(path)})
            continue
        try:
            py_compile.compile(str(full), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "path": str(path), "detail": str(exc)})

    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""
    maturity_text = (REPO_ROOT / MATURITY).read_text(encoding="utf-8") if (REPO_ROOT / MATURITY).exists() else ""

    # After PHASE_28D10 engine cleanup, engine.py no longer needs to import
    # maturity.py directly. D1 must only ensure that maturity helpers/constants
    # were extracted out of engine.py and remain available through maturity.py.
    if "def maturity_pct" in engine_text or "def maturity_level_from_score" in engine_text:
        findings.append({"finding_id": "ENGINE_STILL_DEFINES_MATURITY_FUNCTIONS", "severity": "blocking"})
    if "MATURITY_AXES_COUNT = 6" in engine_text or "MATURITY_MAX_SCORE = 24" in engine_text:
        findings.append({"finding_id": "ENGINE_STILL_DEFINES_MATURITY_CONSTANTS", "severity": "blocking"})
    for snippet in ["MATURITY_AXES_COUNT = 6", "MATURITY_MAX_SCORE = 24", "def maturity_pct", "def maturity_level_from_score"]:
        if snippet not in maturity_text:
            findings.append({"finding_id": "MATURITY_MODULE_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

    official_rc, official_stdout, official_stderr = run_command([sys.executable, str(OFFICIAL)])
    engine_rc, engine_stdout, engine_stderr = run_command([sys.executable, str(ENGINE)])
    tmp_rc, tmp_stdout, tmp_stderr = run_command([sys.executable, str(TMP)])
    raw_rc, raw_stdout, raw_stderr = run_command([sys.executable, str(OFFICIAL), "--raw-signals-overlay"])

    for name, rc, stderr in [("official", official_rc, official_stderr), ("engine", engine_rc, engine_stderr), ("tmp", tmp_rc, tmp_stderr), ("raw", raw_rc, raw_stderr)]:
        if rc != 0:
            findings.append({"finding_id": "COMMAND_FAILED", "severity": "blocking", "command": name, "returncode": rc, "stderr_excerpt": stderr[:500]})

    if "maturity_summary:" not in engine_stdout:
        findings.append({"finding_id": "ENGINE_OUTPUT_MISSING_MATURITY_SUMMARY", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in official_stdout:
        findings.append({"finding_id": "OFFICIAL_OUTPUT_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_stdout:
        findings.append({"finding_id": "TMP_OUTPUT_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_stdout:
        findings.append({"finding_id": "RAW_OUTPUT_MISSING_OVERLAY", "severity": "blocking"})

    return {
        "pipeline_launcher_maturity_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D1",
            "purpose": "Extract maturity constants and helpers from the pipeline launcher engine into a dedicated module.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "maturity_helpers_extracted",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "artifacts": {"maturity_module": str(MATURITY).replace("\\", "/"), "engine": str(ENGINE).replace("\\", "/"), "official_command": str(OFFICIAL).replace("\\", "/"), "tmp_wrapper": str(TMP).replace("\\", "/")},
            "inputs": [{"ref": str(path).replace("\\", "/"), "sha256": sha256_file(REPO_ROOT / path)} for path in [ENGINE, MATURITY, OFFICIAL, TMP] if (REPO_ROOT / path).exists()],
            "blocking_findings": findings,
            "result_summary": {
                "maturity_module_created": (REPO_ROOT / MATURITY).exists(),
                "engine_imports_maturity_module": "from docs.patcher.shared.pipeline_launcher.maturity import" in engine_text,
                "engine_defines_maturity_functions": "def maturity_pct" in engine_text or "def maturity_level_from_score" in engine_text,
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_stdout,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_stdout and "PIPELINE_SIGNALS_REVIEW:" not in engine_stdout,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_stdout,
                "recommended_next_phase": "PHASE_28D2",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_maturity_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    report_path = REPO_ROOT / args.report
    write_yaml(report_path, report)

    root = report["pipeline_launcher_maturity_extraction_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Maturity module created: {summary['maturity_module_created']}")
    print(f"Engine imports maturity module: {summary['engine_imports_maturity_module']}")
    print(f"Engine defines maturity functions: {summary['engine_defines_maturity_functions']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
