---
name: test-validation
description: "Generate backend tests and validation coverage for APIs and services. Use when Codex needs unit tests, API tests, edge-case coverage, request examples, or a validation plan for backend endpoints and server-side logic."
---

# Test Validation

Validate backend correctness through tests and executable examples.

## Responsibilities

- generate unit tests
- generate API tests
- generate edge-case tests
- provide request examples

## Coverage Requirements

Always include:
1. success case
2. missing fields
3. invalid types
4. boundary values
5. failure scenarios

## Output

Use these section headers:

```md
## Tests
```

```md
## Request Examples
```

Prefer runnable Python tests for Python backends. Match the repository test framework when it already exists.
