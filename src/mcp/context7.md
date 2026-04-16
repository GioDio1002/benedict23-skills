# context7 MCP In Codex

## What it is

Context7 provides up-to-date library and framework documentation retrieval for coding agents. It is designed to give the model recent docs and code examples instead of relying on stale memory.

## Why install it in Codex

- library APIs change often; Codex benefits from live docs during implementation
- it reduces hallucinated framework usage
- it is especially useful for React, Next.js, Supabase, database SDKs, and newer agent frameworks

## Current local setup

The current local Codex setup uses:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

This matches the long-standing local stdio package form.

## Latest official guidance

The current official Context7 documentation highlights:

- quick setup through `npx ctx7 setup`
- manual installation support
- a hosted MCP endpoint at `https://mcp.context7.com/mcp`

That means the official project now supports newer installation flows beyond the older local package-only pattern.

## Recommended Codex install pattern

### Stable parity with the current local setup

Use this if you want the repository docs to match the currently running Codex environment:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

### Re-evaluate for greenfield installs

If you are setting up a brand-new machine, review Context7's current official setup first because the hosted endpoint and `ctx7 setup` flow may become the preferred path over time.

## Good use cases

- ask for the latest framework-specific API examples
- verify exact package syntax before writing code
- compare multiple library installation or usage patterns
- ground implementation against official docs rather than blog posts

## Example prompts

- `用 context7 查一下 Next.js App Router 里最新的 route handlers 用法。`
- `帮我确认 Supabase JS v2 里 auth listener 的当前写法。`
- `检索 Prisma relation filters 的最新官方示例。`

## Caveats

- Context7 is most useful for public library documentation, not for your private repo logic
- if the upstream install model changes again, this local `npx` setup may stop being the best default
- remote-hosted MCP can change auth and network expectations compared with local stdio

## Why this is useful for Codex specifically

Codex often needs exact, current library behavior. Context7 narrows the gap between code generation and official documentation, which improves correctness on modern stacks.

## Sources

- Context7 install docs: https://context7.com/docs/installation
- Context7 repository: https://github.com/upstash/context7
