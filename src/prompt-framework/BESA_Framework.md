<p align="right">
  <a href="#中文">中文版</a> |
  <a href="#english">英文版</a>
</p>

# BESA Framework

## English

## Purpose

The BESA framework is a practical prompt structure for asking an agent to help with real software work.

It is designed to reduce ambiguity, speed up investigation, and make it easier to route the request into the right skills, tools, or execution path.

Use it when you want an agent to:

- investigate a bug
- explain bad behavior
- debug a flow
- review code
- plan work
- build or change something

The core idea is simple:

- describe what is wrong now
- describe what should happen instead
- define the scope and skill triggers
- define the working mode or procedure

## BESA = Four Prompt Blocks

## B: Bug / Bad Behavior

Describe the current situation.

This block answers:

- what is broken
- what is confusing
- what is happening now
- where it was observed
- whether a screenshot, logs, or repro exists

Useful details:

- exact error message
- observed symptoms
- URL, screen, file, or workflow step
- repro steps
- optional screenshot or stack trace

Example:

```md
## B: Bug / Bad Behavior

The login modal closes after submit, but the user is not logged in.
Observed on the web app settings page after clicking "Sign in".
No visible error toast appears.
Browser console shows a 401 from the session endpoint.
Screenshot optional.
```

## E: Expected Behavior

Describe the intended result.

This block answers:

- what success looks like
- what the user expected
- what should happen after the fix
- what the end goal is

Useful details:

- expected UI behavior
- expected backend behavior
- expected data or status change
- optional screenshot of correct state

Example:

```md
## E: Expected Behavior

After submitting valid credentials, the modal should close only after the session is created.
The user avatar should appear in the header.
The session endpoint should return 200 and the protected page should load normally.
```

## S: Scope

Define the work boundary.

This block answers:

- is this single-repo or cross-repo
- which systems or files are in scope
- which skills or workflows should be triggered
- what should stay out of scope

Useful details:

- repo name or repos involved
- frontend/backend/db/infra boundaries
- files, directories, or services to inspect first
- skills that should be invoked
- constraints such as "no dependency changes"

Example:

```md
## S: Scope

Single repo.
Focus on auth UI, session API client, and related tests.
Inspect `src/auth/`, `src/api/`, and login flow tests first.
Trigger debugging, investigate, and test-validation style workflows.
Do not touch unrelated billing code.
```

## A: Action / Approach

Define how the agent should work.

This block answers:

- should the agent investigate first
- should it plan before coding
- should it debug, review, or build
- what sequence of actions should happen

This is the execution control block.

Common action modes:

- Investigation
- Plan
- Debug
- Code Review
- Build

You can also define a step sequence.

Example:

```md
## A: Action / Approach

1. Reproduce the failure.
2. Trace the auth request path.
3. Identify whether the issue is UI state, API usage, or session persistence.
4. Propose the smallest safe fix.
5. Update tests.
6. Summarize root cause and behavior change.
```

## Why BESA Works Well With Agents

BESA is useful because it separates four concerns that are often mixed together in weak prompts:

- observed reality
- desired outcome
- execution boundary
- operating procedure

This separation helps an agent avoid common failure modes:

- fixing the wrong thing
- changing too much
- missing key repos or files
- choosing the wrong workflow
- jumping into implementation before understanding the problem

## Partial Composition

BESA does not have to be used in full every time.

It can be broken into smaller combinations depending on the task.

## BEA

Use `BEA` when:

- the scope is obvious
- only one repo is involved
- the agent already knows the working boundary

Example:

```md
B: Search results are timing out after 10 seconds.
E: Queries should return within 2 seconds for common filters.
A: Investigate, benchmark the current query, identify the bottleneck, and propose a minimal fix.
```

## BSA

Use `BSA` when:

- the goal is implied
- the most important part is routing and work mode
- you need to constrain an agent before it starts

Example:

```md
B: CI is failing after the latest auth changes.
S: Single repo, auth module only, no dependency upgrades.
A: Review the failing tests, identify the regression, patch the smallest safe fix, and rerun relevant checks.
```

## ESA

Use `ESA` when:

- there is no bug yet
- this is new work or an enhancement
- you want to define the target, scope, and process

Example:

