---
artifact_type: implementation_brief
title: BEAST-STATE.md correction — live-verified against running estate
author: Perplexity Computer (AI_PARTNER_PROXY)
attribution: drafted by Perplexity Computer; verified via live Beast read/write connector
created: 2026-06-24T11:35:00+01:00
tier: STRUCTURED
provenance: live Beast connector — docker_ps (84 containers), list_dir /opt/amplified, read BEAST-STATE.md (2026-06-24)
target: /opt/amplified/BEAST-STATE.md
route: through the pipe (Python + Rust + Vellum + AI + Human) — NOT a direct Beast write
---

# Implementation brief — refresh /opt/amplified/BEAST-STATE.md

## Why
The committed `/opt/amplified/BEAST-STATE.md` is stale and has drifted from the running estate. Drift verified live on 2026-06-24.

## Verified drift (live vs doc)

| Field | Doc says (2026-05-06) | Live reality (2026-06-24) |
|---|---|---|
| Container count | 42 | **84 total, ~60+ running healthy** |
| Graph DB | FalkorDB (`falkordb`, 4 graphs) | **No FalkorDB container running.** Postgres + Apache AGE graphs (per prior verified Beast brain: business_brain [old/corrupted], compound_design) |
| Vector DB | Qdrant (`qdrant`, 5 collections, 57,434 pts) | **No Qdrant container running.** Postgres + pgvector HNSW (~225K knowledge vectors per Beast health_check) |
| Last verified | 2026-05-06 by Devon-6164 | 2026-06-24 by Perplexity Computer (proxy) |

## Live-verified running spine (from docker_ps + list_dir)

- **Pipe (Python, on disk + running):** agent_home.py, brain_api.py, memory_store_writer.py, pre_ingestion_pipe.py, pre_ingestion_pipe_v3.py, pudding_extractor.py, pudding_pre_filter.py
- **Rust spine:** rust-agent (healthy), rust_home_runner.py, start_rust_home.sh, rust-agent-container/
- **Per-AI homes (all healthy):** perplexity-home, perplexity-computer-home, claude-home, grok-home, devin-home, codex-home, cursor-home, deepseek-home, kimi-home, stoa-home, northumbrian-home, comet-home, sweep-home
- **Pipe/ledger services (healthy):** vellum, vellum-mcp, perplexity-ingest, research-pipe, enforcer, brain-mcp-readonly, brain-mcp-writer, amplified-knowledge-mcp, beast-control-mcp
- **Data layer (running):** clickhouse, minio, redis, cove-postgres (timescaledb pg15)
- **AI layer (running):** litellm, ollama / ollama-2 / ollama-pudding, searxng
- **Workflow:** cove-temporal, docker-temporal-worker-1
- **Sovereign fleet (healthy):** entity_alpha, entity_charlie, entity_kimmy
- **App layer:** amplified-core (healthy), amplified-crm (healthy), amplified-marketing-engine, mission-control, traefik, watchtower

## Known stale "Known Issues" to re-verify (doc lists, may be resolved)
- AMP-140 Traefik :8080 dashboard
- AMP-136 Tailscale stuck Created (tailscale now shows Up 6 days — likely RESOLVED)
- AMP-142 LLM providers degraded
- amplified-crm-dev restart loop (now shows Up 6 days — likely RESOLVED)

## Job for the M5 watcher / pipe
1. Replace the Hardware + "What's Running" + "What's in the Databases" sections of `/opt/amplified/BEAST-STATE.md` with the live-verified figures above (run a fresh `docker ps` + Postgres/pgvector/AGE counts at commit time to get exact current numbers — do not trust this brief's counts as final; they are a 2026-06-24 snapshot).
2. Correct the DB section: Postgres + pgvector + Apache AGE. Remove FalkorDB/Qdrant unless those containers are actually reintroduced.
3. Re-verify the four "Known Issues" and close the resolved ones.
4. Commit through the pipe with Vellum attribution. Do NOT direct-write; this is a routed change.

## Constitution / grants compliance
- Drafted by AI as proxy, logged. Routed to inbox (Tier A drop), not written to Beast (Tier C, gated absolutely).
- Counts in this brief are a point-in-time snapshot (STRUCTURED); the watcher must re-measure at commit time before promoting any number.

[CLOSURE] branch=ACTION | proxy=1 logged (state-doc correction drafted as AI_PARTNER_PROXY) | gates=none | inbox=beast-state-correction-live-verified__2026-06-24T1135__perplexity.md | tier=STRUCTURED
