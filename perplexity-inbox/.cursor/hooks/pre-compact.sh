#!/usr/bin/env bash
# preCompact — preserve task context before compaction strips it
set -euo pipefail
INPUT=$(cat)

BACKUP_DIR="${HOME}/.cursor/compact-backups"
mkdir -p "$BACKUP_DIR"
TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)

echo "$INPUT" >"$BACKUP_DIR/$TS-trigger.json"

for TASK_FILE in ".cursor/CURRENT_TASK" "${HOME}/.cursor/CURRENT_TASK"; do
  if [[ -f "$TASK_FILE" ]]; then
    cp "$TASK_FILE" "$BACKUP_DIR/$TS-task.md"
    break
  fi
done

echo '{}'
exit 0
