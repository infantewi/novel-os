# -*- coding: utf-8 -*-
"""Unit tests for Context Assembler and Retrieval Trace generation."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.openviking import OpenVikingAdapter


class TestRetrievalTrace(unittest.TestCase):

    def setUp(self):
        self.adapter = OpenVikingAdapter(root_dir)

    def test_context_assembler_with_trace(self):
        # Seed test nodes
        self.adapter.ingest_node(
            "viking://resources/novel/chapters/050",
            "第50章：踏浪登轮折断孙侯合金机械臂。",
            {"chapter": 50, "location": "公海游轮"},
            {"full_event": "万鬼大阵启动"}
        )

        ctx = self.adapter.assemble_context(
            chapter=50,
            objective="踏浪登轮断臂",
            location="东海公海",
            pov="陆辰",
            active_characters=["陆辰", "孙侯"],
            active_hooks=["H-050-01"]
        )

        self.assertIn("l0", ctx)
        self.assertIn("l1", ctx)
        self.assertIn("l2", ctx)
        self.assertIn("retrieval_trace", ctx)

        trace = ctx["retrieval_trace"]
        self.assertTrue(trace["trace_id"].startswith("TRACE-"))
        self.assertIn("provenance", ctx)


if __name__ == "__main__":
    unittest.main()
