# -*- coding: utf-8 -*-
"""Unit tests for OpenViking Health Check and Strict Fallback Policy."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.openviking.health import HealthMonitor, HealthStatus


class TestHealthAndFallback(unittest.TestCase):

    def test_healthy_state(self):
        monitor = HealthMonitor(simulate_offline=False)
        health = monitor.check_health()
        self.assertEqual(health["status"], HealthStatus.HEALTHY)

        fallback = monitor.evaluate_fallback(is_critical_production=True)
        self.assertTrue(fallback["allow_execution"])
        self.assertFalse(fallback["fallback_used"])

    def test_critical_production_blocks_on_offline(self):
        """During critical chapter production, offline OpenViking MUST BLOCK (NO SILENT RECOVERY)."""
        monitor = HealthMonitor(simulate_offline=True)
        fallback = monitor.evaluate_fallback(is_critical_production=True)
        self.assertFalse(fallback["allow_execution"])
        self.assertEqual(fallback["action"], "BLOCK_STOP_REPORT")
        self.assertIn("NO SILENT RECOVERY", fallback["error"])

    def test_diagnostic_non_critical_allows_fallback(self):
        """During non-critical diagnostic runs, fallback to context_ranker is explicitly recorded."""
        monitor = HealthMonitor(simulate_offline=True)
        fallback = monitor.evaluate_fallback(is_critical_production=False)
        self.assertTrue(fallback["allow_execution"])
        self.assertTrue(fallback["fallback_used"])
        self.assertEqual(fallback["backend"], "context_ranker")


if __name__ == "__main__":
    unittest.main()
