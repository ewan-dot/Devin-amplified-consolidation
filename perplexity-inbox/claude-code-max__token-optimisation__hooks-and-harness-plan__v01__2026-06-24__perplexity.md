---
project: claude-code-max
artifact_type: implementation-plan
purpose: token-optimisation-via-hooks-and-harness
version: v01
date: 2026-06-24
origin: perplexity
intended_implementer: claude-code-on-mac (self-editing his own config)
status: ready-to-implement
tier: STRUCTURED
preconditions:
  - implementer is Claude Code on Ewan's Mac (Max consumer plan, claude.ai login)
  - implementer has write access to ~/.claude/ and project .claude/
  - implementer will NOT use Anthropic API key — Max consumer login only
  - all changes must be via hooks + harness (settings.json, hook scripts, statusline, subagents, output-styles) — no other mechanism
provenance:
  - https://docs.anthropic.com/en/docs/claude-code/hooks  (official hooks reference, 2026-06-16)
  - https://docs.anthropic.com/en/docs/claude-code/hooks-guide  (hooks guide)
  - https://docs.anthropic.com/en/docs/claude-code/settings  (settings reference)
  - https://docs.anthropic.com/en/docs/claude-code/output-styles  (output styles)
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  (2025-09-29)
  - https://www.anthropic.com/engineering/claude-code-best-practices  (2025-04-18)
  - https://institute.sfeir.com/en/claude-code/claude-code-context-management/optimization/  (SFEIR optimisation guide with measured deltas)
  - https://github.com/ryoppippi/ccusage  (ccusage statusline + reports)
  - https://www.mindstudio.ai/blog/claude-code-compact-command-context-management  (/compact at 60% practice)
---

# Claude Code (Max) — Token-Optimised Operating Plan

**Audience:** Claude Code, self-implementing on Ewan's Mac.
**Constraint:** changes ONLY via hooks and harness (settings.json + hook scripts + statusline + subagents + output-styles). No API key. No SDK wrappers. No proxy. No prompt-rewriting middleware.
**Goal:** reduce tokens-per-useful-outcome on the Max consumer plan so the 5-hour and weekly limits stretch further, without degrading work quality.

---

## 0. Mental model (read first)

The Max plan meters **tokens, not requests**, in rolling 5-hour blocks and a weekly cap. Every token you save in any of these five places compounds across the block:

1. **System prompt + CLAUDE.md** — paid on every turn.
2. **Tool result payloads** — biggest variable cost (file reads, bash output, MCP responses).
3. **Message history** — re-sent every turn until compacted.
4. **Subagent transcripts** — isolated; only the final summary returns to the parent.
5. **Output tokens (your own replies)** — cost ~5× input tokens at the model layer; on the Max plan you pay the same meter for output.

Hooks act on (1), (2), (3). Harness (subagents, output-styles, plan mode) acts on (4), (5). MCP server choice acts on (2).

Anchor numbers (MEASURED on third-party benchmarks, treat as STRUCTURED for your own setup until re-measured):

- Plan mode: ~50% input-token reduction on analysis/review/refactor-planning tasks (SFEIR).
- Subagent offload: ~40% reduction in main context (SFEIR).
- `.gitignore` discipline: ~25% reduction in file-read tokens on a Node-shaped project (SFEIR).
- Structured prompts vs narrative: ~30% fewer tokens, 92% vs 71% post-compact fidelity (SFEIR).
- Combining plan mode + PreCompact + multi-session: ~60% overall daily reduction (SFEIR).
- Compact at 60% utilisation, not 95% — proactive, not reactive (MindStudio).

---

## 1. The five-layer optimisation stack

Implement bottom-up. Each layer is independent; do not skip.

### Layer 1 — Settings & file-read discipline (deterministic, no LLM cost)

**Edit `~/.claude/settings.json` and project `.claude/settings.json`. These are the cheapest wins.**

