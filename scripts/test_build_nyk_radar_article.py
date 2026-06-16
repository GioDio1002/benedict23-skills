from build_nyk_radar_article import sanitize_style


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
