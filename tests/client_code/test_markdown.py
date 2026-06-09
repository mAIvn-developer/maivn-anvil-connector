from __future__ import annotations

from maivn_anvil_connector.markdown import escape_html, render_markdown


def test_escape_html_neutralizes_tags() -> None:
    assert escape_html('<script>&"') == "&lt;script&gt;&amp;&quot;"


def test_render_wraps_paragraphs() -> None:
    html = render_markdown("hello world")
    assert html == "<p>hello world</p>"


def test_render_separates_double_newline_paragraphs() -> None:
    html = render_markdown("one\n\ntwo")
    assert html == "<p>one</p><p>two</p>"


def test_render_fenced_code_block() -> None:
    html = render_markdown("intro\n\n```\nx = 1\n```")
    assert '<pre class="maivn-code"><code>x = 1</code></pre>' in html
    assert "<p>intro</p>" in html


def test_render_escapes_inside_code() -> None:
    html = render_markdown("```\n<b>\n```")
    assert "&lt;b&gt;" in html
