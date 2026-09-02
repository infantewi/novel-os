# NOVEL OS V2.2 — OPENVIKING 兼容性与架构审计报告 (COMPATIBILITY AUDIT)

## 一、审计目的与核心原则

在 NOVEL OS V2.1 稳定生产并完成前 50 章定稿的背景下，评估引入 **OpenViking** 作为小说专属记忆与检索基础设施（Novel Memory Infrastructure）的可行性、兼容性与边界模型，严格遵循：
> **`INTEGRATION, NOT REWRITE`（受控集成，绝非重构）**
> **`HUMAN > CANON > CONTINUITY > STATE > OUTLINE > PLOT > STYLE > TONE`**

---

## 二、十二项核心审计问题逐项解答 (A – L)

### A. 当前系统架构 (Current Architecture)
- **调度中枢**：Master Orchestrator 独占路由与权限。
- **创作四核心**：`OH-STORY` (商业顾问) + `WEBNOVEL-WRITER` (初稿) + `DE-AI` (文风协议) + `LIEFLAT` (去AI味终审，受 Diff 门禁保护)。
- **平台层**：`FANQIE PLATFORM ADAPTER` 独立运行于交付层，只读母本正文，产出番茄专属物料与合规报告。
- **真实性来源**：物理文件 Single-Source-of-Truth（`01_CANON`, `02_OUTLINE`, `04_STATE`, `00_SYSTEM`）。

### B. 当前 Memory 架构 (Current Memory Architecture)
- 既有代码在 `scripts/data_modules/memory/`（`orchestrator.py`, `store.py`, `schema.py`）中实现了一个基于 Python 内存与本地 JSON/Scratchpad 的临时事实记录器；
- 根目录下尚未创建独立的 `memory/` 顶层目录；
- **现状评价**：具备初级的多分类记忆数据结构，但缺乏层级化目录结构（L0/L1/L2）、知识边界（Knowledge Boundary）、溯源防伪（Provenance）与百万字规模的高性能向量/混合检索能力。

### C. 当前 Retrieval 架构 (Current Retrieval Architecture)
- 既有代码在 `scripts/data_modules/rag_adapter.py` 中实现了基于 SQLite BM25 与外部 API 的混合检索封装；
- 在 `scripts/data_modules/query_router.py` 和 `knowledge_query.py` 中实现了实体/章节的关键字路由；
- **现状评价**：检索路径较为分散，缺乏统一的上下文分层装配器（Context Assembly）与检索轨迹可观测性（Retrieval Trace）。

### D. SQLite 当前职责 (Current SQLite Responsibilities)
- **物理路径**：`.webnovel/index.db` (包含 18 张结构化表：`chapters`, `scenes`, `appearances`, `entities`, `aliases`, `state_changes`, `relationships`, `override_contracts`, `chase_debt`, `rag_query_log` 等)；
- **核心职责定位**：**事务性元数据与状态投影注册表（Transactional Metadata & Event Registry）**；
- **裁决结论**：**100% 完整保留，不得删除**。SQLite 是工程元数据与状态机事务的物理底座，与语义检索层形成分工互补。

### E. context_ranker 当前职责 (Current context_ranker Responsibilities)
- **物理路径**：`scripts/data_modules/context_ranker.py`；
- **核心职责**：通过时效性（Recency）、出现频次（Frequency）及悬念钩子启发式规则对 Context Pack 中的片段进行权重重排；
- **裁决结论**：**保留为兼容适配与降级备用层（Compatibility / Fallback Layer）**。当 OpenViking 处于活跃状态时，由 OpenViking 原生 Rerank 接管；当 OpenViking 不可用时，自动无缝降级至 context_ranker。

### F. OpenViking 可以接管什么 (What OpenViking CAN Take Over)
1. **统一 URI 资源寻址**：`viking://resources/novel/...`（涵盖 canon, characters, relationships, timeline, chapters, memory）。
2. **L0 / L1 / L2 层次化语义索引**：
   - `L0 (Abstract)`：快速相关性判断与粗筛；
   - `L1 (Overview)`：结构化概览、人物状态、时间线锚点；
   - `L2 (Details)`：精确事实、章节全文、原文章节片段。
3. **原生检索与上下文装配能力**：原生 `find()`, `search()`, `search(mode="context")`，支持预算控制、分层填充与去重。
4. **多模型重排与轨迹跟踪**：原生 Rerank 及 `retrieval_trace`（精确追溯每次上下文召回的证据链）。
5. **百万字长篇可扩展性**：消除全量扫描与 Context 线性膨胀风险。

### G. OpenViking 不应该接管什么 (What OpenViking MUST NOT Take Over)
1. ❌ **不得作为 Canon 设定真相裁决者**（Canon 决定什么是真理，OpenViking 仅记录信息在哪里）。
2. ❌ **不得作为全局状态跃迁权威**（`EXECUTION_STATE.yaml` 与状态机决定当前进度）。
3. ❌ **不得作为大纲或剧情推进引擎**（大纲由 Human/Outline 决定）。
4. ❌ **不得允许 Worker 直接写入 OpenViking**（Worker 必须经由 Governor 提交 Memory Delta）。

