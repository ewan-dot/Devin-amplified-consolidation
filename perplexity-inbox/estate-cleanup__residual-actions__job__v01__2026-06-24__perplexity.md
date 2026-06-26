---
title: M5 Estate Cleanup — Residual Actions From Wipe/Sweep/Dedup Thread
origin: perplexity
author: AI_PARTNER_PROXY (logged proxy; Ewan ratifies)
created_utc: 2026-06-24T17:09Z
device: macairm5
tier: MEASURED (all paths/states read live off macairm5 this thread)
provenance: pc bash on macairm5 + gh on Amplified-Partners
status: ready-to-implement; one Tier-C gate (deletes) flagged for ratification
---

# Residual Actions — M5 Estate Cleanup

Context: home dir was swept into `~/ingestion-to-research-pipe/` (rsync, sources still present),
then deduped (Phase A applied, log written, zero quarantine). These are the leftovers.

**IMPORTANT — verify before acting.** Several of these may already be done by
Antigravity/Devin/Cascade (see `perplexity-inbox/completed-by-*` folders). Each item
below carries a CHECK. If the CHECK shows already-done, skip and mark complete. Do NOT redo.

## ACT (reversible — implement directly)

1. **Re-stage the dedup scripts** (swept off `~/`):
   CHECK: `ls ~/dedup_scan.py ~/dedup_apply.py` — if both present, DONE, skip.
   - `cp "$R/code/dedup_scan.py" ~/ 2>/dev/null || find "$R" -name dedup_scan.py`
   - same for `dedup_apply.py`. They were moved into the pond by the sweep.

2. **Re-run dedup over the post-sweep tree** (home content landed after first scan; 307k scanned of 514k — `Library` etc. excluded by design):
   - `cd $R && python3 ~/dedup_scan.py $R` then review `_DEDUP-MANIFEST.json`
   - `python3 ~/dedup_apply.py $R --apply` (YAML-aware, quarantines divergent).

   CHECK: compare `_DEDUP-MANIFEST.json` mtime vs latest sweep; if newer, DONE.

3. **Repoint or disable the orphaned watcher**
   CHECK: `ls ~/Library/LaunchAgents | grep -i nightly` — if none, already removed, DONE. — `cmd-watcher` launchd fires every interval
   looking for `~/amplified-nightly/cmd-watcher.py` which now lives at
   `$R/amplified-nightly/`. Either fix the plist path under `~/Library/LaunchAgents`
   or `launchctl bootout` it. Currently erroring on every tick (harmless but noisy).

## GATE — needs Ewan (Tier C: deletes of non-workspace-reproducible data)

4. **Delete stale duplicate dirs** (verified redundant this thread, but deletion is irreversible):
   CHECK each path exists before deleting; if GONE, DONE.
   - `$R/Amplified:Paerplexity` — colon-named fat-finger; partial stale copy of
     `Clone Github/corpus-raw` MINUS 5 files (AGENTS.md, AMPLIFIED.md, OPEN_FIRST.md,
     RESEARCH_PIPE_CONVENTIONS.md, RESEARCH_PIPE_SPEC.md). The good copy supersedes it.
   - `$R/Cursor/Full sweep of M5/intake/home/clean-build` — DEAD carcass, no `.git`,
     flat copy of the live hub. Misleads any agent that opens it.

## DECISION — needs Ewan (not automatable: real divergent git history)

5. **Pick canonical `clean-build`.** CHECK: count copies still present; if <3, partially resolved. Three LIVE divergent copies:
   - `$R/clean-build` — branch `cascade/temporal-job-harness…` HEAD fe3b71b, 8 worktrees (the live hub)
   - `$R/Projects/clean-build` — `main` HEAD 593fcc5
   - `$R/Clone Github/clean-build` — `main` HEAD bb17fb7
   Two different `main`s. Decide canonical, point research-pipe ingest at ONE, exclude the rest.

6. **Confirm 5 worktree branches are pushed** to `fleet-clean-build` (were local-only):
   void-zenith-rises-09h13, antigravity/cman-data-prep, feat/scout-v2,
   feat/programme-agent-native-audit, perplexity/seat.
   - `for b in <list>; do gh api repos/Amplified-Partners/fleet-clean-build/branches/$b --jq .name; done`
   - Any "Not Found" → `git -C <worktree> push origin HEAD`.

`$R` = `/Users/ewansair/ingestion-to-research-pipe`
