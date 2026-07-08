---
title: "conclusions-v03-lens-fix-engine-pullapart-mre-suite"
document_type: baton
date_utc: 2026-07-08
from_agent: cursor
to_agent: next-seat
author: cursor
epistemic_tier: INTUITED
baton_ts: 2026-07-08T220450Z
---

# Baton pass — cursor — 2026-07-08 (evening seat, ~13:44–23:03 UTC+1)

## Done this seat (verified)

- **Conclusions handoff edition v01 → v02 → v03** in `~/Scoped-agentic-work-space-01-07-2026/`:
  v02 fixed six review findings (validation scoping "existence ≠ correctness", class tally,
  entry-11/14 tier fixes, A2 orphan wired, entry-13 freshness caveat, 5↔29 bronze/projection
  resolution); v03 added Part 8 delta (α=0.398 first calibration bounce, worktree contract,
  fix-as-found, should→how, usefulness rater) + entry 38a (axes never hand-ratified: facet
  analysis derives [A22], construct validation validates [A23], both title-matched).
- **Cursor rules encoded** (home `~/.cursor/rules/` + repo SSOT `ingestion-to-research-pipe/.cursor/rules/`,
  commits 8b6d7b3, 47eee07, e6a4de5, +1): `amplified-evidenced-conclusions.mdc` (digest, kept
  in sync through the uchg lock cycle) and `outcome-first.mdc` (alwaysApply; architect
  correction embedded verbatim: NO selling drift — methodology working end-to-end is the
  outcome; Amplified is its own first customer; dogfood runs with used/discarded verdicts count).
- **Lens (intent-interface) verify green**: fixed preload `index.d.ts` missing `fetchInbox`
  (typecheck was failing), added `BRAIN_API_KEY` → `X-API-Key` header in `brain.ts` (the
  knowledge.beast proxy EXISTS behind an API key — G2 doc claim stale). Commit `fed7a57` on
  branch `fix/verify-green-brain-auth` in `~/ingestion-to-research-pipe/Projects/intent-interface`
  (nested repo, remote Amplified-Partners/intent-interface). Patch exported to
  `~/amplified-pipeline/cursor/PATCH__intent-interface__verify-green-brain-auth__fed7a57__2026-07-08.patch`.
  Merge request ledgered (Vellum bf637108). NOT merged — Mac push-read-only + Devin ignores
  GitHub mentions (fact in `~/ESTATE-NOTES.md`, created this seat).
- **UI state-of-play verified across M5 + M4 mini + Beast** (measured): Lens v0.1.0 installed
  both Macs; smoke 24/24; `~/Projects/intent-interface` on M5 is a DIFFERENT stray v0.0.0
  project (sprawl trap, unretired); codex-mcp credential vault reported unavailable.
- **Thread extraction run**: 8 live cowork/claude threads rendered deterministically to bronze
  + swarm-extracted → 113 quote-verified atoms (run dir
  `~/amplified-pipeline/data/evidence-field-corpus/runs/2026-07-08__thread-extract-cowork-claude/`).
- **Coherence audit of the 13-doc scoped-workspace corpus** →
  `00-COHERENCE-AUDIT__scoped-workspace-13-docs__v01__2026-07-08__cursor.md`; consolidated
  5-item architect decision queue (tokens rotation = only blast-radius item, 3 days old).
- **Three cross-checks, all citations title-matched live, zero fabrications found today**:
  `research/00-CROSSCHECK__rater-x-pipeline-prior-art__v01` (13/13),
  `research/00-CROSSCHECK__rater-convergence__estate-sweep-x-perplexity__v01` (D1: math_grade
  demoted usefulness→verification-affordance; combination GAP resolved by dogfood receipts),
  and the five-stage pull-apart `research/00-PULL-APART__refinement-engine-prior-art__v01`
  (engine components all owned: T→DSPy/TextGrad/GEPA, ratchet→FrugalGPT-adjacent,
  collapse-to-code→PROSE/PBE, adaptivity→Howard-Ramdas, truth-budget→Snorkel; sole surviving
  novelty = statistically-licensed plug retirement; estate-first FAILED inside the hypothesis:
  Snorkel+DSPy were in local_sweep, uncited; 6 methodology-improvement findings documented;
  JSONL witness `~/amplified-pipeline/data/research-pipe-docs/2026-07-08_five-stage_39e3c699.jsonl`).
