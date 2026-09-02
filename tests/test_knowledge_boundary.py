# -*- coding: utf-8 -*-
"""Unit tests for Knowledge Boundary enforcement."""

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
    KnowledgeStatus
)


class TestKnowledgeBoundary(unittest.TestCase):

    def setUp(self):
        self.governor = NovelMemoryGovernor(root_dir)

    def test_unrevealed_knowledge_leak_intercepted(self):
        """Protagonist possessing UNREVEALED secret -> KNOWLEDGE_BOUNDARY_VIOLATION."""
        delta = MemoryDelta(
            memory_type=MemoryType.KNOWLEDGE_BOUNDARY_MEMORY,
            entity="北美黑水基地",
            claim="黑水战队绝密潜入坐标",
            source_chapter=50,
            knowledge_status=KnowledgeStatus.UNREVEALED,
            knowledge_holders=["陆辰"]  # Protagonist should NOT know this yet
        )
        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta)
        self.assertEqual(res["status"], "NEEDS_HUMAN")
        self.assertEqual(res["conflict"].conflict_type, "KNOWLEDGE_BOUNDARY_VIOLATION")


if __name__ == "__main__":
    unittest.main()
