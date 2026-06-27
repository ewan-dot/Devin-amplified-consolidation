# Shape gate — Antigravity workspace rule

After any **tiered document write** (YAML frontmatter with `epistemic_tier`), run the bee:

```bash
python3 "${AMPLIFIED_INBOX:-$HOME/ingestion-to-research-pipe/perplexity-inbox}/harness/hooks/shape-gate-cli.py" \
  --seat antigravity --path "<written-file>"
```

Or pipe write payload:

```bash
python3 "${AMPLIFIED_INBOX:-$HOME/ingestion-to-research-pipe/perplexity-inbox}/harness/hooks/antigravity-post-write-shape-gate.py"
```

## Parameters (same bee as Cursor + Claude)

- **Shape only** — tier arithmetic, author present, no agent→human attribution without `proxy_act`
- **Human default ceiling:** INTUITED until `promotion_record_id`
- **Agent default ceiling:** INTUITED; `consulted_llm_at_runtime` defaults true for agent seats
- **Witness:** `~/.amplified/logs/harness-hooks.jsonl`
- **Non-judgmental:** wrong fact at INTUITED passes; wrong tier shape gets P0 logged

## Author fields

| Who | Set `author` to |
|-----|-----------------|
| Ewan steer / human doc | `ewan` |
| Antigravity emission | `antigravity` |
| Proxy on Ewan's behalf | `ewan` + `proxy_act: true` |
| Dual contribution | `author` + `contributors` list |

SSOT: `perplexity-inbox/harness/shape_gate.py` + `harness/opa/amplified/honesty/min_rule.rego`
