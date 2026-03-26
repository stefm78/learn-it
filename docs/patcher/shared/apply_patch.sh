#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="${PYTHON_CMD:-python}"

exec "$PYTHON_CMD" "$SCRIPT_DIR/apply_patch.py" "$@"
