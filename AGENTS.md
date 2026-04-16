# AGENTS.md

Repository guidance for agents working in this repo.

## Purpose

This repository is a normalized, documentation-first home for:

- reusable Codex skills under `src/skills/`
- shared reference material under `src/shared/`
- MCP server notes under `src/mcp/`
- Codex instruction notes under `src/instructions/`

This is not an application runtime repository. Most changes here should improve clarity, maintainability, portability, and publishing readiness.

## Directory Rules

### `src/skills/`

- `src/skills/<skill-name>/SKILL.md` is the canonical source for each skill.
- `src/skills/<skill-name>/agents/openai.yaml` should stay aligned with the actual skill behavior.
- Avoid absolute machine-specific paths inside skill content unless the skill explicitly documents a local-only workflow.
- Prefer repository-relative references where possible.

### `src/shared/`

- Put reusable guidance here when it is shared by more than one skill.
- Do not duplicate the same engineering rule across multiple skill files if it can live here once.

### `src/mcp/`

- This folder is documentation-only.
- Each file should describe one MCP server used in the working Codex setup.
- For each MCP doc, distinguish clearly between:
  - current local setup
  - latest official guidance
  - recommended install pattern
- If upstream package names or install methods changed, call out the drift explicitly.

### `src/instructions/`

- This folder is documentation-only.
- Keep it limited to visible, locally verifiable instruction layers and runtime preferences.
- Do not present hidden platform prompts as if they are repository-owned documents.
- Summaries should explain:
  - what the instruction/config does
  - why it is useful
  - typical use cases
  - trade-offs

## Editing Rules

- Keep Markdown concise, operational, and easy to scan.
- Prefer plain headings and short sections over long narrative blocks.
- When documenting external tools, prefer official upstream sources over third-party summaries.
- If a file describes a local setup, say when it was last verified.
- Preserve bilingual structure in `README.md` when editing it.

## Documentation Sync

When changing repository structure or adding a new documentation area:

1. Update `README.md` if the visible layout or maintenance rules changed.
2. Update this `AGENTS.md` if working rules, scope, or maintenance expectations changed.
3. Keep `README.md` focused on repo consumers.
4. Keep `AGENTS.md` focused on agents and maintainers.

## Git Expectations

- Use focused documentation commits.
- Do not rewrite history unless explicitly requested.
- Prefer fast-forward merges when there is no reason to create a merge commit.
- Before pushing, verify the working tree is clean and the intended branch is checked out.

## Validation

For documentation-only changes, the minimum validation bar is:

- file exists in the intended directory
- repository structure references are accurate
- cross-references are not stale
- git status is clean after commit

For research-backed docs, also verify:

- the source is primary or official where possible
- current local config is not confused with latest upstream guidance
