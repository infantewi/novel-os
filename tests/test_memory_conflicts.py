# -*- coding: utf-8 -*-
"""Unit tests for Canon & Timeline Conflict Detection."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.governor import (
    NovelMemoryGovernor,
    MemoryDelta,
    MemoryType
)


class TestMemoryConflicts(unittest.TestCase):

    def setUp(self):
        self.governor = NovelMemoryGovernor(root_dir)

    def test_canon_realm_conflict_intercepted(self):
        """Injected claim that Lu Chen broke into Jindan in Ch50 -> STOP & NEEDS_HUMAN."""
        delta = MemoryDelta(
            memory_type=MemoryType.CHARACTER_MEMORY,
            entity="陆辰",
            claim="陆辰在第50章突破至金丹中期，祭出天问剑",
            source_chapter=50
        )
        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta)
        self.assertEqual(res["status"], "NEEDS_HUMAN")
        conflict = res["conflict"]
        self.assertEqual(conflict.conflict_type, "CANON_CONFLICT")
        self.assertEqual(conflict.action, "STOP_NEEDS_HUMAN")
        self.assertGreaterEqual(len(conflict.legal_options), 2)

    def test_canon_talk_no_jutsu_conflict_intercepted(self):
        """Injected claim that Lu Chen used moral preaching to save villain -> STOP."""
        delta = MemoryDelta(
            memory_type=MemoryType.EVENT_MEMORY,
            entity="陆辰",
            claim="陆辰以德报怨，口头话疗感化孙侯并与之结拜",
            source_chapter=50
        )
        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta)
        self.assertEqual(res["status"], "NEEDS_HUMAN")
        self.assertEqual(res["conflict"].conflict_type, "CANON_CONFLICT")


if __name__ == "__main__":
    unittest.main()
