"""
Unit tests for the email-actioning agent.

These use small SYNTHETIC fixtures (fine for unit tests). The live measured demo
runs on real captured mail only — see harness/run_demo.sh and the README. The
"No mock responses ever" rule applies to the demo/measurement, not to unit fixtures.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

PKG_PARENT = Path(__file__).resolve().parent.parent
if str(PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(PKG_PARENT))

from email_actioning_agent.classifier import classify
from email_actioning_agent.config import ROUTES
from email_actioning_agent.router import route_one, _tier_for
from email_actioning_agent.servers.base import Email, JsonlAdapter
from email_actioning_agent.tokens import measure


def mk(**kw) -> Email:
    base = dict(inbox="byker", msg_id="m1", thread_id="t1", sender="x@example.com",
                to=["ewan@bykerbusinesshelp.ai"], subject="", snippet="", body="")
    base.update(kw)
    return Email.from_dict(base)


# ---- classifier ---------------------------------------------------------- #

def test_infra_critical_beats_everything():
    e = mk(sender="notifications@github.com", subject="CI pipeline failed on main",
           body="Your deploy failed: incident on container postgres")
    c = classify(e)
    assert c.category == "INFRA_CRITICAL"
    assert c.work_tier == "high_stakes"


def test_financial_detected():
    e = mk(sender="billing@stripe.com", subject="Your invoice is ready",
           body="Payment of £40 received. Receipt attached.", has_attachment=True)
    c = classify(e)
    assert c.category == "FINANCIAL"
    assert c.work_tier == "high_stakes"


def test_newsletter_vs_attribution():
    plain = mk(sender="news@store.substack.com", subject="Weekly deals",
               body="Big sale this week", list_unsubscribe=True)
    assert classify(plain).category == "NEWSLETTER"

    research = mk(sender="ai@labs.substack.com", subject="New MCP + Claude agent patterns",
                  body="Deep dive on agentic LLM token context engineering", list_unsubscribe=True)
    assert classify(research).category == "ATTRIBUTION"


def test_urgent_human():
    e = mk(sender="Jane Partner <jane@realco.com>", subject="Quick question — can you respond today?",
           body="Are you available for a call? Action required by deadline.")
    c = classify(e)
    assert c.category == "URGENT_HUMAN"
    assert c.work_tier == "high_stakes"


def test_confident_noise_from_noreply_sender():
    e = mk(sender="noreply@randompromo.com", subject="hello", body="...")
    c = classify(e)
    assert c.category == "NOISE"
    assert c.confidence >= 0.5          # two noise-sender signals -> confident


def test_unmatched_defaults_to_low_confidence_noise():
    # No signal at all: obscure machine sender, no personal name, no keywords.
    e = mk(sender="system@obscure-domain.io", subject="ping", body="ok")
    c = classify(e)
    assert c.category == "NOISE"
    assert c.confidence <= 0.3
    assert c.signals == ["unmatched-default"]


def test_bulk_path_truncates():
    long_body = "x" * 50000
    e = mk(sender="news@x.substack.com", subject="digest", body=long_body, list_unsubscribe=True)
    c = classify(e, truncate=1000)
    assert c.truncated_chars == 1000   # bulk path only looked at 1000 chars


# ---- router / gating ----------------------------------------------------- #

def test_tier_mapping_via_doctrine():
    assert _tier_for(ROUTES["INFRA_CRITICAL"])[0] == "A"     # write_inbox
    assert _tier_for(ROUTES["ATTRIBUTION"])[0] == "A"
    assert _tier_for(ROUTES["NEWSLETTER"])[0] == "B"          # label
    assert _tier_for(ROUTES["NOISE"])[0] == "B"               # archive
    assert _tier_for(ROUTES["FINANCIAL"])[0] == "C"           # send -> hard gate
    assert _tier_for(ROUTES["URGENT_HUMAN"])[0] == "C"


def test_dry_run_never_mutates():
    e = mk(sender="news@x.substack.com", subject="d", body="b", list_unsubscribe=True)
    c = classify(e)
    ad = JsonlAdapter("byker", "/nonexistent.jsonl")
    r = route_one(c, e, ad, apply=False)
    assert r.performed is False


def test_tier_c_never_auto_runs_even_with_apply():
    e = mk(sender="billing@stripe.com", subject="invoice", body="payment receipt")
    c = classify(e)
    ad = JsonlAdapter("byker", "/nonexistent.jsonl")
    r = route_one(c, e, ad, apply=True)
    assert r.tier == "C"
    assert r.performed is False
    assert "action_request" in r.detail


def test_apply_tier_b_records_intent():
    e = mk(sender="noreply@promo.com", subject="x", body="y")
    c = classify(e)           # -> NOISE -> archive (Tier B)
    ad = JsonlAdapter("byker", "/nonexistent.jsonl")
    r = route_one(c, e, ad, apply=True)
    assert r.tier == "B"
    # JsonlAdapter is a dry-run no-op, so performed stays False but intent recorded.
    assert r.detail["action"]["op"] == "archive"


# ---- measurement --------------------------------------------------------- #

def test_determinism_boundary_needs_ai():
    # confident newsletter -> deterministic, zero model tokens
    nl = classify(mk(sender="news@x.substack.com", subject="d", body="b", list_unsubscribe=True))
    assert nl.resolution == "deterministic" and nl.needs_ai is False
    # urgent human action -> needs AI (judge/draft)
    uh = classify(mk(sender="Jane <jane@realco.com>", subject="can you respond today? action required",
                     body="are you available"))
    assert uh.category == "URGENT_HUMAN" and uh.needs_ai is True
    # low-confidence default -> needs AI triage
    lc = classify(mk(sender="system@obscure-domain.io", subject="ping", body="ok"))
    assert lc.needs_ai is True and lc.ai_reason == "low_confidence_triage"


def test_extract_infra_deterministic():
    from email_actioning_agent.extract import extract_infra
    e = mk(sender="notifications@github.com", subject="[Org/repo] Run failed: Deploy (abc)",
           body="All jobs have failed. View results: https://github.com/Org/repo/actions/runs/12345")
    x = extract_infra(e)
    assert x["repo"] == "Org/repo" and x["run_id"] == "12345" and x["status"] == "failed"


def test_extract_financial_deterministic():
    from email_actioning_agent.extract import extract_financial
    e = mk(sender="billing@stripe.com", subject="Invoice INV-2026-09",
           body="Amount due £40.00 for your subscription.")
    x = extract_financial(e)
    assert x["vendor"] == "stripe.com" and x["amounts_found"] is True
    assert x["invoice_ref"] == "INV-2026-09"


def test_telemetry_health_verdict():
    from email_actioning_agent.telemetry import RunReport, health_verdict
    base = dict(run_id="r", ts="t", n_emails=5, inboxes_authed=1, inboxes_configured=3,
                by_category={}, by_tier={}, deterministic=5, needs_ai=0,
                deterministic_pct=100.0, tier_c_pending=0, tokens={})
    assert health_verdict(RunReport(**base)) == "OK"
    assert health_verdict(RunReport(**{**base, "warnings": ["x"]})) == "DEGRADED"
    assert health_verdict(RunReport(**{**base, "errors": ["boom"]})) == "FAILED"
    assert health_verdict(RunReport(**{**base, "n_emails": 0})) == "FAILED"


def test_subscription_payment_failed_is_cancel_candidate():
    from email_actioning_agent.subscriptions import detect
    e = mk(sender="failed-payments+acct_x@stripe.com",
           subject="$240.00 payment to Cognition AI Inc. was unsuccessful",
           body="We weren't able to charge the credit card you provided.")
    s = detect(e)
    assert s is not None and s.signal_type == "payment_failed"
    assert s.recommended_action == "cancel_candidate"
    assert s.vendor == "Cognition AI Inc."        # recovered from subject, not 'stripe.com'
    assert s.amount == "$240.00"


def test_subscription_trial_detected_despite_weak_core():
    from email_actioning_agent.subscriptions import detect
    e = mk(sender="learn@sentry.io", subject="Trial ending: Limits will apply",
           body="Your trial is ending soon. You'll move to the free plan with limits.")
    s = detect(e)
    assert s is not None and s.signal_type == "trial_converting" and s.unused_risk == "high"


def test_subscription_non_billing_email_is_none():
    from email_actioning_agent.subscriptions import detect
    e = mk(sender="friend@example.com", subject="lunch?", body="are you free thursday")
    assert detect(e) is None


def test_overlap_dedups_vendor_name_variants():
    from email_actioning_agent.subscriptions import overlaps, detect
    es = [
        mk(msg_id="a", sender="learn@sentry.io", subject="Trial ending", body="your trial is ending"),
        mk(msg_id="b", sender="noreply@md.getsentry.com", subject="trial has ended", body="your free trial has ended"),
        mk(msg_id="c", sender="upcoming-invoice@stripe.com", subject="Your Kilo Code subscription will renew", body="renew"),
    ]
    subs = [s for s in (detect(e) for e in es) if s]
    ov = overlaps(subs)
    # sentry.io + md.getsentry.com collapse to one vendor -> no false observability overlap
    assert not any(o["category"] == "observability" for o in ov)


def test_jsonld_invoice_parser():
    from email_actioning_agent.subscriptions import parse_invoice_jsonld
    html = ('<html><script type="application/ld+json">'
            '{"@type":"Invoice","provider":{"name":"Acme"},'
            '"totalPaymentDue":{"price":"12.00","priceCurrency":"GBP"},'
            '"billingPeriod":"P1M","paymentStatus":"PaymentDue"}</script></html>')
    inv = parse_invoice_jsonld(html)
    assert inv["provider"] == "Acme" and inv["amount"] == "12.00"
    assert inv["currency"] == "GBP" and inv["billing_period"] == "P1M"


def test_measure_per_email_saving_and_projection():
    emails = [mk(msg_id=f"m{i}", subject="s", body="word " * 500) for i in range(10)]
    routed = [{"msg_id": e.msg_id, "category": "NOISE", "route": "NOISE", "tier": "B"} for e in emails]
    m = measure(emails, routed, classifier_source="def classify(): pass", projected_inbox_size=200)
    assert m.n_emails == 10
    # full body >> compact row, so steady-state per-email saving is large & positive
    assert m.per_email_baseline > m.per_email_code_exec
    assert m.per_email_saving_pct > 0
    assert m.breakeven_emails is not None
    # at inbox scale the one-time classifier cost is dwarfed -> net positive
    assert m.projected_codeexec_tokens < m.projected_naive_tokens


# ---- regression: the substring / precedence bugs found on real mail ---------- #

def test_no_substring_false_positive_vat_in_avatar():
    e = mk(sender="workspace-noreply@google.com", subject="Google Vids personal avatar feature",
           body="create a personal avatar using their own likeness")
    assert classify(e).category != "FINANCIAL"   # 'vat' must NOT match inside 'avatar'


def test_no_substring_false_positive_digits_in_ticket():
    e = mk(sender="support@vendor.com", subject="Re: [Ticket#2026062503030731] Misc",
           body="reference number 2026062503030731 for your records")
    # '503' inside the ticket number must not trigger an infra incident on its own
    assert "infra:503" not in classify(e).signals


def test_unpaid_invoice_beats_infra_noun():
    # mentions postgres (infra noun) but is really a billing email -> FINANCIAL wins
    e = mk(sender="hello@notify.railway.app", list_unsubscribe=True,
           subject="Final warning: subscription cancellation",
           body="You have an unpaid invoice for the Provision PostgreSQL team. Please pay the invoice.")
    assert classify(e).category == "FINANCIAL"


def test_real_incident_beats_billing_footer():
    e = mk(sender="notifications@github.com", subject="Run failed: Deploy to Beast",
           body="All jobs have failed. (this email also has an unsubscribe/invoice footer)")
    assert classify(e).category == "INFRA_CRITICAL"


def test_vendor_newsletter_not_infra():
    # infra-vendor sender but a marketing newsletter (List-Unsubscribe) -> not INFRA
    e = mk(sender="learn@sentry.io", subject="New in Sentry: Snapshots, now in beta",
           body="Generate screenshots of your application with each code change", list_unsubscribe=True)
    assert classify(e).category != "INFRA_CRITICAL"