1.1 **Drop the compaction threshold to 0.85.**
```json
{
  "autoCompactThreshold": 0.85
}
```
Triggers compaction earlier; preserves more usable context, ~2.3 s faster responses in long sessions (SFEIR / Anthropic changelog Jan 2026).

1.2 **Keep CLAUDE.md under 3,000 tokens, per directory.**
A bloated root `CLAUDE.md` is paid on every turn forever. Split into per-subdirectory files so each session loads only what is relevant. Audit existing CLAUDE.md files: anything > 3k tokens is broken into subdirectory files.

1.3 **`.gitignore` discipline at every project root.**
Claude Code respects `.gitignore` for auto-reads. Always-exclude list:
```
node_modules/
dist/
build/
.next/
coverage/
vendor/
*.min.js
*.map
*.lock
.venv/
__pycache__/
target/         # rust
*.pyc
```
This alone saved ~25% of file-read tokens in SFEIR's Node benchmark.

1.4 **Prune the tool list at the project level.** In each `.claude/settings.json`, declare only the tools that project actually needs (`allowedTools` / `disallowedTools`). Bloated tool sets waste prompt tokens and produce ambiguous routing (Anthropic context-engineering paper). Default-deny `WebFetch` and `WebSearch` on projects that don't need them.

### Layer 2 — Hooks (the heart of the plan)

All hook scripts live in `~/.claude/hooks/` (user-global) or `<project>/.claude/hooks/` (project-scoped). Make every script executable. Each hook reads JSON on stdin and writes JSON on stdout. Exit 0 for success; only `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart` stdout is injected as context — for every other hook, return structured JSON via `additionalContext`, `updatedToolOutput`, etc.

**2.1 `SessionStart` — inject a tight, high-signal preamble once.**

Purpose: replace ad-hoc CLAUDE.md bloat with a controlled, ≤500-token preamble that loads project state at session start instead of repeating it every turn.

Path: `~/.claude/hooks/session-start-preamble.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
# Read stdin (unused but required)
cat > /dev/null
# Build a compact preamble: git branch, last 3 commits, current task marker if present
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
{
  echo "branch: $(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || echo none)"
  echo "recent:"
  git -C "$PROJECT_DIR" log --oneline -3 2>/dev/null || true
  if [[ -f "$PROJECT_DIR/.claude/CURRENT_TASK" ]]; then
    echo "task:"
    head -c 800 "$PROJECT_DIR/.claude/CURRENT_TASK"
  fi
} | jq -Rs '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: .}, sessionTitle: "claude-code"}'
```

Settings entry (`~/.claude/settings.json`):
```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/session-start-preamble.sh" }
      ]}
    ]
  }
}
```

**2.2 `PreCompact` — protect critical context from being summarised away.**

Purpose: dump the live task spec and recent decisions to disk before compaction strips them, then re-inject them as a single short block.

Path: `~/.claude/hooks/pre-compact-preserve.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
INPUT=$(cat)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
BACKUP_DIR="$PROJECT_DIR/.claude/compact-backups"
mkdir -p "$BACKUP_DIR"
TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
# Persist a snapshot of the current task + last assistant message hash
echo "$INPUT" | jq '{trigger, custom_instructions}' > "$BACKUP_DIR/$TS-trigger.json"
[[ -f "$PROJECT_DIR/.claude/CURRENT_TASK" ]] && cp "$PROJECT_DIR/.claude/CURRENT_TASK" "$BACKUP_DIR/$TS-task.md" || true
# Do NOT block compaction — just observe and preserve
exit 0
```

Settings:
```json
{
  "hooks": {
    "PreCompact": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/pre-compact-preserve.sh" }
      ]}
    ]
  }
}
```

Pair this with a `SessionStart`-on-resume re-injection (the same hook reads the most recent backup if `$source == "compact"` or `$source == "resume"`).

**2.3 `PostToolUse` on `Bash`, `Read`, `WebFetch` — redact noisy output.**

