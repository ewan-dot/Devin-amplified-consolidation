# LLM Consistency & Reliability: Hard Numbers (2025–2026)

**Compiled:** June 2026  
**Purpose:** Evidence-based audit of the claim "AI is brilliant but inconsistent" — with hard data on frontier LLM coding agents, specifically at moderate context utilisation (~50%), on well-bounded tasks.

---

## Executive Summary

The short answer: **On a well-bounded, clearly specified coding task at ~50% context utilisation, a frontier LLM agent achieves a first-attempt (pass@1) success rate in the range of 60–80%, with run-to-run variance of ±2–6 percentage points, and a full-consistency rate (pass^8, meaning all 8 runs correct) that can drop to 25–50% even on tasks the model "mostly" solves.** The inconsistency is real, not a myth — but it is task-structure-dependent, context-load-dependent, and meaningfully improvable by bounding the task well and keeping context below the 50% threshold. The "brilliant but inconsistent" framing holds, with an important nuance: reliability and accuracy are diverging metrics that have been improving at very different rates.

---

## 1. PASS@1 vs PASS@K: Run-to-Run Variance on Coding Benchmarks

### Key finding: Single-run scores are statistically unreliable; variance is 2–6 pp even at temperature 0.

**Bjarnason et al. (KTH/arXiv, 2025) — "On Randomness in Agentic Evals"**  
Source: https://arxiv.org/abs/2602.07150  
The most rigorous study to date. Collected 60,000 agent trajectories across 10 independent runs each of 6 agent configurations on SWE-Bench-Verified (500 tasks × 10 runs).

Key results:
- **Single-run pass@1 estimates vary by 2.2 to 6.0 percentage points** depending on which run is selected.
- **Standard deviation: 1.5 pp**, even at temperature 0.
- A reported improvement of 2–3 pp between two models may be pure evaluation noise, not genuine progress.
- **Gaps between optimistic and pessimistic bounds:**
  - DeepSWE-preview on r2e-gym: pass@1 = 34.4%, pass@5 = 52.9% (+18.5 pp), passˆ5 = 15.5% (−18.9 pp)
  - Devstral-2 on nano-agent: pass@1 = 63.5%, pass@5 = 76.2% (+12.7 pp), passˆ5 = 49.1% (−14.4 pp)
  - Maximum gap across all configurations: **24.9 percentage points** between best-case (pass@5) and worst-case (passˆ5).
- **Temperature 0 does not suppress variance.** Counter-intuitively, some configurations show *higher* variance at temp 0 than at temp 0.6 (e.g. Qwen3-32B: σ=0.7% at temp 0.6 → σ=1.2% at temp 0). Trajectories still diverge, median divergence at token position 5 (default temp) or position 32–56 (temp 0), always within the first 1% of the total trajectory.

**What pass@k vs passˆk reveals about "consistency":**

| Metric | Definition | What it measures |
|--------|-----------|-----------------|
| pass@1 | Mean single-run success | Average first-attempt probability |
| pass@k | P(at least 1 success in k tries) | Optimistic ceiling / best-day performance |
| passˆk | P(all k runs succeed) | Consistency floor / production reliability |

The gap between pass@k and passˆk is the **stochastic exploration gap** — how much of the model's apparent capability depends on lucky draws rather than deterministic problem-solving.

**SWE-rebench (continuous benchmark, 2025–2026)**  
Source: https://swe-rebench.com  
Runs every model 5 times per task on SWE-Bench-Verified, reporting mean, SEM, pass@5, and 5/5 consistency count.
- Claude Opus 4.6: mean ~38%, pass@5 = 40 tasks, **5/5 consistency = 34 tasks**
- GLM-5: pass@5 = 40 tasks, 5/5 consistency = 30 tasks (same ceiling, less reliable floor)
- DeepSeek-V3.2: pass@5 = 42 tasks, 5/5 consistency = 24 tasks (broadest coverage, least stable)

