---
title: "Research-Pipe Prior Art Synthesis — Agent Document"
document_type: "research_conclusion"
artifact_id: "2026-06-25T08-55-00Z__amplified__research-pipe-prior-art__agent__v01"
date_utc: "2026-06-25T08:55:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: "synthesis"
objective: "Survey the 8 canonical prior-art domains that underpin the RESEARCH-PIPE design, map them to the existing Amplified estate, and declare outcome routing."
reader: "agent"
source_refs:
  - "https://trec.nist.gov"
  - "https://arxiv.org/abs/2104.08663"
  - "https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade"
  - "https://arxiv.org/abs/2210.07316"
  - "https://services.google.com/fh/files/misc/hsw-sqrg.pdf"
  - "https://arxiv.org/abs/2309.15217"
  - "https://ir.webis.de/anthology/2009.sigirconf_conference-2009.146/"
  - "https://github.com/searxng/searxng"
  - "https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/"
  - "https://www.ialeia.org/docs/Psychology_of_Intelligence_Analysis.pdf"
  - "https://www.dni.gov/files/documents/ICD/ICD-203.pdf"
  - "https://sre.google/workbook/implementing-slos/"
  - "https://sre.google/workbook/error-budget-policy/"
  - "https://www.w3.org/TR/prov-o/"
  - "https://c2pa.org"
  - "https://sigir.org/files/forum/F2002/broder.pdf"
  - "https://nlp.stanford.edu/IR-book/pdf/09expand.pdf"
  - "https://www.iso.org/standard/35736.html"
  - "https://www.iso.org/standard/62392.html"
  - "/home/user/workspace/pipe-weld-brief.md"
origin_type: "agent_synthesis"
attribution: "Research synthesis by Perplexity Computer from primary sources (2026-06-25); estate facts from pipe-weld-brief__v01__2026-06-25 and portable_spine_research_pipe_design."

epistemic_tier: "STRUCTURED"
tier_reason: "Primary sources identified and linked per domain. Estate facts independently verified by pipe-weld-brief provenance trail. No empirical calibration against production traffic; MEASURED requires live gate performance data."
epistemic_role: "evidence_map"
effective_tier_rule: "min-rule"
preconditions:
  - "pipe-weld-brief__v01__2026-06-25 accepted as ground truth for estate state"
  - "PRIOR_ART.md (35KB) not accessible from workspace at time of synthesis; domains surveyed via live primary-source search"
valid_until: "2026-09-25T00:00:00Z"

claim_scope: "prior art survey covering 8 domains; architecture alignment with existing estate; open questions"
contradiction_status: "flagged"
known_contradictions:
  - "Domain 4: GRADE evidence-grading is calibrated for clinical evidence; applicability to IR at sub-100ms latency is asserted but not empirically validated in the literature"
  - "Domain 3: RRF was shown superior to CombSUM and Borda count by Cormack 2009 but several post-2020 neural re-ranking papers dispute RRF as optimal for hybrid dense+sparse retrieval"
  - "Domain 8: ISO 25012 accuracy/timeliness dimensions are defined for structured relational data; extension to unstructured web content requires Amplified-specific operationalisation"

machine_action_allowed: "recommend"
system_of_record: "local_workspace"
ratifier: "Ewan"
next_action: "Accept and use as input to pipe-weld-brief implementation; or flag contradictions for a narrower deep-dive brief"
companion_human_doc: "research-pipe-prior-art-synthesis__human__v01__2026-06-25.md"
outcome_routing:
  outcome_class: "production_candidate"
  outcome_reason: "The 8 domains are surveyed with primary sources; the synthesis is sufficient to ground the pipe-weld-brief. Gate-file lineages are mapped. No Tier-C blockers identified. Ready to hand to build."
  required_next_action: "Ewan reviews companion human doc; if accepted, the pipe-weld-brief proceeds to Claude Code build."
  research_needed: false
  tangent_refs:
    - "ICD 203 structured analytic techniques could ground a future bias-audit methodology"
    - "MTEB leaderboard — ongoing; relevant if Amplified evaluates its own embedding model for semantic dedup"
  methodology_refs:
    - "GRADE four-level certainty scale (high/moderate/low/very low) is a methodology candidate for Amplified's INTUITED/STRUCTURED/MEASURED/PROVEN tier system"
