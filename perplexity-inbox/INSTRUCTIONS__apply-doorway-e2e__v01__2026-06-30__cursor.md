---
title: "Instructions — Antigravity builds apply_doorway end-to-end"
document_type: operating_instructions
artifact_id: INSTRUCTIONS__apply-doorway-e2e__v01__2026-06-30__cursor
date_utc: 2026-06-30
author: cursor
reader: antigravity
assignee: antigravity
epistemic_tier: INTUITED
ratifier: ewan
provenance: "Ewan 2026-06-30 — one seat owns job end-to-end; third-party validation via scoped API + harnesses, not another IDE."
registry_id: R-003
---

# Antigravity — `apply_doorway` (end-to-end owner)

**Audience:** Antigravity seat  
**Owner:** **antigravity only** — spec → build → test → push → deploy → witness. No split to Cascade/Devin unless you hit a hard rod block; then baton with blocker detail, don't drop the row.

**Goal:** Rust binary `apply_doorway` reads JSON patches from `outbound_doorway/`, validates through **deterministic harnesses**, applies file changes, runs **shape_gate**, commits on pass. Third-party proof = **scoped verify API/CLI**, not "ask Cursor to look at it."

**Registry:** `docs/OWNERSHIP-REGISTRY.md` R-003 · R-004

---

## 0. Ewan's rule (non-negotiable)

> If you take the job, you own it **end to end**. Worktree checkpoints, checklists, what bad looks like, what good looks like, success = **tested + pushed + validated by a scoped API** (hooks/harnesses), **not** by another IDE eyeballing your diff.

---

## 1. Prerequisites

| Check | Command / note |
|-------|----------------|
| **Worktree** | `git worktree add .worktrees/antigravity-apply-doorway -b antigravity/apply-doorway` from repo root |
| **Export inbox** | `export AMPLIFIED_INBOX=/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox` |
| **Vellum intent** | Post plan to Vellum before substantive work (author `antigravity`, tier INTUITED) |
| **Read first** | `harness/shape_gate.py`, `harness/gatekeeper.py`, `outbound_doorway/README.md`, `docs/OWNERSHIP-REGISTRY.md` |
| **Rust toolchain** | `rustc --version`; crate lives under `control-centre/` (create `control-centre/crates/apply_doorway/` if missing) |
| **Beast SSH** | `ssh beast` for deploy checkpoint only — you deploy, not hand off |

---

## 2. Worktree checkpoints

Complete in order. Do not skip. Commit at each ✅.

| CP | Gate | Done when |
|----|------|-----------|
| **CP0** | Intent | Vellum row posted: artefact R-003, branch name, 5-step plan |
| **CP1** | Schema | `outbound_doorway/PATCH-SCHEMA.json` + 2 fixture patches + doc in `outbound_doorway/README.md` |
| **CP2** | Verify-only | `apply_doorway verify patch.json` exits 0 on good fixture, 1 on bad — **no writes** |
| **CP3** | Apply + gate | `apply_doorway apply patch.json` writes files, invokes `shape_gate.py` on touched paths, witness JSONL |
| **CP4** | Tests | `cargo test` + integration test applying fixture in temp dir; `python3 harness/gatekeeper.py` still passes |
| **CP5** | Mac install | Binary at `~/control-centre/bin/apply_doorway` (build script in `control-centre/scripts/`) |
| **CP6** | Push | Feature branch on GitHub (you push — sovereign seat for this job) |
| **CP7** | Beast | `/opt/amplified/bin/apply_doorway` installed; one live verify call over SSH |
| **CP8** | API validation | Scoped verify endpoint or CLI documented below — **external caller** proves pass/fail |
| **CP9** | Close | Registry R-003 → DONE; inbox status doc; Vellum compound delta; baton if blocked items remain |

---

## 3. Patch JSON schema (minimum)

```json
{
  "patch_id": "uuid-or-slug",
  "agent_id": "antigravity",
  "created_at": "2026-06-30T12:00:00Z",
  "target_repo": "ingestion-to-research-pipe",
  "base_ref": "antigravity/apply-doorway",
  "operations": [
    {
      "op": "write",
      "path": "relative/path/from/repo/root",
      "content_sha256": "hex",
      "content": "file body or base64"
    }
  ],
  "witness": {
    "vellum_entry_id": "",
    "epistemic_tier": "INTUITED"
  }
}
```

**Forbidden ops (hard reject in verify):** `delete_repo`, `shell`, `chmod`, paths outside repo root, `../` traversal, `.env`, private keys, direct `.git/` writes.

---

## 4. Binary interface

```bash
# Dry run — primary third-party validation surface
apply_doorway verify  outbound_doorway/patch_<ts>_antigravity.json
# Exit 0 + stdout JSON {"status":"pass","checks":[...]}
# Exit 1 + stdout JSON {"status":"fail","deny":[...]}

# Apply (only after verify pass)
apply_doorway apply    outbound_doorway/patch_<ts>_antigravity.json [--dry-run]

# Optional tight-scope HTTP (CP8) — bind localhost only unless Beast deploy
apply_doorway serve-verify --port 9477 --scope doorway:verify-only
# POST /v1/verify  body=patch JSON  Authorization: Bearer <scoped-token>
# Returns same JSON as CLI verify; never applies writes
```

