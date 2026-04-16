<p align="right">
  <strong>Language</strong>:
  <a href="#english">English</a> |
  <a href="#中文">中文</a>
</p>

# homemade-skills

Normalized repository for a focused set of homemade Codex skills.

---

## English

### Overview

This repository collects a small set of homemade Codex skills that were organized for long-term maintenance and publishing.

These skills were not written as raw copies of any single upstream project. They were shaped around real usage scenarios from daily work, then adjusted and refined with ideas, patterns, and references taken from open source projects when useful.

In short:

- scenario-driven first
- refined through actual usage
- informed by open source references
- normalized into one portable repository

### Scope

This repo currently tracks nine local-first skills:

- `agents-init-helper`
- `deep-search-orchestrator`
- `deep-search-pipeline`
- `deep-search-scoring`
- `explain-fastapi-endpoint`
- `multi-agent-api-dev`
- `prd-writer`
- `standards-security`
- `test-validation`

### Repository Layout

```text
.
├── LICENSE
├── README.md
└── src
    ├── instructions
    │   ├── README.md
    │   └── *.md
    ├── mcp
    │   ├── README.md
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
- `src/mcp/` stores practical MCP server notes for the local Codex/Cursor workflow.
- `src/instructions/` stores instruction-layer notes for the current Codex environment.
- `src/shared/` stores shared reference material used by more than one skill.
- Skills should prefer repository-relative references so the repo can be cloned anywhere.

### Included Skills

| Skill | Purpose |
| --- | --- |
| `agents-init-helper` | Read repository-local `AGENTS.md` instructions before implementation work |
| `deep-search-orchestrator` | Produce structured deep research reports |
| `deep-search-pipeline` | Run report generation followed by scoring |
| `deep-search-scoring` | Score deep research quality and hallucination risk |
| `explain-fastapi-endpoint` | Trace FastAPI endpoints end-to-end |
| `multi-agent-api-dev` | Orchestrate requirement analysis, code generation, validation, and security review |
| `prd-writer` | Standardize PRDs and product specs |
| `standards-security` | Review backend reliability, logging, and security hygiene |
| `test-validation` | Generate backend test coverage and request examples |

### Maintenance Workflow

1. Edit the source skill under `src/skills/<skill-name>/`.
2. Keep prompt metadata in `agents/openai.yaml` aligned with the skill behavior.
3. Add shared references under `src/shared/` instead of duplicating guidance across skills.
4. Update `src/manifest.json` whenever a skill is added, removed, or renamed.

### Publishing Notes

- This repository is organized for Git-based maintenance first.
- If these skills are later imported into another Codex or agent environment, copy each skill directory as-is.
- Avoid absolute local filesystem paths inside `SKILL.md` files.
- `src/mcp/` and `src/instructions/` are documentation-only directories; they are not imported as skills.

---

## 中文

### 仓库说明

这个仓库用于集中维护一组整理过的 homemade Codex skills，方便后续持续更新、迁移和发布。

这些 skills 不是照搬某一个上游项目的内容，而是按照我自己的实际使用场景逐步打磨出来的；在整理过程中，也会参考一些开源项目里的思路、模式和表达方式，再结合真实使用反馈做调整。

可以把它理解成：

- 先从使用场景出发
- 再通过日常使用不断修正
- 必要时参考开源项目
- 最后统一整理成可迁移的仓库结构

### 当前收录

目前仓库收录以下 9 个本地优先维护的 skills：

- `agents-init-helper`
- `deep-search-orchestrator`
- `deep-search-pipeline`
- `deep-search-scoring`
- `explain-fastapi-endpoint`
- `multi-agent-api-dev`
- `prd-writer`
- `standards-security`
- `test-validation`

### 目录结构

```text
.
├── LICENSE
├── README.md
└── src
    ├── instructions
    │   ├── README.md
    │   └── *.md
    ├── mcp
    │   ├── README.md
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

### 结构约定

- `src/skills/<skill-name>/SKILL.md` 是 skill 的主文档。
- `src/skills/<skill-name>/agents/openai.yaml` 用于保存面向助手的元数据和默认提示词。
- `src/mcp/` 用于整理当前本地 Codex/Cursor 工作流里实际使用的 MCP server 说明。
- `src/instructions/` 用于整理当前 Codex 环境中的 instruction 层说明。
- `src/shared/` 用于存放多个 skill 共用的参考内容。
- skill 内部尽量使用仓库相对路径，避免依赖某台机器上的绝对路径。

### Skills 说明

| Skill | 作用 |
| --- | --- |
| `agents-init-helper` | 在开始实现前优先读取仓库本地 `AGENTS.md` 指令 |
| `deep-search-orchestrator` | 生成结构化深度研究报告 |
| `deep-search-pipeline` | 先生成报告，再自动做评分与质检 |
| `deep-search-scoring` | 对深度研究内容做质量与幻觉风险评分 |
| `explain-fastapi-endpoint` | 端到端追踪 FastAPI 接口执行路径 |
| `multi-agent-api-dev` | 编排需求分析、代码生成、测试验证和安全审查 |
| `prd-writer` | 规范化 PRD 和产品需求文档 |
| `standards-security` | 审查后端可靠性、日志和安全卫生 |
| `test-validation` | 生成后端测试覆盖和请求示例 |

### 维护方式

1. 直接编辑 `src/skills/<skill-name>/` 下的内容。
2. 确保 `agents/openai.yaml` 与 skill 的实际行为保持一致。
3. 能复用的公共规则放到 `src/shared/`，不要重复拷贝到多个 skill 里。
4. 新增、删除或重命名 skill 时，同步更新 `src/manifest.json`。

### 发布说明

- 这个仓库首先是为了 Git 维护和版本管理而设计的。
- 如果后续要导入到其他 Codex 或 agent 环境，可以直接复制单个 skill 目录使用。
- 尽量不要在 `SKILL.md` 里写本机绝对路径。
- `src/mcp/` 和 `src/instructions/` 只用于文档整理，不会作为 skill 直接导入。