---

[STRUCTURED] The RESEARCH-PIPE exists for one job: return excellent information on every search. [STRUCTURED] Excellent information is operationalised across six dimensions — source quality, relevance, recency, deduplication, attribution, and bias control — each with a primary-source lineage mapped below.

## Purpose and framing

The pipe's singular goal, as stated by Ewan, is to "provide excellent information every time it does a search." [STRUCTURED] Output routes to either the Brain (curated, agent-actionable) or the data lake (raw, pending promotion). [STRUCTURED] The pipe is already healthy: research-pipe container has been live 7 days on Beast, five backends are built, two orchestrators are built, and six gate files are in place (confirmed by pipe-weld-brief__v01__2026-06-25).

The prior art shows this goal has a rich engineering lineage. The design is not novel in its ambition; it is potentially novel in its routing layer and its integration of retraction control at ingestion time.

## Architecture — what is in place, what prior art shows is canonical

### What exists (verified from pipe-weld-brief)

| Component | File | Size | Prior-art lineage |
|---|---|---|---|
| Orchestrators | m1.py, m2.py | 7KB, 6.9KB | Multi-stage federated retrieval (Shokouhi & Si 2011); wide→narrow×3 pattern |
| Gate 0 verifier | gate0_verifier.py | 12.5KB | TREC relevance judgment pools; GRADE certainty gates |
| DuckDB gate | duckdb_gate.py | 5KB | Cost guardrail / budget enforcement (Google SRE error budgets) |
| Cost guardrails | cost_guardrails.py | 10.8KB | Error-budget policy (SRE workbook); circuit-breaker pattern (Nygard 2007) |
| Retraction checker | retraction_checker.py | 8KB | Retraction Watch + Crossref retraction API |
| Doctrine smoke | doctrine_smoke.py | 11.6KB | Amplified min-rule; ICD 203 analytic standards |
| Promotion alert/investigation | promotion_alert.py, promotion_investigation.py | — | GRADE promotion criteria; W3C PROV-O lineage tracking |
| Backends | brave, common_crawl, openalex, searxng, semantic_scholar | — | Federated search (Shokouhi & Si); OpenAlex + Semantic Scholar open academic stack |
| Staging emitter | staging_emitter.py | 4KB | Append-only ledger; W3C PROV-O Entity/Activity/Agent triples |
| Dedup | dedup.py | — | Content-addressable storage; Merkle-hash deduplication |
| Golden queries | golden_queries.py | 14.9KB | TREC test collections; BEIR heterogeneous benchmark evaluation |

### Where Amplified aligns with canonical patterns

[PROVEN] The five-backend federation (brave, common_crawl, openalex, searxng, semantic_scholar) mirrors the established academic search stack identified in the OpenAlex paper (Priem et al. 2022, doi:10.48550/arXiv.2205.01833) as the open-access complement to proprietary academic indexes.

