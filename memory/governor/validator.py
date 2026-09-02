# -*- coding: utf-8 -*-
"""Memory Validator ensuring data structure, mandatory fields, and semantic completeness."""

from __future__ import annotations
from typing import Dict, Any, List
from .memory_delta import MemoryDelta


class MemoryValidator:
    """Validates structural and semantic properties of memory deltas."""

    @staticmethod
    def validate(delta: MemoryDelta) -> Dict[str, Any]:
        errors = []
        if not delta.entity and delta.memory_type not in ["CHAPTER_MEMORY", "TIMELINE_MEMORY"]:
            errors.append("Missing required field: 'entity'")
        if not delta.claim:
            errors.append("Missing required field: 'claim'")
        if delta.source_chapter < 0:
            errors.append("Invalid 'source_chapter': must be >= 0")
        if not delta.provenance:
            errors.append("Missing 'provenance' tracking information")
        if not (0.0 <= delta.confidence <= 1.0):
            errors.append(f"Invalid confidence score: {delta.confidence}")

        passed = len(errors) == 0
        return {
            "passed": passed,
            "errors": errors,
            "delta_id": delta.delta_id
        }