**τ-bench (Sierra Research, 2024–2025) — pass^k for tool-use agents**  
Source: https://arxiv.org/abs/2406.12045 | https://github.com/sierra-research/tau-bench

Measures whether agents can consistently solve the same task repeated k times. Retail and airline customer-service domains.

| Model | Domain | Pass^1 | Pass^2 | Pass^3 | Pass^4 | Pass^8 |
|-------|--------|--------|--------|--------|--------|--------|
| Claude 3.5 Sonnet (Oct 2024) | Retail | 0.692 | 0.576 | 0.509 | 0.462 | ~0.25* |
| GPT-4o | Retail | 0.604 | 0.491 | 0.430 | 0.383 | <0.25 |
| Claude 3.5 Sonnet (Oct 2024) | Airline | 0.460 | 0.326 | 0.263 | 0.225 | — |
| GPT-4o | Airline | 0.420 | 0.273 | 0.220 | 0.200 | — |

*Pass^8 confirmed in Sierra's blog post: GPT-4o drops to ~25% in retail, a 60% relative drop from pass^1.

Source: https://sierra.ai/blog/benchmarking-ai-agents (June 2024)  
"Even state-of-the-art agents, such as those based on GPT-4, succeeded in fewer than 50% of tasks and struggled with consistency — achieving only ~25% success when repeating the same task eight times."

**Verdent Technical Report (Feb 2026) — cross-provider SWE-bench variance**  
Source: https://www.verdent.ai/ko/guides/claude-sonnet-5-swe-bench-verified-results
- Cross-provider gap (same model, different API endpoint): up to **1.2 pp** in pass@1
- Amazon Bedrock showed noticeably higher run-to-run variance than direct API access
- Claude Sonnet 4.5: pass@1 = 76.1%, pass@3 = 81.2% (on full 500 problems)

**HumanEval data point:**  
- GPT-4: pass@1 ≈ 88.4% on HumanEval, drops to 76.2% on HumanEval+ (harder test suite) — a 12 pp gap from benchmark hygiene alone.
- Frontier models in 2026 reach 80–90% pass@1 on standard HumanEval, but drop 20–31 pp on anti-contamination variants (HumanEvalNext).

**Princeton "Science of AI Agent Reliability" (Feb 2026)**  
Source: https://arxiv.org/abs/2602.16666  
Authors: Rabanser, Kapoor, Kirgis, Liu, Utpala, Narayanan  
Evaluated 14 frontier models across two benchmarks. Core finding:  
- **Pass@1 metrics overestimate true reliability by 20–40 percent.**
- Accuracy has improved ~7x faster than reliability on customer-service benchmarks since 2023.
- Outcome Consistency (C_out) scores for best models: **Claude Opus 4.5: 73%, Gemini 3 Pro: 85% (best overall reliability score), but safety score for Gemini 3 Pro only 25%.**
- "Reliability has barely budged" despite rapid capability gains across 18 months of frontier model releases.

---

## 2. Context Window Degradation: What Happens as Context Fills Up

### Key finding: Performance degrades at every increment; the 50% threshold is a phase transition point.

**Liu et al. (Stanford/TACL 2024) — "Lost in the Middle"**  
Source: widely cited; see Redis summary at https://redis.io/blog/context-rot/  
The foundational study. Multi-document QA with 20 documents (~4,000 tokens):
- Accuracy at position 1 or 20: **70–75%**
- Accuracy at positions 5–15 (middle): **55–60%**
- **Drop: 15–20 percentage points** based purely on information position
- **30%+ accuracy drops** when key document is in middle positions vs edge positions
- Effect holds across multiple model families

**Veseli et al. (2025) — "Positional Biases Shift as Inputs Approach Context Window Limits"**  
Source: https://openreview.net/pdf/1fa87a52bb87f4535aa4c24f858f215c6d329083.pdf

