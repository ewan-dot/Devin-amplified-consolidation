---
project: amplified-ide-harness
artifact_type: implementation-plan
purpose: token-optimisation-AND-effectiveness-via-hooks-harness-and-compound-engineering
version: v02
date: 2026-06-24
origin: perplexity
supersedes: claude-code-max__token-optimisation__hooks-and-harness-plan__v01__2026-06-24__perplexity.md
intended_implementer: any IDE on the Sovereign Agent Harness — Claude Code, Codex, Cursor, Antigravity, Copilot, Factory Droid, Gemini CLI, Qwen Code, OpenCode, Kiro, Pi
status: ready-to-implement
tier: STRUCTURED
preconditions:
  - implementer is an IDE/agent on Ewan's Mac fleet (M5/M4/WanMin) running consumer subscriptions, not raw API
  - implementer has write access to its own config surface (~/.claude/, ~/.codex/, .cursor/, .github/copilot/, ~/.config/<tool>/) and to project .claude/, AGENTS.md, CLAUDE.md
  - VSCodium is the operator console; per-agent worktrees per Sovereign Agent Harness; Vellum Baton mediates writes; M5 polls Vellum for work
  - no proxying of consumer subscriptions into raw tokens (per vscodium-agent-workbench wiki, cite [5])
  - the implementer will treat token-optimisation (efficiency) and Compound Engineering (effectiveness) as two complementary layers, not a trade-off
provenance:
  # Token optimisation
  - https://docs.anthropic.com/en/docs/claude-code/hooks  (official hooks reference, 2026-06-16 — schema changed materially this release)
  - https://docs.anthropic.com/en/docs/claude-code/hooks-guide
  - https://docs.anthropic.com/en/docs/claude-code/settings
  - https://docs.anthropic.com/en/docs/claude-code/output-styles
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  (2025-09-29)
  - https://www.anthropic.com/engineering/claude-code-best-practices  (2025-04-18)
  - https://institute.sfeir.com/en/claude-code/claude-code-context-management/optimization/  (measured deltas)
  - https://github.com/ryoppippi/ccusage  (ccusage statusline + reports)
  - https://www.mindstudio.ai/blog/claude-code-compact-command-context-management  (compact-at-60%)
  # Compound Engineering (effectiveness layer)
  - https://github.com/EveryInc/compound-engineering-plugin  (canonical repo, MIT, 21k+ stars, v3.12.0 as of 2026-06-09; multi-IDE)
  - https://every.to/guides/compound-engineering  (Every guide, 2026-01-17)
  - https://every.to/source-code/compound-engineering-camp-every-step-from-scratch  (2026-03-13)
  - https://every.to/source-code/the-folder-is-the-agent  (2026-04-13, “the folder is the agent”)
  - https://lethain.com/everyinc-compound-engineering/  (Will Larson, 2026-01-19, independent analysis)
  - https://www.buildthisnow.com/pt/blog/guide/mechanics/compound-engineering  (2026-06-08, hand-rolled recipe)
  # Amplified prior art
  - memory/knowledge/projects/vscodium-agent-workbench.md  (VSCodium as scriptable console; Vellum is source of truth)
  - memory/knowledge/projects/sovereign-agent-harness.md  (single write lease, blinkers without ceilings, per-cell isolation)
  - memory/notes/work/Amplified/methodologies/compound_engineering.md  (Plan/Work/Review/Compound; 80% in plan+review)
---

# Amplified IDE — Token-Optimised AND Compound-Engineered Operating Plan

**Audience:** every IDE on Ewan's Sovereign Agent Harness — not just Claude Code.
**Constraint:** changes ONLY via hooks, settings files, and harness surface of each tool — never via SDK wrappers, proxies, or weight modifications. Consumer subscriptions stay consumer subscriptions.
**Goal:** maximise *useful work shipped per token spent* by stacking two independent layers — efficiency (hooks + harness) and effectiveness (Compound Engineering loop). Tokens saved are reinvested in the work, not pocketed.

**What changed from v01:** v01 was Claude-Code-only and treated tokens as the only optimisation target. v02 extends to every IDE in the fleet, adds the Compound Engineering layer (Plan / Work / Review / Compound) as the *effectiveness* axis that the token savings fund, and slots both into the existing VSCodium Agent Workbench and Sovereign Agent Harness models so nothing is bolted on sideways.

