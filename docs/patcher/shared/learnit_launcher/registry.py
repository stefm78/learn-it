from __future__ import annotations

from pathlib import Path
from typing import Any


def discover_pipelines(registry_path: Path) -> list[dict[str, Any]]:
    if not registry_path.exists():
        raise FileNotFoundError(f"Missing pipeline registry: {registry_path}")

    pipelines: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in registry_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped.startswith("### "):
            if current and str(current.get("path", "")).startswith("docs/pipelines/"):
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

        if current and stripped.startswith("- Goal:"):
            current["goal"] = stripped[len("- Goal:"):].strip()

    if current and str(current.get("path", "")).startswith("docs/pipelines/"):
        pipelines.append(current)

    return pipelines
