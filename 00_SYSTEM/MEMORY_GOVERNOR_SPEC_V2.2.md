# NOVEL OS V2.2 — MEMORY GOVERNOR 治理规范 (MEMORY GOVERNOR SPEC)

## 1. 零信任记忆提案模型 (Zero-Trust Memory Proposal)
- 任何 Worker 严禁直接写入 OpenViking 存储。
- 允许的唯一通道：
  ```text
  Worker ──> Memory Delta (提案) ──> Governor ──> Validator ──> Conflict Gate ──> Permission Gate ──> Commit
  ```

## 2. 记忆分类体系 (10 大标准类型)
1. `CANON_MEMORY`：世界观核心规则、战力天花板（需 Human 签字才可生效）
2. `CHARACTER_MEMORY`：角色境界、装备、当前状态
3. `RELATIONSHIP_MEMORY`：角色间敌友、契约、恩怨关系
4. `EVENT_MEMORY`：历史重大战斗、转折点事件
5. `TIMELINE_MEMORY`：时间戳、事件先后次序
6. `LOCATION_MEMORY`：地理场景、宗门遗迹特征
7. `FORESHADOW_MEMORY`：未闭合伏笔、读者承诺（Hooks）
8. `KNOWLEDGE_BOUNDARY_MEMORY`：角色主观知晓边界（防止全知剧透）
9. `CHAPTER_MEMORY`：单章摘要与核心动作
10. `STATE_MEMORY`：当前全局进度快照

## 3. 冲突拦截法则 (Conflict Interception)
- **Canon Conflict**：若提取或提案的事实与 `story_bible.md` 或官方设定集冲突（如擅自突破境界、以德报怨），立即触发 `STOP ➔ NEEDS_HUMAN`，严禁自动修复或自动重试。
- **Timeline Conflict**：时序倒流或因果矛盾立即拦截。
- **Knowledge Boundary Violation**：若主角获取了当前未解密（`UNREVEALED`）的反派秘密，立即阻断。
