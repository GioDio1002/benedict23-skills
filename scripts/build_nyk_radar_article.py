#!/usr/bin/env python3
import argparse
import math
import re
from pathlib import Path


ARTICLE_SLUG = "2026-nba-finals-knicks-radars"


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


def article_shell(*, page_title: str, page_headline: str, page_intro: str, page_no: int, total_pages: int, body: str, local_style: str) -> str:
    prev_href = f"page-{page_no - 1}.html" if page_no > 1 else None
    next_href = f"page-{page_no + 1}.html" if page_no < total_pages else None
    prev_button = f'<a class="button" href="{prev_href}">Previous Page</a>' if prev_href else '<span class="button disabled">Previous Page</span>'
    next_button = f'<a class="button" href="{next_href}">Next Page</a>' if next_href else '<span class="button disabled">Next Page</span>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
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
      <h1>{page_headline}</h1>
      <p>{page_intro}</p>
      <div class="nav">
        <a href="../index.html">All Articles</a>
        <a href="../../index.html">Site Home</a>
      </div>
      <div class="pager">
        {prev_button}
        <div class="pager-note">Page {page_no} / {total_pages}</div>
        {next_button}
      </div>
    </section>
    <section class="embed-shell">
      {body}
    </section>
    <footer class="footer">Article rebuilt from the latest local Knicks Finals radar artifact for GitHub Pages publishing.</footer>
  </main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--per-page", type=int, default=4)
    args = parser.parse_args()

    source = Path(args.source)
    output_root = Path(args.output_root)
    html = source.read_text(encoding="utf-8")
    style = sanitize_style(extract_style(html))
    sections = extract_sections(html)

    article_dir = output_root / "articles" / ARTICLE_SLUG
    article_dir.mkdir(parents=True, exist_ok=True)

    total_pages = math.ceil(len(sections) / args.per_page)
    headline = "2026 NBA Finals · New York Knicks Radar Book"
    intro = "A paginated reading version of the Knicks Finals radar analysis. Each page carries part of the original player-by-player breakdown so the article stays readable on GitHub Pages."

    for idx in range(total_pages):
        start = idx * args.per_page
        end = start + args.per_page
        page_sections = "\n".join(sections[start:end])
        page_html = article_shell(
            page_title=f"{headline} · Page {idx + 1}",
            page_headline=headline,
            page_intro=intro,
            page_no=idx + 1,
            total_pages=total_pages,
            body=f'<div class="article-radar-body">{page_sections}</div>',
            local_style=style,
        )
        (article_dir / f"page-{idx + 1}.html").write_text(page_html, encoding="utf-8")


if __name__ == "__main__":
    main()
