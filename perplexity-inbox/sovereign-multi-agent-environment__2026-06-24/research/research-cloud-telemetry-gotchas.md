# Cloud Agents + Telemetry + Gotchas
**Research document — Multi-agent AI dev environment (Mac mini cells + Beast + optional Google Cloud over Tailscale)**
*Compiled: 21 June 2026*

---

## AREA A — Google Cloud for Running Cloud Agents

### Services Overview

There are four main Google Cloud surfaces for autonomous AI agent workloads, each with a different tradeoff:

| Service | Model | Best fit | Isolation |
|---|---|---|---|
| **Cloud Run** | Serverless containers, scale-to-zero | Short-to-medium agent tasks, API-wrapped agents, multi-agent microservices | Container per instance; second-gen execution environment |
| **GCE (Compute Engine)** | Persistent VMs | Long-running coding agents, GPU workloads, bring-your-own environment | VM-level; full kernel control |
| **Vertex AI Agent Engine (Agent Platform Runtime)** | Fully managed, serverless | Managed ADK/LlamaIndex agents, Google-native tooling, no infra ops | Secure sandbox execution; per-agent session isolation |
| **Cloud Workstations** | Managed dev VMs with IDE access | Interactive coding sessions, human-in-the-loop agents | Per-user VM, VPC-connected |

#### Cloud Run
As of April 2026, Cloud Run is Google's primary surface for hosting production agent workloads. A key new capability is [Cloud Run individual instances](https://cloud.google.com/blog/products/serverless/whats-new-for-cloud-run-at-next26) — you can now allocate a single long-running instance (rather than a service/job abstraction) backed by Cloud Storage volume mounts, ideal for persistent background agents. Cloud Run also integrates with the **Gemini Enterprise Agent Platform** (preview as of April 2026), which handles transition from experimental to production without rebuilding agents.

Practical limits to know:
- Default request timeout is 60 minutes (configurable to longer for jobs)
- GPU support now includes NVIDIA RTX PRO 6000 Blackwell Server Edition
- Min instances = 1 eliminates cold starts but incurs idle cost
- Set `cpu_idle = true` so background async operations (callbacks, cache warming) are not throttled to near-zero CPU when there are no active requests

#### Vertex AI Agent Engine (Gemini Enterprise Agent Platform)
[Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) is a fully managed runtime — you deploy an ADK or LlamaIndex agent and Google manages the infrastructure. It provides:
- Built-in observability via Cloud Trace and custom metrics
- **Sessions** and **Memory Bank** for persistent conversation state (began billing January 28, 2026)
- **Secure sandbox execution** for Code Execution and Computer Use
- **Private Service Connect (PSC) interface** to connect agents back to a customer VPC without public internet traversal ([PSC-I docs](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/private-service-connect-interface), Oct 2025)

Agent Engine is the most hands-off option — you trade configuration flexibility for zero infrastructure management.

#### GCE
Standard VMs — install Tailscale directly on the instance. Best when you need persistent GPU access, kernel-level control, or a stable long-lived environment for a coding agent that runs for hours. More expensive than Cloud Run at low utilisation (you pay whether the agent is working or not), but cheaper per hour for continuous heavy workloads.

#### Cloud Workstations
Managed dev VMs with IDE access over the browser or a local IDE. Primarily for human-in-the-loop workflows where an agent assists a developer working in a cloud IDE. Cost is higher than Cloud Run or GCE for pure automation because the service includes the workstation management layer.

---

### Workload Isolation

| Surface | Isolation mechanism |
|---|---|
| Cloud Run | Container per revision instance; second-gen execution uses microVM (gVisor-based sandboxing optional) |
| GCE | Full VM; each agent on its own instance has complete kernel isolation |
| Agent Engine | Google-managed secure sandbox; agents cannot access underlying infrastructure |
| Cloud Workstations | Per-user VM, VPC-peered, session-scoped |

For multi-agent coding workloads where agents touch code or execute arbitrary commands, GCE VMs or Cloud Run with separate containers per agent provide the safest isolation. Agent Engine provides strong sandbox-level isolation for its compute, but you can't customise the runtime environment.

