---
title: "Ingestion-to-Brain Prior Art Synthesis — Human"
document_type: readable_research_conclusion
artifact_id: "ingestion-to-brain-prior-art-synthesis__human__v01__2026-06-25"
date_utc: "2026-06-25T08:00:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: synthesis
audience: Ewan
purpose: "Confirm that the ingestion-to-brain design is defensible against prior art, name what is strong, thin, and missing, and identify the one remaining decision."
source_refs:
  - "https://www.w3.org/TR/prov-o/"
  - "https://docs.sigstore.dev/logging/overview/"
  - "https://www.rfc-editor.org/rfc/rfc9162.pdf"
  - "https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14"
  - "https://www.dni.gov/files/documents/ICD/ICD-203.pdf"
  - "https://arxiv.org/abs/1603.09320"
  - "https://arxiv.org/abs/1908.10084"
  - "https://www.cs.cornell.edu/~shmat/courses/cs6434/fellegi-sunter.pdf"
attribution: "Research synthesis by Perplexity Computer, 2026-06-25. Prior-art sources cited inline."

epistemic_tier: STRUCTURED
epistemic_role: clarity
tier_reason: "Pipeline stages mapped to named prior-art patterns with citations. Tier assignments and gap calls are judgment-based, not empirically calibrated."
confidence_plain_english: "The design is coherent and has a named prior-art lineage for every stage. Three gaps are real and should be closed before production gate sign-off."
open_questions:
  - "Does Vellum compute a signed checkpoint (Merkle root) or only store flat event entries?"
  - "What algorithm drives the near-dedup step in filtered_for_ingestion?"
  - "What tier applies to store_b_clean (1.19M rows) and store_m5_drop_2026_05_11 (447K rows)?"

companion_agent_doc: "ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md"
system_of_record: local_workspace
machine_action_allowed: recommend
next_human_decision: "Confirm Vellum Merkle checkpoint exists (or commission it), then sign off the production gate."
outcome:
  class: more_detailed_research_needed
  plain_english_reason: "Three thin spots require confirmation before the design can be called fully production-gated: Vellum checkpoint, near-dedup algorithm, and tier assignment for the two largest source stores."
---

The brain's ingestion path maps cleanly onto established computer-science and data-engineering prior art at every stage — the design is defensible — with one functional witness gap (Vellum's Merkle checkpoint) and two documentation gaps that need to be closed before production gate sign-off.

---

## What the brain is now (2026-06-25)

The Amplified brain (`amplified_brain` on Beast / cove-postgres) holds **2.64 million vectors** across roughly 15 named source types. The five largest are `store_b_clean` (1,187,422 rows), `store_m5_drop_2026_05_11` (447,286), `document` (309,870), `_staging` (112,161), and `vault-markdown` (111,721). The graph layer (Apache AGE) contains 53,900 entities and 4,200 episodes. Five containers are live and healthy: `brain-mcp-writer`, `brain-mcp-readonly`, `brain-web`, `amplified-knowledge-mcp`, and `plumb-knowledge-http`. The perplexity-ingest drop zone accepts material via a single authenticated endpoint and enforces a 256 KB cap and secrets scan before anything touches the store.

---

## How material gets in today

| Stage | What happens | Beast component | Scale (rows) |
|-------|-------------|-----------------|-------------|
| Discover | External sources are harvested by the APDS workflow | `apds_ingestion_workflow.py` | upstream |
| Fetch | Raw material lands in inboxes | `_inbox`, `_inbox-voice` | 77,815 |
| Validate / filter | Schema checks, secrets scan, size cap | `_staging`, `filtered_for_ingestion` | 161,473 |
| Dedup | Exact-match hash check; near-duplicate filter | `filtered_for_ingestion` | absorbs above |
| Tier | Source type label assigned (determines trust level) | `source_type` column on every row | all 2.64M |
| Enrich | Graph relationships extracted | Apache AGE graph | 53,900 entities |
| Embed | Text converted to 384-dimension vectors via Ollama all-MiniLM | pgvector HNSW index | 2.64M vectors |
| Write | Rows written idempotently (duplicate = no-op) | `brain-mcp-writer`, `sweep_to_brain` (59,007) | cumulative |
| Attest | Immutable event record written by Vellum sensor | `/opt/amplified/vellum/evidence/entries/` | per packet |

---

## What prior art says we should be doing

