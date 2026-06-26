---
title: Skill Bug — amplified-standing-grants mis-tiers the inbox write
origin: perplexity
author: AI_PARTNER_PROXY (logged proxy; Ewan ratifies)
created_utc: 2026-06-24T19:00Z
tier: MEASURED (observed live: inbox push triggered confirm/deny twice this thread)
status: contradiction logged — needs skill edit
---

# Contradiction: inbox write is Tier B, not Tier A

`amplified-standing-grants` states the endpoint write to
`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/` is **Tier A**
("a reversible drop into Ewan's own sandboxed workspace... Do it freely").

**Observed behaviour (this thread, 2x):** `pc push` to the inbox triggers a
platform confirmation and was denied. A cross-boundary write to the Mac is
**gated** — it behaves as **Tier B** (proxy-sign + platform confirm), not Tier A.

## Fix
Edit the skill so the inbox write is classified **Tier B**: proxy-sign and
proceed, but expect/honour the platform confirm step (irreversible-external
rule still applies to writes that leave the Perplexity sandbox onto the Mac).
Either reclassify, or add a line: "the inbox write surfaces a platform confirm;
that confirm is the single gate, not a closure failure."

## Why it matters
Mis-tiering the endpoint makes closure look like a failure when the push is
denied, and tempts the agent to treat a gated act as free. Min-rule: the
skill claimed Tier A on a Tier-B act — a tier launder in the doctrine itself.
