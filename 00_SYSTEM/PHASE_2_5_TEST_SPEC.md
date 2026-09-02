# NOVEL OS V2.1 — PHASE 2.5 测试规范与设计 (PHASE 2.5 TEST SPEC)

## 1. 测试原则与目标 (Core Principles)
1. **真实工业化流水线验证**：验证 V2.1 架构在 LOW / MEDIUM / HIGH 三级风险分支下的 Context 解析、Worker 权限隔离、Diff 保真门禁、原子状态机与交接机制。
2. **严禁生产污染与第 50 章绝对冻结**：
   - 测试产物 100% 隔离于 `03_PRODUCTION/TEST_RUNS/PHASE_2_5/`；
   - 官方 Canon、大纲、状态机、49 章定稿正文绝对只读；
   - 第 50 章保持 `UNWRITTEN / FROZEN / STANDBY_FOR_CHAPTER_50`。
3. **零隐式修复 (NO SILENT RECOVERY)**：任何设定冲突必须强制触发 `STOP ➔ NEEDS_HUMAN`，严禁私自修复。

---

## 2. 三大核心生产测试用例

### 2.1 TEST 01 — LOW RISK (CH001 样本重放)
- **目标场景**：第 1 章主角苏醒与至亲确认。
- **风险定级**：LOW (Score=2)。
- **激活门禁**：`LOW QA`（6 项基础合规检查：字数、实体、必要事件、禁止事件、基础设定、结尾钩子）。
- **预期流水线**：`Context ➔ OH-Story ➔ De-AI ➔ Writer ➔ Low QA ➔ Lieflat ➔ Diff Gate ➔ Sandbox State`。

### 2.2 TEST 02 — MEDIUM RISK (CH002 样本重放 + 重试机制)
- **目标场景**：第 2 章医院办公室冲突与断骨立威。
- **风险定级**：MEDIUM (Score=6)。
- **激活门禁**：`MEDIUM QA`（6 LOW + 5 连续性检查：人物、时间线、关系谱、状态跃迁、伏笔呼应 = 11 项）。
- **重试子测试**：首发异常注入，验证同阶段、同 Worker 自动重试（最多 2 次）。

### 2.3 TEST 03 — HIGH RISK (CH003 样本重放 + 深度审查)
- **目标场景**：第 3 章九转针法定生死与指尖神雷起死回生。
- **风险定级**：HIGH (硬触发：`major_reversal`, `core_foreshadowing_payoff`，Score=9)。
- **激活门禁**：`HIGH QA`（11 项基础/连续性 + 12 项深度因果/战力平衡/防话疗检查 = 23 项）。

---

## 3. 专项门禁与安全测试

| 专项测试 | 场景与断言 | 预期结果 |
| :--- | :--- | :--- |
| **Canon Conflict Test** | 注入“以德报怨/废弃修仙改修佛门”冲突用例 | **STOP ➔ NEEDS_HUMAN**，产出 3 项合规选项，禁止自动重试与修复 |
| **Diff Integrity Test** | 润色阶段注入角色篡改与剧情逆转 | **FAIL ➔ ROLLBACK_TO_DRAFT**，自动回滚至初稿 |
| **Atomic State Test** | 模拟状态写入故障与崩溃 | 临时文件销毁，既有状态零破坏，保证事务原子性 |
| **Fanqie Regression** | 执行 Fanqie 适配器全量测试套件 | **8/8 PASS**，平台物料严格隔离于专属命名空间 |
| **Global Integrity** | 全量比对 13 处生产核心资产 SHA-256 哈希 | **零污染 / 0 Diff**，第 50 章未创建 |
