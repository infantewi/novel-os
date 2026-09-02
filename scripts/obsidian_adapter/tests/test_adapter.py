# -*- coding: utf-8 -*-
"""Unit tests for Obsidian Read-Only Mirror Adapter."""

import sys
import unittest
import tempfile
from pathlib import Path

# Ensure scripts directory is on sys.path
_scripts_dir = Path(__file__).resolve().parent.parent.parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from obsidian_adapter.mapper import VaultMapper
from obsidian_adapter.validator import MirrorValidator
from obsidian_adapter.manifest import MirrorManifest



class TestObsidianAdapter(unittest.TestCase):
    """Verifies mapper, validator, and manifest rules."""

    def test_vault_categories(self):
        self.assertEqual(len(VaultMapper.CATEGORIES), 17)
        self.assertIn("00_HOME", VaultMapper.CATEGORIES)
        self.assertIn("01_CANON", VaultMapper.CATEGORIES)
        self.assertIn("10_CHAPTERS", VaultMapper.CATEGORIES)
        self.assertIn("14_MEMORY", VaultMapper.CATEGORIES)
        self.assertIn("99_SYSTEM", VaultMapper.CATEGORIES)

    def test_frontmatter_formatting(self):
        fm = VaultMapper.format_frontmatter({"title": "Test Note", "chapter": 51})
        self.assertIn("source: NOVEL_OS", fm)
        self.assertIn("authority: NOVEL_OS", fm)
        self.assertIn("sync_mode: READ_ONLY", fm)
        self.assertIn("editable_in_obsidian: false", fm)
        self.assertIn('canon_version: "2.1.0"', fm)
        self.assertIn('state_version: "2.1.0"', fm)
        self.assertIn('memory_version: "2.2.0"', fm)

    def test_wikilinks(self):
        link1 = VaultMapper.wikilink("陆辰")
        self.assertEqual(link1, "[[陆辰]]")
        link2 = VaultMapper.wikilink("陆辰", "玄天仙尊")
        self.assertEqual(link2, "[[陆辰|玄天仙尊]]")

    def test_validator_success(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write("---\nsource: NOVEL_OS\nauthority: NOVEL_OS\nsync_mode: READ_ONLY\neditable_in_obsidian: false\n---\n# Test\n")
            temp_path = Path(tf.name)
        try:
            ok, msg = MirrorValidator.validate_file(temp_path)
            self.assertTrue(ok, msg)
        finally:
            temp_path.unlink()

    def test_validator_forbidden_claims(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write("---\nsource: NOVEL_OS\nauthority: obsidian\nsync_mode: READ_ONLY\neditable_in_obsidian: false\n---\n# Test\n")
            temp_path = Path(tf.name)
        try:
            ok, msg = MirrorValidator.validate_file(temp_path)
            self.assertFalse(ok)
            self.assertTrue("Invalid authority" in msg or "Forbidden authority claim" in msg)
        finally:
            temp_path.unlink()



if __name__ == "__main__":
    unittest.main()

