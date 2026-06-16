#!/usr/bin/env python3
import argparse
import math
import re
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


def localize_section(section: str, lang: str) -> str:
    if lang != "zh":
        return section
    for english, chinese in NAME_MAP.items():
        section = section.replace(english, chinese)
    for english, chinese in ROLE_MAP.items():
        section = section.replace(english, chinese)
    section = section.replace("PPG", "场均得分")
    section = section.replace("MPG", "场均分钟")
    return section


def article_shell(*, html_lang: str, page_title: str, page_headline: str, page_intro: str, page_no: int, total_pages: int, body: str, local_style: str, footer_note: str, article_index_href: str, site_home_href: str, prev_label: str, next_label: str, page_label: str, switch_label: str, switch_href: str, all_articles_label: str, site_home_label: str) -> str:
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
  <link rel="stylesheet" href="../../assets/site.css">
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
    page_label = "Page" if args.lang == "en" else "第"
    page_title_label = "Page" if args.lang == "en" else "第"
    prev_label = "Previous Page" if args.lang == "en" else "上一页"
    next_label = "Next Page" if args.lang == "en" else "下一页"
    switch_label = "中文版" if args.lang == "en" else "English"
    all_articles_label = "All Articles" if args.lang == "en" else "全部文章"
    site_home_label = "Site Home" if args.lang == "en" else "站点首页"
    html_lang = "en" if args.lang == "en" else "zh-CN"

    for idx in range(total_pages):
        start = idx * args.per_page
        end = start + args.per_page
        page_sections = "\n".join(localize_section(section, args.lang) for section in sections[start:end])
        if args.lang == "en":
            switch_href = f"../../zh/articles/{args.slug}/page-{idx + 1}.html"
        else:
            switch_href = f"../../articles/{args.slug}/page-{idx + 1}.html"
        page_html = article_shell(
            html_lang=html_lang,
            page_title=f"{args.headline} · {page_title_label}{idx + 1}{'' if args.lang == 'en' else '页'}",
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


if __name__ == "__main__":
    main()
