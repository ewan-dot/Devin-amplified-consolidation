"""
tokens.py — the measurement spine.

The brief's whole value claim is token efficiency via code-execution-with-MCP:
full bodies stay in the sandbox; only structured actions enter model context.
This module measures that on REAL captured mail:

  naive_baseline  = tokens of N full email bodies loaded into context
                    (what a "dump every body into the model" loop costs)
  code_execution  = tokens of the compact structured JSONL the classifier emits
                    + the amortised classifier source (loaded once, reused)

We count with tiktoken (cl100k_base). That is an OpenAI tokenizer, not Claude's,
so absolute counts are an APPROXIMATION for Claude — but the *ratio* baseline:code
is stable across tokenizers, and the ratio is the brief's claim. Every number we
emit is labelled `approximate_tokenizer: cl100k_base`. We never echo the brief's
own 150k->2k figure as our result.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    _TOKENIZER = "cl100k_base"

    def count_tokens(text: str) -> int:
        return len(_ENC.encode(text or ""))
except Exception:  # pragma: no cover - fallback only if tiktoken missing
    _TOKENIZER = "approx-chars/4"

    def count_tokens(text: str) -> int:
        return (len(text or "") + 3) // 4


import math


@dataclass
class Measurement:
    n_emails: int                       # full-body sample the headline is computed on
    tokenizer: str
    naive_baseline_tokens: int          # full bodies in context, for the sample
    code_execution_emit_tokens: int     # compact structured rows, for the sample
    one_time_classifier_tokens: int     # classifier source: loaded ONCE per run, not per email
    # steady-state (the honest per-email comparison, excludes the one-time cost)
    per_email_baseline: float
    per_email_code_exec: float
    per_email_saving: float
    per_email_saving_pct: float
    breakeven_emails: object            # emails needed to repay the one-time load (None if no per-email saving)
    # projection to a realistic inbox size, one-time cost included
    projected_inbox_size: int
    projected_naive_tokens: int
    projected_codeexec_tokens: int
    projected_saving_pct: float
    note: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


def measure(emails, routed_dicts, classifier_source: str = "",
            projected_inbox_size: int = 200) -> Measurement:
    """Honest comparison on real mail.

    Steady state (per email): naive carries the full body; code-execution carries
    only the compact structured row. The classifier source is a ONE-TIME context
    load per run (not per email), reported separately with a breakeven point, and
    folded into the at-scale projection. We never echo the brief's own 98.7%.
    """
    emails = list(emails)
    n = len(emails)

    baseline_payload = "\n\n".join(
        f"From: {e.sender}\nSubject: {e.subject}\n\n{e.body}" for e in emails)
    baseline = count_tokens(baseline_payload)

    emit_payload = "\n".join(json.dumps(d, separators=(",", ":")) for d in routed_dicts)
    emit = count_tokens(emit_payload)

    src = count_tokens(classifier_source)

    pe_base = baseline / n if n else 0.0
    pe_code = emit / n if n else 0.0
    pe_save = pe_base - pe_code
    pe_pct = (pe_save / pe_base * 100.0) if pe_base else 0.0
    breakeven = math.ceil(src / pe_save) if pe_save > 0 else None

    N = projected_inbox_size
    proj_naive = round(pe_base * N)
    proj_code = round(src + pe_code * N)
    proj_pct = ((proj_naive - proj_code) / proj_naive * 100.0) if proj_naive else 0.0

    return Measurement(
        n_emails=n, tokenizer=_TOKENIZER,
        naive_baseline_tokens=baseline, code_execution_emit_tokens=emit,
        one_time_classifier_tokens=src,
        per_email_baseline=round(pe_base, 1), per_email_code_exec=round(pe_code, 1),
        per_email_saving=round(pe_save, 1), per_email_saving_pct=round(pe_pct, 2),
        breakeven_emails=breakeven,
        projected_inbox_size=N, projected_naive_tokens=proj_naive,
        projected_codeexec_tokens=proj_code, projected_saving_pct=round(proj_pct, 2),
        note=(f"approximate_tokenizer={_TOKENIZER}; absolute counts approximate for Claude, "
              f"ratios comparable; measured on {n} REAL full-body emails; classifier source "
              f"is a one-time per-run load (breakeven_emails repays it); projection assumes an "
              f"inbox of {N} of similar emails. Headline = per_email_saving_pct (steady state)."),
    )
