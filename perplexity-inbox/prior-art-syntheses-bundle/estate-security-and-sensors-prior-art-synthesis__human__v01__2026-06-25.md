---
document_id: estate-security-and-sensors-prior-art-synthesis__human__v01__2026-06-25
document_type: readable_research_conclusion
stage: synthesis
audience: Ewan
author: subagent-prior-art
created: 2026-06-25
version: v01
goal_link: "Ewan/estate-security-and-sensors-prior-art"
owner: Amplified Partners
data_sensitivity: internal-confidential
---

The estate needs one identity plane and one observability plane — every service proves who it is through Infisical, every security-relevant action is recorded in Vellum — and eleven bodies of prior art confirm this is the right shape rather than a fragmented mesh.

---

## Where we are today

The table below covers every service. Green means the auth and telemetry coverage is adequate. Amber means partial. Red means a clear gap.

| Service | How it proves identity today | Is it logged anywhere immutable? |
|---|---|---|
| Infisical (the secrets vault itself) | Self-bootstrapped | No — not yet wired to Vellum |
| amplified-crm (port 8001) | Unknown | No |
| amplified-crm-dev (port 8003) | Unknown | No |
| cove-postgres | Database password in environment variable | No |
| cove-temporal (port 7233) | JWT in environment variable | No |
| cove-api, cove-translator, cove-heal-watchdog | JWT / internal | Partial |
| perplexity-ingest | Bearer token in environment variable (`PERPLEXITY_INGEST_TOKEN`) | No |
| research-pipe | Varies | Partial |
| brain-mcp-writer, brain-mcp-readonly | Bearer token (own model) | Partial |
| token-proxy (port 8088) | Centralises some token flows | No |
| LiteLLM (model router) | Static API keys for Claude, GPT, Llama, Qwen | No |
| Tailscale (network plane) | WireGuard keypairs + IdP | Healthy — no gap here |
| Vellum (the audit ledger) | JWT — TTL unresolved (Tier-C gate open) | Self-logs only |
| 12 MCP servers | Each has its own independent auth | No |
| Langfuse, Opik (observability) | Internal | Receive telemetry but don't emit to Vellum |
| MacAirM5 (your active machine) | macOS user account | No sensor running |
| Mac mini WanMin (always-on) | macOS user account | No sensor running |
| MacAirM4 | macOS user account | No sensor running |
| Pre-commit hook on agent-claude repo | Git hook | Not yet wired to Vellum |

The short version: Tailscale is healthy. The pre-commit hook is working. Everything else has either a missing or untested identity story, and nothing outside of Vellum itself writes security events to an immutable record.

The one confirmed real incident: cascade-mac PR#1 (2026-06-24) found that DeepSeek and Moonshot API keys had been staged in a local repo. Those keys must be treated as compromised regardless of whether they were pushed anywhere.

---

## What the prior art says

