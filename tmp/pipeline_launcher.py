#!/usr/bin/env python3
"""Compatibility wrapper for the official pipeline launcher.

The human-facing launcher now lives at:
  python docs/patcher/shared/pipeline_launcher/cli.py

This tmp path is kept only for temporary backward compatibility.
"""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
