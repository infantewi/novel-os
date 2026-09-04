# NOVEL OS V2.1 — 雪花小说工程学集成规范与技能全生命周期边界体系 (SNOWFLAKE INTEGRATION SPEC)

---

## 1. 架构定位与冲突判定分析 (Conflict Analysis)

### 1.1 结论：零冲突，正交互补
新引入的 `snowflake-novel-craft` **不仅不会与工作区既有技能产生任何冲突，反而从根本上补全了系统此前在“微观场景动力学”与“底层感官展示”上的核心空白**。

### 1.2 为什么不会冲突？（正交分层架构）
系统内所有技能均严格运行于 NOVEL OS V2.1 的权威层级之下：
```text
HUMAN > CANON > CONTINUITY > STATE > OUTLINE > PLOT > STYLE > TONE
```
各技能分别驻守在不同的抽象维度，互不重叠，彼此支撑：

```
【市场与商业层】 ───> oh-story / fanqie-novel-skill (题材、黄金三章、商业钩子、付费转化)
                             │
【设定与状态层】 ───> webnovel-writer / openviking-memory (Canon设定、真实源、时间线、状态机)
                             │
【结构动力学层】 ───> snowflake-novel-craft (雪花10步、双螺旋场景切片、主动/被动动力学)  ★[核心驱动]
                             │
【微观表现与展示层】 ───> snowflake-novel-craft / De-AI (7大展示工具、MRU动作链、感官具象)
                             │
【文字终审清洗】 ───> lieflat-less-ai-tone (283万字真实语料库、微观去AI味词汇替换)
```

---

## 2. 全技能生命周期时序与职责边界矩阵 (Skill Boundary Matrix)

工作区内每一个 Skill 均有严格的**触发时序、核心职能与神圣边界（绝对禁区）**：

| 阶段 / 序号 | 参与 Skill | 触发时机 (When to use) | 核心职责 (What it does) | 严格禁区与边界 (Strict Boundaries) |
| :--- | :--- | :--- | :--- | :--- |
| **阶段 0<br>宏观立项/分卷** | **`story-setup`**<br>+ **`snowflake (Mode 1)`** | 开新书或开启全新大卷时。 | · 提炼 25 字 Logline 核心钩子；<br>· 规划三幕四区大纲及三大灾难节点（25%/50%/75%）；<br>· 构建丰满的人物宝典（创伤、缺陷、核心价值观）。 | · **严禁** 直接修改既有 Canon 设定；<br>· **严禁** 越权擅自决定全书大结局；<br>· 任何战力与核心设定跃迁必须报批 Human。 |
| **阶段 1<br>前置规划 (PREWRITE)** | **`webnovel-plan`**<br>+ **`snowflake (Mode 2)`**<br>+ **`fanqie-novel-skill`** | 单章生产启动前（默认必经门禁）。 | · 读取上一章状态与本章目标；<br>· **雪花原子场景切片**：将单章拆解为 1-2 个独立微型场景；<br>· 锁定**单一视点（Strict Single POV）**；<br>· 声明场景模式（主动/被动）与驱动力（目标-冲突-挫折 / 反应-困境-决定）；<br>· 注入番茄平台的章节结尾钩子（Hook）。 | · **绝对禁止写正文**；<br>· **严禁** 设定无冲突、无阻力的平淡流水账场景；<br>· **严禁** 视角乱跳（Head-Hopping）；<br>· **严禁** 凭空发明主线事实。 |
| **阶段 2<br>正文起草 (DRAFT)** | **`webnovel-write`**<br>+ **`snowflake (Mode 3)`** | 预写场景卡片通过审查后。 | · 严格按照场景切片逐段铺开剧情；<br>· 严格执行 Swain **MRU 刺激-反应链**（刺激 ➔ 生理 ➔ 动作 ➔ 对话/思维）；<br>· **全面调用 7 大展示工具**（具体感官、动作、微表情、生理内脏反应、原声对白、视点隐藏、节奏呼吸）；<br>· 严密扣紧场景驱动力（主动挫折 / 反应进攻性决定）。 | · **绝对禁止“通篇讲述”式说教与设定解释**；<br>· **严禁** 主角毫无代价轻易通关（必须落实挫折结局）；<br>· **严禁** 擅自改变既定大纲走向。 |
| **阶段 3<br>去AI味与文风 (STYLE & TONE)** | **`De-AI-Prompt-Enhancer`**<br>➔ **`lieflat-less-ai-tone`** | 正文初稿产出后。 | · 先由 De-AI 进行具象物理细节增强，消除机械讲义腔；<br>· 再由 lieflat 调用 283 万字语料库进行白名单词汇精准清洗。 | · **绝对禁止修改情节事实与因果链**；<br>· **严禁** 删改核心人物对话与关键动作；<br>· 必须 100% 通过 Diff Integrity Gate（差异保真门禁）。 |
| **阶段 4<br>质量审查 (QA & AUDIT)** | **`fanqie-novel-skill`**<br>+ **`snowflake (Mode 4)`**<br>+ **`story-review`** | 正文定稿前（双重门禁校验）。 | · **番茄商业审查**：对话占比 <= 40%、禁止“话疗说服 BOSS”、战斗场景深度审计；<br>· **雪花场景体检**：场景三分类（优/差/尚可）、单一视点纯净度、挫折真实性、十大拒稿死穴排查。 | · 审查者仅有**裁决与驳回权**，**严禁自行静默修改正文**；<br>· 发现 Canon 冲突立即触发 `HARD STOP` 并报告 Human（禁止隐式修复）。 |
| **阶段 5<br>提交与交接 (COMMIT & HANDOFF)**| **`webnovel-writer`**<br>+ **`MASTER_ORCHESTRATOR`** | 正文完全通过 QA 审查后。 | · 执行原子状态写入（更新角色、伏笔、状态机）；<br>· 输出本章生产完成报告与交接快照（Handoff）；<br>· 自动生成下一章授权协议；<br>· **执行安全熔断（HARD STOP）**，挂起等待 Human 下一次授权。 | · **任何单一 Worker 严禁越权提交状态**；<br>· **严禁** 擅自推进下一章生产。 |

