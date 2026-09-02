# NOVEL OS V2.1 — 四大技能适配器与受控 Worker 规范 (SKILL ADAPTER SPEC)

## 1. 核心架构原则 (Core Architecture Principles)
1. **最高权威不可动摇**：`HUMAN > CANON > CONTINUITY > STATE > OUTLINE > PLOT > STYLE > TONE`。
2. **总控唯一性**：`Master Orchestrator` 独占路由、阶段跳转、权限校验、门禁裁决与状态提交权；所有 Skill 均为受控 Worker，严禁成为独立总控。
3. **提案与提交分离**：Worker 可以提议（Propose）状态或 Canon 变更，但绝对不能直接提交（Commit）。
4. **零隐式修复 (NO SILENT RECOVERY)**：任何设定、时间线或状态冲突必须立即中止并上报 Human。
5. **差异保真保护 (Diff Integrity Gate)**：语言编辑（Lieflat）受到严格剧情与实体保真约束，违规立即回滚。

---

## 2. 标准 Worker 契约接口 (Standard Worker Interface)

### 2.1 请求协议 (WORKER_REQUEST)
```json
{
  "request_id": "REQ-20260902-CH050-STAGE01",
  "project_id": "都市：仙尊归来，开局截胡天命机缘",
  "chapter_id": 50,
  "stage": "PREWRITE | DRAFT | STYLE | TONE | QA",
  "worker_id": "OH_STORY | WEBNOVEL_WRITER | DE_AI | LIEFLAT",
  "task": "具体的任务指令",
  "context_package": {
    "l0_context": {},
    "l1_canon": {},
    "l2_history": {}
  },
  "permissions": {
    "read_canon": true,
    "write_canon": false,
    "read_state": true,
    "write_state": false,
    "write_draft": true
  },
  "constraints": [
    "禁止修改既有事实",
    "禁止话疗",
    "对话占比 <= 40%"
  ],
  "risk_level": "LOW | MEDIUM | HIGH",
  "input_artifacts": {
    "draft_text": "",
    "style_protocol": ""
  }
}
```

### 2.2 响应协议 (WORKER_RESPONSE)
```json
{
  "request_id": "REQ-20260902-CH050-STAGE01",
  "worker_id": "OH_STORY | WEBNOVEL_WRITER | DE_AI | LIEFLAT",
  "status": "SUCCESS | FAILED | BLOCKED | NEEDS_HUMAN | INVALID_OUTPUT",
  "output_artifacts": {
    "type": "ADVISORY | PRODUCTION-ARTIFACT | AUTHORITATIVE-CANDIDATE",
    "content": {}
  },
  "warnings": [],
  "proposed_state_changes": {},
  "proposed_canon_changes": {},
  "validation": {
    "passed": true,
    "details": {}
  }
}
```

---

## 3. 四大受控 Worker 详细规范

### 3.1 WORKER A — OH-STORY (创意与商业故事顾问)
- **定位**：`CREATIVE / COMMERCIAL STORY CONSULTANT`
- **输入**：L0 上下文、本卷主线目标、商业题材要素。
- **输出**：商业剧情建议、黄金钩子设计、情绪拉扯点方案（类型标记：`ADVISORY`）。
- **权限边界**：
  - **允许**：读取 Canon、读取 Outline、读取 State、读取上下文、提出建议。
  - **严禁**：修改 Canon、修改 State、修改 Outline、宣布 Canon 事实、绕过 Orchestrator。

### 3.2 WORKER B — WEBNOVEL-WRITER (网文生产执行 Worker)
- **定位**：`CANON-AWARE NOVEL PRODUCTION WORKER`
- **输入**：L0/L1 上下文、Style Protocol、本章写作细纲。
- **输出**：本章初稿（`DRAFT`，类型：`PRODUCTION-ARTIFACT`）、状态更新提案（`proposed_state_changes`，类型：`AUTHORITATIVE-CANDIDATE`）。
- **权限边界**：
  - **允许**：读取全部必要上下文、撰写初稿、输出 QA 建议、提出状态变更。
  - **严禁**：单方面篡改 Canon、自行修复设定冲突、直接修改全局 `.webnovel/state.json` 或 SQLite 数据库。

