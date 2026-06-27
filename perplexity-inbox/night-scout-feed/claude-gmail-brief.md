---
title: Claude as token-efficient email-actioning system across multiple inboxes
origin: perplexity-thread
created: 2026-06-26T12:15+01:00
tier: STRUCTURED
status: brief-ready-for-implementation
dual_purpose: [implementation, night-scout-feed]
scout_tags: [email-triage, mcp-code-execution, token-efficiency, multi-inbox, actioning-not-replying]
sources:
  - https://www.anthropic.com/engineering/code-execution-with-mcp
  - https://www.linkedin.com/posts/shivam-yadav-full-stack-developer-react-native-mern-601634313_systemdesign-n8n-devops-activity-7416329712773386241-EfyX
---

# Email-actioning agent: architecture brief

## Goal
Multi-inbox email triage that ACTIONS (labels, files, extracts, ingests into the Beast, notifies) rather than replies. Token-efficient. No human-in-the-loop except at the implementation boundary.

## Canonical pattern
Anthropic's Code Execution with MCP (2025-11-04). Each inbox is an MCP server; agent writes code; intermediate results (full email bodies, attachments) stay in the sandbox; only structured actions enter model context. Measured saving on Anthropic's worked example: 150k -> 2k tokens (98.7%).

## Tier the work, not the prompt
Per Yadav's n8n+Groq pipeline:
- Bulk classification (newsletters, promos, low-stakes) -> small/fast model, 1000-char truncation
- High-stakes (financial, security, infra-critical, partner threads) -> stronger model, full body
- Truncation alone cuts tokens ~60% with no loss for classification.

## Routing surface (post-classification switch)
- INFRA_CRITICAL  -> extract -> JSONL -> Beast ingestion pipe
- FINANCIAL       -> attachment to Drive + row to ledger + notify
- ATTRIBUTION/SRC -> content-harvester -> brain
- URGENT_HUMAN    -> Telegram/Slack push to Ewan
- NEWSLETTER      -> digest label, no model spend after classification
- NOISE           -> archive, no further spend

## Multi-inbox handling
One MCP server per inbox under ./servers/. Agent loads only what the current task needs. No need to dump all inbox schemas into context.

## What is NOT in public prior art
The synthesis of (a) Anthropic's code-execution pattern + (b) Yadav's tiered-routing pattern + (c) actioning-into-a-private-ingestion-pipe is not published anywhere I can find. Amplified would be first.

## Next executable step
Stand up one MCP server against Ewan's primary inbox, write the classifier as code (not as a tool-loop), route INFRA_CRITICAL into perplexity-inbox as JSONL, measure tokens/email vs naive baseline.

## Night Scout routing (dual-purpose handoff)
This brief is BOTH an implementation order AND a Night Scout feed item. The implementing agent must:

1. Discover the Night Scout feed location on the M5 (likely sibling to `perplexity-inbox/`, or pointed to by a config file in `ingestion-to-research-pipe/`). If ambiguous, ask Ewan once and record the resolved path for future handoffs.
2. Place a copy (or symlink) of this brief into that feed so overnight scouts will:
   - watch for new public prior art on Claude/MCP email-actioning systems
   - watch for new publications on token-efficient multi-inbox triage
   - watch for anyone else publishing the synthesis described in the "What is NOT in public prior art" section above (so we know if/when we lose first-publisher position)
   - re-ingest the brief itself as a brain artifact under `scout_tags`
3. Do not block implementation on the scout routing — they are independent. Both happen.
4. Tier-tag any scout findings under min-rule when they come back.

---

## Resolution log (implementer: cascade-mac, 2026-06-26)
- Built at `perplexity-inbox/email_actioning_agent/` on branch `feat/email-actioning-agent`.
- Night Scout feed: canonical sink `/opt/amplified-machine/apds/staging/` is **Beast-only, not on M5** this session; `~/clean-build/.../nightscout/` also absent on M5. Resolved M5-local mirror = `perplexity-inbox/night-scout-feed/` (see `night_scout.py`); sync mirror → Beast APDS when reachable. **One open question for Ewan:** confirm the canonical M5 feed path if it should differ from this mirror.
