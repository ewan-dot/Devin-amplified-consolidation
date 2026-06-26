# Google Cloud SDK & Compute Deep-Dive
### For Amplified Partners Infrastructure — Sovereignty-First AI Stack

*Research completed June 2026. Sources dated 2025–2026.*

---

## Executive Summary

Google Cloud offers genuinely differentiated compute — multi-hundred-GPU clusters, custom TPUs, and GB-scale memory instances that a single 128GB server simply cannot match. The SDK/agent tooling (ADK, Vertex AI Agent Engine) is real, open-source, and model-agnostic. **You can use GCP as pure GPU/CPU compute without touching any managed AI services.** The sovereignty trade-off is manageable but not zero — data traverses Google infrastructure, and Google employees can access it under certain legal and support conditions. The honest answer: GCP makes an excellent burst/overflow layer without compromising your self-hosted core, *as long as you treat it as pure compute and keep sensitive data on-prem.* It does not replace sovereign infrastructure; it extends it.

---

## 1. Compute: What GCP Offers That a 128GB Server Cannot

### The GPU / TPU Ladder (as of mid-2026)

Your 128GB server is excellent for a single-node inference stack. What it cannot do: run a 70B+ parameter model in full precision, fine-tune a 30B+ model in reasonable time, or handle burst loads across parallel agent workloads. GCP's compute tiers address each of these gaps:

| Machine Series | GPU | VRAM per GPU | Max per Instance | Total VRAM | Best For |
|---|---|---|---|---|---|
| A2 High (n1-standard) | NVIDIA A100 40GB | 40 GB HBM2e | 8 | 320 GB | Inference, smaller fine-tune |
| A2 Ultra | NVIDIA A100 80GB | 80 GB HBM2e | 8 | 640 GB | Large model inference, fine-tune |
| A3 High | NVIDIA H100 80GB | 80 GB HBM3 | 8 | 640 GB | Training, fast inference |
| A3 Mega | NVIDIA H100 Mega 80GB | 80 GB HBM3e | 8 | 640 GB | Large-scale training |
| A3 Ultra | NVIDIA H200 141GB | 141 GB HBM3e | 8 | 1,128 GB | Frontier training, inference |
| A4 | NVIDIA B200 | (next-gen Blackwell) | 8 | — | Emerging availability |
| A4X / A4X Max | NVIDIA GB200/GB300 | 186–279 GB HBM3e | 8 | Up to 2,232 GB | Trillion-param MoE models |
| G2 | NVIDIA L4 24GB | 24 GB | 8 | 192 GB | Cost-effective inference |
| N1 + T4 | NVIDIA T4 16GB | 16 GB | 4 | 64 GB | Light inference, lowest cost |

