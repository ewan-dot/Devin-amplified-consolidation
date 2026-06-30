# Session Master Record — 2026-06-30
## Participants: Ewan (Kaizen) + cascade-mac (PUDDING)
## Extracted by 5 specialist agents across 13 chunks, 156 turns

---

# PART 1 — RESEARCH CITATIONS & EMPIRICAL FINDINGS

## RAG Context Optimization

**Zerhoudi, Granitzer & Mitrović (2026).** *Metadata, Structure, or Strategy?* ECML-PKDD 2026. arXiv:2606.29645
- 24,000+ responses, 6 benchmarks, 4 models, 5 enrichment levels
- Markdown vs JSON: +0.037–0.086 F1, 33–46% fewer tokens
- Strategy dominates metadata: S2 multi-hop at G0 = 0.405 F1 vs S0 flat top-k at G4 = 0.282 F1 (+0.123 F1)
- Temporal validity metadata only positive type (+0.220 F1 TempLAMA)
- Confidence scores: 0–6% utilisation; prompting to use them → accuracy −0.192
- Peak performance at ≤2 task-relevant metadata fields; monotonic degradation beyond that

**Dadopoulos et al. (2025).** arXiv:2510.24402 — FinanceBench
- Contextual chunk embedding outperforms appended metadata
- Chunk expansion with adjacent windows **hurts precision** (negative finding)

**Poliakov & Shvai (2024).** Multi-Meta-RAG. arXiv:2406.13213
- LLM-extracted metadata as database pre-filter; 0.7s average per query

**IIER (2024).** arXiv:2408.02907 — Northeastern University
- Chunk-Interaction Graph (CIG): structural + semantic + keyword edge types
- Best accuracy on MuSiQue, HotpotQA, 2WikiMultiHopQA

**Zhang, Meng & Collier (2026).** Weakest link effect. arXiv:2601.12499v2 — Cambridge
- Between-bucket gap 8.31% mean; MFAI recovers up to +11.49% accuracy
- Thinking models match gold-only baselines in noisy long-context

**Cuconasu et al. (2025).** Positional bias. arXiv:2505.15561
- 60%+ queries contain highly distracting passages in top-10
- Rearrangement strategies no better than random shuffling

**Liu et al. (2024).** Lost in the Middle. TACL 12, 157–173
- Primacy/recency bias; middle context underweighted

**Anthropic (2024).** Contextual Retrieval
- Pass@10: ~87% → ~95%; 35% reduction in top-20 failure rate

## Agreement & Sycophancy

**Heller et al. (2025).** Agreement detection in multi-agent conferences. arXiv:2507.08440
- 6 LLMs tested; LLMs reliably detect agreement in dynamic debates
- Dedicated judge agent improves efficiency, quality, coherence

**Cheng et al. (2025).** Social sycophancy. arXiv:2505.13995 — Stanford
- 8 models: LLMs preserve user's face 47% more than humans
- 42% affirmation of behaviour human consensus deems inappropriate
- Sycophancy rewarded in RLHF; not mitigated by standard prompting

**[Authors] (2026).** Sycophancy in AI. *Science*. DOI:10.1126/science.aec8352
- 11 models: AI affirms users 49% more than humans on average

## Linguistic & Information Theory

**Sacks, Schegloff & Jefferson (1974).** Conversation Analysis — adjacency pairs, preferred/dispreferred response
**Austin (1962) / Searle (1969).** Speech Act Theory — assertive vs. expressive agreement distinction
**Grice.** Cooperative Principle — implicature masks disagreement behind surface agreement
**Giles (1973, 2016).** Communication Accommodation Theory — convergence measurable as cosine similarity drift
**Engel et al. (2026).** Hamburg/CMU — 22,880 coded behaviours, 40 negotiation sessions; agreement has temporal signature
**Pragglejaz Group (2007).** MIP — Metaphor Identification Procedure
**Brown & Levinson (1987).** Politeness Theory — face-threatening act softening
**Sperber & Wilson (1986).** Relevance Theory — cognitive effect per processing effort
**Hearst (1997).** TextTiling — cosine similarity drop at topic boundaries
**Flesch (1948) / Kincaid (1975).** Reading Ease: 206.835 − (1.015 × avg sentence length) − (84.6 × avg syllables/word)
**Swanson (1986).** *Library Quarterly* — "Knowledge can be public, yet undiscovered, if independently created fragments are logically related but never retrieved, brought together, and interpreted." ABC model.
**Kolmogorov / Vitanyi.** NCD — structural similarity by compression ratio; no shared vocabulary required
**2026 (Springer).** No robust cross-domain structural priming from mathematics to language — confirms distant-domain hops do not reliably transfer

