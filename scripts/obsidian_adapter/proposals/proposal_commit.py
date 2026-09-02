# -*- coding: utf-8 -*-
"""Proposal Commit Gate and Atomic Committer for NOVEL OS V2.3."""

from __future__ import annotations
import hashlib
import json
import shutil
import tempfile
import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from .proposal_schema import Proposal, ProposalLifecycleStatus
from .proposal_permission import ProposalPermissionGate
from .proposal_audit import ProposalAuditLogger


class ProposalCommitGate:
    """Executes pre-commit checks and atomic application of approved proposals."""

    def __init__(self, workspace_root: Optional[Path] = None, audit_logger: Optional[ProposalAuditLogger] = None):
        self.workspace_root = workspace_root or Path("D:/Ai work/novel")
        self.permission_gate = ProposalPermissionGate(self.workspace_root / "00_SYSTEM" / "PERMISSION_MATRIX.yaml")
        self.audit_logger = audit_logger or ProposalAuditLogger(self.workspace_root / "04_STATE" / "PROPOSAL_AUDIT")

    def _compute_hash(self, path: Path) -> str:
        if path.exists() and path.is_file():
            return hashlib.sha256(path.read_bytes()).hexdigest()
        return ""

    def commit(
        self,
        proposal: Proposal,
        actor: str,
        dry_run: bool = False,
        target_override_root: Optional[Path] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """Atomically applies an approved proposal."""
        target_root = target_override_root or self.workspace_root
        
        # 1. State Check
        if proposal.lifecycle_status != ProposalLifecycleStatus.APPROVED:
            return False, f"Commit Gate Blocked: Proposal status must be APPROVED (Current: {proposal.lifecycle_status.value}).", None
        
        # 2. Human Approval Check
        if not proposal.approved_by:
            return False, "Commit Gate Blocked: Missing explicit approver signature.", None

        # 3. Permission Check
        perm_ok, perm_msg = self.permission_gate.check_permission("COMMIT", actor, proposal)
        if not perm_ok:
            return False, f"Commit Gate Permission Denied: {perm_msg}", None

        # 4. Authority Hash Re-check
        if proposal.source_reference and proposal.current_authority_hash:
            target_path = target_root / proposal.source_reference
            if target_path.exists():
                current_hash = self._compute_hash(target_path)
                if current_hash and current_hash != proposal.current_authority_hash:
                    return False, f"Commit Gate Conflict: Target file hash mutated since proposal creation (Expected: {proposal.current_authority_hash[:8]}, Actual: {current_hash[:8]}).", None

        # 5. Generate Commit ID
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        commit_id = f"COMMIT-{timestamp_str}-{proposal.proposal_id}"

        if dry_run:
            return True, f"Dry run successful for commit {commit_id}.", commit_id

        # 6. Atomic Write Implementation
        if proposal.source_reference:
            target_file = target_root / proposal.source_reference
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Atomic write via temp file
            temp_file = target_file.parent / f".tmp_{target_file.name}_{timestamp_str}"
            try:
                # Append or update proposed change
                if target_file.exists():
                    existing_text = target_file.read_text(encoding="utf-8")
                    updated_text = f"{existing_text}\n\n<!-- Applied by {proposal.proposal_id} ({commit_id}) -->\n{proposal.proposed_change.strip()}\n"
                else:
                    updated_text = f"<!-- Created by {proposal.proposal_id} ({commit_id}) -->\n{proposal.proposed_change.strip()}\n"

                temp_file.write_text(updated_text, encoding="utf-8")
                
                # Atomic replacement
                temp_file.replace(target_file)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                return False, f"Atomic commit write failed: {e}", None

        # 7. Update Proposal Object State
        prev_status = proposal.lifecycle_status.value
        proposal.lifecycle_status = ProposalLifecycleStatus.COMMITTED
        proposal.commit_status = "COMMITTED"
        proposal.commit_id = commit_id
        proposal.committed_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # 8. Log to Append-Only Audit Trail
        self.audit_logger.log_event(
            proposal_id=proposal.proposal_id,
            event="PROPOSAL_COMMITTED",
            actor=actor,
            previous_status=prev_status,
            new_status="COMMITTED",
            commit_id=commit_id,
            source_hash=proposal.current_authority_hash,
            reason=proposal.reason,
            metadata={"target_id": proposal.target_id, "target_type": proposal.target_type}
        )

        return True, f"Proposal {proposal.proposal_id} committed successfully as {commit_id}.", commit_id
