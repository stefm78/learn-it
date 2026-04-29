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

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.overlay import build_pipeline_signals_overlay
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        args,
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
        timeout=30,
    )
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def build_report() -> dict[str, Any]:
    paths = {
        "tmp_launcher": REPO_ROOT / "tmp" / "pipeline_launcher.py",
        "wrapper": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher_with_signals.py",
        "overlay": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher" / "overlay.py",
        "pipeline_signals": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher" / "pipeline_signals.py",
    }

    findings: list[dict[str, Any]] = []

    for name, path in paths.items():
        if not path.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "name": name, "path": str(path)})
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            findings.append(
                {"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "name": name, "detail": str(exc)}
            )

    tmp_rc, tmp_stdout, tmp_stderr = run_command([sys.executable, str(paths["tmp_launcher"])])
    wrapper_rc, wrapper_stdout, wrapper_stderr = run_command([sys.executable, str(paths["wrapper"])])

    if tmp_rc != 0:
        findings.append({"finding_id": "TMP_LAUNCHER_RUNTIME_FAILED", "severity": "blocking", "returncode": tmp_rc})
    if wrapper_rc != 0:
        findings.append(
            {"finding_id": "SIGNALS_WRAPPER_RUNTIME_FAILED", "severity": "blocking", "returncode": wrapper_rc}
        )

    overlay = build_pipeline_signals_overlay(REPO_ROOT)
    root = overlay.get("pipeline_signals_overlay", {})
    summary = root.get("signal_summary", {})
    prompt_binding = root.get("open_new_run_prompt_binding_addition", {})
    action = root.get("action_menu_addition", {})
    next_best = root.get("next_best_actions_addition", {}).get("review_pipeline_signals", {})

    if root.get("recommended_default_hint") != "review_pipeline_signals":
        findings.append(
            {
                "finding_id": "UNEXPECTED_RECOMMENDED_DEFAULT_HINT",
                "severity": "blocking",
                "actual": root.get("recommended_default_hint"),
            }
        )

    if summary.get("has_attention_signals") is not True:
        findings.append({"finding_id": "MISSING_ATTENTION_SIGNAL", "severity": "blocking"})

    if action.get("key") != "review_pipeline_signals" or action.get("recommended") is not True:
        findings.append({"finding_id": "INVALID_REVIEW_ACTION_SLOT", "severity": "blocking"})

    if next_best.get("status") != "attention_review_available":
        findings.append(
            {
                "finding_id": "INVALID_REVIEW_NEXT_BEST_ACTION",
                "severity": "blocking",
                "actual": next_best.get("status"),
            }
        )

    if "attention_signal_must_be_acknowledged" not in prompt_binding.get("pipeline_signals_handling", ""):
        findings.append({"finding_id": "PROMPT_BINDING_MISSING_ATTENTION_ACK", "severity": "blocking"})

    if root.get("launcher_authorizes_run_from_signals") is not False:
        findings.append({"finding_id": "OVERLAY_MUST_NOT_AUTHORIZE_RUN_OPENING", "severity": "blocking"})

    runtime_required = [
        "PIPELINE_SIGNALS_OVERLAY:",
        "recommended_default_hint: review_pipeline_signals",
        "key: review_pipeline_signals",
        "attention_signal_must_be_acknowledged",
        "launcher_authorizes_run_from_signals: false",
    ]
    missing_runtime = [snippet for snippet in runtime_required if snippet not in wrapper_stdout]
    if missing_runtime:
        findings.append(
            {
                "finding_id": "WRAPPER_OUTPUT_MISSING_EXPECTED_SNIPPETS",
                "severity": "blocking",
                "missing": missing_runtime,
            }
        )

    return {
        "pipeline_launcher_with_signals_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_27B",
            "purpose": "Provide a non-invasive launcher wrapper that appends pipeline signal overlay to tmp/pipeline_launcher.py output.",
            "mutation_policy": {
                "tmp_pipeline_launcher": "not_modified",
                "wrapper": "added",
                "overlay_module": "added",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {
                    "ref": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                    "sha256": sha256_file(path),
                }
                for path in paths.values()
                if path.exists()
            ],
            "overlay": root,
            "tmp_launcher_runtime": {
                "status": "PASS" if tmp_rc == 0 else "FAIL",
                "stdout_excerpt": tmp_stdout[:1500],
                "stderr_excerpt": tmp_stderr[:800],
            },
            "wrapper_runtime": {
                "status": "PASS" if wrapper_rc == 0 else "FAIL",
                "stdout_excerpt": wrapper_stdout[:3000],
                "stderr_excerpt": wrapper_stderr[:800],
            },
            "blocking_findings": findings,
            "result_summary": {
                "has_attention_signals": summary.get("has_attention_signals"),
                "recommended_default_hint": root.get("recommended_default_hint"),
                "wrapper_appends_pipeline_signals_overlay": "PIPELINE_SIGNALS_OVERLAY:" in wrapper_stdout,
                "launcher_authorizes_run_from_signals": False,
                "tmp_pipeline_launcher_behavior_changed": False,
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_with_signals_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    report_path = REPO_ROOT / args.report
    write_yaml(report_path, report)

    root = report["pipeline_launcher_with_signals_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Recommended default hint: {summary['recommended_default_hint']}")
    print(f"Wrapper appends overlay: {summary['wrapper_appends_pipeline_signals_overlay']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
