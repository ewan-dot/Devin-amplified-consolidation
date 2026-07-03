# Cursor Config Integrity

Tamper-evident + self-healing guard for the Cursor global config
(`~/.cursor/rules/*.mdc`, `~/.cursor/hooks/*`, `~/.cursor/hooks.json`).

## Honest threat model

This is a **single-user Mac**. Any process running as you (including Cursor
agents, this script, and anything you run) can read and write these files —
and can also edit the manifest or disable the hook. So absolute prevention is
**not achievable in-box**; it needs root / off-box enforcement.

What this gives you instead, achievably and strongly:

- **Tamper-EVIDENT** — every session start recomputes sha256 for all config
  files and compares them to a blessed manifest. Any change/add/remove is
  printed LOUDLY into the agent's startup context and logged.
- **Self-HEALING** — any drifted **rule** whose canonical copy exists in the
  SSOT repo is automatically restored to canonical content.
- **LOCK-GUARDED (rules only)** — `rules/*.mdc` are held under a macOS
  user-immutable (`uchg`) lock. On session start, a rule found unlocked
  (`nouchg`) **or** hash-drifted is treated as a tamper signal: it is
  unlocked, restored from SSOT canonical if content drifted, then re-locked.

It is **not tamper-PROOF**. A same-user attacker who also re-blesses the
manifest, removes the hook, or clears the lock (`chflags nouchg`) can defeat it.

## Files

| Path | What |
|---|---|
| `~/.cursor/integrity/manifest.sha256` | Blessed hashes (local copy) |
| `~/.cursor/integrity/drift.log` | Timestamped drift + heal events |
| `~/.cursor/hooks/verify-config-integrity.py` | Tripwire + self-heal (sessionStart) |
| `~/.cursor/hooks/update-config-manifest.py` | Re-bless after intentional changes |
| `<SSOT repo>/.cursor/integrity/manifest.sha256` | Blessed hashes (repo copy) |

SSOT repo defaults to `~/ingestion-to-research-pipe`; override with the
`CURSOR_SSOT_REPO` env var (keeps everything portable — no hardcoded user path).

## How it runs

`verify-config-integrity.py` is wired into `~/.cursor/hooks.json` under
`sessionStart`. It fails **open** (always exits 0, never blocks or hangs) and
ignores its own `integrity/` directory.

## Re-bless (after intentional edits)

When you deliberately change a rule/hook/hooks.json, regenerate the manifest so
the tripwire stops firing:

```bash
python3 ~/.cursor/hooks/update-config-manifest.py
```

This writes the manifest to both the local and repo integrity dirs. Commit the
repo copy so the blessed state is versioned.

## OS-level immutability lock — ON for RULES, OFF for hooks/harness

**Decision (Ewan, 2026-07-03):** the macOS user-immutable flag (`uchg`) is turned
**ON for `~/.cursor/rules/*.mdc` only** — the constitution. It is **OFF** for
`hooks.json`, `~/.cursor/hooks/*`, harness scripts, and `~/.cursor/integrity/*`,
because the hooks/harness are still under active development and must stay
freely editable.

`uchg` makes a file un-writable/un-deletable — even by the owning user — until
the flag is cleared with `nouchg`. Use the helper, not raw `chflags`:

```bash
~/.cursor/hooks/config-lock.sh status   # show ls -lO flags (look for `uchg`)
~/.cursor/hooks/config-lock.sh lock      # chflags uchg   every rules/*.mdc
~/.cursor/hooks/config-lock.sh unlock    # chflags nouchg every rules/*.mdc
```

### Correct edit cycle for a rule (do NOT edit a locked file directly)

```bash
~/.cursor/hooks/config-lock.sh unlock          # 1. clear the lock
$EDITOR ~/.cursor/rules/<file>.mdc             # 2. edit the rule(s)
python3 ~/.cursor/hooks/update-config-manifest.py   # 3. re-bless the manifest
~/.cursor/hooks/config-lock.sh lock            # 4. re-lock
```

The sessionStart verify hook also **re-applies the lock automatically**: if a
rule is left unlocked it will be re-locked (and restored from SSOT canonical if
its content drifted). So if you unlock, edit, and re-bless but forget step 4,
the next session locks it for you — provided the content matches canonical.

### Honest limits

- Same user can always `config-lock.sh unlock` (or `chflags nouchg`) — this is a
  deliberate speed-bump against accidental/automated edits, **not** a vault.
- `uchg` is **not root-proof** and **not tamper-PROOF**. `schg` (system
  immutable) is stronger but needs root and is intentionally not used here.
- Only `rules/*.mdc` are locked. hooks/harness/integrity stay editable — verify
  reports drift there but never heals or locks them.