Purpose: the single biggest non-prompt token leak. A `cargo build`, `pnpm install`, `pytest -v`, or full file read is mostly noise. Replace verbose payloads with a structured summary that preserves what Claude actually needs.

Path: `~/.claude/hooks/post-tool-redact.py`
```python
#!/usr/bin/env python3
"""Token-saving redactor for Bash/Read/WebFetch output.
Reads hook JSON on stdin; writes hook JSON on stdout.
Keeps head + tail, collapses middles, strips ANSI, hides node_modules walks."""
import json, re, sys

MAX_CHARS = 6000        # ~1500 tokens hard cap per tool result
HEAD = 2000
TAIL = 2000
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
NOISE = re.compile(r'(node_modules/|\.next/cache/|target/debug/|__pycache__/)')

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
resp = data.get("tool_response", {})
# tool_response shape varies; pull a string view
text = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
text = ANSI.sub("", text)
# Drop pure-noise lines
lines = [l for l in text.splitlines() if not NOISE.search(l)]
text = "\n".join(lines)
if len(text) > MAX_CHARS:
    head = text[:HEAD]
    tail = text[-TAIL:]
    elided = len(text) - HEAD - TAIL
    text = f"{head}\n\n[... {elided} chars elided by post-tool-redact ...]\n\n{tail}"
out = {
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "updatedToolOutput": text
    },
    "suppressOutput": True
}
print(json.dumps(out))
```

Settings:
```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Bash|Read|WebFetch", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/post-tool-redact.py" }
      ]}
    ]
  }
}
```

This is the highest-leverage single hook in the plan. A `pnpm install` is routinely 50–200k characters; capping at 6k removes ~95% of that load.

**2.4 `PreToolUse` on `Bash` — refuse known-bloat commands; rewrite where safe.**

Purpose: stop tokens being spent before they exist. Block or rewrite recursive `cat`, `find` over `node_modules`, `tree`-without-depth, `npm ls`, `pip list -v`, and similar.

Path: `~/.claude/hooks/pre-bash-guard.py`
```python
#!/usr/bin/env python3
import json, re, sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

# Hard-block patterns that almost always waste tokens
BLOCK = [
    (re.compile(r'\bfind\s+\.\s+(?!.*-(?:maxdepth|prune))'),
     "Use `find . -maxdepth N` or `rg --files -g 'pattern'`. Unbounded find on the repo blows context."),
    (re.compile(r'\bcat\s+.*\.(lock|min\.js|map)\b'),
     "Refusing to cat a lockfile/minified/map file — read what you need with rg or head."),
    (re.compile(r'\btree\b(?!.*-L)'),
     "Use `tree -L 2` or `tree -L 3`. Unbounded tree is a token bomb."),
    (re.compile(r'\bnpm\s+ls\b(?!.*--depth)'),
     "Use `npm ls --depth 0`."),
]
# Soft-rewrite patterns (we silently fix instead of blocking)
REWRITES = [
    (re.compile(r'\bcat\s+(\S+)\s*$'),
     lambda m: f"head -200 {m.group(1)}   # auto-trimmed by pre-bash-guard"),
]

for pat, reason in BLOCK:
    if pat.search(cmd):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason
            }
        }))
        sys.exit(0)

new_cmd = cmd
for pat, repl in REWRITES:
    new_cmd = pat.sub(repl, new_cmd)
if new_cmd != cmd:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": {"command": new_cmd}
        }
    }))
    sys.exit(0)

# default: allow silently
print("{}")
```

Settings:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/pre-bash-guard.py" }
      ]}
    ]
  }
}
```

**2.5 `UserPromptSubmit` — light prompt linter (no LLM call).**

Purpose: nudge yourself toward structured prompts (the 30% saving from SFEIR). Pure regex check; no model call, no extra token cost.

Path: `~/.claude/hooks/prompt-lint.py`
```python
#!/usr/bin/env python3
import json, sys
data = json.load(sys.stdin)
prompt = data.get("prompt", "")
hints = []
if len(prompt) > 1200 and "\n" not in prompt:
    hints.append("Long narrative prompt — consider structured fields (File:/Bug:/Action:) for ~30% token saving and better post-compact fidelity.")
