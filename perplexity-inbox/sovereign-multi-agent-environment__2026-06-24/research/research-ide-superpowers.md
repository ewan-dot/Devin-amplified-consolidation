# IDE Superpowers + CLI Isolation Research
**Target architecture:** Claude Code · Cursor · Antigravity (Google) · Devin — each in an isolated Apple Container VM cell on macOS Tahoe, connecting to a remote Beast server over Tailscale.

*Last updated: 2026-06-21*

---

## TASK A — Per-IDE Configuration & Superpower Reference

---

### 1. Claude Code

#### Config files & locations

| Scope | File / Directory | Purpose |
|---|---|---|
| Managed / org policy | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL: `/etc/claude-code/CLAUDE.md`; Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | IT/DevOps-controlled org-wide instructions (highest precedence, cannot be overridden by users) |
| User (global) | `~/.claude/CLAUDE.md` | Personal preferences applied to every project |
| User (global rules) | `~/.claude/rules/*.md` | Modular user-level rules applying to every project |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared project instructions; committed to VCS |
| Project (rules dir) | `./.claude/rules/*.md` | Modular project rules |
| Local project | `./CLAUDE.local.md` | Personal project-specific overrides; should be `.gitignore`d |
| Settings (user) | `~/.claude/settings.json` | Global hooks, permissions, auto-memory settings |
| Settings (project) | `.claude/settings.json` | Project-level settings; committable |
| Settings (local) | `.claude/settings.local.json` | Local project overrides; gitignored when Claude Code creates it |
| Settings (managed) | `managed-settings.json` + `managed-mcp.json` | Org-wide policy; delivered via MDM, registry, or server |
| MCP (user + local) | `~/.claude.json` | User-scope and local-scope MCP server configs; also stores OAuth sessions and per-project state |
| MCP (project) | `.mcp.json` (project root) | Project-scoped MCP servers; committed to VCS |
| Auto-memory | `~/.claude/projects/<project>/memory/` | `MEMORY.md` plus topic sub-files that Claude writes itself |

Precedence (highest → lowest for MCP): Local → Project → User → Plugin-provided → claude.ai connectors.  
Precedence for settings: Managed policy > Local > Project > User.

