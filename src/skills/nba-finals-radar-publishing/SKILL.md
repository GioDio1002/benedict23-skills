---
name: nba-finals-radar-publishing
description: "Turn official NBA Finals box score data into publishable radar analysis, coach notes, paginated long-form articles, and Xiaohongshu-ready single-player cards. Use when Codex needs a repeatable workflow for playoff or Finals coverage that starts from official nba_api data and ends in static HTML publishing."
---

# NBA Finals Radar Publishing

Use this skill when the task is NBA playoff or Finals coverage that needs both analysis and publishing.

## Responsibilities

- prefer official `stats.nba.com` data through `nba_api`
- distinguish team context, player context, and coach context
- turn one series into:
  - full-team radar pages
  - player-by-player publishable pages
  - paginated long-form article pages
  - social-first card layouts

## Workflow

1. Gather official game-level data for the whole series.
2. Keep only players with real minutes.
3. Build per-player Finals metric bundles.
4. Remove redundant axes when two metrics tell the same story.
5. Add a player-specific playoffs baseline when evaluating Finals drop-off:
   - fetch `SeasonType=Playoffs` player and team per-game stats
   - include Finals inside that playoffs average
   - use this as the gray comparison line instead of a generic Finals overall average
6. Render:
   - team radar overview
   - player pages
   - article index
   - paginated article pages
7. Keep labels readable in both Chinese and English when publishing.

## Metric guidance

- Do not pair strongly overlapping axes without reason.
- Prefer:
  - `TS%` for scoring efficiency
  - `Team Score Share` for scoring burden
  - `USG%` for possession burden
  - `AST%` for creation
  - `REB%` for board impact
  - `AST/TO` for decision quality
  - `PIE` for overall game impact
  - `NetRtg` for on-court results
- Avoid using `Finals overall avg` as the third radar/table baseline when the reader is asking whether a player choked in the Finals. Use `Player playoffs avg (Finals included)` so each player is compared against his own full playoff level.

## Publishing guidance

- Long-form article pages should be paginated when one page becomes too long to read comfortably.
- Single-player pages should be easy to convert into image cards.
- Keep English and Chinese publishing shells aligned when labels, baselines, or explanatory summaries change.
- Avoid machine-specific links in published output.
- Prefer repository-relative site links and stable slugs.
