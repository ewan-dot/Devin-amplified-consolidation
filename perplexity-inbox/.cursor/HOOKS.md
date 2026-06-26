# Hooks — SSOT + runtime

**Install template:** `../../.cursor/hooks.install.json` → copy to `~/.cursor/hooks.json` (paths use `./hooks/` — valid only beside `~/.cursor/hooks/` scripts).

**Project `hooks.json`:** must stay **empty** (`{"version":1,"hooks":{}}`). Active project hooks with `./hooks/` paths block submit — scripts live in `.cursor/hooks/`, not `./hooks/`. User harness at `~/.cursor/hooks.json` is the live chain.

Do not re-register hooks here — empty `hooks.json` avoids double-firing sessionStart in this workspace.
