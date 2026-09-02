# -*- coding: utf-8 -*-
"""Vault Schema and Path Mapper for Obsidian Read-Only Mirror."""

import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class VaultMapper:
    """Maps NOVEL OS domain entities to Obsidian Vault categories."""

    CATEGORIES = [
        "00_HOME",
        "01_CANON",
        "02_CHARACTERS",
        "03_RELATIONSHIPS",
        "04_TIMELINE",
        "05_LOCATIONS",
        "06_FACTIONS",
        "07_ABILITIES",
        "08_ITEMS",
        "09_FORESHADOWING",
        "10_CHAPTERS",
        "11_ARCS",
        "12_STATE",
        "13_HANDOFF",
        "14_MEMORY",
        "15_QA",
        "99_SYSTEM"
    ]

    @classmethod
    def get_vault_path(cls, vault_root: Path, category: str, filename: str) -> Path:
        if category not in cls.CATEGORIES:
            raise ValueError(f"Unknown vault category: {category}")
        return vault_root / category / filename

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

