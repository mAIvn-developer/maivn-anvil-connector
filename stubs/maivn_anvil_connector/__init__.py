from __future__ import annotations

import os

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
__path__ = [
    os.path.join(_REPO_ROOT, 'server_code'),
    os.path.join(_REPO_ROOT, 'client_code'),
]
