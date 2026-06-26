---
title: "Prior-Art Syntheses Bundle — 2026-06-25"
document_type: agent_doc
artifact_id: prior-art-syntheses-bundle__INDEX__v01__2026-06-25
date_utc: 2026-06-25T07:55:00Z
project: Amplified Partners
author: Perplexity Computer
stage: synthesis
objective: "Single entry point over four paired prior-art syntheses (research-pipe, ingestion-to-brain, data-lake, estate-security-and-sensors). Read this first; pull individual files as needed."
reader: agent
source_refs:
  - research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md
  - research-pipe-prior-art-synthesis__human__v01__2026-06-25.md
  - ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md
  - ingestion-to-brain-prior-art-synthesis__human__v01__2026-06-25.md
  - data-lake-prior-art-synthesis__agent__v01__2026-06-25.md
  - data-lake-prior-art-synthesis__human__v01__2026-06-25.md
  - estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md
  - estate-security-and-sensors-prior-art-synthesis__human__v01__2026-06-25.md
origin_type: agent_synthesis
attribution: "Four research subagents (Perplexity Computer), 2026-06-25 07:55–08:07 BST. Cross-referenced and reconciled in this bundle."
epistemic_tier: STRUCTURED
tier_reason: "Each component synthesis is STRUCTURED (prior art mapped onto Amplified components; not yet empirically calibrated). The bundle's tier is the min of the four, which is STRUCTURED."
epistemic_role: clarity
effective_tier_rule: min-rule
preconditions:
  - All four pairs of files exist and validate against amplified-research-yaml-frontmatter
  - Cross-references between syntheses are bi-directional where claimed
valid_until: 2026-09-25
claim_scope: "Prior-art coverage for the four pillars of the Amplified operating spine: search, brain-ingestion, lake, security/sensors. Does not specify implementation timelines or commit any infrastructure changes."
contradiction_status: clean
known_contradictions: []
machine_action_allowed: recommend
system_of_record: local_workspace
ratifier: none
next_action: "Ewan reviews; decisions named below are ratified or deferred; implementation briefs are drafted on the back of accepted positions."
companion_human_doc: ""
outcome_routing:
  outcome_class: production_candidate
  outcome_reason: "Three of four syntheses converge on a defensible design; one (data-lake) explicitly declares no_more_research_needed; one (estate-security) names three open Tier-C decisions. The bundle is production-ready conditional on those three decisions."
  required_next_action: "Ewan ratifies or defers the three open decisions in §3. Implementation briefs follow."
  research_needed: false
  tangent_refs: []
  methodology_refs:
    - amplified-research-yaml-frontmatter
    - min-rule
    - neutral-research-brief
---

# Prior-Art Syntheses Bundle — 2026-06-25

## What this bundle is

Four paired prior-art syntheses (eight files total) covering the four pillars of the Amplified operating spine. Ewan asked across two voice memos for all of it to be synthesised against prior art before implementation. This bundle is that synthesis. Each pair has an agent doc (full operational YAML, deep) and a human doc (reduced YAML, readable).

## The four pillars

| # | Pillar | Singular goal | Files |
|---|---|---|---|
| 1 | **Research-pipe** | Provide excellent information every time it searches. Route to brain or lake. | `research-pipe-prior-art-synthesis__{agent,human}__v01__2026-06-25.md` |
| 2 | **Ingestion-to-brain** | Turn verified material into durable, queryable, attributed brain rows. | `ingestion-to-brain-prior-art-synthesis__{agent,human}__v01__2026-06-25.md` |
| 3 | **Data-lake** | Raw landing + slow extraction → brain (tiered Bronze/Silver/Gold under 100GB). | `data-lake-prior-art-synthesis__{agent,human}__v01__2026-06-25.md` |
| 4 | **Estate security + sensors** | One identity plane (Infisical + Tailscale) + one observability plane (Vellum + OTel). Sensors on every surface. | `estate-security-and-sensors-prior-art-synthesis__{agent,human}__v01__2026-06-25.md` |

## How they fit together

