---
source: NOVEL_OS
authority: NOVEL_OS
sync_mode: READ_ONLY
editable_in_obsidian: false
generated_at: "2026-09-02T21:29:10"
canon_version: "2.1.0"
state_version: "2.1.0"
memory_version: "2.2.0"
title: "风险网关规则"
category: "15_QA"
source_file: "00_SYSTEM/RISK_GATE.yaml"
---

schema_version: "2.1"

# Hard Triggers: 命中任意一项直接判定为 HIGH
hard_triggers:
  - climax
  - arc_finale
  - core_character_death
  - major_character_death
  - major_injury
  - major_reversal
  - core_foreshadowing_payoff
  - protagonist_major_power_change
  - system_permission_change
  - major_canon_change
  - timeline_break
  - relationship_break

hard_trigger_level: "HIGH"

# Risk Scores: 积分量化表
risk_scores:
  new_character: 1
  new_location: 1
  new_rule: 2
  relationship_change: 2
  new_ability: 2
  foreshadowing_plant: 1
  foreshadowing_payoff: 3
  timeline_jump: 2
  multiple_pov: 2
  important_information: 2
  combat: 1
  power_scaling_change: 3

# 阈值分级
thresholds:
  low_max: 3      # 0–3 LOW
  medium_max: 7   # 4–7 MEDIUM
  high_min: 8     # 8+  HIGH