### H. Novel Memory Governor 应保留与治理什么 (What Governor MUST Govern)
`NOVEL MEMORY GOVERNOR` 是介于 Orchestrator/Workers 与 OpenViking 之间的**主权与安全守门人**：
1. **Memory Policy**：定义记忆类型（Canon, Character, Relationship, Event, Timeline, Foreshadow, Knowledge Boundary 等）。
2. **Conflict Gate**：严格拦截 Canon 冲突、时间线倒流、战力体系冲突；触发时强制 `STOP ➔ NEEDS_HUMAN`。
3. **Permission Gate**：执行零信任写入边界，Worker 只能提交 `Memory Delta` 提案。
4. **Knowledge Boundary**：标记主观知识边界（`KNOWN`, `UNKNOWN`, `UNREVEALED`），防止主角全知全能与剧透幻觉。
5. **Provenance & Versioning**：记录每条记忆的来源章节、哈希、版本号与审批链；支持 `ACTIVE / SUPERSEDED / INVALIDATED`。
6. **Atomic Commit Gate**：事务性原子写入，任何校验失败或底层故障即刻回滚。

### I. 预计新增文件清单 (Planned New Files)
```text
memory/
├── governor/
│   ├── __init__.py
│   ├── governor.py
│   ├── policy.py
│   ├── validator.py
│   ├── conflict_detector.py
│   ├── permission.py
│   ├── memory_delta.py
│   ├── provenance.py
│   ├── commit_gate.py
│   └── README.md
└── openviking/
    ├── __init__.py
    ├── client.py
    ├── adapter.py
    ├── uri_mapper.py
    ├── retrieval.py
    ├── context_assembler.py
    ├── health.py
    ├── config.py
    └── README.md

00_SYSTEM/
├── OPENVIKING_INTEGRATION_BASELINE.md       [已创建]
├── OPENVIKING_COMPATIBILITY_AUDIT.md        [已创建]
├── OPENVIKING_ARCHITECTURE_V2.2.md
├── MEMORY_GOVERNOR_SPEC_V2.2.md
├── MEMORY_RETRIEVAL_POLICY_V2.2.yaml
├── OPENVIKING_MIGRATION_MAP.md
├── OPENVIKING_PERMISSION_MODEL.md
├── OPENVIKING_BACKFILL_PLAN.md
├── OPENVIKING_TEST_SPEC.md
└── OPENVIKING_ACCEPTANCE_REPORT.md

tests/
├── test_openviking_adapter.py
├── test_memory_governor.py
├── test_memory_permissions.py
├── test_memory_conflicts.py
├── test_knowledge_boundary.py
├── test_memory_atomicity.py
├── test_retrieval_trace.py
├── test_backfill.py
├── test_rebuild.py
├── test_ch050_regression.py
└── test_million_character_stress.py
```

### J. 预计修改文件清单 (Planned Modified Files)
- `scripts/data_modules/context_ranker.py`：微调为兼容性 Fallback 适配器，接口保持完全向后兼容；
- `00_SYSTEM/PERMISSION_MATRIX.yaml`：增加 Memory Governor 与 OpenViking 适配器的读写权限约束定义；
- `00_SYSTEM/MASTER_ORCHESTRATOR_V2.1.md`：记录 Context Resolver 2.0 与 Memory Governor 调度协议；
- **受保护文件（正文 1-50 章、Canon、大纲、当前 State）零修改**。

### K. 风险评估与防御策略 (Risks & Mitigations)
1. **风险 1：OpenViking 服务离线或连接异常**
   - *防御*：`health.py` 探活与降级机制；生产流程中若关键检索缺失触发 `BLOCK ➔ REPORT`；非关键流程使用本地元数据兼容回退，并记录 `fallback_used`。
2. **风险 2：记忆提取污染官方 Canon**
   - *防御*：Memory Governor 的 `Conflict Gate` 硬拦截；任何涉及人物核心存亡、战力突破、主线更迭的 Delta 强制标为 `requires_human: true`，禁止自动提交。
3. **风险 3：主角掌握未公开信息的剧透幻觉（OOC）**
   - *防御*：`Knowledge Boundary` 显式判定矩阵；若检索召回了主角未知的反派底细，在 Context 组装阶段对 Writer 进行视点隔离。

### L. 审计结论与进入 Phase 2 建议 (Recommendation)
> **`RECOMMENDATION: PROCEED TO PHASE 2 (建议进入第二阶段)`**

**论证结论**：
- 现有工程资产（50 章正文、SQLite 数据库、V2.1 状态机与四大 Worker 适配器）架构清晰完备；
- OpenViking 的引入与现有体系不存在根本性冲突，通过 **Novel Memory Governor** 的受控封装，能够完美实现“**语义索引归 OpenViking，权威管控归 Governor，调度归 Orchestrator**”的工业化升级。

---

# HARD STOP — WAITING FOR HUMAN AUTHORIZATION

- 已完成 Phase 0（安全基线锁定）与 Phase 1（兼容性全量审计）。
- 未修改任何生产代码、未修改正文、未回填数据、未触碰第 51 章。
- 等待 Human 审阅审计报告并下达明确指令：
  ```text
  PROCEED PHASE 2
  ```
