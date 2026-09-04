# -*- coding: utf-8 -*-
"""Proposal Schema and Data Structures for NOVEL OS V2.3."""

from __future__ import annotations
import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Any, List, Optional


class ProposalType(str, Enum):
    CANON = "P2C-CANON"
    CHARACTER = "P2C-CHARACTER"
    RELATIONSHIP = "P2C-RELATIONSHIP"
    TIMELINE = "P2C-TIMELINE"
    LOCATION = "P2C-LOCATION"
    FACTION = "P2C-FACTION"
    ABILITY = "P2C-ABILITY"
    ITEM = "P2C-ITEM"
    FORESHADOW = "P2C-FORESHADOW"
    STATE = "P2C-STATE"
    MEMORY = "P2C-MEMORY"
    OUTLINE = "P2C-OUTLINE"


class ProposalLifecycleStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    APPROVED = "APPROVED"
    COMMITTING = "COMMITTING"
    COMMITTED = "COMMITTED"
    REJECTED = "REJECTED"
    CONFLICT = "CONFLICT"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ValidationStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    VALID = "VALID"
    INVALID = "INVALID"
    STALE = "STALE"
    BOUNDARY_VIOLATION = "BOUNDARY_VIOLATION"


class ConflictStatus(str, Enum):
    NOT_CHECKED = "NOT_CHECKED"
    NO_CONFLICT = "NO_CONFLICT"
    SOFT_CONFLICT = "SOFT_CONFLICT"
    HARD_CONFLICT = "HARD_CONFLICT"
    DUPLICATE = "DUPLICATE"


@dataclass
class Proposal:
    proposal_id: str
    proposal_type: ProposalType
    target_id: str
    target_type: str
    proposed_change: str
    reason: str
    
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    created_by: str = "HUMAN_AUTHOR"
    workspace: str = "."
    vault: str = "NOVEL_OS_VAULT"
    
    source_reference: str = ""
    source_version: str = "2.1.0"
    current_authority_hash: str = ""
    
    expected_effect: str = ""
    affected_entities: List[str] = field(default_factory=list)
    affected_chapters: List[int] = field(default_factory=list)
    affected_hooks: List[str] = field(default_factory=list)
    
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: int = 0
    hard_trigger: str = ""
    
    validation_status: ValidationStatus = ValidationStatus.NOT_STARTED
    validation_details: str = ""
    conflict_status: ConflictStatus = ConflictStatus.NOT_CHECKED
    conflict_details: str = ""
    
    provenance: Dict[str, Any] = field(default_factory=dict)
    
    human_review_required: bool = True
    lifecycle_status: ProposalLifecycleStatus = ProposalLifecycleStatus.DRAFT
    
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    commit_status: str = "NOT_COMMITTED"
    commit_id: Optional[str] = None
    committed_at: Optional[str] = None
    
    revision_of: Optional[str] = None
    schema_version: str = "2.3.0"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["proposal_type"] = self.proposal_type.value if isinstance(self.proposal_type, ProposalType) else str(self.proposal_type)
        d["lifecycle_status"] = self.lifecycle_status.value if isinstance(self.lifecycle_status, ProposalLifecycleStatus) else str(self.lifecycle_status)
        d["risk_level"] = self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level)
        d["validation_status"] = self.validation_status.value if isinstance(self.validation_status, ValidationStatus) else str(self.validation_status)
        d["conflict_status"] = self.conflict_status.value if isinstance(self.conflict_status, ConflictStatus) else str(self.conflict_status)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Proposal:
        d = dict(data)
        if "proposal_type" in d and isinstance(d["proposal_type"], str):
            d["proposal_type"] = ProposalType(d["proposal_type"])
        if "lifecycle_status" in d and isinstance(d["lifecycle_status"], str):
            d["lifecycle_status"] = ProposalLifecycleStatus(d["lifecycle_status"])
        if "risk_level" in d and isinstance(d["risk_level"], str):
            d["risk_level"] = RiskLevel(d["risk_level"])
        if "validation_status" in d and isinstance(d["validation_status"], str):
            d["validation_status"] = ValidationStatus(d["validation_status"])
        if "conflict_status" in d and isinstance(d["conflict_status"], str):
            d["conflict_status"] = ConflictStatus(d["conflict_status"])
        return cls(**d)
