# -*- coding: utf-8 -*-
"""Unit tests for Atomic Memory Commit and Rollback on failure."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.governor.commit_gate import AtomicCommitGate


class TestMemoryAtomicity(unittest.TestCase):

    def setUp(self):
        self.test_store_file = root_dir / "04_STATE" / "test_memory_atomicity.json"
        self.gate = AtomicCommitGate(self.test_store_file)

    def tearDown(self):
        if self.test_store_file.exists():
            self.test_store_file.unlink()
        tmp_file = self.test_store_file.with_suffix(".tmp")
        if tmp_file.exists():
            tmp_file.unlink()

    def test_atomic_commit_success(self):
        records = [{"id": 1, "claim": "Valid Memory 1"}]
        success = self.gate.commit(records)
        self.assertTrue(success)

        read_records = self.gate.read_store()
        self.assertEqual(len(read_records), 1)
        self.assertEqual(read_records[0]["claim"], "Valid Memory 1")

    def test_atomic_commit_failure_rollback(self):
        # Initial commit
        self.gate.commit([{"id": 1, "claim": "Initial Stable Memory"}])

        # Attempt corrupted commit with simulated failure
        corrupted = [{"id": 99, "claim": "Corrupted Data"}]
        success = self.gate.commit(corrupted, simulate_failure=True)
        self.assertFalse(success)

        # Verify original state preserved and .tmp cleaned up
        read_records = self.gate.read_store()
        self.assertEqual(len(read_records), 1)
        self.assertEqual(read_records[0]["claim"], "Initial Stable Memory")
        self.assertFalse(self.test_store_file.with_suffix(".tmp").exists())


if __name__ == "__main__":
    unittest.main()
