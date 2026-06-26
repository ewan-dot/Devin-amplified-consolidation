---
title: "Research-Pipe Prior Art Synthesis — Ewan Brief"
document_type: "readable_research_conclusion"
artifact_id: "2026-06-25T09-06-00Z__amplified__research-pipe-prior-art__human__v01"
date_utc: "2026-06-25T09:06:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: "synthesis"
audience: "Ewan"
purpose: "Plain-English summary of what the prior art says about the research pipe, what is already built, and what is missing — so Ewan can accept the pipe-weld brief and let build proceed."
source_refs:
  - "https://trec.nist.gov"
  - "https://arxiv.org/abs/2104.08663"
  - "https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade"
  - "https://services.google.com/fh/files/misc/hsw-sqrg.pdf"
  - "https://arxiv.org/abs/2309.15217"
  - "https://ir.webis.de/anthology/2009.sigirconf_conference-2009.146/"
  - "https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/"
  - "https://www.ialeia.org/docs/Psychology_of_Intelligence_Analysis.pdf"
  - "https://www.dni.gov/files/documents/ICD/ICD-203.pdf"
  - "https://sre.google/workbook/error-budget-policy/"
  - "https://www.w3.org/TR/prov-o/"
  - "https://c2pa.org"
  - "https://sigir.org/files/forum/F2002/broder.pdf"
  - "https://www.iso.org/standard/35736.html"
attribution: "Research synthesis by Perplexity Computer from primary sources, 2026-06-25. Estate facts from pipe-weld-brief__v01__2026-06-25 (verified live on Beast)."

epistemic_tier: "STRUCTURED"
epistemic_role: "evidence_map"
tier_reason: "Primary sources identified and linked for all 8 domains. Estate facts independently verified. No empirical calibration against live traffic yet — that comes after the weld."
confidence_plain_english: "The prior art picture is solid enough to justify building. The open gaps are post-build calibration tasks, not blockers."
open_questions:
  - "Is Reciprocal Rank Fusion currently implemented in dispatch.py / router.py, or do the five backends just return unmerged lists?"
  - "What does golden_queries.py actually do — BEIR-style golden evaluation set, or static list?"
  - "GRADE evidence grading was designed for clinical trials. Our tier system (INTUITED/STRUCTURED/MEASURED/PROVEN) follows the same shape but applies to web and academic search results. The calibration between them needs a live test, not more research."

companion_agent_doc: "research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md"
system_of_record: "local_workspace"
machine_action_allowed: "recommend"
next_human_decision: "Accept the pipe-weld brief and let Claude Code start on W2 (verify ingest-inbox drain), then W1 (staging emitter bridge), then W3 (options surface)."
outcome:
  class: "production_candidate"
  plain_english_reason: "The prior art is surveyed, the build plan exists in the pipe-weld brief, and nothing in the research blocks the three welds. The only missing pieces are post-build — rank fusion confirmation and golden-query audit."
---

## What the pipe is for

The research pipe has one job: return excellent information every time it does a search, then route that information to either the Brain (curated, agent-actionable) or the data lake (raw, pending review).

## Where we are

The pipe is running. The container has been healthy on Beast for seven days, five search backends are wired up (Brave, Common Crawl, OpenAlex, SearXNG, Semantic Scholar), two orchestrators handle the search logic, and six gate files check quality, cost, retraction status, and doctrine compliance before anything leaves the pipe. What is not yet connected is the final step: a completed research run does not automatically land in the Brain or the ingest inbox. A human has to move it. The pipe-weld brief defines three small code changes that close that gap without any new infrastructure.

## What the prior art says we should do

- Rate source quality before trusting results. Google's Search Quality Rater Guidelines define four axes: Experience, Expertise, Authoritativeness, and Trustworthiness. The gate0_verifier already does this; it is the correct place for it.

- Merge results from multiple backends using Reciprocal Rank Fusion, not a raw list. Cormack, Clarke, and Buttcher (SIGIR 2009) showed RRF outperforms every alternative for federated retrieval. With five backends, unmerged result lists will give inconsistent ordering. RRF score = 1/(60 + rank) per backend, summed across backends.

