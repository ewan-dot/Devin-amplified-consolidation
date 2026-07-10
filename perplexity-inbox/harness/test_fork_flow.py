#!/usr/bin/env python3
"""Executable checks for the fork-flow foundation."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.append(str(HARNESS_DIR))

from fork_flow import resolve, validate_contract, validate_index


class TestForkFlow(unittest.TestCase):
    def contract(self, root: Path) -> dict:
        worktree = root / "worktree"
        output = root / "output"
        validation = root / "validation"
        baton = root / "baton"
        for path in (worktree, output, validation, baton):
            path.mkdir()
        return {
            "schema_version": "fork-contract/v1",
            "fork_id": "fork-test-001",
            "parent_job": "parent-test",
            "discovery_trigger": "A bounded discovery needs its own lane.",
            "working_hypothesis": {"role": "investigating", "statement": "The selected checks catch missing returns."},
            "goals": {"actual": "Exercise the contract.", "compounding": "Leave a reproducible test."},
            "ownership": {"seat": "cursor", "owner": "cursor-child"},
            "paths": {
                "worktree": str(worktree),
                "branch": "cursor/fork-test",
                "shared_output": str(output),
                "validation": str(validation),
                "baton": str(baton),
            },
            "file_scope": ["perplexity-inbox/armamentarium/**"],
            "checkpoints": [{"id": "contract", "required": True, "pass_condition": "The contract is valid."}],
            "validation": {
                "commands": ["python3 harness/fork_flow.py validate contract.yaml"],
                "acceptance_checks": ["contract is valid"],
                "independent_review": ["separate agent review"],
            },
            "return": {
                "condition": "Required checkpoints pass.",
                "parent_update": "State, link, next unblocker.",
                "verdict_path": str(output / "verdict.yaml"),
                "verdict": "used",
            },
            "armamentarium_selection": {
                "hypotheses": ["fork-flow-baseline-v1"],
                "pathways": ["fork-contract-validator-v1", "worktree-isolation-v1"],
            },
        }

    def registry(self) -> dict:
        return {
            "schema_version": "armamentarium/v1",
            "required_aspects": ["discovery-forking"],
            "working_hypotheses": [{
                "id": "fork-flow-baseline-v1",
                "aspect": "discovery-forking",
                "role": "in_use",
                "version": "v1",
                "statement": "A bounded discovery receives an explicit path.",
            }],
            "pathways": [
                {
                    "id": "fork-contract-validator-v1",
                    "kind": "harness",
                    "trigger": "before check",
                    "deterministic_check": "contract is valid",
                    "failure_outcome": "chase",
                    "ssot_path": "perplexity-inbox/harness/fork_flow.py",
                },
                {
                    "id": "worktree-isolation-v1",
                    "kind": "harness",
                    "trigger": "before implementation",
                    "deterministic_check": "worktree is isolated",
                    "failure_outcome": "chase",
                    "ssot_path": "perplexity-inbox/harness/agentic_checks.py",
                },
            ],
        }

    def test_resolver_rejects_missing_required_aspect(self):
        with TemporaryDirectory() as temporary:
            contract = self.contract(Path(temporary))
            registry = self.registry()
            registry["required_aspects"] = ["discovery-forking", "review-gate"]
            with self.assertRaisesRegex(ValueError, "required aspect unselected: review-gate"):
                resolve(contract, registry)

    def test_valid_contract_with_resolving_paths(self):
        with TemporaryDirectory() as temporary:
            contract = self.contract(Path(temporary))
            self.assertEqual(validate_contract(contract, require_existing_paths=True), [])

    def test_rejects_invalid_role_and_unsafe_scope(self):
        with TemporaryDirectory() as temporary:
            contract = self.contract(Path(temporary))
            contract["working_hypothesis"]["role"] = "canonical"
            contract["file_scope"] = ["../protected-file"]
            errors = validate_contract(contract)
            self.assertIn("working_hypothesis.role: must be investigating or in_use", errors)
            self.assertIn("file_scope: unsafe entry: ../protected-file", errors)

    def test_resolver_emits_explicit_selection(self):
        with TemporaryDirectory() as temporary:
            manifest = resolve(self.contract(Path(temporary)), self.registry())
            self.assertEqual(manifest["fork_id"], "fork-test-001")
            self.assertEqual(len(manifest["hypotheses"]), 1)
            self.assertEqual(len(manifest["pathways"]), 2)

    def test_index_requires_known_state_and_file_paths(self):
        valid = {
            "schema_version": "fork-park-index/v1",
            "forks": [{
                "fork_id": "fork-test-001",
                "state": "parked",
                "file_paths": {
                    "contract": "/tmp/contract.yaml",
                    "worktree": "/tmp/worktree",
                    "shared_output": "/tmp/output",
                    "validation": "/tmp/validation",
                    "baton": "/tmp/baton",
                },
            }],
        }
        self.assertEqual(validate_index(valid), [])
        valid["forks"][0]["state"] = "done"
        self.assertIn("forks[0].state: unsupported state", validate_index(valid))


if __name__ == "__main__":
    unittest.main()
