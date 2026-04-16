# BESA Framework of Prompt

## Purpose

The BESA framework is a practical prompt structure for asking an agent to help with real software work.

It is designed to reduce ambiguity, speed up investigation, and make it easier to route the request into the right skills, tools, or execution path.

Use it when you want an agent to:

- investigate a bug
- explain bad behavior
- debug a flow
- review code
- plan work
- build or change something

The core idea is simple:

- describe what is wrong now
- describe what should happen instead
- define the scope and skill triggers
- define the working mode or procedure

## BESA = Four Prompt Blocks

## B: Bug / Bad Behavior

Describe the current situation.

This block answers:

- what is broken
- what is confusing
- what is happening now
- where it was observed
- whether a screenshot, logs, or repro exists

Useful details:

- exact error message
- observed symptoms
- URL, screen, file, or workflow step
- repro steps
- optional screenshot or stack trace

Example:

```md
## B: Bug / Bad Behavior

The login modal closes after submit, but the user is not logged in.
Observed on the web app settings page after clicking "Sign in".
No visible error toast appears.
Browser console shows a 401 from the session endpoint.
Screenshot optional.
```

## E: Expected Behavior

Describe the intended result.

This block answers:

- what success looks like
- what the user expected
- what should happen after the fix
- what the end goal is

Useful details:

- expected UI behavior
- expected backend behavior
- expected data or status change
- optional screenshot of correct state

Example:

```md
## E: Expected Behavior

After submitting valid credentials, the modal should close only after the session is created.
The user avatar should appear in the header.
The session endpoint should return 200 and the protected page should load normally.
```

## S: Scope

Define the work boundary.

This block answers:

- is this single-repo or cross-repo
- which systems or files are in scope
- which skills or workflows should be triggered
- what should stay out of scope

Useful details:

- repo name or repos involved
- frontend/backend/db/infra boundaries
- files, directories, or services to inspect first
- skills that should be invoked
- constraints such as "no dependency changes"

Example:

```md
## S: Scope

Single repo.
Focus on auth UI, session API client, and related tests.
Inspect `src/auth/`, `src/api/`, and login flow tests first.
Trigger debugging, investigate, and test-validation style workflows.
Do not touch unrelated billing code.
```

## A: Action / Approach

Define how the agent should work.

This block answers:

- should the agent investigate first
- should it plan before coding
- should it debug, review, or build
- what sequence of actions should happen

This is the execution control block.

Common action modes:

- Investigation
- Plan
- Debug
- Code Review
- Build

You can also define a step sequence.

Example:

```md
## A: Action / Approach

1. Reproduce the failure.
2. Trace the auth request path.
3. Identify whether the issue is UI state, API usage, or session persistence.
4. Propose the smallest safe fix.
5. Update tests.
6. Summarize root cause and behavior change.
```

## Why BESA Works Well With Agents

BESA is useful because it separates four concerns that are often mixed together in weak prompts:

- observed reality
- desired outcome
- execution boundary
- operating procedure

This separation helps an agent avoid common failure modes:

- fixing the wrong thing
- changing too much
- missing key repos or files
- choosing the wrong workflow
- jumping into implementation before understanding the problem

## Partial Composition

BESA does not have to be used in full every time.

It can be broken into smaller combinations depending on the task.

## BEA

Use `BEA` when:

- the scope is obvious
- only one repo is involved
- the agent already knows the working boundary

Example:

```md
B: Search results are timing out after 10 seconds.
E: Queries should return within 2 seconds for common filters.
A: Investigate, benchmark the current query, identify the bottleneck, and propose a minimal fix.
```

## BSA

Use `BSA` when:

- the goal is implied
- the most important part is routing and work mode
- you need to constrain an agent before it starts

Example:

```md
B: CI is failing after the latest auth changes.
S: Single repo, auth module only, no dependency upgrades.
A: Review the failing tests, identify the regression, patch the smallest safe fix, and rerun relevant checks.
```

## ESA

Use `ESA` when:

