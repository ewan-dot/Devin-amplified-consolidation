---
title: Amplified Partners Control Centre prior art synthesis
date: 2026-06-25
artifact: control-centre-prior-art-synthesis
source_provenance:
  sessions:
    - 4a26d8c1
    - 94681082
    - a4942258
    - a3d93899
    - 244626bd
    - 602ca20c
    - dcab1284
    - 443de0db
    - f739134b
    - edc6e306
    - 38331437
    - f6aa9edf
    - a7e4db1f
  wiki_paths:
    - memory/knowledge/index.md
    - memory/knowledge/entities/amplified-partners.md
    - memory/knowledge/projects/relay-vellum.md
    - memory/knowledge/concepts/ai-management-ui.md
    - memory/knowledge/concepts/agent-worktree-contract.md
    - memory/knowledge/concepts/deterministic-ai-feed.md
    - memory/knowledge/projects/intent-interface.md
    - memory/knowledge/projects/corpus-reconnaissance-pipeline.md
    - memory/knowledge/learnings/2026-06-22.md
tier: STRUCTURED
iso_8601: 2026-06-25T08:37:00+01:00
---

The Control Centre is the mission-control surface for Amplified Partners’ AI work: a single pane over Vellum/Relay that turns chatty, dispersed work into routed artifacts, evidence, telemetry, decisions, and handoffs, with Vellum as the canonical witness layer and Postgres-backed ledger beneath it [STRUCTURED].

## Purpose & framing

- The core problem is work fragmentation: outputs vanish into chats, summaries, and disconnected tools unless they are forced through the ledger. Vellum is framed as the substrate that records what agents and humans say and do, so the system stays auditable and recoverable [STRUCTURED].
- The Control Centre is not a generic dashboard; it is a work surface that makes the operating system visible and routes outputs to the right sink: Beast/Brain, Vellum, Drive, GitHub, Slack, or a content queue [STRUCTURED].
- Vellum is repeatedly described as the “mycelial network” / “audit substrate” and a “distributed weak-signal early-warning system” that sees semantic and operational signals before they become financially visible [PROVEN].
- The architecture is intentionally control-plane first: the user wants Vellum to be the anchor, with deterministic workers handling execution and human/agent judgment reserved for exceptions, design, and kaizen [STRUCTURED].

## Architecture

- The preferred flow is Pipe → Vellum (Postgres) → surface layer. Vellum is its own PostgreSQL database named `vellum` on the same Postgres 15 instance as the brain; drafts only become real when written through the pipe to Vellum [PROVEN].
- The control plane uses a split stack: Python infrastructure plus Rust memory containers / execution components, with Brain/Beast orchestrating shared retrieval and private continuity [STRUCTURED].
- Deterministic code is responsible for the feed, schema, routing, tolerance checks, retries, and measurable boundaries; AI sits where interpretation and outlier handling are needed [STRUCTURED].
- The near-term rollout preference is lightweight and staged: propagate deterministic `INDEX.md`, `AGENTS.md`, and `pre_build_check.py` patterns per repo first, then centralise the fuller `artifact_type/state_machine/proforma_set/evidence_pack/VCK` control plane later [STRUCTURED].
- The execution stack preference includes Rust-based containers; the user also explicitly said Vellum is not a SaaS [PROVEN].

## Telemetry sources

- Vellum should observe, rather than rely on manual narration: touched files, changes, retries, escalations, routes, accept/reject outcomes, and transition notes [STRUCTURED].
- The sensor catalogue already includes validation failures, threshold crossings, API/schema failures, stalled Cove tasks, agent-loop excess, context-threshold reached, anonymisation failure, tier demotion, contradiction detection, telemetry gaps, and handoff lifecycle events [STRUCTURED].
- Vellum is also the canonical monitoring and witness layer for brain intake and related operational signals; every packet going into the brain has an immutable Vellum sensor attached [PROVEN].
- Evidence can originate from agents, workers, and humans; the broader operating model treats Vellum as a paper trail across the estate rather than a diary [STRUCTURED].
- External intake is part of the design: SearXNG was registered as a VellumPacket upstream source in the relay-vellum line, linking live research intake into the ledger [STRUCTURED].

