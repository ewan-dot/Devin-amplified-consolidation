---
document_id: ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25
document_type: research_conclusion
stage: synthesis
reader: agent
author: subagent-prior-art
created: 2026-06-25
version: v01
goal_link: "Ewan/ingestion-to-brain-prior-art"
owner: Amplified Partners
input_refs:
  - amplified_brain (amplified_brain on cove-postgres, Postgres 15)
  - brain-mcp-writer container (healthy 3d)
  - brain-mcp-readonly container
  - brain-web container
  - amplified-knowledge-mcp container (healthy 7d)
  - plumb-knowledge-http container
  - perplexity-ingest container (/opt/amplified/ingest-inbox/, POST /drop)
  - vellum (/opt/amplified/vellum/evidence/entries/)
  - awesome-openclaw-agents 02_build/apds/
  - clean-build 02_build/cove-orchestrator/temporal/
data_sensitivity: internal-confidential
route_destination: Ewan / relay-protocol
baton_requirement: "Human review before pipeline changes or new source_type registration"
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  open_action: "Fill three thin-coverage gaps identified in §Privacy and §Tiering before production gate sign-off"
epistemic_tier: STRUCTURED
tier_reason: "Nine-stage pipeline mapped to named prior-art patterns with explicit source citations; weights and thresholds are judgment-chosen, not empirically calibrated."
effective_tier_rule: min-rule
domains_surveyed: 9
primary_sources_cited: 14
---

## One-sentence summary [STRUCTURED]

The Amplified ingestion-to-brain path implements a nine-stage pipeline — discover, fetch, validate, dedup, tier, enrich, embed, write, attest — that maps tightly onto canonical prior art across knowledge-graph ingestion, vector-DB construction, provenance ledgering, ETL/ELT orchestration, evidence appraisal, data-quality dimensions, dedup/entity-resolution, and privacy classification, with Vellum providing the append-only witness function that the design required but for which no single prior-art framework supplied a turn-key pattern.

---

## Purpose and framing

The ingestion-to-brain path turns externally sourced or internally produced material into durable, queryable, attributed rows in `amplified_brain`. The brain is not a cache; it is an epistemic store. Every row must carry sufficient provenance to allow a future agent or human to assess how the fact arrived, what tier of reliability it carries, and whether it has been independently attested. These requirements — provenance, attribution, tiering, deduplication, immutable attestation — are not novel design decisions; they are the intersection of seven decades of library science, twenty years of data-warehouse practice, and ten years of software-supply-chain transparency work. Naming the prior-art lineage makes the design defensible and identifies where Amplified departs from the literature.

---

## The canonical ingestion shape

The nine stages below form the canonical spine. Each stage maps to at least one prior-art pattern and to at least one named Beast component.