```md
E: Add a reusable loading state for dashboard widgets.
S: Single repo, frontend only, no API changes.
A: Inspect the current widget pattern, propose one reusable component, implement it, and update affected views.
```

## Suggested Procedure Types For A

You can standardize the `A` block into one of these modes:

### Investigation

Use when the problem is unclear.

```md
A: Investigate first. Gather evidence, locate the failing path, and explain likely root cause before proposing changes.
```

### Plan

Use when the task is large or architectural.

```md
A: Create a short implementation plan first, including files to touch, risks, and validation steps. Do not code before the plan is clear.
```

### Debug

Use when the issue is reproducible and needs root cause isolation.

```md
A: Reproduce the bug, isolate the failing component, confirm root cause, implement the smallest safe fix, and verify with targeted tests.
```

### Code Review

Use when the primary job is review rather than implementation.

```md
A: Review the diff for correctness, regressions, missing tests, and operational risks. Findings first, summary second.
```

### Build

Use when the feature is understood and implementation should proceed.

```md
A: Implement the requested change, keep scope tight, add or update validation, and summarize behavior changes.
```

## Full BESA Template

Copy and fill this in:

```md
# BESA Prompt

## B: Bug / Bad Behavior
- Current situation:
- Repro:
- Evidence:
- Screenshot/logs:

## E: Expected Behavior
- Desired outcome:
- Success condition:
- Optional reference state:

## S: Scope
- Repo scope:
- File/module scope:
- Required skills or workflows:
- Out of scope:

## A: Action / Approach
1. {Reproduce the issue}
2. {Trace the failing path}
3. {Apply the smallest safe fix}
4. {Verify with targeted checks}
```

## Compact BESA Template

Use this for faster requests:

```md
B:
E:
S:
A:
```

## Example 1: Bugfix Prompt

```md
## B: Bug / Bad Behavior
The profile save button spins forever after clicking submit.
Observed on the account settings page.
Network tab shows the PATCH request succeeds, but the UI never exits loading state.

## E: Expected Behavior
After a successful PATCH response, the spinner should stop and a success state should appear.

## S: Scope
Single repo.
Focus on profile form state and save handler.
Do not modify unrelated account deletion flows.

## A: Action / Approach
1. Reproduce the issue.
2. Trace the loading-state lifecycle.
3. Fix the smallest safe state bug.
4. Add or update a regression test.
5. Summarize root cause.
```

## Example 2: Cross-Repo Prompt

```md
## B: Bug / Bad Behavior
Webhook delivery succeeds from the sender service, but the receiver repo does not process the event.

## E: Expected Behavior
An accepted webhook should create a processing record and trigger the downstream job.

## S: Scope
Cross-repo.
Inspect sender webhook client and receiver ingestion handler.
Trigger investigation and cross-repo debugging workflow.

## A: Action / Approach
1. Compare payload shape between sender and receiver.
2. Confirm auth and signature validation behavior.
3. Identify where the event is dropped.
4. Propose the smallest fix across the correct repo boundary.
```

## Example 3: Build Prompt

```md
## E: Expected Behavior
Add a reusable empty state component for dashboard modules.

## S: Scope
Single repo.
Frontend only.
Use existing component conventions.

## A: Action / Approach
1. Review current empty-state patterns.
2. Propose one reusable component shape.
3. Implement it in the shared UI layer.
4. Replace two duplicated instances.
5. Verify visual and behavioral consistency.
```

## Operating Notes

- If the problem is unknown, make `A` investigation-heavy.
- If the task is large, make `A` plan-first.
- If multiple systems are involved, make `S` explicit and narrow.
- If there is no bug, `B` can be omitted and you can use `ESA`.
- If there is a bug but the scope is obvious, `BEA` is often enough.

## Recommended Use

Use BESA when you want an agent request to feel:

- operational
- debuggable
- reviewable
- composable
- reusable across repos and workflows

The framework is intentionally simple enough to write quickly, but structured enough to produce better agent behavior than an unscoped paragraph prompt.

---

## 中文

## 用途

BESA 是一个偏工程执行的 prompt 框架，适合让 agent 处理真实的软件工作。

它的目标是：

- 减少歧义
- 提高排查速度
- 更容易把请求路由到正确的技能、工具或执行路径

