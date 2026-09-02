# -*- coding: utf-8 -*-
"""Unit tests for Zero-Trust Memory Permissions."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.governor import (
    NovelMemoryGovernor,
    MemoryDelta,
    MemoryType,
    MemoryPermissionGate
)


class TestMemoryPermissions(unittest.TestCase):

    def setUp(self):
        self.governor = NovelMemoryGovernor(root_dir)

    def test_worker_direct_commit_blocked(self):
        """Worker B (WEBNOVEL_WRITER) attempts direct commit -> BLOCKED."""
        delta = MemoryDelta(
            memory_type=MemoryType.EVENT_MEMORY,
            entity="测试实体",
            claim="测试内容",
            source_chapter=50
        )
        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta, direct_commit=True)
        self.assertEqual(res["status"], "BLOCKED")
        self.assertIn("strictly FORBIDDEN", res["reason"])

    def test_de_ai_and_lieflat_forbidden_from_proposing(self):
        """Worker C & D are forbidden from proposing memory deltas."""
        delta = MemoryDelta(
            memory_type=MemoryType.EVENT_MEMORY,
            entity="测试",
            claim="测试",
            source_chapter=50
        )
        res_de = self.governor.process_delta(worker_id="DE_AI", delta=delta)
        self.assertEqual(res_de["status"], "BLOCKED")

        res_lie = self.governor.process_delta(worker_id="LIEFLAT", delta=delta)
        self.assertEqual(res_lie["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
