# -*- coding: utf-8 -*-
"""Novel Memory Governor — Master Governance Facade for NOVEL OS V2.2."""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Optional
from .memory_delta import MemoryDelta, MemoryType, KnowledgeStatus
from .policy import MemoryPolicy
from .validator import MemoryValidator
from .conflict_detector import ConflictDetector, ConflictReport
from .permission import MemoryPermissionGate
from .provenance import ProvenanceTracker
from .commit_gate import AtomicCommitGate


class NovelMemoryGovernor:
    """Master governance boundary protecting story truth between Workers and OpenViking."""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.validator = MemoryValidator()
        self.conflict_detector = ConflictDetector()
        self.provenance_tracker = ProvenanceTracker()
        self.commit_gate = AtomicCommitGate(self.project_root / "04_STATE" / "memory_registry.json")

    def process_delta(self, worker_id: str, delta: MemoryDelta, direct_commit: bool = False) -> Dict[str, Any]:
        perm_res = MemoryPermissionGate.check_proposal(worker_id, delta)
        if not perm_res["allowed"]:
            return {"status": "BLOCKED", "reason": perm_res["reason"], "delta_id": delta.delta_id}

        if direct_commit:
            direct_check = MemoryPermissionGate.check_direct_commit(worker_id)
            if not direct_check["allowed"]:
                return {"status": "BLOCKED", "reason": direct_check["reason"], "delta_id": delta.delta_id}

        val_res = self.validator.validate(delta)
        if not val_res["passed"]:
            return {"status": "VALIDATION_FAILED", "errors": val_res["errors"], "delta_id": delta.delta_id}

        conflict_res = self.conflict_detector.inspect(delta)
        if conflict_res.has_conflict:
            return {
                "status": "NEEDS_HUMAN",
                "conflict": conflict_res,
                "delta_id": delta.delta_id,
                "message": f"Conflict detected: {conflict_res.description}. STOP -> REPORT -> PROPOSE OPTIONS -> WAIT FOR HUMAN."
            }

        policy_res = MemoryPolicy.evaluate_impact(delta)
        if policy_res["requires_human"]:
            return {
                "status": "NEEDS_HUMAN",
                "policy_reasons": policy_res["reasons"],
                "delta_id": delta.delta_id,
                "message": "High-impact memory delta requires explicit Human approval."
            }

        self.provenance_tracker.seal_provenance(delta, author=worker_id)

        return {
            "status": "ACCEPTED",
            "delta_id": delta.delta_id,
            "delta": delta,
            "message": "Memory Delta validated and approved for OpenViking ingestion."
        }
