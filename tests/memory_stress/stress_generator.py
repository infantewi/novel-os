# -*- coding: utf-8 -*-
"""
Million-Character Stress Test Dataset Generator and Benchmark Harness.
Strictly isolated in viking://stress-test/... namespace.
"""

import random
from typing import Dict, Any, List


class StressDatasetGenerator:
    """Generates synthetic novel chapters and structured memory candidates for stress testing."""

    @classmethod
    def generate_synthetic_chapters(cls, chapter_count: int = 100) -> List[Dict[str, Any]]:
        dataset = []
        for i in range(1, chapter_count + 1):
            dataset.append({
                "chapter_id": i,
                "title": f"第{i:04d}章-合成修仙争锋第{i}回",
                "uri": f"viking://stress-test/chapters/{i:04d}",
                "character_uri": f"viking://stress-test/characters/修仙者_{i % 20}",
                "l0": f"合成第{i}章摘要：修仙者跨越虚空进行法则碰撞。",
                "l1": {"chapter": i, "synthetic_seed": random.randint(1000, 9999)},
                "l2": {"full_text": "合成小说文本内容 " * 150}
            })
        return dataset
