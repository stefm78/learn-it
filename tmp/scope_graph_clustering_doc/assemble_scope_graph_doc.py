#!/usr/bin/env python3
"""Assemble the scope graph clustering approach document from small Markdown parts.

This script is intentionally temporary. It exists to avoid large single-file writes
through remote tooling and to keep the generated document reproducible.

Run from repository root:

    python tmp/scope_graph_clustering_doc/assemble_scope_graph_doc.py

It reads:

    tmp/scope_graph_clustering_doc/parts/*.md

and writes:

    docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md
"""

from __future__ import annotations

from pathlib import Path


PARTS_DIR = Path("tmp/scope_graph_clustering_doc/parts")
OUTPUT_PATH = Path("docs/transformations/core_modularization/SCOPE_GRAPH_CLUSTERING_APPROACH.md")


def main() -> int:
    if not PARTS_DIR.exists():
        raise FileNotFoundError(f"Missing parts directory: {PARTS_DIR}")

    part_paths = sorted(PARTS_DIR.glob("*.md"))
    if not part_paths:
        raise FileNotFoundError(f"No Markdown parts found in: {PARTS_DIR}")

    chunks: list[str] = []
    for path in part_paths:
        chunks.append(path.read_text(encoding="utf-8").rstrip())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")

    print(f"Assembled {len(part_paths)} parts into {OUTPUT_PATH.as_posix()}")
    for path in part_paths:
        print(f" - {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
