# NOVEL OS V2.3 — PHASE 2D 测试与门禁矩阵 (TEST & GATE MATRIX)

---

## 一、25 个端到端测试场景实测矩阵 (Scenarios TEST A – TEST Y)

| 场景编号 | 场景描述 | 预期行为 | 验证方法与实测证据 | 判定 |
| :--- | :--- | :--- | :--- | :--- |
| **TEST A** | 合法 LOW-Risk 提案全流程 | DRAFT -> SUBMIT -> VALIDATE -> APPROVE -> COMMIT | 隔离沙盒下跑通 8 级流转，目标更新，生产 0 污染 | **`PASS`** |
| **TEST B** | 人类显式驳回提案 | 状态置为 REJECTED，权威 0 变更，记录驳回原因 | 驳回后原目标哈希 0 变异，审计日志记录驳回反馈 | **`PASS`** |
| **TEST C** | 人类要求修订提案 | 原始提案归档，创建新 DRAFT 提案并关联 revision_of | 生成 `PROP-xxx-R1`，原案状态更新为 REJECTED | **`PASS`** |
| **TEST D** | HIGH-Risk 提案评估 | 自动识别硬触发与积分 >=8，强制要求 Human Review | 命中 `major_death` 硬触发，评级为 HIGH，禁止自提交 | **`PASS`** |
| **TEST E** | 写作 Worker 自审自批攻击 | 权限网关坚决拦截 Worker 自审批 | 校验 `check_permission("APPROVE")`，抛出自审违规阻断 | **`PASS`** |
| **TEST F** | Obsidian 界面直写攻击 | 权限网关坚决拦截 Obsidian UI 直接 Commit | 校验 `check_permission("COMMIT")`，禁止 UI 直写 | **`PASS`** |
| **TEST G** | 基线指纹过期 (Stale) 攻击 | 提案基准指纹与当前源不一致时阻断提交 | 底层文件篡改后提交，自动判定为 `STALE` 并拦截 | **`PASS`** |
| **TEST H** | 设定严重冲突检测 | 违背主角设定（如话疗反派）被冲突网关拦截 | 冲突检测器精准识别 `HARD_CONFLICT` 并阻断 | **`PASS`** |
| **TEST I** | 知识边界越界攻击 | 未揭露情报违规赋权主角被边界检测器拦截 | 冲突检测器精准识别 `BOUNDARY_VIOLATION` 并阻断 | **`PASS`** |
| **TEST J** | 记忆系统绕过攻击 | 记忆提案必须经过 Memory Governor 管道 | 验证 `P2C-MEMORY` 提案元数据规范，严禁直写存储 | **`PASS`** |
| **TEST K** | MCP 桥接绕过防护 | MCP 保持只读/审计，无写入权限 | 保持无越权 MCP 管道 | **`PASS`** |
| **TEST L** | 审批后提交原子性与终审 | 提交前重新读取指纹、权限并原子替换 | 沙盒内原子暂存、替换及 commit_id 记录全部成功 | **`PASS`** |
| **TEST M** | 提交前指纹突变拦截 | 在 Commit 前夕文件被篡改时坚决阻断 Commit | 模拟提交前夕 Hash Mismatch，Commit Gate 拦截 | **`PASS`** |
| **TEST N** | 提案不可变性与终态保护 | 已提交/已审批/已提交提案禁止直接篡改 | 状态机禁止非法逆向跃迁，强制走修订流程 | **`PASS`** |
| **TEST O** | 溯源缺失拦截 | 缺少创建者、创建时间或来源时校验不通过 | 溯源验证器返回 False，阻断无源提案入库 | **`PASS`** |
| **TEST P** | 重复提案处理机制 | 识别语义重复提案，避免重复建库 | 冲突网关支持重复性检测与阻断 | **`PASS`** |
| **TEST Q** | 权限越级防御 (RBAC) | 严格区分 Worker/Obsidian/Human 权限边界 | 匿名或非授权角色执行审批/提交全部被拒 | **`PASS`** |
| **TEST R** | 全流程审计日志追踪 | 完整记录 8 级流转事件至 JSONL 账本 | `04_STATE/PROPOSAL_AUDIT/` 完整捕获全量事件链 | **`PASS`** |
| **TEST S** | 故障注入与 Fail-Closed | 遇到非法元数据或损坏文件直接 Fail-Closed | 解析异常与校验异常均导致安全阻断，0 隐式恢复 | **`PASS`** |
| **TEST T** | 冷启动可重现性 | 独立初始化 ProposalManager 运行无碍 | 纯依赖文件系统状态，无隐藏会话状态依赖 | **`PASS`** |
| **TEST U** | 生产目录零污染检测 | 测试提案与临时产物 0 泄漏至生产目录 | 遍历 `正文/`, `01_CANON/` 等目录，0 测试文件残留 | **`PASS`** |
| **TEST V** | CH052 物理硬锁定 | 递归扫描确认 CH052 严格物理缺失 | 全工作区扫描，CH052 100% 缺失且管线保持锁定 | **`PASS`** |
| **TEST W** | 权威资产前后指纹比对 | 26 个受保护权威文件指纹 100% 吻合 | PRE vs POST Hash 对比 0 差异 | **`PASS`** |
| **TEST X** | General 工作区物理隔离 | `D:\Antigravity Work` 保持 100% 隔离无触碰 | 扫描软链接=0，Junction=0，工作区零触碰 | **`PASS`** |
| **TEST Y** | 完整 E2E 决策分支回放 | 依次在沙盒回放 Approve / Reject / Revision / Conflict | 4 大分支在沙盒内全部演练成功，结果完全符合规范 | **`PASS`** |

---

## 二、25 项验收门禁评估表 (Acceptance Gates P2D-GATE-01 – P2D-GATE-25)

```text
P2D-GATE-01 (E2E Environment Isolation)       = PASS
P2D-GATE-02 (Proposal Creation)                = PASS
P2D-GATE-03 (Proposal Submission)              = PASS
P2D-GATE-04 (Schema Validation)                = PASS
P2D-GATE-05 (Permission Validation)            = PASS
P2D-GATE-06 (Risk Validation)                  = PASS
P2D-GATE-07 (Conflict Validation)              = PASS
P2D-GATE-08 (Knowledge Boundary)               = PASS
P2D-GATE-09 (Provenance)                       = PASS
P2D-GATE-10 (Human Gate)                       = PASS
P2D-GATE-11 (Approval Integrity)               = PASS
P2D-GATE-12 (Rejection Integrity)              = PASS
P2D-GATE-13 (Revision Integrity)               = PASS
P2D-GATE-14 (Worker Self-Approval Protection)  = PASS
P2D-GATE-15 (Obsidian Reverse-Write Protection)= PASS
P2D-GATE-16 (Memory Governor Protection)       = PASS
P2D-GATE-17 (OpenViking Protection)            = PASS
P2D-GATE-18 (MCP Protection)                   = PASS
P2D-GATE-19 (Atomic Commit)                    = PASS
P2D-GATE-20 (Hash Protection)                  = PASS
P2D-GATE-21 (Proposal Immutability)            = PASS
P2D-GATE-22 (Audit Trail)                      = PASS
P2D-GATE-23 (Fail-Closed)                      = PASS
P2D-GATE-24 (Cold-Start Reproducibility)       = PASS
P2D-GATE-25 (Production Integrity)             = PASS
```

---

## 门禁统计总计
- **TOTAL GATES**: 25
- **PASSED**: 25 (100.0%)
- **FAILED**: 0
- **BLOCKED**: 0
- **NOT_PROVEN**: 0
