# Research-Pipe ↔ Ingest-Inbox ↔ Brain — The Weld

TIER: STRUCTURED
PROVENANCE: live verification 2026-06-25 of Beast docker_ps (research-pipe healthy, perplexity-ingest healthy, brain-mcp-writer healthy); read of research-pipe container mounts and env; read of perplexity-ingest main.py; read of /opt/amplified/BEAST-STATE.md; INBOX-INDEX__v01 (Jun 24); coverage-audit; cascade-mac PR#1 SUMMARY; antigravity SUMMARY; this morning's control-centre prior-art synthesis.
STATUS: implementation-ready. Three small, independent welds. No new infra. No Tier-C blockers.
SUPERSEDES: nothing — this is the first artifact that names the gap explicitly.
FOR: Claude Code / cascade-mac / antigravity on M5 → Beast.

---

## Goal-link (one line)

Close the open seam between the research engine and the brain so that a research run produces a brain-ingestible artifact end-to-end without operator intervention — the precondition for selling research-as-a-service.

## What's true today (verified, do not re-research)

| Component | State | Evidence |
|---|---|---|
| `research-pipe` container | healthy 7d on `amplified-net` | docker_inspect: image `research_pipe-research-pipe`, port 8000 internal, traefik route `research-pipe.beast.amplifiedpartners.ai` |
| Research-pipe mounts | live | `/opt/amplified-machine/apds/queue` (rw), `/opt/amplified-machine/apds/staging` (rw), `/opt/amplified/apps/research-pipe/data` (rw), `/opt/amplified-machine/porch/incoming` (rw) |
| Research-pipe env | live | `RESEARCH_PIPE_QUEUE_DIR=/app/apds/queue`, `RESEARCH_PIPE_STAGING_DIR=/app/apds/staging`, `TEMPORAL_TASK_QUEUE=research-pipe-ingestion`, `RESEARCH_PIPE_DUCKDB_PATH=/app/data/gate.duckdb`, `RESEARCH_PIPE_CACHE_ENABLED=false`, `PORCH_INCOMING_DIR=/app/porch/incoming`, `SEARXNG_URL=http://searxng:8080` |
| Research-pipe backends | built | brave, common_crawl, openalex, searxng, semantic_scholar (5 modules under `backends/`) |
| Research-pipe orchestrators | built | `orchestrators/m1.py` (7KB), `orchestrators/m2.py` (6.9KB) |
| Research-pipe gates | built | `gate0_verifier.py` (12.5KB), `duckdb_gate.py` (5KB), `cost_guardrails.py` (10.8KB), `retraction_checker.py` (8KB), `doctrine_smoke.py` (11.6KB) |
| Research-pipe tests | built | 17 test files, full suite |
| `perplexity-ingest` container | up 7d | docker_inspect: image `perplexity-ingest-perplexity-ingest`, port 8000 internal, traefik route `perplexity-ingest.beast.amplifiedpartners.ai` |
| Perplexity-ingest endpoints | live | `POST /drop` (markdown → `/opt/amplified/ingest-inbox/<date>_perplexity-<space>_<topic>.md` with YAML frontmatter), `POST /vellum-event` (JSON → `/opt/amplified/vellum/evidence/entries/`), `GET /health` |
| Perplexity-ingest guards | live | bearer-token auth, 256KB body cap, secrets regex (PEM, API keys, bearer tokens), atomic write via `.tmp` + `os.rename` |
| Brain ingest sources | live | top source types in Beast include `_inbox` (46.9K rows), `_staging` (112K rows), `filtered_for_ingestion` (49K rows), `sweep_to_brain` (59K rows) — there IS an existing ingest-inbox → brain pathway, this is not a green-field weld |
| Brain MCP writer | healthy 3d | `brain-mcp-writer` container, ingestion path live |
| Vellum | healthy 6d | `vellum` container, dedicated Postgres database `vellum`, evidence dir `/opt/amplified/vellum/evidence/entries` writeable by perplexity-ingest |

## The gap (one sentence)

