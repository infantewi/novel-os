# NOVEL OS V2.1 — 资产迁移与映射总表 (MIGRATION MAP)

## 1. 迁移策略原则
- **模式**：`SAFE LEGACY INTEGRATION`（存量保护 + 逻辑镜像索引）。
- **原则**：旧资产全部保持物理原位，V2.1 编号目录建立单向权威索引（Authority Map），严禁产生双份可独立修改的 Canon 分裂源。

---

## 2. 核心资产映射表

| 原始路径 (Legacy Source) | V2.1 逻辑角色 (Logical Role) | 权威状态 (Authority Status) | 迁移状态 (Migration Status) | 策略说明 |
| :--- | :--- | :--- | :--- | :--- |
| `story_bible.md` | `STORY_BIBLE` | **AUTHORITATIVE** | `PRESERVE` | 小说设定圣经，只读保留在根目录 |
| `设定集/世界观.md` | `CANON_WORLD_RULES` | **AUTHORITATIVE** | `PRESERVE` | 世界观底座，保持原位 |
| `设定集/主角卡.md` | `CANON_PROTAGONIST` | **AUTHORITATIVE** | `PRESERVE` | 陆辰角色档案，保持原位 |
| `设定集/力量体系.md` | `CANON_POWER_SYSTEM` | **AUTHORITATIVE** | `PRESERVE` | 修仙境界法则，保持原位 |
| `设定集/势力与反派谱系.md` | `CANON_FACTIONS` | **AUTHORITATIVE** | `PRESERVE` | 势力与反派关系，保持原位 |
| `设定集/反派设计.md` | `CANON_VILLAINS` | **AUTHORITATIVE** | `PRESERVE` | 反派动机与底牌，保持原位 |
| `设定集/重要配角卡.md` | `CANON_SUPPORTING` | **AUTHORITATIVE** | `PRESERVE` | 核心配角档案，保持原位 |
| `大纲/总纲.md` | `MASTER_OUTLINE` | **AUTHORITATIVE** | `PRESERVE` | 200 万字主线总纲，保持原位 |
| `大纲/第01卷~第07卷.md` | `ARC_OUTLINE` | **AUTHORITATIVE** | `PRESERVE` | 7 卷分卷细纲，保持原位 |
| `正文/第0001章~第0049章.md` | `FINAL_PROSE` | **AUTHORITATIVE** | `PRESERVE` | 49 章定稿正文（13.8万字），禁止移动/修改 |
| `正文/原始归档/*.md` | `ARCHIVED_PROSE_BATCH` | **ARCHIVE** | `PRESERVE` | 10/20/30/40/50 章合辑归档 |
| `current_state.md` | `STATE_HUMAN_DASHBOARD` | **AUTHORITATIVE** | `MIRROR` | 人类可读状态面板，映射至 04_STATE |
| `handoff_current.md` | `HANDOFF_ACTIVE` | **AUTHORITATIVE** | `MIRROR` | 第 50 章会话交接，映射至 06_HANDOFF |
| `pending_hooks.md` | `STATE_HOOKS_REGISTER` | **AUTHORITATIVE** | `MIRROR` | 伏笔悬念追踪表，映射至 04_STATE |
| `progress_tracker.md` | `STATE_PROGRESS_METRICS`| **DERIVED** | `MIRROR` | 生产进度追踪，映射至 04_STATE |
| `pattern-detection.md` | `STATE_PATTERN_MONITOR` | **DERIVED** | `MIRROR` | 叙事模式与高潮节奏监控 |
| `chapter_summaries.md` | `CONTEXT_MEMORY_CACHE` | **DERIVED** | `MIRROR` | 1-49 章全量摘要汇总 |
| `.webnovel/state.json` | `MACHINE_STATE_INDEX` | **DERIVED** | `MIRROR` | 结构化机器运行快照 |
| `.webnovel/index.db` | `SQLITE_SEARCH_INDEX` | **DERIVED** | `SYSTEM` | 向量与实体检索数据库 |
| `.story-system/*.json` | `STORY_SYSTEM_METADATA` | **DERIVED** | `SYSTEM` | 章节/卷/评审历史元数据 |
| `references/csv/*.csv` | `DOMAIN_KNOWLEDGE_BASE` | **AUTHORITATIVE** | `PRESERVE` | 9 大核心写作技法与规则库 |
| `templates/*` | `GENRE_TEMPLATES` | **AUTHORITATIVE** | `PRESERVE` | 题材模板库 |
| `scripts/data_modules/*` | `ENGINE_MODULES` | **SYSTEM** | `PRESERVE` | Python 核心数据引擎与测试套件 |
| `skills/*` / `.agents/*` | `AGENT_SKILLS` | **SYSTEM** | `PRESERVE` | 本地 Agent 生产技能包 |
