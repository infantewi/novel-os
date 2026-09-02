# -*- coding: utf-8 -*-
"""Validator for Obsidian Mirror files and boundary enforcement."""

import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List


class MirrorValidator:
    """Validates that Obsidian Mirror strictly maintains read-only downstream semantics."""

    @classmethod
    def validate_file(cls, file_path: Path) -> Tuple[bool, str]:
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"
        
        # Only check markdown files for frontmatter
        if file_path.suffix.lower() == ".md":
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                return False, f"Cannot read file as utf-8: {e}"

            if not content.startswith("---"):
                return False, f"Missing frontmatter header in {file_path.name}"
            
            if "source: NOVEL_OS" not in content:
                return False, f"Missing 'source: NOVEL_OS' in {file_path.name}"
            
            if "authority: NOVEL_OS" not in content:
                return False, f"Invalid authority in {file_path.name} (must be NOVEL_OS)"
            
            if "sync_mode: READ_ONLY" not in content:
                return False, f"Invalid sync_mode in {file_path.name} (must be READ_ONLY)"
            
            if "editable_in_obsidian: false" not in content:
                return False, f"Missing 'editable_in_obsidian: false' in {file_path.name}"
            
            content_lower = content.lower()
            if "authority: obsidian" in content_lower:
                return False, f"Forbidden authority claim 'authority: obsidian' in {file_path.name}"
            
            if "source: human" in content_lower and "source: novel_os" not in content_lower:
                return False, f"Forbidden source claim in {file_path.name}"
            
            # Ensure CH052 is not inadvertently marked complete or generated as production text
            if "ch052" in file_path.name.lower() and "10_chapters" in str(file_path).lower():
                return False, f"Forbidden chapter file detected in 10_CHAPTERS: {file_path.name}"

        return True, "Valid"

    @classmethod
    def validate_vault(cls, vault_root: Path) -> Tuple[bool, List[str]]:
        """Validate entire vault directory tree."""
        errors = []
        if not vault_root.exists():
            return False, ["Vault root does not exist."]
        
        for md_file in vault_root.rglob("*.md"):
            ok, msg = cls.validate_file(md_file)
            if not ok:
                errors.append(msg)

        # Check for forbidden CH052 chapter note
        ch052_path = vault_root / "10_CHAPTERS" / "CH052.md"
        if ch052_path.exists():
            errors.append("CH052.md found in 10_CHAPTERS/ (Forbidden in Phase 2A)")

        return len(errors) == 0, errors

    @classmethod
    def compute_sha256(cls, file_path: Path) -> str:
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