## Surfaces & views

- The UI should show routed work, telemetry, memory, model routing, content creation, scouting, and output routing in one place [STRUCTURED].
- The live surface is described as a mission-control workbench / live lens rather than a passive archive [STRUCTURED].
- The Surface needs to expose status and drift, not just finished items: it should convert exploratory work into routed artifacts, decisions, Vellum events, GitHub issues, content drafts, and evidence trails [STRUCTURED].
- It should surface model disagreements and weak signals indirectly through telemetry, contradiction detection, and the witness layer, but no single canonical “model disagreement” schema was found in the provided material [INTUITED].
- It should preserve “semantic before financial visibility”: the ledger is meant to see meaningful operational and conversational signals before they show up as financial consequences [PROVEN].
- The current implementation path for the live lens is Intent Interface: Electron/React tray app, Monologue capture, Vellum append, Brain query, interrupts, Second Head, local todo, research engines, and chief-of-staff routing [STRUCTURED].

## Governance bindings

- There is a strict separation between the Truth Team and the Production Team: Truth monitors systems and interprets incongruence; Production implements and publishes [PROVEN].
- This separation is meant to stop truth detection and production authority collapsing into one role [PROVEN].
- Control-centre outputs should carry provenance-preserving evidence rather than lossy summaries; the audit log is an append-only ledger for important actions and mistakes [STRUCTURED].
- Min-rule tagging appears in the live UI path: certainty marks exist, but marks never add epistemic authority before appending verbatim and reformatted text to Vellum [STRUCTURED].
- The control surface should maintain attribution chains and source traceability; claim traceability back to source versions is part of the corpus pipeline and should be preserved in the Control Centre as well [STRUCTURED].

## Doctrines & invariants

- “Vellum is not an after-work archive; it is where work happens.” [PROVEN]
- “Nothing enters the Beast except through the pipe.” [INTUITED] This exact wording was not found in the pulled pages, but the same doctrine is strongly implied by the pipe-first ingestion and pre-Beast feed framing [STRUCTURED].
- Vellum is an integrity witness: it is the canonical record, the monitoring layer, and the provenance ledger for brain intake [PROVEN].
- Vellum is also a task primitive, not a generic todo list: task inbox, simple statuses, Today view, parity between human and agent tasks, evidence on every task, and approve/reject gates are part of the design [PROVEN].
- Workspace hygiene should be rooted through Vellum rather than governed by agents, with humans/agents handling judgment while deterministic workers do filing, validation, and path execution [STRUCTURED].
- The deterministic AI feed doctrine says input control, schema control, routing control, and radius checks are more important than trying to make the model itself deterministic [STRUCTURED].

## Open questions / unresolved decisions

- Whether Intent Interface, Relay UI, Relay Lens, Knock Live Lens, and Amplified Cockpit are one lineage or several remains unresolved [STRUCTURED].
- The exact location of the de-bias / model-agnostic normaliser remains unclear [STRUCTURED].
- Whether Vellum Baton is global or scopeable by system/agent, and whether Postgres is the final live backend, was explicitly left open in the learnings log [STRUCTURED].
- The Control Centre’s final canonical event schema is not yet nailed down in the provided material; only partial schema language was found (`artifact_type/state_machine/proforma_set/evidence_pack/VCK`, `VellumPacket`, `vellum-events_*.jsonl`) [STRUCTURED].
- The intended relationship between Control Centre, Intent Interface, and Relay/Vellum is conceptually clear but still product-line ambiguous [INTUITED].
- The source set does not settle which views are required for “model disagreement surfacing” beyond contradiction detection and telemetry gaps [INTUITED].

## Specific reusable artifacts

