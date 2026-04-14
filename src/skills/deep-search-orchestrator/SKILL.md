---
name: deep-search-orchestrator
description: Produce structured deep research reports for a company, market, product, technology, or issue. Use when the user wants report generation only, a deep search write-up without QA scoring, or a reusable report-drafting behavior that gathers evidence, separates facts from interpretation, and synthesizes findings into a clean research memo.
---

# Deep Search Orchestrator

## Overview

Generate a structured research report from raw evidence. Build the report in stages so the writing reflects actual findings rather than generic narrative.

## Workflow

Run the report in this order:

1. Understand the query
2. Define scope
3. Plan sources
4. Extract facts
5. Synthesize sections
6. Assemble the final report

## 1. Understand The Query

Identify:

- topic or entity
- intended audience if implied
- requested depth
- decision the user is trying to support
- uncertainty or ambiguity in the ask

If the ask is broad, choose the narrowest reasonable interpretation and state assumptions.

## 2. Define Scope

Pick sections that match the research type.

Default company sections:

- Executive Summary
- Overview
- Products / Services
- Business Model
- Market / Competition
- Traction / Signals
- Strengths
- Risks
- Open Questions

Optional sections:

- Funding
- Partnerships
- Technology
- Investment Perspective

Do not include sections with no substance just to make the report look complete.

## 3. Plan Sources

Prefer sources in this order:

1. official site
2. product documentation or product pages
3. company blog or newsroom
4. reputable news
5. funding or investor sources
6. competitor material for comparison
7. secondary analysis only as support

Prefer recent and primary evidence when the topic is time-sensitive.

## 4. Extract Facts

Before polished writing, separate notes into:

- factual claims
- informed interpretation
- weak signals
- unresolved gaps

Avoid blending speculation into fact statements.

## 5. Synthesize Sections

Write section by section.

For each section:

- keep only claims that earn inclusion
- remove repetition
- state what matters, not every discovered fact
- call out uncertainty when evidence is thin

## 6. Assemble The Final Report

Return a clean report using this structure unless the user requests another format:

```md
# {Entity or Topic}

## Executive Summary

## Overview

## Products / Services

## Business Model

## Market / Competition

## Traction / Signals

## Strengths

## Risks

## Open Questions
```

Add optional sections only when relevant. End with the strongest unresolved questions if evidence is incomplete.

## Guardrails

Do not:

- overstate confidence
- pad with generic market commentary
- confuse quantity of notes with analytical depth
- hide major gaps in evidence

A good report is specific, source-aware, and honest about what remains unclear.

## Failure Handling

If evidence is partial or stale:

- reduce scope instead of padding
- state the evidence gap directly
- preserve the distinction between fact and interpretation
- leave open questions rather than forcing certainty
