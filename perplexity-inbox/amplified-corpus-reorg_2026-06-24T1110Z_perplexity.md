---
title: "Amplified Corpus Reorg — dedupe-quarantine → clean department structure"
type: executable-brief
status: ready-to-implement
tier: STRUCTURED
provenance: "Classification of all 611 md files in _dedup-apply-quarantine by Perplexity, 2026-06-24, from content+path+heading signal. Companion data files included."
ratifier: "Ewan Bramley (for-now). Implementation runs locally on MacAirM5 watchers."
created: 2026-06-24
companion_dir: reorg-files/
---

# Executable Brief — Clean the Corpus, Move It Out

## Goal
Get the data OUT of `_dedup-apply-quarantine` and into a clean, department-sorted location where what-exists and what's-been-done are obvious — so research is not redone. Completeness without bloat.

## What this produces
A new folder `~/amplified-corpus-clean/` containing:
- **9 department folders** (current, visible work) + **`_archive/`** (bloat, out of sight).
- **A README in every folder** stating what it holds and what's been done.
- **498 current files** sorted; **113 bloat files** archived (vault-monitor runs, shared-board v3–v14, superseded -vN versions).
- Originals in `_dedup-apply-quarantine` are LEFT UNTOUCHED (this is a COPY, reversible).

### Department layout
```
amplified-corpus-clean/
├── README.md
├── 01-doctrine/            (13)  rods, manifestos, Ulysses, constitution, identity material (for-now, unsettled)
├── 02-methodology/          (7)  Pudding, ABC bridge, min-rule, validation methodology, phrase index, taxonomy standard
├── 03-math-logic/         (1+)  Soviet stack (Markov/Voronoi/Kolmogorov), Taguchi, Kantorovich
├── 04-product/             (23)  Covered AI, HGV, Dave/Jesmond, pricing, GTM
├── 05-engineering-infra/   (18)  architecture, Redis/Qdrant/FastEmbed, Retell, deployment
├── 06-agents-orchestration/(50)  partners (Sam/Clawd=Claude, Grok=xAI), hub-and-spoke, OpenClaw
├── 07-research/            (21)  deep-research reports, comparisons
├── 08-content-marketing/   (34)  Substack/LinkedIn/Gary Vee, calendars (Eli = independent author)
├── 09-transcripts-voice/  (331)  RAW SOURCE voice memos/transcripts — feedstock, not conclusions
├── 99-unsorted/            (1)   did not classify cleanly — review
└── _archive/                    superseded versions + vault-monitor + shared-board churn (history only)
```

## How to implement (M5)
1. Review `reorg-files/move_manifest.json` (per-file placement) and `reorg-files/classification.json` (department signal) — spot-check the sort.
2. Run `reorg-files/do_move.sh`. It is idempotent-safe (cp, `|| true`), reads from the quarantine folder, writes only to `~/amplified-corpus-clean/`. No deletes, no moves, no Beast writes.
3. Verify counts match the layout above, then (optionally, your call) delete the quarantine folder once satisfied.

## Decisions baked in (from Ewan, 2026-06-24)
- Sort by DEPARTMENT (methodologies, math, logic, product, etc.). Function-first.
- Bloat (versioned dups, monitor runs, board churn) → `_archive/`, not deleted, not in the way.
- Copy not move (originals preserved until Ewan verifies).
- READMEs everywhere so finished work is visible and not redone.

## NOT done in this pass (deliberate — needs your ruling first)
- **Bracketed-prior-name renaming** (canonical name with old name in brackets for searchability). Held back because it depends on the open taxonomy rulings (partner harnesses, Devon-vs-Devin, prefix syntax). Do the sort first; rename in a second pass once the taxonomy standard is ratified.
- **Math thinking buried in voice transcripts** — flagged: your Markov/Kolmogorov reasoning is mostly SPOKEN (in 09-transcripts-voice), not in documents. A later extraction pass (content-harvester) can lift it into 03-math-logic.

## Min-rule
TIER: STRUCTURED. The classifier is a keyword+path heuristic (reproducible, judgment-weighted), not measured against a labelled set. ~1 file landed unsorted; spot-check before deleting originals.

[CLOSURE] action=ready-to-implement · endpoint=perplexity-inbox · gates=Ewan/M5 runs do_move.sh (Tier C: bulk filesystem reorg — Perplexity does not execute it). Renaming pass deferred pending taxonomy ratification.