if "everything" in prompt.lower() or "the whole" in prompt.lower():
    hints.append("Avoid 'everything'/'the whole repo' — name files/dirs explicitly to keep just-in-time loading working.")
if hints:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "[prompt-lint] " + " | ".join(hints)
        }
    }))
else:
    print("{}")
```

Settings:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/prompt-lint.py" }
      ]}
    ]
  }
}
```

**2.6 `Stop` — auto-suggest `/compact` at 60% utilisation.**

Purpose: enforce the proactive-compact discipline (MindStudio: compact at ~60% beats compact at 95% by a wide margin on coherence and speed).

Implementation note: Claude Code does not currently expose live token-utilisation to a hook directly, but it does write the transcript path. Read `$transcript_path`, count approximate tokens (chars/4), and emit a soft nudge.

Path: `~/.claude/hooks/stop-compact-nudge.py`
```python
#!/usr/bin/env python3
import json, os, sys
data = json.load(sys.stdin)
tp = data.get("transcript_path")
if not tp or not os.path.exists(tp):
    print("{}"); sys.exit(0)
size = os.path.getsize(tp)
# Rough heuristic: 1 token ≈ 4 chars; 200k window ≈ 800k chars
util = size / 800_000
if util > 0.60:
    msg = f"[ctx] transcript ~{int(util*100)}% of window. Run /compact with explicit preservation: '/compact Keep: open task, last decision, file list, current bug.' before continuing."
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": msg
        }
    }))
else:
    print("{}")
```

Settings:
```json
{
  "hooks": {
    "Stop": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/stop-compact-nudge.py" }
      ]}
    ]
  }
}
```

### Layer 3 — Harness: subagents, output-styles, plan mode

**3.1 Build three reusable subagents for high-token tasks.**

Each lives as a markdown file in `~/.claude/agents/`. The cost of a subagent: parent context grows only by the subagent's final summary (typically 1–2k tokens) regardless of how much work the subagent did (Anthropic context-engineering paper).

`~/.claude/agents/repo-explorer.md`:
```markdown
---
name: repo-explorer
description: Search and summarise unknown codebases. Use whenever the task starts with "where is", "find all uses of", "what does this repo do".
tools: [Read, Glob, Grep, Bash]
---
You are a repo-exploration subagent. Return ONLY:
1. A 5-bullet summary of what you found.
2. The exact file paths the parent should read next (max 5).
3. A one-line `[NOT FOUND]` note if applicable.
No code dumps. No reasoning narrative. The parent already has the plan; you supply targeted references.
```

`~/.claude/agents/log-triager.md`:
```markdown
---
name: log-triager
description: Read large log/test/build output files and return the relevant failure context only.
tools: [Read, Bash, Grep]
---
You are a log-triage subagent. Given a path or command output, return:
1. The first stack trace / error line verbatim.
2. The five lines of context before and after.
3. A one-line hypothesis.
Nothing else.
```

`~/.claude/agents/doc-summariser.md`:
```markdown
---
name: doc-summariser
description: Fetch and summarise long external docs (WebFetch / Read on markdown). Use instead of loading full doc pages into parent context.
tools: [WebFetch, Read]
---
You are a doc-summariser subagent. Return:
1. The 5 facts directly relevant to the parent's task.
2. The canonical URL.
3. One sentence on what the doc does NOT cover.
```

Trigger rule (in `~/.claude/CLAUDE.md`):
> "When a task requires reading >2 unknown files, >100 lines of logs, or any external URL, **delegate to the appropriate subagent** instead of doing it in the main thread. Subagent context is free; main context is the bottleneck."

