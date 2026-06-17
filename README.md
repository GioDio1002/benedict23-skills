<p align="right">
  <strong>Language</strong>:
  <a href="#english">English</a> |
  <a href="#中文">中文</a>
</p>

# benedict23-skills

Normalized repository for a focused set of homemade agent skills, usable in both Codex and Claude Code.

---

## English

### Overview

This repository collects a small set of homemade agent skills that were organized for long-term maintenance and publishing. The skills are runtime-portable: they run in both Codex and Claude Code (and any agent environment that loads `SKILL.md`-style skill directories).

These skills were not written as raw copies of any single upstream project. They were shaped around real usage scenarios from daily work, then adjusted and refined with ideas, patterns, and references taken from open source projects when useful.

In short:

- scenario-driven first
- refined through actual usage
- informed by open source references
- normalized into one portable repository

### Scope

This repo currently tracks eleven local-first skills:

- `agents-init-helper`
- `daily-brief`
- `deep-search-orchestrator`
- `deep-search-pipeline`
- `deep-search-scoring`
- `explain-fastapi-endpoint`
- `multi-agent-api-dev`
- `nba-finals-radar-publishing`
- `prd-writer`
- `weekly-highlights`
- `standards-security`
- `test-validation`

### Repository Layout

```text
.
├── LICENSE
├── README.md
├── docs
│   ├── index.html
│   ├── articles/
│   └── assets/
└── src
    ├── instructions
    │   ├── README.md
    │   └── *.md
    ├── mcp
    │   ├── README.md
    │   └── *.md
    ├── prompt-framework
    │   └── *.md
    ├── manifest.json
    ├── shared
    │   └── engineering_rules.md
    └── skills
        └── <skill-name>
            ├── SKILL.md
            └── agents
                └── openai.yaml
```

### Structure Rules

- `src/skills/<skill-name>/SKILL.md` is the canonical skill document.
- `src/skills/<skill-name>/agents/openai.yaml` stores the assistant-facing prompt metadata.
- `src/mcp/` stores practical MCP server notes for the local Codex / Claude Code / Cursor workflow.
- `src/instructions/` stores instruction-layer notes for the agent environment (Codex and Claude Code).
- `src/prompt-framework/` stores reusable prompt-structuring references that are not themselves skills.
- `src/shared/` stores shared reference material used by more than one skill.
- Skills should prefer repository-relative references so the repo can be cloned anywhere.

### Runtime Compatibility (Codex + Claude Code)

- Each `SKILL.md` uses YAML front matter with `name` and `description`, which both Codex and Claude
  Code read for skill discovery and triggering.
- Skills are self-describing and reference only repository-relative paths, so the same directory works
  unchanged in either runtime.
- **Codex**: point the assistant at `src/skills/<skill-name>/` (with `agents/openai.yaml` carrying the
  prompt metadata).
- **Claude Code**: copy or symlink `src/skills/<skill-name>/` into a skills directory it scans
  (e.g. `~/.claude/skills/<skill-name>/`); the front-matter `description` drives auto-triggering.
- Keep skill bodies tool-agnostic — describe intent and workflow, not one runtime's exact tool names —
  so behavior stays consistent across both.

Current prompt-framework references include:

- `BESA_Framework.md` for bug, expectation, scope, and action driven prompts
- `ROSEAG_Framework.md` for compact role, objective, scope, expectation, action, and guardrail based requests

### Included Skills

| Skill | Purpose |
| --- | --- |
| `agents-init-helper` | Read repository-local `AGENTS.md` instructions before implementation work |
| `daily-brief` | Produce concise daily cross-repo or cross-source standup summaries |
| `deep-search-orchestrator` | Produce structured deep research reports |
| `deep-search-pipeline` | Run report generation followed by scoring |
| `deep-search-scoring` | Score deep research quality and hallucination risk |
| `explain-fastapi-endpoint` | Trace FastAPI endpoints end-to-end |
| `multi-agent-api-dev` | Orchestrate requirement analysis, code generation, validation, and security review |
| `nba-finals-radar-publishing` | Publish official-data NBA Finals radar analysis into pages and social-ready layouts |
| `prd-writer` | Standardize PRDs and product specs |
| `standards-security` | Review backend reliability, logging, and security hygiene |
| `test-validation` | Generate backend test coverage and request examples |
| `weekly-highlights` | Build compact weekly highlight summaries from recent repo activity |

