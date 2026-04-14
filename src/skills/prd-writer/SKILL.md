---
name: prd-writer
description: "Use this skill when the user wants to write, expand, revise, or standardize a Product Requirements Document (PRD), feature spec, product brief, or implementation-ready requirements document. Do not use this skill for pure code generation, bug fixing, API implementation, or low-level technical design docs unless the user explicitly asks for a PRD-style product document."
---

# PRD Writer

Use this skill to create clear, decision-ready Product Requirements Documents from rough ideas, tickets, notes, stakeholder requests, feature proposals, or partially written drafts.

Help Codex behave like a strong product-thinking collaborator rather than a generic writer.

## Core Goals

Produce a PRD that is:
- clear
- scoped
- actionable
- implementation-aware
- easy for engineering and stakeholders to review

The PRD should reduce ambiguity, surface assumptions, and separate product intent from implementation details.

## Default PRD Structure

Use these sections unless the user requests a different format:
1. Title
2. Summary
3. Background / Problem
4. Goal
5. Non-Goals
6. Users / Stakeholders
7. User Story / Jobs To Be Done
8. Scope
9. Functional Requirements
10. Non-Functional Requirements
11. UX / Workflow Notes
12. Success Metrics
13. Risks / Open Questions
14. Dependencies
15. Rollout / Validation Plan

## Writing Rules

- Write in a structured, direct, professional style.
- Prefer clarity over buzzwords.
- Separate confirmed requirements from assumptions.
- Clearly mark unknowns and open questions.
- Avoid pretending uncertain details are finalized.
- Prefer implementation-aware wording, but do not jump into code unless asked.
- Keep requirements testable where possible.
- Turn vague requests into explicit bullets.
- Break large features into subflows when useful.

## Requirement Quality Rules

For each important requirement, make it as much as possible:
- specific
- testable
- scoped
- observable
- free from hidden assumptions

When requirements are weak or incomplete, explicitly add:

```md
### Assumptions
- ...

### Open Questions
- ...
```

## Expected Output Behavior

When generating a PRD:
1. Start with a concise summary of the feature or problem.
2. State the business or user problem clearly.
3. Define goals and non-goals separately.
4. List functional requirements as numbered items.
5. Include edge cases or failure scenarios where relevant.
6. Add measurable success criteria if possible.
7. Add dependencies, risks, and open questions.
8. If the input is rough, normalize it into a clean PRD structure.

## Functional Requirement Style

Prefer language like:
- The system must...
- The user can...
- The product should...
- The workflow must support...

Avoid vague language like:
- maybe
- probably
- somehow
- improve experience

Unless you are explicitly listing uncertainty.

## Output Template

```md
# {Feature Name}

## Summary
Brief summary of the feature and why it matters.

## Background / Problem
What problem exists today? Who feels it? Why does it matter?

## Goal
What outcome should this feature achieve?

## Non-Goals
What is explicitly out of scope?

## Users / Stakeholders
Who uses it, owns it, or is affected?

## User Story
As a {user}, I want to {action}, so that {outcome}.

## Scope
What is included in this version?

## Functional Requirements
1. ...
2. ...
3. ...

## Non-Functional Requirements
- performance
- reliability
- security
- observability
- localization
- compliance
- accessibility

## UX / Workflow Notes
Describe the intended flow or states.

## Success Metrics
How do we know this worked?

## Dependencies
What teams, systems, or inputs are required?

## Risks / Open Questions
What is unclear, risky, or still undecided?

## Rollout / Validation Plan
How should this be validated, released, or reviewed?
```

## Review Pass

Before finalizing, improve the PRD for:
- clarity
- completeness
- internal consistency
- scope discipline
- implementation readiness

If something is unknown, say so explicitly instead of inventing details.
