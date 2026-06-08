# This repository is an Anvil dependency app. Learn more at https://anvil.works/
# To run server-side code locally with the Anvil App Server, see README.md.

from __future__ import annotations

import os

__path__ = [
    os.path.join(os.path.dirname(__file__), "server_code"),
    os.path.join(os.path.dirname(__file__), "client_code"),
]
