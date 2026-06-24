# Tailscale + Vellum Integration — 2026-06-24 (cascade-mac)

## What was done

### Vellum API URL (PRs #4 and #5 on agent-claude)
All scripts and hooks were using `http://100.101.0.53:8400` to post Vellum witnesses.
This never worked because Beast's iptables INPUT chain only allows ports 22/80/443 + ESTABLISHED —
port 8400 is silently dropped from all external/Tailscale connections.

**Fix:** `VELLUM_API="https://beast-amplified.tail27a0cc.ts.net:8443"`

Beast already has Tailscale serve configured:
```
https://beast-amplified.tail27a0cc.ts.net:8443 -> http://vellum:8400
```
Confirmed working: `curl https://beast-amplified.tail27a0cc.ts.net:8443/health`
→ `{"status":"ok","storage":"PostgresSheetStore","memory_backend":"rust_agent"}`

### Epistemic tier (same PRs)
The hooks were claiming `MEASURED` tier, which requires `evidence_refs` or `source_id` —
this triggers an Idea Meritocracy constitution violation.

After testing: cascade-mac's Vellum floor is `INTUITED`. The hooks now use `INTUITED`.
(STRUCTURED/MEASURED/PROVEN require the agent to be registered with a higher floor.)

### Pending queue flushed
`~/.pending-vellum-queue` had 7 entries from previous sessions (all witness posts that
failed because port 8400 was unreachable). All 7 flushed successfully at 2026-06-24T18:42.

## Beast/Tailscale topology (for reference)

| Route | Notes |
|-------|-------|
| `beast` (SSH config) | `135.181.161.131` — public IP, `IdentityAgent none`, works anytime |
| `beast-ts` (SSH config) | `100.101.0.53` — SSH refused (bound to public IP only, not Tailscale) |
| `https://beast-amplified.tail27a0cc.ts.net:8443` | Tailscale HTTPS → Vellum ✅ |
| `https://vellum.beast.amplifiedpartners.ai` | Traefik → Vellum ✅ |
| `https://vellum-mcp.beast.amplifiedpartners.ai/sse` | Traefik → vellum-mcp (MCP SSE endpoint) ✅ |
| `http://100.101.0.53:8400` | BLOCKED — iptables DROP |

## Files changed

- `agent-claude/.hooks/pre-commit` — VELLUM_API + tier
- `agent-claude/scripts/gk-worktree-start.sh` — VELLUM_API + tier

## Remaining items

- **cascade-mac floor is INTUITED** — to post STRUCTURED or higher, the agent needs to be registered in the Vellum fleet with a higher floor. This is a Vellum admin action (Ewan).
- **beast-ts SSH** — no fix possible from M5; Beast SSH is only listening on the public IP. Use `ssh beast` (via `IdentityAgent none` + `IdentityFile ~/.ssh/beast_m5`).
- **vellum-mcp.beast.amplifiedpartners.ai** — working (returns 200 at `/sse`, 404 at `/health` which doesn't exist). The MCP Claude Code config is correct.
