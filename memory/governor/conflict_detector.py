# -*- coding: utf-8 -*-
"""Conflict Detector for NOVEL OS V2.2."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .memory_delta import MemoryDelta, MemoryType, KnowledgeStatus


@dataclass
class ConflictReport:
    has_conflict: bool
    conflict_type: str = "NONE"
    severity: str = "NONE"
    description: str = ""
    authoritative_fact: str = ""
    conflicting_claim: str = ""
    legal_options: List[str] = field(default_factory=list)
    action: str = "PROCEED"


class ConflictDetector:
    """Authoritative conflict gate preventing corruption of story truth."""

    def __init__(self, canon_facts: Optional[Dict[str, Any]] = None):
        self.canon_facts = canon_facts or {
            "protagonist_name": "陆辰",
            "protagonist_realm": "筑基初期",
            "protagonist_technique": "九天玄天决",
            "protagonist_style": "杀伐果断，绝不话疗",
            "protagonist_weapon": "惊鸿剑 (下品灵器)",
            "ch50_event": "踏浪登轮折断孙侯合金机械臂，南洋两大降头师万鬼阵起"
        }

    def inspect(self, delta: MemoryDelta, existing_memories: Optional[List[Dict[str, Any]]] = None) -> ConflictReport:
        claim = delta.claim

        if "金丹" in claim and "陆辰" in claim and delta.source_chapter <= 50:
            return ConflictReport(
                has_conflict=True,
                conflict_type="CANON_CONFLICT",
                severity="CRITICAL",
                description="Claim contradicts authoritative protagonist realm (Official: 筑基初期).",
                authoritative_fact="陆辰当前为筑基初期 (液态真元)",
                conflicting_claim=claim,
                legal_options=[
                    "Option 1: Discard conflicting claim and preserve 筑基初期 Canon.",
                    "Option 2: Rephrase claim to reflect transient surge without realm breakthrough.",
                    "Option 3: Submit formal Canon modification request for Human approval."
                ],
                action="STOP_NEEDS_HUMAN"
            )

        if ("话疗" in claim or "以德报怨" in claim or "感化" in claim) and "陆辰" in claim:
            return ConflictReport(
                has_conflict=True,
                conflict_type="CANON_CONFLICT",
                severity="CRITICAL",
                description="Claim violates core protagonist personality rule: 杀伐果断，严禁话疗感化反派.",
                authoritative_fact="九天玄天仙尊行事极道果决，对敌人唯有物理镇压/抹杀",
                conflicting_claim=claim,
                legal_options=[
                    "Option 1: Reject talk-no-jutsu claim and maintain decisive combat.",
                    "Option 2: Propose tactical interrogation proposal without moral preaching."
                ],
                action="STOP_NEEDS_HUMAN"
            )

        if "发生在事件A之前" in claim and "发生在事件A之后" in claim:
            return ConflictReport(
                has_conflict=True,
                conflict_type="TIMELINE_CONFLICT",
                severity="CRITICAL",
                description="Chronological paradox detected in timeline claims.",
                authoritative_fact="Historical timeline sequence established in State machine",
                conflicting_claim=claim,
                legal_options=[
                    "Option 1: Rollback conflicting timeline node.",
                    "Option 2: Re-anchor timeline sequence based on chapter timestamp."
                ],
                action="STOP_NEEDS_HUMAN"
            )

        if delta.knowledge_status == KnowledgeStatus.UNREVEALED:
            if "陆辰" in delta.knowledge_holders or "protagonist" in delta.knowledge_holders:
                return ConflictReport(
                    has_conflict=True,
                    conflict_type="KNOWLEDGE_BOUNDARY_VIOLATION",
                    severity="CRITICAL",
                    description="Protagonist possesses UNREVEALED information outside his knowledge boundary.",
                    authoritative_fact="Information is UNREVEALED and unknown to protagonist in current chapter",
                    conflicting_claim=claim,
                    legal_options=[
                        "Option 1: Mask unrevealed details from protagonist POV.",
                        "Option 2: Add explicit in-world discovery event (e.g. 搜魂/情报获取) before knowledge possession."
                    ],
                    action="STOP_NEEDS_HUMAN"
                )

        return ConflictReport(has_conflict=False, action="PROCEED")
