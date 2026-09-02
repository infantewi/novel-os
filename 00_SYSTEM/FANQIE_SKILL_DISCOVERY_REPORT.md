# FANQIE NOVEL SKILL — V2.1 DISCOVERY REPORT

## 1. Physical Location (实际物理路径)

- **主技能目录**：[`skills/fanqie-novel-skill`](file:///D:/Ai%20work/novel/skills/fanqie-novel-skill)
- **镜像技能目录**：[`D:/Ai work/novel/.agents/skills/fanqie-novel-skill`](file:///D:/Ai%20work/novel/.agents/skills/fanqie-novel-skill)
- **核心文件清单**：
  - 指令与入口：`SKILL.md` (11.8 KB), `README.md` (11.1 KB), `CHANGELOG.md`
  - 平台参考知识库 (`references/`)：
    - `fanqie-platform-rules.md`：番茄平台商业规则、字数规范与签约机制 (20k/50k/80k)
    - `audit-dimensions.md`：33 个审计维度与 v2.0.1 最小审计集（8 项强制检查）
    - `battle-scene-guide.md`：战斗场景专项指引与“禁止话疗”硬约束
    - `dialogue-monitor.md`：对话占比监控规范 (<40%)
    - `pattern-detection.md`：叙事循环与高潮节拍检测
    - `commercial-review.md`：商业审阅与黄金三章留存模型
    - `ai-detox-guide.md`：AI 禁词表与智能替换表
  - 项目模板库 (`assets/project-template/`)：包含 `book_rules.md`, `story_bible.md`, `current_state.md`, `handoff_current.md` 等标准脚手架（本项目根目录现有规范即源自该模板体系）。
  - 示例工程 (`examples/demo-novel/`)：样例小说参考。

---

## 2. Skill Purpose (技能实际用途与定位)

`fanqie-novel-skill` 是一套专为**番茄小说（Fanqie Novel）平台**定制的长篇网文全生命周期创作、商业合规审查与平台交付系统。其核心目标是解决长篇网文在番茄平台的“签约率、读完率、去 AI 味、防话疗、防战力崩溃”等工业化痛点，支持 120 万字以上的长线运营。

---

## 3. Capability Matrix (能力完整矩阵)

| 判定维度 (Capability) | 是否具备 (Present) | 详细实现与行为特征 (Details) |
| :--- | :---: | :--- |
| **Story Generation (故事构思)** | ✅ 具备 | 提供基于番茄热门爽点（无敌流、打脸、快反转）的故事设计方法。 |
| **Chapter Writing (正文起草)** | ✅ 具备 | 包含章节起草 Prompt 模板与黄金前三章节奏模板。 |
| **Editing (语言去味与精修)** | ✅ 具备 | 集成 `ai-detox-guide.md`，提供禁用词检测与智能替换机制。 |
| **Planning (大纲与节拍规划)** | ✅ 具备 | 提供总纲、分卷节拍表与 2 万/5 万/8 万字签约关键节点规划。 |
| **Title Generation (书名/章节名生成)** | ✅ 具备 | 番茄爆款书名公式（主书名 + 钩子副标题）与高点击率章节名生成。 |
| **Synopsis Generation (简介生成)** | ✅ 具备 | 番茄“三段式”简介模板（人设标签 + 核心金手指 + 极致冲突反差）。 |
| **Tags & Category (标签与分类定位)** | ✅ 具备 | 番茄官方题材标签库与平台推荐算法画像定位。 |
| **Platform Formatting (排版呈现)** | ✅ 具备 | 单章 2000-2500 字，段落 1-3 句紧凑手写体，禁用破折号（——）。 |
| **Compliance (平台合规与红线审查)** | ✅ 具备 | 严格审查涉政、涉黄、恶意抹黑官方机关等平台封禁红线（军方/九局保持正面）。 |
| **Marketing (商业化与留存包装)** | ✅ 具备 | 黄金前三章生死线留存率设计、付费节点与章末强钩子（4 种断章写法）。 |
| **Submission Preparation (交付打包)** | ✅ 具备 | 整理番茄后台发布所需的三要素（书名、简介、首发 3-5 章）与首签包。 |
| **Account Interaction (账号交互)** | ❌ 不具备 | 无自动登录番茄作者后台脚本。 |
| **Browser Automation (浏览器自动化)** | ❌ 不具备 | 无内置 CDP / Playwright 自动上传脚本。 |
| **External Network / API (外部网络)** | ❌ 不具备 | 纯本地规则库与提示词指令集，无外部网络依赖。 |
| **Routing / Orchestration (自主调度)** | ⚠️ 局部具备 | 包含工作流状态跳转描述，但在 V2.1 架构下必须被拦截收拢。 |

---

## 4. Architecture Classification (架构属性分类)

- **Primary Role (主要角色)**：**`PLATFORM ADAPTER` (番茄平台适配与交付包装 Worker)**
- **Secondary Roles (次要角色)**：
  - `COMPLIANCE WORKER` (番茄平台合规与红线门禁)
  - `MARKETING / PACKAGING WORKER` (番茄书名、简介、标签与签约包生成)

---

## 5. Four-Skill Overlap & Redundancy Analysis (与现有四大 Worker 重叠度分析)

遵循 **`ONE CAPABILITY ➔ ONE AUTHORITY`** 原则，对重叠能力进行权威归属划分：

| 功能领域 | `fanqie-novel-skill` 既有能力 | V2.1 权威 Worker 归属 | 裁决与整合策略 |
| :--- | :--- | :--- | :--- |
| **正文起草与章节规划** | 包含番茄起草与大纲指令 | **`WEBNOVEL-WRITER`** (Worker B) | **剥离并委托**：正文起草 100% 由 Worker B 唯一负责，严禁产生第二写作大脑。 |
| **商业题材与宏观构思** | 包含番茄爽点分析 | **`OH-STORY`** (Worker A) | **协同咨询**：宏观故事顾问归 Worker A，Fanqie Skill 仅提供番茄专属细分算法特征。 |
| **写前文风协议** | 包含句式与手写体指引 | **`DE-AI`** (Worker C) | **协议共享**：Fanqie 的手写体与段落规则作为参数注入 Worker C 的 `STYLE_PROTOCOL`。 |
| **微观去 AI 味润色** | 包含 AI 禁词替换表 | **`LIEFLAT`** (Worker D) | **词表沉淀**：其词表已包含在 `references/`，终审润色 100% 由 Worker D 执行并受 Diff 门禁保护。 |
| **平台红线与防话疗门禁** | 包含 8 项最小审计集与 33 维度 | **`QA Policy (HIGH/MED)`** | **规则复用**：其“禁止话疗”与对话监控已固化为 V2.1 系统的核心审计门禁。 |
| **番茄书名/简介/签约包交付** | 包含完整番茄交付模板 | **`FANQIE ADAPTER` (本技能独占)** | **独占授权**：平台物料生成由本技能作为平台适配器独家承载。 |

---

## 6. Canon Risk (设定破坏与分歧风险)

- **风险特征**：若将 `fanqie-novel-skill` 作为自由创作脑接入，可能会为了迎合番茄“即时爽感”或过激打脸套路，擅自修改人物性格（OOC）、篡改战力境界、突兀插入与现有 49 章不符的俗套反派，或为了避规私自删减历史背景设定。
- **V2.1 安全约束**：
  - `fanqie-novel-skill` **绝对禁止写入 `01_CANON/` 与 `设定集/`**。
  - 任何因平台适配引发的设定微调建议，只能以 `PLATFORM ADAPTATION PROPOSAL` 形式上报，未经 Human 签署批准严禁改变故事事实。

---

## 7. State Risk (状态机污染风险)

- **风险特征**：该技能自带一套模板状态定义（`current_state.md`, `progress_tracker.md` 等），若直接运行可能覆盖或扰乱 V2.1 的 `00_SYSTEM/EXECUTION_STATE.yaml`。
- **V2.1 安全约束**：
  - 剥离其所有状态直写权限，只读获取当前主生产状态，其自身运行状态封装在 `05_MARKETING/` 或平台专用命名空间下。

---

## 8. Permission Recommendation (推荐安全权限模型)

```yaml
FANQIE_PLATFORM_ADAPTER:
  read_permissions:
    canon: true             # 只读读取设定
    outline: true           # 只读读取大纲
    state: true             # 只读读取进度
    final_prose: true       # 只读读取已完结定稿正文 (用于提取简介与首发包)
    marketing_data: true

  write_permissions:
    canon: false            # 严格禁止写入设定
    state: false            # 严格禁止写入全局状态
    story_prose: false      # 严格禁止起草正文
    official_outline: false # 严格禁止修改主线总纲

  create_artifacts:
    - "05_MARKETING/fanqie_title_proposals.md"
    - "05_MARKETING/fanqie_synopsis_and_tags.md"
    - "05_MARKETING/fanqie_contract_milestones.md"
    - "03_PRODUCTION/FINAL/platform_packages/fanqie/"
    - "00_SYSTEM/fanqie_compliance_audit_report.md"

  can_route: false          # 无路由权，受 Orchestrator 调度
```

---

## 9. Platform Adapter Recommendation (平台适配器定位论证)

**推荐定位**：**`PLATFORM ADAPTER`（平台层适配器）**

**论证与收益**：
1. **职责单一清晰**：定位为平台适配器后，它不再与 `WEBNOVEL-WRITER` 竞争正文写作权，而是专注于“将高质量母本小说适配为番茄平台最佳发布形态”。
2. **保护核心生产线**：主生产线保持 `Master Story` 的纯粹性与高文学/商业质感；平台层负责转化出符合番茄算法高分特征的标题、简介、章节分块与红线审计。

---

## 10. Multi-Platform Architecture (多平台协同架构演进)

为支持未来可能接入的海外平台（如 GoodNovel, WebNovel, MegaNovel）或中文其他平台（七猫、起点、知乎），V2.1 系统推荐采用 **“单一主母本 ➔ 多平台适配”** 架构：

```text
                        MASTER ORCHESTRATOR
                                 │
                                 ▼
                         ONE CANON (唯一设定源)
                                 │
                                 ▼
                      ONE MASTER STORY (主正文流)
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             STORY PRODUCTION           PLATFORM LAYER (平台交付层)
         (Webnovel-Writer / De-AI)            │
                                  ┌───────────┴───────────┐
                                  │                       │
                                  ▼                       ▼
                         FANQIE ADAPTER          GOODNOVEL ADAPTER
                     (番茄标题/简介/红线包)   (海外本地化/短快付费节拍)
```

- **核心铁律**：无论下游分发多少平台，**设定源（ONE CANON）与正文母本（ONE MASTER STORY）永远唯一**，彻底根除多平台发布导致的剧情设定精神分裂。

---

## 11. External Action Requirements (外部动作依赖)

- **网络与浏览器依赖**：技能本身为本地静态规则集，无自动化联网/上传脚本。
- **人工外接动作 (EXTERNAL ACTION REQUIRED)**：
  - 番茄作者后台账号注册与实名认证（`fanqienovel.com`）需由 **Human** 完成；
  - 最终生成好的首发签约包（前 3-5 章、书名、简介、标签）需由 **Human** 复制到番茄作者后台进行物理发布与签约申请；
  - 严禁任何 AI 试图猜测或自动发起未授权的平台外网提交。

---

## 12. Recommendation (最终审计裁决结论)

> **`KEEP / PLATFORM ADAPTER`**

**结论说明**：
- **不删除 (DO NOT DELETE)**：其包含极具价值的番茄平台红线合规规则、签约节点追踪与高转化物料生成方法；
- **不做第五核心写作脑 (NOT A 5TH CORE WRITER)**：剥离其正文生成权，防止与 `WEBNOVEL-WRITER` 产生架构冲突；
- **保留并收编为平台适配器**：正式归入 V2.1 `PLATFORM LAYER`，作为专门负责番茄平台合规审查与上架包装的受控 `PLATFORM ADAPTER`。

---

## 13. Required Future Changes (未来实施清单 — 需 Human 批准后执行)

以下操作在当前阶段保持冻结，仅在 Human 正式授权后推进：
1. **Adapter 代码接入**：在 `scripts/data_modules/` 中增加 `FanqiePlatformAdapter` 封装；
2. **物料生成路由**：在 Orchestrator 中增加 `GENERATE_PLATFORM_PACKAGE(platform='fanqie')` 阶段指令；
3. **输出目录就位**：建立 `05_MARKETING/fanqie/` 与 `03_PRODUCTION/FINAL/platform_packages/fanqie/`；
4. **权限矩阵收敛**：正式将 `FANQIE_ADAPTER` 权限写入 `00_SYSTEM/PERMISSION_MATRIX.yaml`。
