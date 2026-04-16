# Local WebSearch Permission

## Source

This note is derived from the project-local file:

- `.claude/settings.local.json`

## What this instruction layer does

It explicitly allows `WebSearch` in the local project context.

Observed setting:

```json
{
  "permissions": {
    "allow": [
      "WebSearch"
    ]
  }
}
```

## Why use it

- enables live documentation and dependency verification
- supports freshness checks for MCP setup, APIs, package docs, and service changes
- reduces stale-memory answers on rapidly changing tools

## Typical use cases

- deep research on MCP server installation
- verifying latest package names
- checking whether an upstream project has moved or been archived
- confirming current official docs before writing setup notes

## Example

This exact permission is what makes it reasonable to verify:

- whether GitHub MCP has moved to a new official repo
- whether Playwright MCP changed package names
- whether Context7 now prefers a different install path

## Advantages

- better factual accuracy
- better doc freshness
- lower chance of copying obsolete setup commands

## Trade-offs

- requires source-quality judgment; not every search result is equally trustworthy
- can add time to tasks that would otherwise be answered from stable local knowledge
