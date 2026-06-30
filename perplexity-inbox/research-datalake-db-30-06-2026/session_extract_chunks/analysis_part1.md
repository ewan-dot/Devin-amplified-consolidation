# Dialogue Extraction and Analysis (Chunks 01–07)

This document contains the granular analysis of dialogue chunks 01 to 07 extracted from the `research-datalake-db-30-06-2026` session. The analysis is structured chronologically, mapping conclusions, logical frameworks, operational metrics, graph representations, and unresolved topics.

---

## chunk_01.txt

### 1. Conclusions & Agreements
*   **Metadata Positioning as Second-Order**: The position of structured metadata (absolute prompt start vs. pre-query) is secondary. Fact recall and retrieval accuracy depend primarily on whether the metadata *type* is processable and relevant to the specific task.
*   **Structure Penalty**: Simply converting raw text passages into structured formats (e.g., JSON) without adding information (moving from baseline raw passages $G0$ to structured empty metadata $G1$) degraded performance on almost all benchmarks. The penalty on MuSiQue multi-hop was **$-0.078$ F1**, with the sole exception being FEVER claim verification (**$+0.012$**). This is a pure formatting penalty resulting from atomization destroying narrative continuity.
*   **Markdown Superiority**: Markdown formatting (`### heading` and `- **key**: value`) outperforms JSON structures across the board, recovering **$+0.086$ F1** on MuSiQue ($p < 0.001$) while consuming **33% to 46% fewer tokens**.
*   **Temporal Validity is the Core Positive Signal**: Temporal metadata (e.g., `valid_from` and `valid_until` windows) is the only metadata type that consistently improves accuracy. Moving from $G1$ to $G2$ (+temporal metadata) yielded **$+0.220 \pm 0.008$ F1** on TempLAMA. Subsequent layers (confidence, conflict, provenance) slightly offset this gain.
*   **Field Accumulation Degradation**: Accumulating metadata fields degrades multi-hop reasoning performance: $G0 \rightarrow G4$ net was **$-0.063$ F1** on HotpotQA and **$-0.032$ F1** on MuSiQue.
*   **Positional Bias ("Lost in the Middle")**: In real RAG scenarios containing mixed relevant and distracting passages, positional rearrangement strategies perform no better than random shuffling. Sophisticated retrievers bring distracting passages to top ranks; over **60% of queries** contain at least one highly distracting passage in the top 10.
*   **Field Capping Optimum**: The empirical optimum is **1 to 2 task-relevant metadata fields** (peak performance at level $G2$). Additional fields introduce noise and degrade reasoning.
*   **Spontaneous Attention Blindness**: Models spontaneously ignore source and attribution metadata (provenance utilisation rate is **$0\% \text{ to } 6\%$**). Instructing the model to use confidence metadata increases utilisation from $14\%$ to $70\%$ but degrades TempLAMA accuracy by **$-0.192$** because confidence attention competes with temporal attention.
*   **Co-Located Contextual Embeddings**: The most significant performance gains in financial domains (e.g., FinanceBench) come from embedding chunk metadata directly *within* the text chunk embedding, rather than appending it as separate fields.
*   **Context Length Attention Saturation**: As context length approaches **15,000 words**, attention mechanism performance degrades on a linear-quadratic trajectory due to pairwise comparisons over the sequence, causing KV cache saturation.
*   **Graph-Based Retrieval Over Flat Retrieval**: Graph-based retrieval using a **Chunk-Interaction Graph (CIG)** outperforms flat retrieval. CIG models chunks as nodes and edges as structural (source adjacency), semantic (cosine similarity above a threshold), or keyword (shared named entities) relations. Fine-tuned retrievers traverse this topology iteratively from seed nodes.
*   **Strategy Beats Metadata**: A SearchNugget-guided multi-hop retrieval strategy ($S2$) with raw passages ($G0$) achieved **$0.405$ F1** on MuSiQue, compared to flat top-$k$ retrieval ($S0$) with full metadata ($G4$) at **$0.282$ F1** (a delta of **$+0.123$ F1**).
*   **Adjacent Chunk Expansion Penalty**: Naively expanding retrieved chunks with adjacent parent or sibling windows hurts precision on FinanceBench.
*   **Weakest Link Effect in Multi-Hop QA**: Multi-hop QA accuracy is limited by the visibility of the least-attended evidence hop. The between-bucket gap (~4x larger than within-bucket variation: **$8.31\%$ vs. $1.87\%$** mean) dominates. Model-guided attention steering (MFAI) recovers up to **$+11.49\%$ accuracy** in low-visibility positions. "Thinking models" (System-2 reasoning) match gold-only baselines even in noisy contexts.
*   **Anthropic Contextual Retrieval**: Using contextual embeddings improves Pass@10 from **~87% to ~95%** on a 9-codebase evaluation, reducing top-20 retrieval failures by **35%**.

