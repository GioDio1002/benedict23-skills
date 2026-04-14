# homemade-skills

Normalized repository for a focused set of homemade Codex skills.

## Scope

This repo currently tracks nine local-first skills that were selected for publication because they do not have a clear exact-match upstream skill repository:

- `agents-init-helper`
- `deep-search-orchestrator`
- `deep-search-pipeline`
- `deep-search-scoring`
- `explain-fastapi-endpoint`
- `multi-agent-api-dev`
- `prd-writer`
- `standards-security`
- `test-validation`

## Repository Layout

```text
.
├── LICENSE
├── README.md
└── src
    ├── manifest.json
    ├── shared
    │   └── engineering_rules.md
    └── skills
        └── <skill-name>
            ├── SKILL.md
            └── agents
                └── openai.yaml
```

## Structure Rules

- `src/skills/<skill-name>/SKILL.md` is the canonical skill document.
- `src/skills/<skill-name>/agents/openai.yaml` stores the assistant-facing prompt metadata.
- `src/shared/` stores shared reference material used by more than one skill.
- Skills should prefer repository-relative references so the repo can be cloned anywhere.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `agents-init-helper` | Reads repo-local `AGENTS.md` instructions before implementation work |
| `deep-search-orchestrator` | Produces structured deep research reports |
| `deep-search-pipeline` | Runs report generation followed by scoring |
| `deep-search-scoring` | Scores deep research quality and hallucination risk |
| `explain-fastapi-endpoint` | Traces FastAPI endpoints end-to-end |
| `multi-agent-api-dev` | Orchestrates requirement, codegen, validation, and security review |
| `prd-writer` | Standardizes PRDs and product specs |
| `standards-security` | Reviews backend reliability, logging, and security hygiene |
| `test-validation` | Generates backend test coverage and request examples |

## Maintenance Workflow

1. Edit the source skill under `src/skills/<skill-name>/`.
2. Keep prompt metadata in `agents/openai.yaml` aligned with the skill behavior.
3. Add shared references under `src/shared/` instead of duplicating guidance across skills.
4. Update `src/manifest.json` whenever a skill is added, removed, or renamed.

## Publishing Notes

- This repository is organized for Git-based maintenance first.
- If these skills are later imported into another Codex or agent environment, copy each skill directory as-is.
- Avoid absolute local filesystem paths inside `SKILL.md` files.
