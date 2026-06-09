from __future__ import annotations

from pathlib import Path

_CSS = Path(__file__).resolve().parents[1] / "theme" / "assets" / "theme.css"


def _css() -> str:
    return _CSS.read_text(encoding="utf-8")


def test_brand_primary_tokens_present() -> None:
    text = _css()
    # Light + dark mAIvn primaries from the website token set.
    assert "#476081" in text
    assert "#c3c4df" in text
    assert "--color-secondary: #00677d" in text


def test_dark_theme_block_present() -> None:
    assert 'data-theme="dark"' in _css()


def test_brand_fonts_declared() -> None:
    text = _css()
    for font in ("Manrope", "IBM Plex Mono", "Bricolage Grotesque"):
        assert font in text


def test_component_layer_is_theme_agnostic() -> None:
    # Reusable component classes must use var() with fallbacks so they render
    # acceptably inside a host app that does not define the mAIvn tokens.
    text = _css()
    assert ".maivn-chat" in text
    assert "var(--color-primary," in text  # fallback form: var(--x, <fallback>)