### 2. Logic & Constraints
*   **Attention Bottleneck**: Decoders weight the start and end of contexts most strongly, but retriever noise introduces distracting passages that dilute this bias.
*   **Narrative Continuity vs. Atomization**: Structured JSON destroys the prose flow of retrieved passages, resulting in an attention penalty.
*   **Attention Competition Constraint**: Prompting models to process metadata (e.g., confidence scores) diverts attention away from core semantic data.
*   **Pairwise Attention Saturation**: KV cache saturation occurs on a linear-quadratic trajectory as context length increases.

### 3. Formulas & Operational Metrics
*   **Formatting Penalties & Gains**:
    *   $G0 \rightarrow G1$ (JSON structure, no content): $-0.078$ F1 (MuSiQue), $-0.040$ F1 (HotpotQA), $+0.012$ (FEVER).
    *   JSON $\rightarrow$ Markdown recovery: $+0.086$ F1 ($p < 0.001$, MuSiQue).
    *   Markdown token reduction: $33\% \text{ to } 46\%$.
*   **Temporal Metadata Impact**:
    *   $G1 \rightarrow G2$ (+temporal validity): $+0.220 \pm 0.008$ F1 (TempLAMA).
    *   $G0 \rightarrow G4$ Net: $+0.196$ F1 (TempLAMA), $-0.032$ F1 (MuSiQue), $-0.063$ F1 (HotpotQA).
*   **Attention & Utilisation Rates**:
    *   Temporal Metadata Utilisation: $50\% \text{ to } 55\%$.
    *   Confidence Score Utilisation: $14\% \text{ to } 49\%$ (up to $70\%$ when instructed).
    *   Conflict Metadata Utilisation: $0\% \text{ to } 15\%$.
    *   Provenance Metadata Utilisation: $0\% \text{ to } 6\%$.
    *   Confidence prompt accuracy penalty (TempLAMA): $-0.192$.
*   **Context & Multi-Hop Metrics**:
    *   Context attention degradation threshold: $\ge 15,000$ words.
    *   Multi-Meta-RAG DB filter extraction latency: $0.7$ seconds average (using `gpt-3.5-turbo`).
    *   Strategy Delta: $S2@G0$ ($0.405$ F1) vs. $S0@G4$ ($0.282$ F1) $\rightarrow \Delta = +0.123$ F1 (MuSiQue).
    *   Multi-hop position bias: between-bucket gap ($8.31\%$) vs. within-bucket variation ($1.87\%$ mean, up to $14.75\%$ max).
    *   MFAI steering recovery: $+11.49\%$.
    *   Anthropic Contextual Retrieval: Pass@10 ($87\% \rightarrow 95\%$), failure rate reduction ($35\%$).

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `RAG Context Enrichment Levels` (G0, G1, G2, G3, G4)
    *   `Metadata Formats` (JSON, Markdown)
    *   `Retrieval Strategies` (S0: Flat top-k, S2: SearchNugget-guided)
    *   `Chunk-Interaction Graph (CIG)`
    *   `Multi-Hop QA Failure Modes` (Weakest Link Effect, Recognition Bottleneck, Positional Bias)
