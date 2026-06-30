---
title: "Chunk 01a2ab34-1 — Fleet routing & shared config-as-database"
document_type: research_chunk
chunk_id: "01a2ab34-1"
source_thread: 01a2ab34-234c-46c7-ae1e-8adc60e3e9f9
partner: partner-01a2ab34-1__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk 01a2ab34-1 — Fleet routing & shared config-as-database

**Source:** Thread `01a2ab34` lines 1–45 · seat **cursor** · 2026-06-30

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architect intent** | Multi-agent model routing must be **Amplified Partners config**, not ad-hoc Cursor defaults | encoded (`fleet-routing-v1.json`, `right-model-routing.mdc`) |
| **Architect intent** | Principles stored in **mutually shared hook+harness "how we do things database"** — bidirectional sync | partially encoded (repo ↔ `~/.cursor` sync; no single DB table yet) |
| **Conclusion** | Cursor has no native "Opus plans, Composer executes" panel — fleet must enforce via rules + manifest + Vellum sidecar | encoded |
| **Conclusion** | Self-compound same-session: rules/hooks changes must land in repo SSOT + Vellum delta | encoded |
| **Gap** | "How we do things database" is half-designed — needs canonical store beyond scattered JSON/MD | open |
| **Internal artefact** | `OPERATING-RULE__right-model-routing__v01__2026-06-30__cursor.md`, `config/fleet-routing-v1.json` | encoded |

## Key facts

1. Opening ask: define multi-agent search model selection (planning vs execution subagents).
2. Architect correction: config must live in **shared fleet harness**, bi-directionally updated so all seats sing from same hymn sheet.
3. Compound-engineering prior art run informed child-agent persona patterns before encoding routing rule.
4. WHO ≠ WHAT (light v1): routing sidecar witnesses seat choice; task body holds WHAT.

## Architect quotes (verbatim)

> "The config, the principles are stored in a mutually shared config hook and harness… updated in a bi-directional way so that everybody's singing from the same hymn page."

## Open gaps

- Unified "how we do things" config store (Postgres? JSON manifest? Vellum sheet?) — architect said half-designed
- Automated block on subagent spawn without Vellum routing sidecar — nudge only until `client_live`

---
*Author: cursor · epistemic_tier: INTUITED*
