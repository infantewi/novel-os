# -*- coding: utf-8 -*-
"""Proposal Manager and Workflow Orchestrator for NOVEL OS V2.3."""

from __future__ import annotations
import datetime
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .proposal_schema import (
    Proposal,
    ProposalType,
    ProposalLifecycleStatus,
    RiskLevel,
    ValidationStatus,
    ConflictStatus,
)
from .proposal_parser import ProposalParser
from .proposal_permission import ProposalPermissionGate
from .proposal_risk import ProposalRiskGate
from .proposal_conflict import ProposalConflictDetector
from .proposal_provenance import ProposalProvenanceTracker
from .proposal_state import ProposalStateMachine
from .proposal_commit import ProposalCommitGate
from .proposal_audit import ProposalAuditLogger


class ProposalManager:
    """High-level facade for proposal creation, submission, review, approval, and execution."""

    SUBDIRS = [
        "00_INBOX_收件箱",
        "01_DRAFT_草稿",
        "02_SUBMITTED_已提交",
        "03_REVIEW_待评审",
        "04_APPROVED_已批准",
        "05_REJECTED_已驳回",
        "06_COMMITTED_已生效",
        "99_ARCHIVE_历史归档"
    ]

    LEGACY_SUBDIRS = [
        "00_INBOX",
        "01_DRAFT",
        "02_SUBMITTED",
        "03_REVIEW",
        "04_APPROVED",
        "05_REJECTED",
        "06_COMMITTED",
        "99_ARCHIVE"
    ]

    def __init__(self, workspace_root: Optional[Path] = None, vault_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path("D:/Ai work/novel")
        self.vault_root = vault_root or (self.workspace_root / "NOVEL_OS_VAULT")
        
        # Check if Chinese-English folder exists or default
        if (self.vault_root / "16_PROPOSALS").exists() and not (self.vault_root / "16_PROPOSALS_人类提案").exists():
            self.proposals_dir = self.vault_root / "16_PROPOSALS_人类提案"
        else:
            self.proposals_dir = self.vault_root / "16_PROPOSALS_人类提案"
        
        self.permission_gate = ProposalPermissionGate(self.workspace_root / "00_SYSTEM" / "PERMISSION_MATRIX.yaml")
        self.risk_gate = ProposalRiskGate(self.workspace_root / "00_SYSTEM" / "RISK_GATE.yaml")
        self.conflict_detector = ProposalConflictDetector(self.workspace_root)
        self.audit_logger = ProposalAuditLogger(self.workspace_root / "04_STATE" / "PROPOSAL_AUDIT")
        self.committer = ProposalCommitGate(self.workspace_root, self.audit_logger)
        
        self._ensure_proposal_directories()

    def _ensure_proposal_directories(self):
        for sub in self.SUBDIRS:
            (self.proposals_dir / sub).mkdir(parents=True, exist_ok=True)
            
        readme_path = self.proposals_dir / "README.md"
        if not readme_path.exists():
            readme_path.write_text(
                "---\ntitle: NOVEL OS V2.3 — Human Proposal Workspace\ncategory: 16_PROPOSALS\nsource: NOVEL_OS_PROPOSAL\nauthority: HUMAN_PROPOSAL\nsync_mode: PROPOSAL_ONLY\neditable_in_obsidian: true\n---\n\n"
                "# NOVEL OS V2.3 — Human Proposal Workspace\n\n"
                "This directory is dedicated to Human Proposal submission and review.\n"
                "Proposals stored here are **PROPOSALS ONLY (PROPOSAL != FACT)**.\n"
                "They become canonical truth ONLY after formal Human Gate Approval and NOVEL OS Commit.\n",
                encoding="utf-8"
            )

    def _get_status_subdir(self, status: ProposalLifecycleStatus) -> str:
        mapping = {
            ProposalLifecycleStatus.DRAFT: "01_DRAFT_草稿",
            ProposalLifecycleStatus.SUBMITTED: "02_SUBMITTED_已提交",
            ProposalLifecycleStatus.VALIDATING: "02_SUBMITTED_已提交",
            ProposalLifecycleStatus.VALIDATED: "03_REVIEW_待评审",
            ProposalLifecycleStatus.HUMAN_REVIEW: "03_REVIEW_待评审",
            ProposalLifecycleStatus.APPROVED: "04_APPROVED_已批准",
            ProposalLifecycleStatus.COMMITTING: "04_APPROVED_已批准",
            ProposalLifecycleStatus.COMMITTED: "06_COMMITTED_已生效",
            ProposalLifecycleStatus.REJECTED: "05_REJECTED_已驳回",
            ProposalLifecycleStatus.CONFLICT: "05_REJECTED_已驳回",
            ProposalLifecycleStatus.BLOCKED: "05_REJECTED_已驳回",
            ProposalLifecycleStatus.EXPIRED: "99_ARCHIVE_历史归档",
            ProposalLifecycleStatus.CANCELLED: "99_ARCHIVE_历史归档",
        }
        return mapping.get(status, "00_INBOX_收件箱")

    def save_proposal(self, proposal: Proposal) -> Path:
        """Saves proposal markdown in the appropriate status subfolder, removing older copies."""
        target_subdir = self._get_status_subdir(proposal.lifecycle_status)
        target_folder = self.proposals_dir / target_subdir
        target_folder.mkdir(parents=True, exist_ok=True)
        
        filename = f"{proposal.proposal_id}.md"
        target_file = target_folder / filename
        
        # Remove from other folders if status moved
        for sub in self.SUBDIRS + self.LEGACY_SUBDIRS:
            other_p = self.proposals_dir / sub / filename
            if other_p.exists() and other_p != target_file:
                other_p.unlink()

        content = ProposalParser.serialize_to_markdown(proposal)
        target_file.write_text(content, encoding="utf-8")
        return target_file

    def load_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Finds and loads a proposal from any subfolder."""
        filename = f"{proposal_id}.md"
        for sub in self.SUBDIRS + self.LEGACY_SUBDIRS:
            p_file = self.proposals_dir / sub / filename
            if p_file.exists():
                txt = p_file.read_text(encoding="utf-8")
                return ProposalParser.parse_from_markdown(txt)
        return None


    def create_proposal(
        self,
        proposal_type: ProposalType,
        target_id: str,
        target_type: str,
        proposed_change: str,
        reason: str,
        created_by: str = "HUMAN_AUTHOR",
        source_reference: str = "",
        affected_entities: Optional[List[str]] = None,
        affected_chapters: Optional[List[int]] = None,
        affected_hooks: Optional[List[str]] = None,
        custom_proposal_id: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Proposal]]:
        """Creates a new proposal in DRAFT state."""
        # Check create permission
        dummy = Proposal(
            proposal_id="tmp",
            proposal_type=proposal_type,
            target_id=target_id,
            target_type=target_type,
            proposed_change=proposed_change,
            reason=reason,
            created_by=created_by
        )
        perm_ok, perm_msg = self.permission_gate.check_permission("CREATE", created_by, dummy)
        if not perm_ok:
            return False, f"Permission Denied: {perm_msg}", None

        # Compute authority base hash
        authority_hash = ""
        if source_reference:
            src_file = self.workspace_root / source_reference
            if src_file.exists():
                authority_hash = hashlib.sha256(src_file.read_bytes()).hexdigest()

        # Generate proposal ID
        if custom_proposal_id:
            pid = custom_proposal_id
        else:
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            pid = f"PROP-{ts}-{proposal_type.value}"

        proposal = Proposal(
            proposal_id=pid,
            proposal_type=proposal_type,
            target_id=target_id,
            target_type=target_type,
            proposed_change=proposed_change,
            reason=reason,
            created_by=created_by,
            source_reference=source_reference,
            current_authority_hash=authority_hash,
            affected_entities=affected_entities or [],
            affected_chapters=affected_chapters or [],
            affected_hooks=affected_hooks or [],
            lifecycle_status=ProposalLifecycleStatus.DRAFT
        )

        # Assess initial risk
        risk_lvl, risk_score, hard_trig = self.risk_gate.assess_risk(proposal)
        proposal.risk_level = risk_lvl
        proposal.risk_score = risk_score
        proposal.hard_trigger = hard_trig

        # Attach provenance
        ProposalProvenanceTracker.attach_provenance(proposal, "PROPOSAL_CREATED", created_by, reason)

        # Save to disk
        self.save_proposal(proposal)

        # Log audit
        self.audit_logger.log_event(
            proposal_id=proposal.proposal_id,
            event="PROPOSAL_CREATED",
            actor=created_by,
            previous_status="NONE",
            new_status="DRAFT",
            reason=reason,
            source_hash=authority_hash,
            metadata={"target_id": target_id, "risk_level": risk_lvl.value}
        )

        return True, f"Proposal {pid} created successfully in DRAFT status.", proposal

    def submit_proposal(self, proposal_id: str, actor: str) -> Tuple[bool, str, Optional[Proposal]]:
        """Submits a draft proposal and executes validation & conflict detection."""
        proposal = self.load_proposal(proposal_id)
        if not proposal:
            return False, f"Proposal '{proposal_id}' not found.", None

        # Permission check
        perm_ok, perm_msg = self.permission_gate.check_permission("SUBMIT", actor, proposal)
        if not perm_ok:
            return False, f"Permission Denied: {perm_msg}", proposal

        # State transition: DRAFT -> SUBMITTED
        ok, msg = ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.SUBMITTED)
        if not ok:
            return False, msg, proposal

        ProposalProvenanceTracker.attach_provenance(proposal, "PROPOSAL_SUBMITTED", actor)
        self.audit_logger.log_event(proposal.proposal_id, "PROPOSAL_SUBMITTED", actor, "DRAFT", "SUBMITTED")

        # Transition: SUBMITTED -> VALIDATING
        ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.VALIDATING)

        # 1. Conflict & Boundary Detection
        val_status, conf_status, details = self.conflict_detector.validate_proposal(proposal)
        proposal.validation_status = val_status
        proposal.conflict_status = conf_status
        proposal.validation_details = details
        proposal.conflict_details = details

        # 2. Risk Re-assessment
        risk_lvl, risk_score, hard_trig = self.risk_gate.assess_risk(proposal)
        proposal.risk_level = risk_lvl
        proposal.risk_score = risk_score
        proposal.hard_trigger = hard_trig

        # If conflicts or boundary violations exist, transition to CONFLICT or BLOCKED
        if val_status == ValidationStatus.STALE:
            proposal.lifecycle_status = ProposalLifecycleStatus.CONFLICT
            self.save_proposal(proposal)
            self.audit_logger.log_event(proposal.proposal_id, "VALIDATION_STALE", actor, "VALIDATING", "CONFLICT", details)
            return False, f"Submission Rejected: {details}", proposal

        if conf_status == ConflictStatus.HARD_CONFLICT or val_status == ValidationStatus.BOUNDARY_VIOLATION or val_status == ValidationStatus.INVALID:
            proposal.lifecycle_status = ProposalLifecycleStatus.CONFLICT
            self.save_proposal(proposal)
            self.audit_logger.log_event(proposal.proposal_id, "VALIDATION_CONFLICT", actor, "VALIDATING", "CONFLICT", details)
            return False, f"Submission Blocked by Conflict Gate: {details}", proposal

        # Successful validation -> Transition to VALIDATED -> HUMAN_REVIEW
        ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.VALIDATED)
        ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.HUMAN_REVIEW)

        ProposalProvenanceTracker.attach_provenance(proposal, "VALIDATION_PASSED", "SYSTEM", details)
        self.save_proposal(proposal)

        self.audit_logger.log_event(
            proposal.proposal_id,
            "PROPOSAL_AWAITING_HUMAN_REVIEW",
            "SYSTEM",
            "VALIDATING",
            "HUMAN_REVIEW",
            details,
            metadata={"risk_level": risk_lvl.value, "risk_score": risk_score}
        )

        return True, f"Proposal {proposal.proposal_id} validated successfully. Status: HUMAN_REVIEW.", proposal

    def human_decide(
        self,
        proposal_id: str,
        decision: str,
        actor: str,
        reason: str = ""
    ) -> Tuple[bool, str, Optional[Proposal]]:
        """Human Gate decision handler: APPROVE / REJECT / REQUEST_REVISION."""
        proposal = self.load_proposal(proposal_id)
        if not proposal:
            return False, f"Proposal '{proposal_id}' not found.", None

        dec = decision.upper()

        if dec == "APPROVE":
            perm_ok, perm_msg = self.permission_gate.check_permission("APPROVE", actor, proposal)
            if not perm_ok:
                return False, f"Approval Denied: {perm_msg}", proposal

            ok, msg = ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.APPROVED)
            if not ok:
                return False, msg, proposal

            proposal.approved_by = actor
            proposal.approved_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            ProposalProvenanceTracker.attach_provenance(proposal, "PROPOSAL_APPROVED", actor, reason)
            self.save_proposal(proposal)

            self.audit_logger.log_event(
                proposal.proposal_id,
                "PROPOSAL_APPROVED",
                actor,
                "HUMAN_REVIEW",
                "APPROVED",
                reason
            )
            return True, f"Proposal {proposal.proposal_id} approved by {actor}.", proposal

        elif dec == "REJECT":
            perm_ok, perm_msg = self.permission_gate.check_permission("REJECT", actor, proposal)
            if not perm_ok:
                return False, f"Rejection Denied: {perm_msg}", proposal

            ok, msg = ProposalStateMachine.transition(proposal, ProposalLifecycleStatus.REJECTED)
            if not ok:
                return False, msg, proposal

            proposal.rejection_reason = reason or "Rejected by Human Gate."
            ProposalProvenanceTracker.attach_provenance(proposal, "PROPOSAL_REJECTED", actor, reason)
            self.save_proposal(proposal)

            self.audit_logger.log_event(
                proposal.proposal_id,
                "PROPOSAL_REJECTED",
                actor,
                "HUMAN_REVIEW",
                "REJECTED",
                reason
            )
            return True, f"Proposal {proposal.proposal_id} rejected by {actor}.", proposal

        elif dec == "REQUEST_REVISION":
            # Create a new revision proposal in DRAFT status, keep original in REJECTED / ARCHIVE
            new_pid = f"{proposal.proposal_id}-R{datetime.datetime.now().strftime('%M%S')}"
            rev_proposal = ProposalStateMachine.create_revision(proposal, new_pid, actor)
            
            # Transition old proposal to REJECTED with note
            proposal.lifecycle_status = ProposalLifecycleStatus.REJECTED
            proposal.rejection_reason = f"Superceded by revision {new_pid}. Feedback: {reason}"
            self.save_proposal(proposal)

            # Save new revision
            self.save_proposal(rev_proposal)

            self.audit_logger.log_event(
                proposal.proposal_id,
                "REVISION_REQUESTED",
                actor,
                "HUMAN_REVIEW",
                "REJECTED",
                reason,
                metadata={"new_revision_id": new_pid}
            )

            return True, f"Revision requested. New draft proposal created: {new_pid}.", rev_proposal

        return False, f"Invalid decision '{decision}'. Expected APPROVE, REJECT, or REQUEST_REVISION.", proposal

    def commit_proposal(
        self,
        proposal_id: str,
        actor: str,
        dry_run: bool = False,
        target_override_root: Optional[Path] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """Commits an approved proposal."""
        proposal = self.load_proposal(proposal_id)
        if not proposal:
            return False, f"Proposal '{proposal_id}' not found.", None

        ok, msg, commit_id = self.committer.commit(
            proposal=proposal,
            actor=actor,
            dry_run=dry_run,
            target_override_root=target_override_root
        )

        if ok and not dry_run:
            self.save_proposal(proposal)

        return ok, msg, commit_id

    def list_proposals(self, status: Optional[ProposalLifecycleStatus] = None) -> List[Proposal]:
        """Lists all proposals stored in vault."""
        proposals = []
        for sub in ["00_INBOX", "01_DRAFT", "02_SUBMITTED", "03_REVIEW", "04_APPROVED", "05_REJECTED", "06_COMMITTED", "99_ARCHIVE"]:
            for p_file in (self.proposals_dir / sub).glob("*.md"):
                if p_file.name == "README.md":
                    continue
                try:
                    txt = p_file.read_text(encoding="utf-8")
                    p = ProposalParser.parse_from_markdown(txt)
                    if status is None or p.lifecycle_status == status:
                        proposals.append(p)
                except Exception:
                    pass
        return proposals
