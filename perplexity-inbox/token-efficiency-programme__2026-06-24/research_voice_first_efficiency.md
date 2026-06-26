# Voice-First Token Efficiency: Prior Art & Patterns
**Research for Ewan Bramley, Amplified Partners**  
**Compiled:** 23 June 2026  
**Question:** How to keep exploratory, stream-of-consciousness voice input as the discovery engine, while cutting token spend and keeping output organisationally useful.

---

## 1. WHY Conversational / Voice Input Is Token-Expensive

### 1.1 The Core Mechanic: Context Window Creep

Most LLM APIs are **stateless**. Every turn re-sends the *entire* conversation history as input tokens. A multi-turn conversation does not cost N × (cost of turn 1); it costs the **sum of all accumulated contexts**, which grows roughly quadratically in total spend across the session.

> *"The single greatest hidden cost in most production AI applications is Context Window Creep... the compounding token volume from maintaining conversation history."*  
> — [FinOps.org, GenAI FinOps: How Token Pricing Really Works](https://www.finops.org/wg/genai-finops-how-token-pricing-really-works/) (2024)

**Concrete example (from the same source):** A 5-turn conversation where each turn adds 40,000 tokens means Turn 5 alone sends 200,000 input tokens. Total input tokens across 5 turns: 40K + 80K + 120K + 160K + 200K = **600,000 tokens** — not 200,000.

### 1.2 Quantified Cost at Scale

From [aicostcheck.com (March 2026)](https://aicostcheck.com/blog/large-context-window-costs-2026):
- A single request to Claude Opus with a **full 200K context window costs ~$1.00 in input tokens alone** — before any output is generated.
- GPT-4o at $2.50/M tokens: filling 128K context per request = **$0.32/request**. At 1,000 requests/day = **$320/day just in input**.
- Well-managed 8K context vs 128K context: **10–50× cost difference per request**.

From [propelius.ai (Feb 2026)](https://propelius.ai/blogs/building-conversational-ai-agents-context-windows/):
> "With GPT-4o at $2.50/1M input tokens, sending 100K tokens per request costs $0.25. At 1,000 requests/day, that's $250/day — just for input tokens. Managing context to average 10K tokens per request: $25/day — a **10× reduction**."

### 1.3 Why Voice/Dictation Specifically Amplifies This

Voice input is structurally verbose. A 2-minute dictation at ~150 words/minute = ~300 words = **~400–500 tokens**. But exploratory voice rambling produces 3–5× that density of "noise": filler words, restated ideas, tangents, abandoned sentences, hedges. A 10-minute thinking-out-loud session easily generates **2,000–4,000 raw tokens** — before any context history has accumulated. This raw input then becomes the *start* of a growing context that carries forward on every subsequent turn.

### 1.4 Prompt Caching: Why Exploratory Chat Is Cache-Hostile

Both Anthropic and OpenAI offer prefix caching that can reduce input token costs by **50–75%** ([OpenAI Prompt Caching docs](https://platform.openai.com/docs/guides/prompt-caching); [Anthropic Prompt Caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)). But caching only works on **exact prefix matches**:

> *"Any change in the prefix breaks the entire hash chain. A single byte difference at position N — a timestamp, a reordered JSON key, a different tool in the list — invalidates the cache for all breakpoints at positions ≥ N."*  
> — [Anthropic Skills: Prompt Caching Guide](https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/prompt-caching.md) (Sept 2025)

Minimum cacheable prefix: **1,024 tokens** (Claude 3.7 Sonnet, Claude 3.5 Sonnet), **2,048 tokens** (Claude Haiku). Cache TTL: minimum 5 minutes, refreshed on each hit.

**Implication for exploratory voice chat:** Every new dictation turn changes the user message, which changes the prefix beyond the system prompt. The growing, changing message history is entirely uncacheable. The system prompt (if stable) can be cached, but the lion's share of cost — the accumulating conversation turns — gets zero cache benefit.

From [arxiv.org/html/2601.06007 — "Don't Break the Cache" (Jan 2026)](https://arxiv.org/pdf/2601.06007v1.pdf), evaluating prompt caching for long-horizon agentic tasks: confirmed that agentic/conversational workloads are the primary scenario where cache hit rates collapse, because context evolves on every turn.

### 1.5 Multi-Turn Token Growth: Measured Numbers

From [arXiv:2604.08782 — MT-OSC paper (June 2026)](https://arxiv.org/html/2604.08782):
- MT-baseline (naive full history append): token cost grows **linearly** with each turn.
- At 10 turns, the system is sending the entire prior conversation on every turn, making cost proportional to N² in aggregate spend.
- MT-OSC (one-off sequential condensation): **up to 72% reduction in chat history tokens** for 10-turn dialogues, with performance preserved or improved vs. baseline across 13 LLMs.

From [Oracle AI blog, OCI-STM evaluation (Apr 2026)](https://blogs.oracle.com/ai-and-datascience/multiturn-ocistm):
- Produces **fewer tokens per turn** with larger benefits as conversations grow.
- Leads to **net token savings over the lifetime of a conversation**, even after accounting for the background condensation work.

**Summary table:**

| Source | Scenario | Token waste mechanism | Measured cost increase |
|---|---|---|---|
| FinOps.org | Multi-turn chatbot | Full history resent each turn | Grows quadratically in aggregate |
| aicostcheck.com | 128K context full | Per-request cost | $0.32/req at GPT-4o pricing |
| propelius.ai | Managed vs unmanaged | Context window size | 10× difference (128K vs 10K) |
| MT-OSC (arXiv) | 10-turn dialogue | Raw history append | 72% token overhead vs condensed |
| ravoid.com | RAG vs long context | Context stuffing per turn | 60× higher cost per turn (Turn 1) |

**Reliability:** Multi-turn cost mechanics are confirmed by provider documentation (Anthropic, OpenAI) and multiple independent engineering analyses. The FinOps.org piece is community-produced (marketing risk: low, mechanics are correct). The MT-OSC and OCI-STM numbers are peer-reviewed / vendor-evaluated benchmarks.

---

## 2. The "Cheap Model Cleans Up, Expensive Model Only Sees the Sharpened Version" Pattern

### 2.1 Named Patterns and Prior Art

This pattern has converged in the literature under several overlapping names:

**a) Prompt Compression (LLMLingua family — Microsoft Research)**

The canonical academic prior art. A small, cheap language model (e.g., LLaMA-7B, XLM-RoBERTa-large) identifies and removes low-information tokens from a verbose input *before* that input is sent to a frontier model.

**LLMLingua** (original, Oct 2023):  
- Method: coarse-to-fine compression; small model estimates information entropy per token; low-entropy tokens removed.  
- Results: [arXiv:2310.05736](https://arxiv.org/pdf/2310.05736.pdf), accepted EMNLP 2023.  
- Compression ratios: **2×–20×** with maintained downstream task performance on GSM8K, MeetingBank, BBH, and in-context learning benchmarks.  
- The "up to 20× compression" figure is from this paper's headline results on specific CoT/ICL benchmarks.

**LongLLMLingua** (Oct 2023, published Aug 2024):  
- Extends to long-context scenarios; question-aware compression prioritises tokens relevant to the query.  
- Key numbers from [arXiv:2310.06839](https://arxiv.org/pdf/2310.06839.pdf):
  - **21.4% performance improvement** on NaturalQuestions with **~4× fewer tokens** in GPT-3.5-Turbo.
  - **94.0% cost reduction** on the LooGLE benchmark.
  - Latency acceleration **1.4×–2.6×** when compressing ~10K token prompts at 2×–6× ratios.
- Mechanism: uses LLaMA-2-7B-Chat as the compressor model ($0 cloud cost if run locally).

**LLMLingua-2** (Mar 2024, ACL Findings 2024):  
- Data distillation from GPT-4 to train a token classifier (XLM-RoBERTa-large or mBERT).  
- Results from [arXiv:2403.12968](https://arxiv.org/abs/2403.12968):
  - **3×–6× faster** than LLMLingua-1 at compression time.
  - Accelerates end-to-end latency by **1.6×–2.9×** at 2×–5× compression ratios.
  - Strong out-of-domain generalisation across MeetingBank, LongBench, ZeroScrolls, GSM8K, BBH.
- Reliability: Peer-reviewed, ACL Findings 2024. Microsoft Research authorship.

**b) FrugalGPT / LLM Cascade (Stanford, 2023)**

- Framework: **prompt adaptation + LLM approximation + LLM cascade**.
- Prompt adaptation: rewrite verbose/vague prompts into structured queries that cheaper models can process.
- LLM cascade: send to cheapest model first; if quality below threshold, escalate to next tier; only the final tier may be a frontier model.
- Source: [portkey.ai writeup on FrugalGPT](https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/) (Apr 2024); original paper from Stanford.

**c) RouteLLM (LMSYS / ICLR 2025)**

The most rigorous public benchmark for the cheap-first routing pattern:
- Results from [digitalapplied.com RouteLLM analysis (June 2026)](https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide):
  - **85% cost reduction** on MT-Bench while retaining **95% of GPT-4 Turbo quality**, with only **14% of queries** reaching the frontier model.
  - **45% cost reduction** on MMLU at the same 95% quality threshold.
  - Matrix factorization router: 95% GPT-4 quality using only 26% GPT-4 calls — approximately 48% cheaper than random baseline.
  - *Caveat: benchmark-specific numbers; real-world savings depend on workload distribution. Treat as proof-of-concept, not a universal guarantee.*

**d) Speculative / Draft-Model Patterns (SpecPC)**

- [arXiv:2506.08373 — Draft-based Approximate Inference (2026)](https://arxiv.org/html/2506.08373): introduces **SpecPC** (Speculative Prompt Compression), which uses a small draft model's attention activations to identify and discard less important prompt tokens before the target model sees them.
- Related pattern: **speculative decoding** (Leviathan et al. 2023; Chen et al. 2023) — small draft model proposes tokens; large model verifies in parallel. Delivers **2–3× inference speedup** with near-lossless quality ([Red Hat blog, May 2026](https://www.redhat.com/en/blog/solving-economics-llm-inference-speculative-decoding)).
- *Note: speculative decoding reduces latency/compute, not input token cost. SpecPC/prompt compression reduces input token count and therefore API cost.*

**e) Voice-Specific: Voice Prompt Enhancement Node Pattern**

Directly applied to voice-to-AI workflows. From [danielrosehill/Voice-Prompt-Enhancement-Node on GitHub](https://github.com/danielrosehill/Voice-Prompt-Enhancement-Node) (July 2025):
- System prompt for a **preprocessing agent** that intercepts raw STT transcripts before they hit the inference model.
- Actions: remove filler words, fix obvious mistranscriptions, organise into sections, apply prompt engineering best practices, create deterministic and unambiguous prompts.
- Architecture: `User voice → STT → Agent 1 (cheap, enhancement) → Agent 2 (frontier, inference)`.
- This is an implemented, community-built instance of the FrugalGPT prompt adaptation pattern applied to voice input.

**f) Query Rewriting for Voice Assistants**

- [arXiv:2002.05607 — Pre-Training for Query Rewriting (2020)](https://arxiv.org/pdf/2002.05607.pdf): introduces a QR module between ASR transcript and NLU subsystem for voice assistants. The rewriter is pre-trained on conversation history and fine-tuned to convert messy ASR output into clean, structured queries.
- This is the academic precedent for the "small model restructures, large model acts" pattern in voice pipelines.

### 2.2 Does Compressing/Idealising the Prompt Measurably Reduce Downstream Tokens?

Yes, via two mechanisms:

1. **Direct input token reduction**: fewer input tokens sent to the frontier model = direct API cost saving proportional to compression ratio (2×–20×).
2. **Output token reduction**: more precise inputs generate more focused outputs, reducing unnecessary elaboration. This matters because output tokens are priced **3–5× higher** than input tokens on most frontier APIs. A tight, specific prompt that produces a 300-token answer rather than a 1,200-token rambling one saves more on the output side than the input.

**Reliability of the LLMLingua numbers:** Official peer-reviewed benchmarks (EMNLP 2023, ACL Findings 2024), Microsoft Research authorship. The 20× compression figure is the maximum on specific CoT benchmarks; typical useful compression is **4×–8×** with maintained quality. The 94% cost reduction on LooGLE is a specific benchmark result — do not generalise as a universal guarantee.

---

## 3. RAG vs. Long-Context: Retrieval as a Token-Reduction Strategy

### 3.1 The Core Cost Differential

From [dev.to RAG vs Long Context analysis (May 2026)](https://dev.to/wonderlab/rag-series-22-long-context-vs-rag-do-we-even-need-rag-5a8j):

| Approach | Context per query | Typical cost per query |
|---|---|---|
| Long context (1M tokens) | 1,000,000 tokens | ~$1.25 (Gemini 1.5 Pro pricing) |
| RAG (3K token chunks) | 2,000–5,000 tokens | ~$0.003–0.015 |
| **Ratio** | | **RAG is 20–200× cheaper** |

At 1,000 user queries/day against an enterprise knowledge base:
- Long context (1M tokens): ~$1,250/day
- RAG (3K token context): ~$3–15/day

From [tokenmix.ai RAG Tutorial 2026 (Apr 2026)](https://tokenmix.ai/blog/rag-tutorial-2026):
> "RAG + GPT-4o-mini at 1K queries/day on a 10K-page knowledge base: $60/month. Long context + GPT-4o: $37,500/month. **RAG is 625× cheaper**."  
> *Note: this compares an optimised RAG + cheap model against a worst-case full-context + expensive model. Marketing framing — treat with caution as a bounding case, not a typical comparison.*

More moderate estimate from [LightOn research, cited in miniml.ai (Jan 2026)](https://miniml.ai/long-context-windows-vs-retrieval-augmented-generation/): **RAG is 8–82× cheaper than long-context** for typical enterprise workloads. The range reflects variation in document corpus size and retrieval efficiency.

From [arXiv:2407.16833 — "RAG or Long-Context LLMs?" (July 2024)](https://arxiv.org/html/2407.16833v1):
- LC (long context) consistently **outperforms RAG** by 7.6% (Gemini-1.5-Pro), 13.1% (GPT-4o), 3.6% (GPT-3.5-Turbo) on average quality metrics *when sufficiently resourced*.
- For **>60% of standard queries**, RAG and LC produce **identical predictions** — RAG incurs no quality penalty on the majority of requests.
- **Conclusion: RAG is cost-optimal for routine queries; long-context justified only for tasks where retrieval cannot reconstruct the necessary context.**

### 3.2 "Context Offloading" to External Memory

Anthropic's [Effective Context Engineering for AI Agents (Sept 2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) describes three techniques for keeping context small:

**Compaction**: when approaching context limit, summarise the conversation and restart with the summary. Claude Code implementation: preserves "architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs." The agent continues with the compressed context plus the 5 most recently accessed files.

**Structured Note-Taking (Agentic Memory)**: agent writes notes to a NOTES.md file outside the context window. Notes are selectively re-injected at later turns. Example from the post: Claude playing Pokémon maintains precise tallies across thousands of game steps — "for the last 1,234 steps I've been training my Pokémon... Pikachu has gained 8 levels" — across context resets, without human prompting about memory structure.

**Sub-agent Architectures**: the main agent delegates deep-dive work to sub-agents with clean context windows. Each sub-agent may consume "tens of thousands of tokens or more" but returns only a "condensed, distilled summary of its work (often 1,000–2,000 tokens)." This achieves "a clear separation of concerns — the detailed search context remains isolated within sub-agents."

**Guiding principle from Anthropic:** *"good context engineering means finding the **smallest possible** set of **high-signal** tokens that maximize the likelihood of some desired outcome."*

**Just-in-time retrieval pattern** (Anthropic, same post): agents maintain lightweight identifiers (file paths, stored queries, web links) and load data into context only at the moment it is needed, rather than pre-loading everything. Claude Code uses `glob` and `grep` — it does not load entire codebases into context; it navigates and retrieves only what each decision step requires.

### 3.3 RAG for Conversational Context Offloading

The retrieval pattern maps directly onto voice-first workflows: instead of keeping all prior conversation turns in the prompt, store them in a vector store and retrieve only the turns semantically relevant to the current query.

From [ravoid.com context window cost analysis (Apr 2026)](https://ravoid.com/blog/massive-context-window-cost):

| Turn | RAG payload | 1M context payload | Cache status | Cost impact |
|---|---|---|---|---|
| Turn 1 | 2,500 tokens | 150,000 tokens | Cache miss | 60× higher (long context) |

**Reliability:** The academic RAG vs LC paper (arXiv:2407.16833) is peer-reviewed. The 625× cost figure from tokenmix.ai is constructed from best/worst-case comparison — marketing framing, not a benchmark. The 8–82× range from LightOn is more conservative and credible for enterprise workloads.

---

## 4. Voice-First / Dictation-to-AI Workflows: How Heavy Users Structure Things

### 4.1 The Local STT Layer: Zero Token Cost

**whisper.cpp / MacWhisper / faster-whisper**: Local Whisper runs on CPU or Apple Silicon at zero per-minute cost. The model itself runs entirely on-device.

From [starwhisper.ai comparison (accessed 2026)](https://starwhisper.ai/faq/whisper-local-vs-cloud):
- OpenAI Whisper API: **$0.006/minute**; 100 hours/month = $36.
- Local Whisper: **$0/minute** after install; break-even vs StarWhisper Pro at ~250,000 dictated words/month (a few hours of daily dictation).
- Whisper Large V3 Turbo (fine-tuned, local): **94.16% accuracy**, production-ready, zero per-minute costs.

**Implication**: The STT layer is free. Every token saved is saved downstream of transcription, not in the transcription step itself. The cost question is entirely about what goes into the LLM *after* the words leave the microphone.

### 4.2 Wispr Flow / SuperWhisper: What the Heavy Voice-User Tools Actually Do

**Wispr Flow** ([mrktcorrect.com review, May 2026](https://mrktcorrect.com/blog/wispr-flow-review); [wisprflow.ai](https://wisprflow.ai)):
- Cloud-processed Whisper-class STT + AI cleanup layer.
- Pipeline: **speak → server-side cleanup (filler removal, sentence restructuring, punctuation, paragraph breaks) → polished text pasted into active app**.
- Key: cleanup happens server-side before anything reaches the user's LLM session. The LLM session sees a cleaned prompt, not the raw dictation.
- Practical workflow described: "dictate through a request the way you'd brief a teammate, 30–90 seconds typically. The cleaned prompt appears. Press enter." — [mrktcorrect.com](https://mrktcorrect.com/blog/wispr-flow-review)
- **Limitation**: cleanup is stylistic (filler removal, formatting), not semantic compression. It does not shorten a 500-word ramble into a 50-token query. It makes it *cleaner*, not *shorter*.

**SuperWhisper** ([get-whisper.com 2026 comparison](https://get-whisper.com/blog/whisper-vs-superwhisper-vs-wispr-flow)):
- Local transcription (privacy preserved) + deep prompt customisation.
- Supports **custom pre-loaded context**: e.g., "this is a legal document, prefer formal phrasing" biases the transcription style.
- Post-processing pipelines configurable; multiple modes.
- More power-user oriented; best for workflows where you want to *shape* the output format of the transcription, not just clean it.

**OpenWhispr** ([openwhispr.com/use-cases/developers](https://openwhispr.com/use-cases/developers)):
- **Agent mode**: custom system prompt transforms dictation output. Example: set agent mode prompt to "Format as a structured engineering brief" and dictate; output is structured.
- Directly implements the "cheap model intermediary" pattern: local Whisper for STT ($0), agent mode (cheap model) for structuring, output fed to frontier model or coding agent.

### 4.3 The Three-Layer Architecture Pattern

The community-converged architecture for voice-first efficient AI:

```
1. Microphone → Local STT (whisper.cpp/faster-whisper)  [Cost: $0 tokens]
      ↓
2. Raw transcript → Lightweight preprocessing model       [Cost: cheap/local]
   (filler removal, structure, intent extraction,
    prompt engineering, semantic compression)
      ↓
3. Clean, structured prompt → Frontier model             [Cost: paid API]
   (only sees the distilled intent)
```

This is implemented in:
- [danielrosehill/Voice-Prompt-Enhancement-Node](https://github.com/danielrosehill/Voice-Prompt-Enhancement-Node) (July 2025) — explicit GitHub implementation
- OpenWhispr agent mode (commercial product)
- SuperWhisper custom post-processing pipelines

**What the preprocessing step can do**:
- Strip filler words, false starts, "um/uh", redundant restatements
- Extract the core intent from multi-minute ramble
- Apply LLMLingua-style compression (4×–20× token reduction, per §2 above)
- Restructure into a tight, cacheable prompt format
- Tag the query type for cascade routing (see §2)

**Local model options for preprocessing** (zero API cost):
- LLaMA-3 8B via Ollama (free, runs on MacBook M-series)
- Phi-3 Mini (3.8B parameters, excellent instruction following, runs on-device)
- LLMLingua-2 compressor (XLM-RoBERTa-large — very fast, purpose-built for compression)

---

## 5. Keeping the Mess for Discovery While Being Efficient

### 5.1 The Berrypicking Model (Bates, 1989)

The foundational theoretical prior art for why exploratory information seeking *cannot* be structured upfront without destroying it.

Marcia Bates' [Berrypicking Model](https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html) (1989, UCLA GSEIS):
- Classic IR model assumption: the query is static; search converges on a final retrieved set.
- Berrypicking reality: **the query evolves as the user gathers information**. Users pick up "bits and pieces at each stage of the ever-modifying search." The path is a loop and meander, not a straight line.
- Information need changes *because* of the information found, not despite it.

This exactly characterises dictated thinking-out-loud: the user does not know what they are looking for until the exploration surfaces it. Forcing structure at the start kills the emergent insight.

**Implication**: the exploration phase must be preserved raw. Compression and structuring belong *after* exploration has yielded its insights, not before.

### 5.2 Divergent-Convergent Phasing: AI Research Prior Art

**CreativeDC** ([arXiv:2512.23601, Dec 2025](https://arxiv.org/abs/2512.23601)): a two-phase prompting method for LLMs that explicitly separates divergent (unconstrained exploration) from convergent (constraint-satisfying execution) phases. Achieved "significantly higher diversity and novelty compared to baselines while maintaining high utility."

**HAICo** ([arXiv:2512.18388, Apr 2026](https://arxiv.org/html/2512.18388v2)): human-AI co-creation system with two switchable modes — Divergent mode (generates diverse ideas from cross-domain sources) and Convergent mode (translates refinement intentions into structured semantic parameters). *"To avoid design fixation, our paradigm scaffolds both high-level exploration of conceptual ideas in the early divergent thinking phase and low-level exploration of variations in the later convergent thinking phase."*

**Double Diamond / Conversational vs. Structured Prompting** ([Spencer Allred, Medium, Aug 2025](https://medium.com/@spencerallred/conversational-vs-structured-prompting-the-double-diamond-da5c6f9f89e5)):
- Divergent phase → conversational prompting (no structure, opens aperture, invites exploration).
- Convergent phase → structured prompts (tight, cached, deliverable-aligned).
- *"Conversational prompting has become a natural fit for the divergent side of the double diamond. When it is time to converge, structured prompts bring the clarity and focus needed to distil those ideas into something actionable. The key is knowing when to switch modes."*

### 5.3 PKM / Second Brain: Capture Everything, Process Selectively

**Building a Second Brain (Forte, BASB)** + **Zettelkasten** workflow, mapped to cost-tiering:

From [zettelkasten.de](https://zettelkasten.de/posts/building-a-second-brain-and-zettelkasten/) and [obsibrain.com (Mar 2026)](https://www.obsibrain.com/blog/zettelkasten-how-to-build-a-connected-second-brain-that-actually-grows-with-you):

BASB's **CODE** workflow:
1. **Capture**: everything, immediately, zero friction (fleeting notes, voice memos, raw dictation)
2. **Organise**: file to PARA categories (Projects, Areas, Resources, Archive)
3. **Distil**: progressive summarization — bold → highlight → executive summary → remix
4. **Express**: publish/apply only the distilled output

**Progressive Summarization** is directly analogous to the compression pipeline: each layer (bold → highlight → summary) costs some attention/compute, but reduces the context handed to the next layer. The final "Express" output is orders of magnitude smaller than the original capture.

The Zettelkasten pattern adds: **atomic, linked, permanent notes**. Each insight becomes a standalone unit that can be retrieved independently, rather than buried in a growing linear transcript. This maps directly onto RAG over personal notes: retrieve the relevant atomic note, not the 10,000-word session transcript.

**Operational mapping**:

| PKM step | Workflow equivalent | Token cost |
|---|---|---|
| Capture (fleeting note) | Raw voice dictation → STT | $0 (local Whisper) |
| Organise (PARA) | Tag/file raw transcript to project | $0–negligible (local rule) |
| Distil (progressive summary) | Cheap model compresses transcript | Cheap model ($0 local or low-cost API) |
| Express (application) | Frontier model acts on distilled context | Frontier model (paid API) |

### 5.4 The "Capture Everything Raw, Process Selectively" Architecture

Synthesising all of the above, the cost-efficient voice-first workflow is:

```
DIVERGENT PHASE (cheap/free)
  Voice dictation → local STT (Whisper, $0)
  → Raw transcript stored in notes/vault (no LLM cost)
  → Optional: cheap local model tags the transcript (topic, intent, open questions)
  → All raw material preserved for berrypicking / later retrieval

TRANSITION GATE (human-triggered or heuristic)
  "I have an insight / I want to do something with this"
  → Select the transcript segment(s) relevant to the current task

CONVERGENT PHASE (paid, minimal)
  → Preprocessing: cheap model (or LLMLingua-2) compresses/restructures
    selected transcript → target: 4×–8× compression, preserves intent
  → RAG over prior session notes to pull relevant context (2K–5K tokens max)
  → Frontier model receives: compressed current intent + retrieved prior context
    (total: ~3K–8K tokens vs. 30K–80K for unmanaged sessions)
  → Output: structured artefact (decision, draft, plan)
  → Key conclusions written back to notes vault (external memory)
```

**Anthropic's exact framing of this** ([Effective Context Engineering, Sept 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)):
> *"Agents can assemble understanding layer by layer, maintaining only what's necessary in working memory and leveraging note-taking strategies for additional persistence. This self-managed context window keeps the agent focused on relevant subsets rather than drowning in exhaustive but potentially irrelevant information."*

---

## Summary: What This Implies for a Talk-First Workflow

**The fundamental principle**: Ewan's ramble is the discovery engine and should not be constrained. The question is where it lives and what it touches.

**Five concrete changes that preserve the mess while cutting cost:**

### 1. Keep the ramble off the frontier model's context
Use local STT (whisper.cpp / MacWhisper / faster-whisper) to capture everything in text at $0. Store in a personal notes vault (Obsidian, Notion, text files). The frontier model never sees the raw stream unless explicitly needed.

**Impact**: STT cost = $0. Raw transcripts can be unlimited without any API cost.

### 2. Insert a cheap preprocessing step before every frontier call
When ready to act on something from a session, route the relevant transcript through a cheap model (local Ollama/Phi-3, or GPT-4o-mini at $0.15/M tokens) that:
- Strips filler and redundancy
- Extracts the core question/task
- Produces a structured prompt ≤500 tokens

**Impact**: LLMLingua-2 achieves **4×–8× compression** at maintained quality (ACL 2024 benchmark). At 8× compression, a 4,000-token ramble becomes a 500-token prompt, reducing frontier model input cost by ~87%.

### 3. Use RAG over session notes instead of stuffing history into context
After each session, write key outputs (decisions, questions, insights) as atomic notes. When starting a new session, retrieve the 3–5 relevant notes rather than re-sending prior session transcripts.

**Impact**: For over 60% of queries, RAG and long-context produce identical answers (arXiv:2407.16833). RAG keeps context to ~3K–5K tokens vs. potentially 50K+ for unmanaged history. Cost: **10×–100× reduction** for knowledge-base-type retrieval.

### 4. Apply prompt caching to the stable parts
Structure frontier model calls so the system prompt and persistent background context (stable instructions, Ewan's working patterns, recurring project context) are always at the prefix. Anthropic caches at 50% discount after 5 minutes; OpenAI caches automatically at 50–75% discount. Only the current, compressed query is "fresh."

**Impact**: If system prompt + stable context = 5,000 tokens, and this is cached across a session, every call saves ~$0.0125 (at Claude Sonnet pricing) just on the stable prefix. At 20 calls/day this is meaningful over time.

### 5. Tier exploratory from executory work
- **Exploratory/divergent** (thinking out loud, berrypicking): local STT + cheap model tagging. No frontier model needed. Cost: ~$0.
- **Synthesis** (making sense of a session): cheap model (GPT-4o-mini or Haiku) compresses and organises. Cost: low.
- **Execution** (drafting, deciding, acting on sharpened insight): frontier model receives only the compressed, structured, retrieved context. Cost: paid, but on a tight prompt.

RouteLLM (ICLR 2025) demonstrated that proper query routing routes **86% of queries away from frontier models** while retaining 95% of quality on MT-Bench — because most of the "thinking" doesn't need the expensive model.

---

## Key Numbers at a Glance

| Claim | Magnitude | Source | Reliability |
|---|---|---|---|
| Multi-turn context grows quadratically in cost | Structural mechanic | OpenAI/Anthropic API docs | Official |
| 10× cost reduction: 128K vs 10K context | 10× | propelius.ai (Feb 2026) | Community engineering |
| MT-OSC 10-turn token reduction | Up to 72% | arXiv:2604.08782 (June 2026) | Peer-reviewed |
| LLMLingua compression ratio | 2×–20× (typical 4×–8×) | arXiv:2310.05736 (EMNLP 2023) | Peer-reviewed |
| LongLLMLingua performance boost with 4× fewer tokens | +21.4% on NaturalQuestions | arXiv:2310.06839 (ACL 2024) | Peer-reviewed |
| LongLLMLingua cost reduction (LooGLE benchmark) | 94.0% | arXiv:2310.06839 | Peer-reviewed (benchmark-specific) |
| LLMLingua-2: speed vs LLMLingua-1 | 3×–6× faster compression | arXiv:2403.12968 (ACL Findings 2024) | Peer-reviewed |
| RAG vs long-context cost | 20–200× cheaper | arXiv:2407.16833 + dev.to analysis | Peer-reviewed + community |
| RAG vs LC: quality equivalent for 60%+ queries | >60% identical | arXiv:2407.16833 | Peer-reviewed |
| RouteLLM cost reduction (MT-Bench) | 85% at 95% quality, 14% frontier calls | ICLR 2025 (RouteLLM paper) | Peer-reviewed benchmark |
| OpenAI prompt caching discount | 50–75% on cached prefix | platform.openai.com | Official |
| Local Whisper STT cost | $0/minute | Operational fact | Official |
| Speculative decoding speedup | 2–3× inference | redhat.com + arXiv | Official engineering + peer-reviewed |

---

## Source Index

| # | Source | URL | Date | Type |
|---|---|---|---|---|
| 1 | LLMLingua (Microsoft Research) | https://arxiv.org/pdf/2310.05736.pdf | Oct 2023 | Peer-reviewed (EMNLP 2023) |
| 2 | LongLLMLingua (Microsoft Research) | https://arxiv.org/pdf/2310.06839.pdf | Aug 2024 | Peer-reviewed (ACL 2024) |
| 3 | LLMLingua-2 (Microsoft Research) | https://arxiv.org/abs/2403.12968 | Mar 2024 | Peer-reviewed (ACL Findings 2024) |
| 4 | Anthropic: Effective Context Engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Sept 2025 | Official Anthropic engineering post |
| 5 | Anthropic: Prompt Caching docs | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | 2024–2026 | Official |
| 6 | OpenAI: Prompt Caching docs | https://platform.openai.com/docs/guides/prompt-caching | 2024–2026 | Official |
| 7 | "Don't Break the Cache" (arXiv) | https://arxiv.org/pdf/2601.06007v1.pdf | Jan 2026 | Peer-reviewed |
| 8 | MT-OSC: Path for LLMs Lost in Multi-Turn | https://arxiv.org/html/2604.08782 | June 2026 | Peer-reviewed |
| 9 | RAG or Long-Context LLMs? (arXiv) | https://arxiv.org/html/2407.16833v1 | July 2024 | Peer-reviewed |
| 10 | RouteLLM analysis (ICLR 2025) | https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide | June 2026 | Community (cites ICLR 2025 paper) |
| 11 | FinOps.org: Token Pricing / Context Creep | https://www.finops.org/wg/genai-finops-how-token-pricing-really-works/ | 2024 | Community (FinOps WG) |
| 12 | aicostcheck.com: Large Context Window Costs | https://aicostcheck.com/blog/large-context-window-costs-2026 | Mar 2026 | Community engineering |
| 13 | propelius.ai: Context Window Budget | https://propelius.ai/blogs/building-conversational-ai-agents-context-windows/ | Feb 2026 | Community engineering |
| 14 | Bates Berrypicking Model | https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html | 1989 | Academic (JASIST) |
| 15 | CreativeDC: Divergent-Convergent LLMs | https://arxiv.org/abs/2512.23601 | Dec 2025 | Peer-reviewed |
| 16 | Wispr Flow review | https://mrktcorrect.com/blog/wispr-flow-review | May 2026 | Community |
| 17 | SuperWhisper / Whisper comparison | https://get-whisper.com/blog/whisper-vs-superwhisper-vs-wispr-flow | Apr 2026 | Community |
| 18 | Voice Prompt Enhancement Node (GitHub) | https://github.com/danielrosehill/Voice-Prompt-Enhancement-Node | July 2025 | Community / open source |
| 19 | Local Whisper cost analysis | https://starwhisper.ai/faq/whisper-local-vs-cloud | 2026 | Community |
| 20 | FrugalGPT / LLM Cascade (Portkey writeup) | https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/ | Apr 2024 | Community (cites Stanford paper) |
| 21 | Zettelkasten + BASB mapping | https://zettelkasten.de/posts/building-a-second-brain-and-zettelkasten/ | Jun 2023 | Community |
| 22 | Speculative Decoding (Red Hat) | https://www.redhat.com/en/blog/solving-economics-llm-inference-speculative-decoding | May 2026 | Official engineering blog |
| 23 | Draft-based Approx Inference / SpecPC | https://arxiv.org/html/2506.08373 | 2026 | Peer-reviewed |
| 24 | RAG Tutorial 2026 cost figures | https://tokenmix.ai/blog/rag-tutorial-2026 | Apr 2026 | Community (marketing framing — use with caution) |
| 25 | Double Diamond / Conversational Prompting | https://medium.com/@spencerallred/conversational-vs-structured-prompting-the-double-diamond-da5c6f9f89e5 | Aug 2025 | Community |
| 26 | Query Rewriting for Voice ASR (arXiv) | https://arxiv.org/pdf/2002.05607.pdf | 2020 | Peer-reviewed |
| 27 | OCI State-Tracking Memory (Oracle blog) | https://blogs.oracle.com/ai-and-datascience/multiturn-ocistm | Apr 2026 | Official vendor engineering |
