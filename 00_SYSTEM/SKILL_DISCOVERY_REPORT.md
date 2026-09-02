# NOVEL OS V2.1 — 技能实地调研与发现报告 (SKILL DISCOVERY REPORT)

## 1. 调研背景与发现概况
通过对 `D:\Ai work\novel\skills\`、`D:\Ai work\novel\.agents\skills\` 以及已有 Python 执行引擎的全面扫描与代码分析，已准确定位项目中 4 大核心技能体系的物理路径、输入输出协议与行为特征。

---

## 2. 四大技能详细审计清单

### 2.1 Worker A: OH-STORY (商业与创意顾问)
- **实际文件路径**：`skills/story`（主入口）及子技能族（`skills/story-long-analyze`, `skills/story-long-scan`, `skills/story-setup`, `skills/story-cover`, `skills/story-import`）。
- **技能定位与用途**：网文市场趋势扫描、爆款拆书分析、黄金三章钩子设计、情绪节拍把控、商业包装与封面建议。
- **当前输入格式**：自然语言提示词、书名、题材标签或外部参考文本。
- **当前输出格式**：Markdown 格式的拆书分析报告、扫榜趋势清单、包装建议与钩子方案。
- **是否读取 Canon**：是（只读读取世界观与主线设定以提供针对性建议）。
- **是否写入 Canon**：否（当前不直接修改设定集）。
- **是否写入 State**：否（不维护全局状态机）。
- **是否写入正文**：在 legacy 模式下有辅助写短篇/长篇入口，但在 V2.1 架构下必须严格剥离。
- **是否执行 QA**：具备子技能 `story-review` 进行对抗式多视角审阅。
- **是否调用其他 Agent**：Legacy `story` 主入口具备自动路由子技能逻辑（如调用 `story-setup`, `story-long-write`）。
- **是否包含路由逻辑**：是（Legacy 包含自主分流逻辑）。
- **是否存在隐式状态变更**：Legacy `story-setup` 会尝试在项目根目录下生成脚手架配置。
- **是否与 V2.1 权威法则冲突**：**存在潜在冲突**。Legacy `story` 试图作为顶级调度总控（Orchestrator），这违反了“Orchestrator 唯一拥有路由权”的法则。
- **所需适配器策略 (Adapter Strategy)**：
  - 将 `OH-STORY` 降级封装为纯粹的 **Worker A (CREATIVE / COMMERCIAL STORY CONSULTANT)**；
  - 拦截其自带的路由分流逻辑，统一由 Master Orchestrator 发起调度；
  - 其产出全部标记为 `ADVISORY`（咨询参考件），严禁对 Canon 和 State 产生直接写入效应。

---

### 2.2 Worker B: WEBNOVEL-WRITER (网文生产主干)
- **实际文件路径**：`skills/webnovel-write` 及支撑套件（`skills/webnovel-plan`, `skills/webnovel-review`, `skills/webnovel-query`, `skills/webnovel-doctor`）。
- **技能定位与用途**：全流程正文生产，涵盖分卷/章纲规划、上下文检索、起草正文、执行门禁、提交入库与备份。
- **当前输入格式**：结构化状态（`.webnovel/state.json`）、上下文数据包（`Context Contract v2`）、章节大纲目标。
- **当前输出格式**：章节正文草稿（`DRAFT`）、审查报告（`CANON_QA`）、状态更新提案。
- **是否读取 Canon**：是（深度读取设定集、力量体系、角色卡、主线大纲）。
- **是否写入 Canon**：Legacy `webnovel-plan` 具备向设定集回写新增设定的逻辑。
- **是否写入 State**：Legacy `webnovel-write` / `postcommit.py` 具备直接修改 `.webnovel/state.json` 和 SQLite 数据库的能力。
- **是否写入正文**：是（起草生成章节正文 Markdown）。
- **是否执行 QA**：是（深度集成 `webnovel-review`、`precommit` 门禁与字数校验）。
- **是否调用其他 Agent**：Legacy 中会调用审阅 agent 与写门禁脚本。
- **是否包含路由逻辑**：Legacy 流程中硬编码了从 context -> draft -> review -> polish -> commit 的单体管道。
- **是否存在隐式状态变更**：是（提交成功后直接更新本地状态文件与数据库）。
- **是否与 V2.1 权威法则冲突**：**存在核心冲突**。V2.1 要求“Worker 只能提议状态/设定变更（Proposed Deltas），不能单方面提交全局状态与 Canon”。
- **所需适配器策略 (Adapter Strategy)**：
  - 封装为 **Worker B (CANON-AWARE PRODUCTION WORKER)**；
  - 劫持其直接提交状态与修改 Canon 的行为，将其重定向为输出 `proposed_state_changes` 与 `proposed_canon_changes`（标记为 `AUTHORITATIVE-CANDIDATE`）；
  - 由 Master Orchestrator 经校验后通过原子事务统一提交。

---

### 2.3 Worker C: DE-AI WRITING COACH (写前文风协议)
- **实际文件路径**：`skills/de-AI-writing` 与 `skills/good-writing`（以及 `skills/fanqie-novel-skill` 中的文风约束）。
- **技能定位与用途**：写前提示词与文风协议生成，提供“Show, don't tell”、感官细节增强、长短句交错手写体规范、消除 AI 空洞用词。
- **当前输入格式**：当前场景上下文、章节写作目标、人物情绪意图。
- **当前输出格式**：`STYLE_PROTOCOL`（写前文风协议与表现力指导规范）。
- **是否读取 Canon**：有限读取（只读读取当前场景人物性格与场景基调）。
- **是否写入 Canon**：否。
- **是否写入 State**：否。
- **是否写入正文**：否（仅在写前提供协议与提示词赋能，不直接生成剧情正文）。
- **是否执行 QA**：否。
- **是否调用其他 Agent**：否。
- **是否包含路由逻辑**：否。
- **是否存在隐式状态变更**：否。
- **是否与 V2.1 权威法则冲突**：无冲突，天然契合 V2.1 阶段划分。
- **所需适配器策略 (Adapter Strategy)**：
  - 封装为 **Worker C (PREWRITE / STYLE PROTOCOL WORKER)**；
  - 统一输入 `WORKER_REQUEST`，输出标准 `STYLE_PROTOCOL` 产物；
  - 产物归类为 `ADVISORY`，直接注入 Worker B 的起草上下文。

---

### 2.4 Worker D: LIEFLAT (终审语言润色)
- **实际文件路径**：`skills/lieflat-less-ai-tone`（基于 283 万字真实语料库白名单）。
- **技能定位与用途**：正文终审语言清洗，消除机械排比与 AI 高频词，按白名单规则严格保留原文框架与情节事实。
- **当前输入格式**：初稿正文（`DRAFT` 纯文本）。
- **当前输出格式**：润色后文本（`TONE_EDIT` 纯文本）。
- **是否读取 Canon**：否（只针对文本表层语言进行模式匹配与替换）。
- **是否写入 Canon**：否。
- **是否写入 State**：否。
- **是否写入正文**：是（输出润色后的正文字符串）。
- **是否执行 QA**：具备白名单命中复查清单。
- **是否调用其他 Agent**：否。
- **是否包含路由逻辑**：否。
- **是否存在隐式状态变更**：否。
- **是否与 V2.1 权威法则冲突**：无原则冲突，但必须补充 V2.1 `DIFF INTEGRITY GATE` 保护。
- **所需适配器策略 (Adapter Strategy)**：
  - 封装为 **Worker D (FINAL PROSE TONE EDITOR)**；
  - 在接收其 `TONE_EDIT` 输出后，强制接入 `DIFF INTEGRITY GATE`；
  - 一旦发现剧情篡改、关键实体丢失、数字被改动或段落缺失，立即执行 `FAIL -> ROLLBACK TO DRAFT`。

---

## 3. 技能发现与适配总结表

| Worker 代号 | 概念角色 | 实际物理路径 | 输出类型 | 状态写入权 | Canon 写入权 | 路由权 | 适配状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Worker A** | `OH-STORY` | `skills/story` 等 | `ADVISORY` | ❌ 禁止 | ❌ 禁止 | ❌ 剥离 | **READY** |
| **Worker B** | `WEBNOVEL-WRITER` | `skills/webnovel-write` 等 | `PRODUCTION-ARTIFACT` / `AUTHORITATIVE-CANDIDATE` | ❌ 拦截转提案 | ❌ 拦截转提案 | ❌ 剥离 | **READY** |
| **Worker C** | `DE-AI` | `skills/de-AI-writing` 等 | `ADVISORY` | ❌ 禁止 | ❌ 禁止 | ❌ 无 | **READY** |
| **Worker D** | `LIEFLAT` | `skills/lieflat-less-ai-tone` | `PRODUCTION-ARTIFACT` | ❌ 禁止 | ❌ 禁止 | ❌ 无 | **READY** |