**3.2 Add a token-lean output style.**

`~/.claude/output-styles/lean.md`:
```markdown
---
name: lean
description: Token-minimal output. Code + 1-line rationale. No preamble, no recap.
---
You operate under lean output:
- No "Great, let me…" preamble.
- No restating the user's request.
- No summary of what you just did unless explicitly asked.
- Code blocks first, prose second.
- One-line rationale per decision; bullet lists only when ≥3 items.
- Never paste full file contents back — diff or path-and-line-numbers only.
```

Activate per-project in `.claude/settings.local.json`:
```json
{ "outputStyle": "lean" }
```

Output tokens cost 5× input at the model layer and are the largest controllable leak in pure chat. This is the chat-side equivalent of `lean-by-default` for Claude Code.

**3.3 Default to Plan mode for exploration.**

CLAUDE.md instruction:
> "For any task whose verb is 'analyse', 'review', 'compare', 'investigate', 'design', or 'plan' — activate Plan mode (Shift+Tab) before reading files. Switch to execute only after the plan is approved or self-approved with rationale."

Measured saving on plan-shaped tasks: ~50% input tokens (SFEIR).

### Layer 4 — Telemetry: see the spend

**4.1 Wire ccusage into the statusline.**

`~/.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "bunx ccusage statusline"
  }
}
```

Shows session cost, today's cost, 5-hour block remaining, and burn rate live. You cannot optimise what you cannot see. (ccusage GitHub.)

**4.2 `SessionEnd` cost-log hook.**

Path: `~/.claude/hooks/session-end-log.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
cat > /dev/null  # consume stdin
LOG=~/.claude/session-costs.jsonl
{
  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"cost\":\"$(bunx ccusage daily --json 2>/dev/null | jq -c '.today // {}')\"}"
} >> "$LOG"
```

Settings:
```json
{
  "hooks": {
    "SessionEnd": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/session-end-log.sh" }
      ]}
    ]
  }
}
```

