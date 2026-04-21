#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/patcher/shared/reconcile_run.py")


NEW_RENDER_DASHBOARD_HUMAN = '''def render_dashboard_human(
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

    headers = {
        "run_id": "RUN_ID",
        "scope_key": "SCOPE_KEY",
        "run_status": "STATUS",
        "current_stage": "STAGE",
        "mode": "MODE",
    }

    def s(value: Any) -> str:
        return "" if value is None else str(value)

    widths = {
        "run_id": len(headers["run_id"]),
        "scope_key": len(headers["scope_key"]),
        "run_status": len(headers["run_status"]),
        "current_stage": len(headers["current_stage"]),
        "mode": len(headers["mode"]),
    }

    for row in rows:
        widths["run_id"] = max(widths["run_id"], len(s(row.get("run_id", ""))))
        widths["scope_key"] = max(widths["scope_key"], len(s(row.get("scope_key", ""))))
        widths["run_status"] = max(widths["run_status"], len(s(row.get("run_status", ""))))
        widths["current_stage"] = max(widths["current_stage"], len(s(row.get("current_stage", ""))))
        widths["mode"] = max(widths["mode"], len(s(row.get("mode", ""))))

    def fmt_row(run_id: str, scope_key: str, run_status: str, current_stage: str, mode: str) -> str:
        return (
            f"{run_id:<{widths['run_id']}} | "
            f"{scope_key:<{widths['scope_key']}} | "
            f"{run_status:<{widths['run_status']}} | "
            f"{current_stage:<{widths['current_stage']}} | "
            f"{mode:<{widths['mode']}}"
        )

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

    header_line = fmt_row(
        headers["run_id"],
        headers["scope_key"],
        headers["run_status"],
        headers["current_stage"],
        headers["mode"],
    )
    separator_line = (
        f"{'-' * widths['run_id']}-+-"
        f"{'-' * widths['scope_key']}-+-"
        f"{'-' * widths['run_status']}-+-"
        f"{'-' * widths['current_stage']}-+-"
        f"{'-' * widths['mode']}"
    )

    lines.append(header_line)
    lines.append(separator_line)

    for row in rows:
        lines.append(
            fmt_row(
                s(row.get("run_id", "")),
                s(row.get("scope_key", "")),
                s(row.get("run_status", "")),
                s(row.get("current_stage", "")),
                s(row.get("mode", "")),
            )
        )

    if not rows:
        lines.append("(no run matched the current filter)")

    return "\\n".join(lines) + "\\n"
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


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    raw = TARGET.read_text(encoding="utf-8")
    newline = detect_newline(raw)
    text = normalize_newlines(raw)

    text = replace_top_level_function(text, "render_dashboard_human", NEW_RENDER_DASHBOARD_HUMAN)

    TARGET.write_text(restore_newlines(text, newline), encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()