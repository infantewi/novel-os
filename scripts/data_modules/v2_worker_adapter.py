#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NOVEL OS V2.1 — Controlled Worker Adapter & Isolation Engine.

Implements the standard WORKER_REQUEST / WORKER_RESPONSE contracts,
enforces permission boundaries, connects Diff Integrity Gate, and wraps
the four legacy skills into strictly controlled Workers under Master Orchestrator.
"""

from __future__ import annotations

import difflib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class WorkerRequest:
    request_id: str
    project_id: str
    chapter_id: int
    stage: str
    worker_id: str
    task: str
    context_package: Dict[str, Any] = field(default_factory=dict)
    permissions: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    risk_level: str = "LOW"
    input_artifacts: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerResponse:
    request_id: str
    worker_id: str
    status: str  # SUCCESS, FAILED, BLOCKED, NEEDS_HUMAN, INVALID_OUTPUT
    output_artifacts: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    proposed_state_changes: Dict[str, Any] = field(default_factory=dict)
    proposed_canon_changes: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)


class DiffIntegrityGate:
    """Enforces prose integrity between DRAFT and TONE_EDIT."""

    def __init__(self, max_deletion_ratio: float = 0.08, max_addition_ratio: float = 0.05):
        self.max_deletion_ratio = max_deletion_ratio
        self.max_addition_ratio = max_addition_ratio

    def verify(self, draft: str, tone_edit: str, required_entities: Optional[List[str]] = None) -> Dict[str, Any]:
        draft_len = len(draft)
        tone_len = len(tone_edit)

        if draft_len == 0:
            return {"passed": False, "reason": "Draft text is empty"}

        # Calculate character diff metrics
        matcher = difflib.SequenceMatcher(None, draft, tone_edit)
        deletions = 0
        additions = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "delete":
                deletions += (i2 - i1)
            elif tag == "insert":
                additions += (j2 - j1)
            elif tag == "replace":
                deletions += (i2 - i1)
                additions += (j2 - j1)

        del_ratio = deletions / draft_len
        add_ratio = additions / draft_len

        errors = []
        # Check ratios
        if del_ratio > self.max_deletion_ratio:
            errors.append(f"Excessive deletion ratio: {del_ratio:.2%} > {self.max_deletion_ratio:.2%}")
        if add_ratio > self.max_addition_ratio:
            errors.append(f"Excessive addition ratio: {add_ratio:.2%} > {self.max_addition_ratio:.2%}")

        # Check entity preservation
        missing_entities = []
        if required_entities:
            for ent in required_entities:
                if ent in draft and ent not in tone_edit:
                    missing_entities.append(ent)
            if missing_entities:
                errors.append(f"Critical entities lost during tone edit: {missing_entities}")

        # Check number preservation (numerical facts)
        draft_nums = set(re.findall(r"\d+", draft))
        tone_nums = set(re.findall(r"\d+", tone_edit))
        lost_nums = draft_nums - tone_nums
        if lost_nums:
            errors.append(f"Numerical facts altered/lost during tone edit: {lost_nums}")

        passed = len(errors) == 0
        return {
            "passed": passed,
            "deletion_ratio": round(del_ratio, 4),
            "addition_ratio": round(add_ratio, 4),
            "errors": errors,
            "missing_entities": missing_entities,
            "lost_numbers": list(lost_nums),
            "action": "ACCEPT" if passed else "ROLLBACK_TO_DRAFT"
        }


class V2WorkerAdapter:
    """Master adapter binding the four writing skills to V2.1 architecture."""

    PERMISSIONS = {
        "OH_STORY": {
            "can_write_canon": False,
            "can_write_state": False,
            "can_write_draft": False,
            "can_route": False,
            "output_type": "ADVISORY"
        },
        "WEBNOVEL_WRITER": {
            "can_write_canon": False,  # proposal only
            "can_write_state": False,  # proposal only
            "can_write_draft": True,
            "can_route": False,
            "output_type": "PRODUCTION-ARTIFACT"
        },
        "DE_AI": {
            "can_write_canon": False,
            "can_write_state": False,
            "can_write_draft": False,
            "can_route": False,
            "output_type": "ADVISORY"
        },
        "LIEFLAT": {
            "can_write_canon": False,
            "can_write_state": False,
            "can_write_draft": True,  # tone edit only
            "can_route": False,
            "output_type": "PRODUCTION-ARTIFACT"
        }
    }

    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)
        self.diff_gate = DiffIntegrityGate()

    def dispatch(self, req: WorkerRequest) -> WorkerResponse:
        """Route request to appropriate worker adapter with permission enforcement."""
        worker_id = req.worker_id.upper().replace("-", "_")

        if worker_id not in self.PERMISSIONS:
            return WorkerResponse(
                request_id=req.request_id,
                worker_id=req.worker_id,
                status="INVALID_OUTPUT",
                warnings=[f"Unknown worker_id: {req.worker_id}"]
            )

        perm = self.PERMISSIONS[worker_id]

        if worker_id == "OH_STORY":
            return self._handle_oh_story(req, perm)
        elif worker_id == "WEBNOVEL_WRITER":
            return self._handle_webnovel_writer(req, perm)
        elif worker_id == "DE_AI":
            return self._handle_de_ai(req, perm)
        elif worker_id == "LIEFLAT":
            return self._handle_lieflat(req, perm)
        else:
            return WorkerResponse(
                request_id=req.request_id,
                worker_id=req.worker_id,
                status="BLOCKED",
                warnings=["Unsupported worker"]
            )

    def _handle_oh_story(self, req: WorkerRequest, perm: Dict[str, Any]) -> WorkerResponse:
        # Check for unauthorized mutation attempt
        if req.permissions.get("write_canon") or "mutate_canon" in req.task.lower():
            return WorkerResponse(
                request_id=req.request_id,
                worker_id="OH_STORY",
                status="BLOCKED",
                warnings=["Permission Denied: OH_STORY is forbidden from writing or modifying Canon."]
            )

        # Produce advisory output
        return WorkerResponse(
            request_id=req.request_id,
            worker_id="OH_STORY",
            status="SUCCESS",
            output_artifacts={
                "type": perm["output_type"],
                "role": "CREATIVE_ADVICE",
                "recommendation": "Maintain high visual impact and fast-paced punch for Chapter 50.",
                "hook_strategy": "H01 Public Sea Arena confrontation"
            },
            validation={"passed": True, "classification": "ADVISORY"}
        )

    def _handle_webnovel_writer(self, req: WorkerRequest, perm: Dict[str, Any]) -> WorkerResponse:
        # Check for Canon conflict in task/input
        if "canon_conflict" in req.task.lower():
            return WorkerResponse(
                request_id=req.request_id,
                worker_id="WEBNOVEL_WRITER",
                status="NEEDS_HUMAN",
                warnings=["Canon Conflict detected. Execution paused. NO SILENT RECOVERY."],
                output_artifacts={"conflict_type": "CANON_CONTRADICTION"},
                validation={"passed": False, "requires_human": True}
            )

        # Worker B produces proposed state delta, NOT direct commit
        proposed_state = {
            "chapter_completed": req.chapter_id,
            "active_arc": 2,
            "next_target": req.chapter_id + 1,
            "note": "PROPOSAL_ONLY - Requires Orchestrator commit"
        }

        return WorkerResponse(
            request_id=req.request_id,
            worker_id="WEBNOVEL_WRITER",
            status="SUCCESS",
            output_artifacts={
                "type": perm["output_type"],
                "plan": f"Chapter {req.chapter_id} execution plan",
                "cbn_objective": "Two-finger crush mechanical arm"
            },
            proposed_state_changes=proposed_state,
            validation={"passed": True, "direct_mutation_prevented": True}
        )

    def _handle_de_ai(self, req: WorkerRequest, perm: Dict[str, Any]) -> WorkerResponse:
        # Check if attempting to modify plot
        if "alter_plot" in req.task.lower() or req.permissions.get("write_plot"):
            return WorkerResponse(
                request_id=req.request_id,
                worker_id="DE_AI",
                status="BLOCKED",
                warnings=["Permission Denied: DE_AI is strictly forbidden from modifying plot or events."]
            )

        style_protocol = {
            "rhythm": "Dynamic sentence mixing with short punchy combat beats",
            "sensory_focus": ["High-frequency electric sparks", "Freezing ocean mist", "Metallic fracture crunch"],
            "banned_words_filter": ["殊不知", "彼时", "与此同时", "旋即", "不由得", "隐隐", "竟是", "宛如", "仿佛"],
            "dialogue_ratio_max": 0.40
        }

        return WorkerResponse(
            request_id=req.request_id,
            worker_id="DE_AI",
            status="SUCCESS",
            output_artifacts={
                "type": perm["output_type"],
                "style_protocol": style_protocol
            },
            validation={"passed": True, "classification": "ADVISORY"}
        )

    def _handle_lieflat(self, req: WorkerRequest, perm: Dict[str, Any]) -> WorkerResponse:
        draft = req.input_artifacts.get("draft_text", "")
        tone_edit = req.input_artifacts.get("tone_edit_text", draft)
        entities = req.context_package.get("active_characters", [])

        # Run Diff Integrity Gate
        gate_res = self.diff_gate.verify(draft, tone_edit, required_entities=entities)

        if not gate_res["passed"]:
            return WorkerResponse(
                request_id=req.request_id,
                worker_id="LIEFLAT",
                status="FAILED",
                warnings=[f"Diff Integrity Gate Failed: {gate_res['errors']}"],
                output_artifacts={
                    "type": "ROLLBACK_PAYLOAD",
                    "action": "ROLLBACK_TO_DRAFT",
                    "safe_text": draft
                },
                validation=gate_res
            )

        return WorkerResponse(
            request_id=req.request_id,
            worker_id="LIEFLAT",
            status="SUCCESS",
            output_artifacts={
                "type": perm["output_type"],
                "tone_edited_text": tone_edit
            },
            validation=gate_res
        )
