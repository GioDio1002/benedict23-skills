---
name: agents-init-helper
description: Read repository-local agent instruction files and use them as the source of truth before starting work. Use when a repository may contain `AGENTS.md`, `CLAUDE.md`, `AGENTS.override.md`, or similar agent instruction files; when the user asks to initialize agent instructions; when the user asks to improve project guidance for the coding agent; or when the task depends on repository-specific working rules. Works in both Codex and Claude Code.
---

# Agents Init Helper

Use this skill to make repository-local instructions the first stop instead of guessing how a repo wants work done.

## Check For Agent Instructions First

Before making changes, look for repository instruction files, especially:
- `AGENTS.md` (Codex and other agents)
- `CLAUDE.md` (Claude Code)
- `AGENTS.override.md`
- any other configured fallback instruction file the repo uses

If such a file exists:
- read it carefully
- follow it as the repository-local source of truth
- summarize the key working rules when that helps the user
- do not contradict it unless the user explicitly asks to update it

## If `AGENTS.md` Is Missing

If the repo does not contain `AGENTS.md`:
- tell the user that both Codex and Claude Code support a built-in `/init` command to scaffold one (`AGENTS.md` in Codex, `CLAUDE.md` in Claude Code)
- offer a direct markdown draft if the user wants content now
- if asked to create it, write a practical `AGENTS.md` with concise, enforceable rules

## Prefer Practical Guidance

When creating or improving `AGENTS.md`, prioritize:
- setup commands
- test commands
- lint or format commands
- project conventions
- file locations
- documentation expectations
- logging and validation expectations
- review checklist items

Avoid:
- vague aspirations
- copied README prose
- long policy documents
- rules that cannot be checked in practice

## Recommended `AGENTS.md` Structure

Use this structure unless the repository already has a better one:

```markdown
# AGENTS.md

## Project overview
- Brief description of the repository and major components.

## Setup
- Install commands
- Environment setup
- Required services

## Development workflow
- How to run the app
- How to run tests
- How to run lint / format
- Migration or build commands if needed

## Code rules
- Type safety expectations
- Error handling expectations
- Logging requirements
- Documentation update requirements

## Validation before completion
- Commands the agent should run after edits
- What must pass before marking work done

## File / architecture notes
- Important directories
- Entry points
- Areas requiring extra caution
```

## Updating Existing `AGENTS.md`

If the file exists but is weak:
- preserve sections that already help
- tighten vague wording into checkable instructions
- remove duplicated content
- keep the document short and operational

## Output Style

When writing or revising `AGENTS.md`:
- be concise
- prefer bullet lists with action verbs
- keep rules testable
- write instructions for repository agents, not a user tutorial

## Example Response Patterns

If `AGENTS.md` exists:
- "I found `AGENTS.md` and will follow its repo rules."
- "The key instructions are: run tests after backend edits, update docs for public behavior changes, and avoid new dependencies without justification."

If `AGENTS.md` does not exist:
- "This repo does not have an `AGENTS.md` / `CLAUDE.md` yet. In Codex or Claude Code, `/init` can scaffold one in the current directory. I can also draft a stronger version for this repo now."

## Starter Draft

Use this when the user wants a short starter:

```markdown
# AGENTS.md

## Repository expectations
- Read this file before making changes.
- Prefer minimal, targeted edits.
- Do not introduce new dependencies unless necessary.

## Validation
- Run tests relevant to changed files.
- Run lint / format before finishing.
- Report any command that could not be run.

## Documentation
- Update docs when behavior, configuration, or public interfaces change.
- Include important operational notes for future maintainers.

## Safety
- Avoid destructive commands unless explicitly requested.
- Confirm schema-affecting or production-sensitive changes before applying them.
```