Critical refinement of the lost-in-the-middle finding:
- The U-shaped curve (middle content lost) holds **only when context < 50% full**
- **Above 50% utilisation:** primacy bias weakens dramatically; the curve shifts to a raw recency gradient — earliest tokens are now most vulnerable to loss
- **Near capacity (>80%):** no U-shape at all; pure distance-based bias where only the most recent tokens are reliably attended to
- Implication: below 50% you lose the middle; above 50% you lose the beginning; near full capacity you lose almost everything except the end

**Practical consequence for the user's question:** Operating at ~50% context is genuinely a phase-transition threshold. Below it, the model's attention pathology is "lost in the middle" — manageable with prompt engineering (put key info at edges). Above it, the model starts forgetting earlier instructions and context, creating a fundamentally different failure mode.

**NoLiMa Benchmark (Adobe Research, ICML 2025)**  
Source: https://icml.cc/virtual/2025/poster/46685 | https://github.com/adobe-research/NoLiMa  
Evaluated 12–13 frontier LLMs on non-lexical matching tasks at varying context lengths:

| Model | Base Score (short) | At 8K | At 16K | At 32K | Effective Length |
|-------|-------------------|-------|--------|--------|----------------|
| GPT-4o | 99.3% | ~82% | 81.6% | 69.7% | 8K |
| GPT-4.1 | 97.0% | — | — | 79.8% | 16K |
| Gemini 2.5 Flash | 94.4% | 68.2% | 57.9% | 48.4% | 2K |
| Llama 3.3 70B | 97.3% | 72.1% | 59.5% | 42.7%* | 2K |
| Claude 3.5 Sonnet | 87.6% | 61.7% | 45.7% | 29.8%* | 4K |
| GPT-o3 (reasoning) | 100% | 94.4% | 86.2% | 74.9% | >32K |

*Italics = below 50% of base score  
**"Effective Length"** = longest context at which model maintains ≥85% of base score. Most models: 2–8K tokens, far below their claimed 128K–1M maximums.  
**At 32K tokens, 11 out of 12 models drop below 50% of their short-context baseline.**

**Chroma Research (2025) — Context Rot on 18 Frontier Models**  
Source: https://www.trychroma.com/research/context-rot  
"Every single one of 18 frontier models gets worse as input length increases — not just near the limit, but at every increment."

**Levy et al. (arXiv, October 2025) — "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval"**  
Even with 100% perfect retrieval of relevant information, performance degrades **13.9% to 85%** as input length increases. The degradation mechanism is not retrieval failure — it is the model's inability to reason effectively over longer inputs regardless of information availability.  
Source referenced in: https://diffray.ai/blog/context-dilution/

**Financial retrieval tasks (Gupta et al., 2024):**  
F1 score drops from near **0.99 at 4K tokens to 0.40 or lower at 128K tokens** for single-concept queries.  
Source: https://www.emergentmind.com/topics/context-degradation-in-llms

**Multi-turn dialogue (Hankache et al., 2025):**  
Relative accuracy drops of up to **73%** for certain models when prior context is extended.

**Paulsen (2025) — Maximum Effective Context Window (MECW)**  
Source: https://arxiv.org/pdf/2509.21361  
Tested 11 LLMs across problem types:
- All models fell short of advertised context windows by **more than 99%** on complex tasks
- Some top models showed accuracy degradation with as **little as 100 tokens** of context on complex reasoning
- Most showed clear degradation by 1,000 tokens
- Simple needle-in-haystack: MECW ≈ 3,000–5,000 tokens
- Complex sorting/summarization: MECW ≈ 400–1,200 tokens

### The 50% Rule: Is There Evidence It Materially Helps?

The Veseli et al. (2025) study provides the most direct evidence. Below 50% context utilisation, the LiM (Lost-in-the-Middle) effect is "strongest" — but the model still has a functioning primacy bias (beginning is safe) and recency bias (end is safe). Above 50%, primacy bias collapses, leaving only a recency gradient on a lower performance floor. The 50% boundary is therefore a structural threshold in transformer attention mechanics, not just a rule of thumb. It does not eliminate degradation but it preserves a different (and more manageable) failure mode.

