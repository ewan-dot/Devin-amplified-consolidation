---
type: RESEARCH
title: Open-Door Harness — Prior-Art INDEX of Ewan's OWN Corpus
slug: open-door-harness-prior-art
version: v01
date: 2026-07-03
author: cursor
epistemic_tier: INTUITED
tier_reason: "Index + synthesis of already-authored/already-paid-for artifacts found on this Mac. No new external research bought."
mode: SOURCE-FIRST (harvest existing before buying external)
purpose: "Stop re-inventing / re-buying the open-door harness. Surface Ewan's OWN prior designs so the build stands on them."
scope: "Read-only harvest of ingestion-to-research-pipe/, Ai-Privacy-Sovereignty-Security/, Downloads/, ~/.cursor/rules/. amplified-knowledge MCP unreachable (see Gaps)."
---

# Open-Door Harness — Prior-Art INDEX of His Own Work

**Bottom line up front:** the open-door harness is **not** an unresearched idea. It is one of the most-documented concepts in the estate, designed at least **four separate times** across 2026-06-18 → 2026-07-03, with a canonical architecture spec, an installed hook/rule stack, a runtime primitive mapping onto Vellum, a completion-telemetry model, and even shippable multi-IDE hook code. External security prior art (NIST, SPIFFE, DeerFlow, Falco, capability/least-privilege) was **also already bought** in his 2026-06-25 syntheses. Almost nothing here needs re-researching — it needs **consolidating and wiring**.

Method note (per architect correction): SOURCE-FIRST. This is an index of HIS material. External web patterns are deliberately minimal — only flagged where his corpus has a genuine hole.

---

## 1. INDEX — his own prior artifacts (path · what it covers · currency)

### Tier 1 — canonical / most complete (build on these first)

| # | Path | What it covers | Currency |
|---|---|---|---|
| A1 | `~/Ai-Privacy-Sovereignty-Security/github-with-hooks-harnesses/open-door-harness__architecture-spec__agent-doc__v02__2026-06-22__perplexity.md` | **THE canonical spec.** "Blinkers without ceilings; one writable door at a time, enforced by a doorkeeper." Origin/allegory in Ewan's voice; the **doorkeeper** (single write-lease, opening B closes A, zero standing write, never the docker socket); **3 enforcement layers** (L2 container boundary = the wall, L1 in-process guardrail, L0 per-worktree hook binding); a **door map** grounded in live Beast state (Brain, Research pipe, CRM, Cove, Telemetry, Marketing, Vellum, Secrets=NO DOOR); enforcement legs honestly tiered (FS/DB=STRUCTURED, network=INTUITED gap); mapping of harness concerns onto **Vellum primitives** (Baton, RodGuard, sensors, tasks). | v02, 2026-06-22. Most complete. Superset of the newer inbox DESIGN. |
| A2 | `perplexity-inbox/DESIGN__open-door-harness__v01__2026-07-03__cursor.md` | **Today's design.** Three primitives (Door / Active-door marker / Harness); **door taxonomy** with access dimensions (FS-read/write globs, Net/Mesh, MCP allow-list, git-write, spend tier); 7 named seed/proposed doors (`research_read` default, `agentsmini_build`, `central_handoff`, `worktree_feature`, `pipe_run`, `config_harness`, `vellum_witness`); concrete **hook-point mapping** to existing scripts; **4-phase install-safe rollout** (SSOT → present → soft-wall → hard-deny); reconciliation table vs every existing rule. | v01, **today**. Current. The Cursor-seat framing of A1. |
| A3 | `perplexity-inbox/DRAFT-RULE__open-door-harness__v01.mdc` | Draft **alwaysApply rule** (the one-page operator contract): choose door → get exactly that access → cannot wander → freedom is choice of door; enter/inside/switch/exit; door-independent Red core + constitution + finish-waypoint. Not installed (awaiting bless). | v01, today. Ready to install. |

### Tier 2 — door doctrine, runtime, telemetry, installed stack