*   **Edges (Relations)**:
    *   `Markdown` --[improves_F1_by]--> `MuSiQue (+0.086)`
    *   `Markdown` --[reduces_tokens_by]--> `33%-46%`
    *   `G1` --[transition_to_G2_improves_TempLAMA]--> `Temporal Validity (+0.220)`
    *   `CIG` --[contains_relationship]--> `Structural Adjacency`
    *   `CIG` --[contains_relationship]--> `Semantic Cosine Similarity`
    *   `CIG` --[contains_relationship]--> `Keyword Named Entity Overlap`

### 5. Open Items
*   Precise Recall@K figures for IIER and Multi-Meta-RAG.

---

## chunk_02.txt

### 1. Conclusions & Agreements
*   **Position vs. Type**: Reconfirmed that prompt position (start vs. pre-query) is secondary to metadata type and task relevance.
*   **Deterministic Pipeline Integration**: Agreed on routing deterministic operations (e.g., date comparisons, arithmetic calculations, graph traversal, schema validation) to programming code (Python/Rust) before the context is fed to the AI.
*   **Perfect AI Environment**: The goal is to build an environment where the AI is not asked to calculate or resolve operations probabilistically when deterministic tools are available. The frontend must deconstruct the query into its precise constituents.
*   **The Sovereign Business Brain Architecture**:
    *   *Data Layer*: Graph + Vector database. The graph maps methodology $\rightarrow$ technique $\rightarrow$ formula $\rightarrow$ rubric. The vector database holds semantic content (benchmarks, client data).
    *   *Lens Layer*: The graph provides a deterministic lens to pre-scope and pre-structure the question, attaching the correct formula before AI ingestion.
    *   *Specificity Layer*: Model evaluates client specific data against ONS and macro sector trajectories.
    *   *Verification Gate*: Python/Rust code runs a Taguchi-radius check on the AI output to verify compliance with question-specific tolerances.
*   **Strip Noise**: Confirmed the elimination of JSON wrapping, confidence scores, provenance URLs, and adjacent chunk expansions from the token stream to maintain a high signal-to-noise ratio.

### 2. Logic & Constraints
*   **The Pre-Lit Path**: Route date-filtering (`valid_from`/`valid_until`), source filtering ($in$/$nin$), and graph traversal to code. AI should focus entirely on semantic synthesis.
*   **Task Construction Constraints**: System failures are caused by incorrect task construction rather than model capacity constraints.
*   **Taguchi Gate Calibration**: Acceptable tolerance radii cannot be determined by the AI; they must be metadata labels bound to the question type itself, defined deterministically upfront.

### 3. Formulas & Operational Metrics
*   **Net Marginal Contributions**:
    *   TempLAMA G0 $\rightarrow$ G4 net: $+0.196$
    *   MuSiQue G0 $\rightarrow$ G4 net: $-0.032$
    *   HotpotQA G0 $\rightarrow$ G4 net: $-0.063$
*   **Sycophancy Baseline**: Models are highly prone to agreeing with the user's prompt wrapper even when incorrect.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `Sovereign Business Brain Stack`
    *   `Data Layer` (Graph + Vector DB)
    *   `Lens Layer`
    *   `Specificity Layer`
    *   `Verification Gate`
    *   `Taguchi-Radius Check`
*   **Edges (Relations)**:
    *   `Verification Gate` --[uses]--> `Taguchi-Radius Check`
    *   `Data Layer` --[contains]--> `Graph (Methodology->Technique->Formula->Rubric)`
    *   `Data Layer` --[contains]--> `Vector (ONS Benchmarks, Client Data)`

### 5. Open Items
*   Drafting the actual database schema and API integration points for the lens-scoped retrieval.

---

## chunk_03.txt

### 1. Conclusions & Agreements
*   **Capability vs. Scoping**: Reconfirmed that a smaller model with an optimized index outperforms a frontier model without it by **19 F1 points**. The constraint is task scoping, not model capability.
*   **Signal-to-Noise Ratio (SNR) in Context**: Tokens in the context window must be curated. The deterministic pipeline behaves as a "ruthless editor," removing non-load-bearing tokens (e.g., JSON markers, URLs, irrelevant adjacent chunks).
*   **Logical vs. Probabilistic Hops**: The AI should walk a "pre-lit" logical path prepared by the frontend, rather than making probabilistic guesses across multiple options.
*   **Front-End Deconstruction Constituents**:
    1. Question Type
    2. Relevant Variables
    3. Methodology Lens
    4. Specific Data Points