---

## 3. Bounded vs Unbounded Task Reliability: Does Clear Scope Raise Consistency?

### Key finding: Ambiguity in task specifications causes 7–40 pp drops in pass@1; clear scoping measurably narrows variance.

**arXiv 2026 — "Assessing the Impact of Requirement Ambiguity on LLM-based Code Generation"**  
Source: https://arxiv.org/html/2604.21505v1  

- Ambiguous specifications reduce pass@1 accuracy by an average of **7.22 percentage points** across models
- The **largest observed decline: 31.10 percentage points** (GPT-4 on highly ambiguous specs)
- GPT-4 conflict rate (generating mutually incompatible implementations): **14.09% on clear specs → 28.29% on ambiguous specs** (2x increase)
- DeepSeek-V3 conflict rate: **6.83% → 17.45%** (2.5x increase)
- Even state-of-the-art models "fail to identify or resolve ambiguity autonomously"
- "Performance gap exceeds 30% when confronted with ambiguous specifications"

**arXiv 2025 — "Evaluating Code Model Robustness to Ambiguous, Contradictory, and Incomplete Task Descriptions"**  
Source: https://arxiv.org/html/2507.20439v1  
Using controlled mutations of HumanEval and MBPP:
- Ambiguous descriptions: **25–30% reduction in pass@1** vs clear descriptions
- Incomplete descriptions: **20–25% reduction in pass@1**
- **Contradictory descriptions: up to 40% reduction**; GPT-4 drops from 73.8% → 6.7% on HumanEval (contradictory)
- 60–90% of code that compiles is semantically incorrect under unclear descriptions

**CSE Buffalo (2026) — "Evaluating Variance and Reliability of LLM-Powered Semantic Operators"**  
Source: https://cse.buffalo.edu/tech-reports/2026-10.pdf  
- Well-defined queries: **reliably low variance**
- Ambiguous queries: **significantly higher variance and inconsistency**
- "Ambiguity significantly increases output variance and decreases reliability"

**The Gap Between SWE-bench Verified and Real-World Variants (2026 data):**  
The same pattern manifests at benchmark level. As tasks shift from narrow/well-scoped to broader/less-specified:
- SWE-bench Verified (isolated bug fixes, 500 tasks): frontier models score **70–80%**
- SWE-bench Pro (private repos, longer-horizon): drops to **~23–46%**
- SWE-EVO (multi-file, evolution-style changes): GPT-5 drops from 65% → **21%**
- SWE-bench Live (continuously updated, anti-contamination): **19–43%**

Source: https://agentmarketcap.ai/blog/2026/04/10/reliability-vs-peak-capability-benchmarks-2026-evaluation-split  
"A 44-percentage-point gap between a number that appears on a leaderboard and a number that predicts production behavior."

---

## 4. Compounding / Multi-Step Decay: What Happens Over Agent Trajectories

### Key finding: Mathematical compounding is real and brutal; empirical data is consistent with theory but real agents typically perform worse than p^n due to cascading errors.

**The Mathematics (verified by multiple sources):**

| Per-Step Accuracy | 5 Steps | 10 Steps | 20 Steps | 50 Steps |
|------------------|---------|---------|---------|---------|
| 99% | 95.1% | 90.4% | 81.8% | 60.5% |
| 97% | 85.9% | 73.7% | 54.4% | 21.8% |
| 95% | 77.4% | 59.9% | 35.8% | 7.7% |
| 90% | 59.0% | 34.9% | 12.2% | 0.5% |
| 85% | 44.4% | 19.7% | 3.9% | ~0% |

Source: https://agentmarketcap.ai/blog/2026/04/14/agent-compound-reliability-problem-multi-step-error-rates

