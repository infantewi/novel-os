# NOVEL OS V2.2 — OPENVIKING 测试规范 (OPENVIKING TEST SPEC)

## 1. 单元测试用例清单 (Unit Tests)
1. **TEST 1: OpenViking Adapter & URI Mapping** (`test_openviking_adapter.py`)
   - 验证 `viking://` URI 格式映射
   - 验证 L0/L1/L2 写入与读取
   - 验证 `find()`, `search()`, `search(mode='context')`
2. **TEST 2: Memory Governor & Validation** (`test_memory_governor.py`)
   - 验证 10 种 Memory Type 校验与合法性
   - 验证 Memory Delta 提交流程
3. **TEST 3: Zero-Trust Permissions** (`test_memory_permissions.py`)
   - 验证 Worker 越权直写 OpenViking 100% 物理拦截
   - 验证仅 Orchestrator 具备授权提交权
4. **TEST 4: Conflict Gate (Canon & Timeline)** (`test_memory_conflicts.py`)
   - 注入金丹境界冲突 ➔ 拦截并置为 `NEEDS_HUMAN` (禁止自动修复)
   - 注入时间线冲突 ➔ 拦截并置为 `NEEDS_HUMAN`
5. **TEST 5: Knowledge Boundary Enforcement** (`test_knowledge_boundary.py`)
   - 验证主角无法获知 `UNREVEALED` 反派隐藏机密，防止剧透
6. **TEST 6: Memory Atomicity & Rollback** (`test_memory_atomicity.py`)
   - 模拟写入异常，验证 `.tmp` 销毁与旧状态无损
7. **TEST 7: Retrieval Traceability** (`test_retrieval_trace.py`)
   - 验证每次检索均生成唯一的 `retrieval_trace`，记录 L0 候选与 L1/L2 升级节点
8. **TEST 8: Health Check & Strict Fallback** (`test_health_and_fallback.py`)
   - 验证 OpenViking 离线时关键生产直接 `BLOCK_STOP_REPORT`，严禁隐式回退
