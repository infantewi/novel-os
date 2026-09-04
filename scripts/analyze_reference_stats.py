#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVEL OS Reference Novel Macro-Stats Analyzer
0-Token local python analysis for massive reference novels (e.g., 500w words).
Extracts chapter counts, word distributions, dialogue ratios, and cliffhanger patterns.
"""

import os
import re
import sys
import json
import argparse
from statistics import mean, median, stdev


CHAPTER_PATTERN = re.compile(
    r'^\s*(?:第\s*[0-9零一二三四五六七八九十百千万]+\s*[章卷回节集篇]|Chapter\s*\d+)\s*.*$',
    re.MULTILINE
)

QUOTE_PATTERN = re.compile(r'[“"「『](.*?)[”"」』]')


def detect_encoding(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'gb18030', 'gbk', 'big5']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(40960)
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'


def count_chinese_words(text):
    # Counts Chinese characters plus English words
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    numbers = len(re.findall(r'\b\d+\b', text))
    return chinese_chars + english_words + numbers


def analyze_novel(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Reference novel file not found: {file_path}")

    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()

    total_chars = len(content)
    total_words = count_chinese_words(content)

    matches = list(CHAPTER_PATTERN.finditer(content))
    chapters = []

    if matches:
        for i in range(len(matches)):
            start_pos = matches[i].start()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            title = matches[i].group().strip()
            body = content[matches[i].end():end_pos].strip()
            chapters.append({
                "index": i + 1,
                "title": title,
                "body": body
            })
    else:
        # Fallback if no explicit chapter headers
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        chunk_size = 50
        for i in range(0, len(paragraphs), chunk_size):
            body = '\n\n'.join(paragraphs[i:i + chunk_size])
            chapters.append({
                "index": (i // chunk_size) + 1,
                "title": f"Section {(i // chunk_size) + 1}",
                "body": body
            })

    chapter_word_counts = []
    dialogue_char_counts = []
    chapter_endings = {"question": 0, "exclamation": 0, "ellipsis": 0, "period": 0, "other": 0}

    for ch in chapters:
        body = ch["body"]
        words = count_chinese_words(body)
        chapter_word_counts.append(words)

        quotes = QUOTE_PATTERN.findall(body)
        dialogue_chars = sum(len(q) for q in quotes)
        dialogue_char_counts.append(dialogue_chars)

        lines = [line.strip() for line in body.split('\n') if line.strip()]
        if lines:
            last_line = lines[-1]
            if last_line.endswith('?') or last_line.endswith('？'):
                chapter_endings["question"] += 1
            elif last_line.endswith('!') or last_line.endswith('！'):
                chapter_endings["exclamation"] += 1
            elif last_line.endswith('…') or '……' in last_line[-4:]:
                chapter_endings["ellipsis"] += 1
            elif last_line.endswith('。') or last_line.endswith('.'):
                chapter_endings["period"] += 1
            else:
                chapter_endings["other"] += 1

    avg_words = round(mean(chapter_word_counts), 1) if chapter_word_counts else 0
    med_words = round(median(chapter_word_counts), 1) if chapter_word_counts else 0
    sd_words = round(stdev(chapter_word_counts), 1) if len(chapter_word_counts) > 1 else 0

    total_body_words = sum(chapter_word_counts) if chapter_word_counts else 1
    total_dialogue_chars = sum(dialogue_char_counts)
    dialogue_ratio = round((total_dialogue_chars / total_body_words) * 100, 2)

    result = {
        "file_path": os.path.abspath(file_path),
        "detected_encoding": encoding,
        "total_characters": total_chars,
        "total_words": total_words,
        "total_chapters": len(chapters),
        "chapter_word_stats": {
            "average": avg_words,
            "median": med_words,
            "min": min(chapter_word_counts) if chapter_word_counts else 0,
            "max": max(chapter_word_counts) if chapter_word_counts else 0,
            "std_deviation": sd_words
        },
        "dialogue_metrics": {
            "total_dialogue_chars": total_dialogue_chars,
            "dialogue_percentage": dialogue_ratio
        },
        "ending_cliffhanger_distribution": chapter_endings,
        "first_5_chapters": [
            {"index": ch["index"], "title": ch["title"], "words": count_chinese_words(ch["body"])}
            for ch in chapters[:5]
        ]
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="NOVEL OS Reference Novel Macro-Stats Analyzer")
    parser.add_argument("--file", "-f", required=True, help="Path to raw novel text file")
    parser.add_argument("--output", "-o", default=None, help="Path to output JSON file")
    args = parser.parse_args()

    try:
        report = analyze_novel(args.file)
        if args.output:
            out_dir = os.path.dirname(args.output)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"[SUCCESS] Analysis report written to: {args.output}")

        print("\n" + "=" * 50)
        print(" NOVEL OS MACRO-STATS ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"Total Chapters : {report['total_chapters']}")
        print(f"Total Words    : {report['total_words']:,}")
        print(f"Avg Words/Ch   : {report['chapter_word_stats']['average']}")
        print(f"Median Words/Ch: {report['chapter_word_stats']['median']}")
        print(f"Dialogue Ratio : {report['dialogue_metrics']['dialogue_percentage']}%")
        print(f"Endings        : {report['ending_cliffhanger_distribution']}")
        print("=" * 50)

    except Exception as e:
        print(f"[ERROR] Failed to analyze novel: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