---

### Tailscale Integration with Google Cloud

**Tailscale's official [GCP reference architecture](https://tailscale.com/docs/reference/reference-architectures/gcp) (updated January 2026)** covers four patterns:

#### 1. Agent-to-agent (GCE instances)
Install Tailscale directly on the GCE instance. Best for static resources. Enables Tailscale SSH and full mesh routing back to your Beast/mini tailnet. Use cloud-init to automate:

```yaml
# GCE user-data (cloud-init)
runcmd:
  - ['sh', '-c', 'curl -fsSL https://tailscale.com/install.sh | sh']
  - ['tailscale', 'up', '--auth-key=tskey-abcdef...', '--advertise-tags=tag:cloud-agent']
```

Tag the node with an ACL tag — this disables key expiry automatically (see gotchas below).

#### 2. Cloud Run — userspace networking + SOCKS5
Cloud Run containers cannot use kernel networking but support [Tailscale userspace networking](https://tailscale.com/docs/install/cloud/cloudrun) (updated January 2026). The container runs `tailscaled` in userspace mode with a SOCKS5 proxy; your application routes outbound traffic through the proxy to reach your tailnet.

Dockerfile pattern (multistage):
```dockerfile
FROM alpine:latest
# Copy Tailscale binaries from official image
COPY --from=tailscale/tailscale:latest /usr/local/bin/tailscaled /app/tailscaled
COPY --from=tailscale/tailscale:latest /usr/local/bin/tailscale  /app/tailscale
RUN mkdir -p /var/run/tailscale /var/cache/tailscale /var/lib/tailscale
CMD ["/app/start.sh"]
```

`start.sh`:
```bash
#!/bin/sh
/app/tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
/app/tailscale up --auth-key=${TAILSCALE_AUTHKEY} --hostname=cloudrun-agent
echo Tailscale started
# Your agent binary, with outbound traffic via SOCKS5
ALL_PROXY=socks5://localhost:1055/ /app/my-agent
```

Store `TAILSCALE_AUTHKEY` as a Cloud Run secret (Variables & Secrets tab → reference as environment variable). Use an **ephemeral** auth key so the device is automatically cleaned up when the container exits.

#### 3. Subnet router (managed services like Cloud SQL)
Deploy a GCE instance running a Tailscale subnet router within your VPC. Exposes the entire VPC subnet to your tailnet without installing Tailscale on each resource. Run **multiple subnet routers across zones** for high availability.

#### 4. Agent Engine → VPC via PSC-I
For Agent Engine reaching private resources (e.g., your Beast server via Tailscale subnet router):
1. Create a VPC network attachment in your GCP project
2. Deploy the agent with `network_attachment` set
3. PSC-I gives the agent a private IP in your VPC; from there it reaches your Tailscale subnet router to access tailnet resources

This is the path to connect a managed Agent Engine agent back to your self-hosted Beast.

---

### Cost Posture (Relative)

| Service | Idle cost | Active cost | GPU availability | When it stings |
|---|---|---|---|---|
| Cloud Run | Near-zero (scale-to-zero default) | Low–moderate per vCPU-second | Yes (L4, Blackwell) | GPU instances: expensive per second |
| GCE | Moderate (pay while VM runs) | Moderate | Yes (full catalogue) | Leaving GPUs idle overnight |
| Agent Engine | Low (serverless) | Moderate–high (managed overhead) | Managed (no choice) | Sessions/Memory Bank billing started Jan 2026 |
| Cloud Workstations | High (includes workstation mgmt fee) | High | Yes | Leaving workstations running unused |

**Rule of thumb:** Cloud Run is cheapest for burst/intermittent agent tasks. GCE wins for continuous GPU-heavy workloads. Agent Engine charges a premium for zero-ops. Cloud Workstations are for human developers, not pure automation.

---

### Cloud Agent Hosting: When It Makes Sense vs. Local/Beast

| Use Cloud when… | Stay local/Beast when… |
|---|---|
| Workload needs to burst beyond Beast's GPU/CPU ceiling | Cost matters and Beast has headroom |
| Agent needs geographic distribution or multi-region execution | Low-latency access to local files/tools matters |
| You want zero-ops (no patching VMs, no Tailscale management) — Agent Engine | You want full control and debugging ability |
| You need to isolate an untrusted agent in a strong sandbox | You need persistent state without cloud storage complexity |
| Task is short-lived and sporadic — Cloud Run scale-to-zero | Task is continuous (model training, long coding sessions) |
| You're running compute-heavy jobs that would starve other mini cells | Beast's idle GPU cycles are being wasted |

The practical answer for your setup: use Cloud Run for bursty agent tasks (CI-triggered code review, one-off refactors), keep long-running coding agents on Beast, and consider Agent Engine only if you want Google to manage the orchestration layer entirely.

---

## AREA B — Telemetry / Observability for Multi-Agent LLM Systems

### Wiring LiteLLM → Langfuse

Both LiteLLM and Langfuse are running but currently not connected. Here is the complete integration config.

#### Option 1: Proxy config (recommended for a proxy/gateway setup)

In your `litellm/config.yaml`:

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  # Wire both success AND failure to Langfuse
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

  # Control which LiteLLM-specific fields become Langfuse tags
  langfuse_default_tags:
    - "user_api_key_alias"     # which virtual key was used
    - "user_api_key_user_id"   # user behind the key
    - "user_api_key_team_alias" # team/agent group
    - "cache_hit"
    - "proxy_base_url"
```

Environment variables (set in `.env` or your secret manager):

```bash
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="http://langfuse.your-tailnet-hostname:3000"  # self-hosted over Tailscale
```

> **Docker networking gotcha:** If LiteLLM and Langfuse are in separate Docker containers, `localhost` in `LANGFUSE_HOST` resolves to the LiteLLM container, not the host. Use the Docker service name (`http://langfuse:3000`) or the Tailscale hostname of the Langfuse host. ([GitHub issue #5088](https://github.com/langfuse/langfuse/issues/5088), January 2025)

Sources: [LiteLLM logging docs](https://docs.litellm.ai/docs/proxy/logging), [LiteLLM Langfuse integration](https://docs.litellm.ai/docs/observability/langfuse_integration)

#### Option 2: OpenTelemetry path (Langfuse v3+)

LiteLLM supports an OTEL exporter that sends directly to Langfuse's OTEL endpoint — preferred for Langfuse v3:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_OTEL_HOST="http://langfuse.your-tailnet:3000"
# For self-hosted, replace with: https://otel.your-langfuse.company.com
```

In `config.yaml`:
```yaml
litellm_settings:
  success_callback: ["langfuse_otel"]
  failure_callback: ["langfuse_otel"]
```

Source: [LiteLLM OTEL integration docs](https://docs.litellm.ai/docs/observability/langfuse_otel_integration)

#### Disabling callbacks per-request (compliance override)

```bash
# Disable Langfuse for a specific request
curl http://localhost:4000/chat/completions \
  -H "x-litellm-disable-callbacks: langfuse" \
  -d '{"model": "gpt-4o", "messages": [...]}'
```

To lock callbacks on (prevent disabling, for audit trail):
```yaml
litellm_settings:
  allow_dynamic_callback_disabling: false
```

---

### What to Capture: Signal Hierarchy

#### Tier 1 — Always capture
| Signal | LiteLLM field / metadata key | Langfuse field |
|---|---|---|
| Model name | Automatic | `model` on generation |
| Input tokens | Automatic from LLM response | `usage.input` |
| Output tokens | Automatic | `usage.output` |
| Cost (USD) | LiteLLM calculates and sends automatically; [Langfuse captures it directly](https://langfuse.com/docs/observability/features/token-and-cost-tracking) | `cost` on generation |
| Latency | Automatic (start/end time) | `latency` |
| Success/failure | Callback type | Trace status |

For **reasoning models** (o1, o3): token inference does not work — Langfuse cannot infer cost without explicit usage. LiteLLM passes the usage from the API response, so as long as you're going through LiteLLM proxy, this is handled automatically.

#### Tier 2 — Per-agent attribution (must be set explicitly)

Pass a `metadata` block with every request. This is how you get "who did what" provenance:

```python
import openai

client = openai.OpenAI(
    api_key="sk-litellm-master-key",
    base_url="http://litellm.your-tailnet:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Refactor this function..."}],
    extra_body={
        "metadata": {
            # Agent identity
            "generation_name": "code-refactor-step",
            "trace_name": "agent:builder-agent",
            "trace_user_id": "agent:builder-1",   # treat agent as a "user"
            "session_id": "task-session-abc123",   # links all calls in one task

            # Custom tags for filtering in Langfuse dashboard
            "tags": [
                "agent:builder",
                "task:refactor",
                "env:beast"
            ],

            # Optional: link to a parent trace if this is a sub-call
            "parent_observation_id": "obs-orchestrator-xyz",
            "existing_trace_id": "trace-orchestrator-xyz"
        }
    }
)
```

The `session_id` groups all generations in a multi-step task. `trace_user_id` set to `"agent:builder-1"` treats each agent as a tracked entity — you can then filter costs by agent in the Langfuse dashboard.

Source: [LiteLLM per-request metadata docs](https://docs.litellm.ai/docs/proxy/logging), [Langfuse multi-agent tracing discussion](https://github.com/orgs/langfuse/discussions/7569)

#### Tier 3 — Cross-agent provenance

For parent→child span relationships across agents (e.g. orchestrator spawning sub-agents), the correct pattern as of Langfuse v3/v4 is to **pass the parent observation object**, not just a `trace_context`:

```python
from langfuse import get_client

