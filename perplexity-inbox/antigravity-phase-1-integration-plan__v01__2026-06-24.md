# Antigravity Phase 1 Integration Plan — Code & Base Prep (Comprehensive Integration)

**TIER:** STRUCTURED
**PROVENANCE:** verified local state + 12 backup skills in `/Users/ewansair/.gemini/antigravity-backup/skills/` + Ewan's sovereign architecture guidelines (2026-06-24).
**STATUS:** published to Perplexity inbox for final reconciliation.

---

## 1. Strategic Context & Sovereignty

1. **AI / Host Allocation:**
   - **Antigravity (our seat):** Runs on the Mac Mini (`wanmini` / `100.77.149.1`), working mostly in the cloud (Google Cloud Workspace) to leverage greater compute.
   - **Devin:** Runs on the Mac Mini in a sealed Apple Container cell.
   - **Claude:** Runs locally on the M5 MacBook Air command seat.
2. **Independent & Self-Protecting Sovereignty:**
   - Each AI operates with its own sovereignty, privacy, and security. 
   - There are no global write locks or run-time execution leases limiting an agent's right to work. AIs write concurrently within their sandboxed worktrees.
3. **Vellum as the Communication Bus:**
   - Ewan's interactions with each IDE and AI route through Vellum. Sourcing prompts and comments from Vellum avoids local chat history bloat, ensuring token-efficient execution and enabling advanced context engineering.
4. **Tailscale Mesh Network:**
   - Traffic routes internally via Tailscale IPs (`100.x.y.z`).
   - *Infrastructure constraint:* Beast SSH is refused on its Tailscale IP (bound to public IP `135.181.161.131` only, using key `~/.ssh/beast_m5`). Mac Mini SSH is active over Tailscale (`one@100.77.149.1`).

---

## 2. User Review Required

### 1. Mac Mini RAM & Exit Node Capacity
- Confirming the Mac Mini has **24 GB** of RAM and operates as a Tailscale Exit Node. This is fully sufficient for local 8B/14B Qwen-Coder models alongside the 4 container cells.

### 2. Vellum & Finneskill (personal-fin) JWT Issues
- There is a reported issue with JWT authentication in Vellum and the `personal-fin` ("Finneskill") stack.
- **Proposed Action:** We will run a diagnostic script on the M5 to test Vellum writes using the HS256 secret (`vellum-dogfood-2026-scaffold`) and inspect the `personal-fin` config files to isolate token signature or clock-drift validation errors.

### 3. Beast State & Opik Telemetry Auto-Restart
- We will update `/opt/amplified/BEAST-STATE.md` to reflect the live data spine (pgvector + AGE, no FalkorDB/Qdrant) and 84 running containers.
- We will inject `restart: unless-stopped` into the Opik compose file on the Beast to ensure the evaluation platform remains active across host restarts.

### 4. Skill Restoration Approval
- We will restore the 13 empty skills from backup by copying their `SKILL.md` files from `/Users/ewansair/.gemini/antigravity-backup/skills/` to `/Users/ewansair/.gemini/config/skills/`.

### 5. VS Code vs VSCodium & M5 Thin-Client Remote-SSH Transition
- **VS Code vs. VSCodium Advice:** VS Code has proprietary licensing and telemetry that gathers background metrics. We advise transitioning to **VSCodium** (the open-source, telemetry-free build of the same editor) to align with a secure, sovereign AI-native environment.
- **M5 Thin-Client Plan:** We will transition all local workspace file checkouts, language servers, and local Docker execution off the M5 MacBook Air. The M5 Mac will run Cursor and VSCodium *only* as GUI thin-clients, connecting to the Mac Mini (`wanmini`) and the Beast (`beast`) over tailnet SSH. This guarantees the M5 host remains 100% clean and free of local CPU-heavy AI tools, docker containers, and dependency bloat.
- **Access & Research Pipe Hardening:**
  - Harden local file permissions of `/Users/ewansair/ingestion-to-research-pipe/` to owner-only (`chmod 700`) to prevent unprivileged local access.
  - Mount the research pipe read-only (`ro`) into the corresponding OrbStack Docker containers on the Mac Mini, restricting direct writes to Git commits checked by our pre-production gates.
  - Harden canonical GitHub branch protections: `enforce_admins: true`, `required_signatures: true`, and ensure workflows (`/.github/workflows/`) are owned strictly by `@ewan-dot` CODEOWNERS to prevent autonomous self-approval loops (e.g., preventing any `AUTO_MERGE_PAT` self-approval).

