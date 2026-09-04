# -*- coding: utf-8 -*-
"""Proposal Conflict Detector and Boundary Validator for NOVEL OS V2.3."""

from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple
from .proposal_schema import Proposal, ValidationStatus, ConflictStatus


class ProposalConflictDetector:
    """Checks proposals against authoritative Canon, State, and Knowledge Boundaries."""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parents[3]

    def _compute_file_hash(self, rel_path: str) -> str:
        p = self.workspace_root / rel_path
        if p.exists() and p.is_file():
            return hashlib.sha256(p.read_bytes()).hexdigest()
        return ""

    def validate_proposal(self, proposal: Proposal) -> Tuple[ValidationStatus, ConflictStatus, str]:
        # 1. Stale Authority Hash Check
        if proposal.source_reference and proposal.current_authority_hash:
            actual_hash = self._compute_file_hash(proposal.source_reference)
            if actual_hash and actual_hash != proposal.current_authority_hash:
                return (
                    ValidationStatus.STALE,
                    ConflictStatus.HARD_CONFLICT,
                    f"Stale Proposal: Target file '{proposal.source_reference}' hash ({actual_hash[:8]}...) does not match proposal base hash ({proposal.current_authority_hash[:8]}...)."
                )

        text = f"{proposal.proposed_change} {proposal.reason}".lower()

        # 2. Hard Canon Conflict: Protagonist Realm / Power scaling violation
        if ("金丹" in text or "金丹期" in text) and "陆辰" in text and "提前" in text:
            return (
                ValidationStatus.INVALID,
                ConflictStatus.HARD_CONFLICT,
                "Hard Canon Conflict: Attempting to advance protagonist to 金丹期 in violation of official 筑基初期 boundary."
            )

        # 3. Hard Canon Conflict: Personality violation (talk therapy / converting villain)
        if ("话疗" in text or "感化" in text or "以德报怨" in text) and "陆辰" in text:
            return (
                ValidationStatus.INVALID,
                ConflictStatus.HARD_CONFLICT,
                "Hard Canon Conflict: Protagonist personality violation (玄天仙尊极道杀伐果断，严禁话疗感化敌人)."
            )

        # 4. Knowledge Boundary Violation
        if "绝密" in text or "未公开" in text or "unrevealed" in text:
            if "陆辰直接知晓" in text or "主角已知" in text:
                return (
                    ValidationStatus.BOUNDARY_VIOLATION,
                    ConflictStatus.HARD_CONFLICT,
                    "Knowledge Boundary Violation: Protagonist possesses UNREVEALED information without in-world discovery event."
                )

        # 5. Timeline Paradox
        if "时间线回溯" in text or "时序颠倒" in text:
            return (
                ValidationStatus.INVALID,
                ConflictStatus.HARD_CONFLICT,
                "Timeline Conflict: Chronological paradox detected in proposed change."
            )

        return ValidationStatus.VALID, ConflictStatus.NO_CONFLICT, "No conflicts detected. Passed validation."
