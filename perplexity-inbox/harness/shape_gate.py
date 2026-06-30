#!/usr/bin/env python3
"""Shape gate — deterministic tier + attribution check at boundaries (Rod 1).

Non-judgmental: checks shape (tier arithmetic, required fields), not semantic truth.
Human and agent emissions use the same OPA policy; ceilings differ only by promotion path.

SSOT: perplexity-inbox/harness/
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
OPA_QUERY = "data.amplified.boundary.deny"
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_SECRET_RE = re.compile(
    r"sk-[a-zA-Z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"xox[baprs]-[0-9A-Za-z-]{10,}|"
    r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"
)

TIER_ORDER: dict[str, int] = {
    "INTUITED": 1,
    "STRUCTURED": 2,
    "MEASURED": 3,
    "PROVEN": 4,
}


def ssot_root() -> Path:
    env = os.environ.get("AMPLIFIED_INBOX", "").strip()
    if env:
        return Path(env).expanduser()
    return Path(__file__).resolve().parent.parent


def _load_actors() -> dict[str, Any]:
    path = Path(__file__).resolve().parent / "actors.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def opa_bundle_candidates() -> list[str]:
    root = ssot_root()
    return [
        str(root / "harness" / "opa"),
        os.path.expanduser("~/agent-claude-wt/doors-harness/harness/opa"),
        os.path.expanduser("~/harness/opa"),
        "/Users/ewansair/container on m5/harness/opa",
    ]


def resolve_opa_bundle() -> str | None:
    for path in opa_bundle_candidates():
        resolved = os.path.expanduser(path)
        if os.path.isdir(resolved):
            return resolved
    return None


def witness(hook: str, event: str, ok: bool, detail: dict[str, Any]) -> None:
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"ts": time.time(), "hook": hook, "event": event, "ok": ok, **detail}
                )
                + "\n"
            )
    except Exception:
        pass


def extract_frontmatter(content: str) -> dict[str, Any] | None:
    m = _FRONTMATTER_RE.match(content)
    if not m:
        return None
    try:
        import yaml  # type: ignore[import]

        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return None


def classify_actor(author: str, actors: dict[str, Any]) -> str:
    if not author:
        return "unknown"
    low = author.strip().lower()
    human = {a.lower() for a in actors.get("human_authors", [])}
    if low in human:
        return "human"
    return "agent"


def infer_author(fm: dict[str, Any], seat: str) -> str:
    for key in ("author", "signed_by", "Signed-by"):
        if fm.get(key):
            return str(fm[key]).strip()
    return seat.strip().lower() if seat else ""


def _has_evidence(fm: dict[str, Any]) -> bool:
    for key in ("evidence", "calibration_ref", "evidence_refs", "source_id"):
        val = fm.get(key)
        if val:
            return True
    return False


def _list_field(fm: dict[str, Any], key: str) -> list[Any]:
    val = fm.get(key)
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def _metadata_has_secret(fm: dict[str, Any]) -> bool:
    blob = json.dumps(fm, default=str)
    return bool(_SECRET_RE.search(blob))


def _path_ok(path: str) -> bool:
    try:
        resolved = Path(path).expanduser().resolve()
    except OSError:
        return False
    roots = [
        ssot_root(),
        Path(os.path.expanduser("~/amplified-pipeline")),
        Path(os.path.expanduser("~/ingestion-to-research-pipe")),
        Path(os.path.expanduser("~/agent-claude-wt")),
        Path("/Users/ewansair/container on m5"),
        Path("/tmp"),
    ]
    for root in roots:
        try:
            if resolved.is_relative_to(root.expanduser().resolve()):
                return True
        except (OSError, ValueError):
            continue
    return False


def build_opa_input(
    fm: dict[str, Any], path: str, seat: str, *, force_llm: bool | None = None
) -> dict[str, Any]:
    actors = _load_actors()
    claim = (fm.get("epistemic_tier") or "").upper()
    origin = (fm.get("origin_type") or "").lower()
    author = infer_author(fm, seat)
    emitter = classify_actor(seat, actors)
    actor = emitter

    if "agent_synthesis" in origin or "llm" in origin:
        input_tiers = ["STRUCTURED"]
    else:
        input_tiers = [claim] if claim else []

    if force_llm is not None:
        consulted_llm = force_llm
    elif fm.get("consulted_llm_at_runtime") is not None:
        consulted_llm = bool(fm.get("consulted_llm_at_runtime"))
    elif actor == "agent" and actors.get("agent_llm_consulted_default", True):
        consulted_llm = True
    else:
        consulted_llm = False

    claim_num = TIER_ORDER.get(claim, 0)
    if claim_num >= TIER_ORDER["MEASURED"]:
        has_evidence = _has_evidence(fm)
        precondition_floor = claim if has_evidence else "STRUCTURED"
    else:
        precondition_floor = claim or "INTUITED"

    valid_until = fm.get("valid_until", "")
    if valid_until:
        try:
            from datetime import date

            if date.fromisoformat(str(valid_until)) < date.today():
                precondition_floor = "INTUITED"
                input_tiers = ["INTUITED"]
        except ValueError:
            pass

    value: dict[str, Any] = {
        "id": path,
        "author": author,
        "emitter_class": emitter,
        "actor_class": actor,
        "consulted_llm_at_runtime": consulted_llm,
        "input_tiers": input_tiers,
        "precondition_floor": precondition_floor,
        "proxy_act": bool(fm.get("proxy_act")),
        "origin_type": fm.get("origin_type") or "",
        "source_refs": _list_field(fm, "source_refs"),
        "evidence_refs": _list_field(fm, "evidence_refs"),
        "attribution_stripped": bool(fm.get("attribution_stripped")),
        "laundering_witness_id": fm.get("laundering_witness_id") or "",
        "money_boundary": bool(fm.get("money_boundary")),
        "counterparty_consent": bool(fm.get("counterparty_consent")),
        "win_win_clear": bool(fm.get("win_win_clear")),
        "harm_declared": bool(fm.get("harm_declared")),
        "no_one_hurt": bool(fm.get("no_one_hurt")),
        "rubric_scored": bool(fm.get("rubric_scored")),
        "author_blind": bool(fm.get("author_blind")),
        "contains_pii": bool(fm.get("contains_pii")),
        "pii_minimised": bool(fm.get("pii_minimised")),
        "client_scope": bool(fm.get("client_scope")),
        "client_consent": bool(fm.get("client_consent")),
        "has_secret_in_metadata": _metadata_has_secret(fm),
        "path_ok": _path_ok(path),
        "system_of_record": fm.get("system_of_record") or "",
    }
    promo = fm.get("promotion_record_id")
    if promo:
        value["promotion_record_id"] = str(promo)
    if claim:
        value["claim"] = claim
    if fm.get("contributors"):
        value["contributors"] = fm.get("contributors")

    return {"emitted_values": [value]}


def opa_check(opa_input: dict[str, Any]) -> list[str]:
    try:
        bundle = resolve_opa_bundle()
        if not bundle:
            witness("shape-gate", "opa-bundle-missing", True, {"candidates": opa_bundle_candidates()})
            return []

        result = subprocess.run(
            ["opa", "eval", "-d", bundle, "-I", OPA_QUERY],
            input=json.dumps(opa_input),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            witness("shape-gate", "opa-error", True, {"stderr": result.stderr[:200]})
            return []
        data = json.loads(result.stdout)
        denies = data["result"][0]["expressions"][0]["value"]
        return denies if isinstance(denies, list) else []
    except Exception as exc:
        witness("shape-gate", "opa-exception", True, {"note": str(exc)[:200]})
        return []


def check_content(content: str, path: str, seat: str) -> tuple[list[str], dict[str, Any] | None]:
    fm = extract_frontmatter(content)
    if fm is None:
        return [], None
    errors = []
    if not fm.get("epistemic_tier"):
        errors.append(f"P0 (shape §2): {path!r} crosses boundary without epistemic_tier")
    
    # Run dynamic glasses validation if schema_code is present
    if "schema_code" in fm:
        try:
            import sys
            harness_path = str(Path(__file__).resolve().parent)
            if harness_path not in sys.path:
                sys.path.append(harness_path)
            from glasses_loader import load_lens_glasses
            res = load_lens_glasses(content)
            if res.get("status") in ("INVALID", "ERROR"):
                errors.extend([f"Lens Validation Error: {err}" for err in res.get("errors", [])])
        except Exception as e:
            errors.append(f"Glasses validation system error: {e}")
            
    opa_input = build_opa_input(fm, path, seat)
    opa_errors = opa_check(opa_input)
    errors.extend(opa_errors)
    return errors, fm


def check_file(path: str, seat: str) -> tuple[list[str], dict[str, Any] | None]:
    try:
        content = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        witness("shape-gate", "read-error", True, {"path": path, "note": str(exc)[:120]})
        return [], None
    return check_content(content, path, seat)


def emit_verdict(
    denies: list[str],
    path: str,
    fm: dict[str, Any] | None,
    seat: str,
    *,
    hook_name: str = "shape-gate",
) -> int:
    if fm is None:
        witness(hook_name, "no-frontmatter", True, {"path": path, "seat": seat})
        return 0
    if denies:
        for msg in denies:
            print(f"[shape-gate] {msg}", file=__import__("sys").stderr)
        witness(
            hook_name,
            "P0",
            False,
            {"path": path, "seat": seat, "denies": denies, "author": fm.get("author")},
        )
        return 0
    witness(
        hook_name,
        "allow",
        True,
        {
            "path": path,
            "seat": seat,
            "tier": fm.get("epistemic_tier", "unknown"),
            "author": infer_author(fm, seat),
        },
    )
    return 0
