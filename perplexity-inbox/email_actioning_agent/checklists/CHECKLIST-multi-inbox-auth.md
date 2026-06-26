# CHECKLIST — multi-inbox auth

Three inboxes are configured (`config.INBOXES`). Live capture needs a Gmail OAuth
connection per account. **OAuth/account auth is a user-only action** (the agent
never enters passwords or completes OAuth) — so the agent builds the adapter and
waits; it never fakes an unauthed inbox.

| Inbox | Address | State | Action needed |
|-------|---------|-------|---------------|
| byker | ewan@bykerbusinesshelp.ai | ✅ authed | none — captured & processed |
| amplified | ewan@amplifiedpartners.ai | ⛔ needs OAuth | user connects Gmail MCP for this account |
| gmail | ewanbramley@gmail.com | ⛔ needs OAuth | user connects Gmail MCP for this account |

> Note: `amplifiedpartyners` in chat was read as a typo for **amplifiedpartners**.
> Correct in `config.py` if that's wrong.

## Per inbox, once OAuth is granted
1. Capture real mail for the account into `data/captured_emails.jsonl` (live
   adapter, or extend `_build_capture.py`) with `inbox=<key>`.
2. Flip `authed=True` for that inbox in `config.py`.
3. `python -m email_actioning_agent run` → the `inbox_unauthed` warning for it
   clears; `health` should move toward OK once all three are authed.

Until then `health=DEGRADED` is the **correct** signal — it is telling the truth
about coverage, not malfunctioning.