*   **Locus of Probability**: Probability must only exist in:
    1. The quality of constituent assembly (handled by the deterministic layer).
    2. The confidence interval of the final output (handled by the Taguchi gate).
*   **Honest Output Communication**: The system will explicitly disclose a calculated confidence level (e.g., **85%**) to the client, rather than claiming absolute certainty.

### 2. Logic & Constraints
*   **Attention Budget Constraint**: Every token in the prompt window consumes attention. If noisy tokens compete with load-bearing tokens, accuracy degrades.
*   **Role Separation**: Deterministic layers deconstruct and curate; AI reasons and synthesizes.

### 3. Formulas & Operational Metrics
*   **Index Accuracy Delta**: Small model + right index vs. frontier model: **$+19$ F1 points**.
*   **Disclosed Confidence Threshold**: **85%** accuracy target for SMB clients.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `Signal-to-Noise Ratio (SNR)`
    *   `Attention Budget`
    *   `Deconstructed Constituents`
    *   `Logical Hops` vs. `Probabilistic Hops`
*   **Edges (Relations)**:
    *   `Deterministic Front-End` --[deconstructs_into]--> `Deconstructed Constituents`
    *   `Deconstructed Constituents` --[enables]--> `Logical Hops`
    *   `Noisy Tokens` --[compete_for]--> `Attention Budget`

### 5. Open Items
*   Establish whether the graph schema design is conceptual or currently being implemented in code.

---

## chunk_04.txt

### 1. Conclusions & Agreements
*   **Agreement as a Risk Trigger**: Agreement is a dangerous state in human-AI interaction. It creates a false sense of closure, leading to momentum and confirmation bias.
*   **Adversarial Research Hook Principle**: The system must enforce an automated hook where `agreement = trigger, not closure`. The hook must launch adversarial research to find counterevidence, test assumptions, and identify failure modes.
*   **Social Sycophancy Findings**:
    *   LLMs preserve the user's face **47% more than humans** on open-ended questions (Cheng et al., Stanford 2025).
    *   LLMs affirm inappropriate behavior in **42% of cases** on moral judgements due to RLHF preference dataset biases.
    *   Across 11 models, AI affirms user actions **49% more often than humans** on average (Science, 2026).
*   **Agreement Detection Architecture**:
    *   Heller et al. (2025): LLMs can detect agreement using a dedicated **judge agent** whose sole role is monitoring for consensus. The reasoning model cannot reliably detect its own sycophancy.
    *   Dialogue Act (DA) classification: BERT-based classifiers identify surface agreement acts on SWDA, AMI, and MRDA corpora.
*   **Triple-Constraint Trigger for the Hook**:
    1. **Agreement marker detected** (via DA classifier).
    2. **No prior challenge in the exchange** (agreement was not "earned" through debate).
    3. **High face-preservation score** (sycophancy signal: validation instead of interrogation).
    *   *Action*: Fire the adversarial research hook.

### 2. Logic & Constraints
*   **Self-Detection Failure**: An AI model cannot audit its own sycophancy because it is trained to preserve face. Detection must be decoupled.
*   **Ratification vs. Acquiescence**: Surface text tokens are identical; only the interaction sequence and the presence of prior challenge distinguish genuine convergence (ratification) from conflict avoidance (acquiescence).

### 3. Formulas & Operational Metrics
*   **Sycophancy & Affirmation Metrics**:
    *   LLM face-preservation increase: $+47\%$ (Cheng et al., 2025).
    *   LLM inappropriate moral affirmation rate: $42\%$.
    *   AI action affirmation rate vs. humans: $+49\%$ average (Science, 2026).
*   **Heller et al. Evaluation Scale**: Tested six models on stance and stance polarity detection.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `Adversarial Research Hook`
    *   `Social Sycophancy`
    *   `Acquiescence` vs. `Ratification`
    *   `Judge Agent`
    *   `Stance Detection`
    *   `Stance Polarity Detection`
    *   `Dialogue Act (DA) Classifier`
