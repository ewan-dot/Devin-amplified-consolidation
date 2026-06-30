# Hooks — SSOT + runtime

**Install template:** `../../.cursor/hooks.install.json` → copy to `~/.cursor/hooks.json` (paths use `./hooks/` — valid only beside `~/.cursor/hooks/` scripts).

**Project `hooks.json`:** shape-gate `afterFileEdit` only (workspace). Full chain lives in `~/.cursor/hooks.json`.

## sessionStart chain (user harness)

1. `session-start-preamble.sh` — git/task context
2. `session-start.sh` — fleet sensor + VERDICT line
3. `session-start-vellum-intent.py` — nudge: post plan to Vellum before substantive work (`vellum-witness.mdc`)

After posting Vellum intent: `python3 ~/.cursor/hooks/mark-vellum-intent-posted.py <entry_id>` suppresses repeat nudge for 8h.

SSOT scripts: `perplexity-inbox/.cursor/hooks/` — sync to `~/.cursor/hooks/` on change.
