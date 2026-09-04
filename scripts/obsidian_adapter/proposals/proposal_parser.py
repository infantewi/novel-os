# -*- coding: utf-8 -*-
"""Proposal Markdown Parser and Serializer for NOVEL OS V2.3."""

from __future__ import annotations
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple
from .proposal_schema import (
    Proposal,
    ProposalType,
    ProposalLifecycleStatus,
    RiskLevel,
    ValidationStatus,
    ConflictStatus,
)


class ProposalParser:
    """Serializes Proposal to Markdown and parses Markdown back to Proposal."""

    @classmethod
    def serialize_to_markdown(cls, proposal: Proposal) -> str:
        data = proposal.to_dict()
        
        # Build Frontmatter
        fm_dict = {
            "proposal_id": data["proposal_id"],
            "proposal_type": data["proposal_type"],
            "schema_version": data["schema_version"],
            "source": "NOVEL_OS_PROPOSAL",
            "authority": "HUMAN_PROPOSAL",
            "sync_mode": "PROPOSAL_ONLY",
            "created_at": data["created_at"],
            "created_by": data["created_by"],
            "workspace": data["workspace"],
            "vault": data["vault"],
            "target_id": data["target_id"],
            "target_type": data["target_type"],
            "source_reference": data["source_reference"],
            "source_version": data["source_version"],
            "current_authority_hash": data["current_authority_hash"],
            "risk_level": data["risk_level"],
            "risk_score": data["risk_score"],
            "hard_trigger": data["hard_trigger"],
            "lifecycle_status": data["lifecycle_status"],
            "validation_status": data["validation_status"],
            "conflict_status": data["conflict_status"],
            "human_review_required": data["human_review_required"],
            "approved_by": data["approved_by"],
            "approved_at": data["approved_at"],
            "commit_status": data["commit_status"],
            "commit_id": data["commit_id"],
            "committed_at": data["committed_at"],
            "rejection_reason": data["rejection_reason"],
            "revision_of": data["revision_of"],
        }
        
        fm_yaml = yaml.dump(fm_dict, allow_unicode=True, sort_keys=False).strip()
        
        body_lines = [
            f"# 提案单：{proposal.proposal_id} ({proposal.proposal_type.value})",
            "",
            "> [!NOTE]",
            "> **提案声明 (PROPOSAL DECLARATION)**：",
            "> 本文件为人类作者/协作者提交的 **修改提案草案 (HUMAN PROPOSAL)**，**不具备设定权威性 (PROPOSAL ≠ FACT)**。",
            "> 必须经过 NOVEL OS 校验网关与 Human Gate 正式批准并 Commit 后，方可沉淀为 Canon 权威事实。",
            "",
            "## 一、提案目标与背景",
            f"- **目标实体 / 范围**: `{proposal.target_id}` ({proposal.target_type})",
            f"- **当前基准版本**: `{proposal.source_version}`",
            f"- **前置基准指纹 (Base Hash)**: `{proposal.current_authority_hash}`",
            f"- **提交人**: `{proposal.created_by}`",
            f"- **提交时间**: `{proposal.created_at}`",
            "",
            "## 二、拟定修改内容 (Proposed Change)",
            "```markdown",
            proposal.proposed_change.strip(),
            "```",
            "",
            "## 三、修改理由与预期影响",
            f"- **修改理由 (Reason)**: {proposal.reason}",
            f"- **预期影响 (Expected Effect)**: {proposal.expected_effect}",
            f"- **受影响实体**: {', '.join(proposal.affected_entities) if proposal.affected_entities else '无'}",
            f"- **受影响章节**: {', '.join(str(c) for c in proposal.affected_chapters) if proposal.affected_chapters else '无'}",
            f"- **受影响伏笔**: {', '.join(proposal.affected_hooks) if proposal.affected_hooks else '无'}",
            "",
            "## 四、安全与风险评估",
            f"- **风险等级**: `{proposal.risk_level.value}` (积分: {proposal.risk_score})",
            f"- **命中硬触发**: `{proposal.hard_trigger or '无'}`",
            f"- **校验状态**: `{proposal.validation_status.value}` ({proposal.validation_details or '未开始'})",
            f"- **冲突检测**: `{proposal.conflict_status.value}` ({proposal.conflict_details or '未检测'})",
            f"- **生命周期状态**: `{proposal.lifecycle_status.value}`",
            "",
            "## 五、审查与签署记录",
            f"- **审批人**: `{proposal.approved_by or '待审批'}`",
            f"- **审批时间**: `{proposal.approved_at or 'N/A'}`",
            f"- **提交状态**: `{proposal.commit_status}` (Commit ID: `{proposal.commit_id or 'N/A'}`)",
            f"- **驳回原因**: `{proposal.rejection_reason or '无'}`",
            f"- **修订前序版本**: `{proposal.revision_of or '无'}`",
        ]
        
        return f"---\n{fm_yaml}\n---\n\n" + "\n".join(body_lines) + "\n"

    @classmethod
    def parse_from_markdown(cls, content: str) -> Proposal:
        if not content.startswith("---"):
            raise ValueError("Invalid proposal markdown: Missing frontmatter header '---'.")
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError("Invalid proposal markdown: Incomplete frontmatter block.")
        
        fm_text = parts[1]
        body_text = parts[2]
        
        meta = yaml.safe_load(fm_text) or {}
        
        if "proposal_id" not in meta:
            raise ValueError("Invalid proposal: 'proposal_id' is missing in frontmatter.")
        if "proposal_type" not in meta:
            raise ValueError("Invalid proposal: 'proposal_type' is missing in frontmatter.")
        
        # Extract proposed_change and reason from body if needed
        proposed_change = ""
        change_match = re.search(r"## 二、拟定修改内容.*?```markdown\s*(.*?)\s*```", body_text, re.DOTALL)
        if change_match:
            proposed_change = change_match.group(1).strip()
            
        reason = ""
        reason_match = re.search(r"- \*\*修改理由 \(Reason\)\*\*:\s*(.*)", body_text)
        if reason_match:
            reason = reason_match.group(1).strip()
            
        expected_effect = ""
        effect_match = re.search(r"- \*\*预期影响 \(Expected Effect\)\*\*:\s*(.*)", body_text)
        if effect_match:
            expected_effect = effect_match.group(1).strip()

        proposal_dict = {
            "proposal_id": meta.get("proposal_id"),
            "proposal_type": meta.get("proposal_type"),
            "target_id": meta.get("target_id", ""),
            "target_type": meta.get("target_type", ""),
            "proposed_change": proposed_change or meta.get("proposed_change", ""),
            "reason": reason or meta.get("reason", ""),
            "created_at": meta.get("created_at", ""),
            "created_by": meta.get("created_by", "HUMAN_AUTHOR"),
            "workspace": meta.get("workspace", "."),
            "vault": meta.get("vault", "NOVEL_OS_VAULT"),
            "source_reference": meta.get("source_reference", ""),
            "source_version": meta.get("source_version", "2.1.0"),
            "current_authority_hash": meta.get("current_authority_hash", ""),
            "expected_effect": expected_effect or meta.get("expected_effect", ""),
            "affected_entities": meta.get("affected_entities", []),
            "affected_chapters": meta.get("affected_chapters", []),
            "affected_hooks": meta.get("affected_hooks", []),
            "risk_level": meta.get("risk_level", "LOW"),
            "risk_score": meta.get("risk_score", 0),
            "hard_trigger": meta.get("hard_trigger", ""),
            "validation_status": meta.get("validation_status", "NOT_STARTED"),
            "validation_details": meta.get("validation_details", ""),
            "conflict_status": meta.get("conflict_status", "NOT_CHECKED"),
            "conflict_details": meta.get("conflict_details", ""),
            "provenance": meta.get("provenance", {}),
            "human_review_required": meta.get("human_review_required", True),
            "lifecycle_status": meta.get("lifecycle_status", "DRAFT"),
            "approved_by": meta.get("approved_by"),
            "approved_at": meta.get("approved_at"),
            "commit_status": meta.get("commit_status", "NOT_COMMITTED"),
            "commit_id": meta.get("commit_id"),
            "committed_at": meta.get("committed_at"),
            "rejection_reason": meta.get("rejection_reason"),
            "revision_of": meta.get("revision_of"),
            "schema_version": meta.get("schema_version", "2.3.0"),
        }
        
        return Proposal.from_dict(proposal_dict)
