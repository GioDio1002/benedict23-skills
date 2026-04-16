# ruflo MCP In Codex

## What it is

Ruflo is a multi-agent orchestration platform that exposes a large MCP tool surface for coordination, routing, memory, browser work, workflows, diagnostics, and more.

## Why install it in Codex

- extends Codex with orchestration and cross-agent coordination primitives
- adds memory, routing, browser helpers, workflow execution, and task management in one MCP server
- useful when you want Codex to operate as part of a broader multi-agent system

## Current local setup

```toml
[mcp_servers.ruflo]
command = "npx"
args = ["ruflo", "mcp", "start"]
```

The current local config also pins approval rules for selected Ruflo tools.

## Latest official guidance

Ruflo's current README shows two relevant Codex paths:

- initialize Codex integration with `npx ruflo@latest init --codex`
- manually add the MCP server with `codex mcp add ruflo -- npx ruflo mcp start`

The broader README now tends to use `ruflo@latest` in install examples, so that is the safer greenfield choice.

## Recommended Codex install patterns

### Basic MCP registration

```toml
[mcp_servers.ruflo]
command = "npx"
args = ["ruflo@latest", "mcp", "start"]
```

### Full Codex-oriented initialization

```bash
npx ruflo@latest init --codex
```

### Manual Codex CLI path

```bash
codex mcp add ruflo -- npx ruflo@latest mcp start
```

## Good use cases

- orchestrate multiple workers or swarms
- maintain richer long-term memory and routing than a minimal MCP stack
- run workflows, browser helpers, coordination, and diagnostics from one place
- connect Codex execution with a broader automation system

## Example prompts

- `用 ruflo 建一个 parallel workflow，把测试、文档、review 拆开跑。`
- `检查当前 swarm 状态，看看有没有 agent 卡住。`
- `创建一个 task，再分配给合适的 agent。`

## Caveats

- Ruflo is powerful but large; its tool surface can be much heavier than a single-purpose MCP server
- local examples in the README mix Claude Code, Codex, and broader orchestration workflows, so you should standardize the subset you actually want to use
- version drift between `ruflo` and `ruflo@latest` matters for reproducibility

## Why this is useful for Codex specifically

Codex is good at direct implementation. Ruflo adds orchestration, persistent coordination, and a broader automation substrate around that executor role.

## Sources

- Ruflo README: https://github.com/ruvnet/ruflo