---

## 0. Mental model (read first, this is the whole thing)

Two orthogonal axes, both must be optimised:

```
        EFFECTIVENESS (Compound Engineering — Every / Klaassen)
        ▲
        │   ┌──────────────────────────────────────┐
   high │   │  v02 target zone                     │
        │   │  CE loop on top of lean hooks        │
        │   │  every PR teaches the system         │
        │   │  every IDE                           │
        │   └──────────────────────────────────────┘
        │   ┌──────────────────────────────────────┐
        │   │  v01 zone                            │
        │   │  lean hooks, Claude only             │
        │   │  no compounding asset                │
        │   └──────────────────────────────────────┘
    low └─────────────────────────────────────────────► EFFICIENCY (hooks + harness)
                                                       low                   high
```

**The trade-off Ewan named is not real for long.** CE costs tokens up-front (planning docs, multi-agent review, lessons capture). It saves tokens permanently because the agent stops re-discovering the same thing. The break-even is fast — Every claims "80% of effort in plan and review" and runs five products with single-person teams as a result (Every, 2025-12-11; 2026-06-08).

**The pipe is the same for every IDE:**

```
operator (VSCodium) ─▶ IDE (Claude/Codex/Cursor/Antigravity/...) ─▶ worktree
                                  │
                                  ├─ hooks/harness reduce per-turn token cost      (efficiency)
                                  ├─ Compound Engineering loop reduces per-task cost over time (effectiveness)
                                  └─ Vellum Baton mediates writes; M5 polls Vellum (sovereignty)
```

CE is **not a Claude-Code-only thing.** The Every plugin officially ships to Claude Code, Codex, Cursor, GitHub Copilot, Factory Droid, Qwen Code, OpenCode, Pi, Gemini CLI, and Kiro — and the underlying loop (rules file + lessons file + capture command) is IDE-agnostic and reproducible by hand in any tool that reads a project markdown file (GitHub repo, README; Build This Now, 2026-06-08).

---

## 1. The two-layer stack

### Layer A — Efficiency (hooks + harness) — per-IDE

This is v01, with one cross-IDE addition. **Implement once per IDE; the patterns transfer.**

**A.1 Claude Code (Max plan):** implement v01 as written. The full 6-hook + 3-subagent + lean-output-style + ccusage statusline + MCP audit stack. See v01 §1–§5.

**A.2 Codex CLI:** the equivalents.
- `~/.codex/config.toml`: prune model list to the one in use; disable tools not needed.
- Codex does not have Claude Code's `PostToolUse` hook — but it does have `~/.codex/hooks/` for pre/post-command callbacks and a `--profile` mechanism to swap personalities. Use a wrapper that pipes `bash`/`read` outputs through the same `post-tool-redact.py` from v01 §2.3 (it's just a stdio filter; works anywhere).
- For statusline: ccusage doesn't track Codex; instead use the OpenAI usage dashboard polled via cron into the same `~/session-costs.jsonl`.

**A.3 Cursor:** Cursor doesn't expose hooks but does expose `.cursorrules` and project `.cursor/` config.
- Cap `.cursorrules` at 3,000 tokens (same rule as CLAUDE.md).
- Set `Cursor Settings → Models → Auto Mode` for routine work (cheaper model picks for cheap tasks).
- Disable indexer on `node_modules`, `dist`, `build`, `.next`, `target`, `__pycache__`, `vendor` via `.cursorignore` (mirrors the `.gitignore` block in v01 §1.3).
- For redaction: Cursor has no PostToolUse hook, but you can wrap noisy commands at the shell level — e.g. a `~/.local/bin/qbuild` that runs `npm run build` and pipes through the same redactor.

**A.4 Antigravity (Google):** uses `AGENTS.md` natively (CE-compatible by default). Apply CE Layer B directly; for efficiency, mirror the gitignore/ignore patterns; Antigravity's plan mode is built-in.

**A.5 GitHub Copilot CLI / VS Code Copilot Agent:** plugin manifests are Claude-compatible (per Every README); CE installs directly. For efficiency, set `copilot.context.maxFiles` low and exclude binary/vendor paths in workspace config.

