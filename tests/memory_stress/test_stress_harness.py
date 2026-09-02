# -*- coding: utf-8 -*-
"""Stress Benchmark Runner."""

import unittest
from .stress_generator import StressDatasetGenerator


class TestMillionCharacterStressHarness(unittest.TestCase):
    """Verifies that the stress test environment is isolated and functional."""

    def test_synthetic_generation_isolation(self):
        dataset = StressDatasetGenerator.generate_synthetic_chapters(chapter_count=10)
        self.assertEqual(len(dataset), 10)
        for item in dataset:
            self.assertTrue(item["uri"].startswith("viking://stress-test/"))
            self.assertFalse(item["uri"].startswith("viking://resources/novel/"))


if __name__ == "__main__":
    unittest.main()