**METR — "Measuring AI Ability to Complete Long Tasks" (Kwa et al., arXiv 2025)**  
Source: https://arxiv.org/pdf/2503.14499v3.pdf | https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/

METR measured AI task completion as a function of human-equivalent task duration on a diverse software/reasoning task set:
- **Near 100% success on tasks taking humans < 4 minutes**
- **< 10% success on tasks taking humans > 4 hours**
- **50% time horizon for Claude 3.7 Sonnet (early 2025): ~50 minutes** (tasks a human finishes in 50 mins)
- For o3 (2025): 50% time horizon ~110 minutes
- METR Wikipedia (May 2026): Claude Mythos 50% horizon ≥ 16 hours, 80% horizon = 3 hours 6 minutes

Under a constant-hazard assumption:
- 50% success at 50-minute tasks → 90% success only at ~7-minute tasks
- 99% success only at tasks of ~43 seconds

Source: https://yodolabs.jp/en/research/multi-step-agent-reliability citing Kwa et al.

**UC Berkeley — "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al., NeurIPS 2025)**  
Over 1,600 execution traces across 7 popular multi-agent frameworks, 14 failure modes identified:  
- Failure rates reached **86.7%** in frameworks like OpenHands and MetaGPT on cross-application tests  
- Failure rates on open-source multi-agent systems: **41% to 86.7%**

Source: https://yodolabs.jp/en/research/multi-step-agent-reliability

**WebArena (real-world web tasks):**  
- GPT-4/Claude 3.5 on 10–15-step tasks: **35–40% success rate**
- On 20-step tasks: **20–25%** — roughly consistent with p^n at 95% per-step accuracy
- Actual rates often worse than theoretical due to cascading failures (14–18% additional gap)

Source: https://ainews.cool/article/20260423-ai-agent-accuracy-failure-rate

**Wand.ai production analysis:**  
"A 1% per-token error rate — an error rate that feels almost negligible — compounds to 87% cumulative failure by token 200."  
Source: https://www.zartis.com/the-compounding-errors-problem

**APEX-Agents 2026 benchmark:**  
Even best-performing models completed only **24% of real-world multi-step tasks on first attempt.**  
"AI agents using frontier models demonstrate failure rates exceeding 91% for complex office automation tasks."  
Source: https://agentmarketcap.ai/blog/2026/04/14/agent-compound-reliability-problem-multi-step-error-rates

**Independent/decentralised multi-agent vs. centralised:**  
Independent architecture amplifies errors **17.2×** vs single-agent baseline;  
Centralised coordination limits this to **4.4×**.  
Source: https://www.zartis.com/the-compounding-errors-problem

---

## 5. Temperature 0 / Determinism: Is It Actually Deterministic?

### Key finding: Temperature 0 is not deterministic in production. GPT-4 generates 30 unique outputs in 30 runs at temp=0. The sources of variance are structural and unavoidable without extreme measures.

**The 152334h experiment (2023, confirmed in later reviews):**  
Source: https://152334h.github.io/blog/non-determinism-in-gpt-4/  
30 API calls to GPT-4 at temperature=0, same prompt. Result:
- **GPT-4: 30 unique completions out of 30 runs** at temperature 0
- GPT-3.5-turbo (presumably denser architecture): **3.67 unique completions on average**
- Hypothesis confirmed: GPT-4's non-determinism is caused by Sparse MoE architecture with batch-level (not sequence-level) determinism

North Denver Tribune evidence map summary: GPT-4 = 11.67 unique completions / 30 runs at temp=0 (different test; GPT-3.5-turbo = 3.67 average)  
Source: https://northdenvertribune.com/ai-analysis/evidence-map-llm-technical-phenomena-research-status/

**OpenAI Community Forum (GPT-4o, 2024):**  
Source: https://community.openai.com/t/deterministic-results-impossible-for-gpt-4o/1059584  
10 API calls to GPT-4o with temp=0, seed set, same system fingerprint:  
- **5 unique responses** out of 10 calls (1 response × 4, 1 × 3, 3 × 1)

