# Manufacturer File & Markdown Schemas

Four AI coding agents — their makers' **official, native conventions** for config files, instruction files, rules, skills, and memory. Each schema is copy-ready and sourced from primary documentation.

---

## 1. Claude Code (Anthropic)

**Source:** [Anthropic Claude Code Docs — How Claude Remembers Your Project](https://docs.anthropic.com/en/docs/claude-code/memory) (published 2026-06-18)

### Canonical config files & locations

| Scope | Path | Notes |
|---|---|---|
| Managed / org-wide | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) · `/etc/claude-code/CLAUDE.md` (Linux) · `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows) | Deployed via MDM/Ansible; cannot be excluded by users |
| User (all projects) | `~/.claude/CLAUDE.md` | Personal preferences; not shared |
| Project (team-shared) | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Committed to version control |
| Project-local (gitignored) | `./CLAUDE.local.md` | Add to `.gitignore`; personal overrides |
| Rules (path-scoped) | `.claude/rules/<topic>.md` | Per-file-glob rules; also `~/.claude/rules/` for user-level |

**Load order:** managed policy → user → project root → project subdir (directory-tree walk, deepest wins for specificity). Multiple files concatenate rather than override.

**Legacy support:** Importing `@AGENTS.md` from `CLAUDE.md` makes Claude read other agents' files too.

---

### Project structure

```
my-project/
├── CLAUDE.md                    # Main project instructions (OR .claude/CLAUDE.md)
├── CLAUDE.local.md              # Personal overrides — gitignored
└── .claude/
    ├── CLAUDE.md                # Alternative main location
    └── rules/
        ├── code-style.md        # Always-on or path-scoped rule
        ├── testing.md
        └── security.md
```

**Generate with:** `/init` inside Claude Code — auto-reads the codebase and proposes a starter `CLAUDE.md`.

---

### CLAUDE.md internal structure (template)

```markdown
# Project Name

## Build & Commands
- Install: `npm install`
- Dev server: `npm run dev`
- Test: `npm test`
- Build: `npm run build`

## Architecture
- `/src` — main application code
- `/tests` — test files

## Coding Standards
- Use TypeScript strict mode
- 2-space indentation
- Prefer named exports

## Workflows
- Create feature branches from `main`
- Run `npm test` before committing
```

No YAML frontmatter in `CLAUDE.md`. Plain markdown only. Import other files with `@path/to/file` (not inside backticks).

---

### .claude/rules/\<topic\>.md (path-scoped rule template)

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

YAML frontmatter `paths:` field uses glob patterns. Files without `paths:` are always-on for all files.

---

### Best practices (Anthropic's guidance)

- **Target under 200 lines** per `CLAUDE.md`; longer files reduce adherence.
- Write specific, verifiable rules: `"Use 2-space indentation"` not `"Format code properly"`.
- Use markdown headers and bullets; Claude scans structure like a reader does.
- Use HTML comments (`<!-- ... -->`) for maintainer notes — they are stripped before injection and don't use context tokens.
- Use `.claude/rules/` for large codebases; path-scoped rules load only when Claude works with matching files.
- Use `Skills` (`.claude/skills/`) for task-specific instructions that don't need to be in context all the time.
- Review and remove outdated rules periodically; conflicting rules may be resolved arbitrarily.

---

## 2. Cursor (Anysphere)

**Source:** [Cursor Docs — Rules](https://docs.cursor.com/en/context/rules) (domain: cursor.com, accessed 2026-06-22)

### Canonical config files & locations

| Scope | Path | Notes |
|---|---|---|
| Project rules | `.cursor/rules/<name>.mdc` | Version-controlled; scoped to codebase |
| Nested project rules | `<subdir>/.cursor/rules/<name>.mdc` | Auto-attaches when files in that subdirectory are referenced |
| User (global) rules | Cursor Settings → Rules (plain text field) | Always applied; no file on disk |
| Legacy (deprecated) | `.cursorrules` in project root | Still supported but use `.cursor/rules/` instead |

---

### Project structure

```
my-project/
└── .cursor/
    └── rules/
        ├── general.mdc            # Always-on rule
        ├── api-style.mdc          # Auto-attached to src/api/**
        ├── rpc-boilerplate.mdc    # Agent-requested (needs description)
        └── deploy-checklist.mdc   # Manual (invoked via @ruleName)