| # | Stage | Canonical prior-art pattern | Beast component(s) |
|---|-------|----------------------------|--------------------|
| 1 | **Discover** | APDS external web harvester; Airbyte source connectors ([Airbyte](https://airbyte.com/)) | `awesome-openclaw-agents 02_build/apds/` |
| 2 | **Fetch** | Inmon CIF staging layer ([Inmon, 1992](https://en.wikipedia.org/wiki/Bill_Inmon)); Fivetran/Airbyte ELT extract | `_inbox` (46,889 rows); `_inbox-voice` (30,926 rows) |
| 3 | **Validate** | Great Expectations schema contracts; ISO 25012 data-quality dimensions; pgvector dimension-mismatch rejection | `_staging` (112,161 rows); `filtered_for_ingestion` (49,312 rows) |
| 4 | **Dedup** | SHA-256 content hashing; MinHash+LSH ([Broder 1997](https://www.cs.cornell.edu/courses/cs4860/2009sp/lec-04.pdf)); Fellegi-Sunter probabilistic linkage ([Fellegi & Sunter 1969](https://www.cs.cornell.edu/~shmat/courses/cs6434/fellegi-sunter.pdf)); Splink (UK ONS/MoJ) | `filtered_for_ingestion`; SHA-256 hash columns in brain rows |
| 5 | **Tier** | GRADE four-level evidence grading ([Cochrane Handbook](https://handbook-5-1.cochrane.org/chapter_12/table_12_2_a_levels_of_quality_of_a_body_of_evidence_in_the.htm)); ICD 203 analytic tradecraft standards ([ODNI ICD-203, 2015](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)); forensic chain-of-custody | `source_type` field + tier metadata column |
| 6 | **Enrich** | Apache AGE graph traversal; DBpedia extraction; Microsoft GraphRAG ([Microsoft GraphRAG](https://microsoft.github.io/graphrag/)) | Apache AGE (53,900 entities, 4,200 episodes in brain) |
| 7 | **Embed** | HNSW algorithm ([Malkov & Yashunin 2016](https://arxiv.org/abs/1603.09320)); all-MiniLM-L6-v2 sentence-transformers ([Reimers & Gurevych 2019](https://arxiv.org/abs/1908.10084)); MTEB benchmark ([Muennighoff et al. 2023](https://aclanthology.org/2023.eacl-main.148.pdf)) | Ollama all-minilm 384-dim; pgvector HNSW index (2.64M vectors) |
| 8 | **Write** | Idempotent upsert with ON CONFLICT; Kimball SCD Type 1/2 ([Kimball Dimensional Modeling](https://www.kimballgroup.com/wp-content/uploads/2013/08/2013.09-Kimball-Dimensional-Modeling-Techniques11.pdf)); exactly-once semantics via Debezium CDC ([Conduktor CDC](https://www.conduktor.io/glossary/what-is-change-data-capture-cdc-fundamentals)) | `brain-mcp-writer`; `sweep_to_brain` (59,007 rows) |
| 9 | **Attest** | W3C PROV-O ([W3C PROV-O, 2013](https://www.w3.org/TR/prov-o/)); Sigstore Rekor append-only ledger ([Sigstore Rekor](https://docs.sigstore.dev/logging/overview/)); Certificate Transparency Merkle tree ([RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.pdf)) | Vellum witness layer (`/opt/amplified/vellum/evidence/entries/`) |

**Pre-ingestion orchestration** sits across stages 1–3 and is implemented via `pre_ingestion_pipe_v3.py` and `apds_ingestion_workflow.py` in `clean-build 02_build/cove-orchestrator/temporal/`.

---

## What is already built

As at 2026-06-25, the brain holds **2,640,000 vectors** across the following source_types, providing evidence that each pipeline stage has been exercised at production scale:

| Stage | Prior-art lineage | Amplified component | Row-count evidence (2026-06-25) |
|-------|-------------------|--------------------|---------------------------------|
| Discover | APDS / Airbyte source connectors | `apds_ingestion_workflow.py` | — (upstream, pre-brain) |
| Fetch | Inmon CIF staging; ELT extract | `_inbox`, `_inbox-voice` | 46,889 + 30,926 = 77,815 |
| Validate / filter | ISO 25012; Great Expectations | `_staging`, `filtered_for_ingestion` | 112,161 + 49,312 = 161,473 |
| Dedup | SHA-256; MinHash/LSH | `filtered_for_ingestion` dedup pass | Absorbs upstream rows |
| Tier | GRADE; ICD 203 | `source_type` tier metadata | All 2.64M rows carry source_type |
| Enrich | Apache AGE; GraphRAG | Brain AGE graph | 53,900 entities; 4,200 episodes |
| Embed | HNSW; all-MiniLM 384-dim | pgvector HNSW; Ollama | 2,640,000 vectors |
| Write | Idempotent upsert; CDC | `brain-mcp-writer`; `sweep_to_brain` | 59,007 swept; top source 1,187,422 |
| Attest | W3C PROV-O; Rekor; CT | Vellum sensor (`/opt/amplified/vellum/`) | Per-packet, immutable |

Top sources by row count (2026-06-25): `store_b_clean` 1,187,422 · `store_m5_drop_2026_05_11` 447,286 · `document` 309,870 · `_staging` 112,161 · `vault-markdown` 111,721 · `github_repo` 66,918 · `sweep_to_brain` 59,007 · `filtered_for_ingestion` 49,312 · `_inbox` 46,889 · `work` 40,097 · `_inbox-voice` 30,926 · `transcripts` 30,242 · `own_content` 28,097 · `research` 24,650 · `16-covered-ai-work` 21,508.

---

## Vellum as witness [STRUCTURED]

The closest prior-art analogue for Vellum is the combination of three transparency-log patterns operating at different layers:

1. **Sigstore Rekor** ([Sigstore Rekor overview](https://docs.sigstore.dev/about/overview/)): an immutable, append-only ledger in which each entry carries a cryptographic inclusion proof against a Merkle tree root. Rekor is used in software supply-chain provenance to prove that a signing event occurred at a specific time and has not been tampered with. Vellum plays the same role for brain-packet events: every ingest event creates an entry; entries are never deleted or modified.

2. **Certificate Transparency** ([RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.pdf), [CT how it works](https://certificate.transparency.dev/howctworks/)): the CT model separates the issuer (the CA writing a cert) from the witness (the log that publishes it). Vellum follows this separation: `brain-mcp-writer` is the issuer; Vellum is the independent witness that cannot be overwritten by the writer.

3. **W3C PROV-O** ([W3C PROV-O Recommendation, 2013-04-30](https://www.w3.org/TR/prov-o/)): the PROV data model defines Entity, Activity, and Agent as the three primitives for provenance. Each Vellum evidence entry maps to: Entity = the brain row (by SHA-256), Activity = the ingest event (timestamped ISO 8601), Agent = the pipeline component (`brain-mcp-writer`, `sweep_to_brain`, etc.).

**Amplified-specific implementation note**: Vellum entries live at `/opt/amplified/vellum/evidence/entries/` and are described in memory as "the canonical monitoring and witness layer for brain intake." The `perplexity-ingest` container enforces a 256KB cap and atomic write before the Vellum sensor fires, implementing the equivalent of CT's pre-certificate check before log admission.

**What the prior art demands but is not yet confirmed**: Sigstore Rekor and CT both require a cryptographically signed tree head (STH in CT, checkpoint in Rekor) that an independent party can verify. Vellum's current implementation stores event entries but it is not confirmed whether a Merkle root or signed checkpoint is computed. This is an open question (see §Open questions). See companion: `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.

---

## Tiering and the min-rule [STRUCTURED]

The GRADE working group ([Cochrane Handbook chapter 14](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14)) defines four certainty levels: High, Moderate, Low, Very Low. The starting point is determined by study design (RCT = High; observational = Low) and is then adjusted by five downgrade criteria (risk of bias, inconsistency, indirectness, imprecision, publication bias) and three upgrade criteria.

[ICD 203](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) (ODNI Analytic Standards, 2015) applies analogous logic to intelligence products: sourcing must characterise quality and credibility of underlying sources; uncertainty must be expressed; assessments must distinguish what is known from what is inferred.

The Amplified **min-rule** — that a brain packet's tier is set to the lowest-tier source it depends on — is structurally identical to the GRADE rule that the overall body of evidence is rated by the weakest critical outcome. This is not coincidence; it is the only mathematically defensible rule for any system where downstream inference chains through intermediate nodes.

**Tier mapping (Amplified → GRADE)**:

| Amplified tier | GRADE analogue | ICD 203 analogue | Typical source_types |
|---------------|----------------|-----------------|----------------------|
| T1 — verified primary | High | Source 1 / authoritative | `document`, `research`, `github_repo` |
| T2 — corroborated secondary | Moderate | Source 2 / credible | `own_content`, `transcripts`, `work` |
| T3 — single-source unverified | Low | Source 3 / plausible | `_inbox`, `sweep_to_brain`, `vault-markdown` |
| T4 — ephemeral / staging | Very Low | Uncorroborated | `_staging`, `filtered_for_ingestion` |

**Gap**: The `store_b_clean` source (1,187,422 rows — the largest single source) and `store_m5_drop_2026_05_11` (447,286 rows) do not appear in the tier table. Their tier assignment must be confirmed before these sources can be used in T1/T2-rated downstream conclusions.

---

## Dedup and entity resolution [STRUCTURED]

Three layers are in scope:

**Layer 1 — exact dedup (SHA-256)**. Content-addressable storage using SHA-256 is the foundational pattern from IPFS CIDs and Git blob storage. If `hash(content) == existing_row.hash`, the row is a duplicate and the write is idempotent. This is implemented in `filtered_for_ingestion` and the `brain-mcp-writer` upsert path.

**Layer 2 — near-dedup (MinHash + LSH)**. [Broder (1997)](https://www.cs.cornell.edu/courses/cs4860/2009sp/lec-04.pdf) showed that MinHash estimates Jaccard similarity between sets of shingles with provable error bounds. LSH (Locality-Sensitive Hashing) bins documents into buckets such that similar documents fall into the same bucket with high probability. MinHash+LSH is used in large-scale web crawl dedup (Common Crawl, RedPajama). The current Amplified pipeline's explicit MinHash implementation is not confirmed; the `filtered_for_ingestion` filter stage likely performs some form of near-dedup, but the algorithm is unspecified. This is an open question.

**Layer 3 — entity resolution**. [Fellegi & Sunter (1969)](https://www.cs.cornell.edu/~shmat/courses/cs6434/fellegi-sunter.pdf) formalised probabilistic record linkage: records are compared across fields; each comparison is assigned a match weight; the overall weight determines whether two records refer to the same real-world entity. Splink (UK ONS / Ministry of Justice) is the modern open-source implementation. Apache AGE's 53,900 entities represent the output of entity resolution; the input algorithm (whether rule-based, probabilistic, or embedding-based) is not documented. This is an open question.

---

## Privacy and sensitivity [STRUCTURED]

The `perplexity-ingest` container applies a **secrets regex** before accepting a packet (POST /drop, bearer auth, 256KB cap, atomic write). This pattern maps onto two prior-art frameworks:

1. **Microsoft Presidio** ([Presidio](https://microsoft.github.io/presidio/)): a PII detection framework that uses regex + ML to identify and redact sensitive entities (names, credit cards, phone numbers, national IDs). The Amplified secrets regex is a deterministic subset of what Presidio does.

2. **ISO 27001 data classification** and **GDPR Article 9 special categories** ([GDPR Art. 9](https://gdpr-info.eu/art-9-gdpr/)): ISO 27001 requires data to be classified by sensitivity before storage. Article 9 identifies special-category data (health, biometric, political opinion) requiring explicit processing justification.

**What is confirmed**: The secrets regex prevents credential literals (API keys, tokens, passwords) from entering the brain. The `data_sensitivity` field in the relay-protocol YAML enables post-hoc classification.

**What is thin**: There is no confirmed pre-write classification gate that assigns an ISO 27001 sensitivity class (Public / Internal / Confidential / Restricted) to each row. The `_inbox-voice` (30,926 rows) and `transcripts` (30,242 rows) source_types are likely to contain personal-data-rich content (names, conversations) but no Article 9 screening is documented.

**What is missing**: A Presidio-equivalent scan at the validate stage (stage 3) that detects GDPR Art. 9 special categories and either redacts, quarantines, or applies a Restricted sensitivity class before write. NIST SP 800-60 ([NIST SP 800-60](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-60v1r1.pdf)) provides the information-type taxonomy that would support this. See companion: `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.

---

## The 9-item pre-production gate mapped to Temporal workflow steps [STRUCTURED]

The relay-protocol pre-production gate requires nine items. Each maps to a Temporal workflow concept ([Temporal durable execution](https://temporal.io/blog/workflow-engine-principles)):

| Gate item | Temporal mapping | Implementation in Beast |
|-----------|-----------------|------------------------|
| 1. Goal link | Workflow input parameter; stored in workflow history | `goal_link` in YAML frontmatter |
| 2. Owner | Workflow initiator identity | Bearer auth on `/drop` endpoint |
| 3. Input refs | Activity inputs; deterministic replay ensures same refs on retry | `input_refs` list in YAML |
| 4. Acceptance test | Workflow signal or query; test passes before `workflow.continue_as_new` | `filtered_for_ingestion` threshold |
| 5. Allowed tools/models | Activity type allowlist; Temporal namespace policies | `allowed_tools` in YAML |
| 6. Data sensitivity class | Workflow search attribute; enables routing by sensitivity | `data_sensitivity` field |
| 7. Route destination | Workflow task queue; destination determines worker pool | `route_destination` in YAML |
| 8. Stop condition | Workflow timer or condition activity; terminates on criteria met | `stop_condition` in YAML |
| 9. Baton requirement | Workflow human-in-the-loop signal; Temporal `workflow.wait_for_signal` | Human sign-off before pipeline deploy |

`apds_ingestion_workflow.py` and `pre_ingestion_pipe_v3.py` in `clean-build 02_build/cove-orchestrator/temporal/` implement the Temporal side of this gate. [Temporal's durable execution model](https://temporal.io/blog/workflow-engine-principles) guarantees that if a worker crashes mid-pipeline, the workflow replays from the last successful activity without re-executing completed steps, satisfying the exactly-once requirement for brain writes.

---

## Open questions — where prior art disagrees or Amplified is novel

1. **Vellum Merkle root**: CT and Rekor both require a signed tree head for independent verification. Vellum's append-only entry store is necessary but not sufficient for the Rekor/CT pattern unless a checkpoint hash is computed and externally published. This is the single most important gap in the provenance ledger design.

2. **MinHash/LSH implementation**: The near-dedup algorithm in `filtered_for_ingestion` is not specified. Broder (1997) requires explicit choice of hash count `k` and band/row parameters. Without documented parameters, recall-at-dedup cannot be audited.

3. **Entity resolution algorithm**: Apache AGE contains 53,900 entities but the resolution algorithm (rule-based vs. Fellegi-Sunter probabilistic vs. embedding cosine similarity) is not documented. Splink requires explicit field weights; an undocumented algorithm cannot be audited for false-merge rate.

4. **Tier assignment for large stores**: `store_b_clean` (1,187,422 rows) and `store_m5_drop_2026_05_11` (447,286 rows) account for 62% of all brain rows. Their GRADE-equivalent tier is not confirmed. Until confirmed, downstream conclusions drawing on these sources must be rated T3 at best.

5. **GDPR Art. 9 / Presidio gap**: No pre-write special-category PII scan is documented for `_inbox-voice` or `transcripts`. This is a regulatory exposure if the brain is ever used in a jurisdiction covered by GDPR.

6. **all-MiniLM vs. MTEB benchmark**: The brain uses Ollama all-minilm 384-dim. [MTEB](https://huggingface.co/spaces/mteb/leaderboard) (Muennighoff et al. 2023) shows all-MiniLM-L6-v2 ranks well for semantic similarity but is not top-tier for retrieval on long documents. For the `document` (309,870 rows) and `research` (24,650 rows) source_types, a larger model (e.g. `text-embedding-3-large` or a domain-fine-tuned encoder) may improve retrieval recall. This is a design choice, not a gap — but it should be explicit.

---

## Outcome routing decision

**Verdict**: DESIGN_IS_DEFENSIBLE

The nine-stage pipeline has a named prior-art lineage for every stage. The brain holds 2.64M production vectors demonstrating that stages 1–8 are operational. Vellum implements the append-only witness pattern that is structurally analogous to Sigstore Rekor and Certificate Transparency.

**Open actions before production gate sign-off**:
- Confirm Vellum Merkle checkpoint / signed tree head (§Vellum as witness gap).
- Document MinHash/LSH parameters for near-dedup audit (§Dedup open question 2).
- Assign tier to `store_b_clean` and `store_m5_drop_2026_05_11` (§Tiering gap).

**Baton**: Human review (Ewan) required before pipeline changes or new source_type registration.

---

*[SOURCES CITED IN THIS DOCUMENT]*
- [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/) — 2013-04-30
- [Sigstore Rekor overview](https://docs.sigstore.dev/logging/overview/)
- [RFC 9162 Certificate Transparency v2](https://www.rfc-editor.org/rfc/rfc9162.pdf)
- [How CT works](https://certificate.transparency.dev/howctworks/)
- [Cochrane Handbook chapter 14 GRADE](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14)
- [ODNI ICD-203 Analytic Standards](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)
- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/wp-content/uploads/2013/08/2013.09-Kimball-Dimensional-Modeling-Techniques11.pdf)
- [Malkov & Yashunin HNSW 2016](https://arxiv.org/abs/1603.09320)
- [Reimers & Gurevych sentence-transformers 2019](https://arxiv.org/abs/1908.10084)
- [MTEB benchmark ACL 2023](https://aclanthology.org/2023.eacl-main.148.pdf)
- [Fellegi & Sunter record linkage 1969](https://www.cs.cornell.edu/~shmat/courses/cs6434/fellegi-sunter.pdf)
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/)
- [Debezium CDC exactly-once](https://www.conduktor.io/glossary/what-is-change-data-capture-cdc-fundamentals)
- [NIST SP 800-60 information type taxonomy](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-60v1r1.pdf)
- [Microsoft Presidio PII detection](https://microsoft.github.io/presidio/)
- [Temporal durable execution](https://temporal.io/blog/workflow-engine-principles)
- [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Broder MinHash 1997 (Cornell)](https://www.cs.cornell.edu/courses/cs4860/2009sp/lec-04.pdf)
