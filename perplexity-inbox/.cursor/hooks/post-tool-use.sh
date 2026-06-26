#!/usr/bin/env bash
# postToolUse — cap noisy Shell/Read/MCP output
set -euo pipefail
exec python3 "$(dirname "$0")/post-tool-redact.py"
