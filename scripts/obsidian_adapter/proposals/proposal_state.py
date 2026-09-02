# -*- coding: utf-8 -*-
"""Proposal State Machine and Lifecycle Controller for NOVEL OS V2.3."""

from __future__ import annotations
import copy
import datetime
from typing import Dict, Any, Tuple
from .proposal_schema import Proposal, ProposalLifecycleStatus


class ProposalStateMachine:
    """Enforces strict proposal lifecycle transitions."""

    LEGAL_TRANSITIONS = {
        ProposalLifecycleStatus.DRAFT: [
            ProposalLifecycleStatus.SUBMITTED,
            ProposalLifecycleStatus.CANCELLED
        ],
        ProposalLifecycleStatus.SUBMITTED: [
            ProposalLifecycleStatus.VALIDATING,
            ProposalLifecycleStatus.BLOCKED,
            ProposalLifecycleStatus.CANCELLED
        ],
        ProposalLifecycleStatus.VALIDATING: [
            ProposalLifecycleStatus.VALIDATED,
            ProposalLifecycleStatus.CONFLICT,
            ProposalLifecycleStatus.BLOCKED
        ],
        ProposalLifecycleStatus.VALIDATED: [
            ProposalLifecycleStatus.HUMAN_REVIEW,
            ProposalLifecycleStatus.BLOCKED
        ],
        ProposalLifecycleStatus.HUMAN_REVIEW: [
            ProposalLifecycleStatus.APPROVED,
            ProposalLifecycleStatus.REJECTED,
            ProposalLifecycleStatus.CANCELLED
        ],
        ProposalLifecycleStatus.APPROVED: [
            ProposalLifecycleStatus.COMMITTING,
            ProposalLifecycleStatus.CANCELLED
        ],
        ProposalLifecycleStatus.COMMITTING: [
            ProposalLifecycleStatus.COMMITTED,
            ProposalLifecycleStatus.BLOCKED
        ],
        # Terminal states
        ProposalLifecycleStatus.COMMITTED: [],
        ProposalLifecycleStatus.REJECTED: [],
        ProposalLifecycleStatus.CONFLICT: [],
        ProposalLifecycleStatus.BLOCKED: [],
        ProposalLifecycleStatus.EXPIRED: [],
        ProposalLifecycleStatus.CANCELLED: [],
    }

    @classmethod
    def can_transition(cls, current_status: ProposalLifecycleStatus, target_status: ProposalLifecycleStatus) -> bool:
        allowed = cls.LEGAL_TRANSITIONS.get(current_status, [])
        return target_status in allowed

    @classmethod
    def transition(cls, proposal: Proposal, target_status: ProposalLifecycleStatus) -> Tuple[bool, str]:
        current = proposal.lifecycle_status
        if not cls.can_transition(current, target_status):
            return False, f"Illegal lifecycle transition: Cannot move proposal from '{current.value}' to '{target_status.value}'."
        proposal.lifecycle_status = target_status
        return True, f"Successfully transitioned to {target_status.value}."

    @classmethod
    def create_revision(cls, original: Proposal, new_proposal_id: str, actor: str) -> Proposal:
        """Creates a new proposal linked as a revision of the original."""
        rev = copy.deepcopy(original)
        rev.proposal_id = new_proposal_id
        rev.revision_of = original.proposal_id
        rev.created_by = actor
        rev.created_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        rev.lifecycle_status = ProposalLifecycleStatus.DRAFT
        rev.approved_by = None
        rev.approved_at = None
        rev.commit_status = "NOT_COMMITTED"
        rev.commit_id = None
        rev.committed_at = None
        rev.rejection_reason = None
        return rev