langfuse = get_client()

# Orchestrator creates the root trace
with langfuse.start_as_current_span(name="orchestrator-task") as root_span:
    root_trace_id = root_span.trace_id
    root_obs_id = root_span.id

    # Pass these to sub-agents; they create child spans by referencing parent
    # Sub-agent side:
    with langfuse.start_as_current_span(
        name="builder-agent-subtask",
        parent_observation_id=root_obs_id,
        trace_id=root_trace_id
    ) as child_span:
        # LLM call here
        pass
```

**Warning (Langfuse v4):** The `trace_context` approach with `parent_span_id` does **not** enforce a true parent-child relationship — it only ensures the span belongs to the same trace. For true nesting, use `start_observation()` on the parent object. In v4, aggressive filtering can also break trace trees when intermediate spans are dropped. If traces appear disconnected, enable `should_export_span=lambda span: True` to diagnose. ([GitHub discussion #12757](https://github.com/orgs/langfuse/discussions/12757), March 2026)

Also note: if you use LangChain's `metadata` to pass `langfuse_session_id` or `langfuse_user_id`, these must be present at the **first call** that triggers trace creation — they are not applied retroactively to the parent trace. ([GitHub discussion #8493](https://github.com/orgs/langfuse/discussions/8493), August 2025)

---

### Recommended `litellm_settings` Block (Complete)

```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

  langfuse_default_tags:
    - "user_api_key_alias"
    - "user_api_key_user_id"
    - "user_api_key_team_alias"
    - "cache_hit"

  # Spend tracking — writes per-transaction spend to DB
  # disable_spend_logs: false  # keep enabled unless DB is a bottleneck

  # Lock callbacks (prevents accidental disabling in dev)
  allow_dynamic_callback_disabling: true  # set false for prod audit trail
