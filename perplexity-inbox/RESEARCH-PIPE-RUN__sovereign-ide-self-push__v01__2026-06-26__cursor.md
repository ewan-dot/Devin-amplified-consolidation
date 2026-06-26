---
title: "Research Pipe Run — Sovereign IDE Self-Push"
document_type: research_pipe_run
artifact_id: RESEARCH-PIPE-RUN__sovereign-ide-self-push__v01__2026-06-26__cursor
date_utc: 2026-06-26
corpus_item_id: sovereign-ide-self-push-2026-06-26
author: cursor
reader: ewan
epistemic_tier: INTUITED
run_host: Beast (research-pipe container + SearXNG L1)
note: five_stage_orchestrator.py not deployed on Beast; run used M1Orchestrator + runner process-queue (canonical Beast entrypoint).
---

## Human summary

Ran on **Beast**: `research-pipe` container healthy; 8 SearXNG fan-out probes + `runner process-queue` for corpus `sovereign-ide-self-push-2026-06-26`. **8/8 probes success**, 160 SearXNG hits, batch `26f2dd5c-70c5-4feb-92a5-ca58d375efe5` (20 packets, Gate0 20/20). Wide→narrow×3 across eight candidate domains (git branch protection, CI/CD craft gates, aviation CRM challenge-response, multi-agent sovereignty, supply-chain signing, IDE plugin isolation, OTP supervision, constitutional gate). Brutal demote stripped homonym junk (unrelated Copilot products, CRM vendors). **Five survivors** converge on one shape: *sovereign IDE seat* — isolated extension/process boundary per IDE, self-managed push to feature branches, automated craft gates (tests/lint/signing) as quality filter not nanny approval, constitutional principles enforced pre-push, merge to protected main via CODEOWNERS cross-seat review. Cross-domain endpoint caps at INTUITED until fleet wiring measured on live seats.

## Orchestrator payload

### meta

```yaml
run_id: sovereign-ide-self-push-2026-06-26
stage: swanson_combine
corpus_item_id: sovereign-ide-self-push-2026-06-26
epistemic_tier: INTUITED
chunk_id: single-item
survivor_count: 5
run_host: beast
beast_entrypoint: research_pipe.runner process-queue + M1Orchestrator
beast_batch_id: 26f2dd5c-70c5-4feb-92a5-ca58d375efe5
beast_alert_id: b3c30ac2-a38f-4c16-b3eb-ce93848f76ed
beast_staging_path: /opt/amplified-machine/apds/staging/26f2dd5c-70c5-4feb-92a5-ca58d375efe5/
jsonl_witness: ~/amplified-pipeline/data/research-pipe-docs/2026-06-26_five-stage_sovereign-ide-self-push-2026-06-26.jsonl
searxng: search.beast.amplifiedpartners.ai (container http://searxng:8080)
mac_supplement: WebSearch gap-fill only (labeled agent-seat, not Beast run)
```

### stage_result

#### Wide 1 — candidate domains (raw terms from Ewan frame only)

| # | Founding discipline | Raw probe terms |
|---|---------------------|-----------------|
| 1 | Software platform governance | git branch protection, CODEOWNERS, signed commits, agent self-approval |
| 2 | DevOps / release engineering | CI/CD quality gate, craft gate, automated pass/fail |
| 3 | Human factors / aviation | CRM, challenge-response, checklist gate |
| 4 | Multi-agent systems | sovereign IDE, self-managed push, minimal architect |
| 5 | Supply chain security | sigstore, cosign, SLSA, artifact attestation |
| 6 | Software security / isolation | IDE plugin sandbox, extension host isolation |
| 7 | Distributed systems / telecom | OTP supervision tree, let it crash, fault containment |
| 8 | Governance / ethics | constitutional gate, radical honesty, transparency, attribution |

#### Narrow 1 — canonical sources per domain

| Domain | Canonical source | URL |
|--------|------------------|-----|
| Branch protection | GitHub Docs — About protected branches | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| CODEOWNERS agent governance | Aido Labs — CODEOWNERS AI agent governance | https://aidolabs.mintlify.app/articles/practices/codeowners-ai-agent-governance |
| Quality vs approval gates | Testkube — Quality Gates glossary | https://testkube.io/glossary/quality-gates |
| Aviation challenge-response | FAA AC 120-51E — Crew Resource Management Training | https://www.faa.gov/documentlibrary/media/advisory_circular/ac120-51e.pdf |
| Supply chain attestation | Sigstore Cosign README | https://github.com/sigstore/cosign |
| IDE isolation | VS Code — Migrating to Process Sandboxing | https://code.visualstudio.com/blogs/2022/11/28/vscode-sandbox |
| OTP supervision | Erlang OTP supervisor behaviour (official docs) | https://www.erlang.org/doc/apps/stdlib/supervisor.html |

