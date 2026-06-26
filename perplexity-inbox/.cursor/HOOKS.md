# Hooks — SSOT + runtime

**Repo SSOT:** `../../.cursor/hooks.json` (constitutional + session chain). Live install: `~/.cursor/hooks.json`. Key hook scripts mirrored under `hooks/` (e.g. `before-submit-constitutional.py`, `stop-self-compound-check.py`).

Do not re-register hooks here — empty `hooks.json` avoids double-firing sessionStart in this workspace.
