---
document_type: executable_preregistration
title: "Specialist Extraction Swarm — Four-Arm Pre-Registered Experiment"
stage: decision
audience: agent
purpose: >-
  Machine-facing, runnable pre-registration of a four-arm experiment comparing a wide extractor
  against role-specialist swarms with escalating validation. Runnable without further design choices
  except values explicitly marked CALIBRATE.
epistemic_tier: STRUCTURED
epistemic_tier_reason: >-
  Design over unrun experiments; thresholds grounded in primary evidence are cited inline, and any
  ungrounded threshold is marked CALIBRATE rather than guessed. The composed architecture is not
  promoted above STRUCTURED.
machine_action_allowed: draft
outcome:
  class: production_candidate
  reason: >-
    An executable protocol subject to calibration. On PASS of the decision table it becomes a
    production candidate; on FAIL it retires the composed design. No direct Beast write.
beast_write: forbidden
companion_human_doc: specialist-extraction-swarm-prior-art__human__2026-07-12T20-50-00Z__perplexity.pplx.md
distinguishes_consistency_from_accuracy: true
source_refs_grounding_thresholds:
  - https://arxiv.org/abs/2407.21787
  - https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf
  - https://arxiv.org/html/2606.13685
  - https://arxiv.org/pdf/2606.19544v1.pdf
  - https://arxiv.org/html/2603.20324v1
  - http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf
  - https://arxiv.org/pdf/1805.05206
  - https://arxiv.org/abs/2303.17651
  - https://aclanthology.org/2024.emnlp-main.706.pdf
  - https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61
  - https://www.iso.org/standard/69418.html
  - http://faculty.washington.edu/jwilker/559/Krippendorf.pdf
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://api-docs.deepseek.com/guides/kv_cache
---

# Specialist Extraction Swarm — Four-Arm Pre-Registered Experiment (Agent Protocol)

## 0. INVARIANTS (must hold every run; violation aborts the run)

