# NOVEL OS V2.1 — 番茄平台适配器架构规范 (FANQIE PLATFORM ADAPTER SPEC)

## 1. 架构总则 (Core Architecture Principle)

1. **唯一设定源与唯一主母本**：
   ```text
   ONE CANON (唯一设定源) ──> ONE MASTER STORY (唯一主母本正文) ──> PLATFORM LAYER (平台适配层)
   ```
2. **非第五核心写作脑**：`fanqie-novel-skill` 不参与主生产线四核心 Worker（OH-Story, Webnovel-Writer, De-AI, Lieflat）的内部正文起草流程，定位为独立运行于 `PLATFORM LAYER` 的 **受控平台适配器（FanqiePlatformAdapter）**。
3. **平台规则 ≠ 小说设定**：番茄平台的商业审查、签约机制与排版规则属于外部平台知识（Platform Knowledge），严禁反向污染 `01_CANON/` 与 `story_bible.md`。

---

## 2. 职责范围 (Responsibilities)

### 2.1 平台物料包装 (PLATFORM PACKAGING)
- **书名与章节名提案**：生成符合番茄高点击率公式的主书名、副标题及章名（`FANQIE_TITLE_PROPOSAL`）。
- **三段式简介**：生成包含人设标签、核心金手指与极致冲突的番茄简介（`FANQIE_SYNOPSIS`）。
- **分类与标签推荐**：匹配番茄官方题材画像（都市/修仙/无敌/杀伐果断）（`FANQIE_TAG_PACKAGE`）。
- **首发与签约包**：整理前 3-5 章首发上架包与签约申请物料（`FANQIE_SUBMISSION_PACKAGE`）。

### 2.2 平台合规门禁 (PLATFORM COMPLIANCE)
- **红线与政策审查**：审查涉政、涉黄、恶意抹黑官方机关等平台违规项。
- **排版呈现规范**：单章 2000-2500 字、段落紧凑、少用破折号（`FANQIE_FORMATTING_SPEC`）。
- **商业结构校验**：对话占比监控（<40%）、黄金前三章生死线留存率、章末断章钩子强度。

### 2.3 商业留存优化 (PLATFORM MARKETING)
- 付费节点与签约里程碑（2万/5万/8万字）指标追踪。

---

## 3. 绝对禁区 (Absolute Prohibitions)

Fanqie 适配器 **绝对严禁** 执行以下操作：
1. **修改 Canon 设定**：严禁篡改主角境界、功法、人物性格、战力体系或核心设定。
2. **修改大纲与状态**：严禁修改 `02_OUTLINE/`、主线总纲或推进 `04_STATE/`。
3. **篡改小说正文**：严禁私自删改正文剧情，严禁因平台迎合而私自“话疗”反派或推翻历史事实。
4. **自发跨 Agent 调度**：严禁自发调用其他 Worker。
5. **账号与网络自动化**：无自主登录、上传或外部网络操作权限。

> **平台冲突升级机制**：若平台合规要求与小说母本剧情发生冲突（如某些平台敏感词触发），**严禁私自修改正文**，必须生成 `FANQIE_ADAPTATION_PROPOSAL` 并标记为 `PENDING_HUMAN`，等待 Human 裁决。

---

## 4. 权限与命名空间模型 (Permission & Namespace Model)

### 4.1 显式权限定义
- **读取权限 (Read Permissions)**：
  - `canon`: `READ_ONLY`
  - `outline`: `READ_ONLY`
  - `state`: `READ_ONLY`
  - `final_prose`: `READ_ONLY`
  - `marketing_data`: `READ_ONLY`
- **写入权限 (Write Permissions)**：
  - `canon`: `FORBIDDEN`
  - `outline`: `FORBIDDEN`
  - `state`: `FORBIDDEN`
  - `story_prose`: `FORBIDDEN`
- **提案权限 (Proposal Permissions)**：
  - `platform_adaptation`: `PROPOSAL_ONLY` (需 Human 审批)
- **路由权限 (Routing)**：
  - `can_route`: `FORBIDDEN`

### 4.2 专属物理命名空间
Fanqie 适配器仅允许向以下目录写入物料：
- `05_MARKETING/fanqie/`
- `03_PRODUCTION/FINAL/platform_packages/fanqie/`
- `00_SYSTEM/` (仅限平台合规报告)

---

## 5. 标准物料类型 (Standard Artifact Types)

所有产出物料必须具备以下标准类型标识之一：
1. `FANQIE_TITLE_PROPOSAL`
2. `FANQIE_SYNOPSIS`
3. `FANQIE_TAG_PACKAGE`
4. `FANQIE_CATEGORY_PROPOSAL`
5. `FANQIE_MARKETING_PACKAGE`
6. `FANQIE_COMPLIANCE_REPORT`
7. `FANQIE_SUBMISSION_PACKAGE`
8. `FANQIE_FORMATTING_SPEC`
9. `FANQIE_ADAPTATION_PROPOSAL`

每个物料均包含：`artifact_id`, `project_id`, `platform: fanqie`, `source_canon_version`, `approval_status` (DRAFT / ADVISORY / PENDING_HUMAN / APPROVED / REJECTED)。