- Frontmatter / seat discipline from the deterministic AI feed: a clean input envelope with schema, routing, and context headroom [STRUCTURED].
- `vellum-events_*.jsonl` as the sandbox draft naming convention for Vellum event packets [PROVEN].
- `INDEX.md`, `AGENTS.md`, and `pre_build_check.py` as the lightweight repo rollout pattern for control-plane hygiene [PROVEN].
- `artifact_type`, `state_machine`, `proforma_set`, `evidence_pack`, and `VCK` as the names of the fuller future control-plane contract [STRUCTURED].
- The live UI’s certainty-marking scheme: per-word certainty 1–9, ambiguity/metaphor marked with ▲, and min-rule compliance before append [STRUCTURED].
- `VellumPacket` as the upstream source contract name for research intake [STRUCTURED].
- The “Task Inbox”, “Today view”, and “ExecutionMode” vocabulary for task management [PROVEN].

## Source map

- Vellum as Postgres database, canonical target, immutable sensor attachment: [wiki: memory/notes/work/Amplified/doctrines/vellum_integrity_witness.md]
- Task primitive / inbox / approve-reject / YOLO ExecutionMode: [wiki: memory/notes/work/doctrines/vellum_task_primitive.md]
- Workspace hygiene, deterministic workers, staged rollout, Rust containers: [wiki: memory/notes/work/doctrines/workspace_hygiene_vellum_control_plane.md]
- Vellum as mycelial network / weak-signal early-warning system: [wiki: memory/notes/work/projects/vellum.md]
- Append-only ledger / diary-like work trail: [wiki: memory/notes/preferences/workflows/audit_logging.md]
- Cove as production, Perplexity as research pipe, Vellum as UI layer: [wiki: memory/notes/projects/Amplified/delivery_flow.md]
- Truth Team vs Production Team separation: [wiki: memory/notes/work/Amplified/governance/teams.md]
- Relay/Vellum overview, telemetry spine, sensor catalogue, Rust memory containers, SearXNG upstream source: [wiki: memory/knowledge/projects/relay-vellum.md]
- AI Management UI mission-control framing and route-first interface: [wiki: memory/knowledge/concepts/ai-management-ui.md]
- Agent worktree contract, isolated worktrees, reviewed PR gate, no self-approval: [wiki: memory/knowledge/concepts/agent-worktree-contract.md]
- Deterministic AI feed, Python/Rust feed control, radius checks, supervisor surface: [wiki: memory/knowledge/concepts/deterministic-ai-feed.md]
- Intent Interface live lens, Monologue→Vellum, route policy, certainty marking, Electron locked: [wiki: memory/knowledge/projects/intent-interface.md]
- Corpus Reconnaissance Pipeline, spike/synthesis split, GO/STOP outcome: [wiki: memory/knowledge/projects/corpus-reconnaissance-pipeline.md]
- Open questions from 2026-06-22 learnings log: [wiki: memory/knowledge/learnings/2026-06-22.md]
- Session 4a26d8c1 on token optimisation / production law / Vellum control surface: [session 4a26d8c1]
- Session 94681082 on Vellum doorkeeper collapse / container isolation / seven-month attribution correction: [session 94681082]
- Session a4942258 on deterministic-vs-AI partition theory: [session a4942258]
- Session a3d93899 on engine selector and build-order slices: [session a3d93899]
- Session 244626bd on Hazel consolidation and clean-build canonicality: [session 244626bd]
- Session 602ca20c on Drive/local estate split and no-remote risk: [session 602ca20c]
- Session dcab1284 on privacy/security/sovereignty folders and plaintext secret risk: [session dcab1284]
- Session 443de0db on Vellum buffering, Langfuse gap, container-runtime gap: [session 443de0db]
- Session f739134b on STOP UI live check and WanMin/M5 distinction: [session f739134b]
- Session edc6e306 on corpus reconnaissance pipeline and STOP outcome: [session edc6e306]
- Session 38331437 on zsh setup and credential open items: [session 38331437]
- Session f6aa9edf on Factory.ai assessment and architecture patterns: [session f6aa9edf]
- Session a7e4db1f on Amplified Cockpit and Computer-as-remote-engine wiring: [session a7e4db1f]
