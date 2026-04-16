# fetch MCP In Codex

## What it is

`fetch` is a reference MCP server from the Model Context Protocol project. It retrieves web content and converts HTML to markdown so the model can read pages more efficiently.

## Why install it in Codex

- turns long web pages into model-readable text
- supports chunked reading through `start_index`
- useful when Codex needs documentation, changelogs, or public web references inside the same session

## Current local setup

```toml
[mcp_servers.fetch]
command = "uvx"
args = ["mcp-server-fetch"]
```

## Latest official guidance

The official MCP reference server docs still recommend `uvx mcp-server-fetch` as the preferred path. `pip install mcp-server-fetch` remains an alternative.

## Recommended Codex install pattern

```toml
[mcp_servers.fetch]
command = "uvx"
args = ["mcp-server-fetch"]
```

Alternative:

```toml
[mcp_servers.fetch]
command = "python"
args = ["-m", "mcp_server_fetch"]
```

## Good use cases

- read public docs pages without opening a browser manually
- extract changelog text or migration notes
- ingest long articles in chunks for analysis
- fetch raw HTML when markdown conversion is not enough

## Example prompts

- `抓取这个文档页面并提取成 markdown，重点看安装部分。`
- `把这个 changelog 分段读取，看看 breaking changes 在哪里。`
- `读取这个网页的原始 HTML，检查 meta 标签。`

## Caveats

- the official docs warn that the server can access local or internal IP addresses, so it should be treated as a security-sensitive tool
- web content may still be stale or partially blocked by the target site
- robots and user-agent behavior can affect what the tool returns

## Why this is useful for Codex specifically

Codex frequently needs first-party web docs during implementation. `fetch` makes that retrieval fast, structured, and less brittle than copying page text by hand.

## Sources

- MCP reference server README: https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