| # | Path | What it covers | Currency |
|---|---|---|---|
| B1 | `perplexity-inbox/archive/research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md` (dup: `.worktrees/antigravity-brain-wipe/…`, `chunks/…_chunk_01.txt`) | Door = bounded permission surface; **door map by system** with worktree paths + hook sets; three-name stack (**Classifier** `amplified_permissions.py` / **Runtime** Baton+RodGuard+lease / **Gate** `epistemic_status.py`); loop patterns; **CLI-vs-MCP** cost table for seats; ordered **gap list**; three ~half-day build jobs (H1 door open/close on Vellum, H2 Cursor hook parity, H3 pipe weld). | v01, 2026-06-26. Current doctrine. |
| B2 | `.worktrees/antigravity-brain-wipe/perplexity-inbox/research-conclusion__doors-telemetry-completion__v01__2026-06-26__cursor.md` | Addendum: doors as the **measurement layer**. door-open → hook → Vellum row → metric; **completion% = jobs(all F1..F8 PASS)/jobs(F1 PASS)**; the 8 finish waypoints (F7 door-close = known gap); deterministic-core-not-LLM; compound signal telemetry (referenced by `self-compound.mdc` §7). | v01, 2026-06-26. Current. |
| B3 | `perplexity-inbox/missing-thread-briefs__2026-06-24/open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md` (dup in archive/ + .worktrees/) | Runtime brief: **Baton** (single estate write-lease), **RodGuard** (rod-violation circuit-breaker kill-switch), Claude-Code-as-keyholder, separate telemetry planes (Langfuse ≠ Vellum), constitutional gate `epistemic_status*.py`. Flags the **name collision**: inbox `amplified_harness.py` (permission classifier) ≠ this Baton+RodGuard runtime → rename to disambiguate. | v01, 2026-06-24. Runtime spine. |
| B4 | `perplexity-inbox/manifest/CURSOR-HARNESS-MANIFEST.md` (dup in .worktrees/) | **What is actually installed** at `~/.cursor/`: alwaysApply rules list; the 9 wired hooks (sessionStart, beforeSubmitPrompt, beforeShellExecution, beforeReadFile, postToolUse, stop, preCompact, subagentStop, sessionEnd); **push-door philosophy** (self-request = granted; hooks fail-open except P0 secrets; nudge-before-deny). | Live SSOT for Cursor seat. |
| B5 | `~/Downloads/amplified-hooks-harness-deploy-kit__code__v01__2026-06-18__perplexity/` | **Shippable multi-IDE hook CODE.** Contains `.cursor/hooks`, `.claude/hooks`, `.codex/hooks`, and `.agent-harness/{schemas,telemetry}`. Concrete deploy kit, not just prose. | v01, 2026-06-18. Verify against current hooks before reuse. |

### Tier 3 — supporting / earlier / duplicated versions

| # | Path | What it covers | Currency |
|---|---|---|---|
| C1 | `perplexity-inbox/prior-art-syntheses-bundle/estate-security-and-sensors-prior-art-synthesis__{agent,human}__v01__2026-06-25.md` | **External security prior art ALREADY BOUGHT.** NIST SP 800-207/207A (zero-trust), 800-57 (key rotation), 800-61r3 (breach); SPIFFE/SPIRE; HashiCorp Vault dynamic creds; Sigstore/Rekor + immudb (append-only ledger = Vellum); Falco/Tetragon eBPF; osquery/Santa; Gitleaks/TruffleHog; Infisical adoption order. Directly feeds the doorkeeper's DB-role / network / audit legs. | v01, 2026-06-25. **Do not re-buy.** |
| C2 | `~/Ai-Privacy-Sovereignty-Security/synthesis/Sovereign_AI_Environment_Full_Synthesis.md` | Sovereign multi-AI environment: deterministic Python+Rust governance (not LLM), human kill-switch/final ratification, append-only V3/V2 vault, "containers are not a sovereign boundary → microVM (Firecracker / Apple Virtualization)". The isolation-philosophy parent of the doorkeeper. | 2026-06-20. Philosophy layer. |
| C3 | `perplexity-inbox/archive/vscodium-build-and-open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md` (+ chunks/, .worktrees/) | Open-door harness in the context of a sovereign VSCodium build. | 2026-06-24. |
| C4 | `perplexity-inbox/archive/HARNESS-CHECKLIST__doors-phase0__2026-06-26__cascade-mac.md` (+ chunks/) | Phase-0 doors checklist; the Claude-Code "7/7 GREEN" harness proof referenced elsewhere. | 2026-06-26. |
| C5 | `perplexity-inbox/archive/claude-code-max__token-optimisation__hooks-and-harness-plan__v0{1,2}__2026-06-24__perplexity.md` (+ chunks/, .worktrees/) | Hooks + harness plan under the token-optimisation lens (Layer-A hooks fund Layer-B planning/review). | 2026-06-24. |
| C6 | `perplexity-inbox/archive/OPERATING-RULE__constitutional-harness__v01__2026-06-26__cursor.md` (+ chunks/, .worktrees/) | Constitutional-harness operating rule (the staged pre_client/client_live gate that layers under every door). | 2026-06-26. |
| C7 | `perplexity-inbox/CONCLUSIONS__ai-native-harness-thread__2026-06-26/…cascade-mac.md` + `archive/BATON-PASS__ai-native-harness-thread__v01__2026-06-26__cascade-mac.md` | Thread conclusions + baton for the ai-native harness thread (cross-seat handoff record). | 2026-06-26. |
| C8 | `perplexity-inbox/archive/RESEARCH-PIPE-RUN__hooks-harness-doorways__v01__2026-06-26__cursor.md` (+ chunks/, .worktrees/) | The research-pipe run that produced the doorways conclusion (survivor-source trail). | 2026-06-26. |

