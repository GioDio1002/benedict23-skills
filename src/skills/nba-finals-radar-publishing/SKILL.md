---
name: nba-finals-radar-publishing
description: "Scrape official NBA box-score data for ANY team's series (Finals, any playoff round, or a regular-season span) and turn it into publishable radar analysis, analyst notes, a searchable swipe-deck article, and social-ready single-player cards. Use when the agent needs a repeatable pipeline that starts from official nba_api data and ends in static HTML publishing. (a.k.a. nba-analysis-pipeline.)"
---

# NBA Series Radar Publishing

Use this skill for the full pipeline — **scrape official NBA data → analyze → generate static HTML** —
for **any team and any series**: the Finals, an earlier playoff round, or a defined regular-season
span. The "Finals vs full-playoff baseline" framing is the headline use case, but the same workflow
generalizes: pick the series, pick the comparison baseline, generate the same publishing shell.

## Responsibilities

- prefer official `stats.nba.com` data through `nba_api`
- distinguish team context, player context, and coach context
- turn one series (any team, any round) into:
  - full-team radar pages
  - player-by-player publishable pages
  - a searchable swipe-deck article (one player per card)
  - social-first card layouts

## Data acquisition (scraping)

The pipeline is parameterized by `(team, season, series scope)` — nothing is hard-coded to a specific
team or to the Finals. To target a new series:

1. Resolve the team and its games for the scope via `nba_api` (`leaguegamefinder` /
   `teamgamelogs`), filtered by `SeasonType` (`Playoffs` or `Regular Season`) and the date/round window.
2. Pull per-game player + team box scores (traditional + advanced) for those games
   (`boxscoretraditionalv3`, `boxscoreadvancedv3`), and the broader baseline split (e.g. full-playoff
   or full-season per-game) for the gray reference line.
3. Be a polite scraper: official endpoints rate-limit — add backoff/retries, cache raw JSON locally,
   and re-run analysis off the cache instead of re-hitting the API.
4. Normalize into per-player metric bundles; derived metrics (e.g. Team Score Share) keep their
   formula explicit and auditable.
5. The chosen baseline is configurable: Finals → player's full-playoff average; a playoff round →
   that player's regular-season or prior-rounds average; a regular-season span → season-to-date.
6. For the **defense expansion axes** (BLK% / STL% / Forced TOV% / Matchup Suppression), pull
   two additional endpoints: `PlayByPlayV3` for each game (so Forced TOV% can attribute each
   `EVENTMSGTYPE=5` event to the defender that produced the steal / 24-second / 5-second
   violation), and `LeagueDashPtDefend` (season-cumulative) plus per-game
   `BoxScoreMatchupsV3` for matchup-level FGM/FGA grouped by primary defender. Cache both
   alongside the traditional/advanced box scores. Publish Matchup FG% Allowed as
   `100 − MFG%` so the axis stays higher-better.

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

The published radar carries **fourteen axes** organized as offense (6) + impact (1) + defense (7):

**Offense — load + efficiency + creation**
- `TS%` — scoring efficiency
- `USG%` — possession burden
- `AST%` — creation
- `Team Score Share` — share of team scoring (role weight)
- `REB%` — board impact
- `Ball Security` (= 100 − TOV%) — clean-possession rate

**Overall impact**
- `+/-` — on-court net points
- `PIE` — official all-in-one impact

**Defense — both team-level and matchup-level signals**
- `Def. Stops` (= 120 − DefRtg) — on-court team defensive disruption
- `Foul Discipline` (= 6 − PF/G) — fouling restraint
- `BLK%` — rim protection (`100 × BLK × (TmMin/5) / (Min × OppFGA2)`)
- `STL%` — perimeter disruption (`100 × STL × (TmMin/5) / (Min × OppPoss)`)
- `Forced TOV%` — share of opponent possessions the defender forced into a giveaway,
  attributed via PlayByPlayV3 (`EVENTMSGTYPE=5` with STEAL / SCREEN_AST chains)
- `Matchup Suppression` (= 100 − Matchup FG% Allowed) — opponent FG% on possessions where
  this player is the primary defender, from `LeagueDashPtDefend` / `BoxScoreMatchupsV3`

