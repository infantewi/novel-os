# -*- coding: utf-8 -*-
"""Memory Policy definitions and threshold enforcers for NOVEL OS V2.2."""

from __future__ import annotations
from typing import Dict, Any, List
from .memory_delta import MemoryDelta, MemoryType, MemoryLifecycle


class MemoryPolicy:
    """Enforces governance policies for memory classification and lifecycle."""

    HIGH_IMPACT_TRIGGERS = {
        "突破", "陨落", "死亡", "结拜", "背叛", "废除修为", "改修",
        "主角死亡", "境界倒退", "时间重置", "逆天改命", "夺舍",
        "retcon", "power_scaling_change", "major_death", "relationship_break"
    }

    @classmethod
    def evaluate_impact(cls, delta: MemoryDelta) -> Dict[str, Any]:
        """Evaluates whether a memory delta requires human escalation."""
        requires_human = False
        reasons = []

        if delta.memory_type == MemoryType.CANON_MEMORY:
            requires_human = True
            reasons.append("Modification to CANON_MEMORY requires explicit Human signoff.")

        claim_lower = delta.claim.lower()
        for trig in cls.HIGH_IMPACT_TRIGGERS:
            if trig in claim_lower or trig in str(delta.payload).lower():
                requires_human = True
                reasons.append(f"High-impact trigger detected in claim: '{trig}'")

        if delta.canon_impact:
            requires_human = True
            reasons.append("Delta declared canon_impact = True.")

        delta.requires_human = requires_human
        return {
            "requires_human": requires_human,
            "reasons": reasons,
            "lifecycle": MemoryLifecycle.ACTIVE
        }
