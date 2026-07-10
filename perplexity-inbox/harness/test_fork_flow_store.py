#!/usr/bin/env python3
"""Tests for the append-only fork-flow lifecycle store."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.append(str(HARNESS_DIR))

from fork_flow import validate_index
from fork_flow_store import build_projection, create, load_events, resume, transition, write_projection


class TestForkFlowStore(unittest.TestCase):
    def write_contract(self, root: Path, fork_id: str = "fork-store-001") -> Path:
        worktree = root / "worktree"
        output = root / "output"
        validation = root / "validation"
        baton = root / "baton"
        for path in (worktree, output, validation, baton):
            path.mkdir(exist_ok=True)
        contract = {
            "schema_version": "fork-contract/v1",
            "fork_id": fork_id,
            "parent_job": "parent-test",
            "discovery_trigger": "A bounded discovery needs its own lane.",
            "working_hypothesis": {"role": "investigating", "statement": "Events preserve the lifecycle."},
            "goals": {"actual": "Exercise the store.", "compounding": "Leave a rebuildable projection."},
            "ownership": {"seat": "cursor", "owner": "cursor-child"},
            "paths": {
                "worktree": str(worktree),
                "branch": "cursor/fork-store-test",
                "shared_output": str(output),
                "validation": str(validation),
                "baton": str(baton),
            },
            "file_scope": ["perplexity-inbox/armamentarium/**"],
            "checkpoints": [{"id": "contract", "required": True, "pass_condition": "The contract is valid."}],
            "validation": {
                "commands": ["python3 harness/fork_flow.py validate contract.yaml"],
                "acceptance_checks": ["contract is valid"],
                "independent_review": ["third-party review pending"],
            },
            "return": {
                "condition": "Required checkpoints pass.",
                "parent_update": "State, link, next unblocker.",
                "verdict_path": str(output / "verdict.yaml"),
                "verdict": "used",
            },
            "armamentarium_selection": {
                "hypotheses": ["fork-flow-baseline-v1"],
                "pathways": ["fork-contract-validator-v1"],
            },
        }
        path = root / "contract.yaml"
        path.write_text(yaml.safe_dump(contract), encoding="utf-8")
        return path

    def test_lifecycle_is_append_only_and_rebuildable(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = self.write_contract(root)
            store = root / "store"
            create(store, contract)
            transition(store, "fork-store-001", "claimed", owner="cursor-child")
            transition(store, "fork-store-001", "running")
            transition(store, "fork-store-001", "checked")
            verdict = root / "output" / "verdict.yaml"
            verdict.write_text("verdict: used\n", encoding="utf-8")
            transition(store, "fork-store-001", "used", verdict_path=str(verdict))

            self.assertEqual(len(load_events(store)), 5)
            projection = build_projection(store)
            self.assertEqual(projection["forks"][0]["state"], "used")
            self.assertEqual(len(projection["file_path_atoms"]), 6)

            output = root / "index.yaml"
            write_projection(store, output)
            self.assertEqual(validate_index(yaml.safe_load(output.read_text(encoding="utf-8"))), [])
            self.assertTrue(output.with_suffix(".file-path-atoms.jsonl").is_file())

    def test_rejects_illegal_transition_and_missing_verdict(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = self.write_contract(root)
            store = root / "store"
            create(store, contract)
            with self.assertRaisesRegex(ValueError, "parked -> used"):
                transition(store, "fork-store-001", "used", verdict_path=str(root / "missing.yaml"))
            transition(store, "fork-store-001", "claimed", owner="cursor-child")
            transition(store, "fork-store-001", "running")
            transition(store, "fork-store-001", "checked")
            with self.assertRaisesRegex(ValueError, "verdict_path"):
                transition(store, "fork-store-001", "used")

    def test_park_resume_claim_collision_and_blocked_baton(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            os.environ["AMPLIFIED_INBOX"] = str(root / "inbox")
            (root / "inbox" / "batons" / "active").mkdir(parents=True)
            contract = self.write_contract(root)
            store = root / "store"
            create(store, contract)
            resume(store, "fork-store-001", owner="cursor-child")
            transition(store, "fork-store-001", "running")
            transition(store, "fork-store-001", "parked", reason="pause")
            with self.assertRaisesRegex(ValueError, "claim collision"):
                resume(store, "fork-store-001", owner="other-agent")
            resume(store, "fork-store-001", owner="cursor-child")
            transition(store, "fork-store-001", "running")
            blocked = transition(
                store,
                "fork-store-001",
                "blocked",
                reason="needs handoff",
            )
            self.assertTrue(Path(blocked["baton_path"]).is_file())
            projection = build_projection(store)
            self.assertIn("fork-store-001", projection["views"]["blocked"])


if __name__ == "__main__":
    unittest.main()
