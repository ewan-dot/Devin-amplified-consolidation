# Session Start — All Seats

**For:** Any fleet seat · **Any IDE or shell** · **Date:** 2026-06-25

Deterministic opening. No LLM in the path.

---

## Run (every session)

From inbox root:

```bash
./scripts/session-start.sh
```

Fixed sequence: optional `amplified_permissions.py` self-test → `monitor.py --signals-only` (falls back to `python3 -m unified_sensor --local-only` on collection failure) → prints `docs/INBOX-STATUS.md` and latest `INBOX-INDEX__*` head.

---

## Exit codes

| Code | Verdict | Seat action |
|---:|---|---|
| **0** | proceed | Pick work from [`AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`](AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md); check ownership in INBOX-STATUS |
| **1** | warn | Proceed with note — copy `VERDICT=` line to Vellum; flag warnings before heavy work |
| **2** | halt | **Stop** — witness on Vellum, do not start substantive work until cleared |

---

## Vellum (human/seat-authored, script-triggered)

After the harness runs, post intent to Vellum task queue. **Author = your seat** (`cursor`, `cascade`, `devin`, …). Paste the harness `VERDICT=` line — do not re-interpret the sensor JSON.

Phase 0 baton still blocking some threads: [`BATON__phase-0__ewan-fill-in__v01__2026-06-25.md`](BATON__phase-0__ewan-fill-in__v01__2026-06-25.md)

---

## Finish rule

Done = company-owned (shared path or Vellum witness). Full model: [`AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`](AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md)

**Path:** `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`