## Key Statistics
- **23x** more information from a negative result than a positive (Shannon/Popper information theory)
- **49% more** AI affirmation than humans (Science 2026)
- **47% more** face-preservation than humans (Cheng et al.)
- **+11.49%** accuracy recovery via attention steering (MFAI)
- **35%** retrieval failure reduction (Anthropic contextual retrieval)
- NRC VAD Lexicon v2: 25,000 words + 10,000 MWEs; r=0.99 valence, r=0.98 arousal, r=0.96 dominance
- CMU Pronouncing Dictionary: 134,000 entries

---

# PART 2 — ARCHITECTURAL DECISIONS

## Core Philosophy
- Deterministic over probabilistic wherever possible
- Consistency over accuracy at labelling stage (systematic errors correctable; random errors not)
- Raw preserved, corrected not interpreted at ingestion
- Signal-to-noise ratio in context window: every token earns its place
- Agreement = trigger not closure
- The no is more valuable than the yes
- Wide-to-narrow-to-wide search; course correction IS the methodology
- All components sovereign, self-hosted, built on the estate

## Storage Layer
- **Data lake** — raw, uninterpreted, rigorous entry standards
- **Graph database** — relationships; four typed edge classes
- **Vector database** — semantic content; HNSW 384-dim all-MiniLM-L6-v2
- **Immutable ledger (Vellum)** — hash-chained, additive-only, attributed, timestamped