```

---

## AREA C — Known Gotchas and Failure Patterns

### C1. Apple Container on macOS Tahoe (DNS, Memory)

#### DNS gotchas

**The `.local` domain trap** — macOS reserves `.local` for mDNS/Bonjour. The Apple `container` tool's embedded DNS service creates records in a custom domain (e.g., `container.test`), but on Tahoe, `mDNSResponder` can silently intercept DNS queries for custom or non-IANA TLDs (`.internal`, `.test`, `.lan`, `.home.arpa`) and handle them as mDNS, bypassing any unicast nameserver configured in `/etc/resolver/`. ([daily.dev bug report](https://app.daily.dev/posts/bug-report-macos-26-breaks-etc-resolver-supplemental-dns-for-custom-tlds-j23fozekh), March 2026; [Hacker News thread](https://news.ycombinator.com/item?id=47440759), March 2026)

The setup sequence for Apple's embedded DNS:
```bash
sudo container system dns create test    # creates /etc/resolver/test
container system dns default set test    # makes "test" the default domain
# Containers are now reachable at <name>.test
```
But on Tahoe 26, this breaks for anything pointing to a custom TLD because of the mDNS regression.

Workarounds:
- **Use `.localhost` or a real subdomain** (e.g., `myapp.dev.yourdomain.com`) — these bypass the mDNS interceptor
- Use `/etc/hosts` entries pointing to `127.0.0.1` for static container hostnames
- Avoid `.local` entirely for container hostnames
- OrbStack users on Tahoe hit the same issue with `.orb.local` ([OrbStack GitHub issue #1984](https://github.com/orbstack/orbstack/issues/1984), June 2025); workaround is `/etc/hosts` + a local reverse proxy (Caddy/Traefik) on `*.localhost`

**Tailscale + Apple Container DNS conflict:** If Tailscale is running alongside Apple Container, VPN-pushed DNS resolvers can override container DNS. Inside a container, disable "Allow Local Network Access" in Tailscale settings to restore container network connectivity ([GitHub apple/container issue #345](https://github.com/apple/container/issues/345), July 2025).

**Tahoe 26 breaks `/etc/resolver/` supplemental DNS** for custom TLDs — confirmed regression as of 26.0, still present in early point releases. The container tool itself creates `/etc/resolver/` entries, so this directly breaks the embedded DNS feature.

Flush sequence when DNS goes wrong:
```bash
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```
If `mDNSResponder` is missing: `sudo launchctl kickstart -k system/com.apple.mDNSResponder`

#### Memory gotchas

**Memory ballooning is not fully implemented.** The macOS Virtualization framework has incomplete support for dynamic memory relinquishment. Apple Container uses a VM-per-container model (each container gets its own Linux kernel via Virtualization.framework). When processes inside the container free memory back to Linux, those pages are **not returned to the macOS host**. ([Apple container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md), confirmed also in [LinuxSecurity.com](https://linuxsecurity.com/news/vendors-products/apples-native-macos-container-tool), June 2025)

Practical impact:
- Running 4–5 containers simultaneously accumulates unreleased host RAM
- A container that spikes to 4 GB and then drops to 200 MB still holds 4 GB from the host's perspective
- You will need to **restart containers periodically** to recover host RAM in memory-intensive multi-agent setups

Workarounds:
- Set explicit `--memory` limits per container: `container run --memory 2g <image>`
- Default is 1 GB RAM and 4 CPUs per container — explicitly set both for agent containers
- Builder VM defaults: 2 GB RAM / 2 CPUs; override with `container builder start --cpus 4 --memory 8g`
- Monitor with `container stats` and restart containers that are retaining excess RAM

**Tahoe memory pressure (8 GB Macs only):** macOS 26 Tahoe introduced a memory management rewrite optimised for 24 GB+ unified memory Macs. On 8 GB models, the Apple Intelligence/Spotlight intelligence layer keeps large neural caches in memory, causing swap spikes and SSD thrash. Running a multi-agent container workload on an 8 GB mini will hit this hard. ([Apple Discussions](https://discussions.apple.com/thread/256175897), October 2025)

**VM-per-container overhead:** Unlike Docker (which shares one Linux kernel across all containers), every Apple Container has its own kernel. Memory overhead per container is ~dozens of MB just for the VM infrastructure before your workload starts. ([Anil Madhavapeddy technical analysis](https://anil.recoil.org/notes/apple-containerisation), June 2025)

---

### C2. Tailscale Persistence and Key Expiry

This is one of the most common "works in dev, breaks silently in prod" failure patterns.

#### The two-key problem

Tailscale uses **two separate keys** that expire independently:

| Key type | Default expiry | What happens on expiry |
|---|---|---|
| **Auth key** (`tskey-auth-...`) | 1–90 days (90 max) | Cannot register new nodes; existing nodes already registered are not affected |
| **Node key** | 180 days (configurable, 3–180 days) | Node drops off the tailnet; all connections from/to that node stop working |

A common misconception: disabling key expiry on a device does not affect the auth key. The auth key is only used for **initial registration**; after that, the node key is what matters. ([Tailscale auth keys docs](https://tailscale.com/docs/features/access-control/auth-keys), December 2025; [Tailscale key expiry docs](https://tailscale.com/docs/features/access-control/key-expiry), January 2026)

#### The pfSense/headless node re-auth trap

If your startup script runs `tailscale up --auth-key=...` on every boot (as many init scripts do), and the auth key has expired, Tailscale **will not start on reboot** — even if you previously had key expiry disabled on the node key. The `tailscale up` command attempts a fresh registration using the auth key, overriding the valid existing node key. ([Netgate forum thread](https://forum.netgate.com/topic/177265/tailscale-is-not-online-problem/43), January 2023, still relevant)

#### Production-safe patterns

**Pattern 1 — Tagged nodes (recommended for servers)**
```bash
# Generate a tagged, reusable auth key in the admin console
# The tag disables node key expiry automatically
tailscale up --auth-key=tskey-auth-... --advertise-tags=tag:beast-server
```
Tagged devices have key expiry **disabled by default** after first auth ([Tailscale blog](https://tailscale.com/blog/tagged-key-expiry), March 2022). Once tagged and authenticated, the node persists indefinitely without re-authentication.

**Pattern 2 — OAuth client for dynamic provisioning**
For scripts that spin up cloud agents (Cloud Run, GCE), use an OAuth client secret instead of a static auth key. OAuth secrets do not expire on a 90-day cycle and can generate auth keys on demand. Generate at `https://login.tailscale.com/admin/settings/oauth`. ([Reddit discussion](https://www.reddit.com/r/Tailscale/comments/17ckdse/auth_keys_90_day_limit/))

