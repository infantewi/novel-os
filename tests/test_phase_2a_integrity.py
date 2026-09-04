# -*- coding: utf-8 -*-
"""NOVEL OS V2.3 Phase 2A Automated Acceptance & Integrity Test Suite."""

import hashlib
import json
import unittest
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_01_ROOT = REPO_ROOT / "projects" / "01_都市_仙尊归来"
ROOT = BOOK_01_ROOT if (BOOK_01_ROOT / "story_bible.md").exists() else REPO_ROOT
VAULT = ROOT / "NOVEL_OS_VAULT"


@unittest.skip("Historical Phase 2A milestone acceptance suite (Book 01 frozen at CH051)")
class TestPhase2AIntegrity(unittest.TestCase):
    """Verifies all Phase 2A Acceptance Gates (TEST-01 to TEST-10 + Contamination + Authority)."""

    @classmethod
    def setUpClass(cls):
        if not (BOOK_01_ROOT / "story_bible.md").exists():
            raise unittest.SkipTest("Book 01 assets not present in repository (private IP)")
        cls.baseline_hashes = {
            "story_bible.md": "78df5bd4bfa6ceaf99f1d790f2797b34340facb29600b728760b8d49cad6c1cf",
            "current_state.md": "b57149387509bd7b48ab291c53389e7c3963ecc4639bd2e5fb43ac1f41c60b82",
            "pending_hooks.md": "b067c7e3099c326a2a50e76794d35fc5d821fecf46ff847feba5de3a814d1e6a",
            "progress_tracker.md": "dbb4197362334702bc4e98acccb992a10e8776c11d2fc0d5a62bad4afcc06ec9",
            "00_SYSTEM/EXECUTION_STATE.yaml": "9188d1d49d282af59eca596333b7976e667b13ba75817de4f1f0bfa356a96cda",
            "06_HANDOFF/CH051_HANDOFF.md": "b729655217168cd9ad6cd797fe3fa4d1cb379f6ee7387807fb1bfd7fd8ea936d",
            "设定集/世界观.md": "5b84a6c05d52f2d7b849978ac29367a4974b9890c972ce3f0cbaf72580665773",
            "设定集/主角卡.md": "f38744c012f1cba2b15c6df32aba4a898c3e230116b10f35b7352dbaba6cdbfd",
            "设定集/力量体系.md": "3bd102ee787e9e1c82edd8a29cb332551fff5b994a2765a815a657273cd4145a",
            "设定集/势力与反派谱系.md": "856e5b654ef2b1a3e5b438beb81a79a9bff921e70a51ac681bf141d9889a86b2",
            "设定集/重要配角卡.md": "3e7dfea3e82abd647b292186d939417a17fab20abdf4c82064af1fec1e0425e6",
            "设定集/反派设计.md": "856e5b654ef2b1a3e5b438beb81a79a9bff921e70a51ac681bf141d9889a86b2",
        }

    def _hash(self, p: Path) -> str:
        if not p.exists():
            return ""
        return hashlib.sha256(p.read_bytes()).hexdigest()

    def test_01_canon_source_hashes_unchanged(self):
        """TEST-01: Canon source files must remain bit-for-bit unchanged."""
        for rel_p, expected_h in self.baseline_hashes.items():
            p = ROOT / rel_p
            self.assertTrue(p.exists(), f"Source file missing: {rel_p}")
            actual_h = self._hash(p)
            self.assertEqual(actual_h, expected_h, f"Source file mutated: {rel_p}")

    def test_02_ch050_hash_unchanged(self):
        """TEST-02: CH050 physical text hash must remain bit-for-bit unchanged."""
        ch050_files = [p for p in (ROOT / "正文").glob("*.md") if "0050" in p.name]
        self.assertEqual(len(ch050_files), 1, "CH050 file not found in 正文/")
        h = self._hash(ch050_files[0])
        self.assertEqual(h, "4147d6b83c21126faebf2db34dc4bcd33cbd01d781c32338554fd07c854b2a3c")

    def test_03_ch051_hash_unchanged(self):
        """TEST-03: CH051 physical text hash must remain bit-for-bit unchanged."""
        ch051_files = [p for p in (ROOT / "正文").glob("*.md") if "0051" in p.name]
        self.assertEqual(len(ch051_files), 1, "CH051 file not found in 正文/")
        h = self._hash(ch051_files[0])
        self.assertEqual(h, "36b53aacf3a3935b3b88ede7495a4cb55c423220aa70d58808829acfb42d2125")

    @unittest.skip("Historical Phase 2A milestone (production progressed past CH052)")
    def test_04_ch052_remains_absent(self):
        """TEST-04: CH052 must be completely absent from production and vault."""
        # 1. No CH052 in 正文
        ch052_text = [p for p in (ROOT / "正文").glob("*.md") if "0052" in p.name or "ch052" in p.name.lower()]
        self.assertEqual(len(ch052_text), 0, "CH052 found in 正文/")

        # 2. No CH052 in 03_PRODUCTION subdirs
        prod_dirs = ["PREWRITE", "DRAFT", "CANON_QA", "FINAL"]
        for pd in prod_dirs:
            p_dir = ROOT / "03_PRODUCTION" / pd
            if p_dir.exists():
                ch52_f = [f for f in p_dir.glob("*") if "52" in f.name or "0052" in f.name]
                self.assertEqual(len(ch52_f), 0, f"CH052 artifact found in 03_PRODUCTION/{pd}")

        # 3. No CH052 in 06_HANDOFF
        handoff_52 = [f for f in (ROOT / "06_HANDOFF").glob("*") if "ch052" in f.name.lower() or "ch52" in f.name.lower()]
        self.assertEqual(len(handoff_52), 0, "CH052 handoff found in 06_HANDOFF/")

        # 4. No CH052 in NOVEL_OS_VAULT/10_CHAPTERS
        for ch_dir in ["10_CHAPTERS", "10_CHAPTERS_章节镜像"]:
            d = VAULT / ch_dir
            if d.exists():
                vault_ch52 = [f for f in d.glob("*") if "ch052" in f.name.lower() or "0052" in f.name]
                self.assertEqual(len(vault_ch52), 0, f"CH052 markdown found in {ch_dir}/")

    def test_05_execution_state_valid(self):
        """TEST-05: EXECUTION_STATE.yaml must confirm state machine integrity."""
        state_file = REPO_ROOT / "00_SYSTEM" / "EXECUTION_STATE.yaml"
        state = yaml.safe_load(state_file.read_text(encoding="utf-8"))
        self.assertIn("last_completed_chapter", state)
        self.assertGreaterEqual(state["last_completed_chapter"], 51)
        self.assertEqual(state["current_stage"], "COMPLETE")

    def test_06_memory_governor_unchanged(self):
        """TEST-06: Memory Governor code and specifications must remain intact."""
        gov_dir = REPO_ROOT / "memory" / "governor"
        self.assertTrue(gov_dir.exists())
        self.assertTrue((gov_dir / "governor.py").exists())
        self.assertTrue((gov_dir / "quality_gate.py").exists())
        self.assertTrue((REPO_ROOT / "00_SYSTEM" / "MEMORY_GOVERNOR_SPEC_V2.2.md").exists())

    def test_07_openviking_data_unchanged(self):
        """TEST-07: OpenViking index file must exist and contain verified memories."""
        idx_file = (REPO_ROOT / ".openviking" / "storage" / "viking_index.json") if (REPO_ROOT / ".openviking" / "storage" / "viking_index.json").exists() else (ROOT / ".openviking" / "storage" / "viking_index.json")
        self.assertTrue(idx_file.exists())
        data = json.loads(idx_file.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data), 126)

    def test_08_no_writer_worker_called(self):
        """TEST-08: All writer workers must be IDLE in execution state."""
        state_file = REPO_ROOT / "00_SYSTEM" / "EXECUTION_STATE.yaml"
        state = yaml.safe_load(state_file.read_text(encoding="utf-8"))
        workers = state.get("workers", {})
        for w_name, w_info in workers.items():
            self.assertEqual(w_info.get("status"), "IDLE", f"Worker {w_name} is not IDLE")
            self.assertIsNone(w_info.get("last_active"), f"Worker {w_name} was active")

    def test_09_no_obsidian_to_novel_os_write_path(self):
        """TEST-09: Vault policy must declare read-only and no writeback hooks exist."""
        policy_file = VAULT / "99_SYSTEM_系统策略" / "OBSIDIAN_READ_ONLY_POLICY.md"
        if not policy_file.exists():
            policy_file = VAULT / "99_SYSTEM" / "OBSIDIAN_READ_ONLY_POLICY.md"
        self.assertTrue(policy_file.exists())
        txt = policy_file.read_text(encoding="utf-8")
        self.assertIn("HUMAN KNOWLEDGE WORKSPACE / VISUAL REVIEW LAYER", txt)
        self.assertIn("NOVEL OS (Authority)", txt)
        self.assertIn("sync_mode: READ_ONLY", txt)

    def test_10_workspace_isolation(self):
        """TEST-10: Verify workspace isolation (no symlinks, no junctions, no external write)."""
        symlinks = [p for p in ROOT.rglob("*") if p.is_symlink()]
        self.assertEqual(len(symlinks), 0, "Symlinks detected in novel workspace")
        if hasattr(Path, "is_junction"):
            junctions = [p for p in ROOT.rglob("*") if p.is_junction()]
            self.assertEqual(len(junctions), 0, "Junctions detected in novel workspace")

    def test_11_content_contamination(self):
        """TEST-11: Content contamination check (foreshadowing resolution and active states)."""
        f_dir = VAULT / "09_FORESHADOWING_伏笔追踪"
        if not f_dir.exists():
            f_dir = VAULT / "09_FORESHADOWING"
        # H-050-01 must be RESOLVED
        h50_01 = (f_dir / "H-050-01_公海万鬼噬魂凶阵.md").read_text(encoding="utf-8")
        self.assertIn("hook_status: \"RESOLVED\"", h50_01)

        # H-050-02 must be ACTIVE
        h50_02 = (f_dir / "H-050-02_洪门海外仲裁庭与神农古秘境残图.md").read_text(encoding="utf-8")
        self.assertIn("hook_status: \"ACTIVE\"", h50_02)

        # H-026-01 must be ACTIVE
        h26_01 = (f_dir / "H-026-01_南洋黑巫教总坛长线复仇.md").read_text(encoding="utf-8")
        self.assertIn("hook_status: \"ACTIVE\"", h26_01)


    def test_12_authority_direction(self):
        """TEST-12: Every note in vault must declare valid authority (NOVEL_OS for mirror, HUMAN_PROPOSAL for proposals)."""
        for md in VAULT.rglob("*.md"):
            txt = md.read_text(encoding="utf-8")
            self.assertTrue(txt.startswith("---"), f"{md.name} missing frontmatter")
            if "16_proposals" in str(md).lower():
                self.assertIn("authority: HUMAN_PROPOSAL", txt, f"{md.name} missing HUMAN_PROPOSAL authority")
                self.assertIn("sync_mode: PROPOSAL_ONLY", txt, f"{md.name} missing PROPOSAL_ONLY sync_mode")
            else:
                self.assertIn("authority: NOVEL_OS", txt, f"{md.name} missing NOVEL_OS authority")
                self.assertIn("sync_mode: READ_ONLY", txt, f"{md.name} missing READ_ONLY sync_mode")
            self.assertNotIn("authority: obsidian", txt.lower(), f"{md.name} illegal authority")



if __name__ == "__main__":
    unittest.main()
