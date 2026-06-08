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
