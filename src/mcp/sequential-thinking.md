# sequential-thinking MCP In Codex

## What it is

`sequential-thinking` is an MCP server for stepwise reasoning. It supports multi-step thought chains, revisions, branches, and dynamic extension of the reasoning process.

## Why install it in Codex

- useful for debugging, architecture trade-offs, and ambiguous problem analysis
- adds an explicit reasoning tool when a task should be decomposed carefully
- helps keep structured thought state outside the free-form answer

## Current local setup

```toml
[mcp_servers."sequential-thinking"]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-sequential-thinking"]
```

## Latest official guidance

The official reference docs still support the `npx -y @modelcontextprotocol/server-sequential-thinking` install path. The README also includes a Codex CLI example.

## Recommended Codex install pattern

```toml
[mcp_servers."sequential-thinking"]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-sequential-thinking"]
```

Equivalent Codex CLI command:

```bash
codex mcp add sequential-thinking npx -y @modelcontextprotocol/server-sequential-thinking
```

## Good use cases

- root-cause analysis
- planning before writing code
- breaking down multi-step technical decisions
- comparing branches of reasoning before choosing an implementation

## Example prompts

- `用 sequential-thinking 帮我分步骤分析这个 bug。`
- `把这个系统设计问题拆成 6 个思考步骤。`
- `先列出两条不同的方案分支，再比较权衡。`

## Caveats

- it is easy to overuse on simple tasks
- explicit reasoning steps cost time and tokens
- teams should keep a clear line between structured analysis and user-facing final output

## Why this is useful for Codex specifically

Codex often needs to move from uncertainty to implementation. `sequential-thinking` is valuable when the task should be decomposed before changes are made.

## Sources

- MCP reference server README: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
