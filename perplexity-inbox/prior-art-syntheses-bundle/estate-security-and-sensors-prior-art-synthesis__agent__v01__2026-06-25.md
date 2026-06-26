---
document_id: estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25
document_type: research_conclusion
stage: synthesis
reader: agent
author: subagent-prior-art
created: 2026-06-25
version: v01
goal_link: "Ewan/estate-security-and-sensors-prior-art"
owner: Amplified Partners
input_refs:
  - infisical container (Beast, port 127.0.0.1:8403→8080, up 12h)
  - 1PASSWORD_INFINISICAL_METHODOLOGY.md (/Users/ewansair/, 3887 bytes, 2026-06-03)
  - amplified-crm / amplified-crm-dev (ports 8001, 8003)
  - cove-postgres / cove-temporal / cove-api / cove-translator / cove-heal-watchdog
  - perplexity-ingest (/opt/amplified/apps/perplexity-ingest/main.py, PERPLEXITY_INGEST_TOKEN)
  - token-proxy (port 8088)
  - LiteLLM (Claude / GPT / Llama / Qwen keys)
  - tailscale (up 7d, mesh plane)
  - MCP servers (12 named: vellum-mcp, claude-cowork-mcp, claude-code-mcp, claude-desktop-mcp, devin-desktop-mcp, codex-mcp, grok-mcp, grok-readonly-mcp, beast-control-mcp, amplified-knowledge-mcp, brain-mcp-writer, brain-mcp-readonly)
  - vellum (up 6d, ports 8400/8411-8413, evidence dir /opt/amplified/vellum/evidence/entries/)
  - Langfuse (langfuse + langfuse-worker, up 7d)
  - Opik (full stack, up 12-19h)
  - cascade-mac PR#1 (pre-commit scanner, 13 patterns, DeepSeek + Moonshot keys found in history)
  - MacAirM5 (active) / WanMin Mac mini M4 Pro / MacAirM4
data_sensitivity: internal-confidential
route_destination: Ewan / relay-protocol
baton_requirement: "Human review before: Infisical adoption order changes, key TTL policy changes, breach-playbook trigger. Do not auto-rotate LiteLLM keys without confirming downstream consumer readiness."
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  open_action: "Three open gates: (1) Vellum JWT TTL — recommend 30d, justified below; (2) SPIRE vs Tailscale-identity choice — recommend Tailscale-derived at this scale, justified below; (3) Mac mini as central sensor vs peer — recommend central sensor role, justified below. All three require Ewan decision before implementation."
tier: T2-moderate
domains_surveyed: 11
primary_sources_cited: 18
companion_syntheses:
  - research-pipe-prior-art-synthesis__agent__v01__2026-06-25
  - ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25
  - data-lake-prior-art-synthesis__agent__v01__2026-06-25
---

## One-sentence summary [T2-moderate]

The Amplified estate needs one identity plane (Infisical as the single secrets source of truth, Tailscale as the network-identity substrate) and one observability plane (Vellum as the immutable audit ledger, OTel as the telemetry wire format), a shape that maps directly onto canonical prior art from HashiCorp Vault dynamic-credential patterns, NIST SP 800-57 key management, NIST SP 800-207 zero-trust architecture, SPIFFE/SPIRE workload identity, Sigstore/Rekor transparency logs, Falco/eBPF runtime detection, osquery + Santa on Mac, and NIST SP 800-61 r3 incident response.

---

## Purpose and framing

The framing question from the voice memo: should every service authenticate via a single Infisical-issued identity, and should every service emit Vellum events on a known schema — or is a federated mesh acceptable? Prior art answers the framing question unambiguously.

[NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) (Zero Trust Architecture, August 2020) establishes that network location is not a trust signal; authentication and authorisation must be discrete functions performed before each session, regardless of whether a service is on a local LAN or remote. The Amplified stack already satisfies the network layer via Tailscale. The gap is the identity layer: twelve MCP servers, four ingestion pipes, two CRM containers, a full Cove/Temporal stack, LiteLLM, and three Mac endpoints each have independent or absent auth models. That is a federated mess, not a designed mesh.

