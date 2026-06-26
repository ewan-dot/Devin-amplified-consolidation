# Related Work Map — Unified Sensor

*Plain summary: several teams already built pieces of this. Reuse them; don't rebuild. The Perplexity tarballs (25 Jun) are the canonical forward spec — v03 doctrine supersedes v01/v02.*

**Operating model:** Each IDE/seat owns one e2e deliverable (working + tested + shared artefact). Shared folders (`~/amplified-pipeline/`, `perplexity-inbox/`, control-centre, Vellum) are the handoff surface; IDE-local worktrees stay local until promoted. Unified sensor = cross-IDE visibility, not shared ownership. Full seat table → `docs/UNIFIED-SENSOR-PLAN.md` §Seat ownership.

---

## Active parallel efforts

| Effort | Where | Status | Relation | Seat (e2e owner) |
|---|---|---|---|---|
| **Perplexity master plan + tarballs** | `perplexity-inbox/` | Delivered 2026-06-25 | **SSOT for phases 0–7** | Perplexity (reader + trial) |
| **`unified_sensor/` Python module** | `perplexity-inbox/unified_sensor/` | Partial — gather + reader on Mac | Track A monitor input | Cursor |
| **Control-centre** | `~/control-centre/` | Live collectors + rules engine | Bridge target for Track A | Existing — Cursor bridges |
| **Vellum witness decorator** | Beast `/opt/amplified/vellum/` | Exists; v03 extension pending | Track B Phase 1 | Cascade-Mac |
| **Pipe weld** | research-pipe `staging_emitter.py` | Brief ready, not welded | Phase 2 — parallel | Claude Code |
| **Job-start hook** | Beast + M5 | Not wired | Phase 3 — after decorator | Claude Code |
| **Vellum senses brief** | `missing-thread-briefs__2026-06-24/vellum-senses/` | Pre-dates bundle | Supplement: `sensor_event.py` on M5 | Claude Code (M5 write path) |
| **Deterministic core brief** | `missing-thread-briefs__2026-06-24/deterministic-core/` | Antigravity completed gate | Pre-production harness | Antigravity (done) |
| **GitLens / worktree pattern** | `gitlens-integration__2026-06-24__cascade-mac/` | Proven on Cascade-Mac | Use for Beast PRs | Cascade-Mac |
| **Nightscout** | `clean-build/.../nightscout/` | **Different system** — RSS intel pipeline | Do not merge with unified sensor | — |

---

## Already built (reuse)

- `friction_monitor.sql` — 58KB detection maths on Beast (signal-reading synthesis queries this)
- `measurement_worker.py` — Beast measurement path
- Control-centre pane collectors: vellum, tailscale, credentials, github, litellm, brain, baton
- `unified_sensor/registry.py` — catalogue aligned to control-centre sources
- Loose inbox doctrine v01/v02 — audit trail only; **v03 in tarball is canonical**

---

## Overlap / conflict risks

| Risk | Mitigation |
|---|---|
| **Nightscout ≠ unified sensor** | Nightscout = external signal scoring; unified sensor = boundary witness + fleet health |
| **Cron vs job-start reader** | v03 explicitly rejects cron; hook at job-start only |
| **Two "sensor" modules** | Mac `unified_sensor/` (read) vs M5 `sensor_event.py` (write) — complementary |
| **control-centre vs friction_monitor** | Mac module bridges control-centre; Beast hook uses friction_monitor.sql — both valid per layer |
| **Two observability panes** | Vellum witness Postgres rows ≠ control-centre DuckDB `stats_events` — complementary, not substitutes |
| **Harness naming** | `amplified_permissions.py` ≠ open-door/RodGuard ≠ dossier `harness_event` |
| **INTUITED tier floor** | Mac witness posts may 403 until Vellum admin raises floor — resolve before STRUCTURED rows |
| **Prove-it-small vs full mesh** | Wire @witness on five boundaries before osquery/Falco (Pillar 4) |

---

## Integration hooks

1. **Perplexity job-start** → read `unified_sensor` snapshot → emit Vellum `witness_read`
2. **Five trial boundaries** → `@vellum.witness` on Beast (Phase 1)
3. **Pipe weld** → `research_pipe.staging_emit` boundary witnessed (Phase 2)
4. **Pillar 4** → Infisical identity plane after Phase 4 trial (Phase 5)
5. **FACILITATOR-COCKPIT** → update baton when WP2/WP3 complete

---

## Gaps (nobody owns yet)

- CLI / shell wrapper for Perplexity to invoke snapshot read
- Vellum `witness_read` emission from Mac module
- Beast decorator extension + unit tests (Cascade-Mac)
- Job-start hook wiring (Claude Code on M5)
- Phase 0 + signal-reading baton decisions (Ewan)

---

## Recommended sequencing

1. Absorb tarballs + v03 (done) → follow `docs/UNIFIED-SENSOR-PLAN.md`
2. Finish Track A CLI + smoke test before Perplexity session hook
3. Phase 1 decorator (Cascade-Mac) in parallel with Phase 2 pipe weld
4. Phase 3 hook after Phase 1 — needs decorator output
5. Do **not** start Phase 5 Infisical migration until Phase 4 trial passes
6. Read `vellum-senses` brief only to wire M5 write path — do not replace v03