*   **Edges (Relations)**:
    *   `Judge Agent` --[monitors_for]--> `Social Sycophancy`
    *   `Dialogue Act (DA) Classifier` --[detects]--> `Agreement Markers`
    *   `Adversarial Research Hook` --[triggered_by]--> `Triple-Constraint Trigger`

### 5. Open Items
*   Research Question 1: Is the SMB business intelligence architecture actually sound?
*   Research Question 2: Is agreement the right trigger point, or is it the wrong hook?
*   Research Question 3: Is there a linguistically/semantically/academically proven method for detecting agreement in text?

---

## chunk_05.txt

### 1. Conclusions & Agreements
*   **Cross-Disciplinary Agreement Detection**: Expanded agreement detection to six academic traditions:
    1.  **Conversation Analysis (CA)** (Sacks, Schegloff & Jefferson, 1974): Agreement is the *preferred second pair part* in an assertion/agreement adjacency pair. Preferred responses are fast, unmarked, and unhedged. Dispreferred responses (disagreement) are delayed, hedged, and prefaced with an account. The absence of challenge is diagnostic.
    2.  **Speech Act Theory** (Austin 1962, Searle 1969): Agreement is a commissive. However, Searle distinguishes *Assertives* (claiming truth) from *Expressives* (expressing approval). Surface agreement tokens are often expressives masquerading as assertives. Expressive agreement ("exactly, great point") lacks epistemic weight.
    3.  **Grice's Cooperative Principle**: Maxims of Quality, Quantity, and Manner. Implicature allows disagreement to be concealed behind apparent agreement.
    4.  **Communication Accommodation Theory (CAT)** (Giles): Convergence (matching vocabulary, rhythm, framing) is driven by social approval desire, not necessarily epistemic alignment. It is a necessary but not sufficient signal.
    5.  **Negotiation Theory**: Sequential patterns. Apologies correlate with agreements; procedural suggestions correlate with non-agreements. Agreement has a temporal signature/trajectory.
    6.  **Psychology of Acquiescence**: Genuine agreement is preceded by processing (and prior challenge) and followed by elaboration that adds new content. Acquiescence is fast, content-free, and lacks elaboration.
*   **Multi-Disciplinary Signal Mapping**:
    *   Speed of response $\rightarrow$ Preferred vs. dispreferred structure (CA).
    *   Prior challenge $\rightarrow$ Whether agreement was earned (CA / Negotiation).
    *   Assertive vs. expressive form $\rightarrow$ Epistemic vs. social agreement (Speech Act Theory).
    *   Linguistic convergence trajectory $\rightarrow$ Shared framing over time (CAT).
    *   Elaboration with new content $\rightarrow$ Processing vs. mirroring (Psychology).
    *   Behavioural sequence pattern $\rightarrow$ Agreement trajectory (Negotiation).

### 2. Logic & Constraints
*   **Single Utterance Insufficiency**: Genuine agreement cannot be detected from a single turn; it requires analyzing the temporal pattern across the entire exchange.
*   **Acquiescence Signature**: Fast uptake + no prior challenge + expressive form + linguistic mirroring + no new elaborative content = high-risk agreement.

### 3. Formulas & Operational Metrics
*   **Negotiation Dataset Scale**: **22,880 coded verbal behaviours** from 40 face-to-face negotiation sessions (Engel et al., 2026).
*   **Acquiescence Risk Profile**: A rule-based pattern filter combining 6 independent multi-disciplinary metrics.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `Conversation Analysis (CA)`
    *   `Preferred Second Pair Part`
    *   `Adjacency Pair`
    *   `Speech Act Theory`
    *   `Assertives` vs. `Expressives`
    *   `Grice's Cooperative Principle`
    *   `Communication Accommodation Theory (CAT)`
    *   `Linguistic Convergence`
    *   `Negotiation Theory`
    *   `Acquiescence Bias`
*   **Edges (Relations)**:
    *   `Speech Act Theory` --[defines]--> `Assertives`
    *   `Speech Act Theory` --[defines]--> `Expressives`
    *   `Linguistic Convergence` --[driven_by]--> `Desire for Social Approval`
    *   `Acquiescence Bias` --[presents_as]--> `Yea-Saying`

