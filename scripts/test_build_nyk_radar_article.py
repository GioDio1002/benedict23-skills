from build_nyk_radar_article import article_shell, sanitize_style


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
        page_title="T",
        page_headline="H",
        page_intro="I",
        page_no=1,
        total_pages=2,
        body="<div>body</div>",
        local_style="",
        footer_note="custom footer",
    )

    assert "custom footer" in html
