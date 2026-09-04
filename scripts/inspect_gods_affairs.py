#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import hashlib
from pathlib import Path


SRC_DIR = Path("C:/Users/hairaito/Desktop/素材/上帝们的那些事儿")


def detect_encoding(file_path):
    for enc in ['utf-8-sig', 'utf-8', 'gb18030', 'gbk', 'big5']:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(10240)
            return enc
        except Exception:
            continue
    return 'utf-8'


def inspect_files():
    report = {}
    for f in sorted(SRC_DIR.iterdir()):
        if not f.is_file():
            continue

        enc = detect_encoding(f)
        size = f.stat().st_size
        with open(f, 'r', encoding=enc, errors='ignore') as fp:
            text = fp.read()

        # Count lines, words
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        total_chars = len(text)
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))

        # Look for chapter headers
        headers = re.findall(r'^\s*(?:第[0-9零一二三四五六七八九十百千万]+[章卷回节集篇]|Chapter\s*\d+|【.*?】|[0-9]+[、\.].*?)\s*$', text, re.M)

        # Sample first 5 headers and last 5 headers
        sample_first = lines[:6]
        sample_last = lines[-6:]

        # Calculate md5 of first 100k chars to check overlap
        prefix_hash = hashlib.md5(text[:100000].encode('utf-8')).hexdigest()

        report[f.name] = {
            "size_bytes": size,
            "size_mb": round(size / (1024 * 1024), 2),
            "encoding": enc,
            "total_lines": len(lines),
            "total_chars": total_chars,
            "chinese_chars": chinese_chars,
            "detected_chapter_headers_count": len(headers),
            "first_headers": headers[:5] if headers else [],
            "last_headers": headers[-5:] if headers else [],
            "first_lines": sample_first,
            "last_lines": sample_last,
            "prefix_hash_100k": prefix_hash
        }

    out_file = Path(__file__).resolve().parent / "gods_affairs_inspection.json"
    with open(out_file, 'w', encoding='utf-8') as fp:
        json.dump(report, fp, ensure_ascii=False, indent=2)
    print(f"Inspection written to {out_file}")


if __name__ == "__main__":
    inspect_files()