Rules:
- Don't pair strongly overlapping axes without reason (e.g. don't also plot AST/TO when
  Ball Security and AST% are already on the radar).
- Every axis must be **higher-better** — invert TOV%, DefRtg, PF/G, and Matchup FG% Allowed
  into their positive opposites at publish time. Don't show "lower is better" tags.
- Defense is **two-layer**: team-level (Def. Stops, Foul Discipline) and matchup-level
  (BLK%, STL%, Forced TOV%, Matchup Suppression). The team-level layer answers "is the
  defense better with him on?", the matchup layer answers "what does he himself do to
  the opponent?" — keep both, they read different stories.
- Use `Player playoffs avg (Finals included)` as the third baseline, not `Finals overall
  avg`, when the reader is asking whether a player choked in the Finals — every player
  must be compared against his own full playoff level.

## Publishing guidance

- Prefer a single-page **swipe deck** over multi-page pagination: render one player per card in a
  horizontal slider (prev/next + keyboard + touch swipe) with a **top, sticky, searchable name
  picker** (above the header so it is always reachable), so readers jump between players instead of
  scrolling a long page. Keep legacy paginated URLs as redirects to the deck. Pagination is the
  fallback only when a swipe deck is not feasible.
- Keep each card short with **collapsible `<details>` sections**: the long metric-definition table is
  collapsed by default; the radar+analysis block is foldable (open by default). Recompute the deck
  viewport height on every `toggle` so the slider resizes to the open content.
- **Deck card layout = radar left, evaluation right.** Inside each player card's `main-grid`, the left
  column holds the radar SVG + legend; the right column leads with a **Finals letter-grade card**
  (square accent badge A+…F + one-line rationale) followed by the player's overall-evaluation prose,
  then the team-relative strength/weakness insight groups. The grade uses the **same analyst-style
  model as the compare page** (volume × absolute efficiency + impact + role bonus + outcome/FMVP),
  baked statically at build time from each card's own Finals stat line — so the per-team decks and the
  head-to-head compare page show a consistent grade for the same player.
