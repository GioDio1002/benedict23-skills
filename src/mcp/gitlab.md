# GitLab MCP In Codex

## What it is

GitLab MCP exposes GitLab project operations as tools for an agent. Typical actions include reading project metadata, listing issues and merge requests, and interacting with CI/CD workflows.

## Why install it in Codex

- Codex can move between local code and remote GitLab state without leaving the same session.
- It reduces context switching when triaging MR status, pipelines, or issue state.
- It is useful when the repository of record lives on GitLab rather than GitHub.

## Current local setup

The current local Codex setup uses a remote MCP endpoint:

```toml
[mcp_servers.GitLab]
url = "https://gitlab.ekohe.com/api/v4/mcp"
```

This is not the same as running a local `glab` process. It means Codex connects to a hosted MCP server exposed by the GitLab instance.

## Latest official guidance

GitLab currently documents `glab mcp serve` as the local stdio entrypoint for GitLab MCP. The docs describe it as experimental and not production-ready.

Official pattern:

```json
{
  "mcpServers": {
    "glab": {
      "type": "stdio",
      "command": "glab",
      "args": ["mcp", "serve"]
    }
  }
}
```

## Recommended Codex install patterns

### Pattern A: keep the hosted endpoint

Use this when your organization already exposes a remote GitLab MCP server:

```toml
[mcp_servers.GitLab]
url = "https://your-gitlab-instance.example.com/api/v4/mcp"
```

### Pattern B: run `glab mcp serve` locally

Use this when you want a local stdio server and already rely on `glab` authentication:

```toml
[mcp_servers.GitLab]
command = "glab"
args = ["mcp", "serve"]
```

Prerequisites:

- install `glab`
- run `glab auth login`
- confirm the target GitLab instance and token scope are correct

## Good use cases

- read merge request status while editing code locally
- check failed GitLab pipelines without opening the browser
- triage issues and link implementation work to the right MR
- inspect project metadata or discussions during release work

## Example prompts

- `检查这个 GitLab 项目的 open merge requests，告诉我哪些 pipeline 失败了。`
- `读取 issue #123，看看它和当前分支改动是否一致。`
- `列出最近 10 条 pipeline，标记失败原因。`

## Caveats

- the official `glab mcp serve` flow is documented as experimental
- remote hosted MCP and local stdio MCP are different operational models
- auth and access control are delegated to either GitLab token management or the hosted endpoint

## Why this is useful for Codex specifically

Codex is strongest when it can connect implementation work with repo state. GitLab MCP gives it MR, issue, and CI context in the same working loop as local edits.

## Sources

- GitLab Docs: https://docs.gitlab.com/cli/mcp/serve/
