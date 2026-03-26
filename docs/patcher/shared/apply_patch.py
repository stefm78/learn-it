#!/usr/bin/env python3
"""Canonical patcher entrypoint for Learn-it.

Current status:
- canonical location is `docs/patcher/shared/apply_patch.py`
- execution delegates to the legacy patcher until the v4 patcher is promoted into the repo
"""
from pathlib import Path
import runpy
import sys

legacy = Path(__file__).resolve().parents[2] / "make_constitution" / "apply_learnit_core_patch.py"
if not legacy.exists():
    raise SystemExit(f"Legacy patcher not found: {legacy}")

sys.argv[0] = str(legacy)
runpy.run_path(str(legacy), run_name="__main__")