### Tier 4 — installed rules that ARE the door primitives (read-only, `~/.cursor/rules/`)

`worktree-door.mdc` (the first concrete door: enter/inside/exit) · `yolo-ceilings.mdc` (green-zone autonomy + universal Red core = door-independent hard stops) · `constitutional-gate.mdc` (7 rods, staged pre_client/client_live) · `finish-waypoint.mdc` (the "exit door out" F1–F8 closure) · `self-compound.mdc` (new doors/scope fixes are capital, encode same session) · `session-discipline.mdc` (sessionStart chain where doors are presented) · `right-model-routing.mdc` (spend-tier = per-door routing ceiling). These are already live and are exactly the layers A2 §5 reconciles.

---

## 2. SYNTHESIS — strongest ideas drawn from HIS OWN material

Everything below is already his; the job is to unify and wire, not invent.

1. **Doorkeeper as the single key (A1).** Zero standing write; the agent can only *request* a door; a dumb trusted component holds the one lease; opening B closes A; **never the docker socket**. This is the mechanism that makes "one door at a time" a *wall*, not a promise. Strongest single primitive in the corpus.

2. **Three enforcement layers, honestly tiered (A1).** L2 container/kernel boundary = the universal wall (`:ro` mount, SELECT-only DB role, detached net) → STRUCTURED. L1 in-process guardrail (pre-tool hook / DeerFlow-style `GuardrailProvider`, `fail_closed`) = inner blinker. L0 per-worktree hook binding = unit of work. Defence in depth; never depend on L1 alone.

3. **Door = access profile, freedom = choice of door (A2).** Each door fixes FS-read/write globs, Net/Mesh, MCP allow-list, git-write level, spend tier. Escalation is by **exit + re-enter another door**, never widening mid-work. `research_read` is the never-stuck read-only default. This is the deny-by-default / least-privilege pattern expressed in Ewan's language.

4. **Runtime already maps onto Vellum primitives (A1 + B3).** Doorkeeper = **Baton** mutex + **RodGuard** circuit-breaker; hooks = witness sensors; door-open/close = ledger rows; tasks carry ExecutionMode (YOLO vs HITL) by door risk class. No new datastore needed — wire onto Vellum v0.2.0.

5. **Doors are the measurement layer (B2).** Every door-open → hook → Vellum row → **completion% (F1–F8 booleans, not agent prose)**. This turns the harness into telemetry for "did the job actually finish," and it's the same core `self-compound.mdc` already references.

6. **Install-safe phased rollout exists (A2 §6).** SSOT-only → presentation-only (advisory door menu + `door` CLI) → soft-wall (nudge + collect `harness-hooks.jsonl`) → hard-deny for the cheap-to-verify doors first. De-risks turning on the wall.

7. **Naming must be disambiguated before building (B3).** `amplified_harness.py` (permission *classifier*) ≠ open-door *runtime* (Baton+RodGuard). Rename one (e.g. `amplified_permissions.py` vs `open_door_runtime/`) or the M5 watcher builds a phantom layer. Cheapest highest-value fix.

**Recommended base for the build (top 3–5):** start from **A1** (canonical mechanism) as the spec, adopt **A2's door taxonomy + 4-phase rollout** as the Cursor-seat plan, wire the runtime onto **Vellum Baton/RodGuard (B3/A1)**, instrument with **completion% (B2)**, and do the **name disambiguation (B3)** first. Reuse **B5** (deploy-kit code) and **C1** (already-bought security prior art) instead of rebuilding either.

---

## 3. GENUINE GAPS (candidates for later research — most are WIRING, not research)

Ordered; only #4 is arguably a real external-research need.

