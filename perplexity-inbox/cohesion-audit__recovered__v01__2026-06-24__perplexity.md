---
artifact: cohesion-audit
version: v01
date: 2026-06-24
origin: perplexity
recovered_from: pplx://sessions/10165011-e903-4229-8d8f-827c98032add
recovered_at: 2026-06-24T18:50Z
recovery_reason: |
  Original session 10165011 (2026-06-24 15:27 UTC) attempted to push this audit
  to the Mac inbox and looped on push retries five times before halting. The
  content was rendered in-thread but never landed in the inbox. This is the
  recovered verbatim text from the session transcript, lifted into the
  perplexity-inbox under the v1.3 standing-grants rule (Tier B, one push,
  no retries on failure).
tier: STRUCTURED
provenance:
  - session transcript pplx://sessions/10165011-e903-4229-8d8f-827c98032add (verbatim)
  - inbox state /Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/ at 2026-06-24T18:50Z
---

# Cohesion Audit — Inbox State After Antigravity Run

**Recovered from thread `10165011` (2026-06-24 15:27 UTC). Original push looped; content preserved here verbatim from session transcript.**

The inbox is more cohesive than it was three hours ago, but it has drifted in two new ways. Three of the six original seams (S1 name lock, S2 LiteLLM duplication, S4 single classifier) are now closed by Antigravity's run. Three seams remain (S3 host-vs-cell enforcement, S5 one-pipe-three-views, S6 §9.6 proof boundary). Two new seams have opened: S7 the word "harness" now means four different things, and S8 AG's phase numbering doesn't match AMPLIFIED-IDE's.

Nothing is fighting yet. The risk is the next agent reads only the newest file and misses the older constraints.

## Three independent verifications needed before §9.7 telemetry leans on AG's run

1. AG's completion record is self-tagged MEASURED but no independent re-test ran. Under the min-rule that's a runtime LLM self-report — caps at INTUITED, generously STRUCTURED. JWTs, Opik restarts, and harness self-test all need a second-agent or deterministic re-verify before §9.7 telemetry leans on them.
2. `deterministic-patches.jsonl` is the cross-agent contract — and AG's four patches aren't in it. AG's summary says "all registered in patches/deterministic-patches.jsonl" but the canonical file at the inbox root only has Devin's entry. Two paths, one ledger → attribution loss.
3. AG Phase 2 says `[DELETE] amplified_harness.py` but the file is still on the M5 inbox. Either the delete didn't happen, or it's the old file still next to the new `amplified_permissions.py`. Two overlapping files is exactly the seam this whole exercise was meant to weld.

## W1–W6 — the welds

- **W1** — Reconcile `amplified_harness.py` vs `amplified_permissions.py`. One file, one name, one import path.
- **W2** — Backfill AG's four patches into the root-level `deterministic-patches.jsonl` and pin the canonical path in README.
- **W3** — Add one paragraph to `BEAST-STATE.md`: lake + pool + Vellum + PUDDING are three views of one pipe, not three pipes.
- **W4** — One sentence in token-eff §9.6: the local-lane proof runs *from inside a sealed cell* calling host Ollama over HTTP at the bridge IP. Proves both economics and seal.
- **W5** — Adopt the glossary: permission classifier / open-door runtime / deterministic CLI cache / pre-production gate. Stop calling all four "harness".
- **W6** — Write `PHASE-MAP.md`: AMPLIFIED-IDE numbering is canonical; AG plans get a sub-prefix (Phase 2.AG).

## Hand-back cluster

Same 13 as `INBOX-INDEX` minus JWT (closed), plus OrbStack daemon auth on the Mac mini (newly surfaced by AG as their Unresolved Item 1). The cluster still collapses to one hand-back.

The W1-W6 patches themselves — they belong with the M5 watcher pass, not from Perplexity, for the same S3 reason (host-pushed files vs cell-internal). Re-tier AG to MEASURED — artifacts exist, independent verification doesn't.

---

[CLOSURE] branch=PLAN | proxy=1 logged (cohesion audit drafted as AI_PARTNER_PROXY) | gates=11-item cluster (INBOX-INDEX minus JWT, plus OrbStack auth) | inbox=cohesion-audit__recovered__v01__2026-06-24__perplexity.md | tier=STRUCTURED
