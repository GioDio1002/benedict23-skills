import json
import logging

from build_nyk_radar_article import JsonFormatter, englishize_section, article_shell, sanitize_style


def test_sanitize_style_removes_page_level_rules():
    style = """
body{background:#000}
.container{max-width:1280px}
header h1{font-size:42px}
.player-section{padding:24px}
"""
    cleaned = sanitize_style(style)

    assert "body{" not in cleaned
    assert ".container{" not in cleaned
    assert "header h1{" not in cleaned
    assert ".player-section" in cleaned


def test_article_shell_uses_custom_footer():
    html = article_shell(
        html_lang="en",
        css_href="../../assets/site.css",
        page_title="T",
        page_headline="H",
        page_intro="I",
        page_no=1,
        total_pages=2,
        body="<div>body</div>",
        local_style="",
        footer_note="custom footer",
        article_index_href="../index.html",
        site_home_href="../../index.html",
        prev_label="Previous Page",
        next_label="Next Page",
        page_label="Page",
        switch_label="Chinese",
        switch_href="../../zh/articles/demo/page-1.html",
        all_articles_label="All Articles",
        site_home_label="Site Home",
    )

    assert "custom footer" in html
    assert 'href="../../assets/site.css"' in html


def test_englishize_section_removes_chinese_labels():
    section = """
<div class="eyebrow">纽约尼克斯 · G</div>
<div class="subtitle">Alpha creator · 5 场 · 39.1 MPG · 32.6 PPG</div>
<div class="legend-item">球员</div>
<div class="group-title">队内相对优势</div>
<div class="insight-label">队内得分占比 Team Score Share</div>
<div class="insight-desc">比队内均值 +22.8%。</div>
<div class="summary-box">这张雷达不是常规赛全联盟画像，而是 2026 总决赛这轮系列赛画像。横向基准是“本队均值 + 全系列均值”。生成时间 2026-06-16 12:51:31 CST。</div>
<th>维度</th><th>总决赛总体均值</th><td>真实命中率 TS%</td>
"""

    cleaned = englishize_section(section)

    assert "New York Knicks" in cleaned
    assert "5 Games" in cleaned
    assert "Player" in cleaned
    assert "Team-relative strengths" in cleaned
    assert "Team Score Share" in cleaned
    assert "vs team avg +22.8%." in cleaned
    assert "This radar is a 2026 NBA Finals series view" in cleaned
    assert "Metric" in cleaned
    assert "Finals overall avg" in cleaned
    assert "True Shooting TS%" in cleaned
    assert not any("\u4e00" <= char <= "\u9fff" for char in cleaned)


def test_json_formatter_outputs_required_observability_fields():
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="generated",
        args=(),
        exc_info=None,
    )
    record.trace_id = "trace"
    record.request_id = "request"
    record.user_id = "local"
    record.status_code = "200"
    record.duration_ms = "12.3"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["message"] == "generated"
    assert payload["level"] == "INFO"
    assert payload["service"] == "nba-finals-radar-publishing"
    assert payload["trace_id"] == "trace"
    assert payload["request_id"] == "request"
    assert payload["user_id"] == "local"
    assert payload["status_code"] == "200"
    assert payload["duration_ms"] == "12.3"
    assert "timestamp" in payload
