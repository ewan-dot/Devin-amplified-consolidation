"""
email_actioning_agent — token-efficient, multi-inbox email *actioning* (not replying).

Built from perplexity-inbox/claude-gmail-brief.md (2026-06-26). Pattern: Anthropic
"Code Execution with MCP" — full bodies stay in the sandbox, only structured
actions enter model context. Deterministic classifier-as-code (no LLM in the
decision path), doctrine-gated router (reuses amplified_permissions), real token
measurement on real captured mail.

tier: STRUCTURED
"""
__version__ = "0.1.0"
