#!/usr/bin/env python3
# Validate minimal pipeline signals contracts.

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ALLOWED_PROVIDER_STATUSES = {"implemented", "not_implemented", "not_applicable"}


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return {}
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
        newline="\n",
    )


def discover_pipelines(registry_path: Path) -> list[dict[str, str]]:
    if not registry_path.exists():
        raise SystemExit(f"Missing registry: {registry_path}")

    pipelines: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in registry_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            if current and current.get("path", "").startswith("docs/pipelines/"):
                pipelines.append(current)
            current = {"pipeline_id": stripped[4:].strip()}
            continue

        if current and stripped.startswith("- Path:"):
            start = stripped.find("`")
            end = stripped.rfind("`")
            if start >= 0 and end > start:
                current["path"] = stripped[start + 1:end]

        if current and stripped.startswith("- Canonical state:"):
            start = stripped.find("`")
            end = stripped.rfind("`")
            if start >= 0 and end > start:
                current["canonical_state"] = stripped[start + 1:end]

    if current and current.get("path", "").startswith("docs/pipelines/"):
        pipelines.append(current)

    return pipelines


def add_finding(findings: list[dict[str, Any]], pipeline_id: str, finding_id: str, detail: str) -> None:
    findings.append(
        {
            "pipeline_id": pipeline_id,
            "finding_id": finding_id,
            "severity": "blocking",
            "detail": detail,
        }
    )


def validate_pipeline(repo_root: Path, pipeline: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pipeline_id = pipeline["pipeline_id"]
    findings: list[dict[str, Any]] = []

    signals_path = repo_root / "docs" / "pipelines" / pipeline_id / "signals.yaml"
    pipeline_summary: dict[str, Any] = {
        "pipeline_id": pipeline_id,
        "signals_path": str(signals_path).replace("\\", "/"),
        "signals_file_present": signals_path.exists(),
        "provider_status": "missing",
        "signals_count": 0,
    }

    if not signals_path.exists():
        add_finding(findings, pipeline_id, "missing_signals_yaml", f"Missing {signals_path}")
        return pipeline_summary, findings

    doc = load_yaml(signals_path)
    root = doc.get("pipeline_signals")
    if not isinstance(root, dict):
        add_finding(findings, pipeline_id, "invalid_root", "Expected root key pipeline_signals mapping")
        return pipeline_summary, findings

    declared_id = root.get("pipeline_id")
    provider_status = root.get("signals_provider")
    signals = root.get("signals", [])

    pipeline_summary["provider_status"] = provider_status
    pipeline_summary["signals_count"] = len(signals) if isinstance(signals, list) else 0
    pipeline_summary["sha256"] = sha256_file(signals_path)

    if declared_id != pipeline_id:
        add_finding(findings, pipeline_id, "pipeline_id_mismatch", f"Expected {pipeline_id}, got {declared_id!r}")

    if provider_status not in ALLOWED_PROVIDER_STATUSES:
        add_finding(
            findings,
            pipeline_id,
            "invalid_provider_status",
            f"signals_provider must be one of {sorted(ALLOWED_PROVIDER_STATUSES)}, got {provider_status!r}",
        )

    if not isinstance(signals, list):
        add_finding(findings, pipeline_id, "invalid_signals_list", "signals must be a list")
        return pipeline_summary, findings

    if provider_status == "implemented" and not signals:
        add_finding(findings, pipeline_id, "implemented_without_signals", "implemented provider must expose at least one signal")

    if provider_status in {"not_implemented", "not_applicable"} and signals:
        add_finding(findings, pipeline_id, "disabled_provider_has_signals", "not_implemented/not_applicable provider must use signals: []")

    allowed_prefix = f"docs/pipelines/{pipeline_id}/"
    for idx, signal in enumerate(signals):
        if not isinstance(signal, dict):
            add_finding(findings, pipeline_id, "invalid_signal_entry", f"Signal at index {idx} must be a mapping")
            continue

        signal_id = signal.get("id")
        signal_status = signal.get("status")
        source = signal.get("source")

        if not signal_id:
            add_finding(findings, pipeline_id, "signal_missing_id", f"Signal at index {idx} is missing id")
        if not signal_status:
            add_finding(findings, pipeline_id, "signal_missing_status", f"Signal {signal_id or idx} is missing status")
        if source:
            source_str = str(source)
            if not source_str.startswith(allowed_prefix):
                add_finding(
                    findings,
                    pipeline_id,
                    "signal_source_outside_pipeline",
                    f"Signal {signal_id or idx} source must start with {allowed_prefix}, got {source_str}",
                )
            elif not (repo_root / source_str).exists():
                add_finding(
                    findings,
                    pipeline_id,
                    "signal_source_missing",
                    f"Signal {signal_id or idx} source does not exist: {source_str}",
                )

    return pipeline_summary, findings


def build_report(repo_root: Path, registry_path: Path) -> dict[str, Any]:
    pipelines = discover_pipelines(registry_path)
    all_findings: list[dict[str, Any]] = []
    checked: list[dict[str, Any]] = []

    for pipeline in pipelines:
        summary, findings = validate_pipeline(repo_root, pipeline)
        checked.append(summary)
        all_findings.extend(findings)

    provider_status_by_pipeline = {
        item["pipeline_id"]: item.get("provider_status", "missing")
        for item in checked
    }

    return {
        "pipeline_signals_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not all_findings else "FAIL",
            "registry_path": str(registry_path).replace("\\", "/"),
            "registry_pipeline_count": len(pipelines),
            "checked_pipelines": checked,
            "provider_status_by_pipeline": provider_status_by_pipeline,
            "blocking_findings": all_findings,
            "result_summary": {
                "blocking_finding_count": len(all_findings),
                "implemented_count": sum(1 for s in provider_status_by_pipeline.values() if s == "implemented"),
                "not_implemented_count": sum(1 for s in provider_status_by_pipeline.values() if s == "not_implemented"),
                "not_applicable_count": sum(1 for s in provider_status_by_pipeline.values() if s == "not_applicable"),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="docs/registry/pipelines.md")
    parser.add_argument("--report", default="docs/registry/reports/pipeline_signals_validation.yaml")
    args = parser.parse_args()

    repo_root = Path(".")
    registry_path = Path(args.registry)
    report_path = Path(args.report)

    report = build_report(repo_root, registry_path)
    write_yaml(report_path, report)

    root = report["pipeline_signals_validation"]
    print(f"Status: {root['status']}")
    print(f"Wrote {report_path}")
    print(f"Checked pipelines: {root['registry_pipeline_count']}")
    print(f"Blocking findings: {root['result_summary']['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
