# -*- coding: utf-8 -*-
"""Vault Schema and Path Mapper for Obsidian Read-Only Mirror."""

import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class VaultMapper:
    """Maps NOVEL OS domain entities to Obsidian Vault categories."""

    CATEGORY_DIRS = {
        "00_HOME": "00_HOME_监控看板",
        "01_CANON": "01_CANON_设定圣经",
        "02_CHARACTERS": "02_CHARACTERS_人物档案",
        "03_RELATIONSHIPS": "03_RELATIONSHIPS_人际谱系",
        "04_TIMELINE": "04_TIMELINE_编年时序",
        "05_LOCATIONS": "05_LOCATIONS_场景地理",
        "06_FACTIONS": "06_FACTIONS_势力分布",
        "07_ABILITIES": "07_ABILITIES_功法神通",
        "08_ITEMS": "08_ITEMS_法宝法器",
        "09_FORESHADOWING": "09_FORESHADOWING_伏笔追踪",
        "10_CHAPTERS": "10_CHAPTERS_章节镜像",
        "11_ARCS": "11_ARCS_分卷大纲",
        "12_STATE": "12_STATE_状态指标",
        "13_HANDOFF": "13_HANDOFF_生产交接",
        "14_MEMORY": "14_MEMORY_记忆库",
        "15_QA": "15_QA_质量审查",
        "16_PROPOSALS": "16_PROPOSALS_人类提案",
        "99_SYSTEM": "99_SYSTEM_系统策略",
    }

    CATEGORIES = list(CATEGORY_DIRS.keys())

    @classmethod
    def get_category_dir(cls, category: str) -> str:
        """Returns the Chinese-English directory name for a category key or folder name."""
        if category in cls.CATEGORY_DIRS:
            return cls.CATEGORY_DIRS[category]
        if category in cls.CATEGORY_DIRS.values():
            return category
        # Fallback matching by prefix (e.g. '01_CANON' in '01_CANON_设定圣经')
        for k, v in cls.CATEGORY_DIRS.items():
            if category.startswith(k):
                return v
        return category

    @classmethod
    def get_vault_path(cls, vault_root: Path, category: str, filename: str) -> Path:
        dir_name = cls.get_category_dir(category)
        return vault_root / dir_name / filename

    @classmethod
    def format_frontmatter(cls, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Construct standard mandatory frontmatter for all mirrored notes."""
        if metadata is None:
            metadata = {}

        now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        lines = ["---"]
        lines.append("source: NOVEL_OS")
        lines.append("authority: NOVEL_OS")
        lines.append("sync_mode: READ_ONLY")
        lines.append("editable_in_obsidian: false")
        lines.append(f"generated_at: \"{metadata.get('generated_at', now_iso)}\"")
        lines.append(f"canon_version: \"{metadata.get('canon_version', '2.1.0')}\"")
        lines.append(f"state_version: \"{metadata.get('state_version', '2.1.0')}\"")
        lines.append(f"memory_version: \"{metadata.get('memory_version', '2.2.0')}\"")

        # Custom extra metadata fields
        for k, v in metadata.items():
            if k in [
                "source", "authority", "sync_mode", "editable_in_obsidian",
                "generated_at", "canon_version", "state_version", "memory_version"
            ]:
                continue
            if isinstance(v, (list, dict)):
                lines.append(f"{k}: {v}")
            elif isinstance(v, bool):
                lines.append(f"{k}: {'true' if v else 'false'}")
            elif isinstance(v, (int, float)):
                lines.append(f"{k}: {v}")
            else:
                lines.append(f"{k}: \"{v}\"")

        lines.append("---")
        return "\n".join(lines)

    @classmethod
    def wikilink(cls, target: str, display_text: Optional[str] = None) -> str:
        """Create standard Obsidian wikilink [[target|display_text]]."""
        if display_text and display_text != target:
            return f"[[{target}|{display_text}]]"
        return f"[[{target}]]"
