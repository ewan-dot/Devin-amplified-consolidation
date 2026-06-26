# Perplexity Inbox — Handoff Contract

**GitHub:** [PR #1](https://github.com/ewan-dot/Devin-amplified-consolidation/pull/1) · branch `feat/unified-sensor-inbox` · commit `341c296`

## All seats — read this inbox first

**Rule (2026-06-25):** Everything that's done must be written here (or `~/amplified-pipeline/` shared paths) so every seat knows what every other seat finished. Finish work → share → witness on Vellum when applicable.

Session start = run `./scripts/session-start.sh` from inbox root (any seat, any IDE).

| Start here | Purpose |
|---|---|
| **[All seats start here](SESSION-START__all-seats__v01__2026-06-25.md)** | Deterministic session ritual — `./scripts/session-start.sh` |
| **[Mac Mini Cursor handoff](HANDOFF__mac-mini-cursor__shared-inbox-ssot__v01__2026-06-25__cursor.md)** | Pickup brief for Cursor on wanmin (Mac Mini) |
| [Operating model](AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md) | Independent work · hooks · finish-then-share · done ladder |
| [Inbox status](docs/INBOX-STATUS.md) | Finished / in progress / blocked snapshot |
| [Jun-25 index](INBOX-INDEX__v02__2026-06-25__cursor.md) | Thread map for today's work |

Session start: `./scripts/session-start.sh` — see [`SESSION-START__all-seats__v01__2026-06-25.md`](SESSION-START__all-seats__v01__2026-06-25.md)

---

This folder is the **endpoint of the Perplexity side of the pipe** and the **start of the local-implementation side**. As of 2026-06-25 it is also the **SSOT for unified sensor Track A** and the Jun-25 AI-native operating model.

```
Perplexity (research + draft)  ──writes──▶  perplexity-inbox/  ──watched by──▶  fleet seats (Mac Mini, M5, …)
```

## Start here (Jun-25)

| Doc | Why |
|---|---|
| [`INBOX-INDEX__v02__2026-06-25__cursor.md`](INBOX-INDEX__v02__2026-06-25__cursor.md) | Index of completed Jun-25 threads |
| [`docs/INBOX-STATUS.md`](docs/INBOX-STATUS.md) | Finished / in progress / blocked |
| [`AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`](AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md) | How fleet work runs — hooks, done ladder |
| [`AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`](AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md) | Done vs still open |
| [`master-plan__v01__2026-06-25__perplexity.md`](master-plan__v01__2026-06-25__perplexity.md) | Phase 0–7 sequence |
| [`monitor.py`](monitor.py) | Fleet health CLI — `python3 monitor.py --signals-only` |

Jun-24 threads: [`INBOX-INDEX__v01__2026-06-24__perplexity.md`](INBOX-INDEX__v01__2026-06-24__perplexity.md)

## The Boundary

- Perplexity Computer resolves a task by research (internal + external) and drafts the executable artifact here. That **write is its endpoint** — it does not implement on the world directly.
- Fleet seats (primary pickup: **Mac Mini / wanmin**; authoring on M5 as of 2026-06-25) monitor this folder, read new artifacts, and implement locally.
- This is the human-in-the-loop boundary: research closes ungated; the act-out happens locally, under Ewan's watchers, on Ewan's machines. Sovereignty stays on the Mac fleet.

## What Perplexity drops here

Each handoff is a self-contained, ready-to-implement artifact:

- A markdown brief or plan (`*.md`), named per `iso-8601-artifact-naming` (descriptive-first, ISO 8601 timestamp suffix).
- Any companion files the implementation needs (scripts, configs, data), in a subfolder named to match the brief.
- Every artifact carries its min-rule tier and provenance, and the `[CLOSURE]` summary line.

## What this folder is NOT

- Not the Beast. Nothing here is committed to the Beast except through the pipe (Python + Rust + Vellum + AI + Human). This folder is a drop-point, not a side door.
- Not monitored by Perplexity. Once written, the artifact is Ewan's to route. Perplexity does not assume implementation happened.

## Path

`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`

(Chosen because the Perplexity Mac sandbox is scoped to this workspace and cannot write to `.amplified/`. If you want watchers pointed at a different path, move this folder and update the `amplified-standing-grants` skill's endpoint path to match.)