---

## 3. Open Questions for Ewan

> [!IMPORTANT]
> 1. **Mac Mini GitHub Access:** Should we clone the clean `main` branch of `intent-interface` directly on the Mini via SSH, or should we push a clean clone from the M5 command seat?
> 2. **Vellum JWT TTL:** Does the Vellum server currently enforce strict JWT expiry that causes the 24-hour tokens minted by `intent-interface` to fail, and should we transition to a manual 30-day token format?
> 3. **Skill Parameter Mapping:** Should we map each agent's specific constraints (Allowed models, Temporal queues, allowed tools) directly in the `SKILL.md` YAML frontmatter, or should we create a central `agent_mesh_skills.json` configuration for the enforcer/orchestrator to read?

---

## 4. Proposed Changes

### Global Customizations Directory (`~/.gemini/config/`)

#### [NEW] [config/skills/*](file:///Users/ewansair/.gemini/config/skills)
- Restore all 13 `SKILL.md` files from `/Users/ewansair/.gemini/antigravity-backup/skills/` to their active locations under `~/.gemini/config/skills/`. (The session hand-off baton skill `amplified-baton` is retained as the context-transmission tool for session continuity).

### Beast Host (`beast` / `135.181.161.131`)

#### [MODIFY] [BEAST-STATE.md](file:///opt/amplified/BEAST-STATE.md)
- Refresh verified date, author metadata, and container counts.
- Remove old FalkorDB/Qdrant documentation and document the live pgvector + AGE data spine.
- Document Traefik dashboard rules and routing domains.

#### [MODIFY] [docker-compose.yaml](file:///opt/amplified/opik/deployment/docker-compose/docker-compose.yaml)
- Add `restart: unless-stopped` to the service definitions for `mysql`, `redis`, `clickhouse`, `zookeeper`, `minio`, `backend`, `python-backend`, `guardrails-backend`, `frontend`, `jaeger`, `otel-collector`.

---

## 5. Detailed Skills Integration, Hooks & Harnesses Plan

To bring the 13 researched skills into our active agent stack, we define the following control zone integration architecture:

```mermaid
graph TD
    subgraph L4/L3 Control Zone
        RodGuard[RodGuard Circuit Breaker] -->|Abort on RED/BLACK signal| WriteHook[Pre-Write Hook]
        Rules[amplified_permissions.classify()] -->|Verify action class| WriteHook
    end

    subgraph L6 VM Agent Cells
        CHWatcher[Companies House Watcher] -->|Chron Schedule| Temporal[Temporal Queue]
        MSwarm[Marketing/Success Agents] -->|Event Trigger| Temporal
        CodeAgents[Motion/Interface Engineers] -->|Dual-API Loop| Temporal
    end

    subgraph Telemetry Senses
        LF[Langfuse Traces] -->|Consecutive tool calls, latency| Senses[Vellum Senses sensor_event.py]
        Opik[Opik Evaluation] -->|LLM-as-Judge failures, guardrails| Senses
        Senses -->|RED/BLACK Signal| RodGuard
        Senses -->|AMBER Signal| Router[estate-token-router]
    end

    Temporal -->|Gated by| L2[9-Item Pre-Production Gate]
    L2 -->|Executes in Cell| WriteHook
    WriteHook -->|Attributed Write| Vellum[Vellum Immutable Ledger]
    WriteHook -->|Emits events| LF
    WriteHook -->|Emits events| Opik
```

### A. The 13 Target Skills
The following skills are restored from `/Users/ewansair/.gemini/antigravity-backup/skills/` to `/Users/ewansair/.gemini/config/skills/`:
- `amplified-companies-house-watcher` (Daily UK SMB incorporations extractor)
- `amplified-motion-engineer` (Remotion programmatic video architect)
- `amplified-interface-engineer` (Frontend Next.js/Tailwind/Vite developer)
- `amplified-customer-success` (CRM monitoring & case study drafter)
- `amplified-planning-department` (Central nervous system coordinator)
- `amplified-soul` (Primary Dalio/Radical/Layer-0 operating context)
- `amplified-insight-generator` (Research-to-insight compiler)
- `amplified-pain-researcher` (Target market pain point analyzer)
- `amplified-referral-curator` (Top-of-funnel referral organizer)
- `amplified-variant-generator` (Creative asset versioning worker)
- `antigravity-designer` (System design & UX layout arbiter)
- `amplified-linear` (Linear issue management)
- `amplified-communication` (Voice transcript & interface messenger)

