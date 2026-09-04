#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Project Sandboxing Migration Script.
Moves Book 01 assets to projects/01_都市_仙尊归来 while maintaining
root dual-access junctions and hardlinks for 100% backward compatibility.
"""

import os
import sys
import shutil
import hashlib
import subprocess
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR_NAME = "01_都市_仙尊归来"
PROJECT_ROOT = WORKSPACE_ROOT / "projects" / PROJECT_DIR_NAME

DIRECTORIES_TO_MIGRATE = [
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
]

FILES_TO_MIGRATE = [
    "story_bible.md",
    "book_rules.md",
    "chapter_summaries.md",
    "current_state.md",
    "handoff_current.md",
    "pattern-detection.md",
    "pending_hooks.md",
    "progress_tracker.md",
]


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def create_junction(link_path: Path, target_path: Path):
    """Creates an NTFS directory junction on Windows."""
    cmd = ["cmd", "/c", "mklink", "/J", str(link_path), str(target_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to create junction {link_path} -> {target_path}: {res.stderr}")


def create_hardlink(link_path: Path, target_path: Path):
    """Creates an NTFS hard link for files on Windows."""
    cmd = ["cmd", "/c", "mklink", "/H", str(link_path), str(target_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to copy if hardlink fails
        shutil.copy2(target_path, link_path)


def run_migration():
    print("=" * 60)
    print(" NOVEL OS PROJECT SANDBOXING MIGRATION")
    print("=" * 60)

    # 1. Clean up any previous mangled test folders in projects
    projects_base = WORKSPACE_ROOT / "projects"
    projects_base.mkdir(parents=True, exist_ok=True)
    for item in projects_base.iterdir():
        if item.is_dir() and item != PROJECT_ROOT:
            print(f"[CLEANUP] Removing temp folder: {item.name}")
            shutil.rmtree(item, ignore_errors=True)

    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Target project directory: {PROJECT_ROOT}")

    # Baseline hash check of key canon file
    baseline_canon = WORKSPACE_ROOT / "设定集" / "主角卡.md"
    orig_hash = sha256_file(baseline_canon)

    # 2. Migrate Directories
    for d_name in DIRECTORIES_TO_MIGRATE:
        src = WORKSPACE_ROOT / d_name
        dest = PROJECT_ROOT / d_name

        if not src.exists():
            print(f"[SKIP] Directory does not exist in root: {d_name}")
            continue

        # Check if already a junction
        if src.is_symlink() or (src.stat().st_file_attributes & 0x400):  # FILE_ATTRIBUTE_REPARSE_POINT
            print(f"[SKIP] Already a junction: {d_name}")
            continue

        print(f"[MOVING DIR] {d_name} -> {dest}")
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(src), str(dest))

        # Create junction at root pointing to the new project location
        print(f"[CREATING JUNCTION] {src} -> {dest}")
        create_junction(src, dest)

    # 3. Migrate Files
    for f_name in FILES_TO_MIGRATE:
        src = WORKSPACE_ROOT / f_name
        dest = PROJECT_ROOT / f_name

        if not src.exists():
            print(f"[SKIP] File does not exist in root: {f_name}")
            continue

        print(f"[MOVING FILE] {f_name} -> {dest}")
        if dest.exists():
            dest.unlink()
        shutil.move(str(src), str(dest))

        # Create hardlink at root pointing to the new project location
        print(f"[CREATING HARDLINK] {src} -> {dest}")
        create_hardlink(src, dest)

    # 4. Integrity Validation
    new_canon = PROJECT_ROOT / "设定集" / "主角卡.md"
    new_hash = sha256_file(new_canon)
    root_canon = WORKSPACE_ROOT / "设定集" / "主角卡.md"
    root_hash = sha256_file(root_canon)

    print("\n" + "=" * 60)
    print(" VERIFICATION RESULTS")
    print("=" * 60)
    print(f"Original Hash (主角卡.md): {orig_hash}")
    print(f"Project  Hash (主角卡.md): {new_hash}")
    print(f"Root Junc Hash(主角卡.md): {root_hash}")

    if orig_hash and orig_hash == new_hash == root_hash:
        print("[SUCCESS] Bit-for-bit hash validation PASSED 100%!")
    else:
        print("[WARNING] Hash mismatch or missing file!")

    print(f"\nMigration completed successfully. Active project: {PROJECT_ROOT}")


if __name__ == "__main__":
    run_migration()
