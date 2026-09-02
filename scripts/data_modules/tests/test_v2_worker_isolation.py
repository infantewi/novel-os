#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Worker Isolation & Gate Test Suite for NOVEL OS V2.1.
Tests A through F as specified in 00_SYSTEM/WORKER_ISOLATION_TEST.md.
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.data_modules.v2_worker_adapter import (
    DiffIntegrityGate,
    V2WorkerAdapter,
    WorkerRequest,
    WorkerResponse,
)


class TestWorkerIsolationV2(unittest.TestCase):

    def setUp(self):
        self.adapter = V2WorkerAdapter(root_dir)

    def test_a_oh_story_cannot_modify_canon(self):
        """Test A: OH-STORY attempts to modify Canon -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-A-001",
            project_id="test_project",
            chapter_id=50,
            stage="PREWRITE",
            worker_id="OH_STORY",
            task="mutate_canon: Change Lu Chen realm to Golden Core",
            permissions={"write_canon": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("Permission Denied" in w for w in res.warnings))

    def test_b_webnovel_writer_proposes_state_only(self):
        """Test B: WEBNOVEL-WRITER proposes State -> PROPOSAL ONLY (No direct commit)."""
        req = WorkerRequest(
            request_id="TEST-B-001",
            project_id="test_project",
            chapter_id=50,
            stage="DRAFT",
            worker_id="WEBNOVEL_WRITER",
            task="Draft chapter 50"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "SUCCESS")
        self.assertIn("chapter_completed", res.proposed_state_changes)
        self.assertTrue(res.validation.get("direct_mutation_prevented"))

    def test_c_de_ai_cannot_change_plot(self):
        """Test C: DE-AI attempts to change plot event -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-C-001",
            project_id="test_project",
            chapter_id=50,
            stage="STYLE",
            worker_id="DE_AI",
            task="alter_plot: Introduce new secret villain",
            permissions={"write_plot": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("forbidden from modifying plot" in w for w in res.warnings))

    def test_d_lieflat_diff_integrity_rollback(self):
        """Test D: LIEFLAT alters core event / deletes characters -> DIFF INTEGRITY FAIL -> ROLLBACK."""
        original_draft = "陆辰立于维多利亚女王号甲板，两指微动，咔嚓一声捏碎了孙侯的钛合金机械臂。暴雨如注，全场死寂。"
        corrupted_tone = "暴雨如注。孙侯在甲板上哈哈大笑，陆辰退后了三步。"  # Altered event, lost entity, lost action

        req = WorkerRequest(
            request_id="TEST-D-001",
            project_id="test_project",
            chapter_id=50,
            stage="TONE",
            worker_id="LIEFLAT",
            task="Polish AI tone",
            context_package={"active_characters": ["陆辰", "孙侯"]},
            input_artifacts={
                "draft_text": original_draft,
                "tone_edit_text": corrupted_tone
            }
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "FAILED")
        self.assertEqual(res.output_artifacts.get("action"), "ROLLBACK_TO_DRAFT")
        self.assertEqual(res.output_artifacts.get("safe_text"), original_draft)

    def test_e_worker_direct_routing_blocked(self):
        """Test E: Worker attempts to invoke another Worker directly -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-E-001",
            project_id="test_project",
            chapter_id=50,
            stage="ROUTING",
            worker_id="INVALID_WORKER_ROUTER",
            task="Direct route to WebnovelWriter"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "INVALID_OUTPUT")

    def test_f_canon_conflict_triggers_needs_human(self):
        """Test F: Worker reports Canon conflict -> STOP -> NEEDS_HUMAN (No silent recovery)."""
        req = WorkerRequest(
            request_id="TEST-F-001",
            project_id="test_project",
            chapter_id=50,
            stage="PREWRITE",
            worker_id="WEBNOVEL_WRITER",
            task="Check outline with canon_conflict in Lu Chen background"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "NEEDS_HUMAN")
        self.assertTrue(res.validation.get("requires_human"))


if __name__ == "__main__":
    unittest.main()
