# MCP Servers Used In This Codex Setup

This folder documents the MCP servers currently used in the local Codex setup observed on 2026-04-16.

## Scope

The current active set is:

- `GitLab`
- `context7`
- `fetch`
- `git`
- `github`
- `memory`
- `playwright-mcp`
- `ruflo`
- `sequential-thinking`

## Why this folder exists

- Keep the actual local setup separate from generic MCP marketing pages.
- Record how each server is installed in Codex, not only in Cursor or VS Code.
- Capture drift between "what is running now" and "what the current official docs recommend".
- Give repeatable examples for why a server belongs in a coding-agent workflow.

## How to read these docs

Each file follows the same structure:

1. What the server does
2. Why it is valuable inside Codex
3. What the current local setup looks like
4. What the latest official install guidance says
5. Recommended Codex install pattern
6. Typical use cases and example prompts
7. Risks, caveats, or migration notes

## Important note on freshness

These docs were written from a combination of:

- the current local Codex config
- official upstream README or docs pages
- the current repository state on 2026-04-16

When an upstream project has clearly moved to a newer package or transport, the file calls that out explicitly instead of pretending the local setup is the latest recommended path.
