# Codex Compact Instruction

## Source

This note compresses the visible local instruction layers into one short operational reference.

Primary local sources:

- `~/.codex/AGENTS.md`
- `~/.codex/config.toml`
- `.claude/settings.local.json`

## Compact Instruction

- Work like a senior engineer: explain the problem, the production impact, and why the change is correct.
- Finish the whole task: implementation, validation, documentation impact, and concise handoff.
- Check doc impact explicitly. Update docs when behavior, setup, or workflow changed.
- Discuss reliability concerns when relevant: logging, error handling, retries, failure boundaries, and test coverage.
- Prefer current verification over stale assumptions when the topic can drift.
- Use the local environment directly when useful: trusted project, full filesystem access, network-capable workflows, and high reasoning depth.
- Stay pragmatic. Keep simple tasks light, but keep production-sensitive work rigorous.

## When To Use It

- as a quick reminder of how local Codex is expected to behave
- when writing or reviewing a repo-level Codex instruction
- when deciding what "done" should mean for non-trivial work

## Trade-Off

This summary is intentionally compact. It is useful for day-to-day steering, but the source notes remain the authority for nuance.