- there is no bug yet
- this is new work or an enhancement
- you want to define the target, scope, and process

Example:

```md
E: Add a reusable loading state for dashboard widgets.
S: Single repo, frontend only, no API changes.
A: Inspect the current widget pattern, propose one reusable component, implement it, and update affected views.
```

## Suggested Procedure Types For A

You can standardize the `A` block into one of these modes:

### Investigation

Use when the problem is unclear.

```md
A: Investigate first. Gather evidence, locate the failing path, and explain likely root cause before proposing changes.
```

### Plan

Use when the task is large or architectural.

```md
A: Create a short implementation plan first, including files to touch, risks, and validation steps. Do not code before the plan is clear.
```

### Debug

Use when the issue is reproducible and needs root cause isolation.

```md
A: Reproduce the bug, isolate the failing component, confirm root cause, implement the smallest safe fix, and verify with targeted tests.
```

### Code Review

Use when the primary job is review rather than implementation.

```md
A: Review the diff for correctness, regressions, missing tests, and operational risks. Findings first, summary second.
```

### Build

Use when the feature is understood and implementation should proceed.

```md
A: Implement the requested change, keep scope tight, add or update validation, and summarize behavior changes.
```

## Full BESA Template

Copy and fill this in:

```md
# BESA Prompt

## B: Bug / Bad Behavior
- Current situation:
- Repro:
- Evidence:
- Screenshot/logs:

## E: Expected Behavior
- Desired outcome:
- Success condition:
- Optional reference state:

## S: Scope
- Repo scope:
- File/module scope:
- Required skills or workflows:
- Out of scope:

## A: Action / Approach
1.
2.
3.
4.
```

## Compact BESA Template

Use this for faster requests:

```md
B:
E:
S:
A:
```

## Example 1: Bugfix Prompt

```md
## B: Bug / Bad Behavior
The profile save button spins forever after clicking submit.
Observed on the account settings page.
Network tab shows the PATCH request succeeds, but the UI never exits loading state.

## E: Expected Behavior
After a successful PATCH response, the spinner should stop and a success state should appear.

## S: Scope
Single repo.
Focus on profile form state and save handler.
Do not modify unrelated account deletion flows.

## A: Action / Approach
1. Reproduce the issue.
2. Trace the loading-state lifecycle.
3. Fix the smallest safe state bug.
4. Add or update a regression test.
5. Summarize root cause.
```

## Example 2: Cross-Repo Prompt

```md
## B: Bug / Bad Behavior
Webhook delivery succeeds from the sender service, but the receiver repo does not process the event.

## E: Expected Behavior
An accepted webhook should create a processing record and trigger the downstream job.

## S: Scope
Cross-repo.
Inspect sender webhook client and receiver ingestion handler.
Trigger investigation and cross-repo debugging workflow.

## A: Action / Approach
1. Compare payload shape between sender and receiver.
2. Confirm auth and signature validation behavior.
3. Identify where the event is dropped.
4. Propose the smallest fix across the correct repo boundary.
```

## Example 3: Build Prompt

```md
## E: Expected Behavior
Add a reusable empty state component for dashboard modules.

## S: Scope
Single repo.
Frontend only.
Use existing component conventions.

## A: Action / Approach
1. Review current empty-state patterns.
2. Propose one reusable component shape.
3. Implement it in the shared UI layer.
4. Replace two duplicated instances.
5. Verify visual and behavioral consistency.
```

## Operating Notes

- If the problem is unknown, make `A` investigation-heavy.
- If the task is large, make `A` plan-first.
- If multiple systems are involved, make `S` explicit and narrow.
- If there is no bug, `B` can be omitted and you can use `ESA`.
- If there is a bug but the scope is obvious, `BEA` is often enough.

## Recommended Use

Use BESA when you want an agent request to feel:

- operational
- debuggable
- reviewable
- composable
- reusable across repos and workflows

The framework is intentionally simple enough to write quickly, but structured enough to produce better agent behavior than an unscoped paragraph prompt.
