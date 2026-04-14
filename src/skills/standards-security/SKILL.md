---
name: standards-security
description: "Review backend implementations for production readiness, logging quality, error handling, and security hygiene. Use when validating API code before completion or when a backend change needs a reliability and security pass."
---

# Standards Security

Review the implementation for production readiness and security.

## Responsibilities

- enforce formatting expectations
- enforce typing expectations
- verify logging coverage
- verify error handling
- enforce security practices

## Logging Rules

Must log:
- request received
- validation success
- execution start
- execution failure
- success completion

Never log:
- secrets
- tokens
- passwords

## Security Rules

- validate all inputs
- sanitize errors
- avoid sensitive data leaks
- hide internal stack traces

## Output

Use these section headers:

```md
## Logging Notes
```

```md
## Security Review
```

Include:
- what is logged
- where logs are placed
- risks identified
- mitigations applied
