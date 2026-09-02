---
source: NOVEL_OS
authority: NOVEL_OS
sync_mode: READ_ONLY
editable_in_obsidian: false
generated_at: "2026-09-02T18:37:13"
canon_version: "2.1.0"
state_version: "2.1.0"
memory_version: "2.2.0"
title: "质量评估策略"
category: "15_QA"
source_file: "00_SYSTEM/QA_POLICY.yaml"
---

schema_version: "2.1"

levels:
  LOW:
    description: "基础质量与合规检查"
    checks:
      - Word_Count
      - Entity_Check
      - Required_Event_Check
      - Forbidden_Event_Check
      - Basic_Canon_Check
      - Ending_Hook_Check

  MEDIUM:
    description: "标准连续性与状态跃迁检查"
    extends: "LOW"
    additional_checks:
      - Character_Consistency
      - Timeline_Consistency
      - Relationship_Consistency
      - State_Transition
      - Foreshadowing_Consistency

  HIGH:
    description: "深度因果链、战力平衡与防话疗高危审查"
    extends: "MEDIUM"
    additional_checks:
      - Deep_Character_Integrity
      - Motivation_Integrity
      - OOC_Detection
      - Power_Scaling
      - Ability_Cost
      - Causality_Chain
      - Foreshadowing_Payoff
      - Information_Boundary
      - Timeline_Penetration
      - Major_Event_Integrity
      - Dialogue_Integrity
      - Anti_Talk_No_Jutsu_Audit
