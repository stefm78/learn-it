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

OFFICIAL_COMMAND = Path("docs/patcher/shared/pipeline_launcher/cli.py")
COMPAT_COMMAND = Path("docs/patcher/shared/pipeline_launcher_with_signals.py")
TMP_WRAPPER = Path("tmp/pipeline_launcher.py")
ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, cwd=str(REPO_ROOT), check=False, text=True, capture_output=True, timeout=30)
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def build_report() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    paths = {
        "official_command": REPO_ROOT / OFFICIAL_COMMAND,
        "compat_command": REPO_ROOT / COMPAT_COMMAND,
        "tmp_wrapper": REPO_ROOT / TMP_WRAPPER,
        "engine": REPO_ROOT / ENGINE,
    }

    for name, path in paths.items():
        if not path.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "name": name, "path": str(path)})
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "name": name, "detail": str(exc)})

    tmp_text = (REPO_ROOT / TMP_WRAPPER).read_text(encoding="utf-8") if (REPO_ROOT / TMP_WRAPPER).exists() else ""
    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""

    if len(tmp_text.splitlines()) > 80:
        findings.append({"finding_id": "TMP_WRAPPER_TOO_LARGE", "severity": "blocking", "line_count": len(tmp_text.splitlines())})
    if "from docs.patcher.shared.pipeline_launcher.cli import main" not in tmp_text:
        findings.append({"finding_id": "TMP_WRAPPER_DOES_NOT_DELEGATE_TO_OFFICIAL_CLI", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW" in engine_text:
        findings.append({"finding_id": "ENGINE_SHOULD_NOT_CONTAIN_SIGNAL_REVIEW_LAYER", "severity": "blocking"})

    official_run_rc, official_run_stdout, official_run_stderr = run_command([sys.executable, str(OFFICIAL_COMMAND)])
    official_raw_rc, official_raw_stdout, official_raw_stderr = run_command([sys.executable, str(OFFICIAL_COMMAND), "--raw-signals-overlay"])
    engine_rc, engine_stdout, engine_stderr = run_command([sys.executable, str(ENGINE)])
    tmp_rc, tmp_stdout, tmp_stderr = run_command([sys.executable, str(TMP_WRAPPER)])
    compat_rc, compat_stdout, compat_stderr = run_command([sys.executable, str(COMPAT_COMMAND)])

    for name, rc, stderr in [
        ("official_run", official_run_rc, official_run_stderr),
        ("official_raw", official_raw_rc, official_raw_stderr),
        ("engine", engine_rc, engine_stderr),
        ("tmp", tmp_rc, tmp_stderr),
        ("compat", compat_rc, compat_stderr),
    ]:
        if rc != 0:
            findings.append({"finding_id": "COMMAND_FAILED", "severity": "blocking", "command": name, "returncode": rc, "stderr_excerpt": stderr[:500]})

    if "PIPELINE_SIGNALS_REVIEW:" not in official_run_stdout:
        findings.append({"finding_id": "OFFICIAL_COMMAND_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in official_raw_stdout:
        findings.append({"finding_id": "OFFICIAL_RAW_FLAG_MISSING_RAW_OVERLAY", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" in engine_stdout:
        findings.append({"finding_id": "ENGINE_SHOULD_NOT_APPEND_HUMAN_REVIEW", "severity": "blocking"})
    if "PIPELINE_LAUNCH_MENU:" not in engine_stdout:
        findings.append({"finding_id": "ENGINE_MISSING_LAUNCH_MENU", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_stdout:
        findings.append({"finding_id": "TMP_WRAPPER_MISSING_OFFICIAL_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in compat_stdout:
        findings.append({"finding_id": "COMPAT_WRAPPER_MISSING_OFFICIAL_REVIEW", "severity": "blocking"})

    return {
        "pipeline_launcher_engine_promotion_validation": {
            "schema_version": "0.2",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D_COMPAT",
            "purpose": "Validate the promoted pipeline launcher state after incremental engine module extraction.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "promoted_and_may_be_incrementally_modularized",
                "tmp_pipeline_launcher": "compatibility_wrapper",
                "compatibility_wrapper": "preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {"ref": str(path.relative_to(REPO_ROOT)).replace("\\", "/"), "sha256": sha256_file(path)}
                for path in paths.values()
                if path.exists()
            ],
            "source_control": {
                "tmp_wrapper_line_count": len(tmp_text.splitlines()),
                "engine_line_count": len(engine_text.splitlines()),
            },
            "blocking_findings": findings,
            "result_summary": {
                "internal_engine_created": (REPO_ROOT / ENGINE).exists(),
                "tmp_pipeline_launcher_is_compatibility_wrapper": len(tmp_text.splitlines()) <= 80 and "pipeline_launcher.cli import main" in tmp_text,
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_run_stdout,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_stdout,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_stdout and "PIPELINE_SIGNALS_REVIEW:" not in engine_stdout,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in official_raw_stdout,
                "tmp_pipeline_launcher_behavior_changed": True,
                "tmp_pipeline_launcher_new_role": "compatibility_wrapper",
                "recommended_next_phase": "PHASE_28D",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_engine_promotion_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    report_path = REPO_ROOT / args.report
    write_yaml(report_path, report)

    root = report["pipeline_launcher_engine_promotion_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Internal engine created: {summary['internal_engine_created']}")
    print(f"tmp is compatibility wrapper: {summary['tmp_pipeline_launcher_is_compatibility_wrapper']}")
    print(f"Official command outputs human review: {summary['official_command_outputs_human_review']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
