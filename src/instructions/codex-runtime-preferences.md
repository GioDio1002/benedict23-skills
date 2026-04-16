# Codex Runtime Preferences In This Environment

## Sources

This note is derived from visible local config:

- `~/.codex/config.toml`

## What this configuration currently says

Observed runtime preferences include:

- model: `gpt-5.4`
- reasoning effort: `xhigh`
- sandbox mode: `danger-full-access`
- approval policy: `on-failure`
- personality: `pragmatic`
- project trust for `/Users/benedict/Documents/cosmetic`: `trusted`
- selected plugins enabled
- MCP servers registered in global Codex config

## Why this matters

These are not prose instructions, but they shape behavior in practice:

- `xhigh` reasoning biases toward deeper analysis
- `danger-full-access` removes filesystem sandbox constraints
- `on-failure` means commands usually run directly unless they fail under sandbox rules
- trusted project state reduces friction when operating inside the repo

## Typical use cases

- long-form analysis or research tasks
- repo editing without repeated file access prompts
- local environment inspection
- MCP-heavy workflows where Codex needs network and filesystem access

## Example

For a task like "research our MCP stack and write installation docs":

- high reasoning helps compare current config against official docs
- trusted project access simplifies repository edits
- full filesystem access makes it easy to inspect local config and related files

## Advantages

- lower friction for serious engineering work
- easier repository-wide inspection
- better support for multi-step agent tasks

## Trade-offs

- `danger-full-access` raises the cost of careless commands
- higher reasoning can slow trivial tasks
- strong capability means the surrounding review discipline matters more
