# Mac Mini Cursor Handoff — Perplexity Inbox Is SSOT for Done Work

**Mac Mini Cursor is one seat.** All seats use `SESSION-START__all-seats__v01__2026-06-25.md` to open a session; this file is the wanmin-specific pickup brief.

**For:** Cursor agent on Mac Mini (wanmin) · **From:** cursor (M5 Cursor — authoring seat) · **Date:** 2026-06-25 · **Tier:** INTUITED

> **Correction (2026-06-26):** Original handoff wrongly targeted M5. Ewan confirmed pickup seat is **Mac Mini (wanmin)**, not Mac-2.lan (M5). This file supersedes `HANDOFF__m5-cursor__shared-inbox-ssot__v01__2026-06-25__cursor.md`.

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

## What M5 Cursor just finished (authoring seat)

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

**Track A is closed for M5 Cursor.** Do not re-implement gather/decision logic.

---

## Mac Mini role — Phase 0 decision pending

**Ewan has not yet decided** (master-plan Phase 0, item 1):

| Option | Meaning |
|---|---|
| **Central sensor hub** | wanmin aggregates M5 + MacAirM4 telemetry, forwards to Vellum — always-on edge per **Pillar 4** prior art |
| **Peer** | All three Macs talk to Beast/Vellum directly; no aggregation layer |

Prior art (`prior-art-syntheses-bundle/estate-security-and-sensors-prior-art-synthesis__*__v01__2026-06-25.md`) favours Mac mini as the **always-on central sensor edge** because M5 and MacAirM4 are portable and may leave Tailnet. Track A `unified_sensor/` is Mac-side gather only — hub vs peer wiring is **not** decided until Ewan answers Phase 0.

**Reach wanmin:** `ssh wanmin` · `ssh wanmin-ts` (Tailscale) · `ssh wanmin-lan` · `ssh wanmin-usb` — machine may be asleep/off; all routes timed out 2026-06-21.

---

## What Mac Mini (wanmin) owns next

Per `docs/UNIFIED-SENSOR-PLAN.md` §Seat ownership and `master-plan__v01__2026-06-25__perplexity.md`:

| Seat (Mac Mini) | Owns | Primary artefact |
|---|---|---|
| **Claude Code** | Phase 2 pipe weld + Phase 3 job-start hook | `pipe-weld-brief__v01__2026-06-25__perplexity.md` · Beast research-pipe |
| **Cascade-Mac** | Track B Phase 1 — `@vellum.witness` on Beast | `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md` |
| **Perplexity** | Read snapshot at job-start; Phase 4 trial | `monitor.py --signals-only` |
| **Devin** | Merge `feat/unified-sensor` + Beast deploy | GitHub PR |
| **Antigravity** | Phase 5 assist (after Phase 4) | master-plan Phase 5 |

**Do not steal Track A.** Mac Mini Cursor may pick up Claude Code seats, pipe weld, or Jun-24 backlog items — but only what your seat owns per the table above.

Priority order: `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`

---

## Session start — run the monitor

From the inbox root (path on wanmin may differ — see below):

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

## Path note (M5 authoring vs Mac Mini pickup)

**Authoring seat:** M5 Cursor (Mac-2.lan / MacAirM5) — wrote Track A and docs on 2026-06-25.  
**Pickup seat:** Mac Mini (wanmin, M4) — stable, always-on, no folder churn.

**Canonical inbox SSOT (architect machine path):**

`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`

**How Mac Mini reaches shared folders:**

| Surface | Path | How wanmin gets it |
|---|---|---|
| Inbox SSOT | `…/ingestion-to-research-pipe/perplexity-inbox/` | Clone/sync repo on wanmin **or** symlink to synced copy — same path preferred |
| Multi-agent bus | `~/amplified-pipeline/` | Seat subfolders (`wanmin/`, `cursor/`, …) + shared `data/` — sync or Tailscale mount |
| Fleet ledger | Vellum HTTPS | `https://vellum.beast.amplifiedpartners.ai` — readable from any Tailnet node |
| Beast ops | SSH `beast` | Tailscale — when Beast is up |

Do **not** fork a second SSOT — one inbox, many readers. Mini stability principle: fixed paths once placed; cross-links symlinked from a central base.

**Fallback ping (if inbox not mounted yet):** `~/amplified-pipeline/wanmin/INBOX-SSOT-PING__2026-06-25.md`

When you finish Mac Mini work, write completion evidence **in perplexity-inbox first**, then mirror a pointer to `~/amplified-pipeline/wanmin/` on your machine.

---

## Vellum witness

Posted by M5 Cursor seat (2026-06-26 correction) — subject **"Mac Mini Cursor — perplexity-inbox SSOT handoff (corrected from M5)"** on Inbox — Ewan sheet. Supersedes erroneous M5-targeted entry from 2026-06-25.

---

## Quick links

| Need | File |
|---|---|
| Done vs open | `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md` |
| Jun-25 threads | `INBOX-INDEX__v02__2026-06-25__cursor.md` |
| Phase 0–7 sequence | `master-plan__v01__2026-06-25__perplexity.md` |
| Ewan hand-back (deduped) | `EWAN-DECISIONS-CONSOLIDATED__v01__2026-06-26.md` |
| Jun-24 backlog | `INBOX-INDEX__v01__2026-06-24__perplexity.md` |

[CLOSURE] branch=ACTION | proxy=none | gates=none | inbox=HANDOFF__mac-mini-cursor__shared-inbox-ssot__v01__2026-06-25__cursor.md | tier=INTUITED
