#!/usr/bin/env python3
"""Smoke: dogfood fixture runs twice with matching normalized projections."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

DOGFOOD = Path(__file__).resolve().parents[1] / "fork_flow" / "dogfood"
sys.path.insert(0, str(DOGFOOD))

from run_dogfood import run_once  # noqa: E402


class TestForkFlowDogfood(unittest.TestCase):
    def test_two_runs_match_normalized_projection(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            os.environ["AMPLIFIED_INBOX"] = str(root / "inbox-a")
            first = run_once(root / "run-1")
            os.environ["AMPLIFIED_INBOX"] = str(root / "inbox-b")
            second = run_once(root / "run-2")
            self.assertEqual(first["verdict"], "used")
            self.assertEqual(first["review_status"], "pending")
            self.assertEqual(
                json.dumps(first["projection"], sort_keys=True),
                json.dumps(second["projection"], sort_keys=True),
            )
            self.assertEqual(first["projection"]["forks"][0]["state"], "used")


if __name__ == "__main__":
    unittest.main()
