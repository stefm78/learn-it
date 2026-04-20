#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/patcher/shared/reconcile_run.py")


NEW_PARSE_ARGS = '''
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile a constitution run.")
    parser.add_argument("--pipeline", required=True)
    parser.add_argument("--run-id", required=False)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the reconciliation plan materially.",
    )
    parser.add_argument(
        "--output",
        choices=("human", "json"),
        default="human",
        help="Select output format. In this step, it affects dashboard mode.",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Render a dashboard view from runs/index.yaml.",
    )
    parser.add_argument(
        "--dashboard-probe",
        action="store_true",
        help="Reserved for the next step: dashboard enriched with reconciliation probes.",
    )
    parser.add_argument(
        "--output-mode",
        choices=("full", "compact"),
        default="full",
        help="Select reconciliation payload verbosity.",
    )
    return parser.parse_args()
'''


NEW_DASHBOARD_HELPERS = '''
def build_dashboard_rows(index_data: Dict[str, Any], pattern: str) -> List[Dict[str, Any]]:
    runs_index = index_data.get("runs_index", {})
    active_runs = runs_index.get("active_runs", [])
    closed_runs = runs_index.get("closed_runs", [])

    normalized_pattern = (pattern or "*").upper()

    def matches(entry: Dict[str, Any]) -> bool:
        candidates = [
            str(entry.get("run_id", "")),
            str(entry.get("scope_key", "")),
            str(entry.get("scope_id", "")),
        ]
        return any(
            candidate and fnmatch.fnmatchcase(candidate.upper(), normalized_pattern)
            for candidate in candidates
        )

    rows: List[Dict[str, Any]] = []

    if isinstance(active_runs, list):
        for entry in active_runs:
            if not isinstance(entry, dict):
                continue
            if not matches(entry):
                continue
            rows.append(
                {
                    "bucket": "active",
                    "run_id": str(entry.get("run_id", "")),
                    "scope_key": str(entry.get("scope_key", "")),
                    "scope_id": str(entry.get("scope_id", "")),
                    "run_status": str(entry.get("run_status", "")),
                    "current_stage": str(entry.get("current_stage", "")),
                    "mode": str(entry.get("mode", "")),
                }
            )

    if isinstance(closed_runs, list):
        for entry in closed_runs:
            if not isinstance(entry, dict):
                continue
            if not matches(entry):
                continue
            rows.append(
                {
                    "bucket": "closed",
                    "run_id": str(entry.get("run_id", "")),
                    "scope_key": str(entry.get("scope_key", "")),
                    "scope_id": str(entry.get("scope_id", "")),
                    "run_status": str(entry.get("run_status", "")),
                    "current_stage": str(entry.get("current_stage", "")),
                    "mode": str(entry.get("mode", "")),
                }
            )

    rows.sort(key=lambda item: (0 if item["bucket"] == "active" else 1, item["run_id"]))
    return rows


def build_dashboard_payload(
    index_data: Dict[str, Any],
    rows: List[Dict[str, Any]],
    pattern: str,
) -> Dict[str, Any]:
    runs_index = index_data.get("runs_index", {})
    active_runs = runs_index.get("active_runs", [])
    closed_runs = runs_index.get("closed_runs", [])

    matched_active = sum(1 for row in rows if row.get("bucket") == "active")
    matched_closed = sum(1 for row in rows if row.get("bucket") == "closed")

    payload = {
        "runs_dashboard": {
            "pipeline_id": str(runs_index.get("pipeline_id", "")),
            "last_updated": str(runs_index.get("last_updated", "")),
            "filter": pattern or "*",
            "counts": {
                "total_runs": (len(active_runs) if isinstance(active_runs, list) else 0)
                + (len(closed_runs) if isinstance(closed_runs, list) else 0),
                "active_runs": len(active_runs) if isinstance(active_runs, list) else 0,
                "closed_runs": len(closed_runs) if isinstance(closed_runs, list) else 0,
                "matched_runs": len(rows),
                "matched_active_runs": matched_active,
                "matched_closed_runs": matched_closed,
            },
            "items": rows,
        }
    }
    return payload


def render_dashboard_human(
    index_data: Dict[str, Any],
    rows: List[Dict[str, Any]],
    pattern: str,
) -> str:
    runs_index = index_data.get("runs_index", {})
    active_runs = runs_index.get("active_runs", [])
    closed_runs = runs_index.get("closed_runs", [])

    total_runs = (len(active_runs) if isinstance(active_runs, list) else 0) + (
        len(closed_runs) if isinstance(closed_runs, list) else 0
    )
    active_count = len(active_runs) if isinstance(active_runs, list) else 0
    closed_count = len(closed_runs) if isinstance(closed_runs, list) else 0

    lines: List[str] = []
    if pattern and pattern != "*":
        lines.append(f"FILTER {pattern}")
    lines.append(
        f"PIPELINE {runs_index.get('pipeline_id', '')}  |  LAST_UPDATED {runs_index.get('last_updated', '')}"
    )
    lines.append(
        f"TOTAL {total_runs}  |  ACTIVE {active_count}  |  CLOSED {closed_count}  |  MATCHED {len(rows)}"
    )
    lines.append("")
    lines.append(
        f"{'RUN_ID':<52} {'SCOPE_KEY':<22} {'STATUS':<15} {'STAGE':<30} {'MODE'}"
    )

    for row in rows:
        lines.append(
            f"{row.get('run_id', ''):<52} "
            f"{row.get('scope_key', ''):<22} "
            f"{row.get('run_status', ''):<15} "
            f"{row.get('current_stage', ''):<30} "
            f"{row.get('mode', '')}"
        )

    if not rows:
        lines.append("(no run matched the current filter)")

    return "\\n".join(lines) + "\\n"
'''


