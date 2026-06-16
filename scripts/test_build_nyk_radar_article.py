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
        switch_label="中文",
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
<div class="stat-chip"><strong>32.6</strong><span>场均得分</span></div>
<div class="legend-item">球员</div>
<div class="group-title">队内相对优势</div>
<div class="insight-label">失误率 TOV%</div>
<div class="insight-desc">高于队内均值 2.9%。</div>
<div class="group-title">相对季后赛表现</div>
<div class="delta-item good"><span>正负值 +/- 比季后赛整体好 87.0%</span></div>
<strong>综合评价</strong>
<div class="summary-box">这张雷达对比的是 2026 总决赛表现、本队总决赛均值，以及该球员整个 2025-26 季后赛均值（含总决赛）。灰线可用来判断球员是否在总决赛相对季后赛整体下滑。PIE 是综合指标，和多个单项维度存在包含关系，因此解读时应更多把它当成总览。生成时间 2026-06-16 12:51:31 CST。</div>
<th>维度</th><th>球员季后赛均值（含总决赛）</th><th>定义 / 备注</th><td>正负值 +/-</td><td>每场个人犯规数。它与防守侵略性有关，但更多反映犯规控制，不等于防守质量，数值越低越好。</td>
"""

    cleaned = englishize_section(section)

    assert "New York Knicks" in cleaned
    assert "5 Games" in cleaned
    assert "PPG" in cleaned
    assert "Player" in cleaned
    assert "Team-relative strengths" in cleaned
    assert "Turnover Rate TOV%" in cleaned
    assert "above team avg by 2.9%." in cleaned
    assert "Vs playoff baseline" in cleaned
    assert "87.0% better than full playoffs" in cleaned
    assert "Overall evaluation" in cleaned
    assert "This radar compares 2026 NBA Finals performance" in cleaned
    assert "Metric" in cleaned
    assert "Player playoffs avg (Finals included)" in cleaned
    assert "Definition / note" in cleaned
    assert "Plus/Minus +/-" in cleaned
    assert "Personal fouls committed per game." in cleaned
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
