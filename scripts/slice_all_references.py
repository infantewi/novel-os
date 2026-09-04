#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Multi-Reference Slice Extractor (Updated with Light Novel Japanese Chapter Formats).
Extracts landmark scenes for REF_002, REF_003, and REF_004.
"""

import os
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1] / "07_REFERENCE_LIBRARY"
DESKTOP_DIR = Path.home() / "Desktop" / "素材"


def slice_mushoku():
    print(">>> Slicing REF_002: 无职转生...")
    txt_dir = DESKTOP_DIR / "无职转生 ～到了异世界就拿出真本事～" / "正文" / "TXT"
    out_dir = BASE_DIR / "REF_002_MUSHOKU_TENSEI" / "slices"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Turning Point 1: vol2.txt 第八话「转折点」
    vol2_text = (txt_dir / "vol2.txt").read_text(encoding="utf-8", errors="ignore")
    pos1 = vol2_text.find("转折点")
    if pos1 != -1:
        start_idx = max(0, vol2_text.rfind("\n", 0, pos1))
        tp1_slice = vol2_text[start_idx:start_idx + 25000]
        (out_dir / "slice_01_turning_point_1_catastrophe.txt").write_text(tp1_slice, encoding="utf-8")
        print(f"  [OK] Extracted Slice 1 (Turning Point 1): {len(tp1_slice)} chars")

    # 2. Turning Point 2: vol6.txt 转折点２
    vol6_text = (txt_dir / "vol6.txt").read_text(encoding="utf-8", errors="ignore")
    pos2 = vol6_text.find("转折点２")
    if pos2 == -1:
        pos2 = vol6_text.find("转折点2")
    if pos2 == -1:
        pos2 = vol6_text.find("转折点")
    if pos2 != -1:
        start_idx = max(0, vol6_text.rfind("\n", 0, pos2))
        tp2_slice = vol6_text[start_idx:start_idx + 25000]
        (out_dir / "slice_02_turning_point_2_orsted.txt").write_text(tp2_slice, encoding="utf-8")
        print(f"  [OK] Extracted Slice 2 (Turning Point 2): {len(tp2_slice)} chars")

    # 3. Labyrinth & Paul's Death: vol12.txt 第九话 死斗 -> 第十一话 墓前
    vol12_text = (txt_dir / "vol12.txt").read_text(encoding="utf-8", errors="ignore")
    pos3 = vol12_text.find("死斗")
    if pos3 != -1:
        start_idx = max(0, vol12_text.rfind("\n", 0, pos3))
        tp3_slice = vol12_text[start_idx:start_idx + 35000]
        (out_dir / "slice_03_labyrinth_paul_sacrifice.txt").write_text(tp3_slice, encoding="utf-8")
        print(f"  [OK] Extracted Slice 3 (Paul's Sacrifice & Depression): {len(tp3_slice)} chars")

    # 4. Old Rudeus Diary: 老鲁迪日记.txt
    diary_file = DESKTOP_DIR / "无职转生 ～到了异世界就拿出真本事～" / "老鲁迪日记.txt"
    if diary_file.exists():
        diary_slice = diary_file.read_text(encoding="utf-8", errors="ignore")
        (out_dir / "slice_04_old_rudeus_diary_turning_point_4.txt").write_text(diary_slice, encoding="utf-8")
        print(f"  [OK] Extracted Slice 4 (Old Rudeus Diary): {len(diary_slice)} chars")


def slice_gods_affairs():
    print(">>> Slicing REF_003: 上帝们的那些事儿...")
    src_dir = DESKTOP_DIR / "上帝们的那些事儿"
    out_dir = BASE_DIR / "REF_003_GODS_AFFAIRS" / "slices"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Prequel
    prequel = src_dir / "00_前传·徐锋篇.txt"
    if prequel.exists():
        t = prequel.read_text(encoding="utf-8", errors="ignore")
        (out_dir / "slice_01_prequel_sms_invitation.txt").write_text(t, encoding="utf-8")
        print(f"  [OK] Extracted Slice 1 (Prequel): {len(t)} chars")

    # 2. Zone 1 Opening
    z1 = src_dir / "01_第一战区·天才博弈篇.txt"
    if z1.exists():
        t1 = z1.read_text(encoding="utf-8", errors="ignore")
        slice_z1_open = t1[:25000]
        (out_dir / "slice_02_zone1_opening_gaotianfeng.txt").write_text(slice_z1_open, encoding="utf-8")
        print(f"  [OK] Extracted Slice 2 (Zone 1 Opening): {len(slice_z1_open)} chars")

        # 3. Zone 1 Deadline Climax
        pos = t1.rfind("DEADLINE")
        if pos == -1:
            pos = t1.rfind("DEAD　LINE")
        if pos != -1:
            start_pos = max(0, pos - 10000)
            end_pos = min(len(t1), pos + 25000)
            slice_z1_climax = t1[start_pos:end_pos]
            (out_dir / "slice_03_zone1_deadline_climax.txt").write_text(slice_z1_climax, encoding="utf-8")
            print(f"  [OK] Extracted Slice 3 (Zone 1 Climax): {len(slice_z1_climax)} chars")


def slice_infinite_challenge():
    print(">>> Slicing REF_004: 无限挑战游戏...")
    src_file = DESKTOP_DIR / "无限挑战游戏.txt"
    out_dir = BASE_DIR / "REF_004_INFINITE_CHALLENGE" / "slices"
    out_dir.mkdir(parents=True, exist_ok=True)

    if src_file.exists():
        t = src_file.read_text(encoding="gb18030", errors="ignore")
        # 1. Opening Chapters 1-3
        m = re.search(r'(第1章\s*死前愿望[\s\S]*?)(第4章|$)', t)
        if m:
            s1 = m.group(1).strip()
            (out_dir / "slice_01_death_wish_opening_ch1_3.txt").write_text(s1, encoding="utf-8")
            print(f"  [OK] Extracted Slice 1 (Opening): {len(s1)} chars")

        # 2. Mid-game rule countdown climax
        pos = t.find("倒计时")
        if pos != -1:
            start_pos = max(0, pos - 5000)
            end_pos = min(len(t), pos + 20000)
            s2 = t[start_pos:end_pos].strip()
            (out_dir / "slice_02_rules_countdown_climax.txt").write_text(s2, encoding="utf-8")
            print(f"  [OK] Extracted Slice 2 (Countdown Climax): {len(s2)} chars")


if __name__ == "__main__":
    slice_mushoku()
    slice_gods_affairs()
    slice_infinite_challenge()
    print("\nAll slices extracted successfully!")