*(The context-transmission skill `amplified-baton` is maintained solely for hand-off state across consecutive agent sessions, with zero role in write locking or execution control).*

### B. Hooks and Harnesses (Built to Free, Not Control)
Pre-agreed hooks and harnesses are designed to **free** the agents from loop thrashing and decision fatigue, ensuring that jobs are distributed deterministically and measured deterministically.

#### Hook A: The Temporal Background Worker Harness (L6/L0)
- **Mechanism:** Background workers (like `companies-house-watcher` and `customer-success`) run as long-lived Temporal Workers listening on target queues on the Beast (e.g., `companies-house-queue`, `customer-success-queue`).
- **Hook Integration:**
  - Before starting any workflow, the Temporal activity runner must check the **9-Item Pre-Production Gate** (L2).
  - All output drafts (emails, Markdown files) are written locally to the cell's output path. No direct writing to host storage or databases is allowed.
  - The worker uses the Vellum API to post logs and request human review before sending outreach.

#### Hook B: The Ken Huang Dual-API Validation Loop (L6/L4)
- **Mechanism:** For code and template generation tasks (`motion-engineer` and `interface-engineer`), the code production runs inside a consensus-seeking loop:
  - **Drafter (Gemini 3.1 Pro):** Generates compositions enforcing pure primitives, canonical time inputs (`useCurrentFrame` for Remotion), and component chunking.
  - **Critic (Claude 3.5 Sonnet):** Audits code determinism, responsive breakpoints, accessibility (ARIA), hydration boundaries, and state management.
- **Hook Integration:**
  - The validation engine is wired as a pre-commit check (`open_door_runtime/consensus_check`).
  - Code is only committed to the cell's repository if the Critic returns a consensus score of `100% PASS` with zero warnings. Any failure raises a `drift_signal` AMBER and aborts the write.

#### Hook C: RodGuard Integration (L4)
- **Mechanism:** To prevent concurrent conflicts and enforce the Layer-0 laws without the operational bottlenecks of global write locks:
  - **RodGuard Circuit Breaker:** Senses continuously monitor drift and rod compliance. If a rod is violated or a P0 incident is detected, RodGuard trips, transitions the state to `BLACK` (Emergency Stop), and locks all write capabilities across the cells.
- **Hook Integration:**
  - A pre-write hook is injected into the git configuration inside each container: `hooks/pre-commit` executes `amplified_permissions.classify("commit")` and checks RodGuard state.

#### Hook D: Outbound Content Tone Audit (L7/L4)
- **Mechanism:** Agents targeting external users (`companies-house-watcher` and `customer-success`) draft outreach assets. These assets must pass a programmatic tone check.
- **Hook Integration:**
  - A validation hook runs the draft through Section 7 of the Marketing Spine (Ken Huang Tone Check) to ensure the language is purely opt-in, non-aggressive, value-first, and contains zero manufactured claims.

#### Hook E: The 9-Item Pre-Production Gate (L2 Relay)
- **Mechanism:** Before any worker starts a task, it must verify the task's Vellum record satisfies the 9-item gate:
  1. `goal_link` (Must link to a valid active business goal)
  2. `owner` (Assigned agent cell ID)
  3. `input_refs` (Vellum event hashes of input materials)
  4. `acceptance_test` (Spec defining successful completion)
  5. `allowed_tools` (List of allowed tool calls)
  6. `data_sensitivity` (Class: Public, Pseudonymized, Confidential)
  7. `route_destination` (Output endpoint)
  8. `stop_condition` (Clear bounds to prevent infinite loops)
  9. `baton_requirement` (Denotes if this task represents a baton-pass continuation of a prior session)