Sources: [Claude Code memory docs](https://docs.anthropic.com/en/docs/claude-code/memory) (2026-06-18), [Claude Code settings docs](https://docs.anthropic.com/en/docs/claude-code/settings) (2026-06-19), [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp) (2026-06-19).

#### Superpowers

| Superpower | What it does | What it needs |
|---|---|---|
| **MCP servers** | Connect to external tools (databases, GitHub, Slack, Jira, Drive). Three transports: `stdio` (local process), `http`/`streamable-http` (remote), `ws` (WebSocket). | Network for remote servers; local Node/Python/binary for stdio servers |
| **Hooks** | 30+ lifecycle events (`PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `FileChanged`, `WorktreeCreate`, etc.). Can run shell commands, POST to HTTP, call MCP tools, spawn prompt/agent verifiers, write `CLAUDE_ENV_FILE`. | Shell access for `command` hooks; network for `http` hooks |
| **Subagents / agent teams** | Spawn parallel Claude Code agents for concurrent subtasks; `background: true` frontmatter runs an agent permanently concurrent; `SubagentStart`/`SubagentStop` hooks observe them. | Network to Anthropic API |
| **Routines / Schedules** | Run on Anthropic-managed infra triggered by time, API calls, or GitHub events — keeps running when your machine is off. | Network; Anthropic subscription |
| **Skills & plugins** | Reusable slash-command definitions bundled with their own hooks and MCP servers in `plugin.json`. | Filesystem |
| **Auto-memory** | Claude writes its own notes (`~/.claude/projects/<project>/memory/`) and injects a `MEMORY.md` summary each session. Requires v2.1.59+. | Filesystem (writable home) |
| **CI/headless mode** | `claude -p "…"` non-interactive; pipe logs; GitHub Actions / GitLab CI/CD integration. | Network |
| **Worktree management** | `WorktreeCreate`/`WorktreeRemove` hooks; subagents can operate in isolated git worktrees. | Filesystem + git |
| **Remote Control / Teleport** | Continue a CLI session from the web or iOS app; hand off to Desktop for visual diff review. | Network; claude.ai subscription for Teleport |

Sources: [Claude Code hooks docs](https://docs.anthropic.com/en/docs/claude-code/hooks) (2026-06-16), [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview) (2026-06-15).

#### Container / remote / headless behaviour

| Feature | Status inside Linux container via SSH |
|---|---|
| Core CLI operation (`claude -p`) | **Fully supported.** Runs headless in CI and over SSH. |
| Authentication in SSH session | Supported via SSH port forwarding (`ssh -L 8080:...`) or by pre-copying `~/.config/claude-code/auth.json`. `--force-manual-token-flow` also available. ([GitHub issue #7100](https://github.com/anthropics/claude-code/issues/7100), 2025-09-04) |
| CLAUDE.md, hooks, MCP (stdio) | Fully functional — all live on the container filesystem. |
| MCP (remote/HTTP) | Works as long as the container has outbound network access or Tailscale connectivity to the MCP server. |
| Routines (cloud-scheduled) | Run on Anthropic infra; the container does not need to be running. |
| Auto-memory | Fully functional — writes to `~/.claude/projects/…` inside the container. |
| Desktop visual features (diff review, `/desktop` hand-off) | **Requires the GUI desktop app on the host machine**, not available inside a headless container. |
| Teleport (`claude --teleport`) | Requires a claude.ai subscription and outbound internet. |
| Subagents | Fully functional in headless/CLI mode. |

**Nothing functionally important breaks** in a headless Linux container. The only losses are the GUI desktop app and the `--teleport` shortcut (which needs internet anyway).

---

### 2. Cursor

#### Config files & locations

| Scope | File / Directory | Purpose |
|---|---|---|
| Legacy global rules | (Cursor Settings → Rules → User) | Applied to every project on this machine; stored internally |
| Legacy project rules | `.cursorrules` (project root) | Single-file legacy format; still read but superseded |
| Modern project rules | `.cursor/rules/*.mdc` | YAML-frontmatter Markdown rules with activation conditions |
| Cross-IDE rules | `AGENTS.md` (project root) | Universal agent instruction file read by Cursor and other tools |
| MCP (global) | `~/.cursor/mcp.json` | Global MCP server config for all projects |
| MCP (project) | `.cursor/mcp.json` (project root) | Project-scoped MCP servers; committable to VCS |

**Rule frontmatter keys:** `description` (one-line label), `globs` (file-pattern activation), `alwaysApply` (boolean — inject regardless of open files). Activation hierarchy: `alwaysApply: true` rules always load; glob-matched rules load when matching files are in context; agent-requested rules load at agent's discretion; manual rules only via `@ruleName`.

**MCP config interpolation:** `${env:NAME}`, `${userHome}`, `${workspaceFolder}`, `${workspaceFolderBasename}` are supported in `command`, `args`, `env`, `url`, and `headers` fields.

Sources: [Cursor MCP reference](https://cursor.com/docs/mcp.md), [Cursor 2026 guide (DeployHQ)](https://www.deployhq.com/guides/cursor) (2026-04-30), [MCP Playground mcp.json guide](https://mcpplaygroundonline.com/blog/cursor-mcp-setup-guide) (2026-01-12).

#### Superpowers

| Superpower | What it does | What it needs |
|---|---|---|
| **Agent mode** | Multi-step autonomous coding; can run arbitrary shell commands and tools. | IDE running; optional MCP servers |
| **MCP servers** | Stdio (local process) and SSE/HTTP (remote URL) transports; GUI server manager + `mcp.json` files. | Outbound network for remote; local runtime for stdio |
| **Background / Cloud Agents** | Clone repo, complete tasks, open PRs while you work locally. Triggered by schedule, GitHub, Slack, Linear, or webhook events. Agents test changes in their own cloud sandbox, produce video/screenshot demos. | **GitHub connection required; usage-based pricing must be enabled; Privacy Mode must be off.** Runs on Cursor's cloud infrastructure. |
| **Skills** | Reusable agent actions invoked as slash commands. | Filesystem |
| **Memory tool** | Cloud agents can access a memory tool to learn from past runs and improve with repetition. | Cloud agent infrastructure |
| **Remote SSH** | Connect to a remote Linux machine and use Cursor's AI against that machine's files. | SSH access; remote machine must reach Cursor's CDN (`windsurf-stable.codeiumdata.com`) on port 443 |
| **Dev Containers** | Attach to a local or remote Docker container as the working environment. | Docker on local or remote host; `devcontainer.json` |

Sources: [Cursor Cloud Agents page](https://cursor.com/cloud) (2026-02-26), [Mastering Cursor IDE guide](https://authorityaitools.com/cookbooks/mastering-cursor-ide) (2026-02-25).

#### Container / remote / headless behaviour

| Feature | Status inside Linux container via SSH |
|---|---|
| SSH Remote mode | **Supported** via Remote-SSH extension (Cursor's own implementation). Linux-only remote hosts. Requires outbound access to `windsurf-stable.codeiumdata.com:443` for REH binary download. |
| AI agent / rules / MCP (stdio) | Fully functional when connected via Remote-SSH. |
| MCP (remote/HTTP) | Works if the container has outbound network access. |
| Background/Cloud Agents | **Cloud-side feature** — they run on Cursor's infrastructure, not on your container. They require GitHub and usage-based pricing. Cloud agents control their own machines; your container is the code source, not the execution environment. |
| Privacy Mode | Incompatible with Background Agents. |
| Remote SSH AI streaming | Known to throttle to ~1–2 kB/s for large plan-mode outputs over SSH (Cursor forum, 2026-01-01). Connection over Tailscale may help. |
| Dev Container (local Docker) | Local only; not directly applicable to a per-agent Apple Container VM. |
| Headless / no-GUI | Cursor is an Electron/VS Code based GUI app. **It cannot run fully headless.** The Remote-SSH model requires Cursor Desktop on the Mac host, connecting to a Remote Extension Host on the Linux VM. |

**Key limitation:** Cursor requires its GUI Desktop app on the macOS host. The Linux container is accessed *from* Cursor via Remote-SSH. You cannot run Cursor itself inside the container; you run the Remote Extension Host there.

---

### 3. Antigravity (Google) — `agy` CLI

> Antigravity CLI (`agy`) is the direct successor to Gemini CLI, which was sunset for individual-tier accounts on 2026-06-18. It is Google's terminal-first coding agent, powered by Gemini models and optionally Claude/GPT.

Sources: [AI Builder Club Antigravity CLI guide](https://www.aibuilderclub.com/blog/antigravity-cli-guide) (2026-06-21), [Agentpedia deep dive](https://agentpedia.codes/blog/antigravity-cli-deep-dive) (2026-05-20), [O'Reilly live events syllabus](https://www.oreilly.com/live-events/agentic-coding-with-google-antigravity-cli/0642572224547/0642572350789/), [O-mega.ai 2026 guide](https://o-mega.ai/articles/google-antigravity-2-0-the-complete-2026-guide) (2026-05-20).

#### Config files & locations

| Scope | File / Directory | Purpose |
|---|---|---|
| Global CLI settings | `~/.gemini/antigravity-cli/settings.json` | Model, theme, sandbox toggle (`enableTerminalSandbox`), permissions |
| Global context file | `~/.gemini/GEMINI.md` | Always-on instructions for every workspace |
| Project context | `GEMINI.md` or `AGENTS.md` at project root | Both are read; `AGENTS.md` is the modern cross-tool standard |
| Project rules dir | `.agents/rules/` (multiple Markdown files) | Structured rules loaded at session start; backward-compatible with `GEMINI.md` |
| Workspace skills | `.agents/skills/*.md` | Slash commands for this workspace |
| Global skills | `~/.gemini/antigravity-cli/skills/` | Cross-project slash commands |
| MCP (workspace) | `.agents/mcp_config.json` | Workspace-scoped MCP servers |
| MCP (global) | `~/.gemini/antigravity-cli/mcp_config.json` | Global MCP server config; uses `serverUrl` field (not `url`) for remote servers |
| Plugins (workspace) | `.agents/plugins/` | Local plugin storage |
| Plugins (global) | `~/.gemini/antigravity-cli/plugins/<plugin_name>/` | Global plugin staging |
| Custom model config | `~/.config/antigravity/config.toml` | Model identifier, `base_url`, API key env var name |
| Keybindings | `~/.gemini/antigravity-cli/keybindings.json` | Custom terminal shortcuts |

Context file loading: global `~/.gemini/GEMINI.md` → project root → ancestor directories → subdirectories (lazy, on file access). All matched files are concatenated and prepended to every prompt. The `contextFileName` setting in `settings.json` can change the filename to `AGENTS.md`, an array of filenames, etc.

**Important rename from Gemini CLI:** MCP config is now in a dedicated `mcp_config.json` (was inline in `settings.json`). Remote server entries use `serverUrl` instead of `url`.

#### Superpowers

| Superpower | What it does | What it needs |
|---|---|---|
| **Agent Skills** | Reusable slash commands defined as `.md` files at `.agents/skills/` (workspace) or `~/.gemini/antigravity-cli/skills/` (global). | Filesystem |
| **Plugins** | Packages of skills + hooks + MCP servers (migrated from Gemini CLI extensions). Import with `agy plugin import gemini`. | Filesystem |
| **MCP servers** | Both local stdio and remote HTTP. Configured in `mcp_config.json`. | Outbound network for remote |
| **JSON Hooks** | Lifecycle interceptors (before tool call, after file edit, on session start). Workspace hooks override global hooks. | Shell/runtime |
| **Dynamic subagents** | Orchestrator spawns specialized background subagents in parallel without user-defined config — it derives the decomposition from your goal. | Network to Gemini API |
| **Scheduled tasks** | Cron-style triggers for recurring agent runs (nightly tests, daily reviews, etc.). | Cloud infra or local daemon |
| **Terminal sandboxing** | `nsjail` on Linux, `sandbox-exec` (Apple Seatbelt) on macOS — kernel-level isolation of agent tool calls. | Linux kernel (nsjail) or macOS (sandbox-exec) |
| **Built-in Chromium browser** | Agents can spin up Chromium for visual verification. | Desktop app (GUI) only; **not available in headless CLI** |
| **Voice commands** | Native voice input via Gemini Audio models. | Desktop app (GUI) only |
| **SDK self-hosting** | Programmatic access to the agent harness; deploy on your own infrastructure. | Network |

#### Container / remote / headless behaviour

| Feature | Status inside Linux container via SSH |
|---|---|
| Core `agy` CLI operation | **Fully supported headless.** Designed explicitly for SSH workflows. |
| Context files, skills, hooks, MCP (stdio) | Fully functional — all config lives on the container filesystem. |
| MCP (remote HTTP) | Works if container has outbound network to the MCP endpoint. |
| Terminal sandboxing | `nsjail` on Linux works inside the container (needs appropriate privileges); `sandbox-exec` is macOS-only and not applicable. |
| Dynamic subagents | Fully functional in CLI mode — spawned inline, not as separate OS processes. |
| Scheduled tasks | Depend on the local daemon or cron setup inside the container. |
| Desktop app features (Chromium browser, voice, visual verification, multi-agent hub GUI) | **GUI-only — unavailable in headless container.** Managed Agents in desktop run in a Google-hosted sandbox, not your container. |
| Settings sync | Desktop app (Antigravity 2.0) syncs permissions/models bidirectionally with CLI — but only when Desktop app is also running on a reachable host. |

**All core superpowers (skills, hooks, MCP, subagents, sandboxing) work headless inside a Linux VM.** Only visual/voice features require the Desktop app.

---

### 4. Devin

> Devin is a cloud-first AI software engineer from Cognition. It has two distinct surfaces: the cloud **Web App + API** (the original product) and the newer **Devin CLI** (local/remote terminal agent). They share some config but have different feature sets. This section covers both, with emphasis on what runs locally in a VM cell.

Sources: [Devin CLI extensibility overview](https://docs.devin.ai/cli/extensibility/index), [Devin CLI configuration](https://docs.devin.ai/cli/extensibility/configuration), [Devin CLI rules](https://docs.devin.ai/cli/extensibility/rules), [Devin Desktop FAQ](https://docs.devin.ai/desktop/devin-desktop-faq), [Devin playbooks](https://docs.devin.ai/product-guides/using-playbooks), [Devin release notes 2026](https://docs.devin.ai/release-notes/2026).

#### Config files & locations (Devin CLI — local agent)

| Scope | File / Directory | Purpose |
|---|---|---|
| User config | `~/.config/devin/config.json` | Global defaults: model, theme, permissions, sandbox settings. Windows: `%APPDATA%\devin\config.json` |
| User global rules | `~/.config/devin/AGENTS.md` | Always-on rules for every project |
| Project config | `.devin/config.json` | MCP servers, permissions, model overrides; committed to VCS |
| Local project overrides | `.devin/config.local.json` | Secrets, personal preference overrides; gitignored automatically |
| Project rules | `AGENTS.md` (project root) | Recommended always-on rules; also `AGENT.md` and `CLAUDE.md` are read |
| Subdirectory rules | `AGENTS.md` in any subdirectory | Lazily loaded when agent accesses files in that directory |
| Hooks | `.devin/hooks.v1.json` | Lifecycle hooks (Claude Code format-compatible) |
| Skills | `.devin/skills/<name>/SKILL.md` | Custom slash commands |
| Custom subagents | `.devin/agents/<name>/AGENT.md` | Subagent profiles |

Devin CLI also **automatically imports** configuration from other tools by default:

| Import source | What is read |
|---|---|
| Claude Code | `CLAUDE.md`, `~/.claude/CLAUDE.md`, `.claude/` directory (commands, subagents, hooks) |
| Cursor | `.cursor/rules/*.md`, `.cursor/rules/*.mdc`, `.cursor/mcp.json` |
| Windsurf | `.windsurf/rules/*.md`, `.windsurf/global_rules.md` |
| OpenCode | `opencode.json` |
| Zed | `.zed/settings.json` |

Disable selectively via `"read_config_from": { "cursor": false }` in `config.json`.

#### Config files & locations (Devin Cloud / Web App)

| Item | Details |
|---|---|
| **Playbooks** | Stored in Devin's cloud at `app.devin.ai`. Markdown documents describing procedures and specifications. Attach to a session via the UI, by macro (`!data-tutorial`), or by attaching a `<filename>.devin.md` file. Can have a **structured output schema** (JSON) so Devin returns results in a defined format. Can specify agent mode (Fast or Normal). |
| **Knowledge** | Enterprise knowledge base at `app.devin.ai/settings/snapshots`. Injected into Devin's context across sessions. Managed at org level. |
| **Declarative blueprints** | Environment configuration (replacing classic "machine configuration" as of 2026-06-30). |

#### Superpowers

| Superpower | What it does | What it needs |
|---|---|---|
| **MCP servers** | Full MCP support in CLI (stdio and HTTP). Configured in `.devin/config.json` or `~/.config/devin/config.json`. | Local runtime / outbound network |
| **Hooks** | `.devin/hooks.v1.json` lifecycle hooks, Claude Code-format compatible. | Shell access |
| **Skills** | Reusable slash commands from `.devin/skills/`. | Filesystem |
| **Custom subagents** | Agent profiles from `.devin/agents/`. | Filesystem |
| **Cross-tool config import** | Reads Claude Code, Cursor, Windsurf rules and MCP configs natively. | Filesystem |
| **Headless / SSH auth** | `--force-manual-token-flow` flag for browser-less login. `COGNITION_API_KEY` env var for CI/CD. | API key / OAuth |
| **`/handoff`** | Escalate a CLI session to cloud Devin for more powerful parallel execution. | Network; Cognition account |
| **Cloud Web App + API** | REST API for session creation, playbook-driven automation, GitHub PR reviews. | Internet; Cognition account |
| **Playbooks** | Cloud-side templates defining task procedures; structured JSON output; batch sessions. | Cloud app access |
| **Batch sessions** | Launch multiple Devin sessions in parallel from one prompt or CSV. | Cloud app access |
| **Embedded IDE + browser** | Real-time IDE and browser in cloud Devin sessions. | Cloud app GUI |

#### Container / remote / headless behaviour

| Feature | Status inside Linux container via SSH |
|---|---|
| Devin CLI core operation | **Fully supported.** Install via `curl -fsSL https://cli.devin.ai/install.sh | bash`. |
| Authentication (headless) | `--force-manual-token-flow` skips browser OAuth. `COGNITION_API_KEY` env var for CI. |
| Config files, rules, hooks, skills, MCP (stdio) | Fully functional — all live on the container filesystem. |
| MCP (remote HTTP) | Works if the container has outbound network to the MCP endpoint or via Tailscale. |
| Cross-tool config import (Cursor, Claude, Windsurf) | Reads those tools' config files from the same container filesystem — useful if multiple configs are co-located. |
| `/handoff` to cloud Devin | Requires outbound internet to `api.devin.ai`. |
| Cloud playbooks / knowledge base | Requires internet; executed in Cognition's cloud infra, not your container. |
| Embedded IDE, browser (cloud) | Cloud-side GUI only; not available in headless container. |
| Remote SSH into Linux (Devin Desktop) | Devin Desktop (Windsurf-derived) has its own Remote-SSH implementation. Remote machine must reach `windsurf-stable.codeiumdata.com:443`. |

---

### Per-IDE Summary Table

| Dimension | Claude Code | Cursor | Antigravity CLI | Devin CLI |
|---|---|---|---|---|
| **Primary config file** | `CLAUDE.md` (hierarchical) | `.cursor/rules/*.mdc` + `AGENTS.md` | `GEMINI.md` / `AGENTS.md` + `.agents/rules/` | `AGENTS.md` + `.devin/config.json` |
| **Global scope** | `~/.claude/CLAUDE.md` | Cursor Settings → User Rules | `~/.gemini/GEMINI.md` | `~/.config/devin/AGENTS.md` |
| **Project scope** | `./CLAUDE.md` / `.claude/CLAUDE.md` / `.claude/rules/*.md` | `.cursor/rules/*.mdc` / `.cursorrules` | `AGENTS.md` at root + `.agents/rules/*.md` | `AGENTS.md` at root + `.devin/config.json` |
| **MCP config** | `.mcp.json` (project), `~/.claude.json` (user) | `.cursor/mcp.json` (project), `~/.cursor/mcp.json` (global) | `.agents/mcp_config.json` (workspace), `~/.gemini/antigravity-cli/mcp_config.json` (global) | `.devin/config.json` (project), `~/.config/devin/config.json` (global) |
| **Hooks** | `.claude/settings.json` → `hooks` key; 30+ events | Not a first-class hooks system (relies on MCP + rules) | `.agents/hooks.json` (JSON lifecycle interceptors) | `.devin/hooks.v1.json` (Claude Code-compatible format) |
| **Background agents** | Via subagent API + `background: true` frontmatter; Routines run on Anthropic infra | Cloud Agents on Cursor infra (needs GitHub + paid plan) | Dynamic subagents orchestrated inline | `/handoff` to cloud Devin; batch sessions in cloud app |
| **Headless / CLI** | ✅ Full support, `claude -p` | ⚠️ GUI app required on host; Linux VM only via Remote-SSH from Desktop | ✅ Full CLI headless support (`agy`) | ✅ Full CLI support |
| **SSH remote** | ✅ Auth via port forwarding or pre-copied token | ✅ Remote-SSH extension (Cursor Desktop → Linux REH) | ✅ Explicitly designed for SSH workflows | ✅ `--force-manual-token-flow`; env var auth |
| **Sandbox / isolation** | Hooks + MCP permission model; worktrees | Dev containers; cloud agents have own sandbox | `nsjail` (Linux) / `sandbox-exec` (macOS) | Permission allow/deny lists in `config.json` |
| **Features lost in headless container** | GUI Desktop app visual diff; Teleport | Entire IDE GUI (it *is* a GUI app) | Chromium browser, voice commands, multi-agent hub GUI | Cloud embedded IDE/browser; cloud playbooks UI |
| **Cross-tool compat** | Reads `.cursorrules`, `.devin/rules/`, `.windsurfrules` via `/init` | Reads `AGENTS.md` as fallback | Reads `GEMINI.md` + `AGENTS.md` + legacy Gemini CLI skills | Auto-imports Claude Code, Cursor, Windsurf, Zed configs |

---

## TASK B — CLI Isolation: Can a CLI Break Out of Its VM Cell?

### Apple Container / VM Architecture (macOS Tahoe)

Apple's `container` tool (v1.0.0, released June 2026) runs **one lightweight VM per container**, built on `Virtualization.framework` (hardware hypervisor on Apple Silicon). Each VM gets:
- Its own Linux kernel (Kata Containers kernel, downloaded at setup)
- Its own network interface (dedicated IP via `vmnet`)
- Its own root filesystem
- A custom Swift `vminitd` init process as the sole binary, communicating via RPC

This is VM-level isolation, not shared-kernel container isolation. The attack surface is reduced by the absence of core utilities, libc, and dynamic libraries in the base VM image.

Sources: [Apple container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md) (2025-05-30), [CybersecurityNews Apple Containerization](https://cybersecuritynews.com/apples-containerization-feature-macos/) (2025-07-29), [DEV.to Apple container v1.0.0](https://dev.to/trknhr/apples-container-just-hit-v100-mid) (2026-06-10), [Devclass Apple Containerization](https://www.devclass.com/containers/2025/06/11/apples-containerization-will-matter-to-developers-but-podman-devs-complain-of-unfixed-issues/101152) (2025-06-11).

---

### What a CLI *Can* and *Cannot* Reach Across the VM Boundary

#### What is **isolated** (cannot cross by default)

| Boundary | Why it holds |
|---|---|
| Host filesystem | No bind mount = no access. The VM sees only its own ext4 image unless you explicitly pass `-v host_path:container_path`. |
| Host loopback (`127.0.0.1`) | Traffic to `localhost` inside the VM stays on the VM's loopback interface; it does not reach host services. (Confirmed in [Apple container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md).) |
| Inter-container network (macOS 26) | Each container attaches to a separate `vmnet` virtual network. `container network create foo` makes an isolated network; containers on different networks have no connectivity. |
| Host Unix sockets (Docker socket, SSH agent) | Not exposed unless explicitly mounted. |
| Other containers' filesystems | Each VM has its own independent filesystem image. |
| Host kernel | Full hypervisor boundary via `Virtualization.framework`; containers do not share the macOS kernel. |

#### What *can* cross the VM boundary (default and misconfiguration risks)

| Vector | Risk |
|---|---|
| **Explicit bind mounts (`-v`)** | Any host directory mounted into the VM is directly accessible to all processes inside, including the CLI agent. If you mount a broad path (e.g., `~/projects`) the agent can read/write the entire tree. Mount only the minimal required subtree, read-only where possible. |
| **Port publishing (`-p`)** | `container run -p 127.0.0.1:8080:8080` bridges host loopback to the VM. A CLI process inside can accept connections from the host. Inbound-only risk, but a malicious agent could set up a reverse proxy. |
| **Outbound network to shared services** | If all VMs share Tailscale credentials and can reach the Beast server, one compromised cell can reach whatever the Beast server exposes. Scope each cell's Tailscale ACLs. |
| **MCP servers on the host** | If an MCP server runs as a process on the macOS host and binds to `0.0.0.0` or to the `vmnet` bridge IP, it is reachable from all containers on the same virtual network. **This is the primary cross-cell bridge risk.** (See below.) |
| **Shared secret stores** | If an API key or Tailscale auth key is embedded in a shared volume or environment variable available to multiple containers, one cell's agent can use another cell's credentials. |
| **SSH agent forwarding** | `container run --ssh-agent` forwards the macOS SSH agent socket into the VM. An agent inside can use any key in your Mac's SSH agent, including keys for other machines. |
| **macOS 15 limitation** | On macOS 15 (Sequoia), `container network` commands do not exist and all containers attach to the same default `vmnet` bridge, making inter-container network isolation unavailable. macOS 26 (Tahoe) is required for per-network isolation. |

---

### MCP Servers on the Host: The Cross-Cell Bridge Problem

If an MCP server (e.g., a GitHub MCP, filesystem MCP, or database MCP) runs as a `stdio` process **inside a specific cell**, it is completely contained — it can only be reached by the agent in that cell, and it can only access whatever that VM's filesystem exposes.

If an MCP server runs as an **HTTP/SSE server on the macOS host** (or on the Beast server), the isolation picture changes dramatically:

| MCP placement | Isolation status |
|---|---|
| `stdio` inside cell | ✅ Isolated — agent spawns it, IPC never leaves the VM |
| HTTP server inside the cell, bound to `127.0.0.1` in that VM | ✅ Isolated — reachable only within the VM |
| HTTP server on the **macOS host**, bound to `0.0.0.0` or the vmnet bridge IP | ❌ **All cells on the same vmnet can reach it.** This defeats per-cell isolation. |
| HTTP server on the **Beast server**, reachable via Tailscale | ⚠️ Reachable by any cell that has Tailscale access to Beast. Isolation depends entirely on Tailscale ACLs. |
| HTTP server on **host**, bound to `127.0.0.1` only | ✅ Cannot reach host loopback from inside VM (no path by default) |

The [Trend Micro MCP container security report](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/using-containers-to-secure-your-mcp-infrastructure) (2025-09-17) explicitly identifies MCP servers bound to `0.0.0.0` as the top isolation-defeating misconfiguration.

---

### CLI Breakout: What a Rogue Agent Can and Cannot Do

#### Cannot do (inside a properly configured per-agent VM cell)

- Read or write host filesystem (no bind mount)
- Reach host loopback services
- Communicate with agents in other cells over the network (with per-network isolation on macOS 26)
- Escape to the host via a container escape (Apple VM boundary requires hypervisor-level exploit, not a namespace escape)
- Access the macOS keychain

#### Can do (within the VM, and sometimes across)

- Read/write any **bind-mounted** directories
- Reach any service on the **vmnet bridge** (host-facing gateway, typically `192.168.64.1`)
- Contact any host-bound MCP server that is **not** restricted to `127.0.0.1`
- Use any **forwarded SSH agent keys** to reach external systems
- Contact any service reachable over **Tailscale** from within the cell (Beast server, other nodes on the tailnet)
- Perform **prompt injection via MCP** if a shared MCP server is exploited — one cell's tool call could poison context in another cell if both share the same HTTP MCP endpoint (this is a logical cross-cell channel, not a VM escape)

---

### Best Practices for Keeping CLI-Driven Agents Inside Their Membrane

#### VM / container level

1. **Run macOS 26 (Tahoe) for full network isolation.** macOS 15 lacks `container network` commands and puts all containers on one bridge.
2. **Create a dedicated `container network` per agent cell.** `container network create agent-claude`, `container network create agent-cursor`, etc. Containers on separate networks have zero L3 connectivity.
3. **Bind-mount only the minimum required path, read-only unless the agent must write.** Never mount `~`, `/`, or any directory an agent doesn't strictly need.
4. **Never pass `--ssh-agent` unless the specific cell needs SSH key access to specific hosts.** Scope SSH key forwarding per cell.
5. **Do not use `--network=host`.** This collapses the entire network boundary.

#### MCP server placement

6. **Run each cell's MCP servers inside that cell as `stdio` processes** (not as separate HTTP daemons on the host). This is the strongest isolation model.
7. **If an HTTP MCP server must run on the host or Beast**, bind it to `127.0.0.1` (not `0.0.0.0`), and use Tailscale ACLs to allow only the specific cell's Tailscale node IP to reach it.
8. **Never share a single MCP server endpoint between multiple agent cells** unless the MCP server has per-client authentication and access controls. A shared MCP server is a logical cross-cell channel.
9. **Prefer `stdio` over HTTP/SSE** for all local MCP servers to avoid any listening socket.

#### Tailscale / network

10. **Use Tailscale ACL policies** to restrict which cell can reach which service on Beast. Each cell should have a distinct Tailscale node or tag with minimal ACL grants.
11. **Scope outbound egress inside each VM** using the `container network` settings or `iptables` inside the VM to allow only the Tailscale interface and known endpoints.

#### Secrets and credentials

12. **Give each cell its own API keys** (Anthropic API key, GitHub tokens, etc.). Never share a key across cells via a common bind mount or environment variable.
13. **Prefer short-lived tokens** (OIDC/STS) over long-lived static keys inside agent cells.
14. **Do not hard-code secrets in CLAUDE.md, AGENTS.md, or any config file** that might be read by the agent and included in its context (risk of exfiltration via prompt).

---

### CLI Partition Verdict

**A CLI inside a properly configured Apple Container VM cell cannot break out of the VM boundary by itself.** The hypervisor boundary enforced by `Virtualization.framework` prevents namespace-level escapes possible in shared-kernel containers. However:

- **Bind mounts, port publishing, and SSH agent forwarding are voluntary holes** — misconfiguring any of these lets the agent touch host or cross-cell resources.
- **The dominant cross-cell risk is not a VM escape; it is a misconfigured MCP server on the host or Beast that all cells can reach.** This creates a logical shared-service channel that defeats the purpose of per-agent cells even without any exploit.
- **Shared Tailscale credentials or overly broad ACLs** allow one agent to impersonate another on the Beast server.
- **macOS 15 (Sequoia) lacks network isolation between containers.** You need macOS 26 (Tahoe) for the `container network` isolation feature.

The partition holds if you: run macOS 26, create one `container network` per cell, keep MCP servers inside their cell as stdio processes, scope Tailscale ACLs per cell, and never share credentials across cells.

---

## Sources

| Source | URL | Date |
|---|---|---|
| Claude Code memory docs | https://docs.anthropic.com/en/docs/claude-code/memory | 2026-06-18 |
| Claude Code settings docs | https://docs.anthropic.com/en/docs/claude-code/settings | 2026-06-19 |
| Claude Code MCP docs | https://docs.anthropic.com/en/docs/claude-code/mcp | 2026-06-19 |
| Claude Code hooks docs | https://docs.anthropic.com/en/docs/claude-code/hooks | 2026-06-16 |
| Claude Code overview | https://docs.anthropic.com/en/docs/claude-code/overview | 2026-06-15 |
| Claude Code headless auth (GitHub issue) | https://github.com/anthropics/claude-code/issues/7100 | 2025-09-04 |
| Cursor 2026 guide | https://www.deployhq.com/guides/cursor | 2026-04-30 |
| Cursor Cloud Agents | https://cursor.com/cloud | 2026-02-26 |
| Cursor MCP reference | https://cursor.com/docs/mcp.md | — |
| Cursor Remote-SSH throttling (forum) | https://forum.cursor.com/t/cursor-remote-ssh-severely-throttles-ai-streaming-during-large-plan-generation-ssh-1-2-kb-s/147779 | 2026-01-01 |
| Mastering Cursor IDE | https://authorityaitools.com/cookbooks/mastering-cursor-ide | 2026-02-25 |
| Antigravity CLI guide (AI Builder Club) | https://www.aibuilderclub.com/blog/antigravity-cli-guide | 2026-06-21 |
| Antigravity CLI deep dive (Agentpedia) | https://agentpedia.codes/blog/antigravity-cli-deep-dive | 2026-05-20 |
| O'Reilly Antigravity CLI live event | https://www.oreilly.com/live-events/agentic-coding-with-google-antigravity-cli/0642572224547/0642572350789/ | — |
| Antigravity 2.0 complete guide (O-mega) | https://o-mega.ai/articles/google-antigravity-2-0-the-complete-2026-guide | 2026-05-20 |
| Antigravity/Gemini CLI configuration (GitHub) | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md | 2025-04-17 |
| Devin CLI extensibility | https://docs.devin.ai/cli/extensibility/index | — |
| Devin CLI configuration | https://docs.devin.ai/cli/extensibility/configuration | — |
| Devin CLI rules | https://docs.devin.ai/cli/extensibility/rules | — |
| Devin Desktop FAQ | https://docs.devin.ai/desktop/devin-desktop-faq | — |
| Devin playbooks | https://docs.devin.ai/product-guides/using-playbooks | — |
| Devin release notes 2026 | https://docs.devin.ai/release-notes/2026 | — |
| Apple container technical overview | https://github.com/apple/container/blob/main/docs/technical-overview.md | 2025-05-30 |
| Apple container how-to (network isolation) | https://github.com/apple/container/blob/main/docs/how-to.md | 2025-05-30 |
| CybersecurityNews Apple Containerization | https://cybersecuritynews.com/apples-containerization-feature-macos/ | 2025-07-29 |
| Devclass Apple Containerization | https://www.devclass.com/containers/2025/06/11/apples-containerization-will-matter-to-developers-but-podman-devs-complain-of-unfixed-issues/101152 | 2025-06-11 |
| DEV.to Apple container v1.0.0 | https://dev.to/trknhr/apples-container-just-hit-v100-mid | 2026-06-10 |
| Trend Micro MCP container security | https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/using-containers-to-secure-your-mcp-infrastructure | 2025-09-17 |
| MicroVM secure agent sandboxes | https://emeditor.it.com/a/5043.html | — |
