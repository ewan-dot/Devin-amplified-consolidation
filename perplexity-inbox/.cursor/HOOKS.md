# Hooks — SSOT + runtime

**Install:** copy `../../.cursor/hooks.install.json` → `~/.cursor/hooks.json` and sync scripts to `~/.cursor/hooks/`.

## Vellum plan → actual (mandatory)

| When | Hook | Action |
|------|------|--------|
| **Session start** (after sensor) | `session-start-vellum-intent.py` | Post **PLAN** to Vellum before any work |
| After plan posted | `mark-vellum-plan-posted.py <entry_id>` | Clears nudge for 8h |
| **Stop / seat close** | `stop-vellum-actual.py` | Append **ACTUAL** (done, blocked, delta, GitHub push) referencing plan `entry_id` |
| After actual posted | `mark-vellum-actual-posted.py <entry_id>` | Clears stop nudge |

Marker: `~/.amplified/logs/vellum-session.json`

## sessionStart chain

1. `session-start-preamble.sh` — git context  
2. `session-start-read-baton.py` — latest baton (`batons/active/`, max 5)  
3. `session-start.sh` — sensor → **VERDICT=** (paste into plan)  
4. `session-start-vellum-intent.py` — **PLAN before work**

SSOT scripts: `perplexity-inbox/.cursor/hooks/`
