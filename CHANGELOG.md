# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-11

Initial release. Anvil dependency app that connects Anvil app backends to
mAIvn services from client and server code.

### Added

- Anvil dependency-app scaffold (`server_code/`, `client_code/`, `theme/`)
  merged onto the `maivn_anvil_connector` package path via `__init__.py`.
- Python 3.10 server / Skulpt client compatibility shims (`_py310_compat`).
