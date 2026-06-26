---
title: "Hooks and Harnesses as Doorways"
document_type: research_conclusion
artifact_id: research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor
date_utc: 2026-06-26
project: Amplified Partners
author: cursor
reader: ewan
epistemic_tier: STRUCTURED
tier_reason: "Composition of verified inbox docs, agent-claude harness proof, and clean-build catalogue reads. CLI-vs-MCP cost comparisons are INTUITED where noted."
ratifier: Ewan
---

# Hooks and Harnesses as Doorways

## 1. TL;DR

**STRUCTURED:** A *door* is a bounded permission surface — you open it only when that kind of work starts, do the job inside an isolated worktree, witness the open and close on Vellum, then tidy and share outward. Hooks are the automatic rails (token guard, session preamble, bash limits); harnesses are the executable contracts (worktree start, permissions classifier, sensor). **Push-door philosophy:** agents self-request access; hooks fail-open except for secrets; waste is nudged, curiosity is not blocked (`CURSOR-HARNESS-MANIFEST.md`, `worktree-door.mdc`).

**INTUITED:** Think of the fleet like a building where each system has its own locked door. You do not carry every key at once — you open ingestion when ingesting, research when researching, brain when writing knowledge. One hook/harness *set* serves a whole loop (e.g. ingest → research → brain), but each stage opens its door in sequence, closes with a witness, then the next opens.

