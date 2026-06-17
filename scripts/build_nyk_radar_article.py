#!/usr/bin/env python3
import argparse
import json
import logging
import math
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

NAME_MAP = {
    "Jalen Brunson": "杰伦·布伦森",
    "OG Anunoby": "OG·阿奴诺比",
    "Mikal Bridges": "米卡尔·布里奇斯",
    "Karl-Anthony Towns": "卡尔-安东尼·唐斯",
    "Josh Hart": "约什·哈特",
    "Landry Shamet": "兰德里·沙梅特",
    "Mitchell Robinson": "米切尔·罗宾逊",
    "Miles McBride": "迈尔斯·麦克布莱德",
    "Jose Alvarado": "何塞·阿尔瓦拉多",
    "Jordan Clarkson": "乔丹·克拉克森",
    "Ariel Hukporti": "阿里埃尔·胡克波尔蒂",
    "Jeremy Sochan": "杰里米·索汉",
    "Victor Wembanyama": "维克托·文班亚马",
    "Devin Vassell": "德文·瓦塞尔",
    "De'Aaron Fox": "德阿隆·福克斯",
    "Stephon Castle": "斯蒂芬·卡斯尔",
    "Julian Champagnie": "朱利安·尚帕尼",
    "Dylan Harper": "迪伦·哈珀",
    "Keldon Johnson": "凯尔登·约翰逊",
    "Harrison Barnes": "哈里森·巴恩斯",
    "Luke Kornet": "卢克·科内特",
    "Carter Bryant": "卡特·布莱恩特",
}

ROLE_MAP = {
    "Alpha creator": "头号持球核心",
    "Secondary creator": "第二发起点",
    "Interior anchor": "内线支柱",
    "Floor spacer": "空间点",
    "Rotation connector": "轮换连接器",
    "Bench specialist": "替补功能位",
}

ENGLISH_REPLACEMENTS = (
    ("球员季后赛均值（含总决赛）", "Player playoffs avg (Finals included)"),
    ("定义 / 备注", "Definition / note"),
    ("综合评价", "Overall evaluation"),
    ("相对季后赛表现", "Vs playoff baseline"),
    ("相对季后赛", "Vs playoff baseline"),
    ("场均分钟", "MPG"),
    ("场均得分", "PPG"),
    ("场均助攻", "APG"),
    ("场均篮板", "RPG"),
    ("场均失误", "TOPG"),
    ("场均犯规", "PFPG"),
    ("队内得分占比 Team Score Share", "Team Score Share"),
    ("真实命中率 TS%", "True Shooting TS%"),
    ("使用率 USG%", "Usage Rate USG%"),
    ("助攻率 AST%", "Assist Rate AST%"),
    ("篮板率 REB%", "Rebound Rate REB%"),
    ("失误率 TOV%", "Turnover Rate TOV%"),
    ("正负值 +/-", "Plus/Minus +/-"),
    ("防守效率 DefRtg", "Defensive Rating DefRtg"),
    ("犯规 PF/G", "Personal Fouls PF/G"),
    ("纽约尼克斯", "New York Knicks"),
    ("圣安东尼奥马刺", "San Antonio Spurs"),
    ("队内相对优势", "Team-relative strengths"),
    ("队内相对短板", "Team-relative gaps"),
    ("总决赛总体均值", "Player playoffs avg"),
    ("本队均值", "Team avg"),
    ("队内均值", "Team avg"),
    ("维度", "Metric"),
    ("球员", "Player"),
    ("真实命中率", "True Shooting"),
    ("使用率", "Usage Rate"),
    ("助攻率", "Assist Rate"),
    ("队内得分占比", "Team Score Share"),
    ("篮板率", "Rebound Rate"),
    ("失误率", "Turnover Rate"),
    ("正负值", "Plus/Minus"),
    ("防守效率", "Defensive Rating"),
    ("犯规", "Personal Fouls"),
    ("综合两分、三分和罚球后的得分效率。和队内得分占比都与得分有关，但 TS% 只看效率，不看产量。", "Scoring efficiency across twos, threes, and free throws. It overlaps with Team Score Share only at the scoring level: TS% measures efficiency, not volume."),
    ("个人终结回合占球队回合的比例。和队内得分占比都反映负荷，但 USG% 看球权占用，不等于真实得分产出。", "Share of team possessions finished by the player. It is related to Team Score Share as a burden stat, but USG% measures possession load rather than actual scoring output."),
    ("队友进球中有多少比例直接来自该球员助攻。和使用率都描述持球，但 AST% 更偏组织而不是终结。", "Estimated share of teammates' made field goals assisted by the player. It sits near USG% because both describe on-ball role, but AST% focuses on creation rather than finishing."),
    ("个人得分占本队得分的比例。和 USG% 相近但不相同，因为它看结果得分，不看所有终结回合。", "Player points divided by team points. It is close to USG% in spirit, but it measures realized scoring output rather than total finishing load."),
    ("在场时可争抢篮板中该球员拿到的比例。相对独立，主要反映篮板控制和回合终结能力。", "Estimated share of available rebounds collected while on court. This is relatively independent and mainly reflects board control and possession finishing."),
    ("每 100 个个人回合消耗里出现多少失误。和使用率存在弱相关，但它只衡量回合终结失误，数值越低越好。", "Turnovers per 100 individual plays used. It has some relationship with USG%, but it isolates possession-ending mistakes only, and lower is better."),
    ("球员在场时球队净胜分。它会吸收队友、对手和阵容环境，是结果值，不是纯个人技术。", "Team point differential while the player is on court. It absorbs teammate, opponent, and lineup context, so it is an outcome stat rather than a pure individual skill stat."),
    ("球员在场时球队每百回合失分。和正负值都受阵容影响，但 DefRtg 更聚焦防守端，数值越低越好。", "Team points allowed per 100 possessions while the player is on court. It shares lineup context with Plus/Minus, but it is more defense-specific, and lower is better."),
    ("每场个人犯规数。它与防守侵略性有关，但更多反映犯规控制，不等于防守质量，数值越低越好。", "Personal fouls committed per game. It is related to defensive aggression, but mostly reflects foul discipline rather than defensive quality, and lower is better."),
    ("NBA 官方综合比赛影响指标，汇总得分、篮板、助攻、失误等。它最不独立，因为已经吸收多个单项维度。", "NBA's official all-in-one impact metric combining scoring, rebounding, assists, turnovers, and more. It is the least independent dimension because it already contains several box-score components."),
)

