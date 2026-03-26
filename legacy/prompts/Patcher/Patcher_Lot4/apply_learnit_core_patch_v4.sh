#!/usr/bin/env bash
set -euo pipefail

PATCH_FILE="${1:-./patchset_v4.yaml}"
ROOT_PATH="${2:-.}"
WHATIF="${3:-true}"
REPORT_PATH="${4:-}"

info()  { printf '[INFO] %s\n' "$1"; }
ok()    { printf '[OK]   %s\n' "$1"; }
warn()  { printf '[WARN] %s\n' "$1"; }
err()   { printf '[ERR]  %s\n' "$1" >&2; }

if [[ ! -f "$PATCH_FILE" ]]; then
  err "Patch file introuvable: $PATCH_FILE"
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  err "python n'est pas disponible dans le PATH."
  exit 1
fi

info "Interpréteur Python: $(python --version 2>&1)"

if ! python -m pip --version >/dev/null 2>&1; then
  err "pip n'est pas disponible via python -m pip"
  exit 1
fi

if ! python -c "import yaml" >/dev/null 2>&1; then
  warn "PyYAML absent. Installation..."
  python -m pip install pyyaml
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/apply_learnit_core_patch_v4.py"

if [[ ! -f "$PY_SCRIPT" ]]; then
  err "Script Python introuvable: $PY_SCRIPT"
  exit 1
fi

info "Validation patchset..."
python "$SCRIPT_DIR/validate_patchset_v4.py" "$PATCH_FILE"

info "Exécution du patch..."
if [[ -n "$REPORT_PATH" ]]; then
  python "$PY_SCRIPT" "$PATCH_FILE" "$ROOT_PATH" "$WHATIF" "$REPORT_PATH"
else
  python "$PY_SCRIPT" "$PATCH_FILE" "$ROOT_PATH" "$WHATIF"
fi

ok "Terminé."