- Offer a **head-to-head compare page** alongside the per-team decks: two searchable pickers (player
  A vs player B, drawn from every player on both teams), and a metric-by-metric delta table.
  - **Recast the lower-is-better axes as positive opposites** (don't just invert for plotting):
    TOV% → Ball Security (100−TOV), DefRtg → Def. Stops (120−DefRtg), PF/G → Foul Discipline (6−PF),
    and rewrite their definitions accordingly. Then all ten axes are higher-better — no "lower is
    better" tags needed, and radar area is meaningful.
  - Each player carries three series — **Finals, playoff average, team average** — and every series is
    a **click-to-hide** legend toggle.
  - A **mode switch**: *Overlay* (A vs B on one radar) and *Split* (two separate per-player radars,
    each showing that player's three series for readability). The comparison table follows the mode —
    A-vs-B edge table in overlay; per-player Finals/playoff/team tables in split.
  - **Sticky global filter bar with native `<select>` per side** — A left, B right, in a
    `position:sticky; top:0` bar so the reader can re-pick either player from anywhere on
    the page without scrolling back up. Each side is a native `<select>` whose options are
    grouped by team via `<optgroup>` (Knicks group, Spurs group). The **Overlay/Split mode
    toggle and the per-series legend chips live INSIDE this same sticky bar** (a second row
    under the two selects) — all controls scroll-pinned together so the reader never loses
    them mid-page. The selected-player subline shows team · position only — **no minutes**
    (MPG is redundant with the stat-mini fold and just clutters the bar). **Do not build a custom
    popover/dropdown inside a collapsible card** — a `<details>` fold has `overflow:hidden`,
    which clips any absolutely-positioned popover so it never appears. The native select's
    dropdown is browser-rendered above all stacking contexts and cannot be clipped; it is
    the robust choice here. (This is the concrete bug that killed the earlier popover
    picker.) The select keeps the per-side accent border (A blue, B orange) but otherwise
    uses the cream theme — no colored chip fills.
  - **Layout order**: sticky filter bar → mode toggle row → radar fold → overall-evaluation
    fold → **per-game stat-mini fold** → data-table fold. The 6-panel per-game basic stats
    sit in their own `<details open>` **below the overall evaluation** (not up by the
    picker), A and B side-by-side with colored captions — descriptive context belongs after
    the analytical read, and it stays collapsible.
  - Each picker's subtitle carries the **six stat-mini panels** (MPG / PPG / APG / RPG / TOPG /
    PFPG) for the currently selected player — same six chips as the per-player deck card — so the
    head-to-head context is visible before the user even reads the radar.
  - Wrap the radar block, the **per-player overall-evaluation cards**, and the comparison
    table each in their own `<details open>` so readers can fold any of the three
    independently. The overall-evaluation fold sits **between radar and table**.
  - On the compare page the evaluation cards are **head-to-head generated**, not deck prose:
    each card reads the other side's vector and writes delta-driven sentences (USG /
    Score Share for burden, TS% for efficiency, the larger of AST% / REB% for the
    secondary trait, the three defensive axes as a single line, +/- and PIE for impact).
    Same-roster pairings get a "队内对位 / Same-roster matchup" lead; cross-team pairs
    get "跨队对位 / Cross-team head-to-head." Regenerate whenever the picker changes.
  - **Drop "A" / "B" labels entirely** once players are selected — the eyebrow shows just
    "OVERALL EVALUATION", the colored left rule + colored tag handle side identity, and
    the player name in the h4 carries the identity. Generic A/B labels are misleading
    once both candidates are named.
  - Open each card with a **Finals letter grade** (A+ through F) rendered as a colored
    square badge next to the player's name, plus a one-line rationale row above the
    prose stating the absolute stat line and series outcome.

    **Grading model — analyst-style, not vs-self.** Earlier iterations graded "Finals vs
    own playoff baseline." That punishes Finals MVPs whose efficiency dips against tougher
    defense (e.g. a 36% USG FMVP at 53% TS reads as "down from 57%" and gets a D — wrong).
    The model below mirrors how working NBA writers actually grade a Finals series: volume
    × absolute efficiency, absolute impact, role-fit credit, and the series outcome itself
    as a categorical signal (rings + FMVP are the loudest signals in any analyst piece).

    Score = `volumeTier × efficiencyCredit + impactTerm + roleBonus + outcomeMod`

    - `volumeTier`: high (USG ≥28 or MPG ≥36) = 1.0 · mid (USG ≥22 or MPG ≥30) = 0.7 ·
      rotation (MPG ≥18) = 0.45 · scrub = 0.25. Heavy-load roles weight efficiency more.
    - `efficiencyCredit` (absolute TS%, not delta): ≥62 → +12 · ≥58 → +8 · ≥54 → +4 ·
      ≥50 → 0 · ≥46 → −4 · ≥42 → −9 · else −14.
    - `impactTerm`: `0.8 × clamp(+/-, −15, +15)` plus a PIE-around-12 spline (above 18
      worth +1.5/pp, 12–18 worth +0.6/pp, below 12 worth −1.4/pp).
    - `roleBonus`: efficient role player (USG <22 + TS ≥60 + MPG ≥20) +4 · efficient star
      (USG ≥28 + TS ≥55) +5 · alpha creator threshold (USG ≥32 + TS ≥53) +4.
    - `outcomeMod`: series winner +6 · FMVP +14 (categorical, mirrors analyst weight) ·
      alpha on losing side dragged team (USG ≥28 + +/- ≤−3) −4 · small-minute loser −1.
    - Small-sample clamp: when MPG <12, score is clamped to `[−8, +4]` (C+ … B). Don't
      hand out A's or F's on a 6-minute sample.

    Buckets: `≥26 A+ · ≥20 A · ≥14 A- · ≥8 B+ · ≥2 B · ≥-4 B- · ≥-10 C+ · ≥-16 C ·
    ≥-22 D · else F`.

    Sanity-check on 2026 Knicks–Spurs: Jalen Brunson (USG 36.6 · TS 53.2 · +/- +1.6 ·
    PIE 15.2 · Knicks won · FMVP) → ~27.2 → **A+**. Karl-Anthony Towns (USG 18.6 · TS
    68.4 · efficient secondary on winning side) → A+. Wembanyama (USG 29.7 · TS 58.9 ·
    losing side star) → B+. The numbers should track common analyst takes; if they don't,
    tune the constants — don't fall back to vs-self deltas.

    **Per-series knobs** (set in compare-page META): `seriesWinner` (team key), `fmvp`
    (player display name), `fmvpTag` / `winTag` / `lossTag` (i18n strings shown in the
    rationale row). When publishing a new series, set these four — the grading code is
    generic.

    The grade reads the player's Finals form **in the analyst sense** (absolute role +
    efficiency + result), while the comparison prose reads him against the picked
    opponent — two complementary lenses in one card.
  - **ZH radar axis labels stack the Chinese term over the English short** (e.g. 真实命中率 / TS%);
    EN radars use the English short alone. Apply the same convention across deck and compare radars
    so a reader can match terms across pages.