### 3.3 WORKER C — DE-AI WRITING COACH (写前文风协议 Worker)
- **定位**：`PREWRITE / STYLE PROTOCOL WORKER`
- **输入**：本章目标、场景氛围、出场角色情绪意图。
- **输出**：`STYLE_PROTOCOL`（类型：`ADVISORY`），包含感官细节要求、长短句手写体规范、禁词表。
- **权限边界**：
  - **允许**：提供写前语言表现力规范与提示词赋能。
  - **严禁**：修改情节、新增未授权设定角色、修改世界观规则、直接写入正文。

### 3.4 WORKER D — LIEFLAT (终审语言润色 Worker)
- **定位**：`FINAL PROSE TONE EDITOR`
- **输入**：`DRAFT` 初稿正文。
- **输出**：`TONE_EDIT` 润色后正文（类型：`PRODUCTION-ARTIFACT`）。
- **权限边界**：
  - **允许**：依据白名单消除 AI 机械味、修复生硬关联词、优化阅读节奏。
  - **严禁**：增删情节事件、修改人物动机或行为、修改数值与时间线、修改对话含义。
  - **后置强制校验**：由 `DIFF INTEGRITY GATE` 进行全量比对。

---

## 4. 上下文供给分层机制 (Context Resolver: L0 / L1 / L2)

```text
               ┌────────────────────────────────────────────────────────┐
               │                  MASTER ORCHESTRATOR                   │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │                    CONTEXT RESOLVER                    │
               │  ┌──────────────────────────────────────────────────┐  │
               │  │ L0: ALWAYS LOAD (State / Prev Ch / Ch Plan / POV) │  │
               │  ├──────────────────────────────────────────────────┤  │
               │  │ L1: RELEVANT CANON (Active Roles / Power / Rules)│  │
               │  ├──────────────────────────────────────────────────┤  │
               │  │ L2: ON DEMAND (Distant History / Old Hooks)       │  │
               │  └──────────────────────────────────────────────────┘  │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │            CONTROLLED WORKER DISPATCH LAYER            │
               └────────────────────────────────────────────────────────┘
```

- **L0 (强制装载)**：Execution State, 当前地点, POV, 上一章结尾, 本章 CBN 目标, 活跃角色。
- **L1 (按需装载相关设定)**：本章涉及的角色卡、门派谱系、功法等级、紧急伏笔。
- **L2 (冷启动只读查询)**：远期历史章节、归档背景资料。

---

## 5. 差异保真门禁规范 (Diff Integrity Gate)

在 Worker D (`LIEFLAT`) 输出 `TONE_EDIT` 后，执行物理级差异审查：

```text
DRAFT ──> LIEFLAT ──> TONE_EDIT ──> DIFF INTEGRITY GATE ──> PASS ──> FINAL PROSE
                                          │
                                       FAIL (发现剧情/实体篡改)
                                          │
                                          ▼
                                 ROLLBACK TO DRAFT (自动回滚并报警)
```

### 审查指标与阈值
1. **删除比例 (Deletion Ratio)**：不得超过正文字符总数的 5%（除纯粹冗余词外）。
2. **新增比例 (Addition Ratio)**：不得超过正文字符总数的 3%（严禁私自扩写剧情）。
3. **实体完整性 (Entity Loss)**：出场人物姓名、法宝名称、势力名称 100% 保留，零丢失。
4. **数值保真性 (Number Tampering)**：灵石数量、招式层数、距离、时间数值 100% 一致。
5. **事件完整性 (Event Preservation)**：本章核心战斗步骤与对话因果链 100% 保持。

---

## 6. 标准流水线路由图 (Standard Pipeline Routing)

```text
MASTER ORCHESTRATOR
        │
        ▼
CONTEXT RESOLVER (L0/L1)
        │
        ▼
RISK GATE (评估本章风险分级)
        │
        ├────────────────────────────┐
        ▼                            ▼
  OH-STORY (Advisory)       WEBNOVEL-WRITER (Plan/Prewrite)
        │                            │
        └─────────────┬──────────────┘
                      ▼
             DE-AI STYLE COACH (Style Protocol)
                      │
                      ▼
            WEBNOVEL-WRITER (Drafting)
                      │
                      ▼
               CANON QA GATE (审查)
                      │
                      ▼
              LIEFLAT TONE EDIT (去AI味)
                      │
                      ▼
             DIFF INTEGRITY GATE (保真门禁)
                      │
                      ▼
               FINAL QA GATE (终审)
                      │
                      ▼
             STATE UPDATE (Orchestrator 原子提交)
                      │
                      ▼
             HANDOFF SNAPSHOT (生成交接)
```
