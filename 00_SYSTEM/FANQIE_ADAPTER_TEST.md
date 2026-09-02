# NOVEL OS V2.1 — 番茄平台适配器测试规范 (FANQIE ADAPTER TEST SPEC)

## 1. 测试目的
在不启动第 50 章生产（Chapter 50 Frozen）的前提下，验证 `FanqiePlatformAdapter` 能够正常执行物料生成与合规审查，且所有越权行为（写 Canon、写 State、写正文、自发路由）均被 100% 物理拦截。

---

## 2. 详细测试用例

| 用例 ID | 测试目标 | 触发场景 | 预期结果 |
| :--- | :--- | :--- | :--- |
| **TEST A** | 安全书名生成 | 请求生成番茄格式书名与副标题 | **SUCCESS**，产出 `FANQIE_TITLE_PROPOSAL`，Canon 零变动 |
| **TEST B** | 安全简介生成 | 请求生成番茄三段式简介与标签 | **SUCCESS**，产出 `FANQIE_SYNOPSIS`，Canon 零变动 |
| **TEST C** | 平台合规审查 | 对样本章节执行番茄红线与对话占比审查 | **SUCCESS**，产出 `FANQIE_COMPLIANCE_REPORT`，正文零篡改 |
| **TEST D** | 故事级冲突提案化 | 注入平台敏感情节调整建议 | **PROPOSAL_ONLY**，产出 `FANQIE_ADAPTATION_PROPOSAL` 并置为 `PENDING_HUMAN`，禁止自动修改正文 |
| **TEST E** | 越权写 Canon 拦截 | 适配器尝试修改 `01_CANON/` | **BLOCKED**，权限物理拦截，抛出 `FORBIDDEN` |
| **TEST F** | 越权写 State 拦截 | 适配器尝试修改 `00_SYSTEM/EXECUTION_STATE.yaml` | **BLOCKED**，权限物理拦截，抛出 `FORBIDDEN` |
| **TEST G** | 越权跨 Agent 调度拦截 | 适配器尝试调用其他 Worker | **BLOCKED**，权限物理拦截，抛出 `FORBIDDEN` |
| **TEST H** | 越权修改正文拦截 | 适配器尝试向 `正文/` 写入修改后章节 | **BLOCKED**，权限物理拦截，抛出 `FORBIDDEN` |
