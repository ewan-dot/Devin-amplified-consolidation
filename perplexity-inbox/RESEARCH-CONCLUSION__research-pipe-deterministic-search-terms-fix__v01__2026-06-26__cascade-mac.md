---
title: "Research Pipe — Deterministic Search Terms Fix (no more 'external' collapse)"
document_type: research_conclusion
artifact_id: RESEARCH-CONCLUSION__research-pipe-deterministic-search-terms-fix__v01__2026-06-26__cascade-mac
date_utc: 2026-06-26
project: Amplified Partners
author: cascade-mac
reader: ewan
epistemic_tier: INTUITED
tier_reason: "AI-authored fix + regression tests; proven against 3 staging noise batches and 365 green tests, but not yet exercised against live Beast SearXNG (stale build) — INTUITED until a live run confirms."
ratifier: Ewan
---

# Research Pipe — Deterministic Search Terms Fix

## TL;DR

The promotion-investigation path sent SearXNG a **prose-wrapped claim**
(`"External evidence for INTUITED→STRUCTURED promotion review: <claim>"`).
SearXNG collapsed on the leading word **"external"** → dictionary noise.
**Fix:** the literal SearXNG query is now derived **deterministically from the
claim terms** (stopwords + promotion boilerplate stripped; NO LLM), and a
**no-silent-failure guard** refuses to stage results that share zero terms with
the claim. Source edited in `fleet-clean-build` (version-controlled, not a
build artifact). 7 regression tests added; full suite 358 → 365 green.

"Research proposes, Python disposes."

---

## 1. The proven defect (evidence)

Three live staging batches at `/opt/amplified-machine/apds/staging/<id>/packets.jsonl`
are all Cambridge / Merriam-Webster **"external"** definitions and
word-frequency dumps — not evidence:

| batch_id | source job |
|---|---|
| `08e25c62-…` | promotion investigation (general) |
| `1d501a25-…` | hooks/harness investigation |
| `26f2dd5c-…` | sovereign-ide investigation |

**Root cause (two layers, same prose):**

1. `promotion_alert.alert_from_drift()` set
   `sharpened_question = "External evidence for {tier}→{tier} promotion review: {claim}"`.
2. `promotion_investigation.build_research_query()` passed that prose verbatim as
   **`query_string`** — and `router.execute()` uses
   `search_string = query.query_string or query.sharpened_question`, so
   `query_string` is the **literal SearXNG query**. Leading word "external" +
   generic boilerplate ("evidence", "promotion", "review") → SearXNG returns
   dictionary/word-frequency pages. Even with good terms, the structural Gate0
   stub (`gate0-promotion-stub`) rubber-stamps structurally-valid noise, so the
   batch staged **green** — a silent failure
   (`DOCTRINE__no-silent-failures`).

The discriminator (`query_string` over `sharpened_question`) was verified by
reading `router.py` directly — fixing the wrong field would have left the patch
inert.

---

## 2. The fix (deterministic; no LLM)

### 2a. Deterministic term derivation — `promotion_alert.py`

New **pure function** `derive_search_terms(text) -> list[str]` (string → terms,
no network, no LLM, no POS tagging): regex tokenise → lower-case → drop standard
stopwords **and** the promotion boilerplate set (`external`, `evidence`,
`promotion`, `review`, `claim`, `peer`, `reviewed`, `primary`, `source`, plus
the tier words `intuited/structured/measured/proven`) → de-dup preserving order
→ cap 12 terms. Reproducible and free.

Mirror methods on `TierPromotionAlert`:
- `deterministic_search_terms()` — terms from the **claim** (falls back to the
  sharpened question only if the claim is degenerate).
- `deterministic_search_query()` — space-joined terms = the literal SearXNG query.

### 2b. Wire it into the query — `promotion_investigation.py`

`build_research_query()` now sets
`query_string = alert.deterministic_search_query() or alert.default_research_question()`.
`sharpened_question` **stays human-readable prose** (it feeds the ASPS scrub and
the logs) — only the backend query is detoxified. `auto_promote: false`, tier cap
INTUITED, producer→staging only, no Brain writes — all unchanged.

**Proof (real `alert_from_drift` → query):**
```
sharpened_question (human prose):
   External evidence for intuited→structured promotion review: Retrieval-augmented
   generation reduces hallucination in legal summarisation
LITERAL SearXNG query_string (backend sees):
   'retrieval-augmented generation reduces hallucination legal summarisation'
starts_with("external") = False
```

### 2c. No-silent-failure guard — `promotion_investigation.py`

After results return, `results_overlap_terms()` counts how many derived claim
terms appear in the result titles/snippets. The guard fails (sets
`success=False` + non-empty `error`, logs a warning, does **not** stage) in
**both** degenerate cases:
- **(a) no derivable terms** — claim is all stopwords/boilerplate, so
  `build_research_query()` fell back to the prose question (re-opening the
  "external" collapse risk) AND relevance is unverifiable → fail, do not stage
  blind;
