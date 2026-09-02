# -*- coding: utf-8 -*-
"""Zero-Trust Memory Permission Gate for NOVEL OS V2.2."""

from __future__ import annotations
from typing import Dict, Any, List
from .memory_delta import MemoryDelta


class MemoryPermissionGate:
    """Enforces zero-trust memory permissions across all Workers and Adapters."""

    ALLOWED_WORKERS = {
        "MASTER_ORCHESTRATOR": {"can_propose": True, "can_direct_commit": True, "can_override": True},
        "OH_STORY": {"can_propose": True, "can_direct_commit": False, "can_override": False},
        "WEBNOVEL_WRITER": {"can_propose": True, "can_direct_commit": False, "can_override": False},
        "DE_AI": {"can_propose": False, "can_direct_commit": False, "can_override": False},
        "LIEFLAT": {"can_propose": False, "can_direct_commit": False, "can_override": False},
        "FANQIE_PLATFORM_ADAPTER": {"can_propose": True, "can_direct_commit": False, "can_override": False},
    }

    @classmethod
    def check_proposal(cls, worker_id: str, delta: MemoryDelta) -> Dict[str, Any]:
        wid = worker_id.upper().replace("-", "_")
        perm = cls.ALLOWED_WORKERS.get(wid, {"can_propose": False, "can_direct_commit": False})

        if not perm["can_propose"]:
            return {
                "allowed": False,
                "reason": f"Permission Denied: Worker '{worker_id}' is forbidden from proposing memory deltas."
            }
        return {"allowed": True, "reason": "Proposal permitted."}

    @classmethod
    def check_direct_commit(cls, worker_id: str) -> Dict[str, Any]:
        wid = worker_id.upper().replace("-", "_")
        perm = cls.ALLOWED_WORKERS.get(wid, {"can_direct_commit": False})

        if not perm["can_direct_commit"]:
            return {
                "allowed": False,
                "reason": f"Permission Denied: Worker '{worker_id}' is strictly FORBIDDEN from direct memory commits."
            }
        return {"allowed": True, "reason": "Direct commit authorized for Orchestrator."}