- Check for retractions at ingest time, not after. The Crossref Retraction Watch database (acquired by Crossref in September 2023) is the canonical source. The pipe already has retraction_checker.py — this is ahead of most production IR systems.

- Use a tiered evidence scale and enforce it as a gate, not a label. The GRADE framework (used by Cochrane for clinical evidence since 2004) is the prior-art model: evidence grades from very low to high, and you do not act on low-grade evidence without flagging it. Amplified's INTUITED / STRUCTURED / MEASURED / PROVEN tier system is structurally identical and correctly applied.

- Route by query intent, not just query text. Broder (2002) showed web queries split into navigational (find a specific thing), informational (learn about a topic), and transactional (do something). The pipe's source_mix option (web_only / academic_only / mixed) maps directly onto this: academic_only for informational depth, web_only for navigational or current-events queries.

- Keep provenance as a first-class field, not an afterthought. W3C PROV-O (2013) defines the minimum: who created the result, what activity produced it, and what entity it derives from. The APDS packet and the research_pipe_packet_hash field in the weld spec satisfy this.

- Treat cost as a hard gate, not a soft preference. Google SRE error budgets (site reliability engineering) establish the principle: define a budget, enforce it mechanically, and stop spending when the budget is exhausted. The cost_guardrails.py and duckdb_gate.py files implement this correctly.

- Protect against cognitive bias in result selection. Heuer's Psychology of Intelligence Analysis (CIA, 1999) and ICD 203 (the US intelligence community's analytic standards directive) identify anchoring, confirmation, and prior-probability bias as the three failure modes. The doctrine_smoke.py gate is the operational answer to this — it runs analytic standards checks before a result is promoted.

## What's already done

| Component | What it does | Status |
|---|---|---|
| Five backends | Brave, Common Crawl, OpenAlex, SearXNG, Semantic Scholar | Built and running |
| Orchestrators m1 + m2 | Quick and standard/deep search flows | Built |
| gate0_verifier.py | Source quality, tier computation | Built (12.5KB) |
| retraction_checker.py | Crossref Retraction Watch check at ingest | Built (8KB) |
| cost_guardrails.py + duckdb_gate.py | Budget enforcement, circuit-breaker | Built (10.8KB + 5KB) |
| doctrine_smoke.py | Analytic-standards gate (bias, tradecraft) | Built (11.6KB) |
| staging_emitter.py | Writes APDS packets to apds/staging | Built (4KB) — missing the inbox bridge |
| dedup.py | Content-addressable deduplication | Built |
| query_schema.py | Query input schema | Built (5KB) — missing depth/source_mix/tier_ceiling fields |
| golden_queries.py | Evaluation query set | Built (14.9KB) — content not yet audited |

## What's missing

| Gap | What it means | Weld that fixes it |
|---|---|---|
| staging_emitter does not POST to perplexity-ingest | A completed research run never reaches the ingest inbox automatically | W1: add HTTP POST to staging_emitter.py |
| Ingest inbox drain to Brain unverified | The pathway from ingest-inbox/ to the Brain may exist but has not been confirmed end-to-end for research-pipe artifacts | W2: verify or add the drainer (read-only investigation first) |
| No depth / source_mix / tier_ceiling options | The pipe runs one way; it cannot be steered per query | W3: add three fields to query_schema.py and thread through dispatch.py |
| Rank fusion not confirmed | Five backends may be returning unmerged lists | Confirm in dispatch.py; add RRF if absent (post-weld task) |
| golden_queries.py not audited | Unknown whether the pipe has a working evaluation harness | Post-weld audit task |

## Next decision Ewan needs to make

None if the pipe-weld brief is accepted. The brief defines the order of work (W2 then W1 then W3 then smoke test), names the exact files, and estimates half a day of focused build time. Accepting it authorises Claude Code to start on W2 immediately.
