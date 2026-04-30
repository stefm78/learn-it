#!/usr/bin/env python3
"""Compute a generic post-run scope evolution score for Constitution runs.

Diagnostic only:
- writes scope_evolution_score.yaml and scope_evolution_score.md;
- may also refresh a diagnostic scope maturity report;
- never publishes maturity to policy.yaml or decisions.yaml.
"""

from __future__ import annotations

import argparse
import re
import subprocess
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

STAGE_CHECKS = [
    ("patch_validation", "work/04_patch_validation/patch_validation.yaml", "PATCHSET_VALIDATION", True),
    ("patch_execution", "reports/patch_execution_report.yaml", "PATCH_EXECUTION_REPORT", True),
    ("core_validation", "work/06_core_validation/core_validation.yaml", "CORE_VALIDATION", True),
    ("release_plan_validation", "reports/release_plan_validation.yaml", "RELEASE_PLAN_VALIDATION", True),
    ("release_materialization", "reports/release_materialization_report.yaml", "RELEASE_MATERIALIZATION_REPORT", True),
    ("release_manifest_validation", "reports/release_manifest_validation.yaml", "RELEASE_MANIFEST_VALIDATION", "release_only"),
    ("promotion", "reports/promotion_report.yaml", "PROMOTION_REPORT", "release_only"),
    ("current_manifest_validation", "reports/current_manifest_validation.yaml", "CURRENT_MANIFEST_VALIDATION", "release_only"),
    ("promotion_report_validation", "reports/promotion_report_validation.yaml", "PROMOTION_REPORT_VALIDATION", "release_only"),
    ("closeout", "reports/closeout_report.yaml", "CLOSEOUT_REPORT", True),
]


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


def status_of(path: Path, root_key: str) -> str:
    doc = load_yaml(path)
    root = doc.get(root_key)
    if isinstance(root, dict) and isinstance(root.get("status"), str):
        return root["status"]
    return "MISSING"


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def closeout_archive_path(run_dir: Path) -> Path | None:
    # STAGE_09 may reset runs/<RUN_ID>/work after archiving the operational
    # snapshot. Post-run scoring therefore must resolve evidence from either
    # the live run directory or the archived snapshot.
    closeout = load_yaml(run_dir / "reports/closeout_report.yaml")
    root = closeout.get("CLOSEOUT_REPORT", {})
    archive = root.get("archive_path") if isinstance(root, dict) else None
    if isinstance(archive, str) and archive:
        return Path(archive)
    return None


def resolve_run_artifact(run_dir: Path, archive_dir: Path | None, rel_path: str) -> Path:
    # Resolve an artifact first from the live run dir, then from closeout archive.
    live = run_dir / rel_path
    if live.exists():
        return live
    if archive_dir is not None:
        archived = archive_dir / rel_path
        if archived.exists():
            return archived
    return live


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_")


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


