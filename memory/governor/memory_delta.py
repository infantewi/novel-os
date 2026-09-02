# -*- coding: utf-8 -*-
"""Memory Delta data models and types for NOVEL OS V2.2."""

from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MemoryType(str, Enum):
    CANON_MEMORY = "CANON_MEMORY"
    CHARACTER_MEMORY = "CHARACTER_MEMORY"
    RELATIONSHIP_MEMORY = "RELATIONSHIP_MEMORY"
    EVENT_MEMORY = "EVENT_MEMORY"
    TIMELINE_MEMORY = "TIMELINE_MEMORY"
    LOCATION_MEMORY = "LOCATION_MEMORY"
    FORESHADOW_MEMORY = "FORESHADOW_MEMORY"
    KNOWLEDGE_BOUNDARY_MEMORY = "KNOWLEDGE_BOUNDARY_MEMORY"
    CHAPTER_MEMORY = "CHAPTER_MEMORY"
    STATE_MEMORY = "STATE_MEMORY"


class KnowledgeStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    UNREVEALED = "UNREVEALED"
    FALSE_BELIEF = "FALSE_BELIEF"
    CONTRADICTED = "CONTRADICTED"
    SUPERSEDED = "SUPERSEDED"


class MemoryLifecycle(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"


@dataclass
class Provenance:
    source_type: str = "PROPOSAL"
    source_uri: str = ""
    source_chapter: int = 0
    source_hash: str = ""
    canon_version: str = "2.2.0"
    state_version: str = "2.2.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    created_by: str = "WEBNOVEL_WRITER"
    approved_by: Optional[str] = None


@dataclass
class MemoryDelta:
    delta_id: str = field(default_factory=lambda: f"DELTA-{uuid.uuid4().hex[:8].upper()}")
    memory_type: MemoryType = MemoryType.EVENT_MEMORY
    entity: str = ""
    claim: str = ""
    source: str = ""
    source_chapter: int = 0
    provenance: Provenance = field(default_factory=Provenance)
    confidence: float = 1.0
    proposed_action: str = "ADD"
    affected_entities: List[str] = field(default_factory=list)
    canon_impact: bool = False
    state_impact: bool = False
    requires_human: bool = False
    knowledge_status: KnowledgeStatus = KnowledgeStatus.KNOWN
    knowledge_holders: List[str] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)
