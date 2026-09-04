#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Root Workspace Cleanup Script.
Removes legacy root junctions and hardlinks so that D:\Ai work\novel
is a clean Studio OS root, with all book files exclusively in projects/01_都市_仙尊归来/.
"""

import os
import sys
import subprocess
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = WORKSPACE_ROOT / "projects" / "01_都市_仙尊归来"

ROOT_JUNCTIONS_TO_REMOVE = [
    "01_CANON",
    "02_OUTLINE",
    "03_PRODUCTION",
    "04_STATE",
    "05_MARKETING",
    "06_HANDOFF",
    "设定集",
    "大纲",
    "正文",
    "审查报告",
    "NOVEL_OS_VAULT",
    ".story-system",
    ".webnovel",
    "test_junc",
]

ROOT_HARDLINKS_TO_REMOVE = [
    "story_bible.md",
    "book_rules.md",
    "chapter_summaries.md",
    "current_state.md",
    "handoff_current.md",
    "pattern-detection.md",
    "pending_hooks.md",
    "progress_tracker.md",
]


def remove_junction(link_path: Path):
    """Removes an NTFS directory junction on Windows safely without touching target."""
    if not link_path.exists() and not link_path.is_symlink():
        return
    # On Windows, rmdir removes junctions without deleting target contents
    cmd = ["cmd", "/c", "rmdir", str(link_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to os.unlink
        try:
            os.unlink(str(link_path))
        except Exception as e:
            print(f"[WARN] Failed to remove junction {link_path}: {res.stderr or e}")


def remove_file(file_path: Path):
    """Removes a file/hardlink from root safely."""
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"[REMOVED FILE] {file_path.name}")
        except Exception as e:
            print(f"[WARN] Failed to remove file {file_path.name}: {e}")


def main():
    print("=" * 60)
    print(" NOVEL OS ROOT WORKSPACE CLEANUP")
    print("=" * 60)

    if not PROJECT_ROOT.exists():
        raise RuntimeError(f"Safety check failed: Project folder not found at {PROJECT_ROOT}!")

    # 1. Clean up root junctions
    for j_name in ROOT_JUNCTIONS_TO_REMOVE:
        j_path = WORKSPACE_ROOT / j_name
        # If it's test_junc, just remove
        if j_name == "test_junc":
            if j_path.exists() or j_path.is_symlink():
                print(f"[REMOVING TEMP JUNCTION] {j_name}")
                remove_junction(j_path)
            continue

        target_path = PROJECT_ROOT / j_name
        if not target_path.exists():
            print(f"[ERROR] Target path does not exist in project: {target_path}! Skipping {j_name}.")
            continue

        print(f"[REMOVING ROOT JUNCTION] {j_name} (Target preserved in {target_path})")
        remove_junction(j_path)

    # 2. Clean up root hardlinks
    for f_name in ROOT_HARDLINKS_TO_REMOVE:
        f_path = WORKSPACE_ROOT / f_name
        target_file = PROJECT_ROOT / f_name
        if not target_file.exists():
            print(f"[ERROR] Target file does not exist in project: {target_file}! Skipping {f_name}.")
            continue

        remove_file(f_path)

    print("\n" + "=" * 60)
    print(" ROOT CLEANUP COMPLETED")
    print("=" * 60)
    print(f"Project folder intact at: {PROJECT_ROOT}")


if __name__ == "__main__":
    main()
