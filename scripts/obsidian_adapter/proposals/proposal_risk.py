# -*- coding: utf-8 -*-
"""Proposal Risk Gate and Scoring for NOVEL OS V2.3."""

from __future__ import annotations
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple
from .proposal_schema import Proposal, RiskLevel


class ProposalRiskGate:
    """Evaluates risk score and hard triggers according to 00_SYSTEM/RISK_GATE.yaml."""

    def __init__(self, risk_gate_path: Path = None):
        self.risk_gate_path = risk_gate_path or Path("D:/Ai work/novel/00_SYSTEM/RISK_GATE.yaml")
        self.config = {}
        if self.risk_gate_path.exists():
            try:
                self.config = yaml.safe_load(self.risk_gate_path.read_text(encoding="utf-8")) or {}
            except Exception:
                self.config = {}

    def assess_risk(self, proposal: Proposal) -> Tuple[RiskLevel, int, str]:
        score = 0
        hard_trigger_hit = ""
        
        change_text = f"{proposal.proposed_change} {proposal.reason} {proposal.target_id}".lower()
        
        # Check Hard Triggers
        hard_triggers = [
            ("major_death", ["死亡", "斩杀", "击毙", "抹杀", "陨落", "死于", "伏诛"]),
            ("core_relationship_change", ["绝交", "反目", "生死仇敌", "断绝关系", "背叛"]),
            ("major_canon_change", ["修改境界", "修改设定", "重写世界观", "改写前世", "颠覆力量体系"]),
            ("protagonist_major_power_change", ["突破金丹", "元婴", "化神", "仙尊道果", "境界连跳"]),
            ("timeline_break", ["时间倒流", "穿越回", "时序颠倒"]),
        ]
        
        for ht_name, keywords in hard_triggers:
            if any(k in change_text for k in keywords):
                hard_trigger_hit = ht_name
                break
                
        # Calculate Risk Score
        if proposal.proposal_type.value in ["P2C-CANON", "P2C-OUTLINE"]:
            score += 4
        elif proposal.proposal_type.value in ["P2C-CHARACTER", "P2C-ABILITY", "P2C-RELATIONSHIP"]:
            score += 2
        else:
            score += 1

        if len(proposal.affected_entities) > 2:
            score += 2
        if len(proposal.affected_chapters) > 3:
            score += 2
        if len(proposal.affected_hooks) > 0:
            score += 2
            
        if hard_trigger_hit:
            level = RiskLevel.HIGH
            score = max(score, 8)
        elif score >= 8:
            level = RiskLevel.HIGH
        elif score >= 4:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW
            
        return level, score, hard_trigger_hit
