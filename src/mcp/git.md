# git MCP In Codex

## What it is

`git` is the MCP reference server for repository interaction. It exposes status, diff, add, reset, log, branch, checkout, show, and commit operations.

## Why install it in Codex

- lets the agent inspect and operate on repositories through MCP tools
- useful for structured Git workflows when shell access is not ideal
- supports branch and diff analysis in a tool-native format

## Current local setup

```toml
[mcp_servers.git]
command = "uvx"
args = ["mcp-server-git"]
```

## Latest official guidance

The official MCP docs still recommend `uvx mcp-server-git` as the primary installation method. `pip install mcp-server-git` is the main alternative.

## Recommended Codex install pattern

### Broad local access

```toml
[mcp_servers.git]
command = "uvx"
args = ["mcp-server-git"]
```

### Safer restricted access

If you want to constrain the tool to a specific repository:

```toml
[mcp_servers.git]
command = "uvx"
args = ["mcp-server-git", "--repository", "/absolute/path/to/repo"]
```

## Good use cases

- inspect unstaged or staged diffs
- create or switch branches as part of an agent workflow
- read commit history during debugging
- show a specific revision without leaving the Codex loop

## Example prompts

- `用 git MCP 看一下当前 repo 的 unstaged diff。`
- `创建一个 staging 分支并切过去。`
- `比较当前工作区和 main 的差异。`

## Caveats

- the official docs note the server is still in early development
- if unrestricted, it may have access to more repositories than you intended
- shell git and MCP git can overlap, so teams should decide which path is preferred for write operations

## Why this is useful for Codex specifically

Codex already reasons about code changes. `git` MCP gives it structured repo state and branch operations without forcing everything through raw shell parsing.

## Sources

- MCP reference server README: https://github.com/modelcontextprotocol/servers/tree/main/src/git
