# NOVEL OS V2.1 — 技能行为差异与适配对齐表 (SKILL ADAPTER GAPS)

## 1. 概述
在不重写 4 大底层技能实现的前提下，记录各技能在 Legacy 模式下的既有行为与 V2.1 规范之间的差距，并明确由适配层（`scripts/data_modules/v2_worker_adapter.py`）负责弥合。

---

## 2. 差异项详细记录

### Gap 1: OH-STORY 自带顶级路由逻辑
- **涉及技能**：`skills/story`
- **Legacy 既有行为**：在接收到命令时，试图自行判断是否调度 `story-setup`、`story-long-write` 或 `story-review`。
- **V2.1 规范要求**：Orchestrator 独占路由控制权，Worker 不得自发调度其他 Worker。
- **适配器解决方案**：
  - 适配器在调用 `OH-STORY` 时，只向其分派单一咨询任务（如 `task=ANALYZE_HOOKS` 或 `task=MARKET_ADVICE`）；
  - 阻断其向子 Agent 的级联分派，返回值统一截获并作为 `ADVISORY` 注入上下文。
- **是否需要修改底层 Skill 代码**：否（适配层参数封装即可）。
- **是否需要 Human 决策**：否。

---

### Gap 2: WEBNOVEL-WRITER 直接修改 State 与 Canon
- **涉及技能**：`skills/webnovel-write`, `skills/webnovel-plan`
- **Legacy 既有行为**：写作完成后调用 `postcommit.py` 直接修改 `.webnovel/state.json` 与 SQLite 数据库，或回写设定集。
- **V2.1 规范要求**：Worker 只能产出 `proposed_state_changes` 和 `proposed_canon_changes`，由 Orchestrator 经门禁校验后原子写入。
- **适配器解决方案**：
  - 适配器拦截 `postcommit` 的直写操作；
  - 将状态更新捕获为内存中的 `ProposedStateDelta` 对象；
  - 校验通过后由 V2.1 State Manager 执行原子替换。
- **是否需要修改底层 Skill 代码**：否（适配层通过重定向入参及输出钩子实现）。
- **是否需要 Human 决策**：否。

---

### Gap 3: DE-AI 文风协议缺乏结构化输出契约
- **涉及技能**：`skills/de-AI-writing`, `skills/good-writing`
- **Legacy 既有行为**：直接输出自然语言的风格指导段落，格式较为自由。
- **V2.1 规范要求**：需输出结构化 `STYLE_PROTOCOL`（包含长短句比例、感官锚点、禁词清单）。
- **适配器解决方案**：
  - 适配器为 Worker C 提供结构化包装器，将输入请求规范化为统一格式，并将输出解析为标准 JSON / YAML 契约注入 DRAFT 阶段。
- **是否需要修改底层 Skill 代码**：否。
- **是否需要 Human 决策**：否。

---

### Gap 4: LIEFLAT 缺乏后置剧情防篡改门禁
- **涉及技能**：`skills/lieflat-less-ai-tone`
- **Legacy 既有行为**：执行白名单去 AI 味替换后直接输出全文，虽有内部规则约束，但无外部自动化校验。
- **V2.1 规范要求**：必须在输出后接入 `DIFF INTEGRITY GATE`，对实体、数值、事件进行 AST / 正则级保真审计。
- **适配器解决方案**：
  - 适配器在 Worker D 输出后自动运行 `DiffIntegrityGate.verify(draft_text, tone_edit_text)`；
  - 若超出阈值或丢失关键实体，自动触发回滚。
- **是否需要修改底层 Skill 代码**：否（外置门禁拦截器）。
- **是否需要 Human 决策**：否。