```

For a monorepo:

```
my-project/
├── .cursor/rules/          # Project-wide rules
├── backend/server/
│   └── .cursor/rules/      # Backend-specific rules
└── frontend/
    └── .cursor/rules/      # Frontend-specific rules
```

---

### .mdc file internal structure (template)

The file format is **MDC** (Markdown with metadata). All fields are controlled by a type dropdown in the Cursor UI, which writes the frontmatter.

```markdown
---
description: RPC Service boilerplate
globs:
alwaysApply: false
---

- Use the internal RPC pattern when defining services
- Always use snake_case for service names

@service-template.ts
```

**Frontmatter fields:**

| Field | Type | Used by rule type |
|---|---|---|
| `description` | string | `Agent Requested` — must be set; this is the trigger phrase the AI matches against |
| `globs` | glob pattern(s) | `Auto Attached` — rule loads when a matching file is referenced |
| `alwaysApply` | boolean | `Always` — set `true`; `Agent Requested` / `Manual` — set `false` |

**Rule types:**

| Type | When it loads | Required frontmatter |
|---|---|---|
| `Always` | Every context, always | `alwaysApply: true` |
| `Auto Attached` | When a file matching `globs` is open/referenced | `globs: "src/**/*.ts"` |
| `Agent Requested` | AI decides based on `description` semantic match | `description: ...` (required) |
| `Manual` | Only when user types `@ruleName` | none (no auto-load) |

Reference files within a rule with `@filename.ts`. Rules can reference other rules.

---

### Best practices (Anysphere's guidance)

- Keep rules **under 500 lines**; split large rules into multiple composable rules.
- Keep rules **focused, actionable, and scoped** — avoid vague guidance; write like clear internal docs.
- Provide concrete examples or referenced files (`@filename.ts`).
- For `Agent Requested` rules, write a precise `description` — it's the semantic trigger.
- For `Auto Attached` rules, ensure glob patterns match the files you intend.
- Reuse rules instead of repeating the same prompt in chat.
- Use `/Generate Cursor Rules` in chat to create rules from conversation history.

---

## 3. Devin (Cognition)

**Sources:**  
- [Devin Docs — AGENTS.md](https://docs.devin.ai/onboard-devin/agents-md) (accessed 2026-06-22)  
- [Devin Docs — Rules & AGENTS.md (CLI)](https://docs.devin.ai/cli/extensibility/rules) (accessed 2026-06-22)  
- [Devin Docs — Extensibility Overview](https://docs.devin.ai/cli/extensibility/index) (accessed 2026-06-22)  
- [Devin Docs — Skills](https://docs.devin.ai/cli/extensibility/skills/overview) (accessed 2026-06-22)  
- [Devin Docs — DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) (accessed 2026-06-22)

### Canonical config files & locations

| Scope | Path | Notes |
|---|---|---|
| Project rules (recommended) | `AGENTS.md` at project root | Always-on; auto-read before coding starts |
| Project rules (nested) | `AGENTS.md` in any subdirectory | Loaded lazily when agent accesses that directory |
| Global rules (all projects) | `~/.config/devin/AGENTS.md` (Linux/macOS) · `%APPDATA%\devin\AGENTS.md` (Windows) | Loaded at every session start |
| Alternate filenames | `AGENT.md` (singular) · `CLAUDE.md` (Claude Code compat.) | All treated identically to `AGENTS.md` |
| Project config | `.devin/config.json` | MCP, permissions; `.devin/config.local.json` for personal overrides (gitignored) |
| Skills | `.devin/skills/<name>/SKILL.md` | Project-scoped; committed to git |
| Global skills | `~/.config/devin/skills/<name>/SKILL.md` | All projects |
| Subagent profiles | `.devin/agents/<name>/AGENT.md` | Custom subagent definitions |
| Hooks | `.devin/hooks.v1.json` | Lifecycle hooks (Claude Code format compatible) |
| Wiki config | `.devin/wiki.json` | Steers DeepWiki auto-generation |

**Important:** `AGENTS.md` is always read and **cannot be disabled**.

---

### Project structure

```
my-project/
├── AGENTS.md                     # Project rules (always-on)
├── .devin/
│   ├── config.json               # MCP servers, permissions
│   ├── config.local.json         # Personal overrides — gitignored
│   ├── hooks.v1.json             # Lifecycle hooks
│   ├── wiki.json                 # DeepWiki configuration
│   ├── skills/
│   │   └── review/
│   │       └── SKILL.md          # Custom skill
│   └── agents/
│       └── reviewer/
│           └── AGENT.md          # Custom subagent profile
└── src/
```

---

### AGENTS.md internal structure (Cognition's example template)

```markdown
# AGENTS.md

