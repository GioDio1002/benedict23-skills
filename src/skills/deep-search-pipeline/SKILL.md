---
name: deep-search-pipeline
description: "Run an end-to-end deep research workflow in one call: first produce a structured deep search report, then evaluate that exact report for coverage, depth, citation support, freshness, consistency, and hallucination trust. Use when the user wants a full company or topic analysis plus automatic QA, a report with a quality gate, or a research deliverable that should include both findings and scorecard rather than report-only or scoring-only output."
---

# Deep Search Pipeline

## Overview

Run the full Deep Search flow in a fixed order:

1. Generate the report
2. Score the generated report
3. Return the report and QA result together

Treat this skill as a controller. Do not stop after drafting unless the user explicitly asks for report-only output.

## Internal Order

Follow this sequence every time:

1. Apply the report-generation behavior from `../deep-search-orchestrator/SKILL.md`
2. Apply the QA and scoring behavior from `../deep-search-scoring/SKILL.md`

Do not reverse the order.

Do not score a hypothetical report.

Do not rewrite the report during scoring unless the user asks for a revised draft.

## Phase 1: Generate The Report

Start by clarifying:

- entity or topic
- likely audience
- expected depth
- known unknowns
- whether the request is company-style, market-style, or issue-style research

Choose sections based on the request. For company research, default to:

- Executive Summary
- Overview
- Products / Services
- Business Model
- Market / Competition
- Traction / Signals
- Strengths
- Risks
- Open Questions

Add optional sections only when they earn their place:

- Funding
- Partnerships
- Technology
- Investment Perspective

Write with these rules:

- separate facts from interpretation
- mark weak signals as weak
- avoid filler and repeated claims
- prefer direct evidence over polished prose
- keep uncertainty explicit

## Phase 2: Score The Report

Immediately evaluate the report from phase 1 across:

1. Coverage
2. Depth
3. Citation Support
4. Freshness
5. Consistency
6. Hallucination Trust

Use default weights unless the user specifies another rubric:

- Coverage: 20%
- Depth: 25%
- Citation Support: 20%
- Freshness: 10%
- Consistency: 15%
- Hallucination Trust: 10%

Apply these default gates:

- Pass: overall >= 80, citation support >= 75, hallucination trust >= 75
- Warning: overall 65-79
- Fail: overall < 65, or citation support < 60, or hallucination trust < 60

Do not let confident writing inflate the score. Penalize unsupported claims even when the prose sounds strong.

## Final Output

Return all of the following in one response:

1. Final Deep Search Report
2. Deep Search Quality Review
3. Scorecard
4. Strengths
5. Weaknesses
6. Recommended Next Actions

Use this shape unless the user asks for another format:

```md
# Deep Search Report

{full report}

---

# Deep Search Quality Review

## Scorecard
- Coverage: X/100
- Depth: X/100
- Citation Support: X/100
- Freshness: X/100
- Consistency: X/100
- Hallucination Trust: X/100
- Overall Score: X/100
- Quality Gate: Pass / Warning / Fail

## Strengths
- ...

## Weaknesses
- ...

## Recommended Next Actions
- ...
```

## Guardrails

Do not:

- stop after report generation unless explicitly asked
- reward verbosity without substance
- hide uncertainty
- present unsupported claims as settled facts
- score before the report exists

Succeed only when the response contains both the research content and the QA result.

## Execution Signals

If the run is interactive or long enough to justify progress updates, expose compact stage signals such as:

- phase: query-understanding, report-generation, scoring, complete
- status: in_progress, blocked, complete
- entity_or_topic
- evidence_gaps
- quality_gate

If evidence is thin, say so before the final score.

## Failure Handling

If phase 1 cannot gather enough evidence:

- lower confidence
- keep the report factual and narrow
- make the missing evidence explicit
- continue to scoring with the reduced-confidence draft

If phase 2 detects unsupported claims:

- lower citation support and hallucination trust
- name the weak sections
- recommend the next evidence to collect
