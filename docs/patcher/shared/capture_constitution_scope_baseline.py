#!/usr/bin/env python3
"""Capture a baseline scope state at Constitution run materialization time.

Diagnostic only:
- writes runs/<RUN_ID>/inputs/baseline_scope_state.yaml;
- does not modify policy, decisions, catalog, Core files, backlog, releases, or tracking.

The baseline is used later by STAGE_06 pre-release preview and STAGE_09 final
scope evolution scoring to compare "before run" and "after run" state.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required.") from exc


SEVERE_BACKLOG_TYPES = {
    "scope_gap",
    "scope_extension_needed",
    "orphan_id",
    "partition_angle_mort",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_scope_key(repo_root: Path, run_id: str, explicit_scope_key: str | None) -> str:
    if explicit_scope_key:
        return explicit_scope_key
    manifest = load_yaml(repo_root / "docs/pipelines/constitution/runs" / run_id / "run_manifest.yaml")
    root = manifest.get("run_manifest", {})
    scope_key = root.get("scope_key")
    if scope_key:
        return scope_key
    scope_binding = root.get("scope_binding", {}) if isinstance(root.get("scope_binding"), dict) else {}
    scope_key = scope_binding.get("scope_key")
    if scope_key:
        return scope_key
    raise SystemExit("ERROR: cannot resolve scope_key. Pass --scope-key explicitly.")


def find_scope_policy(policy: Dict[str, Any], scope_key: str) -> Dict[str, Any]:
    root = policy.get("scope_generation_policy", {})
    for item in root.get("declared_scopes", []) or []:
        if isinstance(item, dict) and item.get("scope_key") == scope_key:
            return item
    # Fallback for older or nested policy shapes.
    stack: List[Any] = [policy]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            if value.get("scope_key") == scope_key:
                return value
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    return {}


def maturity_from_scope_policy(scope_policy: Dict[str, Any]) -> Dict[str, Any]:
    maturity = scope_policy.get("maturity", {})
    if isinstance(maturity, dict):
        axes = maturity.get("axes", {})
        return {
            "source": "policy.yaml",
            "score_total": maturity.get("score_total") or maturity.get("score"),
            "level": maturity.get("level"),
            "axes": axes if isinstance(axes, dict) else {},
        }

    # Fallback for flatter shapes.
    return {
        "source": "policy.yaml",
        "score_total": scope_policy.get("score_total") or scope_policy.get("maturity_score"),
        "level": scope_policy.get("level") or scope_policy.get("maturity_level"),
        "axes": scope_policy.get("axes", {}) if isinstance(scope_policy.get("axes"), dict) else {},
    }


def open_backlog_for_scope(backlog_doc: Dict[str, Any], scope_key: str) -> List[Dict[str, Any]]:
    root = backlog_doc.get("governance_backlog", {})
    entries = []
    for item in root.get("entries", []) or []:
        if not isinstance(item, dict) or item.get("status") != "open":
            continue
        related = set()
        if isinstance(item.get("scope_key"), str):
            related.add(item["scope_key"])
        for value in item.get("related_scope_keys", []) or []:
            if isinstance(value, str):
                related.add(value)
        if scope_key in related:
            entries.append(item)
    return sorted(entries, key=lambda x: x.get("entry_id", ""))


def compact_backlog_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "entry_id": item.get("entry_id"),
            "type": item.get("type"),
            "status": item.get("status"),
            "title": item.get("title"),
            "source_run_id": item.get("source_run_id"),
            "related_scope_keys": item.get("related_scope_keys", []),
        }
        for item in entries
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--scope-key")
    parser.add_argument("--pipeline", default="constitution")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / "docs/pipelines/constitution").exists():
        raise SystemExit("ERROR: run from repo root or pass --repo-root.")

    scope_key = resolve_scope_key(repo_root, args.run_id, args.scope_key)
    run_dir = repo_root / "docs/pipelines" / args.pipeline / "runs" / args.run_id

    output = Path(args.output) if args.output else run_dir / "inputs/baseline_scope_state.yaml"
    if not output.is_absolute():
        output = repo_root / output

    policy_path = repo_root / "docs/pipelines/constitution/policies/scope_generation/policy.yaml"
    backlog_path = repo_root / "docs/pipelines/constitution/scope_catalog/governance_backlog.yaml"
    current_manifest_path = repo_root / "docs/cores/current/manifest.yaml"
    scope_manifest_path = run_dir / "inputs/scope_manifest.yaml"
    impact_bundle_path = run_dir / "inputs/impact_bundle.yaml"
    integration_gate_path = run_dir / "inputs/integration_gate.yaml"

    policy = load_yaml(policy_path)
    backlog = load_yaml(backlog_path)
    current_manifest = load_yaml(current_manifest_path)
    scope_manifest = load_yaml(scope_manifest_path)
    impact_bundle = load_yaml(impact_bundle_path)
    integration_gate = load_yaml(integration_gate_path)

    scope_policy = find_scope_policy(policy, scope_key)
    maturity = maturity_from_scope_policy(scope_policy)
    open_entries = open_backlog_for_scope(backlog, scope_key)
    severe_entries = [x for x in open_entries if x.get("type") in SEVERE_BACKLOG_TYPES]

    report = {
        "baseline_scope_state": {
            "schema_version": 0.1,
            "status": "PASS",
            "authority": "diagnostic_snapshot_only",
            "does_not_update_policy": True,
            "run_id": args.run_id,
            "scope_key": scope_key,
            "capture_stage": "MATERIALIZE_NEW_RUN",
            "baseline_kind": "pre_stage_01_pre_patch",
            "maturity_baseline": maturity,
            "backlog_baseline": {
                "open_count": len(open_entries),
                "severe_open_count": len(severe_entries),
                "open_entries": compact_backlog_entries(open_entries),
            },
            "current_manifest_baseline": {
                "path": repo_rel(current_manifest_path, repo_root),
                "sha256": sha256_file(current_manifest_path),
                "manifest_id": current_manifest.get("manifest", {}).get("manifest_id")
                if isinstance(current_manifest.get("manifest"), dict)
                else current_manifest.get("id"),
                "release_id": current_manifest.get("manifest", {}).get("release_id")
                if isinstance(current_manifest.get("manifest"), dict)
                else current_manifest.get("release_id"),
            },
            "run_input_fingerprints": {
                "scope_manifest": {
                    "path": repo_rel(scope_manifest_path, repo_root),
                    "present": bool(scope_manifest),
                    "sha256": sha256_file(scope_manifest_path),
                },
                "impact_bundle": {
                    "path": repo_rel(impact_bundle_path, repo_root),
                    "present": bool(impact_bundle),
                    "sha256": sha256_file(impact_bundle_path),
                },
                "integration_gate": {
                    "path": repo_rel(integration_gate_path, repo_root),
                    "present": bool(integration_gate),
                    "sha256": sha256_file(integration_gate_path),
                },
            },
            "notes": [
                "Baseline captured before STAGE_01_CHALLENGE.",
                "Used later for STAGE_06 pre-release scope evolution preview and STAGE_09 final scope evolution score.",
                "This file is diagnostic only and does not publish any maturity value.",
            ],
        }
    }

    write_yaml(output, report)
    print(f"Wrote {repo_rel(output, repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
