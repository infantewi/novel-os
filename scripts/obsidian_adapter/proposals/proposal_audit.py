# -*- coding: utf-8 -*-
"""Proposal Audit Trail Logger for NOVEL OS V2.3."""

from __future__ import annotations
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from .proposal_schema import Proposal


class ProposalAuditLogger:
    """Maintains an append-only JSONL audit log for all proposal events."""

    def __init__(self, audit_dir: Optional[Path] = None):
        repo_root = Path(__file__).resolve().parents[3]
        self.audit_dir = audit_dir or (repo_root / "04_STATE" / "PROPOSAL_AUDIT")
        self.audit_file = self.audit_dir / "audit_log.jsonl"
        self._ensure_dir()

    def _ensure_dir(self):
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        readme = self.audit_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                "# NOVEL OS V2.3 — Proposal Audit Trail\n\n"
                "This directory contains the append-only JSONL audit trail (`audit_log.jsonl`) recording "
                "every proposal creation, submission, validation, decision, and commit event.\n",
                encoding="utf-8"
            )

    def log_event(
        self,
        proposal_id: str,
        event: str,
        actor: str,
        previous_status: str,
        new_status: str,
        reason: str = "",
        commit_id: Optional[str] = None,
        source_hash: str = "",
        authority_version: str = "2.1.0",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Appends an event to the append-only audit log."""
        entry = {
            "proposal_id": proposal_id,
            "event": event,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "actor": actor,
            "previous_status": previous_status,
            "new_status": new_status,
            "reason": reason,
            "commit_id": commit_id,
            "source_hash": source_hash,
            "authority_version": authority_version,
            "metadata": metadata or {}
        }
        
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
        return entry

    def get_proposal_history(self, proposal_id: str) -> List[Dict[str, Any]]:
        """Retrieves complete chronological event history for a given proposal."""
        if not self.audit_file.exists():
            return []
        
        history = []
        with open(self.audit_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        if record.get("proposal_id") == proposal_id:
                            history.append(record)
                    except Exception:
                        pass
        return history
