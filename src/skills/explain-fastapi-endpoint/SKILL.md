---
name: explain-fastapi-endpoint
description: Analyze a FastAPI endpoint end-to-end, including trigger conditions, request flow, handler logic, service calls, database or queue interactions, external API usage, success and failure paths, SSE behavior, and data transformations. Use when Codex needs to explain or review a FastAPI route, debug endpoint behavior, trace request processing across modules, document backend flows, or inspect how an API endpoint reaches schemas, models, tasks, and downstream systems.
---

# Explain FastAPI Endpoint

## Catalogue

- [Overview](#overview)
- [Workflow](#workflow)
- [1. Locate the endpoint precisely](#1-locate-the-endpoint-precisely)
- [2. Build the execution chain](#2-build-the-execution-chain)
- [3. Classify the endpoint shape](#3-classify-the-endpoint-shape)
- [4. Inspect success and failure paths](#4-inspect-success-and-failure-paths)
- [5. Inspect SSE or streaming behavior when present](#5-inspect-sse-or-streaming-behavior-when-present)
- [6. Track data transformations](#6-track-data-transformations)
- [7. Identify important schemas and storage](#7-identify-important-schemas-and-storage)
- [8. Trace table and field mutations by phase](#8-trace-table-and-field-mutations-by-phase)
- [9. Build cURL request and expected output examples](#9-build-curl-request-and-expected-output-examples)
- [Required Output Structure](#required-output-structure)
- [1. Endpoint Summary](#1-endpoint-summary)
- [2. Short Intuition](#2-short-intuition)
- [3. High-Level Flow Diagram](#3-high-level-flow-diagram)
- [4. Trigger and Entry Conditions](#4-trigger-and-entry-conditions)
- [5. Step-by-Step Request Lifecycle](#5-step-by-step-request-lifecycle)
- [6. Success Path](#6-success-path)
- [7. Failure and Edge Paths](#7-failure-and-edge-paths)
- [8. SSE or Streaming Behavior](#8-sse-or-streaming-behavior)
- [9. Data Processing and Transformation](#9-data-processing-and-transformation)
- [10. Schemas, Models, and Tables](#10-schemas-models-and-tables)
- [11. cURL Input and Expected Output Examples](#11-curl-input-and-expected-output-examples)
- [12. Table Field Updates by Phase](#12-table-field-updates-by-phase)
- [13. Key Takeaways](#13-key-takeaways)
- [Explanation Standards](#explanation-standards)
- [Diagram Patterns](#diagram-patterns)
- [Investigation Checklist](#investigation-checklist)

## Overview

Explain one endpoint as a traced execution path, not as a vague feature summary. Read the route definition, follow the actual called symbols, and distinguish confirmed behavior from inference whenever code or config is missing.

When referring to files, scripts, modules, or handlers, always use repository-relative paths such as `src/api/routes/files.py`. Do not mention absolute local filesystem paths.

## Workflow

### 1. Locate the endpoint precisely

Identify:
- HTTP method
- Path
- Router file
- Handler function
- Router inclusion path if the route is mounted indirectly

Quote actual code symbols whenever possible:
- `router.post("/x")`
- `async def create_report(...)`
- `Depends(get_db)`
- `EventSourceResponse(...)`

If the user gives only a path or function name, search the codebase and confirm the exact definition before explaining.

When citing the file location, use the repository-relative path only.

### 2. Build the execution chain

Trace the call path in order:
1. Request entry at router
2. Dependency injection and auth checks
3. Handler body
4. Service layer or helper calls
5. Database queries or writes
6. Queue, worker, cache, filesystem, or external API calls
7. Response construction

Prefer concrete chains such as:

```text
POST /reports
  -> `create_report`
  -> `validate_payload`
  -> `report_service.create`
  -> `ReportRepository.insert`
  -> `celery_app.send_task`
  -> JSON response
```

Do not stop at the controller if the real behavior lives in services or repositories.

### 3. Classify the endpoint shape

Decide which pattern fits best:
- Synchronous JSON endpoint
- Create-and-enqueue endpoint
- Read/query endpoint
- Streaming or SSE endpoint
- Upload and processing endpoint

This choice should shape the diagram and the explanation emphasis.

### 4. Inspect success and failure paths

Explain:
- Validation failures
- Auth failures
- Missing resource paths
- Timeout behavior
- Retry or idempotency behavior if present
- Raised exceptions and their HTTP mapping
- Silent failure risks such as swallowed exceptions, partial writes, or background tasks launched after DB failure

If exception handling is indirect, say so explicitly:
- Confirmed: caught in handler with `HTTPException(status_code=404, ...)`
- Inferred: likely converted by a global exception handler, but handler not shown

### 5. Inspect SSE or streaming behavior when present

For SSE endpoints, trace:
- Generator function
- Yield points
- Event names
- Payload structure
- Keepalive behavior
- Terminal event
- Error event behavior

Call out the exact emitted structure if visible, for example:

```text
event: progress
data: {"step":"ocr","progress":40,"message":"Parsed page 2"}
```

If the implementation streams plain text chunks instead of true SSE events, say that clearly.

### 6. Track data transformations

Follow how input becomes output:
- Request schema parsing
- Normalization or coercion
- Enrichment
- Mapping into ORM or SQL shapes
- Background payload construction
- Response schema serialization

Focus on transformations that matter operationally:
- chunking
- filtering
- deduplication
- status transitions
- page extraction
- summarization payload assembly

### 7. Identify important schemas and storage

List the concrete objects involved:
- Pydantic request and response models
- ORM models
- SQL tables
- queue payload schema
- cache keys
- storage paths

If table names are not explicit in code, mark them as inferred from ORM model naming.

When request or response schemas are visible, also identify:
- required request fields
- optional request fields
- defaulted fields
- response fields that are always present
- response fields that are conditional, nullable, or stream-only

### 8. Trace table and field mutations by phase

Depict how the endpoint changes persistent state over time, not just which tables exist.

For each phase, identify:
- phase name
- function or symbol performing the write
- table or model touched
- fields inserted or updated
- when the write happens relative to streaming or external calls
- whether the write is confirmed, inferred, conditional, retried, or best-effort

Prefer a compact phase table such as:

```text
Phase                Symbol                            Table                         Field changes
-------------------  --------------------------------  ----------------------------  ---------------------------------------------
request accepted     `create_report_row`               `reports`                     insert `status='queued'`, `user_id`, `query`
generation started   `mark_report_running`             `reports`                     update `status='running'`, `started_at`
section persisted    `save_section_result`             `report_sections`             insert `report_id`, `section_key`, `content`
finalize             `mark_report_complete`            `reports`                     update `status='complete'`, `completed_at`
public sync          `sync_user_report`                `user_reports`                upsert `summary`, `report_id`
```

If no database write exists for a phase, say so explicitly.

### 9. Build cURL request and expected output examples

When the endpoint contract is visible in code, include concrete examples of how to call it and what to expect back.

For request examples:
- prefer `curl` over pseudocode
- include required headers
- mark required fields with `(required)`
- mark optional fields with `(optional)`
- omit speculative fields that are not supported by the inspected code

For response examples:
- show the expected success payload shape for JSON endpoints
- show representative SSE frames for streaming endpoints
- mark fields that are always present versus conditional when that is visible
- mention whether the example is confirmed from code or inferred from schema naming or serializer patterns

Prefer a compact format such as:

```text
Required request fields:
- `user_id` (required)
- `query` (required)
- `locale` (optional)

Example:
curl -X POST http://localhost:8000/reports \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "user_id": 42,
    "query": "Summarize the record"
  }'
```

## Required Output Structure

Use this exact section structure when explaining an endpoint:

### 1. Endpoint Summary

Include:
- Method
- Path
- Handler
- Purpose
- Defined in

For `Defined in`, use a repository-relative path only.

### 2. Short Intuition

Explain the endpoint in plain language in 2 to 4 sentences.

### 3. High-Level Flow Diagram

Always include an ASCII diagram in a fenced code block.

Choose the diagram style that best fits the endpoint:
- left-to-right for request and response chains
- top-down for staged processing
- branching for success versus failure

### 4. Trigger and Entry Conditions

Explain what must happen for the endpoint to run:
- client action or upstream caller
- required auth
- required headers
- required body or params
- dependency injection preconditions

### 5. Step-by-Step Request Lifecycle

Walk through the handler in execution order. Use actual function names and file locations when possible.

### 6. Success Path

Describe the happy path from validated request to returned response or emitted events.

### 7. Failure and Edge Paths

Describe the concrete failure modes and where they originate.

### 8. SSE or Streaming Behavior

Include only when relevant. Explain event format, sequencing, completion, and disconnect behavior.

### 9. Data Processing and Transformation

Explain how the input is reshaped, enriched, stored, and returned.

### 10. Schemas, Models, and Tables

List the important request or response models and persistence objects.

### 11. cURL Input and Expected Output Examples

Show at least one concrete request example when the contract is visible in code.

Include:
- required headers
- required query params, path params, or body fields marked as `(required)`
- optional fields marked as `(optional)`
- one `curl` example
- expected JSON response example or representative SSE frames
- a short note if the example is partially inferred because serializer code is missing

For SSE endpoints, prefer:

```text
curl -N -H "Accept: text/event-stream" ...
```

and show 2 to 4 representative emitted frames.

### 12. Table Field Updates by Phase

Show how the endpoint mutates persistent state across phases.

Include:
- phase ordering
- write symbol
- table or model name
- inserted fields
- updated fields
- terminal success fields
- terminal failure fields
- conditional writes such as audit rows, section rows, or mirror tables

Prefer a compact table or timeline.

### 13. Key Takeaways

Summarize in 3 to 5 flat bullet points.

## Explanation Standards

Always:
- distinguish `Confirmed` from `Inferred`
- quote concrete symbols where possible
- mention missing pieces explicitly
- explain why the design exists, not only what it does
- use repository-relative paths only for scripts, handlers, and modules
- call out transaction boundaries, async boundaries, and external side effects
- include concrete request and response examples when schema visibility allows it
- mark required versus optional input fields explicitly
- show field-level persistence transitions when tables are updated in phases
- include trade-offs, performance implications, and likely failure points

Do not:
- mention absolute local directories or workstation-specific paths
- paraphrase the route without tracing it
- invent tables, payload fields, or services not supported by code
- claim SSE semantics just because streaming exists
- ignore background tasks, caches, or side effects
- present guessed request fields as confirmed contract requirements
- hide persistence-sensitive writes behind a vague phrase like "updates the DB"
- collapse success and failure behavior into one vague paragraph

## Diagram Patterns

Use simple ASCII-only diagrams inside fenced code blocks.

Architecture or dependency view:

```text
+--------+      +---------+      +-----------+
| Client | ---> | Router  | ---> | Service   |
+--------+      +---------+      +-----------+
                               /      |      \
                              v       v       v
                        +---------+ +-----+ +--------+
                        |   DB    | | SSE | |  API   |
                        +---------+ +-----+ +--------+
```

Success versus failure branching:

```text
Request
  |
  v
Validate input
  |
  +--> invalid ----------> 422 response
  |
  v
Run business logic
  |
  +--> dependency fails --> 500 or mapped error
  |
  v
Persist / enqueue
  |
  v
Return success
```

SSE sequencing:

```text
Client connects
  |
  v
Open generator
  |
  +--> yield `start`
  +--> yield `progress`
  +--> yield `progress`
  +--> yield `complete`
  \--> on error: yield `error` or terminate connection
```

## Investigation Checklist

Check these files or symbols when relevant:
- router module
- included router registration
- dependency providers
- request and response schemas
- services and repositories
- ORM models and migrations
- queue or worker publishers
- SSE generator helpers
- exception handlers
- settings or environment-driven branches
- tests covering the endpoint