- INV-1 `quote_is_source_substring`: every accepted candidate's quote is a byte-exact substring of the normalised source. Deterministic (string membership).
- INV-2 `offsets_in_bounds_monotone`: all offsets within `[0, len(source_norm))`, non-overlapping per role output, monotone.
- INV-3 `schema_valid`: candidate validates against the frozen JSON schema `SCHEMA_V1`.
- INV-4 `label_in_closed_vocab`: every label ∈ `VOCAB_V1`.
- INV-5 `identity_resolved`: every entity mention maps to a canonical id via the deterministic linker or is flagged `unlinked`.
- INV-6 `producer_checker_family_disjoint`: for any candidate, `checker.model_family != producer.model_family`. Grounded: same-family judges are lenient/correlated ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf); [Selection Bottleneck same-family tie 34.9% vs cross 28.8%](https://arxiv.org/html/2603.20324v1)).
- INV-7 `no_synthesis`: aggregation may UNION and SELECT but never merges candidates into a new synthesised string. Grounded: synthesis loses to single-model baseline in 82% of comparisons ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)).
- INV-8 `frozen_prompts_within_run`: each role/checker system prompt is byte-identical within a run (prefix-cache precondition). Grounded: prefix must fully match to hit ([DeepSeek caching](https://api-docs.deepseek.com/guides/kv_cache)).
- INV-9 `consistency_not_accuracy`: any agreement/spread statistic is labelled `precision` and reported separately from any bias-vs-gold statistic labelled `trueness`. Grounded ([ISO 5725-1](https://www.iso.org/standard/69418.html); [Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)).
- INV-10 `provenance_written`: every accepted candidate carries `{doc_id, char_start, char_end, role_id, run_seed, checker_verdict, reason_code}`.

## 1. FROZEN CORPUS AND SPLITS

- `CORPUS_FROZEN`: 40 fixed files, versioned list `corpus_v1.lock` (hash-pinned). CALIBRATE: exact file ids (draw from the internal v05 corpus; freeze before any run).
- `SPLIT_TUNE` = 10 files (threshold-setting only). `SPLIT_TEST` = 30 files (scored, never used for tuning).
- `DURABILITY_CORPUS`: a second 30-file corpus of a different register (`perplexity-inbox`), zero re-tuning. Purpose: attack the internal deep-gate durability FLAG (RATIFY spread 0.57–0.90) as a precision-vs-register question.
- Text normalisation pinned: `norm_v1` (unicode NFC, whitespace collapse policy, case policy). All INV-1/INV-2 defined against `norm_v1`.

## 2. ARMS

| Arm | Producers | Validators | Aggregation |
|---|---|---|---|
| A. Wide extractor (control) | one generic worker, whole-atom extraction, N runs | downstream gates only (current behaviour) | union of runs |
| B. Specialists, no validators | roles R1–R4 (boundary, evidence, atomiser, classifier), each N runs | none (raw role output) | union of role outputs |
| C. Specialists + deterministic validators | roles R1–R4, each N runs | Layer-A only (INV-1..INV-5), one reason-coded retry | union then Layer-A select |
| D. Specialists + deterministic + independent semantic validators | roles R1–R4, each N runs | Layer-A + Layer-B (different-family narrow-question checker), one reason-coded retry | union then Layer-A then Layer-B select |

- Optional additive arms (each its own mini-ablation, off by default): R5 bridge-spotter, R6 dedup/contradiction-scout; a **no-roles repeated-sampling arm** = Arm A run at high N (include, because plain k-shot may dominate agents per cost, [Independent Sampling](https://arxiv.org/html/2605.08478v1)); a **deterministic-boundary arm** = R1 replaced by unsupervised segmentation (grounded feasible at F≈0.76, [AAAI 2007](https://dias.users.greyc.fr/publications/aaai2007.pdf)).

## 3. ROLE PROMPTS (frozen, narrow, small option set)

- R1 boundary-scout → outputs offset list only.
- R2 evidence-harvester → verbatim spans ≤25 words, must satisfy INV-1.
- R3 atomiser → schema fill from R1+R2, every field grounded in an R2 span.
- R4 classifier → labels ∈ `VOCAB_V1` (stage / grain / deterministic-vs-probabilistic).
- Layer-B checker prompt: input `{chunk, producer_output, one_narrow_question}`; output ∈ `{accept, reject:<reason_code>}`. Reason codes: `{quote_mismatch, offset_error, schema_violation, label_error, identity_error, unsupported_claim, other}`.
- Full prompt text: CALIBRATE (author the byte-frozen strings before run; keep first ≥256 tokens identical across roles to share the cache prefix, [DeepSeek caching](https://api-docs.deepseek.com/guides/kv_cache)).

## 4. MODEL / PROVIDER / VERSION CONTROLS

- Producer family: DeepSeek (`deepseek-chat` and/or `deepseek-reasoner`), version-pinned by API model id + snapshot date. Grounded pricing anchor: cache-hit input "$0.0028"/1M vs cache-miss "$0.14"/1M for deepseek-chat ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)).
- Checker family (Arm D): a DIFFERENT family than the producer (INV-6). CALIBRATE: choose from a non-DeepSeek family (e.g. a Claude-class or Gemini-class model); rotate per arm to test family effect. Checker must not be weaker than producer (grounded: weak judge saves at most factor-two, [LLM-as-Judge won't beat twice the data](https://openreview.net/pdf?id=NO6Tv6QcDs)).
- Producer temperature: positive, to build coverage (grounded: coverage scales with samples, [Large Language Monkeys](https://arxiv.org/abs/2407.21787)). CALIBRATE exact T (start 0.7).
- Checker temperature: 0 for the deterministic-verdict sub-run; positive only for the multi-trial consensus sub-study (§9). Grounded: T=0 cuts flip rate ([Coin Flip Judge](https://arxiv.org/html/2606.13685)).

## 5. REPLICATION / SEEDS

- Each producer role runs with seeds `S = {s1..sN}`, fresh sessions, no shared context across seeds (independence precondition for coverage and capture–recapture, [Large Language Monkeys](https://arxiv.org/abs/2407.21787); [capture–recapture independence caveat](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)).
- Precision sub-study (E3-analogue): 3 fully independent whole-pipeline repetitions per arm; report per-role accept-rate spread and atom-set Jaccard across repetitions (ISO 5725 repeatability, [ISO 5725-1](https://www.iso.org/standard/69418.html)).
- N (initial run count): governed by §9 stopping rules, not fixed. Seed logging mandatory (INV-10).

## 6. IDENTITY / ALIGNMENT METHOD

- Cross-run/cross-arm candidate alignment: deterministic hash on `{doc_id, char_start, char_end}` for exact-span identity; for same-idea alignment use graded similarity validated against a small human-aligned gold, threshold frozen per corpus (grounded: keep similarity graded, do not port a cut-off, [Lightweight Pyramid](https://arxiv.org/pdf/1904.05929.pdf)). CALIBRATE: similarity threshold on `SPLIT_TUNE` only.

## 7. UNION POLICY

- Aggregation = UNION of all candidates surviving the arm's validators, then SELECT by gate/checker verdict. No majority filtering pre-union (grounded: majority vote ≈ baseline on open tasks, [Selection Bottleneck](https://arxiv.org/html/2603.20324v1)). No synthesis (INV-7). Recurrence count retained as an importance weight, not a filter ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf)).

## 8. DETERMINISTIC GATES + VALIDATOR BLINDING + PLANTED-FAULT BATTERY

- Layer-A gates: INV-1..INV-5, code, free, immediate; reject → one reason-coded retry → quarantine (grounded bound: retry gains shrink, near-zero when already correct, [Self-Refine](https://arxiv.org/abs/2303.17651)).
- Layer-B blinding: checker sees no producer identity; runs in fresh context (grounded: own-family mitigation via blinded multi-judge, [FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)).
- Planted-fault battery (calibrate validators BEFORE trusting any number, mutation-testing style, [DeepMutation](https://arxiv.org/pdf/1805.05206)): inject ≥50 deterministically-mutated bad items per role stream — classes `{mutated_quote, off_by_one_offset, wrong_label, fabricated_atom, identity_swap}` — plus ≥100 known-good ledger-RATIFIED items. Metrics: catch-rate per fault class (trueness of validator); false-kill rate on known-good.
  - Grounded threshold: Layer-A catch on `mutated_quote` and `fabricated_atom` should be ≈1.0 (deterministic). CALIBRATE Layer-B catch target and false-kill ceiling — the literature standardises the *measure* (mutation score) but sets *no required value* ([DeepMutation](https://arxiv.org/pdf/1805.05206)). Provisional CALIBRATE: catch ≥0.90 on fabrications/quote-mutations, false-kill ≤0.05.

## 9. RUN-COUNT AND STOPPING RULES (yield-driven, difficulty-adaptive)

- STOP-HARVEST (recall): after each added run, compute new-item yield and best-case-recall-vs-runs; STOP when Δ best-case recall < ε (CALIBRATE ε on `SPLIT_TUNE`). Estimate hidden pool from run overlap via capture–recapture; report estimate + CI; test independence before trusting it ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf); [capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)).
- STOP-VERDICT (checker, Arm D consensus sub-study): repeat checker until consensus fidelity target reached. Grounded reference curve: 95% fidelity ≈ 11 majority-vote trials overall, 3 for easy, >50 for hard items; 90% ≈ 3 / 1 / 15 ([Coin Flip Judge](https://arxiv.org/html/2606.13685)). Map item difficulty to trial budget accordingly; do NOT use a fixed count.
- RETRY-DEPTH sub-study: run retry depths {0,1,2}; measure marginal recovery rate and per-attempt cost; report the depth where marginal recovery < marginal cost (grounded shape: diminishing per round, [Self-Refine](https://arxiv.org/abs/2303.17651)).

## 10. METRICS

Primary (report per arm, with 95% CI):
- `quote_gate_accept_rate` (quotation validity) — Wilson interval.
- `recall_vs_gold` / coverage — against seeded-fault + published-gold truth; also best-case-recall-vs-runs curve.
- `schema_fault_rate`, `label_fault_rate`.
- `validator_catch_rate` per fault class (trueness of validator) and `false_kill_rate`.
- `atoms_per_dollar` and `atoms_per_model_call` (grounded cost frame: k-shot vs agents compared per dollar AND per call, [Independent Sampling](https://arxiv.org/html/2605.08478v1)).

Secondary:
- `precision` (run-to-run accept-rate spread, per-role Jaccard) — labelled precision, NOT accuracy (INV-9, [ISO 5725-1](https://www.iso.org/standard/69418.html)).
- `duplicate_rate`, `hallucination_rate` post-union (grounded reference magnitudes: union hallucination 38–52% before scrutiny, [L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)).
- `prefix_cache_hit_rate` from `prompt_cache_hit_tokens/(hit+miss)` ([DeepSeek caching](https://api-docs.deepseek.com/guides/kv_cache)).

## 11. PREVALENCE-ROBUST AGREEMENT

- Producer↔checker agreement on the rare-rejection class: report Gwet's AC1 AND Krippendorff's alpha with CIs; do NOT report Cohen's kappa alone (grounded: kappa collapses under skew; "85% agreement" ≈ κ 0.48, [Gwet AC1 vs kappa](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61); [Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf); [Krippendorff](http://faculty.washington.edu/jwilker/559/Krippendorf.pdf)). Krippendorff thresholds: rely on α≥0.800, tentative at α≥0.667.

## 12. ERROR-CORRELATION CHECK (same vs different family)

- Estimate pairwise error correlation δ between repeated same-family producer runs and between producer and different-family checker. Grounded: uncorrelated members cut added error by 1/L; correlated members do not ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)). Report δ on the items the pipeline WRONGLY accepts (the failure set), not only overall. Do NOT use disagreement as a proxy for accuracy (same source's caution): measure accuracy directly on the gold/seeded-fault truth.

## 13. CACHE / COST LOGGING

- Per call log `{prompt_cache_hit_tokens, prompt_cache_miss_tokens, output_tokens, model_id, role_id}`; compute cost via pinned prices ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)). Report κ_t (cost per accepted atom) and per-role cache-hit rate per arm. PASS-cache: role arms' cache-hit ≥ control arm's reported ~47% (USER/REPO-ORIGINATED baseline, not remeasured).

## 14. MULTIPLE-COMPARISON HANDLING

- Pre-register the primary comparison as D vs A on `quote_gate_accept_rate` and `atoms_per_dollar`. All other arm comparisons are secondary. Control family-wise error with Holm–Bonferroni across the secondary set; report adjusted p-values (mirrors adjusted-p reporting in [Selection Bottleneck](https://arxiv.org/html/2603.20324v1)). Effect sizes (Hedges' g) reported alongside p.

## 15. FAILURE CRITERIA (kill conditions — a null result is a valid, valuable outcome)

- KILL-DESIGN if Arm B/C/D do not beat Arm A on `quote_gate_accept_rate` by the pre-registered margin at ≤ the pre-registered cost multiplier (i.e. decomposition adds cost without measured error removal → the wide block was fine; keep A). Grounded rationale: decomposition must remove a measured error to justify itself ([least-to-most within-domain failure](https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf); [MAST design-failure taxonomy](https://arxiv.org/html/2503.13657v2)).
- KILL-DESIGN if the no-roles repeated-sampling arm dominates all role arms on `atoms_per_dollar` AND `atoms_per_model_call` ([Independent Sampling](https://arxiv.org/html/2605.08478v1)).
- KILL-VALIDATOR (Arm D unusable) if Layer-B false-kill rate exceeds ceiling OR Layer-B rubber-stamps (catch-rate on seeded faults below target) — grounded by consistency-without-validity risk ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)).

## 16. DECISION TABLE

| Condition (on SPLIT_TEST, with CI) | Decision |
|---|---|
| D beats A on quote-gate accept by margin M at ≤ cost× C, AND D beats C (semantic checker adds catch), AND validator false-kill ≤ ceiling | ADOPT D as production_candidate (subject to durability §17) |
| C beats A but D does not beat C | ADOPT C; semantic checker not justified; log Layer-B failure shapes |
| B/C/D do not beat A within cost | KILL composed design; keep wide extractor A |
| No-roles k-shot arm dominates on cost-efficiency | KILL role decomposition; keep k-shot + gates |
| Any role's validator kill-rate → ~0 with concentrated near-miss errors | PROMOTE that role to deterministic code candidate; re-test (expressibility + durability) |
| Durability corpus accept-rates fall outside ±5 pt band | HOLD; treat deep-gate as non-durable, not adopted |

- Pre-registered thresholds M, C, cost×, and the ±5 pt band: **CALIBRATE on SPLIT_TUNE before scoring** (the design file's provisional "+5 pts quote-gate at ≤1.3× cost" is a starting point, not a validated bar).

## 17. DURABILITY

- Re-run the winning arm on `DURABILITY_CORPUS` with zero re-tuning. PASS: per-role accept-rates within ±5 pt (CALIBRATE band). This directly tests whether the internal deep-gate spread 0.57–0.90 is register non-comparability (precision) rather than gate failure — reported as precision, separated from trueness (INV-9).

## 18. ARTEFACTS TO RETAIN

- `corpus_v1.lock`, `norm_v1` spec, frozen role/checker prompt hashes.
- Per-candidate ledger (INV-10 fields) for every arm and seed.
- Planted-fault battery + per-class catch/false-kill tables.
- Coverage-vs-runs, best-case-recall-vs-runs, consensus-fidelity-vs-trials, retry-depth curves.
- AC1/alpha with CIs; precision (spread/Jaccard) tables; trueness (bias-vs-gold) tables — kept in separate files (INV-9).
- Cost logs (cache hit/miss/output tokens, κ_t, cache-hit rate per role/arm).
- Decision-table evaluation with adjusted p-values and effect sizes.
- Failure-shape ledger (reason-coded validator kills) as labelled wrong-examples.

## 19. ROUTING

- machine_action_allowed: **draft**. No direct Beast write (`beast_write: forbidden`). Emit results to `local_workspace`. Companion narrative: `specialist-extraction-swarm-prior-art__human__2026-07-12T20-50-00Z__perplexity.pplx.md`. Any value marked CALIBRATE must be fixed ex-ante (before scoring SPLIT_TEST) and logged; no CALIBRATE value may be tuned on SPLIT_TEST. All non-CALIBRATE values are runnable as written.
