# pyright: basic
"""Minimal, dependency-free markdown rendering for chat bubbles.

Skulpt-safe (no annotations/typing). HTML-escapes everything, then renders
fenced code blocks and paragraphs. `re` is available in the Anvil client.
"""

import re


def escape_html(text):
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def render_markdown(text):
    """Render a safe subset of markdown: fenced code blocks + paragraphs."""
    parts = re.split(r"```(.*?)```", text, flags=re.DOTALL)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(f'<pre class="maivn-code"><code>{escape_html(part.strip())}</code></pre>')
        else:
            for para in filter(None, (p.strip() for p in part.split("\n\n"))):
                out.append(f"<p>{escape_html(para)}</p>")
    return "".join(out)
