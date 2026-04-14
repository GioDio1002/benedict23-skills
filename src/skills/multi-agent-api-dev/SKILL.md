---
name: multi-agent-api-dev
description: "Orchestrate backend and API implementation through a strict sequential workflow: requirement analysis, code generation, test validation, and standards/security review. Use when building APIs, implementing backend logic, defining request/response contracts, or adding validation, logging, and tests for server-side features."
---

# Multi-Agent API Dev

Use this skill as the top-level backend delivery workflow.

## Workflow

Run these stages in order:
1. `requirement-analysis`
2. `code-generation`
3. `test-validation`
4. `standards-security`

Never skip a stage.
Never reorder the flow.

## Orchestration Rules

- Pass structured output from each stage into the next stage.
- Keep the contract stable across the full flow.
- If true subagent delegation is available and explicitly permitted, delegate by stage.
- If subagent delegation is unavailable, execute the same stages sequentially in one thread.
- Do not jump straight to code before the requirement contract is explicit.

## Global Output Format

Always produce the final result in this order:
1. Requirement Breakdown
2. API Definition
3. Generated Code
4. Tests
5. Logging Notes
6. Security Review

## Engineering Standard

Behave like a senior backend engineer, not a raw code generator.

Prioritize:
- correctness
- clarity
- reliability
- maintainability

## Shared Rules

If `../../shared/engineering_rules.md` exists, read and apply it before finalizing the answer.
