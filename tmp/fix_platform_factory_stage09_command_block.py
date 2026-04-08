#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PATH_MD = REPO_ROOT / "docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md"

OLD = """```bash
python docs/patcher/shared/closeout_platform_factory_run.py   ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml   ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml   ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml   ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml   ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md   ./docs/pipelines/platform_factory/archive
```"""

NEW = """```bash
python docs/patcher/shared/closeout_platform_factory_run.py \\
  ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml \\
  ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \\
  ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \\
  ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml \\
  ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md \\
  ./docs/pipelines/platform_factory/archive
```"""


def main() -> None:
    text = PATH_MD.read_text(encoding="utf-8")
    if OLD not in text:
        raise SystemExit("Expected flattened Stage 09 command block not found.")
    text = text.replace(OLD, NEW, 1)
    PATH_MD.write_text(text, encoding="utf-8")
    print(f"UPDATED {PATH_MD.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