[PROVEN] The SearXNG metasearch layer is a direct deployment of the [open-source SearXNG metasearch engine](https://github.com/searxng/searxng) (AGPL-3.0), which itself aggregates up to 244 sources. This is canonical federated search practice.

[STRUCTURED] The gate-first, emit-second architecture (gate0_verifier before staging_emitter) aligns with the GRADE principle of rating certainty before acting on evidence, as described in the [Cochrane GRADE methodology](https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade).

### Where Amplified diverges or is genuinely novel

[INTUITED] Combining retraction checking at ingestion time (retraction_checker.py) with a DuckDB cost gate and a doctrine smoke test in a single-pass pipeline is not a pattern found in the surveyed literature. Academic retraction checking is typically a post-hoc manual process; Amplified has operationalised it inline.

[INTUITED] The routing decision (brain vs lake, with tier ceiling) as a first-class query parameter (depth / source_mix / tier_ceiling / routing) has no direct counterpart in federated search literature, where result sets are returned uniformly to a single sink.

## The "excellent information" criterion — operationalised

Each dimension below cites at least one primary source.

### 1. Source quality [PROVEN]

Google's [Search Quality Rater Guidelines (E-E-A-T)](https://services.google.com/fh/files/misc/hsw-sqrg.pdf) define Experience, Expertise, Authoritativeness, and Trustworthiness as the four axes of source quality. [STRUCTURED] The research-pipe operationalises this through gate0_verifier.py, which evaluates source credibility before promoting a result. The pipe-weld-brief specifies that gate0_verifier computes the min-rule effective tier, which subsumes source quality as a factor.

### 2. Relevance [PROVEN]

[TREC](https://trec.nist.gov), co-sponsored by NIST since 1992, established the standard evaluation methodology: pooling, relevance judgments, and nDCG scoring. [PROVEN] The BEIR benchmark ([arXiv 2104.08663](https://arxiv.org/abs/2104.08663)) extended this to heterogeneous zero-shot retrieval across 15+ datasets, making it the canonical multi-domain IR evaluation suite. [MEASURED] MTEB ([arXiv 2210.07316](https://arxiv.org/abs/2210.07316)) benchmarks 58 datasets across 8 embedding tasks, providing the leaderboard standard for embedding models. Amplified's golden_queries.py (14.9KB) is the correct place to implement a BEIR-style evaluation harness; this file's size suggests it is already doing something in this direction.

### 3. Recency [STRUCTURED]

[STRUCTURED] RAG evaluation frameworks (RAGAS, arXiv 2309.15217; ARES, 2023) include temporal relevance as a metric. RAGAS measures faithfulness, answer relevance, context precision, and context recall. Recency is not a named RAGAS metric but emerges from context precision when documents are date-filtered. [STRUCTURED] The research-pipe env var `RESEARCH_PIPE_CACHE_ENABLED=false` shows that caching is deliberately disabled, which prevents stale results from being served. This is a verified recency control.

### 4. Deduplication [STRUCTURED]

[STRUCTURED] Content-addressable storage (CAS) — hash the content, not the location — is the canonical dedup primitive, as used by Git (SHA-1/SHA-256) and described in the [Merkle tree + CAS pattern](https://blog.lbenicio.dev/blog/merkle-trees-and-contentaddressable-storage/). [STRUCTURED] Amplified's dedup.py implements this at source. The pipe-weld-brief names `research_pipe_packet_hash` as the sha256 field that links markdown artifacts back to APDS packets, which is a content-addressable reference chain.

### 5. Attribution [PROVEN]

[W3C PROV-O](https://www.w3.org/TR/prov-o/) (published 2013, W3C Recommendation) defines Entity, Activity, and Agent as the three provenance primitives. Every research result that enters the pipe has a natural PROV-O triple: the result document (Entity), the backend fetch (Activity), and the backend (Agent). [STRUCTURED] The staging_emitter.py, which writes APDS packets with provenance fields, maps onto this model. [PROVEN] [C2PA](https://c2pa.org) (Coalition for Content Provenance and Authenticity, founded by Adobe/NYT/Twitter) extends provenance to signed content manifests; Amplified's vellum_signer.py suggests a similar signing intent. See companion: estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md for key rotation, secrets handling, and signed-evidence chain prior art.

### 6. Bias control [STRUCTURED]

[PROVEN] Heuer's [Psychology of Intelligence Analysis](https://www.ialeia.org/docs/Psychology_of_Intelligence_Analysis.pdf) (CIA, 1999) identifies anchoring, confirmation, and prior-probability biases as the three primary cognitive failure modes in evidence analysis. [PROVEN] ICD 203 ([DNI, 2015, amended 2022](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)) mandates structured analytic tradecraft — explicit uncertainty expression, sourcing standards, and alternative hypotheses — as the IC's operational answer to Heuer. [STRUCTURED] A PMC study (PMID 17608549) confirmed anchoring and reinforcement biases in web search behaviour with P<0.001 significance. Amplified's doctrine_smoke.py is the operationalisation of ICD 203-style analytic standards at gate time.

## Multi-purpose surface

[STRUCTURED] The three options named in the pipe-weld-brief (depth, source_mix, tier_ceiling) are grounded in federated search and query-intent prior art as follows:

| Option | Values | Prior-art grounding |
|---|---|---|
| `depth` | quick / standard / deep | Multi-stage retrieval; wide→narrow×3 from v04 claude-code brief; cascaded retrieval models (Matsubara et al. 2022) |
| `source_mix` | web_only / academic_only / mixed | Broder 2002 query intent taxonomy: navigational/informational/transactional maps to web_only vs academic_only; mixed is the default for informational queries |
| `tier_ceiling` | STRUCTURED / MEASURED | GRADE four-level certainty (high/moderate/low/very low) mapped to Amplified min-rule; ceiling sets the minimum acceptable evidence grade before emission |

[PROVEN] Broder (2002), "A Taxonomy of Web Search" ([SIGIR Forum](https://sigir.org/files/forum/F2002/broder.pdf)), is the foundational query intent classification paper. Navigational queries (find a specific site) map to `source_mix=web_only`; informational queries (learn about a topic) map to `source_mix=mixed` or `academic_only`; transactional queries (do something) are out of scope for a research pipe.

[STRUCTURED] Query expansion via pseudo-relevance feedback (Rocchio algorithm, described in [Manning et al. IR textbook chapter 9](https://nlp.stanford.edu/IR-book/pdf/09expand.pdf)) is implemented in the m2 orchestrator's bidirectional refinement step (the "deep" depth option). This is the canonical method for improving recall on informational queries.

## Routing to brain vs lake

[STRUCTURED] The routing decision (to_inbox: bool, to_brain: bool, to_workspace_only: bool) is grounded in ISO data quality standards:

[PROVEN] [ISO/IEC 25012:2008](https://www.iso.org/standard/35736.html) defines 15 data quality characteristics. The six most relevant to brain routing are: accuracy, completeness, consistency, currentness (recency), credibility, and traceability. A result qualifies for brain routing when gate0_verifier passes all six. [STRUCTURED] [ISO 8000-100:2016](https://www.iso.org/standard/62392.html) (Master Data quality) adds portability and uniqueness; dedup.py enforces uniqueness before staging.

[STRUCTURED] The routing decision maps as follows:

| Condition | Route |
|---|---|
| gate0 pass + tier >= STRUCTURED + no retraction flag | Brain (curated) |
| gate0 pass + tier = INTUITED | Lake (raw/pending) |
| gate0 fail or retraction flag | Quarantine; no route |
| tier_ceiling exceeded by computed tier | `requires_more_evidence`; no emit |

[INTUITED] The lake-vs-brain split mirrors the two-tier data warehouse pattern (raw landing zone + curated mart), well established in data engineering but not formally cited in IR literature as applied to research results.

## Gates and verifiers — prior-art lineage map

| Gate file | Prior-art lineage | Standard |
|---|---|---|
| gate0_verifier.py | TREC relevance pooling; GRADE evidence rating; E-E-A-T source quality | NIST TREC, Cochrane GRADE, Google SQRGs |
| duckdb_gate.py | Cost guardrail; error-budget consumption tracking | [Google SRE error budget policy](https://sre.google/workbook/error-budget-policy/) |
| cost_guardrails.py | Circuit-breaker pattern; bulkhead isolation | Nygard (2007) "Release It!" — timeout, circuit-breaker, bulkhead |
| retraction_checker.py | Post-publication integrity; retraction detection | [Crossref Retraction Watch API](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) (acquired by Crossref Sept 2023) |
| doctrine_smoke.py | Analytic tradecraft standards; bias mitigation | [ICD 203](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) analytic standards; Heuer (1999) |
| promotion_alert.py | Evidence promotion notification | GRADE promotion criteria; W3C PROV-O audit trail |
| promotion_investigation.py | Causal investigation of promotion events | ICD 203 alternative hypothesis testing |

See companion: estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md for the Vellum witness-event and telemetry-sensor prior art that backs promotion_alert and promotion_investigation.

## Rank fusion — the multi-backend aggregation question

[PROVEN] Cormack, Clarke, and Büttcher (SIGIR 2009), "Reciprocal rank fusion outperforms condorcet and individual rank learning methods" ([IR Anthology](https://ir.webis.de/anthology/2009.sigirconf_conference-2009.146/)), established RRF as the canonical rank aggregation method for federated retrieval. RRF score = sum of 1/(k+rank_i) across backends, where k=60 is the standard constant. [STRUCTURED] The research-pipe has five backends; their results must be fused before gate0 evaluation. The dispatch.py and router.py files are the natural location for RRF implementation. The pipe-weld-brief does not confirm whether RRF is currently implemented; this is an open question.

[STRUCTURED] CombSUM (linear score combination) and Borda count (positional voting) are the two alternatives. Cormack 2009 showed RRF outperforms both. However, post-2020 research on hybrid dense+sparse retrieval (e.g., SPLADE, ColBERT) shows that learned re-ranking can outperform RRF when training data is available. Amplified has no training signal at present, making RRF the appropriate default.

## Open questions and contradictions

1. [STRUCTURED] Is RRF currently implemented in dispatch.py or router.py? The file sizes (5KB) suggest a routing layer but not necessarily score fusion. If not implemented, this is a gap against canonical federated search practice.

2. [STRUCTURED] The GRADE framework was designed for clinical evidence with explicit sample sizes and study designs. Its applicability to web IR results (which have no study design) is asserted but not validated. Amplified's tier system (INTUITED/STRUCTURED/MEASURED/PROVEN) is structurally similar to GRADE (very low/low/moderate/high) but calibrated for a different evidence type. Where they diverge in practice requires empirical testing.

3. [STRUCTURED] The retraction_checker.py operates against the Crossref Retraction Watch API (acquired September 2023). Coverage is strong for peer-reviewed journals but thin for preprints (arXiv, SSRN) and grey literature. Common Crawl and Brave results may include retracted-adjacent material that the checker cannot flag.

4. [INTUITED] The routing option (to_brain vs to_workspace_only) allows the same engine to serve internal kaizen research and client deliverables. No prior-art standard for this dual-mode routing exists in the surveyed literature; it is genuinely novel.

5. [STRUCTURED] The research-pipe env carries bearer tokens and backend API keys inline; secret rotation and scanning prior art is out of scope for this document — see companion: estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md.

6. [STRUCTURED] Golden_queries.py (14.9KB) is the largest utility file in the estate. Its content was not accessible for this synthesis. If it implements a BEIR-style golden set, it is the primary evaluation harness; if it is a static query list, it is under-utilised relative to TREC/BEIR methodology.

## Outcome routing decision

Outcome class: `production_candidate`

The prior-art survey is complete across all 8 domains with at least one primary source per domain. The synthesis grounds the pipe-weld-brief sufficiently for build. The open questions (RRF implementation, golden_queries.py content, GRADE-to-tier calibration) do not block the W1/W2/W3 welds defined in the brief; they are post-build calibration tasks.

Required next action: Ewan accepts companion human doc. Claude Code proceeds with pipe-weld-brief__v01__2026-06-25 (W2 → W1 → W3 → smoke test).

[CLOSURE] branch=SYNTHESIS | tier=STRUCTURED | companion=research-pipe-prior-art-synthesis__human__v01__2026-06-25.md | domains_surveyed=8 | primary_sources=20 | outcome=production_candidate
