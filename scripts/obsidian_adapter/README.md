# NOVEL OS V2.3 — Obsidian Read-Only Mirror Adapter

## 架构定位
本适配器负责将 NOVEL OS 权威数据（Canon、State、Outline、Memory、Chapters、Handoff、QA）单向导出至 `NOVEL_OS_VAULT/`，供人类作者在 Obsidian 中进行双链可视化查阅与设定审计。

## 核心原则
1. **单向流向**：`NOVEL OS (Authority) -> Obsidian (Read-Only Mirror)`
2. **零写回保护**：禁止任何从 Obsidian 到 Canon/State/Memory 的反向自动写回。
3. **元数据声明**：所有导出文件均强制携带 `source: NOVEL_OS`, `authority: NOVEL_OS`, `sync_mode: READ_ONLY` Frontmatter。
