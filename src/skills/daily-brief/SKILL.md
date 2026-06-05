---
name: daily-brief
description: Generate a concise bilingual standup summary from recent Git commit history across local repositories, with optional cross-reference support from internal activity sources. Use when the user wants a daily engineering brief grounded in commit activity and wants project names masked.
---

# Daily Brief

## English

Use this skill to generate a concise engineering standup summary from Git commit history across the last 3 natural working days in UTC+8.

### Input Expectations

- Review commits from the staging and active feature branches in the working directory repositories.
- Focus only on commits authored by the specified target author.
- Treat Git history as the primary source of truth.
- If available, cross-reference relevant internal activity sources for context, but do not replace commit evidence with activity alone.

### Priorities

Summarize meaningful engineering outcomes, especially:

- user-facing features
- backend and API logic changes
- infrastructure or deployment updates
- queue, worker, or background job changes
- deep research or evaluation improvements
- UI and UX updates
- bug fixes
- observability and logging improvements
- documentation or workflow updates

### Filtering Rules

Ignore:

- merge commits without meaningful implementation changes
- formatting-only commits
- commits by other authors
- dependency-only bumps unless they are impactful

### Writing Rules

- Group related commits into one logical workstream when appropriate.
- Keep each bullet concise, 1 to 2 lines max.
- Describe the engineering outcome, not just the commit title.
- End each bullet with the repository name.
- Use action-oriented wording such as Improved, Added, Refactored, Fixed, Implemented, or Enhanced.
- Mask project names as `[project_name]` whenever project names would otherwise appear in the summary text.

### Output Format

Return exactly this structure unless the user requests otherwise:

```md
# Standup Summary

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## Cross-Repo Themes (Optional)

* {shared initiative or related workstream}
* {shared initiative or related workstream}
```

### Quality Bar

- Prefer a small number of accurate bullets over a long noisy list.
- Combine small iterative commits into one coherent update when they clearly belong together.
- Keep the result suitable for internal team updates.

## 中文

使用这个 skill 时，要基于 Git commit 历史生成一份简洁但有信息量的工程日报，范围是 UTC+8 最近 3 个自然工作日。

### 输入要求

- 重点查看工作目录内各仓库的 staging 分支和活跃 feature 分支上的 commit。
- 只关注指定目标作者的 commits。
- 以 Git 历史作为主要事实来源。
- 如果可以，再参考内部活动来源补充上下文，但不要让活动记录替代 commit 证据。

### 优先总结内容

优先归纳以下类型的工程结果：

- 面向用户的功能
- 后端和 API 逻辑变化
- 基础设施或部署更新
- 队列、worker、后台任务变化
- 深度研究或评估能力改进
- UI 和 UX 更新
- bug 修复
- 可观测性和日志改进
- 文档或工作流更新

### 过滤规则

忽略以下内容：

- 没有实际实现变化的 merge commits
- 仅格式化的 commits
- 其他作者的 commits
- 只有依赖升级、且没有明显影响的 commits

### 写作规则

- 相关 commits 可以合并为一个逻辑 workstream 来写。
- 每个 bullet 保持简短，最多 1 到 2 行。
- 写工程结果，不要只写 commit 标题。
- 每条 bullet 结尾都要带上仓库名。
- 优先使用行动导向的表达，例如 Improved、Added、Refactored、Fixed、Implemented、Enhanced。
- 当摘要文本里会直接出现 project name 时，统一用 `[project_name]` 替换。

### 输出格式

默认返回下面这个结构，除非用户另有要求：

```md
# Standup Summary

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## YYYY-MM-DD Day

* {meaningful summarized change} — {repo}
* {meaningful summarized change} — {repo}

## Cross-Repo Themes (Optional)

* {shared initiative or related workstream}
* {shared initiative or related workstream}
```

### 质量标准

- 宁可少而准，不要多而杂。
- 如果多个小 commit 明显属于同一件事，可以合并成一个 workstream 来写。
- 结果要适合内部团队的 daily standup 更新。