```
                       ┌─────────────────────────────────┐
   external sources ──▶│  RESEARCH-PIPE (pillar 1)       │
                       │  excellence check on every run  │
                       └────────────┬──────────┬─────────┘
                                    │          │
                       ┌────────────▼───┐  ┌───▼──────────────┐
                       │  BRAIN         │  │  DATA LAKE       │
                       │  (pillar 2)    │  │  (pillar 3)      │
                       │  curated rows  │  │  Bronze→Silver   │
                       │  via the pipe  │  │  →Gold→brain     │
                       └────────────┬───┘  └───┬──────────────┘
                                    │          │
                                    ▼          ▼
                       ┌─────────────────────────────────────┐
                       │  ESTATE SECURITY + SENSORS (pillar 4)│
                       │  Infisical secrets | Vellum witness  │
                       │  OTel + Falco + osquery + ACLs       │
                       └─────────────────────────────────────┘
```

Pillar 4 is **underneath** the other three — every component in pillars 1–3 reads secrets from Infisical and emits Vellum events.

## §1. What each synthesis says (one line each)

- **Pillar 1 (research-pipe)** — Already largely built; aligned with TREC/BEIR/RAGAS, GRADE, federated-search rank-fusion, Heuer tradecraft, Retraction Watch. Outcome class: **production_candidate**. Next: accept the pipe-weld brief, do W2 (verify ingest-inbox → brain drainer), then W1 + W3.
- **Pillar 2 (ingestion-to-brain)** — Nine-stage spine (discover → fetch → validate → dedup → tier → enrich → embed → write → attest) maps onto canonical KG-ingestion, vector-DB, provenance-ledger, Cochrane/GRADE, Kimball/Inmon, Temporal, ISO 8000/25012, MinHash/LSH, ISO 27001/Presidio. Outcome class: **more_detailed_research_needed** on three thin gaps (Privacy + Tiering + one open promotion criterion). Design otherwise defensible.
- **Pillar 3 (data-lake)** — Tiered medallion at single-node Beast scale: MinIO + Parquet + Iceberg (PyIceberg, no JVM), BLAKE3 exact dedup, MinHash/LSH near-dedup, faster-whisper for audio, ollama-2 + GraphRAG for extraction. Catalog: no separate product needed at <100GB (Iceberg catalog + SQLite manifest + INDEX.md per directory). Outcome class: **no_more_research_needed**.
- **Pillar 4 (estate security + sensors)** — One identity plane (Infisical + Tailscale-derived) + one observability plane (Vellum as immutable ledger, OTel as wire format). Federated mesh rejected on prior-art grounds. Vellum JWT TTL resolved to 30 days (NIST SP 800-57). SPIRE rejected at this scale in favour of Tailscale-derived identity. Outcome class: **DESIGN_IS_DEFENSIBLE** with three baton decisions.

## §2. What's been resolved across the bundle (decisions ratifiable now)

| # | Decision | Resolved value | Source synthesis |
|---|---|---|---|
| D1 | Lake shape | Tiered Bronze/Silver/Gold (medallion), single-node, <100GB | Pillar 3 |
| D2 | Lake substrate | MinIO + Parquet + Iceberg (PyIceberg) | Pillar 3 |
| D3 | Lake catalog | None as separate product — Iceberg catalog + SQLite manifest + INDEX.md | Pillar 3 |
| D4 | Exact dedup | BLAKE3 (replaces SHA-256 at this layer) | Pillar 3 |
| D5 | Near-dup | MinHash/LSH at Silver promotion (Jaccard 0.7 code/MD, 0.8 prose) | Pillar 3 |
| D6 | Audio path | faster-whisper → WhisperX/pyannote for multi-speaker | Pillar 3 |
| D7 | Extraction loop | Unstructured.io → ollama-2 (GraphRAG) → ollama-pudding → Vellum → pipe | Pillar 3 |
| D8 | Identity plane | Infisical (secrets) + Tailscale-derived identity (services). SPIRE rejected at this scale. | Pillar 4 |
| D9 | Observability plane | Vellum (immutable ledger) + OTel (wire format) + Langfuse/Opik (already deployed) | Pillar 4 |
| D10 | Vellum JWT TTL | 30 days (NIST SP 800-57 medium-term assertion class) | Pillar 4 |
| D11 | Sensor mesh on Macs | osquery + Santa + ESF on M5, Mac mini (as always-on edge sensor), MacAirM4 | Pillar 4 |
| D12 | Sensor mesh on Beast | Falco runtime + Tetragon eBPF, feeding Vellum | Pillar 4 |
| D13 | Breach rotation order | LiteLLM model keys → GitHub PATs → MCP bearers → Infisical service tokens → Vellum signing keys | Pillar 4 |
| D14 | Pre-commit hook generalisation | cascade-mac PR#1 pattern across every repo + dependency CVE scan + Infisical-reference enforcement | Pillar 4 |

