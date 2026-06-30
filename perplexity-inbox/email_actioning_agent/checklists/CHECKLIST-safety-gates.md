# CHECKLIST — safety gates

The agent **actions** a live inbox, so every side effect is decision-first and
gated. Verified properties (each has a test in `tests/`):

- [x] **Default dry-run** — a bare `run` mutates nothing (`test_dry_run_never_mutates`)
- [x] **Tier C never auto-runs** — FINANCIAL/URGENT_HUMAN (external send/Drive) are
      emitted as action-requests even with `--apply` (`test_tier_c_never_auto_runs_even_with_apply`)
- [x] **Tier B only under --apply** — label/archive are reversible and logged (`test_apply_tier_b_records_intent`)
- [x] **Tier A is inbox-local** — JSONL emit into perplexity-inbox; **no direct Beast write** (doctrine forbids `beast_write`)
- [x] **No email is ever sent / replied** — there is no send path; the brief is *actioning, not replying*
- [x] **Gate = repo doctrine** — `amplified_permissions.classify()` decides the tier (`test_tier_mapping_via_doctrine`)
- [x] **Phishing-safe** — suspected-phishing financial mail (e.g. Hetzner "pay overdue invoices") routes FINANCIAL → Tier C gated; **no link is followed, no payment actioned**
- [x] **Fails cautious** — unknown/low-confidence routes to NOISE/`needs_ai`, never to a destructive action

## Prohibited actions (must remain human-only — never coded in)
- [ ] Entering payment/credentials, paying invoices, moving money
- [ ] Granting/altering share or access permissions
- [ ] Permanent deletion (we archive, never hard-delete/trash)
- [ ] Sending messages/replies on the user's behalf
These are intentionally absent from the codebase. Adding any requires explicit
human authorisation per action.
