---
document_type: readable_research_conclusion
title: "Specialist Extraction Swarm with Per-Agent Validators — Prior-Art Test"
stage: synthesis
audience: Ewan
purpose: >-
  One comprehensive prior-art test of the composed hypothesis that a written-language
  extraction pipeline is more accurate and consistent when one wide extraction task is
  split into narrow specialist roles, each run independently several times, unioned,
  each followed by deterministic then different-family semantic checks, with reason-coded
  retry, information-yield-driven run counts, and deterministic promotion of stabilised roles.
epistemic_tier: STRUCTURED
epistemic_tier_reason: >-
  The composed architecture is a structured synthesis over primary evidence; no proposed
  specialist experiment has been run. Individual cited results keep their own tier inline
  (MEASURED for dataset results, PROVEN for standards/formal results). The composed
  architecture is never promoted above STRUCTURED.
epistemic_role: clarity
attribution: Perplexity (research synthesis); every measured/proven value attributed inline to its primary source
system_of_record: local_workspace
machine_action_allowed: recommend
next_human_decision: "Approve or amend the four-arm pre-registered experiment before any specialist run."
companion_agent_doc: specialist-extraction-swarm-experiment__agent__2026-07-12T20-50-00Z__perplexity.pplx.md
outcome:
  class: methodology_candidate
  reason: >-
    A primary-source-grounded prior-art test plus an executable four-arm protocol, ready to run.
    No human decision is required to close the research; the natural next step is the experiment.
internal_baseline_status: USER/REPO-ORIGINATED — reported by the internal pipeline, not re-measured here
source_refs:
  - https://arxiv.org/html/2502.18702v1
  - https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf
  - https://www.arxiv.org/pdf/2507.15152.pdf
  - https://arxiv.org/abs/2407.21787
  - https://arxiv.org/html/2605.08478v1
  - https://arxiv.org/abs/2410.12189
  - https://arxiv.org/html/2606.13685
  - https://arxiv.org/pdf/2606.19544v1.pdf
  - https://arxiv.org/html/2503.13657v2
  - https://arxiv.org/abs/2502.00674
  - https://arxiv.org/html/2603.20324v1
  - http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf
  - https://dias.users.greyc.fr/publications/aaai2007.pdf
  - https://api-docs.deepseek.com/guides/kv_cache
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://aclanthology.org/2024.emnlp-main.706.pdf
  - https://arxiv.org/abs/2203.11171
  - https://arxiv.org/abs/2303.17651
  - https://arxiv.org/pdf/1805.05206
  - https://arxiv.org/pdf/1904.05929.pdf
  - https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf
  - https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61
  - https://www.iso.org/standard/69418.html
  - http://faculty.washington.edu/jwilker/559/Krippendorf.pdf
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/
  - https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
---

# Specialist Extraction Swarm with Per-Agent Validators — A Primary-Source Prior-Art Test

*Plain-English report. Every measured or standardised value is attributed inline to the original source that states it — a paper, an official standard, or official provider documentation. The composed architecture under test is a design, not a measured result: it is tagged **STRUCTURED** throughout and never promoted above the strength of its parts. This report extends, and does not repeat, the earlier evidence file `written-language-extraction-methodologies__human__2026-07-12T19-47-00Z__perplexity.pplx.md`; it focuses on the parts of the composition that file left thin — multi-agent role decomposition, error correlation across model families, aggregation policy (union vs select vs synthesise), saturation of repeated sampling, and the separation of consistency from trueness.*

## 0. How to read this, and the three evidence tiers

- **[MEASURED]** — the primary source reports a real number on a named dataset with a stated way of measuring. Strongest.
- **[STRUCTURED]** — the source describes a method or design but does not report the specific number we wanted; a good idea, not yet a measured result.
- **[PROVEN]** — a formal or standardised fact: a published standard, a mathematical result, or a defined statistic.

Plain-English terms used below: a **role/specialist** is one narrow model job (find a boundary, copy a quote, fill a schema field, pick a label); **union harvesting** means keeping every candidate any run produced rather than keeping only the majority answer; a **producer→checker** pair is one model that emits and a second, separate model or code that judges; **coverage** is the fraction of true items found by *any* run; **trueness** is closeness to the truth; **consistency/precision** is closeness of repeats to each other; **saturation** is the point where more runs stop adding new true items.

The internal pipeline's own reported figures (5,450 candidates, 96% coverage, exact-quote gate 0.96 at n=725, label gate 0.867, deep-checker RATIFY spread 0.57–0.90 across batches, ~47% prefix-cache hit) are used only to keep this test relevant. They are **USER/REPO-ORIGINATED and not re-measured here**, and the proposed specialist experiments **have not run**; unrun thresholds are never treated as validated.

