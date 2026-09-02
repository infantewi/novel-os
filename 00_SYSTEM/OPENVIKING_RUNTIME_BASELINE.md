# NOVEL OS V2.2 — OPENVIKING RUNTIME BASELINE

## 1. 运行环境配置 (Runtime Environment)
- **Python 版本**: 3.12 (Windows 64-bit)
- **操作系统**: Windows (win32)
- **项目根目录**: `D:\Ai work\novel`
- **官方 OpenViking 引擎包**: `D:\Ai work\novel\OpenViking\openviking`
- **OpenViking 命名空间**: `viking://resources/novel`
- **本地持久化存储**: `D:\Ai work\novel\.openviking\storage\viking_index.json`
- **适配器版本**: OpenViking Adapter v2.2.0 (封装官方 OpenViking 语义与分层检索模型)
- **记忆治理中枢**: Novel Memory Governor v2.2.0 (零信任权限 + 冲突拦截门禁)

## 2. 检索与分层参数 (Retrieval Configuration)
- **L0 摘要上限**: 20 项
- **L1 概览上限**: 15 项
- **L2 详情上限**: 5 节点
- **重排器 (Rerank)**: OpenViking Keyword + Semantic Weight Rerank v1
- **降级策略 (Fallback)**: 正式生产离线强制 `BLOCK_STOP_REPORT`；诊断任务使用 `context_ranker` 兼容回退。