1. **Consolidation gap (not research).** Four overlapping designs (A1/A2/A3/B1/B3) — no single ratified SSOT. Action: pick A1 as parent, fold A2 into it, bless A3. Zero new research.
2. **Network leg is the one weak enforcement leg (A1, own admission).** Beast `amplified-net` is flat → the "one door" network boundary is policy, not wall, until per-system nets / host firewall exist. Owner Devin; engineering, not research.
3. **Per-DB `*_ro`/`*_rw` Postgres roles not created (A1, C1).** DB door is policy until roles exist. Engineering.
4. **F7 door-close witness unbuilt (B1 H1, B2).** Open is scripted; close is manual. Build `gk-worktree-close.sh` + close event schema. Engineering.
5. **Cursor-specific hard-deny hook wiring (A2 Phase 3).** The macOS/Cursor path to a real `permission:deny` at `beforeShellExecution`/`beforeReadFile` against the active-door manifest is designed but not implemented/tested. Small verification, not research.
6. **(Only possible true external gap)** macOS process-level sandbox enforcement for the doorkeeper on Mac (Seatbelt/`sandbox-exec` is deprecated; Apple `container`/microVM is the C2 direction). If a *kernel-enforced* Mac wall is wanted beyond the container boundary, that specific macOS-2026 mechanism is the one thing thinly covered in his corpus — but note C1 + C2 already point at microVM isolation, so even this is mostly decided.

Everything else the architect listed in the original brief (capability tokens, deny-by-default allowlists, OPA/Cedar policy-as-code, HITL step-up gates, FSM-constrained execution, blast-radius containment) is **already represented** in his own material — as the doorkeeper's allow/deny contract (A1), the constitutional gate (C6), completion-state machine (B2), and the bought security synthesis (C1). **Do not re-buy these.**

---

## 4. Tool gap (transparency)

The `amplified-knowledge` MCP (`user-amplified-knowledge-mcp`) was **unreachable** this session: `search_knowledge` returned `-32602 Invalid request parameters` on every parameter shape, and `health_check` failed identically — i.e. the server/Beast surface is down or misconfigured, not an auth problem. **Brain vector hits were therefore NOT harvested.** Re-run the eight targeted `search_knowledge` queries (`agent harness design`, `open door blast radius`, `hooks harness waypoints`, `capability scoping least privilege agent`, `sandbox permissions agent`, `guardrails deny by default`, `worktree door`, `sovereign vellum harness`) when the Beast MCP is live, to confirm nothing in the 225K-vector store adds beyond the filesystem artifacts above.

---

## 5. Source refs (his own corpus)

- `~/Ai-Privacy-Sovereignty-Security/github-with-hooks-harnesses/open-door-harness__architecture-spec__agent-doc__v02__2026-06-22__perplexity.md`
- `~/Ai-Privacy-Sovereignty-Security/synthesis/Sovereign_AI_Environment_Full_Synthesis.md`
- `perplexity-inbox/DESIGN__open-door-harness__v01__2026-07-03__cursor.md`, `DRAFT-RULE__open-door-harness__v01.mdc`
- `perplexity-inbox/archive/research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md` (+ `.worktrees/…doors-telemetry-completion…`)
- `perplexity-inbox/missing-thread-briefs__2026-06-24/open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md`
- `perplexity-inbox/manifest/CURSOR-HARNESS-MANIFEST.md`
- `perplexity-inbox/prior-art-syntheses-bundle/estate-security-and-sensors-prior-art-synthesis__{agent,human}__v01__2026-06-25.md`
- `~/Downloads/amplified-hooks-harness-deploy-kit__code__v01__2026-06-18__perplexity/`
- `~/.cursor/rules/{worktree-door,yolo-ceilings,constitutional-gate,finish-waypoint,self-compound,session-discipline,right-model-routing}.mdc`
- Supporting: `archive/{HARNESS-CHECKLIST__doors-phase0…, claude-code-max…hooks-and-harness-plan v01/v02, OPERATING-RULE__constitutional-harness…, RESEARCH-PIPE-RUN__hooks-harness-doorways…, vscodium-build-and-open-door-harness…}`, `CONCLUSIONS__ai-native-harness-thread__2026-06-26/`

[CLOSURE] branch=PLAN | proxy=none | mode=source-first (≈zero external bought) | gaps=consolidate + wire (research only for macOS-native sandbox if kernel-enforced Mac wall wanted) | tool-gap=amplified-knowledge MCP down | tier=INTUITED