- Bind the per-team decks and the compare page under one **unified entry** (`2026-nba-finals/`,
  titled "2026 NBA 总决赛球员表现分析") with a **collapsible left sidebar**, hash-routed:
  - Sidebar order surfaces the most analytical view first: **Comparison → Team A → Team B →
    Metrics & Data** (`#compare` / `#<teamA>` / `#<teamB>` / `#definitions`). Comparison is the
    default landing view.
  - Collapse UX must be **obvious, not hidden**: a dedicated `«` button next to the brand title,
    plus the brand title itself clickable, both collapse. When collapsed, a labeled floating
    `☰ Expand` button (icon + text, not just an icon) sits top-left so the entry point is
    discoverable on first look.
  - **One language switch, scoped to the whole shell** — never two. The sidebar carries no
    EN/中文 link; the language toggle lives only inside the iframe pages (top-right of each
    child page) AND the shell intercepts clicks on `.lang-switch a` / `[data-lang-switch]`
    inside the iframe to redirect the *parent* to the counterpart shell URL with the same
    `#hash`. Otherwise the iframe swaps language while the sidebar stays in the old
    language — confusing and broken. Every iframe-loaded child page (decks, compare,
    definitions) must carry one lang-switch element so the user has a switch from every
    view.
- Publish a **Metrics & Data** companion page (`#definitions`) that documents the radar's ten
  axes (Chinese + English name, exact formula, what the metric *means on the court*) as a
  fixed-layout table, then walks through the **seven-step data acquisition pipeline**: source
  endpoints (`LeagueGameFinder`, `TeamGameLogs`, `BoxScoreTraditionalV3`, `BoxScoreAdvancedV3`),
  caching strategy, polite-scrape rate-limit / UA discipline, the three baselines (Finals /
  player full-playoff / team-Finals), derived-metric formulas, cross-verification against
  `BoxScoreSummaryV2` and the public stats.nba.com page (≤0.5pp tolerance), and per-axis
  min/max normalization. This page is the reproducibility receipt — without it the radars
  read as black-box analytics.
- Long-form article pages should be paginated when one page becomes too long to read comfortably.
- Single-player pages should be easy to convert into image cards.
- Keep English and Chinese publishing shells aligned when labels, baselines, or explanatory summaries change.
- Avoid machine-specific links in published output.
- Prefer repository-relative site links and stable slugs.

## Overall-evaluation writing

The per-player "overall evaluation" must read like a professional analyst, not a template. Every
sentence has to carry a concrete number and a judgment; never emit filler clauses such as "needs to
be read in role context" or "efficiency is neutral" that assert nothing.

Build each evaluation from the player's own stat line, anchored on comparisons (Finals value vs the
player's full-playoff value vs team average):

- **Burden** — classify role from USG% and Team Score Share (primary / secondary / complementary /
  low-usage off-ball), and state the minutes load.