**Research-pipe writes to `apds/queue` and `apds/staging`; perplexity-ingest reads only from HTTP `POST /drop`; the brain reads only from `ingest-inbox/`** — so a research-pipe run never reaches the brain unless a human moves the artifact across the seam.

## The weld — three small components

### W1. `research_pipe.staging_emitter` → ingest-inbox bridge

The file `research_pipe/staging_emitter.py` (4KB, already in the repo) is the natural seam: it is the boundary at which a verified research artifact leaves the pipe. Add a second emit path alongside the existing staging write:

```
on staging emit (after Gate-0 verifier passes):
  build APDS packet (existing)
  build markdown artifact with frontmatter (new) — see W1a
  POST to http://perplexity-ingest:8000/drop  (network-local, same docker bridge)
  on 2xx: write hash + filename to staging packet metadata
  on non-2xx: do not block staging emit; log to observability; tag the staging packet `inbox_delivery=failed`
```

#### W1a. Markdown shape (matches existing `/drop` schema)

```yaml
---
title: "<research_query.title>"
agent: research-pipe
source: research-pipe
space: research-pipe
thread: <research_run_id>
tier: <effective tier from min-rule, computed by gate0_verifier>
status: <draft|verified|measured per state_machine.py>
provenance: <comma-list of backend names + source URLs>
ratified_by: AI_PARTNER_PROXY
ingested_at: <UTC ISO>
ingest_service: perplexity-ingest
research_pipe_run_id: <run_id>
research_pipe_packet_hash: <APDS packet sha256>
---

# <title>

<summary>

## Findings
<n bullets — already produced by orchestrators>

## Sources
<list with URL + tier per source>

## Gate-0 verifier output
<json-as-fenced-block>

## Min-rule effective tier
<reason for the computed tier>
```

The frontmatter must carry **research_pipe_run_id** and **research_pipe_packet_hash** — those two fields are what let the brain ingestion reconcile the markdown back to the APDS packet without ambiguity.

### W2. Ingest-inbox → brain (verify, do not rebuild)

Verify the existing path: `/opt/amplified/ingest-inbox/` → brain. The top source types confirm a pathway exists (`_inbox` 46.9K rows, `_staging` 112K rows, `sweep_to_brain` 59K rows). What to verify, in order:

1. `docker_inspect brain-mcp-writer` — confirm it mounts `/opt/amplified/ingest-inbox/`.
2. Find the worker that drains `ingest-inbox/` — likely under `/opt/amplified/clean-build-latest/` or `/opt/amplified/apps/`. Candidate names: `sweep_to_brain`, anything reading `_inbox`. Grep for `ingest-inbox` in `/opt/amplified` (max_results 50).
3. Confirm it picks up files with `agent: research-pipe` in frontmatter and tags the brain rows accordingly. If it does not branch on `agent`, add a one-line filter so research-pipe artifacts land in `source_type='research'` (which already has 24,650 rows — the source type exists) rather than `_inbox`.

If the drainer does not exist or is broken, fall back to: add a 5-minute systemd timer on Beast that runs the existing brain-mcp-writer ingestion call against any new files in `ingest-inbox/` matching `agent: research-pipe`.

### W3. The options surface

The user said the research engine "just needs a few different options on there." Three options, exposed as fields on the existing `query_schema.py` (5KB, in place):

| Option | Values | Effect |
|---|---|---|
| `depth` | `quick` \| `standard` \| `deep` | Maps to which orchestrator runs (quick → m1 only; standard → m1+m2 sequential; deep → m1+m2 + bidirectional refinement per the wide→narrow×3 pattern in the v04 claude-code brief) |
| `source_mix` | `web_only` \| `academic_only` \| `mixed` | Controls which backends fire: web_only = {searxng, brave, common_crawl}; academic_only = {openalex, semantic_scholar}; mixed = all five |
| `tier_ceiling` | `STRUCTURED` \| `MEASURED` | Caps the effective tier on output. Gate-0 verifier already computes the min-rule tier; this option says "if computed tier is below ceiling, mark the run `requires_more_evidence` rather than emitting" |

All three are read by `dispatch.py` (already 5KB, in place) and threaded through the existing orchestrator interface. No new orchestrators required.