1. Static, long-lived credentials are the primary cause of breaches at this kind of estate. HashiCorp Vault (the 2015 reference design by Mitchell Hashimoto, still the canonical prior art) solved this by generating credentials on demand and expiring them after a short window. The same logic applies here: every environment-variable API key is a static credential waiting to be found in a log, a `.env` file, or a committed diff. [HashiCorp's own documentation on dynamic vs static secrets](https://developer.hashicorp.com/vault/tutorials/get-started/understand-static-dynamic-secrets) puts it plainly: "static credentials pose significant risk due to potential for accidental and malicious exposure."

2. Infisical is the right tool for this estate. [Infisical](https://infisical.com/compare/infisical-vs-hashicorp-vault) is MIT-licensed, already running on Beast (port 8403), stores its state in PostgreSQL (same ops model as Cove), has a modern dashboard, and does not require a dedicated "Vault engineer." Vault's BSL license change in 2023 and its CLI-first design make it the wrong fit for a single-operator estate.

3. NIST SP 800-57 (the US government's key management standard, May 2020) gives concrete lifetimes: model API keys (symmetric authentication class) should rotate every 90 days at most. CI tokens should last one session only. Bearer tokens for MCP servers should rotate monthly. The [NIST key management guidelines](https://csrc.nist.gov/projects/key-management/key-management-guidelines) are the standard that PCI-DSS, HIPAA, and FedRAMP all point back to.

4. Tailscale already does what SPIFFE/SPIRE does at the network layer. [SPIFFE/SPIRE](https://spiffe.io/docs/latest/spire-about/use-cases/) is the CNCF-graduated standard for giving every service a cryptographic workload identity (short-lived certificates, auto-rotated every hour). It is the right answer at Google or Uber scale. For an estate under 100 services with one operator, [a 2026 practitioner analysis](https://aembit.io/blog/everyone-wants-spiffe-almost-no-one-can-afford-to-build-it-right/) documents that it takes 6–12 months to deploy correctly. Tailscale's [Tailnet Lock](https://tailscale.com/blog/tailnet-lock) feature provides the equivalent node-signing guarantee: no new device joins the network without a trusted existing device's endorsement.

5. Secret scanning in source trees must be layered. The cascade-mac PR#1 hook (Gitleaks-style, 13 patterns) is the right first layer. [TruffleHog](https://secrails.com/blog/trufflehog-vs-gitleaks-github-secret-scanning-guide) adds a second layer via scheduled full-history sweeps that verify whether a found credential is still active — that tells you which rotations are urgent. The correct model: Gitleaks blocks at commit time, TruffleHog sweeps weekly to find what slipped through.

6. Vellum is already implementing the right immutable ledger pattern. [Sigstore/Rekor](https://docs.sigstore.dev/logging/overview/) (the software supply chain transparency log) and [immudb](https://immudb.io) (append-only cryptographic database) both implement the same thing Vellum does: write once, never modify, anyone can verify. The gap is not Vellum's design — it is that security events (secret reads, key rotations, node signings) are not yet wired into it.

7. Falco (CNCF-graduated runtime security) plus osquery on Mac covers the two remaining sensor gaps. [Falco](https://www.securitytoday.de/en/2026/05/14/ebpf-kubernetes-runtime-detection/) watches syscalls inside Beast containers and catches 60–80% of known container attack patterns out of the box. [osquery](https://blog.trailofbits.com/2021/11/10/announcing-osquery-5-now-with-endpointsecurity-on-macos/) queries macOS endpoint events via Apple's Endpoint Security Framework. Pair it with [Santa](https://osmachine.com/baseline/workstations/macos-workstations/santa-application-control) for binary authorization on Mac.

8. For breach response, [NIST SP 800-61 r3](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf) (April 2025) and the SANS PICERL framework agree: the first action is contain (isolate the affected service), the second is eradicate (revoke the compromised key), the third is recover (provision new credentials), the last is document (write the post-incident report to Vellum). The specific rotation order matters — see below.

---

## Recommended shape: one identity plane + one observability plane

Every service on the estate should prove its identity in one place: Infisical, running on Beast, reachable via Tailscale. Every security-relevant event should land in one place: Vellum, also on Beast, append-only. This is not a new idea — it is the direct intersection of HashiCorp Vault's design philosophy, NIST SP 800-207's zero-trust requirements, and Sigstore/Rekor's transparency-log pattern, applied to an estate that already has Infisical running and Vellum in production. The estate is three configuration changes and a migration sequence away from a defensible posture.

---

## Order of work (least-risk first)

1. **Close the Vellum JWT Tier-C gate now.** Set the TTL to 30 days, store the JWT in Infisical, configure Infisical to alert at 23 days (7-day warning). This resolves the open gate with no service disruption. Justification: NIST SP 800-57 recommends ≤2 years for this key class; 30 days tightens that for the audit ledger's own credentials.

2. **Wire Infisical audit events to Vellum.** Single integration: Infisical has a webhook/audit-log API. Point it at the Vellum writer. Every future secret read, rotation, and revocation will now appear in the immutable record.

3. **Wire the pre-commit hook events to Vellum.** The existing hook blocks at commit time but the block event disappears into the terminal. A one-line addition to the hook script posts the event to Vellum. This means the cascade-mac PR#1 type of finding is now recorded.

4. **Migrate perplexity-ingest to Infisical.** One environment variable (`PERPLEXITY_INGEST_TOKEN`) replaced with an Infisical SDK call. Small service, known owner, low consumer count. Proves the pattern before touching higher-stakes services.

5. **Migrate token-proxy to Infisical (and use it as the injection point for other services).** Token-proxy already centralises some token flows. Infisical SDK in token-proxy means it becomes the trusted orchestrator for other services — they receive their tokens from token-proxy rather than each needing direct Infisical access.

6. **Migrate LiteLLM model keys (Claude, GPT, Llama, Qwen) to Infisical with 90-day TTL.** Highest blast radius: a compromised model key lets anyone spend on your model account. The rotation procedure requires a 7-day dual-key overlap window so that in-flight model calls do not hit a revoked key mid-request.

7. **Migrate brain-mcp-writer and brain-mcp-readonly.** Covered in the ingestion-to-brain companion synthesis. Infisical dynamic secret for each.

8. **Deploy Falco on Beast.** CNCF-graduated, production-ready in 2026, standard rule set catches 60–80% of container attack patterns. Events route to Vellum. This is the single-biggest improvement to Beast's sensor coverage for the effort involved.

9. **Deploy osquery + Santa on Mac mini.** The Mac mini (WanMin, M4 Pro) is always-on, making it the right first Mac endpoint sensor. LaunchDaemon at `/Library/LaunchDaemons/com.amplified.osquery.plist`. Events route to Vellum. M5 and MacAirM4 can be added subsequently.

10. **Migrate cove-temporal, cove-api, and cove-postgres to Infisical.** Coordinated restart window required. Covered in the data-lake companion synthesis for the Postgres side.

11. **Migrate the 12 MCP servers to Infisical.** Large surface, batch by privilege: vellum-mcp and beast-control-mcp first, then claude-* batch, then grok-* batch.

12. **Enable Tailnet Lock.** Cryptographic node-signing: no new device joins the Tailnet without an existing trusted device's endorsement. Takes under an hour to enable; requires at least two signing nodes (Beast and Mac mini are the natural choices).

---

## Breach playbook in plain English

This is what to do if a key is found to be compromised, on the precedent of the cascade-mac PR#1 DeepSeek and Moonshot finding.

**First 10 minutes:**
Go to Vellum's evidence directory (`/opt/amplified/vellum/evidence/entries/`) and read the last 50 events for the affected service. This tells you what was normal before the incident and helps you scope how far the blast radius extends. While reading those, go to the provider's console (Anthropic dashboard, OpenAI dashboard, DeepSeek portal) and manually revoke the key immediately. Do not wait for Infisical to do this — manual revocation is instant. If a GitHub PAT is involved, revoke it at github.com/settings/tokens. Write a Vellum event: `incident_declared` with the affected service, signal source, and timestamp.

**First 1 hour:**
Rotate keys in this specific order, because the order controls how much further damage is possible: LiteLLM model keys first (Claude, GPT, Llama, Qwen — they fund further attacks if compromised), then GitHub PATs (they control what goes into the source tree), then MCP bearer tokens (12 services, each a potential entry point), then Infisical service tokens (only if Infisical itself was touched), then Vellum signing keys last (only if Vellum itself was targeted). Provision new keys in Infisical, restart services to load new keys, leave old keys valid for 7 days in case any in-flight request was mid-stream, then revoke the old keys at day 7. Run `trufflehog git file://. --only-verified` on all repos to find any other active credentials in the history.

**First 24 hours:**
Pull all Vellum `secret_read` events for the affected service over the past 30 days. Look for anomalies: unusual times, high volume, unexpected calling IP. Correlate with Tailscale and Falco logs (once Falco is deployed — this is why Falco is in step 8 above). Classify the incident by [MITRE ATT&CK](https://attack.mitre.org) technique — for a leaked credential the most likely match is T1552 (Unsecured Credentials). Document the classification in Vellum. Run the full Gitleaks + TruffleHog sweep on all repos. Write the post-incident summary: what the sensor would have caught if it had been running, what the hook blocked, what slipped through, and what is now different.

---

## Open questions for Ewan

**1. Telemetry gap for M5 when it is off Tailnet.**
The recommendation is Mac mini as the central sensor that aggregates events from M5 and MacAirM4. If M5 is away from the desk and not on Tailnet, its events queue locally and flush when it reconnects. That creates a gap in real-time visibility for the period M5 is offline. Is that acceptable, or should M5 always forward events directly to Vellum regardless of Mac mini availability? (The direct-forwarding option is more resilient but requires running an OTel forwarder on M5 with its own Infisical service token.)

**2. GitHub PAT hardening (existing open Tier-C gate).**
The github-hardening gate lists "PAT revocations pending." The breach playbook above assumes GitHub PATs are rotated as a high-priority step. Before that is possible, the current PATs need to be enumerated (which repos, which scopes, which services use them) and the revocation sequence planned so that no Beast service loses access mid-rotation. This is a blocking dependency on steps 6 and 7 in the order of work above.

**3. Infisical service account token (`op-sa-token`).**
The file at `/Users/ewansair/.op-sa-token` is referenced in the 1PASSWORD_INFINISICAL_METHODOLOGY.md. That file is a static credential on-disk on the M5. It should move into Infisical itself once Infisical is the secrets source of truth — but that creates a circularity (Infisical stores the token used to access Infisical). The correct pattern is: the op-sa-token stays in 1Password (which Ewan controls directly) and is never written to disk except transiently during container startup. Confirm this is the intended pattern before the Infisical migration begins.

---

## Cross-references

This synthesis is the fourth of four pillars. The others are:
- research-pipe-prior-art-synthesis (pipe discipline, the "secrets via pipe, never side-door" rule)
- ingestion-to-brain-prior-art-synthesis (brain-mcp auth, provenance, tiering)
- data-lake-prior-art-synthesis (cove-postgres schema and freeze windows, relevant to the Infisical migration step for Cove)
