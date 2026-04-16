# memory MCP In Codex

## What it is

`memory` is a local knowledge-graph memory server. It stores entities, relations, and observations so the agent can persist structured facts across sessions.

## Why install it in Codex

- useful for durable user, project, and workflow context
- supports relationship-aware memory instead of plain note blobs
- helps the agent remember recurring preferences, constraints, and entities over time

## Current local setup

```toml
[mcp_servers.memory]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]
```

## Latest official guidance

The official reference docs still describe the `npx -y @modelcontextprotocol/server-memory` path as a supported installation pattern. Docker is the other main option.

## Recommended Codex install pattern

```toml
[mcp_servers.memory]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]
```

Optional custom storage path:

```toml
[mcp_servers.memory]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]

[mcp_servers.memory.env]
MEMORY_FILE_PATH = "/absolute/path/to/memory.jsonl"
```

## Good use cases

- remember stable user preferences
- store project entities and relationships
- keep long-lived context that should survive a single conversation
- support personalized workflows or recurring operational patterns

## Example prompts

- `把这个项目的核心实体和关系存进 memory。`
- `查一下 memory 里之前记录的部署约束。`
- `为这个用户增加一个“偏好简洁回复”的 observation。`

## Caveats

- memory quality depends on what gets stored; bad facts become durable noise
- sensitive data should not be stored casually
- a local file-backed memory store needs filesystem hygiene and backup decisions

## Why this is useful for Codex specifically

Codex benefits when durable context can be kept out of the transient prompt and retrieved only when relevant. That reduces repetition and helps maintain stable working preferences.

## Sources

- MCP reference server README: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