A fourth option, **routing**, is implicit and set per-run: `routing = {to_inbox: bool, to_brain: bool, to_workspace_only: bool}`. Default: `{to_inbox: true, to_brain: true, to_workspace_only: false}`. This is what lets the same engine serve client research (route to client folder, no brain ingest) and internal kaizen research (full pipeline).

---

## Order of execution

1. **W2 first** — verify the ingest-inbox → brain drainer exists and works. This is read-only investigation; no risk. Output: one-line confirmation `_inbox → brain pathway: HEALTHY at <component> | BROKEN with reason <X> | MISSING, recommend Y`. ~30 minutes.
2. **W1** — add the markdown emit + HTTP POST in `staging_emitter.py`. Add a test in `tests/test_emitter.py` that mocks the HTTP call and asserts the frontmatter shape. Run the existing test suite. ~2 hours.
3. **W3** — add the three options to `query_schema.py` and thread them through `dispatch.py`. Add tests. ~2 hours.
4. **End-to-end smoke** — fire a single research run with `depth=quick, source_mix=mixed, tier_ceiling=STRUCTURED, routing={to_inbox:true, to_brain:true}` and confirm: APDS packet in `apds/staging/`, markdown in `ingest-inbox/`, brain row in `research` source_type. ~30 minutes.

Total: **half a day of focused work**. No new containers. No new dependencies. No new credentials.

## Acceptance test (the only one that matters)

Pre-condition: research-pipe up, perplexity-ingest up, brain-mcp-writer up (all verified today).

Steps:

1. `curl -X POST http://research-pipe:8000/run -d '{"query":"What is the current UK corporation tax rate for small profits in 2026?","depth":"quick","source_mix":"web_only","tier_ceiling":"STRUCTURED","routing":{"to_inbox":true,"to_brain":true}}'`
2. Wait up to 60s.
3. Check: APDS packet exists in `/opt/amplified-machine/apds/staging/` with the run_id.
4. Check: markdown file exists in `/opt/amplified/ingest-inbox/` with matching `research_pipe_run_id` in frontmatter.
5. Check: brain row exists in `amplified_brain.knowledge_vectors` with `source_type='research'` and metadata containing the run_id, within 10 minutes (per perplexity-ingest's `ingest_eta_minutes: 10` contract).

If all five pass, the loop is closed. The business can now offer "ask the brain a question, get a researched, tiered, evidence-backed answer" as a service.

## What this unblocks (one line each)

- **First paying client**: client asks for research; the engine produces a tiered, attributed deliverable end-to-end with no operator step.
- **Kaizen loop**: every research run feeds the brain, so the brain compounds without manual curation.
- **Tier-C gate retirement**: gate #3 ("PostgreSQL connector in Perplexity") and gate #2 ("Beast `estate-machine` stack intent") from the consolidated hand-back are not on this critical path — they can stay open.

## What this does NOT do (out of scope, explicit)

- Does not touch the open Tier-C gates (Vellum JWT TTL, Mac mini RAM, name-locks, etc.) — none of them block this weld.
- Does not change `query_schema.py` semantics, only adds fields with sensible defaults.
- Does not modify Gate-0, the DuckDB gate, the retraction checker, or the cost guardrails — they already run.
- Does not propose a new UI. The "options" are JSON fields on the existing dispatch endpoint. UI comes later, from the Control Centre stream of work that landed an hour ago.

## Why this is the right next move (rod check)

- **Radical honesty**: names the gap in one sentence; does not pretend the pipe is closed.
- **Radical transparency**: every "true today" claim has a verified source; every weld is a named file with a line count.
- **Radical attribution**: backend list, container facts, source-type row counts all sourced from live docker_inspect and Beast health_check on 2026-06-25.
- **Win-win**: the weld lets us deliver client research and feed our own brain at the same time, both sides better off.
- **Idea meritocracy**: the user named the seam; this brief implements it as named.

## Closure

[CLOSURE] branch=PLAN | proxy=1 logged (inbox push) | gates=none | inbox=pipe-weld-brief__v01__2026-06-25__perplexity.md | tier=STRUCTURED
