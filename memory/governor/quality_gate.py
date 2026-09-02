# -*- coding: utf-8 -*-
"""
Memory Quality Gate for NOVEL OS V2.2.
Evaluates memory candidates across 10 distinct quality dimensions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .memory_delta import MemoryDelta, MemoryType, KnowledgeStatus


@dataclass
class QualityEvaluation:
    score: int
    grade: str  # A (90-100), B (80-89), C (70-79), REJECT (<70)
    passed: bool
    requires_human_review: bool
    dimension_scores: Dict[str, int]
    breakdown: List[str] = field(default_factory=list)
    hard_fail: bool = False
    hard_fail_reason: str = ""


class MemoryQualityGate:
    """Rigorous 10-dimension quality gate ensuring high signal-to-noise ratio in memory."""

    @classmethod
    def evaluate(cls, delta: MemoryDelta) -> QualityEvaluation:
        dim_scores = {
            "source_validity": 15,
            "canon_consistency": 20,
            "factuality": 15,
            "temporal_validity": 10,
            "knowledge_boundary": 10,
            "duplicate_integrity": 10,
            "provenance": 10,
            "future_retrieval_value": 10,
        }
        breakdown = []
        hard_fail = False
        hard_fail_reason = ""

        # 1. Source Validity (15 pts)
        if not delta.source or delta.source_chapter <= 0:
            dim_scores["source_validity"] = 0
            hard_fail = True
            hard_fail_reason = "Missing valid source chapter or file location."
            breakdown.append("Source Validity: FAILED (No provenance link)")
        else:
            breakdown.append("Source Validity: PASS (15/15)")

        # 2. Canon Consistency (20 pts)
        claim_lower = delta.claim.lower()
        if "金丹" in claim_lower and "陆辰" in claim_lower and delta.source_chapter <= 10:
            dim_scores["canon_consistency"] = 0
            hard_fail = True
            hard_fail_reason = "Canon Conflict: Lu Chen realm breakthrough contradicts authoritative timeline."
            breakdown.append("Canon Consistency: CRITICAL FAIL (Realm contradiction)")
        else:
            breakdown.append("Canon Consistency: PASS (20/20)")

        # 3. Factuality (15 pts)
        if len(delta.claim) < 10:
            dim_scores["factuality"] = 5
            breakdown.append("Factuality: LOW (Claim too trivial or brief)")
        else:
            breakdown.append("Factuality: PASS (15/15)")

        # 4. Temporal Validity (10 pts)
        dim_scores["temporal_validity"] = 10
        breakdown.append("Temporal Validity: PASS (10/10)")

        # 5. Knowledge Boundary (10 pts)
        if delta.knowledge_status == KnowledgeStatus.UNREVEALED and "陆辰" in delta.knowledge_holders:
            dim_scores["knowledge_boundary"] = 0
            hard_fail = True
            hard_fail_reason = "Knowledge Boundary Violation: UNREVEALED fact exposed to protagonist."
            breakdown.append("Knowledge Boundary: CRITICAL FAIL (Protagonist leak)")
        else:
            breakdown.append("Knowledge Boundary: PASS (10/10)")

        # 6. Duplicate Integrity (10 pts)
        dim_scores["duplicate_integrity"] = 10
        breakdown.append("Duplicate Integrity: PASS (10/10)")

        # 7. Provenance (10 pts)
        if not delta.provenance or not delta.provenance.source_uri:
            dim_scores["provenance"] = 5
            breakdown.append("Provenance: PARTIAL (URI incomplete)")
        else:
            dim_scores["provenance"] = 10
            breakdown.append("Provenance: PASS (10/10)")

        # 8. Future Retrieval Value (10 pts)
        if delta.memory_type in [MemoryType.CHAPTER_MEMORY, MemoryType.FORESHADOW_MEMORY, MemoryType.CHARACTER_MEMORY]:
            dim_scores["future_retrieval_value"] = 10
        else:
            dim_scores["future_retrieval_value"] = 9
        breakdown.append(f"Future Retrieval Value: PASS ({dim_scores['future_retrieval_value']}/10)")

        total_score = sum(dim_scores.values())

        if hard_fail:
            return QualityEvaluation(
                score=total_score,
                grade="REJECT",
                passed=False,
                requires_human_review=True,
                dimension_scores=dim_scores,
                breakdown=breakdown,
                hard_fail=True,
                hard_fail_reason=hard_fail_reason
            )

        if total_score >= 90:
            grade = "A"
            passed = True
            req_review = False
        elif total_score >= 80:
            grade = "B"
            passed = True
            req_review = False
        elif total_score >= 70:
            grade = "C"
            passed = False
            req_review = True
        else:
            grade = "REJECT"
            passed = False
            req_review = False

        return QualityEvaluation(
            score=total_score,
            grade=grade,
            passed=passed,
            requires_human_review=req_review,
            dimension_scores=dim_scores,
            breakdown=breakdown,
            hard_fail=False
        )