[HashiCorp Vault's design rationale](https://developer.hashicorp.com/vault/tutorials/get-started/understand-static-dynamic-secrets) (the canonical secrets-management prior art, pre-dating Infisical) shows why: static long-lived credentials are compromised through exposure in source trees, environment variables, and log lines. The estate already has one confirmed instance of this — cascade-mac PR#1 (2026-06-24) documented that DeepSeek and Moonshot API keys had been staged in local repo trees. Dynamic, short-lived credentials eliminate this class of exposure by generating credentials on demand and revoking them after TTL expiry.

Infisical (MIT-licensed, [positioned against Vault](https://infisical.com/compare/infisical-vs-hashicorp-vault) as "security through simplicity") is the right choice for an estate at this scale: self-hosted, PostgreSQL-backed (stateless app layer, same ops model as Cove), native RBAC, audit logging, and 60+ integrations. Vault requires a dedicated "Vault engineer" operational posture that a single-operator estate cannot sustain.

The observability plane follows the same logic. [Sigstore/Rekor](https://docs.sigstore.dev/logging/overview/) (CNCF project) implements an append-only tamper-evident transparency log for the software supply chain — Vellum already implements the same pattern for Amplified's epistemic and action events. [immudb](https://immudb.io) (Apache 2.0) and [RFC 9162 Certificate Transparency](https://www.rfc-editor.org/info/rfc9162) establish the same architectural requirement: every security-relevant event must be written to an append-only ledger that external auditors can verify. Vellum is that ledger; it just needs every security event wired into it.

**Verdict on the framing question:** One identity plane + one observability plane. Not federated mesh. This is not a preference; it is the only shape that prior art consistently validates for estates with confirmed credential-leakage history.

---

## The estate today

| Service | Auth model today | Infisical adoption | OTel / Vellum telemetry | Status |
|---|---|---|---|---|
| infisical container | Self (bootstrap) | Source | None | 🟡 Amber — up, underadopted |
| amplified-crm (8001) | Unknown / local-only | None | None | 🔴 Red — no secrets plane |
| amplified-crm-dev (8003) | Unknown / local-only | None | None | 🔴 Red — no secrets plane |
| cove-postgres | DB password (env) | None | None | 🔴 Red — static credential |
| cove-temporal (7233) | JWT / env | None | None | 🔴 Red — static credential |
| cove-api (8081) | JWT | None | None | 🔴 Red |
| cove-translator (8092) | Unknown | None | None | 🔴 Red |
| cove-heal-watchdog | Internal | None | None | 🟡 Amber — healthy but no audit |
| perplexity-ingest | Bearer token (env PERPLEXITY_INGEST_TOKEN) | None | None | 🔴 Red — static token in env |
| research-pipe | Varies | None | Partial | 🟡 Amber |
| brain-mcp-writer | Bearer (own model) | None | None | 🔴 Red |
| brain-mcp-readonly | Bearer (own model) | None | Partial | 🟡 Amber |
| plumb-knowledge-http | Unknown | None | None | 🔴 Red |
| token-proxy (8088) | Centralised token flow | Partial intent | None | 🟡 Amber — good skeleton |
| LiteLLM | Static API keys (Claude/GPT/Llama/Qwen) | None | None | 🔴 Red — highest blast radius |
| tailscale | WireGuard + Tailscale coord server | N/A | None | 🟢 Green — network plane healthy |
| vellum (8400/8407) | JWT (Tier-C gate open) | Not sourced | Self (source) | 🟡 Amber — JWT TTL unresolved |
| vellum-mcp (8407) | JWT | Not sourced | None | 🔴 Red |
| Langfuse (up 7d) | Internal | None | Consumes OTel | 🟡 Amber — receiving but not emitting to Vellum |
| Opik (full stack) | Internal | None | Consumes OTel | 🟡 Amber — same |
| MCP servers ×12 | Each own model | None | None | 🔴 Red — worst surface |
| MacAirM5 | OS-level | None | perplexity-inbox only | 🔴 Red — no endpoint sensor |
| WanMin Mac mini | OS-level | None | None | 🔴 Red — no endpoint sensor |
| MacAirM4 | OS-level | None | None | 🔴 Red — no endpoint sensor |
| pre-commit hook (agent-claude) | Git hook | N/A | None | 🟢 Green — 13 patterns active |

Legend: 🟢 = adequate for current state, 🟡 = partial / in-flight, 🔴 = gap requiring remediation.

---

## Infisical adoption plan [T2-moderate]

**Pattern from prior art:** [HashiCorp Vault's AppRole + token-wrapping model](https://www.hashicorp.com/en/resources/secret-zero-mitigating-the-risk-of-secret-introduction-with-vault) solves the "secret zero" problem by bootstrapping each service's identity via a trusted orchestrator (in Amplified's case: the token-proxy container, which already centralises some token flows). The OIDC/JWT path (most dynamic, least static) is the goal state; AppRole with short-lived wrapped tokens is an acceptable interim per [HashiCorp's OIDC with GitHub Actions guide](https://www.hashicorp.com/resources/using-oidc-with-hashicorp-vault-and-github-actions). Infisical supports both.

**Migration order (least-risk first):**

1. **token-proxy** — already a central flow hub; adding Infisical SDK here creates a single injection point without touching any downstream service. No consumer breakage.
2. **perplexity-ingest** — single env var (`PERPLEXITY_INGEST_TOKEN`); known location, known owner. Replace env var with Infisical SDK call at startup. Low consumer count.
3. **research-pipe** — partial telemetry already; auth model is reachable. Companion synthesis: see research-pipe-prior-art-synthesis__agent__v01__2026-06-25.
4. **brain-mcp-writer / brain-mcp-readonly** — both need bearer rotation; Infisical dynamic secret for each. Companion synthesis: see ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.
5. **LiteLLM** — highest blast radius (four model-provider keys). Migrate last among pipes because a LiteLLM restart propagates to every agent. Plan for dual-key overlap window (see §Key rotation policy).
6. **cove-temporal / cove-api / cove-translator** — Temporal JWT and DB passwords become Infisical dynamic secrets. Cove restart requires coordinated window.
7. **amplified-crm / amplified-crm-dev** — stable, local-only; migrate after Cove to avoid simultaneous downtime.
8. **MCP servers ×12** — large surface, heterogeneous auth. Batch by risk: vellum-mcp and beast-control-mcp first (highest privilege), then claude-*/codex-* batch, then grok-* batch.
9. **Mac endpoints (M5 / Mac mini / MacAirM4)** — agent processes on Mac read secrets via Infisical SDK over Tailscale (already the network plane). LaunchDaemon loads SDK at boot.
10. **vellum itself** — last, because it is the audit record; its own credentials must not be disrupted mid-migration.

**Key adoption constraint:** Infisical is self-hosted on Beast (port 8403). All services that need secrets must be reachable to Beast via Tailscale. This is already satisfied for all listed services.

---

## Key rotation policy [T2-moderate]

Prior art basis: [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) (May 2020) defines cryptoperiods for each key type. [PCI-DSS Requirement 3](https://www.pcisecuritystandards.org/document_library/) (cryptographic key management) mandates documented rotation periods. [CISA guidance](https://www.cisa.gov) on key rotation cadence aligns with NIST for API keys: treat them as symmetric authentication keys, cryptoperiod ≤2 years, rotate immediately on any compromise signal.

| Key class | Recommended TTL | Prior-art basis | Notes |
|---|---|---|---|
| Production model API keys (Claude, GPT, Llama, Qwen in LiteLLM) | 90 days | NIST SP 800-57 §5.3.5 (symmetric auth key, ≤2yr; tighten for high-blast keys) | Dual-key overlap: 7-day window |
| Ephemeral CI tokens (GitHub PATs used in Actions) | 24 hours or per-job | NIST SP 800-57 §5.6 (session keys: single session only) | Use OIDC if possible to eliminate static token |
| mTLS certs (if SPIRE or Infisical PKI used) | 1 hour (SVID default) | [SPIRE defaults](https://spiffe.io/docs/latest/spire-about/use-cases/): 1-hour SVIDs, auto-rotated at 50% window | SPIRE renews at 30 min |
| MCP bearer tokens | 30 days | NIST SP 800-57 §5.3 (asymmetric auth key ≤1yr; tighten to monthly for bearer tokens with large surface) | Infisical dynamic secret with 30-day TTL |
| Vellum JWT | **30 days** | See below | Open Tier-C gate — recommend close at 30d |
| Infisical service tokens (per-service) | 90 days | NIST SP 800-57 §5.3.5; rotate on any Infisical container restart or upgrade | Store disablement secrets in 1Password |
| Tailscale auth keys | Per machine, 90 days | [Tailscale docs](https://tailscale.com/docs/features/access-control/acls): reusable auth keys expire; non-reusable preferred | Use Tailnet lock to prevent rogue node addition |

**Vellum JWT TTL — explicit answer to the open Tier-C gate:**
The current gate reads "vellum-jwt-recovery (TTL + Infisical decision pending)". Prior-art justification for 30 days: NIST SP 800-57 recommends ≤2 years for symmetric authentication keys, but Vellum is the immutable audit ledger (the highest-sensitivity internal service). Shorter is better; 30 days matches the MCP bearer token class. This is short enough to limit exposure if the JWT is intercepted, long enough to avoid operational breakage from missed rotation. Store the JWT in Infisical with a 30-day TTL and Infisical alerts on expiry minus 7 days. Close the Tier-C gate with this value.

**Dual-key overlap window pattern:**
From [HashiCorp Vault dynamic credential guidance](https://developer.hashicorp.com/vault/tutorials/get-started/understand-static-dynamic-secrets): during rotation, both old and new credentials are valid for an overlap window. For model API keys (Claude, GPT), the overlap window is 7 days: new key provisioned on day 0, old key revoked on day 7. This prevents the "rotation breaks consumers" anti-pattern where LiteLLM routes calls to an already-revoked key mid-request.

---

## Service identity [T2-moderate]

**The question:** Should every Amplified service get a [SPIFFE-style identity](https://spiffe.io/docs/latest/spire-about/use-cases/) (X.509-SVID issued by SPIRE), or is Tailscale-derived identity sufficient?

**Prior art on SPIRE:**
[SPIFFE/SPIRE](https://tag-security.cncf.io/community/assessments/projects/spiffe-spire/self-assessment/) (CNCF Graduated) issues short-lived X.509-SVIDs (1-hour default, auto-rotated) that enable workload-to-workload mTLS without any stored secret. At Google, Uber, Netflix scale this is the canonical solution. However, a [2026 practitioner analysis](https://aembit.io/blog/everyone-wants-spiffe-almost-no-one-can-afford-to-build-it-right/) documents that a production-grade SPIRE deployment requires 6–12 months and a dedicated ops team: SPIRE Server in HA mode, SPIRE agents on every node, PostgreSQL or MySQL datastore, Envoy sidecars for mTLS at network layer, SPIFFE-helper for legacy apps, cert-manager for non-SPIRE certificates. "Most teams underestimate it by a year and two engineers."

**Prior art on Tailscale identity:**
[Tailscale's zero-trust model](https://tailscale.com/blog/security-productivity-and-ztna-with-tailscale-enterprise) derives identity from the WireGuard keypair and the identity provider (IdP) authentication. [Tailnet Lock](https://tailscale.com/docs/features/tailnet-lock) adds cryptographic node signing so no new node can join without a trusted existing node's endorsement — even if Tailscale's coordination server is compromised. This is functional SPIFFE-at-the-network-layer without the operational overhead.

**Recommendation for <100 services, single operator:**
Tailscale-derived identity as the network and node identity layer; Infisical service tokens as the secrets identity layer. This combination covers the estate adequately: every service on a Tailscale-assigned IP has a node identity (Tailnet Lock enforced), and every service's secrets are accessed via an Infisical service token (short-lived, per-service). Full SPIRE deployment is premature at this scale and would consume disproportionate operator time. Revisit SPIRE when the estate exceeds 100 services or when a regulated customer requires SPIFFE-attested workload identity in an SLA.

**NIST SP 800-207A** ([September 2023](https://csrc.nist.gov/pubs/sp/800/207/a/final)) explicitly supports this: "network-tier policies must be augmented with identity-tier policies" — Tailscale provides the network tier, Infisical provides the identity tier for secrets access. The combination satisfies ZTA requirements without full SPIRE.

---

## Vellum as the immutable audit ledger [T2-moderate]

**Prior-art lineage:**
- [Sigstore/Rekor](https://github.com/sigstore/rekor): append-only tamper-evident ledger for software supply chain metadata. Auditors verify consistency proofs; entries are never mutated or removed. Vellum implements this same append-only pattern for Amplified operational events.
- [RFC 9162 Certificate Transparency Version 2.0](https://www.rfc-editor.org/info/rfc9162) (December 2021): CAs submit certificates to append-only logs; TLS clients can verify inclusion proofs. The structural parallel: every Infisical secret read, rotation event, and revocation must appear in Vellum's evidence log — the same way every certificate issuance must appear in a CT log.
- [immudb](https://immudb.io) (Apache 2.0, Merkle-tree backed): demonstrates that cryptographic append-only semantics do not require blockchain overhead. Vellum's evidence directory at `/opt/amplified/vellum/evidence/entries/` is the local implementation of this pattern.

**What Vellum currently receives:** Validation failures, threshold crossings, API/schema failures, stalled Cove tasks, agent-loop excess, context-threshold reached, anonymisation failure, tier demotion, contradiction detection, telemetry gaps, handoff lifecycle.

**What Vellum must additionally receive (security events):**

| Event class | Source | Current status |
|---|---|---|
| Secret read (any service reads from Infisical) | Infisical audit log → Vellum | Not wired |
| Secret rotation completed | Infisical → Vellum | Not wired |
| Key revocation | Infisical → Vellum | Not wired |
| Pre-commit scan blocked commit | git hook → Vellum | Not wired |
| Pre-commit scan found secret in history | git hook → Vellum | Not wired |
| Infisical service token issued or revoked | Infisical → Vellum | Not wired |
| Tailnet Lock node signing event | Tailscale → Vellum | Not wired |
| Falco alert (container threat detection) | Falco → Vellum | Not wired |
| Santa blocked binary (Mac endpoints) | osquery/Santa → Vellum | Not wired |
| MCP bearer token rotation | Per-MCP → Vellum | Not wired |
| Vellum JWT rotation | Internal → Vellum | Not wired |

Every one of these is a security boundary crossing. The immutability guarantee is only meaningful if the ledger is complete.

---

## The sensor mesh [T2-moderate]

### Beast (container runtime)

**Falco** (CNCF Graduated, [production-ready in 2026](https://www.securitytoday.de/en/2026/05/14/ebpf-kubernetes-runtime-detection/)): monitors syscalls and container behaviour via eBPF probes. Standard rule set catches 60–80% of MITRE ATT&CK-for-Container techniques out of the box. Relevant rules for the Amplified stack: container attempting to read `/etc/passwd` or Infisical-related paths, unexpected outbound connections from cove-temporal or LiteLLM, processes spawning shells inside MCP server containers. Falco emits structured JSON events → Vellum writer via HTTP POST.

**Cilium Tetragon** (complementary to Falco): full process genealogy and real-time enforcement. Use in the `infisical`, `vellum`, and `litellm` containers specifically — the three highest-sensitivity surfaces. Tetragon can block a forbidden syscall in the kernel before it completes; Falco only detects after the fact.

**Feed path:** Falco/Tetragon events → OTel Collector (running on Beast) → Langfuse (for ML-context traces) + Opik (for agent traces) + Vellum (for the immutable audit ledger). This satisfies the OTel convergence pattern per the [OpenTelemetry logging specification](https://opentelemetry.io/docs/specs/otel/logs/): logs, traces, and metrics all carry the same resource attributes and can be correlated by `service.name`.

### M5 + Mac mini + MacAirM4 (Mac endpoints)

**osquery** ([Trail of Bits / open source](https://blog.trailofbits.com/2021/11/10/announcing-osquery-5-now-with-endpointsecurity-on-macos/)): v5 introduced EndpointSecurity-based `es_process_events` on macOS, replacing the deprecated kauth framework. Install as LaunchDaemon on each Mac. Queries of interest: process execution events, network connections, user logins, file access on sensitive paths (`~/.op-sa-token`, Infisical SDK config files, `.env` files).

**Santa** ([now Northpole Security fork](https://osmachine.com/baseline/workstations/macos-workstations/santa-application-control)): binary authorization. In MONITOR mode initially: all executions logged, unknown or denied binaries stored for aggregation. LOCKDOWN mode is the goal state for Mac mini (always-on, lower human-intervention requirement). Santa + osquery integration via the [Trail of Bits osquery extension](https://github.com/trailofbits/osquery-extensions/blob/master/santa/README.md) gives SQL-queryable `santa_denied` and `santa_allowed` tables.

**Mac mini as central sensor:** The WanMin Mac mini (M4 Pro) is always-on, unlike the M5 and MacAirM4 which are carried. This makes it the natural edge sensor: osquery daemon on Mac mini aggregates its own events AND acts as the syslog/OTel receiver for the other two Macs when they are on the same Tailnet. LaunchDaemon plist at `/Library/LaunchDaemons/com.amplified.osquery.plist` (startup: `osqueryd --flagfile /etc/osquery/osquery.flags`). Events → OTel Collector → Vellum.

### Network plane

**Tailscale ACL events:** Tailscale's policy file changes (adds, removes, ACL modifications) must be version-controlled (GitOps) and each change emitted as a Vellum event. [Tailscale supports GitOps for ACLs](https://tailscale.com/docs/features/access-control/acls). Commit hook triggers Vellum write.

**Tailnet Lock node signing:** Every new node signing event (Beast approving M5, Mac mini approving a new container) should emit a Vellum event. This is the network-identity equivalent of a certificate issuance event in a CT log.

### Pipes (perplexity-ingest, research-pipe, plumb-knowledge-http)

Each pipe must emit Vellum events on: every request received (event class: `ingest_request`), every secret access (event class: `secret_read`), every gate decision (event class: `gate_decision`). This extends the existing sensor catalogue from the control-centre synthesis. The in-process sensor pattern is: before returning from any request handler, call `vellum_write(event_type, payload, source_service)`. The Vellum client must be embedded in each pipe's SDK dependencies, not called via HTTP side-channel (to prevent the pipe discipline "secrets via pipe, never side-door" constraint from being violated for Vellum calls themselves).

### CRM, cove-temporal, cove-api

[OpenTelemetry SDK](https://opentelemetry.io/docs/concepts/semantic-conventions/) instrumentation: add OTel SDK to each service's runtime. Use standard semantic conventions: `service.name=amplified-crm`, `service.version`, `deployment.environment.name=production`. Export to OTel Collector on Beast, which routes: traces → Langfuse (ML context), metrics → Opik (agent observability), security events → Vellum. The OTel Collector's `resource detection processor` adds infra metadata (host, container ID) automatically — no manual enrichment needed.

---

## Pre-commit and pre-push hooks [T2-moderate]

**cascade-mac PR#1 baseline** (2026-06-24): 13 secret patterns active on agent-claude repo: Anthropic/DeepSeek/Moonshot/OpenAI `sk-*` keys, GitHub `gho_`/`ghp_`, AWS `AKIA`, Linear keys, PEM blocks.

**Generalise to every repo in the estate:**

Pattern from [secret scanning tool comparison](https://rafter.so/blog/secrets/secret-scanning-tools-comparison): Gitleaks is the correct pre-commit tool (fast, offline, broad 150+ rule set), TruffleHog for scheduled CI full-history sweeps with `--only-verified` (confirms which findings are active, drives rotation priority). Per [secrails.com analysis](https://secrails.com/blog/trufflehog-vs-gitleaks-github-secret-scanning-guide): "Gitleaks is the best tool for pre-commit enforcement; TruffleHog is the best tool for verified, actionable findings in CI/CD."

**Three additional hook layers on top of the existing secret scanner:**

1. **Dependency CVE scan:** `pip-audit` (Python) or `npm audit` (Node) as a pre-push hook. Flags known CVEs in dependencies before code reaches Beast. Tool: [pip-audit](https://github.com/pypa/pip-audit) for Python services (cove-api, brain-mcp-*, perplexity-ingest).

2. **Dynamic-secret check (no static creds in code paths):** Custom hook that searches staged files for any reference to an API key variable assigned a literal value (regex: `(ANTHROPIC|OPENAI|DEEPSEEK|MOONSHOT|GITHUB)_.*=\s*["'][a-zA-Z0-9_\-]{20,}["']`). This is distinct from the existing entropy scanner — it targets assignment patterns specifically.

3. **Infisical-reference enforcement:** Hook that warns if a service reads a secret via a mechanism other than the Infisical SDK (e.g., `os.environ.get('SOME_KEY')` in Python without a corresponding Infisical client call). This is a soft block: warn on violation, require explicit override comment to bypass. Enforces the pipe discipline: "code reads via SDK only."

**Hook deployment matrix:**

| Repo | Current state | Target state |
|---|---|---|
| agent-claude | 13 patterns active | Add CVE scan + Infisical enforcement |
| awesome-openclaw-agents | Unknown | Full hook suite |
| clean-build | Unknown | Full hook suite |
| Any repo with cove-* services | Unknown | Full hook suite |
| Any repo with MCP server code | Unknown | Full hook suite |

---

## Breach response playbook [T2-moderate]

**Prior-art basis:** [NIST SP 800-61 r3](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf) (April 2025, supersedes r2): Prepare → Detect → Analyse → Contain → Eradicate → Recover → Post-Incident. [SANS PICERL](https://www.sans.org/white-papers/33901/): Prepare, Identify, Contain, Eradicate, Recover, Lessons Learned. Both frameworks converge on the same sequence; NIST r3 aligns explicitly with CSF 2.0 Functions.

**Amplified-specific preconditions:**
- Known historical breach signal: DeepSeek and Moonshot keys were in staged local repo trees (cascade-mac PR#1, 2026-06-24). Those keys must be treated as compromised regardless of whether they were pushed to remote.
- Vellum is the forensic record. Before any containment action, read the Vellum evidence log for the affected service's recent events to establish a baseline of what was normal before the incident.
- Tailscale is the network isolation plane. Container isolation = remove the container's Tailscale tag from the ACL policy.

### First 10 minutes

1. Identify the signal source: Falco alert, pre-commit block, Vellum anomaly, external notification.
2. Open `/opt/amplified/vellum/evidence/entries/` and read the last 50 events for the affected service. Establish the blast-radius perimeter.
3. If LiteLLM model keys are implicated (DeepSeek, Moonshot confirmed; Claude/GPT/Llama/Qwen potential): immediately revoke the affected key at the provider console (Anthropic dashboard, OpenAI dashboard, DeepSeek portal). Do not wait for Infisical rotation — manual revocation first, then Infisical update.
4. If GitHub PATs are implicated: revoke at github.com/settings/tokens immediately. PAT revocation is instant and does not break pull operations (only push and API calls).
5. Set Tailscale ACL to isolate the affected container's tag: add `deny` rule for all traffic to/from the affected container's tag.
6. Write a Vellum event: `incident_declared`, recording: affected service, signal source, timestamp, operator identity.

### First 1 hour

6. Rotate in priority order (per NIST SP 800-61 r3 §RS.MI: "mitigate effects, prevent expansion"):
   a. LiteLLM model keys (Claude, GPT, Llama, Qwen) — highest blast radius, directly fund further attacks if compromised.
   b. GitHub PATs — control source tree; a compromised PAT allows injecting new secrets into repos.
   c. MCP bearer tokens — 12 servers, each a potential pivot point.
   d. Infisical service tokens — if Infisical itself is implicated, rotate the master token and re-bootstrap each service.
   e. Vellum signing keys — last, only if Vellum is directly implicated.
7. Deploy dual-key overlap window: new keys provisioned in Infisical, services restarted to load new keys, old keys revoked after 7-day overlap (or immediately if active exfiltration is confirmed).
8. Run `trufflehog git file://. --only-verified` on all local repos to enumerate which credentials are still active. Each verified finding requires immediate rotation.
9. Check Tailnet Lock signing log for any unauthorised node additions in the past 24 hours.
10. Write Vellum events: `key_rotation_completed` for each key class rotated.

### First 24 hours

11. Full Vellum audit: query all `secret_read` events for the affected service over the past 30 days. Identify any anomalous access patterns (time of day, volume, IP) that Falco/Tailscale logs can corroborate.
12. MITRE ATT&CK mapping: classify the incident by technique (T1552 — Unsecured Credentials; T1078 — Valid Accounts; T1567 — Exfiltration Over Web Service). Document in Vellum.
13. Post-incident: run the full hook suite on all repos (Gitleaks full-history scan + TruffleHog verified sweep). Produce a written summary of what the pre-commit hook would have blocked if deployed earlier (the cascade-mac PR#1 model).
14. Update the Infisical migration order: any service implicated in the incident moves to position 1 in the migration queue, overriding the least-risk-first sequence.

---

## What sensors must report and where [T2-moderate]

| Sensor source | Event class | Primary destination | Secondary destination |
|---|---|---|---|
| Falco (Beast containers) | Container escape attempt, privilege escalation, unexpected shell, forbidden file access | Vellum (immutable audit) | Langfuse (agent context) |
| Tetragon (Beast, high-sensitivity containers) | Syscall enforcement action, process genealogy anomaly | Vellum | Beast system log |
| osquery (M5, Mac mini, MacAirM4) | Process execution, network connection, file access on sensitive paths | Vellum | Opik (if agent-triggered) |
| Santa (Mac mini primary) | Binary denied execution, binary allowed (forensic) | Vellum | osquery `santa_denied` table |
| Tailscale ACL change | Policy file commit, node signing, node removal | Vellum | GitHub (GitOps commit log) |
| Infisical audit log | Secret read, secret write, token issued, token revoked, rotation completed | Vellum | Internal Infisical log |
| Pre-commit hook | Secret blocked in staged files, dependency CVE found, Infisical violation | Vellum | Console output (developer) |
| TruffleHog CI sweep | Verified active credential in repo history | Vellum | Linear ticket (via hook) |
| cove-temporal / cove-api | Workflow started, workflow failed, stalled task | Langfuse (primary) + Vellum (if security gate hit) | Opik |
| amplified-crm / amplified-crm-dev | Request received, auth failure, DB query | Opik (primary) | Vellum (if auth failure) |
| LiteLLM | Model route decision, key used, error returned | Langfuse (primary) | Vellum (if key rotation event) |
| perplexity-ingest | Request received, secret accessed, gate decision | Vellum | Langfuse |
| brain-mcp-writer / brain-mcp-readonly | Write operation, read operation, auth event | Vellum | Opik |
| MCP servers ×12 | Auth challenge, bearer token used, connection established | Vellum | Langfuse (if agent-triggered) |
| Vellum itself | JWT rotation, signing key rotation | Internal self-log | 1Password (disablement record) |

---

## Open questions and contradictions [T2-moderate]

**1. SPIRE vs Tailscale-identity for service-to-service auth:**
SPIFFE/SPIRE provides cryptographically attested workload identity independent of the network — theoretically stronger than Tailscale-derived identity (an attacker with Tailscale coordination server access could theoretically reroute traffic). However, [Tailnet Lock](https://tailscale.com/blog/tailnet-lock) mitigates the coordination-server trust issue by requiring node-signed endorsement. The practical contradiction: SPIRE takes 6–12 months to operationalise correctly for a single engineer; Tailscale + Infisical takes days. The recommendation above (Tailscale-derived) accepts a small theoretical gap in exchange for actual deployment. This is a documented trade-off, not an oversight.

**2. Mac mini as central sensor vs. all three Macs as peers:**
Prior art (osquery's fleet model; Wazuh's distributed agent model) supports both topologies. Peer topology means each Mac independently forwards events to Vellum. Central sensor topology means Mac mini aggregates M5 and MacAirM4 events when they are on Tailnet. Contradiction: if M5 is off Tailnet (away from desk), its events queue locally and flush on reconnect — this creates a telemetry gap for the period it is offline. The recommendation (Mac mini as central sensor) accepts this gap for M5/MacAirM4 in exchange for simpler Vellum writer management. Open question for Ewan: is the telemetry-gap for M5 when away from Tailnet acceptable, or should M5 always forward directly to Vellum regardless of Mac mini availability?

**3. Where the prior art disagrees — static vs dynamic secrets for LiteLLM:**
[HashiCorp Vault dynamic credentials](https://developer.hashicorp.com/hcp/docs/vault-secrets/dynamic-secrets) are ideal for database credentials (LiteLLM does not hold database credentials). For third-party model API keys (Anthropic, OpenAI, DeepSeek, Moonshot), there is no "dynamic secret" equivalent — the provider issues a static key, and the best the estate can do is rotate it on a defined schedule via Infisical's auto-rotation feature. This is a fundamental limit of the provider's API surface, not a design gap in Amplified's approach. It is documented here so that future model-provider selection considers whether the provider supports dynamic API key issuance (none currently do at the consumer tier as of 2026-06-25).

---

## Outcome routing

```yaml
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  route_to: Ewan / relay-protocol
  baton_actions:
    - close_tier_c_gate: "Vellum JWT TTL → 30 days (justified above)"
    - decide: "SPIRE vs Tailscale-identity (recommendation: Tailscale-derived, justified above)"
    - decide: "Mac mini central sensor vs peer topology (recommendation: central sensor, justified above)"
    - prioritise: "LiteLLM key migration to Infisical (highest blast radius)"
    - deploy: "Falco on Beast (CNCF-graduated, production-ready 2026)"
    - deploy: "osquery + Santa on Mac mini as first Mac endpoint sensor"
    - wire: "Infisical audit log → Vellum"
    - wire: "Pre-commit hook events → Vellum"
  block_conditions:
    - "Do not auto-rotate LiteLLM model keys without confirming dual-key overlap window is ready"
    - "Do not deploy SPIRE without Ewan explicit decision — it is a 6–12 month commitment"
    - "Do not migrate Vellum itself to Infisical before all other services are migrated (Vellum is the audit record)"
```

---

## Cross-references

- research-pipe-prior-art-synthesis__agent__v01__2026-06-25: covers the pipe discipline (secrets via pipe, never side-door) that informs the Infisical adoption order and the in-process Vellum sensor pattern for perplexity-ingest and research-pipe.
- ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25: covers provenance, tiering, and the brain-mcp-writer/readonly auth model that requires Infisical migration in step 4 above.
- data-lake-prior-art-synthesis__agent__v01__2026-06-25: covers the cove-postgres data-lake pattern; the Infisical migration for cove-temporal/cove-api/cove-postgres (step 6 above) must coordinate with data-lake schema freeze windows documented in that synthesis.