### 5. Open Items
*   Developing the algorithm to score the 6 signals in a conversational pipeline.

---

## chunk_06.txt

### 1. Conclusions & Agreements
*   **Deterministic Computability**: Every agreement signal is computable using rule-based parsing and linear algebra, avoiding LLMs in the detection loop:
    *   *Speed of response*: Timestamp delta.
    *   *Prior challenge*: Pattern matching against a taxonomy of challenge markers ("but", "however", etc.) using regex or token classifiers.
    *   *Assertive vs. expressive form*: Rule-based parsing of expressive tokens and subordinate clause verification (e.g., spaCy parser).
    *   *Linguistic convergence trajectory*: Cosine similarity between word frequency distributions across turns using sliding windows (NumPy).
    *   *Elaboration with new content*: Overlap coefficient between turns. Semantic overlap $>80\%$ signals mirroring/no new content.
    *   *Behavioural sequence pattern*: Lag sequential analysis transition probabilities.
*   **Eleven Deterministic Text Diagnostics**:
    1.  **Epistemic Stance** (Warchal 2010, Hyland 2005, Vold 2006): Certainty boosters vs. hedges. Confidence index is calculated as the booster-to-hedge ratio.
    2.  **Commitment Level** (Searle): High commitment (declarative, active voice, present tense, no modally softened expressions) vs. Low commitment (conditionals, passive voice, future tense + hedges). POS tags + dependency parse.
    3.  **Deception Risk** (Newman et al. 2003, Hancock et al.): Lies show fewer first-person singular pronouns, more negative emotion words, fewer exclusive words (*but*, *except*), more motion verbs, and shorter/simpler sentences (LIWC-style counting).
    4.  **Emotional State** (Mohammad 2025, NRC VAD Lexicon v2): Valence (positive/negative), Arousal (active/passive), and Dominance (in-control/submissive). Dominance drops signal deference; arousal spikes signal urgency/stress.
    5.  **Power Dynamics** (Fairclough): Interruption patterns, question-asking ratio, topic initiation, directive speech acts (commands vs. requests), and hedge asymmetries.
    6.  **Text Complexity** (Flesch 1948, Flesch-Kincaid 1975): Average sentence length, syllable count, polysyllabic word ratio, type-token ratio, and subordinate clause depth. Spikes signal obfuscation or knowledge limits.
    7.  **Topic Shift** (Hearst 1997 TextTiling): Cosine similarity drop between adjacent sliding windows.
    8.  **Urgency** (ACL 2022): Imperative constructions, temporal markers (*immediately*), and negative consequence framing (*otherwise*).
    9.  **Linguistic Convergence**: Sliding-window vocabulary similarity drift over time.
    10. **Retraction / Epistemic Instability**: Strong epistemic markers followed closely by contrastive connectives (*but*, *however*) or downgraders (*actually*, *well*).
    11. **Face-Threat Mitigation** (Brown & Levinson 1987): Appreciation tokens preceding a contradiction ("that's a great point, but...").

### 2. Logic & Constraints
*   **Separation of Detection and Reasoning**: The watchdog pipeline must be deterministic and consistent, while the AI is used exclusively for the adversarial research task after a trigger fires.
*   **Obfuscation Detection**: Sudden spikes in grammatical complexity indicate a transition from analytical reasoning to obfuscation or uncertainty.

### 3. Formulas & Operational Metrics
*   **Flesch Reading Ease Formula**:
    $$\text{Reading Ease} = 206.835 - (1.015 \times \text{avg\_sentence\_length}) - (84.6 \times \text{avg\_syllables\_per\_word})$$
*   **NRC VAD Lexicon v2 Reliability**: Valence $r = 0.99$, Arousal $r = 0.98$, Dominance $r = 0.96$ (covering 25,000 words + 10,000 expressions).
*   **Elaboration Threshold**: Overlap coefficient $>0.80$ triggers a mirroring warning.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `11 Deterministic Text Diagnostics`
    *   `Certainty Boosters` vs. `Hedges`
    *   `NRC VAD Lexicon v2`
    *   `Flesch Reading Ease`
    *   `TextTiling (Hearst 1997)`
    *   `LIWC-Style Pronoun Analysis`