## Setup Commands
- Install dependencies: `npm install`
- Start development server: `npm run dev`
- Run tests: `npm test`
- Build for production: `npm run build`

## Code Style
- Use TypeScript strict mode
- Prefer functional components in React
- Use ESLint and Prettier configurations
- Follow conventional commit format

## Testing Guidelines
- Write unit tests for all new functions
- Use Jest for testing framework
- Aim for >80% code coverage
- Run tests before committing

## Project Structure
- `/src` — Main application code
- `/tests` — Test files
- `/docs` — Documentation
- `/public` — Static assets

## Development Workflow
- Create feature branches from `main`
- Use pull requests for code review
- Squash commits before merging
- Update documentation for new features
```

No YAML frontmatter in `AGENTS.md`. Plain markdown. Rules are always-on by definition.

---

### .devin/skills/\<name\>/SKILL.md (template)

```markdown
---
name: review
description: Review code changes before committing
allowed-tools:
  - read
  - grep
  - glob
  - exec
---

Review the current git diff and provide feedback:

1. Run `git diff --staged` (or `git diff` if nothing is staged)
2. Check for:
   - Logic errors or bugs
   - Missing error handling
   - Security issues
   - Style inconsistencies
3. Summarize findings and suggest improvements
```

**Frontmatter fields:**

| Field | Purpose |
|---|---|
| `name` | Skill identifier; invoked as `/name` |
| `description` | What the skill does |
| `allowed-tools` | Restrict tool access within the skill |
| `triggers` | `user` (slash command) and/or `model` (autonomous); both enabled by default |

---

### .devin/wiki.json (DeepWiki config template)

```json
{
  "repo_notes": [
    {
      "content": "The /src folder contains the main app; /backend has the API layer.",
      "author": "Team Lead"
    }
  ],
  "pages": [
    {
      "title": "Architecture Overview",
      "purpose": "High-level overview of application structure",
      "parent": null
    }
  ]
}
```

---

### Best practices (Cognition's guidance)

- **Keep `AGENTS.md` concise** — long, verbose rules dilute agent attention.
- Be specific: `"Use pnpm"` beats `"use the right package manager"`.
- Include examples — show the pattern you want, not just describe it.
- Version-control `AGENTS.md` so the whole team benefits.
- **Prefer Skills over Rules** whenever possible — skills are only injected when relevant, reducing context and cost. Use rules mainly to reference which skills to invoke.
- Set `triggers: [user]` in a skill to prevent autonomous agent invocation.

---

## 4. Antigravity (Google)

**Sources:**  
- [Antigravity Docs — Rules & Workflows](https://antigravity.google/docs/rules-workflows) (official; accessed 2026-06-22)  
- [Google Codelabs — Authoring Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) (published 2026-06-18)  
- [Google Blog — Introducing Managed Agents in the Gemini API](https://blog.google/innovation-and-ai/technology/developers-tools/managed-agents-gemini-api/) (published 2026-05-19)  
- [Google AI Developers Forum — .agent vs .agents folder](https://discuss.ai.google.dev/t/new-folder-for-rules/126165) (2026-02-24; official Antigravity team response)  
- [GEMINI.md Guide — Antigravity AI Directory](https://antigravityai.directory/gemini-md-guide) (community reference, consistent with official docs)

### Canonical config files & locations

| Scope | Path | Notes |
|---|---|---|
| Global rules | `~/.gemini/GEMINI.md` (Linux/macOS) · `C:\Users\<Name>\.gemini\GEMINI.md` (Windows) | Applied across all workspaces; 6,000 char limit |
| Global workflows | `~/.gemini/antigravity/global_workflows/` | Available in all projects |
| Global skills | `~/.gemini/antigravity/skills/<name>/` | Available in all projects (IDE); also `~/.gemini/config/skills/` per Codelab |
| Workspace rules | `<workspace>/.agents/rules/` | **Current standard** (pluralized); `.agent/rules/` supported for backward compat |
| Workspace workflows | `<workspace>/.agents/workflows/` | Slash commands; `.agent/workflows/` also supported |
| Workspace skills | `<workspace>/.agents/skills/<name>/` | Per-project skills; `.agent/skills/` also supported |
| AGENTS.md (universal) | `AGENTS.md` at project root | Read as instructions in Managed Agent / Jules / API context |

**Directory note:** Antigravity migrated from `.agent/` (singular) to `.agents/` (plural) in v1.19.5+. Both work; `.agents/` is looked up first; use `.agents/` for new projects.

---

### Project structure

```
my-project/
├── AGENTS.md                         # Project instructions (universal standard)
├── GEMINI.md                         # Thin entry point for Antigravity (optional)
└── .agents/
    ├── rules/
    │   ├── code-style.md             # Always-on rule
    │   └── git-commit-rules.md       # Always-on rule
    ├── workflows/
    │   ├── devloop.md                # /devloop workflow
    │   └── review.md                 # /review workflow
    └── skills/
        └── postgres-query/
            ├── SKILL.md              # Skill definition
            ├── scripts/
            │   └── query.py
            └── references/
                └── schema.md
