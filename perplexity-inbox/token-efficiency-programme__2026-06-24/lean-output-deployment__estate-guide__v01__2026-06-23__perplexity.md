# Lean Output — Estate Deployment

TIER: STRUCTURED · output/input ratio MEASURED on Ewan's threads · 5× output multiplier MEASURED at source · per-IDE knobs from prior research (official docs)
Goal: one lean-output rule, deployed in the right config slot for every IDE/UI. Cutting reply length ~X% cuts per-turn spend ~X% (your input is ~0.5% of turn cost).

## The rule (identical everywhere)
Default 1–3 sentences. Answer, stop. No preamble, recap, "great question", or summary closer. No option-menus unless the path is genuinely ambiguous and a wrong guess is costly. Don't explain what's already known. Expand only on request or a real judgment call (show only the reasoning that changes the decision). Lead with the answer. Code/deliverables complete but fluff-free; the chat around them stays short. One follow-up question max.

## Where it goes, per surface

| Surface | Put the rule in | Mechanism |
|---|---|---|
| **Claude Code** | `CLAUDE.md` (top, "Output discipline" block) + optional `/output-style` | Loaded every session. Also cap `MAX_THINKING_TOKENS`, `/effort low` for routine work. |
| **Cursor** | `.cursor/rules/lean-output.mdc` with `alwaysApply: true` | Project rule, every request. Pin model; Auto mode, not Max. |
| **Windsurf / Cascade** | `.windsurfrules` (repo root) | Global rule for Cascade. |
| **Cline / Roo** | Custom Instructions field (settings) | Applied to every task. |
| **Aider** | `.aider.conf.yml` → `read:` a `CONVENTIONS.md` holding the rule | Loaded as read-only context each run. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Repo-wide chat instructions. |
| **Gemini CLI** | `GEMINI.md` (repo root) | Hierarchical context, every invocation. |
| **OpenAI Codex CLI** | `AGENTS.md` (repo root) | Read on start. |
| **Zed** | Assistant → Custom Instructions | Per-thread system prompt. |
| **Consumer UIs** (ChatGPT, Claude.ai, Gemini, Perplexity) | Custom Instructions / Personalization field | Persists across chats. |

## Canonical block to paste
Keep one copy as `CONVENTIONS.md` in each repo; the IDE-specific files above either contain it or `read:`/reference it. Single source, no drift.

```
# Output discipline (non-negotiable)
Be lean. The user understands things and will ask if he wants more.
- Default reply: 1–3 sentences. Answer the thing asked, then stop.
- No preamble, no recap of my question, no "great question", no summary closer.
- No option-menus or (a)/(b)/(c) branches unless genuinely ambiguous and a wrong guess is costly.
- Don't explain what I already know. Don't define terms unprompted.
- Expand only when I ask, or when a real judgment call needs its reasoning shown — and then only the reasoning that changes the decision.
- Lead with the answer; detail after.
- Code/deliverables: complete but fluff-free. The chat around them stays short.
- One follow-up question max, only if you can't proceed without it.
Self-check before sending: did he ask for this much? Does every sentence earn its place? If not, cut.
```

## Apply once, then leave it
1. Drop `CONVENTIONS.md` in each active repo.
2. Wire the surface-specific file from the table (most just contain the block).
3. New repos: copy `CONVENTIONS.md` in at init.

Sources: per-IDE config slots from official docs (Anthropic, Cursor, Codeium, GitHub, Google, OpenAI, Zed); output-cost multiplier from provider pricing. Full detail in `research_ide_controls.md`.
```