**A.6 Cross-IDE: the shared redactor.** Drop the v01 `post-tool-redact.py` and `pre-bash-guard.py` into `~/.amplified/bin/` once, symlink from each IDE's hook directory. One implementation, many consumers — Sovereign Agent Harness, "one active write door" principle applied to hook code (sovereign-agent-harness wiki, cite [1]).

### Layer B — Effectiveness (Compound Engineering) — per-project, every-IDE

**This is the new layer.** Install once per project; every IDE that opens that project worktree picks it up automatically because the loop lives in repo files (`AGENTS.md`, `CLAUDE.md`, `.claude/lessons.md`, `.claude/commands/`), not IDE config.

**B.1 The loop (Every, Klaassen + Shipper):**

```
Plan ─▶ Work ─▶ Review ─▶ Compound ─▶ (next Plan reads what Compound wrote)
```

- **Plan:** the agent reads the issue, researches, writes a markdown plan with file refs, data models, edge cases, sources. Decouples implementation from research (Larson, 2026-01-19). 80% of effort lives here and in Review (Every README).
- **Work:** agent executes plan in an isolated worktree, runs tests/lint/typecheck. (Already enforced by Sovereign Agent Harness — one worktree per agent, vscodium-agent-workbench cite [3].)
- **Review:** human reviews two things — the output AND the lessons learned. Multi-agent review (`/ce-code-review`) catches more before human eyes.
- **Compound:** agent writes lessons back to `lessons.md` / skills / agents so the next Plan inherits them. **This is the only step that creates compounding capital. Skipping it is the most common failure mode** (Larson; Build This Now).

**B.2 Install the Every plugin in every supported IDE in the fleet:**

