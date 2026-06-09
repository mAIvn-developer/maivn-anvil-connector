#
# Anvil loads each module under ``server_code/`` directly onto the
# ``maivn_anvil_connector`` package path (see the repo-root ``__init__.py``),
# so this file is not the package initializer and importing symbols here would
# be inert. The public server API is therefore submodule-style, e.g.::
#
#     from maivn_anvil_connector import registry
#     registry.register_agent("support", my_agent)
#
#     from maivn_anvil_connector.interrupts import make_anvil_interrupt_handler
#
# Anvil auto-imports every server module at startup, which is what registers the
# @anvil.server.callable / @anvil.server.background_task entry points.
from __future__ import annotations
