# Senior Engineer Mentor Mode

## Source

This note is derived from the visible local file:

- `~/.codex/AGENTS.md`

## What this instruction layer does

It pushes the assistant toward a staff-engineer posture instead of a "just write code fast" posture.

Core behaviors:

- explain why a change is needed
- explain what problem it solves
- explain how it behaves in production
- focus on reliability, observability, and risk reduction

## Why use it

- forces engineering reasoning instead of superficial patching
- improves review quality on operational or production-sensitive work
- makes implementation notes more useful for future maintainers

## Typical use cases

- backend changes with failure modes
- worker or queue flows
- logging or observability work
- architecture or production hardening reviews
- complex bugfixes where "what changed" is not enough

## Example

Instead of only saying:

```text
Fixed the retry bug.
```

this instruction layer pushes toward:

```text
The retry condition previously treated permanent validation errors as transient.
That caused wasteful retries and hid the real failure mode in production.
The new flow separates transient transport errors from permanent validation errors.
```

## Advantages

- better production thinking
- stronger explanation quality
- lower failure risk from under-specified fixes
- more maintainable handoff notes

## Trade-offs

- responses become longer
- simple tasks can feel heavier than necessary
- if used rigidly, it can add overhead to documentation-only work
