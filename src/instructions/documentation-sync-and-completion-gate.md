# Documentation Sync And Completion Gate

## Source

This note is derived from the visible local file:

- `~/.codex/AGENTS.md`

## What this instruction layer does

It declares that code work is not complete until documentation impact, error handling, logging, testing, and completion criteria have been reviewed.

Key expectations:

- review whether `AGENTS.md` must be updated
- do not silently skip doc impact
- explicitly discuss logging and observability
- explicitly discuss error handling
- explicitly discuss testing strategy
- include a mandatory change summary

## Why use it

- reduces the common failure mode where code changes ship but ops docs or workflow notes stay stale
- keeps "definition of done" tied to operational reality
- forces the assistant to think past the diff itself

## Typical use cases

- feature work that changes behavior
- bugfixes that alter failure handling
- new environment variables or setup steps
- background jobs, retries, fallbacks, or deployment behavior
- API changes or testing workflow changes

## Example

If a change adds retry logic to a worker, this instruction layer expects all of the following:

- code change
- explanation of retry behavior
- logging review
- test coverage or a proposed test plan
- docs review for operational impact

## Advantages

- better doc hygiene
- clearer operational accountability
- fewer "works locally but nobody documented it" failures
- stronger completion criteria

## Trade-offs

- can feel strict for lightweight tasks
- assumes there is a repository root `AGENTS.md` to update when applicable
- requires explicit "no update needed" reasoning when that file does not exist
