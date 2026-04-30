#!/usr/bin/env python3
"""Compute a STAGE_06 pre-release scope evolution preview for Constitution runs.

This script answers:
- What was the baseline state when the run was opened?
- What does the sandboxed post-patch state prove before release?
- Is it reasonable to proceed to STAGE_07 release materialization?

It is diagnostic and does not decide material release_required. STAGE_07
build_release_plan.py remains authoritative for material release necessity.
"""

from __future__ import annotations

import argparse
import re
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


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def root_status(path: Path, root_key: str) -> str:
    doc = load_yaml(path)
    root = doc.get(root_key)
    if isinstance(root, dict) and isinstance(root.get("status"), str):
        return root["status"]
    return "MISSING"


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


def find_scope_result(maturity_report: Dict[str, Any], scope_key: str) -> Dict[str, Any]:
    root = maturity_report.get("scope_maturity_scoring_report", {})
    for item in root.get("scope_results", []) or []:
        if isinstance(item, dict) and item.get("scope_key") == scope_key:
            return item
    return {}


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


def count_backlog_candidates(arbitrage_dir: Path) -> int:
    if not arbitrage_dir.exists():
        return 0
    count = 0
    for path in sorted(arbitrage_dir.glob("arbitrage*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        # Conservative count: candidate_id lines inside report text.
        count += len(re.findall(r"candidate_id\s*:", text))
    return count


def material_change_signal(patch_execution_report: Dict[str, Any]) -> Dict[str, Any]:
    root = patch_execution_report.get("PATCH_EXECUTION_REPORT", {})
    if not isinstance(root, dict):
        return {"material_change_detected": False, "reason": "patch_execution_report_missing"}
    if root.get("status") != "PASS":
        return {"material_change_detected": False, "reason": "patch_execution_not_pass"}
    if root.get("whatif") is True:
        return {"material_change_detected": False, "reason": "whatif_execution"}
    # The execution report schema may vary. A PASS non-whatif execution after a validated
    # patchset is a sufficient pre-release signal that STAGE_07 should compute the release plan.
    return {
        "material_change_detected": True,
        "reason": "patch_execution_pass_non_whatif",
    }


def score_pre_release_stage_chain(repo_root: Path, run_dir: Path) -> Dict[str, Any]:
    checks = [
        ("patch_validation", run_dir / "work/04_patch_validation/patch_validation.yaml", "PATCHSET_VALIDATION"),
        ("patch_execution", run_dir / "reports/patch_execution_report.yaml", "PATCH_EXECUTION_REPORT"),
        ("core_validation", run_dir / "work/06_core_validation/core_validation.yaml", "CORE_VALIDATION"),
    ]
    pass_count = 0
    rows = []
    for name, path, root_key in checks:
        status = root_status(path, root_key)
        if status == "PASS":
            pass_count += 1
        rows.append({
            "name": name,
            "path": repo_rel(path, repo_root),
            "status": status,
            "expected": True,
        })
    score = round(40 * pass_count / len(checks))
    return {
        "score": score,
        "max": 40,
        "status": "PASS" if pass_count == len(checks) else "WARN",
        "expected_pass_count": len(checks),
        "actual_pass_count": pass_count,
        "checks": rows,
    }


def score_maturity_delta(baseline: Dict[str, Any], scope_result: Dict[str, Any]) -> Dict[str, Any]:
    base = baseline.get("baseline_scope_state", {}).get("maturity_baseline", {})
    computed = scope_result.get("computed_maturity", {})
    before_score = base.get("score_total")
    before_level = base.get("level")
    computed_score = computed.get("score_total")
    computed_level = computed.get("level")

    if not isinstance(before_score, int) or not isinstance(computed_score, int):
        return {
            "score": 0,
            "max": 20,
            "status": "UNKNOWN",
            "reason": "baseline or computed maturity missing",
        }

    delta = computed_score - before_score
    if delta >= 2:
        score = 20
    elif delta == 1:
        score = 15
    elif delta == 0:
        score = 10
    elif delta == -1:
        score = 5
    else:
        score = 0

    return {
        "score": score,
        "max": 20,
        "status": "PASS" if delta >= 0 else "WARN",
        "before_score": before_score,
        "before_level": before_level,
        "computed_score": computed_score,
        "computed_level": computed_level,
        "score_delta_preview": delta,
        "note": "Computed maturity is based on current governed inputs; sandbox maturity publication remains out of scope.",
    }


def score_backlog_delta(baseline: Dict[str, Any], current_entries: List[Dict[str, Any]], candidate_count: int) -> Dict[str, Any]:
    baseline_root = baseline.get("baseline_scope_state", {}).get("backlog_baseline", {})
    before_open = baseline_root.get("open_count", 0) if isinstance(baseline_root.get("open_count"), int) else 0
    before_severe = baseline_root.get("severe_open_count", 0) if isinstance(baseline_root.get("severe_open_count"), int) else 0
    current_severe = sum(1 for x in current_entries if x.get("type") in SEVERE_BACKLOG_TYPES)

    projected_open = len(current_entries) + candidate_count
    projected_severe = current_severe + candidate_count
    severe_delta = projected_severe - before_severe

    if projected_severe == 0:
        score = 20
    elif severe_delta <= 0:
        score = 16
    elif severe_delta <= 2:
        score = 12
    elif severe_delta <= 4:
        score = 8
    else:
        score = 4

    return {
        "score": score,
        "max": 20,
        "status": "PASS" if severe_delta <= 0 else "WARN",
        "before_open_backlog_count": before_open,
        "before_severe_open_backlog_count": before_severe,
        "current_open_backlog_count": len(current_entries),
        "current_severe_open_backlog_count": current_severe,
        "candidate_backlog_count_from_arbitrage": candidate_count,
        "projected_open_backlog_count_after_closeout": projected_open,
        "projected_severe_open_backlog_count_after_closeout": projected_severe,
        "projected_severe_delta": severe_delta,
    }


def score_release_value(stage_chain: Dict[str, Any], material_signal: Dict[str, Any], maturity_delta: Dict[str, Any], backlog_delta: Dict[str, Any]) -> Dict[str, Any]:
    if stage_chain.get("status") != "PASS":
        score = 0
        recommendation = "do_not_release_return_upstream"
        reason = "pre_release_stage_chain_not_pass"
    elif not material_signal.get("material_change_detected"):
        score = 8
        recommendation = "build_release_plan_to_confirm_noop"
        reason = material_signal.get("reason")
    elif backlog_delta.get("projected_severe_delta", 0) > 4:
        score = 12
        recommendation = "release_possible_but_high_backlog_pressure"
        reason = "material_change_positive_but_backlog_pressure_high"
    else:
        score = 20 if maturity_delta.get("score_delta_preview", 0) > 0 else 16
        recommendation = "proceed_to_stage_07_release_plan"
        reason = "material_change_validated_and_core_validation_passed"

    return {
        "score": score,
        "max": 20,
        "status": "PASS" if score >= 16 else "WARN" if score > 0 else "FAIL",
        "recommendation": recommendation,
        "reason": reason,
        "material_release_required_authority": "STAGE_07_build_release_plan.py",
        "preview_position": "This preview can recommend whether to proceed to STAGE_07, but cannot itself declare release_required.",
    }


def markdown(report: Dict[str, Any]) -> str:
    root = report["scope_evolution_preview"]
    lines = [
        f"# Scope evolution preview — {root['scope_key']}",
        "",
        f"- Run: `{root['run_id']}`",
        f"- Status: `{root['status']}`",
        f"- Score: `{root['score_total']}/100`",
        f"- Classification: `{root['classification']}`",
        f"- Release recommendation: `{root['release_assessment']['recommendation']}`",
        "",
        "## Before / after preview",
        "",
        f"- Baseline maturity: `{root['before']['maturity_score']}` / `{root['before']['maturity_level']}`",
        f"- Computed maturity preview: `{root['after_sandbox']['computed_maturity_score']}` / `{root['after_sandbox']['computed_maturity_level']}`",
        f"- Maturity delta preview: `{root['delta']['maturity_score_delta']}`",
        f"- Projected severe backlog delta: `{root['delta']['projected_severe_backlog_delta']}`",
        "",
        "## Dimensions",
        "",
    ]
    for key, value in root["dimensions"].items():
        lines.append(f"- `{key}`: `{value['score']}/{value['max']}` — `{value['status']}`")
    lines.extend(["", "## Interpretation", "", root["interpretation"], ""])
    return "\n".join(lines)


def classify(score: int) -> str:
    if score >= 85:
        return "strong_pre_release_progress"
    if score >= 70:
        return "positive_pre_release_progress_with_open_debt"
    if score >= 55:
        return "limited_pre_release_progress_requires_attention"
    return "weak_or_blocked_pre_release_progress"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--scope-key")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--maturity-report", default="docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml")
    parser.add_argument("--output")
    parser.add_argument("--summary")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / "docs/pipelines/constitution").exists():
        raise SystemExit("ERROR: run from repo root or pass --repo-root.")

    scope_key = resolve_scope_key(repo_root, args.run_id, args.scope_key)
    run_dir = repo_root / "docs/pipelines/constitution/runs" / args.run_id
    baseline_path = run_dir / "inputs/baseline_scope_state.yaml"
    output_path = Path(args.output) if args.output else run_dir / "work/06_core_validation/scope_evolution_preview.yaml"
    summary_path = Path(args.summary) if args.summary else run_dir / "work/06_core_validation/scope_evolution_preview.md"
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    if not summary_path.is_absolute():
        summary_path = repo_root / summary_path

    baseline = load_yaml(baseline_path)
    if not baseline:
        raise SystemExit(f"ERROR: missing baseline: {baseline_path}")

    maturity_report_path = Path(args.maturity_report)
    if not maturity_report_path.is_absolute():
        maturity_report_path = repo_root / maturity_report_path
    maturity_report = load_yaml(maturity_report_path)
    scope_result = find_scope_result(maturity_report, scope_key)
    if not scope_result:
        raise SystemExit(f"ERROR: scope {scope_key!r} not found in maturity report {maturity_report_path}")

    backlog = load_yaml(repo_root / "docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")
    current_entries = open_backlog_for_scope(backlog, scope_key)
    candidate_count = count_backlog_candidates(run_dir / "work/02_arbitrage")

    stage_chain = score_pre_release_stage_chain(repo_root, run_dir)
    patch_execution = load_yaml(run_dir / "reports/patch_execution_report.yaml")
    material_signal = material_change_signal(patch_execution)
    maturity_delta = score_maturity_delta(baseline, scope_result)
    backlog_delta = score_backlog_delta(baseline, current_entries, candidate_count)
    release_value = score_release_value(stage_chain, material_signal, maturity_delta, backlog_delta)

    dimensions = {
        "pre_release_stage_chain": stage_chain,
        "maturity_delta_preview": maturity_delta,
        "backlog_delta_preview": backlog_delta,
        "release_value_preview": release_value,
    }
    total = sum(item["score"] for item in dimensions.values())
    classification = classify(total)

    baseline_root = baseline.get("baseline_scope_state", {})
    maturity_base = baseline_root.get("maturity_baseline", {})
    before_score = maturity_base.get("score_total")
    before_level = maturity_base.get("level")
    computed = scope_result.get("computed_maturity", {})

    report = {
        "scope_evolution_preview": {
            "schema_version": 0.1,
            "status": "PASS" if total >= 55 and stage_chain.get("status") == "PASS" else "WARN",
            "authority": "pre_release_diagnostic_only",
            "does_not_update_policy": True,
            "run_id": args.run_id,
            "scope_key": scope_key,
            "stage": "STAGE_06_CORE_VALIDATION",
            "score_total": total,
            "max_score": 100,
            "classification": classification,
            "before": {
                "baseline_path": repo_rel(baseline_path, repo_root),
                "maturity_score": before_score,
                "maturity_level": before_level,
                "open_backlog_count": baseline_root.get("backlog_baseline", {}).get("open_count"),
                "severe_open_backlog_count": baseline_root.get("backlog_baseline", {}).get("severe_open_count"),
            },
            "after_sandbox": {
                "computed_maturity_score": computed.get("score_total"),
                "computed_maturity_level": computed.get("level"),
                "material_change_signal": material_signal,
                "core_validation_status": root_status(run_dir / "work/06_core_validation/core_validation.yaml", "CORE_VALIDATION"),
            },
            "delta": {
                "maturity_score_delta": maturity_delta.get("score_delta_preview"),
                "projected_severe_backlog_delta": backlog_delta.get("projected_severe_delta"),
            },
            "release_assessment": {
                "recommendation": release_value.get("recommendation"),
                "reason": release_value.get("reason"),
                "material_release_required_authority": "STAGE_07 build_release_plan.py",
            },
            "dimensions": dimensions,
            "interpretation": (
                f"Pre-release preview for {scope_key}: {classification}. "
                "This report compares the run-opening baseline with the sandboxed post-patch state before release. "
                "It recommends whether to proceed to STAGE_07, but STAGE_07 remains authoritative for material release_required."
            ),
        }
    }

    write_yaml(output_path, report)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(markdown(report), encoding="utf-8")

    print(f"Wrote {repo_rel(output_path, repo_root)}")
    print(f"Wrote {repo_rel(summary_path, repo_root)}")
    print(f"Score: {total}/100 ({classification})")
    print(f"Release recommendation: {release_value.get('recommendation')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
