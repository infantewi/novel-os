# -*- coding: utf-8 -*-
"""Unit tests for Novel Memory Governor processing and validation."""

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
    Provenance
)


class TestMemoryGovernor(unittest.TestCase):

    def setUp(self):
        self.governor = NovelMemoryGovernor(root_dir)

    def test_valid_event_delta_proposal(self):
        delta = MemoryDelta(
            memory_type=MemoryType.EVENT_MEMORY,
            entity="孙侯",
            claim="在第50章被陆辰折断暗青合金右臂并失去战斗力",
            source="正文/第0050章",
            source_chapter=50,
            provenance=Provenance(source_chapter=50, created_by="WEBNOVEL_WRITER")
        )

        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta)
        self.assertEqual(res["status"], "ACCEPTED")
        self.assertTrue(delta.provenance.source_hash != "")

    def test_invalid_delta_missing_fields(self):
        delta = MemoryDelta(
            memory_type=MemoryType.CHARACTER_MEMORY,
            entity="",  # Missing entity
            claim="",   # Missing claim
            source_chapter=-1
        )
        res = self.governor.process_delta(worker_id="WEBNOVEL_WRITER", delta=delta)
        self.assertEqual(res["status"], "VALIDATION_FAILED")
        self.assertGreaterEqual(len(res["errors"]), 2)


if __name__ == "__main__":
    unittest.main()