**Bjarnason et al. (KTH, 2025/2026):**  
On SWE-Bench-Verified at temperature 0:  
- DeepSWE-preview (nano-agent, temp 0): **20.4 ± 1.0%** (range: 18.2%–21.4%)
- Qwen3-32B (R2E-Gym, temp 0): **22.3 ± 1.8%** (range: 19.8%–25.2%)
- **Variance sometimes higher at temp 0 than at temp 0.6**

Source: https://arxiv.org/abs/2602.07150

**Thinking Machines Lab (2025) — "Defeating Nondeterminism in LLM Inference"**  
Source: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/  
Root causes identified:
1. **Batch-size variation:** same request processed in different batch sizes → different outputs
2. **Kernel non-invariance:** FlashAttention/KV kernels lack batch-invariant behaviour
3. **Floating-point non-associativity:** GPU parallel reduction order changes summation result
4. **Speculative decoding & continuous batching** (vLLM, TGI) add further sources

"Non-determinism is structural, not a bug."

**Structural sources of variance in production APIs:**
- Mixture-of-Experts (MoE) routing: batch-level determinism only; cross-request expert token competition
- Multi-GPU sharding: different reduction paths
- Datacenter routing: different GPU types / hardware generations
- Continuous batching: request arrives in different batch contexts

**"API variance is reported at ~38% even with deterministic sampling"**  
Source: https://northdenvertribune.com/ai-analysis/evidence-map-llm-technical-phenomena-research-status/

**Yuan et al. (NeurIPS 2025) — "Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference"**  
Formally characterises floating-point non-associativity as the fundamental source; proposes mitigation strategies requiring significant performance trade-offs.

---

## 6. Direct Answer: How Consistent is a Frontier LLM Agent on a Well-Bounded Task at ~50% Context?

### The Number

**On a well-bounded, clearly specified, single-step coding task (HumanEval-class difficulty) at ~50% context utilisation:**
- **Pass@1: 70–85%** for top frontier models in 2026 (Claude Opus 4.x, GPT-5.x, Gemini 3.x)
- **Run-to-run standard deviation: ±1.5–1.8 pp**
- **Single-run estimate can land anywhere in a ±3–6 pp window** (not the true mean)

**For a short, isolated, well-constrained coding task with no ambiguity and short context (< 50% utilisation):**
- Pass@1 approaches **90–95%** on standard benchmarks for frontier models
- PassˆK consistency (all k runs correct): at k=4, this drops to roughly **70–80%**

**For a realistic agentic coding task (multi-file, GitHub issue, ~5–10 steps):**
- Pass@1: **35–65%** (SWE-bench Verified range across frontier models, 2025–2026)
- PassˆK at k=5: estimated **15–35%** based on SWE-rebench data
- The gap between "can it do it sometimes" and "does it do it every time" is **20–30 pp**

**The inconsistency is real, not overstated — but it is structured:**

| Condition | Typical pass@1 | Typical consistency (passˆ4–8) |
|-----------|---------------|-------------------------------|
| Simple, bounded, short-context coding task | 85–95% | 70–85% |
| Mid-complexity coding task, ~50% context | 65–80% | 45–65% |
| Multi-step agent, full SWE-bench-class | 35–65% | 15–40% |
| Same tasks with ambiguous specs | subtract 7–31 pp | variance roughly doubles |
| >50% context utilisation | subtract 10–30+ pp | additional degradation |
| Real-world vs benchmark gap | subtract 20–44 pp | production reliability far lower |

---

## 7. Data Gaps and Caveats

1. **No published study directly measures pass@K at exactly "50% context utilisation" as an independent variable.** The Veseli et al. (2025) study identifies 50% as a phase-transition threshold in positional bias, and the Chroma/NoLiMa/Paulsen studies show monotonic degradation with context length, but isolating the 50% mark vs 25% or 75% in a single controlled experiment on agentic coding tasks has not been done to this researcher's knowledge as of mid-2026.

