"""
servers/ — one adapter per inbox.

The brief's pattern (Anthropic "Code Execution with MCP", 2025-11-04) is: each
inbox is an MCP server; the agent writes *code* that calls it; full bodies and
attachments stay in the sandbox; only structured actions enter model context.

In a code-execution runtime the adapter would wrap the live MCP server. In this
environment the MCP tools are model-invoked, so the live capture is performed
once by the model into a JSONL (config.CAPTURE_JSONL) and the adapters read from
that captured real data. The interface is identical either way, so swapping in a
true in-sandbox MCP bridge later is a drop-in change — no caller edits.
"""
from .base import Email, InboxAdapter, load_adapter

__all__ = ["Email", "InboxAdapter", "load_adapter"]
