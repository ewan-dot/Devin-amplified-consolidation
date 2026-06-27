"""
_build_capture.py — one-shot builder that materialises captured_emails.jsonl from
REAL emails the model fetched via the Gmail MCP on 2026-06-26 (account
ewan@bykerbusinesshelp.ai). No synthetic content: full bodies are verbatim
plaintext from get_thread(FULL_CONTENT); snippet-bodied rows carry Gmail's own
real snippet as the body (body_source="snippet"). Re-runnable; overwrites output.

This exists because this environment has no in-sandbox MCP bridge — the capture
that a code-execution runtime would do in-sandbox was performed by the model and
frozen here so the pipeline runs on real data deterministically.
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path(__file__).with_name("captured_emails.jsonl")

# ---- 5 rows with REAL full plaintext bodies (verbatim from get_thread) ------- #
FULL = []

FULL.append(dict(
    inbox="byker", msg_id="19f03c5b3eae7080", thread_id="19f03c5b3eae7080",
    sender="notifications@github.com", to=["control-centre@noreply.github.com"],
    subject="[Amplified-Partners/control-centre] Run failed: Deploy to Beast - main (0bebb71)",
    label_ids=["UNREAD", "INBOX"], has_attachment=False, list_unsubscribe=False,
    body=r'''[Amplified-Partners/control-centre] Deploy to Beast workflow run

Repository: Amplified-Partners/control-centre
Workflow: Deploy to Beast
Duration: 10.0 seconds
Finished: 2026-06-26 11:51:34 UTC

View results: https://github.com/Amplified-Partners/control-centre/actions/runs/28236219157

Jobs:
  * deploy failed (2 annotations)

--
You are receiving this because you are subscribed to this thread.
Manage your GitHub Actions notifications: https://github.com/settings/notifications''',
))

FULL.append(dict(
    inbox="byker", msg_id="19f00a57279eedf1", thread_id="19f00a57279eedf1",
    sender="hello@notify.railway.app", to=["ewan@bykerbusinesshelp.ai"],
    subject="Final warning: Subscription cancellation for the Provision PostgreSQL team tomorrow",
    label_ids=["UNREAD", "IMPORTANT", "INBOX"], has_attachment=False, list_unsubscribe=True,
    body=r'''Final subscription cancellation warning

You have an unpaid invoice for the Provision PostgreSQL team.

Please pay the invoice to continue using Railway. Unless your pay your invoice, your subscription will be canceled tomorrow.

View invoice ( https://billing.stripe.com/p/session/live_... )

In the event we cancel your subscription due to nonpayment, the amount you owe Railway remains unchanged.

If you have questions about your unpaid invoice, please reply to this email.

Regards,
The Railway Team''',
))

FULL.append(dict(
    inbox="byker", msg_id="19f03c3330e276bf", thread_id="19f03c3330e276bf",
    sender="hi@app.kilocode.ai", to=["ewan@bykerbusinesshelp.ai"],
    subject="Action Required: Code Reviewer Disabled",
    label_ids=["UNREAD", "IMPORTANT", "INBOX"], has_attachment=False, list_unsubscribe=False,
    body=r'''Code Reviewer Disabled

Code Reviewer was disabled for this reason:
Code Reviewer was disabled because the selected model is not available for cloud agent sessions. Choose an available model, then enable Code Reviewer again.

Existing review history remains available. Resolve the issue, then enable Code Reviewer again to resume automatic reviews.

Update Code Reviewer settings.

If you have questions, reply to this email or contact hi@kilocode.ai.

The Kilo Team''',
))

FULL.append(dict(
    inbox="byker", msg_id="19f03afbed6e5efa", thread_id="19f03afbed6e5efa",
    sender="c.lim@hello.designcrowd.com", to=["ewan@bykerbusinesshelp.ai"],
    subject="Our Small Business Sale is ending, Ewan",
    label_ids=["UNREAD", "Label_36", "INBOX"], has_attachment=False, list_unsubscribe=True,
    body=r'''Hey Ewan,

Just a reminder that our Small Business Sale is ending soon.

You have until Tuesday (30 June) to launch any new design project with a £1 posting fee*

Simply create your design project here or use code CO-EOFY26-01WP when ordering.

If you have any questions, please let me know by replying to this email.

Kind regards,
Cheryl Lim | Support Team Leader
US:800 377 6955 | AU:1800 228 020 | UK:0800 680 0685
Level 2, 44a Foveaux St, Surry Hills NSW 2010, Australia

*Applies to new multiple-designer contests only. Ends Tuesday, 30 June 2026 at 11:59 PM.
You received this message because you are subscribed to DesignCrowd. Unsubscribe.''',
))

FULL.append(dict(
    inbox="byker", msg_id="19f0230b03f57f1d", thread_id="19f0230b03f57f1d",
    sender="noreply@x.ai", to=["ewan@bykerbusinesshelp.ai"],
    subject="Beast/MCP audit: AI-native gaps",
    label_ids=["IMPORTANT", "INBOX"], has_attachment=False, list_unsubscribe=True,
    body=r'''MPCP Beast Intelligence Review is ready
Beast/MCP audit: AI-native gaps

Plan (as per your style preference):
1. Formulate understanding - Clarify "MPCP server" and "the beast" via tools (MCP = Model Context Protocol, standard for AI-tool integration; Beast often refers to powerful local/remote AI setups like high-GPU Ollama hosts or MCP gateways).
2. Explore environment - Use sandbox tools (bash, read_file, grok-mcp if available) to inspect current state for changes.
3. Analyze for AI-nativeness - Radical honesty on dogfooding, strengths/weaknesses, gaps.
4. Document observations - For learning/transparency.
5. Give clear opinions + actionable recommendations - Meritocratic, additive (build on what's good), drive toward brilliant AI-native work that helps people. No sugarcoating.

This planning saves repeat cycles. Now executing.

Exploration Results (Transparency on What I "Dialed Into")
Continue reading on grok.com.
© 2026 X.AI LLC. Unsubscribe.''',
))

# ---- snippet-bodied REAL rows (Gmail's own snippet = body_source "snippet") -- #
# Real sender/subject/snippet/labels from search_threads on 2026-06-26.
SNIP = [
    ("19f03ba3fcf8b1f0", "notifications@github.com",
     "Re: [Amplified-Partners/agent-claude] feat(core): proxy-action ledger for non-commit AI_PARTNER_PROXY acts (PR #11)",
     "@Copilot commented on this pull request. Pull request overview Adds a durable, append-only JSONL proxy-action ledger for non-commit AI_PARTNER_PROXY actions",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19f03b21c9eec4a2", "notifications@github.com",
     "[Amplified-Partners/control-centre] Run failed: Deploy to Beast - main (b706ca9)",
     "Deploy to Beast: All jobs have failed View workflow run Status Job Annotations Deploy to Beast / deploy Failed in 6 seconds",
     ["UNREAD", "INBOX"]),
    ("19f01e93ad76477e", "notifications@github.com",
     "[Amplified-Partners/fleet-vellum] Run failed: Generate Monitoring Dashboards - main (8b275e0)",
     "Generate Monitoring Dashboards: All jobs have failed View workflow run Status Job Annotations",
     ["UNREAD", "INBOX"]),
    ("19f02ec02e9c030c", "support_at_hetzner.com_ampliand@duck.com",
     "Re: [Ticket#2026062503030731] Misc",
     "Dear Mr. Bramley, Your account has been blocked due to non payment, we can only unlock your servers if all overdue invoices have been paid. Please pay the invoices via our Administration Console",
     ["IMPORTANT", "INBOX"]),
    ("19f0069c922dd35e", "noreply_at_hetzner.com_ampliand@duck.com",
     "Power button press for your server AX162-R #2907522 (135.181.161.131) the beast",
     "Dear Mr. Bramley, Your assigned power button press for your server AX162-R #2907522 (135.181.161.131) the beast has just been initiated. This is an automatically generated email.",
     ["UNREAD", "INBOX"]),
    ("19f009c090676fb5", "workspace-noreply@google.com",
     "[Action Advised] Google Vids personal avatar feature and Admin control",
     "Review the Administrative controls available to you. Dear administrator, We're preparing to release a new feature in Google Vids that will allow users to create a personal avatar",
     ["UNREAD", "INBOX"]),
    ("19f00a95ed49166e", "learn@sentry.io",
     "New in Sentry: Snapshots, now in beta",
     "Generate screenshots of your application with each code change, diff the visuals from build to build, and see right in the PR if there are any visual changes",
     ["UNREAD", "Label_36", "INBOX"]),
    ("19f01b609796c95b", "rahul.vohra@superhuman.com",
     "Gift a month, get a month",
     "Hi Ewan, Thank you so much for using Superhuman Mail. You're the reason why we do what we do. On behalf of our whole team, I want to extend our warmest and most heartfelt of thanks",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19f00b1d0de2f481", "claudedesign@substack.com",
     "I stopped posting because it felt fake",
     "30% off yearly ends in a couple days, right before the weekend build rhythm kicks back in.",
     ["UNREAD", "Label_36", "INBOX"]),
    ("19f008dd7ff53bbc", "claudedesktop@substack.com",
     "I Almost Posted Just To Look Alive",
     "30% off yearly closes in a couple days, and I wanted to explain the silence before Sunday.",
     ["UNREAD", "Label_36", "INBOX"]),
    ("19f012a627f574c6", "neuronomicon+filmmaking_at_substack.com_ampliand@duck.com",
     "How I'm using video to world-build with my audience",
     "I'm testing my universe on you. Let's cook.",
     ["UNREAD", "Label_37", "INBOX"]),
    ("19f00f685a89d402", "noreply@inbox.xhamsterlive.com",
     "New content from favorite & trending models",
     "Enjoy your weekly dose of hotness",
     ["UNREAD", "Label_36", "INBOX"]),
    ("19f03d11bd93def3", "noreply@github.com",
     "[GitHub] You have used 100% of the GitHub AI Credits included for the Amplified Partners Enterprise account",
     "Your account has used all of its included GitHub AI Credits (3000 of 3000)",
     ["UNREAD", "INBOX"]),
    ("19f01ec2f3dedfaa", "notifications@github.com",
     "Re: [Amplified-Partners/shared-design-tokens] build(deps-dev): bump the npm_and_yarn group across 1 directory with 4 updates (PR #22)",
     "@dependabot requested your review on: Amplified-Partners/shared-design-tokens#22 build(deps-dev): bump the npm_and_yarn group across 1 directory with 4 updates as a code owner.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
]


# ---- real subscription/billing rows (snippet-bodied) captured 2026-06-26 ----- #
# High-signal recurring-spend mail across the inbox — the financial-control set.
SUBS = [
    ("19efe331fa53b6c7", "billing_at_hetzner.com_ampliand@duck.com",
     "Final Payment Warning / Services blocked (K0173938926)",
     "Dear Mr Ewan Bramley, Attached you will find your latest reminder as PDF file. Please contact us regarding your invoice. Final payment warning, services blocked.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19efc895225c5cdb", "failed-payments+acct_1MkZiULG36r4uSlK@stripe.com",
     "$90.00 payment to Circleback was unsuccessful",
     "We weren't able to charge the credit card you provided. Your $90.00 payment to Circleback was unsuccessful.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19efc1b5a6729a80", "noreply@md.getsentry.com",
     "Your free 14-day Business trial has ended",
     "Sentry Billing Period June 25 - July 24. Your free 14-day Business trial has ended. Your organization Amplified Partners has completed its 14-day free trial.",
     ["UNREAD", "INBOX"]),
    ("19efb27e9048872d", "upcoming-invoice+acct_1R1ePOJ7A6SsvrfS@stripe.com",
     "Your Kilo Code subscription will renew soon",
     "This is a friendly reminder that your Kilo Code subscription for Kilo Pass (Pro) will automatically renew on July 1, 2026.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19efa11d44e1e286", "invoice+statements+acct_1Om98nD4cNvH28G6@stripe.com",
     "Your receipt from Cognition AI Inc. #2769-1608",
     "Your receipt from Cognition AI Inc. #2769-1608. Payment received.",
     ["UNREAD", "INBOX"]),
    ("19ef5e57fc975a7f", "workspace-noreply@google.com",
     "IMPORTANT: Upcoming change to your AI Ultra Access subscription for bykerbusinesshelp.ai",
     "Your AI Ultra Access subscription will transition to an AI Expanded Access subscription beginning July 8, 2026.",
     ["UNREAD", "INBOX"]),
    ("19ef590398c0cf8c", "support@cognition.ai",
     "Payment Failed - Action Required",
     "Your most recent payment failed - update your payment details to keep using Devin. The most recent charge for $240.00 on June 23, 2026 failed.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19ef56367714fc26", "learn@sentry.io",
     "Trial ending: Limits will apply",
     "Your trial is ending soon. Here's what to expect after the trial. Your organization will move to the free plan with limits.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
    ("19ef2052655555d6", "notifications@circleback.ai",
     "Your Circleback trial ends in 2 days",
     "Your trial ends on June 25. There's still time to give Circleback a try.",
     ["UNREAD", "Label_36", "INBOX"]),
    ("19eec0bf900b3d81", "hello@notify.railway.app",
     "Subscription cancellation for the Provision PostgreSQL team in 5 days",
     "Subscription cancellation warning. You have an unpaid invoice for the Provision PostgreSQL team. Please pay the outstanding balance to continue using Railway.",
     ["UNREAD", "IMPORTANT", "INBOX"]),
]


def main() -> int:
    rows = []
    for d in FULL:
        d = dict(d)
        d.setdefault("headers", {})["body_source"] = "full"
        d["snippet"] = d["body"][:120]
        rows.append(d)
    for msg_id, sender, subject, snippet, labels in SNIP + SUBS:
        rows.append(dict(
            inbox="byker", msg_id=msg_id, thread_id=msg_id, sender=sender,
            to=["ewan@bykerbusinesshelp.ai"], subject=subject, snippet=snippet,
            body=snippet, label_ids=labels, has_attachment=False,
            list_unsubscribe=("substack" in sender or "@noreply" not in sender and "list" in snippet.lower()),
            headers={"body_source": "snippet"},
        ))
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows -> {OUT}  (full={len(FULL)}, snippet={len(SNIP)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