```

---

### ~/.gemini/GEMINI.md (global rules template)

```markdown
# GEMINI.md - Global Rules for Google Antigravity

## Coding Preferences
### Language Defaults
- Always use TypeScript over JavaScript
- Prefer functional programming patterns
- Use async/await instead of .then() chains

### Code Style
- Use descriptive variable names (isLoading, hasError)
- Keep functions under 30 lines when possible
- Add JSDoc comments for public functions

### Error Handling
- Always handle errors explicitly
- Use try/catch for async operations
- Never silently swallow errors

### Git & Commits
- Use conventional commit format (feat:, fix:, docs:, etc.)
- Keep commits atomic and focused

## Things to Avoid
- No console.log in production code
- No `any` types in TypeScript (use `unknown`)
- No hardcoded credentials or API keys
```

**Character limit: 6,000 characters.** Reference other files with `@filename` (relative, absolute, or repo-relative).

---

### .agents/rules/\<topic\>.md (workspace rule template)

```markdown
# Code Style Rules

- Use 2-space indentation for all TypeScript files
- Prefer named exports over default exports
- Always add error boundaries to async API routes
- Run `npm run lint` before every commit
```

Plain markdown. No mandatory frontmatter. Rules files are limited to **12,000 characters each**. Some community implementations use frontmatter with `trigger: always_on` and `globs:` (informal convention, not documented in official docs). Rules can reference files with `@path/to/file.md`.

---

### .agents/workflows/\<name\>.md (workflow template)

```markdown
# Deploy Workflow

Deploy the application to the staging environment.

## Steps

1. Run `npm run test` and verify all tests pass
2. Run `npm run build` and verify the build succeeds
3. Run `npm run deploy:staging`
4. Open the staging URL and verify the deployment

Call `/review` to review any changes before deploying.
```

Plain markdown with a title, description, and numbered steps. Invoked as `/workflow-name`. Workflows can call other workflows. 12,000 character limit.

---

### .agents/skills/\<name\>/SKILL.md (skill template)

```markdown
---
name: postgres-query
description: Use this skill when the user asks to query the database, check table schemas, or inspect data in the local PostgreSQL instance.
---