OLD_MAIN_HEAD = '''
def main() -> int:
    args = parse_args()
    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline for now: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline
    run_root = pipeline_root / "runs" / args.run_id
    run_manifest_path = run_root / "run_manifest.yaml"
    runs_index_path = pipeline_root / "runs" / "index.yaml"
'''


NEW_MAIN_HEAD = '''
def main() -> int:
    args = parse_args()
    if args.pipeline != "constitution":
        raise SystemExit("Unsupported pipeline for now: constitution only")

    repo_root = Path(args.repo_root).resolve()
    pipeline_root = repo_root / "docs" / "pipelines" / args.pipeline

    if args.dashboard or args.dashboard_probe:
        if args.dashboard_probe:
            raise SystemExit(
                "--dashboard-probe is reserved for the next step. Use --dashboard first."
            )

        runs_index_path = pipeline_root / "runs" / "index.yaml"
        if not runs_index_path.exists():
            raise SystemExit(f"runs/index.yaml missing: {runs_index_path}")

        index_data = load_yaml(runs_index_path)
        filter_pattern = args.run_id or "*"
        rows = build_dashboard_rows(index_data, filter_pattern)

        if args.output == "json":
            payload = build_dashboard_payload(index_data, rows, filter_pattern)
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(render_dashboard_human(index_data, rows, filter_pattern), end="")
        return 0

    if not args.run_id:
        raise SystemExit("--run-id is required outside dashboard mode")

    run_root = pipeline_root / "runs" / args.run_id
    run_manifest_path = run_root / "run_manifest.yaml"
    runs_index_path = pipeline_root / "runs" / "index.yaml"
'''


def detect_newline(text: str) -> str:
    if "\\r\\n" in text:
        return "\\r\\n"
    if "\\r" in text:
        return "\\r"
    return "\\n"


def normalize_newlines(text: str) -> str:
    return text.replace("\\r\\n", "\\n").replace("\\r", "\\n")


def restore_newlines(text: str, newline: str) -> str:
    return text.replace("\\n", newline)


def cleanup_broken_literal_newlines(text: str) -> str:
    text = text.replace("import fnmatch\\\\n\\n", "import fnmatch\\n")
    text = text.replace("import fnmatch\\\\n", "import fnmatch\\n")
    return text


def replace_top_level_function(source: str, func_name: str, new_block: str) -> str:
    lines = source.splitlines(keepends=True)

    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"def {func_name}("):
            start = i
            break
    if start is None:
        raise RuntimeError(f"Function not found: {func_name}")

    end = None
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.startswith("def ") or line.startswith('if __name__ == "__main__":'):
            end = i
            break
    if end is None:
        end = len(lines)

    replacement = new_block.strip("\\n").splitlines(keepends=True)
    replacement = [line if line.endswith("\\n") else line + "\\n" for line in replacement]
    replacement.append("\\n")

    return "".join(lines[:start] + replacement + lines[end:])


def insert_import_if_missing(source: str, import_line: str) -> str:
    lines = source.splitlines(keepends=True)

    if any(line.strip() == import_line for line in lines):
        return source

    insert_at = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            insert_at = i + 1

    if insert_at is None:
        raise RuntimeError("No import block found in target file")

    lines.insert(insert_at, import_line + "\\n")
    return "".join(lines)


def insert_before_top_level_function(source: str, func_name: str, block: str) -> str:
    if block.strip() in source:
        return source

    lines = source.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"def {func_name}("):
            start = i
            break
    if start is None:
        raise RuntimeError(f"Top-level function marker not found: {func_name}")

    insertion = block.strip("\\n").splitlines(keepends=True)
    insertion = [line if line.endswith("\\n") else line + "\\n" for line in insertion]
    insertion.append("\\n")

    return "".join(lines[:start] + insertion + lines[start:])


def replace_exact_once(source: str, old: str, new: str) -> str:
    if old not in source:
        raise RuntimeError("Expected block not found for replacement")
    return source.replace(old, new, 1)


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    raw_text = TARGET.read_text(encoding="utf-8")
    newline = detect_newline(raw_text)
    text = normalize_newlines(raw_text)

    text = cleanup_broken_literal_newlines(text)
    text = insert_import_if_missing(text, "import fnmatch")
    text = replace_top_level_function(text, "parse_args", NEW_PARSE_ARGS)
    text = insert_before_top_level_function(
        text,
        "build_compact_reconciliation_payload",
        NEW_DASHBOARD_HELPERS,
    )
    text = replace_exact_once(text, OLD_MAIN_HEAD.strip("\\n"), NEW_MAIN_HEAD.strip("\\n"))

    TARGET.write_text(restore_newlines(text, newline), encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()