---

## 3. 默认必经门禁实施规约 (Mandatory Gate Rules)

### 3.1 预写门禁增强（PREWRITE GATE RULE）
每一章正式动笔写正文前，必须在 Prewrite Plan 中明确以下**雪花场景切片元数据**：
```markdown
### 场景切片 1 (Scene 1)
- 视点人物 (POV): [必须且只能有且仅有 1 位在场角色]
- 时空背景 (Setting): [具体地点与时间]
- 场景模式 (Mode): [主动型 Proactive / 被动型 Reactive]
- 场景推进动力 (Driver):
  - [若为主动型]: 目标(Goal) ➔ 冲突阻力(Conflict) ➔ 挫折结局(Setback: No / No+ / Yes, but)
  - [若为被动型]: 生理内脏反应(Reaction) ➔ 两难困境(Dilemma) ➔ 进攻性决定(Decision)
- 预期字数: [例如 1500 字]
```

### 3.2 起草展示规约（SHOW-NOT-TELL RULE）
- 严禁出现“他心中充满了愤怒与震惊”等抽象概述，必须替换为“瞳孔骤缩、心跳漏跳、冷汗渗入衣领”等生理内脏反应。
- 打斗与动作交互必须严格按外部刺激在先、内部反应在后的因果链展开，杜绝因果倒置。

### 3.3 质检门禁升级（QA POLICY GATING）
在 `QA_POLICY.yaml` 的审查清单中，正式将以下四项列为自动化与人工审核检查点：
- `Scene_POV_Integrity`：单场景视点纯度（严禁上帝视角乱跳）；
- `Scene_Disaster_Integrity`：主动场景挫折坚实度（杜绝无脑碾压通关）；
- `Visceral_Reaction_Check`：被动场景生理反应链完整度；
- `Swain_MRU_Check`：微观因果链与感官物理展示比率。
