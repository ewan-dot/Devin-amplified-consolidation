---
description: 
alwaysApply: false
---

---
description: 
alwaysApply: true
---

---
description: "Amplified Partners agent context — load on demand. Overflow → ESTATE-NOTES.md"
alwaysApply: false
---

## What this is
Amplified Partners fleet. AI-native company. Beast (Hetzner EPYC) + Mac (architect input only).
Mac is read-only from 2026-06-17 — no git push from Mac. All pushes via Devin or Beast.

## Rules
Ewan's 11 rules: ~/.cursor/rules/ewan-core-rules.mdc
7 operational rules: ~/clean-build/docs/amplified-agent-operational-rules.md
Spine Size Law: `AGENTS.md` must be kept at a perfect, readable size and MUST never exceed 500 lines. If the file approaches 500 lines, migrate verbose details, environment context, and logs to `ESTATE-NOTES.md` (or portable spine reference directories) to compress the file.

## Key locations
- Codebase SSOT: ~/clean-build/ (GitHub: Amplified-Partners/fleet-clean-build)
- Agent workspace: ~/Code/
- Vellum ledger: https://vellum.beast.amplifiedpartners.ai (post before/after every seat)
- Beast: ssh beast (135.181.161.131, Hetzner EPYC 48c, 251GB RAM)
- Estate notes: ~/ESTATE-NOTES.md (detailed facts — load on demand)
- Credential catalog: ~/clean-build/docs/credential-catalog.yaml
- Fleet roster: ~/Code/FLEET-ROSTER.md
- Facilitator cockpit: ~/Code/FACILITATOR-COCKPIT.md

## Before starting any job
1. Read ~/Code/FACILITATOR-COCKPIT.md (current state of play)
2. Post intent to Vellum task queue (/api/v1/tasks/)
3. On finish: fill seat-pass, post to Vellum, update baton, and run reference hook.

## Continual-learning hook
New durable facts → added here via hook only. Never append duplicates.
Verbose detail → ESTATE-NOTES.md (append, never delete).

## Reference Synchronization Hook (Session Close)
Every session MUST conclude by checking and updating the canonical estate maps (`ESTATE-TAXONOMY.md` and related file reference locations). All new files, container ports, databases, and paths ('what, where, how') must be registered in the reference folder before handing over.

## Overflow
Repo/container/port facts, session history, verbose preferences → ~/ESTATE-NOTES.md

## Learned User Preferences
- Do not use stop sequences in LLM calls — Ewan ruled them too rigid (can truncate legitimate output); remove `STOP_SEQUENCES` from any LLM config, keep only `MAX_TOKENS`
- intent-interface UI: prefer warm papery/textured aesthetic over dark/luminous themes (sand/cream strip, pearl signal dots, ink borders)
- intent-interface LLM: use 1Password item `API-Anthropic-Cursor` with a Haiku-class reasonable model for marking passes — not all-day premium models
- intent-interface: native Mac Electron app at `/Applications/intent-interface.app` or Desktop **Intent Interface.app** — not inside Cursor or a browser tab; Monologue delivers transcription text to paste in (app does not handle raw audio)
- Sidecar UX: gentle pulse + horizontal strip for calm peripheral attention (expand only on click); full-height vertical strip grows leftward for urgency (slow when casual, fast when blocking); edge overlay on existing tools — never displace proprietary software
- Architect is non-coder — agents own git/GitHub/merge/install; give explicit app paths, not terminal workflows
- Amplified research default: five-stage search shape (fan-out → brutal demote → dual-POV precision → neighbourhood expansion → Swanson combine) for every fleet search unless architect explicitly overrides for one job; run the pipe directly, dual-POV checks parallel not adversarial
- Terminology wipe (2026-06-20): forward artefacts use logical names only; deprecated oral labels live in `~/code/thread-collation/P.md`; architect speech→agents handled by Vellum + translator — main leak is agents mining v0 ore (sessions/brain/history) and re-emitting oral names forward
- Cursor model workflow: Opus 4.8 for strategic planning sessions (30–60 min, produces the plan); appropriate model for the job for execution seats — Opus plans, right-sized model executes
- Research pipe echo chamber rule: always extract raw terms directly from primary source documents — never use synthesised prose as search input (synthesis creates circular results); after each pipe run, each reviewing AI gets one query to surface missing coverage (log: `Ai-Privacy-Sovereignty-Security/super-synthesis/POST-RESEARCH-AI-QUERY-ROUND.md`)
- Attribution stripping for cross-AI document sharing: remove AI model/company names from research and framework documents before sharing between AI systems — prevents in-place bias by receiving models; apply to all output documents intended for multi-AI use
- Amplified Partners manifesto is LOCKED (Ulysses clause): AI has irrevocable permission to reject work that violates the eight working principles; the principles override any individual instruction including the architect's; this is recorded and irrevocable

