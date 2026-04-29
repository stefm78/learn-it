from __future__ import annotations

import re
from pathlib import Path


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def discover_pipelines_from_registry(registry_path: Path) -> list[dict[str, str]]:
    text = load_text(registry_path)
    lines = text.splitlines()
    pipelines: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if current:
                pipelines.append(current)
            current = {"pipeline_id": stripped[4:].strip()}
            continue
        if current and stripped.startswith("- Path:"):
            match = re.search(r"`([^`]+)`", stripped)
            if match:
                current["path"] = match.group(1)
        if current and stripped.startswith("- Canonical state:"):
            match = re.search(r"`([^`]+)`", stripped)
            if match:
                current["canonical_state"] = match.group(1)
        if current and stripped.startswith("- Goal:"):
            current["goal"] = stripped[len("- Goal:"):].strip()
    if current:
        pipelines.append(current)
    return pipelines

# Backward-compatible public name used by overlay.py and validators.
def discover_pipelines(registry_path: Path) -> list[dict[str, str]]:
    return discover_pipelines_from_registry(registry_path)

