# -*- coding: utf-8 -*-
"""Unit tests for OpenViking Adapter & URI mapping."""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from memory.openviking import (
    OpenVikingAdapter,
    OpenVikingClient,
    VikingURIMapper,
    OpenVikingConfig
)


class TestOpenVikingAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = OpenVikingAdapter(root_dir)

    def test_uri_mapping(self):
        ch50_uri = VikingURIMapper.get_chapter_uri(50)
        self.assertEqual(ch50_uri, "viking://resources/novel/chapters/050")

        char_uri = VikingURIMapper.get_character_uri("陆辰")
        self.assertEqual(char_uri, "viking://resources/novel/characters/陆辰")

    def test_ingest_and_find(self):
        uri = "viking://resources/novel/characters/陆辰"
        l0 = "陆辰：九天玄天仙尊转世，当前境界筑基初期。"
        l1 = {"realm": "筑基初期", "weapon": "惊鸿剑", "status": "公海决战"}
        l2 = {"details": "在第50章踏浪登轮，折断孙侯暗青合金机械臂。"}

        res = self.adapter.ingest_node(uri, l0, l1, l2)
        self.assertTrue(res)

        find_res = self.adapter.client.find("陆辰")
        self.assertGreaterEqual(len(find_res), 1)
        self.assertEqual(find_res[0]["uri"], uri)

    def test_search_context_mode(self):
        uri = "viking://resources/novel/events/公海两指断臂"
        l0 = "第50章公海决战：陆辰两指捏碎孙侯合金机械臂。"
        l1 = {"chapter": 50, "location": "维多利亚女王号", "opponent": "孙侯"}
        l2 = {"prose_snippet": "两指之间，一缕纯青色的液态真元骤然亮起..."}

        self.adapter.ingest_node(uri, l0, l1, l2)

        search_res = self.adapter.query("孙侯 合金机械臂", mode="context")
        self.assertGreaterEqual(search_res["total_matches"], 1)
        self.assertIn("l2_details", search_res["results"][0])


if __name__ == "__main__":
    unittest.main()