*Source: [Google Cloud GPU machine types documentation](https://docs.cloud.google.com/compute/docs/gpus), retrieved June 2026.*

**TPU options** are Google's proprietary differentiator — no hardware vendor lock, but software ecosystem matters:

| TPU Generation | Key Stats | Status (mid-2026) | Best For |
|---|---|---|---|
| v5e (Trillium-lite) | Cost-optimized inference | GA | High-volume LLM serving |
| v5p | 3,672 TFLOPS, 760 GB/8-chip | GA | Training |
| v6e (Trillium) | 7,344 TFLOPS, 256 GB/8-chip | GA | Inference; Anthropic's primary chip |
| v7x (Ironwood) | 10× peak perf over v5p, 4× over v6e | GA since March 31, 2026 | Large-scale training + inference |

*Source: [Cloud TPU release notes](https://docs.cloud.google.com/tpu/docs/release-notes); [Ironwood GA announcement](https://cloud.google.com/blog/products/compute/ironwood-tpus-and-new-axion-based-vms-for-your-ai-workloads), November 2025.*

**What TPU v6e delivered in practice:** Midjourney cut monthly inference spend from \$2.1M to \$700K migrating from NVIDIA to TPU v6e. Anthropic committed to hundreds of thousands of Trillium chips. The TPU story is real — but only for workloads that run JAX/XLA well or use vLLM's TPU backend (added 2025). *Source: [Introl TPU vs GPU framework, January 2026](https://introl.com/blog/google-tpu-vs-nvidia-gpu-infrastructure-decision-framework-2025).*

### What a 128GB Server Genuinely Cannot Match

1. **Clustered inference at scale.** An 8×H100 A3 instance gives 640 GB of HBM3. To serve Llama 3 405B in FP16 you need ~810 GB VRAM — a 16×H100 configuration or multi-node. Impossible on one server.
2. **Distributed fine-tuning.** Fine-tuning a 70B model with full gradients needs ~560 GB VRAM minimum. On a 128GB-RAM CPU-only server with consumer GPU(s), you're doing quantized fine-tune at best.
3. **Burst handling.** If 20 simultaneous users hit a 70B inference endpoint, you need parallelism. A single server serializes requests; GCP auto-scales.
4. **Networking.** A3 instances use 3,200 Gbps NVLink + high-bandwidth ICI for multi-node jobs. Matching that on-prem requires NVLink Switch infrastructure costing $500K+.
5. **Large-memory CPU instances.** GCP's M3 mega instances go to 30 TB RAM (x4 Intel Xeon, 30,720 GB). Not GPU, but relevant if any analytics workloads need it.

**Autoscaling:** Vertex AI Inference autoscales GPU replicas based on CPU/GPU utilization targets. Default is 60% CPU target. Scale-to-zero (min replicas = 0) is now supported, meaning you pay nothing for idle GPU time. GKE's GPU autoprovisioner (GKE 2025-R43) reduced stabilization time by 40%. *Source: [Vertex AI autoscaling docs](https://cloud.google.com/vertex-ai/docs/predictions/autoscaling); [Usage.ai GCP NVIDIA guide, October 2025](https://www.usage.ai/blogs/gcp/ai-ml-cost/vertex-ai/google-cloud-nvidia-enterprise-ai/).*

---

## 2. The SDK & Agent Tooling: What It Is, What's Genuine

### Google Cloud Agent Development Kit (ADK)

ADK is Google's open-source agent framework. It is genuinely open-source (Apache 2.0), model-agnostic, and deployment-agnostic. The 1.0.0 stable release shipped May 2025; Go SDK launched November 2025; Java 1.0.0 released mid-2026.

**What ADK actually provides:**

- **Model agnosticism.** ADK integrates natively with Gemini but ships with LiteLLM integration — you can route to Anthropic, Meta Llama, Mistral, AI21, or any OpenAI-compatible endpoint, including your self-hosted LiteLLM instance. *Source: [Google Developers Blog, April 9, 2025](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/).*
- **Multi-agent by design.** Sequential, parallel, loop, and graph-based orchestration. Sub-agents, tool delegation, and agent-to-agent (A2A) protocol (standardized inter-framework agent communication launched 2025).
- **Framework interop.** Supports LangChain, LlamaIndex, CrewAI, LangGraph as tools or sub-agents.
- **Deployment agnosticism.** Runs locally, in Docker, on GKE, on Vertex AI Agent Engine, or on any container platform. The framework does not require Google Cloud to run.
- **MCP support.** Model Context Protocol tools work natively.
- **Built-in streaming.** Bidirectional audio/video streaming for real-time agent interaction.
- **Local dev UI.** CLI + browser-based debugging UI, inspect events and state step-by-step.

**ADK 2.0 (I/O '26, May 2026):** Introduced a unified graph-based engine with a "slider" from dynamic LLM-led reasoning to strict deterministic workflows. *Source: [Google Cloud I/O '26 news, May 19, 2026](https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud).*

**Honest assessment:** ADK is a real, well-engineered framework. Its differentiator over LangChain/LlamaIndex is tighter graph-based orchestration and native production deployment to Agent Engine. You already run LiteLLM — ADK can sit on top of it. The Gemini default in code examples is marketing default, not a constraint.

### Vertex AI Agent Engine (managed runtime)

Agent Engine is the hosted managed runtime for deploying ADK agents. What it provides beyond a raw GKE deployment:

- **Serverless deploy.** No container management; pay per request.
- **Sessions** (GA, Feb 2026): Turn-by-turn context persistence.
- **Memory Bank** (GA, Feb 2026): Cross-session persistent memory. \$0.25/1,000 stored memories, \$0.50/1,000 retrievals.
- **Native IAM agent identities** (April 2026): Agents as first-class IAM principals — not shared service accounts. Required for SOC 2/HIPAA audit trails.
- **Observability** (April 2026): Single-pane dashboard for latency, token consumption, error rates.
- **A2A protocol.** Agents on Agent Engine can communicate with agents on other frameworks. *Source: [Vertex AI Agent Builder April 2026 analysis](https://agentmarketcap.ai/blog/2026/04/11/google-vertex-ai-agent-builder-april-2026).*

**Honest assessment:** Agent Engine is genuinely useful for teams that want a managed runtime and don't want to manage GKE. For your use case (self-hosted stack, sovereignty focus), Agent Engine is optional. You can use ADK as a local library and deploy on GKE or bare Compute Engine VMs without touching Agent Engine at all.

### Vertex AI Model Garden

Model Garden currently hosts **200+ models** including:
- Google first-party: Gemini 3.x, Gemma 4, Imagen, Veo
- Third-party commercial: Anthropic Claude (all tiers), Mistral
- Open models: Meta Llama 4, Gemma 4, Phi-4, Falcon, Mixtral

**Self-deployed models** — critical distinction for sovereignty — let you deploy open or partner models into *your GCP project and VPC*, not Google's multi-tenant inference infrastructure. The model runs in your project; Google doesn't see inference traffic. *Source: [Model Garden self-deployed models docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-garden/self-deployed-models), June 2026.*

### Gemini API (managed inference)

This is the sovereign-compromised option. When you call `gemini-2.5-flash` via the API, your prompt goes to Google's multi-tenant inference cluster. Google contractually does not train on it, but they process it. Avoid for sensitive data. Not relevant if you use open models or Claude on Anthropic's API.

---

## 3. Sovereignty & Neutrality Trade-Off (Most Important)

This is the crux. The question is: *if you rent GCP compute, what exactly does Google see and what rights do they have?*

### What Google Contractually Commits To

Per the [Google Cloud Privacy Notice (effective April 8, 2026)](https://cloud.google.com/terms/cloud-privacy-notice) and Cloud Data Processing Addendum:

1. **Your data is not used to train Google models** without explicit permission. This is contractual, not just a policy claim.
2. **Customer Data** (your workloads, prompts, outputs) is governed by the Cloud DPA, not the Privacy Notice — meaning it's processed per your instructions only.
3. **Service Data** (billing info, config, logs) is collected and processed by Google to operate the platform.

### What Google Can Access (The Honest List)

Even on raw Compute Engine VMs:

- **Access Transparency:** Google logs every time a Google employee accesses your data; you get near-real-time logs. This is a tool to *see* access, not prevent it.
- **Access Approval:** You can require Google to request explicit approval before accessing your data. You can approve/deny per request.
- **Key Access Justifications (Assured Workloads):** With customer-managed encryption keys (CMEK) + KAJ, you can deny Google decryption access entirely, even for support. *Source: [Google Cloud Assured Workloads overview](https://docs.cloud.google.com/assured-workloads/docs/overview).*
- **Legal process.** If Google receives a valid legal order (subpoena, FISA, etc.) for your data, they are bound to comply with applicable law. This is true of every cloud provider.
- **Infrastructure visibility.** Google sees VM metadata, network flows (at the fabric level), and utilization metrics. They do not see memory contents of running VMs by default, but the hypervisor does.

### Running Open Models on GCP: Fully Viable

Yes, you can run your entire open-source stack on GCP compute with no Gemini/managed AI:

- Spin up an A3 VM (8× H100 80GB) or GKE cluster with GPU node pools.
- Install your own container: vLLM, LiteLLM, Langfuse, Postgres — exactly your current stack.
- Google sees the VM exists, its CPU/network metrics, and its storage usage. Google does not see what model you're running or what prompts you process.
- Google publishes official guides for running vLLM with Llama 4 on GKE. *Source: [Serve Llama models on GKE with vLLM](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/serve-llama-gpus-vllm).*

**What you give up vs full self-hosting:**
- Physical hardware control — you can't audit the hardware or wipe SSDs
- Network path control — traffic to/from the VM traverses Google's network fabric
- Legal jurisdiction — data is subject to US law (and EU law if you use EU regions) by default
- FISA/NSL risk — applicable if using US-based infrastructure for sensitive intelligence/national-security content (not typical for commercial AI agents)

**What you keep:**
- Model choice (any model, any provider)
- Stack neutrality (run exactly what you run today)
- No dependency on Google's AI APIs
- Data residency control (specify region; Assured Workloads enforces it)

### Assured Workloads: The Mitigation Tool

[Assured Workloads](https://cloud.google.com/security/products/assured-workloads) is GCP's control package system for sovereignty. It provides:

- **Regional data boundary enforcement** via Organization Policy — data cannot leave a specified region
- **Personnel access controls** — restrict which Google employees can access data based on location/clearance level
- **CMEK + KAJ** — customer-managed keys; Google must request justification before decryption; you can deny it
- **Access Approval** — explicit approval flow for any Google employee access

For your use case (commercial AI agents, not regulated government data), the standard contractual protections are likely sufficient. Assured Workloads is the tier for HIPAA, FedRAMP IL4, or EU GDPR-restricted scenarios.

### Google Sovereign Cloud Partners

For the strictest sovereignty (Google staff locked out entirely), Google has partner-operated clouds where a third party (Thales in France via S3NS, T-Systems in Germany, etc.) operates the infrastructure. Google employees have no access. This is premium-priced and only available in specific regions. *Source: [Google sovereignty blog, May 2025](https://cloud.google.com/blog/products/identity-security/google-advances-sovereignty-choice-and-security-in-the-cloud).*

### Bottom Line on Sovereignty

| Scenario | Google Sees | Your Control |
|---|---|---|
| Raw Compute Engine VM, open model | VM metadata, network metrics | Full stack control; model/data invisible |
| GKE cluster with vLLM | Pod metrics, container registry access | Full stack control |
| Vertex AI Model Garden (self-deploy) | Deployment metadata | Model runs in your VPC |
| Vertex AI Managed Inference (Gemini API) | Prompts and outputs | Low — avoid for sensitive data |
| Assured Workloads + CMEK + KAJ | Can't decrypt without your key | Can deny decryption |

**The sovereignty floor on GCP raw compute is: Google is your infrastructure provider and IaaS landlord, not your model/data processor.** That's a fundamentally different exposure than using Gemini API. It's equivalent to hosting your stack on any major IaaS provider, including Hetzner, AWS, or OVH — none of which are zero-trust either.

---

## 4. Cost Posture

### GPU Rental Pricing (mid-2026, on-demand, us-central1)

| Instance | GPU | On-Demand /hr | Spot /hr | 1-yr CUD /hr |
|---|---|---|---|---|
| n1-standard-4 + T4 | 1× T4 16GB | ~\$0.35 | ~\$0.11 | ~\$0.25 |
| g2-standard-4 | 1× L4 24GB | ~\$0.71 | ~\$0.25 | ~\$0.50 |
| a2-highgpu-1g | 1× A100 40GB | ~\$3.67 | ~\$1.10 | ~\$2.31 |
| a2-ultragpu-1g | 1× A100 80GB | ~\$5.10 | ~\$1.53 | ~\$3.21 |
| a3-highgpu-8g (÷8) | 1× H100 80GB | ~\$4.10–\$11.06 | ~\$1.23–\$2.25 | ~\$2.90 |

*Sources: [GPU Cloud Pricing Guide 2026](https://www.gpucloudlist.com/en/blog/google-cloud-gpu-pricing-guide); [DeployBase GCP GPU pricing, March 2026](https://deploybase.ai/articles/google-cloud-gpu-cloud-pricing-complete-guide-vs-hr-for); [GPU Finder, May 2026](https://gpufinder.dev/providers/google-cloud).*

**Note:** GCP on-demand GPU pricing is 2–3× more expensive than specialists (Lambda Labs, RunPod, CoreWeave) for the same hardware. The premium buys compliance, SLAs, integration with GCP networking, and geographic availability. For pure burst inference where you don't need GCP-specific integration, Lambda Labs or CoreWeave may be cheaper with comparable latency — and they have zero egress fees.

### Egress Fees: The Hidden Cost

| Provider | First 10 TB/month | 10–50 TB/month | Free Tier |
|---|---|---|---|
| GCP | \$0.08/GB | \$0.06/GB | None |
| AWS | \$0.09/GB | \$0.085/GB | 100 GB/month |
| CoreWeave | \$0/GB | \$0/GB | N/A |
| Lambda Labs | \$0/GB | \$0/GB | N/A |
| RunPod | \$0/GB | \$0/GB | N/A |

*Source: [Spheron GPU cloud egress guide, May 2026](https://www.spheron.network/blog/gpu-cloud-egress-data-transfer-costs-ai-workloads-2026/).*

For your use case (agent inference, not large model weight transfers), egress from GCP to the internet is mostly streaming tokens. 100M tokens/day ≈ 18 GB/month ≈ \$1.44/month in GCP egress. This is not a significant cost driver for text inference. It becomes material if you're streaming large audio/video outputs or pulling model weights repeatedly.

**Intra-GCP traffic is free.** GCE VM to GCE VM in the same region: \$0. This matters if you split your stack (Postgres on one VM, inference on another) inside GCP.

### Cloud vs. Hardware Economics

| Comparison Point | Cloud (GCP on-demand) | Self-Owned Hardware |
|---|---|---|
| 1× A100 80GB GPU cost/hour | ~\$5.10/hr | ~\$0.30–\$0.50/hr (amortized 3yr) |
| 8× A100 server, continuous | ~\$38K/month | ~\$25–35K hardware once + ~\$500–800/month power |
| Break-even point | — | ~4–6 months at 24/7 utilization |
| Utilization risk | Pay per second | Pay regardless of use |
| Time to provision | Minutes | Weeks (GPU supply varies) |

*Source: [Petronella AI Workstation vs Cloud 2026](https://petronellatech.com/blog/ai-workstation-vs-cloud-cost/); [CiroCloud TCO analysis, April 2026](https://cirocloud.com/de/artikel/ai-model-training-on-cloud-vs-onpremise-tco-2025).*

**For your situation specifically:**

Your 128GB server is already owned. The question is whether to *add* cloud as overflow. The economics favor this:

- **Burst workloads (0–20% of time):** Cloud is dramatically cheaper than buying a second server for occasional spikes.
- **Continuous high utilization (>50% of time):** Hardware wins. At 24/7 utilization, a cloud A100 costs 8–10× more per hour than amortized owned hardware.
- **Fine-tuning jobs (days–weeks, not continuous):** Cloud is ideal. Rent 4× A100 for 3 days, pay ~\$1,060, finish the job. No capital outlay.

---

## 5. Hybrid Pattern: GCP as Burst Compute on Tailscale

This is the most relevant architecture for your situation. "Own the base, rent the spike."

### The Pattern

```
[Amplified Partners Infra 1]         [GCP Burst VMs]
128GB server                    ←→   A3/A2 GPU VMs
Cove Temple                          vLLM / LiteLLM
LiteLLM (primary)                    (ephemeral, on-demand)
Langfuse                             ↑ Tailscale subnet router
Postgres                    
Agents                       
Mac mini (4 agent cells)    
        ↕ Tailscale
[Private Tailscale Network]
```

### Tailscale + GCP Integration: Fully Documented

Tailscale's official documentation covers GCE VMs directly. The pattern:

1. Create a GCE instance (any machine type, including GPU).
2. Install Tailscale on the VM; enable IP forwarding.
3. Advertise GCP VPC subnet routes via Tailscale subnet router.
4. Set GCP firewall rules to allow UDP 41641 (Tailscale direct connections).
5. Add GCP DNS forwarding to Tailscale split DNS config.

After this, GCP VMs appear as private Tailscale nodes. Your on-prem LiteLLM orchestrator can route overflow requests directly to `burst-vm.tailnet` over the encrypted Tailscale mesh — no public endpoint needed. *Source: [Tailscale GCE documentation, December 2025](https://tailscale.com/docs/install/cloud/gce).*

### Routing Burst Traffic

LiteLLM already supports multiple model backends with load balancing and fallback. You configure your GCP inference endpoint as a secondary/overflow provider:

```yaml
# LiteLLM config (existing stack)
model_list:
  - model_name: llama3-70b
    litellm_params:
      model: openai/llama3-70b
      api_base: http://local-vllm:8000  # primary: on-prem
  - model_name: llama3-70b  
    litellm_params:
      model: openai/llama3-70b
      api_base: http://burst-vllm.tailnet:8000  # overflow: GCP VM
      rpm_limit: 1000
      tpm_limit: 500000
```

LiteLLM handles routing, failover, and rate limiting. The burst VM only exists when provisioned (via `gcloud compute instances create` in a startup script or Terraform). For cost control: provision on traffic spike, deprovision after idle for 15 minutes.

### Data Isolation in the Hybrid Pattern

In this architecture:
- **Sensitive data stays on-prem.** Postgres with conversation history, user data, API keys — never leaves your server.
- **Only inference requests traverse the Tailscale tunnel.** The prompt goes to the GCP VM; the response comes back. The VM has no persistent storage of prompt history.
- **Ephemeral VMs with no persistent disks.** A burst VM with no attached persistent disk has no long-term storage of your prompts. At shutdown, memory is cleared.
- **No Google AI services involved.** The vLLM process on the VM is your code, your model weights (pulled from GCS or your on-prem server), Google's VMs are just iron.

**Model weights management:** You have two options:
1. Store model weights in a GCS bucket (private to your project). Warm VMs download weights on startup (~10–15 min for 70B). Cost: ~\$0.02/GB/month storage.
2. Bake weights into a custom GCE image (faster cold start, larger image, less flexible).

### Alternatives to GCP for Pure Burst Compute

If sovereignty and cost are both paramount:

| Provider | Sovereignty Posture | GPU Egress | Notes |
|---|---|---|---|
| **CoreWeave** | US company, similar legal exposure as GCP | Free | Better per-GPU price; Tailscale-compatible |
| **Lambda Labs** | US company; strong privacy posture | Free | Cheapest H100 rates; reliable API |
| **Hetzner Dedicated** | German provider; EU law | Free | Limited GPU SKUs; strong EU sovereignty |
| **RunPod** | US; serverless GPU, pay-per-second | Free | Good for ephemeral jobs |

For pure burst with no GCP-ecosystem benefit, Lambda Labs or CoreWeave are cheaper and have zero egress. GCP wins if you want GCP Interconnect, GKE integration, or the GCP billing consolidated with other Google services.

---

## 6. Recommendation

### Use GCP? Yes — for compute only, in a specific role.

**Use GCP for:**
- **Burst/overflow GPU inference** when local server is saturated. An A2 (1× A100) at ~\$3.67/hr gives you overflow capacity on demand. Provision for 2–4 hours during peak, then destroy.
- **One-off fine-tuning jobs.** Instead of buying a second A100, rent 4× A100 for 3 days, run the LoRA fine-tune, shut it down. This pays for itself vs capital outlay after the first job.
- **Experimenting with larger models** (70B+ at full precision, MoE models, Llama 4 Scout/Maverick) that exceed your 128GB server's VRAM.
- **GKE autoscaling** if your agent workloads grow enough to need orchestrated multi-node inference.

**Do not use GCP for:**
- Storing sensitive conversation data, PII, or proprietary datasets. Keep Postgres and Langfuse on-prem.
- Routing all inference through GCP. Keep primary inference on your server; cloud is overflow only.
- Managed Gemini API or Vertex AI managed inference. This is where sovereignty meaningfully degrades — Google sees prompts.
- Agent Engine (managed runtime) unless you actively want managed state/memory and accept the trade-off. ADK itself is fine locally.

**Does GCP compromise the sovereignty/neutrality principle?**

*It depends on what layer you use.*

- **Raw Compute Engine / GKE + your own stack:** Sovereignty compromise is minimal and equivalent to any IaaS. Google is your landlord, not your data processor. The contractual commitment that Google doesn't train on your data is enforceable. Use CMEK + Access Approval if you need stronger control.
- **Vertex AI managed inference / Gemini API:** Sovereignty meaningfully compromised — Google processes prompts. Avoid.
- **ADK framework (local/GKE):** Zero sovereignty compromise — it's a local library.
- **Agent Engine (managed runtime):** Some compromise — Google manages the runtime; memory/session data goes through Google infrastructure. Acceptable for non-sensitive agent state; avoid for sensitive workflows.

**Model neutrality is fully preserved** on raw compute. Running Llama 4, Mistral, Phi, or any open model on a GCP VM is identical to running it on your server — Google doesn't know or care what model binary is executing.

### The Hybrid Architecture Is Sound

"Rent GPU compute only, keep data/core at home" is not just viable — it's a well-documented pattern with active community support. The Tailscale integration with GCE is official and production-tested. LiteLLM's multi-backend routing handles the orchestration. The risk surface is bounded: only inference payloads traverse the GCP boundary, and only when you choose to route there.

### Relative Priority of Alternatives

1. **GCP (recommended for burst):** Best when you want GCP ecosystem depth, GKE, or potential future use of Vertex AI managed services selectively.
2. **Lambda Labs or CoreWeave:** Best if you want cheapest GPU burst with zero egress and no Google relationship. Slightly less integrated; Tailscale still works.
3. **Buy a second server:** Right answer if burst becomes continuous (>40% utilization). At that point, the 6-month hardware payback makes ownership clearly cheaper. Also maximizes sovereignty.

---

## Sources

| # | Source | Date | URL |
|---|---|---|---|
| 1 | Google Cloud GPU machine types documentation | Retrieved June 2026 | https://docs.cloud.google.com/compute/docs/gpus |
| 2 | Cloud TPU release notes (Ironwood GA, March 2026) | 2026 | https://docs.cloud.google.com/tpu/docs/release-notes |
| 3 | Ironwood GA announcement blog | November 2025 | https://cloud.google.com/blog/products/compute/ironwood-tpus-and-new-axion-based-vms-for-your-ai-workloads |
| 4 | Introl: Google TPU vs NVIDIA GPU framework | January 2026 | https://introl.com/blog/google-tpu-vs-nvidia-gpu-infrastructure-decision-framework-2025 |
| 5 | ADK launch blog (Google Cloud Next 2025) | April 2025 | https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/ |
| 6 | ADK 1.0 / Google I/O 2025 enhancements | May 2025 | https://developers.googleblog.com/agents-adk-agent-engine-a2a-enhancements-google-io/ |
| 7 | Google Cloud I/O '26 ADK news | May 2026 | https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud |
| 8 | Vertex AI Agent Builder 2026 guide (UIBakery) | April 2026 | https://uibakery.io/blog/vertex-ai-agent-builder |
| 9 | Vertex AI Agent Builder April 2026 analysis | April 2026 | https://agentmarketcap.ai/blog/2026/04/11/google-vertex-ai-agent-builder-april-2026 |
| 10 | Model Garden self-deployed models docs | June 2026 | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-garden/self-deployed-models |
| 11 | Google Cloud Privacy Notice | April 2026 | https://cloud.google.com/terms/cloud-privacy-notice |
| 12 | Google Cloud sovereignty advancement blog | May 2025 | https://cloud.google.com/blog/products/identity-security/google-advances-sovereignty-choice-and-security-in-the-cloud |
| 13 | Assured Workloads overview | 2025 | https://docs.cloud.google.com/assured-workloads/docs/overview |
| 14 | DeployBase GCP GPU pricing guide | March 2026 | https://deploybase.ai/articles/google-cloud-gpu-cloud-pricing-complete-guide-vs-hr-for |
| 15 | GPU Cloud list pricing 2026 | March 2026 | https://www.gpucloudlist.com/en/blog/google-cloud-gpu-pricing-guide |
| 16 | GPU Finder GCP pricing | May 2026 | https://gpufinder.dev/providers/google-cloud |
| 17 | Spheron GPU cloud egress costs guide | May 2026 | https://www.spheron.network/blog/gpu-cloud-egress-data-transfer-costs-ai-workloads-2026/ |
| 18 | Petronella AI Workstation vs Cloud 2026 | March 2026 | https://petronellatech.com/blog/ai-workstation-vs-cloud-cost/ |
| 19 | CiroCloud TCO AI training on cloud vs on-prem | April 2026 | https://cirocloud.com/de/artikel/ai-model-training-on-cloud-vs-onpremise-tco-2025 |
| 20 | Tailscale GCE access documentation | December 2025 | https://tailscale.com/docs/install/cloud/gce |
| 21 | CloudExpat: AWS Trainium vs TPU v5e vs H100 comparison | March 2025 | https://www.cloudexpat.com/blog/comparison-aws-trainium-google-tpu-v5e-azure-nd-h100-nvidia/ |
| 22 | LMCache blog: vLLM on GCP GKE | February 2025 | https://blog.lmcache.ai/en/2025/02/20/deploying-llms-in-clusters-2-running-vllm-production-stack-on-aws-eks-and-gcp-gke/ |
| 23 | GKE + vLLM Llama serving tutorial | 2025–2026 | https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/serve-llama-gpus-vllm |
| 24 | Vertex AI autoscaling documentation | 2025 | https://cloud.google.com/vertex-ai/docs/predictions/autoscaling |
| 25 | GPU.fm cloud providers comparison 2026 | February 2026 | https://www.gpu.fm/blog/cloud-gpu-providers-comparison-2026 |
