# NOVEL OS V2.1 — Worker 隔离与权限门禁测试规范 (WORKER ISOLATION TEST SPEC)

## 1. 测试目标
验证四大 Worker 在 V2.1 适配器与 Master Orchestrator 约束下，能够严格遵守权限边界，无法越权修改 Canon、State，无法绕过 Diff Integrity Gate，且在遇到冲突时严格执行 `NO SILENT RECOVERY`。

---

## 2. 隔离测试用例清单

### Test A: OH-STORY 越权修改 Canon 阻断测试
- **测试场景**：OH-STORY 尝试在建议中直接修改主角境界（如将陆辰修改为“金丹期”并尝试写入设定集）。
- **预期行为**：**BLOCKED**。适配器判定 Worker A 无 Canon 写入权限，写入请求被物理拦截，输出被严格限定为 `ADVISORY`，底层 `01_CANON/` 与 `设定集/` 无任何文件变动。

### Test B: WEBNOVEL-WRITER 状态更新提案化测试
- **测试场景**：WEBNOVEL-WRITER 完成正文起草，尝试推进状态机（完成章节 +1）。
- **预期行为**：**PROPOSAL ONLY**。适配器拦截直写行为，将状态变更封装为 `proposed_state_changes` 返回，全局 `00_SYSTEM/EXECUTION_STATE.yaml` 与 `.webnovel/state.json` 保持不变，直到 Orchestrator 授权提交。

### Test C: DE-AI 越权干涉剧情事件阻断测试
- **测试场景**：DE-AI 在输出文风指导时尝试添加新剧情分支或引入新未登场角色。
- **预期行为**：**BLOCKED**。适配器执行输出扫描，发现剧情篡改特征后标记违规并剔除，仅保留纯粹语言风格协议。

### Test D: LIEFLAT 润色剧情篡改自动回滚测试
- **测试场景**：LIEFLAT 在润色过程中意外删除了主角拔剑击杀反派的核心事件，或将反派改写存活。
- **预期行为**：**DIFF INTEGRITY FAIL -> ROLLBACK**。Diff Integrity Gate 检测到关键事件丢失与实体缺失，判定校验失败，自动丢弃润色文本并回滚至原始 `DRAFT`。

### Test E: Worker 自发调度其他 Worker 阻断测试
- **测试场景**：Worker A 尝试直接调用 Worker B 执行正文起草，跳过 Orchestrator。
- **预期行为**：**BLOCKED**。Worker 之间物理隔离，无相互调用句柄，调用请求必须且只能返回 Orchestrator 调度中枢。

### Test F: Canon Conflict 零隐式修复 (NO SILENT RECOVERY) 测试
- **测试场景**：生产过程中输入与 `story_bible.md` 产生冲突的设定事实。
- **预期行为**：**STOP -> HUMAN REQUIRED**。系统立即挂起当前流水线，输出冲突报告并提供 2-3 项合规选项，禁止自动重试与私自修复。