---

## 1. Direct verdict

The composed hypothesis is **plausible and mostly aligned with primary evidence, but two of its seven claims are only conditionally supported and one is at real risk.** Tagged **STRUCTURED** as a whole:

1. **Split a wide task into narrow roles** — *conditionally supported [STRUCTURED]*. Role decomposition measurably raises extraction accuracy when each split removes a *specific* model weakness (a cooperative multi-agent NER system improves zero-shot F1 by up to 13.21% on WNUT-17 and 4.49% on GENIA over the best baseline, per [CMAS, WWW 2025](https://arxiv.org/html/2502.18702v1); an agentic document pipeline reports plans 25–80% more accurate than well-engineered baselines, per [DocETL](https://arxiv.org/abs/2410.12189)). But decomposition can *invert*: a documented case shows a split failing to generalise even within one subject area ([least-to-most, ICLR 2023](https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf)), a measured multi-agent failure taxonomy attributes 41.77% of failures to specification/role/context issues and 36.94% to inter-agent misalignment ([MAST](https://arxiv.org/html/2503.13657v2)), and under fixed budgets simple repeated independent sampling *beats* agentic decomposition on accuracy-per-dollar and accuracy-per-call across all difficulty levels ([When Independent Sampling Outperforms Agentic Reasoning](https://arxiv.org/html/2605.08478v1)).
2. **Run each role independently several times** — *supported [MEASURED]*. Coverage (fraction solved by any sample) scales with the number of samples over four orders of magnitude, log-linear as an exponentiated power law ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)).
3. **Union rather than majority-select** — *conditionally supported, with a caveat [MEASURED]*. Unioning across prompts/passages lifts recall dramatically (recall-oriented union reaches 84.3% Stage-1 recall vs 38.7–49.6% for single/ensemble LLM-only baselines, per [L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); majority voting itself is *statistically indistinguishable from baseline* for open-ended tasks ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)), which supports union over majority — **but** the aggregation *policy* matters more than diversity: naive union preserves noise (union raises recall while precision falls to ~12–15%, per [L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)), so a strong downstream selector/gate is mandatory.
4. **Deterministic checks then a different-family semantic checker** — *supported [MEASURED + PROVEN]*. Same-family judges show measured leniency and correlated agreement; a landmark study across 21 judges and ~541,000 judgments proves *reliability without validity* — a judge can be perfectly self-consistent yet biased and wrong ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)); classical ensemble theory proves uncorrelated members cut added error by 1/L while correlated members do not ([Kuncheva & Whitaker, 2003](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)).
5. **One reason-coded retry before quarantine** — *supported but bounded [MEASURED]*. Retry-with-reason adds ~20% on average but shrinks each round and is near-zero on tasks the model already handles ([Self-Refine](https://arxiv.org/abs/2303.17651)).
6. **Run count follows measured new-information yield / saturation** — *supported as a method [MEASURED]*. Coverage-vs-samples curves and consensus-fidelity curves give a principled stop (95% consensus needs 11 majority-vote trials overall, 3 for easy, >50 for hard items, per [Coin Flip Judge](https://arxiv.org/html/2606.13685)); best-case-recall-vs-runs and overlap-based hidden-pool estimation give the harvesting stop ([Atomic Self-Consistency](https://aclanthology.org/2024.emnlp-main.706.pdf); [capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)).
7. **Replace stabilised roles with deterministic code** — *supported in principle, modest for some roles [MEASURED]*. Deterministic/unsupervised topic segmentation reaches F≈0.76 (Pk 0.17) and beats classic C99/TextTiling by up to 33%/24% F-measure ([AAAI 2007 segmentation](https://dias.users.greyc.fr/publications/aaai2007.pdf)) — good enough to test a code substitute for the boundary role, not obviously good enough to retire it outright.

**Net:** the field supports *independent repeated sampling + union + a strong different-family checker + deterministic gates + bounded retry + yield-driven stopping*. It is more skeptical of *heavy role decomposition and coordination* than the hypothesis assumes, and it warns that *union without a strong selector, and diversity without an accuracy measure, can add noise or false confidence.* The right posture is a controlled four-arm experiment, not adoption.

---

## 2. Component-by-component evidence table

Each row: the hypothesis claim; the strongest primary support; the strongest null/counterexample; and the tier of the individual claim (never promoting the composed architecture above STRUCTURED).

| Component (hypothesis) | Strongest primary support | Strongest null / counterexample | Claim tier |
|---|---|---|---|
| Split wide → narrow roles | Cooperative multi-agent NER +13.21% F1 WNUT-17, +4.49% GENIA over best baseline; removing a role reverts to a weaker system ([CMAS](https://arxiv.org/html/2502.18702v1)); agentic decomposition 25–80% more accurate ([DocETL](https://arxiv.org/abs/2410.12189)) | Decomposition fails to generalise within a domain ([least-to-most](https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf)); 41.77%+36.94% of MAS failures are spec/role/coordination ([MAST](https://arxiv.org/html/2503.13657v2)); k-shot beats agents per dollar and per call ([Independent Sampling](https://arxiv.org/html/2605.08478v1)) | MEASURED (both directions) |
| Repeat each role independently | Coverage scales over 4 orders of magnitude, log-linear power law; SWE-bench Lite 15.9%→56% at 250 samples with DeepSeek-Coder-V2 ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)) | Coverage rises but selection is the bottleneck; majority voting & reward models plateau beyond several hundred samples ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)) | MEASURED |
| Union rather than majority | Union of runs/passages → 84.3% Stage-1 recall vs 38.7% single ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); majority vote indistinguishable from baseline ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)) | Union keeps noise: precision ~12–15%, hallucination 38–52% after union ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); combining models not significantly better than baseline ([meta-analysis benchmark](https://www.arxiv.org/pdf/2507.15152.pdf)) | MEASURED |
| Deterministic gate immediately after each role | Exact-substring/schema/label checks are deterministic given fixed normalisation ([spaCy](https://spacy.io/usage/linguistic-features); [Kaplan & Kay](https://aclanthology.org/J94-3001.pdf) as cited in the earlier file) | GenIE/DREEAM (conventional deterministic IE) reach <5% recall on long-list extraction ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)) — code alone is not enough | PROVEN (gate) / MEASURED (limits) |
| Different-family semantic checker | *Reliability without validity*: high test–retest ≠ correctness; kappa deflation 33.8–41.3 pp on MT-Bench; consistency–bias paradox ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)); uncorrelated members cut added error 1/L ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)) | A judge weaker than the generator can only save a factor-two of labels ([LLM-as-Judge won't beat twice the data, OpenReview](https://openreview.net/pdf?id=NO6Tv6QcDs)); diversity metrics do not reliably predict accuracy ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)) | MEASURED + PROVEN |
| Narrow-question checker | FACTS Grounding decomposes then judges with three different judge models to avoid own-family bias ([DeepMind FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)) | No opened source isolates narrow-question vs full-context checker accuracy with cost — **GAP** | STRUCTURED |
| Reason-coded single retry | ~20% average gain, reason-carrying feedback ([Self-Refine](https://arxiv.org/abs/2303.17651)) | Gains shrink each round; near-zero on already-solved tasks ([Self-Refine](https://arxiv.org/abs/2303.17651)) | MEASURED |
| Yield/saturation-driven run count | Coverage-vs-samples power law ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)); best-case recall vs runs ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf)); overlap→hidden pool ([capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)); 11/3/>50 trials by difficulty ([Coin Flip Judge](https://arxiv.org/html/2606.13685)) | Non-independence of runs biases capture–recapture ([Ades et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4036210/) as cited in the earlier file) | MEASURED |
| Promote stabilised roles → code | Deterministic segmentation F≈0.76, +33%/+24% over C99/TextTiling ([AAAI 2007](https://dias.users.greyc.fr/publications/aaai2007.pdf)) | Same source: deterministic segmentation still errs (Pk 0.17); code is a candidate, not a guaranteed replacement | MEASURED |
| Frozen per-role prompts for cache economics | DeepSeek on-disk prefix cache; cache-hit input "$0.0028"/1M vs cache-miss "$0.14"/1M (deepseek-chat) — ~50× cheaper ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing); [DeepSeek caching](https://api-docs.deepseek.com/guides/kv_cache)) | Cache is best-effort; any early prompt variation breaks the hit ([DeepSeek caching](https://api-docs.deepseek.com/guides/kv_cache)) | PROVEN (provider spec) |

---

## 3. Strongest support and strongest null

**Strongest support for the composition.** Two measured pillars converge. First, *repeated independent sampling reliably widens coverage*: coverage scales with samples over four orders of magnitude, log-linear ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)), and unioning those samples is what lifts recall from 38.7% to 84.3% in long-list extraction ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)). Second, *a separate, different-family checker is the right instrument*, because self-consistency is not correctness — the largest judge study to date proves a judge can be perfectly repeatable yet biased and wrong, with chance-corrected agreement 33.8–41.3 points below raw agreement ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)), and classical theory shows only *uncorrelated* checkers cut error by 1/L ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)).

