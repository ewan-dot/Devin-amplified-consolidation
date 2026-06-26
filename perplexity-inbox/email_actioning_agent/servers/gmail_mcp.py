"""
gmail_mcp.py — mapping between Gmail MCP tools and the Email record.

This module documents (and, in a code-execution runtime, would implement) the
live Gmail-MCP-backed adapter. In this environment the MCP tools are invoked by
the model, so the model performs the capture once using the mapping below and
writes Email-shaped rows to config.CAPTURE_JSONL; servers.base.JsonlAdapter then
serves them. Keeping the mapping here means the live adapter is a small edit, not
a rewrite.

Capture recipe (model-side, read-only):
    search_threads(query=..., pageSize=N)      -> thread ids
    get_thread(threadId, messageFormat=FULL_CONTENT) -> full bodies + headers
  For each message build:
    msg_id            <- message id
    thread_id         <- thread id
    sender            <- From header
    to                <- To recipients
    subject           <- Subject
    snippet           <- snippet
    body              <- plaintext_body (FULL — stays in sandbox)
    label_ids         <- labelIds
    has_attachment    <- attachment_ids present
    list_unsubscribe  <- ('List-Unsubscribe' in headers) or category Promotions

Action recipe (only under --apply, after doctrine gate authorises):
    apply_label(msg_id, label) <- label_message(messageId, labelIds=[<id of label>])
    archive(msg_id)            <- label_message removing 'INBOX' (Gmail archive)
"""
from __future__ import annotations

# Gmail system label ids used by the action recipes above.
INBOX_LABEL = "INBOX"

# Route -> Gmail user label display name we would apply under --apply.
ROUTE_LABEL = {
    "NEWSLETTER": "EAA/Newsletter",
    "NOISE": "EAA/Noise-Archived",
    "INFRA_CRITICAL": "EAA/Infra-Critical",
    "FINANCIAL": "EAA/Financial",
    "ATTRIBUTION": "EAA/Attribution",
    "URGENT_HUMAN": "EAA/Urgent",
}
