# GitHub MCP In Codex

## What it is

GitHub MCP connects the agent to GitHub repositories, issues, pull requests, code search, workflows, and related platform data.

## Why install it in Codex

- lets Codex connect local code work with hosted repository state
- useful for issue triage, PR review, and release operations
- enables repo metadata and workflow inspection without leaving the coding session

## Current local setup

The current local Codex setup uses an older package:

```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]

[mcp_servers.github.env]
GITHUB_TOKEN = "${GITHUB_TOKEN}"
```

## Latest official guidance

GitHub has moved active development to the official `github/github-mcp-server` project.

Current official options are:

- remote hosted MCP: `https://api.githubcopilot.com/mcp/`
- local Docker image: `ghcr.io/github/github-mcp-server`
- local binary built from source

This means the current local Codex config is functional for parity, but it does not match GitHub's current official preferred implementation.

## Recommended Codex install patterns

### Pattern A: keep parity with the current local setup

Use this only when exact environment parity matters more than following the newest official GitHub server:

```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]

[mcp_servers.github.env]
GITHUB_TOKEN = "${GITHUB_TOKEN}"
```

### Pattern B: migrate to the current official local server

```toml
[mcp_servers.github]
command = "docker"
args = ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"]

[mcp_servers.github.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_TOKEN}"
```

If you build the binary locally instead of Docker:

```toml
[mcp_servers.github]
command = "/absolute/path/to/github-mcp-server"
args = ["stdio"]

[mcp_servers.github.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_TOKEN}"
```

## Good use cases

- inspect and update issues while coding
- open or review pull requests from the same session
- search code or repositories before implementing a change
- inspect workflow failures and release metadata

## Example prompts

- `列出这个仓库最近打开的 PR，并标出失败的 checks。`
- `读取 issue #52 的内容，再对照本地改动给出实施建议。`
- `搜索 org 里关于 mcp 的现有实现，找出可复用模块。`

## Caveats

- the legacy `@modelcontextprotocol/server-github` path no longer represents the actively developed official implementation
- PAT scope should be minimized
- remote and local GitHub MCP modes have different auth and hosting assumptions

## Why this is useful for Codex specifically

Codex gains a tighter loop between implementation, hosted review state, and issue tracking. That becomes especially valuable when code changes depend on PR or workflow context.

## Sources

- Official GitHub MCP server: https://github.com/github/github-mcp-server
- Archived MCP reference server note: https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github