## Goal
Execute read-only SQL queries against the local PostgreSQL database.

## Instructions
1. Connect using the credentials in `.env`
2. Execute the requested query via the script: `scripts/query.py`
3. Format results as a Markdown table
4. Summarize key findings in plain language

## Constraints
- Do not run DELETE, UPDATE, or DROP queries
- Do not expose raw credentials in output
```

**Frontmatter fields:**

| Field | Required | Notes |
|---|---|---|
| `name` | Optional | Defaults to directory name; must be unique in scope; lowercase, hyphens |
| `description` | **Mandatory** | Semantic trigger phrase — the LLM matches user intent against this; be precise |

**Skill directory:**

```
postgres-query/
├── SKILL.md          # Required — brain of the skill
├── scripts/          # Optional — Python, Bash, or Node scripts
│   └── query.py
├── references/       # Optional — docs, templates, API specs
│   └── schema.md
└── assets/           # Optional — static assets
```

---

### AGENTS.md / GEMINI.md relationship (project-level)

When using both, the recommended pattern is to keep `AGENTS.md` as the single source of truth for project guidelines and use `GEMINI.md` as a thin pointer:

```markdown
<!-- GEMINI.md -->
Read and follow all instructions in ./AGENTS.md

Read and follow all rules defined in:
- .agents/rules/*
```

If `AGENTS.md` exists, it typically takes precedence over `GEMINI.md` per the community convention at [antigravity.md](https://antigravity.md).

---

### Best practices (Google's guidance)

- **GEMINI.md**: global preferences only; keep under 6,000 characters; move framework-specific rules to workspace level; include `"Things to Avoid"` sections.
- **Rules**: encode constraints, style, and conventions; keep files concise (12,000 char limit per file); use `@filename` for heavy reference content rather than embedding it inline.
- **Skills**: use a directory-based package; put instructions in `SKILL.md`, logic in `scripts/`, knowledge in `references/`; write precise `description` fields — they are the semantic trigger for skill activation; load skills on-demand rather than embedding all knowledge in rules.
- **Workflows**: define step-by-step sequences for repetitive processes; invoke via `/workflow-name`; can call other workflows (nested); ask the Agent to generate workflows from conversation history.
- Use **workspace scope** (`.agents/`) for team/project-specific configuration; use **global scope** (`~/.gemini/`) for personal preferences that span all projects.

---

## Cross-agent summary

| Feature | Claude Code | Cursor | Devin | Antigravity |
|---|---|---|---|---|
| Primary instruction file | `CLAUDE.md` | `.cursor/rules/*.mdc` | `AGENTS.md` | `GEMINI.md` (global) · `AGENTS.md` (project) |
| Project root file | `./CLAUDE.md` or `./.claude/CLAUDE.md` | — | `./AGENTS.md` | `./AGENTS.md` (+ `GEMINI.md` thin pointer) |
| Global user file | `~/.claude/CLAUDE.md` | Settings UI (plain text) | `~/.config/devin/AGENTS.md` | `~/.gemini/GEMINI.md` |
| Rules/skills directory | `.claude/rules/*.md` | `.cursor/rules/*.mdc` | `.devin/skills/<n>/SKILL.md` | `.agents/rules/*.md` · `.agents/skills/<n>/SKILL.md` |
| File format | Plain markdown | MDC (markdown + YAML frontmatter) | Plain markdown (AGENTS.md) · YAML frontmatter (SKILL.md) | Plain markdown (rules/workflows) · YAML frontmatter (SKILL.md) |
| Frontmatter support | `paths:` in `.claude/rules/` only | `description`, `globs`, `alwaysApply` | `name`, `description`, `allowed-tools`, `triggers` in SKILL.md | `name`, `description` in SKILL.md |
| Recommended length | <200 lines per file | <500 lines per rule | Keep small; prefer Skills | <6,000 chars (GEMINI.md); <12,000 chars (rules/workflows) |
| Init command | `/init` | `New Cursor Rule` command | — | Antigravity UI → Customizations |
