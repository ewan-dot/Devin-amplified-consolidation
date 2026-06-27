"""Tests for shape gate — human + agent, same bee."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

INBOX = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INBOX))

from harness.shape_gate import (  # noqa: E402
    build_opa_input,
    check_content,
    classify_actor,
    resolve_opa_bundle,
)

OPA = Path(__file__).resolve().parents[1] / "harness" / "opa"


def _opa_denies(opa_input: dict) -> list[str]:
    r = subprocess.run(
        ["opa", "eval", "-d", str(OPA), "-I", "data.amplified.boundary.deny"],
        input=json.dumps(opa_input),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(r.stdout)["result"][0]["expressions"][0]["value"]


@pytest.fixture(scope="module")
def require_opa():
    if subprocess.run(["opa", "version"], capture_output=True).returncode != 0:
        pytest.skip("opa not installed")


def test_bundle_resolves():
    assert resolve_opa_bundle()


def test_human_intuited_allow(require_opa):
    fm = {
        "epistemic_tier": "INTUITED",
        "origin_type": "human_steer",
        "author": "ewan",
    }
    inp = build_opa_input(fm, "/tmp/h.md", "ewan")
    assert _opa_denies(inp) == []


def test_human_proven_without_promotion_p0(require_opa):
    fm = {
        "epistemic_tier": "PROVEN",
        "origin_type": "human_steer",
        "author": "ewan",
    }
    inp = build_opa_input(fm, "/tmp/h.md", "ewan")
    denies = _opa_denies(inp)
    assert any("shape §7" in d for d in denies)


def test_agent_intuited_allow(require_opa):
    fm = {
        "epistemic_tier": "INTUITED",
        "origin_type": "agent_synthesis",
        "author": "cursor",
        "win_win_clear": True,
    }
    inp = build_opa_input(fm, "/tmp/a.md", "cursor")
    assert _opa_denies(inp) == []


def test_agent_win_win_gate_p0(require_opa):
    fm = {
        "epistemic_tier": "INTUITED",
        "origin_type": "agent_synthesis",
        "author": "cursor",
    }
    inp = build_opa_input(fm, "/tmp/a.md", "cursor")
    denies = _opa_denies(inp)
    assert any("win-win" in d for d in denies)


def test_agent_structured_without_promotion_p0(require_opa):
    fm = {
        "epistemic_tier": "STRUCTURED",
        "origin_type": "agent_synthesis",
        "author": "antigravity",
        "win_win_clear": True,
    }
    inp = build_opa_input(fm, "/tmp/ag.md", "antigravity")
    denies = _opa_denies(inp)
    assert any("shape §8" in d for d in denies)


def test_agent_human_author_without_proxy_p0(require_opa):
    fm = {
        "epistemic_tier": "INTUITED",
        "origin_type": "agent_synthesis",
        "author": "ewan",
        "win_win_clear": True,
    }
    inp = build_opa_input(fm, "/tmp/bad.md", "antigravity")
    denies = _opa_denies(inp)
    assert any("shape §6" in d for d in denies)


def test_flat_earth_intuited_passes(require_opa):
    body = "---\nepistemic_tier: INTUITED\norigin_type: agent_synthesis\nauthor: cursor\nwin_win_clear: true\n---\n\nflat"
    denies, _ = check_content(body, "/tmp/flat.md", "cursor")
    assert denies == []


def test_transparency_structured_without_refs_p0(require_opa):
    fm = {
        "epistemic_tier": "STRUCTURED",
        "origin_type": "agent_synthesis",
        "author": "cursor",
        "promotion_record_id": "promo-1",
        "win_win_clear": True,
    }
    inp = build_opa_input(fm, "/tmp/t.md", "cursor")
    denies = _opa_denies(inp)
    assert any("transparency" in d for d in denies)


def test_classify_actor():
    assert classify_actor("ewan", {"human_authors": ["ewan"]}) == "human"
    assert classify_actor("antigravity", {"human_authors": ["ewan"]}) == "agent"