2. **Most run-to-run variance studies use open-weights or mid-tier models.** Bjarnason et al. used Qwen3-32B, DeepSWE-preview, and Devstral-2 — not Claude Opus 4.x or GPT-5. The τ-bench data uses GPT-4o and Claude 3.5 Sonnet (Oct 2024). Direct pass^K data for the newest frontier models (Claude Opus 4.6+, GPT-5.x) is from commercial blogs/leaderboards, not peer-reviewed studies.

3. **Benchmark contamination inflates pass@1 figures.** HumanEval variants that minimise contamination (HumanEvalNext, HumanEval-T) show 20–31 pp drops vs standard HumanEval. The "well-bounded task" advantage is partly a function of whether the task is novel or in-distribution.

4. **The METR time-horizon data assumes a constant-hazard model.** Real agent failure is not uniformly distributed across steps — some failure modes are early (plan errors), some late (verification failures). The p^n model is a lower bound; real sequential failure rates are often worse due to error propagation (Cemri et al. NeurIPS 2025 confirmed 14 distinct failure modes).

5. **"Well-bounded" is a spectrum.** Studies confirm the direction (clearer = better), but the magnitude of improvement from specification quality varies significantly by model, task domain, and ambiguity type. The 7–40 pp range reflects real heterogeneity.

---

## 8. Verdict on "AI is brilliant but inconsistent"

**The claim is substantially true, but the inconsistency is not uniformly distributed.**

- **For the ideal case** (short, well-specified, novel task, < 50% context): frontier models in 2026 are genuinely consistent — pass@1 of 85–95%, run-to-run standard deviation of ~1.5 pp. The inconsistency here is mostly statistical noise, not a fundamental reliability problem.

- **For anything resembling real agentic use** (multi-step, semi-ambiguous, real codebase): the gap between "can solve" (pass@k) and "reliably solves" (passˆk) is 15–25 pp. A model that "passes" a task 65% of the time will pass it every time in 8 consecutive runs at roughly 3–8% (0.65^8 ≈ 0.032). This is the actual inconsistency users experience in production.

- **The consistency gap is NOT narrowing as fast as the capability gap.** Princeton's Narayanan-Kapoor (2026) paper is the sharpest evidence: accuracy has improved 7× faster than reliability on customer-service benchmarks. A model can get dramatically better at solving problems while remaining equally unpredictable about *which* problems it will solve on a given run.

- **The 50% context threshold matters.** It is not a magic number, but it is a real phase transition. Below it, information placement determines which content is lost. Above it, the failure mode shifts and compounds. Staying below 50% is a meaningful engineering choice that preserves the more manageable failure mode.

---

## Source Index

