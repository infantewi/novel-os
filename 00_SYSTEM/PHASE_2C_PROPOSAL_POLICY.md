# NOVEL OS V2.3 — PHASE 2C 提案治理与安全策略
## PROPOSAL GOVERNANCE & SECURITY POLICY

---

### 一、最高权威与权限层级 (Authority Hierarchy)

严格执行 NOVEL OS 最高权威准则：

$$\text{HUMAN} > \text{CANON} > \text{CONTINUITY} > \text{STATE} > \text{OUTLINE} > \text{PLOT} > \text{STYLE} > \text{TONE}$$

1. **提案非权威性**: 所有 Obsidian 提案文件前言强制标记 `authority: HUMAN_PROPOSAL` 与 `sync_mode: PROPOSAL_ONLY`。
2. **禁止假冒权威**: 提案中严禁声明 `authority: CANON`、`authority: STATE` 或 `authority: MEMORY`。
3. **禁止自动化直写**: Obsidian 笔记保存行为绝对不能直接触发权威源文件的自动覆盖。

---

### 二、角色权限策略 (Role-Based Access Control)

与 `00_SYSTEM/PERMISSION_MATRIX.yaml` 深度整合：

| 操作 (Action) | 人类作者 (HUMAN_AUTHOR) | 编排主控 (MASTER_ORCHESTRATOR) | 写作 Worker (WEBNOVEL_WRITER) | Obsidian 插件/UI (OBSIDIAN_UI) |
| :--- | :--- | :--- | :--- | :--- |
| **CREATE** | **ALLOWED** | **ALLOWED** | **ALLOWED** | **ALLOWED** |
| **EDIT** (Draft) | **ALLOWED** | **ALLOWED** | **ALLOWED** | **ALLOWED** |
| **SUBMIT** | **ALLOWED** | **ALLOWED** | **ALLOWED** | **ALLOWED** |
| **APPROVE** | **ALLOWED** | **ALLOWED** (需授权) | **FORBIDDEN** (严禁自审自批) | **FORBIDDEN** (需 Human Gate) |
| **REJECT** | **ALLOWED** | **ALLOWED** | **FORBIDDEN** | **FORBIDDEN** |
| **REQUEST_REVISION** | **ALLOWED** | **ALLOWED** | **FORBIDDEN** | **FORBIDDEN** |
| **COMMIT** | **ALLOWED** | **ALLOWED** | **FORBIDDEN** | **FORBIDDEN** (无直写通道) |

---

### 三、风险量化与硬触发门禁 (Risk & Hard Triggers)

与 `00_SYSTEM/RISK_GATE.yaml` 严格对齐：
- **硬触发条件 (Hard Triggers)**:
  - 核心/重要角色死亡 (`major_death`)
  - 核心人际关系决裂/反目 (`core_relationship_change`)
  - 核心设定/世界观篡改 (`major_canon_change`)
  - 主角境界越级突破 (`protagonist_major_power_change`)
  - 时序颠倒悖论 (`timeline_break`)
- **风险等级划分**:
  - **LOW (0–3 分)**: 局部描写、陈设细节补充。
  - **MEDIUM (4–7 分)**: 次要配角信息补充、单向关系演进。
  - **HIGH (8+ 分 或 命中任一硬触发)**: 必须强制触发 **HUMAN GATE**，绝不进行自动化放行。

---

### 四、知识边界与防剧透策略 (Knowledge Boundary Protection)

提案校验必须严格区分 **“作者全知视角 (Author Knowledge)”** 与 **“角色当期知晓范围 (Character Knowledge)”**：
1. 严禁未揭露情报 (`UNREVEALED`) 在缺乏当期剧情发现事件（如搜魂、审讯、密报）的前提下直接赋权给主角或配角。
2. 任何越界提案均判定为 `BOUNDARY_VIOLATION` 并直接置入 `CONFLICT` 状态拦截。

---

### 五、不可变性与审计追加策略 (Immutability & Audit Trail)

1. **提案不可变性**:
   - 提案一旦进入 `SUBMITTED` 或 `APPROVED` 状态，其原始内容载荷冻结。
   - 如需修改，必须通过 `REQUEST_REVISION` 创建关联的新版本草稿（如 `PROP-001-R1`），原始提案保留在历史归档中。
2. **追加写入日志 (Append-Only Audit)**:
   - 所有事件必须追加记录在 `04_STATE/PROPOSAL_AUDIT/audit_log.jsonl`。
   - 严禁篡改、截断或重写历史审计记录。
