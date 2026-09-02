# NOVEL OS V2.3 — OBSIDIAN VAULT ARCHITECTURE MAP

---

## 1. Vault 总体架构 (Vault Overview)

- **Vault 根目录**: `D:\Ai work\novel\NOVEL_OS_VAULT`
- **定位**: **HUMAN KNOWLEDGE WORKSPACE / VISUAL REVIEW LAYER**
- **数据流向**: `NOVEL OS (Authority) ───[Exporter]───► Obsidian Novel Vault (Read-Only Mirror)`
- **目录类别总数**: 17 个一级分类
- **已镜像文件总数**: 275 个 Markdown 节点 + 1 个 Manifest 索引文件

---

## 2. 目录架构与映射矩阵 (Category Mapping Matrix)

```text
NOVEL_OS_VAULT/
├── 00_HOME/                  # 生产监控与视觉评审看板 (NOVEL_OS_HOME.md)
├── 01_CANON/                 # 权威世界观、主角档案、力量体系、设定圣经
├── 02_CHARACTERS/            # 角色独立档案 (14 位核心人物/反派/配角)
├── 03_RELATIONSHIPS/         # 角色关系双链网络 (8 组已验证核心关系)
├── 04_TIMELINE/              # 时序因果链 (6 个分段节点 + 总索引)
├── 05_LOCATIONS/             # 场景与地理档案 (8 个核心地理空间)
├── 06_FACTIONS/              # 宗门/财阀/官方谱系 (8 个主要势力)
├── 07_ABILITIES/             # 功法、神识、真火、肉身法门 (8 门核心神通)
├── 08_ITEMS/                 # 本命法宝、丹药、阵图 (8 件关键器具)
├── 09_FORESHADOWING/         # 伏笔生命周期追踪 (8 条伏笔 + 伏笔总表)
├── 10_CHAPTERS/              # 1-51章正文摘要镜像 (CH001~CH051, CH052严格缺失)
├── 11_ARCS/                  # 1-7卷主线大纲与分卷架构 (含当前名动江南卷)
├── 12_STATE/                 # 系统执行状态、创作状态、进度指标镜像
├── 13_HANDOFF/               # CH050/CH051交接快照与生产中枢镜像
├── 14_MEMORY/                # OpenViking 126 个结构化记忆节点
├── 15_QA/                    # 质量评估、回填全局审计与风控规则
└── 99_SYSTEM/                # 只读协议策略文件与镜像物理清单 (MANIFEST)
```

---

## 3. 分类映射详细说明

### 3.1 `00_HOME/`
- `NOVEL_OS_HOME.md`: 实时反映 NOVEL OS 生产状态，展示作品信息、当前卷（第二卷·名动江南）、完结章节（CH051）、待产章节（CH052 严格锁定）、活跃伏笔与记忆库统计。

### 3.2 `01_CANON/`
- 镜像自 `story_bible.md` 及 `设定集/`（世界观、主角卡、力量体系、势力与反派谱系、反派设计、重要配角卡）。

### 3.3 `02_CHARACTERS/`
- 包含陆辰、陆小晚、苏清璇、冷月、叶破天、暴熊、赵天宇、赵老太爷、沈天豪、雷震霄、雷千绝、孙侯、巴颂、阿赞扎等全量已登场或立案角色。

### 3.4 `03_RELATIONSHIPS/`
- 包含陆辰与陆小晚（至亲逆鳞）、苏清璇（世俗代行者）、冷月（官方国士结盟）、叶家（武道臣服）、海外洪门（血仇死敌）、南洋黑巫教（灭杀宿怨）等结构化关系。

### 3.5 `04_TIMELINE/`
- 按 10 章一批次精确切分时序因果（CH001-CH010, CH011-CH020, CH021-CH030, CH031-CH040, CH041-CH050, CH051），配合 `TIMELINE_MASTER_CH001_CH051.md` 形成完整闭环。

### 3.6 `05_LOCATIONS/`
- 云顶山庄一号天宫、迎宾馆、百草堂、望江楼、叶家庄园、秦淮河沈家祖宅、维多利亚女王号游轮、神农古秘境（锁定）。

### 3.7 `06_FACTIONS/`
- 灵辰集团、叶家、华夏九局朱雀小队、海外洪门总舵、南洋黑巫教、暗网黑水佣兵、已覆灭赵氏财团与江南武道盟。

### 3.8 `07_ABILITIES/`
- 九天玄天决、太衍吞天决、青帝琉璃身雏形、九天纯阳三昧真火、九天引雷诀、破甲飞针、因果搜魂术、虚空画符与聚灵阵。

### 3.9 `08_ITEMS/`
- 惊鸿飞剑、首山赤铜鼎、九转还魂丹、纯阳培元液、洗髓丹、阴阳造化丹、神农古秘境残图、特级顾问黑卡。

### 3.10 `09_FORESHADOWING/`
- 严格标记状态：
  - `H-050-01`: `RESOLVED` (三昧真火破万鬼阵)
  - `H-050-02`: `ACTIVE` (神农古秘境残图，锁定第52章)
  - `H-046-01`: `ACTIVE` (北美黑水战队潜伏)
  - `H-042-01`: `ACTIVE` (陆小晚玄阴圣体进阶)
  - `H-026-01`: `ACTIVE` (南洋黑巫教总坛)

### 3.11 `10_CHAPTERS/`
- `CH001.md` ~ `CH051.md` (51 篇)。
- 标记 `status: COMPLETE`。
- **CH052 物理文件与镜像笔记 100% 缺失与锁定**。

### 3.12 `11_ARCS/`
- 第01卷（潜龙出渊，已完结）、第02卷（名动江南，进行中）、第03卷至第07卷（大纲总纲），及 `ARCS_MASTER_OVERVIEW.md`。

### 3.13 `12_STATE/` & `13_HANDOFF/`
- `EXECUTION_STATE_MIRROR.md`、`CURRENT_STATE_MIRROR.md`、`PROGRESS_TRACKER_MIRROR.md`、`PENDING_HOOKS_MIRROR.md`、`PATTERN_DETECTION_MIRROR.md`。
- `CH050_HANDOFF_MIRROR.md`、`CH051_HANDOFF_MIRROR.md`、`HANDOFF_CURRENT_MIRROR.md`。

### 3.14 `14_MEMORY/`
- 完整镜像 OpenViking 126 个结构化记忆节点（角色、时序、地点、章节、伏笔、知识边界、关系）。

### 3.15 `15_QA/` & `99_SYSTEM/`
- `MEMORY_FULL_BACKFILL_AUDIT_MIRROR.md`、`QA_POLICY_MIRROR.md`、`RISK_GATE_MIRROR.md`。
- `OBSIDIAN_READ_ONLY_POLICY.md`、`MIRROR_MANIFEST.yaml`。

---

## 4. Frontmatter 标准约束
每个镜像文件头部均强制注入以下元数据：
```yaml
---
source: NOVEL_OS
authority: NOVEL_OS
sync_mode: READ_ONLY
editable_in_obsidian: false
generated_at: "2026-09-02T18:37:13"
canon_version: "2.1.0"
state_version: "2.1.0"
memory_version: "2.2.0"
---
```
