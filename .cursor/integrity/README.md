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

It is **not tamper-PROOF**. A same-user attacker who also re-blesses the
manifest (or removes the hook) can defeat it. See "Optional stronger lock".

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

## Optional stronger lock (OS-level immutability) — LEFT OFF

macOS user-immutable flag (`uchg`) makes a file un-writable/un-deletable even
by you, until the flag is cleared. This is the strongest same-machine lock, but
it **interferes with the `self-compound` auto-sync workflow** (agents can no
longer update rules/hooks without first clearing the flag), so it is
deliberately **NOT applied**. Ewan must decide.

To turn it ON (example — locks all rules and hooks.json):

```bash
chflags uchg ~/.cursor/rules/*.mdc ~/.cursor/hooks.json
# stronger, requires root, survives more: chflags schg (system immutable)
```

To turn it OFF again (required before any legit edit / re-bless):

```bash
chflags nouchg ~/.cursor/rules/*.mdc ~/.cursor/hooks.json
```

Trade-off: `uchg` ON = real write-prevention on this machine, but every
intentional edit and every self-compound sync must first `nouchg`, edit,
re-bless, then `uchg` again. That friction is why it is off by default.