Builds a daily JSONL of spend, which feeds back into measurement (this is the loop that promotes the STRUCTURED claims here to MEASURED for Ewan's specific workload).

### Layer 5 — MCP & integration hygiene

5.1 **Audit installed MCP servers.** Every MCP server adds tool definitions to every prompt. Remove servers you don't actively use this week. List with `claude mcp list`; remove with `claude mcp remove <name>`.

5.2 **Prefer local CLIs over MCP wrappers** when both exist (e.g. `gh` CLI vs a GitHub MCP server). CLIs go through `Bash` (one tool entry), MCP servers add N tool entries.

5.3 **Headless mode for one-shots.** For deterministic batch work, run `claude -p "…" --output-format stream-json` instead of opening an interactive session. No CLAUDE.md, no statusline, no history — minimum prompt overhead.

---

## 2. Implementation order (Claude executes top-down)

1. Create `~/.claude/hooks/` and drop in all six hook scripts above. `chmod +x` each.
2. Merge the settings JSON snippets into `~/.claude/settings.json` (preserve existing keys; do not clobber).
3. Create `~/.claude/agents/` and add the three subagent markdown files.
4. Create `~/.claude/output-styles/lean.md`.
5. Install ccusage and wire the statusline (`bunx ccusage statusline` will lazy-install on first call).
6. Audit and reduce MCP servers; commit the reduction.
7. Sweep CLAUDE.md files; split anything > 3k tokens into per-subdirectory CLAUDE.md.
8. Ensure every project root has the standard `.gitignore` block from §1.3.
9. Start a fresh session; verify `/cost` shows lower per-turn deltas vs. baseline.
10. Run for 7 days. At end-of-week, read `~/.claude/session-costs.jsonl` and re-measure the deltas — promote claims from STRUCTURED to MEASURED for this specific workload.

---

## 3. Verification

After implementation, the following must be true; if not, the hook is mis-installed:

- `claude` shows the ccusage statusline at the bottom.
- A `find . -type f` command on the main thread is denied with the pre-bash-guard reason.
- A `Bash` command producing >6k chars output appears truncated in transcript with `[... N chars elided by post-tool-redact ...]`.
- A new session shows the `branch:` / `recent:` / `task:` preamble in the very first model turn (visible via `/debug` or transcript inspection).
- `/agents` lists `repo-explorer`, `log-triager`, `doc-summariser`.
- `/output-style lean` activates without error.
- `~/.claude/session-costs.jsonl` gains one entry per closed session.

---

## 4. What this plan deliberately does NOT do

- Does **not** use an API key. Max consumer login only.
- Does **not** proxy the network or rewrite traffic outside the harness.
- Does **not** auto-trigger `/compact` (Claude Code's compact must be user-initiated or auto by threshold; the Stop hook only nudges).
- Does **not** modify Claude's weights, system prompt at the platform level, or anything Anthropic owns.
- Does **not** introduce any new long-lived background process beyond what Claude Code already runs.

Everything is local, reversible (delete the hook file or remove the settings entry), and inside the published hook + harness surface.

---

## 5. Expected impact (STRUCTURED, to be re-measured)

Compounding the published deltas conservatively (assume diminishing returns; multiply by 0.7 floor):

| Layer | Headline saving | Conservative actual |
|---|---|---|
| 1.3 `.gitignore` | 25% of file-read tokens | ~15% on mixed workload |
| 2.3 Post-tool redact | 60–90% of bash/read tail-output | ~30% of total tool-result tokens |
| 2.4 Pre-bash guard | Blocks worst-case bombs | tail-event saving only, but high-variance |
| 3.1 Subagents | 40% of main context | ~25% blended (depends on adoption) |
| 3.2 Lean output style | ~30% of output tokens | ~20% |
| 3.3 Plan mode default | 50% on plan-shaped tasks | ~25% blended |
| 1.1 Compact at 0.85 | Fewer reactive compactions | quality, not token-count |

**Blended ceiling: ~50–60% reduction in tokens-per-useful-outcome on a typical mixed coding day**, consistent with SFEIR's headline 60% combined figure. Re-measure after 7 days; promote claims to MEASURED only with the JSONL evidence.

---

## 6. Open questions (parked, not blocking)

- Whether prompt-based hooks (`type: "prompt"`, Haiku-backed) are worth using for `Stop` / `SubagentStop` — costs Haiku tokens to save Sonnet/Opus tokens. Worth a one-week A/B once the deterministic layers are in.
- Whether to add a `PreToolUse` hook on the `Agent` tool to enforce the subagent-delegation rule mechanically rather than via CLAUDE.md prose.
- Long-term: a small Rust harness that watches `~/.claude/session-costs.jsonl` and emits a Vellum event when daily spend crosses a threshold — out of scope here, belongs in the Beast pipe, not in `.claude/`.

---

## 7. Attribution

Hooks reference, settings, output-styles, subagents: Anthropic Claude Code docs (URLs in front-matter).
Token-saving framework (just-in-time, compaction, structured notes, subagent offload): Anthropic, *Effective context engineering for AI agents*, 2025-09-29.
Measured deltas (plan mode, PreCompact, multi-session, gitignore, structured prompts): SFEIR Institute, *Context Management — Optimization Guide*.
Compact-at-60% practice: MindStudio, *How to Use the /compact Command*.
ccusage statusline + reports: Ryoppippi, github.com/ryoppippi/ccusage.

— STRUCTURED · synthesised from 5 primary + 3 secondary sources · valid 90d (re-check on Claude Code minor version bumps; hooks schema changed materially in 2026-06-16 release)

[CLOSURE] branch=PLAN | proxy=none | gates=none | inbox=claude-code-max__token-optimisation__hooks-and-harness-plan__v01__2026-06-24__perplexity.md | tier=STRUCTURED
