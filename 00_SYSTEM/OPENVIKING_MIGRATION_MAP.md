# NOVEL OS V2.2 — OPENVIKING 架构迁移与兼容映射表 (MIGRATION MAP)

| 功能模块 | V2.1 既有实现 | V2.2 OpenViking 集成实现 | 迁移与保留策略 |
| :--- | :--- | :--- | :--- |
| **设定源 (Canon)** | `01_CANON/`, `设定集/` | `01_CANON/` (映射为 `viking://resources/novel/canon/`) | **100% 保留物理文件为最高真理** |
| **状态机 (State)** | `04_STATE/`, `EXECUTION_STATE.yaml` | `04_STATE/` (映射为 `viking://resources/novel/state/`) | **100% 保留为全局进度权威** |
| **元数据注册表** | `.webnovel/index.db` (SQLite) | `.webnovel/index.db` (SQLite) | **100% 完整保留，负责事务性关系索引** |
| **启发式重排** | `scripts/data_modules/context_ranker.py` | `OpenViking Rerank` + `context_ranker` 降级备用 | **保留为 Fallback 兼容层** |
| **向量/混合检索** | `scripts/data_modules/rag_adapter.py` | `memory/openviking/retrieval.py` | **平滑迁移至 OpenViking 原生分层检索** |
| **记忆治理守门** | 初级分类存储 | `memory/governor/` (Novel Memory Governor) | **升级为工业级零信任治理网关** |
| **URI 寻址体系** | 相对文件路径 | `viking://resources/novel/...` | **新增统一语义空间** |
| **上下文装配** | Context Contract v2 | Context Assembler 2.0 (含 `retrieval_trace`) | **升级为具备全轨迹溯源能力的装配器** |