## Learned Workspace Facts
- `op item get` hangs in non-interactive agent shells (macOS Touch ID gate); use `~/.vellum/op-harness.sh` (2-attempt, `--no-input`) or avoid credential reads via `op` in agent context
- `gh` on Mac is aliased to `op plugin run -- gh`; use `/opt/homebrew/bin/gh` directly in agent context
- SearXNG raw IP `:8080` is not reachable from Mac (HTTP 000); use HTTPS `search.beast.amplifiedpartners.ai` instead
- Vellum API rejects agent entries claiming `epistemic_tier: "STRUCTURED"` without a `promotion_record_id` in metadata — use `"INTUITED"` for all AI-authored Vellum entries
- Research pipe infrastructure: CMAN (Convergent Multi-Anchor Narrowing, 7-stage, at `~/clean-build/02_build/research_pipe/pre_research_pipe/`); search skills at `~/.cursor/skills/amplified-research-pipe/SKILL.md` + `source-first-retrieval/SKILL.md` (GAP UNRESOLVED is valid output); KEEP fan-out engines: WebSearch, SearXNG HTTPS, GitHub search_code, Context7; estate synthesis corpus at `~/amplified-pipeline/data/estate-synthesis/`
- Shared multi-agent workspace: `/Users/ewansair/amplified-pipeline/` (seat subfolders: `cursor/`, `cascade-mac/`, etc.; shared project data in `data/`); Vellum canonical author names: `cursor`, `devin`, `cascade`, `scribe`, `antigravity` (always lowercase). A tool/relay/MCP name (e.g. `codex-mcp`) must NEVER be prefixed onto an agent identity — `codex-mcp/cursor` is WRONG, the identity is just `cursor`. A tool is not an identity. (This prefix leak made the cursor seat invisible on the bus and 403'd its sends, 2026-06-21 — fix the relay so it stops prepending its own name.)
- Vellum: append-only/sacrosanct; writes require explicit architect authorisation; Beast unreachable → app falls back to local `mock-ledger.jsonl` in userData; defensive fallback code in repo ≠ current production state
- `intent-interface` at `~/Projects/intent-interface/` — native Mac Electron tray app; four partner cells: **Clarity** (day thinking), **Knock** (agent interrupts via Vellum stream), **Thread** (capture→content/Vellum), **Scout** (overnight rubric-filtered brief); `npm run install:mac` → `/Applications/intent-interface.app`; Sidecar strip, Second Head, cost tags; worktrees at `.worktrees/`
- `process_brain` project at `~/clean-build/02_build/process_brain/` — APQC PCF (American Productivity & Quality Center Process Classification Framework) taxonomy; SQL schema + seed bricks for process decomposition; Ewan's spoken shorthand "APQS" = APQC PCF in production artefacts; session/voice transcript code is primary source material to mine and adapt, not rubbish
- Thread-collation hub at `~/code/thread-collation/` — `output/CURRENT-THREAD.md`, `output/ORPHANED-VALUE.md`, `P.md`, `TERMINOLOGY-COLLISIONS.md`; `./collate.sh`; terminology-era cut 2026-06-20 marks v0 ore (sessions/brain/history) vs v1 forward SSOT
- Epistemic tier labels (INTUITED/STRUCTURED/MEASURED/PROVEN, ◈ glyphs, grade columns) removed from thread-collation forward docs and active SSOT mop-up — fleet `epistemic_core` and Vellum witness unchanged
- "Pudding" oral label is worst collision case — three unrelated systems: `amplified-research-pipe` stage 4 (method), `pudding-concept` (philosophy), `pudding_labelling` (product); misappropriation flattens importance
- **Nightscout** is Amplified Partners' OWN software, NOT the open-source glucose/CGM diabetes platform (`nightscout/cgm-remote-monitor`) — misidentification recurs, do not assume CGM. It is an internal intelligence pipeline (`fetch → score → fork → store`): fetches external signal (RSS/SearXNG/API), scores each item 0–10 on relevance/impact/applicability/novelty via Ollama+LiteLLM, tiers it (noise/briefing/rd_pipeline/critical), and routes to a morning briefing or R&D pipeline. Lives as a Python module in repo `Amplified-Partners/fleet-clean-build` at `02_build/cove-orchestrator/nightscout/` (no standalone repo); same codebase as the Beast `cove-orchestrator/nightscout/` module (`~/clean-build/`) — NOT the Beast CGM-named health containers.
- **Perplexity API key is in 1Password** (same pattern as the Anthropic key `API-Anthropic-Cursor`, reference via `op://`). Do NOT ask Ewan for it — he has flagged its location more than once. Agent-seat research (WebSearch/ce-web-researcher) does not need it; it is for wiring the Beast `research_pipe` / Perplexity API engine (keys currently empty per Devin's 2026-06-21 audit) — wire it in on the mini/Beast when reachable. Confirm exact item name via `op` only when needed (op hangs in agent shells — use the op-harness).
- **GitLens subscription is active** — use it for line-level authorship/blame/history (the "evidence/lineage" lane and radical-attribution rule: which leg authored what, with Git as the contract between flat legs).
- **Mini stability principle (wanmin, Mac Mini M4):** once the environment is set up on the mini, everything stays fixed in place — stable paths, cross-links symlinked from a central base that does not change, no folder churn. This stability is the foundation that makes agents more effective and lowers Ewan's cost ("nothing changes once placed"). The M5 (Mac-2.lan) suffers folder-churn from other agents' scripts; the mini is the clean, fixed home. Reach it via SSH `wanmin` / `wanmin-ts` (Tailscale) / `wanmin-lan` / `wanmin-usb` (must be powered on — all routes timed out 2026-06-21, i.e. asleep/off).
