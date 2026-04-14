---
name: deep-search-scoring
description: Evaluate a deep research report for quality, trust, and decision usefulness. Use when the user wants QA scoring only, wants an existing report assessed for coverage and hallucination risk, or needs a scorecard covering coverage, depth, citation support, freshness, consistency, and hallucination trust.
---

# Deep Search Scoring

## Overview

Score the actual report in front of you. Judge substance, support, and trustworthiness rather than style alone.

## Scoring Dimensions

Evaluate these dimensions on a 0-100 scale:

1. Coverage
2. Depth
3. Citation Support
4. Freshness
5. Consistency
6. Hallucination Trust

Use these definitions:

- Coverage: how fully the report covers the expected dimensions of the topic
- Depth: how specific, analytical, and decision-useful the report is
- Citation Support: how well important claims are grounded in evidence
- Freshness: how current the report appears for the topic
- Consistency: how well sections align without contradiction
- Hallucination Trust: how safe the report is from unsupported or fabricated claims

Higher hallucination trust is better.

## Default Weights

Unless the user specifies otherwise, weight scores as:

- Coverage: 20%
- Depth: 25%
- Citation Support: 20%
- Freshness: 10%
- Consistency: 15%
- Hallucination Trust: 10%

## Quality Gate

Apply these default gates:

- Pass: overall >= 80, citation support >= 75, hallucination trust >= 75
- Warning: overall 65-79
- Fail: overall < 65, or citation support < 60, or hallucination trust < 60

## Review Method

Score by reading the report against its own scope.

Check:

- whether key sections are missing
- whether major claims are evidenced
- whether dates and timing seem current enough
- whether sections contradict each other
- whether conclusions outrun the evidence

Penalize:

- generic prose that avoids specifics
- claims that appear unsupported
- strong conclusions built on weak signals
- fake precision

Do not reward polish if the content is thin.

## Output Format

Return:

```md
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

- score a report that is not provided
- assume citations exist when they do not
- give a pass score to elegant but unsupported writing
- hide low trust behind vague language

A good scorecard is specific about why the report passed or failed and what should improve next.

## Failure Handling

If the report is missing, refuse scoring and ask for the report.

If sourcing is unclear:

- lower citation support
- lower hallucination trust when claims appear fabricated or overconfident
- explain which sections triggered the downgrade