适用于：

- 排查 bug
- 解释异常行为
- 调试流程
- 做代码评审
- 规划工作
- 实现或修改功能

核心思路很简单：

- 说清楚现在哪里有问题
- 说清楚理想结果是什么
- 说清楚范围和边界
- 说清楚 agent 应该如何推进

## BESA = 四个模块

## B: Bug / Bad Behavior

描述当前问题。

这个模块用于回答：

- 现在哪里坏了
- 具体哪里让人困惑
- 现在实际发生了什么
- 在哪里观察到这个问题
- 是否已经有截图、日志或复现步骤

建议包含：

- 精确报错
- 观察到的症状
- 页面、URL、文件或流程节点
- 复现步骤
- 可选的截图或堆栈

示例：

```md
## B: Bug / Bad Behavior

登录弹窗提交后会关闭，但用户并没有真正登录。
问题出现在 web 设置页点击 “Sign in” 之后。
页面没有出现报错提示。
浏览器控制台显示 session 接口返回 401。
可附截图。
```

## E: Expected Behavior

描述期望结果。

这个模块用于回答：

- 什么才算成功
- 用户原本期待什么
- 修复后应该发生什么
- 最终目标是什么

建议包含：

- 期望的 UI 表现
- 期望的后端行为
- 期望的数据或状态变化
- 可选的正确状态参考图

示例：

```md
## E: Expected Behavior

提交正确凭证后，只有在 session 创建成功后弹窗才关闭。
页头应显示用户头像。
session 接口应返回 200，受保护页面应正常加载。
```

## S: Scope

定义工作边界。

这个模块用于回答：

- 是单仓库还是跨仓库
- 哪些系统、文件或目录在范围内
- 应该触发哪些 skill 或 workflow
- 哪些内容必须排除在外

建议包含：

- 仓库名称
- 前端、后端、数据库、基础设施边界
- 优先检查的文件、目录或服务
- 需要触发的技能
- 例如“不允许改依赖”这类约束

示例：

```md
## S: Scope

单仓库。
聚焦 auth UI、session API client 和相关测试。
优先检查 `src/auth/`、`src/api/` 和登录流测试。
触发 debugging、investigate 和 test-validation 风格流程。
不要改动无关的 billing 代码。
```

## A: Action / Approach

定义 agent 的工作方式。

这个模块用于回答：

- 是否先调查再改
- 是否先出计划再写代码
- 是调试、评审还是直接实现
- 具体执行顺序是什么

这就是执行控制模块。

常见模式：

- Investigation
- Plan
- Debug
- Code Review
- Build

也可以直接写成步骤序列。

示例：

```md
## A: Action / Approach

1. 先复现问题。
2. 追踪 auth 请求链路。
3. 判断问题出在 UI state、API 调用还是 session 持久化。
4. 提出最小且安全的修复方案。
5. 更新测试。
6. 总结根因和行为变化。
```

## 为什么 BESA 适合 Agent

BESA 的价值在于，它把弱 prompt 里经常混在一起的四件事拆开了：

- 当前现实
- 目标结果
- 范围边界
- 执行方式

这样可以减少一些常见失误：

- 修错问题
- 改动过大
- 漏掉关键仓库或文件
- 选错工作流
- 还没理解问题就开始写代码

## 部分组合

BESA 不需要每次完整使用。

可以根据任务只保留必要模块。

## BEA

适用于：

- 范围已经很明显
- 只涉及一个仓库
- agent 已经知道边界

示例：

```md
B: 搜索结果在 10 秒后超时。
E: 常见过滤条件下查询应在 2 秒内返回。
A: 先调查，给当前查询做基准，找出瓶颈，再提出最小修复方案。
```

## BSA

适用于：

- 目标已经隐含在上下文里
- 最重要的是约束范围和工作方式
- 你需要在 agent 开工前把边界锁紧

示例：

```md
B: 最近 auth 改动后，CI 开始失败。
S: 单仓库，仅 auth 模块，不升级依赖。
A: 先看失败测试，找出回归点，做最小安全修复，再跑相关检查。
```

## ESA

适用于：

- 不是 bug，而是新工作
- 目标是增强或新增
- 你想先定义目标、范围和过程

示例：

