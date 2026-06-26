---
title: Self-Compound — Operating Rule
document_type: operating_rule
artifact_id: OPERATING-RULE__self-compound__v01__2026-06-26__cursor
date_utc: 2026-06-26
author: cursor
reader: ewan
epistemic_tier: INTUITED
---

# Self-compound (plain English)

When an agent fixes a small gap — a hook that missed something, a rule hole, a failure that keeps coming back — **that fix must become fleet property the same session**, not stay in chat.

## What agents must do

1. **Fix it in durable form** — a rule, hook, or inbox doc the whole fleet can find.
2. **Check first** — search inbox and Vellum so we don't pay to research the same gap twice.
3. **Tell the ledger** — one short Vellum line: what closed, where it lives on disk.

## How we know it's working (telemetry)

| Good | Bad |
|---|---|
| New kinds of failure showing up in research **less often** | Same topic researched again with **nothing built** |
| More jobs finishing completely (completion %) | Same hook failing on problems we already encoded |
| Less token spend per finished job | Fixes that only exist in chat |

The stop hook reminds agents if they changed rules or hooks but haven't copied them into the repo SSOT.

## Where it lives

- Rule: `~/.cursor/rules/self-compound.mdc` (always on)
- Stop check: `stop-self-compound-check.py` (runs when a seat ends)
- Detail: doors-telemetry doc §7, harness manifest

[CLOSURE] branch=IMPLEMENT | proxy=none | gates=self-compound harness v01 | inbox=OPERATING-RULE__self-compound__v01__2026-06-26__cursor.md | tier=INTUITED