ENGLISH_SUMMARY = (
    "This radar compares 2026 NBA Finals performance against team Finals average "
    "and the player's full 2025-26 playoffs average, with Finals included. The gray "
    "line helps show whether the player dropped from his wider playoff level. PIE is "
    "a composite metric, so it should be read more as an overall snapshot than as an "
    "independent skill axis."
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "nba-finals-radar-publishing",
            "env": os.getenv("APP_ENV", "local"),
            "trace_id": getattr(record, "trace_id", ""),
            "request_id": getattr(record, "request_id", ""),
            "user_id": getattr(record, "user_id", ""),
            "status_code": getattr(record, "status_code", ""),
            "duration_ms": getattr(record, "duration_ms", ""),
        }
        return json.dumps(payload, ensure_ascii=True)


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("nba_finals_radar_publishing")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def extract_style(html: str) -> str:
    match = re.search(r"<style>(.*?)</style>", html, re.S)
    if not match:
        raise ValueError("style block not found")
    return match.group(1).strip()


def sanitize_style(style: str) -> str:
    lines = style.splitlines()
    blocked_prefixes = (
        "body{",
        "body {",
        ".container{",
        ".container {",
        "header{",
        "header {",
        "header h1{",
        "header h1 {",
        "header .meta{",
        "header .meta {",
    )
    kept = []
    skip_depth = 0
    for line in lines:
        stripped = line.strip()
        if skip_depth > 0:
            skip_depth += line.count("{") - line.count("}")
            continue
        if stripped.startswith(blocked_prefixes):
            skip_depth = line.count("{") - line.count("}")
            if skip_depth < 0:
                skip_depth = 0
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def extract_sections(html: str) -> list[str]:
    sections = re.findall(r'(<section class="player-section">.*?</section>)', html, re.S)
    if not sections:
        raise ValueError("no player sections found")
    return sections