### Maintenance Workflow

1. Edit the source skill under `src/skills/<skill-name>/`.
2. Keep prompt metadata in `agents/openai.yaml` aligned with the skill behavior.
3. Add shared references under `src/shared/` instead of duplicating guidance across skills.
4. Update `src/manifest.json` whenever a skill is added, removed, or renamed.

### Publishing Notes

- This repository is organized for Git-based maintenance first.
- `docs/` is the static GitHub Pages layer for this repository.
- The expected Pages URL after deployment is the repository Pages URL, typically `https://giodio1002.github.io/benedict23-skills/`.
- If these skills are later imported into another agent environment (Codex, Claude Code, or other), copy each skill directory as-is.
- Avoid absolute local filesystem paths inside `SKILL.md` files.
- `src/mcp/`, `src/instructions/`, and `src/prompt-framework/` are documentation-only directories; they are not imported as skills.

### Design System (NBA Radar Pages)

All player radar pages under `docs/` use a unified design language inspired by the huasheng.ai/parrots naturalist aesthetic:

- **Palette**: warm cream `#F8F4EE` background, `#006BB6` Knicks blue accent, `#F58426` orange secondary
- **Typography**: Playfair Display (italic serif, player names) · Inter (body) · JetBrains Mono (stats and numbers)
- **Radar SVG colors**: swapped client-side via injected JavaScript — team color `#006BB6`, reference color `#F58426`
- **Cards**: flat borders, no shadows, ↑/↓ arrows for insight sentiment (no gradient chips)
- All six radar articles (Knicks + Spurs, pages 1–3, Chinese + English) share this CSS verbatim

---

## 中文

### 仓库说明

这个仓库用于集中维护一组整理过的 homemade agent skills，方便后续持续更新、迁移和发布。这些 skills 跨运行时通用：在 Codex 和 Claude Code 中都能使用（以及任何加载 `SKILL.md` 形式 skill 目录的 agent 环境）。

这些 skills 不是照搬某一个上游项目的内容，而是按照我自己的实际使用场景逐步打磨出来的；在整理过程中，也会参考一些开源项目里的思路、模式和表达方式，再结合真实使用反馈做调整。

可以把它理解成：

- 先从使用场景出发
- 再通过日常使用不断修正
- 必要时参考开源项目
- 最后统一整理成可迁移的仓库结构

### 当前收录

目前仓库收录以下 11 个本地优先维护的 skills：

- `agents-init-helper`
- `daily-brief`
- `deep-search-orchestrator`
- `deep-search-pipeline`
- `deep-search-scoring`
- `explain-fastapi-endpoint`
- `multi-agent-api-dev`
- `nba-finals-radar-publishing`
- `prd-writer`
- `weekly-highlights`
- `standards-security`
- `test-validation`

### 目录结构

```text
.
├── LICENSE
├── README.md
├── docs
│   ├── index.html
│   ├── articles/
│   └── assets/
└── src
    ├── instructions
    │   ├── README.md
    │   └── *.md
    ├── mcp
    │   ├── README.md
    │   └── *.md
    ├── prompt-framework
    │   └── BESA_Framework.md
    ├── manifest.json
    ├── shared
    │   └── engineering_rules.md
    └── skills
        └── <skill-name>
            ├── SKILL.md
            └── agents
                └── openai.yaml
```

### 结构约定

- `src/skills/<skill-name>/SKILL.md` 是 skill 的主文档。
- `src/skills/<skill-name>/agents/openai.yaml` 用于保存面向助手的元数据和默认提示词。
- `src/mcp/` 用于整理本地 Codex / Claude Code / Cursor 工作流里实际使用的 MCP server 说明。
- `src/instructions/` 用于整理 agent 环境（Codex 和 Claude Code）的 instruction 层说明。
- `src/prompt-framework/` 用于整理可复用的 prompt 结构框架，这些内容本身不是 skill。
- `src/shared/` 用于存放多个 skill 共用的参考内容。
- skill 内部尽量使用仓库相对路径，避免依赖某台机器上的绝对路径。