| Source | URL | Date | Key Data |
|--------|-----|------|----------|
| Bjarnason et al. (KTH), "On Randomness in Agentic Evals" | https://arxiv.org/abs/2602.07150 | 2025/2026 | 60K trajectories; 2.2–6.0 pp single-run variance; 24.9 pp pass@k gap |
| Sierra Research, τ-bench | https://arxiv.org/abs/2406.12045 | 2024 | GPT-4o pass^8 <25% in retail; consistency data table |
| τ-bench GitHub | https://github.com/sierra-research/tau-bench | 2024 | Full pass^1 to pass^4 tables |
| SWE-rebench | https://swe-rebench.com | 2025–2026 | 5-run consistency data; Claude Opus 4.6 leads on reliability |
| Rabanser et al. (Princeton), "Science of AI Agent Reliability" | https://arxiv.org/abs/2602.16666 | Feb 2026 | 12 reliability metrics; pass@1 overestimates by 20–40% |
| Liu et al., "Lost in the Middle" (Stanford/TACL) | Referenced in: https://redis.io/blog/context-rot/ | 2023/2024 | 30% accuracy drop middle positions; U-curve |
| Veseli et al., "Positional Biases Shift" | https://openreview.net/pdf/1fa87a52bb87f4535aa4c24f858f215c6d329083.pdf | 2025 | 50% context threshold; phase transition in LiM effect |
| NoLiMa (Adobe Research, ICML 2025) | https://icml.cc/virtual/2025/poster/46685 | 2025 | Full table: GPT-4o 99.3%→69.7% at 32K; 11/12 models <50% at 32K |
| Chroma, "Context Rot" (18 models) | https://www.trychroma.com/research/context-rot | 2025 | All 18 models degrade at every context length increment |
| Levy et al., "Context Length Alone Hurts" | Referenced in: https://diffray.ai/blog/context-dilution/ | Oct 2025 | 13.9–85% degradation despite perfect retrieval |
| Paulsen, MECW (2025) | https://arxiv.org/pdf/2509.21361 | Sep 2025 | Effective context often <1% of advertised; degradation at 100–1000 tokens |
| Bjarnason ambiguous specs | https://arxiv.org/html/2604.21505v1 | Apr 2026 | 7–31 pp pass@1 drop; 2× conflict rate under ambiguity |
| Code robustness to unclear specs | https://arxiv.org/html/2507.20439v1 | 2025 | 25–40% pass@1 drop; GPT-4: 73.8%→6.7% on contradictory |
| METR, Long Task Completion | https://arxiv.org/pdf/2503.14499v3.pdf | Mar 2025 | 50% time horizon: ~50 min (Claude 3.7), ~110 min (o3) |
| METR Time Horizons | https://metr.org/time-horizons/ | Updated May 2026 | Claude Mythos: 80% horizon = 3h 6min |
| Cemri et al. (Berkeley), NeurIPS 2025 | Referenced in: https://yodolabs.jp | 2025 | 86.7% failure rate in multi-agent frameworks |
| Compound error trap (WebArena data) | https://ainews.cool/article/20260423-ai-agent-accuracy-failure-rate | Apr 2026 | 10–15 step tasks: 35–40%; 20-step: 20–25% |
| 152334h GPT-4 MoE non-determinism | https://152334h.github.io/blog/non-determinism-in-gpt-4/ | 2023 | 30 unique completions/30 runs at temp=0 |
| Thinking Machines Lab non-determinism | https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | Sep 2025 | Structural sources of temp-0 variance |
| Verdent SWE-bench Claude Sonnet 4.5 | https://www.verdent.ai/ko/guides/claude-sonnet-5-swe-bench-verified-results | Feb 2026 | pass@1=76.1%, pass@3=81.2%; 1.2 pp cross-provider gap |
| SWE-rebench leaderboard | https://swe-rebench.com | 2025–2026 | Claude Opus 4.6: 34 tasks 5/5 consistent vs 40 tasks pass@5 |
| Hippocampus Garden, pass^k vs pass@k | https://hippocampus-garden.com/pass_k/ | Oct 2025 | Mathematical comparison; same 0.5 mean → 500× difference in continuous success |
| Product Talk, Context Rot | https://www.producttalk.org/context-rot/ | Feb 2026 | Veseli et al. synthesis; 50% threshold explanation |
| Atlan, Context Window Limitations 2026 | https://atlan.com/know/llm-context-window-limitations/ | Feb 2026 | 99% MECW gap; 30%+ accuracy drops |
| Princeton reliability findings (Fortune) | https://fortune.com/2026/03/24/ai-agents-are-getting-more-capable-but-reliability-is-lagging-narayanan-kapoor/ | Mar 2026 | 7× accuracy-reliability gap on customer service |
| Yodo Labs multi-step synthesis | https://yodolabs.jp/en/research/multi-step-agent-reliability | May 2026 | Synthesis of METR + Princeton + Berkeley data |
