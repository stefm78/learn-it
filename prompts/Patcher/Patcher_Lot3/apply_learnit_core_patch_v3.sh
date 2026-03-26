#!/usr/bin/env bash
set -euo pipefail

PATCH_FILE="${1:-./patchset_v3_example.yaml}"
ROOT_PATH="${2:-.}"
WHATIF="${3:-true}"

info()  { printf '[INFO] %s\n' "$1"; }
err()   { printf '[ERR] %s\n' "$1" >&2; }
ok()    { printf '[OK]   %s\n' "$1"; }

if [[ ! -f "$PATCH_FILE" ]]; then
  err "Patch file introuvable: $PATCH_FILE"
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  err "python n'est pas disponible dans le PATH."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/apply_learnit_core_patch_v3.py"

if [[ ! -f "$PY_SCRIPT" ]]; then
  err "Script Python introuvable: $PY_SCRIPT"
  exit 1
fi

info "Interpréteur Python: $(python --version 2>&1)"
info "Exécution du patch v3..."
python "$PY_SCRIPT" "$PATCH_FILE" "$ROOT_PATH" "$WHATIF"
ok "Terminé."
