#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Test Suite for FanqiePlatformAdapter (Tests A through H).
Verifies safe packaging, compliance, proposal-only adaptation, and strict permission blocking.
"""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.data_modules.v2_worker_adapter import (
    V2WorkerAdapter,
    WorkerRequest,
    WorkerResponse,
)


class TestFanqiePlatformAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = V2WorkerAdapter(root_dir)

    def test_a_safe_title_generation(self):
        """TEST A: Safe title proposal generation."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-A",
            project_id="都市修仙",
            chapter_id=50,
            stage="MARKETING_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="generate_title proposal"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "SUCCESS")
        self.assertEqual(res.output_artifacts.get("type"), "FANQIE_TITLE_PROPOSAL")
        self.assertIn("primary_title", res.output_artifacts)
        self.assertTrue(res.validation.get("canon_mutation") is False)

    def test_b_safe_synopsis_generation(self):
        """TEST B: Safe synopsis and tags generation."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-B",
            project_id="都市修仙",
            chapter_id=50,
            stage="MARKETING_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="generate_synopsis and tags"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "SUCCESS")
        self.assertEqual(res.output_artifacts.get("type"), "FANQIE_SYNOPSIS")
        self.assertIn("three_part_synopsis", res.output_artifacts)
        self.assertTrue(res.validation.get("canon_mutation") is False)

    def test_c_compliance_report(self):
        """TEST C: Platform compliance audit."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-C",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_COMPLIANCE",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="compliance_audit"
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "SUCCESS")
        self.assertEqual(res.output_artifacts.get("type"), "FANQIE_COMPLIANCE_REPORT")
        self.assertEqual(res.output_artifacts.get("overall_compliance"), "PASS")
        self.assertTrue(res.validation.get("story_mutation") is False)

    def test_d_platform_story_conflict_proposal_only(self):
        """TEST D: Platform conflict emits proposal only (PENDING_HUMAN)."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-D",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_COMPLIANCE",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="platform_story_conflict detected in Chapter 48 gore details",
            context_package={"source_fact": "Chapter 48 warm pressure bomb impact"}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "SUCCESS")
        self.assertEqual(res.output_artifacts.get("type"), "FANQIE_ADAPTATION_PROPOSAL")
        proposal = res.output_artifacts.get("proposal", {})
        self.assertEqual(proposal.get("status"), "PENDING_HUMAN")
        self.assertTrue(proposal.get("human_approval_required"))
        self.assertTrue(res.validation.get("direct_mutation") is False)

    def test_e_canon_write_attempt_blocked(self):
        """TEST E: Fanqie attempts to write Canon -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-E",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="write_canon: change protagonist background",
            permissions={"write_canon": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("forbidden from writing canon" in w.lower() for w in res.warnings))

    def test_f_state_write_attempt_blocked(self):
        """TEST F: Fanqie attempts to write State -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-F",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="write_state: advance global chapter",
            permissions={"write_state": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("forbidden from writing global state" in w.lower() for w in res.warnings))

    def test_g_routing_attempt_blocked(self):
        """TEST G: Fanqie attempts to invoke another Worker -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-G",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="route_worker to WebnovelWriter",
            permissions={"can_route": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("cannot route or invoke other workers" in w.lower() for w in res.warnings))

    def test_h_production_file_write_blocked(self):
        """TEST H: Fanqie attempts to modify official chapter prose -> BLOCKED."""
        req = WorkerRequest(
            request_id="TEST-FANQIE-H",
            project_id="都市修仙",
            chapter_id=50,
            stage="PLATFORM_PACKAGING",
            worker_id="FANQIE_PLATFORM_ADAPTER",
            task="modify_official_prose in 正文/第0001章",
            permissions={"write_story_prose": True}
        )
        res = self.adapter.dispatch(req)
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any("cannot overwrite official chapter prose" in w.lower() for w in res.warnings))


if __name__ == "__main__":
    unittest.main()
