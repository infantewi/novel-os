# NOVEL OS V2.1 — 既有脚本与引擎映射表 (EXISTING ENGINE MAP)

## 1. 既有脚本资产概况
项目在 `scripts/data_modules/` 下拥有极度完备的 Python 引擎体系（50+ 模块及丰富测试套件），涵盖门禁、上下文管理、实体图谱、状态管理器及测试用例。

---

## 2. 既有模块与 V2.1 架构映射

| 既有模块路径 | 对应 V2.1 架构功能 | 复用与整合策略 |
| :--- | :--- | :--- |
| `scripts/data_modules/write_gates/prewrite.py` | V2.1 Pre-write Gate (L0 Context & Outline Validator) | **REUSE (可直接复用)**：前置写作门禁检查 |
| `scripts/data_modules/write_gates/precommit.py` | V2.1 Pre-commit Gate (QA & Word Count Validator) | **REUSE (可直接复用)**：提交前质量与字数检查 |
| `scripts/data_modules/write_gates/postcommit.py` | V2.1 Post-commit Gate (State & Projection Updater) | **REUSE (可直接复用)**：提交后状态机与事件投影同步 |
| `scripts/data_modules/context_weights.py` / `context_ranker.py` | V2.1 Context Resolver (L0/L1/L2) | **REUSE (可直接复用)**：上下文权重计算与检索 |
| `scripts/data_modules/memory/` | V2.1 Memory Compression & Compactor | **REUSE (可直接复用)**：记忆压缩与预算管理 |
| `scripts/data_modules/doctor.py` | V2.1 System Health & Diagnostics | **REUSE (可直接复用)**：项目完整性诊断 |
| `scripts/data_modules/state_manager_*.py` | V2.1 Atomic State Manager | **ADAPTER (封装适配)**：原子状态读写底层实现 |
| `references/author_error_catalog.json` | V2.1 Anti-AI & Error Catalog | **REUSE (可直接复用)**：去 AI 味与错误词库 |
| `skills/story-*` & `skills/webnovel-*` | V2.1 Agent Toolchain | **REUSE (保持原位)**：写作与分析工具链 |

---

## 3. 防重复开发原则
- **不重写**：已有 `write_gates`、`memory` 和 `context` 逻辑严密，V2.1 不需要重复开发轮子。
- **统一接口**：V2.1 的 `MASTER_ORCHESTRATOR` 与 YAML 配置作为全局规则与策略层，既有 Python 模块作为执行引擎层（Execution Engine）。
