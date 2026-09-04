# NOVEL OS — 新一代长篇网文创作操作系统

<p align="center">
  <strong>专为百万字长篇网络小说打造的工业级多智能体协同创作系统 (Multi-Agent Novel Studio OS)</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square" alt="Python Version" />
  <img src="https://img.shields.io/badge/Architecture-V2.3_Sandbox-green?style=flat-square" alt="Architecture Version" />
  <img src="https://img.shields.io/badge/Methodology-Snowflake_Novel_Craft-orange?style=flat-square" alt="Methodology" />
  <img src="https://img.shields.io/badge/Memory_Engine-OpenViking_Backbone-purple?style=flat-square" alt="Memory Engine" />
  <img src="https://img.shields.io/badge/License-MIT-success?style=flat-square" alt="License" />
</p>

---

## 为什么需要 NOVEL OS？

用简单的单次 Prompt 或基础对话框写网文，在 5~10 万字内必定崩溃：
- **设定漂移与吃书**：AI 遗忘前文战力、因果与伏笔，前后自相矛盾；
- **木偶感与 AI 味**：概念化旁白泛滥，缺乏具象感官动作，角色毫无真实人性；
- **流水账与中段塌陷**：缺少戏剧推进阻力，平淡通关，缺乏可读性；
- **不可逆污染**：AI 擅自改变结局走向，破坏大纲节奏。

**NOVEL OS** 是一套严密的**网络小说创作工程学操作系统**。它通过**八层神圣权威层级**、**雪花小说工程学动力学**、**OpenViking 分层记忆守门人**以及**多题材物理沙盒**，为创作者提供安全、稳定、长效的百万字长篇生产闭环。

---

## 核心架构与技术基石

```text
                                HUMAN (人类作者·最高仲裁)
                                           │
                                           ▼
                              MASTER ORCHESTRATOR (总调度中枢)
                                           │
┌──────────────────────────────────────────┼──────────────────────────────────────────┐
│                                          │                                          │
▼                                          ▼                                          ▼
CANON (真理设定圣经)               STATE (事实时序与状态机)                  OUTLINE (雪花宏观大纲)
(主角卡/力量体系/势力谱系)          (编年史/伏笔追踪/交接报告)              (一句话钩子/三幕骨架/场景表)
│                                          │                                          │
└──────────────────────────────────────────┼──────────────────────────────────────────┘
                                           ▼
                         NOVEL MEMORY GOVERNOR (记忆守门人)
                      (零信任权限隔离 + 知识边界冲突拦截 + 事务原子提交)
                                           │
                                           ▼
                            OPENVIKING ADAPTER (分层检索基座)
                      (L0 抽象摘要 / L1 卷节梗概 / L2 细节片段 + Rerank)
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              FOUR WORKERS (工兵流水线)                               │
├──────────────────────┬──────────────────────┬──────────────────────┬────────────────┤
│ 1. 结构大纲工兵      │ 2. 场景起草工兵      │ 3. 去 AI 味润色工兵  │ 4. 质检风控门禁 │
│ (雪花原子场景切片)   │ (MRU刺激反应链起草)  │ (283万字语料库替换)  │ (十大拒稿死穴体检)│
└──────────────────────┴──────────────────────┴──────────────────────┴────────────────┘
                                           │
                                           ▼
                         OBSIDIAN READ-ONLY MIRROR & PROPOSALS
                          (双向可视化治理看板 + 人类零漂移提案闭环)
```

### 1. 八层神圣权威层级 (Hierarchy of Authority)
```text
HUMAN > CANON > CONTINUITY > STATE > OUTLINE > PLOT > STYLE > TONE
```
任何 AI Worker 绝不允许隐式修复冲突（`NO SILENT RECOVERY`）。下层永远无条件服从上层，遇冲突立即触发安全熔断（`HARD STOP`）并上报人类裁决。