### 运行时兼容（Codex + Claude Code）

- 每个 `SKILL.md` 使用带 `name` 和 `description` 的 YAML front matter，Codex 和 Claude Code 都靠它做
  skill 发现与触发。
- skill 自描述、只引用仓库相对路径，所以同一个目录在两种运行时里都能直接用，无需改动。
- **Codex**：把助手指向 `src/skills/<skill-name>/`（`agents/openai.yaml` 保存提示词元数据）。
- **Claude Code**：把 `src/skills/<skill-name>/` 复制或软链到它扫描的 skills 目录
  （如 `~/.claude/skills/<skill-name>/`）；front matter 里的 `description` 驱动自动触发。
- skill 正文保持工具无关——描述意图和流程，而不是某个运行时的具体工具名——以保证两边行为一致。

当前 `prompt-framework` 目录主要包括：

- `BESA_Framework.md`，适合围绕问题现状、预期结果、范围和执行方式来组织请求
- `ROSEAG_Framework.md`，适合用角色、目标、范围、期望、行动和约束来写紧凑需求

### Skills 说明

| Skill | 作用 |
| --- | --- |
| `agents-init-helper` | 在开始实现前优先读取仓库本地 `AGENTS.md` 指令 |
| `daily-brief` | 生成跨仓库或跨信息源的简洁日报摘要 |
| `deep-search-orchestrator` | 生成结构化深度研究报告 |
| `deep-search-pipeline` | 先生成报告，再自动做评分与质检 |
| `deep-search-scoring` | 对深度研究内容做质量与幻觉风险评分 |
| `explain-fastapi-endpoint` | 端到端追踪 FastAPI 接口执行路径 |
| `multi-agent-api-dev` | 编排需求分析、代码生成、测试验证和安全审查 |
| `nba-finals-radar-publishing` | 把官方 NBA 总决赛雷达分析整理成页面和社媒可发布内容 |
| `prd-writer` | 规范化 PRD 和产品需求文档 |
| `standards-security` | 审查后端可靠性、日志和安全卫生 |
| `test-validation` | 生成后端测试覆盖和请求示例 |
| `weekly-highlights` | 生成紧凑的周度高亮与进展摘要 |

### 维护方式

1. 直接编辑 `src/skills/<skill-name>/` 下的内容。
2. 确保 `agents/openai.yaml` 与 skill 的实际行为保持一致。
3. 能复用的公共规则放到 `src/shared/`，不要重复拷贝到多个 skill 里。
4. 新增、删除或重命名 skill 时，同步更新 `src/manifest.json`。

### 发布说明

- 这个仓库首先是为了 Git 维护和版本管理而设计的。
- `docs/` 目录同时作为这个仓库的 GitHub Pages 静态站点发布层。
- 部署后默认访问地址通常是 `https://giodio1002.github.io/benedict23-skills/`。
- 如果后续要导入到其他 agent 环境（Codex、Claude Code 或其他），可以直接复制单个 skill 目录使用。
- 尽量不要在 `SKILL.md` 里写本机绝对路径。
- `src/mcp/`、`src/instructions/` 和 `src/prompt-framework/` 只用于文档整理，不会作为 skill 直接导入。

### 设计系统（NBA 雷达页面）

`docs/` 下所有球员雷达页面使用统一设计语言，风格参考 huasheng.ai/parrots 的博物学美学：

- **色彩**：暖奶油底色 `#F8F4EE`，尼克斯蓝 `#006BB6` 主强调色，橙色 `#F58426` 辅助色
- **字体**：Playfair Display（斜体衬线，球员名）· Inter（正文）· JetBrains Mono（数据和数字）
- **雷达 SVG 颜色**：通过页面内嵌 JavaScript 在客户端替换 —— 球队色 `#006BB6`，参照线色 `#F58426`
- **卡片**：纯边框，无阴影，洞察情感用 ↑/↓ 箭头标注（不使用渐变色块）
- 全部六篇雷达文章（尼克斯 + 马刺，中英文各 3 页）共用同一套 CSS
