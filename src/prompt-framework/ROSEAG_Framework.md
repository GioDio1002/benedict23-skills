<p align="right">
  <a href="#中文">中文版</a> |
  <a href="#english">英文版</a>
</p>

# ROSEAG Framework

## English

### Purpose

This framework helps turn vague requests into clear, executable agent tasks.

Use it when you want to:

- assign software work
- write a GitHub or GitLab issue
- prepare an AI prompt
- scope research or documentation work

The goal is to remove ambiguity without making the request heavy.

### Summary

Start with a short summary when the reader needs fast context.

This first section is optional, but useful when:

- the task spans multiple steps
- the prompt will be shared or forwarded
- the user wants the goal visible at a glance

You do not need to use every section every time.

The user can include only the sections that help in the current prompt.

### ROSEAG Blocks

ROSEAG stands for:

- Role
- Objective
- Scope
- Expectation
- Action
- Guardrails

#### 1. Role

Define who the executor should act as.

Why it matters:

- sets the working mindset
- sets the quality bar
- shapes how trade-offs are made

Good:

```md
Act as a senior backend engineer focused on reliability.
```

Weak:

```md
Help me.
```

#### 2. Objective

Define the result you want.

Why it matters:

- keeps the task goal-oriented
- avoids random changes
- improves review quality

Good:

```md
Improve retry behavior for failed jobs.
```

Weak:

```md
Make it better.
```

#### 3. Scope

Define what is in and out.

Why it matters:

- prevents scope creep
- reduces risk
- keeps the request reviewable

Good:

```md
In scope:
- Retry button
- API trigger

Out of scope:
- Full UI redesign
```

Weak:

```md
Everything related.
```

#### 4. Expectation

Define what success looks like.

Why it matters:

- makes validation possible
- improves handoff quality
- sets a clear finish line

Good:

```md
- Retry works from the UI
- Logs include timestamp and request_id
```

Weak:

```md
It should work well.
```

#### 5. Action

Define the concrete work to perform.

Why it matters:

- turns intent into execution
- makes the task easier to route
- reduces hand-wavy requests

Good:

```md
- Add retry button
- Call retry API
- Add logging
```

Weak:

```md
Fix it.
```

#### 6. Guardrails

Define the rules and constraints.

Why it matters:

- blocks common mistakes
- protects unrelated areas
- keeps execution disciplined

Good:

```md
Guardrails:
- Use PostgreSQL
- Add logging
- Refactor unrelated code
```

Weak:

```md
Be careful.
```

### Full Template

```md
## Summary

## Role
Act as:

## Objective
The goal is:

## Scope
In scope:
Out of scope:

## Expectation
Success means:

## Action
Please:

## Guardrails
Rules:
```

### Why It Works

This framework separates the main parts of a strong request:

- summary
- role
- goal
- boundary
- validation
- execution
- constraints

That makes requests easier to understand, safer to execute, and easier to review.

### Best Fits

This framework is especially useful for:

- AI prompts
- engineering tasks
- bug tickets
- research plans
- documentation requests

---

## 中文

### 用途

这个框架用于把模糊需求整理成清晰、可执行的 agent 任务。

适用于：

- 分配工程任务
- 写 GitHub 或 GitLab issue
- 编写 AI prompt
- 规划研究或文档工作

它的目标不是把需求写得很重，而是把歧义压到最低。

### Summary

如果读者需要先快速理解上下文，可以先写一个简短摘要。

这个开头不是强制项，但在下面这些场景里很有用：

- 任务包含多个步骤
- prompt 会被转发或复用
- 需要让目标一眼就清楚

你不需要每次都把所有模块全部写上。

用户可以只选择当前 prompt 真正需要的部分。

### ROSEAG 模块

ROSEAG 代表：

- Role
- Objective
- Scope
- Expectation
- Action
- Guardrails

#### 1. 角色

定义执行者应该以什么角色来思考和执行。

为什么重要：

- 决定工作视角
- 决定质量标准
- 影响取舍方式

好例子：

```md
作为一名关注稳定性的高级后端工程师。
```

弱例子：

```md
帮我做一下。
```

#### 2. 目标

定义你真正想达成的结果。

为什么重要：

- 让任务围绕目标展开
- 避免随意修改
- 提高评审质量

好例子：

```md
优化失败任务的重试机制。
```

弱例子：

```md
优化一下。
```

#### 3. 范围

定义什么在范围内，什么不在范围内。

为什么重要：

- 防止需求膨胀
- 降低无关改动风险
- 让任务更容易评审

好例子：

```md
包含：
- 重试按钮
- API 触发

不包含：
- 整体 UI 重做
```

弱例子：

```md
所有相关的都处理。
```

#### 4. 期望

定义什么叫成功。

为什么重要：

- 便于验证
- 提高手交与交接质量
- 明确完成标准

好例子：

```md
- 可以从 UI 正常触发重试
- 日志包含 timestamp 和 request_id
```

弱例子：

```md
差不多能用就行。
```

#### 5. 行动

定义具体要执行的工作。

为什么重要：

- 把意图变成动作
- 让任务更容易路由
- 减少空泛表达

好例子：

```md
- 添加重试按钮
- 调用重试 API
- 增加日志
```

弱例子：

```md
修一下。
```

#### 6. Guardrails

定义规则和约束。

为什么重要：

- 避免常见错误
- 保护无关区域
- 保持执行纪律

好例子：

```md
约束：
- 使用 PostgreSQL
- 增加日志
- 重构无关代码
```

弱例子：

```md
注意一点。
```

### 完整模板

```md
## Summary

## 角色
作为：

## 目标
目标是：

## 范围
包含：
不包含：

## 期望
成功标准：

## 行动
请执行：

## Guardrails
规则：
```

### 为什么有效

这个框架把强需求里最常混在一起的几个部分拆开了：

- 摘要
- 角色
- 目标
- 边界
- 验证
- 执行
- 约束

这样需求会更容易理解、更安全执行，也更容易评审。

### 适用场景

这个框架特别适合：

- AI prompts
- 工程任务
- 缺陷工单
- 调研计划
- 文档请求
