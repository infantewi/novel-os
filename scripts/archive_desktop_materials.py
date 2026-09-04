#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Desktop Materials Archiver.
1. Moves desktop materials from ~/Desktop/素材 to references/raw_materials/
2. For 《无职转生》, keeps ONLY the Markdown (.md) format (the gold standard for AI comprehension),
   discarding bloated EPUB and redundant TXT.
3. Cleans up Desktop folder completely.
"""

import os
import shutil
from pathlib import Path


DESKTOP_SRC = Path.home() / "Desktop" / "素材"
ARCHIVE_DEST = Path(__file__).resolve().parents[1] / "references" / "raw_materials"


def archive_materials():
    print("=" * 60)
    print(" NOVEL OS DESKTOP MATERIALS ARCHIVING & STREAMLINING")
    print("=" * 60)

    if not DESKTOP_SRC.exists():
        print(f"[WARN] Desktop folder does not exist: {DESKTOP_SRC}")
        return

    ARCHIVE_DEST.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # 1. Process 《无职转生》: Keep MD format (Most suitable for AI)
    # -------------------------------------------------------------
    mushoku_src = DESKTOP_SRC / "无职转生 ～到了异世界就拿出真本事～"
    mushoku_dest = ARCHIVE_DEST / "无职转生"
    if mushoku_src.exists():
        print(">>> Archiving 《无职转生》 (Selecting Markdown as the optimal AI format)...")
        mushoku_dest.mkdir(parents=True, exist_ok=True)

        # Copy notes
        notes_src = mushoku_src / "无职转生笔记"
        if notes_src.exists():
            shutil.copytree(notes_src, mushoku_dest / "无职转生笔记", dirs_exist_ok=True)
            print("  [OK] Copied 16 analysis notes")

        # Copy re0联动
        re0_src = mushoku_src / "re0联动"
        if re0_src.exists():
            shutil.copytree(re0_src, mushoku_dest / "re0联动", dirs_exist_ok=True)
            print("  [OK] Copied re0联动 chapters")

        # Copy 老鲁迪日记
        diary_src = mushoku_src / "老鲁迪日记.txt"
        if diary_src.exists():
            shutil.copy2(diary_src, mushoku_dest / "老鲁迪日记.txt")
            print("  [OK] Copied 老鲁迪日记.txt")

        # Copy ONLY MD text
        md_src = mushoku_src / "正文" / "MD"
        md_dest = mushoku_dest / "正文_Markdown"
        if md_src.exists():
            shutil.copytree(md_src, md_dest, dirs_exist_ok=True)
            md_count = len(list(md_dest.glob("*.md")))
            print(f"  [OK] Copied {md_count} Markdown volumes to 正文_Markdown/ (Skipped EPUB & TXT)")

    # -------------------------------------------------------------
    # 2. Process 《上帝们的那些事儿》
    # -------------------------------------------------------------
    gods_src = DESKTOP_SRC / "上帝们的那些事儿"
    gods_dest = ARCHIVE_DEST / "上帝们的那些事儿"
    if gods_src.exists():
        print(">>> Archiving 《上帝们的那些事儿》...")
        gods_dest.mkdir(parents=True, exist_ok=True)
        for f in gods_src.iterdir():
            if f.is_file():
                shutil.copy2(f, gods_dest / f.name)
        print(f"  [OK] Copied cleaned volumes and master complete edition")

    # -------------------------------------------------------------
    # 3. Process 《无限挑战游戏》
    # -------------------------------------------------------------
    infinite_src = DESKTOP_SRC / "无限挑战游戏.txt"
    if infinite_src.exists():
        print(">>> Archiving 《无限挑战游戏》...")
        shutil.copy2(infinite_src, ARCHIVE_DEST / "无限挑战游戏.txt")
        print("  [OK] Copied 无限挑战游戏.txt")

    # -------------------------------------------------------------
    # 4. Verification Check before Desktop Removal
    # -------------------------------------------------------------
    print("\n>>> Verifying archived files in D drive...")
    mushoku_check = len(list((ARCHIVE_DEST / "无职转生" / "正文_Markdown").glob("*.md")))
    gods_check = (ARCHIVE_DEST / "上帝们的那些事儿" / "《上帝们的那些事儿》(全五卷·完整精校合订本).txt").exists()
    infinite_check = (ARCHIVE_DEST / "无限挑战游戏.txt").exists()

    if mushoku_check >= 26 and gods_check and infinite_check:
        print("[VERIFICATION PASSED] All assets safely archived in D:/Ai work/novel/references/raw_materials/")
        print(">>> Cleaning up desktop materials folder...")
        shutil.rmtree(DESKTOP_SRC)
        print(f"[SUCCESS] Desktop folder {DESKTOP_SRC} has been completely removed.")
    else:
        print(f"[ERROR] Verification failed: mushoku={mushoku_check}, gods={gods_check}, infinite={infinite_check}")
        print("Desktop folder was NOT removed for safety.")

    print("=" * 60)


if __name__ == "__main__":
    archive_materials()
