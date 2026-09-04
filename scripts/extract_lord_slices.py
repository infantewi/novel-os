#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract landmark slices from 《山那边的领主》 into 07_REFERENCE_LIBRARY/REF_005_MEDIEVAL_LORD/slices/.
"""

import os
import re
from pathlib import Path


repo_root = Path(__file__).resolve().parents[1]
SRC_FILE = repo_root / "references/raw_materials/山那边的领主/山那边的领主.txt"
DEST_DIR = repo_root / "07_REFERENCE_LIBRARY/REF_005_MEDIEVAL_LORD/slices"


def extract_slices():
    print(">>> Extracting slices for REF_005: 山那边的领主...")
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    with open(SRC_FILE, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Slice 1: Founding White Dove Valley & First Economic Cycle (Ch 1 - 5)
    p1 = text.find("第一章 祖父的故事1")
    p2 = text.find("第六章 吉尔的故事 1")
    if p1 != -1 and p2 != -1:
        s1 = text[p1:p2].strip()
        (DEST_DIR / "slice_01_valley_founding_and_woodworking_ch1_5.txt").write_text(s1, encoding="utf-8")
        print(f"  [OK] Slice 1 (Valley Founding & Woodworking Economy): {len(s1)} chars")

    # Slice 2: Autumn Harvest & Medieval Peasant Life (Ch 37 - 41)
    p3 = text.find("第三十七章 秋收时期的爱情故事 1")
    p4 = text.find("第四十二章 秋收时期的爱情故事 6")
    if p3 != -1 and p4 != -1:
        s2 = text[p3:p4].strip()
        (DEST_DIR / "slice_02_autumn_harvest_and_peasant_life_ch37_41.txt").write_text(s2, encoding="utf-8")
        print(f"  [OK] Slice 2 (Autumn Harvest & Peasant Life): {len(s2)} chars")

    # Slice 3: Valley Defense / Militia / Mountain Choke Point
    m3 = re.search(r'(强盗|巡逻队|哨卡|敌袭|警钟|白鸽谷[\s\S]{10,200}防守)', text[200000:600000])
    if m3:
        start_pos = 200000 + max(0, m3.start() - 3000)
        end_pos = start_pos + 30000
        s3 = text[start_pos:end_pos].strip()
        (DEST_DIR / "slice_03_militia_defense_and_chokepoint.txt").write_text(s3, encoding="utf-8")
        print(f"  [OK] Slice 3 (Militia & Valley Defense): {len(s3)} chars")

    # Slice 4: Second Generation Transition & Outward Expansion (around Ch 120 / Vol 2)
    p5 = text.find("第二卷")
    if p5 == -1:
        p5 = text.find("第一百二十章")
    if p5 != -1:
        start_pos = max(0, p5 - 5000)
        end_pos = start_pos + 30000
        s4 = text[start_pos:end_pos].strip()
        (DEST_DIR / "slice_04_second_generation_and_expansion.txt").write_text(s4, encoding="utf-8")
        print(f"  [OK] Slice 4 (Second Generation & Expansion): {len(s4)} chars")


if __name__ == "__main__":
    extract_slices()