#### Wide 2 — cross-domain failure modes (others identified)

- Branch protection: agent can push feature branch and open PR but cannot self-approve merge; cross-domain PR requires human/other-seat CODEOWNERS (GitHub docs; Aido Labs).
- Quality gates: manual approval gates create bottlenecks; craft gates automate measurable pass/fail but miss contextual risk (DevOps Training Institute; ADHDecode).
- Aviation CRM: challenge-response fails when culture punishes questioning; monitoring role essential on approach/landing (FAA AC 120-51E).
- Sigstore: signing proves identity not build integrity alone; SLSA provenance needed for process witness (Sigstore; SLSA spec).
- IDE sandbox: extension host isolation per window; Node.js APIs removed from renderer — extensions delegate to utility process (VS Code blog 2022).

#### Narrow 2 — convergent mechanisms (2–3 strongest)

1. **Self-push + merge gate split** — sovereign seat pushes to own branch; protected main requires cross-seat/human CODEOWNERS approval (platform governance + multi-agent).
2. **Craft gate not nanny gate** — automated quality gates (tests, lint, signing) filter craft; human approval reserved for constitutional/policy exceptions (DevOps + supply chain).
3. **Challenge-response constitutional check** — pre-push hooks verify honesty/transparency/attribution principles; independent monitor challenges before merge proceeds (aviation CRM + governance).

#### Wide 3 / Narrow 3 — multi-domain endpoint claim (INTUITED)

**Endpoint claim:** Fleet sovereign IDE shape = each IDE (Cursor, Claude Code, Copilot, etc.) runs as isolated seat with own hooks/harness, self-managed push to feature branches, automated craft gates (CI + sigstore attestation) as Copilot-equivalent quality filter, constitutional gate on Ewan's seven principles enforced pre-push (IDE-agnostic rules in repo), auto-push on pass with minimal architect involvement; merge to protected main requires CODEOWNERS from another seat. Prior art spans platform governance (≥1), DevOps gates (≥1), aviation CRM (≥1), supply chain signing (≥1). **Not promoted to STRUCTURED** — per-IDE auto-push wiring and constitutional hook enforcement not yet measured on fleet.

#### Brutal demote — survivors (5)

| id | vector | founding discipline |
|----|--------|---------------------|
| S1 | CODEOWNERS + branch protection (push yes, self-merge no) | Software platform governance |
| S2 | Automated craft/quality gates vs manual approval gates | DevOps / release engineering |
| S3 | Aviation challenge-response CRM (independent verification) | Human factors / aviation |
| S4 | Sigstore/cosign + SLSA provenance attestation on push | Supply chain security |
| S5 | IDE extension-host isolation + OTP fault containment per seat | Software security + distributed systems |

#### Beast run metrics

```yaml
m1_fan_out_queries: 8
searxng_hits_total: 160
runner_alert_id: b3c30ac2-a38f-4c16-b3eb-ce93848f76ed
packets_staged: 20
gate0_passed: 20
gate0_failed: 0
auto_promote: false
```

### handoff

```yaml
next_stage: done
architect_flags:
  - "five_stage_orchestrator.py absent on Beast; M1+runner is live path"
  - "Endpoint claim INTUITED — per-IDE auto-push + constitutional hooks not fleet-wired"
  - "Copilot-as-craft-gate is pattern name; actual craft gate = CI quality gates + signing"
do_not:
  - promote epistemic tier from agent output
  - synthesise final truth without promotion gates
  - use prior synthesis prose as search input
goal_link: "Sovereign IDE seats self-push with craft+constitutional gates; plan → pipe → implement → brain"
fleet_pipeline: plan → pipe → implement → brain
```

### Research prompt (raw terms only — for re-run)

```
Corpus: sovereign-ide-self-push-2026-06-26
Pattern: wide→narrow×3
Terms: sovereign IDE, self-managed push GitHub, craft gate not nanny gate,
  constitutional gate radical honesty transparency attribution meritocracy privacy sovereignty security,
  IDE agnostic, auto-push minimal architect, CODEOWNERS branch protection signed commits,
  CI CD quality gate automated pass fail, aviation CRM challenge-response checklist,
  multi-agent sovereignty isolated seat, sigstore cosign SLSA attestation,
  IDE plugin sandbox extension host isolation, OTP supervision let it crash,
  Cursor Claude Code Copilot sovereign seats, plan pipe implement brain
Exclude: prior synthesis headings, hooks-harness-doorways survivors
```

[CLOSURE] branch=AUDIT | proxy=none | gates=Beast run complete; local commit pending Devin push for F8 | inbox=RESEARCH-PIPE-RUN__sovereign-ide-self-push__v01__2026-06-26__cursor.md | tier=INTUITED
