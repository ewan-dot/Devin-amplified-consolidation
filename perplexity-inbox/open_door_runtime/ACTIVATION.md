# Open-Door Harness — ACTIVATION (Phase 0 → live)

**Current state: STAGED. Nothing here is wired.** The live `~/.cursor/hooks.json`
is untouched. Zero door-deny enforcement is active. Reading or running any file
in this directory has no effect on a Cursor session. Activation is a deliberate,
reversible, staged sequence **you (Ewan) run** — described exactly below.

Design source of truth: `../SSOT__open-door-harness__v01__2026-07-03__cursor.md`
(§6 phased wiring, §7 ratified defaults). Manifest: `../config/doors-v1.json`.
Marker: `~/.amplified/active-door.json`.

---

## The model (Phase 1): a door is a PRESET, not a shell wall

Per `RESEARCH__cursor-heavyuser-harness-guidance__v01` (R1–R3), a door is a **preset of Cursor's
own enforced surfaces**. The macOS **Seatbelt sandbox** (`sandbox.json`, Cursor v2.0+) does the
walling — workspace-scoped FS, default-deny network, `.cursorignore` reads, backed by External-File
and File-Deletion Protection. **"Door enter" = swap the door's two preset files into `~/.cursor/`.**
The shell hook shrinks to **nudge/telemetry + a fail-closed hard-deny core** (Red core + `git push`).

## What is in this directory

| File | Role | Wired? |
|---|---|---|
| `presets/<door>/permissions.json` | Per-door `terminalAllowlist` + `autoRun` steering (6 doors) | no |
| `presets/<door>/sandbox.json` | Per-door Seatbelt scope: `type`, writable paths, `networkPolicy` | no |
| `presets/_base/cursorignore` | Base `.cursorignore` — the **reliable read boundary** (secrets/noise) | no |
| `presets/README.md` | Preset-swap model, net_mesh→networkPolicy map, placeholder-binding contract | n/a |
| `hooks-failclosed.snippet.json` | Exact `hooks.json` per-script config with `"failClosed": true` | no |
| `door_enforcement.py` | Pure `decide(action, door, manifest) -> allow/nudge/deny` + self-tests | no |
| `hook_adapter.py` | Cursor-hook adapter. **Fail-CLOSED hard-deny core** (secrets/push/Red) + fail-open door-scope. Mode-aware. | no |
| `hooks/before-shell-execution.door.sh` | Staged wrapper: door check → existing token-bomb guard | no |
| `hooks/before-read-file.door.sh` | Staged wrapper: door **nudge** → existing noisy-path nudge | no |
| `active-door.example.json` | Reproducible template of the live marker | n/a |

**The knob:** mode is read from env `OPEN_DOOR_MODE`, else the file
`~/.amplified/open-door-mode`, else `scaffold`. Modes:
`scaffold` (advisory allow — zero behaviour change) → `nudge` (message, still allow)
→ `deny` (hard block, enforcing doors only). Door-independent hard lines
(secrets, Red-core destroy/launder, git push on Mac) deny in **every** mode, **fail-closed**.

## Door enter = swap the preset pair in (staged; nothing auto-applied)

```bash
DOOR=research_read      # one of: research_read agentsmini_build central_handoff worktree_feature pipe_run config_harness
OPEN_DOOR_HOME="$HOME/ingestion-to-research-pipe/perplexity-inbox/open_door_runtime"   # path after merge to main

# substitute placeholders (__PROJECT_SUBTREE__ / __WORKTREE_SUBTREE__ / __PIPE_RUN_DIR__ / __CORPUS_DIR__)
# from the active-door marker, DROP any unbound placeholder, then copy in:
cp "$OPEN_DOOR_HOME/presets/$DOOR/permissions.json" ~/.cursor/permissions.json
cp "$OPEN_DOOR_HOME/presets/$DOOR/sandbox.json"     ~/.cursor/sandbox.json
# read boundary (once): cp "$OPEN_DOOR_HOME/presets/_base/cursorignore" <workspace>/.cursorignore
# write the marker: {door, entered, task, seat, <bindings>} -> ~/.amplified/active-door.json
```

A `door` CLI (Phase-1 presentation layer, to be added) does the substitution + marker write. Swapping
`sandbox.json` takes effect for **new** sandboxed commands; it cannot retroactively widen a running one.
`permissions.json`/`sandbox.json` only bite when a **Run Mode** is enabled (Auto-review recommended).

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

`hooks.json` entries already point at those two `.sh` filenames, so the wiring copy
does not need to touch `hooks.json` — **except** to add the fail-closed flag on the
shell hook. Set `"failClosed": true` on the `beforeShellExecution` entry (see
`hooks-failclosed.snippet.json` for the exact fragment): without it, hooks are
**fail-open**, so a script crash/timeout/bad-JSON would let `git push` / secrets /
Red-core through. Leave `beforeReadFile` **without** `failClosed` on purpose — it is
nudge-only; the read boundary is `.cursorignore`, not that hook. `OPEN_DOOR_HOME` must
be visible to the hook process; if Cursor does not inherit your shell env, hardcode the
path in the two wrappers instead.

Defence in depth: the hard-deny core is fail-closed **twice** — the adapter denies if
its own core probe errors on a shell/MCP call, **and** `hooks.json` `failClosed:true`
denies if the wrapper never returns valid JSON.

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

1. **Write boundary now rides the sandbox, not a hook.** There is no `beforeWriteFile`
   hook, so `fs_write` scoping is enforced by the door's **`sandbox.json`**
   (`type` + `additionalReadwritePaths`) + **External-File Protection** — the STRUCTURED
   L2 wall. `decide()`/the shell hook only catch shell-mediated Red-core + `git push`.
   `central_handoff` must list `~/amplified-pipeline` + `perplexity-inbox` in
   `additionalReadwritePaths` or External-File Protection will prompt on every shared write.
2. **Mac DOES have an L2 wall (C-3 revised).** Cursor v2.0+ ships a macOS **Seatbelt**
   sandbox + External-File/File-Deletion Protection, so the per-door blast radius is
   **STRUCTURED on Mac**, expressed as the `sandbox.json` preset. Hooks are the
   **complement** (door-awareness + fail-closed hard-deny core), not the sole wall.
   What stays INTUITED: hooks are fail-open unless `failClosed:true`, and `beforeReadFile`
   deny is unreliable (read wall → `.cursorignore`).
3. **`permissions.json`/`sandbox.json` only bite with a Run Mode enabled** and are **not**
   security boundaries themselves (the Seatbelt sandbox + Protections are). Team-dashboard
   config overrides user+project files.
4. **Mac-desktop-only.** User hooks + `sessionStart`/`beforeSubmitPrompt`/`stop`/MCP hooks
   **do not fire in cloud agents**; Cloud Agents don't use Run Modes. Estate/Beast/teammate
   reach needs the presets + enforceable hooks committed at **project** `<repo>/.cursor/`
   (SSOT §3a). Phase 1 stages them so either home can adopt without redesign.
5. **Path globs / allowlists are first-pass** (INTUITED), to be refined from Phase-2 nudge
   telemetry before flipping to deny.
6. **Placeholder doors** (`worktree_feature`, `agentsmini_build`, `pipe_run`) need their
   subtree bound in the marker (e.g. `"worktree_subtree": "/abs/path"`) for scoping to
   resolve; unbound `__…__` tokens are **dropped** at enter (never left literal).
