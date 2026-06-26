#!/usr/bin/env bash
# beforeShellExecution — token-bomb guard (Cursor-native)
set -euo pipefail
exec python3 "$(dirname "$0")/pre-bash-guard.py"