def englishize_section(section: str) -> str:
    section = re.sub(r" · (\d+) 场 · ", r" · \1 Games · ", section)
    section = re.sub(r" · (\d+) 场(?=<)", r" · \1 Games", section)
    section = re.sub(r"角色: ([^。]+)。场均 ([0-9.]+) 分钟，说明这是稳定轮换而不是临时补位。", r"Role: \1. Averaged \2 minutes, which marks a stable rotation spot rather than an emergency cameo.", section)
    section = re.sub(r"高持球负荷。USG ([0-9.]+%)，说明很多回合以他收尾。", r"Heavy on-ball burden. USG \1 shows that many possessions finished with him.", section)
    section = re.sub(r"偏组织驱动。AST% ([0-9.]+%)，更多承担串联而非纯终结。", r"More creator-driven. AST% \1 points to setup work over pure finishing.", section)
    section = re.sub(r"空间价值明确。场均三分出手 ([0-9.]+) 次，主要拉开半场。", r"Clear spacing value. Averaged \1 three-point attempts and mainly stretched the halfcourt.", section)
    section = re.sub(r"低触球补位型角色。更多靠防守、篮板或短回合终结提供价值。", r"Low-touch complementary role. Value comes more from defense, rebounding, or short-play finishing.", section)
    section = re.sub(r"终结效率高。TS ([0-9.]+%)，属于系列赛强点。", r"High finishing efficiency. TS \1 was a real series strength.", section)
    section = re.sub(r"终结效率偏低。TS ([0-9.]+%)，若高持球则会拖慢进攻回报。", r"Below-par finishing efficiency. TS \1 can drag down returns if paired with heavy usage.", section)
    section = re.sub(r"终结效率中性。TS ([0-9.]+%)，更多要结合角色理解。", r"Neutral finishing efficiency. TS \1 needs to be read in role context.", section)
    section = re.sub(r"在场赢分明显。Net Rating ([+-][0-9.]+)。", r"Clear on-court winning impact. Net Rating \1.", section)
    section = re.sub(r"在场容易被打击。Net Rating ([+-][0-9.]+)。", r"On-court minutes were vulnerable. Net Rating \1.", section)
    section = re.sub(r"在场净胜负接近中性。Net Rating ([+-][0-9.]+)。", r"On-court net margin stayed close to neutral. Net Rating \1.", section)
    section = re.sub(
        r"这张雷达对比的是 2026 总决赛表现、本队总决赛均值，以及该球员整个 2025-26 季后赛均值（含总决赛）。灰线可用来判断球员是否在总决赛相对季后赛整体下滑。生成时间 [^。]+。",
        ENGLISH_SUMMARY,
        section,
    )
    section = re.sub(
        r"这张雷达对比的是 2026 总决赛表现、本队总决赛均值，以及该球员整个 2025-26 季后赛均值（含总决赛）。灰线可用来判断球员是否在总决赛相对季后赛整体下滑。PIE 是综合指标，和多个单项维度存在包含关系，因此解读时应更多把它当成总览。生成时间 [^。]+。",
        ENGLISH_SUMMARY,
        section,
    )
    section = re.sub(
        r"这张雷达不是常规赛全联盟画像，而是 2026 总决赛这轮系列赛画像。横向基准是“本队均值 \+ 全系列均值”。生成时间 [^。]+。",
        ENGLISH_SUMMARY,
        section,
    )
    section = re.sub(r"比队内均值 ([+-]?[0-9.]+%?)。", r"vs team avg \1.", section)
    section = re.sub(r"低于队内均值 ([0-9.]+%?)。", r"below team avg by \1.", section)
    section = re.sub(r"高于队内均值 ([0-9.]+%?)。", r"above team avg by \1.", section)
    section = re.sub(r"比季后赛整体好 ([0-9.]+%)", r"\1 better than full playoffs", section)
    section = re.sub(r"比季后赛整体差 ([0-9.]+%)", r"\1 worse than full playoffs", section)
    for chinese, english in sorted(ENGLISH_REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
        section = section.replace(chinese, english)
    return section


def localize_section(section: str, lang: str) -> str:
    if lang == "en":
        return englishize_section(section)
    if lang != "zh":
        return section
    for english, chinese in NAME_MAP.items():
        section = section.replace(english, chinese)
    for english, chinese in ROLE_MAP.items():
        section = section.replace(english, chinese)
    section = section.replace("PPG", "场均得分")
    section = section.replace("MPG", "场均分钟")
    return section


def article_shell(*, html_lang: str, css_href: str, page_title: str, page_headline: str, page_intro: str, page_no: int, total_pages: int, body: str, local_style: str, footer_note: str, article_index_href: str, site_home_href: str, prev_label: str, next_label: str, page_label: str, switch_label: str, switch_href: str, all_articles_label: str, site_home_label: str) -> str:
    prev_href = f"page-{page_no - 1}.html" if page_no > 1 else None
    next_href = f"page-{page_no + 1}.html" if page_no < total_pages else None
    prev_button = f'<a class="button" href="{prev_href}">{prev_label}</a>' if prev_href else f'<span class="button disabled">{prev_label}</span>'
    next_button = f'<a class="button" href="{next_href}">{next_label}</a>' if next_href else f'<span class="button disabled">{next_label}</span>'
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <link rel="stylesheet" href="{css_href}">
  <style>{local_style}</style>
</head>
<body>
  <main class="page">
    <section class="article-header">
      <div class="lang-switch"><a class="button" href="{switch_href}">{switch_label}</a></div>
      <h1>{page_headline}</h1>
      <p>{page_intro}</p>
      <div class="nav">
        <a href="{article_index_href}">{all_articles_label}</a>
        <a href="{site_home_href}">{site_home_label}</a>
      </div>
      <div class="pager">
        {prev_button}
        <div class="pager-note">{page_label} {page_no} / {total_pages}</div>
        {next_button}
      </div>
    </section>
    <section class="embed-shell">
      {body}
    </section>
    <footer class="footer">{footer_note} · <a href="https://github.com/GioDio1002/benedict23-skills/tree/main/src/skills/nba-finals-radar-publishing">Generated with skill: nba-finals-radar-publishing</a></footer>
  </main>
</body>
</html>
"""


def main():
    started = time.perf_counter()
    logger = configure_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--per-page", type=int, default=4)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--headline", required=True)
    parser.add_argument("--intro", required=True)
    parser.add_argument("--footer-note", default="Article rebuilt from the latest local radar artifact for GitHub Pages publishing.")
    parser.add_argument("--lang", choices=["en", "zh"], default="en")
    args = parser.parse_args()

    source = Path(args.source)
    output_root = Path(args.output_root)
    html = source.read_text(encoding="utf-8")
    style = sanitize_style(extract_style(html))
    sections = extract_sections(html)

    article_root = output_root / "articles" / args.slug if args.lang == "en" else output_root / "zh" / "articles" / args.slug
    article_dir = article_root
    article_dir.mkdir(parents=True, exist_ok=True)

    total_pages = math.ceil(len(sections) / args.per_page)
    article_index_href = "../index.html"
    site_home_href = "../../index.html"
    css_href = "../../assets/site.css" if args.lang == "en" else "../../../assets/site.css"
    page_label = "Page" if args.lang == "en" else "第"
    page_title_label = "Page" if args.lang == "en" else "第"
    prev_label = "Previous Page" if args.lang == "en" else "上一页"
    next_label = "Next Page" if args.lang == "en" else "下一页"
    switch_label = "Chinese" if args.lang == "en" else "English"
    all_articles_label = "All Articles" if args.lang == "en" else "全部文章"
    site_home_label = "Site Home" if args.lang == "en" else "站点首页"
    html_lang = "en" if args.lang == "en" else "zh-CN"

    for idx in range(total_pages):
        start = idx * args.per_page
        end = start + args.per_page
        page_sections = "\n".join(localize_section(section, args.lang) for section in sections[start:end])
        page_title_suffix = f"{page_title_label} {idx + 1}" if args.lang == "en" else f"{page_title_label}{idx + 1}页"
        if args.lang == "en":
            switch_href = f"../../zh/articles/{args.slug}/page-{idx + 1}.html"
        else:
            switch_href = f"../../../articles/{args.slug}/page-{idx + 1}.html"
        page_html = article_shell(
            html_lang=html_lang,
            css_href=css_href,
            page_title=f"{args.headline} · {page_title_suffix}",
            page_headline=args.headline,
            page_intro=args.intro,
            page_no=idx + 1,
            total_pages=total_pages,
            body=f'<div class="article-radar-body">{page_sections}</div>',
            local_style=style,
            footer_note=args.footer_note,
            article_index_href=article_index_href,
            site_home_href=site_home_href,
            prev_label=prev_label,
            next_label=next_label,
            page_label=page_label,
            switch_label=switch_label,
            switch_href=switch_href,
            all_articles_label=all_articles_label,
            site_home_label=site_home_label,
        )
        (article_dir / f"page-{idx + 1}.html").write_text(page_html, encoding="utf-8")

    logger.info(
        "radar article pages generated",
        extra={
            "trace_id": f"{args.slug}:{args.lang}",
            "request_id": args.slug,
            "user_id": "local",
            "status_code": "200",
            "duration_ms": str(round((time.perf_counter() - started) * 1000, 2)),
        },
    )


if __name__ == "__main__":
    main()