**Pattern 3 — Disable key expiry via admin console**
For static servers (Beast, mini cells): Admin console → Machines → `...` menu → Disable Key Expiry. Note: this must be done **after** the device is authenticated. A change to the Key Expiry setting only applies to devices logged in after the change; existing devices are unchanged until their next login. ([Tailscale docs](https://tailscale.com/docs/features/access-control/key-expiry))

**Pattern 4 — Ephemeral keys for Cloud Run / short-lived containers**
Use ephemeral auth keys for containers and serverless workloads. Tailscale automatically removes ephemeral nodes from the tailnet when they go offline, keeping the machine list clean. ([Tailscale auth keys docs](https://tailscale.com/docs/features/access-control/auth-keys))

#### What no built-in auto-renewal means in practice
As of June 2026, Tailscale has no native auto-renewal for node keys on headless systems. Once a node key expires on an unattended server, you need out-of-band access to re-authenticate. The Tailscale admin console offers a 30-minute "Temporarily extend key" option for expired nodes, but this still requires someone to trigger it. ([GitHub feature request #16566](https://github.com/tailscale/tailscale/issues/16566), July 2025) The mitigation is to use tagged nodes + disable key expiry for all production servers.

---

### C3. Multi-Agent File Collisions

When multiple AI agents operate simultaneously on the same repository, they reproduce distributed systems concurrency problems — with the added danger that agents do not detect or surface these failures. ([Augment Code guide](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution), April 2026)

#### Failure modes

| Mode | Mechanism | Detection | Impact |
|---|---|---|---|
| **Silent file overwrites** | Two agents write to the same file simultaneously | None — agents proceed on corrupted state | Data loss |
| **Context contamination** | Agent A's changes invalidate Agent B's assumptions; B can't see A's work | None until compile/test | Cascading breakage |
| **`.git/index.lock` contention** | Concurrent git operations on the same worktree compete for file-based locks | Immediate exception — but blocks all agents | System-wide git freeze until manual `rm .git/index.lock` |
| **Shared infrastructure thrash** | Multiple agents trigger `./gradlew test` or DB migrations simultaneously | Silent — just slow | Corrupted build artifacts, flaky tests |

#### Prevention: git worktree isolation

Git worktrees are the correct primitive for parallel agent isolation. Each worktree gets its own working directory and git index while sharing the object store:

```bash
# Create a worktree per agent/task
git worktree add ../agent-builder-task feature/agent-builder-task
git worktree add ../agent-reviewer-task feature/agent-reviewer-task

# Each agent works in its own directory; no index lock contention
# Conflicts surface at merge time via standard git tooling
```

Key rules:
- Git prevents the same branch from being checked out in more than one worktree — this is a feature, not a bug
- Use `git worktree remove` and `git worktree prune` for cleanup, not `rm -rf` (avoids stale metadata)
- Enable `git rerere` so conflict resolutions are recorded: `git config rerere.enabled true`
- For large repos: `git worktree add` + `git sparse-checkout set <paths>` limits each agent to only the files it needs

#### Orchestration patterns
- **Assign non-overlapping file domains before work begins** — the most reliable prevention
- **Sequence dependent tasks** rather than parallelising them
- **Verification gates before merge**: run tests after each agent completes; attribute regressions to the agent's branch
- Use worktree-per-task for ephemeral work; worktree-per-agent for long-lived specialised agents

---

### C4. Infisical Self-Hosted Secret Manager

#### The `ENCRYPTION_KEY` trap (hardest gotcha)

Infisical encrypts all secrets at rest using `ENCRYPTION_KEY`. This key must be set **before** the first startup and **never changed** afterwards.

**Symptom:** Infisical fails to start with `"Unsupported state or unable to authenticate data"` or `RangeError: Invalid key length`.

**Root cause:** The key must be exactly **32 hex characters (16 bytes)**:
```bash
openssl rand -hex 16   # correct — produces 32 hex chars
openssl rand -hex 32   # WRONG — produces 64 hex chars, causes RangeError on startup
```

The docs historically linked to envvar documentation that implied you could change the key at any time. You cannot. Changing `ENCRYPTION_KEY` after initial setup renders all existing secrets **permanently unreadable**. The only recovery is to delete the Docker volumes and rebuild from scratch. ([GitHub issue #2005](https://github.com/Infisical/infisical/issues/2005), June 2024; [selfhosting.sh Infisical guide](https://selfhosting.sh/apps/infisical/), February 2026)

**Mitigation:**
- Generate and store `ENCRYPTION_KEY` in a separate secure location (not alongside your database backup) immediately at setup
- Use `openssl rand -hex 16` explicitly
- Consider using an external KMS (AWS KMS, Google Cloud KMS) to wrap the root key — this separates the root key from the Infisical instance ([Infisical KMS docs](https://infisical.com/docs/documentation/platform/kms/overview))

#### Kubernetes operator idempotency bug
The Infisical Kubernetes operator (as of mid-2024) reads `InfisicalSecret` CRDs only once and does not react to updates. If you change `envSlug` from `dev` to `staging`, nothing happens — the operator continues to print "No secrets modified so reconcile not needed." ([GitHub issue #2038](https://github.com/Infisical/infisical/issues/2038), June 2024) The workaround is to delete and recreate the CRD resource.

#### Kubernetes operator auth — case-sensitive secret keys
The operator expects `clientId` and `clientSecret` (camelCase) in the Kubernetes secret. Using `client-id` or `client_id` causes a `no authentication method provided` error that is difficult to diagnose from logs alone. ([GitHub issue #2170](https://github.com/Infisical/infisical/issues/2170), July 2024)

```bash
# Correct
kubectl create secret generic infisical-secrets \
  --from-literal=clientId=<uuid> \
  --from-literal=clientSecret=<secret>

# Wrong — will silently fail auth
kubectl create secret generic infisical-secrets \
  --from-literal=client-id=<uuid> \
  --from-literal=client-secret=<secret>
```

#### Secret rotation silently fails on free self-hosted tier
Secret rotation (e.g. AWS IAM key rotation) is gated behind the Pro plan. On the free self-hosted tier, the UI lets you configure rotation without error, then the rotation silently fails with a `"Provider not found"` error in server logs only. There is no in-UI warning. ([GitHub issue #2043](https://github.com/Infisical/infisical/issues/2043), June 2024)

#### Service token 401s
Service tokens have configurable TTLs. A 401 on API calls usually means the token expired — check TTL in the Infisical UI, not just the operator logs. For always-on server access, use Machine Identities (Universal Auth) instead of service tokens.

#### MongoDB → PostgreSQL migration failures
Infisical migrated from MongoDB to PostgreSQL (now PostgreSQL-only). If you have an old MongoDB-based instance, the migration script fails if there are two admin-level accounts (`duplicate key value violates unique constraint "super_admin_pkey"`). Delete one admin account before migrating. ([GitHub issue #1727](https://github.com/Infisical/infisical/issues/1727), April 2024)

#### Helm chart `ENCRYPTION_KEY` base64 encoding
Helm chart deployments store the key in a Kubernetes Secret, which base64-encodes values. If you accidentally provide a base64-encoded key in `stringData` (which Kubernetes re-encodes), you end up with a double-encoded value that Infisical cannot use. Verify the actual decoded value in the secret before reporting Infisical bugs. ([GitHub issue #2733](https://github.com/Infisical/infisical/issues/2733), November 2024)

#### KMS key rotation caveats
After rotating a KMS key in Infisical, existing ciphertexts encrypted with the old key remain decryptable **only through the Infisical instance** — the old key material is retained internally. However:
- Exported key material (for escrow/DR) only ever captures the **current** version — re-export after each rotation
- KMIP clients retrieve raw key material and will fail to decrypt data encrypted with the previous version after rotation ([Infisical KMS docs](https://infisical.com/docs/documentation/platform/kms/overview))

---

## Quick Reference: Decision Matrix

### Where to run an agent

```
Is it long-running (hours) and needs GPU?
  → Beast (local) or GCE (cloud)

Is it bursty, short-lived, containerised?
  → Cloud Run with Tailscale userspace sidecar

Do you want zero infrastructure ops?
  → Vertex AI Agent Engine (costs more; started billing for Sessions Jan 2026)

Is it an interactive coding session with a human?
  → Cloud Workstations (priciest; designed for this)

Are you just experimenting and Beast has headroom?
  → Beast
```

### LiteLLM → Langfuse: minimum viable wire-up

```yaml
# litellm config.yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]
```

```bash
# .env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://langfuse.your-tailnet:3000
```

Per-agent attribution: pass `extra_body={"metadata": {"trace_user_id": "agent:builder-1", "session_id": "task-123", "tags": ["agent:builder"]}}` in every request.

### Tailscale production checklist

- [ ] Tag all server nodes with an ACL tag at first auth → key expiry disabled automatically
- [ ] Use OAuth clients (not static auth keys) for cloud agent provisioning scripts
- [ ] Use ephemeral keys for Cloud Run / short-lived containers
- [ ] Set `TS_AUTH_ONCE=true` in container env so containers don't re-register on every restart
- [ ] Never run `tailscale up --auth-key=...` on boot for nodes where key expiry is disabled (it overrides the node key)

### Infisical self-hosted checklist

- [ ] Generate `ENCRYPTION_KEY` with `openssl rand -hex 16` (32 hex chars exactly)
- [ ] Store `ENCRYPTION_KEY` separate from DB backups before first `docker compose up`
- [ ] Use Machine Identities (Universal Auth) for service access, not service tokens with TTLs
- [ ] Use `clientId`/`clientSecret` (camelCase) in Kubernetes secrets for the operator
- [ ] Do not rotate KMS keys used by KMIP clients

---

*Sources compiled from Tailscale docs (Jan 2026), Google Cloud docs (Apr 2026), LiteLLM docs, Langfuse docs (Jun 2026), Apple container GitHub repo, OrbStack GitHub issues, and community reports cited inline.*
