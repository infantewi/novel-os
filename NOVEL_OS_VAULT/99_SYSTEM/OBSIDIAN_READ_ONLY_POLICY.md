---
source: NOVEL_OS
authority: NOVEL_OS
sync_mode: READ_ONLY
editable_in_obsidian: false
generated_at: "2026-09-02T18:37:13"
canon_version: "2.1.0"
state_version: "2.1.0"
memory_version: "2.2.0"
title: "OBSIDIAN_READ_ONLY_POLICY"
category: "99_SYSTEM"
---

# NOVEL OS V2.3 — OBSIDIAN READ-ONLY POLICY & BOUNDARY CONTRACT

## 1. 核心定位 (System Authority)
Obsidian 在 NOVEL OS 体系中被严格定义为：
> **HUMAN KNOWLEDGE WORKSPACE / VISUAL REVIEW LAYER** (人类创作者知识工作区与视觉审阅层)

它 **不是**：
- Canon Authority (设定权威)
- Memory Authority (记忆权威)
- State Authority (状态权威)
- AI Brain (AI大脑)
- Writer Worker (写作执行器)
- QA Engine (质量判定引擎)

---

## 2. 真实权威法则 (True Authority Hierarchy)
```text
HUMAN
  >
CANON
  >
CONTINUITY
  >
STATE
  >
OUTLINE
  >
PLOT
  >
STYLE
  >
TONE
```

---

## 3. 单向只读数据流向 (Strict Downstream Mirror)
```text
NOVEL OS (Authority)
       ↓ (Exporter Sync)
Obsidian Novel Vault (Read-Only Mirror)
```

**绝对禁止**：
- 从 Obsidian 到 NOVEL OS 的反向直接写入。
- 在 Obsidian 中直接修改 Canon、State、Memory 或 Outline 并期望系统静默同步。
- 安装第二套独立的 AI Memory / RAG 插件（如 Khoj、Smart Connections、Copilot 等），避免多头检索与记忆污染。

---

## 4. 变更提议协议 (Human Gate Proposal Protocol)
任何在 Obsidian 中产生的修改意图必须遵循：
1. 人类在 Obsidian 中提出修改意见 / 提议草稿。
2. 经由 Human 明确授权进入 NOVEL OS 审核管道。
3. 经由 Memory Governor / Canon QA 验证无冲突后，由 NOVEL OS 官方工具链写回源文件。
4. 重新触发 Exporter 同步至 Obsidian 镜像。
