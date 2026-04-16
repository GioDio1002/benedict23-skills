# playwright-mcp In Codex

## What it is

Playwright MCP gives the agent browser automation capabilities through Playwright. It is useful for navigation, form interaction, page inspection, snapshots, and deterministic UI workflows.

## Why install it in Codex

- enables browser-driven QA inside the same coding session
- useful for reproducing front-end bugs and validating flows
- supports iterative UI inspection without switching tools

## Current local setup

The current local Codex config uses:

```toml
[mcp_servers."playwright-mcp"]
command = "npx"
args = ["-y", "playwright-mcp@latest"]
```

## Latest official guidance

Microsoft's current official package is `@playwright/mcp@latest`, not `playwright-mcp@latest`.

Official Codex example:

```bash
codex mcp add playwright npx "@playwright/mcp@latest"
```

And config form:

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

## Recommended Codex install pattern

### Pattern A: keep the current local setup for parity

```toml
[mcp_servers."playwright-mcp"]
command = "npx"
args = ["-y", "playwright-mcp@latest"]
```

### Pattern B: migrate to the current official package

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

If you want to mirror the official docs more closely, prefer Pattern B for new installs.

## Good use cases

- reproduce browser bugs
- smoke-test a user flow after making UI changes
- inspect accessibility-tree output for agent-friendly page navigation
- capture deterministic page state during debugging

## Example prompts

- `打开本地应用首页，走一遍登录流程并告诉我哪里失败了。`
- `导航到设置页，检查表单字段是否可交互。`
- `抓一下页面文本快照，确认 CTA 文案有没有更新。`

## Caveats

- Microsoft explicitly notes that coding agents may sometimes benefit more from Playwright CLI plus skills than from MCP, because CLI can be more token-efficient
- package naming has changed; this is a likely migration point for the current setup
- browser automation can be slower and more stateful than pure code-only work

## Why this is useful for Codex specifically

Codex can implement and verify front-end changes in one loop. Playwright MCP makes UI validation part of the same agent workflow instead of a separate manual browser pass.

## Sources

- Official Playwright MCP README: https://github.com/microsoft/playwright-mcp