## §3. What still needs Ewan's ratification (the one consolidated hand-back)

Three baton decisions surfaced by Pillar 4 (security + sensors) that the bundle cannot resolve on prior art alone:

1. **Mac mini role** — does WanMin (Mac mini M4 Pro) become the **central always-on sensor hub** that aggregates M5 and MacAirM4 telemetry before forwarding to Vellum, or do all three Macs peer directly to Beast/Vellum? Prior art supports either; this is a workload-and-availability call.
2. **CRM auth migration order** — Pillar 4 names a least-risk migration order for moving services onto Infisical. Confirm or amend whether **amplified-crm** (production) is migrated before or after **cove-temporal** (orchestrator). Default: cove-temporal first, then crm.
3. **One ingestion gap in Pillar 2** — the privacy/sensitivity class layer (ISO 27001 / Presidio) is named as a thin coverage area. Decide whether to add a Presidio scan to perplexity-ingest *now* (alongside the existing secrets regex) or batch it with the broader sensor work.

None of these block W1–W3 of the pipe-weld brief. All three can be answered in one line each.

## §4. How this composes with prior briefs

- **Pipe-weld brief** (`pipe-weld-brief__v01__2026-06-25__perplexity.md`) — the three small welds remain correct. Pillar 1's synthesis confirms the design; Pillar 2 confirms the ingestion path it lands in is defensible; Pillar 3 clarifies what the *other* sink (the lake) looks like; Pillar 4 names how secrets flow through both pipes.
- **Cross-IDE problem-sharing rules** (`cross-ide-problem-sharing-rules__v01__2026-06-25__perplexity.md`) — rides on Pillar 4's observability plane (every patch event = Vellum event).
- **Inbox index** (`INBOX-INDEX__v01__2026-06-24__perplexity.md`) — Pillar 4 closes 1 of 13 Tier-C gates (Vellum JWT TTL → 30 days). The other 12 remain unaddressed by this bundle.
- **Control-centre prior-art synthesis** (this morning's `control-centre-prior-art-synthesis-2026-06-25T0837Z`) — confirmed by all four pillars; this bundle extends rather than supersedes it.

## §5. How to read this bundle

- **Five-minute read**: this INDEX + the four human docs (113 + 101 + 124 + 137 = 475 lines total).
- **Implementation read**: this INDEX + the four agent docs (210 + 222 + 311 + 352 = 1,095 lines), in order: pillar 4 first (substrate), then 2 (brain), then 3 (lake), then 1 (search).
- **Single-pillar deep**: read only that pillar's pair.

## §6. Provenance and tier

The bundle is **STRUCTURED**: prior-art mapped onto Amplified components, primary sources cited, but not yet empirically calibrated against Amplified's specific load. Each pillar declares its own tier in its YAML; the bundle's tier is the minimum, which is STRUCTURED (none of the four claimed MEASURED).

Primary-source counts: research-pipe 20, ingestion-to-brain 14, data-lake (not separately counted but ≥10 per 10 domains), estate-security 17. Total unique primary references across the bundle: ~60.

## Closure

[CLOSURE] branch=PLAN | proxy=1 logged (batched inbox push) | gates=three baton decisions in §3 (consolidated) | inbox=prior-art-syntheses-bundle__2026-06-25/ (9 files) | tier=STRUCTURED