Three names, one stack (ratified in `EWAN-DECISIONS-CONSOLIDATED__v01__2026-06-26.md` #17):
- **Classifier** — `amplified_permissions.py` / `amplified_harness.py` (what may I do?)
- **Runtime** — Baton + RodGuard + open-door lease (who may write now?)
- **Gate** — `epistemic_status.py` constitutional predicates (does this pass tier/rules?)

---

## 2. Door map

| System | Door name | Worktree path pattern | Hook set | Harness checklist | Predecessor door |
|---|---|---|---|---|---|
| **Beast (ops)** | `beast-ops` | N/A — read-only from Mac; deploy via PR worktree on M5/Beast | `beforeShellExecution` nudge on token bombs (Cursor) | SSH/beast MCP or CLI: `docker_ps`, verify container health; never docker socket from Mac | None — entry for infra checks |
| **Vellum (witness)** | `vellum-witness` | N/A — append-only ledger | `sessionStart` preamble + fleet sensor; `sessionEnd` witness | Post intent + completion; MCP `vellum_create_entry` or curl with queue fallback (`gk-worktree-start.sh`) | Session-start sensor (proceed/warn/halt) |
| **Brain (knowledge store)** | `brain-write` | `clean-build/02_build` branch worktree or Beast-side deploy | `@witness` decorator on write boundaries (v03 doctrine) | R1/R2 rubrics for production lane; porch/incoming release; no direct write from research_pipe | Ingest-inbox drainer verified (pipe-weld W2) |
| **Ingestion pipe** | `ingest-inbox` | `perplexity-inbox/` (shared SSOT) or Beast `perplexity-ingest` deploy worktree | Perplexity-ingest bearer auth + secrets regex (server-side) | `POST /drop` atomic write; Vellum event side-channel; session-start paths | Research staging emit (W1) or human drop |
| **Research pipe** | `research-run` | M5: `~/amp-worktrees/fleet-clean-build/<lane>/<ts>/<slug>` | Pre-bash guard, post-tool redact (Claude Code doors-phase0 — **STRUCTURED proof**) | Gate-0 verifier → staging_emitter → porch; needs Beast SearXNG | Intake validator + file-type router (partial — prose only today) |
| **CRM** | `crm-secrets` | TBD — Infisical migration worktree | None wired fleet-wide yet | Infisical as identity plane; JWT TTL 30d (ratified) | Phase 4 witness trial + Ewan baton: CRM vs Cove order |
| **Cove Temple (Temporal)** | `cove-temporal` | `clean-build/02_build/cove-orchestrator` worktree | `@witness` on workflow start/end (planned Phase 3) | `APDSIngestionWorkflow` — legacy live loop; gate behind research_pipe | Research pipe staging → porch release |
| **Containers (cell isolation)** | `container-cell` | Per-agent Apple Container or Beast tenant | Layer 2: ro mounts, SELECT-only DB, detached network (open-door spec v02) | One writable system at a time; opening a door closes the last | Baton lease on Vellum |

**Mac read-only rule (STRUCTURED):** Mac seats draft and witness; landing on Beast goes through Cascade-Mac / Devin PR (`AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`).

---

## 3. Loop patterns

### 3a. Ingest → research → brain (production loop)

**STRUCTURED** — two pipelines exist today (`CODE-CATALOGUE__ingestion-research-brain__2026-06-26.md`):
1. **Legacy:** Cove `APDSIngestionWorkflow` → brain (ungated; bloated 2.64M rows).
2. **Target:** `research_pipe` → staging → porch → ingest-inbox → brain drainer (gated; not fully welded).

Sequential witness per stage (master-plan Phases 1–3):

```
[door: research-run]  intake → search backends → methodology → sign → staging emit
        ↓ @witness
[door: ingest-inbox]  perplexity-ingest /drop OR porch → ingest-inbox
        ↓ @witness
[door: brain-write]   brain_curator R1 → (production: R2) → knowledge_vectors
        ↓ @witness + seat-pass
[door: vellum-witness] completion row + baton update
```

Each arrow = close previous door (commit, tidy, witness) before opening next.

### 3b. Agent seat loop (any IDE)

**STRUCTURED** (`AI-NATIVE-OPERATING-MODEL`, `WORKTREE_PLAN.md`):

```
session-start.sh → sensor verdict → Vellum intent
  → worktree door open (gk-worktree-start or manual)
  → waypoints (commits) inside worktree
  → share to company path (inbox / amplified-pipeline / PR)
  → Vellum completion + seat-pass
  → session-end witness
```

### 3c. Compound Engineering loop (effectiveness layer)

**STRUCTURED** (hooks plan v02): Plan → Work → Review → Compound — lives in repo files so every IDE opening the worktree inherits it. Token savings from Layer A (hooks) fund Layer B (planning/review).

---

## 4. Worktree protocol

**STRUCTURED** — synthesised from `WORKTREE_PLAN.md`, `worktree-door.mdc`, `gk-worktree-start.sh`, `HARNESS-CHECKLIST__doors-phase0__2026-06-26__cascade-mac.md`.

### Before open
- Check what else is active in that area (sensor, inbox status, active branches on bare clone).
- Match task to branch naming: `<agent_lane>/<YYYYMMDDHHMMSS>/<task-slug>`.
- Run session-start / sensor; post intent to Vellum.
- Open door via worktree script — records `door:open` event (curl or MCP; queues if Beast down).

### During
- One task → one worktree; never commit on `main` directly from Mac feature work.
- Waypoint commits: `wp(<task>): <what now works>` after each coherent unit.
- Watch context runway (~¾) — land plane: commit, update BATON, push (M5) or hand off (Mac).
- Drafts stay local until finished; hooks nudge waste, fail-open except P0 secrets.

### After close
- Tests/smoke where applicable (no-silent-failures gate: hook must run E2E + sensor or boundary proof).
- Promote artefact to **shared path** — not worktree-only (`inbox-finish-and-testing.mdc`).
- Vellum witness + seat-pass if handing off.
- Merge/absorb useful work before abandoning branch (`branch-absorb-before-abandon`).
- `door:close` witness (not yet standardised — **gap**; today only open is scripted).

---

## 5. CLI vs MCP — for fleet seats

| Dimension | CLI / shell scripts | MCP tools |
|---|---|---|
| **Token/cost** | **INTUITED:** Lower per call — no tool-schema bloat in model context; ideal for harness scripts agents run once per session | **INTUITED:** Higher standing cost (schemas loaded); cheaper per *complex* op when it replaces many round-trips |
| **Latency** | **STRUCTURED:** Local scripts (`session-start.sh`, `harness_selfcheck.py`) — instant | Network hop to Beast/Vellum; depends on tailnet |
| **Sovereignty** | **STRUCTURED:** Runs on your machine; stdout → witness log; queue file when offline (`~/.pending-vellum-queue`) | **STRUCTURED:** Server-mediated; good for attributed fleet bus; credential broker pattern (`codex-mcp`) |
| **Determinism** | **STRUCTURED:** Harness hooks must be deterministic — `amplified_harness.py` explicitly no LLM in decision path | Read/query tools fine; do not use MCP for permission *classification* |

### When each wins

| Job | Prefer | Why (tier) |
|---|---|---|
| Beast container health, file reads on Beast | **CLI** via SSH or Knowledge MCP `docker_ps` / `read_file` | **STRUCTURED:** Knowledge MCP is read-only Beast ops without stuffing compose files into chat |
| Vellum intent/completion at session start | **MCP** `vellum_create_entry` when live; **CLI** curl + queue when not | **STRUCTURED:** `gk-worktree-start.sh` proves curl fallback; MCP nicer for structured metadata |
| Brain semantic lookup | **MCP** `search_knowledge` | **INTUITED:** One call vs crafting SQL; worth the schema cost for research seats |
| Brain bulk SQL / graph | **CLI** or MCP `run_query` with fixed query | **STRUCTURED:** Repeatable scripts belong in repo, not re-generated each turn |
| Worktree open | **CLI** `gk-worktree-start.sh` | **STRUCTURED:** Single deterministic contract; already witnesses door open |
| Permission check (spend, push, external) | **CLI** `amplified_permissions.py` / harness classify | **STRUCTURED:** Codified rules JSON — never LLM |
| Bash guard / output redact | **Hooks** (not CLI nor MCP) | **STRUCTURED:** Phase 0 proof — 7/7 GREEN on Claude Code |

**Honest summary (INTUITED):** MCP wins for *read-and-witness* flows where structure beats prose (Vellum, brain search). CLI wins for *open-once, run-many* harness rituals and Beast ops. Hooks beat both for per-turn waste prevention — they cost almost no tokens because they run outside the model. Do not duplicate: witness via one channel per event (MCP **or** curl, not both unless failover).

---

## 6. Gap list (ordered)

1. **Open-door runtime unwired** — Baton + RodGuard + door-close schema designed, not one runnable thing (`open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md`). **STRUCTURED.**
2. **Pipe weld W1/W2/W3** — research-pipe never reaches brain without human seam cross (`pipe-weld-brief__v01__2026-06-25__perplexity.md`). **STRUCTURED.**
3. **Door-close witness** — open is scripted; close is manual seat-pass only. **INTUITED gap from read of gk-worktree-start.sh.**
4. **Cursor hook parity** — Claude Code Phase 0 GREEN; Cursor has manifest + rules but not full sensor parity (`HARNESS-CHECKLIST` vs `CURSOR-HARNESS-MANIFEST.md`). **STRUCTURED.**
5. **File-type router** — research_pipe loads `.md/.txt` only; json/db/audio deferred (`CODE-CATALOGUE`). **STRUCTURED.**
6. **Production rubric R2 / J1** — brain two-lane split not codified (`brain-ingestion__full-design-brief__v02`). **STRUCTURED.**
7. **CRM + Cove Infisical doors** — Phase 5 blocked on Phase 4 witness trial; Ewan baton on migration order still open in docs (`master-plan` Phase 0). **STRUCTURED.**
8. **Vellum Merkle checkpoint** — flat hash chain only; witness elevation thin spot. **STRUCTURED** (brain brief open Q1).

---

## 7. Three build jobs

Smallest next steps — same shape as brain brief J1/J2/J3.

### H1 — Standardise door open/close on Vellum
**Owner:** Cascade-Mac (script) + Cursor (Mac witness). **Time:** ~half day. **Tier-C gates:** none.

- Extend `gk-worktree-start.sh` with paired `gk-worktree-close.sh`: commit check, shared-path check, `door:close` payload.
- Publish door event schema (`worktree_opened` / `worktree_closed`) for Vellum index.
- Mirror curl + queue fallback for both events.

**Done when:** open + close events appear in Vellum (or queue file) with same branch/worktree metadata; sensor asserts both scripts exit 0.

### H2 — Cursor session harness parity (Phase 0.5)
**Owner:** Cursor seat on Mac mini. **Time:** ~half day. **Tier-C gates:** none.

- Align `~/.cursor/hooks.json` with proven Claude hooks: bash guard, post-tool redact, session-end witness line to `~/.amplified/logs/harness-hooks.jsonl`.
- Add inbox project hooks per `token-efficiency-inbox.mdc`.
- Run equivalent of `harness_selfcheck.py` — GREEN or RED, never silent.

**Done when:** sensor GREEN; one denied `find . -type f` and one witness line in log (matches Phase 0 proof bar).

### H3 — Pipe weld W1 with per-stage witness
**Owner:** Claude Code → Beast. **Time:** ~half day. **Tier-C gates:** none (parallel with H1/H2).

- Wire `staging_emitter.py` second emit: markdown + `POST perplexity-ingest:8000/drop` after Gate-0 pass (`pipe-weld-brief` W1).
- Add `@witness(boundary="research_pipe.staging_emit")` per v03 doctrine (depends Phase 1 decorator — can stub log line first).

**Done when:** one research run produces a file in ingest-inbox without human hand-move; Vellum row references run_id + packet hash.

---

## Source refs

- `perplexity-inbox/HARNESS-CHECKLIST__doors-phase0__2026-06-26__cascade-mac.md`
- `perplexity-inbox/claude-code-max__token-optimisation__hooks-and-harness-plan__v02__2026-06-24__perplexity.md`
- `perplexity-inbox/AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`
- `perplexity-inbox/CODE-CATALOGUE__ingestion-research-brain__2026-06-26.md`
- `perplexity-inbox/pipe-weld-brief__v01__2026-06-25__perplexity.md`
- `perplexity-inbox/brain-ingestion__production-substrate__full-design-brief__v02__2026-06-26__perplexity.md`
- `perplexity-inbox/master-plan__v01__2026-06-25__perplexity.md`
- `perplexity-inbox/open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md`
- `agent-claude/WORKTREE_PLAN.md`, `agent-claude/scripts/gk-worktree-start.sh`
- `~/.cursor/CURSOR-HARNESS-MANIFEST.md`, `~/.cursor/rules/worktree-door.mdc`

**Not loaded:** `~/Code/FACILITATOR-COCKPIT.md` (path missing on this Mac). Knowledge MCP entity search skipped (optional; primary docs sufficient).

---

[CLOSURE] branch=PLAN | proxy=none | gates=Ewan reads door map + H1/H2/H3 priority | inbox=research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md | tier=STRUCTURED
