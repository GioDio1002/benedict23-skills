# Engineering Rules

## Core Principles

- API-first design
- strong typing
- validation by default
- explicit error handling
- production-quality code

## Mandatory Practices

### Validation

- validate all inputs
- use schema-based validation

### Typing

- type all functions
- avoid untyped dictionaries when a model or schema is clearer

### Logging

- include useful context
- avoid sensitive data

### Error Handling

- map failures to explicit HTTP responses
- never expose stack traces to clients

## Anti-Patterns

- skipping validation
- missing tests
- silent exception handling
- monolithic functions
- unclear API contracts