| IDE | Install commands |
|---|---|
| Claude Code | `/plugin marketplace add EveryInc/compound-engineering-plugin` then `/plugin install compound-engineering` |
| Codex | `codex plugin marketplace add EveryInc/compound-engineering-plugin` → `bunx @every-env/compound-plugin install compound-engineering --to codex` → `/plugins` TUI to enable. **All three steps needed** (Codex spec doesn't yet register custom agents natively). |
| Cursor | In Cursor Agent chat: `/add-plugin compound-engineering` |
| Copilot CLI | `copilot plugin marketplace add EveryInc/compound-engineering-plugin` → `copilot plugin install compound-engineering@compound-engineering-plugin` |
| VS Code Copilot Agent | `Chat: Install Plugin from Source` → `EveryInc/compound-engineering-plugin` → select `compound-engineering` |
| Factory Droid | `droid plugin marketplace add https://github.com/EveryInc/compound-engineering-plugin` → `droid plugin install compound-engineering@compound-engineering-plugin` |
| Qwen Code | `qwen extensions install EveryInc/compound-engineering-plugin:compound-engineering` |
| OpenCode | `bunx @every-env/compound-plugin install compound-engineering --to opencode` |
| Gemini CLI | `bunx @every-env/compound-plugin install compound-engineering --to gemini` |
| Kiro | `bunx @every-env/compound-plugin install compound-engineering --to kiro` |
| Pi | `pi install npm:pi-subagents` (required) + `pi install npm:pi-ask-user` (recommended) → `bunx @every-env/compound-plugin install compound-engineering --to pi` |
| **All at once** | `bunx @every-env/compound-plugin install compound-engineering --to all` (auto-detects installed targets) |

After install, the same loop runs everywhere: `/ce-strategy` → `/ce-ideate` → `/ce-brainstorm` → `/ce-plan` → `/ce-work` → `/ce-code-review` → `/ce-compound`. Side commands: `/ce-debug`, `/ce-product-pulse`, `/ce-setup`.

**B.3 Hand-rolled fallback** (for any IDE the plugin doesn't yet support, or for sovereignty if Ewan ever wants to fork): three files per project.

`AGENTS.md` (IDE-agnostic; most modern coding agents read it):
```markdown
# Project Rules

Stack: <python|rust|node|...>
Conventions: <house rules>
Definition of done: tests pass, type-check clean, /ce-compound has been run.

@./.claude/lessons.md
```

`.claude/lessons.md` (the compounding asset — starts empty, grows one entry at a time):
```markdown
# Lessons (append-only)

<!-- Each entry: ## YYYY-MM-DD — short rule phrased as a "don't" or "always" -->
```

`.claude/commands/compound.md` (the capture command — IDE-agnostic markdown):
```markdown
---
description: Extract lessons from this task and append to lessons.md
---
Review what we just did in this session.
Identify mistakes the agent made, surprises, gotchas, or conventions we discovered.
For each, write one short rule (imperative, phrased as "always X" or "never Y").
Append to .claude/lessons.md under today's date.
Do not duplicate existing entries.
```

The `@./.claude/lessons.md` syntax in `AGENTS.md` makes the lessons load into every session automatically. The next `/plan` reads them. The circle closes (Build This Now, 2026-06-08).

**B.4 Where CE lives in the Sovereign Agent Harness:**

- The CE plugin files (`AGENTS.md`, `lessons.md`, `STRATEGY.md`, `docs/brainstorms/`, `docs/pulse-reports/`) live **in the project repo** and travel with the worktree.
- The plan-docs (`/ce-plan` output) and the multi-agent review (`/ce-code-review`) are exactly what the harness's "witnessed authority" expects — the work is auditable, the lessons are attributed (rod 3, radical attribution), and the PR is the merge gate where Ewan holds the pen (per sovereign-agent-harness cite [6]).
- "The folder is the agent" (Every, 2026-04-13) is the same idea as the workbench's "contract-bearing work-desks" (vscodium-agent-workbench cite [4]). They compose cleanly.

---

## 2. Why CE is worth the tokens (the honest trade-off)

CE adds token cost in three places:

1. `/ce-plan` produces a markdown plan (~2–5k tokens output, one-off per feature).
2. `/ce-code-review` spawns multiple review subagents (~5–15k tokens, one-off per PR).
3. `/ce-compound` synthesises and appends lessons (~500–1500 tokens, one-off per task).

It saves token cost in five places, **permanently and compoundingly**:

1. The agent re-reads `lessons.md` every session — but it's tiny (kilobytes after months), and prevents repeated re-discovery of the same gotchas. Net win after ~3–5 repeats.
2. `/ce-plan` upfront eliminates the typical 3–10 round-trips of "wait, what about edge case X?" mid-implementation. Each round-trip avoided = full prompt re-send saved.
3. Multi-agent review catches mistakes before they become rework loops. Rework on a 200-line PR can cost 50k+ tokens; CE review costs 15k.
4. Plan docs are reusable artefacts that train the next plan via `lessons.md` — the same lesson that cost 5k to learn the first time costs near-zero to apply the 50th time.
5. CE pairs naturally with Layer A's subagent offload (v01 §3.1) — the plan-then-execute pattern *is* the subagent pattern. They aren't two costs; they're the same cost paid once.

Will Larson's independent analysis (2026-01-19) frames it bluntly: the four steps "are not shocking but are an extremely effective way to convert intuited best-practices into something specific, concrete, and largely automatic." The token cost buys automation that doesn't degrade.

**Net expectation (STRUCTURED, to be re-measured at week 1, 4, 12):**

- Week 1: CE adds ~15% net token spend, no measurable speed gain (the `lessons.md` is empty).
- Week 4: parity; lessons start preventing real rework.
- Week 12: net 30–50% reduction in tokens-per-shipped-feature, plus durable quality gains (fewer regressions, less context-loss on resumption).

---

## 3. Implementation order (a single sequence any of you can follow)

Do Layer A first per-IDE (one-off setup), then Layer B per-project (recurring on every repo). Do them in this order:

**Phase 1 — Layer A install (one Saturday afternoon, per IDE in fleet):**
1. Implement v01 §1–§5 for Claude Code (Max).
2. Repeat the analogous setup for each other IDE in active use (start with Codex and Cursor; Antigravity, Copilot can follow).
3. Drop `post-tool-redact.py` and `pre-bash-guard.py` into `~/.amplified/bin/`; symlink from each IDE's hook directory. Single source of truth, multiple consumers.
4. Wire ccusage statusline into Claude Code; wire OpenAI usage poller into the same JSONL for Codex; do the same for any other paid surface.

**Phase 2 — Layer B install (per project, ongoing):**
5. Pick the top 3 active project repos (the ones touched this week).
6. In each, install the CE plugin via the IDE you most use on that repo (probably Claude Code).
7. Author a project `AGENTS.md` that names the stack, conventions, and definition of done — and includes `@./.claude/lessons.md`.
8. Create an empty `.claude/lessons.md`.
9. From now on, **every task starts with `/ce-plan` and ends with `/ce-compound`.** No exceptions. The discipline is the asset.
10. On any new project, repeat steps 6–9 as the first commit.

**Phase 3 — Fleet integration (per Sovereign Agent Harness):**
11. Each agent worktree (per Apple-container cell, per sovereign-agent-harness cite [5]) carries its own copy of the CE files. Lessons learned in cell A propagate to cell B only by Vellum (the witness layer), not by direct file sync — keeps "single write lease" intact.
12. When `/ce-compound` runs in any cell, the resulting lesson is emitted as a Vellum event (`event_type: compound_lesson`) with `signed_by: <agent_id>`, `tier: STRUCTURED` (since it's a heuristic written by an LLM), per the min-rule. M5 picks it up, deduplicates, and updates a canonical `~/lessons-canonical.md` that the next plan in any cell reads.
13. This makes lessons a **federated asset** under the min-rule's federation rule — aggregation across contributors cannot promote tier, so the canonical lessons stay STRUCTURED, not MEASURED, until someone empirically tests them.

---

## 4. The combined stack — what a session looks like end-to-end

(Claude Code shown; substitute slash commands per IDE.)

```
[VSCodium opens worktree on M5]
    ↓
[SessionStart hook] injects 500-token preamble (branch, last 3 commits, CURRENT_TASK)
    ↓
[ccusage statusline] shows: today $X, block $Y remaining, burn rate Z/h
    ↓
You: /ce-plan "add retry-with-backoff to the job queue"
    ↓
[plan subagent] reads issue, lessons.md (already knows: "never use setTimeout in workers"), writes docs/plans/2026-06-24-retry-backoff.md
    ↓
You review plan, approve.
    ↓
You: /ce-work
    ↓
[work subagent] executes plan in worktree; [PreBash guard] blocks unbounded find; [PostToolUse redactor] truncates pnpm install output from 80k chars to 6k
    ↓
[Stop hook] sees transcript at 55% of window, no nudge yet
    ↓
You: /ce-code-review
    ↓
[review subagents] check style, security, perf, test coverage; surface 2 issues
    ↓
You fix the 2 issues with a targeted edit.
    ↓
You: /ce-compound
    ↓
[compound subagent] appends to lessons.md: "always pass AbortSignal to retry timers" + "test coverage rule: every new worker fn needs a timeout test"
    ↓
[Vellum event emitted] event_type=compound_lesson, signed_by=claude-code-on-m5, tier=STRUCTURED
    ↓
[SessionEnd hook] writes session cost to ~/.claude/session-costs.jsonl
    ↓
[Next session, any IDE on this repo] reads the new lessons via AGENTS.md @-include. Doesn't re-make the same mistake.
```

Every component above is either Layer A (efficiency) or Layer B (effectiveness). They run together by design.

---

## 5. Verification

After implementation, these must hold; if not, something is mis-installed:

**Layer A (per IDE):** as v01 §3.

**Layer B (per project, after first `/ce-compound`):**
- `AGENTS.md` exists at repo root and `@`-includes `.claude/lessons.md`.
- `.claude/lessons.md` has at least one entry within 24 hours of installation.
- `/ce-plan`, `/ce-work`, `/ce-code-review`, `/ce-compound` are recognised slash commands in the IDE.
- Opening the same repo in a *different* IDE in the fleet (e.g. Cursor after Claude) shows the same lessons being honoured — proves the loop is IDE-agnostic.

**Layer B (fleet, after week 1):**
- `~/lessons-canonical.md` exists on M5 and aggregates lessons from at least 2 different agent cells.
- Vellum has at least 5 `event_type: compound_lesson` events, each `signed_by` an agent proxy, each `tier: STRUCTURED`.
- A plan written in week 2 cites at least one lesson from week 1 by reference.

---

## 6. What this plan deliberately does NOT do (carried from v01, plus new)

From v01 (unchanged):
- No API keys. Consumer subscriptions only.
- No proxy of consumer subs into raw tokens (vscodium-agent-workbench cite [5]).
- No auto-`/compact`; the Stop hook nudges, the human decides.
- No weight/system-prompt modification at the platform level.

New in v02:
- No promotion of CE lessons to MEASURED tier by virtue of repetition alone. Federated aggregation does not promote tier (min-rule federation rule). Lessons stay STRUCTURED until someone runs an eval harness against them.
- No skipping `/ce-compound`. The discipline IS the asset. A session that ships code without compounding has spent tokens and grown no capital.
- No direct file-sync of `lessons.md` between agent cells. Lessons travel only via Vellum events, keeping the single-write-lease invariant intact (sovereign-agent-harness cite [1]).
- No replacement of VSCodium as the operator console. Antigravity, Cursor, Claude Code, Codex are agents *inside* the console; VSCodium remains the human's seat.

---

## 7. Expected impact (STRUCTURED → MEASURED over 12 weeks)

| Lever | Source | Week 1 | Week 4 | Week 12 |
|---|---|---|---|---|
| Layer A: lean hooks | SFEIR / v01 | ~30% input-token cut | ~50% | ~50% (steady-state) |
| Layer A: lean output style | v01 | ~20% output-token cut | ~20% | ~20% |
| Layer B: CE plan-first | Every | +15% spend (no lessons yet) | 0% (parity) | -25% (lessons working) |
| Layer B: CE multi-agent review | Every | +5% spend | -10% (rework prevented) | -20% |
| Layer B: CE compound asset | Every / Larson | 0% | -5% | -15% (durable) |
| **Net blended** | combined | **~35% reduction, slight quality lift** | **~55% reduction, real quality lift** | **~60% reduction, durable quality + cross-IDE portability** |

The week-1 number is consistent with v01's ceiling. Weeks 4–12 are the compounding return on CE.

---

## 8. Open questions (parked, not blocking)

- **Codex agent-spec convergence:** Every's docs say "once Codex's native plugin spec supports custom agents, the Bun agent step goes away." Track that; remove the extra step when it lands.
- **Antigravity ↔ CE plugin:** Antigravity uses AGENTS.md natively and has a Skills system. Verify CE plugin installs cleanly there; if not, the hand-rolled fallback (§B.3) works regardless.
- **Vellum schema for `compound_lesson` events:** define the schema once, register it in the pipe, then every IDE emits the same shape. Belongs in a follow-up artifact in this folder.
- **Lesson-eval harness:** the path from STRUCTURED lessons to MEASURED lessons. Needs an eval suite (bash script that runs lesson-violating prompts and checks the agent catches them). Out of scope here; flagged for a future task.
- **Cross-IDE statusline:** ccusage is Claude Code only. Codex/Cursor/Antigravity each have their own usage UI. A unified "fleet cost" dashboard (read all the JSONLs, render one number) is a 50-line Python script — schedule it.

---

## 9. Attribution

**Token optimisation:** Anthropic Claude Code docs (hooks, settings, output-styles, subagents); Anthropic engineering blog (*Effective context engineering*, 2025-09-29); SFEIR Institute (measured deltas); MindStudio (compact-at-60%); Ryoppippi (ccusage).

**Compound Engineering:** Every (Dan Shipper + Kieran Klaassen) — guides, the plugin (EveryInc/compound-engineering-plugin, MIT, 21k+ stars), the "folder is the agent" piece. Will Larson (independent analysis, 2026-01-19). Build This Now (hand-rolled recipe, 2026-06-08).

**Amplified prior art:** vscodium-agent-workbench wiki, sovereign-agent-harness wiki, compound_engineering note — all in `memory/`.

— STRUCTURED · synthesised from 9 primary + 4 secondary external sources + 3 internal wikis · valid 90d · re-check on Claude Code minor version bumps, Every plugin minor releases (currently v3.12.0), and Codex plugin-spec changes

[CLOSURE] branch=PLAN | proxy=none | gates=none | inbox=claude-code-max__token-optimisation__hooks-and-harness-plan__v02__2026-06-24__perplexity.md | tier=STRUCTURED