- **(b) zero term-overlap** — terms exist but none appear in any result
  title/snippet → off-topic noise → fail.

`process_queue()` already releases the alert + warns on failure → that is the
visible sensor. New `InvestigationResult.term_overlap` field records the signal.
Rule is fixed ("no terms OR zero overlap = fail") — no tunable threshold.

### 2d. Content capture (listed defect #3) — already satisfied on this path

The "counts `len(results)` and discards content" defect is the **standalone
documented fan-out script**, NOT `investigate_alert`. On the investigation path,
`M1Orchestrator._results_to_packets` already captures url/title/snippet into
APDS packets. No change needed here; stated explicitly so the defect is not
silently dropped.

---

## 3. The diff (source; tests omitted for brevity)

Edited at source in `fleet-clean-build` repo (the nested, version-controlled
repo at `clean-build/` — `origin: Amplified-Partners/fleet-clean-build`; the
clean-build is a *build artifact only* relative to the outer
ingestion-to-research-pipe repo, but is itself git-tracked, so the fix lands at
source, not on a build artifact).

```diff
# promotion_alert.py — new deterministic term derivation
+_STOPWORDS / _PROMOTION_BOILERPLATE / _LOW_VALUE_TERMS frozensets
+def derive_search_terms(text) -> list[str]:   # regex tokenise, strip, de-dup, cap 12
+    TierPromotionAlert.deterministic_search_terms() -> list[str]
+    TierPromotionAlert.deterministic_search_query() -> str

# promotion_investigation.py — wire query + guard
-        query_string=alert.default_research_question(),
+        query_string=alert.deterministic_search_query() or alert.default_research_question(),
+def results_overlap_terms(results, terms) -> int:   # deterministic relevance probe
+    # in investigate_alert, after results:
+    if derived_terms and overlap == 0:
+        result.error = "degenerate search: zero term-overlap ... not staged"
+        return result   # no silent green
+    InvestigationResult.term_overlap: int = 0
```

Full diff: `git diff HEAD` on branch `claude/deterministic-search-terms` in the
`fleet-clean-build` repo. `git diff --stat`:
```
 02_build/research_pipe/promotion_alert.py          | 112 ++++++++
 02_build/research_pipe/promotion_investigation.py  |  ~85 ++++++-
 .../research_pipe/tests/test_promotion_wiring.py   | ~225 +++++++++-
 (~420 insertions; see `git diff HEAD` for exact)
```

---

## 4. The test (catches it if it regresses)

8 new tests in `test_promotion_wiring.py`
(`TestDeterministicSearchTerms` + `TestNoSilentFailureGuard`):

- query terms do **not** lead with / contain "external" or boilerplate;
- query terms **overlap** the claim terms (`hallucination` present);
- query is reproducible (same input → same query);
- `sharpened_question` stays human prose;
- overlap counter: on-topic > 0, dictionary-noise = 0;
- degenerate (dictionary "external") results → `success=False`, `error`
  contains "zero term-overlap", `packets_staged == 0`;
- all-boilerplate claim (no derivable terms) → `success=False`, `error`
  contains "no salient search terms", `packets_staged == 0`;
- on-topic results → still succeed and stage.

**Result:** `pytest research_pipe/tests/ -q` → **366 passed** (clean origin/main
baseline = **358**; delta = exactly the 8 added tests; no regressions). Tests run
offline (FakeRouter), no Beast/SearXNG needed.

---

## 5. Caveats / honesty

1. **Deployment gap (live still broken until rebuild).** The fix is in the
   version-controlled source. The live Beast container reads
   `/opt/amplified/clean-build-latest/` — a **stale build** (its `m1.py`
   predates the in-repo tier-lifting; it produced the 3 noise batches). Nothing
   changes in production until source is rebuilt/redeployed.

2. **Pre-existing tier-lifting × Gate0 interaction (separate bug, NOT fixed
   here, surfaced honestly).** origin/main's `M1Orchestrator._assess_tier`
   deterministically **lifts** academic/DOI/.gov/arxiv results to STRUCTURED,
   but the promotion path caps packets at INTUITED, so Gate0 then **rejects
   exactly the highest-quality evidence** with a misleading
   `"gate0 filtered all packets or staging empty"`. Net effect: even with the
   good deterministic query, the promotion path can only stage **plain-web
   INTUITED** hits; academic results are dropped. This is **non-silent**
   (`success=False`), so it does not violate the doctrine, and it is out of
   scope for this fix — flagged for a follow-up. My "works end-to-end" proof
   therefore covers **query-building + plain-web staging**, not academic-result
   staging.

3. **Embedding/semantic backend not used** — the relevance guard is pure
   lexical term-overlap (deterministic, free) by design; no embeddings.

---

[CLOSURE] branch=IMPLEMENT | proxy=none (no push, no Vellum — drafted for human) | gates=human runs the 2 push commands + posts the Vellum row | inbox=RESEARCH-CONCLUSION__research-pipe-deterministic-search-terms-fix__v01__2026-06-26__cascade-mac.md | tier=INTUITED
