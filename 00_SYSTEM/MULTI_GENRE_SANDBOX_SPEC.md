# NOVEL OS — 多题材插件与沙盒隔离规范 (MULTI-GENRE SANDBOX SPEC)

> **版本**：V2.3  
> **适用场景**：用户后续引入历史权谋、悬疑推理、现代言情、硬核科幻等跨题材参考书及新项目写作。  
> **设计核心**：**插件化文风 (Style Plugins) + 通用人性经验 (Universal Humanity) + 项目物理沙盒 (Project Sandboxing)**。

---

## 一、 核心架构分层

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. 题材专属雪花预设 (Genre & Snowflake Templates - 相互独立) │
│    • templates/genres/ (30+ 热门题材设定骨架)               │
│    • templates/snowflake/ (雪花小说工程学十步演进骨架)      │
│    • 00_SYSTEM/SNOWFLAKE_NOVEL_CRAFT_STANDARD.md            │
├─────────────────────────────────────────────────────────────┤
│ 2. 底层通用人性与叙事经验 (Universal Humanity - 跨书复用)   │
│    • 00_SYSTEM/CHARACTER_HUMANIZATION_RULES.md             │
│    • 涵盖：利益博弈试探、情感债务补偿、微表情控制、阶级对话 │
├─────────────────────────────────────────────────────────────┤
│ 3. 项目独立沙盒 (Project Sandboxing - 严禁记忆串扰)         │
│    • 每个创作项目独立拥有 01_CANON, 02_OUTLINE, 04_STATE   │
│    • OpenViking 启用独立命名空间 (Memory Namespace)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、 新参考书导入标准流程 (SOP)

当用户引入一本新的几十万或数百万字参考小说时，系统执行以下 4 步标准流水线：

### 1. 教学科目打标 (Assign Specialty)
* 明确该书唯一学习目标，严禁全盘照搬：
  * *范例 A（某历史权谋文）*：仅学习“话里有话的对白艺术与官员微表情博弈”。
  * *范例 B（某悬疑推理文）*：仅学习“信息隐藏节奏与视角盲区设计”。

### 2. 自动化宏观体检 (Python 0-Token Analysis)
* 运行 `python scripts/analyze_reference_stats.py -f <novel_path> -o 07_REFERENCE_LIBRARY/<REF_ID>/STATS_SUMMARY.json`。
* 2 秒内提取章节均长、对白比、段落密度与卡点悬念规律。

### 3. 精准黄金切片 (3 Slices Only)
* 绝不通读全书，只提取 3 个代表性弧光（约 5~8 万字）：
  * **开篇切片**（如何切入世界观与核心矛盾）
  * **巅峰高潮切片**（如何组织大冲突与情绪释放）
  * **日常缓冲切片**（如何体现人情味与生活真实感）

### 4. 物理隔离入库 (Zero Contamination)
* 沉淀为：`07_REFERENCE_LIBRARY/<REF_ID>/`。
* **绝对红线**：
  * 严禁向既有小说 Canon、大纲、生产章节写入参考书情节；
  * 严禁将参考书文本直接注入 OpenViking 的 Canon 知识库。