- **MRE validation methodology + nine-test suite persisted verbatim** (were chat-only) to
  `methodologies/MRE__{continuous-external-validation,test-suite-nine-claims}__v01__2026-07-08__perplexity-verbatim.md`
  + review companion `MRE__validation-suite-review__v01__2026-07-08__cursor.md` (4 fixes:
  audit budget, H(t) gameable by non-registration, Lane-1 citation≠MEASURED, extend
  validate_conclusions.py — do NOT birth a second ledger).
- Vellum witnesses posted throughout (b0f61dd4, 29f60807, 0d90206e, bd81a822, b93eca8c,
  c692d339, e41119bd, ccff40c2, 21530f7c, 3824c37f, e8ff42ff). Estate/log payload shape that
  works: `{author, content, metadata:{repo, action, pr, ...}}` — 422 without metadata trio.

## Open

| Item | Owner | Blocker |
|------|-------|---------|
| Rotate 3 live GitHub tokens in Beast git remotes (admin scopes, located 07-05) | Ewan | account-side only |
| Merge `fed7a57` Lens patch + set BRAIN_API_URL/BRAIN_API_KEY env | Ewan bypass-merge or Devin (after console flip: enable respond-to-mentions for Amplified-Partners) | Devin silent on GH mentions |
| 50-atom triple-purposed gold sample (rater signal-1 + T5 + κ machinery) | Ewan labels + second judge; cursor = independent recomputation | — |
| MRE bootstrap step 1: seed claim ledger (extend validate_conclusions.py schema) | claude-code/cascade-mac | consume pull-apart verifiers[] seeds |
| §10.C3 quote-gate replication (second oracle from spec, no shared code) | **cursor volunteered** | needs the 725 triples published |
| §10.C6 gate ablation (doctrine's biggest single risk) | claude-code | run before building on the 0.10 figure |
| Hypothesis thread parked awaiting `/compact` | Ewan (slash command in that session) | — |
| Cowork 57319faa awaiting file-access grant (verify Vellum wiring) | Ewan | — |
| Retire/rename stray `~/Projects/intent-interface` (v0.0.0 trap) | any seat | — |

## Next seat should

1. Read the four-threads synthesis + the two MRE verbatim docs + my review companion in
   `methodologies/` — then execute MRE bootstrap step 1 by EXTENDING `tools/validate_conclusions.py`
   (verifiers[], next_audit_due, falsifier fields), seeding engine claims from the pull-apart's
   eight title-matched anchors (several with refutes roles — the contradiction protocol wants them).
2. Drive the 50-atom gold sample to collection (sample selection by a seat that is NOT the
   scorer author — entry 15/Lane 5; cursor recomputes from raw when it lands).
3. Run §10.C3 first, §10.C6 second per the suite's own priority; publish the 725 triples so
   the independent oracle can be written.
4. Sync handoff v03 → v04 only after M1-stamped survivors exist (avoid pre-gate banking);
   build the ledger→handoff generator then (audit flagged dual-maintenance drift).
5. Keep the never-unlearn list live: κ 0.19 ≠ 0.398 (different metrics/datasets); centrality ≠
   brokerage; tuning-sample collapse = candidate not code; confidence ≠ salience; counts
   without disparity are echo-blind; un-persisted numbers are HYPOTHESIS.

## Read first

- `~/Scoped-agentic-work-space-01-07-2026/00-CONCLUSIONS__v2-EVIDENCED__2026-07-08.md` (ledger, 55 checks)
- `~/Scoped-agentic-work-space-01-07-2026/methodologies/` (MRE pair + cursor review)
- `~/Scoped-agentic-work-space-01-07-2026/research/00-PULL-APART__refinement-engine-prior-art__v01__2026-07-08__cursor.md`
- `~/Scoped-agentic-work-space-01-07-2026/00-COHERENCE-AUDIT__scoped-workspace-13-docs__v01__2026-07-08__cursor.md`
- `/Users/ewansair/container on m5/SYNTHESIS__four-threads-one-engine__v01__2026-07-08__cascade-mac.md`

## Blockers

None hard for the next seat. Soft: codex-mcp credential vault "unavailable" (blocks
knowledge-API key wiring via broker); Devin GitHub-mentions integration off (bypass-merge is
the second identity until flipped); arXiv export API flaky (use OpenAlex DOI route first).

[CLOSURE] tier=INTUITED | branch=fix/verify-green-brain-auth (intent-interface) / task/sandbox-intelligence-lake (ingestion-to-research-pipe)
