# -*- coding: utf-8 -*-
"""Proposal Provenance and Lineage Tracker for NOVEL OS V2.3."""

from __future__ import annotations
import datetime
from typing import Dict, Any
from .proposal_schema import Proposal


class ProposalProvenanceTracker:
    """Attaches and verifies provenance records on proposals."""

    @classmethod
    def attach_provenance(cls, proposal: Proposal, event: str, actor: str, details: str = "") -> Dict[str, Any]:
        if not proposal.provenance:
            proposal.provenance = {
                "created_by": proposal.created_by,
                "created_at": proposal.created_at,
                "source_file": proposal.source_reference,
                "source_version": proposal.source_version,
                "source_hash": proposal.current_authority_hash,
                "history": []
            }
            
        record = {
            "event": event,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "actor": actor,
            "details": details
        }
        proposal.provenance.setdefault("history", []).append(record)
        return proposal.provenance

    @classmethod
    def verify_provenance(cls, proposal: Proposal) -> bool:
        if not proposal.created_by or not proposal.created_at:
            return False
        return True
