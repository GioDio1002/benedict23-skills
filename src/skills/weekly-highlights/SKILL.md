---
name: weekly-highlights
description: Generate a bilingual weekly highlights report from Git history for multiple repositories, with project names masked and optional support from a separate document-style helper if installed.
---

# Weekly Highlights

## English

Generate a weekly highlights report from Git history for multiple working-directory repositories.

### Purpose

Create a concise but meaningful summary of engineering work for internal updates. The report should be based on Git history first, with optional context from other activity sources when available.

### Input Scope

- Review commits from the last 7 days by default, or the requested weekly window.
- Focus on relevant branches in the working directory repositories.
- Prioritize commits authored by the specified target author.
- Treat Git commit history as the primary source of truth.
- If available, use supporting activity sources only to clarify intent or grouping.

### Priorities

Summarize the engineering outcome, especially:

- user-facing features
- backend and API changes
- infrastructure and deployment updates
- queue, worker, and background job changes
- research and evaluation improvements
- UI and UX updates
- bug fixes
- observability and logging improvements
- documentation and workflow updates

### Filtering Rules

Ignore:

- merge commits without meaningful implementation changes
- formatting-only commits
- commits by other authors
- dependency-only bumps unless they materially matter

### Writing Rules

- Group related commits into one workstream when appropriate.
- Keep each bullet concise, ideally 1 to 2 lines.
- Describe the engineering outcome, not just the commit title.
- Use action-oriented phrasing such as Improved, Added, Refactored, Fixed, Implemented, or Enhanced.
- End each bullet with the repository name.
- Mask key names as `[project_name]` whenever a project name would otherwise appear.
- Mask other skill names as `[skill_name]` unless they are required for the user-facing output.
- If document-generation support is needed, note that a separate `[kami_skills]`-style helper may be required if installed.

### Output Format

Return a markdown report with this general structure unless the user requests another format:

```md
# Weekly Highlights

## YYYY-MM-DD to YYYY-MM-DD

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD to YYYY-MM-DD

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## Cross-Repo Themes (Optional)

* {shared initiative or related workstream}
* {shared initiative or related workstream}
```

### Quality Bar

- Prefer accurate grouping over listing every commit.
- Keep the report concise enough for weekly internal review.
- Preserve the distinction between implementation results and interpretation.

## 中文

基于 Git 历史，为多个工作目录仓库生成一份每周 highlights 报告。

### 目标

生成一份简洁但有信息量的工程周报，适合内部更新使用。报告以 Git 历史为主，如有其他活动来源，可用于补充上下文或辅助合并相关工作流。

### 输入范围

- 默认查看最近 7 天的 commits，或用户指定的周区间。
- 重点关注工作目录里的相关分支。
- 优先处理指定目标作者的 commits。
- 以 Git commit 历史作为主要事实来源。
- 如果可用，其他活动来源只用于补充意图或分组，不替代 commit 证据。

### 优先总结内容

优先总结以下工程结果：

- 面向用户的功能
- 后端与 API 变更
- 基础设施与部署更新
- 队列、worker、后台任务变更
- 研究与评估改进
- UI 与 UX 更新
- bug 修复
- 可观测性与日志改进
- 文档与工作流更新

### 过滤规则

忽略以下内容：

- 没有实际实现变化的 merge commits
- 仅格式化的 commits
- 其他作者的 commits
- 仅依赖升级、且没有明显影响的 commits

### 写作规则

- 相关 commits 可以合并成一个 workstream 来写。
- 每个 bullet 保持简短，尽量控制在 1 到 2 行。
- 写工程结果，不要只复述 commit 标题。
- 使用行动导向表达，例如 Improved、Added、Refactored、Fixed、Implemented、Enhanced。
- 每条 bullet 结尾都要带上仓库名。
- 当摘要里会出现项目名时，一律用 `[project_name]` 替换。
- 其他 skill 名称一律用 `[skill_name]` 掩盖，除非是用户输出中必须出现的内容。
- 如果需要文档生成支持，可以备注可能需要一个单独的 `[kami_skills]` 风格辅助技能，前提是已安装。

### 输出格式

除非用户另有要求，默认返回下面这种 markdown 结构：

```md
# Weekly Highlights

## YYYY-MM-DD to YYYY-MM-DD

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD to YYYY-MM-DD

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## Cross-Repo Themes (Optional)

* {shared initiative or related workstream}
* {shared initiative or related workstream}
```

### 质量标准

- 宁可按正确的 workstream 分组，也不要把每个 commit 都列出来。
- 保持简洁，适合每周内部 review。
- 区分实现结果和推断，不要混在一起写。