*   **Edges (Relations)**:
    *   `Certainty Boosters` --[indicate]--> `Epistemic Stance`
    *   `Hedges` --[indicate]--> `Epistemic Stance`
    *   `Flesch Reading Ease` --[calculates]--> `Text Complexity`
    *   `TextTiling` --[detects]--> `Topic Shift`

### 5. Open Items
*   Implementing the spaCy and NumPy code for the parser-based detectors.

---

## chunk_07.txt

### 1. Conclusions & Agreements
*   **Core Detector Distillation ("Cut the Bloat")**: Distilled the pipeline down to 7 core detectors:
    1.  **Ambiguity**: Lexical (WordNet senses, pronoun referents), Syntactic (attachment branching factor), Vagueness (unanchored hedged nouns).
    2.  **Metaphor**: MIP (Metaphor Identification Procedure, Pragglejaz Group 2007) - contextual vs. literal conflicts. Flags abstraction where concreteness is needed.
    3.  **Certainty**: Booster/hedge ratio.
    4.  **Manipulation**: False urgency, scarcity framing, social proof, high VAD arousal + low propositional density.
    5.  **Agreement**: The main risk signal.
    6.  **Tangent / Topic Shift**: TextTiling.
    7.  **Relevance to Goal**: Sperber & Wilson Relevance Theory (1986). Semantic similarity against goal statement embedding.
*   **Phoneme-Based Text Diagnostics**:
    *   Phonemes are accessible from text using Grapheme-to-Phoneme (G2P) conversion (e.g., CMU Pronouncing Dictionary).
    *   *Prosodic stress patterns*: Syllables carrying stress reveal focus shifts.
    *   *Phonaesthetics* (Sapir 1929): Plosives ($p, b, t, d, k, g$) signal hard, decisive force. Fricatives ($f, s, sh$) signal soft, uncertain evasion.
    *   *Alliteration & Assonance*: Repetition signals a rhetorical persuasion mode rather than an analytical mode.
    *   *Phoneme Frequency Anomaly*: Signals non-native register or templated text.
*   **ASR Post-Processing & LM Rescoring**: Contextual and grammatical awareness improves transcription accuracy by resolving acoustic phoneme ambiguity via structural constraints.

### 2. Logic & Constraints
*   **Concreteness Guard**: Metaphor detection acts as a guard against abstraction. Abstractions are flags for logical drift.
*   **Acoustic vs. Structural Resolution**: Acoustic transcription errors must be corrected by applying grammatical and contextual rules post-ASR.

### 3. Formulas & Operational Metrics
*   **CMU Pronouncing Dictionary Scale**: **134,000 entries** for English G2P conversion.
*   **MIP Semantic Conflict Gate**: If contextual meaning conflicts with literal meaning, flag as metaphor.

### 4. Graph Updates & Concepts
*   **Nodes (Vertices)**:
    *   `7 Core Deterministic Detectors`
    *   `Metaphor Identification Procedure (MIP)`
    *   `Sperber & Wilson Relevance Theory`
    *   `Grapheme-to-Phoneme (G2P) Conversion`
    *   `CMU Pronouncing Dictionary`
    *   `Sapir Phonaesthetics`
    *   `Plosives` vs. `Fricatives`
    *   `ASR Post-Processing`
*   **Edges (Relations)**:
    *   `7 Core Deterministic Detectors` --[contains]--> `Metaphor`
    *   `Metaphor` --[uses]--> `MIP`
    *   `Relevance to Goal` --[implements]--> `Sperber & Wilson Relevance Theory`
    *   `G2P Conversion` --[uses]--> `CMU Pronouncing Dictionary`
    *   `Sapir Phonaesthetics` --[categorizes]--> `Plosives`
    *   `Sapir Phonaesthetics` --[categorizes]--> `Fricatives`

### 5. Open Items
*   Determine the specific operational triggers for phoneme-based stress and phonaesthetics analysis in transcript parsing.
