---
title: Prior art — detecting recurring subscriptions & unused spend from email alone
origin: perplexity-thread + ce-web-researcher (cascade-mac)
created: 2026-06-26
tier: STRUCTURED
feeds: email_actioning_agent/subscriptions.py
---

# Prior art: email-only subscription & unused-spend detection

Research run 2026-06-26 to ground the `subscriptions.py` detector. Headline: the
architecture we built (deterministic provider patterns first, AI only for the
unknown residue) is exactly what the leading email-only product uses — and the
**"unused / wasteful from email alone"** problem is commercially unaddressed and
academically unresearched. That gap is the novel part.

## Two camps
- **Bank-transaction-primary (dominant):** Rocket Money/Truebill, Trim, Hiatus,
  PocketGuard, Emma, Monarch, Copilot — connect via Plaid/MX/Finicity and pattern-match
  amount/interval over transactions. Privacy friction (full banking history) is the main objection.
- **Email-primary (emerging, privacy-differentiated):** Subby (Gmail OAuth read-only),
  Track-Subs (explicitly no bank link, multi-currency USD/EUR/GBP). **Track-Subs'
  engine = (1) deterministic match against 60+ provider patterns, (2) AI classifier
  for unknown senders, "temperature 0 — same result every scan."** This validates our
  deterministic-first + needs_ai-residue design directly.

## Most reliable deterministic signal: schema.org Invoice JSON-LD
Gmail markup (`<script type="application/ld+json">`, `@type: Invoice/Order`) carries
`provider`, `totalPaymentDue` (price+currency), `billingPeriod` (ISO-8601 P1M/P1Y),
`paymentDue`, `paymentStatus`. Authoritative WHEN present — but most senders omit it,
so it augments keyword signals. Implemented as `parse_invoice_jsonld()`.
Refs: developers.google.com/workspace/gmail/markup/reference/invoice

## Closest patents (service detection from email)
US11799884 + continuation US12137117 (2024): dual-layer = heuristic sender/subject
templates → bootstrap-train an ML classifier. Focus on service *existence* (account
creation, logins), NOT billing cadence or waste. Our billing+waste focus is beyond them.

## "Unused / wasteful" — the unaddressed gap (our novel signals)
No product detects waste from email alone (all use SSO/login usage data, e.g. Ramp:
30/60/90-day inactivity thresholds). Working email-only heuristics we implement:
- **payment_failed** (a forgotten tool quietly failing to bill) → cancel candidate
- **winback/dormant** ("we miss you", "come back") → cancel candidate
- **trial_converting** ("trial ends/ended") → review (surprise charge incoming)
- **price_increase** → review
- **overdue/cancellation** → review
- **duplicate/overlapping tools** (2+ vendors in one category) → review — documented
  by Ramp for B2B; novel applied to a personal email-only pipeline.

## Distinction that matters
Gmail's own "Manage Subscriptions" (July 2025) keys on `List-Unsubscribe` headers →
it finds **marketing** subscriptions, NOT billing ones (transactional billing mail is
exempt from List-Unsubscribe). So our NEWSLETTER(list-unsubscribe) vs FINANCIAL/billing
split is the right cut for *financial* control.

## Recommended deterministic signal set (implemented in subscriptions.py)
Tier 1 (near-certain): known-biller sender list; subject regex for subscription/
invoice/receipt/renewal/charged; amount+date proximity; schema.org JSON-LD; billing
sender patterns `(billing|invoices|receipts|payments|subscriptions|no-reply)@`.
Tier 2 (combine 2+): trial/price/winback/auto-renew phrasing; monthly±3d / annual±7d
thread cadence (needs inbox history — future).
Tier 3 (waste): winback, trial-converting, price-increase-on-existing-sub, duplicate
category, dormant-while-billing.

## Sources
Plaid transaction parsing & AI categorization; Finexer recurring detection; Track-Subs;
Subby; Yorba; Gmail Invoice schema + JSON-LD; US11799884 / US12137117; Ramp unused
subscriptions; Recurly win-back; Gmail "Manage Subscriptions" (List-Unsubscribe);
Apple renewal receipts. (Full URLs in the session research transcript.)
