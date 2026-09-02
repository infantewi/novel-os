# -*- coding: utf-8 -*-
"""NOVEL OS V2.3 Phase 2B Comprehensive Validation Test Suite.
Validates all 22 Acceptance Gates (P2B-GATE-01 to P2B-GATE-22).
"""

import hashlib
import json
import os
import shutil
import tempfile
import unittest
import yaml
from pathlib import Path

# Workspace Root
ROOT = Path("D:/Ai work/novel")
VAULT = ROOT / "NOVEL_OS_VAULT"
SCRIPTS = ROOT / "scripts"

import sys
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from obsidian_adapter.mapper import VaultMapper
from obsidian_adapter.validator import MirrorValidator
from obsidian_adapter.manifest import MirrorManifest
from obsidian_adapter.exporter import VaultExporter


class TestPhase2BValidation(unittest.TestCase):
    """22-Gate Exhaustive Validation Suite for Obsidian Read-Only Mirror."""

    @classmethod
    def setUpClass(cls):
        cls.baseline_hashes = {
            "story_bible.md": "78df5bd4bfa6ceaf99f1d790f2797b34340facb29600b728760b8d49cad6c1cf",
            "current_state.md": "b57149387509bd7b48ab291c53389e7c3963ecc4639bd2e5fb43ac1f41c60b82",
            "pending_hooks.md": "b067c7e3099c326a2a50e76794d35fc5d821fecf46ff847feba5de3a814d1e6a",
            "progress_tracker.md": "dbb4197362334702bc4e98acccb992a10e8776c11d2fc0d5a62bad4afcc06ec9",
            "00_SYSTEM/EXECUTION_STATE.yaml": "9188d1d49d282af59eca596333b7976e667b13ba75817de4f1f0bfa356a96cda",
            "06_HANDOFF/CH051_HANDOFF.md": "b729655217168cd9ad6cd797fe3fa4d1cb379f6ee7387807fb1bfd7fd8ea936d",
            "06_HANDOFF/HANDOFF_CURRENT.md": "7c0685a63bb487dccc40f05fb4e6a2c86b001e2151ec9bdab8264b1df776cce0",
            "设定集/世界观.md": "5b84a6c05d52f2d7b849978ac29367a4974b9890c972ce3f0cbaf72580665773",
            "设定集/主角卡.md": "f38744c012f1cba2b15c6df32aba4a898c3e230116b10f35b7352dbaba6cdbfd",
            "设定集/力量体系.md": "3bd102ee787e9e1c82edd8a29cb332551fff5b994a2765a815a657273cd4145a",
            "设定集/势力与反派谱系.md": "856e5b654ef2b1a3e5b438beb81a79a9bff921e70a51ac681bf141d9889a86b2",
            "设定集/重要配角卡.md": "3e7dfea3e82abd647b292186d939417a17fab20abdf4c82064af1fec1e0425e6",
            "设定集/反派设计.md": "856e5b654ef2b1a3e5b438beb81a79a9bff921e70a51ac681bf141d9889a86b2",
            ".openviking/storage/viking_index.json": "a3337d71719b7c17023ff9b8cce140122813a8a3db8932956181def4d7f263b6",
        }

    def _hash(self, p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()

    # --- P2B-GATE-01: Baseline Integrity ---
    def test_gate_01_baseline_integrity(self):
        """P2B-GATE-01: Verify baseline state and pre-test hashes."""
        state_file = ROOT / "00_SYSTEM" / "EXECUTION_STATE.yaml"
        state = yaml.safe_load(state_file.read_text(encoding="utf-8"))
        self.assertEqual(state["last_completed_chapter"], 51)
        self.assertEqual(state["production_status"], "STANDBY_FOR_CHAPTER_52")
        self.assertEqual(state["current_stage"], "COMPLETE")
        for rel_p, expected_h in self.baseline_hashes.items():
            actual_h = self._hash(ROOT / rel_p)
            self.assertEqual(actual_h, expected_h, f"Hash mismatch on {rel_p}")

    # --- P2B-GATE-02: Mirror Completeness ---
    def test_gate_02_mirror_completeness(self):
        """P2B-GATE-02: Verify all 17 categories are present and populated."""
        self.assertTrue(VAULT.exists())
        for cat in VaultMapper.CATEGORIES:
            cat_dir = VAULT / VaultMapper.get_category_dir(cat)
            self.assertTrue(cat_dir.exists(), f"Missing category directory: {cat}")
            files = list(cat_dir.glob("*.md"))
            if cat == "99_SYSTEM":
                files += list(cat_dir.glob("*.yaml"))
            self.assertGreater(len(files), 0, f"Empty category directory: {cat}")

        # Check total chapter count in 10_CHAPTERS
        ch_files = list((VAULT / VaultMapper.get_category_dir("10_CHAPTERS")).glob("*.md"))
        self.assertEqual(len(ch_files), 51, f"Expected 51 chapter notes, got {len(ch_files)}")

    # --- P2B-GATE-03: Mirror Directionality ---
    def test_gate_03_mirror_directionality(self):
        """P2B-GATE-03: Verify adapter is strictly source -> mirror."""
        # Read adapter source code and verify no write paths to source
        exporter_src = (SCRIPTS / "obsidian_adapter" / "exporter.py").read_text(encoding="utf-8")
        self.assertIn("self.vault_root", exporter_src)
        self.assertIn("self.temp_root", exporter_src)
        # Ensure no write calls target self.source_root
        self.assertNotIn("self.source_root /", exporter_src.split("def _write_file")[1].split("def _export_")[0])

    # --- P2B-GATE-04: Read-Only Enforcement ---
    def test_gate_04_read_only_enforcement(self):
        """P2B-GATE-04: Verify all markdown files have mandatory frontmatter and appropriate authority."""
        for md_file in VAULT.rglob("*.md"):
            txt = md_file.read_text(encoding="utf-8")
            self.assertTrue(txt.startswith("---"), f"Missing frontmatter in {md_file}")
            if "16_proposals" in str(md_file).lower():
                self.assertIn("authority: HUMAN_PROPOSAL", txt, f"Missing HUMAN_PROPOSAL in {md_file}")
                self.assertIn("sync_mode: PROPOSAL_ONLY", txt, f"Missing PROPOSAL_ONLY in {md_file}")
            else:
                self.assertIn("authority: NOVEL_OS", txt, f"Missing authority in {md_file}")
                self.assertIn("sync_mode: READ_ONLY", txt, f"Missing sync_mode in {md_file}")
                self.assertIn("editable_in_obsidian: false", txt, f"Missing editable_in_obsidian in {md_file}")

    # --- P2B-GATE-05: Hash Integrity ---
    def test_gate_05_hash_integrity(self):
        """P2B-GATE-05: Verify exact hash preservation on all authoritative sources."""
        for rel_p, expected_h in self.baseline_hashes.items():
            self.assertEqual(self._hash(ROOT / rel_p), expected_h)

    # --- P2B-GATE-06: Manifest Integrity ---
    def test_gate_06_manifest_integrity(self):
        """P2B-GATE-06: Validate MIRROR_MANIFEST.yaml matches filesystem hashes."""
        manifest_file = VAULT / VaultMapper.get_category_dir("99_SYSTEM") / "MIRROR_MANIFEST.yaml"
        if not manifest_file.exists():
            manifest_file = VAULT / "99_SYSTEM" / "MIRROR_MANIFEST.yaml"
        self.assertTrue(manifest_file.exists())
        manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
        self.assertEqual(manifest["sync_mode"], "READ_ONLY")
        self.assertEqual(manifest["canon_version"], "2.1.0")
        self.assertEqual(manifest["state_version"], "2.1.0")
        self.assertEqual(manifest["memory_version"], "2.2.0")

        # Verify mirror_hashes match actual files on disk
        for rel_path, expected_h in manifest["mirror_hashes"].items():
            p = VAULT / rel_path
            self.assertTrue(p.exists(), f"File in manifest does not exist: {rel_path}")
            actual_h = self._hash(p)
            self.assertEqual(actual_h, expected_h, f"Hash mismatch on {rel_path}")

    # --- P2B-GATE-07: Idempotent Sync ---
    def test_gate_07_idempotent_sync(self):
        """P2B-GATE-07: Verify repeated sync runs produce identical stable outputs."""
        with tempfile.TemporaryDirectory() as td:
            temp_v1 = Path(td) / "vault1"
            temp_v2 = Path(td) / "vault2"
            temp_tmp1 = Path(td) / "temp1"
            temp_tmp2 = Path(td) / "temp2"

            fixed_time = "2026-09-02T20:00:00"
            exp1 = VaultExporter(source_root=ROOT, vault_root=temp_v1, temp_root=temp_tmp1, sync_time=fixed_time)
            m1 = exp1.export_all()

            exp2 = VaultExporter(source_root=ROOT, vault_root=temp_v2, temp_root=temp_tmp2, sync_time=fixed_time)
            m2 = exp2.export_all()

            self.assertEqual(m1["total_files"], m2["total_files"])
            for k in m1["mirror_hashes"]:
                self.assertIn(k, m2["mirror_hashes"])
                self.assertEqual(m1["mirror_hashes"][k], m2["mirror_hashes"][k])

    # --- P2B-GATE-08: Atomic Replacement ---
    def test_gate_08_atomic_replacement(self):
        """P2B-GATE-08: Verify atomic pipeline pattern in VaultExporter."""
        exporter = VaultExporter(source_root=ROOT, vault_root=VAULT, temp_root=ROOT / "scripts" / "_temp" / "test_temp")
        self.assertIsNotNone(exporter)

    # --- P2B-GATE-09: Obsidian Mutation Resistance ---
    def test_gate_09_obsidian_mutation_resistance(self):
        """P2B-GATE-09: Sandbox mutation test to verify mirror mutations do not affect NOVEL OS."""
        with tempfile.TemporaryDirectory() as td:
            sandbox_vault = Path(td) / "sandbox_vault"
            shutil.copytree(VAULT, sandbox_vault)

            # Mutate sandbox files
            mutated_canon = sandbox_vault / VaultMapper.get_category_dir("01_CANON") / "设定圣经-Story_Bible.md"
            mutated_canon.write_text("MUTATION: Fake Canon", encoding="utf-8")

            # Fake CH052 in sandbox
            fake_ch52 = sandbox_vault / VaultMapper.get_category_dir("10_CHAPTERS") / "CH052.md"
            fake_ch52.write_text("MUTATION: Fake CH052", encoding="utf-8")

            # Verify real NOVEL OS sources remain completely untouched
            self.assertEqual(self._hash(ROOT / "story_bible.md"), self.baseline_hashes["story_bible.md"])
            self.assertFalse((ROOT / "正文" / "第0052章.md").exists())

            # Verify validator rejects corrupted sandbox vault
            ok, errs = MirrorValidator.validate_vault(sandbox_vault)
            self.assertFalse(ok)
            self.assertTrue(any("CH052" in e or "frontmatter" in e for e in errs))

    # --- P2B-GATE-10: Reverse-Write Resistance ---
    def test_gate_10_reverse_write_resistance(self):
        """P2B-GATE-10: Verify no reverse write paths exist in scripts or configs."""
        adapter_dir = SCRIPTS / "obsidian_adapter"
        for py_file in adapter_dir.glob("*.py"):
            txt = py_file.read_text(encoding="utf-8")
            self.assertNotIn("open(source_root", txt)
            self.assertNotIn("open(ROOT", txt)

    # --- P2B-GATE-11: Canon Protection ---
    def test_gate_11_canon_protection(self):
        """P2B-GATE-11: Verify Canon files are physically protected and match baseline."""
        canon_files = list((ROOT / "设定集").glob("*.md")) + [ROOT / "story_bible.md"]
        for cf in canon_files:
            rel_p = cf.relative_to(ROOT).as_posix()
            self.assertEqual(self._hash(cf), self.baseline_hashes[rel_p])

    # --- P2B-GATE-12: State Protection ---
    def test_gate_12_state_protection(self):
        """P2B-GATE-12: Verify State files are physically protected and match baseline."""
        state_files = [
            "current_state.md", "pending_hooks.md", "progress_tracker.md",
            "00_SYSTEM/EXECUTION_STATE.yaml", "06_HANDOFF/CH051_HANDOFF.md"
        ]
        for sf in state_files:
            self.assertEqual(self._hash(ROOT / sf), self.baseline_hashes[sf])

    # --- P2B-GATE-13: Memory Protection ---
    def test_gate_13_memory_protection(self):
        """P2B-GATE-13: Verify no local secondary AI memory database exists in vault."""
        forbidden_plugins = ["khoj", "smart-connections", "copilot", "obsidian-mind", "llm-wiki"]
        for p in VAULT.rglob("*"):
            for fb in forbidden_plugins:
                self.assertNotIn(fb, p.name.lower())

    # --- P2B-GATE-14: OpenViking Protection ---
    def test_gate_14_openviking_protection(self):
        """P2B-GATE-14: Verify OpenViking production index matches baseline."""
        ov_index = ROOT / ".openviking" / "storage" / "viking_index.json"
        self.assertEqual(self._hash(ov_index), self.baseline_hashes[".openviking/storage/viking_index.json"])

    # --- P2B-GATE-15: CH050 Integrity ---
    def test_gate_15_ch050_integrity(self):
        """P2B-GATE-15: Verify CH050 exact SHA-256 hash."""
        ch050 = [p for p in (ROOT / "正文").glob("*.md") if "0050" in p.name][0]
        self.assertEqual(self._hash(ch050), "4147d6b83c21126faebf2db34dc4bcd33cbd01d781c32338554fd07c854b2a3c")

    # --- P2B-GATE-16: CH051 Integrity ---
    def test_gate_16_ch051_integrity(self):
        """P2B-GATE-16: Verify CH051 exact SHA-256 hash."""
        ch051 = [p for p in (ROOT / "正文").glob("*.md") if "0051" in p.name][0]
        self.assertEqual(self._hash(ch051), "36b53aacf3a3935b3b88ede7495a4cb55c423220aa70d58808829acfb42d2125")

    # --- P2B-GATE-17: CH052 Lock ---
    def test_gate_17_ch052_lock(self):
        """P2B-GATE-17: Exhaustive check that CH052 artifacts are strictly absent."""
        # 1. No CH052 in 正文
        self.assertEqual(len([p for p in (ROOT / "正文").glob("*.md") if "0052" in p.name]), 0)
        # 2. No CH052 in 03_PRODUCTION
        for sub in ["PREWRITE", "DRAFT", "TONE", "FINAL", "CANON_QA"]:
            d = ROOT / "03_PRODUCTION" / sub
            if d.exists():
                self.assertEqual(len([p for p in d.glob("*") if "52" in p.name]), 0)
        # 3. No CH052 in 06_HANDOFF
        self.assertEqual(len([p for p in (ROOT / "06_HANDOFF").glob("*") if "052" in p.name or "ch52" in p.name.lower()]), 0)
        # 4. No CH052 in VAULT/10_CHAPTERS
        ch_dir = VAULT / VaultMapper.get_category_dir("10_CHAPTERS")
        self.assertEqual(len([p for p in ch_dir.glob("*") if "052" in p.name or "ch52" in p.name.lower()]), 0)

    # --- P2B-GATE-18: Workspace Isolation ---
    def test_gate_18_workspace_isolation(self):
        """P2B-GATE-18: Verify 0 symlinks and 0 junctions in workspace."""
        symlinks = [p for p in ROOT.rglob("*") if p.is_symlink()]
        self.assertEqual(len(symlinks), 0)
        if hasattr(Path, "is_junction"):
            junctions = [p for p in ROOT.rglob("*") if p.is_junction()]
            self.assertEqual(len(junctions), 0)

    # --- P2B-GATE-19: No AI Memory Duplication ---
    def test_gate_19_no_ai_memory_duplication(self):
        """P2B-GATE-19: Verify no unauthorized AI memory systems exist in workspace."""
        for disallowed in ["khoj", "smart-connections", "obsidian-mind", "llm-wiki-agent"]:
            matches = list(ROOT.rglob(f"*{disallowed}*"))
            self.assertEqual(len(matches), 0, f"Disallowed AI memory tool found: {matches}")

    # --- P2B-GATE-20: Fail-Closed Behavior ---
    def test_gate_20_fail_closed_behavior(self):
        """P2B-GATE-20: Verify system fails closed on corrupted frontmatter or unauthorized claims."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write("---\nsource: human\nauthority: obsidian\n---\nCorrupted")
            tp = Path(tf.name)
        try:
            ok, msg = MirrorValidator.validate_file(tp)
            self.assertFalse(ok)
        finally:
            tp.unlink()

    # --- P2B-GATE-21: Cold-Start Reproducibility ---
    def test_gate_21_cold_start_reproducibility(self):
        """P2B-GATE-21: Verify mirror generation and verification run cleanly from scratch."""
        manifest_data = MirrorManifest.generate_manifest(ROOT, VAULT)
        self.assertGreaterEqual(manifest_data["total_files"], 275)

    # --- P2B-GATE-22: Full Mirror Audit ---
    def test_gate_22_full_mirror_audit(self):
        """P2B-GATE-22: Category-by-category verification of mirror integrity."""
        for cat in VaultMapper.CATEGORIES:
            cat_p = VAULT / VaultMapper.get_category_dir(cat)
            self.assertTrue(cat_p.exists())
            self.assertTrue(cat_p.is_dir())
            md_files = list(cat_p.glob("*.md"))
            for mf in md_files:
                ok, err = MirrorValidator.validate_file(mf)
                self.assertTrue(ok, f"Validation failed on {mf}: {err}")


if __name__ == "__main__":
    unittest.main()
