# NOVEL OS V2.2 — OPENVIKING MEMORY INFRASTRUCTURE ARCHITECTURE

## 1. 架构定位与核心分工 (System Positioning)

NOVEL OS V2.2 将小说记忆与检索基础设施升级为 **OpenViking-backed Novel Memory Infrastructure**。

```text
                     HUMAN (最高仲裁)
                       │
                       ▼
          MASTER ORCHESTRATOR V2.1 (总调度中枢)
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        CANON         STATE       OUTLINE
    (真理权威)     (事实进度)    (剧情大纲)
          │            │            │
          └────────────┼────────────┘
                       ▼
             NOVEL MEMORY GOVERNOR (记忆守门人)
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   Memory Policy   Conflict Gate   Permission Gate
          │            │            │
          └────────────┼────────────┘
                       ▼
                OPENVIKING ADAPTER (适配器)
                       │
                       ▼
             OPENVIKING NATIVE STORAGE (语义底座)
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
       L0             L1             L2
    (Abstract)     (Overview)     (Details)
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              Hierarchical Retrieval (分层检索)
                       │
                     Rerank (精准重排)
                       │
               Context Assembly (上下文装配)
                       │
                       ▼
               CONTEXT RESOLVER 2.0
                       │
                       ▼
                 FOUR WORKERS (创作工兵)
```

### 核心分工原则：
1. **SQLite (`.webnovel/index.db`)**：事务性元数据、状态机事件投影、关系表注册（Transactional / Governance Metadata）。
2. **OpenViking**：语义上下文、分层索引（L0/L1/L2）、混合检索、Rerank 与检索轨迹跟踪（Semantic Context / Hierarchical Retrieval）。
3. **Novel Memory Governor**：守护设定真实性、执行零信任权限隔离、拦截 Canon/Timeline/知识边界冲突（Governance & Truth Boundary）。
4. **Master Orchestrator**：拥有绝对独占的路由权与事务提交权。