**Strongest null evidence against the composition.** The most direct threat is that *elaborate decomposition/coordination is not worth its cost*: under fixed budgets, simple repeated independent sampling beats agentic decomposition on accuracy-per-dollar and accuracy-per-model-call across all difficulty levels, a gap that persists even with prompt caching, because agents waste budget on "unproductive refinement" ([When Independent Sampling Outperforms Agentic Reasoning](https://arxiv.org/html/2605.08478v1)). This is reinforced by a measured failure taxonomy in which most multi-agent failures are design/coordination, not model, failures ([MAST](https://arxiv.org/html/2503.13657v2)), and by the finding that *mixing different models often lowers average quality* ([Self-MoA](https://arxiv.org/abs/2502.00674)). The lesson is not "don't decompose" but "decompose only where a split removes a measured error, and prefer simple parallelism to deep coordination."

---

## 4. Deterministic replacements (what code can do instead of a model)

- **Exact-quote / offset / schema / allowed-label / identity gates** are already deterministic given fixed text normalisation; this is the cheapest and most reliable layer and should run immediately after each role (the exact-substring gate is a string-membership test, per the earlier file's [spaCy](https://spacy.io/usage/linguistic-features) and [Kaplan & Kay](https://aclanthology.org/J94-3001.pdf) anchors).
- **Boundary detection** has a credible deterministic substitute: unsupervised segmentation reaches F≈0.76 and beats C99/TextTiling by up to 33%/24% ([AAAI 2007](https://dias.users.greyc.fr/publications/aaai2007.pdf)) — worth running as a code arm against the boundary role.
- **Cross-run linkage / hidden-pool estimation** are deterministic counting once "same item" is decided: overlap between independent passes estimates completeness (87.2% in a literature harvest, per [capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)).
- **What code cannot yet replace:** the semantic "does this quote back this claim / is this label right" judgement, and open-ended long-list recall — conventional deterministic IE (GenIE/DREEAM) reaches <5% recall on the long-list task ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)). These stay model roles, bounded and measured.

---

## 5. Recommended producer–checker architecture

Grounded in the measured evidence, the defensible arrangement is:

1. **Producer:** a specialist role model (DeepSeek or comparable), sampled independently several times at positive temperature to build coverage ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)).
2. **Layer-A deterministic gate (code, free, immediate):** exact-quote substring, offset-in-bounds, schema-valid, label∈closed-vocab, identity checks. Reject → one reason-coded retry → quarantine.
3. **Layer-B semantic checker (a different model family from the producer), narrow question, small answer set (accept / reject+reason-code):** required because same-family judges are measurably lenient and correlated, and because consistency is not validity ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf); [Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)). Prefer a checker not weaker than the producer, since a weaker judge saves at most a factor-two of labels ([LLM-as-Judge won't beat twice the data](https://openreview.net/pdf?id=NO6Tv6QcDs)).
4. **Aggregation = union then select, never synthesise.** Keep all candidates (union) for recall, then let the gate+checker select; do not merge candidates into one synthesised output, which loses to a single-model baseline in 82% of comparisons ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)).
5. **Validator blinding:** the checker sees only {input span, producer output, one narrow question}, not the producer's identity — mirroring FACTS Grounding's three-judge, own-family-mitigation design ([DeepMind FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)).
6. **Calibrate the checker before trusting it** with planted faults (mutation testing), reporting catch-rate per fault class and false-kill rate on known-good items ([DeepMutation](https://arxiv.org/pdf/1805.05206)).

---

## 6. Repeated-run and stopping method

Two orthogonal stops, both measured-grounded:

- **Harvesting stop (recall side):** plot best-case-recall-vs-runs; stop when an added run yields < ε new best-case recall ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf)). Estimate the hidden pool from run-to-run overlap via capture–recapture, first testing the independence assumption because non-independent runs bias the estimate downward ([capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)). Coverage itself follows a predictable power law, so the curve can be forecast rather than exhausted ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)).
- **Verdict stop (checker side):** repeat the checker until consensus fidelity reaches target — measured at 11 majority-vote trials for 95% fidelity overall, 3 for easy items, >50 for hard items ([Coin Flip Judge](https://arxiv.org/html/2606.13685)). Run count should therefore be *difficulty-adaptive*, not a fixed constant.

The internal design's fixed "3 runs" is neither endorsed nor refuted by primary evidence; it must be replaced by these curves (this is USER/REPO-ORIGINATED and not validated here).

---

## 7. Statistics (separating five different things)

The field insists these be reported separately, and the composition risks conflating them:

- **Consistency / precision** (repeats agree with each other) — ISO 5725 precision, the standard deviation across runs ([ISO 5725-1](https://www.iso.org/standard/69418.html)). **This is what the internal deep-checker RATIFY spread 0.57–0.90 measures — a precision signal, not accuracy.**
- **Trueness / accuracy** (closeness to truth) — ISO 5725 trueness, bias vs a gold ([ISO 5725-1](https://www.iso.org/standard/69418.html)). *Reliability without validity* is precisely the warning that high consistency can hide low trueness ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)).
- **Quotation validity** (quote is a literal source substring) — a deterministic string test; report accept-rate with a Wilson interval.
- **Recall / coverage** (fraction of true items found) — coverage-vs-runs and Recall@Precision ([Large Language Monkeys](https://arxiv.org/abs/2407.21787); [L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)).
- **Skewed agreement** (producer–checker agreement when rejections are rare) — use Gwet's AC1 or Krippendorff's alpha, not Cohen's kappa, because kappa collapses under rare-event skew ([Gwet AC1 vs kappa, BMC](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61); [Krippendorff](http://faculty.washington.edu/jwilker/559/Krippendorf.pdf)). The judge study quantifies the trap directly: raw "85% agreement" corresponds to chance-corrected κ ≈ 0.48 ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)).

---

## 8. Open-source reuse table (official repositories, with licence where stated)

| Project (official page) | Licence (as stated) | Reuse for this system | Exact vs model-dependent |
|---|---|---|---|
| Large Language Monkeys code ([repo](https://github.com/ScalingIntelligence/large_language_monkeys)) | not stated on the opened page — "not reported by the primary source" | reference implementation for repeated sampling + coverage/pass@k curves | model-dependent generation; exact coverage counting |
| SAFE / long-form factuality — Google DeepMind ([repo](https://github.com/google-deepmind/long-form-factuality)) | Apache-2.0 for code; CC-BY 4.0 for other materials (stated on repo) | decompose-then-check producer→checker template | model-dependent fact splitting; external search |
| CMAS cooperative multi-agent NER ([repo](https://github.com/WZH-NLP/WWW25-CMAS)) | not stated on the opened page — "not reported by the primary source" | role-decomposition reference for extraction | model-dependent roles; deterministic scaffold |
| DocETL agentic document processing ([paper](https://arxiv.org/abs/2410.12189); site docetl.org) | not stated on the opened abstract page — "not reported by the primary source" | declarative decompose→validate pipeline pattern | model-dependent operators; agent-selected plans |
| DeepMutation ([paper](https://arxiv.org/pdf/1805.05206)) | not stated on the opened page | planted-fault battery to calibrate the checker | exact mutation/catch-count; model under test |
| ISO 5725-1/2 ([standard](https://www.iso.org/standard/69418.html)) | ISO copyrighted standard | precision vs trueness reporting frame | exact statistics |
| Krippendorff's alpha ([author PDF](http://faculty.washington.edu/jwilker/559/Krippendorf.pdf)) | author copy | skew-robust agreement statistic | exact statistic |

Licences not printed on the opened page are recorded as unreported rather than guessed; confirm the repo `LICENSE` file before reuse.

---

## 9. Novelty map (established vs adapted vs apparently novel vs untested)

- **Established (measured elsewhere):** repeated independent sampling for coverage ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)); union harvesting for recall ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); producer→checker with a different family and planted-fault calibration ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf); [DeepMutation](https://arxiv.org/pdf/1805.05206)); bounded reason-carrying retry ([Self-Refine](https://arxiv.org/abs/2303.17651)); skew-robust agreement and precision/trueness split ([Gwet](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61); [ISO 5725-1](https://www.iso.org/standard/69418.html)).
- **Adapted (proven in an adjacent field, transfer is the proposal):** capture–recapture hidden-pool estimation from ecology/literature-search ([capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)); consensus-fidelity run-count curves from judge-reliability ([Coin Flip Judge](https://arxiv.org/html/2606.13685)); ensemble-error-correlation theory from classifier ensembles ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)).
- **Apparently novel (no direct prior art opened):** the *specific composition* — narrow role swarm + per-role Layer-A/Layer-B validators + union + reason-coded single retry + saturation-driven counts + deterministic promotion — as one auditable extraction engine; and a narrow-question-checker-vs-full-context-checker accuracy/cost comparison (**GAP**).
- **Untested internally:** every specialist experiment (E1–E5 in the design file) is unrun; the exact-quote 0.96, label 0.867, deep-checker 0.57–0.90 spread, and ~47% cache-hit figures are USER/REPO-ORIGINATED and not remeasured here.

---

## 10. What the field would say we are doing wrong

- **"You may be paying for decomposition you don't need."** Under fixed budgets, plain repeated independent sampling beat agentic decomposition on cost-efficiency across all difficulty levels, gap persisting through prompt caching ([Independent Sampling](https://arxiv.org/html/2605.08478v1)); most multi-agent failures are coordination, not model, failures ([MAST](https://arxiv.org/html/2503.13657v2)). Justify each role split by a measured error it removes, or drop it.
- **"Union without a strong selector just banks noise."** Union raises recall but drives precision to ~12–15% and leaves hallucination at 38–52% until a scrutiniser prunes ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); majority vote and MoA synthesis are indistinguishable-from-baseline or worse ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)). The gate/checker is not optional dressing; it is the whole value.
- **"Your consistency number is not an accuracy number."** The deep-checker RATIFY spread and cross-run agreement measure precision, not trueness; a judge can be maximally self-consistent and still wrong ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)). Report AC1/alpha with confidence intervals and a separate bias-vs-gold, never a raw agreement rate ([Gwet](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61); [ISO 5725-1](https://www.iso.org/standard/69418.html)).
- **"Same-model repeats create false consistency."** Correlated members give almost no error reduction (δ→1 in the added-error formula), so three same-model runs that agree may just be agreeing on the same mistake ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)); same-family judges tie more often (34.9% vs 28.8% cross-family, χ²=117.61) ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)).
- **"A fixed run count is arbitrary."** Required trials for a stable verdict range from 3 (easy) to >50 (hard) items ([Coin Flip Judge](https://arxiv.org/html/2606.13685)); use difficulty-adaptive curves, not "3."

---

## 11. The three highest-leverage changes (each tied to evidence)

1. **Add a real aggregation-policy arm: union-then-select, and forbid synthesis.** Union for recall is measured ([L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); synthesis loses to a single-model baseline 82% of the time and majority vote adds nothing on open tasks ([Selection Bottleneck](https://arxiv.org/html/2603.20324v1)). The single biggest lever is a strong selector/gate on top of the union, not more roles. **[MEASURED]**
2. **Make the checker a different family, not weaker than the producer, calibrated on planted faults, and report AC1/alpha + precision/trueness — never raw agreement.** Same-family judges are lenient and correlated, weaker judges save at most factor-two, and consistency ≠ validity ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf); [LLM-as-Judge won't beat twice the data](https://openreview.net/pdf?id=NO6Tv6QcDs); [DeepMutation](https://arxiv.org/pdf/1805.05206); [Gwet](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61)). **[MEASURED + PROVEN]**
3. **Replace the fixed run count with two measured stop curves (best-case-recall-vs-runs and consensus-fidelity-vs-trials) and run an ablation that includes a plain repeated-sampling arm with no roles.** Coverage/consensus curves are measured ([Large Language Monkeys](https://arxiv.org/abs/2407.21787); [ASC](https://aclanthology.org/2024.emnlp-main.706.pdf); [Coin Flip Judge](https://arxiv.org/html/2606.13685)); include the no-roles arm because it may win on cost-efficiency ([Independent Sampling](https://arxiv.org/html/2605.08478v1)). **[MEASURED]**

---

## 12. Google Research / Google DeepMind discovery notes

Explicit Google/DeepMind primary work found and used at true tier: **Self-Consistency** (sample-and-agree accuracy gains, e.g. +17.9% GSM8K, [Wang et al.](https://arxiv.org/abs/2203.11171)); **Least-to-Most** decomposition with the documented within-domain failure ([ICLR 2023](https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf)); **FACTS Grounding**, which uses three different judge models specifically "to mitigate any potential bias of a judge giving higher scores to the responses produced by a member of its own model family" ([DeepMind FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)) — a direct precedent for the different-family checker. No Google-specific primary source was found for the role-swarm-with-per-agent-validators composition itself; that gap is recorded rather than implied.

## 13. Open-source discovery notes

Reusable official code found: repeated-sampling coverage tooling ([Large Language Monkeys repo](https://github.com/ScalingIntelligence/large_language_monkeys)); the decompose-then-check SAFE template ([long-form-factuality, Apache-2.0](https://github.com/google-deepmind/long-form-factuality)); a role-decomposition NER reference ([CMAS repo](https://github.com/WZH-NLP/WWW25-CMAS)); and a declarative decompose→validate document pipeline ([DocETL](https://arxiv.org/abs/2410.12189)). Licences absent from the opened pages are recorded as unreported.

## 14. Journalism discovery trail (not an evidence tier)

Secondary write-ups on "multi-agent systems failing," "LLM-judge ensembles agreeing because they are the same family," and "prompt-cache savings" were used only to *discover* candidate primary work; every number in this report was then traced to and taken from the underlying paper, standard, or official documentation. No measured value here originates from a blog or news article; secondary-source measurements were removed from the evidence layer.

---

## 15. Internal baseline vs external prior art (USER/REPO-ORIGINATED, not remeasured)

*Everything in this section is the internal pipeline's own reported figures, supplied for relevance only and not independently re-measured here. Private repository URLs and paths are deliberately omitted.*

| Internal figure/method (USER/REPO-ORIGINATED) | External verdict | Basis in opened primary evidence |
|---|---|---|
| Wide extractor: 5,450 candidates, 96% coverage | Plausible but unverified here | Coverage rises with runs ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)); 96% is an internal claim, not remeasured |
| Exact-quote gate 0.96 at n=725 | **Unvalidated** (fills a gap the literature does not report) | No opened source reports an exact-quote-rate-before/after-with-cost pair (open gap in the earlier file) |
| Label gate 0.867 | **Unvalidated** internally-set threshold | Argument-mining human ceiling ~0.867 F1 is coincidental, not a validation ([earlier file's argument-mining anchor](https://aclanthology.org/J17-3005.pdf)) |
| Deep-checker RATIFY spread 0.57–0.90 across batches | **Consistency, not trueness — flagged** | This is precision spread; separate it from bias-vs-gold ([ISO 5725-1](https://www.iso.org/standard/69418.html); [Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)) |
| ~47% prefix-cache hit | Economically material, plausible | DeepSeek cache-hit ~50× cheaper than miss ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)) |
| Fixed 3 runs / role | **Neither endorsed nor refuted** | Use difficulty-adaptive curves instead (3–>50 trials, [Coin Flip Judge](https://arxiv.org/html/2606.13685)) |
| Grouped merge canonicalises one statement, notes extra sources | **At risk** | Collapsing to one representative risks unmeasured nuance loss (open gap in the earlier file, [ASC](https://aclanthology.org/2024.emnlp-main.706.pdf)) |

---

## 16. Evidence ledger

| Source (URL) | Type | Component(s) | Numbers? | Opened? |
|---|---|---|---|---|
| [CMAS — arXiv 2502.18702](https://arxiv.org/html/2502.18702v1) | paper | role decomposition | Yes (F1 deltas) | Yes |
| [L3X — TACL PDF](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf) | paper | union, recall, scrutiny | Yes (recall/R@P) | Yes |
| [Meta-analysis extraction — arXiv 2507.15152](https://www.arxiv.org/pdf/2507.15152.pdf) | paper | ensemble vs prompt, recall | Yes (recall deltas) | Yes |
| [Large Language Monkeys — arXiv 2407.21787](https://arxiv.org/abs/2407.21787) | paper | repeat sampling, coverage | Yes (15.9%→56%) | Yes |
| [Independent Sampling vs Agents — arXiv 2605.08478](https://arxiv.org/html/2605.08478v1) | paper | decomposition null | Yes (cost/query) | Yes |
| [DocETL — arXiv 2410.12189](https://arxiv.org/abs/2410.12189) | paper | decompose+validate | Yes (25–80%) | Yes |
| [Coin Flip Judge — arXiv 2606.13685](https://arxiv.org/html/2606.13685) | paper | run-count, judge noise | Yes (11/3/>50) | Yes |
| [Reliability without Validity — arXiv 2606.19544](https://arxiv.org/pdf/2606.19544v1.pdf) | paper | consistency≠validity | Yes (κ deflation) | Yes |
| [MAST — arXiv 2503.13657](https://arxiv.org/html/2503.13657v2) | paper | decomposition failures | Yes (mode %) | Yes |
| [Self-MoA — arXiv 2502.00674](https://arxiv.org/abs/2502.00674) | paper | mixing null | Yes (6.6%/3.8%) | Yes |
| [Selection Bottleneck — arXiv 2603.20324](https://arxiv.org/html/2603.20324v1) | paper | union vs select, family | Yes (BT-WR) | Yes |
| [Kuncheva & Whitaker 2003](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf) | paper | error correlation | Formula + caution | Yes |
| [Segmentation — AAAI 2007](https://dias.users.greyc.fr/publications/aaai2007.pdf) | paper | deterministic boundary | Yes (F/Pk/WD) | Yes |
| [DeepSeek caching docs](https://api-docs.deepseek.com/guides/kv_cache) | provider docs | cache economics | Mechanism | Yes |
| [DeepSeek pricing docs](https://api-docs.deepseek.com/quick_start/pricing) | provider docs | cache economics | Yes (prices) | Yes |
| [ASC — EMNLP 2024](https://aclanthology.org/2024.emnlp-main.706.pdf) | paper | recall ceiling, merge | Yes | Yes (earlier file) |
| [Self-Consistency — arXiv 2203.11171](https://arxiv.org/abs/2203.11171) | paper | repeat sampling | Yes | Yes (earlier file) |
| [Self-Refine — arXiv 2303.17651](https://arxiv.org/abs/2303.17651) | paper | retry | Yes (~20%) | Yes (earlier file) |
| [DeepMutation — arXiv 1805.05206](https://arxiv.org/pdf/1805.05206) | paper | planted faults | Yes | Yes (earlier file) |
| [Lightweight Pyramid — arXiv 1904.05929](https://arxiv.org/pdf/1904.05929.pdf) | paper | content-unit match | Yes | Yes (earlier file) |
| [Least-to-Most — ICLR 2023](https://webdocs.cs.ualberta.ca/~dale/papers/iclr23a.pdf) | paper | decomposition | Yes | Yes (earlier file) |
| [Gwet AC1 vs kappa — BMC](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61) | paper | skew stats | Yes | Yes (earlier file) |
| [ISO 5725-1](https://www.iso.org/standard/69418.html) | standard | precision/trueness | Definitions | Yes (earlier file) |
| [Krippendorff PDF](http://faculty.washington.edu/jwilker/559/Krippendorf.pdf) | paper | agreement stat | Yes | Yes (earlier file) |
| [capture–recapture — PMC3082794](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/) | paper | hidden pool | Yes (87.2%) | Yes (earlier file) |
| [FACTS Grounding — DeepMind](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/) | official page | different-family judges | Yes | Yes (earlier file) |
| [LLM-as-Judge won't beat twice the data — OpenReview](https://openreview.net/pdf?id=NO6Tv6QcDs) | paper | weak-judge limit | Theorem | Yes |

---

## 17. Gap register

| # | Gap | Status | Best anchor |
|---|---|---|---|
| S1 | Narrow-question checker vs full-context checker accuracy, with cost | **GAP UNRESOLVED — no prior art found** | different-family, decompose-then-judge design ([FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)) |
| S2 | Reason-coded retry recovery-rate curve by depth, with per-attempt cost, for hard-rejection retry | **GAP UNRESOLVED** | ~20% average, shrinking ([Self-Refine](https://arxiv.org/abs/2303.17651)) |
| S3 | Capture–recapture applied specifically to pooling model-extracted facts | **GAP UNRESOLVED** | 87.2% literature-harvest completeness ([capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)) |
| S4 | Measured cost/latency of role decomposition for extraction (vs a wide extractor) | **Partly open** | cost-per-dollar/query for agents vs k-shot ([Independent Sampling](https://arxiv.org/html/2605.08478v1)); CMAS/DocETL give accuracy not token cost |
| S5 | The specific role-swarm-with-per-agent-validators composition as one auditable engine | **Apparently novel — untested** | component parts measured above |
| S6 | Portable "same-idea" match threshold for union de-duplication | **GAP UNRESOLVED** (carried from earlier file) | graded-to-gold ([Lightweight Pyramid](https://arxiv.org/pdf/1904.05929.pdf)) |
| S7 | Nuance/qualifier-preservation of merge | **GAP UNRESOLVED** (carried from earlier file) | coverage/correctness only ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf)) |

---

## 18. Epistemic and routing note

This document is a **STRUCTURED synthesis**: the composed architecture is derived across sources and never promoted above STRUCTURED, while each empirical result keeps its own inline tier (**MEASURED** / **PROVEN**). No number was taken from memory; every external numeric claim links to an opened primary public source. The internal-baseline comparison is **USER/REPO-ORIGINATED and not independently re-measured**; unrun thresholds are not treated as validated. Machine action allowed: **recommend** only. The natural next step is the executable four-arm experiment in the companion agent document `specialist-extraction-swarm-experiment__agent__2026-07-12T20-50-00Z__perplexity.pplx.md`. This is a reading/answer artifact for the system of record **local_workspace** and must not be written directly to any knowledge store.