```md
E: 给 dashboard widgets 增加可复用的 loading state。
S: 单仓库，仅前端，不改 API。
A: 先看现有 widget 模式，提一个可复用组件，再实现并更新相关视图。
```

## A 模块推荐模式

你可以把 `A` 标准化为下面几种模式：

### Investigation

适用于问题还不清晰时。

```md
A: 先调查。收集证据，定位失败路径，在提出修改前先解释最可能的根因。
```

### Plan

适用于任务较大或偏架构时。

```md
A: 先给一个简短实现计划，包含会改哪些文件、主要风险和验证步骤。计划清晰前不要编码。
```

### Debug

适用于问题可复现且需要隔离根因时。

```md
A: 先复现 bug，隔离失败组件，确认根因，做最小安全修复，并用针对性测试验证。
```

### Code Review

适用于主要任务是评审而不是实现时。

```md
A: 先评审 diff 的正确性、回归风险、缺失测试和运维风险。先给 findings，再给总结。
```

### Build

适用于需求已经清楚，可以直接实现时。

```md
A: 实现请求的改动，保持范围紧凑，补充或更新验证，并总结行为变化。
```

## 完整 BESA 模板

复制后直接填写：

```md
# BESA Prompt

## B: Bug / Bad Behavior
- 当前情况：
- 复现方式：
- 证据：
- 截图/日志：

## E: Expected Behavior
- 目标结果：
- 成功标准：
- 可选参考状态：

## S: Scope
- 仓库范围：
- 文件/模块范围：
- 需要触发的 skills 或 workflows：
- 不在范围内：

## A: Action / Approach
1. {先复现问题}
2. {再追踪失败路径}
3. {做最小且安全的修复}
4. {用针对性检查验证}
```

## 紧凑模板

适合更快的请求：

```md
B:
E:
S:
A:
```

## 示例 1：Bugfix Prompt

```md
## B: Bug / Bad Behavior
点击提交后，profile 保存按钮会一直 loading。
问题出现在 account settings 页面。
网络面板显示 PATCH 请求成功，但 UI 没有退出 loading 状态。

## E: Expected Behavior
PATCH 成功后，loading 应停止，并显示成功状态。

## S: Scope
单仓库。
聚焦 profile form state 和 save handler。
不要改动无关的 account deletion 流程。

## A: Action / Approach
1. 复现问题。
2. 追踪 loading state 生命周期。
3. 修复最小的状态问题。
4. 增加或更新回归测试。
5. 总结根因。
```

## 示例 2：Cross-Repo Prompt

```md
## B: Bug / Bad Behavior
sender service 成功发出 webhook，但 receiver repo 没有处理事件。

## E: Expected Behavior
webhook 被接受后，应创建 processing record，并触发下游任务。

## S: Scope
跨仓库。
检查 sender webhook client 和 receiver ingestion handler。
触发 investigation 和 cross-repo debugging workflow。

## A: Action / Approach
1. 对比 sender 和 receiver 的 payload 结构。
2. 确认 auth 和 signature validation 行为。
3. 找出事件在哪一层被丢弃。
4. 在正确的仓库边界内提出最小修复方案。
```

## 示例 3：Build Prompt

```md
## E: Expected Behavior
为 dashboard modules 增加一个可复用的 empty state 组件。

## S: Scope
单仓库。
仅前端。
遵循现有组件约定。

## A: Action / Approach
1. 查看当前 empty-state 模式。
2. 提一个可复用组件形态。
3. 在共享 UI 层实现。
4. 替换两个重复实例。
5. 验证视觉和行为一致性。
```

## 使用提示

- 如果问题不明确，就让 `A` 更偏 investigation。
- 如果任务较大，就让 `A` 先 plan。
- 如果涉及多个系统，就把 `S` 写得更明确。
- 如果不是 bug，可以省略 `B`，直接用 `ESA`。
- 如果有 bug 但范围很清楚，通常 `BEA` 就够了。

## 推荐使用场景

当你希望 agent 请求具备这些特点时，适合使用 BESA：

- 可执行
- 可排查
- 可评审
- 可组合
- 可跨仓库复用

这个框架足够简单，写起来不会太重，但比一整段没有边界的自然语言 prompt 更容易产出稳定的 agent 行为。
