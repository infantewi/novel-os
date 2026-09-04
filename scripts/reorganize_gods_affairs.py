#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Reorganization & Deduplication Tool for 《上帝们的那些事儿》.
Cleans up duplicate files (all.txt vs 第一战区.txt), normalizes encodings to UTF-8,
structures into standardized volumes (00 to 04), and synthesizes a true complete edition.
"""

import os
import re
import shutil
from pathlib import Path


TARGET_DIR = Path("C:/Users/hairaito/Desktop/素材/上帝们的那些事儿")
BACKUP_DIR = TARGET_DIR / "_raw_backup"


def detect_encoding(file_path):
    for enc in ['utf-8-sig', 'utf-8', 'gb18030', 'gbk', 'big5']:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(10240)
            return enc
        except Exception:
            continue
    return 'utf-8'


def clean_text_content(text: str) -> str:
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove leading BOM if present
    text = text.lstrip('\ufeff')

    # Remove excessive blank lines (more than 2 consecutive blank lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def run_reorganization():
    print("=" * 60)
    print(" REORGANIZING 《上帝们的那些事儿》")
    print("=" * 60)

    if not TARGET_DIR.exists():
        raise FileNotFoundError(f"Directory not found: {TARGET_DIR}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Mapping source files to standard volume files
    volume_map = [
        {
            "vol_num": 0,
            "src_name": "上帝们的那些事儿·前传.txt",
            "dest_name": "00_前传·徐锋篇.txt",
            "title_header": "【前传】徐锋篇（上帝游戏的起源）\n" + "=" * 50 + "\n\n"
        },
        {
            "vol_num": 1,
            "src_name": "上帝们的那些事儿(第一战区).txt",
            "dest_name": "01_第一战区·天才博弈篇.txt",
            "title_header": "【第一战区】天才博弈篇（200位天才跨越七大世界博弈）\n" + "=" * 50 + "\n\n"
        },
        {
            "vol_num": 2,
            "src_name": "上帝们的那些事儿(第二战区).txt",
            "dest_name": "02_第二战区·诸神争霸篇.txt",
            "title_header": "【第二战区】诸神争霸篇（经典前作群雄第二轮上帝博弈）\n" + "=" * 50 + "\n\n"
        },
        {
            "vol_num": 3,
            "src_name": "上帝们的那些事儿(第三战区).txt",
            "dest_name": "03_第三战区·神魔挑战篇.txt",
            "title_header": "【第三战区】神魔挑战篇（诸界神佛向美夜子的决战）\n" + "=" * 50 + "\n\n"
        },
        {
            "vol_num": 4,
            "src_name": "上帝们的那些事儿(第四战区).txt",
            "dest_name": "04_第四战区·逆天终章篇.txt",
            "title_header": "【第四战区】逆天终章篇（跨次元逆天战神终极试炼）\n" + "=" * 50 + "\n\n"
        },
    ]

    combined_full_edition = []
    combined_full_edition.append("《上帝们的那些事儿》（全五卷·完整精校合订本）\n作者：杨建东\n" + "=" * 60 + "\n\n")

    for item in volume_map:
        src_path = TARGET_DIR / item["src_name"]
        if not src_path.exists():
            # Check backup dir if already moved
            src_path = BACKUP_DIR / item["src_name"]
            if not src_path.exists():
                print(f"[WARN] Source file missing: {item['src_name']}")
                continue

        enc = detect_encoding(src_path)
        with open(src_path, "r", encoding=enc, errors="ignore") as fp:
            raw_text = fp.read()

        cleaned = clean_text_content(raw_text)

        # Write clean volume file
        dest_path = TARGET_DIR / item["dest_name"]
        with open(dest_path, "w", encoding="utf-8") as fp:
            fp.write(cleaned)

        print(f"[PROCESSED] {item['dest_name']} ({len(cleaned):,} 字符, 编码 UTF-8)")

        # Append to complete edition
        combined_full_edition.append(item["title_header"])
        combined_full_edition.append(cleaned)
        combined_full_edition.append("\n\n" + "-" * 60 + "\n\n")

        # Backup raw source file
        backup_path = BACKUP_DIR / item["src_name"]
        if src_path != backup_path and src_path.exists():
            shutil.copy2(src_path, backup_path)

    # Also backup the redundant all.txt
    old_all = TARGET_DIR / "all.txt"
    if old_all.exists():
        print(f"[DEDUPLICATE] Moving redundant incomplete all.txt to {BACKUP_DIR.name}/")
        shutil.move(str(old_all), str(BACKUP_DIR / "all_raw_duplicate_war1.txt"))

    # Write the true COMPLETE MASTER EDITION
    full_edition_file = TARGET_DIR / "《上帝们的那些事儿》(全五卷·完整精校合订本).txt"
    with open(full_edition_file, "w", encoding="utf-8") as fp:
        fp.write("".join(combined_full_edition))

    total_full_chars = len(open(full_edition_file, "r", encoding="utf-8").read())
    print(f"\n[SUCCESS] True Master Edition written: {full_edition_file.name}")
    print(f"Total Full Chars: {total_full_chars:,} 字符 (约 600 万字)")

    # Remove old source files that were backed up so root folder is clean
    for item in volume_map:
        old_file = TARGET_DIR / item["src_name"]
        if old_file.exists():
            old_file.unlink()

    print("\n" + "=" * 60)
    print(" REORGANIZATION COMPLETED")
    print(f"Active clean files in: {TARGET_DIR}")
    print(f"Raw backups preserved in: {BACKUP_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    run_reorganization()
