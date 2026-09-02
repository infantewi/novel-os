# NOVEL OS V2.2 — OPENVIKING 权限模型 (PERMISSION MODEL)

```text
                               OPENVIKING MEMORY
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
            READ ACCESS                               WRITE ACCESS
                 │                                         │
        ┌────────┼────────┐                                ▼
        ▼        ▼        ▼                      NOVEL MEMORY GOVERNOR
     OH-STORY  WRITER   FANQIE                             │
     (只读)   (只读)   (只读)                 ┌────────────┴────────────┐
                                              ▼                         ▼
                                      MASTER ORCHESTRATOR         WORKER DELTA
                                      (AUTHORIZED COMMIT)        (PROPOSAL ONLY)
```

## 权限矩阵明细：
1. **Master Orchestrator**：`can_direct_commit: true`, `can_route: true`
2. **Worker A (OH-STORY)**：`read_memory: READ_ONLY`, `propose_delta: PROPOSAL_ONLY`, `write_openviking: FORBIDDEN`
3. **Worker B (WEBNOVEL-WRITER)**：`read_memory: READ_ONLY`, `propose_delta: PROPOSAL_ONLY`, `write_openviking: FORBIDDEN`
4. **Worker C (DE-AI)**：`read_memory: READ_ONLY`, `propose_delta: FORBIDDEN`, `write_openviking: FORBIDDEN`
5. **Worker D (LIEFLAT)**：`read_memory: FORBIDDEN`, `propose_delta: FORBIDDEN`, `write_openviking: FORBIDDEN`
6. **Fanqie Platform Adapter**：`read_memory: READ_ONLY`, `propose_delta: PROPOSAL_ONLY`, `write_openviking: FORBIDDEN`
