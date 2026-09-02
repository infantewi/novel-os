# -*- coding: utf-8 -*-
"""Manifest Generator and Tracker for Obsidian Mirror."""

import time
import yaml
from pathlib import Path
from typing import Dict, Any, List
from .validator import MirrorValidator


class MirrorManifest:
    """Tracks exported mirror files and hashes."""

    @classmethod
    def generate_manifest(cls, source_root: Path, vault_root: Path, sync_time: str = None) -> Dict[str, Any]:
        manifest_data = {
            "source_root": str(source_root).replace("\\", "/"),
            "vault_root": str(vault_root).replace("\\", "/"),
            "sync_mode": "READ_ONLY",
            "last_sync": sync_time or time.strftime("%Y-%m-%dT%H:%M:%S"),
            "canon_version": "2.1.0",
            "state_version": "2.1.0",
            "memory_version": "2.2.0",
            "total_files": 0,
            "mappings": {},
            "source_hashes": {},
            "mirror_hashes": {}
        }


        # Track key source hashes
        key_source_files = [
            "story_bible.md",
            "current_state.md",
            "handoff_current.md",
            "pending_hooks.md",
            "progress_tracker.md",
            "00_SYSTEM/EXECUTION_STATE.yaml",
            "06_HANDOFF/CH051_HANDOFF.md",
            "设定集/世界观.md",
            "设定集/主角卡.md",
            "设定集/力量体系.md",
            "设定集/势力与反派谱系.md",
            "设定集/重要配角卡.md",
            "设定集/反派设计.md",
            "大纲/总纲.md",
            "大纲/第02卷-名动江南.md",
        ]
        for rel_src in key_source_files:
            src_file = source_root / rel_src
            if src_file.exists():
                manifest_data["source_hashes"][rel_src] = MirrorValidator.compute_sha256(src_file)

        # Track exported mirror files
        total_count = 0
        for cat_dir in sorted(vault_root.iterdir()):
            if cat_dir.is_dir() and not cat_dir.name.startswith("."):
                files_in_cat = []
                for md_file in sorted(cat_dir.glob("*.md")):
                    rel_p = str(md_file.relative_to(vault_root)).replace("\\", "/")
                    h = MirrorValidator.compute_sha256(md_file)
                    manifest_data["mirror_hashes"][rel_p] = h
                    files_in_cat.append(md_file.name)
                    total_count += 1
                manifest_data["mappings"][cat_dir.name] = files_in_cat

        manifest_data["total_files"] = total_count

        manifest_path = vault_root / "99_SYSTEM" / "MIRROR_MANIFEST.yaml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            yaml.dump(manifest_data, f, allow_unicode=True, sort_keys=False)

        return manifest_data

