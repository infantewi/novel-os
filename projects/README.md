# NOVEL OS — 项目工作区 (Projects Sandbox Workspace)

欢迎来到 NOVEL OS 的作品沙盒目录！

---

## 隐私与安全保护声明

> [!IMPORTANT]
> **作者著作权保护**：本目录已在根目录 `.gitignore` 中配置全面排除规则。  
> 您在此目录下创建、起草或导入的任何长篇小说、短篇故事、大纲设定与正文稿件，**均严格保留在您的本地磁盘，绝不会被 Git 追踪或推送到远程仓库**。

---

## 如何创建新作品沙盒？

使用 NOVEL OS 提供的工程初始化脚本或 Agent 技能命令即可快速创建独立沙盒：

### 方法 1：使用 Python CLI 快速创建

```bash
# 语法：python scripts/init_project.py --title <书名> --genre <题材>
python scripts/init_project.py --title "我的第一部玄幻小说" --genre "玄幻"
```

该命令将在 `projects/` 下生成规范的沙盒目录结构：

```text
projects/<书名>/
├── 01_CANON/           # 设定集与世界观（主角卡、力量体系、势力谱系）
├── 02_OUTLINE/         # 雪花工程大纲（三幕骨架、卷分章细纲、场景表）
├── 03_PRODUCTION/      # 生产流水线中间件（预写卡、草稿、审查报告）
├── 04_STATE/           # 运行时状态机与伏笔追踪
├── 06_HANDOFF/         # 章节交接快照
└── 正文/               # 最终定稿章节 (.md / .txt)
```

### 方法 2：使用 AI 写作技能向导

在支持的智能体终端（如 Claude Code / Antigravity）中运行：
- `/story-setup`：跟随交互式向导完成题材选型、金手指设计与开篇立项。
- `/webnovel-init`：自动执行环境与沙盒配置。

---

## 多题材沙盒物理隔离原则

NOVEL OS 严格执行**零交叉污染 (Zero Contamination)** 原则：
- 每一本小说拥有独占的设定圣经、人物关系网与编年史；
- OpenViking 记忆检索库自动按项目命名空间隔离，绝不发生世界观串扰。
