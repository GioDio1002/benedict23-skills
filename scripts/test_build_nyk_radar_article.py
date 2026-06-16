import json
import logging

from build_nyk_radar_article import JsonFormatter, article_shell, sanitize_style


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
        switch_label="中文版",
        switch_href="../../zh/articles/demo/page-1.html",
        all_articles_label="All Articles",
        site_home_label="Site Home",
    )

    assert "custom footer" in html
    assert 'href="../../assets/site.css"' in html


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