- **Provenance on every row.** The [W3C PROV-O standard](https://www.w3.org/TR/prov-o/) (2013) defines Entity, Activity, and Agent as the three required fields to describe where anything came from. Every brain row needs all three to be auditable.
- **Append-only witness log.** [Sigstore Rekor](https://docs.sigstore.dev/logging/overview/) and [Certificate Transparency (RFC 9162)](https://www.rfc-editor.org/rfc/rfc9162.pdf) both require a Merkle tree whose root hash is periodically signed so that an independent party can prove no entries were deleted or altered. Vellum's flat event entries are the right idea; the signed checkpoint is the missing piece.
- **Four-level evidence grading.** The [Cochrane GRADE system](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14) and [US intelligence ICD 203](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) both require that every piece of evidence carry an explicit confidence tier (High / Moderate / Low / Very Low in GRADE; Amplified's equivalent is PROVEN / MEASURED / STRUCTURED / INTUITED). The tier of any conclusion is bounded by the weakest input — this is the min-rule.
- **Two-layer dedup.** SHA-256 catches exact copies. [MinHash + LSH (Broder 1997)](https://www.cs.cornell.edu/courses/cs4860/2009sp/lec-04.pdf) catches near-duplicates (paraphrases, reformatted versions). Both layers are needed; exact-match alone lets semantically identical content accumulate.
- **Probabilistic entity resolution.** [Fellegi & Sunter (1969)](https://www.cs.cornell.edu/~shmat/courses/cs6434/fellegi-sunter.pdf) proved that assigning match weights across fields and thresholding probabilistically is the optimal record-linkage strategy. The brain's 53,900 AGE entities should have a documented resolution algorithm with declared false-merge tolerance.
- **Idempotent, durable workflow orchestration.** [Temporal](https://temporal.io/blog/workflow-engine-principles) (already running as `cove-temporal` on Beast) provides exactly-once execution with deterministic replay: if a worker crashes mid-ingest, the workflow restarts from the last successful step without re-writing rows. This is the correct pattern.
- **PII screening before write.** [GDPR Article 9](https://gdpr-info.eu/art-9-gdpr/) requires explicit justification for processing special-category data (health, biometric, political opinion). The current secrets regex blocks credentials; it does not screen for personal data in `_inbox-voice` (30,926 rows) or `transcripts` (30,242 rows). See companion: `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.

---

## What's strong

- Nine-stage pipeline is fully implemented and running at production scale (2.64M vectors).
- Idempotent write pattern (`ON CONFLICT DO UPDATE`) prevents duplicate rows.
- Vellum sensor fires on every packet — the witness layer exists.
- Temporal is the orchestrator and provides durable, replayable execution.
- HNSW index (pgvector) and Ollama all-MiniLM are the right choices for this scale and embedding dimension.
- Apache AGE provides graph enrichment; 53,900 entities and 4,200 episodes demonstrate the layer is live.
- The pre-production 9-item gate maps coherently to Temporal workflow primitives.
- The secrets regex at the drop endpoint prevents credential leakage into the store.

---

## What's thin

- **Vellum checkpoint**: event entries exist but it is not confirmed whether a signed Merkle root (the piece that makes the ledger independently verifiable) is computed. Without it, Vellum is a log, not a witness in the Rekor/CT sense.
- **Near-dedup algorithm**: the `filtered_for_ingestion` stage almost certainly performs near-dedup, but the algorithm (MinHash parameters, band/row settings) is not documented. Cannot audit recall without it.
- **Tier assignment for the two largest stores**: `store_b_clean` (1.19M rows, 45% of the brain) and `store_m5_drop_2026_05_11` (447K rows, 17%) have no documented GRADE-equivalent tier. Until confirmed, downstream conclusions drawing on them should be treated as INTUITED.
- **Entity resolution algorithm**: Apache AGE entities are present but the resolution method (rule-based vs. probabilistic vs. embedding cosine) is not documented. False-merge rate is therefore unknown.

---

## What's missing

- A Presidio-style PII scan at the validate stage (stage 3) for GDPR Article 9 special-category data — particularly relevant for `_inbox-voice` and `transcripts`. See companion: `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.
- A signed Merkle checkpoint on the Vellum ledger (the piece that elevates it from "log" to "witness" in the Certificate Transparency sense).
- Documented MinHash/LSH parameters so near-dedup recall can be audited.

---

## Next decision

Confirm whether Vellum computes a signed Merkle checkpoint; if not, commission it — this is the single change that closes the largest structural gap and makes the witness layer fully defensible.

*— STRUCTURED · Perplexity Computer synthesis · 2026-06-25*