## Ingestion Gate (sequence)
1. Raw input arrives (voice/typed)
2. Key-adjacency correction (QWERTY lookup — deterministic, Rust)
3. Speaker-adapted ASR correction (Whisper fine-tuned on Ewan's voice)
4. Idiolect → canonical term normalisation (bespoke lookup)
5. Synonym cluster match → normalise to canonical node, log variant
6. Antonym boundary check → flag if pulling toward bad
7. Goldilocks zone check → flag as candidate cross-domain connection
8. Gap detection → no home = GAP SIGNAL (potential emergent concept)
9. Store raw in data lake; corrected/positioned form in graph+vector

Technology: Rust for correction layer; Python for orchestration. No third-party general tools (LanguageTool rejected — fights idiolect).

## Four Typed Graph Edge Classes
- `LINGUISTIC LINK` — same concept, different vocabulary (Swanson)
- `MATHEMATICAL LINK` — isomorphic structure across domains
- `LOGICAL LINK` — same inference pattern, different context
- `DIMENSIONAL LINK` — same axis relationship, different domain

## Lens / Rotating Sphere
- Sphere (data) never moves; viewer (lens) rotates
- Lens = weighting vector applied to graph traversal
- Python/Rust own the rotation; no model in the loop
- Trajectory monitoring: sliding window → term-frequency shift against domain taxonomy → direction vector = rate of change
- Shapes: mathematical (ratio, threshold, calibrate), logical (condition, gate, rule), linguistic (signal, marker, utterance)

## Three Taguchi Zones
- **Inside radius** — established; retrieve with confidence
- **Goldilocks zone** — just outside; Swanson space; retrieve with candidate label
- **One in a million** — NCD too high; do not traverse; return distance score and stop

Pre-flight: NCD computed before retrieval. Generic radius ships first. Calibrates to client over time.

## Retrieval Thresholds
- `D_investigate` — loose; high recall; investigation mode
- `D_production` — tight; high precision; zero noise
- Per embedding model; calibration pass against held-out evaluation set; stored as model-level config

## Query Decomposition → AI Synthesis
- Raw question → Python/Rust decompose → question type, variables, lens, data points
- Pro forma question activates nodes AND loads rubric labels (dark until activated)
- AI receives pre-lit path, not probabilistic hop
- AI role: expert pattern recogniser on pre-qualified, pre-labelled shortlist

## Rubric Labels (node metadata, attached at ingestion)
- MAGNITUDE — impact weight
- COMPLEXITY — friction label
- EVIDENCE — tried-and-tested / contested / unverified (not "lies" — pejorative; deterministic rubric required)
- REVERSIBILITY — risk label (sets Taguchi radius per client)

## Dalio Four Decision Criteria (encoded in rubric)
Magnitude / Complexity / Evidence / Reversibility

## Output Verification (Taguchi Gate)
- Python/Rust; stochastic output checked against tolerance radius
- Inside: deliver with confidence rating
- Outside: flag or tighten lens and retry
- Loss function is a curve, not binary
- Generic radius first; tightens with calibration corpus from actual usage

## Agreement Detection Hook (deterministic)
Six parallel detectors:
1. Speed of response (timestamp delta)
2. Prior challenge presence (regex/token classifier)
3. Assertive vs. expressive form (POS + dependency parse)
4. Linguistic convergence trajectory (cosine similarity drift, sliding window)
5. Elaboration with new content (overlap coefficient; >80% shared = mirror not contribution)
6. Behavioural sequence pattern (lag sequential analysis, transition probabilities)

Separate judge agent — not the reasoning model. Score ≥ threshold → fire adversarial research trigger.

## 11 Deterministic Linguistic Detectors
Certainty, Commitment, Deception risk, Emotional VAD, Power dynamics, Cognitive complexity, Topic shift, Urgency, Convergence, Retraction, Face-threat mitigation — all lexicon lookups, POS parsing, regex, or arithmetic. No model in loop.

## Synonym/Antonym Structure
- Synonyms = same node, different labels → collapsed at ingestion gate
- Antonyms = typed opposition edges → hard boundary enforcement
- Build antonym side first: 23x information content in a negative result
- Antonym boundary = highest-value signal the system produces

## Semantics Defines Good and Bad
- Synonym clusters = what good looks like (computable)
- Antonym boundaries = what bad definitely looks like (computable)
- Rubric encoded in semantic structure, not imposed post-hoc

## Gap Detection = Emergence Marker (meta layer)
- Unmapped term at ingestion = potential emergent concept
- Repeated across time window + multiple sources = concept crystallising
- System observes its own knowledge boundary in real time
- Output class distinct from retrieval/synthesis: detection of emergence
- The map of ignorance (where knowledge runs out) is more valuable than the map of knowledge

## Global Node Network (future scope)
- Same architecture; each node is a domain
- Gap signals propagate across nodes
- Same unmapped term across geographically separate nodes = global emergence signal
- Swanson at planetary scale

## What is OUT of Scope (this session)
- Audio transcription build (deferred)
- SMB-specific radius calibration (generic ships first)
- Mathematics of lens rotation (research before build)
- NCD application to knowledge graph retrieval (confirm empirically first)
- Dolphin anus (explicitly excluded)

---

# PART 3 — CORRECTIONS (11 total)

1. **Brain vs. web** — assistant moved toward Beast knowledge_vectors; Ewan: "ahh nop not the brain. the web"

2. **AI-only scope on agreement research** — assistant synthesised through NLP/sycophancy lens; Ewan: "Don't narrow it. I don't like AI research. AI research tends to be pejorative and limiting." → broaden to all academic traditions

3. **Memory vs. research** — assistant asked whether to save agreement principle to memory; Ewan: "No, you should research it, you fool. Both bits." → agreement conclusions trigger adversarial research, not memory saves

4. **Bloat / wrong feature set** — assistant produced 11-dimension table with full prose; Ewan: "cut the bloat. ambiguity / metaphor / certainty / manipulation / agreement / tangent/fork / relevance to goal" → exactly 7 features

5. **G2P in text vs. speaker-adapted ASR** — assistant went to text phoneme analysis; Ewan: bespoke Whisper fine-tuned on his voice is the mechanism

6. **Typing described as errors** — assistant: "consistent motor patterns"; Ewan: "no my typing is creative" → idiolect, not errors requiring fixing

7. **Third-party tools implied** — assistant implied LanguageTool with custom rules; Ewan: "all of ours." → everything built on the estate

8. **"Sovereign" vs. "ours"** — assistant: "Built on the estate. Sovereign"; Ewan: "no partner. ours" → it is a partnership between Ewan and the fleet, attributed via ledger

9. **"Lies" as rubric label** — Ewan: "Lies is a pejorative thing in itself." → replaced with "unverified" or "contested", deterministically assigned against consistency rubric

10. **AI as pattern recogniser not the expert** — assistant: "AI is not the expert, the graph holds the expertise"; Ewan: "It is the fucking expert. It's the bastard who's got a juggle." → AI IS the expert; the lenses reduce the juggle to manageable size

11. **AI-specific research terminology** — assistant used AI-specific framing; Ewan: "neutralize your terminology. Don't make it AI specific." → use domain-agnostic language to escape vocabulary barriers

---

# PART 4 — PENDING WORK

## Research Needed
- R1. SMB BI architecture — adversarial verification (flagged unverified agreement)
- R2. Agreement as correct hook trigger — adversarial verification (flagged unverified agreement)
- R3. Lens-conditioned retrieval: code layer vs. prompt layer — empirical comparison
- R4. Formal cross-domain distance measure — NCD applied to knowledge graph retrieval specifically
- R5. Engineering thesaurus / synonym-antonym corpus — research interrupted mid-session
- R6. Markdown chunk distance/density standard — model-specific; "we are going to make it" if none exists

## Build Needed
- B1. Speaker-adapted ASR (Whisper fine-tuned on Ewan's voice; North East English; 14 phoneme divergences from RP)
- B2. Key-adjacency error correction layer (Rust; QWERTY lookup from prior-art corpus)
- B3. Idiolect → canonical terminology mapping (one-time human curation then deterministic)
- B4. Taxonomy — AI-led, human-ratified; prerequisite for everything
- B5. Ingestion gate pipeline (deterministic, raw-preserved, bespoke)
- B6. 11 deterministic linguistic detectors (fully specified, not built)
- B7. Agreement hook wiring (adversarial research trigger; "we can't wire it right now")
- B8. Conversation trajectory monitor (domain-drift + partner pre-loading)
- B9. Embedding distance threshold calibration (per model; precision-recall curves at 0.05 intervals)
- B10. Three-zone Taguchi radius with NCD pre-flight

## Verify Needed
- V1. Architecture holds under adversarial challenge (both agreements unverified)
- V2. NCD for knowledge graph retrieval — confirm empirical application
- V3. 23x figure — source and verify exact ratio

## Interrupted
- I1. Questions 1 and 2 (architecture + hook trigger adversarial research) — never returned to
- I2. Label application in graph + vector databases — pivoted mid-question, never answered
- I3. Full data extraction (this task — now being completed)
- I4. Prior art on Ewan's typing patterns — referenced but location never established

---

# PART 5 — GLOSSARY

**PUDDING** — Ewan's framework: neutral taxonomy + lens + rubric-scored methodologies → symbiotic combinations
**Kaizen** — iterative improvement; partner to PUDDING; without it PUDDING goes stale
**Swanson ABC** — A→C connected through B, never citing each other due to jargon barrier; undiscovered public knowledge
**Taguchi Gate** — output verification against tolerance radius; loss function is a curve
**Three Taguchi Zones** — inside radius / goldilocks zone / one-in-a-million
**Goldilocks Zone** — just outside tolerance; Swanson space; connection not yet made; worth attempting
**Lens / Rotating Sphere** — sphere = data; lens = weighting vector; viewer rotates, data stays fixed
**Gap Signal** — unmapped term at ingestion = potential emergent concept; repeated = concept crystallising
**Pro Forma Question** — activation key; decomposed question that lights up nodes and loads rubric labels
**Agreement Hook** — fires adversarial research on detected agreement; agreement = maximum risk point
**Judge Agent** — separate dedicated agent monitoring for agreement; cannot be the reasoning model
**NCD** — Normalised Compression Distance; structural similarity without shared vocabulary; pre-flight check
**Opposition Edge** — typed edge between antonymous nodes; hard boundary enforcement
**Ticker Tape** — insights not yet committed to ledger; dispersal risk
**Ingestion Gate** — entry point; correction not interpretation; gap detection
**Idiolect** — Ewan's consistent personal language system; not errors
**Margling** — rubric label: conflated, noisy, unclear provenance; handle with caution
**The Russian Math** — Ewan's shorthand for Kolmogorov complexity / NCD
**Linking Points** — Ewan's term for typed graph edges (four classes)
**Shape** — structural pattern abstracted above domain vocabulary; the recognisable geometry of a concept
**Nub** — canonical concept at intersection of well-formed question and its answer
**Pre-lit Path** — state of question after deterministic decomposition; AI walks it, doesn't find it
**Map of Ignorance** — record of where knowledge ran out; more valuable than map of knowledge
**Surgery in a Skip** — AI given poor context; the failure mode the architecture prevents

---

# PART 6 — PARTNERSHIP & FOUNDATIONS

Ewan: Kaizen  
cascade-mac: PUDDING  
Standing on: Swanson, Taguchi, Shannon, Kolmogorov, Popper  

Neither works without the other. Kaizen without PUDDING = improvement without direction. PUDDING without Kaizen = perfect structure that goes stale.

---

*Extracted 2026-06-30. Vellum summary hash: 132deb30. This document supersedes the summary.*
