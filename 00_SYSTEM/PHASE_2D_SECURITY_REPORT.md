# NOVEL OS V2.3 — PHASE 2D 安全与防护评估报告
## PROPOSAL SECURITY & THREAT MODEL REPORT

---

### 一、威胁模型与防御架构 (Threat Model & Defenses)

| 威胁向量 (Threat Vector) | 潜在危害 | 防御机制 | 验证证据 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| **Worker 越权自审批 (Self-Approval)** | 自动化 AI Worker 伪造人类批准修改核心设定 | `ProposalPermissionGate` 强制禁止创建者与审批者同为非 Human Worker | `test_scenario_e_worker_self_approval_attack` (Blocked) | **`SECURE`** |
| **Obsidian 界面直接越界写 (Direct Write)** | 绕过审查流程直接修改只读设定集或生产文件 | 严格单向数据流与权限网关拦截，Obsidian 无 Commit 接口 | `test_scenario_f_obsidian_direct_write_attack` (Blocked) | **`SECURE`** |
| **过期提案覆盖并发冲突 (Stale Overwrite)** | 提案基于老旧版本，提交时覆盖更新的权威修改 | 提交与校验阶段双重哈希比对 (`current_authority_hash`) | `test_scenario_g_hash_stale_proposal` & `test_scenario_m` (Blocked) | **`SECURE`** |
| **全知剧透注入知识边界越界 (Knowledge Leak)** | 将作者视角的未揭露情报直接赋予当期角色 | `ProposalConflictDetector` 针对 `UNREVEALED` 关键词与角色认知执行强校验 | `test_scenario_i_knowledge_boundary_attack` (Blocked) | **`SECURE`** |
| **核心人设与设定严重冲突 (Canon Break)** | 提案颠覆主角极道杀伐果断性格或跨境界突变 | 硬触发规则与核心禁令（如禁止话疗/禁止提前金丹）强校验 | `test_scenario_h_hard_conflict` (Blocked) | **`SECURE`** |
| **记忆基础设施直接绕过 (Memory Direct Write)** | 提案绕过 Governor 直接污染 OpenViking 命名空间 | 记忆提案声明非权威性，写回必须受 Memory Governor 治理 | `test_scenario_j_memory_governor_bypass` (Blocked) | **`SECURE`** |
| **提交中断导致部分写入 (Partial Write)** | 写入异常导致权威文件损坏或产生半成品 | 临时文件预写 (`.tmp_xxx`) -> 全局校验 -> 原子替换 (`replace`) | `test_scenario_l` & `test_scenario_s` (Atomic) | **`SECURE`** |

---

### 二、权限矩阵与角色边界执行情况 (RBAC Boundary Audit)

- **HUMAN_AUTHOR**: 具备全流程发起、审查、批准、驳回、修订及提交授权。
- **MASTER_ORCHESTRATOR**: 具备编排主控、系统性审查与授权提交权限。
- **WEBNOVEL_WRITER / OH_STORY**: 仅具备 `PROPOSE` 权限，**严禁自审自批**。
- **OBSIDIAN_UI**: 仅具备 `CREATE` / `EDIT` / `SUBMIT` 提案草案权限，**严禁直接 Commit**。

---

### 三、审计追踪与不可篡改性 (Audit Trail & Immutability)

- **追加账本**: `04_STATE/PROPOSAL_AUDIT/audit_log.jsonl`
- **记录属性**: 包含 `proposal_id`, `event`, `timestamp`, `actor`, `previous_status`, `new_status`, `source_hash`, `commit_id`, `reason`。
- **不可变性**: 任何已进入终态或审批态的提案均禁止原地篡改，强制触发 `REQUEST_REVISION` 创建新版本节点。
