# -*- coding: utf-8 -*-
"""Proposal Permission Gate for NOVEL OS V2.3."""

from __future__ import annotations
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple
from .proposal_schema import Proposal


class ProposalPermissionGate:
    """Enforces explicit RBAC on proposal creation, approval, and commit actions."""

    def __init__(self, matrix_path: Path = None):
        self.matrix_path = matrix_path or Path("D:/Ai work/novel/00_SYSTEM/PERMISSION_MATRIX.yaml")
        self.config = {}
        if self.matrix_path.exists():
            try:
                self.config = yaml.safe_load(self.matrix_path.read_text(encoding="utf-8")) or {}
            except Exception:
                self.config = {}

    def check_permission(self, action: str, actor: str, proposal: Proposal) -> Tuple[bool, str]:
        act = action.upper()
        act_actor = actor.upper()
        
        # 1. Action: CREATE
        if act == "CREATE":
            allowed_creators = ["HUMAN", "HUMAN_AUTHOR", "OBSIDIAN", "OBSIDIAN_UI", "WEBNOVEL_WRITER", "OH_STORY", "MASTER_ORCHESTRATOR"]
            if any(c in act_actor for c in allowed_creators):
                return True, "Authorized to create proposal."
            return False, f"Actor '{actor}' is not authorized to create proposals."

        # 2. Action: SUBMIT
        if act == "SUBMIT":
            return True, "Authorized to submit proposal for review."

        # 3. Action: APPROVE
        if act == "APPROVE":
            # Worker self-approval is STRICTLY FORBIDDEN
            if act_actor == proposal.created_by.upper() and not ("HUMAN" in act_actor or "ORCHESTRATOR" in act_actor):
                return False, f"Worker self-approval violation: '{actor}' cannot approve its own proposal."
            
            if "OBSIDIAN" in act_actor and "HUMAN" not in act_actor:
                return False, "Obsidian standalone UI cannot self-approve without explicit Human Gate."
                
            allowed_approvers = ["HUMAN", "HUMAN_AUTHOR", "HUMAN_GATE", "MASTER_ORCHESTRATOR"]
            if any(a in act_actor for a in allowed_approvers):
                return True, f"Actor '{actor}' authorized to approve proposal."
            return False, f"Actor '{actor}' is not authorized to approve proposals."

        # 4. Action: COMMIT
        if act == "COMMIT":
            # Obsidian cannot directly commit
            if "OBSIDIAN" in act_actor and "HUMAN" not in act_actor:
                return False, "Obsidian cannot directly commit to authoritative Canon/State."
            
            # Non-human worker cannot commit unapproved proposal
            if proposal.approved_by is None:
                return False, "Cannot commit proposal without prior explicit approval."

            allowed_committers = ["HUMAN", "HUMAN_AUTHOR", "MASTER_ORCHESTRATOR", "SYSTEM_COMMIT_GATE"]
            if any(a in act_actor for a in allowed_committers):
                return True, f"Actor '{actor}' authorized to commit proposal."
            return False, f"Actor '{actor}' is not authorized to commit."

        return False, f"Unknown action '{action}'."
