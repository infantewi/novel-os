#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Reference Slice Extractor.
Extracts specific landmark chapter ranges from the raw reference novel into isolated slice files.
"""

import os
import re
import sys
from pathlib import Path


CHAPTER_PATTERN = re.compile(
    r'^\s*(?:第\s*[0-9零一二三四五六七八九十百千万]+\s*[章卷回节集篇]|Chapter\s*\d+)\s*.*$',
    re.MULTILINE
)

SLICES_CONFIG = [
    {
        "id": "slice_01_persona_establishment",
        "title": "切片一：仙尊格调与世俗反差",
        "start_ch": 27,
        "end_ch": 30,
        "filename": "slice_01_persona_establishment_ch27_30.txt"
    },
    {
        "id": "slice_02_supernatural_revelation",
        "title": "切片二：超凡显圣与多层震惊铺垫",
        "start_ch": 66,
        "end_ch": 74,
        "filename": "slice_02_supernatural_revelation_ch66_74.txt"
    },
    {
        "id": "slice_03_three_stage_climax",
        "title": "切片三：三段式反差打脸巅峰(药神谷)",
        "start_ch": 175,
        "end_ch": 181,
        "filename": "slice_03_three_stage_climax_ch175_181.txt"
    },
    {
        "id": "slice_04_emotional_debt_catharsis",
        "title": "切片四：前世遗憾与亲情尊严清算(燕京王家)",
        "start_ch": 605,
        "end_ch": 616,
        "filename": "slice_04_emotional_debt_catharsis_ch605_616.txt"
    }
]


def extract_slices(novel_file: str, output_dir: str):
    with open(novel_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    matches = list(CHAPTER_PATTERN.finditer(content))
    print(f"Total chapter header matches found: {len(matches)}")

    chapters = []
    for i in range(len(matches)):
        start_pos = matches[i].start()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        title = matches[i].group().strip()
        body = content[matches[i].end():end_pos].strip()

        # Parse chapter number if possible
        num_match = re.search(r'第\s*([0-9零一二三四五六七八九十百千万]+)\s*章', title)
        ch_num = i + 1
        if num_match:
            raw_num = num_match.group(1)
            # Try parsing integer or chinese numeral
            if raw_num.isdigit():
                ch_num = int(raw_num)

        chapters.append({
            "seq_idx": i + 1,
            "title": title,
            "ch_num": ch_num,
            "text": f"{title}\n\n{body}\n\n"
        })

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    for cfg in SLICES_CONFIG:
        start_ch = cfg["start_ch"]
        end_ch = cfg["end_ch"]
        target_file = out_path / cfg["filename"]

        # Filter chapters
        # Look for chapters where either ch_num or seq_idx is in range, or title contains the chapter number
        selected = []
        for ch in chapters:
            t = ch["title"]
            # Check if title matches 第X章
            m = re.search(r'第\s*(\d+)\s*章', t)
            if m:
                num = int(m.group(1))
                if start_ch <= num <= end_ch:
                    selected.append(ch)
            elif start_ch <= ch["seq_idx"] <= end_ch:
                selected.append(ch)

        if not selected:
            # Fallback by sequential index
            selected = [ch for ch in chapters if start_ch <= ch["seq_idx"] <= end_ch]

        combined_text = "".join(c["text"] for c in selected)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(combined_text)

        word_count = len(re.findall(r'[\u4e00-\u9fa5]', combined_text))
        print(f"[OK] Extracted {cfg['title']}: {len(selected)} chapters, {word_count:,} words -> {target_file.name}")


if __name__ == "__main__":
    src_file = "C:/Users/hairaito/Downloads/重生之都市修仙.txt"
    dest_dir = "07_REFERENCE_LIBRARY/REF_001_URBAN_IMMORTAL/slices"
    extract_slices(src_file, dest_dir)
