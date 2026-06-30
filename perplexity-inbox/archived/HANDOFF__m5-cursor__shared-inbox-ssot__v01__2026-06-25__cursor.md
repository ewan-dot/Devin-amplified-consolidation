# M5 Cursor Handoff — Perplexity Inbox Is SSOT for Done Work

**For:** Cursor agent on Mac-2.lan (M5) · **From:** cursor (architect Mac) · **Date:** 2026-06-25 · **Tier:** INTUITED

---

## Ewan's rule (read this first)

> Everything that's done (for now) must be written in **perplexity-inbox** so everybody knows what everybody else is doing.

**Operating model:** Independent IDE work → hooks/harnesses keep seats aligned → **finish, then share**. Shared path or Vellum witness = **minimum done**. **Working** (tested, runs) = **target**.

Full plain-language version: `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`

---

## Read first (in order)

1. `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` — how fleet work flows
2. `docs/INBOX-STATUS.md` — what's finished / in progress / blocked right now
3. `README.md` — inbox boundary and path
4. This file — your pickup brief

Then scan: `INBOX-INDEX__v02__2026-06-25__cursor.md` · `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`

---

## The rule for every seat

When you **finish** work (or reach a meaningful checkpoint):

1. **Write it here** — spec, summary, or `completed-by-<seat>__YYYY-MM-DD/` folder in `perplexity-inbox/`
2. **Or** promote to `~/amplified-pipeline/` shared paths (seat subfolder + shared `data/`)
3. **Witness on Vellum** when the job warrants fleet visibility (INTUITED tier for AI-authored rows)
4. **Do not** leave done work only in a local worktree or IDE session

Shared is the **floor**. Working + tested is the **goal**.

---

## What Cursor (architect Mac) just finished

**Track A — unified sensor (Mac gather).** Working, tested, on disk.

| What | Where |
|---|---|
| Completion summary | `completed-by-cursor__2026-06-25/SUMMARY__unified-sensor-track-a__2026-06-25__cursor.md` |
| Python module | `unified_sensor/` (7 files) |
| CLI | `monitor.py` |
| Tests | `tests/test_unified_sensor.py` (6 green) |
| Last snapshot | `data/sensor_snapshot.json` |
| Plan + seat table | `docs/UNIFIED-SENSOR-PLAN.md` |
| Jun-25 index | `INBOX-INDEX__v02__2026-06-25__cursor.md` |
| Tarballs extracted | `signal-reading-bundle/`, `prior-art-syntheses-bundle/` |
| Worktree (not merged) | `/Users/ewansair/ingestion-to-research-pipe/.worktrees/feat-unified-sensor` → `feat/unified-sensor` |

**Track A is closed for Cursor.** Do not re-implement gather/decision logic.

---

## What M5 owns next

Per `docs/UNIFIED-SENSOR-PLAN.md` §Seat ownership and `master-plan__v01__2026-06-25__perplexity.md`:

| Seat (M5) | Owns | Primary artefact |
|---|---|---|
| **Claude Code** | Phase 2 pipe weld + Phase 3 job-start hook | `pipe-weld-brief__v01__2026-06-25__perplexity.md` · Beast research-pipe |
| **Cascade-Mac** | Track B Phase 1 — `@vellum.witness` on Beast | `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md` |
| **Perplexity** | Read snapshot at job-start; Phase 4 trial | `monitor.py --signals-only` |
| **Devin** | Merge `feat/unified-sensor` + Beast deploy | GitHub PR |
| **Antigravity** | Phase 5 assist (after Phase 4) | master-plan Phase 5 |

**Do not steal Track A.** M5 Cursor may pick up Claude Code seats, pipe weld, or Jun-24 backlog items — but only what your seat owns per the table above.

Priority order: `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`

---

## Session start — run the monitor

From the inbox root:

```bash
cd /Users/ewansair/ingestion-to-research-pipe/perplexity-inbox
python3 monitor.py --signals-only
```

Exit codes: `0` proceed · `1` warn · `2` halt.

Also useful:

```bash
python3 monitor.py              # full collect + terminal summary
python3 monitor.py --no-collect --signals-only   # read last snapshot only
python3 -m pytest tests/test_unified_sensor.py -q
```

---

## Path note (architect Mac vs M5)

**Canonical inbox on architect Mac:**

`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`

If M5 path differs:

- Symlink to the above if this repo is synced/cloned on Mac-2.lan
- Or read via Tailscale/shared sync if the ingestion repo lives elsewhere on M5
- Do **not** fork a second SSOT — one inbox, many readers

**Cross-seat bus:** `~/amplified-pipeline/` (seat subfolders e.g. `cursor/`, shared `data/`). On architect Mac, `~/amplified-pipeline/cursor/` does not exist yet — **perplexity-inbox is the live SSOT** until that folder is created.

When you finish M5 work, write completion evidence **here first**, then mirror a pointer to `~/amplified-pipeline/cursor/` if that folder exists on your machine.

---

## Vellum witness

Posted by architect Mac cursor seat — see fleet bus entry subject **"M5 Cursor — perplexity-inbox is SSOT for done work"** (2026-06-25).

---

## Quick links

| Need | File |
|---|---|
| Done vs open | `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md` |
| Jun-25 threads | `INBOX-INDEX__v02__2026-06-25__cursor.md` |
| Phase 0–7 sequence | `master-plan__v01__2026-06-25__perplexity.md` |
| Ewan hand-back (deduped) | `EWAN-DECISIONS-CONSOLIDATED__v01__2026-06-26.md` |
| Jun-24 backlog | `INBOX-INDEX__v01__2026-06-24__perplexity.md` |

[CLOSURE] branch=ACTION | proxy=none | gates=none | inbox=HANDOFF__m5-cursor__shared-inbox-ssot__v01__2026-06-25__cursor.md | tier=INTUITED