#### Hook F: Telemetry Loop & Thrash Detection Engine (Vellum + Opik + Langfuse)
- **Mechanism:** Senses must monitor LLM run loops programmatically rather than depending on agent self-reporting:
  - **Langfuse Middleware:** Tracks sequential tool executions (e.g., running `cat` or `grep` repeatedly on the same files) and monitors token consumption/latency gradients per step.
  - **Opik Online Evaluators:** Runs automated guardrail evaluations on task inputs/outputs (LLM-as-judge checks for structural format drift or hallucination patterns).
  - **Vellum Senses (`sensor_event.py`):** Consumes Langfuse and Opik telemetry, aggregating them into three programmatic detectors:
    - `tool_loop_sensor`: Fires if the same tool is executed with identical parameters $>3$ times within a trace.
    - `edit_thrash_sensor`: Fires if the same lines of code are modified back-and-forth across consecutive turns.
    - `semantic_drift_sensor`: Monitors the cosine similarity of the agent's consecutive reasoning states. A sharp drop indicates context confusion/looping.
- **Hook Integration:**
  - **Pre-emptive Mitigation (Reflex 2):** If a sensor raises an `AMBER` signal, the `estate-token-router` intercepts the next turn, injects context compaction instructions to prune the trace history, or switches the model to a higher-judgment tier (Opus/Sonnet) to break the loop.
  - **Circuit Breaker (Reflex 1):** If the loop persists and raises a `RED` or `BLACK` signal, RodGuard trips, revokes the cell's write capabilities, terminates the Temporal execution, and posts the issue to the Cockpit Work Queue as `needs_attention`.

---

## 6. Comprehensiveness & Cohesion Check

### 1. Criticality Triaging (FMECA)
Not all agents require the same heavy guardrails. We triage the 13 agents by failure impact:
- **CRITICAL (REACT + PREDICT + RECOVER):**
  - `amplified-planning-department` (Central coordinator) — failure halts task routing.
  - `antigravity-designer` (System/Arbiter role) — handles final layouts and gates.
- **IMPORTANT (REACT + PREDICT):**
  - `amplified-motion-engineer` (Remotion worker) — consumes high Lambda compute.
  - `amplified-interface-engineer` (Frontend Next.js developer) — writes user-facing code.
- **STANDARD (REACT only):**
  - `amplified-companies-house-watcher` (Daily chron extraction worker) — low real-time cost.
  - `amplified-customer-success` (CRM monitoring worker).
  - `amplified-linear` (Task tracker worker).
  - `amplified-communication` (Voice transcript & messaging cleanup worker).
- **BEST-EFFORT (No Reflex / Anomaly Logging only):**
  - `amplified-pain-researcher` (Target market researcher).
  - `amplified-referral-curator` (Referral compiler).
  - `amplified-variant-generator` (Creative variation generator).
  - `amplified-insight-generator` (Insight compiler).

### 2. Boundary & Seal Auditing
- **Credential Leakage:** Background workers like `companies-house-watcher` require API tokens. The Apple Containers must not inherit these credentials from the Mac Mini host environment. All keys are injected inside the container via a JIT credential broker at runtime, maintaining isolation.
- **Unified Rules:** `amplified_rules.json` and `amplified_harness.py` are the single source of truth for permission classification. Cells will read this local config inside their sandbox rather than calling external permission endpoints, preventing latency.

### 3. Vocabulary Reconciliation
- **Beast vs. Infrastructure 1:** The code, container labels, and telemetry schemas will canonicalize on `Beast`. The label `Infrastructure 1` is reserved strictly for external documentation.
- **Harness definitions:** `amplified_permissions.py` (the classifier script) is distinguished from `open_door_runtime/` (the RodGuard daemon).

---

## 7. Verification Plan

### Automated & Manual Checks

1. **Vellum JWT Diagnostic:**
   - Execute the diagnostic script locally on the M5 command seat using the HS256 secret (`vellum-dogfood-2026-scaffold`) and verify successful token generation.
2. **Beast Container Status:**
   - Verify that Traefik routers are healthy and compose restart policy `unless-stopped` keeps Opik containers active.
3. **Skill Restoration & Read Test:**
   - Run:
     ```bash
     ls -la /Users/ewansair/.gemini/config/skills/
     ```
     Verify that all 13 restored skills contain their respective `SKILL.md` files.
4. **Harness Classification Test:**
   - Execute:
     ```bash
     python3 /Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/amplified_harness.py
     ```
     Verify that the self-test prints `ALL PASS`.
5. **Loop and Thrash Simulation:**
   - Simulate a repeating tool execution trace in a mock container cell, verifying that the Vellum `tool_loop_sensor` triggers an `AMBER` signal, and is intercepted by `estate-token-router` to inject compaction instructions.