### 2. 雪花小说工程学核心体系 (Snowflake Novel Craft)
以兰迪·英格曼森《雪花写作法》与德怀特·斯温《小说写作技巧》为理论基石：
- **宏观十步演进 (Macro 10 Steps)**：从 25 字一句话电梯钩子 ➔ 五段式三幕骨架（1设置 + 3大灾难 + 1结局）➔ 人物欲望与创伤 (Want vs Need) ➔ 场景总清单表 ➔ 逐章细分起草。
- **微观双螺旋场景动力学 (Micro Scene Dynamics)**：
  - **主动型场景 (Proactive Scene)**：目标 (Goal) ➔ 阻力冲突 (Conflict) ➔ 绝境挫败 (Setback: `No` / `No, and` / `Yes, but`)。
  - **反应型场景 (Reactive Sequel)**：生理情绪冲击 (Reaction) ➔ 两难困境 (Dilemma: 两害相权) ➔ 进攻性决定 (Decision)。
- **纳观动作链 (MRU)**：严格按照感知顺序起草：`外部刺激 ➔ 生理内脏反应 ➔ 骨骼肌物理动作 ➔ 语言口癖与理性思考`。
- **7 大展示去 AI 味工具 (Show, Don't Tell)**：具体感官、内脏反应、微动作、潜台词对话、视点隐藏、环境投射与句式长短顿挫呼吸。
- **十大出版拒稿体检 (Medical Diagnostics)**：严查无阻力平淡流水账、视点乱跳 (Head-Hopping)、机械降神、中段塌陷与作者下场说教。

### 3. 多题材物理沙盒 (Multi-Genre Sandboxing)
所有创作项目放置在独立的 `projects/<项目名称>/` 物理沙盒中：
- **著作权绝对隔离**：`projects/` 目录受 `.gitignore` 保护，您的正文稿件与私密大纲永不上传 GitHub。
- **世界观零污染**：OpenViking 记忆检索库自动按项目命名空间隔离，绝不发生世界观与人设穿帮。

### 4. Obsidian 双向治理看板 (Human-in-the-Loop)
- **只读单向投影**：工程后台将复杂的 Canon、大纲、时间线、伏笔自动映射为美观的 Obsidian 笔记网络。
- **提案式修改闭环 (Proposals)**：人类作者在 Obsidian 中通过专属模板提交修改提案，系统自动执行权限校验、冲突检测与原子提交，彻底消除直接改笔记导致的元数据损坏。

---

## 目录架构全景

```text
novel/ (Repo Root)
├── .agents/                    # 智能体技能标准层 (Claude Code / Antigravity / Cursor)
│   ├── plugins/                # 插件扩展
│   └── skills/                 # snowflake-novel-craft, openviking-memory, de-AI 等
├── 00_SYSTEM/                  # NOVEL OS 核心系统规约
│   ├── MASTER_ORCHESTRATOR_V2.1.md          # 权威调度中枢说明
│   ├── SNOWFLAKE_NOVEL_CRAFT_STANDARD.md   # 雪花小说工程学全流程工业标准
│   ├── CHARACTER_HUMANIZATION_RULES.md     # 角色深度、人性博弈与情感债务
│   ├── MULTI_GENRE_SANDBOX_SPEC.md         # 多题材沙盒物理隔离规约
│   ├── MEMORY_GOVERNOR_SPEC_V2.2.md        # OpenViking 记忆守门人规约
│   ├── QA_POLICY.yaml                      # 质量风控指标矩阵
│   └── PERMISSION_MATRIX.yaml              # 零信任权限矩阵
├── 07_REFERENCE_LIBRARY/       # 通用拆书分析库（指标 JSON / 叙事范式 / 结构化切片）
├── memory/                     # OpenViking 记忆守门人核心模块
│   ├── governor/               # 冲突检测、权限门禁、原子提交守门人
│   └── openviking/             # 分层索引客户端、混合检索与上下文装配
├── projects/                   # 作者作品沙盒目录（受 .gitignore 保护）
│   ├── .gitkeep
│   └── README.md               # 沙盒使用向导
├── templates/                  # 模板与输出脚手架
│   ├── snowflake/              # 雪花核心模板（Logline / 三幕骨架 / 人物宝典 / 场景清单）
│   ├── genres/                 # 30+ 热门题材开篇预设 (修仙/科幻/悬疑/历史/末世等)
│   └── output/                 # 大纲与设定集标准输出骨架
├── scripts/                    # 自动化脚本工具包
│   ├── init_project.py         # 一键初始化新书沙盒
│   ├── build_obsidian_mirror.py # 编译 Obsidian 可视化镜像
│   ├── project_locator.py      # 多项目动态定位器
│   └── obsidian_adapter/       # 双向镜像与提案治理引擎
├── tests/                      # 自动化测试套件 (Memory, Governor, Proposals, Health)
├── .env.example                # 环境变量配置文件模版
├── .gitignore                  # 全面排除规则（保护私有作品、第三方外部库与缓存）
├── LICENSE                     # MIT 开源许可证
├── GEMINI.md                   # 智能体工作区指令
└── README.md                   # 系统主页
```

---

## 快速上手 (Quick Start)

### 1. 环境准备
- **操作系统**：Windows / macOS / Linux
- **Python 环境**：Python >= 3.10
- **依赖安装**：
  ```bash
  pip install -r scripts/requirements.txt
  ```

### 2. 初始化第一本小说沙盒
运行项目生成脚本，创建您的专属作品沙盒：
```bash
# 语法：python scripts/init_project.py --title <书名> --genre <题材>
python scripts/init_project.py --title "星海领主" --genre "科幻"
```
系统将自动在 `projects/星海领主/` 下构建完整的设定集、分卷大纲、状态机及正文目录。

### 3. 应用雪花工程法完成宏观立项
1. 打开 `templates/snowflake/01_ONE_SENTENCE_LOGLINE.md`，提炼 25 字核心剧情电梯钩子；
2. 打开 `templates/snowflake/02_FIVE_PARAGRAPH_STRUCTURE.md`，规划全书三幕骨架与三大灾难节点；
3. 打开 `templates/snowflake/03_CHARACTER_BIBLE_TEMPLATE.md`，定义核心角色的灵魂创伤 (Ghost) 与欲望 (Want vs Need)；
4. 打开 `templates/snowflake/04_SCENE_SPREADSHEET_TEMPLATE.md`，规划前 10 章的原子场景清单。

### 4. 启动单章生产流水线 (以 AI 终端为例)
在 Claude Code、Antigravity 或任意支持 Agent Skills 的终端中：
1. **前置规划**：运行 `/webnovel-plan`，系统调用 `snowflake-novel-craft` 输出包含主动/被动驱动力、单一视点 (Single POV) 的场景卡片；
2. **正文起草**：运行 `/webnovel-write`，严格执行 MRU 刺激-反应链与 7 大展示工具；
3. **去 AI 味打磨**：运行 `/story-deslop`，调用 283 万字真实作家语料库进行白名单词汇清洗；
4. **质量审查**：运行 `/story-review`，执行雪花十大拒稿死穴体检与商业门禁审计；
5. **提交交接**：通过后自动更新状态机与记忆库，输出生产交接报告并熔断待命。

### 5. 同步 Obsidian 可视化看板 (可选)
运行镜像构建脚本，将设定与章节一键投影至 Obsidian：
```bash
python scripts/build_obsidian_mirror.py
```
用 Obsidian 打开生成的 Vault 目录，即可获得带双向链接的知识图谱与全景编年时序看板。

### 6. 运行自动化测试套件
验证记忆守门人、冲突检测与提案治理闭环：
```bash
python -m pytest tests/
```

---

## 创作技能生态 (Agent Skills)

NOVEL OS 深度整合了现代智能体技能生态，所有技能均位于 `.agents/skills/`：
- **`snowflake-novel-craft`**：雪花小说工程学核心引擎（宏观十步、微观切片、7大展示工具、十大体检诊断）；
- **`openviking-memory`**：火山引擎 OpenViking 长效记忆与语义检索集成；
- **`de-AI-writing` / `De-AI-Prompt-Enhancer`**：写前提示词具象增强与物理感官注入；
- **`lieflat-less-ai-tone`**：基于 283 万字真实中文文学语料库的白名单去 AI 味清洗；
- **`obsidian-skills`**：Obsidian 双向笔记与提案协同控制；
- **`oh-story` / `fanqie-novel-skill`**：网文平台黄金开篇设计与商业转化审查。

---

## 开源协议 (License)

本项目采用 [MIT License](LICENSE) 开源协议。
您使用 NOVEL OS 创作的所有小说作品、大纲与设定均属于创作者本人的独立知识产权。
