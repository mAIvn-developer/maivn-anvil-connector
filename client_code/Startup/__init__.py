# pyright: basic, reportMissingModuleSource=false
"""Startup form: applies the mAIvn theme and opens the branded Home.

Skulpt-safe (no annotations/typing). Set as the app ``startup_form`` in
anvil.yaml. Detects the user's preferred color scheme and sets ``data-theme`` so
the mAIvn light/dark tokens apply.
"""

import anvil.js
from anvil import open_form

from ._anvil_designer import StartupTemplate

_THEME_BOOTSTRAP = """
<script>
  (function () {
    var prefersDark = window.matchMedia
      && window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  })();
</script>
""".strip()


class Startup(StartupTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.html = _THEME_BOOTSTRAP
        anvil.js.call_js("eval", _THEME_BOOTSTRAP.replace("<script>", "").replace("</script>", ""))
        open_form("Home")
