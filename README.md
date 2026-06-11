# mAIvn Anvil Connector

Public Anvil dependency app that helps Anvil developers connect app backends to
mAIvn services from client and server code.

This repository is both:

- an **Anvil app** (Git clone target for the Anvil Editor and App Server), and
- a **git submodule** inside the [maivn-apps](https://github.com/mAIvn-developer/maivn-apps)
  monorepo for local development and CI.

## Anvil layout

The repo follows the standard [Anvil app structure](https://anvil.works/docs/workflows/app-architecture/python-directory-structure):

```
maivn-anvil-connector/
├── __init__.py          # merges server_code/ and client_code/ onto the package path
├── anvil.yaml           # package_name: maivn_anvil_connector
├── client_code/         # client-side modules and components
├── server_code/         # server modules (@anvil.server.callable, etc.)
└── theme/               # minimal theme stubs required by Anvil
```

Import from consuming Anvil apps (after adding this app as a dependency):

```python
from maivn_anvil_connector import version
```

## Using the connector

The connector wires your own `maivn.Agent` / `Swarm` (running in your Anvil
server via the SDK) to a streaming chat UI, using **only Anvil-native
infrastructure** (background task + Data Tables + an adaptive client poll). No
browser-to-mAIvn connection and no mAIvn platform changes.

### Prerequisites

- A **paid Anvil plan** — the connector runs each turn in an
  `@anvil.server.background_task`, which requires background tasks.
- The **`maivn` SDK** installed in your app's server packages.
- This app added as a **dependency** in your app's Dependencies.
- Your consuming app must use Anvil's **Python 3.10** server environment
  (the default; see
  [Python versions and packages](https://anvil.works/docs/server/python-versions/packages)).

### Anvil server runtime

Anvil's hosted server uses **Python 3.10** by default, but the **downlink worker**
evaluates every annotation at import time and does not tolerate modern typing
syntax. The connector's `server_code/` modules are therefore **annotation-free**
(the same policy as `client_code/` for Skulpt):

| Constraint | Why |
| --- | --- |
| No type annotations in `server_code/` | Downlink import fails on `list[str]`, `dict[str, Any]`, `str \| None`, subscripted `Callable`, etc. |
| No `from __future__ import annotations` in server modules | Anvil prepends a line to every server module, which breaks future imports. |
| Import `maivn` only after `_py310_compat` (or import the connector package first) | The SDK expects `datetime.UTC` and `typing.Self` (3.11+); the connector backports them in `_py310_compat.py`. |
| Client modules stay annotation-free | The browser runs Skulpt (Python 3.7). |

When adding your own server modules, follow the same annotation-free style or
import `maivn_anvil_connector._py310_compat` before `maivn`.

### 1. Configure the API key

Set an App Secret named `MAIVN_API_KEY` (Anvil → Secrets). The connector reads
it server-side via `maivn_anvil_connector.config.resolve_api_key()`. The key
never reaches the browser.

### 2. Register your agent (server module, at import time)

```python
from maivn import Agent
from maivn_anvil_connector import registry
from maivn_anvil_connector.config import resolve_api_key

agent = Agent(
    name="support",
    description="Customer support assistant",
    system_prompt="You are a helpful support agent.",
    api_key=resolve_api_key(),
)
registry.register_agent("support", agent)
```

Register **at module import time** (top level), not inside a callable: Anvil may
run callables and background tasks on different server instances, so each
instance must rebuild the registry on import.

### 3. Drop in the UI (client form)

```python
from maivn_anvil_connector.components.MaivnChatPanel import MaivnChatPanel

self.add_component(MaivnChatPanel(agent_key="support"))
```

That is the whole integration. `MaivnChatPanel` streams assistant text, shows a
live activity feed (tools, system tools, swarm assignments), handles
attachments, and renders interrupt prompts. Pass `show_badge=False` to hide the
"Powered by mAIvn" badge.

### Interrupts (human-in-the-loop)

Attach `make_anvil_interrupt_handler()` as a tool's `input_handler`. Omit the
session id — the connector binds the active session around each turn:

```python
from maivn import depends_on_interrupt
from maivn_anvil_connector.interrupts import make_anvil_interrupt_handler

@agent.toolify(description="Delete a record after explicit approval")
@depends_on_interrupt(
    arg_name="confirmation",
    input_handler=make_anvil_interrupt_handler(
        input_type="boolean", prompt="Approve deleting this record?"
    ),
)
def delete_record(confirmation: bool) -> dict:
    # Boolean interrupt: Anvil sends "yes"/"no"; the SDK coerces to bool.
    return {"deleted": confirmation}
```

The run pauses, the panel renders the control, and the turn resumes in the same
background task once the user answers.

### Security — full mAIvn `private_data` parity

Every event reaches the client only through a `frontend_safe`
`maivn.events.EventBridge`, which redacts injected `private_data`, merged PII,
and internal error details. Raw SDK events are **never** persisted, so private
data and PII never reach the Data Table or the browser. Your
`@depends_on_private_data` tools work exactly as in any SDK integration.
Sensitive interrupt responses are data-minimized: consumed by the handler and
deleted immediately, never copied into the event log. The connector's Data
Tables are server-only (`client: none`); the client reaches data only through
ownership-checked callables.

### Public API (submodule-style)

```python
from maivn_anvil_connector import registry                  # register_agent / resolve_agent
from maivn_anvil_connector.config import resolve_api_key
from maivn_anvil_connector.interrupts import make_anvil_interrupt_handler
from maivn_anvil_connector.attachments import media_to_attachment
from maivn_anvil_connector.components.MaivnChatPanel import MaivnChatPanel
from maivn_anvil_connector.session import MaivnSession       # advanced: custom client UIs
```

SDK reference docs (agents, tools, swarms, structured output) live at
[developer.maivn.io/docs](https://developer.maivn.io/docs) and are not
duplicated here.

### Showcase / docs app

This repo **is** a runnable, branded Anvil app: its startup form opens a mAIvn-
branded home with in-app Anvil+mAIvn guidance and three runnable examples
(basic chat, an interrupt approval gate, a research swarm). The examples are
usage-capped (per-day message limit, short responses) so demoing does not burn
tokens — see `server_code/limits.py`.

## Local development (monorepo)

From the maivn-apps root:

```powershell
uv sync
uv run pytest libraries/maivn-anvil-connector/tests
uv run ruff check libraries/maivn-anvil-connector
powershell -File scripts/verify.ps1 maivn-anvil-connector
```

Pytest adds the repo root to `PYTHONPATH` so imports match Anvil's runtime layout
without modifying `anvil.yaml`.

## Local Anvil App Server testing

To test inside a consuming Anvil app with the [Anvil App Server](https://github.com/anvil-works/anvil-runtime),
clone this repo **next to** the consuming app (sibling directories), then map the
dependency ID from the consumer's `anvil.yaml` to this directory name.

Example `config.yaml` beside your consuming app (copy from `local/anvil-server.config.yaml.example`):

```yaml
dep-id:
  "<YOUR_DEPENDENCY_APP_ID>": "maivn-anvil-connector"
```

Do **not** commit consumer-specific `config.yaml` files; they are local-only.

## Push workflow

1. Work on a branch inside `libraries/maivn-anvil-connector`.
2. Commit and push to `https://github.com/mAIvn-developer/maivn-anvil-connector.git`.
3. In Anvil, pull the dependency from Git or point your test app at the branch.
4. Bump the submodule pointer in maivn-apps when ready.

## License

Apache License 2.0. See [LICENSE](LICENSE).
