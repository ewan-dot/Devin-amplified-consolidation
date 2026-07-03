# Open-Door Harness — ACTIVATION (Phase 0 → live)

**Current state: STAGED. Nothing here is wired.** The live `~/.cursor/hooks.json`
is untouched. Zero door-deny enforcement is active. Reading or running any file
in this directory has no effect on a Cursor session. Activation is a deliberate,
reversible, staged sequence **you (Ewan) run** — described exactly below.

Design source of truth: `../SSOT__open-door-harness__v01__2026-07-03__cursor.md`
(§6 phased wiring, §7 ratified defaults). Manifest: `../config/doors-v1.json`.
Marker: `~/.amplified/active-door.json`.

---

## What is in this directory

| File | Role | Wired? |
|---|---|---|
| `door_enforcement.py` | Pure `decide(action, door, manifest) -> allow/nudge/deny` + 27 self-tests | no |
| `hook_adapter.py` | Cursor-hook adapter (stdin JSON → permission JSON). Fail-open. Mode-aware. | no |
| `hooks/before-shell-execution.door.sh` | Staged wrapper: door check → existing token-bomb guard | no |
| `hooks/before-read-file.door.sh` | Staged wrapper: door check → existing noisy-path nudge | no |
| `active-door.example.json` | Reproducible template of the live marker | n/a |

**The knob:** mode is read from env `OPEN_DOOR_MODE`, else the file
`~/.amplified/open-door-mode`, else `scaffold`. Modes:
`scaffold` (advisory allow — zero behaviour change) → `nudge` (message, still allow)
→ `deny` (hard block, enforcing doors only). Door-independent hard lines
(secrets, Red-core destroy/launder, git push on Mac) deny in **every** mode.

---

## Pre-flight (safe — run anytime, changes nothing)

```bash
cd ~/ingestion-to-research-pipe/perplexity-inbox/open_door_runtime   # path after merge to main
python3 door_enforcement.py            # expect: ALL PASS (27/27)
echo '{"command":"git push origin main"}' | OPEN_DOOR_MODE=scaffold python3 hook_adapter.py shell   # expect deny (universal)
echo '{"path":"/etc/hosts"}'            | OPEN_DOOR_MODE=nudge   python3 hook_adapter.py read        # expect allow + nudge
```

---

## THE ONE ACTIVATION STEP (staged wiring — run once)

This copies the two staged wrappers over the two live hook dispatchers, keeping
timestamped backups. It leaves mode at **scaffold**, so **behaviour does not
change** — the door adapter only logs and (already-true) universal denies apply.

```bash
export OPEN_DOOR_HOME="$HOME/ingestion-to-research-pipe/perplexity-inbox/open_door_runtime"

# backup live dispatchers
cp ~/.cursor/hooks/before-shell-execution.sh ~/.cursor/hooks/before-shell-execution.sh.pre-door.bak
cp ~/.cursor/hooks/before-read-file.sh       ~/.cursor/hooks/before-read-file.orig.sh   # wrapper chains to this

# wire the wrappers (hooks are editable; NO config-lock unlock needed — only rules/*.mdc are locked)
cp "$OPEN_DOOR_HOME/hooks/before-shell-execution.door.sh" ~/.cursor/hooks/before-shell-execution.sh
cp "$OPEN_DOOR_HOME/hooks/before-read-file.door.sh"       ~/.cursor/hooks/before-read-file.sh
chmod +x ~/.cursor/hooks/before-shell-execution.sh ~/.cursor/hooks/before-read-file.sh
```

`hooks.json` itself is **not edited** — the entries already point at those two
`.sh` filenames. `OPEN_DOOR_HOME` must be visible to the hook process; if Cursor
does not inherit your shell env, hardcode the path in the two wrappers instead.

### Then progress the wall one knob at a time (no re-copy, no restart)

```bash
echo nudge > ~/.amplified/open-door-mode     # Phase 2: measure false-block rate in ~/.amplified/logs/harness-hooks.jsonl
# when the nudge log looks clean:
echo deny  > ~/.amplified/open-door-mode      # Phase 3: hard-deny, cheapest doors first
export OPEN_DOOR_ENFORCING="research_read,config_harness"   # SSOT §7 D3 — these two first; others still nudge
```

Removing the mode file returns to `scaffold` instantly.

---

## Rollback (full revert to pre-door behaviour)

```bash
rm -f ~/.amplified/open-door-mode
cp ~/.cursor/hooks/before-shell-execution.sh.pre-door.bak ~/.cursor/hooks/before-shell-execution.sh
cp ~/.cursor/hooks/before-read-file.orig.sh              ~/.cursor/hooks/before-read-file.sh
```

---

## Honest limitations (radical transparency)

1. **No write-boundary hook.** The live hook set is `beforeReadFile` +
   `beforeShellExecution` — there is no file-write hook. So `fs_write` **scoping**
   is enforced by `decide()` but not reachable from hooks except for shell-mediated
   writes, which Phase 0 does **not** parse (only Red-core + `git push` are caught in
   shell). `decide()` is ready for a write-boundary hook the day one exists.
2. **Mac has no L2 wall.** This is L1 hook-deny only — INTUITED policy, not a kernel
   boundary (SSOT §3 C-3). Do not overclaim "one door at a time" as STRUCTURED on Mac.
3. **Path globs are first-pass** (INTUITED), to be refined from Phase-2 nudge
   telemetry before flipping to deny.
4. **Placeholder doors** (`worktree_feature`, `agentsmini_build`, `pipe_run`) need
   their subtree bound in the marker (e.g. `"worktree_subtree": "/abs/path"`) for
   scoping to resolve; unbound → those globs are skipped.