def tracking_state(runs_index: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    root = runs_index.get("runs_index", {})
    active = [x for x in root.get("active_runs", []) or [] if isinstance(x, dict)]
    closed = [x for x in root.get("closed_runs", []) or [] if isinstance(x, dict)]
    return {
        "active_runs_count": len(active),
        "run_in_active_runs": any(x.get("run_id") == run_id for x in active),
        "run_in_closed_runs": any(x.get("run_id") == run_id for x in closed),
        "current_stage": next((x.get("current_stage") for x in active + closed if x.get("run_id") == run_id), None),
    }


def release_required(run_dir: Path, archive_dir: Path | None) -> bool:
    plan_path = resolve_run_artifact(run_dir, archive_dir, "work/07_release/release_plan.yaml")
    plan = load_yaml(plan_path)
    root = plan.get("RELEASE_PLAN", {})
    return root.get("release_required") is True


def run_maturity_scoring(repo_root: Path, output: Path, force: bool) -> Dict[str, Any]:
    if output.exists() and not force:
        return load_yaml(output)
    script = repo_root / "docs/patcher/shared/score_constitution_scope_maturity.py"
    if not script.exists():
        raise SystemExit(f"Missing script: {script}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(script), "--report", str(output)]
    completed = subprocess.run(cmd, cwd=repo_root, text=True, capture_output=True)
    if completed.returncode != 0:
        raise SystemExit(
            "score_constitution_scope_maturity.py failed\n"
            + " ".join(cmd)
            + "\nSTDOUT:\n"
            + completed.stdout
            + "\nSTDERR:\n"
            + completed.stderr
        )
    return load_yaml(output)


def score_stage_chain(repo_root: Path, run_dir: Path, archive_dir: Path | None, rel_required: bool) -> Dict[str, Any]:
    checks = []
    expected_count = 0
    pass_count = 0

    for name, rel_path, root_key, expected_rule in STAGE_CHECKS:
        expected = expected_rule is True or (expected_rule == "release_only" and rel_required)
        path = resolve_run_artifact(run_dir, archive_dir, rel_path)
        status = status_of(path, root_key)
        if expected:
            expected_count += 1
            if status == "PASS":
                pass_count += 1
        checks.append({
            "name": name,
            "path": repo_rel(path, repo_root),
            "expected": expected,
            "status": status if expected else "NOT_EXPECTED",
        })

    score = round(20 * pass_count / expected_count) if expected_count else 0
    return {
        "score": score,
        "max": 20,
        "status": "PASS" if pass_count == expected_count else "WARN",
        "expected_pass_count": expected_count,
        "actual_pass_count": pass_count,
        "checks": checks,
    }


def score_closeout(repo_root: Path, run_dir: Path, tracking: Dict[str, Any]) -> Dict[str, Any]:
    closeout_path = run_dir / "reports/closeout_report.yaml"
    closeout_doc = load_yaml(closeout_path)
    closeout = closeout_doc.get("CLOSEOUT_REPORT", {})
    status = closeout.get("status") if isinstance(closeout, dict) else None
    summary_path = run_dir / "outputs/final_run_summary.md"

    if status == "PASS" and summary_path.exists() and tracking["run_in_closed_runs"]:
        score = 20
    elif status == "PASS" and summary_path.exists():
        score = 18
    elif status == "PASS":
        score = 12
    else:
        score = 0

    return {
        "score": score,
        "max": 20,
        "status": "PASS" if score >= 18 else "WARN" if score > 0 else "FAIL",
        "closeout_status": status or "MISSING",
        "final_summary_exists": summary_path.exists(),
        "governance_backlog_entries_exported": closeout.get("governance_backlog_entries_exported") if isinstance(closeout, dict) else None,
        "tracking": tracking,
    }


def score_maturity(scope_result: Dict[str, Any]) -> Dict[str, Any]:
    published = scope_result.get("published_maturity", {})
    computed = scope_result.get("computed_maturity", {})
    published_score = published.get("score_total")
    computed_score = computed.get("score_total")
    published_level = published.get("level")
    computed_level = computed.get("level")

    if not isinstance(published_score, int) or not isinstance(computed_score, int):
        return {"score": 0, "max": 20, "status": "UNKNOWN", "reason": "missing maturity score"}

    delta = computed_score - published_score
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
        "published_score": published_score,
        "published_level": published_level,
        "computed_score": computed_score,
        "computed_level": computed_level,
        "score_delta": delta,
    }


def score_backlog(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    severe = sum(1 for x in entries if x.get("type") in SEVERE_BACKLOG_TYPES)
    if severe == 0:
        score = 20
    elif severe <= 2:
        score = 16
    elif severe <= 4:
        score = 10
    elif severe <= 7:
        score = 7
    else:
        score = 4
    return {
        "score": score,
        "max": 20,
        "status": "PASS" if severe <= 2 else "WARN",
        "related_open_backlog_count": len(entries),
        "related_severe_open_backlog_count": severe,
        "open_entries": [
            {
                "entry_id": x.get("entry_id"),
                "type": x.get("type"),
                "title": x.get("title"),
                "source_run_id": x.get("source_run_id"),
            }
            for x in entries
        ],
    }


def score_cross_scope(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    terms = ("referentiel", "link", "learner_state", "deployment_governance", "cross-core", "cross_core")
    count = 0
    for item in entries:
        hay = " ".join(str(v or "") for v in [
            item.get("title"),
            item.get("description"),
            item.get("recommended_action"),
            " ".join(item.get("related_scope_keys", []) or []),
        ]).lower()
        if any(term in hay for term in terms):
            count += 1
    score = 10 if count == 0 else 7 if count <= 2 else 5 if count <= 4 else 3
    return {
        "score": score,
        "max": 10,
        "status": "PASS" if score >= 7 else "WARN",
        "cross_scope_open_count": count,
    }


def score_repeatability(repo_root: Path, run_dir: Path, archive_dir: Path | None) -> Dict[str, Any]:
    expected = [
        resolve_run_artifact(run_dir, archive_dir, "reports/patch_execution_report.yaml"),
        resolve_run_artifact(run_dir, archive_dir, "work/07_release/release_plan.yaml"),
        resolve_run_artifact(run_dir, archive_dir, "reports/promotion_report.yaml"),
        resolve_run_artifact(run_dir, archive_dir, "reports/closeout_report.yaml"),
        resolve_run_artifact(run_dir, archive_dir, "outputs/final_run_summary.md"),
    ]
    present_count = sum(1 for p in expected if p.exists())
    score = round(10 * present_count / len(expected))
    return {
        "score": score,
        "max": 10,
        "status": "PASS" if present_count == len(expected) else "WARN",
        "evidence": [{"path": repo_rel(p, repo_root), "present": p.exists()} for p in expected],
    }


def classify(score: int) -> str:
    if score >= 85:
        return "strong_scope_progress"
    if score >= 70:
        return "positive_progress_with_open_debt"
    if score >= 55:
        return "limited_progress_requires_follow_up"
    return "weak_or_incomplete_progress"


def markdown(report: Dict[str, Any]) -> str:
    root = report["scope_evolution_score"]
    lines = [
        f"# Scope evolution score — {root['scope_key']}",
        "",
        f"- Run: `{root['run_id']}`",
        f"- Status: `{root['status']}`",
        f"- Score: `{root['score_total']}/100`",
        f"- Classification: `{root['classification']}`",
        "",
        "## Dimensions",
        "",
    ]
    for key, value in root["dimensions"].items():
        lines.append(f"- `{key}`: `{value['score']}/{value['max']}` — `{value['status']}`")
    lines += ["", "## Interpretation", "", root["interpretation"], ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--scope-key", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--maturity-report")
    parser.add_argument("--output")
    parser.add_argument("--summary")
    parser.add_argument("--force-maturity-rescore", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_dir = repo_root / "docs/pipelines/constitution/runs" / args.run_id

    if not (repo_root / "docs/pipelines/constitution").exists():
        raise SystemExit("ERROR: run from repo root or pass --repo-root.")
    if not run_dir.exists():
        raise SystemExit(f"ERROR: run not found: {run_dir}")

    maturity_report_path = Path(args.maturity_report) if args.maturity_report else (
        repo_root / "docs/pipelines/constitution/reports" / f"scope_maturity_scoring_report_post_{slug(args.run_id)}.yaml"
    )
    if not maturity_report_path.is_absolute():
        maturity_report_path = repo_root / maturity_report_path

    output_path = Path(args.output) if args.output else run_dir / "reports/scope_evolution_score.yaml"
    summary_path = Path(args.summary) if args.summary else run_dir / "reports/scope_evolution_score.md"
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    if not summary_path.is_absolute():
        summary_path = repo_root / summary_path

    maturity_report = run_maturity_scoring(repo_root, maturity_report_path, args.force_maturity_rescore)
    scope_result = find_scope_result(maturity_report, args.scope_key)
    if not scope_result:
        raise SystemExit(f"ERROR: scope {args.scope_key!r} not found in maturity report.")

    runs_index = load_yaml(repo_root / "docs/pipelines/constitution/runs/index.yaml")
    backlog = load_yaml(repo_root / "docs/pipelines/constitution/scope_catalog/governance_backlog.yaml")

    archive_dir = closeout_archive_path(run_dir)
    if archive_dir is not None and not archive_dir.is_absolute():
        archive_dir = repo_root / archive_dir
    rel_required = release_required(run_dir, archive_dir)
    tracking = tracking_state(runs_index, args.run_id)
    entries = open_backlog_for_scope(backlog, args.scope_key)

    dimensions = {
        "stage_chain_integrity": score_stage_chain(repo_root, run_dir, archive_dir, rel_required),
        "closeout_and_tracking_readiness": score_closeout(repo_root, run_dir, tracking),
        "structural_maturity_delta": score_maturity(scope_result),
        "backlog_pressure": score_backlog(entries),
        "cross_scope_alignment_pressure": score_cross_scope(entries),
        "operational_repeatability": score_repeatability(repo_root, run_dir, archive_dir),
    }
    total = sum(v["score"] for v in dimensions.values())
    classification = classify(total)
    maturity = dimensions["structural_maturity_delta"]
    backlog_dim = dimensions["backlog_pressure"]

    report = {
        "scope_evolution_score": {
            "schema_version": 0.1,
            "status": "PASS" if total >= 55 else "WARN",
            "authority": "diagnostic_report_only",
            "does_not_update_policy": True,
            "run_id": args.run_id,
            "scope_key": args.scope_key,
            "score_total": total,
            "max_score": 100,
            "classification": classification,
            "evidence_resolution": {
                "live_run_dir": repo_rel(run_dir, repo_root),
                "archive_dir": repo_rel(archive_dir, repo_root) if archive_dir else None,
                "archive_fallback_enabled": archive_dir is not None,
            },
            "maturity_context": {
                "published_score": maturity.get("published_score"),
                "published_level": maturity.get("published_level"),
                "computed_score": maturity.get("computed_score"),
                "computed_level": maturity.get("computed_level"),
                "score_delta": maturity.get("score_delta"),
                "maturity_report": repo_rel(maturity_report_path, repo_root),
            },
            "dimensions": dimensions,
            "interpretation": (
                f"Run {args.run_id} produced {classification} for scope {args.scope_key}. "
                f"This is diagnostic only. Published maturity is not changed. "
                f"Related severe open backlog count is {backlog_dim.get('related_severe_open_backlog_count')}."
            ),
            "recommended_next_action": (
                "Keep this report as diagnostic evidence; use STAGE_00 / partition_refresh or a dedicated cross-scope run before publishing a stronger maturity score."
                if backlog_dim.get("related_severe_open_backlog_count", 0) > 0
                else "Consider a governed maturity publication step only if human arbitration approves it."
            ),
        }
    }

    write_yaml(output_path, report)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(markdown(report), encoding="utf-8")

    print(f"Wrote {repo_rel(output_path, repo_root)}")
    print(f"Wrote {repo_rel(summary_path, repo_root)}")
    print(f"Score: {total}/100 ({classification})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