- **Efficiency** — compare Finals TS% against the player's own playoff TS%; report the signed gap in
  points and call it a drop, a rise, or holding. Add an absolute read only at the extremes
  (elite ≥60%, cold <48%).
- **One salient secondary trait** — pick the most deviant of: turnover security (TOV%), creation
  (AST%), rebounding (REB%), or defense (DefRtg vs playoff). Skip the rest.
- **On-court impact + verdict** — report +/- vs the player's playoff on-court mark, then a one-line
  verdict synthesized from the efficiency gap, +/- delta, and PIE delta (matched/beat baseline,
  mixed, or clear step down).
- **Small samples** — for sub-10-minute players, do not over-read: state the minutes, flag the
  sample as too small, and stop. No manufactured insight.

Keep the English and Chinese versions generated from the same computed facts so they stay aligned.

## Visual design (radar article shell)

A naturalist, scholarly design language (huasheng.ai/parrots-inspired) is shared by every radar
article page. Shared rules live in the site stylesheet under the `.article-radar-body` scope so both
languages and every page stay aligned; do not fork per-page styles.

- Palette: warm cream background, team primary as the single accent (Knicks `#006BB6`, secondary
  `#F58426`), naturalist neutrals. No gradients on content surfaces.
- Typography: Playfair Display (italic serif, player names) / Inter (body) / JetBrains Mono (stats and numbers).
- Radar SVG colors are swapped client-side by injected JS (team color and reference/gray line),
  not by rewriting the SVG path data.
- Summary ("overall evaluation") block uses the same flat-card scheme as the stat chips: light
  surface, hairline border, accent left-rule, dark body text, uppercase accent label. Never a dark
  or gradient fill — it must stay readable.
- Stat tables use `table-layout: fixed`: keep the metric and the three value columns narrow and give
  the definition/note column the majority of the width so notes flow wide instead of stacking tall.
- Insight sentiment uses ↑/↓ arrows (good/bad), not colored left-border accent cards or chips.
- Do not render a redundant per-card score badge in the player-header corner.
- **Cross-page metric consistency**: every published radar — per-team deck and head-to-head compare
  alike — uses the positive-opposite naming (Ball Security / Def. Stops / Foul Discipline) so all ten
  axes are higher-better. Radar geometry is consistent too: axis 0 (TS%) at the top, going clockwise.
  Per-axis normalization uses min/max across all players on the page so cross-player comparison stays
  meaningful. ZH radars stack the Chinese term over the English short on every axis (e.g. 真实命中率
  / TS%; 护球率 / Ball Security); EN radars use the English short alone.
- When the metric polarity is flipped, also regenerate any precomputed delta-pill / insight cards —
  or drop them — so their wording and percentages stay consistent with the new positive metrics.

## Mobile / responsive

The published deck must read well on a phone, not just desktop:

- Header: below ~720px the language toggle goes `position: static` and stacks above the title — never
  absolutely positioned where it can overlap the `<h1>`. Scale the heading down (`clamp` to ~1.9rem).
- Stat chips collapse to 2 columns; the radar/insights grid collapses to a single column.
- The name picker stays a sticky bar; chips scroll horizontally; the search box goes full width.
- Swipe-deck navigation works by touch swipe (pointer events) in addition to buttons and arrow keys.
- Verify at 390px width (one common phone viewport) before shipping.

## URL & title naming

- Publish the deck as a clean directory `index.html` (e.g. `.../2026-nba-finals-knicks-radars/`),
  not `page-1.html`; redirect any legacy paginated URLs to it.
- When a deck is loaded inside the unified-shell iframe, **drop the per-page "All articles /
  Site home" nav block** — the shell sidebar already owns cross-view navigation, so the
  in-iframe nav is redundant. Also don't cap the zh `article-header h1` width so tight that
  a short title (e.g. `2026 尼克斯总决赛表现`) wraps to a second line — `text-wrap: balance`
  plus a narrow `max-width` will force an ugly mid-word CJK break; give it room for one line.
- Give each page a descriptive, branded `<title>` (e.g. `2026 NBA Finals · Knicks Player Performance
  | benedict23`) rather than a bare or numbered title — it is the tab label and the share preview name.