**After apply:** shell out to `python3 "$AMPLIFIED_INBOX/harness/shape_gate.py"` on each written markdown with frontmatter.

---

## 5. Checklists

### Pre-flight (every session)

- [ ] On feature branch, not `main`
- [ ] `python3 harness/gatekeeper.py` → exit 0
- [ ] Vellum intent row < 8h old OR reposted
- [ ] `AMPLIFIED_INBOX` set

### Pre-push

- [ ] All `cargo test` green
- [ ] Integration: good patch applies, bad patch rejected
- [ ] No secrets in patch fixtures
- [ ] `shape_gate` invoked on sample `.md` write

### Pre-close (CP9)

- [ ] GitHub branch pushed
- [ ] Beast binary smoke: `ssh beast /opt/amplified/bin/apply_doorway verify /tmp/fixture.json`
- [ ] **API validation record** in inbox (see §7)
- [ ] OWNERSHIP-REGISTRY R-003 = DONE

---

## 6. Good vs bad vs success

### Good looks like

- Agent drops JSON patch in `outbound_doorway/` — **never** edits repo files directly
- `verify` returns structured JSON with named checks (`schema`, `path_allowlist`, `sha256`, `shape_gate_dry`)
- `apply` is idempotent-safe on same patch_id (reject duplicate)
- Witness line in `~/.amplified/logs/harness-hooks.jsonl` per apply
- One seat (you) can demo full loop in <5 commands

### Bad looks like

- Another IDE asked to "review whether this looks OK" as the validation step
- Direct file edits bypassing doorway
- `apply` without prior `verify` pass
- Binary modifies its own binary or OPA bundle
- Silent fail (exit 0 on deny)
- Split ownership: "Devin will push" / "Cascade will deploy" without baton blocker

### Success (F8 for this job)

| # | Bar |
|---|-----|
| 1 | **Working** — verify + apply + shape_gate on Mac |
| 2 | **Tested** — cargo + integration + gatekeeper green |
| 3 | **Pushed** — branch on GitHub |
| 4 | **Deployed** — Beast `/opt/amplified/bin/apply_doorway` |
| 5 | **Third-party validation** — scoped **API/CLI verify** called by harness **not** an IDE agent (see §7) |
| 6 | **Shared** — inbox completion doc + Vellum witness + registry DONE |

---

## 7. Third-party validation (API — not IDE)

Validation means a **deterministic caller with tight scope** — not Claude/Cursor reading your PR.

**Required proof artefact:**  
`perplexity-inbox/completed-by-antigravity__2026-06-30/APPLY-DOORWAY__verify-api-proof__v01__2026-06-30__antigravity.md`

Must include:

1. **Caller identity** — e.g. `gatekeeper.py` extended, CI job, or `curl` with scoped bearer (scope: `doorway:verify-only`)
2. **Good patch** — verify returns `"status":"pass"` (paste JSON)
3. **Bad patch** — verify returns `"status":"fail"` with explicit `deny` reason (paste JSON)
4. **No apply** on bad patch — exit non-zero, zero files changed (show `git status --porcelain`)
5. **Hook witness** — line from `harness-hooks.jsonl` showing verify event

**Acceptable callers:** `gatekeeper.py`, GitHub Actions step, `inbox_watcher` verify hook, local `curl` to `serve-verify`.  
**Not acceptable:** "Cascade-mac confirmed it looks fine in chat."

---

## 8. Finish sequence

```bash
cd .worktrees/antigravity-apply-doorway

git add control-centre/ outbound_doorway/ perplexity-inbox/completed-by-antigravity__2026-06-30/
git commit -m "$(cat <<'EOF'
feat(doorway): apply_doorway verify+apply with shape_gate integration.

EOF
)"
git push -u origin antigravity/apply-doorway
```

**Vellum:** completion row + compound delta (gap closed + paths).  
**Registry:** set R-003 DONE, R-004 DONE.  
**Chat to Ewan:** pointer only (inbox path + PR link).

---

## 9. References

| Doc | Role |
|-----|------|
| `harness/shape_gate.py` | Post-write OPA gate |
| `harness/gatekeeper.py` | Pre-flight deterministic checks pattern |
| `raw_searches/synthesis__deterministic_agent_validation__2026-06-30.md` | Architecture rationale |
| `BATON__cursor-setup-orientation__v01__2026-06-30__antigravity.md` | Outbound doorway law |
| `docs/OWNERSHIP-REGISTRY.md` | R-003 owner row |

---

[CLOSURE] branch=INSTRUCTIONS | assignee=antigravity | registry=R-003 | inbox=INSTRUCTIONS__apply-doorway-e2e__v01__2026-06-30__cursor.md | tier=INTUITED
