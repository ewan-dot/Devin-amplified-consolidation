#!/usr/bin/env python3
"""Unit tests for the Deterministic Outbound Doorway Patch Applicator."""

import json
import unittest
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from harness.apply_doorway import DoorwayApplicator


class TestDoorwayApplicator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.doorway_path = self.root_path / "outbound_doorway"
        self.doorway_path.mkdir()

        # Create dummy file to modify
        self.dummy_file = self.root_path / "dummy.txt"
        self.dummy_content = "Hello, this is a dummy file.\nDo not edit this directly.\nKeep it clean.\n"
        self.dummy_file.write_text(self.dummy_content)

        self.applicator = DoorwayApplicator(root_dir=self.root_path, doorway_dir=self.doorway_path)
        self.applicator.setup_directories()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_apply_valid_patch(self):
        patch_data = {
            "agent_id": "test-agent",
            "timestamp": "2026-06-30T13:45:00Z",
            "changes": [
                {
                    "file_path": str(self.dummy_file),
                    "action": "modify",
                    "target_content": "Do not edit this directly.",
                    "replacement_content": "Modifications allowed via doorway."
                }
            ]
        }

        patch_file = self.doorway_path / "patch_20260630_test.json"
        with open(patch_file, 'w') as f:
            json.dump(patch_data, f)

        ok, msg = self.applicator.apply_patch(patch_file)
        self.assertTrue(ok, f"Patch failed: {msg}")

        # Check modifications applied
        updated_content = self.dummy_file.read_text()
        self.assertIn("Modifications allowed via doorway.", updated_content)
        self.assertNotIn("Do not edit this directly.", updated_content)

        # Check patch file was archived
        self.assertFalse(patch_file.exists())
        self.assertTrue((self.doorway_path / "applied" / patch_file.name).exists())

    def test_conflict_detection(self):
        patch_data = {
            "agent_id": "test-agent",
            "timestamp": "2026-06-30T13:45:00Z",
            "changes": [
                {
                    "file_path": str(self.dummy_file),
                    "action": "modify",
                    "target_content": "This line does not exist.",
                    "replacement_content": "Conflict here."
                }
            ]
        }

        patch_file = self.doorway_path / "patch_conflict.json"
        with open(patch_file, 'w') as f:
            json.dump(patch_data, f)

        ok, msg = self.applicator.apply_patch(patch_file)
        self.assertFalse(ok)
        self.assertIn("conflict detected", msg.lower())

        # Check target content was not modified
        self.assertEqual(self.dummy_file.read_text(), self.dummy_content)


if __name__ == "__main__":
    unittest.main()
