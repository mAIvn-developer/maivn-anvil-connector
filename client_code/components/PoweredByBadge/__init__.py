# pyright: basic, reportMissingModuleSource=false
"""Small, dismissible 'Powered by mAIvn' badge. Skulpt-safe (no annotations).

Theme-agnostic: it inherits the host app's roles/colors and only adds a subtle
attribution link. Hidden when the chat panel is created with show_badge=False.
"""

from ._anvil_designer import PoweredByBadgeTemplate

_HTML = """
<a class="maivn-powered" href="https://maivn.io" target="_blank" rel="noopener">
  Powered by <strong>mAIvn</strong>
</a>
""".strip()


class PoweredByBadge(PoweredByBadgeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.html = _HTML
