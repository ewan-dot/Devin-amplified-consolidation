#!/usr/bin/env python3
"""Unit tests to verify strict single-version database curation for AI Orientation Guide."""

import sqlite3
import unittest
from uuid import uuid4


class TestAIOrientationDBCuration(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cur = self.conn.cursor()

        # Create the orientation guide table
        self.cur.execute("""
            CREATE TABLE ai_orientation_guide (
                guide_id TEXT PRIMARY KEY,
                topic TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                version INTEGER NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_commit TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def execute_curation_transaction(self, topic: str, content: str, version: int, commit: str) -> str:
        """Executes the exact DELETE-before-INSERT transaction rule."""
        guide_id = str(uuid4())
        try:
            self.cur.execute("BEGIN TRANSACTION;")
            
            # Step 1: Purge previous version of this topic
            self.cur.execute("DELETE FROM ai_orientation_guide WHERE topic = ?;", (topic,))
            
            # Step 2: Insert new version
            self.cur.execute("""
                INSERT INTO ai_orientation_guide (guide_id, topic, content, version, source_commit)
                VALUES (?, ?, ?, ?, ?);
            """, (guide_id, topic, content, version, commit))
            
            self.conn.commit()
            return guide_id
        except Exception as e:
            self.conn.rollback()
            raise e

    def test_purge_on_version_update(self):
        topic = "agent-git-guideline"

        # 1. Insert Version 1
        id_v1 = self.execute_curation_transaction(
            topic=topic,
            content="Version 1: AI must check git worktree status.",
            version=1,
            commit="a1b2c3d4"
        )

        # Assert Version 1 is there
        self.cur.execute("SELECT content, version, source_commit FROM ai_orientation_guide WHERE topic = ?;", (topic,))
        row = self.cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 1)
        self.assertEqual(row[0], "Version 1: AI must check git worktree status.")

        # Check total rows in the table
        self.cur.execute("SELECT COUNT(*) FROM ai_orientation_guide;")
        self.assertEqual(self.cur.fetchone()[0], 1)

        # 2. Insert Version 2 (which should trigger a delete/purge of Version 1)
        id_v2 = self.execute_curation_transaction(
            topic=topic,
            content="Version 2: AI must checkout a separate worktree and never commit on main.",
            version=2,
            commit="e5f6g7h8"
        )

        # Assert Version 2 is now active
        self.cur.execute("SELECT guide_id, content, version, source_commit FROM ai_orientation_guide WHERE topic = ?;", (topic,))
        row = self.cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], id_v2)
        self.assertEqual(row[2], 2)
        self.assertEqual(row[1], "Version 2: AI must checkout a separate worktree and never commit on main.")

        # Check total rows in table remains exactly 1 (verifying old row was deleted and no bloat occurred)
        self.cur.execute("SELECT COUNT(*) FROM ai_orientation_guide;")
        self.assertEqual(self.cur.fetchone()[0], 1)

        # Verify that guide ID of version 1 is no longer in the DB
        self.cur.execute("SELECT COUNT(*) FROM ai_orientation_guide WHERE guide_id = ?;", (id_v1,))
        self.assertEqual(self.cur.fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
